from multiprocessing import Pool
from pathlib import Path

from src.io import run_node

from .nodes import enrich_int_data


def run_primary_pipeline() -> None:
    # TODO: with a proper config parser, the filepaths
    # and parameters below should be controlled via
    # conf/catalog.yml and conf/parameters.yml
    int_dir = Path("data/02_intermediate")
    pri_dir = Path("data/03_primary")

    # Create primary directory if it doesn't exist
    pri_dir.mkdir(parents=True, exist_ok=True)

    # Declare each step to enrich intermediate data
    # into primary layer data
    steps = [
        dict(
            function=enrich_int_data,
            inputs=[int_dir / "consumer.feather", int_dir / "sec_master.feather"],
            output=pri_dir / "consumer.feather",
            group_cols=["consumer_id", "date"],
        ),
        dict(
            function=enrich_int_data,
            inputs=[int_dir / "prices.feather", int_dir / "sec_master.feather"],
            output=pri_dir / "prices.feather",
            group_cols=["price_id", "date"],
        ),
        dict(
            function=enrich_int_data,
            inputs=[int_dir / "web.feather", int_dir / "sec_master.feather"],
            output=pri_dir / "web.feather",
            group_cols=["web_id", "date"],
        ),
    ]

    # Leverage parallel processing
    with Pool() as pool:
        pool.map(run_node, steps)


if __name__ == "__main__":
    run_primary_pipeline()
