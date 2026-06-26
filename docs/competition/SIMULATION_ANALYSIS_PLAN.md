# Aegis-40 — Safety Simulation & Analysis Plan

*Owner: Azamhon (3S). Created 2026-06-26. Re-baselined to the rev_4 37-FA core (`docs/aegis40_neutronics_FER.ipynb`).*
*Purpose: enumerate every simulation and every analysis the safety case (FER §8.5–8.7) needs, sorted by the tool that produces it, with a clear count of deliverable files and an explicit "what's missing" list.*

---

## 0. How to read this plan

Two distinct kinds of work, often confused — keep them separate:

- **SIMULATION** = a code *run* that produces raw physics numbers (OpenMC k-eigenvalue, OpenFOAM CFD field…). Input deck → output data.
- **ANALYSIS** = turning numbers into a *safety conclusion* (compare to a limit, build an event tree, propagate uncertainty, allocate a budget). An analysis may consume simulation output **or** may be pure reasoning with no simulation behind it.

Each item below is tagged **[SIM]** or **[ANALYSIS]**, and each analysis says whether it is *of simulation results* or *standalone*.

**Status of the current run:** the 37-FA neutronics model exists; the **medium-statistics** run (`STAT_MEDIUM` = 180 batches / 20 k particles) is done; the **high-statistics** run (`STAT_FINAL` = 400 batches / 50 k particles) is running on a separate machine. Reported FER numbers use `STAT_FINAL`.

---

## 1. SIMULATIONS — by tool

### 1.A · OpenMC (neutronics / Monte-Carlo transport + depletion)

All of these live in **one notebook** — Samira's `docs/aegis40_neutronics_FER.ipynb` is already the single OpenMC file (see §3). They are *sections* of that notebook, not separate files.

| # | Simulation | Produces | Feeds safety criterion | Status |
|---|---|---|---|---|
| N1 | BOC k-eigenvalue (3-D, ARO) | k_eff BOL, excess reactivity | `k_eff_operating` | medium ✓ / high running |
| N2 | Moderator temperature coefficient (ΔT perturbation) | MTC [pcm/K] | `mtc_full_power` (hard <0) | medium ✓ / high running |
| N3 | Doppler coefficient (fuel-T perturbation) | DTC [pcm/K] | `dtc_doppler` (hard <0) | medium ✓ / high running |
| N4 | Void coefficient (moderator void perturbation) | void coeff [pcm/%void] | `void_coefficient` (hard <0) | medium ✓ / high running |
| N5 | Control-rod worth (ARO vs ARI) + **shutdown margin** (most-reactive rod stuck out) | ARO worth, cold SDM | `control_rod_worth_aro`, `shutdown_margin` (hard ≥1%) | medium ✓ / high running |
| N6 | **Power peaking** — pin-by-pin F_ΔH (radial) + F_z (axial) + separable F_Q | F_ΔH, F_Q | `f_delta_h_radial`, `f_q_total` (hard LCO) | **governing** — high-stat needed |
| N7 | Depletion BOC→EOC (3-D, design specific power) + 4-batch equilibrium (linear-reactivity model) | cycle length [EFPD], discharge burnup, k(BU) curve | `cycle_length`, `fuel_burnup_max` | medium ✓ / high running |
| N8 | Gd/Er burnable-absorber inventory evolution | absorber burnout curve | supports `k_eff` hold-down story | medium ✓ |
| N9 | Flux maps (thermal/fast/total, midplane) | flux distributions (FER figure) | shielding / activation inputs | medium ✓ |
| N10 | **EBIS borated-core case** — boron mass/concentration for standalone cold-subcritical at most-reactive state | required boron mass | `independent_shutdown_systems` §6.10 | **MISSING — not yet in notebook** |
| N11 | **SFP storage-rack criticality** — k_eff(95/95) in unborated water, max-reactivity assembly | SFP rack k_eff | fuel-handling criticality (§8.8.6) | **MISSING — separate model** |
| N12 | **MSLB cooldown reactivity** — k vs moderator-T down to cold, most-reactive rod stuck | return-to-power margin vs SDM | MSLB acceptance (§8.6.5b) | **MISSING — needs cold/cooldown branch** |

### 1.B · OpenFOAM (thermal-hydraulics / CFD)

