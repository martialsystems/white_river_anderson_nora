# Copyright (c) 2026 Martial Systems LLC
"""NWIS only. No NWM. No 2026 overlay."""

from __future__ import annotations

from datetime import date
from typing import Any

import numpy as np

from upq.config import ANDERSON_ID, INDY_ID, LIVE_END, LIVE_START, NORA_ID
from upq.errors import FetchError
from upq.nwis import fetch_three
from upq.pack import QPack


def fetch_live(*, start: date = LIVE_START, end: date = LIVE_END, get_json_fn=None) -> tuple[QPack, dict[str, Any]]:
    series = fetch_three(start=start, end=end, get_json_fn=get_json_fn)
    dates = np.arange(np.datetime64(start.isoformat()), np.datetime64(end.isoformat()) + np.timedelta64(1, "D"))

    def align(site: str) -> np.ndarray:
        m = series[site]
        return np.array([m.get(d, np.nan) for d in dates], dtype=float)

    andq, nora, indy = align(ANDERSON_ID), align(NORA_ID), align(INDY_ID)
    if not np.isfinite(andq).any():
        raise FetchError("Anderson 00060 has no overlap")
    if not np.isfinite(nora).any():
        raise FetchError("Nora 00060 has no overlap")
    pack = QPack(
        dates=dates,
        anderson_cfs=andq,
        nora_cfs=nora,
        indy_cfs=indy,
        source="nwis_dv_00060",
        extra={"indy_id": INDY_ID, "indy_role": "diagnostic"},
    )
    return pack, {"sites": [ANDERSON_ID, NORA_ID, INDY_ID], "n_days": pack.n_days}
