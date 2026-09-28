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
uv run python -m src.dataset            # download data to data/raw/california_housing.csv
uv run python -m src.modeling.train     # train, print RMSE / MAE / R², save models/model.joblib
uv run pytest                           # run tests
uv run ruff check . && uv run ruff format --check .
```

## Project Organization

```
├── Makefile           <- Convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project
├── CONTRIBUTING.md    <- Branching model, commit convention, merge policy
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
    ├── features.py    <- Feature engineering
    ├── plots.py       <- Visualizations
    └── modeling
        ├── __init__.py
        ├── predict.py <- Model inference
        └── train.py   <- Train and evaluate the model
```
