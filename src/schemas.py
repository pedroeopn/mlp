from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_LEARNING_RATE = 0.1
DEFAULT_HIDDEN_NEURONS = 64
DEFAULT_SECOND_HIDDEN_NEURONS = 32
DEFAULT_HIDDEN_ACTIVATION = "relu"
DEFAULT_OUTPUT_ACTIVATION = "softmax"
DEFAULT_EPOCHS = 800
DEFAULT_MOMENTUM = 0.9
DEFAULT_RANDOM_SEED = 42
DEFAULT_TEST_SIZE = 0.2


@dataclass(frozen=True, slots=True)
class HyperParameters:
    learning_rate: float = DEFAULT_LEARNING_RATE
    hidden_neurons: int = DEFAULT_HIDDEN_NEURONS
    second_hidden_neurons: int = DEFAULT_SECOND_HIDDEN_NEURONS
    hidden_activation: str = DEFAULT_HIDDEN_ACTIVATION
    output_activation: str = DEFAULT_OUTPUT_ACTIVATION
    epochs: int = DEFAULT_EPOCHS
    momentum: float = DEFAULT_MOMENTUM
    random_seed: int = DEFAULT_RANDOM_SEED
    test_size: float = DEFAULT_TEST_SIZE


DEFAULT_HYPERPARAMETERS = HyperParameters()


@dataclass(slots=True)
class EngineResult:
    engine_name: str
    accuracy: float | None = None
    precision: float | None = None
    recall: float | None = None
    f1_score: float | None = None
    training_time: float | None = None
    status: str = "pending"
    note: str = ""
    raw_output: str = ""
    extra: dict[str, str] = field(default_factory=dict)
