# Digital Appendix - Operating biological-shield dose (37-FA, final CAD radial build)

The Chapter 8.x radiation-shielding evidence: operating-power biological-shield dose and RPV fast fluence for the final 37-FA core and the latest CAD radial build.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`inputs/radial-build.md` - the CAD-anchored radial layer stack (37-FA core envelope R755.4, barrel R975/1000, downcomer to RPV-in R1350, RPV R1350/1515, then the **adopted §4.3 shield**: 5 cm SS thermal shield + **20 cm borated PE** neutron layer + **180 cm magnetite concrete** + 10 cm finish; outer shield diameter ~7.63 m). Source = 125 MWth fission emission. Full write-up in `README_results.md`.

## Approach
Two complementary methods: (1) **OpenMC 0.15.3 fixed-source coupled neutron+gamma** transport (`code/shield_37fa_cad.py`, materials/dose/weight-windows in `code/shielding_common.py`) - volume-smeared core emitter (Watt neutrons + Maienschein prompt-fission gammas), ICRP-116 AP flux-to-dose, MAGIC weight windows - for the RPV fast fluence; (2) an **ANS-6.4 point-kernel / removal-cross-section** hand calculation (`code/point_kernel_dose.py`) for the occupational dose, anchored on the converged MC RPV flux. `code/aegis40_cask_v7.py` is the spent-fuel cask (Task B).

## Outputs obtained
`outputs/shield_37fa_results.json` + `figures/shield_cross_section_37fa.png`:
- **RPV fast (E>1 MeV) flux 1.59e9 n/cm2/s -> 60-yr fluence 3.0e18 n/cm2 < 1e19 limit (PASS)**.
- **Operational dose: gamma ~5e-7 uSv/h; fast neutron 0.23 uSv/h nominal (<=5.5 uSv/h across the removal-cross-section band) -> total ~0.23 uSv/h < 10 uSv/h target (PASS, ~40x margin)**.
The earlier 10 cm-PE / 120 cm-magnetite stack did not robustly meet the neutron target; the borated-PE and magnetite bulk were resized (+70 cm radial) to close it - see `README_results.md` sections 4.2-4.3.

## How to reproduce
```bash
OPENMC_THREADS=8 python code/shield_37fa_cad.py   # MC RPV fast fluence
python code/point_kernel_dose.py                  # ANS-6.4 point-kernel dose (n + gamma)
python code/plot_shield_cross_section_37fa.py     # Figure 1 cross-section
```

## Verification & validation (reliable sources)
Neutron removal cross sections from Rockwell (*Reactor Shielding Design Manual*, TID-7004) and Chilton/Shultis/Faw; gamma coefficients from NIST-XCOM; ICRP-116 dose coefficients; materials/architecture per Ogul et al. (2026) SMART multilayer and Bagheri & Khalafi (2023). Lead-free by team constraint.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
