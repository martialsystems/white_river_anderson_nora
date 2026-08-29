# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from upqforge.graphs.claim_bans import build_graph as claim_bans
    from upqforge.graphs.fetch_nwis import build_graph as fetch_nwis
    from upqforge.graphs.no_p_sfha import build_graph as no_p_sfha
    from upqforge.graphs.temporal_split import build_graph as temporal_split

    return [
        {
            "id": "upq.no_p_sfha",
            "build": no_p_sfha,
            "state": {"p_sfha_feature": False, "p_sfha_label": False, "p_sfha_figure": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "upq.temporal_split",
            "build": temporal_split,
            "state": {"temporal_ok": True, "tau_from_train": True, "indy_predictor": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "upq.fetch_nwis",
            "build": fetch_nwis,
            "state": {"nwis_ok": True, "nwm_repull": False, "indy_predictor": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "upq.claim_bans",
            "build": claim_bans,
            "state": {"lag_as_wet_mask": False, "flood_warning": False, "feet_invert": False, "n_figures": 2},
            "allow_decisions": ["allow"],
        },
    ]
