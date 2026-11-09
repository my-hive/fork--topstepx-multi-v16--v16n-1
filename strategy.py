"""RB late-morning liquidity reversal after an unusually large cash-open impulse.
At 09:30 CT, compare completed 08:30-09:30 return with trailing completed-session
cash-range scale. Fade excess move through 11:00 CT; all inputs known on entry bar.
"""
import numpy as np
import pandas as pd

FAMILY = "energy-opening-impulse-reversal"
PARAMS = {"lookback_sessions": 20, "impulse_scale": 1.0, "stop_dollars": 250}
BASKET = ("RB",)


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["stop_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    out = {}
    for symbol, df in panel.items():
        target = np.zeros(len(df), dtype=np.int64)
        out[symbol] = target
        if symbol not in BASKET:
            continue
        session = df.session.to_numpy()
        sec = df.ct_sec.to_numpy()
        opened = df.open.to_numpy(dtype=float)
        closed = df.close.to_numpy(dtype=float)
        scales = []
        for label in pd.unique(session):
            ix = np.flatnonzero(session == label)
            cash = ix[(sec[ix] >= 30600) & (sec[ix] < 54300)]
            first_hour = ix[(sec[ix] >= 30600) & (sec[ix] <= 34200)]
            if len(first_hour) and len(scales) >= PARAMS["lookback_sessions"]:
                impulse = closed[first_hour[-1]] - opened[first_hour[0]]
                scale = np.mean(scales[-PARAMS["lookback_sessions"]:])
                if scale and abs(impulse) > PARAMS["impulse_scale"] * scale:
                    hold = ix[(sec[ix] >= 34200) & (sec[ix] < 39600)]
                    target[hold] = -1 if impulse > 0 else 1
            if len(cash):
                scales.append(abs(closed[cash[-1]] - opened[cash[0]]))
        out[symbol] = target
    return out
