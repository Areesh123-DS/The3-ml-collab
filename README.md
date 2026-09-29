# The3-ml-collab

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

California Housing price regression, run as a team project with Git, DVC, reviewed pull requests and CI.

- **Dataset:** [California Housing](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset) (`sklearn.datasets.fetch_california_housing`), 20,640 rows, 8 numeric features, target `MedHouseVal`.
- **Model:** `RandomForestRegressor`, hyperparameters in `configs/params.yaml`.
- **Workflow:** see [CONTRIBUTING.md](CONTRIBUTING.md).

## Quick start

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync                                 # create .venv from uv.lock
uv run dvc pull                         # fetch data and model from the DVC remote (see CONTRIBUTING.md)
uv run dvc repro                        # prepare -> train -> evaluate, writes metrics.json
uv run pytest                           # run tests
uv run ruff check . && uv run ruff format --check .
```

## Project Organization

```
├── Makefile           <- Convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project
├── CONTRIBUTING.md    <- Branching model, commit convention, merge policy
├── dvc.yaml           <- Pipeline stages: prepare -> train -> evaluate
├── dvc.lock           <- Hashes of every stage's deps, params and outputs
├── metrics.json       <- Test metrics and the git SHA of the run
├── configs
│   └── params.yaml    <- Seed, split and model hyperparameters
├── data               <- Ignored by Git, tracked by DVC
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── docs               <- Project documentation
├── models             <- Trained models (ignored by Git, tracked by DVC)
├── notebooks          <- Jupyter notebooks, paired with .py scripts via jupytext
├── references         <- Data dictionaries, manuals, and other explanatory materials
├── reports
│   └── figures        <- Generated graphics and figures
├── tests              <- Unit tests (pytest)
├── .github/workflows  <- CI pipelines
├── pyproject.toml     <- Project metadata, dependencies and tool configuration
├── uv.lock            <- Pinned dependency versions
│
└── src                <- Source code for use in this project
    ├── __init__.py
    ├── config.py      <- Project paths
    ├── dataset.py     <- Download the raw dataset
    ├── prepare.py     <- Stage 1: seeded train/test split
    ├── features.py    <- Feature engineering
    ├── plots.py       <- Visualizations
    └── modeling
        ├── __init__.py
        ├── predict.py  <- Model inference
        ├── train.py    <- Stage 2: fit the model on the train split
        └── evaluate.py <- Stage 3: score on the test split, write metrics.json
```
