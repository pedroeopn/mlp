from __future__ import annotations

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ENGINE_ORDER = ["custom", "sklearn", "weka"]
ENGINE_TITLES = {
    "custom": "Custom mlp.py",
    "sklearn": "Scikit-Learn",
    "weka": "Weka",
}


class ChartPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(9, 4.6), dpi=100, facecolor="#FFFFFF")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.draw({})

    def draw(self, results: dict) -> None:
        self.figure.clear()
        self.figure.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.16, wspace=0.34)

        metrics = [
            ("Accuracy (%)", "accuracy", "#1F4B67"),
            ("F1-Score", "f1_score", "#F2A65A"),
            ("Training Time (s)", "training_time", "#70A37F"),
        ]

        names = [ENGINE_TITLES[key] for key in ENGINE_ORDER]
        for index, (title, attribute, color) in enumerate(metrics, start=1):
            axis = self.figure.add_subplot(1, 3, index)
            values = []
            for engine_key in ENGINE_ORDER:
                result = results.get(engine_key)
                value = getattr(result, attribute, 0.0) if result and result.status == "completed" else 0.0
                values.append(value)
            axis.bar(names, values, color=color, width=0.58)
            axis.set_title(title, fontsize=11, color="#17364A")
            axis.tick_params(axis="x", labelrotation=18, labelsize=9)
            axis.tick_params(axis="y", labelsize=9)
            axis.grid(axis="y", alpha=0.2)
            axis.set_axisbelow(True)

        self.canvas.draw_idle()
