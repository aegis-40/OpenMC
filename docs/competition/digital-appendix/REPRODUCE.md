# Aegis-40 Digital Appendix - reproducibility guide

This file is the single entry point for reproducing every result in the appendix. It lists the
environment, the one command per folder, the expected result, and an integrity check. Per-folder
`README.md` files carry the full conditions/approach/V&V detail.

## 1. Environment

```bash
conda create -n aegis python=3.11 && conda activate aegis
pip install -r requirements.txt
# nuclear data (install once; ~5 GB):
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=<physical-cores>
```
- Neutronics: **OpenMC 0.15.3 + ENDF/B-VIII.0**. TH CFD: **OpenFOAM v2412** (`8_thermal_hydraulics/`). TCES: **Clojure** (`9_tces_model/`).

## 2. One command per folder

| Folder | Command (from the folder) | Expected result | Runtime |
|---|---|---|---|
| 0_icsbep_criticality | `cd inputs/case-1 && openmc` (x4 cases) | k vs measured, mean bias ~-50 pcm | min |
| 1_core_transport | `cd inputs && openmc` (or run the notebook) | BOC k~1.150, coefficients | ~10 min |
| 2_depletion_benchmark | `python code/benchmark_depletion_pincell.py [--repeat SEED]` | k ~20 pcm vs Romano (2021) | ~20 min |
| 3_storage_criticality | `PYTHONPATH=src python3 code/run_storage_criticality.py` | k(95/95) <= 0.95 | ~5 min |
| 4_safety_neutronics | `bash code/run_resumable.sh` | rod worth 21,509 pcm (16 CRA, N5C); EBIS/SFP/MSLB margins | hours |
| 5_digital_twin | `bash src/run_twin_sweep.sh` then `python src/fit_surrogates.py` | GP/POD surrogate + validation | ~1 h (sweep) |
| 6_waste_results | `PYTHONPATH=src python3 code/run_decay_heat.py` (etc.) | 7.95 MW shutdown; 4.40 tHM/TWhe | min |
| 7_energy_cycle | `python code/thermo_cycle.py` ; `python code/economics_lcoe.py` | 40 MWe/32%; LCOE $74.8/MWh | min |
| 8_thermal_hydraulics | `cd 01_OpenFOAM_CFD/sample_case && ./Allmesh && ./Allrun` ; `python 02_.../cycle_mdnbr.py` | MDNBR 1.33 (W-3) / 2.13 (Bowring) | ~1 h CFD |
| 9_tces_model | `clojure -M ...` (see UPSTREAM_README) | COPh ~0.973 vs Yan (2020) | min |
| 10_shielding | `python code/shield_37fa_cad.py` ; `python code/point_kernel_dose.py` | RPV fluence 3.0e18; dose 0.23 µSv/h | ~min-hours |

## 3. Integrity check

Every shipped file is listed with its SHA-256 in `CHECKSUMS.sha256`. Verify with:
```bash
sha256sum -c CHECKSUMS.sha256
```

## 4. Notes on reproducibility / repeatability / benchmarking (the appendix gate)

- **Reproducibility** - fixed library (ENDF/B-VIII.0) and chain versions; built-in benchmark
  models (BEAVRS pincell, ICSBEP decks) need no external geometry.
- **Repeatability** - `--repeat <seed>` reruns agree within combined Monte-Carlo sigma.
- **Benchmarking** - measured OECD/NEA ICSBEP criticals (folder 0); code-to-code depletion vs
  Serpent (Romano 2021, folder 2); ASME V&V-20 grid convergence (folder 8); Yan (2020) TCES
  (folder 9). Reliable-source data (IAEA / OECD-NEA / US-NRC / ASME / IAPWS) throughout.
- Raw multi-MB statepoint/depletion `.h5` are regenerable from these inputs and are not shipped
  in the archive (the STAT_FINAL depletion `.h5` is on the team drive).
