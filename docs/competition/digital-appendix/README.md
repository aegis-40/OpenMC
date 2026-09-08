# Aegis-40 — Digital Appendix (Neutronics & Fuel-Cycle V&V)

Reproducibility package for the Aegis-40 detailed-design FER. It satisfies the
competition Digital-Appendix gate (spec §4.3.2): **for each code, one representative
sample input + an explanation of the case, its approach and outputs + repeatability,
benchmarking and reproducibility evidence.**

All files in this appendix reflect the **final locked design** below. Monte-Carlo
neutronics is **OpenMC 0.15.3** with **ENDF/B-VIII.0** cross sections and the
`chain_endfb80_pwr.xml` depletion chain, run in the WSL/Linux environment.

---

## 1. Final design basis

| Parameter | Value |
|---|---|
| Reactor type | Integral PWR (iPWR), **soluble-boron-free (SBF)**, natural circulation |
| Thermal / electric power | **125 MWth / 40 MWe** (~32 %) |
| Core | **37 fuel assemblies**, 17×17 pin lattice, 2.0 m active height |
| Heavy-metal loading | ~9.39 tHM (~13.3 MW/tHM specific power) |
| Enrichment | in-out zoned 4.0–4.95 wt% ²³⁵U (core-average ~4.43 wt%, peak 4.95 wt%) |
| Burnable absorber | integral **20 Gd rods/FA @ 6 wt% Gd₂O₃** + **16 Er rods/FA @ 0.75 wt% Er₂O₃** |
| Control | **16 control-rod assemblies (CRAs)**, 90 %-enriched-B-10 B₄C (NuScale NPM configuration) |
| Fuel cycle | **once-through** (no refuelling), ~29.6 GWd/tHM discharge, ~2224 EFPD (~6 FPY) |

**Representative BOC results** (full core, ENDF/B-VIII.0): k_BOL ≈ 1.1503; MTC ≈ −26.87
pcm/K; DTC ≈ −1.91 pcm/K; void ≈ −173 pcm/%void; 16-CRA bank worth ≈ 21 509 pcm →
hot all-rods-in k ≈ 0.927 (hot SDM 7.85 %); F_ΔH ≈ 1.513, F_q ≈ 1.937 (within the design-specific COLR envelope); cold shutdown is credited to the diverse EBIS (SSR-2/1 Req. 46). Detailed
safety-neutronics margins are in `4_safety_neutronics/`.

---

## 2. Contents — what each item proves

| # | Folder | Code / case | What it proves |
|---|---|---|---|
| 0 | `0_icsbep_criticality/` | OpenMC criticality — **OECD/NEA ICSBEP LEU-COMP-THERM-008, 4 measured critical experiments** | **Experimental validation with OECD/NEA data** (explicit spec requirement): all 4 LEU-lattice criticals reproduced within the handbook uncertainty (mean bias ≈ −50 pcm, ENDF/B-VIII.0). |
| 1 | `1_core_transport/` | OpenMC transport — Aegis-40 core deck (`geometry/materials/settings.xml`) | The full-core input structure (37-FA geometry, zoned enrichment, Gd+Er absorbers, reflector) is a valid, self-contained OpenMC deck. |
| 2 | `2_depletion_benchmark/` | OpenMC depletion — BEAVRS 2.4 % PWR pincell | **Reproduction + repeatability**: reproduces the published Romano (2021) OpenMC-vs-Serpent validation case configuration (identical built-in model/schedule/chain) and demonstrates seed-to-seed repeatability; the quantitative depletion validation itself is the published Romano result (k ~20 pcm, nuclides <1 %), cited. |
| 3 | `3_storage_criticality/` | OpenMC criticality — spent-fuel storage rack | Discharged fuel stays sub-critical `k(95/95) ≤ 0.95` in unborated water (SBF-consistent). |
| 4 | `4_safety_neutronics/` | OpenMC criticality — §8.5–8.6 safety suite (rod worth/SDM, EBIS, SFP, MSLB) | Every credited shutdown function clears its adjusted-k target with margin. |
| 5 | `5_digital_twin/` | OpenMC eigenvalue sweep + ML surrogates | Physics-trained fast surrogate core twin (k, coefficients, power map) — the §8.7.6 originality item. |
| 6 | `6_waste_results/` | Back-end fuel-cycle physics (`src/aegis40/back_end/`) | The §8.11 waste numbers: discharge inventory, rigorous decay heat, source term, waste intensity, storage criticality. |
| 7 | `7_energy_cycle/` | Rankine + SOE-H₂ + TCES-DH balance (Python, IAPWS-IF97) | §8.9 energy-cycle state points, hydrogen schedule (427 t/yr), district-heat balance. |
| 8 | `8_thermal_hydraulics/` | OpenFOAM v2412 conjugate-heat-transfer CFD (`01_OpenFOAM_CFD/sample_case`, runnable) + full Python safety toolchain (`02_`) + acceptance criteria (`03_`) + V&V (`04_`) | §8.4/§8.5: MDNBR (W-3 + Bowring + Groeneveld-2006 LUT), PCT, natural circulation, AOO/cycle DNBR; ASME V&V-20 grid convergence + NuScale validation; reliable-source V&V in `04_VV_and_benchmarking/`. |
| 9 | `9_tces_model/` | TCES thermodynamic model (`tces`, Clojure) | **Validated** NiCl₂–SrCl₂/NH₃ store: reproduces Yan et al. (2020) COPh/γ_h; §8.9 sizing. |
| 10 | `10_shielding/` | OpenMC fixed-source biological-shield + RPV fluence (37-FA, final CAD radial build) | RPV E>1 MeV 60-yr fluence **3.0×10¹⁸ n/cm² < 1×10¹⁹ (PASS)**; bioshield dose ≪ 10 µSv/h (deep-attenuation, leakage 1.4×10⁻⁴). Materials lead-free (Ogul 2026; Bagheri & Khalafi 2023). |
| 11 | `11_cad_drawings/` | Technical drawings (2-D PDF): integral reactor-module assembly + 17×17 fuel-assembly, exported from the parametric CAD model | The mechanical/geometry deliverable behind §8.1.9 / Table 8.1-9 (report Figures 8.1-2, 8.2-2a); native 3-D STEP/SolidWorks on the shared drive. |
| — | `figures/` | Representative model renders & result plots | Core map, pin map, XY/XZ geometry renders, BOC power distribution, k(BU) depletion, absorber burn-down. |

