# Digital Appendix — Aegis-DT v0.6 read-only digital twin

This compressed digital appendix supports the Aegis-40 FER digital-appendix requirement for code used in analyses/calculations. It provides the latest Aegis-DT v0.6 dashboard code, one representative sample input file, output files, model snapshots, figures, and explanatory notes.

## Scope and safety boundary

Aegis-DT v0.6 is a read-only advisory dashboard for design review, training, V&V presentation, and consistency checking. It is not credited for reactor protection, shutdown, decay heat removal, containment isolation, safety actuation, or Class 1E I&C functions.

The dashboard is deliberately separated into independent data layers:

1. **STAT_FINAL cycle records** — exact BOC/MOC/EOC OpenMC record values. Surrogate outputs are hidden in this view.
2. **GP/POD surrogate sensitivity** — fitted local sensitivity of `k_eff`, `F_assembly`, and 7x7 assembly power map to moderator temperature, fuel temperature, inserted rod count, and void fraction. This surrogate has no burnup input and is not used to create BOC/MOC/EOC records.
3. **Plant scenario display** — simplified user-interface demonstration for normal, TCES/H2, loss of normal heat sink, and SBO scenarios.
4. **V&V evidence** — benchmark and closure-summary material used to explain the dashboard confidence level.

## Sample input conditions

The representative sample input file is:

`inputs/aegis_dt_v06_sample_input.json`

It was created for:

- 125 MWth / 40 MWe Aegis-40 iPWR basis;
- 37-FA, 17x17, 2.0 m active-height core;
- STAT_FINAL cycle-state records for BOC, MOC hump, and EOC;
- local surrogate sensitivity cases around HFP/ARO conditions;
- plant-display scenarios separated from neutronic calculations.

## Approaches used

- **OpenMC record data:** BOC/MOC/EOC values are hard-separated as record data in the dashboard.
- **Gaussian-process surrogates:** `surrogate_k_eff.pkl` and `surrogate_F_assembly.pkl` are fitted to OpenMC sweep data and exported into JavaScript arrays inside the standalone HTML file.
- **POD/PCA power-map surrogate:** `surrogate_powermap.pkl` reconstructs a 7x7 assembly-level power-map trend from low-order modes. It does not predict pin-level `F_deltaH` or `Fq`.
- **Finite-difference coefficients:** MTC, DTC, void coefficient and rod worth shown in the surrogate tab are finite differences of the `k_eff` GP. The MTC derivative is flagged as less robust than direct STAT_FINAL coefficients.
- **Plant scenarios:** plant scenario values are UI demonstration values and are kept separate from OpenMC and the surrogate model.

## Outputs obtained

The sample run produces:

- `outputs/aegis_dt_v06_cycle_and_colr_output.csv` — STAT_FINAL cycle records and MOC COLR closure values.
- `outputs/aegis_dt_v06_surrogate_sample_output.csv` — GP/POD surrogate responses for the sample input cases.
- `outputs/aegis_dt_v06_plant_scenario_output.csv` — simplified plant-display scenario outputs.
- `outputs/validation_metrics.txt` and `figures/validation.png` — surrogate validation summary and parity/coefficients plot.

Key record results included in the dashboard:

- BOC: `k_eff = 1.1502`, `F_deltaH = 1.513`, `Fq = 1.937`.
- MOC hump: `k_eff = 1.1358`, `F_deltaH = 1.729`, `Fq = 2.435`.
- EOC: `k_eff = 0.9910`, `F_deltaH = 1.497`, `Fq = 2.121`.
- MOC envelope closure: `F_deltaH = 1.75`, `Fq = 2.468`, `MDNBR = 1.33` with W-3 and `2.13` with Bowring.

## How to reproduce the sample output

From the root of this appendix folder:

```bash
python code/run_sample_surrogate.py
```

The script reads `inputs/aegis_dt_v06_sample_input.json` and the three model files in `models/`, then writes `outputs/aegis_dt_v06_surrogate_sample_output.csv`.

The interactive dashboard is standalone:

```text
code/Aegis_DT_demo_v06.html
```

Open it locally in a web browser. It does not require an internet connection and does not load `.pkl` files at runtime because the exported surrogate coefficients are embedded directly in the HTML/JavaScript.

## Folder map

- `code/` — standalone dashboard and sample Python reproducer.
- `inputs/` — representative sample input JSON plus OpenMC sweep CSV used for surrogate evidence.
- `models/` — GP/POD model snapshots used by the reproducer and exported into the HTML.
- `outputs/` — sample outputs and validation metrics.
- `figures/` — validation and burnup figures used by the dashboard.
- `evidence/` — STAT_FINAL, V&V and COLR closure notes.

## FER wording

Suggested Appendix A row:

`Aegis_DT_v06_Digital_Appendix.zip — read-only digital twin dashboard; includes standalone HTML/JavaScript code, sample input JSON, GP/POD model snapshots, representative outputs, validation figure, STAT_FINAL cycle records and COLR closure evidence. Used for Section 8.7.6/8.7.8 advisory digital twin and V&V demonstration only; not credited for safety actuation.`
