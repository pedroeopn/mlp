from __future__ import annotations

import time
import warnings

from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.neural_network import MLPClassifier

from .schemas import EngineResult, HyperParameters

SKLEARN_ACTIVATIONS = {
    "relu": "relu",
    "sigmoid": "logistic",
    "logistic": "logistic",
    "tanh": "tanh",
}


def run_sklearn_mlp(
    x_train,
    y_train,
    x_test,
    y_test,
    params: HyperParameters,
) -> EngineResult:
    requested_activation = params.hidden_activation.lower()
    sklearn_activation = SKLEARN_ACTIVATIONS.get(requested_activation, "relu")

    classifier = MLPClassifier(
        hidden_layer_sizes=(params.hidden_neurons,),
        activation=sklearn_activation,
        learning_rate_init=params.learning_rate,
        max_iter=params.epochs,
        random_state=params.random_seed,
        solver="adam",
        early_stopping=True,
        n_iter_no_change=20,
    )

    start_time = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always", ConvergenceWarning)
        classifier.fit(x_train, y_train) # treinando o modelo
    elapsed = time.perf_counter() - start_time
    predictions = classifier.predict(x_test) # testando o modelo
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    result = EngineResult(
        engine_name="Scikit-Learn",
        accuracy=float(accuracy_score(y_test, predictions) * 100.0), # no specification, binary class
        precision=float(precision * 100.0),
        recall=float(recall * 100.0),
        f1_score=float(f1_score * 100.0),
        training_time=float(elapsed),
        status="completed",
        extra={"iterations": str(classifier.n_iter_)},
    )

    notes: list[str] = ["Metrics from Scikit-Learn."]
    if requested_activation not in SKLEARN_ACTIVATIONS:
        notes.append(f"Unsupported hidden activation '{params.hidden_activation}' mapped to ReLU.")
    if caught_warnings:
        notes.append(str(caught_warnings[-1].message))

    result.note = " ".join(notes)
    return result
