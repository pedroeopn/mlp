from __future__ import annotations

import customtkinter as ctk

from src.core.models import EngineResult


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, title: str, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family="Avenir Next", size=22, weight="bold"),
            text_color="#17364A",
        )
        self.title_label.grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")

        self.status_label = ctk.CTkLabel(
            self,
            text="Pending",
            text_color="#6C7F8E",
        )
        self.status_label.grid(row=1, column=0, padx=18, pady=(0, 8), sticky="w")

        self.metrics_label = ctk.CTkLabel(
            self,
            text="Accuracy: --\nF1-Score: --\nTraining Time: --",
            justify="left",
            text_color="#27485C",
        )
        self.metrics_label.grid(row=2, column=0, padx=18, pady=(0, 10), sticky="w")

        self.note_label = ctk.CTkLabel(
            self,
            text="Awaiting execution.",
            wraplength=320,
            justify="left",
            text_color="#6C7F8E",
        )
        self.note_label.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="w")

    def update_result(self, result: EngineResult | None) -> None:
        if result is None or result.status == "pending":
            self.status_label.configure(text="Pending", text_color="#6C7F8E")
            self.metrics_label.configure(text="Accuracy: --\nF1-Score: --\nTraining Time: --")
            self.note_label.configure(text="Awaiting execution.")
            return

        status_colors = {
            "running": "#2D6286",
            "completed": "#2F7D57",
            "failed": "#8B2E34",
            "cancelled": "#8B6A2B",
        }
        self.status_label.configure(
            text=result.status.title(),
            text_color=status_colors.get(result.status, "#6C7F8E"),
        )

        if result.status == "completed":
            metrics_text = (
                f"Accuracy: {result.accuracy:.2f}%\n"
                f"F1-Score: {result.f1_score:.4f}\n"
                f"Training Time: {result.training_time:.3f}s"
            )
            if "iterations" in result.extra:
                metrics_text += f"\nIterations: {result.extra['iterations']}"
        else:
            metrics_text = "Accuracy: --\nF1-Score: --\nTraining Time: --"

        self.metrics_label.configure(text=metrics_text)

        if result.status == "running":
            note_text = "Training in progress..."
        else:
            note_text = result.note or "Execution completed successfully."

        self.note_label.configure(text=note_text)
