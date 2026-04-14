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
DISPLAY_FONT = "Didot"
BODY_FONT = "Optima"


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
