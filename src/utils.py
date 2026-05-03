from __future__ import annotations

from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from .schemas import HyperParameters


def load_raw_numeric_dataset(dataset_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    path = Path(dataset_path)
    rows: list[list[float]] = []

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append([float(value) for value in line.split()])

    data = np.asarray(rows, dtype=float)
    x = data[:, :-1]
    y = data[:, -1].astype(int)

    unique_classes = sorted(np.unique(y).tolist())
    if unique_classes and unique_classes[0] != 0:
        mapping = {label: index for index, label in enumerate(unique_classes)}
        y = np.vectorize(mapping.get)(y).astype(int)

    return x, y


def load_numeric_dataset(dataset_path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    x, y = load_raw_numeric_dataset(dataset_path)
    x = normalize_features(x)
    return x, y


def normalize_features(features: np.ndarray) -> np.ndarray:
    minimum = features.min(axis=0)
    maximum = features.max(axis=0)
    denominator = maximum - minimum
    denominator[denominator == 0] = 1
    return (features - minimum) / denominator


def split_dataset(
    features: np.ndarray,
    labels: np.ndarray,
    params: HyperParameters,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=params.test_size,
        random_state=params.random_seed,
        stratify=labels,
    )

    return x_train, x_test, y_train, y_test
