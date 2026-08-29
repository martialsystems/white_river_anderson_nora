# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from typing import Any

from upqforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from upqforge.graphs.claim_bans import build_graph as build_claims
from upqforge.graphs.fetch_nwis import build_graph as build_fetch
from upqforge.graphs.no_p_sfha import build_graph as build_p
from upqforge.graphs.temporal_split import build_graph as build_split


def require_no_p_sfha(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "upq_p"))
    state = {"p_sfha_feature": False, "p_sfha_label": False, "p_sfha_figure": False}
    state.update(flags)
    require_law(build_p(), state, allow_decisions=["allow"], law_id="upq.no_p_sfha", thread_id=thread_id, raise_error=True)


def require_split(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "upq_split"))
    state = {"temporal_ok": True, "tau_from_train": True, "indy_predictor": False}
    state.update(flags)
    require_law(build_split(), state, allow_decisions=["allow"], law_id="upq.temporal_split", thread_id=thread_id, raise_error=True)


def require_fetch(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "upq_fetch"))
    state = {"nwis_ok": False, "nwm_repull": False, "indy_predictor": False}
    state.update(flags)
    require_law(build_fetch(), state, allow_decisions=["allow"], law_id="upq.fetch_nwis", thread_id=thread_id, raise_error=True)


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "upq_claims"))
    state = {"lag_as_wet_mask": False, "flood_warning": False, "feet_invert": False, "n_figures": 2}
    state.update(flags)
    require_law(build_claims(), state, allow_decisions=["allow"], law_id="upq.claim_bans", thread_id=thread_id, raise_error=True)
