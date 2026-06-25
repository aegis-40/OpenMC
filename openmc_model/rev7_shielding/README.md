# Aegis-40 — rev7 Shielding models (OpenMC)

Self-contained **fixed-source coupled neutron+photon** shielding models for the
FER §8.8 (radiation protection) and §8.10 (biological-shield footprint, ISFSI
layout). Built on the rev6 core conventions (`../rev6_standards/`), but with the
real radiation-transport pieces the core notebook never had: **RPV + downcomer +
biological shield** (Task A) and a **spent-fuel cask** (Task B).

Owner to run: **Laziz (LAY)**. Source terms come from **NEU (Samira)**.

---

## Why this supersedes the loose source files

The earlier `docs/competition/shielding/source_spectra.md` and
`gamma_spectrum.csv` are an **estimate tier** (principal gamma lines only,
Windows-generated). They are fine as a first cut, but version 7 puts
**everything in one place**: Task A drives the shield with the **real pin-lattice
fission source** (eigenvalue + coupled photon transport — OpenMC makes the
fission/capture gammas itself, no synthetic source), and Task B regenerates the
**full** decay-photon spectrum (every emitter, every line) directly from the
OpenMC depletion results via `material.get_decay_photon_energy()`. No
hand-curated spectrum is required (the CSV is only a fallback if the depletion
`.h5` is absent).

---

## Files

| File | What it does |
|---|---|
| `aegis40_3d_core_shielding_rev7.ipynb` | **Task A** — rev6 notebook (verbatim) **+ shielding section §9**: wraps the **real 17×17 pin lattice** in the lead-free biological shield, eigenvalue + photon transport, dose/flux/heating tallies + plot |
| `aegis40_cask_v7.py` | **Task B** — spent-fuel dry-cask shield (basket→steel→borated-poly→concrete overpack); decay-photon source from depletion results |
| `shielding_common.py` | Lead-free material library, ICRP-116 flux→dose, source rates, weight-window helper, stats profiles (used by the cask script) |
| `_build_rev7_notebook.py` | Regenerates the rev7 notebook from rev6 + the §9 cells (re-run if rev6 changes) |

## Run — Task A (notebook)

Open `aegis40_3d_core_shielding_rev7.ipynb` and run all cells. Sections 1–8 are
your rev6 model unchanged; **section 9** builds the shield, runs it, and draws the
dose-vs-radius plot. The shielding run reuses `build_core` — the **real pin
lattice is the source**. Statistics are LOW by default (`STAT_SHIELD`, 60×10k);
bump once it runs. Outputs land in `aegis40_rev6_outputs/shielding_rev7/`:
`doseA_vs_radius.png` + `.csv`, `doseA_spectra.csv`, and printed fast-flux /
heating / PASS-FAIL.

## Run — Task B (cask script)

```bash
export OPENMC_CROSS_SECTIONS=/mnt/d/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
python aegis40_cask_v7.py          # -> ./out_taskB/
```

Task B optionally reads the depletion results to build the source:
```bash
export AEGIS_DEPLETION_H5=/mnt/d/.../aegis40_rev6_outputs/depletion/depletion_results.h5
```
If unset/missing it falls back to `gamma_spectrum.csv` and still runs.

## Statistics (start low, as requested)

Default is `STAT_FAST` (20 batches × 20k particles) in `shielding_common.py` —
a smoke test that finishes in minutes. Once it runs clean, bump:
```python
STAT = STAT_MEDIUM   # working draft
STAT = STAT_FINAL    # appendix-grade report numbers
```
Deep-penetration dose needs the **weight windows** (MAGIC, on by default,
`USE_WW=True`). If your OpenMC build rejects the WW API, set `USE_WW=False` and
raise the stats.

---

## Materials — LEAD-FREE by design

Lead is toxic (handling/disposal); tungsten is too expensive for a stationary
wall. So the bulk gamma+neutron shield is **magnetite (heavy) concrete** —
cheap, lead-free, with bound water that also moderates fast neutrons — plus a
**borated-polyethylene** thermal-neutron capture layer. Architecture follows the
two optimization papers (Ogul et al. 2026 SMART multilayer; Bagheri & Khalafi
2023 GA shield), with their lead/tungsten outer high-Z swapped for heavy
concrete. The papers' design criterion — **total (n+γ) dose < 10 µSv/h behind
the last layer** — is the PASS/FAIL used in Task A.

| Material | ρ (g/cm³) | Role |
|---|---|---|
| SS304 | 8.00 | core barrel, thermal shield, cask basket |
| SA-508 carbon steel | 7.90 | RPV wall, cask gamma steel |
| water | 0.72 (hot) | downcomer |
| borated polyethylene (5 % B) | 0.95 | thermal-neutron capture |
| magnetite concrete | 3.90 | **bulk biological shield (lead-free)** |
| ordinary concrete | 2.30 | finish / cask overpack |

---

## Outputs we need (maps to the 6-tally handoff spec)

**Task A** (notebook §9 → `aegis40_rev6_outputs/shielding_rev7/`):
- `doseA_vs_radius.csv` / `.png` — **#1** dose µSv/h vs radius (n, γ, total) + 10 µSv/h target (plot also shown inline)
- printed in the cell — **#2** RPV fast flux (E>1 MeV) + 60-yr fluence, **#4** heating (W), PASS/FAIL
- `doseA_spectra.csv` — **#3** n & γ spectra at downcomer / cavity / outside

**Task B** (`out_taskB/`):
- `doseB_vs_radius.csv` / `.png` — dose vs radius through the cask
- `doseB_summary.txt` — **#5** surface / 1 m / 2 m dose vs IAEA SSR-6 / 10 CFR 71 (2 mSv/h surface, 0.1 mSv/h @ 2 m)

> **#2 caveat:** the RPV fast-fluence number is also produced by NEU's eigenvalue
> model (it is physically a criticality-source quantity). Use Task A's value as a
> fixed-source cross-check; quote NEU's eigenvalue number as primary in §8.3.

## Notes / refinements (if time allows)
- Penetration streaming (CRDM, instrument lines) is **not** in this radial model
  — flag as a known refinement (tally spec #6).
- Axial heads are simplified (water/steel plena, vacuum far away); the radial
  dose profile is sampled at mid-plane (z ∈ [−50, 50] cm).
- Feed the **outside dose (Task A)** into §8.8 zoning and the **shield outer
  radius (≈2.5 m)** into the §8.10 reactor-building footprint.
