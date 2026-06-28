# Systematic Trading Strategies Backtesting Framework

The project aims to backtest 5 well-known strategies when trading a single US equity.
I focused on getting statistically plausible results which are justified by statistic tests.
The framework ultimately reveals whether the strategies show statistically plausible differences in their **sharpe ratio**.

> **The goal is not to find the highest profitable strategy but to successfully claim that 
> one strategy did show higher returns than the others. It is about answering to a methodological question.
> ** Therefore, the crucial point of the evaluation is focused on the statistical strictness of comparation.

---

## 0. Journey of the Project (From Start to the End)
This part will illustrate the whole steps of **how I started this project and what process I have gone through to get to the results** chronologically. 

### 0.1 Start off (What am I building exactly?)
From my deep interest in quantitative finance field, I first thought of building a trading strategies backtesting framework. Firstly, I chose the identities: **Not "Finding the best strategy" but the "Methodology that statistically justifies the comparation of the strategies"**.

In addition, I decided to build a vectorisation engine other than importing already built libraries. The big picture of the framework (e.g. pairwise comparing 5 strategies in a single stock, sharpe ratio as the main indicator, T-bill as rf ...) was drawed at this stage.

### 0.2 Selection of strategies 
I have collected trading strategies without any bias from [QuantConnect](https://www.quantconnect.com/research/), [TradingView](https://www.tradingview.com/), Peng Liu's [Quantitative Trading Strategies Using Python](https://link.springer.com/book/10.1007/978-1-4842-9675-2). Multiple equities and cross-sectional strategies were omitted since the framework I planned was only focusing on trading one stock. 

### 0.3 Choosing Data Source
I had two options for getting price data.
1. Polygon
2. yfinance

However, Polygon has been rebranded and now restricts some past data so I chose to implement **yfinance**.
Risk-free rate was selected as **FRED DTB3** (3-Month Treasury Bill Secondary Market Rate).

### 0.4 Setting final 5 strategies 
I changed strategies quite a few times before I do the code part.
- First, the sets were "MACD, Donchian, PSAR, Bollinger and Stochastic, I selected these by their popularities and the time they were mentioned. 
- But, at the end it became **MACD, RSI, Bollinger, Stochastic, PSAR** (Donchian out, RSI in) since I was more familiar with RSI. 
- The mechanisms are various, momentum/trend/mean reversion/oscillator.
