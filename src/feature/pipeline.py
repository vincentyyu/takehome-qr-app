from pathlib import Path

from src.io import run_node

from .nodes import fea_aggregate, fea_join_all


def run_feature_pipeline() -> None:
    # TODO: with a proper config parser, the filepaths
    # and parameters below should be controlled via
    # conf/catalog.yml and conf/parameters.yml
    pri_dir = Path("data/03_primary")
    fea_dir = Path("data/04_feature")

    # Create intermediate directory if it doesn't exist
    fea_dir.mkdir(parents=True, exist_ok=True)

    # TODO: with better pipeline design (extra classes and helper functions)
    # this can be mitigated by checking inter-node dependencies

    # Declare each step to create additional feature layer datasets
    steps = [
        dict(
            function=fea_join_all,
            inputs=[
                pri_dir / "consumer.feather",
                pri_dir / "prices.feather",
                pri_dir / "web.feather",
            ],
            output=fea_dir / "master_df.feather",
        ),
        dict(
            function=fea_aggregate,
            inputs=[fea_dir / "master_df.feather"],
            output=fea_dir / "agg_by_freq.feather",
            frequencies=["Y", "Q", "M", "W", "D"],
        ),
    ]

    # Instead of parallel runs, this time it's sequential due to
    # node dependencies
    for step in steps:
        run_node(step)


if __name__ == "__main__":
    run_feature_pipeline()
