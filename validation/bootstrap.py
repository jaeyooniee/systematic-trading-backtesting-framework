import numpy as np
import pandas as pd


def sharpe_axis(x):
    mean = x.mean(axis=-1)
    std = x.std(axis=-1)  # numpy ddof=0

    return np.where(std == 0, np.nan, mean / std)


def compare(excess_a, excess_b, block_length=4, n_resamples=5000, seed=42):
    df = pd.concat({"a": excess_a, "b": excess_b}, axis=1).dropna()

    a = df["a"].to_numpy()
    b = df["b"].to_numpy()
    n = len(a)

    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block_length))   # how many blocks do we need to cover n

    all_indices = []

    for _ in range(n_resamples):
        indices = []

        for _ in range(n_blocks):                     # build one block at a time
            start = rng.integers(0, n)                # random block start point
            for offset in range(block_length):        # consecutive days within the block
                indices.append((start + offset) % n)  # wrap to start if it runs past the end
        
        all_indices.append(indices[:n])               # trim to exactly n indices

    idx = np.array(all_indices)                       # (n_resamples, n) index matrix

    a_res = a[idx]
    b_res = b[idx]
    diffs = sharpe_axis(a_res) - sharpe_axis(b_res)   # raw Sharpe difference distribution

    valid = diffs[~np.isnan(diffs)]                   # drop NaNs (e.g. when std was 0)
    ci_low = np.percentile(valid, 2.5) * 252**0.5
    ci_high = np.percentile(valid, 97.5) * 252**0.5
    point_estimate = (sharpe_axis(a) - sharpe_axis(b)) * 252**0.5

    p_left = np.mean(valid <= 0)
    p_right = np.mean(valid >= 0)

    p_value = min(1, 2 * min(p_left, p_right))

    return ci_low, ci_high, point_estimate, p_value