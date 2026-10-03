import numpy as np
import pandas as pd

from src.modeling.train import load_params, train_and_evaluate

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


def test_train_returns_metrics():
    _, metrics = train_and_evaluate(_synthetic_housing(), _small_params())
    assert set(metrics) == {"rmse", "mae", "r2"}
    assert metrics["rmse"] >= 0


def test_training_is_deterministic():
    df = _synthetic_housing()
    _, m1 = train_and_evaluate(df, _small_params())
    _, m2 = train_and_evaluate(df, _small_params())
    assert m1 == m2
