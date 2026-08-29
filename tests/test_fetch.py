# Copyright (c) 2026 Martial Systems LLC

from datetime import date

import numpy as np
import pytest

from upq.errors import FetchError
from upq.fetch import fetch_live
from upq.nwis import parse_dv_q


def test_parse_dv() -> None:
    doc = {
        "value": {
            "timeSeries": [
                {
                    "variable": {"variableCode": [{"value": "00060"}]},
                    "values": [{"value": [{"dateTime": "2019-07-01T00:00:00.000", "value": "900"}]}],
                }
            ]
        }
    }
    assert parse_dv_q(doc)[np.datetime64("2019-07-01")] == 900.0


def test_empty_stops(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*, site, start, end, get_json_fn=None):
        del start, end, get_json_fn
        raise FetchError(f"NWIS daily 00060 is empty for {site}")

    monkeypatch.setattr("upq.fetch.fetch_three", lambda **k: (_ for _ in ()).throw(FetchError("empty")))
    with pytest.raises(FetchError):
        fetch_live(start=date(2019, 7, 1), end=date(2019, 7, 2))
