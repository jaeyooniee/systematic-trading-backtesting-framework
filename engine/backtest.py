import pandas as pd

def run(price_df, signal_function, rf_daily, cost_pct=0):
    signal = signal_function(price_df)
    position = signal.shift(1)
    daily_returns = price_df['Close'].pct_change()

    returns = position * daily_returns
    trades = position.diff().abs()
    returns = returns - trades * cost_pct / 100      # 거래비용 차감된 raw 전략 수익률

    excess = returns - rf_daily                       # excess

    return returns, excess