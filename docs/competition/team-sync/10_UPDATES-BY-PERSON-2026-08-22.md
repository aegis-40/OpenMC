# Team Update by Person — 22 August 2026

**Finals: 26 August — four days out.**
Everything below is what changed in your area since the last sync, what you need for Q&A, and what still needs you.

**Read your own section first.** The cross-cutting section at the end affects everyone.

**Live documents:** `07_DATA-AUDIT` (what data is current) · `08_PROTOCOL-PRESENTATION-GUIDE` (the 7.5-min VIP deck) · `09_MAIN-DECK-REBUILD-SPEC` (jury deck structure + design system)

---

## Azamkhon — Safety & I&C

### What changed

**Your MSLB case was on the wrong core.** The shipped N12/N12B cases were computed with **12 CRAs of natural B₄C** (bank ≈ 13,409 pcm). The design we present is **16 CRAs at 90 % enriched B-10** (21,509 pcm) — the analysis was missing ~7,500 pcm of shutdown depth. Re-run on the correct basis:

| T (K) | old (12 CRA) | **new (16 CRA)** | |
|---|---|---|---|
| 556 | 1.0183 | **0.9345** | subcritical |
| 473 | 1.0611 | **0.9787** | subcritical |
| 423 | 1.0867 | 1.0039 | supercritical |
| 294 | **1.1142** | **1.0311** | supercritical |

The old case was supercritical **from the very first point** — rods couldn't hold the core even hot. On the real core, **rods alone hold it subcritical from full power down to ~443 K (~170 °C)**.

**EBIS needs only ~785 ppm**, not the 3,000 ppm credited (which gives k_adj = 0.790). That's a **3.8× margin** you weren't claiming.

### The Q&A risk — this is the important part

The deck used to say EBIS *"caps the return-to-power that rods alone cannot."* The SBF literature says the **opposite** — that high rod worth is exactly what makes MSLB manageable in boron-free cores (KIT TRACE/PARCS on a boron-free SMART core, *NED* 2019). A juror who knows that literature had an easy opening.

**Fixed in the deck. Your new answer:**

> "Rod worth handles the hot trip **and most of the cooldown** — at 21,509 pcm the core stays subcritical from full power down to about 170 °C with the most-reactive rod stuck. EBIS covers only the deep cold state, where a boron-free core is inherently supercritical. And we need about 785 ppm to do it; we credit 3,000."

That is now consistent with the literature instead of contradicting it.

### What still needs you

1. **I&C diagram** — slide 22 currently carries the v1 architecture. The v2 adds the **≤500 ms response-time budget** (sensor ≤150 → conditioning ≤50 → voting ≤100 → breaker/rod ≤200, + ~2.5 s free-fall). Check it reads correctly to you before Monday.
2. **Two new slides are needed in your area** (see `09_...SPEC`): **Defence in Depth** (§8.5.3, five levels) and **Site Hazards — Sinop** (§8.5.2c). Both are FER content with no slide at all right now.
3. **GDC-28 reactivity limits** (§8.6.6) — absent from the deck, should fold into the shutdown-architecture slide.
4. **Decide** whether to supersede N12/N12B inside the shipped digital appendix. Replacing results in a submitted package is a team call — I flagged it, didn't do it.

**Files:** `openmc_model/results_mslb_n5c/` · `openmc_model/scripts/run_mslb_n5c.py`

---

## Adilbek — Safety & Auxiliary Systems

### What changed

Several audit corrections landed in your slides:

| Was | Now |
|---|---|
| "9 six-field FER tables" | **Nine auxiliary systems (six-rubric FER subsections)** |
| "rad-protection 4 layers (RG 1.97)" | **4 dose-rate zones (NS-G-1.13 / ICRP 103)** — RG 1.97 is monitoring, not zoning |
| Island I list included "control room" | **MCR is Cat I but sited in the Turbine Island** |
| LOHS "~10⁻⁷/ry" | **~10⁻⁸/ry** (the per-initiator value) |
| SBO "72 h" | **≥240 h grace (72 h battery for monitoring)** |

**New content added:** a support-systems block — *Class-1E 2×EDG + 72 h batteries · fail-safe instrument air & valve actuation · fuel route fresh → refuelling cavity → SFP → dry cask · demineralised water & reduced CVCS.*

### What you need for Q&A

**The SFP boron question is near-certain.** "You say the reactor is boron-free — why does your spent-fuel pool have boron?"

> "Boron-free applies to **reactor-coolant reactivity control** during normal operation. The spent-fuel pool independently uses ~2000 ppm plus fixed absorber racks with burnup credit, as criticality defence-in-depth. They're separate systems."

This is now explicit on the waste slide rather than left to Q&A.

### What still needs you

