from multiprocessing import Pool
from pathlib import Path

from .nodes import preprocess_raw_data


def run_intermediate_pipeline() -> None:
    # TODO: with a proper config parser, the filepaths
    # and parameters below should be controlled via
    # conf/catalog.yml and conf/parameters.yml
    raw_dir = Path("data/01_raw")
    int_dir = Path("data/02_intermediate")

    # Create intermediate directory if it doesn't exist
    int_dir.mkdir(parents=True, exist_ok=True)

    # Declare each step to preprocess raw data into intermediate data
    steps = [
        dict(
            input=raw_dir / "consumer.csv",
            output=int_dir / "consumer.feather",
            rename={
                "CreditCardSpend": "Credit Card Spend",
                "TransactionCount": "Transaction Count",
            },
            datetime_cols=["Date", "Timestamp"],
        ),
        dict(
            input=raw_dir / "prices.csv",
            output=int_dir / "prices.feather",
            datetime_cols=["Date", "Timestamp"],
        ),
        dict(
            input=raw_dir / "web.csv",
            output=int_dir / "web.feather",
            rename={
                "WebsiteVisits": "Website Visits",
            },
            datetime_cols=["Date", "Timestamp"],
        ),
        dict(
            input=raw_dir / "sec_master.csv",
            output=int_dir / "sec_master.feather",
            rename={
                "CompanyName": "Company Name",
            },
        ),
    ]

    # Leverage parallel processing
    with Pool() as pool:
        pool.map(preprocess_raw_data, steps)


if __name__ == "__main__":
    run_intermediate_pipeline()
