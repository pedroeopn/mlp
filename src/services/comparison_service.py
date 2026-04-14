from __future__ import annotations

import multiprocessing as mp
import queue
import shutil
import threading
from pathlib import Path
from tempfile import mkdtemp

from src.core.custom_mlp import CustomMLPEngine
from src.core.dataset_utils import load_numeric_dataset, split_dataset
from src.core.lib_mlp import SklearnMLPEngine
from src.core.models import EngineResult, HyperParameters, SessionEvent
from src.core.weka_mlp import execute_weka_mlp, write_split_to_arff

ENGINE_NAMES = {
    "custom": "Custom mlp.py",
    "sklearn": "Scikit-Learn",
    "weka": "Weka",
}
CONTROL_KEY = "__session__"


def _build_failure_result(engine_key: str, message: str) -> EngineResult:
    return EngineResult(
        engine_name=ENGINE_NAMES[engine_key],
        status="failed",
        note=message,
    )


def _run_custom_worker(result_queue, x_train, y_train, x_test, y_test, params) -> None:
    try:
        result = CustomMLPEngine().run(x_train, y_train, x_test, y_test, params)
    except Exception as exc:  # pragma: no cover - process safety
        result = _build_failure_result("custom", str(exc))
    result_queue.put(("custom", result))


def _run_sklearn_worker(result_queue, x_train, y_train, x_test, y_test, params) -> None:
    try:
        result = SklearnMLPEngine().run(x_train, y_train, x_test, y_test, params)
    except Exception as exc:  # pragma: no cover - process safety
        result = _build_failure_result("sklearn", str(exc))
    result_queue.put(("sklearn", result))


def _run_weka_worker(result_queue, train_arff_path, test_arff_path, params, weka_jar_path) -> None:
    try:
        result = execute_weka_mlp(train_arff_path, test_arff_path, params, weka_jar_path)
    except Exception as exc:  # pragma: no cover - process safety
        result = _build_failure_result("weka", str(exc))
    result_queue.put(("weka", result))


class ComparisonService:
    def __init__(self, dataset_path: str | Path, weka_jar_path: str | Path | None = None):
        self.dataset_path = Path(dataset_path)
        self.weka_jar_path = Path(weka_jar_path) if weka_jar_path else Path("bin/weka.jar")
        self.result_queue: queue.Queue[tuple[str, EngineResult | SessionEvent]] = queue.Queue()
        self._mp_context = mp.get_context("spawn")
        self._mp_queue = None
        self._collector_thread: threading.Thread | None = None
        self._processes: dict[str, mp.Process] = {}
        self._cancel_requested = threading.Event()
        self._active = False
        self._temp_dir: Path | None = None
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._active

    def start(self, params: HyperParameters) -> None:
        with self._lock:
            if self._active:
                raise RuntimeError("A comparison is already running.")
            self.result_queue = queue.Queue()
            self._cancel_requested.clear()
            self._processes = {}
            self._mp_queue = self._mp_context.Queue()
            self._active = True

        try:
            features, labels = load_numeric_dataset(self.dataset_path)
            split = split_dataset(features, labels, params)
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            self._temp_dir = Path(mkdtemp(prefix="weka_arff_", dir=str(data_dir)))

            train_arff = write_split_to_arff(
                split.x_train,
                split.y_train,
                self._temp_dir / "train.arff",
                relation_name="train_split",
            )
            test_arff = write_split_to_arff(
                split.x_test,
                split.y_test,
                self._temp_dir / "test.arff",
                relation_name="test_split",
            )

            workers = {
                "custom": self._mp_context.Process(
                    target=_run_custom_worker,
                    args=(self._mp_queue, split.x_train, split.y_train, split.x_test, split.y_test, params),
                ),
                "sklearn": self._mp_context.Process(
                    target=_run_sklearn_worker,
                    args=(self._mp_queue, split.x_train, split.y_train, split.x_test, split.y_test, params),
                ),
                "weka": self._mp_context.Process(
                    target=_run_weka_worker,
                    args=(self._mp_queue, train_arff, test_arff, params, self.weka_jar_path),
                ),
            }

            self._processes = workers
            for process in workers.values():
                process.daemon = True
                process.start()

            self._collector_thread = threading.Thread(
                target=self._collect_results,
                daemon=True,
            )
            self._collector_thread.start()
        except Exception as exc:
            self._active = False
            self._cleanup_temp_dir()
            for engine_key in ENGINE_NAMES:
                self.result_queue.put((engine_key, _build_failure_result(engine_key, str(exc))))
            self.result_queue.put(
                (
                    CONTROL_KEY,
                    SessionEvent(
                        event_type="session",
                        status="failed",
                        message=str(exc),
                    ),
                )
            )

    def cancel(self) -> None:
        with self._lock:
            if not self._active:
                return
            self._cancel_requested.set()
            for process in self._processes.values():
                if process.is_alive():
                    process.terminate()

    def _collect_results(self) -> None:
        delivered: set[str] = set()
        session_status = "completed"
        session_message = "Comparison completed."

        try:
            while len(delivered) < len(ENGINE_NAMES):
                if self._cancel_requested.is_set():
                    session_status = "cancelled"
                    session_message = "Comparison cancelled."
                    break

                try:
                    engine_key, result = self._mp_queue.get(timeout=0.2)
                except queue.Empty:
                    if all(not process.is_alive() for process in self._processes.values()):
                        break
                    continue
                except (EOFError, OSError) as exc:
                    session_status = "failed"
                    session_message = f"Result collection failed: {exc}"
                    break

                if engine_key in delivered:
                    continue

                delivered.add(engine_key)
                self.result_queue.put((engine_key, result))

            if self._cancel_requested.is_set():
                session_status = "cancelled"
                session_message = "Comparison cancelled."
                self._emit_missing_results(delivered, status="cancelled", note="Execution cancelled by user.")
            else:
                if len(delivered) < len(ENGINE_NAMES):
                    session_status = "failed"
                    session_message = "Comparison ended before all engines returned results."
                    self._emit_missing_results(
                        delivered,
                        status="failed",
                        note="Worker did not return a result before the session ended.",
                    )
        except Exception as exc:  # pragma: no cover - collector safety
            session_status = "failed"
            session_message = str(exc)
            self._emit_missing_results(
                delivered,
                status="failed",
                note=f"Collector failed: {exc}",
            )
        finally:
            for engine_key in list(self._processes):
                process = self._processes[engine_key]
                if process.is_alive():
                    process.terminate()
                process.join(timeout=0.2)

            if self._mp_queue is not None:
                self._mp_queue.close()
                self._mp_queue.join_thread()

            self._cleanup_temp_dir()

            with self._lock:
                self._active = False

            self.result_queue.put(
                (
                    CONTROL_KEY,
                    SessionEvent(
                        event_type="session",
                        status=session_status,
                        message=session_message,
                    ),
                )
            )

    def _emit_missing_results(self, delivered: set[str], status: str, note: str) -> None:
        for engine_key in ENGINE_NAMES:
            if engine_key in delivered:
                continue

            self.result_queue.put(
                (
                    engine_key,
                    EngineResult(
                        engine_name=ENGINE_NAMES[engine_key],
                        status=status,
                        note=note,
                    ),
                )
            )
            delivered.add(engine_key)

    def _cleanup_temp_dir(self) -> None:
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
        self._temp_dir = None
