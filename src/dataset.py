from pathlib import Path

from loguru import logger
from sklearn.datasets import fetch_california_housing
import typer

from src.config import RAW_DATA_DIR

app = typer.Typer()


def download(output_path: Path) -> Path:
    """Fetch California Housing from scikit-learn and save it as a raw CSV."""
    df = fetch_california_housing(as_frame=True).frame
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
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
