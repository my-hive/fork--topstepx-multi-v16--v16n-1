"""Daily trend sign (trailing N-session close-to-close return, lagged by one session)
held through the pit session as one trade/day. Basket CL GC ZN 6E ZC, 1 contract each.
"""
import numpy as np

FAMILY = "daily-trend-intraday-carry"
PARAMS = {"lookback": 20, "start": 30600, "end": 50400, "atr_mult": 1.0, "risk_cap": 300}
BASKET = ("CL", "GC", "ZN", "6E", "ZC")


def _daily(df):
    g = df.groupby("session", sort=True)
    return g.close.last(), (g.high.max() - g.low.min())


def entry_risk(panel):
    out = {}
    for s, df in panel.items():
        _, rng = _daily(df)
        from instruments import SPECS  # noqa
        r = rng.rolling(PARAMS["lookback"]).mean().shift(1) * PARAMS["atr_mult"] * SPECS[s].point_value
        out[s] = df.session.map(r).fillna(1e9).to_numpy(dtype=float).clip(0, PARAMS["risk_cap"])
    return out


def signals(panel):
    out = {}
    for s, df in panel.items():
        t = np.zeros(len(df), dtype=np.int64)
        if s in BASKET:
            close, _ = _daily(df)
            trend = np.sign(close.shift(1) - close.shift(1 + PARAMS["lookback"]))
            side = df.session.map(trend).fillna(0).to_numpy()
            sec = df.ct_sec.to_numpy()
            t[(sec >= PARAMS["start"]) & (sec < PARAMS["end"])] = side[(sec >= PARAMS["start"]) & (sec < PARAMS["end"])].astype(np.int64)
        out[s] = t
    return out
