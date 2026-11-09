"""Monday heating-oil reversal after cash opening. Short HO from 09:30 to 15:00 CT.
Calendar weekday is known at bar time; no price look-ahead.
"""
import numpy as np

FAMILY = "energy-monday-heatingoil-reversal"
PARAMS = {"entry_ct_sec": 34200, "exit_ct_sec": 54000, "stop_dollars": 250}
BASKET = ("HO",)


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["stop_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    targets = {}
    for symbol, df in panel.items():
        signal = np.zeros(len(df), dtype=np.int64)
        if symbol in BASKET:
            sec = df.ct_sec.to_numpy()
            monday = df.index.day_of_week.to_numpy() == 0
            signal[(sec >= PARAMS["entry_ct_sec"]) & (sec < PARAMS["exit_ct_sec"]) & monday] = -1
        targets[symbol] = signal
    return targets
