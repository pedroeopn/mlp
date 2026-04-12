from __future__ import annotations

import random
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from .models import EngineResult, HyperParameters

ROOT_DIR = Path(__file__).resolve().parents[2]
BLACK_BOX_MLP_PATH = ROOT_DIR / "src" / "core" / "mlp.py"
SOURCE_SPLIT_MARKER = "# MÓDULO PRINCIPAL"


def _load_black_box_namespace() -> dict[str, object]:
    source = BLACK_BOX_MLP_PATH.read_text(encoding="utf-8")
    executable_source = source.split(SOURCE_SPLIT_MARKER, maxsplit=1)[0]
    namespace: dict[str, object] = {}
    exec(compile(executable_source, str(BLACK_BOX_MLP_PATH), "exec"), namespace)
    return namespace


class CustomMLPEngine:
    def __init__(self) -> None:
        self.namespace = _load_black_box_namespace()
        self.relu = self.namespace["relu"]
        self.softmax = self.namespace["softmax"]
        self.mlp_treino = self.namespace["mlp_treino"]

    def run(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_test: np.ndarray,
        y_test: np.ndarray,
        params: HyperParameters,
    ) -> EngineResult:
        result = EngineResult(engine_name="Custom mlp.py", status="running")
        note_parts: list[str] = []

        if params.learning_rate != 0.01:
            note_parts.append("The preserved black-box mlp.py uses a fixed learning rate of 0.01.")

        if params.activation_function.lower() != "relu":
            note_parts.append(
                "The preserved black-box mlp.py uses ReLU/Softmax internally."
            )

        np.random.seed(params.random_seed)
        random.seed(params.random_seed)

        num_inputs = x_train.shape[1]
        num_outputs = int(max(np.max(y_train), np.max(y_test))) + 1

        start_time = time.perf_counter()
        weights_v, weights_w = self.mlp_treino(
            num_inputs,
            params.hidden_neurons,
            num_outputs,
            params.epochs,
            x_train.tolist(),
            y_train.tolist(),
        )
        elapsed = time.perf_counter() - start_time

        predictions = np.asarray(
            [
                self._predict_row(
                    row=row,
                    num_inputs=num_inputs,
                    num_hidden=params.hidden_neurons,
                    num_outputs=num_outputs,
                    weights_v=weights_v,
                    weights_w=weights_w,
                )
                for row in x_test
            ],
            dtype=int,
        )

        result.accuracy = float(accuracy_score(y_test, predictions) * 100.0)
        result.f1_score = float(
            f1_score(y_test, predictions, average="weighted", zero_division=0)
        )
        result.training_time = float(elapsed)
        result.status = "completed"
        result.note = " ".join(note_parts)
        return result

    def _predict_row(
        self,
        row: np.ndarray,
        num_inputs: int,
        num_hidden: int,
        num_outputs: int,
        weights_v: np.ndarray,
        weights_w: np.ndarray,
    ) -> int:
        x = np.zeros(num_inputs + 1, dtype=float)
        z = np.zeros(num_hidden + 1, dtype=float)

        for index in range(num_inputs):
            x[index] = row[index]
        x[num_inputs - 1] = 1

        for hidden_index in range(num_hidden):
            activation_input = 0.0
            for input_index in range(num_inputs + 1):
                activation_input += weights_v[input_index][hidden_index] * x[input_index]
            z[hidden_index] = self.relu(activation_input)
        z[num_hidden - 1] = 1

        output_input = np.zeros(num_outputs, dtype=float)
        for output_index in range(num_outputs):
            for hidden_index in range(num_hidden + 1):
                output_input[output_index] += (
                    weights_w[hidden_index][output_index] * z[hidden_index]
                )

        scores = self.softmax(output_input)
        return int(np.argmax(scores))
