import numpy as np
import matplotlib.pyplot as plt


def compute_acf(excess_returns, max_lags=50):
    """
    calculate ACF using numpy.
    Biased estimate: denominator = variance * n.

    Returns: (acf_values, confidence_band)
      - acf_values: correlation of lag 0 ~ max_lags (lag 0 = 1)
      - confidence_band: ±1.96/sqrt(n)

    """
    x = excess_returns.dropna().to_numpy()
    n = len(x)

    max_lags = min(max_lags, n-1)
    x_demeaned = x - x.mean()
    denominator = np.sum(x_demeaned ** 2) 

    acf_values = np.empty(max_lags + 1)
    acf_values[0] = 1

    for lag in range(1, max_lags + 1):
        cov = np.sum(x_demeaned[lag:] * x_demeaned[:-lag])
        acf_values[lag] = cov / denominator

    confidence_band = 1.96 / n**0.5
    return acf_values, confidence_band


def get_block_length(acf_values, confidence_band, cushion=2):
    """
    Determine the block length for the block bootstrap from the ACF.

    Rule (agreed on during the project):
      - Starting from lag 1, count only the consecutively significant lags.
      - Stop at the first lag that falls back inside the band (consecutive run breaks).
        -> Isolated distant significant lags are likely chance under multiple testing, so ignore them.
      - If there is no significant autocorrelation at all, the block length is 1
        (effectively a plain bootstrap).
      - Otherwise, set it generously as (run length + cushion) to cover the whole structure,
        since matching it exactly would cut the autocorrelation structure at block boundaries.
    """

    max_lags = len(acf_values) - 1
    consecutive_significant = 0

    for lag in range(1, max_lags + 1):
        if abs(acf_values[lag]) > confidence_band:
            consecutive_significant = lag

        else:
            break 

    if consecutive_significant == 0:
        return 1
    
    return consecutive_significant + cushion


def plot_acf(acf_values, confidence_band):
    """Plot ACF values"""

    max_lags = len(acf_values) - 1

    plt.figure(figsize=(12, 4))
    plt.bar(range(max_lags + 1), acf_values, color='steelblue', alpha=0.7)
    plt.axhline(confidence_band, color='red', linestyle='--', label='95% confidence band')
    plt.axhline(-confidence_band, color='red', linestyle='--')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.xlabel('Lag')
    plt.ylabel('ACF')
    plt.title('ACF of Excess Returns')
    plt.legend()
    plt.tight_layout()

    plt.show()