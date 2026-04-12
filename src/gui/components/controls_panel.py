from __future__ import annotations

from pathlib import Path
from tkinter import StringVar

import customtkinter as ctk


class ControlsPanel(ctk.CTkFrame):
    def __init__(self, master, on_run, on_cancel, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#132A3A", **kwargs)
        self.on_run = on_run
        self.on_cancel = on_cancel

        self.learning_rate_var = StringVar(value="0.01")
        self.hidden_neurons_var = StringVar(value="12")
        self.activation_var = StringVar(value="relu")
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
        title = ctk.CTkLabel(
            self,
            text="MLP Comparison",
            font=ctk.CTkFont(family="Avenir Next", size=28, weight="bold"),
            text_color="#F2F4F8",
        )
        title.grid(row=0, column=0, padx=24, pady=(28, 12), sticky="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Compare the preserved custom MLP, Scikit-Learn, and Weka under the same parameters.",
            wraplength=280,
            justify="left",
            text_color="#C7D0D9",
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        self._add_entry("Learning Rate", self.learning_rate_var, 2)
        self._add_entry("Hidden Neurons", self.hidden_neurons_var, 4)

        activation_label = ctk.CTkLabel(self, text="Activation Function", text_color="#F2F4F8")
        activation_label.grid(row=6, column=0, padx=24, pady=(18, 8), sticky="w")
        activation_menu = ctk.CTkOptionMenu(
            self,
            variable=self.activation_var,
            values=["relu", "sigmoid", "tanh"],
            fg_color="#1F4B67",
            button_color="#38739D",
            button_hover_color="#2D6286",
        )
        activation_menu.grid(row=7, column=0, padx=24, sticky="ew")

        dataset_label = ctk.CTkLabel(self, text="Dataset", text_color="#F2F4F8")
        dataset_label.grid(row=8, column=0, padx=24, pady=(18, 8), sticky="w")
        dataset_entry = ctk.CTkEntry(self, textvariable=self.dataset_var)
        dataset_entry.grid(row=9, column=0, padx=24, sticky="ew")

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=10, column=0, padx=24, pady=(28, 10), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)

        self.run_button = ctk.CTkButton(
            buttons,
            text="Run",
            command=self.on_run,
            height=42,
            fg_color="#F2A65A",
            hover_color="#DE8E44",
            text_color="#10212B",
        )
        self.run_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.cancel_button = ctk.CTkButton(
            buttons,
            text="Cancel",
            command=self.on_cancel,
            height=42,
            fg_color="#8B2E34",
            hover_color="#73252B",
            state="disabled",
        )
        self.cancel_button.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            wraplength=280,
            justify="left",
            text_color="#C7D0D9",
        )
        status_label.grid(row=11, column=0, padx=24, pady=(8, 14), sticky="w")

        hint = ctk.CTkLabel(
            self,
            text="Weka expects `bin/weka.jar`. Cancel stops the active worker processes and unlocks the UI immediately.",
            wraplength=280,
            justify="left",
            text_color="#9DB1BF",
        )
        hint.grid(row=12, column=0, padx=24, pady=(0, 24), sticky="w")

    def _add_entry(self, label_text: str, variable: StringVar, row: int) -> None:
        label = ctk.CTkLabel(self, text=label_text, text_color="#F2F4F8")
        label.grid(row=row, column=0, padx=24, pady=(10, 8), sticky="w")
        entry = ctk.CTkEntry(self, textvariable=variable)
        entry.grid(row=row + 1, column=0, padx=24, sticky="ew")
