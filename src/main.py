from __future__ import annotations

from pathlib import Path


def main() -> int:
    try:
        from src.app import ComparativeMLPApp
    except ModuleNotFoundError as exc:
        missing = getattr(exc, "name", "dependency")
        print(
            "Missing dependency for the GUI: "
            f"{missing}. Install project requirements including customtkinter and matplotlib."
        )
        return 1

    root_dir = Path(__file__).resolve().parents[1]
    dataset_path = root_dir / "data" / "dados.data-numeric"

    app = ComparativeMLPApp(dataset_path=dataset_path)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
