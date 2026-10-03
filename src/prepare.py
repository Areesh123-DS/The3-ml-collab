"""Stage 1: split the raw dataset into fixed train and test files."""

from pathlib import Path

from loguru import logger
import pandas as pd
from sklearn.model_selection import train_test_split
import typer

from src.config import DEFAULT_PARAMS, PROJ_ROOT, TEST_PATH, TRAIN_PATH, load_params
from src.features import add_bedroom_ratio

app = typer.Typer()


def split_data(df: pd.DataFrame, params: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Seeded split. Any preprocessing must be fit on the train part only, later."""
    return train_test_split(
        df,
        test_size=params["split"]["test_size"],
        random_state=params["seed"],
    )


@app.command()
def main(
    params_path: Path = DEFAULT_PARAMS,
    input_path: Path | None = None,
    train_path: Path = TRAIN_PATH,
    test_path: Path = TEST_PATH,
):
    params = load_params(params_path)
    input_path = input_path or PROJ_ROOT / params["data"]["raw_path"]

    df = pd.read_csv(input_path)
    # Row-wise ratio, nothing is fit, so adding it before the split cannot leak test data
    if params["features"]["bedroom_ratio"]:
        df = add_bedroom_ratio(df)
    train_df, test_df = split_data(df, params)

    # Fixed "\n" so the outputs (and their DVC hashes) are identical on Windows and Linux
    train_path.parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(train_path, index=False, lineterminator="\n")
    test_df.to_csv(test_path, index=False, lineterminator="\n")
    logger.success(f"Train: {len(train_df)} rows -> {train_path}")
    logger.success(f"Test: {len(test_df)} rows -> {test_path}")


if __name__ == "__main__":
    app()
