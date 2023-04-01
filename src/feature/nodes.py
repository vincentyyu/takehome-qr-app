"""
Feature layer preprocessing script.

The main purpose of feature layer pipeline is
feature engineering, which includes correlation
calculations and time-series aggregations

Usually there's a downstream layer, model input layer,
to further merge the data for data science purposes, but
given we are directly serving the reporting layer,
this is the last step of the DE pipeline
"""

from typing import List

import pandas as pd


def fea_join_all(
    pri_consumer: pd.DataFrame, pri_prices: pd.DataFrame, pri_web: pd.DataFrame
) -> pd.DataFrame:
    """
    Join consumer, prices, and web data together into a master DataFrame.

    :param pri_consumer: DataFrame containing primary layer consumer data
    :param pri_prices: DataFrame containing primary layer prices data
    :param pri_web: DataFrame containing primary layer web data
    :return: A master DataFrame containing all input data,
        sorted by company_name and date
    """
    # Remove duplicated columns and join keys
    duplicated_cols = ["company_name", "symbol", "price_id", "web_id"]
    pri_prices.drop(columns=duplicated_cols, inplace=True)
    pri_web.drop(columns=duplicated_cols, inplace=True)

    # Merge all data together and leave it to reporting layer for filtering
    join_cols = ["consumer_id", "date"]
    master_df = pri_consumer.merge(pri_prices, how="inner", on=join_cols).merge(
        pri_web, how="inner", on=join_cols
    )

    # Remove redundant columns
    master_df.drop(columns=["price_id", "web_id", "consumer_id"], inplace=True)

    return master_df.sort_values(["company_name", "date"]).reset_index(drop=True)


def fea_aggregate(master_df: pd.DataFrame, frequencies: List[str]) -> pd.DataFrame:
    """
    Aggregate the master DataFrame at specified frequencies and
        add datetime indicators for reporting purposes.

    :param master_df: The master DataFrame containing all data
    :param frequencies: List of aggregation frequencies, e.g., ['Y', 'Q', 'M', 'W']
    :return: The aggregated DataFrame, sorted by company_name, agg_freq, and date
    """
    # Gather each dataframe aggregated at each frequency
    agg_dfs = [_aggregate_by_freq(master_df, freq) for freq in frequencies]

    # Union all individual dataframes
    unioned_df = pd.concat(agg_dfs, ignore_index=True)

    # Add several datetime indicators for reporting purposes
    unioned_df = _add_datetime_indicators(unioned_df)

    return unioned_df.sort_values(["company_name", "agg_freq", "date"]).reset_index(
        drop=True
    )


def _aggregate_by_freq(df: pd.DataFrame, freq: str = "M") -> pd.DataFrame:
    """
    Aggregate a DataFrame based on a specified frequency.

    :param df: The input DataFrame
    :param freq: The aggregation frequency (default: 'M' for monthly)
    :return: The aggregated DataFrame with an additional column
        indicating the aggregation frequency
    """
    # Use grouper to aggregate on yearly, quaterly, monthly, weekly, or daily bases
    agg_df = (
        df.groupby([pd.Grouper(key="date", freq=freq), "company_name", "symbol"])
        .agg(["mean", "sum", "min", "max"])
        .reset_index()
    )

    # Flatten columns
    agg_df.columns = [
        "_".join(col).strip() if col[-1] != "" else col[0]
        for col in agg_df.columns.values
    ]

    # Indicate frequency for filtering
    agg_df["agg_freq"] = freq

    return agg_df


def _add_datetime_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add datetime indicators to the input DataFrame.

    :param df: The input DataFrame
    :return: The DataFrame with additional datetime columns for easier filtering
    :raises KeyError: If 'agg_freq' is not present in the input DataFrame
    """
    # Check if agg_freq is in dataframe or not
    if "agg_freq" not in df.columns:
        raise KeyError("Column `agg_freq` not present in dataframe. Unable to proceed")

    # Create some additional datetime columns for easier filtering later
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    # Prevent beginning of year being the last week via isocalendar
    df["week"] = df["date"].dt.strftime("%U")

    # Create Labeling for readability
    label_format_map = {
        "Y": lambda row: f"{row['year']}",
        "Q": lambda row: f"{row['year']} Q{row['quarter']}",
        "M": lambda row: f"{row['year']} M{row['month']}",
        "W": lambda row: f"{row['year']} W{row['week']}",
    }

    df["dt_label"] = df.apply(
        lambda row: label_format_map.get(row["agg_freq"])(row)
        if row["agg_freq"] in label_format_map
        else row["date"].strftime("%m/%d/%Y"),
        axis=1,
    )

    return df
