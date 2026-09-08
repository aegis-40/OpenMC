# Aegis-40 decay heat & activity — rigorous (chain-coupled) vs curated

- Decay run: `docs/competition/waste/decay_run/depletion_results.h5`
- Chain: `/home/samira/openmc_data/chain_endfb80_pwr.xml`
- Rigorous = zero-flux IndependentOperator over the full chain (all nuclides + in-growth); curated = source_term 20-nuclide quick-look.

| cooling (yr) | decay heat W (rigorous) | decay heat W (curated) | activity Bq (rigorous) | activity Bq (curated) |
|---|---|---|---|---|
| 0 | 7.947e+06 | 1.655e+04 | 2.764e+19 | 1.230e+17 |
| 1 | 4.840e+04 | 1.423e+04 | 4.658e+17 | 1.115e+17 |
| 3 | 1.874e+04 | 1.123e+04 | 2.215e+17 | 9.546e+16 |
| 5 | 1.234e+04 | 9.519e+03 | 1.614e+17 | 8.487e+16 |
| 10 | 8.966e+03 | 7.497e+03 | 1.193e+17 | 6.872e+16 |
| 30 | 5.988e+03 | 4.643e+03 | 6.629e+16 | 3.727e+16 |
| 50 | 4.321e+03 | 3.079e+03 | 4.002e+16 | 2.158e+16 |
| 100 | 2.274e+03 | 1.272e+03 | 1.285e+16 | 6.422e+15 |
| 300 | 9.537e+02 | 3.102e+02 | 1.298e+15 | 4.197e+14 |
| 1000 | 4.171e+02 | 2.087e+02 | 5.966e+14 | 2.518e+14 |
| 10000 | 1.127e+02 | 1.108e+02 | 2.288e+14 | 1.361e+14 |
| 100000 | 9.995e+00 | 6.061e+00 | 2.566e+13 | 1.048e+13 |

_If rigorous >> curated at <5 yr (expected — short-lived FPs) but the two converge by ~10-30 yr, that convergence is the V&V check. Use the rigorous column for §8.11 and the cask thermal design._
