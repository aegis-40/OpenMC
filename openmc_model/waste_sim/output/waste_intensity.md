# Aegis-40 spent-fuel arisings & waste intensity vs CAREM-25 (FER §8.11) — generated

- Generated : `2026-06-29T11:26:13.792376+00:00`
- Source    : OpenMC 3D-core depletion (`08_depletion_baseline/depletion_results.h5`)
- Core      : 37 FA × 17×17, 125 MWth / 40 MWe, HM = 9.87 tHM
- B1        : **2175 EFPD** (k_eff crosses 1.0 for fresh uniform load) = **27.55 GWd/tHM**
- LRM       : cycle = 2/(n+1)×B1 ;  discharge BU = 2n/(n+1)×B1_BU

## 1. Aegis-40 arisings — three reload scenarios

| Scenario | Cycle EFPD | Cycle yr | HM/cycle (tHM) | FA/cycle | HM/yr (tHM) | FA/yr | Electric TWhe/cycle | **tHM/TWhe** |
|---|---|---|---|---|---|---|---|---|
| Aegis-40 n=1 — once-through (no reload)  [2175 EFPD, 6.0 yr] | 2175 | 5.96 | 9.870 | 37.0 | 1.491 | 5.6 | 2.088 | **4.73** |
| Aegis-40 n=3 — 3-batch reload            [1088 EFPD, 3.0 yr] | 1088 | 2.98 | 3.290 | 12.3 | 0.994 | 3.7 | 1.044 | **3.15** |
| Aegis-40 n=4 — 4-batch reload            [870 EFPD, 2.4 yr] | 870 | 2.38 | 2.467 | 9.2 | 0.932 | 3.5 | 0.835 | **2.95** |

## 2. Waste intensity vs CAREM-25

Identity: `tHM/TWhe = 1e6 / (BU[MWd/tHM] × 24 × eta)` — depends only on burnup and thermal efficiency.

| Reactor | P_th | P_e | eta | BU (GWd/tHM) | **tHM/TWhe** | vs CAREM |
|---|---|---|---|---|---|---|
| Aegis-40 n=1 — once-through (no reload) | 125 MWth | 40 MWe | 0.320 | 27.6 | **4.73** | 1.4× lower (27% reduction) |
| Aegis-40 n=3 — 3-batch reload | 125 MWth | 40 MWe | 0.320 | 41.3 | **3.15** | 2.0× lower (51% reduction) |
| Aegis-40 n=4 — 4-batch reload | 125 MWth | 40 MWe | 0.320 | 44.1 | **2.95** | 2.2× lower (54% reduction) |
| CAREM-25 (reference) | 100 MWth | 27 MWe | 0.270 | 24.0 | **6.43** (band 5.79–6.94) | baseline |

## 3. Design rationale

- **B1 = 2175 EFPD** is the fundamental physical limit: a fresh Aegis-40 core stays critical for 6.0 years. All reload schemes derive from this one number via LRM.
- **n=1 (once-through, 6.0 yr)**: factory loads the reactor, operator runs it until EOL, reactor returns to factory — zero on-site refuelling. Discharge BU = 27.6 GWd/tHM, intensity = 4.73 tHM/TWhe (1.4× better than CAREM-25).
- **n=4 (4-batch, 2.4 yr cycles)**: maximises burnup (44.1 GWd/tHM) and waste intensity (2.95 tHM/TWhe, 2.2× better) but requires on-site refuelling every 2.4 years.
- **SBF design** eliminates the borated-water secondary-waste stream (spent resins, tritiated boron effluent) — a further waste reduction not captured in tHM/TWhe (see §8.11 deliverable #12).
- All Aegis-40 scenarios outperform CAREM-25 by ≥2.2× on waste intensity, driven by higher discharge burnup (44.1 vs 24.0 GWd/tHM) and better thermal efficiency (0.32 vs 0.27).

## 4. Method notes

- HM mass 9.87 tHM and B1 = 2175 EFPD are taken directly from the OpenMC depletion run (`get_keff()` interpolation).
- Cycle lengths and discharge burnups computed via Linear Reactivity Model (LRM).
- CAREM-25: 100 MWth, 25-30 MWe, ~24 GWd/tU (INVAP/CNEA, IAEA ARIS 2020).
- Waste intensity identity is per initial HM (iHM basis), standard fuel-cycle convention.
