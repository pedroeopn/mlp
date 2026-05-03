from __future__ import annotations

import random
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from .schemas import EngineResult, HyperParameters

SRC_DIR = Path(__file__).resolve().parent
BLACK_BOX_MLP_PATH = SRC_DIR / "mlp.py"
SOURCE_SPLIT_MARKER = "# MÓDULO PRINCIPAL"


def _load_black_box_namespace() -> dict[str, object]:
    source = BLACK_BOX_MLP_PATH.read_text(encoding="utf-8")
    executable_source = source.split(SOURCE_SPLIT_MARKER, maxsplit=1)[0]
    namespace: dict[str, object] = {}
    exec(compile(executable_source, str(BLACK_BOX_MLP_PATH), "exec"), namespace)
    return namespace


def _custom_mlp_forward(
    sample,
    nx: int,
    nz: int,
    ny: int,
    weights_v,
    weights_w,
    namespace: dict[str, object],
    hidden_activation: str,
    output_activation: str,
):
    x = np.zeros(nx + 1, float)
    z = np.zeros(nz + 1, float)
    y = np.zeros(ny, float)

    sigmoid = namespace["sigmoide"]
    relu = namespace["relu"]
    softmax = namespace["softmax"]

    for i in range(nx):
        x[i] = sample[i]
    x[nx - 1] = 1

    for j in range(nz):
        for i in range(nx + 1):
            z[j] += weights_v[i][j] * x[i]
        if hidden_activation == "sigmoid":
            z[j] = sigmoid(z[j])
        else:
            z[j] = relu(z[j])

    z[nz - 1] = 1

    if output_activation == "sigmoid":
        for k in range(ny):
            for j in range(nz + 1):
                y[k] += weights_w[j][k] * z[j]
            y[k] = sigmoid(y[k])
        return y

    logits = np.zeros(ny)
    for k in range(ny):
        for j in range(nz + 1):
            logits[k] += weights_w[j][k] * z[j]
    return softmax(logits)


def _custom_mlp_predict(
    x_test,
    nx: int,
    nz: int,
    ny: int,
    weights_v,
    weights_w,
    namespace: dict[str, object],
    hidden_activation: str,
    output_activation: str,
):
    predictions: list[int] = []
    for sample in x_test:
        output = _custom_mlp_forward(
            sample,
            nx,
            nz,
            ny,
            weights_v,
            weights_w,
            namespace,
            hidden_activation,
            output_activation,
        )
        if output_activation == "sigmoid":
            if ny == 1:
                prediction = 1 if output[0] >= 0.5 else 0
            else:
                prediction = int(np.argmax(output >= 0.5))
        else:
            prediction = int(np.argmax(output))
        predictions.append(prediction)
    return predictions


def run_custom_mlp(x_train, y_train, x_test, y_test, params: HyperParameters) -> EngineResult:
    namespace = _load_black_box_namespace()
    mlp_treino = namespace["mlp_treino"]
    calcular_acuracia = namespace["calcular_acuracia"]

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

    predictions = _custom_mlp_predict(
        x_test.tolist(),
        num_inputs,
        params.hidden_neurons,
        num_outputs,
        weights_v,
        weights_w,
        namespace,
        params.hidden_activation.lower(),
        params.output_activation.lower(),
    )
    matrix = confusion_matrix(y_test, predictions, labels=[1, 0])

    return EngineResult(
        engine_name="Custom mlp.py",
        accuracy=float(calcular_acuracia(y_test.tolist(), predictions)),
        precision=float(precision_score(y_test, predictions, average="binary", zero_division=0) * 100.0),
        recall=float(recall_score(y_test, predictions, average="binary", zero_division=0) * 100.0),
        f1_score=float(f1_score(y_test, predictions, average="binary", zero_division=0) * 100.0),
        training_time=float(elapsed),
        status="completed",
        note=(
            f"hidden={params.hidden_activation.lower()} output={params.output_activation.lower()} "
            f"lr={params.learning_rate}. Accuracy from mlp.py; precision, recall, F1, "
            "and confusion matrix from Scikit-Learn using binary average. "
            "Confusion matrix layout: [[VP, FN], [FP, VN]]."
        ),
        extra={
            "confusion_matrix": np.array2string(matrix, separator=", "),
        },
    )
