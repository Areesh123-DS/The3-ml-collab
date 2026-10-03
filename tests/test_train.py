import numpy as np
import pandas as pd

from src.config import load_params
from src.modeling.evaluate import evaluate_model
from src.modeling.train import train_model
from src.prepare import split_data

FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]


def _synthetic_housing(n_rows: int = 200) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    df = pd.DataFrame(rng.random((n_rows, len(FEATURES))), columns=FEATURES)
    df["MedHouseVal"] = 2 * df["MedInc"] + rng.normal(0, 0.1, n_rows)
    return df


def _small_params() -> dict:
    params = load_params()
    params["train"]["n_estimators"] = 10
    return params


def _run_pipeline(df: pd.DataFrame, params: dict) -> dict:
    train_df, test_df = split_data(df, params)
    model = train_model(train_df, params)
    return evaluate_model(model, test_df, params["data"]["target"])


def test_split_is_seeded_and_disjoint():
    df = _synthetic_housing()
    params = _small_params()
    train1, test1 = split_data(df, params)
    train2, test2 = split_data(df, params)
    assert train1.index.equals(train2.index)
    assert test1.index.equals(test2.index)
    assert train1.index.intersection(test1.index).empty
    assert len(test1) == int(len(df) * params["split"]["test_size"])


def test_pipeline_returns_metrics():
    metrics = _run_pipeline(_synthetic_housing(), _small_params())
    assert set(metrics) == {"rmse", "mae", "r2"}
    assert metrics["rmse"] >= 0


def test_pipeline_is_deterministic():
    df = _synthetic_housing()
    assert _run_pipeline(df, _small_params()) == _run_pipeline(df, _small_params())
