from __future__ import annotations

from pathlib import Path

from src.core.models import HyperParameters
from src.services.comparison_service import ComparisonService


class ComparisonController:
    def __init__(self, dataset_path: str | Path, weka_jar_path: str | Path | None = None):
        self.service = ComparisonService(dataset_path, weka_jar_path)
        self.result_queue = self.service.result_queue

    def start_comparison(self, params: HyperParameters) -> None:
        self.service.start(params)
        self.result_queue = self.service.result_queue

    def cancel_comparison(self) -> None:
        self.service.cancel()

    @property
    def is_running(self) -> bool:
        return self.service.is_running
