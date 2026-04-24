from __future__ import annotations

from pathlib import Path
from queue import Empty
from tkinter import StringVar, messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.models import EngineResult, HyperParameters, SessionEvent
from src.comparison_service import (
    CONTROL_KEY,
    create_comparison_state,
    start_comparison,
    cancel_comparison,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ENGINE_ORDER = ["custom", "sklearn", "weka"]
ENGINE_TITLES = {
    "custom": "Custom mlp.py",
    "sklearn": "Scikit-Learn",
    "weka": "Weka",
}
DISPLAY_FONT = "Didot"
BODY_FONT = "Optima"


class ControlsPanel(ctk.CTkFrame):
    def __init__(self, master, on_run, on_cancel, **kwargs):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="#020202",
            border_width=1,
            border_color="#252525",
            **kwargs,
        )
        self.on_run = on_run
        self.on_cancel = on_cancel
        self.learning_rate_var = StringVar(value="0.01")
        self.hidden_neurons_var = StringVar(value="12")
        self.epochs_var = StringVar(value="400")
        self.hidden_activation_var = StringVar(value="relu")
        self.output_activation_var = StringVar(value="softmax")
        self.dataset_var = StringVar()
        self.status_var = StringVar(value="Ready")
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def set_dataset_path(self, dataset_path: str | Path) -> None:
        self.dataset_var.set(str(Path(dataset_path).resolve()))

    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    def set_running(self, running: bool) -> None:
        self.run_button.configure(state="disabled" if running else "normal")
        self.cancel_button.configure(state="normal" if running else "disabled")

    def _build(self) -> None:
        subtitle = ctk.CTkLabel(
            self,
            text="Pedro Ernesto",
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=16),
            text_color="#D6D6D6",
        )
        subtitle.grid(row=0, column=0, padx=24, pady=(30, 20), sticky="w")

        self._add_entry("Learning Rate", self.learning_rate_var, 2)
        self._add_entry("Hidden Neurons", self.hidden_neurons_var, 4)
        self._add_entry("Epochs", self.epochs_var, 6)

        hidden_activation_label = ctk.CTkLabel(
            self,
            text="Hidden Activation (valid for Custom and Scikit)",
            font=ctk.CTkFont(family=BODY_FONT, size=15),
            text_color="#F2F2F2",
        )
        hidden_activation_label.grid(row=8, column=0, padx=24, pady=(18, 8), sticky="w")
        hidden_activation_menu = ctk.CTkOptionMenu(
            self,
            variable=self.hidden_activation_var,
            values=["relu", "sigmoid"],
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            fg_color="#101010",
            button_color="#B6B5B5",
            button_hover_color="#D9D9D9",
            dropdown_fg_color="#111111",
            text_color="#FFFFFF",
            dropdown_text_color="#FFFFFF",
        )
        hidden_activation_menu.grid(row=9, column=0, padx=24, sticky="ew")

        output_activation_label = ctk.CTkLabel(
            self,
            text="Output Activation (valid for Custom)",
            font=ctk.CTkFont(family=BODY_FONT, size=15),
            text_color="#F2F2F2",
        )
        output_activation_label.grid(row=10, column=0, padx=24, pady=(18, 8), sticky="w")
        output_activation_menu = ctk.CTkOptionMenu(
            self,
            variable=self.output_activation_var,
            values=["softmax", "sigmoid"],
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            fg_color="#101010",
            button_color="#B6B5B5",
            button_hover_color="#D9D9D9",
            dropdown_fg_color="#111111",
            text_color="#FFFFFF",
            dropdown_text_color="#FFFFFF",
        )
        output_activation_menu.grid(row=11, column=0, padx=24, sticky="ew")

        shared_hint = ctk.CTkLabel(
            self,
            text="Learning Rate, Hidden Neurons, and Epochs are valid for Custom, Scikit, and Weka.",
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=12),
            text_color="#8F8F8F",
        )
        shared_hint.grid(row=12, column=0, padx=24, pady=(8, 6), sticky="w")

        dataset_label = ctk.CTkLabel(
            self,
            text="Dataset",
            font=ctk.CTkFont(family=BODY_FONT, size=15),
            text_color="#F2F2F2",
        )
        dataset_label.grid(row=13, column=0, padx=24, pady=(18, 8), sticky="w")
        dataset_entry = ctk.CTkEntry(
            self,
            textvariable=self.dataset_var,
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            fg_color="#0A0A0A",
            border_color="#383838",
            text_color="#FFFFFF",
        )
        dataset_entry.grid(row=14, column=0, padx=24, sticky="ew")

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=15, column=0, padx=24, pady=(28, 10), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)

        self.run_button = ctk.CTkButton(
            buttons,
            text="Start",
            command=self.on_run,
            height=42,
            fg_color="#FFFFFF",
            hover_color="#D8D8D8",
            text_color="#000000",
            font=ctk.CTkFont(family=BODY_FONT, size=14, weight="bold"),
        )
        self.run_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.cancel_button = ctk.CTkButton(
            buttons,
            text="Cancel",
            command=self.on_cancel,
            height=42,
            fg_color="#FFFFFF",
            hover_color="#D8D8D8",
            text_color="#000000",
            state="disabled",
            font=ctk.CTkFont(family=BODY_FONT, size=14, weight="bold"),
        )
        self.cancel_button.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        status_tag = ctk.CTkLabel(
            self,
            text="STATUS",
            font=ctk.CTkFont(family=BODY_FONT, size=11, weight="bold"),
            text_color="#AFAFAF",
        )
        status_tag.grid(row=16, column=0, padx=24, pady=(10, 2), sticky="w")

        status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            text_color="#FFFFFF",
        )
        status_label.grid(row=17, column=0, padx=24, pady=(0, 10), sticky="w")

        comparison_hint = ctk.CTkLabel(
            self,
            text="All three engines use the same split from this app: test size 20% and seed 42.",
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=13),
            text_color="#8F8F8F",
        )
        comparison_hint.grid(row=18, column=0, padx=24, pady=(0, 14), sticky="w")

        weka_hint = ctk.CTkLabel(
            self,
            text="Weka ignores both activation selectors and needs `bin/weka.jar`.",
            wraplength=280,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=13),
            text_color="#8F8F8F",
        )
        weka_hint.grid(row=19, column=0, padx=24, pady=(0, 24), sticky="w")

    def _add_entry(self, label_text: str, variable: StringVar, row: int) -> None:
        label = ctk.CTkLabel(
            self,
            text=label_text,
            font=ctk.CTkFont(family=BODY_FONT, size=15),
            text_color="#F2F2F2",
        )
        label.grid(row=row, column=0, padx=24, pady=(10, 8), sticky="w")
        entry = ctk.CTkEntry(
            self,
            textvariable=variable,
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            fg_color="#0A0A0A",
            border_color="#383838",
            text_color="#FFFFFF",
        )
        entry.grid(row=row + 1, column=0, padx=24, sticky="ew")


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, title: str, **kwargs):
        super().__init__(
            master,
            fg_color="#0B0B0B",
            corner_radius=24,
            border_width=1,
            border_color="#2F2F2F",
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family=DISPLAY_FONT, size=24, weight="bold"),
            text_color="#FFFFFF",
        )
        self.title_label.grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")
        self.status_label = ctk.CTkLabel(
            self,
            text="Idle",
            text_color="#B5B5B5",
            font=ctk.CTkFont(family=BODY_FONT, size=13, weight="bold"),
        )
        self.status_label.grid(row=1, column=0, padx=18, pady=(0, 8), sticky="w")
        self.metrics_label = ctk.CTkLabel(
            self,
            text="Acc  --\nTime --",
            justify="left",
            text_color="#FFFFFF",
            font=ctk.CTkFont(family=BODY_FONT, size=16),
        )
        self.metrics_label.grid(row=2, column=0, padx=18, pady=(0, 10), sticky="w")
        self.note_label = ctk.CTkLabel(
            self,
            text="Waiting.",
            wraplength=320,
            justify="left",
            font=ctk.CTkFont(family=BODY_FONT, size=14),
            text_color="#A8A8A8",
        )
        self.note_label.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="w")

    def update_result(self, result: EngineResult | None) -> None:
        if result is None or result.status == "pending":
            self.status_label.configure(text="Idle", text_color="#B5B5B5")
            self.metrics_label.configure(text="Acc  --\nPrec --\nRec  --\nF1   --\nTime --")
            self.note_label.configure(text="Waiting.")
            return

        self.status_label.configure(
            text=result.status.title(),
            text_color={
                "running": "#FFFFFF",
                "completed": "#FFFFFF",
                "failed": "#F1F1F1",
                "cancelled": "#D6D6D6",
            }.get(result.status, "#B5B5B5"),
        )

        if result.status == "completed":
            metrics_text = (
                f"Acc  {self._format_metric(result.accuracy, '.2f', suffix='%')}\n"
                f"Prec {self._format_metric(result.precision, '.2f', suffix='%')}\n"
                f"Rec  {self._format_metric(result.recall, '.2f', suffix='%')}\n"
                f"F1   {self._format_metric(result.f1_score, '.2f', suffix='%')}\n"
                f"Time {self._format_metric(result.training_time, '.3f', suffix='s')}"
            )
            if "iterations" in result.extra:
                metrics_text += f"\nIter {result.extra['iterations']}"
        else:
            metrics_text = "Acc  --\nPrec --\nRec  --\nF1   --\nTime --"

        self.metrics_label.configure(text=metrics_text)
        self.note_label.configure(text="Running..." if result.status == "running" else (result.note or "Done."))

    @staticmethod
    def _format_metric(value: float | None, specifier: str, suffix: str = "") -> str:
        if value is None:
            return "--"
        return f"{value:{specifier}}{suffix}"


class ChartPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#0B0B0B",
            corner_radius=24,
            border_width=1,
            border_color="#2F2F2F",
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.figure = Figure(figsize=(9, 4.6), dpi=100, facecolor="#0B0B0B")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.draw({})

    def draw(self, results: dict) -> None:
        self.figure.clear()
        self.figure.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.2, wspace=0.34)
        metrics = [
            ("Acc %", "accuracy", "#FFFFFF"),
            ("Time", "training_time", "#8F8F8F"),
        ]
        names = [ENGINE_TITLES[key] for key in ENGINE_ORDER]
        for index, (title, attribute, color) in enumerate(metrics, start=1):
            axis = self.figure.add_subplot(1, 2, index)
            axis.set_facecolor("#0B0B0B")
            values = []
            for engine_key in ENGINE_ORDER:
                result = results.get(engine_key)
                value = 0.0
                if result and result.status == "completed":
                    raw_value = getattr(result, attribute, None)
                    value = float(raw_value) if raw_value is not None else 0.0
                values.append(value)
            axis.bar(names, values, color=color, width=0.58)
            axis.set_title(title, fontsize=11, color="#FFFFFF", fontfamily=BODY_FONT)
            axis.tick_params(axis="x", labelrotation=18, labelsize=9, colors="#E4E4E4")
            axis.tick_params(axis="y", labelsize=9, colors="#BFBFBF")
            axis.grid(axis="y", alpha=0.16, color="#505050")
            axis.set_axisbelow(True)
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)
            axis.spines["left"].set_color("#3A3A3A")
            axis.spines["bottom"].set_color("#3A3A3A")
        self.canvas.draw_idle()