1. **§8.8.9 Cogeneration Interface Isolation has no slide** — and *"could the hydrogen or district heat be contaminated?"* is a near-certain jury question. You have a strong three-barrier answer (OTSG tube wall → intermediate heat exchanger → monitored non-radioactive loop). Build it with Alisher; spec is in `09_...SPEC` Part 3.
2. **§8.6.7 Fault-tree analysis** appears only as a passing mention on slide 6. Event trees are shown; fault trees are not.

---

## Shakhzod — Thermal-Hydraulics & CAD

### What changed

**MDNBR defending footnote added** to the thermal-margin slide:

> MDNBR 1.33 uses W-3 with the record (most top-peaked) axial shape; the 1.30 limit already embeds the 95/95 statistical DNB margin — true margin to CHF is far larger (Groeneveld LUT 6.18).

This pre-empts *"1.33 looks thin"*, which is the obvious attack on that number.

**CFD chart regenerated** with the real values — CFD [345, 866, 408, 389] vs correlation [345, 867, 399, 381], near-wall Δ < 9 K.

### What still needs you

1. **Your two thermal slides merge into one** (`Thermal Margin Closure` + `Thermal-Hydraulics` → *Thermal Margins*). See `09_...SPEC` Block C.
2. **Figure quality standard** — every figure needs ≥ 200 dpi and **no text below 10 pt at placed size**. Check yours by placing and reading from 2 m. Several figures were flagged as unreadable from the back of a room.
3. **Slide 24 (Advisory Dashboard) still shows a 3-D CAD viewer screenshot**, not a dashboard. Either swap in the real dashboard image or move the CAD render to a slide where it belongs.
4. **Your RPV render is the single best visual asset the team owns** — it's the hero image for both the jury deck and the protocol deck. If you have a higher-resolution or better-angled export, it's worth producing.

---

## Alisher — Cogeneration & Secondary Cycle

### ⚠️ Two problems found in the DWSIM PFD today — check before Monday

First, confirming the model is the right one: the three turbine duties sum to **42,793.76 kW**, exactly the **42.794 MW** shaft power in FER §8.4.3. So this is the FER cycle, and anything you change here propagates to the 40 MWe and 32 % net headline numbers.

**1. MIX-1 puts two-phase fluid into PUMP-2's suction.**

```
in :  38.44 kg/s @ 39.0 °C  +  11.62 kg/s @ 111.35 °C  (MS drain 10 + IP extraction 8)
out:  50.06 kg/s, h = 233.9 kJ/kg
at 0.007 MPa: hf = 163.4  →  TWO-PHASE, ~2.9 % vapour
```

The 39.00 °C on stream 14 is thermodynamically correct — the hot drains flash at condenser pressure and sit at saturation. But that means **PUMP-2 takes wet suction and will cavitate.**

The fix is architectural: cascade the MS drain and IP extraction **into the condenser** (upstream, so the flash steam condenses), or into a feedwater heater/deaerator at their own pressure. Do not mix them into the condensate line *downstream* of the condenser.

*Caveat: I inferred the topology from a screenshot using the mass balance (38.44 + 5.61 + 6.01 = 50.06 ≈ 50.05, which closes). Confirm against the DWSIM file before reworking.*

**2. The 39 °C / 0.01 MPa pairing is inconsistent as displayed.**

| | |
|---|---|
| Tsat at 0.010 MPa | 45.81 °C |
| Psat at 39.00 °C | **0.0070 MPa** |

39 °C at 0.010 MPa is 6.8 K subcooled — and stream 11 is a turbine exhaust, which cannot be subcooled liquid. Almost certainly the true condenser pressure is ~0.007 MPa and DWSIM's two-decimal display rounds it. **Confirm**, because condenser pressure sets LP backpressure and hence the 32 % net efficiency.

**3. Minor:** PUMP-1 appears to add no head — streams 12 and 13 both read 0.01 MPa. Check its specified discharge pressure.

**Answered for the record:** no, pressure should *not* drop across the condenser. Condensation is isobaric; a real unit has a few kPa of steam-side ΔP, negligible in a cycle model. That part of your diagram is right.

### What still needs you

1. **Cogeneration isolation slide** (§8.8.9) — with Adilbek, see above.
2. **Your two economics slides merge into one**; the LCOE tornado moves to backup. A reviewer capped economics at 2–3 minutes.
3. For the **protocol deck**, the cogeneration PFD is too dense — a simple three-arrow graphic (electricity / heat / hydrogen) is specified instead.

---

## Laziz — Neutronics & NPP Layout

### Your 3 July run is now the authoritative basis

The **STAT_FINAL production run** (400 batches × 50,000 particles, 32 threads) is the agreed source of truth for full-power quantities: k_BOL 1.15042, MTC −26.868, DTC −1.911, void −173.156, burnup 29.608 GWd/tHM, 2224.17 EFPD, F_ΔH 1.576, F_q 2.045.

