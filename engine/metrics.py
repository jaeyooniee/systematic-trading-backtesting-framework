import pandas as pd
import numpy as np

def sharpe(excess_returns):
    # raw Sharpe (mean/std, ddof=0으로 bootstrap의 numpy 계산과 통일). √252는 외부에서.
    std = excess_returns.std(ddof=0)
    return excess_returns.mean() / std if std != 0 else np.nan

def calmar(returns):
    annual_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    cumulative = (1 + returns).cumprod()
    mdd = ((cumulative - cumulative.cummax()) / cumulative.cummax()).min()
    return annual_return / abs(mdd) if mdd != 0 else np.nan

def sortino(excess_returns):
    downside = excess_returns.copy()
    downside[downside > 0] = 0
    downside_dev = (downside ** 2).mean() ** 0.5   # 이미 ddof 무관 (제곱평균제곱근)
    return excess_returns.mean() / downside_dev if downside_dev != 0 else np.nan