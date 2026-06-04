# Aegis-40 decay heat & activity — rigorous (chain-coupled) vs curated

- Decay run: `docs/competition/waste/decay_run/depletion_results.h5`
- Chain: `/mnt/d/openmc_data/chain_endfb80_pwr.xml`
- Rigorous = zero-flux IndependentOperator over the full chain (all nuclides + in-growth); curated = source_term 20-nuclide quick-look.

| cooling (yr) | decay heat W (rigorous) | decay heat W (curated) | activity Bq (rigorous) | activity Bq (curated) |
|---|---|---|---|---|
| 0 | 7.747e+06 | 1.822e+04 | 2.778e+19 | 1.200e+17 |
| 1 | 5.093e+04 | 1.524e+04 | 4.477e+17 | 1.062e+17 |
| 3 | 1.922e+04 | 1.145e+04 | 2.014e+17 | 8.751e+16 |
| 5 | 1.212e+04 | 9.333e+03 | 1.412e+17 | 7.588e+16 |
| 10 | 8.318e+03 | 7.003e+03 | 1.018e+17 | 5.976e+16 |
| 30 | 5.444e+03 | 4.247e+03 | 5.615e+16 | 3.195e+16 |
| 50 | 3.930e+03 | 2.820e+03 | 3.386e+16 | 1.845e+16 |
| 100 | 2.087e+03 | 1.188e+03 | 1.092e+16 | 5.513e+15 |
| 300 | 8.400e+02 | 2.648e+02 | 1.106e+15 | 3.537e+14 |
| 1000 | 3.415e+02 | 1.546e+02 | 4.664e+14 | 1.868e+14 |
| 10000 | 8.075e+01 | 7.795e+01 | 1.563e+14 | 9.620e+13 |
| 100000 | 7.082e+00 | 3.859e+00 | 2.205e+13 | 7.246e+12 |

_If rigorous >> curated at <5 yr (expected — short-lived FPs) but the two converge by ~10-30 yr, that convergence is the V&V check. Use the rigorous column for §8.11 and the cask thermal design._
