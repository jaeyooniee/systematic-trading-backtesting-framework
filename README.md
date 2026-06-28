# Systematic Trading Strategies Backtesting Framework

The project aims to backtest 5 well-known strategies on a single US equity.
I focused on producing statistically plausible results justified by statistical tests.
The framework ultimately reveals whether the strategies show statistically significant differences in their **Sharpe ratio**.

> The goal is not to find the most profitable strategy, but to determine whether one can
> statistically justify the claim that one strategy outperformed the others. It is about answering
> a methodological question. Therefore, the crucial point of the evaluation is the statistical
> rigour of the comparison.

---

## 0. Journey of the Project (From Start to End)
This part illustrates the whole process of **how I started this project and what steps I went
through to reach the results**, chronologically.

### 0.1 Starting Off (What Am I Building Exactly?)
Out of my deep interest in the quantitative finance field, I first thought of building a trading
strategies backtesting framework. I began by choosing the identity of the project: **not "finding
the best strategy" but a "methodology that statistically justifies the comparison of strategies".**

In addition, I decided to build a vectorised engine rather than importing existing backtesting
libraries. The big picture of the framework (e.g. pairwise comparison of 5 strategies on a single
stock, Sharpe ratio as the main metric, T-bill as the risk-free rate) was drawn at this stage.

### 0.2 Selection of Strategies
I collected trading strategies without any bias from [QuantConnect](https://www.quantconnect.com/research/),
[TradingView](https://www.tradingview.com/), and Peng Liu's [Quantitative Trading Strategies Using
Python](https://link.springer.com/book/10.1007/978-1-4842-9675-2). Multi-asset and cross-sectional
strategies were omitted, since the framework I planned focused only on trading a single stock.

### 0.3 Choosing the Data Source
I had two options for price data:
1. Polygon
2. yfinance

However, Polygon has been rebranded and now restricts some historical data, so I chose to use
**yfinance**. The risk-free rate was taken from **FRED DTB3** (3-Month Treasury Bill Secondary
Market Rate).

### 0.4 Setting the Final 5 Strategies
I changed the strategy set quite a few times before starting the coding part.
- At first, the set was MACD, Donchian, PSAR, Bollinger, and Stochastic, which I selected based on
  their popularity and how often they were mentioned.
- In the end it became **MACD, RSI, Bollinger, Stochastic, PSAR** (Donchian out, RSI in), as I was
  more familiar with RSI.
- The mechanisms are varied: momentum / trend / mean reversion / oscillator.

### 0.5 Testing Methods — Using Methods from University Modules
I decided to use methods from the modules I studied last year, especially Statistics 1 and Data
Science. I had kept study projects where I explicitly filed every chapter, so it was easy to recall
the contents.
- First, I focused on the difference between comparing PnLs and comparing Sharpe ratios.
- The Sharpe ratio is a non-linear statistic, so the clean t-test formula does not apply; I figured
  I would have to use a bootstrap method. I had learned bootstrapping in the Data Science module in
  Semester 2, for sampling with replacement when the number of data points is small.
- To use the bootstrap, the data is supposed to be i.i.d.; however, stock prices cannot be
  independent across days (they are autocorrelated), and this fact should not be neglected.
- After some research, I found that in this case I would have to use a **block bootstrap** to
  preserve the temporal continuity of the price series within each period.
- Moreover, to guard against false positives from multiple comparisons, I researched how to
  account for that randomness, and found I could use **Holm's correction**.
