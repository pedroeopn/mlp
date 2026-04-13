# Comparative MLP Dashboard

Desktop application for comparing three Multilayer Perceptron implementations over the same dataset and hyperparameters:

- Custom implementation preserved in `src/core/mlp.py`
- Scikit-Learn `MLPClassifier`
- Weka `MultilayerPerceptron` through the CLI

The interface is built with CustomTkinter and includes:

- Shared hyperparameter controls
- Side-by-side result cards
- A Matplotlib chart for Accuracy, F1-Score, and Training Time
- Cancel support for active runs
- Responsive layout behavior for narrower windows

## Project Structure

```text
.
├── README.md
├── context.md
├── data/                         # Temporary ARFF files generated at runtime
├── bin/                          # Optional location for weka.jar
└── src/
    ├── main.py                   # Application entrypoint
    ├── controllers/
    ├── core/
    │   ├── custom_mlp.py
    │   ├── dataset_utils.py
    │   ├── lib_mlp.py
    │   ├── mlp.py                # Preserved black-box algorithm
    │   ├── models.py
    │   └── weka_mlp.py
    ├── data/
    │   └── dados.data-numeric    # Default dataset
    ├── gui/
    │   ├── app.py
    │   └── components/
    └── services/
        └── comparison_service.py
```

## Requirements

- Python 3.10 or newer
- `pip`
- Java Runtime Environment if you want to run Weka
- Optional: `weka.jar` placed at `bin/weka.jar`

## Python Dependencies

Install the required Python packages:

```bash
python3 -m pip install customtkinter matplotlib numpy scikit-learn
```

If you want a pinned environment, create a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install customtkinter matplotlib numpy scikit-learn
```

## Weka Setup

Weka support is optional. Without `bin/weka.jar`, the application still runs, but the Weka card will show a failure state.

Steps:

1. Download a Weka 3.8+ jar.
2. Create the `bin/` folder if it does not exist.
3. Place the jar at `bin/weka.jar`.
4. Make sure `java` is available in your `PATH`.

Check Java:

```bash
java -version
```

## How To Run

From the project root:

```bash
python3 -m src.main
```

The app starts with the default dataset at `src/data/dados.data-numeric`.

## How It Works

1. The app loads and normalizes the numeric dataset.
2. It splits the dataset into train and test partitions with a fixed random seed.
3. The custom engine, Scikit-Learn engine, and Weka engine run in isolated worker processes.
4. Results are pushed back to the GUI and displayed as cards and a comparative chart.

## Notes About The Engines

- `src/core/mlp.py` is treated as a black box and must not be modified.
- The custom engine does not support arbitrary internal changes; some requested hyperparameters may only be approximated externally.
- Scikit-Learn uses early stopping to reduce long-running fits.
- Weka may not support the same activation options exposed by the UI. When parity is imperfect, the UI shows a note.

## Custom Engine Limitations

- In the current custom `src/core/mlp.py` integration, selecting `sigmoid` in the UI does not switch the model from Softmax to Sigmoid. The UI option is misleading for the custom engine.
- The preserved `mlp.py` still runs the ReLU/Softmax path because the sigmoid forward-pass and derivative lines are commented out in the black-box source.
- For the custom engine, only `hidden_neurons` and `epochs` actually affect training.
- `learning_rate` does not affect the custom engine today because `mlp.py` uses a fixed internal value `alfa = 0.01`.

Brief fix:

- Update the UI to label activation and learning rate as applying only to Scikit-Learn/Weka for the custom engine, or disable those controls when the comparison includes the preserved custom model.
- If real parity is required, refactor the custom wrapper so the preserved training function can receive activation mode and learning rate as explicit inputs instead of using hardcoded internal behavior.

## Common Issues

### Dataset not found

The default dataset path is:

```text
src/data/dados.data-numeric
```

If you move the dataset, update the path in the interface or adjust `src/main.py`.

### Weka fails immediately

Check both:

- `java -version` works
- `bin/weka.jar` exists

### GUI dependencies missing

If the app prints a missing dependency error, install:

```bash
python3 -m pip install customtkinter matplotlib
```

## Development Notes

- Entry point: [src/main.py](/Users/pedroernesto/Downloads/mlp/src/main.py)
- Preserved algorithm: [src/core/mlp.py](/Users/pedroernesto/Downloads/mlp/src/core/mlp.py)
- Main GUI: [src/gui/app.py](/Users/pedroernesto/Downloads/mlp/src/gui/app.py)
- Background execution: [src/services/comparison_service.py](/Users/pedroernesto/Downloads/mlp/src/services/comparison_service.py)

## Verification

A quick syntax check can be run with:

```bash
python3 -m py_compile src/main.py src/gui/app.py src/services/comparison_service.py
```
