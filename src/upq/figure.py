# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from upq.claims import require_clean
from upq.config import MAX_FIGURES
from upq.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError(f"this tree stops at {MAX_FIGURES} figures")


def write_hydrograph(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ho = fit["holdout"]
    dates = [datetime.strptime(str(x)[:10], "%Y-%m-%d") for x in ho["dates"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(dates, ho["nora_cfs"], color="#222222", lw=1.4, label="Nora 00060")
    ax.plot(
        dates,
        ho["persistence_cfs"],
        color="#7a7a7a",
        lw=1.0,
        ls="--",
        label="Nora 00060 lag 1 d",
    )
    ax.plot(
        dates,
        ho["anderson_lag_cfs"],
        color="#1b6ca8",
        lw=1.2,
        label=f"Anderson 00060 lag {fit['tau_star']} d",
    )
    ax.set_ylabel("USGS daily mean 00060 (cfs)")
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper left", fontsize=7, frameon=False)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.16, top=0.88, left=0.12, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_lag_curve(dest: Path, *, fit: dict[str, Any], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    curve = fit["lag_curve"]
    taus = [int(r["tau_days"]) for r in curve]
    corrs = [r["corr_train"] for r in curve]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(taus, corrs, color="#1b6ca8", marker="o")
    ax.axvline(fit["tau_star"], color="#b36b00", ls=":", lw=1.0, label=f"tau* = {fit['tau_star']} d")
    ax.set_xlabel("lag (days), Anderson leading Nora")
    ax.set_ylabel("train correlation")
    ax.set_title(title, fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.text(0.5, 0.03, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.18, top=0.88, left=0.14, right=0.98)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=130)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, fit: dict[str, Any]) -> list[Path]:
    paths = [
        write_hydrograph(
            log_dir / "hydrograph.png",
            fit=fit,
            title="Nora holdout: USGS daily mean 00060",
            subtitle="Observed Nora 00060, Nora 00060 lag 1 d, Anderson 00060 lag tau*. cfs, not feet.",
        ),
        write_lag_curve(
            log_dir / "lag_corr.png",
            fit=fit,
            title="Train corr(Anderson 00060 lagged, Nora 00060)",
            subtitle="Lag in calendar days. tau* from train only. Indianapolis is not in this fit.",
        ),
    ]
    _cap(len(paths))
    return paths
