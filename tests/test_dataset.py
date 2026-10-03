import pandas as pd

from src.dataset import drop_capped_target


def test_drop_capped_target_removes_cap_rows():
    df = pd.DataFrame({"MedHouseVal": [1.0, 4.99, 5.0, 5.00001]})
    assert drop_capped_target(df)["MedHouseVal"].tolist() == [1.0, 4.99]
