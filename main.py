import pandas as pd
import data_loader
import engine.backtest as backtest
import strategies.buy_and_hold as buy_and_hold
import validation.acf as acf

ticker = input("INPUT TICKER: ")
price_df, tbill_daily_rate = data_loader.sync_date(ticker)

print(price_df, tbill_daily_rate)

"""

returns = backtest.run(price_df, buy_and_hold.signal)
excess = returns - tbill_daily_rate

acf_values, confidence_band = acf.compute_acf(excess)
block_length = acf.get_block_length(acf_values, confidence_band)
print("추천 블록 길이:", block_length)
acf.plot_acf(acf_values, confidence_band)
"""
