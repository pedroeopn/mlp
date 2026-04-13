from __future__ import annotations

import customtkinter as ctk

from src.core.models import EngineResult

DISPLAY_FONT = "Didot"
BODY_FONT = "Optima"


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
            text="Acc  --\nF1   --\nTime --",
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
            self.metrics_label.configure(text="Acc  --\nF1   --\nTime --")
            self.note_label.configure(text="Waiting.")
            return

        status_colors = {
            "running": "#FFFFFF",
            "completed": "#FFFFFF",
            "failed": "#F1F1F1",
            "cancelled": "#D6D6D6",
        }
        self.status_label.configure(
            text=result.status.title(),
            text_color=status_colors.get(result.status, "#B5B5B5"),
        )

        if result.status == "completed":
            metrics_text = (
                f"Acc  {result.accuracy:.2f}%\n"
                f"F1   {result.f1_score:.4f}\n"
                f"Time {result.training_time:.3f}s"
            )
            if "iterations" in result.extra:
                metrics_text += f"\nIter {result.extra['iterations']}"
        else:
            metrics_text = "Acc  --\nF1   --\nTime --"

        self.metrics_label.configure(text=metrics_text)

        if result.status == "running":
            note_text = "Running..."
        else:
            note_text = result.note or "Done."

        self.note_label.configure(text=note_text)
