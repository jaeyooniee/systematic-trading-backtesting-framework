import pandas as pd
from strategies.helpers import stateful_signal

"""
Bollinger Band based long-only strategy.
Computes a 20-day moving average with +-2 standard deviation bands, 
Enters when price closes below the lower band,
Exits when it closes above the middle band. 
Holds the position in between.
"""

WINDOW = 20
WIDTH = 2

def signal(price_df) -> pd.Series:
    close = price_df["Close"]

    middle_band = close.rolling(WINDOW, min_periods=WINDOW).mean()      # 20-day moving average
    rolling_sd = close.rolling(WINDOW, min_periods=WINDOW).std(ddof=0)  # population standard deviation, the definition uses population SD.

    lower_band = middle_band - WIDTH * rolling_sd                     # lower band only (entry trigger)

    # Close < lower band to enter, Close > middle band to exit (mean reversion)
    return stateful_signal(close < lower_band, close > middle_band)