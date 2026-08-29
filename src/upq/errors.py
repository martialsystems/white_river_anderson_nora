# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class FetchError(GateError):
    """NWIS empty or 404."""


class SplitError(GateError):
    """Temporal split leaked holdout, or tau* chosen on holdout."""


class FigureCapError(GateError):
    """This tree stops at two figures."""


class LeakError(GateError):
    """Indianapolis used as a Nora predictor."""
