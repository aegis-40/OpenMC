# FER correction checklist — Aegis40_FER_submission_ready_compact_final.docx

Do these as Word Find & Replace (Ctrl+H) unless noted. Formatting stays intact because you
type into existing styled cells. Authoritative source for every number is the digital appendix
(the actual OpenMC / model output), noted per item.

Legend:  🟢 safe number swap · ⚪ deletion · 🔴 needs your decision · 🔵 cosmetic

================================================================================
GROUP 1 — SAFE NUMBER SWAPS (A and C)
================================================================================

🟢 A. BOC PEAKING — §8.2 is correct (1.513 / 1.937); fix §8.5 only.
   Source: 5_digital_twin/.../evidence/cycle-peaking-COLR-paste.md (STAT_FINAL 2026-07-03)

   Table 8.5-2 (Principal safety criteria):
     Find "2.035 (beginning-of-cycle)"   → replace "1.937 (beginning-of-cycle)"
     Find "1.583 (beginning-of-cycle)"   → replace "1.513 (beginning-of-cycle)"
   §8.5.2 body text (paragraph after Table 8.5-2):
     Find "F_Q 2.035 / F_DeltaH 1.583"   → replace "F_Q 1.937 / F_DeltaH 1.513"
   (optional consistency) §8.5.2 and §8.5.4 "12.8 kW/m" BOC hot-rod
     → "12.4 kW/m"  (matches §8.3.2, which uses BOC F_q 1.937 → 12.4 kW/m)

🟢 C. DECAY HEAT — CORRECTED (my earlier advice was backwards).
   Your report's rigorous shutdown value 7.94/7.95 MW IS the final Jul-3 STAT_FINAL sim
   (§8.11 says so explicitly). The 7.747 MW in decay_heat_rigorous.csv is the OLDER Jun-4 run
   -> the APPENDIX CSV is stale, NOT the report. And 7.75 MW in §8.5/§8.6 is the ANS-5.1 design
   curve = a deliberately DIFFERENT basis. So DO NOT change 7.94/7.95 -> 7.75.

   Real fixes (unify the report TO the §8.11 final-run set):
   Table 8.2-9 (Depleted-fuel indicators):
     Find "10.3 kW"   → replace "9.0 kW"     (match §8.11 final-run 10-yr value)
     Find "7.94 MW"   → replace "7.95 MW"    (match §8.11; trivial rounding)
   §8.8.4 body text:
     Find "about 7.8-7.9 MW at shutdown" → replace "about 7.95 MW at shutdown"
   §8.5/§8.6 "7.75 MW"  → KEEP (ANS-5.1 curve; different basis, report explains it).
   §8.11.3 "7.95 MW ... 48.4 kW at 1 yr ... 9.0 kW at 10 yr" → KEEP (final rigorous run).

   APPENDIX-SIDE (I can do): decay_heat_rigorous.csv, Table 8.11-2 and plot_decay_heat.py are
   the Jun-4 run and now disagree with §8.11 -> regenerate from the Jul-3 STAT_FINAL record so
   DA-6 matches the report. (Needs the final depletion H5.)

================================================================================
GROUP 2 — DELETE LEFTOVER AUTHORING NOTES + DUPLICATE ROWS  ⚪
================================================================================

Table 8.1-1: delete the phrase "; use same value in 8.11/8.12"
   (row "Capacity factor - fuel/waste/economics sensitivity"; keep "90-95 % range")
Table 8.1-1: DELETE the duplicated last row
   "Plant type | Integral PWR (iPWR)... | Light-water reactor, UO2/Zr-4 fuel"  (it repeats row 1)
Table 8.1-2: delete the phrase "Keep consistent with 8.4 model"
   (row "Primary coolant inventory"; keep "~26 t / ~35 m3")
Table 8.1-7: DELETE the duplicated last row "Class-1 pressure boundary | ASME BPVC Section III..."
Table 8.1-8: DELETE the duplicated last row "IAEA SSR-2/1 Rev. 1 | Top-level NPP design..."

