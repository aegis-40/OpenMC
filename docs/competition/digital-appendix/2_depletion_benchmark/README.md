# Digital Appendix - Depletion benchmark + Aegis-40 depletion driver

Validates the OpenMC depletion capability (CoupledOperator + Predictor integrator, ENDF/B-VIII.0 chain) and provides the driver used for the Aegis-40 cycle depletion.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`code/benchmark_depletion_pincell.py` builds the OpenMC-internal BEAVRS 2.4% PWR pincell (no external geometry - maximally reproducible). `code/run_depletion_fixed.py` is the Aegis-40 full-core depletion driver.

## Approach
Reproduces the published Romano (2021) OpenMC-vs-Serpent validation configuration (identical model/schedule/chain); `--repeat <seed>` demonstrates seed-to-seed repeatability.

## Outputs obtained
k_eff within ~20 pcm and actinides/fission-products within ~1% of the Romano (2021) reference across burnup; Aegis-40 cycle reaches ~29.6 GWd/tHM at 2224 EFPD.

## How to reproduce
```bash
`python code/benchmark_depletion_pincell.py` (add `--repeat 12345` for repeatability).
```

## Verification & validation (reliable sources)
Code-to-code benchmark vs Serpent (Romano 2021, published). Reproducibility + repeatability legs included.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
