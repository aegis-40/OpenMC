# Aegis-40 Core — Design Targets and Standards Basis

**Purpose.** Fixes the *acceptance criteria* (pass/fail design targets) that the Aegis-40
neutronics model must demonstrate, and traces each target to a published standard or licensed
precedent so it can be cited directly in the FER. Created 2026-06-14 (Samira / NEU) in response
to the review of the OpenMC core model.

This document is the **single source of truth for the numbers the new core code must report as
PASS/FAIL.** Every quantity in the model's summary table must map to a row here.

---

## 1. Standards and references reviewed

| Tag | Document | What we take from it |
|-----|----------|----------------------|
| **[SSG-52]** | IAEA Safety Standards Series **No. SSG-52**, *Design of the Reactor Core for Nuclear Power Plants*, Specific Safety Guide, IAEA, Vienna (2019). ISBN 978-92-0-103819-7. | §3.18 list of **nuclear key safety parameters** (the FER core-physics checklist); §3.23 local power control / peak LHGR; §3.24–3.25 shutdown margin & burnable-absorber depletion; §3.27–3.30 thermohydraulic design limits (DNBR, peak fuel T/enthalpy); §3.40 peak fuel temperature < melting; §3.65–3.76 fuel design limits & discharge burnup; **Table I-1** (burnable absorber held to keep MTC negative *and reduce required moderator boron* → our SBF basis). |
| **[SSR-2/1]** | IAEA Safety Standards Series **No. SSR-2/1 (Rev. 1)**, *Safety of Nuclear Power Plants: Design*, Specific Safety Requirements, IAEA, Vienna (2016). ISBN 978-92-0-109315-8. | **Req 43** fuel performance; **Req 44** core structural capability; **Req 45** (6.4–6.6) core must be **inherently stable**, minimize demands on control system, limit positive reactivity insertion; **Req 46** (6.7–6.12) **two diverse, independent shutdown systems**; at least one alone holds subcritical "even for the most reactive conditions"; **6.8 = single-failure (stuck-rod) criterion** for shutdown margin. |
| **[NUREG-1431]** | U.S. NRC **NUREG-1431 Rev. 5.0**, *Standard Technical Specifications — Westinghouse Plants*, Vol. 1, Office of Nuclear Reactor Regulation (2016). | **Requirement form** (numeric values are deferred to the plant COLR): LCO 3.1.1 **SDM**; LCO 3.1.2 measured **core reactivity within ±1% Δk/k of prediction**; LCO 3.1.3 **MTC upper limit ≤ 0** (non-positive at power); LCO 3.2.1 **F_Q(Z)** heat-flux hot-channel; LCO 3.2.2 **F^N_ΔH** enthalpy-rise hot-channel. |
| **[NuScale]** | NuScale **Final Safety Analysis Report**, Ch. 4.3 (Nuclear Design), Tables 4.3-2/4.3-3. | The **numeric LWR-SMR precedent** for an SBF integral PWR: design F_Q, F_ΔH and their limits; Doppler & MTC ranges; Gd rods/assembly; control-rod-assembly worths. |
| **[RITM-200]** | Gaganov, *Thesis* (2025-04), RITM-200 iPWR SMR (2×55 MWe). | Life/refuel precedent for an integral PWR: 60-yr design life, multi-year refuel interval, HALEU enrichment band. |
| **[ATOM]** | X.H. Nguyen, S. Jang, Y. Kim, "Truly-optimized PWR lattice for innovative soluble-boron-free small modular reactor," *Scientific Reports* **11**, 12891 (2021). https://doi.org/10.1038/s41598-021-92350-5 | **The closest peer-reviewed SBF peer** (KAIST ATOM, 450 MWth, two-batch, 4.95 w/o, integral BA = CSBA+DiBA, no soluble boron). Directly supports our design choices: reactivity swing <1000 pcm; **HFP MTC −41 / FTC −2.34 pcm/K**; radial peaking ~1.5 / axial <1.3; **(N-1) stuck-rod cold-shutdown** via pseudo checker-board CR pattern; and — key for Finding 4 — **excess reactivity managed by weak mechanical-shim rods with only marginal local peaking** (pin PPF 1.07–1.12 under full MS maneuvering). |
| **[TECDOC-1936]** | IAEA **TECDOC-1936**, *Applicability of Design Safety Requirements to Small Modular Reactor Technologies Intended for Near Term Deployment* (LWR & HTGR), IAEA (2020). | SMR-specific framing: extensive **inherent + passive** safety features, lower power density, reduced source term — supports our self-regulation narrative (not numeric core targets). |

**Not neutronics targets (captured for the I&C / 3S sections, not fetched here):**
IEEE **Std 603-2018**, *Standard Criteria for Safety Systems for Nuclear Power Generating Stations*
(reactor protection / safety-system I&C — belongs to the protection-system section); IAEA **Nuclear
Security Series** collection (physical protection — belongs to §3S/safeguards). Neither sets core
physics values; listed so they are not lost.

