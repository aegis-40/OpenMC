# OpenMC core model & results (Aegis-40)

The OpenMC neutronics workstream for the Aegis-40 40 MWe SBF iPWR: the full-core
3D depletion notebook and the curated results it produces. The model runs in the
WSL/Linux OpenMC 0.15.3 environment (not from Windows).

## Contents
- `aegis40_3d_core_notebook.ipynb` — the working full-core model: geometry, 3-zone
  enrichment, Gd+Er burnable absorbers with radial zoning, feedback coefficients,
  rod worth / shutdown margin, depletion, and the two-stage parameter sweep.
- `results/`
  - `summary_report.txt` — the locked rev_3 safety-parameter summary (all gates PASS).
  - `sweep_ranked.txt`, `sweep_log.csv`, `sweep_results.yaml` — parameter-sweep output.
  - `plots/` — core map, geometry renders, BOC power distribution, depletion &
    burnable-absorber curves, FA pin map.
- `sample_inputs/` — a representative OpenMC input deck (`geometry.xml`,
  `materials.xml`, `settings.xml`) from the baseline depletion run, for the
  Digital-Appendix "sample input file per code" requirement.

## Notes
- Raw run artifacts (statepoint/summary/depletion `.h5`, ~113 MB) are **not** in
  git — they are regenerable and belong in the separately-uploaded Digital
  Appendix ZIP. Only lightweight, human-readable results are tracked here.
- The locked design basis (Table 1 / Table 2 / peaking before-after) is in
  `../docs/competition/design-basis-locked.md`.
- The back-end fuel-cycle / waste analysis that consumes this model's depletion
  output lives in `../src/aegis40/back_end/` with its driver scripts in
  `../scripts/`.
