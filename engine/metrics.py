import pandas as pd
import numpy as np

def sharpe(excess_returns):
    return excess_returns.mean() / excess_returns.std()

def calmar(returns):
    annual_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    cumulative = (1 + returns).cumprod()
    mdd = ((cumulative - cumulative.cummax()) / cumulative.cummax()).min()

    if mdd == 0:
        return np.nan
    
    return annual_return / abs(mdd)

def sortino(excess_returns):
    downside = excess_returns[excess_returns < 0]
    return excess_returns.mean() / downside.std()