# Aegis-40 decay heat & activity — rigorous (chain-coupled) vs curated

- Decay run: `waste_sim/output/decay_run/depletion_results.h5`
- Chain: `/home/useropenmc/openmc_data/chain_endfb80_pwr.xml`
- Rigorous = zero-flux IndependentOperator over the full chain (all nuclides + in-growth); curated = source_term 20-nuclide quick-look.

| cooling (yr) | decay heat W (rigorous) | decay heat W (curated) | activity Bq (rigorous) | activity Bq (curated) |
|---|---|---|---|---|
| 0 | 7.973e+06 | 4.439e+05 | 2.789e+19 | 4.717e+18 |
| 1 | 4.981e+04 | 1.952e+04 | 4.756e+17 | 2.849e+17 |
| 3 | 1.953e+04 | 8.439e+03 | 2.288e+17 | 1.491e+17 |
| 5 | 1.295e+04 | 5.558e+03 | 1.675e+17 | 1.096e+17 |
| 10 | 9.424e+03 | 3.325e+03 | 1.243e+17 | 7.732e+16 |
| 30 | 6.289e+03 | 1.902e+03 | 6.907e+16 | 3.939e+16 |
| 50 | 4.539e+03 | 1.370e+03 | 4.170e+16 | 2.266e+16 |
| 100 | 2.392e+03 | 7.695e+02 | 1.340e+16 | 6.730e+15 |
| 300 | 9.968e+02 | 3.212e+02 | 1.355e+15 | 4.426e+14 |
| 1000 | 4.319e+02 | 2.148e+02 | 6.175e+14 | 2.600e+14 |
| 10000 | 1.157e+02 | 1.137e+02 | 2.313e+14 | 1.407e+14 |
| 100000 | 1.042e+01 | 6.254e+00 | 2.603e+13 | 1.175e+13 |

_If rigorous >> curated at <5 yr (expected — short-lived FPs) but the two converge by ~10-30 yr, that convergence is the V&V check. Use the rigorous column for §8.11 and the cask thermal design._
