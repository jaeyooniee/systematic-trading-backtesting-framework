import pandas as pd

"""
MACD based long-only strategy.
Computes MACD(12, 26, 9): the difference between the 12- and 26-day EMAs,
with a 9-day EMA signal line. Holds long position (1) whenever the MACD
line is above its signal line, otherwise stays in cash (0). 
The position each day depends only on that day's MACD vs signal.

"""

# Standard MACD hyperparameters (most commonly used)
FAST = 12     # short EMA span
SLOW = 26     # long EMA span
SIGNAL = 9    # signal-line EMA span


def signal(price_df) -> pd.Series:
    close = price_df["Close"]

    # EMAs (adjust=False -> recursive EMA, the standard MACD definition)
    ema_fast = close.ewm(span=FAST, min_periods=FAST, adjust=False).mean()
    ema_slow = close.ewm(span=SLOW, min_periods=SLOW, adjust=False).mean()

    macd = ema_fast - ema_slow                                                    # MACD line
    macd_signal = macd.ewm(span=SIGNAL, min_periods=SIGNAL, adjust=False).mean()  # signal line

    # Long (1) when MACD is above signal, else cash (0). no signal -> stateless.
    return (macd > macd_signal).fillna(False).astype(int)