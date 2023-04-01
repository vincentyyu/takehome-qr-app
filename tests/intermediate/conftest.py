import pandas as pd
import pytest


@pytest.fixture
def uncleaned_df():
    data = {
        "Unnamed: 0": [1, 2, 3],
        "Col_1": [4, 5, 6],
        "Colümn-2": [7, 8, 9],
        "Col 3": [10, 11, 12],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def mock_raw_price_data():
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Date": ["2023-01-01" for _ in range(5)],
        "TimeStamp": pd.date_range("2023-01-01", periods=5, freq="D"),
        "value": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def expected_int_price_data():
    data = {
        "id": [1, 2, 3, 4, 5],
        "date": pd.to_datetime(["2023-01-01" for _ in range(5)]),
        "timestamp": pd.date_range("2023-01-01", periods=5, freq="D"),
        "price_value": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)
    return df
