"""
Intermediate layer preprocessing script.

The main purpose of intermediate layer pipeline is to
pre-clean the raw data and convert incorrectly read-in
data types to the correct data types (e.g., string to datetime).

More complicated cleanup should be left to primary layer.
"""
from typing import Any, Dict, List, Optional

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the column names of a DataFrame.

    :param df: Input DataFrame with unclean column names.
    :return: DataFrame with cleaned column names.
    """
    # Drop unnamed index column if any
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)

    # Clean up column names
    df.columns = (
        # Apply lower case conversion
        df.columns.str.lower()
        # Convert non-ASCII chars to ASCII only
        .str.normalize("NFD")
        .str.encode("ascii", "ignore")
        .str.decode("ascii")
        # Replace non-word/number char with space
        .str.replace(r"[^A-Za-z0-9]", " ", regex=True)
        # Remove trailing spaces
        .str.strip()
        # Reaplce multiple spaces with underscore
        .str.replace(r"\s+", "_", regex=True)
    )

    return df


def preprocess(
    df: pd.DataFrame,
    rename: Optional[Dict[str, str]] = None,
    datetime_cols: Optional[List[str]] = [],
) -> pd.DataFrame:
    """
    Preprocesses a DataFrame by cleaning up column names,
    dropping duplicates, renaming columns, and converting
    datetime columns.

    :param df: Input raw DataFrame to preprocess.
    :param rename: Optional dictionary mapping original column names to new names.
    :param datetime_cols: Optional list of column names to be converted to datetime.
    :return: Intermediate level DataFrame.
    """
    # Drop duplicated columns and rows if any
    df = df.loc[:, ~df.columns.duplicated()]
    df.drop_duplicates(inplace=True)

    # Rename columns if any specified
    if rename:
        df.rename(columns=rename, inplace=True)

    # Conduct datetime casting with original column names first
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col])

    # Clean up column names
    df_cleaned = clean_column_names(df)

    return df_cleaned


def preprocess_raw_data(args: Dict[str, Any]) -> None:
    """
    Reads in raw data from a CSV file, preprocesses it,
    and saves the preprocessed data as a Feather file.

    :param args: Dictionary containing input and output
    file paths, and optional rename and datetime_cols arguments.
    """
    # Unpack input and output paths
    input, output = args.pop("input"), args.pop("output")

    # TODO: with logging configured, should pair with `try` block
    # to catch situations where file doesn't exist (FileNotFoundError)
    raw_df = pd.read_csv(input)
    int_df = preprocess(raw_df, **args)
    int_df.to_feather(output)
