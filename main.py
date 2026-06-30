import numpy as np
import matplotlib.pyplot as plt

import data_loader
import engine.backtest as backtest
import engine.metrics as metrics
import validation.bootstrap as bootstrap
import validation.holm as holm

import strategies.macd as macd
import strategies.rsi as rsi
import strategies.bollinger_band as bollinger
import strategies.stochastic as stochastic
import strategies.psar as psar

STRATEGIES = {
    "MACD": macd.signal,
    "RSI": rsi.signal,
    "Bollinger": bollinger.signal,
    "Stochastic": stochastic.signal,
    "PSAR": psar.signal,
}

MIN_TRADES = 30
ANNUALIZE = 252**0.5


def build_returns(price_df, rf_daily):
    """Run each strategy through the engine once, storing (raw returns, excess)."""
    results = {}

    for name, signal in STRATEGIES.items():
        returns, excess = backtest.run(price_df, signal, rf_daily)
        results[name] = {"returns": returns, "excess": excess}

    return results

def show_metrics(strat_results, price_df):
    """Print per-strategy Sharpe / Calmar / Sortino + trade count."""

    print("\n=== Strategy metrics ===")

    for name, data in strat_results.items():
        excess = data["excess"].dropna()
        returns = data["returns"].dropna()

        sharpe_ratio = metrics.sharpe(excess) * ANNUALIZE
        calmar_ratio = metrics.calmar(returns)
        sortino_ratio = metrics.sortino(excess) * ANNUALIZE

        n_trades = int(STRATEGIES[name](price_df).shift(1).diff().abs().sum())
        label = "NOT ENOUGH TRADES" if n_trades < MIN_TRADES else ""

        print(f"{name}: Sharpe={sharpe_ratio:.3f}, Calmar={calmar_ratio:.3f}, Sortino={sortino_ratio:.3f}, trades={n_trades} {label}")

def compare_strategies(strat_results):
    """10 pairwise comparisons: bootstrap CI + p-value -> Holm correction -> verdict"""

    names = list(STRATEGIES.keys())

    # build all 10 unique pairs
    pairs = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pairs.append((names[i], names[j]))

    p_values = {}
    pair_info = {}

    for a, b in pairs:
        ci_low, ci_high, point, p = bootstrap.compare(strat_results[a]["excess"], strat_results[b]["excess"])
        key = f"{a} vs {b}"
        p_values[key] = p
        pair_info[key] = (ci_low, ci_high, point)

    holm_result = holm.holm_correct(p_values)

    print("\n=== Strategy comparison (Sharpe difference, 95% CI, Holm-corrected) ===")

    any_sig = False

    for key, (ci_low, ci_high, point) in pair_info.items():
        adj_p, sig = holm_result[key]

        if sig:
            any_sig = True

        mark = "SIGNIFICANT" if sig else "-"
        print(f"{key}: point={point:.3f}, CI=[{ci_low:.3f}, {ci_high:.3f}], adj_p={adj_p:.3f} {mark}")

    if not any_sig:
        print("\n-> No distinguishable pair: statistically indistinguishable (a valid result).")

def show_return_histogram(strat_results):
    """Histogram of each strategy's daily excess returns on in-market days only"""

    names = list(strat_results.keys())

    # keep only in-market days (drop cash days where excess is exactly 0)
    nonzero = {}

    for name in names:
        excess = strat_results[name]["excess"].dropna()
        nonzero[name] = excess[excess != 0].to_numpy()

    # common x-range (trim the extreme 0.5% so the center stays readable)
    all_nonzero = np.concatenate(list(nonzero.values()))
    lo, hi = np.percentile(all_nonzero, [0.5, 99.5])

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    for i, name in enumerate(names):
        axes[i].hist(nonzero[name], bins=80, range=(lo, hi), color="steelblue")
        axes[i].axvline(0, color="gray", linestyle="--", linewidth=0.8)
        axes[i].set_title(f"{name} (n={len(nonzero[name])})")
        axes[i].set_xlabel("Daily excess return (in-market days)")
        axes[i].set_ylabel("Frequency")

    for j in range(len(names), len(axes)):
        axes[j].axis("off")

    fig.suptitle("Strategy daily excess return distribution — in-market days only")
    fig.tight_layout()
    plt.show()

def main():
    while True:
        ticker = input("\nTicker (or 'q' to quit): ").upper()

        if ticker == "Q":
            break

        try:
            price_df, rf_daily = data_loader.sync_date(ticker)

        except Exception as e:
            print(f"Failed to load data: {e}")
            continue

        if price_df.empty:
            print("Please check the ticker.")
            continue

        # run everything automatically
        strat_results = build_returns(price_df, rf_daily)
        show_metrics(strat_results, price_df)
        print("Comparing Strategies...\nThis may take 1-2 minutes.")
        compare_strategies(strat_results)
        show_return_histogram(strat_results)

if __name__ == "__main__":
    main()