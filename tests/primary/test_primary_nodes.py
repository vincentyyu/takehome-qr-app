from pandas.testing import assert_frame_equal

from src.primary.nodes import enrich_int_data, keep_latest_data


def test_keep_latest_data(mock_int_price_data, expected_latest_price_data):
    group_cols = ["company_name", "date"]
    timestamp_col = "timestamp"

    result = keep_latest_data(mock_int_price_data, group_cols, timestamp_col)
    assert_frame_equal(result, expected_latest_price_data)


def test_enrich_int_data(
    mock_int_price_data,
    mock_sec_master_data,
    expected_pri_price_data,
):
    group_cols = ["company_name", "id", "date"]
    timestamp_col = "timestamp"

    result = enrich_int_data(
        mock_int_price_data,
        mock_sec_master_data,
        group_cols,
        timestamp_col,
    )
    assert_frame_equal(result, expected_pri_price_data)
