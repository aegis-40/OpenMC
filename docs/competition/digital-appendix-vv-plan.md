# Digital Appendix — Verification & Validation plan (FER §8.11 / spec §4.3.2)

**Hard gate (spec p.43):** the Digital Appendix must provide, *per code*, one
sample input file + an explanation of the case/approach/outputs + **repeatability,
benchmarking, and reproducibility** results. This document is the plan and the
index; each leg points at the script that produces it and the published reference
it is judged against.

Owner: **Samira [NEU]**. Status as of 2026-06-05.

---

## Why this gate matters for the safety case

Every §8.11 number — storage-rack `k(95/95)`, the discharge source term, the
7.75 MW shutdown decay heat, the radiotoxicity curve — is produced by the **OpenMC
depletion + transport** path. The V&V is the evidence that path is used correctly.
Concretely it supplies the **code/data bias term `Δ_bias`** that currently sits at
0 in `scripts/run_storage_criticality.py`; a defensible storage-criticality
licensing argument needs that bias to come from benchmarking, not assumption.

The three competition keywords map to three things we must show:

| Term | Question it answers | How we show it |
|---|---|---|
| **Reproducibility** | Can someone else rebuild our result from the inputs? | Public, built-in benchmark models + tracked sample input decks + fixed library/chain versions |
| **Repeatability** | Does *our* result hold across reruns? | Re-run with different RNG seeds; agreement within Monte-Carlo σ |
| **Benchmarking** | Does the code reproduce a *known answer*? | Code-to-code (Serpent) + measured-assay (SFCOMPO) + criticality-array references |

---

## Leg 1 — Depletion / spent-fuel isotopics  ⟶ DONE (code-to-code), measured pending

**Script:** `scripts/benchmark_depletion_pincell.py` (run in WSL).
**Model:** `openmc.examples.pwr_pin_cell()` — the **BEAVRS 2.4 wt% PWR pincell**
(UO₂ 10.29769 g/cm³, Zircaloy clad r=0.45720 cm, pitch 1.26 cm, borated water +
S(α,β)), built into OpenMC ⇒ zero external data, maximally reproducible.
**Reference:** Romano, Josey, Johnson, Liang, *Ann. Nucl. Energy* 152 (2021)
107989, §3.2. OpenMC vs Serpent on this exact case: **k_eff within ~20 pcm,
actinides <1 %, fission products <1 %**, depleted to 50 MWd/kg with the
0.1/0.4/0.5 → 1.0(→10) → 2.5(→50) MWd/kg schedule, CE (predictor) integration.
**What we report:** k_eff(BU) curve + principal actinide/FP build-up (the
burnup-credit set: U/Pu/Am/Cm + Cs-137/Sr-90/Sm-149…) vs burnup, against the
paper's agreement bands. Outputs → `docs/competition/digital-appendix/`.

- **Reproducibility:** built-in model + ENDF/B-VIII.0 + `chain_endfb80_pwr.xml`.
- **Repeatability:** `--repeat <seed>` rerun; k_eff per step within combined σ.
- **Open (stronger, measured):** benchmark the *same* isotopics against a
  **SFCOMPO 2.0** destructive-assay PWR sample and/or the tabulated nuclide
  concentrations of the **OECD/NEA Burnup-Credit Criticality Benchmark Phase I-B**
  (absolute reference numbers, not code-to-code). Needs the source documents.

## Leg 2 — Storage-rack criticality  ⟶ cross-checked, formal benchmark pending

**Script:** `scripts/run_storage_criticality.py` (already validated on OpenMC
0.15.3). **Current cross-checks:** method follows Cabrera (2023) PWR spent-fuel-
pool burnup-credit recipe; result (credited burnup-credit + Boral `k(95/95)=0.782`)
sits below the Kim, Jung & Yoon (2024) SBF small-PWR storage band 0.932–0.949 —
consistent and conservative.
**Open (formal):** OpenMC k_eff against the **OECD/NEA Burnup-Credit Benchmark
Phase II** (spent-fuel array) or an **ANS-8.1** critical-array benchmark, to put a
quantitative bias/uncertainty on the criticality side. Feeds `--bias`/`--unc`.

## Leg 3 — Transport k_eff (core)  ⟶ available, low effort

The full-core OpenMC model can additionally be sanity-checked against a published
PWR lattice/whole-core benchmark (BEAVRS HZP, or the NuScale-like SMR benchmark in
`D:\projects\literature`). Lower priority for §8.11 (waste) but strengthens §8.2.

---

## Acceptance criteria (what "pass" means)

| Leg | Metric | Acceptance |
|---|---|---|
| 1 (code-to-code) | k_eff(BU) vs Romano-2021 OpenMC/Serpent | within ~20–30 pcm; actinides <1 %, FPs <1 % |
| 1 (measured) | key isotopics vs SFCOMPO assay | within stated experimental + method uncertainty |
| 2 (formal) | k_eff vs OECD Phase II / ANS-8 | C/E within benchmark σ; defines Δ_bias, Δ_unc |
| repeatability | k_eff across seeds | agree within combined Monte-Carlo σ |

`k(95/95) = k_calc + 2σ + Δ_bias + Δ_unc`. Legs 1–2 are what turn the present
`Δ_bias = Δ_unc = 0` placeholders into defensible, benchmarked values; the
storage margin (~0.16) is wide enough that a few-hundred-pcm bias still passes.

---

## Sample-input deck index (one per code, per the gate)

| Code / capability | Sample input | Case |
|---|---|---|
| OpenMC transport | `openmc_model/sample_inputs/{geometry,materials,settings}.xml` | Aegis-40 core deck snapshot |
| OpenMC depletion | `scripts/benchmark_depletion_pincell.py` | BEAVRS 2.4% pincell to 50 MWd/kg |
| OpenMC criticality (storage) | `scripts/run_storage_criticality.py` | burnup-credit storage rack k(95/95) |
| Back-end physics (Python) | `src/aegis40/back_end/` (15/15 tests) | source term, decay, classification, arisings |

---

## Status summary

- ✅ Leg 1 code-to-code benchmark **scripted** (`benchmark_depletion_pincell.py`) —
  awaiting the WSL run to populate `docs/competition/digital-appendix/`.
- ⬜ Leg 1 measured (SFCOMPO / OECD Phase I-B) — needs source data.
- 🟡 Leg 2 cross-checked (Cabrera method, Kim band); formal OECD Phase II pending.
- ⬜ Leg 3 core transport benchmark — optional, §8.2.

See `reference-reactors-comparison.md` (method precedents) and
`waste/storage-criticality-interpretation.md` (the safety case the bias feeds).
