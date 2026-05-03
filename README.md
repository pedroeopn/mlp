# MLP

Terminal comparison between the custom MLP in `src/mlp.py` and the professor-style
Scikit-Learn implementation from `src/rna_scikit.py`.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 -m src.main
```

Optional parameters:

```bash
python3 -m src.main --epochs 800 --learning-rate 0.1 --hidden-neurons 64 --second-hidden-neurons 32 --momentum 0.9
```

To run the professor's `op == 1` path for Scikit-Learn:

```bash
python3 -m src.main --sklearn-train-equals-test
```

## Files

- Python dataset: `data/dados.data-numeric`
- Active Scikit-Learn implementation: `src/rna_scikit.py`

## Defaults

- test size: `20%`
- random seed: `42`
- metrics: macro precision, macro recall, macro F1
- Scikit-Learn scaler: `MinMaxScaler(feature_range=(-1, 1))`
- Scikit-Learn solver: `sgd`
- Scikit-Learn momentum: `0.9`
