"""Train a random forest regressor on California Housing.

Starter code adapted from the scikit-learn California Housing examples:
https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset
"""

from pathlib import Path

import joblib
from loguru import logger
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import typer
import yaml

from src.config import PROJ_ROOT

app = typer.Typer()

DEFAULT_PARAMS = PROJ_ROOT / "configs" / "params.yaml"


def load_params(path: Path = DEFAULT_PARAMS) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def train_and_evaluate(df: pd.DataFrame, params: dict):
    """Split, fit and score. Returns (model, metrics)."""
    target = params["data"]["target"]
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=params["split"]["test_size"],
        random_state=params["seed"],
    )

    model = RandomForestRegressor(
        n_estimators=params["train"]["n_estimators"],
        max_depth=params["train"]["max_depth"],
        random_state=params["seed"],
        n_jobs=1,  # parallel prediction sums trees in random order -> non-identical floats
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }
    return model, metrics


@app.command()
def main(
    params_path: Path = DEFAULT_PARAMS,
    data_path: Path | None = None,
    model_path: Path | None = None,
):
    params = load_params(params_path)
    data_path = data_path or PROJ_ROOT / params["data"]["raw_path"]
    model_path = model_path or PROJ_ROOT / params["train"]["model_path"]

    logger.info(f"Training on {data_path}...")
    df = pd.read_csv(data_path)
    model, metrics = train_and_evaluate(df, params)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    for name, value in metrics.items():
        logger.info(f"{name}: {value:.4f}")
    logger.success(f"Model saved to {model_path}")


if __name__ == "__main__":
    app()
