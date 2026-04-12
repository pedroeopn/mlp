from __future__ import annotations

import time
import warnings

from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neural_network import MLPClassifier

from .models import EngineResult, HyperParameters

SKLEARN_ACTIVATIONS = {
    "relu": "relu",
    "sigmoid": "logistic",
    "logistic": "logistic",
    "tanh": "tanh",
}


class SklearnMLPEngine:
    def run(
        self,
        x_train,
        y_train,
        x_test,
        y_test,
        params: HyperParameters,
    ) -> EngineResult:
        requested_activation = params.activation_function.lower()
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
            classifier.fit(x_train, y_train)
        elapsed = time.perf_counter() - start_time
        predictions = classifier.predict(x_test)

        result = EngineResult(
            engine_name="Scikit-Learn",
            accuracy=float(accuracy_score(y_test, predictions) * 100.0),
            f1_score=float(
                f1_score(y_test, predictions, average="weighted", zero_division=0)
            ),
            training_time=float(elapsed),
            status="completed",
            extra={"iterations": str(classifier.n_iter_)},
        )

        if requested_activation not in SKLEARN_ACTIVATIONS:
            result.note = f"Unsupported activation '{params.activation_function}' mapped to ReLU."
        elif caught_warnings:
            result.note = str(caught_warnings[-1].message)

        return result
