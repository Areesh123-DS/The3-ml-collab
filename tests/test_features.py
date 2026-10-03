import pandas as pd
import pytest

from src.features import add_bedroom_ratio


def test_add_bedroom_ratio_values():
    df = pd.DataFrame({"AveRooms": [4.0, 5.0], "AveBedrms": [1.0, 2.0]})
    result = add_bedroom_ratio(df)
    assert result["BedroomRatio"].tolist() == pytest.approx([0.25, 0.4])


def test_add_bedroom_ratio_does_not_modify_input():
    df = pd.DataFrame({"AveRooms": [4.0], "AveBedrms": [1.0]})
    add_bedroom_ratio(df)
    assert "BedroomRatio" not in df.columns


def test_add_bedroom_ratio_keeps_rows_and_existing_columns():
    df = pd.DataFrame(
        {"MedInc": [8.3, 7.2, 5.6], "AveRooms": [6.9, 6.2, 8.3], "AveBedrms": [1.0, 0.9, 1.1]},
        index=[10, 20, 30],
    )
    result = add_bedroom_ratio(df)
    assert list(result.columns) == ["MedInc", "AveRooms", "AveBedrms", "BedroomRatio"]
    assert result.index.tolist() == [10, 20, 30]
    pd.testing.assert_frame_equal(result[df.columns], df)