### The 590 pcm puzzle — resolved, and it is *not* an error

Your run and the safety-neutronics suite disagree by ~590 pcm on absolute k. Cause: **different evaluation states, both self-consistent.**

- Your run holds fuel at **900 K** for both rodded and unrodded states.
- The safety suite passes `fuel_temp = moderator temp`, i.e. **isothermal hot zero power**.

The Doppler shift appears equally on both states (589 pcm on ARO, 647 pcm on the single-rod case), which is what proves it's a state difference rather than a modelling error.

**Agreed split:** full-power quantities from your run; **bank worth and hot SDM from HZP (21,509 pcm / 7.85 %)**, because with rods inserted the reactor is shut down — rods-in *and* fuel at 900 K is not a physical steady state. **The FER's existing numbers are correct; no Word edit needed.**

### One caution about your summary file

`safety_analysis_results.yaml` reports `central_rod_worth_pcm = 722.5`. That value matches a **natural-boron** rod (794 ± 48 pcm, 1.5σ), not the 90 %-enriched design (902 ± 34 pcm, 5σ away). **Don't use it for the rod-ejection case** — worth checking what absorber that diagnostic was run with.

### New this week

**β_eff computed: 704.5 ± 28.2 pcm** (prompt-k method, STAT_FINAL both runs). That's ~8 % above the 650 pcm literature default everyone assumes.

### What still needs you (layout)

1. **§8.10.6 Critical piping arrangement** — no slide.
2. **§8.10.7 Multi-unit roadmap** — currently one clause on the layout slide; the FER has a fuller treatment.
3. Your **in-line site layout diagram** is correct for the jury but far too dense for the protocol deck — a simplified version is specified in `08_...GUIDE`.
4. **`N_BATCHES = 4`** is a stale label in the safety module's print banner (the production YAML correctly has `n_batches_reload: 1`). Cosmetic, but grep before the FER is final.

---

## Samira — Neutronics & Digital Twin

- Digital twin refreshed on the **168-point sweep**: k_eff R² = 0.9925, F_ΔH R² = 0.9961, power-map R² = 0.9768. The sweep's raw data existed only in a scratch directory and is now committed (`outputs_v2/core_sweep_168pt.csv`).
- **Twin and dashboard merge into one slide** — it's an advisory, non-credited tool and currently has two.
- Speaker notes written for intro / core / ending (`speaker-notes-Samira.md`), ~14 min 40 s.
- Paper draft ready for team review (`papers/01_rod-worth-invessel-crdm/`).

---

## Cross-cutting — everyone

### The jury deck is being rebuilt

Nine FER areas have **no slide at all**, including **three numbered FER template sections** the jury scores against:

- **§3 Literature Review**
- **§6 Project Work Plan**
- **§7 Broader Impacts & Target Audience**

Plus §8.5.2c site hazards, §8.5.3 defence in depth, §8.6.6 GDC-28, §8.8.9 cogen isolation, §8.10.6 critical piping, and §8.6.7 fault trees.

Target: **40 → 30 main slides + 10 backup**, ≈28:30. Full structure and a slide design system (grid, type scale, palette, seven layout archetypes) in `09_MAIN-DECK-REBUILD-SPEC`.

### Rules that came out of this week's mistakes

1. **Every number on a slide must exist in the FER with the same value.** A mismatched rod-worth figure cost two days of investigation.
2. **No duplicate slide titles.** There are currently two "Core Design" and two "Reactor Safety Systems".
3. **Figure numbers sequential, no duplicates** — Fig. 4, 9, 10 and 13 each appeared twice before being fixed.
4. **The .pptx round-trips through Google Slides lose edits.** Three times now. Tell Samira before you open it, and treat the file as final once she's re-applied changes.

### There is a second presentation

A **≤7.5-minute protocol presentation** for the official delegation (minister, TENMAK, T3 Vakfı, rectors). It is **not scored** — representational. It needs a **separate deck**: 8 slides, Turkish text, minimal formulas, maximum visuals. Do not reuse jury slides. Guide: `08_PROTOCOL-PRESENTATION-GUIDE`.

### Open items needing a person

| # | Item | Who |
|---|---|---|
| 1 | Commit the final ~7 Jul waste CSV backing the FER's 78.1 kg Pu — nothing in the repo reproduces it | whoever ran it |
| 2 | Decide on superseding N12/N12B in the shipped appendix | Azamkhon + team |
| 3 | Confirm the DWSIM condenser pressure and drain routing | Alisher |
| 4 | Verify the absorber used in `central_rod_worth_pcm` | Laziz |
| 5 | Build the six missing slides | per section above |
| 6 | Turkish text reviewed by a fluent technical speaker | team |