**UPDATE 2026-06-26 — OpenFOAM work EXISTS** (`docs/Aegis40_TH_report.docx`): a 3-region conjugate-CFD model (**chtMultiRegionFoam**, OpenFOAM v2412, k-ω SST) of the fuel/clad/coolant pin, coupled to a **correlation stack** (W-3 CHF + Tong F-factor for MDNBR; Dittus-Boelter + 1-D conduction + Jens-Lottes subcooled-boiling clamp for PCT). Built on the **37-FA / 9 768-pin rev_4 core**, V&V'd against NuScale NPM-160, energy-conservative (GATE-1 ×1.00) and mesh-independent (ASME V&V-20 GCI < 0.15 %). So this is **no longer the big gap** — the steady-state and natural-circulation cases are done; the **transient/accident** cases remain.

| # | Simulation | Produces | Feeds safety criterion | Status |
|---|---|---|---|---|
| F1 | Steady-state hot-channel (nominal flow + power, peaking from N6) | MDNBR (steady), coolant/clad/fuel T | `mdnbr_steady` (hard ≥1.3), `fuel_centerline_temperature` | **DONE** — MDNBR **1.56** (>1.3, +20 %); PCT **349 °C**; fuel centreline **734 °C**. See ⚠ coupling below |
| F2 | AOO transient hot-channel (loss of flow, overpower) | MDNBR (transient) | `mdnbr_transient` (hard ≥1.3) | **MISSING** — TH report is steady-state only |
| F3 | SBLOCA blowdown/reflood | peak clad temperature, oxidation | `pct_loca` (≤1204 °C), `cladding_oxidation`, `hydrogen_generation` | **MISSING** — no LOCA transient run (the 349 °C is steady operating PCT, not LOCA) |
| F4 | Natural-circulation primary-loop verification | flow rate, ΔT, circulation adequacy | `primary_circulation`, decay-heat removal | **DONE** — 1-D buoyancy balance; H_tc 4 m → G 542, MDNBR 1.56; H_tc sweep shows 3 m FAILS, ≥4 m PASS; vessel ~10 m / Ø3.0–3.5 m |
| F5 | PRHR / IRWST decay-heat removal transient | heat-removal ratio, IRWST boil-off, **grace period** | `prhr_capacity` (≥1.05), `operator_grace_period` (≥72 h) | **MISSING** — F4 is normal-op steady flow, NOT the post-scram decay-heat transient |
| F6 | Containment pressure/temperature response (limiting DBA mass-energy) | peak containment P/T | `containment_pressure` (≤0.414 MPa) | **MISSING — also gated on C5** |

> **⚠ Key coupling (F1 ↔ N6).** The TH report's MDNBR 1.56 was computed with the **de-peaked design-target peaking** (F_Q 2.00, F_ΔH 1.55) — *not* a fresh per-pin reconstruction (the notebook compute cells weren't executed). So **F1's PASS is contingent on the high-stat OpenMC (N6) confirming F_Q ≈ 2.0 / F_ΔH ≈ 1.55.** If N6 comes back higher, MDNBR must be recomputed. The two runs must be reconciled before either result is final.
>
> **TH report caveats to close for the final safety case:** (i) W-3 CHF is extrapolated below its mass-flux range (G 543 ≪ 1356) — conservative, but a **low-flow CHF correlation** is recommended; (ii) the hot-channel single-phase outlet slightly exceeds T_sat (~4 K) → a two-phase enthalpy model would cap it.

### 1.C · Other tools

| # | Simulation | Tool | Produces | Feeds | Status |
|---|---|---|---|---|---|
| O1 | Atmospheric dispersion (source term → site boundary) | RASCAL / HotSpot / MACCS-class | boundary dose 0–2 h, EPZ basis | `dose_site_boundary` (≤0.25 Sv), `epz_radius` | **CITE/BOUND** (see §1.C.1) |
| O2 | Fuel-performance / rod mechanics | FRAPCON-class | rod internal P, clad strain, fuel-clad gap, fission-gas | `fuel_core_structural` (Req 43–44) | **CITE/BOUND** (see §1.C.1) |
| O3 | Decay-heat source term | ORIGEN / depletion post-process | decay-heat curve, isotopic source term (Bq) | PRHR sizing (F5), dispersion (O1) | **CITE** — ANS/ANSI-5.1 is the standard, no run needed |
| O4 | Level-1 PRA (event-tree quantification) | SAPHIRE-class / by-hand | CDF, LRF | `cdf`, `lrf` | **CITE/BOUND** — hand trees + NuScale-class PRA reference |
| O5 | Seismic / structural (combined seismic+LOCA core loads) | FEA | core hold-down, rod insertability | `fuel_core_structural`, `sse_design` | **CITE/BOUND** — standards + mechanical scope |