**Uniform layout.** Every discipline folder now follows the same input/output structure
introduced in the digital-twin package: `code/` (scripts / cleaned notebook), `inputs/`
(the representative sample input), `outputs/` (sample results), `evidence/` (V&V material)
and `figures/`, each with a `README.md` stating the case conditions, approach, outputs and
reliable-source V&V. Folders `5_digital_twin/` and `8_thermal_hydraulics/` are self-contained
teammate packages that already embody this input/output separation under their own layout.

---

## 3. How to run each sample case

All OpenMC cases run in WSL/Linux with the library configured:
```bash
conda activate <openmc-env>
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=<physical-cores>
```

- **1 — core transport:** `openmc` in `1_core_transport/` runs the deck (eigenvalue). It is
  a point-in-time export of the locked core; the authoritative, fully-parameterised source is
  the `aegis40_neutronics_FER.ipynb` notebook.
- **2 — depletion benchmark:** `python benchmark_depletion_pincell.py` (add `--repeat <seed>`
  for the repeatability leg). Needs no external geometry — the BEAVRS pincell is built into
  OpenMC, so it is maximally reproducible. Acceptance: k_eff within ~20–30 pcm, actinides/FPs
  within ~1 % of Romano (2021) §3.2.
- **3 — storage criticality:** `PYTHONPATH=src python3 run_storage_criticality.py [--results
  depletion_results.h5]`. Fresh-fuel bounding cases run with no results file; pass `--results`
  for the burnup-credit case.
- **4 — safety neutronics:** see `4_safety_neutronics/README.md` — `bash run_resumable.sh`
  (self-resuming). Judged by `k_adj = k_mean + 2σ + 0.005`.
- **5 — digital twin:** see `5_digital_twin/README.md` — `bash run_twin_sweep.sh` generates
  `core_sweep.csv` (a representative 51-point live sample is included as
  `core_sweep_sample.csv`); then `python fit_surrogates.py` fits the surrogates + validation.

---

## 4. V&V mapping (the three gate keywords)

| Keyword | How it is shown here |
|---|---|
| **Reproducibility** | Built-in benchmark model (no external data) + tracked sample decks + fixed library (ENDF/B-VIII.0) and chain versions. |
| **Repeatability** | `--repeat <seed>` reruns; k_eff agrees within combined Monte-Carlo σ. Eigenvalue σ is reported per case (statistical, not weight-windowed — WW is fixed-source-only). |
| **Benchmarking** | Depletion code-to-code vs Serpent (Romano 2021); storage vs Kim/Jung/Yoon (2024) SBF small-PWR band; safety-margin convention with an explicit +500 pcm bias allowance. |

Full V&V plan and acceptance criteria: `../digital-appendix-vv-plan.md`.

---

## 5. Notes

- **Raw run artifacts** (statepoint / summary / depletion `.h5`, ~100 MB+) are **not**
  included — they are regenerable from the inputs above. Only lightweight, human-readable
  inputs, results and figures are kept.
- Numbers here are ENDF/B-VIII.0 STAT_FINAL / STAT_MEDIUM values for the final design
  (Gd 6 wt%, Er 0.75 wt%, 16 CRA, once-through). Earlier design iterations (higher Gd,
  12 CRA, multi-batch) have been removed from this appendix.
