# Copyright (c) 2026 Martial Systems LLC
"""Anderson Q routed to Nora with lag 2 plus local noise. Indy lags Nora."""

from __future__ import annotations

from datetime import date

import numpy as np

from upq.pack import QPack

FIXTURE_START = date(2016, 10, 1)
FIXTURE_END = date(2020, 12, 31)
TRUE_LAG = 2


def build_fixture(*, seed: int = 5) -> QPack:
    rng = np.random.default_rng(seed)
    dates = np.arange(
        np.datetime64(FIXTURE_START.isoformat()),
        np.datetime64(FIXTURE_END.isoformat()) + np.timedelta64(1, "D"),
    )
    n = dates.shape[0]
    y = dates.astype("datetime64[Y]")
    doy = (dates - y).astype("timedelta64[D]").astype(int) + 1
    seasonal = 400 + 250 * np.sin(2 * np.pi * (doy - 50) / 365.25)
    andq = np.zeros(n)
    andq[0] = seasonal[0]
    for t in range(1, n):
        burst = rng.gamma(2.0, 80.0) if rng.random() < 0.07 else 0.0
        andq[t] = 0.75 * andq[t - 1] + 0.2 * seasonal[t] + burst + rng.normal(0, 15)
        andq[t] = max(80.0, andq[t])
    nora = np.zeros(n)
    for t in range(n):
        src = andq[t - TRUE_LAG] if t >= TRUE_LAG else andq[0]
        local = rng.gamma(1.2, 40.0) if rng.random() < 0.12 else rng.normal(0, 20)
        nora[t] = 1.15 * src + local
        nora[t] = max(90.0, nora[t])
    indy = np.zeros(n)
    for t in range(n):
        src = nora[t - 1] if t else nora[0]
        indy[t] = max(100.0, 1.2 * src + rng.normal(0, 40))
    return QPack(
        dates=dates,
        anderson_cfs=andq,
        nora_cfs=nora,
        indy_cfs=indy,
        source="fixture",
        extra={"true_lag": TRUE_LAG},
    )
