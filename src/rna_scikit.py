from __future__ import annotations

import time
import warnings
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

from src.schemas import DEFAULT_HYPERPARAMETERS, EngineResult, HyperParameters
from src.utils import load_raw_numeric_dataset


def run_sklearn_mlp(
    dataset_path: str | Path,
    params: HyperParameters = DEFAULT_HYPERPARAMETERS,
    train_equals_test: bool = False,
) -> EngineResult:
    # Carregando os dados do arquivo
    x, y = load_raw_numeric_dataset(dataset_path)

    # Normalizando as características (MinMax)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(x)

    # Dividindo os dados em treino (80%) e teste (20%)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=params.test_size,
        random_state=params.random_seed,
    )

    # Parâmetros da RNA
    t_max = params.epochs
    alfa = params.learning_rate
    momento = params.momentum
    qn1 = params.hidden_neurons
    qn2 = params.second_hidden_neurons
    f_ati = params.hidden_activation

    # Configurando o MLPClassifier
    mlp = MLPClassifier(
        hidden_layer_sizes=(qn1, qn2),
        activation=f_ati,
        solver="sgd",
        learning_rate_init=alfa,
        momentum=momento,
        max_iter=t_max,
        random_state=params.random_seed,
    )

    if train_equals_test:
        train_x, train_y = x, y
        eval_x, eval_y = x, y
        mode = "TREINO = TESTE"
    else:
        train_x, train_y = x_train, y_train
        eval_x, eval_y = x_test, y_test
        mode = "TREINO != TESTE"

    start_time = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always", ConvergenceWarning)
        mlp.fit(train_x, train_y)
    elapsed = time.perf_counter() - start_time

    # Avaliando o modelo
    y_pred = mlp.predict(eval_x)

    # Gerando as métricas
    ac = accuracy_score(eval_y, y_pred)
    pr = precision_score(eval_y, y_pred, average="macro", zero_division=0)
    re = recall_score(eval_y, y_pred, average="macro", zero_division=0)
    f1 = f1_score(eval_y, y_pred, average="macro", zero_division=0)
    m = confusion_matrix(eval_y, y_pred, labels=[1, 0])

    result = EngineResult(
        engine_name="Scikit-Learn",
        accuracy=float(ac * 100.0),
        precision=float(pr * 100.0),
        recall=float(re * 100.0),
        f1_score=float(f1 * 100.0),
        training_time=float(elapsed),
        status="completed",
        extra={
            "confusion_matrix": np.array2string(m, separator=", "),
            "iterations": str(mlp.n_iter_),
            "mode": mode,
        },
        note=(
            "rna_scikit.py: MinMaxScaler(-1, 1), MLPClassifier(solver=sgd, "
            f"momentum={momento}), macro metrics. "
            "Confusion matrix layout: [[VP, FN], [FP, VN]]."
        ),
    )

    if caught_warnings:
        result.note = f"{result.note} {caught_warnings[-1].message}"

    return result


def print_result(result: EngineResult) -> None:
    print(f"\n*** {result.extra.get('mode', 'TREINO != TESTE')} ***")
    print(f"Acurácia...........: {result.accuracy:.2f}%")
    print(f"Precisão...........: {result.precision:.2f}%")
    print(f"Recall.............: {result.recall:.2f}%")
    print(f"F1-measure.........: {result.f1_score:.2f}%")
    print("Matriz de Confusão:\n", result.extra["confusion_matrix"])


def main() -> int:
    dataset_path = Path(__file__).resolve().parents[1] / "data" / "dados.data-numeric"
    result = run_sklearn_mlp(dataset_path)
    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
