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
- After some research and my experience in IMC Prosperity 4, I found that in this case I would have to use a **block bootstrap** to preserve the temporal continuity of the price series within each period.
- Moreover, to guard against false positives from multiple comparisons, I researched how to
  account for that randomness, and found I could use **Holm's correction**.

### 0.6  Setting Parameters Before Seeing the Results
Before checking the results of the strategies, I fixed all parameters. 
- Bootstrap: 5000
- Confidence Level: 95%
- Data Period: 2005-2025
- Minimum Trades: 30
- Cost Percentage: 0 (default)

To set block length for block bootstrap, I applied **ACF** and fixed the length to 4. 

[per-pair block length distribution]("C:\Users\comac\Downloads\block_length_distribution.png")


### 0.7 Realising and Testing
I did most of my work from scratch, which was my whole plan and idea of this project if I'm honest. 
The progress was from building data loader to engine, metrics and so on. 

In short, I checked that engine works well by building 'buy & hold' file and simply printed and evaulated the results. 

5 selected strategies were explicitly sorted to match the interface (0/1 signal with no shift) and vectorised using numpy for efficiency.

### 0.8 Results
Most of the results showed 'statistically indistinguishable'. So I wanted to visualise and see the results of backtests. I used histograms (Learned this graph from Stats 1 and DS as well).

'Indistinguishable' doesn not mean it's a failure but this is a valid result for what I have been aiming for this whole framework where I wanted to keep statistical accuracy from the start to the end of the project and keep being honest. 

> What I've learned: I mentioned every reason and sources of my decision among building the framework and even if the results were not close to what I've been expecting, I have not modified the process that I have set before testing. This made the project be a research which can be methodologically defendable. 

---

## 1. Some important questions

> If the sharpe ratio of strategy A is higher than that of strategy B, are we able to say that the difference is not a chance but from statistically meaningful results in a high confidence interval?

To answer to this question, I am not only simply comparing sharpe ratio but also applying testing process including bootstrap confidence level and multiple comparation correction.

---

## 2. Key Design Decisions and Rationale

| Decision | Contents | Comments |
|------|------|------|
| Compare Range | Compare 5 strategies pairwise on a single ticker (10 pairs total) | Every strategy uses the same data, so survivorship bias does not arise here |
| Position | LONG-ONLY, 0 (cash) or 1 (hold) | Short positions require cost modelling and introduce possible skewness, so they are omitted. "Sell" simply means setting the position to 0 |
| Position Size | Binary (signal on = 100% hold, off = 100% cash) | Position sizing is omitted for comparison clarity, as it is an overfitting axis and a complex variable |
| Stop-loss | None | No stop-loss is added, so the strategies themselves can be compared cleanly |
| Volume | Not used for signals | Avoids split-adjustment burden and the extreme fat tails of volume data |
| ML | None | Conflicts with the "fix parameters before seeing the data" principle (ML inherently learns from the data) |
| Parameter | Fixed before seeing data, using theoretical/conventional values | Tuning on the data would be overfitting; every strategy uses the standard settings for its indicator |
| Data Period | Fixed 20 years (2005-01-01 to 2025-01-01) | Choosing the period after seeing results/trade counts would bias it, so it is fixed beforehand. Gives sufficient power and reflects modern market structure (excluding overly old data); the end is fixed so the window does not grow on re-runs |

---

## 3. Data Layer
- **Price Data**: yfinance, adjusted OHLC price.
- **OHLC preservation**: Most of the time I used Close price but I had OHLC saved in cache.
- **Risk-Free rate(rf)**: FRED DTB3 (3-month T-bill)
  - DTB3 uses annualised percentage so it was modified as daily percentage by `rf_daily = rf_annual / 100 / 252` (252-days often refer to 1-year trading days)

---

## 4. Strategies
Every strategy is Long-only, uses `signal(prices) -> pd.Series` format which only returns signals of 0/1.
Parameters are set to be standard settings of each indicator.

| # | Strategy | Parameters | Type |
|---|------|----------|--------------|
| 1 | MACD | 12 / 26 / 9 | MA Momentum |
| 2 | RSI | 14, Entry < 30 / Exit > 70 (stateful) | Mean Reversion (Momentum Oscillator) |
| 3 | Parabolic SAR | step 0.02 / max 0.2 | Trend (Stateful Recursion) |
| 4 | Bollinger Band | window 20 / 2 SD | Mean Reversion |
| 5 | Stochastic Oscillator | 14 / 3 / 3 | Osciallator (Mean Reversion) |

I tried to use as various strategies as possible.

---
