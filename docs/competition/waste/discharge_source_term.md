# Aegis-40 discharge source term (FER §8.11) — generated

- Generated: `2026-07-04T05:03:36.006579+00:00`
- Depletion results: `/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_neutronics_outputs (2)/aegis40_neutronics_outputs/08_depletion_baseline/depletion_results.h5`
- Nominal core HM loading: 9.386 t

## Bridge-accessor validation

| probe | result |
|---|---|
| materials accessor | `results[0].index_mat` (7 materials) |
| nuclides accessor | `results[0].index_nuc` (3820 nuclides) |
| mass accessor | `results.get_mass(mat, nuc) -> (times, mass[g])` |
| timesteps in results | 38 |

## Inventory totals

- Total mass tracked: **10.6905 t** (1.069e+07 g)
- Heavy metal (U+Np+Pu+Am+Cm): **9.0898 t** (nominal 9.386 t — ratio 0.968)
- Nuclides tracked: 2078; with decay data: 20; without: 2058

## Source term at discharge (0 yr cooling)

- Total activity: **1.230e+17 Bq** (3.325e+06 Ci)
- Decay heat: **1.655e+04 W** (1.820e+03 W/tHM)
- Ingestion radiotoxicity: **2.113e+09 Sv**
- Bulk specific activity: 1.151e+10 Bq/g; heat density ~1.610e+04 W/m³
- **Waste class (bulk SNF): HLW** — decay heat 1.61e+04 W/m^3 >= 2000 W/m^3 (heat-generating)

### Top nuclides by activity at discharge

| nuclide | grams | activity (Bq) | T½ (yr) |
|---|---|---|---|
| Pu241 | 8.661e+03 | 3.317e+16 | 14.33 |
| Cs137 | 1.004e+04 | 3.223e+16 | 30.08 |
| Cs134 | 6.191e+02 | 2.959e+16 | 2.065 |
| Sr90 | 4.906e+03 | 2.504e+16 | 28.79 |
| Eu154 | 1.560e+02 | 1.558e+15 | 8.6 |
| Pu238 | 1.105e+03 | 7.006e+14 | 87.7 |
| Cm244 | 9.247e+01 | 2.769e+14 | 18.1 |
| Pu240 | 1.613e+04 | 1.355e+14 | 6561 |
| Pu239 | 4.786e+04 | 1.099e+14 | 2.411e+04 |
| Sm151 | 1.049e+02 | 1.021e+14 | 90 |
| Am241 | 5.778e+02 | 7.331e+13 | 432.6 |
| Tc99 | 7.067e+03 | 4.473e+12 | 2.111e+05 |
| Am243 | 3.554e+02 | 2.625e+12 | 7370 |
| U234 | 2.496e+03 | 5.748e+11 | 2.455e+05 |
| Pu242 | 2.465e+03 | 3.593e+11 | 3.75e+05 |

### Nuclides present but missing decay data (extend NUCLIDE_DATA if any are significant)

O16, Xe136, Gd158, Xe134, Gd156, Ba138, La139, Ce140, Cs133, Ce142, Pr141, Nd144, Xe132, Mo100, Nd143, Gd160, Zr96, Mo98, Mo97, Zr94, Ru101, Zr93, Ru102, Mo95, Nd145, Cs135, Zr92, Nd146, Zr91, Y89, Ru104, Xe131, Rh103, Sr88, Te130, Nd148, Pd105, O18, Rb87, Sm150

## Decay heat & radiotoxicity vs cooling time

| cooling (yr) | activity (Bq) | decay heat (W) | radiotox (Sv) |
|---|---|---|---|
| 0 | 1.230e+17 | 1.655e+04 | 2.113e+09 |
| 1 | 1.115e+17 | 1.423e+04 | 1.916e+09 |
| 3 | 9.546e+16 | 1.123e+04 | 1.650e+09 |
| 5 | 8.487e+16 | 9.519e+03 | 1.483e+09 |
| 10 | 6.872e+16 | 7.497e+03 | 1.249e+09 |
| 30 | 3.727e+16 | 4.643e+03 | 8.008e+08 |
| 50 | 2.158e+16 | 3.079e+03 | 5.455e+08 |
| 100 | 6.422e+15 | 1.272e+03 | 2.541e+08 |
| 300 | 4.197e+14 | 3.102e+02 | 8.574e+07 |
| 1000 | 2.518e+14 | 2.087e+02 | 6.079e+07 |
| 10000 | 1.361e+14 | 1.108e+02 | 3.272e+07 |
| 100000 | 1.048e+13 | 6.061e+00 | 1.667e+06 |

_Quick-look independent-decay model (source_term.decay). For the rigorous chain-coupled curve (Pu-241→Am-241 in-growth) run openmc_bridge.run_decay_only and overlay._
