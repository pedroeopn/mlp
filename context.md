Context: Neural Network Comparative Analysis (Python vs. Weka)

Project Objective
Develop a graphical desktop application for comparative analysis of Multilayer Perceptron (MLP) neural networks. The system evaluates three engines side by side: the preserved custom implementation in `mlp.py`, Scikit-Learn (`MLPClassifier`), and Weka (`weka.jar` via CLI).

Current Technology Stack
Language: Python 3.10+

GUI Framework: CustomTkinter

Visualization: Matplotlib

Data Processing: NumPy, Scikit-Learn

External Integration: Weka 3.8+ through `subprocess`

Project Structure
Plaintext
/
├── data/                           # Temporary ARFF files generated at runtime
├── bin/                            # Optional location for weka.jar
└── src/
    ├── main.py                     # App bootstrap and recommended entrypoint
    ├── controllers/
    │   └── comparison_controller.py
    ├── core/
    │   ├── custom_mlp.py           # Wrapper around the preserved black-box mlp.py
    │   ├── dataset_utils.py        # Dataset loading, normalization, split
    │   ├── lib_mlp.py              # Scikit-Learn wrapper
    │   ├── mlp.py                  # [CRITICAL: BLACK-BOX CORE ALGORITHM - DO NOT MODIFY]
    │   ├── models.py               # Shared dataclasses
    │   └── weka_mlp.py             # ARFF conversion and Weka CLI parsing
    ├── data/
    │   └── dados.data-numeric      # Default numeric dataset
    ├── gui/
    │   ├── app.py                  # Main window composition
    │   └── components/
    │       ├── chart_panel.py
    │       ├── controls_panel.py
    │       └── result_card.py
    └── services/
        └── comparison_service.py   # Background execution, cancellation, worker lifecycle

Hard Constraints
Core Preservation: `src/core/mlp.py` is proprietary and must remain unchanged. Its mathematical logic must be treated as read-only. Any integration must happen through wrapper code only.

Architectural Parity: The interface must expose the shared hyperparameters used for comparison: learning rate, hidden neurons, and activation function. When an engine cannot honor one of them exactly, the UI must communicate that limitation explicitly.

Metrics: The dashboard must compare Accuracy, Training Time (seconds), and F1-Score.

Responsiveness: The GUI must stay responsive while work is running. Long tasks must execute outside the main Tk loop, and the window layout must adapt cleanly to narrower widths.

Cancellation: The application must expose a cancel action. Cancel must stop active worker execution and immediately return control to the interface.

Data Handling: The default dataset lives at `src/data/dados.data-numeric`. It must be normalized and split consistently, and Weka runs must receive generated ARFF files automatically.

Operational Rules
Scikit-Learn and the custom engine now run in isolated worker processes managed by a background service. This keeps the GUI responsive and allows cancellation without terminating the whole application.

Weka execution must validate Java availability and the presence of `bin/weka.jar` before training.

Fixed random seeds must be used for reproducible comparisons.

The UI must surface engine-level notes and failure states clearly so users can distinguish "still running", "completed", "cancelled", and "failed".

Coding Standards
Separation of Concerns: Keep GUI components, controller logic, and execution services isolated.

Naming Convention: Follow PEP 8 for functions and variables, and PascalCase for classes.
