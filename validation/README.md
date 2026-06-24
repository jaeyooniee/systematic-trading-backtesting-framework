# Hypothesis Testing Notes

- I am making notes regarding hypothesis testing before working on the strategies and downloading APIs.
- This approach will prioritise the rationalization and accuracy of the results.
- My focus on the testing is "Did strategy A beat strategy B by a margin that is statistically distinguishable from a random chance".

## Validation Protocal Details

- Main Test Engine: **Block Bootstrap**
  - The procedure:
    - Work on the date-aligned series so that both strategies shares the same market moves.
    - For each of B = 10,000 bootstrap interations, we take the difference between the sharpe ratio of A and B.

- Supporting Tools:
  - **ACF**: Before, to justify the block length based on the data
  - **Holm correction**: After, diagnose the chance

- Comparisons are two-sided. A short description of the thought process of this decision is briefly introduced on the "Thought Processes" part.

## Metric

- Primary metric I am weighing is **annualized Sharpe ratio**.
- Secondary metrics are Calmar ratio and Sortino ratio. I am using these values to claim strong ties when these metrics collide. 
  - Drawdown in Profit and Loss is not uncontrollable, the responsibility is fully on the logic of the strategies and this is the reason I need secondary metrics for more concise interpretation.

**Sharpe computation details**
  - Apply T-bill series from FRED (ideally)
  - Annualization: report annualized Sharpe by multiplying $\sqrt{252}$, where the number indicates the trading days of a single year.

## Determining the best strategy
  - First of all, I prioritised statistical accuracy over personal decision which may distort the results. So if there does not exists any "better" strategy, then the valid conclusion would be "statistically indistinguishable".
  - The main metric is **Sharpe Ratio** as mentioned however, the other two metrics are not neglected.

## Data Management
  - It is crucial to not look at the results during strategy development whatsoever. 
  - The built strategy should be deployed on unseen data which is future data (compared to the 'past' data for development).
  - I am thinking of spliting the whole data into 70:30 ratio.


## Thought Processes 

- Rejected z-test due to 2 reasons.
  1. A specific day's return is correlated with prior days's prices and this breaks the independence assumption.
  2. By some macro incidents (sometimes the stock's internal incidents), the possibility of having extreme amount of returns might destabilizes the standard deviation for Sharpe Ratio so normal-based standard errors understate the true uncertainty and produce confidence intervals which can be too narrow.

- I confused myself when choosing decision rule of how to interpret the results and whether I should use one-tailed or two-sided.
- The fact I could not determine which strategy outperforms the other before seeing the data, I chose to use two-tailed test so that I figure the statistical difference between two strategies and make a decision.

- I was considering of using some stocks for optimising strategies and their hyperparameters. After the optimisation, it will end up comparing the results from unseen stock data (apparently other stocks).
- However, the stocks themselves would've gone through same market circumstances hence, we cannot ensure the test has been clean and generalised.

## Project Architecture
  1. Data layer
  2. Bootstrap Engine
  3. Strategies
