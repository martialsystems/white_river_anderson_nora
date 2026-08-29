# Agent notes: white_river_anderson_nora

Public GitHub. MIT. Question: Does lagged USGS daily mean 00060 at Anderson beat lag-1 USGS daily mean 00060 at Nora?

Science lock: `58859be`. Yes: 971 vs 1,243 vs 1,316. Cheaper gage beat both. Do not restamp NWM-error (`fa2e315` / `fbbe1fd`). That tree is NWM vs lag-1 00060. This tree is a cheaper gage beat both.

Do not edit rain-stage, Nora HAND, FIM, HWM, or map-completion. Do not download NWM again. Do not use Indianapolis as a Nora predictor. Do not invert Nora 00060 to feet. Do not open a sixth raster tree.

`upqforge/` GraphForge pin: no `p_sfha`, tau* from train, Indy not a predictor, NWIS fetch-or-stop, no NWM re-pull.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`
