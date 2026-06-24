"""
Very good description about How to use FredAPI on 'https://mortada.net/python-api-for-fred.html'
Currently, the file is more like getting familiar with the APIs.

"""


import yfinance as yf
import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt

FRED_API_KEY = "4d956eea01967253c50032abe3cf6091"
fred = Fred(api_key=FRED_API_KEY)

TBILL = 'DTB3'

def sync_date(ticker, start_date='2015-01-01', end_date='2019-12-31'):
    price_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    rf_data = fred.get_series(TBILL, observation_start=start_date, observation_end=end_date)

    price_df = price_data[['Close']]
    price_df.index = pd.to_datetime(price_df.index)
    price_df.index = price_df.index.normalize()

    print(price_df)

sync_date("AAPL")
