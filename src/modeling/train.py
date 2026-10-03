"""Stage 2: train a random forest regressor on the training split.

Starter code adapted from the scikit-learn California Housing examples:
https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset
"""

from pathlib import Path

import joblib
from loguru import logger
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import typer

from src.config import DEFAULT_PARAMS, PROJ_ROOT, TRAIN_PATH, load_params

app = typer.Typer()


def train_model(train_df: pd.DataFrame, params: dict) -> RandomForestRegressor:
    if params["train"]["model"] != "random_forest":
        raise ValueError(f"Unsupported model: {params['train']['model']}")

    target = params["data"]["target"]
    X = train_df.drop(columns=[target])
    y = train_df[target]

    model = RandomForestRegressor(
        n_estimators=params["train"]["n_estimators"],
        max_depth=params["train"]["max_depth"],
        random_state=params["seed"],
        n_jobs=1,  # parallel prediction sums trees in random order -> non-identical floats
    )
    model.fit(X, y)
    return model


@app.command()
def main(
    params_path: Path = DEFAULT_PARAMS,
    train_path: Path = TRAIN_PATH,
    model_path: Path | None = None,
):
    params = load_params(params_path)
    model_path = model_path or PROJ_ROOT / params["train"]["model_path"]

    logger.info(f"Training on {train_path}...")
    model = train_model(pd.read_csv(train_path), params)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    logger.success(f"Model saved to {model_path}")


if __name__ == "__main__":
    app()
