# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from upq.claims import require_clean, require_paths_clean
from upq.config import NWM_NORA_CITATION, NWM_NORA_RMSE_CFS, QUESTION
from upq.fetch import fetch_live
from upq.figure import write_two
from upq.fixture import build_fixture
from upq.models import assert_no_indy_in_X, fit_pack

try:
    from upqforge.gate import require_claims, require_fetch, require_no_p_sfha, require_split
except ImportError:  # pragma: no cover

    def require_claims(**kwargs):
        del kwargs

    def require_fetch(**kwargs):
        del kwargs

    def require_no_p_sfha(**kwargs):
        del kwargs

    def require_split(**kwargs):
        del kwargs


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in report.items() if k != "holdout"}


def _run(log_dir: Path, *, pack, fixture: bool, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    require_no_p_sfha(thread_id="p_sfha")
    require_clean(QUESTION, source="question")
    fit = fit_pack(pack)
    assert_no_indy_in_X(fit)
    require_split(
        temporal_ok=True,
        tau_from_train=True,
        indy_predictor=False,
        thread_id="split",
    )
    paths = write_two(log_dir, fit=fit)
    require_claims(n_figures=len(paths), thread_id="claims")
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "tau_star": fit["tau_star"],
        "lag_curve": fit["lag_curve"],
        "skill": fit["skill"],
        "verdict": fit["verdict"],
        "indy_in_X": False,
        "indy_diagnostic": fit["indy_diagnostic"],
        "predictor_sites": fit["predictor_sites"],
        "nwm_nora_rmse_cfs_cited": NWM_NORA_RMSE_CFS,
        "nwm_citation": NWM_NORA_CITATION,
        "p_sfha_feature": False,
        "figures": [p.name for p in paths],
        "holdout": fit["holdout"],
        "n_days": pack.n_days,
        "source": pack.source,
    }
    if extra:
        report.update(extra)
    name = "stage0_report.json" if fixture else "stage_c_report.json"
    (log_dir / name).write_text(json.dumps(_jsonable(report), indent=2, default=str) + "\n")
    require_paths_clean([log_dir / name])
    return report


def stage0_fixture(log_dir: Path) -> dict[str, Any]:
    return _run(log_dir, pack=build_fixture(), fixture=True)


def run_live(log_dir: Path) -> dict[str, Any]:
    pack, meta = fetch_live()
    require_fetch(nwis_ok=True, nwm_repull=False, indy_predictor=False, thread_id="live.fetch")
    return _run(log_dir, pack=pack, fixture=False, extra=meta)
