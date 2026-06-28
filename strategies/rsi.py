import pandas as pd
from strategies.helpers import safe_divide, stateful_signal

"""
RSI based long-only strategy.
Computes RSI(14), enters when RSI < 30 and exits when RSI > 70
Holds the position in between. 

"""

PERIOD = 14

def calculate_rsi(close) -> pd.Series:
    delta = close.diff()         # daily change
    gain = delta.clip(lower=0)   # gain >= 0
    loss = -delta.clip(upper=0)  # less <= 0

    # Wilder smoothing: ewm with alpha=1/PERIOD, adjust=False => recursive
    average_gain = gain.ewm(alpha=1/PERIOD, min_periods=PERIOD, adjust=False).mean()
    average_loss = loss.ewm(alpha=1/PERIOD, min_periods=PERIOD, adjust=False).mean()

    rs = safe_divide(average_gain, average_loss)

    return 100 - (100 / (1 + rs))


def signal(price_df) -> pd.Series:
    close = price_df["Close"]
    rsi = calculate_rsi(close)

    return stateful_signal(rsi < 30, rsi > 70)