================================================================================
GROUP 3 — 🔴 B: ROD WORTH / SHUTDOWN MARGIN  (DECISION NEEDED)
================================================================================
Authoritative: 4_safety_neutronics/outputs/results/safety_neutronics_results.json, case N5B
(90 %-enriched-B-10, 16 CRA = your FINAL rod design):
   total_bank_worth_pcm = 15,672   (NOT 21,437 / 21,479)
   k_aro_hot 1.1583 → k_ari_hot 0.9803  → hot all-rods-in SUBCRITICAL by ~2.0 %  ✓
   k_ari_cold 1.0815 (supercritical) → cold shutdown credited to EBIS (as §8.6.2a already says)

DECISION: (a) keep 16 CRA and correct the numbers to N5B (recommended), OR
          (b) if you actually ran 20 CRA (N5C) to get ~21k pcm, change "16 CRA"→"20 CRA"
              everywhere (bigger change) and give me that run to confirm the worth.

If (a) — apply these exact edits:

Table 8.2-3 (Neutronic safety results):
   Row "Control-rod bank worth, 16 CRA ARO -> ARI":
      "21,479 pcm"  → "15,672 pcm"   (Limit >=5,000 pcm; Status PASS — unchanged)
   Row "Shutdown margin, most-reactive rod stuck, hot | +7.68% Delta-k/k signed | ... | PASS":
      → replace the whole row with:
      "Shutdown margin, hot all-rods-in (ARI) | ~2.0 % Delta-k/k (k=0.980) | >= 1.0 % | PASS"
   (add, if not present) a row:
      "Cold shutdown | credited to EBIS boron injection (§8.6.2a) | k<=0.99 at ~2153 ppm | PASS (diverse system)"

§8.2.3 "Shutdown-margin interpretation" paragraph — replace:
   "The hot most-reactive-rod-stuck shutdown margin is +7.68% Delta-k/k, exceeding the 1% target."
   WITH:
   "With 90 %-enriched-B-10 rods the 16-CRA bank worth is 15,672 pcm; the hot all-rods-in state
    is subcritical (k=0.980, ~2.0 % Delta-k/k). Because the soluble-boron-free core is
    supercritical when cold with rods alone, cold shutdown is credited to the diverse EBIS
    (Section 8.6.2a), satisfying SSR-2/1 Req. 46."

Table 8.5-2:
   "Hot shutdown margin (16 rod assemblies) | >= 1 % | ~7.6 % | x7.6"
      → "... | >= 1 % | ~2.0 % (hot, all rods in) | x2"
   "Control-rod bank worth (16 rod assemblies) | - | ~21,437 pcm vs ~13,300 pcm ... excess | -"
      → "... | - | ~15,672 pcm vs ~13,300 pcm BOC excess | -"

Table 8.5-6 (reactivity/power-control row):  "bank worth 21,437 pcm, hot SDM ~7.6 %"
      → "bank worth 15,672 pcm, hot SDM ~2.0 %"

§8.6.2a list item 1 (control rods):  "bank worth ~21,437 pcm gives a hot-trip subcritical margin of ~7.6 %."
      → "bank worth ~15,672 pcm gives a hot all-rods-in subcritical margin of ~2.0 % (k=0.980)."

Also fix any 21,437 / 21,479 / "hot SDM 7.6 %" anywhere else (global Find "21,437" and "21,479").

NOTE: 2.0 % hot margin is still > the 1 % requirement (PASS), and cold is EBIS — your §8.6.2a
logic is already correct, this just makes the summary tables match the calculation.

