from pandas.testing import assert_frame_equal

from src.feature.nodes import fea_aggregate, fea_join_all


def test_fea_join_all(pri_consumer, pri_prices, pri_web, master_df):
    result = fea_join_all(pri_consumer, pri_prices, pri_web)
    assert_frame_equal(result, master_df)


def test_fea_aggregate(master_df, master_df_agg):
    frequencies = ["Y", "Q", "M", "W"]
    result = fea_aggregate(master_df, frequencies)

    assert_frame_equal(result, master_df_agg)