### 1.C.1 · Strategy — cite/bound against IAEA/NRC standards instead of running unfamiliar tools

For a **detailed-design competition entry** (not a license application), the §1.C items do not need de-novo simulation in tools the team doesn't operate. Each can be supported by **(a) a recognized standard/correlation, and/or (b) a bounding or by-similarity argument against the NRC-reviewed reference plant** — Aegis-40's core is geometrically the **NuScale NPM** (37 FA / 9 768 pins / 2.0 m, per the TH report), so "by similarity to NuScale" is a strong, legitimate basis. This is the standard "demonstration by reference to the licensed envelope" approach. **Each such claim must be labelled as bounding/by-reference, not as a plant-specific calculation.**

| Item | How to substantiate without running the tool | Citations |
|---|---|---|
| **O1 dispersion / EPZ** | Bound the source term by core power (125 MWth, ~⅓ of NuScale NPM) and credit the passive containment; argue boundary dose < PAG with the **plant-boundary EPZ** by reference to NuScale's NRC-approved site-boundary EPZ methodology and scaling. A full MACCS run is *not* required for the FER. | RG 1.183 (alternative source term); 10 CFR 50.33(g) + SMR EPZ final rule; NEI 12-02; NuScale FSAR Ch. 15 / SECY-15-0077; IAEA NS-G-2.x |
| **O2 fuel performance** | Bound by the **NRC-licensed fuel envelope**: standard 17×17 UO₂/Zircaloy-4 at ≤62 GWd/MTU is already within the approved design basis, and Aegis-40 runs at **low linear power (12.8 kW/m peak ≪ ~43 kW/m PWR limit)** — so rod-internal-pressure, clad-strain and fission-gas margins are large *by inspection*. No FRAPCON run needed; state it as bounded-by-envelope. | NRC SRP 4.2 (NUREG-0800); 10 CFR 50.46; ANS fuel criteria; IAEA NF-T-2.1 |
| **O3 decay heat** | **ANS/ANSI-5.1 is the standard decay-heat curve** — citing it *is* the deliverable; no simulation. Already cross-checked against the depletion. | ANSI/ANS-5.1-2014 |
| **O4 PRA (CDF/LRF)** | The hand-built LOHS/SBO event trees give per-initiator CDF; **bound the plant CDF/LRF by the NuScale-class passive-PRA result** (passive iPWRs report CDF ~1e-8–1e-10) by similarity. A full SAPHIRE model is beyond FER scope; cite the reference and the de-energize-to-actuate argument. | NuScale FSAR Ch. 19 (PRA); IAEA SSG-3 / SSG-4; NRC RG 1.174 |
| **O5 seismic/structural** | Cite the **design spectrum + qualification standards** (SSE 0.3 g to RG 1.60; 1E equipment to IEEE 344); the combined seismic+LOCA core-structural FEA is the **mechanical/civil teammate's** scope, referenced not run here. | RG 1.60, RG 1.61; IEEE 344; IAEA SSG-9, NS-G-1.6 |

> **Honesty rule:** these are **bounding / by-reference** justifications appropriate to a design-stage report, not plant-specific safety demonstrations. The FER must say so explicitly (e.g. "bounded by the NRC-licensed fuel envelope" / "by similarity to the NuScale NPM"). Where a number is genuinely needed and cheap (e.g. a scaling dose estimate), do the hand-calc; where the tool is unfamiliar and the standard suffices, cite.

---

## 2. ANALYSES — of simulation results vs standalone

### 2.A · Analyses OF simulation results (consume the runs above)

