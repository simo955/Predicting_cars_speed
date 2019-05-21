import numpy as np
import pandas as pd

def discretize_timestamp(df, col_name, step=15*60, rename_col=None):
    """
    Discretize a dataframe datetime column.
    df (dataframe):     dataframe
    col_name (str):     name of the datetime column
    step (int):         interval of discretization
    rename_col (str):   name of the new column, None to replace the old one
    """
    unix_timestamps = df[col_name].astype('int64') // 10**9 #s
    remainders = unix_timestamps % step
    if isinstance(rename_col, str):
        df[rename_col] = pd.to_datetime(unix_timestamps - remainders + step, unit='s')
    else:
        df[col_name] = pd.to_datetime(unix_timestamps - remainders + step, unit='s')
    return df