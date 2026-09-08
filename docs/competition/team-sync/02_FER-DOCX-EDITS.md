# Aegis-40 — Pending FER `.docx` Edits (apply in Word)

**Updated:** 2026-08-14. These are consistency fixes the appendix/code already reflect but the report `.docx` does not yet. Each is a find-and-replace-scale change. Owner in **bold**. Check the box when done.

> Legend: 🔴 = must-fix (a juror can catch it) · 🟡 = polish.

---

## A. Control rods → 16 CRA (🔴 highest priority — new this round) — **Neutronics**
The report labels the rods "16 CRA" but quotes the **12-CRA** values. Adopt the 16-CRA (N5C) numbers everywhere:

| Find | Replace with |
|---|---|
| rod worth **15,672 pcm** | **21,509 pcm** |
| hot SDM **~2.0 %** | **7.85 %** |
| k_ARI (hot, all rods in) **0.980** | **0.927** |
| k_adj (hot) **0.987** | **0.933** |
| SDM margin factor **≈ ×2** | **≈ ×7.85** |

**Locations:** Table 8.2-3 · Table 8.5-2 (margin column) · Table 8.5-6 · §8.2.3 (rod-worth paragraph) · §8.6.2a (shutdown-margin paragraph).
**Also add one sentence** (§8.2.3 or §8.6.2a): *"The 16 CRAs comprise 12 peripheral + 4 central-cross assemblies occupying existing guide tubes; cold shutdown remains credited to the diverse EBIS per IAEA SSR-2/1 Req. 46."*

- [ ] Table 8.2-3  - [ ] Table 8.5-2  - [ ] Table 8.5-6  - [ ] §8.2.3  - [ ] §8.6.2a  - [ ] added the sentence

💡 *This is a net **upgrade** — lead with it in Q&A: "our rod system delivers 7.85 % hot shutdown margin, ~4× the acceptance criterion." Don't bury it as a correction.*

## B. Thermal-hydraulics typo (🔴) — **TH**
- [ ] **Table 8.4-3**, riser-height sweep, **6 m** row: MDNBR **2.78 → 1.78** (monotonic between 5 m→1.58 and 8 m→2.11; 2.78 breaks the trend).

💡 *While in this table, add a one-line footnote naming the correlation (W-3) and pressure/mass-flux range of validity.*

## C. Economics cascade (🔴) — **Economics/BOP**
The DA-7 model was recomputed at 4.43 wt%; the report has three stale spots:
- [ ] **Table 8.12-2:** LCOE **75.9 → 74.8**; cogen-credited **65.9 → 64.8**.
- [ ] **§8.12.3** text: cogen LCOE **65.9 → 64.8**.
- [ ] **Table 8.12-6**, NOAK 3 %-discount cell: **"55." → "55.5"** (truncated value).

💡 *Add a sensitivity chart (capex / capacity factor / discount rate) from `lcoe_sensitivity.csv` — turns §8.12 from a single number into a defensible range.*

## D. Figure caption (🟡) — **Neutronics/Editor**
- [ ] **Figure 8.2-4** caption: state the y-axis is **k-effective** (currently ambiguous).

💡 *Quick sweep of every figure caption for axis labels + units while you're in there — cheap consistency points.*

---

## E. Cross-check after edits (everyone, 15 min)
Once A–D are in, confirm these three numbers read identically in **FER docx + appendix + slide deck**:
1. Rod worth **21,509 pcm** / hot SDM **7.85 %**
2. LCOE NOAK **$74.8/MWh**
3. MDNBR **1.33 (W-3)**

💡 *Longer-term: keep this `team-sync/` folder as the master and treat the docx as a render of it — it's what kept us out of the 12-vs-16 trap. Consider a 10-min pre-submission "numbers parity" pass as standard.*

---

## Not-yet-in-docx design updates (context, no action unless adopted)
- **16 CRDMs in CAD:** upper-vessel drawings should show 16 rod positions (currently may show 12). — **Mechanical/CAD**
- **Fresh digital-twin sweep** (16-CRA, enriched B-10) is scripted and ready; run when the OpenMC machine is free, then the coefficients/rod-worth in DA-5 tighten automatically. — **Neutronics**

---

## ✅ WITHDRAWN 2026-08-22 — no FER change needed after all

A 21 Aug entry here asked for rod worth 21,509 → 21,479 pcm and hot SDM 7.85 → 7.68 %. **That request
is withdrawn. Do not make those edits.** The FER's existing 21,509 pcm / 7.85 % / k_ARI 0.927 are correct.

Why: the two calculations differ by evaluation state, not by quality. The safety-neutronics suite
evaluates rod worth and shutdown margin at **isothermal hot zero power** (fuel = moderator = 556 K),
which is the physically consistent state for a rods-in condition — with rods inserted the reactor is
shut down, so the fuel is not at full-power temperature. The 3 July production run holds the fuel at
900 K for both the rodded and unrodded state, giving 21,479 pcm / 7.68 %. The ~590 pcm difference is
Doppler between the two states.

The 3 July run remains authoritative for genuine full-power quantities: k at BOL, MTC, DTC, void
coefficient, discharge burnup and cycle length. Those were already correct in the FER.