| # | Analysis | Consumes | Produces (safety conclusion) |
|---|---|---|---|
| A1 | Reactivity-balance + feedback-coefficient compliance | N1–N5 | MTC/DTC/void <0 PASS; reactivity balance closes |
| A2 | Peaking vs LCO compliance + engineering uncertainty factors | N6 | F_ΔH ≤1.65, F_Q ≤2.50 PASS/FAIL → gates MDNBR/PCT |
| A3 | DNBR margin assessment | F1 ✓ (steady), F2 (transient pending), N6 | **steady MDNBR 1.56 DONE** (+20 %); transient (F2) + N6-confirmation pending |
| A4 | LOCA acceptance (10 CFR 50.46) | F3 | PCT ≤1204 °C, oxidation ≤17 %, H₂ ≤1 % — pending F3 |
| A5 | Decay-heat-removal & grace-period demonstration | F4 ✓ (normal-op nat-circ), F5 (decay transient pending), O3 | normal-op natural circulation DONE; ≥72 h grace + PRHR ≥105 % pending F5 |
| A6 | Shutdown-margin & two-shutdown-system adequacy | N5, N10 | SDM ≥1 %; EBIS alone subcritical (§6.10) |
| A7 | Containment integrity | F6 | peak P ≤0.414 MPa |
| A8 | Radiological consequence + EPZ justification | O1, O3 | boundary dose ≤0.25 Sv; EPZ ≤0.5 km |
| A9 | Burnup / cycle-length / fuel-utilization | N7 | cycle ≥365 EFPD; burnup ≤62 GWd/MTU |
| A10 | PRA quantification (CDF/LRF roll-up) | O4 + event trees | CDF <1e-7, LRF <1e-8 |

### 2.B · Standalone analyses (NO simulation behind them — reasoning / design audit)

These are **done or doable now** without waiting on any run — and several are already in the FER draft.

| # | Analysis | Basis | Status |
|---|---|---|---|
| B1 | Practical-elimination argument (LBLOCA, rod-ejection, boron-dilution, surge-line) | deterministic geometry (integral RPV, internal CRDM, SBF) | DONE (FER §8.6.1) |
| B2 | Plant-states / DEC classification | SSR-2/1 Req 13/20 | DONE (FER §8.5.1a) |
| B3 | Event-tree logic & success-path mapping (LOHS, SBO, + 6 simplified) | top-event → trip/ESF | DONE (FER §8.6.3/8.6.5) |
| B4 | Defense-in-depth mapping (5 levels) | SSR-2/1 §2.13 | DONE (FER §8.5.3) |
| B5 | Trip-setpoint table + response-time budget (≤500 ms) | I&C design | DONE (FER §8.7.2a) |
| B6 | Internal/external hazards register | SSR-2/1 Req 17 | DONE (`hazards_register.md`) |
| B7 | Heat-sink architecture (normal seawater vs passive safety UHS) | Req 52/53 | DONE (FER §8.5.2a) |
| B8 | Coastal external-hazard screening (surge/tsunami/intake-blockage) | SSR-1/SSG-9 | framework done; **DBFL number = O1-adjacent site study MISSING** |
| B9 | Tritium permeation/carryover budget (SOE Req 35) | mass-transport hand-calc | **MISSING — analysis, no sim needed** |
| B10 | Setpoint-uncertainty roll-up (ISA-67.04) | instrument accuracies (`sensor_inventory.md`) | **MISSING — analysis, no sim** |
| B11 | EDG battery-vs-72h-grace sizing | load profile | **MISSING — analysis, no sim** |

---

## 3. How many simulation FILES do we need?

You asked for the single-file approach. Recommended structure — **4 simulation files/projects total**:

