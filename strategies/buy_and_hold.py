import pandas as pd


def signal(price_df):
    return pd.Series(1, index=price_df.index)