class ComparativeMLPApp(ctk.CTk):
    def __init__(self, dataset_path: str | Path, weka_jar_path: str | Path | None = None):
        super().__init__()
        self.title("MLP Glass Dashboard")
        self.geometry("1360x860")
        self.minsize(860, 640)
        self.configure(fg_color="#000000")
        self.comparison_state = create_comparison_state(dataset_path, weka_jar_path)
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
                hidden_activation=self.controls.hidden_activation_var.get(),
                output_activation=self.controls.output_activation_var.get(),
                epochs=int(self.controls.epochs_var.get()),
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
            self._render_result(engine_key, EngineResult(engine_name=ENGINE_TITLES[engine_key], status="running"))

        self.comparison_state = create_comparison_state(dataset_path=dataset_path, weka_jar_path=Path("bin/weka.jar"))
        start_comparison(self.comparison_state, params)

    def _on_cancel_clicked(self) -> None:
        cancel_comparison(self.comparison_state)
        self.controls.set_status("Cancelling active runs...")

    def _poll_results(self) -> None:
        while True:
            try:
                item_key, payload = self.comparison_state["result_queue"].get_nowait()
            except Empty:
                break

            try:
                if item_key == CONTROL_KEY and isinstance(payload, SessionEvent):
                    self._handle_session_event(payload)
                    continue
                if isinstance(payload, EngineResult):
                    self.results[item_key] = payload
                    self._render_result(item_key, payload)
            except Exception as exc:
                self.controls.set_running(False)
                self.controls.set_status(f"UI update failed: {exc}")
                if item_key in self.cards and isinstance(payload, EngineResult):
                    failed_result = EngineResult(
                        engine_name=payload.engine_name,
                        status="failed",
                        note=f"UI could not render the engine result: {exc}",
                    )
                    self.results[item_key] = failed_result
                    self._render_result(item_key, failed_result)

        self.after(150, self._poll_results)

    def _handle_session_event(self, event: SessionEvent) -> None:
        self.controls.set_running(False)
        self.controls.set_status(event.message or event.status.title())

    def _render_result(self, engine_key: str, result: EngineResult) -> None:
        self.cards[engine_key].update_result(result)
        self.chart_panel.draw(self.results)