---

## 2. Design-target table (the model's PASS/FAIL criteria)

Targets are stated as **design value (what we aim for)** and **limit (must not cross)**. The model
reports the computed value against the limit; "design value" is the margin we want to show the jury.

### 2.1 Reactivity & criticality

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| R1 | k_eff prediction vs benchmark | within ±0.5 % Δk/k | **±1 % Δk/k** | [NUREG-1431] 3.1.2 | Bias/uncertainty budget vs NuScale/RITM or a code-to-code check. |
| R2 | HFP equilibrium k_eff (controlled) | 1.000 ± held by BA+rods | critical, controllable | [SSR-2/1] R45 | BOC ARO excess must be shown *controllable*, not just reported. |
| R3 | BOC ARO excess reactivity | as low as practical | must be covered by SDM | [SSG-52] 3.24 | The ~5,000 pcm ARO excess is the headline the jury will probe — must tie to rod+BA hold-down. |

### 2.2 Shutdown margin (the N-1 / two-system requirement)

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| S1 | Shutdown margin (cold, **most-reactive stuck rod**, ARI−1) | ≥ 2.0 % Δk/k | **≥ 1.3 % Δk/k (1300 pcm)** | [SSR-2/1] 6.7–6.10, **6.8 stuck-rod**; [NUREG-1431] 3.1.1; [NuScale] | Evaluate with the single highest-worth rod fully withdrawn. |
| S2 | Diverse second shutdown means | provided & independent | **two diverse systems** | [SSR-2/1] 6.9–6.10 | Rods = primary; document the diverse second means (e.g. passive borated injection). BA is *not* a shutdown system. |

### 2.3 Reactivity coefficients — inherent stability (SSR-2/1 Req 45)

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| C1 | Moderator temp coeff (MTC), HFP, all cycle | ≤ −10 pcm/°C | **≤ 0 (non-positive)** at power | [NUREG-1431] 3.1.3; [NuScale] 0…−32.5 pcm/°F | Most-positive point = HZP/BOC; must still be ≤ 0. |
| C2 | Fuel temp coeff (Doppler) | < 0 always | **< 0** | [SSG-52] 3.18(a); [NuScale] −1.63…−2.07 pcm/°F | ≈ −2.9…−3.7 pcm/K. |
| C3 | Power coefficient | < 0 at all power levels | **< 0** | [SSR-2/1] R45 (inherent stability) | Combination coefficient — the self-regulation proof. |
| C4 | Void coefficient (coolant) | < 0 | **< 0** | [SSG-52] 3.18(h) | |

### 2.4 Power distribution / peaking (SSG-52 3.18(f), 3.23)

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| P1 | **F_ΔH** nuclear enthalpy-rise hot-channel (max-to-avg integrated **pin** power) | ≤ 1.55 | **≤ 1.65 × [1 + 0.3(1−P)]** → **1.65 at full power** | [NUREG-1431] 3.2.2; [NuScale] design 1.386 | DNBR-governing radial metric. **This is a PASS/FAIL row, not a diagnostic.** |
| P2 | **F_Q** total (3-D) heat-flux hot-channel | ≤ 2.0 | **≤ 2.32 × K(z)/P** | [NUREG-1431] 3.2.1; [NuScale] design 1.860 | Governs peak LHGR / centerline T. |
| P3 | Assembly (radial) peaking F_xy | ≤ 1.45 | design | [SSG-52] 3.23 | Already healthy (~1.24); keep. |
| P4 | Peaking incl. **xenon-oscillation + uncertainty** allowance | bounded | within P1/P2 with allowance | [SSG-52] 3.18(f) | Apply engineering uncertainty factors on the raw tally. |

### 2.5 Thermohydraulic / fuel design limits (SSG-52 3.27–3.41, 3.65–3.76)

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| T1 | Min DNBR (95/95) | ≥ 1.50 | **≥ 1.30** | [SSG-52] 3.27, 3.30 | Correlation limit; couples to F_ΔH and §8.4 BCs. |
| T2 | Peak linear heat rate (LHGR) | ≤ 25 kW/m | **≤ ~43 kW/m** (typ. PWR) | [SSG-52] 3.18(g), 3.23 | Our low power density gives large margin — a selling point. |
| T3 | Peak fuel centreline temperature | ≤ 1800 °C | **< melting (~2840 °C BOL, derated w/ burnup)** | [SSG-52] 3.40 | |
| T4 | Cladding transient strain | — | **≤ 1 %** | [SSG-52] 3.41, 3.73 | TH/fuel-perf section. |
| T5 | Rod-average discharge burnup | ~43 GWd/t (our design) | **≤ 62 GWd/t** (Zr-clad licensing) | [SSG-52] 3.70, 3.76 | 42.8 GWd/t → comfortable margin. |

### 2.6 Burnable absorber & cycle

