# Manifest

| Path | Purpose |
|---|---|
| README.md | Main explanation of sample input conditions, methods, and outputs. |
| code/Aegis_DT_demo_v06.html | Latest standalone Aegis-DT v0.6 dashboard. |
| code/run_sample_surrogate.py | Reproducer for surrogate sample output from JSON input and PKL model files. |
| code/export_model_js.py | Original utility used to export fitted Python surrogate objects into JavaScript arrays. |
| inputs/aegis_dt_v06_sample_input.json | Required representative sample input file for the digital twin code. |
| inputs/core_sweep.csv | OpenMC sweep data used as surrogate/validation evidence. |
| models/surrogate_k_eff.pkl | Gaussian-process k_eff surrogate snapshot. |
| models/surrogate_F_assembly.pkl | Gaussian-process assembly peaking surrogate snapshot. |
| models/surrogate_powermap.pkl | POD/PCA assembly power-map surrogate snapshot. |
| outputs/aegis_dt_v06_cycle_and_colr_output.csv | STAT_FINAL BOC/MOC/EOC and MOC-COLR closure output. |
| outputs/aegis_dt_v06_surrogate_sample_output.csv | GP/POD sample-output file generated from the sample input JSON. |
| outputs/aegis_dt_v06_plant_scenario_output.csv | Simplified plant-display output for UI scenario modes. |
| outputs/validation_metrics.txt | Surrogate validation metrics. |
| figures/validation.png | Validation figure shown in the dashboard. |
| figures/fig_8.2-5c_burnup_by_assembly_EOC.png | EOC assembly burnup figure shown in the dashboard. |
| evidence/neutronics-STATFINAL-results.md | OpenMC STAT_FINAL record evidence. |
| evidence/benchmarks-VV-summary.md | Benchmark/V&V evidence. |
| evidence/cycle-peaking-COLR-paste.md | MOC COLR closure evidence. |
