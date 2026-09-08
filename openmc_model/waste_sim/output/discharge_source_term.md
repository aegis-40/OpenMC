# Aegis-40 discharge source term (FER §8.11) — generated

- Generated: `2026-06-29T11:26:51.947125+00:00`
- Depletion results: `/mnt/c/projects/openmc/aegis/aegis40_neutronics_outputs/08_depletion_baseline/depletion_results.h5`
- Nominal core HM loading: 5.6 t

## Bridge-accessor validation

| probe | result |
|---|---|
| materials accessor | `results[0].index_mat` (8 materials) |
| nuclides accessor | `results[0].index_nuc` (3820 nuclides) |
| mass accessor | `results.get_mass(mat, nuc) -> (times, mass[g])` |
| timesteps in results | 36 |

## Inventory totals

- Total mass tracked: **10.6931 t** (1.069e+07 g)
- Heavy metal (U+Np+Pu+Am+Cm): **9.0802 t** (nominal 5.6 t — ratio 1.621)
- Nuclides tracked: 2088; with decay data: 50; without: 2038
- ⚠️ HM mass is off nominal by >10% — check whether the depletion volumes are whole-core or need pin-count scaling.

## Source term at discharge (0 yr cooling)

- Total activity: **4.717e+18 Bq** (1.275e+08 Ci)
- Decay heat: **4.439e+05 W** (4.888e+04 W/tHM)
- Ingestion radiotoxicity: **9.867e+09 Sv**
- Bulk specific activity: 4.411e+11 Bq/g; heat density ~4.317e+05 W/m³
- **Waste class (bulk SNF): SNF** — Specific activity 4.41e+11 Bq/g (threshold 4e+09) or heat density 4.32e+05 W/m³ exceeds HLW threshold (IAEA SSG-40). Spent nuclear fuel → HLW/SNF category.

### Top nuclides by activity at discharge

| nuclide | grams | activity (Bq) | T½ (yr) |
|---|---|---|---|
| Np239 | 2.612e+02 | 2.241e+18 | 0.00645 |
| Xe133 | 3.858e+01 | 2.672e+17 | 0.01437 |
| Mo99 | 1.363e+01 | 2.424e+17 | 0.007522 |
| Nb95 | 1.530e+02 | 2.225e+17 | 0.0958 |
| Zr95 | 2.792e+02 | 2.220e+17 | 0.1753 |
| Ce141 | 2.060e+02 | 2.173e+17 | 0.08898 |
| Ru103 | 1.636e+02 | 1.956e+17 | 0.1075 |
| Pr144 | 6.819e-02 | 1.908e+17 | 3.285e-05 |
| Ce144 | 1.604e+03 | 1.890e+17 | 0.78 |
| Sr89 | 1.204e+02 | 1.295e+17 | 0.1383 |
| I131 | 2.778e+01 | 1.278e+17 | 0.02197 |
| Nd147 | 2.862e+01 | 8.572e+16 | 0.03006 |
| Rh106 | 6.415e-04 | 8.484e+16 | 9.443e-07 |
| Ru106 | 6.460e+02 | 7.926e+16 | 1.018 |
| Pm147 | 1.426e+03 | 4.893e+16 | 2.623 |

### Nuclides present but missing decay data (extend NUCLIDE_DATA if any are significant)

O16, Xe136, Xe134, Gd158, Ba138, Gd156, La139, Ce140, Cs133, Ce142, Pr141, Nd144, Xe132, Mo100, Nd143, Zr96, Mo98, Mo97, Gd160, Zr94, Ru101, Ru102, Mo95, Nd145, Zr92, Nd146, Zr91, Y89, Ru104, Xe131, Rh103, Sr88, Te130, Nd148, Pd105, O18, Rb87, Sm150, Pd106, Kr86

## Decay heat & radiotoxicity vs cooling time

| cooling (yr) | activity (Bq) | decay heat (W) | radiotox (Sv) |
|---|---|---|---|
| 0 | 4.717e+18 | 4.439e+05 | 9.867e+09 |
| 1 | 2.849e+17 | 1.952e+04 | 2.795e+09 |
| 3 | 1.491e+17 | 8.439e+03 | 1.909e+09 |
| 5 | 1.096e+17 | 5.558e+03 | 1.614e+09 |
| 10 | 7.732e+16 | 3.325e+03 | 1.331e+09 |
| 30 | 3.939e+16 | 1.902e+03 | 8.512e+08 |
| 50 | 2.266e+16 | 1.370e+03 | 5.798e+08 |
| 100 | 6.730e+15 | 7.695e+02 | 2.706e+08 |
| 300 | 4.426e+14 | 3.212e+02 | 8.983e+07 |
| 1000 | 2.600e+14 | 2.148e+02 | 6.247e+07 |
| 10000 | 1.407e+14 | 1.137e+02 | 3.355e+07 |
| 100000 | 1.175e+13 | 6.254e+00 | 1.716e+06 |

_Quick-look independent-decay model (source_term.decay). For the rigorous chain-coupled curve (Pu-241→Am-241 in-growth) run openmc_bridge.run_decay_only and overlay._