================================================================================
GROUP 4 — 🔴 D: HYDROGEN OUTPUT (DECISION NEEDED — has an economics cascade)
================================================================================
Two different operating assumptions, both defensible:
   • 120 t/yr — 7_energy_cycle/code/soe_h2_schedule.py, explicit off-peak schedule
                (8 MWe electrolyser, ~585 h/yr; in-code note "DECIDED 2026-07-02 → ~120 t/yr")
   • 427 t/yr — §8.12 estimate "5 % of net electricity ÷ 39 kWh/kg" (≈2 MWe avg, ~25 % duty)

The report's §8.12 economics (H2 revenue ~$2.1 M, cogen-credited LCOE $65.9/MWh) are already
built on 427 t. So:
   • Lowest-risk before deadline: KEEP 427 t in the report and update the appendix DA-7 note +
     soe_h2_schedule.py hours to match (electrolyser runs ~2080 h/yr, not 585). One appendix edit.
   • More physically-grounded: adopt 120 t and redo §8.12 H2 revenue + LCOE (bigger change).
Either way, report and appendix MUST state the same number and same electrolyser duty.
Tell me which and I'll make the appendix side consistent.

================================================================================
GROUP 5 — 🔵 COSMETIC / LIST / ABBREVIATIONS
================================================================================
Abbreviations table — ADD (at least the first two):
   COLR  Core Operating Limits Report   ·   SGTR  Steam-Generator Tube Rupture
   NOAK  Nth-of-a-kind · FOAK First-of-a-kind · SWU Separative Work Unit
   LCOE/LCOH/LCOH2 Levelized Cost of Electricity/Heat/Hydrogen · CNV Containment Vessel · LWR Light-Water Reactor · GDC General Design Criteria

List of Tables/Figures — title mismatches (make list = body caption):
   Table 8.4-5: list "Secondary Rankine-cycle state points" vs body "Secondary-cycle design-point summary"
   Figure 8.10-2: list "Secondary-side steam distribution..." vs body "Combined energy-island interface"
Appendix E text: "Figures 8.8-1 to 8.8-16" → "8.8-1 to 8.8-15"

Table numbering: List skips Table 8.1-5 and Table 8.3-5, and Table 8.6-4 prints before 8.6-2/8.6-3
   in the body. Confirm these gaps/order are intentional or renumber. (Cosmetic; a jury scanning
   the list notices missing numbers.)

Digital-appendix maps: Table A-1 lists DA-5 → "Section 8.7, 8.12" but Table A-2's 8.12 row credits
   only DA-7. Either add DA-5 to the A-2 8.12 row or drop 8.12 from DA-5 in A-1.

"STAT_FINAL" jargon (appears ~6× in main text): gloss once in §8.2.3, e.g.
   "the high-statistics reference depletion run (STAT_FINAL: 400 batches / 80 inactive / 50 000 particles)."

§8.11 intro: "corrected material volumes, 2026-07-03" → "final verified depletion record."

Efficiency: Table 8.1-1 "32.0 nameplate / 31.8 computed" — either explain 31.8 (gross vs net) or
   just state "32.0 %".

Condenser pressure: standardize to 7 kPa / 39 °C (39 °C saturates at ~7 kPa, not 0.01 MPa).
   Appears in Tables 8.4-1, 8.4-4, 8.4-5, 8.4-12 and F-2. (Minor thermo consistency.)

Residual U-235: §8.2.5 "151 kg" vs §8.11.3 "1.77 wt% U-235" — 151 kg / ~9.1 tHM ≈ 1.66 wt%.
   Reconcile the two (pick 1.66 wt% or restate the mass). Minor.

================================================================================
PRIORITY IF SHORT ON TIME
================================================================================
1. B — rod worth 15,672 + SDM re-label (Group 3)   ← most important, a jury can catch this
2. A — 1.583/2.035 → 1.513/1.937 (Group 1)
3. Delete authoring notes + duplicate rows (Group 2)
4. C — 7.94/7.95 → 7.75, 10.3/9.0 → 8.3 (Group 1)
5. Add COLR + SGTR to abbreviations (Group 5)
6. D — decide hydrogen number (Group 4)
