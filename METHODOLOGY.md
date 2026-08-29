# Methodology: lagged Anderson 00060 versus Nora lag-1 00060

Question: Does lagged USGS daily mean 00060 at Anderson beat lag-1 USGS daily mean 00060 at Nora?

Live science is `58859be`. Yes. 971 vs 1,243 vs 1,316 cfs on the same holdout. A cheaper gage beat Nora lag-1 00060 and beat cited NWM-at-Nora. NWM-error remains NWM versus lag-1 00060 at each gage; do not restamp it.

Train corr 0.88 at lag 1 d vs 0.87 at lag 0: daily 00060 barely sees travel time. The win is that Anderson already has the pulse. Anderson 00060 from the previous calendar day is still the morning nowcast.

Scale 2.30 is drainage area plus lag, not a routing time. Daily 00060. No 2026. None of that flips 971 < 1,243.

## Layers

| Layer | Role | Source |
|-------|------|--------|
| Feature | lagged 00060 | NWIS 03348000 Anderson |
| Label | 00060 | NWIS 03351000 Nora. Not 00065. |
| Diagnostic | 00060 | NWIS 03353000 Indianapolis. Downstream of Nora. Not a feature. |
| Split | same as NWM error | Train through 2018-09-30, hold out 2018-10-01 to 2020-12-31 |

tau* from train only. NWM Nora RMSE 1,316 cfs is cited from `fa2e315`, not recomputed.

## Figures

1. Holdout hydrograph: Nora 00060, Nora 00060 lag 1 d, Anderson 00060 lag 1 d. cfs.
2. Train corr versus lag. Caption: scale 2.30 is area plus lag, not routing time; daily 00060; no 2026; 971 < 1,243 holds.

## Claims

Allowed: lagged Anderson 00060 versus Nora lag-1 00060; a cheaper gage beat both; NWM left gage skill on the table; Indianapolis is diagnostic only.

Banned: P as a forecast; HAND as a FIRM; lag-scatter as inundation; Indianapolis as a Nora predictor; inverting Nora 00060 to feet; a third figure; restamping NWM-error.
