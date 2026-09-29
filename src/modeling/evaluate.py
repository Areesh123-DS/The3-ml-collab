"""Stage 3: score the trained model on the test split and write metrics.json."""

import json
from pathlib import Path
import subprocess

import joblib
from loguru import logger
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import typer

from src.config import DEFAULT_PARAMS, METRICS_PATH, PROJ_ROOT, TEST_PATH, load_params

app = typer.Typer()


def evaluate_model(model, test_df: pd.DataFrame, target: str) -> dict:
    preds = model.predict(test_df.drop(columns=[target]))
    y = test_df[target]
    return {
        "rmse": float(np.sqrt(mean_squared_error(y, preds))),
        "mae": float(mean_absolute_error(y, preds)),
        "r2": float(r2_score(y, preds)),
    }


def get_git_sha() -> str:
    """Commit the run was made from. Commit code before `dvc repro` so this matches it."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJ_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


@app.command()
def main(
    params_path: Path = DEFAULT_PARAMS,
    test_path: Path = TEST_PATH,
    model_path: Path | None = None,
    metrics_path: Path = METRICS_PATH,
):
    params = load_params(params_path)
    model_path = model_path or PROJ_ROOT / params["train"]["model_path"]

    model = joblib.load(model_path)
    metrics = evaluate_model(model, pd.read_csv(test_path), params["data"]["target"])

    for name, value in metrics.items():
        logger.info(f"{name}: {value:.4f}")

    metrics["git_sha"] = get_git_sha()
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")
    logger.success(f"Metrics saved to {metrics_path}")


if __name__ == "__main__":
    app()
