# Digital Appendix - Spent-fuel storage-rack criticality

Demonstrates the discharged fuel stays sub-critical in the storage rack, consistent with the soluble-boron-free design (no credit for soluble boron).

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`code/run_storage_criticality.py` - fresh-fuel bounding case (no results file) or burnup-credit case (`--results depletion_results.h5`). Rack pitch, poison and water conditions set in-script.

## Approach
Eigenvalue criticality of a periodic rack cell in unborated water; 95/95 margin applied to the mean.

## Outputs obtained
k(95/95) <= 0.95 in unborated water for the bounding geometry (values in outputs/).

## How to reproduce
```bash
`PYTHONPATH=src python3 code/run_storage_criticality.py`.
```

## Verification & validation (reliable sources)
Bounding cases cross-checked against the Kim/Jung/Yoon (2024) SBF small-PWR sub-criticality band.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
