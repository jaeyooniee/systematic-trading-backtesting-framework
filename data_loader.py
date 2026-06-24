"""
Very good description about How to use FredAPI on 'https://mortada.net/python-api-for-fred.html'
Currently, the file is more like getting familiar with the APIs.

"""


import yfinance as yf
import pandas as pd
from fredapi import Fred
import matplotlib.pyplot as plt

ticker = input("INPUT TICKER = ")
price_data = yf.download(ticker, start="2015-01-01", end="2019-12-31", auto_adjust=True)

fred = Fred(api_key='4d956eea01967253c50032abe3cf6091')

tbill_data = fred.get_series('DTB3', observation_start='2015-01-01', observation_end='2019-12-31')
tbill_info = fred.get_series_info('DTB3')

print(tbill_info['title'])

df = pd.DataFrame({'DTB3', tbill_data})
df = df.dropna()
df.plot()

plt.show()