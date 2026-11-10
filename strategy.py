"""Treasury month-end afternoon duration bid: benchmark index extensions and
pension month-end duration rebalancing creates buying in ZN cash session after 09:30 CT."""
import numpy as np
import pandas as pd

FAMILY = "rates-monthend-duration-afternoon"
PARAMS = {"min_day_of_month": 28, "entry_ct_sec": 34200, "exit_ct_sec": 54000, "stop_dollars": 250}
BASKET = ("ZN",)

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["stop_dollars"], dtype=float) for s, df in panel.items()}

def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol in BASKET:
            day = pd.to_datetime(df.session.astype(str))
            sec = df.ct_sec.to_numpy()
            mask = (day.dt.day >= PARAMS["min_day_of_month"]).to_numpy() & (sec >= PARAMS["entry_ct_sec"]) & (sec < PARAMS["exit_ct_sec"])
            out[mask] = 1
        result[symbol] = out
    return result
