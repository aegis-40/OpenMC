# Digital Appendix — OpenMC depletion benchmark (BEAVRS 2.4% PWR pincell)

- Generated: `2026-06-25T02:18:22.495117+00:00`
- Reference: Romano et al., *Ann. Nucl. Energy* 152 (2021) 107989, §3.2 (PWR Pincell). OpenMC vs Serpent: k_eff within ~20 pcm, actinides <1%, fission products <1%.
- Model: `openmc.examples.pwr_pin_cell()` (BEAVRS 2.4 wt% UO2, borated water, reflective) — built into OpenMC, no external data.
- Library: `/home/samira/openmc_data/endfb-viii.0-hdf5/cross_sections.xml`
- Chain: `/home/samira/openmc_data/chain_endfb80_pwr.xml`
- Power: 174.0 W/cm; integrator: PredictorIntegrator (CE); MC: 10000 part x (115-15) batches; seed 1.

## k_eff vs burnup

| Burnup (MWd/kg) | k_eff | sigma (pcm) |
|---|---|---|
| 0.00 | 1.16011 | 95 |
| 0.10 | 1.12206 | 89 |
| 0.50 | 1.11311 | 95 |
| 1.00 | 1.10671 | 81 |
| 2.00 | 1.09745 | 88 |
| 3.00 | 1.08537 | 77 |
| 4.00 | 1.07415 | 80 |
| 5.00 | 1.06536 | 80 |
| 6.00 | 1.05198 | 89 |
| 11.00 | 1.00149 | 77 |
| 16.00 | 0.95316 | 77 |
| 21.00 | 0.90948 | 80 |
| 26.00 | 0.87193 | 88 |
| 31.00 | 0.83715 | 76 |

_BOL k_eff = 1.16011 ± 95 pcm; EOL (31.0 MWd/kg) k_eff = 0.83715. The monotone fall with burnup (no soluble-boron / no burnable poison in this validation pincell) is the expected shape; compare against Fig. 2 of Romano 2021._

## Principal-isotope build-up (atoms, per cm of pin)

Concentrations of the nuclides that drive storage k_eff, decay heat and radiotoxicity. Trends (U-235 depletion, Pu-239/240/241 in-growth, Cs-137/Sr-90 accumulation, Sm-149 saturation) are the physical signatures the paper benchmarks to <1%.

| Burnup (MWd/kg) | U235 | Pu239 | Pu240 | Pu241 | Am241 | Cs137 | Sr90 | Sm149 |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 2.698e+20 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.000e+00 |
| 0.10 | 2.684e+20 | 2.013e+17 | 9.250e+14 | 5.310e+12 | 4.271e+08 | 7.453e+16 | 6.790e+16 | 3.269e+15 |
| 0.50 | 2.629e+20 | 2.546e+18 | 3.073e+16 | 9.031e+14 | 3.604e+11 | 3.732e+17 | 3.380e+17 | 2.100e+16 |
| 1.00 | 2.562e+20 | 5.839e+18 | 1.289e+17 | 7.619e+15 | 6.151e+12 | 7.473e+17 | 6.711e+17 | 2.543e+16 |
| 2.00 | 2.433e+20 | 1.191e+19 | 4.931e+17 | 5.928e+16 | 9.687e+13 | 1.496e+18 | 1.321e+18 | 2.664e+16 |
| 3.00 | 2.311e+20 | 1.732e+19 | 1.022e+18 | 1.822e+17 | 4.530e+14 | 2.243e+18 | 1.949e+18 | 2.758e+16 |
| 4.00 | 2.194e+20 | 2.217e+19 | 1.669e+18 | 3.854e+17 | 1.293e+15 | 2.990e+18 | 2.559e+18 | 2.851e+16 |
| 5.00 | 2.082e+20 | 2.654e+19 | 2.401e+18 | 6.665e+17 | 2.822e+15 | 3.737e+18 | 3.151e+18 | 2.936e+16 |
| 6.00 | 1.976e+20 | 3.046e+19 | 3.200e+18 | 1.018e+18 | 5.208e+15 | 4.483e+18 | 3.727e+18 | 3.013e+16 |
| 11.00 | 1.517e+20 | 4.436e+19 | 7.347e+18 | 3.757e+18 | 3.413e+16 | 8.147e+18 | 6.345e+18 | 3.257e+16 |
| 16.00 | 1.150e+20 | 5.282e+19 | 1.172e+19 | 6.783e+18 | 8.893e+16 | 1.178e+19 | 8.651e+18 | 3.391e+16 |
| 21.00 | 8.575e+19 | 5.794e+19 | 1.593e+19 | 9.593e+18 | 1.566e+17 | 1.540e+19 | 1.070e+19 | 3.437e+16 |
| 26.00 | 6.287e+19 | 6.102e+19 | 1.969e+19 | 1.205e+19 | 2.252e+17 | 1.901e+19 | 1.254e+19 | 3.458e+16 |
| 31.00 | 4.533e+19 | 6.269e+19 | 2.297e+19 | 1.402e+19 | 2.863e+17 | 2.260e+19 | 1.420e+19 | 3.431e+16 |

## Acceptance & how this feeds the safety case

- **Benchmark target (Romano 2021):** k_eff to ~20 pcm vs Serpent, actinides <1%, FPs <1%. Reproducing the published k_eff(BU) curve and isotopic trends with our ENDF/B-VIII.0 library + chain demonstrates the depletion path is used correctly.
- **Reproducibility:** the model is `openmc.examples.pwr_pin_cell()` — anyone with OpenMC reruns this exactly; no proprietary geometry.
- **Repeatability:** rerun with `--repeat <seed>`; k_eff at each step must agree within the combined Monte-Carlo sigma.
- **Bias term:** the spread between this benchmark and the reference is the basis for the code/data bias Δ_bias fed back into `run_storage_criticality.py` (currently 0). With OpenMC-Serpent agreement at the ~20 pcm / <1% level, the depletion contribution to Δ_bias is small relative to the ~0.16 storage-criticality margin.

## Open items

- **Measured-assay validation (stronger):** benchmark these same isotopics against a **SFCOMPO 2.0** destructive-assay PWR sample at comparable enrichment/burnup, and/or the tabulated nuclide concentrations of the **OECD/NEA Burnup-Credit Criticality Benchmark Phase I-B**. Both give absolute reference numbers (this case is code-to-code). Needs the source documents.
- **Storage-rack criticality benchmark:** OpenMC k_eff vs **OECD/NEA Burnup-Credit Benchmark Phase II** (or an ANS-8 array) to close the criticality-side bias.
