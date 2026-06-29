import pandas as pd

"""
Parabolic SAR based long-only strategy.
Computes Wilder's Parabolic SAR (step 0.02, max 0.20), which trails price and
flips when price crosses it. 
Holds a long position (1) while the trend is bullish (price above SAR) and stays in cash (0) while bearish.

Algorithm reference: J. Welles Wilder Jr. (1978), New Concepts in Technical Trading Systems.

"""

STEP = 0.02     # acceleration factor step (and its initial value)
MAX_STEP = 0.2  # acceleration factor cap


def calculate_psar(high, low, close, step=STEP, max_step=MAX_STEP) -> pd.Series:
    """Compute the PSAR trend direction (1 = bullish, -1 = bearish) per bar."""

    frame = pd.concat({"high": high, "low": low, "close": close}, axis=1).dropna()
    highs = list(frame["high"])
    lows = list(frame["low"])
    closes = list(frame["close"])
    length = len(frame)

    psar = closes[:]      # start psar as a copy of close
    trend = [0] * length  # 1 = bullish, -1 = bearish
    bull = True           # current trend direction
    af = step             # acceleration factor (grows as the trend extends)
    ep = highs[0]         # extreme point (best price reached in current trend)

    for i in range(2, length):
        # move SAR toward the extreme point by the acceleration factor
        psar[i] = psar[i - 1] + af * (ep - psar[i - 1])
        reverse = False  # whether the trend flips on this bar

        if bull:
            if lows[i] < psar[i]:  # price broke below SAR -> turn bearish
                bull = False
                reverse = True
                psar[i] = ep       # SAR jumps to the prior extreme point
                ep = lows[i]       # reset extreme point to current low
                af = step          # reset acceleration factor

        else:
            if highs[i] > psar[i]:  # price broke above SAR -> turn bullish
                bull = True
                reverse = True
                psar[i] = ep
                ep = highs[i]
                af = step

        # only when no flip occurred: update extreme point / accelerate / clamp SAR
        if not reverse:
            if bull:
                if highs[i] > ep:   # new high -> extend trend, accelerate
                    ep = highs[i]
                    af = min(af + step, max_step)

                # SAR cannot exceed the prior two lows
                psar[i] = min(psar[i], lows[i - 1], lows[i - 2])

            else:
                if lows[i] < ep:    # new low -> extend trend, accelerate
                    ep = lows[i]
                    af = min(af + step, max_step)

                # SAR cannot fall below the prior two highs
                psar[i] = max(psar[i], highs[i - 1], highs[i - 2])

        trend[i] = 1 if bull else -1

    return pd.Series(trend, index=frame.index)


def signal(price_df) -> pd.Series:
    """Return the PSAR strategy's 0/1 signal from an OHLC prices."""

    trend = calculate_psar(price_df["High"], price_df["Low"], price_df["Close"])
    raw = (trend == 1).astype(int)  # bullish -> 1 (hold), else 0 (cash)

    # restore the original index (calculate_psar dropped leading NaN rows)
    return raw.reindex(price_df.index, fill_value=0)