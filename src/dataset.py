from pathlib import Path

from loguru import logger
import pandas as pd
from sklearn.datasets import fetch_california_housing
import typer

from src.config import RAW_DATA_DIR

app = typer.Typer()

MAX_TARGET = 5.0


def drop_capped_target(df: pd.DataFrame, target: str = "MedHouseVal") -> pd.DataFrame:
    """Remove rows whose target sits at the dataset's $500k cap."""
    return df[df[target] < MAX_TARGET].reset_index(drop=True)


def download(output_path: Path) -> Path:
    """Fetch California Housing from scikit-learn, drop capped labels and save a raw CSV."""
    df = drop_capped_target(fetch_california_housing(as_frame=True).frame)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, lineterminator="\n")
    return output_path


@app.command()
def main(
    output_path: Path = RAW_DATA_DIR / "california_housing.csv",
):
    logger.info("Downloading California Housing dataset...")
    download(output_path)
    logger.success(f"Saved raw dataset to {output_path}")


if __name__ == "__main__":
    app()
