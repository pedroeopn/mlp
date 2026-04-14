from __future__ import annotations

import random
import time
from pathlib import Path

import numpy as np

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
        self.mlp_treino = self.namespace["mlp_treino"]
        self.mlp_teste = self.namespace["mlp_teste"]

    def run(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_test: np.ndarray,
        y_test: np.ndarray,
        params: HyperParameters,
    ) -> EngineResult:
        result = EngineResult(engine_name="Custom mlp.py", status="running")
        note_parts = [
            f"Custom hidden={params.hidden_activation.lower()} output={params.output_activation.lower()} lr={params.learning_rate}.",
        ]

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
            params.learning_rate,
            params.hidden_activation.lower(),
            params.output_activation.lower(),
        )
        elapsed = time.perf_counter() - start_time

        accuracy = self.mlp_teste(
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

        result.accuracy = float(accuracy)
        result.training_time = float(elapsed)
        result.status = "completed"
        result.note = " ".join(note_parts)
        return result
