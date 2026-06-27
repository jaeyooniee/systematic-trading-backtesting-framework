import pandas as pd
import numpy as np


def safe_divide(numerator, denominator) -> pd.Series:
    # Replace 0 in denominator with NaN -> only zero positions yield NaN
    return numerator / denominator.replace(0, np.nan)


def stateful_signal(entry_condition, exit_condition):
    """
    Build a 0/1 signal that maintains position state.

    1 -> when the entry condition is true
    0 -> when the exit condition is true
    Hold the previous state in between. 
    
    If both are true on the same day, the current state decides 
    - exit takes priority while in a long position

    """

    # Pre-warmup NaNs -> False, so that early period stays in cash: 0
    entry = entry_condition.fillna(False).astype(bool)
    exit = exit_condition.fillna(False).astype(bool)

    is_long = False   # current position state (True = long, False = cash)
    values = []

    for should_enter, should_exit in zip(entry, exit):
        if is_long and should_exit:         # in long + exit signal -> close
            is_long = False
        elif not is_long and should_enter:  # in cash + entry signal -> open
            is_long = True
            
        # neither -> keep is_long unchanged (hold previous state)

        values.append(1 if is_long else 0)

    return pd.Series(values, index=entry.index, name="signal").astype(int)