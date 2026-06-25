import pandas as pd

def run(price_df, signal_function, cost_bps=0) -> pd.Series:
    signal = signal_function(price_df)              # signal: 1(long) / 0(out)
    position = signal.shift(1)                      # avoid looking ahead
    daily_returns = price_df['Close'].pct_change()  
    returns = position * daily_returns              

    return returns