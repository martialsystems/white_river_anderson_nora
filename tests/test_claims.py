# Copyright (c) 2026 Martial Systems LLC

from upq.claims import scan_text
from upq.config import QUESTION


def test_question_and_bans() -> None:
    assert scan_text(QUESTION) == []
    assert "indy_pred" in scan_text("Indianapolis is a Nora predictor")
    assert "lag_wet" in scan_text("lag-scatter is a wet mask")
    assert "nwm_repull" in scan_text("re-pulling NWM")
