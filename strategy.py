"""Friday gasoline strength. Long RB after cash opening on Fridays, flat before EOD.
Weekday comes from completed calendar timestamp; price input is no future data.
"""
import numpy as np

FAMILY = "energy-friday-gasoline-drift"
PARAMS = {"entry_ct_sec": 34200, "exit_ct_sec": 54000, "stop_dollars": 250}
BASKET = ("RB",)


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["stop_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    targets = {}
    for symbol, df in panel.items():
        signal = np.zeros(len(df), dtype=np.int64)
        if symbol in BASKET:
            sec = df.ct_sec.to_numpy()
            friday = df.index.day_of_week.to_numpy() == 4
            signal[(sec >= PARAMS["entry_ct_sec"]) & (sec < PARAMS["exit_ct_sec"]) & friday] = 1
        targets[symbol] = signal
    return targets
