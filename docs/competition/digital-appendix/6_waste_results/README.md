# Digital Appendix - Back-end fuel cycle (inventory, decay heat, source term, safeguards)

The Chapter 8.11 waste and safeguards numbers, computed from the STAT_FINAL discharge inventory.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`code/extract_discharge_inventory.py` reads the depletion result; `run_decay_heat.py`, `run_source_spectra.py`, `run_waste_intensity.py`, `run_safeguards_attractiveness.py` derive the back-end quantities. Discharge burnup 29.6 GWd/tHM, 2224 EFPD.

## Approach
Nuclide inventory from OpenMC depletion; decay heat by rigorous nuclide summation (ANS-5.1-consistent); neutron/gamma source terms vs cooling time; Bathke figure-of-merit for the discharge Pu vector.

## Outputs obtained
`outputs/`: discharge_inventory.csv, decay_heat_rigorous.csv, source_term_vs_cooling.csv, waste_intensity.csv (~4.40 tHM/TWhe), storage_criticality.csv. Discharge Pu is reactor-grade (high Pu-240).

## How to reproduce
```bash
`PYTHONPATH=src python3 code/run_decay_heat.py` etc. (each reads the discharge inventory).
```

## Verification & validation (reliable sources)
Decay-heat method cross-checked against ANS-5.1 decay-heat standard; waste intensity benchmarked to CAREM-25 once-through band.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
