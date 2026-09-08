# Digital Appendix - ICSBEP criticality validation (OECD/NEA measured experiments)

Experimental validation of the OpenMC + ENDF/B-VIII.0 stack against measured critical experiments. This is the explicit 'reliable-source (IAEA/OECD-NEA) data' gate.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`inputs/case-1,2,5,7/` are complete OpenMC decks (geometry/materials/settings.xml) for four LEU-COMP-THERM-008 low-enriched-uranium lattice criticals from the OECD/NEA ICSBEP Handbook.

## Approach
Each benchmark configuration is modelled as-published and run in eigenvalue mode; computed k_eff is compared to the evaluated benchmark-model k_eff (1.0007 +/- 0.0016 for LCT-008 - note this is NOT unity).

## Outputs obtained
`outputs/results.csv` - computed vs benchmark k_eff for all four cases. The ICSBEP benchmark-model k_eff is 1.0007 +/- 0.0016 (NOT unity), so C-E = k_calc - 1.0007: -23, -28, -8, -143 pcm. Mean bias = -50 pcm; every case within the handbook experimental uncertainty (worst 0.86 sigma).

## How to reproduce
```bash
`cd inputs/case-1 && openmc` (repeat per case); compare with outputs/results.csv.
```

## Verification & validation (reliable sources)
Source: OECD/NEA ICSBEP Handbook, LEU-COMP-THERM-008. This is measured-data validation, not code-to-code.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
