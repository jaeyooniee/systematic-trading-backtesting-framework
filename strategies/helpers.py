import pandas as pd
import numpy as np


def safe_divide(numerator, denominator) -> pd.Series:
    return numerator / denominator.replace(0, np.nan)


def stateful_signal(entry_condition, exit_condition):
    entry = entry_condition.fillna(False).astype(bool)
    exit = exit_condition.fillna(False).astype(bool)

    is_long = False
    values = []

    for should_enter, should_exit in zip(entry, exit):
        if is_long and should_exit:
            is_long = False

        elif not is_long and should_enter:
            is_long = True

        values.append(1 if is_long else 0)

    return pd.Series(values, index=entry.index, name="signal").astype(int)