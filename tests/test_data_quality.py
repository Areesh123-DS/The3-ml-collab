from pathlib import Path

import pandas as pd

from src.dataset import MAX_TARGET

SAMPLE = Path(__file__).parent / "fixtures" / "sample_housing.csv"

COLUMNS = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
    "MedHouseVal",
]


def _load() -> pd.DataFrame:
    return pd.read_csv(SAMPLE)


def test_schema_matches_expected_columns():
    assert list(_load().columns) == COLUMNS


def test_no_null_values():
    assert int(_load().isna().sum().sum()) == 0


def test_values_within_expected_ranges():
    df = _load()
    assert df["MedInc"].between(0, 16).all()
    assert df["HouseAge"].between(1, 52).all()
    assert (df["AveRooms"] > 0).all()
    assert (df["AveBedrms"] > 0).all()
    assert (df["Population"] > 0).all()
    assert (df["AveOccup"] > 0).all()
    assert df["Latitude"].between(32, 43).all()
    assert df["Longitude"].between(-125, -114).all()


def test_target_is_positive_and_below_cap():
    target = _load()["MedHouseVal"]
    assert (target > 0).all()
    assert (target < MAX_TARGET).all()
