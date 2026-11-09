"""CL opening-range breakout. Completed 08:30-09:00 CT range; trade first break until 14:00 CT."""
import numpy as np

FAMILY = "energy-opening-range-reversion"
PARAMS = {"range_start": 30600, "range_end": 32400, "trade_end": 50400, "stop_dollars": 250}


def entry_risk(panel):
    return {symbol: np.full(len(df), PARAMS["stop_dollars"], dtype=float) for symbol, df in panel.items()}


def signals(panel):
    out = {}
    for symbol, df in panel.items():
        target = np.zeros(len(df), dtype=np.int64)
        if symbol != "CL":
            out[symbol] = target
            continue
        high, low, close, sec = (df.high.to_numpy(), df.low.to_numpy(), df.close.to_numpy(), df.ct_sec.to_numpy())
        for inds in df.groupby("session", sort=False).indices.values():
            ids = np.asarray(inds)
            opening = ids[(sec[ids] >= PARAMS["range_start"]) & (sec[ids] < PARAMS["range_end"])]
            if not len(opening):
                continue
            top, bottom, side = high[opening].max(), low[opening].min(), 0
            for i in ids:
                if sec[i] >= PARAMS["trade_end"]:
                    side = 0
                elif sec[i] >= PARAMS["range_end"] and side == 0:
                    if close[i] > top: side = -1
                    elif close[i] < bottom: side = 1
                target[i] = side
        out[symbol] = target
    return out
