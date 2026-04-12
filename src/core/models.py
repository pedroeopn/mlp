from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class HyperParameters:
    learning_rate: float
    hidden_neurons: int
    activation_function: str
    epochs: int = 400
    random_seed: int = 42
    test_size: float = 0.2


@dataclass(slots=True)
class EngineResult:
    engine_name: str
    accuracy: float | None = None
    f1_score: float | None = None
    training_time: float | None = None
    status: str = "pending"
    note: str = ""
    raw_output: str = ""
    extra: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SessionEvent:
    event_type: str
    status: str
    message: str = ""


@dataclass(slots=True)
class DatasetSplit:
    x_train: object
    x_test: object
    y_train: object
    y_test: object
