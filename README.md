# White River Anderson → Nora Q

Does yesterday at Anderson help you guess Nora's flow today?

Most days, yes. Anderson lag 1 d, scaled, is 971 cfs RMSE against yesterday at Nora 1,243 and NWM 1,316 (`fa2e315`, not recomputed). A cheaper gage beat both.

So this is not "we timed the wave." Train corr is 0.88 at lag 1 d and 0.87 at lag 0: daily 00060 barely sees travel time. Anderson already has the pulse. Yesterday at Anderson is still what you can use this morning.

Science lock: `58859be`.

Indianapolis 03353000 is downstream of Nora: diagnostic only, not a predictor. This tree does not read `p_sfha` and does not paint HAND. NWM-error stays "NWM vs lag-1 00060 at each gage." Do not restamp it.

![Figure 1. Holdout hydrograph](logs/nora_live/hydrograph.png)

Figure 1. Nora 00060, Nora 00060 lag 1 d, Anderson 00060 lag 1 d scaled on train. cfs. 971 beats 1,243.

![Figure 2. Lag correlation](logs/nora_live/lag_corr.png)

Figure 2. Train corr vs lag. tau* = 1 d (0.88) vs lag 0 (0.87). Scale 2.30 is drainage area plus lag, not a routing time. Daily 00060. No 2026. None of that flips 971 < 1,243.

## What was compared

White River, Indiana, upstream to downstream:

| USGS site | Official name | Role |
|-----------|---------------|------|
| 03348000 | White River at Anderson, IN | Feature: daily mean discharge **00060**, lagged 0 to 7 calendar days |
| 03351000 | White River near Nora, IN | Label: daily mean **00060** on day t |
| 03353000 | White River at Indianapolis, IN | Diagnostic only. Downstream of Nora. Not a feature. |

00060 is USGS daily mean discharge in cfs. Not gage height 00065. Not feet.

tau* is chosen on train (through 2018-09-30) as the lag in 0 to 7 days that maximizes Pearson corr(Anderson 00060 lagged, Nora 00060). Frozen at 1 d. Then Nora 00060 is predicted as 2.30 * Anderson 00060(lag 1 d) + 390, coefficients from train only.

The NWM column is retrospective v2.1 streamflow at COMID 18476353 versus the same Nora 00060 on this split (RMSE 1,316 cfs). This repo does not download NWM again.

## Live skill (holdout 2018-10-01 to 2020-12-31)

| Predictor of Nora 00060 on day t | RMSE (cfs) | MAE (cfs) |
|---------------------------------|-----------:|----------:|
| Nora 00060 lag 1 calendar day | 1,243 | 549 |
| 2.30 * Anderson 00060 lag 1 d + 390 | 971 | 531 |
| NWM v2.1 at Nora COMID (cited fa2e315) | 1,316 | n/a |

## Stage 0

Synthetic Anderson 00060 routed to Nora at lag 2 so CI recovers tau* without NWIS. Fixture under `logs/stage0_fixture/`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```

Two figures max. Empty NWIS 00060 stops (`run_live.py` exit 2).

| File | Role |
|------|------|
| [METHODOLOGY.md](METHODOLOGY.md) | Locked contract |
| [AGENTS.md](AGENTS.md) | Agent rules |
| [CHECKLIST.md](CHECKLIST.md) | Operator list |
| `src/upq/` | NWIS 00060, tau*, skill, figures |
| `upqforge/` | GraphForge pin |

Parent: 
- [![white_river_nwm_error](https://img.shields.io/badge/white__river__nwm__error-2e7d32?style=for-the-badge)](https://github.com/martialsystems/white_river_nwm_error) (Nora persistence 1,243 / NWM 1,316 cited)
  
Next reach:
- [![white_river_fall_creek_gap](https://img.shields.io/badge/white__river__fall__creek__gap-2e7d32?style=for-the-badge)](https://github.com/martialsystems/white_river_fall_creek_gap)
  
Write-up:
- [![White River Q](https://img.shields.io/badge/White_River_Q-2e7d32?style=for-the-badge)](https://gist.github.com/martialsystems/1104e5e47b8a04006ec694d289d43639)

This tree does not read `p_sfha` and is not a flood map.

[![Open the research console](https://img.shields.io/badge/Open_the_research_console-2e7d32?style=for-the-badge)](https://martialsystems.github.io/indiana_wx_pages/)
