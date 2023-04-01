import pandas as pd
import pytest


@pytest.fixture
def mock_int_price_data():
    data = {
        "id": [1, 1, 1, 1, 1],
        "company_name": ["Company A" for _ in range(5)],
        "date": pd.to_datetime(["2023-01-01" for _ in range(5)]),
        "timestamp": pd.date_range("2023-01-01", periods=5, freq="D"),
        "price_value": [100, 200, 300, 400, 500],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def mock_sec_master_data():
    data = {
        "id": [1, 2, 3],
        "company_name": ["Company A", "Company B", "Company C"],
        "symbol": ["CMPA", "CMPB", "CMPC"],
    }
    sec_master_df = pd.DataFrame(data)
    return sec_master_df


@pytest.fixture
def expected_latest_price_data():
    data = {
        "id": [1],
        "company_name": ["Company A"],
        "date": pd.to_datetime(["2023-01-01"]),
        "price_value": [500],
    }
    df = pd.DataFrame(data)
    return df


@pytest.fixture
def expected_pri_price_data():
    data = {
        "id": [1],
        "company_name": ["Company A"],
        "date": pd.to_datetime(["2023-01-01"]),
        "price_value": [500],
        "symbol": ["CMPA"],
    }
    df = pd.DataFrame(data)
    return df
