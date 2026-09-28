from src.modeling.train import DEFAULT_PARAMS, load_params


def test_params_file_has_required_keys():
    params = load_params(DEFAULT_PARAMS)
    assert isinstance(params["seed"], int)
    assert 0 < params["split"]["test_size"] < 1
    assert params["train"]["n_estimators"] > 0
    assert params["data"]["target"] == "MedHouseVal"
