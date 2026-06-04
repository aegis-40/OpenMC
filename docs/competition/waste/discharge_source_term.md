# Aegis-40 discharge source term (FER §8.11) — generated

- Generated: `2026-06-04T09:58:53.827008+00:00`
- Depletion results: `/mnt/d/conda-envs/openmc-py311/SMRs/Claude version/aegis40_3d_core_outputs/08_depletion_baseline/depletion_results.h5`
- Nominal core HM loading: 5.6 t

## Bridge-accessor validation

| probe | result |
|---|---|
| materials accessor | `results[0].index_mat` (6 materials) |
| nuclides accessor | `results[0].index_nuc` (3820 nuclides) |
| mass accessor | `results.get_mass(mat, nuc) -> (times, mass[g])` |
| timesteps in results | 19 |

## Inventory totals

- Total mass tracked: **6.0561 t** (6.056e+06 g)
- Heavy metal (U+Np+Pu+Am+Cm): **5.0413 t** (nominal 5.6 t — ratio 0.900)
- Nuclides tracked: 2004; with decay data: 20; without: 1984

## Source term at discharge (0 yr cooling)

- Total activity: **1.200e+17 Bq** (3.243e+06 Ci)
- Decay heat: **1.822e+04 W** (3.615e+03 W/tHM)
- Ingestion radiotoxicity: **2.175e+09 Sv**
- Bulk specific activity: 1.981e+10 Bq/g; heat density ~3.129e+04 W/m³
- **Waste class (bulk SNF): HLW** — decay heat 3.13e+04 W/m^3 >= 2000 W/m^3 (heat-generating)

### Top nuclides by activity at discharge

| nuclide | grams | activity (Bq) | T½ (yr) |
|---|---|---|---|
| Cs134 | 8.163e+02 | 3.902e+16 | 2.065 |
| Pu241 | 7.697e+03 | 2.948e+16 | 14.33 |
| Cs137 | 8.646e+03 | 2.775e+16 | 30.08 |
| Sr90 | 3.909e+03 | 1.996e+16 | 28.79 |
| Eu154 | 1.703e+02 | 1.701e+15 | 8.6 |
| Pu238 | 1.507e+03 | 9.552e+14 | 87.7 |
| Cm244 | 2.694e+02 | 8.069e+14 | 18.1 |
| Pu240 | 1.362e+04 | 1.144e+14 | 6561 |
| Sm151 | 6.950e+01 | 6.765e+13 | 90 |
| Pu239 | 2.894e+04 | 6.642e+13 | 2.411e+04 |
| Am241 | 3.715e+02 | 4.713e+13 | 432.6 |
| Am243 | 7.101e+02 | 5.245e+12 | 7370 |
| Tc99 | 5.754e+03 | 3.642e+12 | 2.111e+05 |
| Pu242 | 3.571e+03 | 5.205e+11 | 3.75e+05 |
| U234 | 1.179e+03 | 2.715e+11 | 2.455e+05 |

### Nuclides present but missing decay data (extend NUCLIDE_DATA if any are significant)

O16, Gd158, Xe136, Gd156, Xe134, Ba138, Gd160, La139, Ce140, Nd144, Ce142, Cs133, Pr141, Xe132, Mo100, Mo98, Zr96, Mo97, Ru102, Zr94, Ru101, Nd143, Zr93, Mo95, Nd146, Nd145, Zr92, Zr91, Cs135, Ru104, Y89, Rh103, Xe131, Pd105, Te130, Nd148, Sr88, Sm150, Rb87, Pd106

## Decay heat & radiotoxicity vs cooling time

| cooling (yr) | activity (Bq) | decay heat (W) | radiotox (Sv) |
|---|---|---|---|
| 0 | 1.200e+17 | 1.822e+04 | 2.175e+09 |
| 1 | 1.062e+17 | 1.524e+04 | 1.930e+09 |
| 3 | 8.751e+16 | 1.145e+04 | 1.607e+09 |
| 5 | 7.588e+16 | 9.333e+03 | 1.413e+09 |
| 10 | 5.976e+16 | 7.003e+03 | 1.163e+09 |
| 30 | 3.195e+16 | 4.247e+03 | 7.442e+08 |
| 50 | 1.845e+16 | 2.820e+03 | 5.112e+08 |
| 100 | 5.513e+15 | 1.188e+03 | 2.433e+08 |
| 300 | 3.537e+14 | 2.648e+02 | 7.247e+07 |
| 1000 | 1.868e+14 | 1.546e+02 | 4.497e+07 |
| 10000 | 9.620e+13 | 7.795e+01 | 2.297e+07 |
| 100000 | 7.246e+12 | 3.859e+00 | 1.070e+06 |

_Quick-look independent-decay model (source_term.decay). For the rigorous chain-coupled curve (Pu-241→Am-241 in-growth) run openmc_bridge.run_decay_only and overlay._
