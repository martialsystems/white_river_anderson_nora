# Methodology: lagged Anderson Q versus Nora persistence

Question: Does lagged USGS daily mean 00060 at Anderson beat lag-1 USGS daily mean 00060 at Nora?

## Layers

| Layer | Role | Source |
|-------|------|--------|
| Feature | lagged 00060 | NWIS 03348000 Anderson |
| Label | 00060 | NWIS 03351000 Nora. Not 00065. |
| Diagnostic | 00060 | NWIS 03353000 Indianapolis. Downstream of Nora. Not a feature. |
| Split | comparable to NWM error | Train through 2018-09-30, hold out 2018-10-01 to 2020-12-31 |

tau* is argmax of train correlation for lags 0 to 7 days, then frozen. Holdout scores a 1-coefficient scale fit of Anderson daily mean 00060 at that lag. The local bar is Nora daily mean 00060 from the previous calendar day. NWM Nora RMSE 1,316 cfs is cited from `fa2e315`, not recomputed.

Live: tau* = 1 day. Anderson 00060 lag 1 d RMSE 971 cfs beats Nora 00060 lag 1 d (1,243) and cited NWM (1,316). Indianapolis train corr is same-day 0.99 (downstream diagnostic).

No Stage IV. No NWM zarr download. No 2026 overlay. No feet inversion.

## Figures

1. Holdout hydrograph: Nora Q, persistence, Anderson lag. cfs.
2. Train corr versus lag, tau* marked. Travel time between gages, not a wet mask.

## Claims

Allowed: lagged Anderson Q versus Nora persistence; lower White is its own system, or NWM left gage skill, according to the holdout ranking; Indianapolis is diagnostic only.

Banned: P as a forecast; HAND as a FIRM; lag-scatter as inundation; Indianapolis as a Nora predictor; inverting Nora Q to feet; a third figure.
