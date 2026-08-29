# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from upq.config import QUESTION
from upq.pipeline import stage0_fixture


def test_fixture_two_figures(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["question"] == QUESTION
    assert report["indy_in_X"] is False
    assert report["figures"] == ["hydrograph.png", "lag_corr.png"]
    assert (tmp_path / "hydrograph.png").is_file()
    assert (tmp_path / "lag_corr.png").is_file()
