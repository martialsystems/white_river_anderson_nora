# Agent notes: white_river_anderson_nora

Public GitHub. MIT. Question: Does lagged USGS Q at Anderson beat yesterday's Q at Nora?

Do not edit NWM error (`fa2e315` / `fbbe1fd`), rain-stage, Nora HAND, FIM, HWM, or map-completion. Do not restamp those figures. Do not download NWM again. Do not use Indianapolis as a Nora predictor. Do not invert Nora Q to feet. Do not open a sixth raster tree.

`upqforge/` GraphForge pin: no `p_sfha`, tau* from train, Indy not a predictor, NWIS fetch-or-stop, no NWM re-pull.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