| # | Parameter | Design target | Hard limit | Source | Note |
|---|-----------|---------------|------------|--------|------|
| B1 | Integral BA used to hold MTC ≤ 0 without soluble boron | Gd₂O₃ + Er₂O₃ zoning | qualitative | [SSG-52] Table I-1, 3.25 | **Explicit IAEA blessing of SBF + integral BA.** |
| B2 | Gd rods per assembly | core-avg 32, zoned 24/40/48 | ≤ ~32-equiv/FA region (cf. NuScale) | [NuScale] Gd ≤ 32/FA | |
| B3 | Cycle length / batches | 16 months, 4-batch | — | design | EOC k_eff ≥ 1.000 at cycle end. |
| B4 | Plant design life | 60 yr | — | [RITM-200] | |

---

## 3. How the rewritten core model must demonstrate each target
*(maps the six review findings to the targets above — this is the work plan for the code rewrite)*

1. **F_ΔH / F_Q are PASS/FAIL, not diagnostics (Findings 1, 3).**
   Add P1/P2/P3 to the YAML summary as explicit PASS/FAIL rows against the §2.4 limits. The
   reported F_ΔH = 2.232 currently **FAILS** P1 (1.65); the rewrite must (a) confirm whether it is a
   real local pin peak at a water gap / Gd-pin edge or a tally artifact (guide-tube cell counted as
   fuel, mis-reshape, normalization), then (b) fix it so F_ΔH ≤ 1.55 design target.

2. **Axial-shape verification case (Finding 2).**
   Add a verification run: **homogeneous core, no BA**, sufficient particles, correct mesh
   `reshape()` order, and compare the axial power to the expected **chopped-cosine** leakage shape.
   A saw-tooth → statistics or reshape/axial-bin-mapping bug, not physics. Document the fix.

3. **Excess-reactivity / rodded-criticality (Finding 4).**
   ~5,000 pcm BOC ARO excess (k=1.0506) must be reconciled with SBF operation: report critical
   **control-bank position** at HFP and evaluate F_Q / F_ΔH **at the critical rod configuration**,
   not only ARO. Demonstrate S1 (SDM with stuck rod) and C1 (MTC ≤ 0) at that state.
   **Precedent [ATOM]:** the KAIST SBF SMR carries an even larger ~7,700 pcm cold ARO excess and
   holds it with a weak mechanical-shim bank (~900 pcm/bank), with the peaking penalty shown to be
   marginal (pin PPF 1.07–1.12 fully in/out). This is the model for our shim-managed critical config.

4. **4-batch equilibrium loading (Finding 5).**
   Replace the fresh-core + linear-reactivity screening with a simplified
   **fresh / once- / twice- / thrice-burned** loading pattern with a shuffling assumption, to give a
   defensible cycle length and discharge burnup (B3, T5).

5. **Er-167 EOC inventory (Finding 6).**
   Reconcile the Er-167 EOC target (currently 15–25 % stated vs 3.1 % computed): fix either the
   target, the absorber-inventory extraction, or the Er zoning so the claim and the result agree.
   Tie to B1/C1 (Er is there to flatten the MTC/spectral history, not to survive to EOC).

---

## 4. Citation block for the FER (ready to paste)

> [SSG-52] International Atomic Energy Agency, *Design of the Reactor Core for Nuclear Power
> Plants*, IAEA Safety Standards Series No. SSG-52, IAEA, Vienna (2019).
>
> [SSR-2/1] International Atomic Energy Agency, *Safety of Nuclear Power Plants: Design*, IAEA
> Safety Standards Series No. SSR-2/1 (Rev. 1), IAEA, Vienna (2016).
>
> [NUREG-1431] U.S. Nuclear Regulatory Commission, *Standard Technical Specifications —
> Westinghouse Plants*, NUREG-1431, Rev. 5.0, Vol. 1, Washington, DC (2016).
>
> [TECDOC-1936] International Atomic Energy Agency, *Applicability of Design Safety Requirements
> to Small Modular Reactor Technologies Intended for Near Term Deployment*, IAEA-TECDOC-1936,
> IAEA, Vienna (2020).
>
> [NuScale] NuScale Power LLC, *NuScale Standard Plant Design Certification Application, Final
> Safety Analysis Report, Chapter 4: Reactor*, Tables 4.3-2, 4.3-3.
>
> [RITM-200] Gaganov, *RITM-200 integral PWR SMR design analysis* (thesis), 2025.
>
> [ATOM] X. H. Nguyen, S. Jang and Y. Kim, "Truly-optimized PWR lattice for innovative
> soluble-boron-free small modular reactor," *Scientific Reports* **11**, 12891 (2021),
> https://doi.org/10.1038/s41598-021-92350-5.
>
> [IEEE-603] IEEE, *Standard Criteria for Safety Systems for Nuclear Power Generating Stations*,
> IEEE Std 603-2018 (protection-system I&C — cited in the I&C section).
