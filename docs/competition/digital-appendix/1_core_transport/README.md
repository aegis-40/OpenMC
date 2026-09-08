# Digital Appendix - Full-core transport model + authoritative neutronics notebook

The locked Aegis-40 full-core OpenMC model and the parameterised notebook that builds every neutronics result in the FER (statics, coefficients, depletion, peaking, SDM).

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`inputs/geometry.xml, materials.xml, settings.xml` - a point-in-time export of the locked core. `code/aegis40_neutronics_FER.ipynb` is the fully parameterised source (outputs cleared).

## Approach
Explicit pin-by-pin 17x17 lattice, ring-zoned enrichment and Gd/Er loading, radial water reflector; eigenvalue transport with ENDF/B-VIII.0.

## Outputs obtained
Representative BOC (full core): k ~= 1.1503; MTC ~= -26.87 pcm/K; DTC ~= -1.91 pcm/K; void ~= -173 pcm/%; 16-CRA (90% enriched-B-10) worth ~= 21,509 pcm (hot ARI k=0.927; hot SDM 7.85%; cold shutdown via EBIS); F_dH ~= 1.513, Fq ~= 1.937.

## How to reproduce
```bash
`cd inputs && openmc`, or run the notebook cell-by-cell in the OpenMC WSL env.
```

## Verification & validation (reliable sources)
Validated by folders 0 (ICSBEP) and 2 (depletion). Internal consistency checks in the notebook.

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
