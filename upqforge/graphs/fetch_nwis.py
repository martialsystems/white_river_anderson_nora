# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from upqforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("nwis_ok"):
        v.append("nwis_empty")
    if state.get("nwm_repull"):
        v.append("nwm_repull")
    if state.get("indy_predictor"):
        v.append("indy_predictor")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="upq.fetch_nwis",
        evaluate=_evaluate,
        extra=["nwis_ok", "nwm_repull", "indy_predictor"],
    )
