from pandas.testing import assert_frame_equal

from src.intermediate.nodes import clean_column_names, preprocess


def test_clean_column_names(uncleaned_df):
    result = clean_column_names(uncleaned_df)
    assert result.columns.to_list() == ["col_1", "column_2", "col_3"]


def test_preprocess(mock_raw_price_data, expected_int_price_data):
    rename = {"value": "Price Value"}
    datetime_cols = ["Date", "TimeStamp"]

    result = preprocess(mock_raw_price_data, rename, datetime_cols)
    assert_frame_equal(result, expected_int_price_data)
