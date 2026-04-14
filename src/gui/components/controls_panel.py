from __future__ import annotations

from pathlib import Path
from tkinter import StringVar

import customtkinter as ctk

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
