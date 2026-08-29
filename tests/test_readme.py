# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from upq.claims import scan_text
from upq.config import QUESTION

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    assert "Anderson" in text
    assert "Indianapolis" in text
    assert "diagnostic" in text.lower()
    assert "fa2e315" in text
    assert "p_sfha" in text
    assert scan_text(text) == []
    assert "—" not in text
    assert "What it is not" not in text
