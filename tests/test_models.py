# Copyright (c) 2026 Martial Systems LLC

from upq.config import INDY_ID
from upq.errors import LeakError
from upq.fixture import TRUE_LAG, build_fixture
from upq.models import assert_no_indy_in_X, fit_pack


def test_fixture_recovers_lag_and_excludes_indy() -> None:
    fit = fit_pack(build_fixture())
    assert fit["tau_star"] == TRUE_LAG
    assert INDY_ID not in fit["predictor_sites"]
    assert fit["indy_in_X"] is False
    assert_no_indy_in_X(fit)
    assert fit["skill"]["nwm_nora_cited"]["source"] == "fa2e315"
    dirty = dict(fit)
    dirty["predictor_sites"] = ["03348000", INDY_ID]
    try:
        assert_no_indy_in_X(dirty)
        raise AssertionError("expected leak")
    except LeakError:
        pass
