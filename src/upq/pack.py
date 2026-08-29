# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class QPack:
    """Daily Q. Indianapolis is diagnostic only and must not enter X."""

    dates: np.ndarray
    anderson_cfs: np.ndarray
    nora_cfs: np.ndarray
    indy_cfs: np.ndarray | None = None
    source: str = "fixture"
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def n_days(self) -> int:
        return int(self.dates.shape[0])
