from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np

from .models import EngineResult, HyperParameters

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WEKA_JAR = ROOT_DIR / "bin" / "weka.jar"


def convert_numeric_to_arff(
    source_path: str | Path,
    target_path: str | Path,
    relation_name: str = "numeric_dataset",
) -> Path:
    rows = np.loadtxt(source_path, dtype=float)
    if rows.ndim == 1:
        rows = rows.reshape(1, -1)

    features = rows[:, :-1]
    labels = rows[:, -1].astype(int)
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    _write_arff(features, labels, target, relation_name)
    return target


def execute_weka_mlp(
    train_arff_path: str | Path,
    test_arff_path: str | Path,
    params: HyperParameters,
    weka_jar_path: str | Path = DEFAULT_WEKA_JAR,
) -> EngineResult:
    java_executable = shutil.which("java")
    if not java_executable:
        return EngineResult(
            engine_name="Weka",
            status="failed",
            note="Java Runtime Environment not found in PATH.",
        )

    jar_path = Path(weka_jar_path)
    if not jar_path.exists():
        return EngineResult(
            engine_name="Weka",
            status="failed",
            note=f"Weka jar not found at {jar_path}.",
        )

    command = [
        java_executable,
        "-cp",
        str(jar_path),
        "weka.classifiers.functions.MultilayerPerceptron",
        "-t",
        str(train_arff_path),
        "-T",
        str(test_arff_path),
        "-L",
        str(params.learning_rate),
        "-H",
        str(params.hidden_neurons),
        "-N",
        str(params.epochs),
        "-S",
        str(params.random_seed),
    ]

    start_time = time.perf_counter()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed = time.perf_counter() - start_time

    raw_output = f"{completed.stdout}\n{completed.stderr}".strip()

    if completed.returncode != 0:
        return EngineResult(
            engine_name="Weka",
            status="failed",
            training_time=float(elapsed),
            note="Weka CLI execution failed.",
            raw_output=raw_output,
        )

    parsed = parse_weka_output(raw_output)
    return EngineResult(
        engine_name="Weka",
        accuracy=parsed.get("accuracy"),
        training_time=parsed.get("training_time", float(elapsed)),
        status="completed" if parsed.get("accuracy") is not None else "failed",
        note="",
        raw_output=raw_output,
    )


def parse_weka_output(output_text: str) -> dict[str, float]:
    parsed: dict[str, float] = {}

    accuracy_matches = re.findall(
        r"Correctly Classified Instances\s+\d+\s+([\d.,]+)\s*%",
        output_text,
    )
    if accuracy_matches:
        parsed["accuracy"] = _parse_weka_number(accuracy_matches[-1])

    training_time_match = re.search(
        r"Time taken to build model:\s*([\d.,]+)\s*seconds",
        output_text,
    )
    if training_time_match:
        parsed["training_time"] = _parse_weka_number(training_time_match.group(1))

    return parsed


def _parse_weka_number(value: str) -> float:
    return float(value.replace(",", "."))


def write_split_to_arff(
    x_data: np.ndarray,
    y_data: np.ndarray,
    target_path: str | Path,
    relation_name: str,
) -> Path:
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_arff(x_data, y_data, target, relation_name)
    return target


def _write_arff(
    x_data: np.ndarray,
    y_data: np.ndarray,
    target_path: Path,
    relation_name: str,
) -> None:
    class_values = sorted({str(int(label)) for label in y_data.tolist()})

    lines = [f"@RELATION {relation_name}", ""]
    for column_index in range(x_data.shape[1]):
        lines.append(f"@ATTRIBUTE feature_{column_index + 1} NUMERIC")
    lines.append(f"@ATTRIBUTE class {{{','.join(class_values)}}}")
    lines.append("")
    lines.append("@DATA")

    for row, label in zip(x_data, y_data):
        row_values = ",".join(f"{value:.10f}" for value in row.tolist())
        lines.append(f"{row_values},{int(label)}")

    target_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
