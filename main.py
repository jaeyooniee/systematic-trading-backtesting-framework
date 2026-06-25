import pandas as pd
import data_loader
import engine.backtest as backtest
import strategies.buy_and_hold as buy_and_hold

ticker = input("INPUT TICKER: ")
price_df, tbill_daily_rate = data_loader.sync_date(ticker)

engine_returns = backtest.run(price_df, buy_and_hold.signal)
manual_returns = price_df['Close'].pct_change()

diff = (engine_returns - manual_returns).abs()

print("max diff = ", diff.max())
print("valid?: ", diff.max() < 1e-10)