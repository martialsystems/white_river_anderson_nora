# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from upqforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from upqforge.gate import require_claims, require_fetch, require_no_p_sfha, require_split
from upqforge.product_laws import laws


def test_laws() -> None:
    require_no_p_sfha(thread_id="t.p")
    with pytest.raises(LawBlockedError):
        require_no_p_sfha(p_sfha_feature=True, thread_id="t.p.bad")
    require_split(thread_id="t.s")
    with pytest.raises(LawBlockedError):
        require_split(indy_predictor=True, thread_id="t.s.indy")
    with pytest.raises(LawBlockedError):
        require_split(tau_from_train=False, thread_id="t.s.tau")
    require_fetch(nwis_ok=True, thread_id="t.f")
    with pytest.raises(LawBlockedError):
        require_fetch(nwis_ok=True, nwm_repull=True, thread_id="t.f.nwm")
    require_claims(n_figures=2, thread_id="t.c")
    with pytest.raises(LawBlockedError):
        require_claims(n_figures=3, thread_id="t.c.fig")
    assert {row["id"] for row in laws()} == {
        "upq.no_p_sfha",
        "upq.temporal_split",
        "upq.fetch_nwis",
        "upq.claim_bans",
    }
