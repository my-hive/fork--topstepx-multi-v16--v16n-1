"""CL post-settlement liquidity reversal.
Fade a large completed pre-settlement move during final liquid half-hour; flat intraday.
"""
import numpy as np

FAMILY = "energy-settlement-reversal"
PARAMS = {"lookback": 60, "entry_sec": 52500, "exit_sec": 54600, "move_bps": 18, "stop_dollars": 250}


def entry_risk(panel):
    return {symbol: np.full(len(df), PARAMS["stop_dollars"], dtype=float)
            for symbol, df in panel.items()}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        target = np.zeros(len(df), dtype=np.int64)
        if symbol != "CL":
            result[symbol] = target
            continue
        close = df.close.to_numpy(dtype=float)
        seconds = df.ct_sec.to_numpy()
        for indices in df.groupby("session", sort=False).indices.values():
            for j in range(PARAMS["lookback"], len(indices)):
                i = indices[j]
                if PARAMS["entry_sec"] <= seconds[i] < PARAMS["exit_sec"]:
                    prior = close[indices[j - PARAMS["lookback"]]]
                    move_bps = 10000 * (close[i] / prior - 1)
                    if abs(move_bps) >= PARAMS["move_bps"]:
                        target[i] = -1 if move_bps > 0 else 1
        result[symbol] = target
    return result
