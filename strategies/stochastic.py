import pandas as pd
from strategies.helpers import safe_divide, stateful_signal

"""
Slow Stochastic based long-only strategy.
Computes the Slow Stochastic %K over a 14-day range (raw %K smoothed by 3)
Enters when %K < 20 and exits when %K > 80.
Holds the position in between.

"""

LOOKBACK = 14  # range window for highest-high / lowest-low
SMOOTH_K = 3   # smoothing applied to raw %K to get the slow %K


def signal(price_df) -> pd.Series:
    # Recent 14-day price range (lowest low and highest high)
    lowest_low = price_df["Low"].rolling(LOOKBACK, min_periods=LOOKBACK).min()
    highest_high = price_df["High"].rolling(LOOKBACK, min_periods=LOOKBACK).max()

    # raw %K: where the close sits within the range (0 = low, 100 = high)
    fast_k = 100 * safe_divide(price_df["Close"] - lowest_low, highest_high - lowest_low)
    # slow %K: raw %K smoothed over 3 days
    slow_k = fast_k.rolling(SMOOTH_K, min_periods=SMOOTH_K).mean()

    # %K < 20 to enter (oversold), %K > 80 to exit (overbought)
    return stateful_signal(slow_k < 20, slow_k > 80)