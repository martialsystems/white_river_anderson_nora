# White River Anderson → Nora Q

Does lagged USGS Q at Anderson beat yesterday's Q at Nora?

Yes, on this split. tau* = 1 day (train). Holdout RMSE: Anderson lag **971 cfs**, Nora persistence **1,243 cfs**, NWM at Nora **1,316 cfs** (cited from `fa2e315`, not recomputed). NWM left gage skill on the table. Indianapolis is downstream: diagnostic only, not a predictor.

This tree does not read `p_sfha` and does not paint HAND. Same temporal split as NWM error: train through 2018-09-30, hold out through 2020-12-31.

NWM error: https://github.com/martialsystems/white_river_nwm_error (`fa2e315`)  
Rain-stage: https://github.com/martialsystems/white_river_rain_stage (`e41fd69`)

![Figure 1. Holdout hydrograph](logs/nora_live/hydrograph.png)

Figure 1. Nora Q, Nora persistence, Anderson lag 1 day. Discharge in cfs, not feet.

![Figure 2. Lag correlation](logs/nora_live/lag_corr.png)

Figure 2. Train corr versus lag. Travel time between gages, not a wet mask. tau* from train only.

## Live skill (holdout WY2019 to 2020)

| Model | RMSE (cfs) | MAE (cfs) |
|-------|-----------:|----------:|
| Nora persistence | 1,243 | 549 |
| Anderson lag 1 d (scale 2.30) | 971 | 531 |
| NWM at Nora (cited `fa2e315`) | 1,316 | n/a |

Caveats (none reverse the ranking): 1-coefficient scale includes drainage-area; daily 00060; no 2026 overlay.

## Stage 0

Synthetic Anderson lag 2 so CI recovers tau* without NWIS. Fixture under `logs/stage0_fixture/`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```

Two figures max. Empty NWIS stops (`run_live.py` exit 2).

| File | Role |
|------|------|
| [METHODOLOGY.md](METHODOLOGY.md) | Locked contract |
| [AGENTS.md](AGENTS.md) | Agent rules |
| [CHECKLIST.md](CHECKLIST.md) | Operator list |
| `src/upq/` | NWIS, tau*, skill, figures |
| `upqforge/` | GraphForge pin |
