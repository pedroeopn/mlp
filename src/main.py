from __future__ import annotations

import argparse
from pathlib import Path

from src.comparison_service import run_custom_mlp
from src.rna_scikit import run_sklearn_mlp
from src.schemas import DEFAULT_HYPERPARAMETERS, EngineResult, HyperParameters
from src.utils import load_numeric_dataset, split_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare the custom MLP with Scikit-Learn MLP.")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "dados.data-numeric",
        help="Path to the numeric dataset.",
    )
    parser.add_argument("--learning-rate", type=float, default=DEFAULT_HYPERPARAMETERS.learning_rate)
    parser.add_argument("--hidden-neurons", type=int, default=DEFAULT_HYPERPARAMETERS.hidden_neurons)
    parser.add_argument("--second-hidden-neurons", type=int, default=DEFAULT_HYPERPARAMETERS.second_hidden_neurons)
    parser.add_argument("--epochs", type=int, default=DEFAULT_HYPERPARAMETERS.epochs)
    parser.add_argument("--hidden-activation", default=DEFAULT_HYPERPARAMETERS.hidden_activation)
    parser.add_argument("--output-activation", default=DEFAULT_HYPERPARAMETERS.output_activation)
    parser.add_argument("--momentum", type=float, default=DEFAULT_HYPERPARAMETERS.momentum)
    parser.add_argument("--test-size", type=float, default=DEFAULT_HYPERPARAMETERS.test_size)
    parser.add_argument("--random-seed", type=int, default=DEFAULT_HYPERPARAMETERS.random_seed)
    parser.add_argument(
        "--sklearn-train-equals-test",
        action="store_true",
        help="Use the professor code path where Scikit-Learn trains and evaluates on the full dataset.",
    )
    return parser


def build_params(args: argparse.Namespace) -> HyperParameters:
    return HyperParameters(
        learning_rate=args.learning_rate,
        hidden_neurons=args.hidden_neurons,
        second_hidden_neurons=args.second_hidden_neurons,
        hidden_activation=args.hidden_activation,
        output_activation=args.output_activation,
        epochs=args.epochs,
        momentum=args.momentum,
        random_seed=args.random_seed,
        test_size=args.test_size,
    )


def print_result(result: EngineResult) -> None:
    print(f"\n=== {result.engine_name} ===")
    if result.status != "completed":
        print(f"Status: {result.status}")
        print(result.note)
        return

    print(f"Accuracy : {result.accuracy:.2f}%")
    print(f"Precision: {result.precision:.2f}%")
    print(f"Recall   : {result.recall:.2f}%")
    print(f"F1-score : {result.f1_score:.2f}%")
    print(f"Time     : {result.training_time:.3f}s")
    if "mode" in result.extra:
        print(f"Mode     : {result.extra['mode']}")
    if "iterations" in result.extra:
        print(f"Iter     : {result.extra['iterations']}")
    if "confusion_matrix" in result.extra:
        print("Confusion matrix:")
        print(result.extra["confusion_matrix"])
    if result.note:
        print(f"Note     : {result.note}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    params = build_params(args)

    features, labels = load_numeric_dataset(args.dataset)
    x_train, x_test, y_train, y_test = split_dataset(features, labels, params)

    print(f"Dataset  : {args.dataset}")
    print(f"Train    : {len(x_train)} samples")
    print(f"Test     : {len(x_test)} samples")

    results = [
        run_custom_mlp(x_train, y_train, x_test, y_test, params),
        run_sklearn_mlp(args.dataset, params, train_equals_test=args.sklearn_train_equals_test),
    ]
    for result in results:
        print_result(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
