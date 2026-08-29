# Copyright (c) 2026 Martial Systems LLC
"""tau* on train only. Anderson lag vs Nora persistence. Indy not in X."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import LinearRegression

from upq.config import INDY_ID, MAX_LAG_DAYS, NWM_NORA_RMSE_CFS
from upq.errors import LeakError, SplitError
from upq.pack import QPack
from upq.split import assert_temporal, temporal_masks


def rmse(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float)
    ok = np.isfinite(e)
    return float(np.sqrt(np.mean(e[ok] * e[ok]))) if ok.any() else float("nan")


def mae(y: np.ndarray, yhat: np.ndarray) -> float:
    e = np.abs(np.asarray(y, dtype=float) - np.asarray(yhat, dtype=float))
    ok = np.isfinite(e)
    return float(np.mean(e[ok])) if ok.any() else float("nan")


def _lag(arr: np.ndarray, k: int) -> np.ndarray:
    if k < 0:
        raise SplitError("negative lag is a future leak")
    out = np.full(arr.shape, np.nan, dtype=float)
    src = np.asarray(arr, dtype=float)
    if k == 0:
        return src.copy()
    out[k:] = src[:-k]
    return out


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 8:
        return float("nan")
    if np.std(a[ok]) == 0 or np.std(b[ok]) == 0:
        return float("nan")
    return float(np.corrcoef(a[ok], b[ok])[0, 1])


def tau_star(anderson: np.ndarray, nora: np.ndarray, train: np.ndarray) -> tuple[int, list[dict[str, float]]]:
    curve = []
    best_t, best_c = 1, -2.0
    for t in range(0, MAX_LAG_DAYS + 1):
        c = _corr(_lag(anderson, t)[train], nora[train])
        curve.append({"tau_days": t, "corr_train": c})
        if np.isfinite(c) and c > best_c:
            best_t, best_c = t, c
    return best_t, curve


def fit_pack(pack: QPack) -> dict[str, Any]:
    andq = np.asarray(pack.anderson_cfs, dtype=float)
    nora = np.asarray(pack.nora_cfs, dtype=float)
    train_all, hold_all = temporal_masks(pack.dates)
    assert_temporal(pack.dates, train_all, hold_all)
    pers = _lag(nora, 1)
    ok = np.isfinite(andq) & np.isfinite(nora) & np.isfinite(pers)
    train, hold = train_all & ok, hold_all & ok
    tau, curve = tau_star(andq, nora, train)
    x = _lag(andq, tau)
    row = train & np.isfinite(x)
    ho = hold & np.isfinite(x)
    if not row.any() or not ho.any():
        raise SplitError("no valid rows after lag")
    lr = LinearRegression()
    lr.fit(x[row].reshape(-1, 1), nora[row])
    yhat = lr.predict(x[ho].reshape(-1, 1))
    y_ho, pers_ho = nora[ho], pers[ho]
    skill = {
        "persistence": {"rmse_cfs": rmse(y_ho, pers_ho), "mae_cfs": mae(y_ho, pers_ho)},
        "anderson_lag": {
            "rmse_cfs": rmse(y_ho, yhat),
            "mae_cfs": mae(y_ho, yhat),
            "tau_days": tau,
            "scale": float(lr.coef_[0]),
            "intercept": float(lr.intercept_),
        },
        "nwm_nora_cited": {"rmse_cfs": NWM_NORA_RMSE_CFS, "source": "fa2e315"},
    }
    a_rmse = skill["anderson_lag"]["rmse_cfs"]
    p_rmse = skill["persistence"]["rmse_cfs"]
    if a_rmse < p_rmse and a_rmse < NWM_NORA_RMSE_CFS:
        verdict = "nwm_left_gage_skill"
    elif a_rmse < p_rmse:
        verdict = "anderson_beats_persistence_not_nwm"
    else:
        verdict = "lower_white_own_system"
    indy_diag = None
    if pack.indy_cfs is not None:
        indy = np.asarray(pack.indy_cfs, dtype=float)
        best_t, best_c = 0, -2.0
        icurve = []
        for t in range(0, MAX_LAG_DAYS + 1):
            c = _corr(_lag(nora, t)[train], indy[train])
            icurve.append({"tau_days": t, "corr_train": c})
            if np.isfinite(c) and c > best_c:
                best_t, best_c = t, c
        indy_diag = {"tau_days": best_t, "corr_train": best_c, "curve": icurve, "role": "diagnostic"}
    return {
        "tau_star": tau,
        "lag_curve": curve,
        "skill": skill,
        "verdict": verdict,
        "indy_in_X": False,
        "indy_diagnostic": indy_diag,
        "holdout": {
            "dates": pack.dates[ho],
            "nora_cfs": y_ho,
            "persistence_cfs": pers_ho,
            "anderson_lag_cfs": yhat,
        },
        "predictor_sites": ["03348000"],
        "label_site": "03351000",
    }


def assert_no_indy_in_X(fit: dict[str, Any]) -> None:
    if INDY_ID in fit.get("predictor_sites") or fit.get("indy_in_X"):
        raise LeakError("Indianapolis used as a Nora predictor")
