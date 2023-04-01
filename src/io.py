"""
Helper functions to facilitate pipeline building
"""

from typing import Any, Dict

import pandas as pd


def run_node(args: Dict[str, Any]) -> None:
    # Unpack paths and params
    function, inputs, output = (
        args.pop("function"),
        args.pop("inputs"),
        args.pop("output"),
    )
    kwargs = args

    # Collect all input dataframes
    dfs = [pd.read_feather(input_path) for input_path in inputs]

    # Call function to process data
    processed_df = function(*dfs, **kwargs)

    # Save data to local
    processed_df.to_feather(output)
