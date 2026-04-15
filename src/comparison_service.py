from __future__ import annotations

import multiprocessing as mp
import queue
import random
import shutil
import threading
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from .models import EngineResult, HyperParameters, SessionEvent
from .sklearn_mlp import SklearnMLPEngine
from .utils import load_numeric_dataset, split_dataset
from .weka_mlp import execute_weka_mlp, write_split_to_arff

ENGINE_NAMES = {
    "custom": "Custom mlp.py",
    "sklearn": "Scikit-Learn",
    "weka": "Weka",
}
CONTROL_KEY = "__session__"
SRC_DIR = Path(__file__).resolve().parent
BLACK_BOX_MLP_PATH = SRC_DIR / "mlp.py"
SOURCE_SPLIT_MARKER = "# MÓDULO PRINCIPAL"


def create_comparison_state(
    dataset_path: str | Path,
    weka_jar_path: str | Path | None = None,
) -> dict:
    return {
        "dataset_path": Path(dataset_path),
        "weka_jar_path": Path(weka_jar_path) if weka_jar_path else Path("bin/weka.jar"),
        "result_queue": queue.Queue(),
        "mp_context": mp.get_context("spawn"),
        "mp_queue": None,
        "collector_thread": None,
        "processes": {},
        "cancel_requested": threading.Event(),
        "active": False,
        "temp_dir_handle": None,
        "temp_dir": None,
        "lock": threading.Lock(),
    }


def start_comparison(state: dict, params: HyperParameters) -> None:
    with state["lock"]:
        if state["active"]:
            raise RuntimeError("A comparison is already running.")
        state["result_queue"] = queue.Queue()
        state["cancel_requested"].clear()
        state["processes"] = {}
        state["mp_queue"] = state["mp_context"].Queue()
        state["active"] = True

    try:
        features, labels = load_numeric_dataset(state["dataset_path"])
        split = split_dataset(features, labels, params)
        state["temp_dir_handle"] = TemporaryDirectory(prefix="weka_arff_")
        state["temp_dir"] = Path(state["temp_dir_handle"].name)

        train_arff = write_split_to_arff(
            split.x_train,
            split.y_train,
            state["temp_dir"] / "train.arff",
            relation_name="train_split",
        )
        test_arff = write_split_to_arff(
            split.x_test,
            split.y_test,
            state["temp_dir"] / "test.arff",
            relation_name="test_split",
        )

        workers = {
            "custom": state["mp_context"].Process(
                target=_run_custom_worker,
                args=(state["mp_queue"], split.x_train, split.y_train, split.x_test, split.y_test, params),
            ),
            "sklearn": state["mp_context"].Process(
                target=_run_sklearn_worker,
                args=(state["mp_queue"], split.x_train, split.y_train, split.x_test, split.y_test, params),
            ),
            "weka": state["mp_context"].Process(
                target=_run_weka_worker,
                args=(state["mp_queue"], train_arff, test_arff, params, state["weka_jar_path"]),
            ),
        }

        state["processes"] = workers
        for process in workers.values():
            process.daemon = True
            process.start()

        state["collector_thread"] = threading.Thread(
            target=_collect_results,
            args=(state,),
            daemon=True,
        )
        state["collector_thread"].start()
    except Exception as exc:
        state["active"] = False
        _cleanup_temp_dir(state)
        for engine_key in ENGINE_NAMES:
            state["result_queue"].put((engine_key, _build_failure_result(engine_key, str(exc))))
        state["result_queue"].put(
            (
                CONTROL_KEY,
                SessionEvent(
                    event_type="session",
                    status="failed",
                    message=str(exc),
                ),
            )
        )


def cancel_comparison(state: dict) -> None:
    with state["lock"]:
        if not state["active"]:
            return
        state["cancel_requested"].set()
        for process in state["processes"].values():
            if process.is_alive():
                process.terminate()


def _build_failure_result(engine_key: str, message: str) -> EngineResult:
    return EngineResult(
        engine_name=ENGINE_NAMES[engine_key],
        status="failed",
        note=message,
    )


def _run_custom_worker(result_queue, x_train, y_train, x_test, y_test, params) -> None:
    try:
        result = run_custom_mlp(x_train, y_train, x_test, y_test, params)
    except Exception as exc:  # pragma: no cover
        result = _build_failure_result("custom", str(exc))
    result_queue.put(("custom", result))


def _run_sklearn_worker(result_queue, x_train, y_train, x_test, y_test, params) -> None:
    try:
        result = SklearnMLPEngine().run(x_train, y_train, x_test, y_test, params)
    except Exception as exc:  # pragma: no cover
        result = _build_failure_result("sklearn", str(exc))
    result_queue.put(("sklearn", result))


