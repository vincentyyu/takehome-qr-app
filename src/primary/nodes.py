"""
Primary layer nodes.

The main purpose of primary layer pipeline is to
further clean up and enrich the data, which includes
correcting data accuracy, joining additional info, etc.

Feature engineering, such as calculating correlations, etc.,
should be left for feature layer
"""

from typing import List

import pandas as pd


def keep_latest_data(
    df: pd.DataFrame, group_cols: List[str], timestamp_col: str = "timestamp"
) -> pd.DataFrame:
    """
    Keep only the latest data for each group based on the specified timestamp column.

    :param df: The input DataFrame
    :param group_cols: List of column names to group by
    :param timestamp_col: The name of the timestamp column (default: 'timestamp')
    :return: The DataFrame with only the latest data for each group
    :raises KeyError: If required columns are missing from the input DataFrame
    """
    # Check if the dataset has the required columns
    required_columns = group_cols + [timestamp_col]
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise KeyError(f"DataFrame is missing the following columns: {missing_columns}")

    # Sort by timestamp and keep the latest
    latest_df = (
        df.sort_values(timestamp_col)
        .drop_duplicates(subset=group_cols, keep="last")
        .drop(columns=timestamp_col)
        .reset_index(drop=True)
    )

    return latest_df


def enrich_int_data(
    int_df: pd.DataFrame,
    int_sec_master: pd.DataFrame,
    group_cols: List[str],
    timestamp_col: str = "timestamp",
) -> pd.DataFrame:
    """
    Enrich the input DataFrame with company info from the sec master.

    :param int_df: The input DataFrame
    :param int_sec_master: The intermediate sec master DataFrame
    :param group_cols: List of column names to group by
    :param timestamp_col: The name of the timestamp column (default: 'timestamp')
    :return: The enriched DataFrame
    """
    # Keep only the latest data based on timestamp column
    df = keep_latest_data(int_df, group_cols, timestamp_col)

    # Remove date column before joining
    group_cols.remove("date")

    # Enrich dataframe with sec master info
    enriched_df = df.merge(int_sec_master, how="left", on=group_cols)

    return enriched_df
