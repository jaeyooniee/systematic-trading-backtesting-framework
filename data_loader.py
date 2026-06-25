"""
Very good description about How to use FredAPI on 'https://mortada.net/python-api-for-fred.html'
Currently, the file is more like getting familiar with the APIs.

"""

import yfinance as yf
import pandas as pd
from fredapi import Fred


FRED_API_KEY = "4d956eea01967253c50032abe3cf6091"     # FRED requires personal key to access the data
fred = Fred(api_key=FRED_API_KEY)                     # Initialising

TBILL = 'DTB3'                                        # We are using 3-months 

def sync_date(ticker, start_date='2015-01-01', end_date='2019-12-31'):
    price_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)  # stores specific ticker's price information within the given time period
    tbill_annual_rate = fred.get_series(TBILL, observation_start=start_date, observation_end=end_date)  # Getting t-bill rate from FRED

    price_data.columns = price_data.columns.droplevel('Ticker')

    price_df = price_data[['Open', 'High', 'Low', 'Close']]  # We need OHLC (not volume)
    price_df.index = pd.to_datetime(price_df.index).normalize()

    tbill_daily_rate = tbill_annual_rate.reindex(price_df.index).ffill() / 100 / 252

    # normalisation: defensive measure to strip any time component and ensure timestamps compatibility
    # reindex: FRED and NYSE have different holidays  

    return price_df, tbill_daily_rate