| File / project | Tool | Contents | Exists? |
|---|---|---|---|
| **1. `aegis40_neutronics_FER.ipynb`** | OpenMC | **ALL neutronics (N1–N12) in one notebook** — already the single file; add the 3 missing sections N10 (EBIS), N11 (SFP rack), N12 (MSLB cooldown) | ✓ exists, extend |
| **2. `aegis40_thermalhydraulics/`** | OpenFOAM | T-H (F1–F6). **F1 steady hot-channel + F4 natural-circulation DONE** (`docs/Aegis40_TH_report.docx`, chtMultiRegionFoam + correlation stack, V&V'd vs NuScale). **Extend** with F2 transients, F3 SBLOCA, F5 PRHR decay-heat, F6 containment | ✓ exists, extend |
| **3. `aegis40_consequence/`** | dispersion + ORIGEN | source term (O3) + dispersion (O1) — small, can be one notebook | ✗ create |
| **4. `aegis40_PRA.xlsx`/notebook** | PRA | event-tree quantification (O4) — CDF/LRF roll-up | partial (by-hand) |

> Mechanical/structural sims (O2 fuel-performance, O5 seismic) are **out of 3S scope** — they belong to the mechanical/civil teammate; tracked here only as dependencies (`fuel_core_structural`).

**So: 1 neutronics notebook (extend) + 1 OpenFOAM project (new, the big gap) + 1 consequence notebook (new) + 1 PRA file (formalize).** Four files cover the whole safety simulation campaign.

Each file must export a machine-readable results file (e.g. `safety_analysis_results.yaml`) so the safety criteria can be auto-checked — the neutronics notebook already does this; the others should follow the same pattern so `safety_criteria.yaml` stays the single source of truth.

---

## 4. What is MISSING (the gap list, prioritized)

**Critical path (gates the design verdict):**
1. **N6 high-stat peaking** on the 37-FA de-peaked core → confirms F_Q ≈2.0 / F_ΔH ≈1.55 (running now). **This also closes the F1↔N6 coupling** — the OpenFOAM MDNBR 1.56 PASS is contingent on it.
2. **F2 transient hot-channel** → transient MDNBR (steady F1 done; AOO transients not).
3. **F3 SBLOCA** → LOCA PCT/oxidation/H₂ (no LOCA transient run yet).
4. **F5 PRHR decay-heat transient** → the 72 h grace + PRHR ≥105 % (F4 covers only normal-op nat-circ).
5. **N10 EBIS sizing** → closes the §6.10 standalone-subcriticality claim.

*Resolved since the last revision:* **F1 steady MDNBR (1.56) and F4 natural-circulation are DONE** — the OpenFOAM model now exists and is V&V'd. The earlier "no OpenFOAM exists / biggest gap" line is retired.

**Important (named in the reviewer audit):**
6. **F6 containment P/T** (also gated on the C5 dry-vs-pool decision).
7. **N12 MSLB cooldown** → the limiting overcooling transient for this strong-negative-MTC core.
8. **N11 SFP-rack criticality** → fuel-handling safety.

*Reclassified to CITE/BOUND (no tool run — §1.C.1):* O1 dispersion/EPZ, O2 fuel performance, O3 decay heat, O4 PRA, O5 seismic — substantiated against NRC/IAEA standards + by-similarity to the NuScale NPM rather than de-novo simulation.

**Analyses with no sim dependency (do anytime):**
9. B9 tritium budget · B10 setpoint-uncertainty roll-up · B11 battery sizing · B8 coastal DBFL (needs a site study, not a reactor sim).

**Out of 3S scope but on the critical dependency list:**
10. O2 fuel-performance (FRAPCON-class) · O5 seismic+LOCA structural — mechanical/civil teammate.

---

## 5. Tool summary (the one-line answer)

| Tool | Count | What for |
|---|---|---|
| **OpenMC** | 12 simulations, **1 file** (extend with N10–N12) | criticality, coefficients, rod worth/SDM, peaking, depletion, EBIS, SFP, MSLB-cooldown |
| **OpenFOAM** | 6 simulations, **1 project (exists, extend)** | **F1 steady MDNBR (1.56) + F4 nat-circ DONE** (chtMultiRegionFoam + correlation stack, V&V'd vs NuScale, `Aegis40_TH_report.docx`); F2 transient, F3 SBLOCA, F5 PRHR, F6 containment remain |
| **Other** (dispersion, ORIGEN, PRA, FRAPCON, FEA) | 5 items — **CITE/BOUND, not run** (§1.C.1) | dose/EPZ, decay heat, CDF/LRF, fuel mechanics, seismic — substantiated by ANS-5.1, NRC SRP 4.2, RG 1.183/1.60, IEEE 344, and by-similarity to the NuScale NPM, instead of unfamiliar-tool runs |
| **Analyses** | 10 of-sim-results + 11 standalone | 11 standalone are mostly DONE; the of-sim ones wait on their runs |

*Single source of truth for limits + the rev_4 design basis: `safety/safety_criteria.yaml`. This plan is the companion that says how each limit gets its number.*
