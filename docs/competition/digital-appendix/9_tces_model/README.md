# Digital Appendix - Thermochemical energy-storage thermodynamic model

Validated thermodynamic model for the district-heat thermochemical store, supporting the Chapter 8.9 TCES sizing.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`inputs/smr-40mwe-pwr.edn` - the Aegis-40 40 MWe TCES configuration. `code/src/*.clj` - the Clojure thermodynamic model (core, modes, properties, thermo, smr).

## Approach
Equilibrium ad/desorption thermodynamics for the salt/ammine and zeolite stores; coefficient-of-performance and hot-side yield computed per operating mode.

## Outputs obtained
Reproduces Yan et al. (2020) COPh and hot-side yield for the NiCl2-SrCl2/NH3 ammine reference (COPh ~= 0.973); used to size the zeolite-13X district-heat store.

## How to reproduce
```bash
Load the config with the Clojure model (`clojure -M ...`) per code/UPSTREAM_README.md.
```

## Verification & validation (reliable sources)
Validated against Yan et al. (2020) published COPh / gamma_h.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
