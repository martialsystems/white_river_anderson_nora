# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from upqforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if not state.get("temporal_ok"):
        v.append("not_temporal")
    if not state.get("tau_from_train"):
        v.append("tau_not_from_train")
    if state.get("indy_predictor"):
        v.append("indy_predictor")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="upq.temporal_split",
        evaluate=_evaluate,
        extra=["temporal_ok", "tau_from_train", "indy_predictor"],
    )
