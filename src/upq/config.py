# Copyright (c) 2026 Martial Systems LLC
"""Anderson Q → Nora Q. Does not read p_sfha. Does not re-pull NWM."""

from __future__ import annotations

from datetime import date

QUESTION = "Does yesterday at Anderson help you guess Nora's flow today?"
ANDERSON_ID = "03348000"
NORA_ID = "03351000"
INDY_ID = "03353000"
ANDERSON_NAME = "Anderson"
NORA_NAME = "Nora"
INDY_NAME = "Indianapolis"
MAX_LAG_DAYS = 7
MAX_FIGURES = 2
# Same window as NWM error fa2e315. Cited NWM Nora RMSE is not a re-pull.
LIVE_START = date(2016, 10, 1)
LIVE_END = date(2020, 12, 31)
TRAIN_END = date(2018, 9, 30)
HOLDOUT_START = date(2018, 10, 1)
NWM_NORA_RMSE_CFS = 1316.13
NWM_NORA_CITATION = "fa2e315"
LOCKED_LIVE_COMMIT = "58859be"
USER_AGENT = "MartialSystemsResearch/white_river_anderson_nora"
NWIS_DV_URL = (
    "https://waterservices.usgs.gov/nwis/dv/?format=json&sites={site}"
    "&startDT={start}&endDT={end}&parameterCd=00060&siteStatus=all"
)