def _run_weka_worker(result_queue, train_arff_path, test_arff_path, params, weka_jar_path) -> None:
    try:
        result = execute_weka_mlp(train_arff_path, test_arff_path, params, weka_jar_path)
    except Exception as exc:  # pragma: no cover
        result = _build_failure_result("weka", str(exc))
    result_queue.put(("weka", result))


def _collect_results(state: dict) -> None:
    delivered: set[str] = set()
    session_status = "completed"
    session_message = "Comparison completed."

    try:
        while len(delivered) < len(ENGINE_NAMES):
            if state["cancel_requested"].is_set():
                session_status = "cancelled"
                session_message = "Comparison cancelled."
                break

            try:
                engine_key, result = state["mp_queue"].get(timeout=0.2)
            except queue.Empty:
                if all(not process.is_alive() for process in state["processes"].values()):
                    break
                continue
            except (EOFError, OSError) as exc:
                session_status = "failed"
                session_message = f"Result collection failed: {exc}"
                break

            if engine_key in delivered:
                continue

            delivered.add(engine_key)
            state["result_queue"].put((engine_key, result))

        if state["cancel_requested"].is_set():
            _emit_missing_results(state, delivered, status="cancelled", note="Execution cancelled by user.")
        elif len(delivered) < len(ENGINE_NAMES):
            session_status = "failed"
            session_message = "Comparison ended before all engines returned results."
            _emit_missing_results(
                state,
                delivered,
                status="failed",
                note="Worker did not return a result before the session ended.",
            )
    except Exception as exc:  # pragma: no cover
        session_status = "failed"
        session_message = str(exc)
        _emit_missing_results(state, delivered, status="failed", note=f"Collector failed: {exc}")
    finally:
        for engine_key in list(state["processes"]):
            process = state["processes"][engine_key]
            if process.is_alive():
                process.terminate()
            process.join(timeout=0.2)

        if state["mp_queue"] is not None:
            state["mp_queue"].close()
            state["mp_queue"].join_thread()

        _cleanup_temp_dir(state)

        with state["lock"]:
            state["active"] = False

        state["result_queue"].put(
            (
                CONTROL_KEY,
                SessionEvent(
                    event_type="session",
                    status=session_status,
                    message=session_message,
                ),
            )
        )


def _emit_missing_results(state: dict, delivered: set[str], status: str, note: str) -> None:
    for engine_key in ENGINE_NAMES:
        if engine_key in delivered:
            continue
        state["result_queue"].put(
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


def _cleanup_temp_dir(state: dict) -> None:
    if state["temp_dir_handle"] is not None:
        state["temp_dir_handle"].cleanup()
    elif state["temp_dir"] and state["temp_dir"].exists():
        shutil.rmtree(state["temp_dir"], ignore_errors=True)
    state["temp_dir_handle"] = None
    state["temp_dir"] = None


def _load_black_box_namespace() -> dict[str, object]:
    source = BLACK_BOX_MLP_PATH.read_text(encoding="utf-8")
    executable_source = source.split(SOURCE_SPLIT_MARKER, maxsplit=1)[0]
    namespace: dict[str, object] = {}
    exec(compile(executable_source, str(BLACK_BOX_MLP_PATH), "exec"), namespace)
    return namespace


def run_custom_mlp(x_train, y_train, x_test, y_test, params: HyperParameters) -> EngineResult:
    namespace = _load_black_box_namespace()
    mlp_treino = namespace["mlp_treino"]
    mlp_teste = namespace["mlp_teste"]

    np.random.seed(params.random_seed)
    random.seed(params.random_seed)

    num_inputs = x_train.shape[1]
    num_outputs = int(max(np.max(y_train), np.max(y_test))) + 1

    start_time = time.perf_counter()
    weights_v, weights_w = mlp_treino(
        num_inputs,
        params.hidden_neurons,
        num_outputs,
        params.epochs,
        x_train.tolist(),
        y_train.tolist(),
        params.learning_rate,
        params.hidden_activation.lower(),
        params.output_activation.lower(),
    )
    elapsed = time.perf_counter() - start_time

    accuracy = mlp_teste(
        num_inputs,
        params.hidden_neurons,
        num_outputs,
        len(x_test),
        x_test.tolist(),
        y_test.tolist(),
        weights_v,
        weights_w,
        params.hidden_activation.lower(),
        params.output_activation.lower(),
    )

    return EngineResult(
        engine_name="Custom mlp.py",
        accuracy=float(accuracy),
        training_time=float(elapsed),
        status="completed",
        note=(
            f"Custom hidden={params.hidden_activation.lower()} "
            f"output={params.output_activation.lower()} "
            f"lr={params.learning_rate}."
        ),
    )
