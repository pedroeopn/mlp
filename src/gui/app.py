from __future__ import annotations

from pathlib import Path
from queue import Empty
from tkinter import messagebox

import customtkinter as ctk

from src.controllers.comparison_controller import ComparisonController
from src.core.models import EngineResult, HyperParameters, SessionEvent
from src.gui.components.chart_panel import ChartPanel
from src.gui.components.controls_panel import ControlsPanel
from src.gui.components.result_card import ResultCard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ENGINE_ORDER = ["custom", "sklearn", "weka"]
ENGINE_TITLES = {
    "custom": "Custom mlp.py",
    "sklearn": "Scikit-Learn",
    "weka": "Weka",
}
CONTROL_KEY = "__session__"
DISPLAY_FONT = "Didot"
BODY_FONT = "Optima"


class ComparativeMLPApp(ctk.CTk):
    def __init__(self, dataset_path: str | Path, weka_jar_path: str | Path | None = None):
        super().__init__()
        self.title("MLP Glass Dashboard")
        self.geometry("1360x860")
        self.minsize(860, 640)
        self.configure(fg_color="#000000")

        self.controller = ComparisonController(dataset_path, weka_jar_path)
        self.results: dict[str, EngineResult] = {}
        self._compact_layout = False

        self._build_layout(dataset_path)
        self.bind("<Configure>", self._on_window_resize)
        self.after(150, self._poll_results)

    def _build_layout(self, dataset_path: str | Path) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.controls = ControlsPanel(self, on_run=self._on_run_clicked, on_cancel=self._on_cancel_clicked, width=340)
        self.controls.grid(row=0, column=0, sticky="nsew")
        self.controls.grid_propagate(False)
        self.controls.set_dataset_path(dataset_path)

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="#050505",
            corner_radius=28,
            border_width=1,
            border_color="#2B2B2B",
        )
        self.content.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        self.header_frame = ctk.CTkFrame(
            self.content,
            fg_color="#0A0A0A",
            corner_radius=24,
            border_width=1,
            border_color="#2F2F2F",
        )
        self.header_frame.grid(row=0, column=0, padx=6, pady=(8, 18), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.header_frame,
            text="comparison ig",
            font=ctk.CTkFont(family=DISPLAY_FONT, size=32, weight="bold"),
            text_color="#FFFFFF",
        )
        header.grid(row=1, column=0, padx=18, pady=(0, 6), sticky="w")

        summary = ctk.CTkLabel(
            self.header_frame,
            text="MLP",
            font=ctk.CTkFont(family=BODY_FONT, size=15),
            text_color="#CFCFCF",
        )
        summary.grid(row=2, column=0, padx=18, pady=(0, 16), sticky="w")

        self.cards_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="nsew", padx=6)

        self.cards = {
            engine_key: ResultCard(self.cards_frame, ENGINE_TITLES[engine_key])
            for engine_key in ENGINE_ORDER
        }
        self._layout_cards(columns=3)

        self.chart_panel = ChartPanel(self.content)
        self.chart_panel.grid(row=2, column=0, sticky="nsew", padx=6, pady=(16, 12))

    def _layout_cards(self, columns: int) -> None:
        for child in self.cards_frame.winfo_children():
            child.grid_forget()

        for column in range(max(columns, 1)):
            self.cards_frame.grid_columnconfigure(column, weight=1)

        for index, engine_key in enumerate(ENGINE_ORDER):
            row = index // columns
            column = index % columns
            self.cards[engine_key].grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

    def _on_window_resize(self, _event=None) -> None:
        width = self.winfo_width()
        compact = width < 1180
        if compact == self._compact_layout:
            return

        self._compact_layout = compact
        if compact:
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.controls.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.content.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=18, pady=(0, 18))
            self._layout_cards(columns=1 if width < 900 else 2)
        else:
            self.grid_rowconfigure(1, weight=0)
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
            self.controls.grid(row=0, column=0, columnspan=1, sticky="nsew")
            self.content.grid(row=0, column=1, columnspan=1, sticky="nsew", padx=18, pady=18)
            self._layout_cards(columns=3)

    def _on_run_clicked(self) -> None:
        try:
            params = HyperParameters(
                learning_rate=float(self.controls.learning_rate_var.get()),
                hidden_neurons=int(self.controls.hidden_neurons_var.get()),
                epochs=int(self.controls.epochs_var.get()),
                activation_function=self.controls.activation_var.get(),
            )
        except ValueError:
            messagebox.showerror("Invalid input", "Use numeric values for rate, neurons, and epochs.")
            return

        dataset_path = Path(self.controls.dataset_var.get()).expanduser()
        if not dataset_path.exists():
            messagebox.showerror("Dataset missing", f"Dataset not found:\n{dataset_path}")
            return

        self.results = {}
        self.controls.set_running(True)
        self.controls.set_status("Launching run...")
        for engine_key in ENGINE_ORDER:
            self._render_result(
                engine_key,
                EngineResult(engine_name=ENGINE_TITLES[engine_key], status="running"),
            )

        self.controller = ComparisonController(dataset_path=dataset_path, weka_jar_path=Path("bin/weka.jar"))
        self.controller.start_comparison(params)

    def _on_cancel_clicked(self) -> None:
        self.controller.cancel_comparison()
        self.controls.set_status("Cancelling active runs...")

    def _poll_results(self) -> None:
        while True:
            try:
                item_key, payload = self.controller.result_queue.get_nowait()
            except Empty:
                break

            if item_key == CONTROL_KEY and isinstance(payload, SessionEvent):
                self._handle_session_event(payload)
                continue

            if isinstance(payload, EngineResult):
                self.results[item_key] = payload
                self._render_result(item_key, payload)

        self.after(150, self._poll_results)

    def _handle_session_event(self, event: SessionEvent) -> None:
        self.controls.set_running(False)
        self.controls.set_status(event.message or event.status.title())

    def _render_result(self, engine_key: str, result: EngineResult) -> None:
        self.cards[engine_key].update_result(result)
        self.chart_panel.draw(self.results)
