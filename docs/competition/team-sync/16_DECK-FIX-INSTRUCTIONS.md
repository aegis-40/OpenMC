# Deck fix instructions — line-by-line audit

**Deck:** `Final presentation-new`, Google Slides, **43 slides**, read 23 Aug 2026.
**Method:** every slide read in full — numbers cross-checked against the authoritative FER
(`Aegis40_FER_submission_ready_compact_final.docx`, 15 Jul) and `FROZEN-MASTER-VALUES.md`; page numbers,
figure numbers, citations, units and Turkish text checked individually.

**Slide order is deliberate** (Samira's OpenMC block pulled forward). Nothing below asks you to move a
slide except where noted.

**Verdict:** the physics is in good shape — I re-derived a dozen values and they check out. What needs
work is bookkeeping: page numbers, figure numbers, a broken reference list, and four genuine technical
errors.

---

# BLOCKERS — wrong, not just untidy

## B1 · Slide 29 carries the wrong body text ⚠️

"Core-Damage Frequency Arithmetic" has the **radiation-shielding paragraph** pasted into it:

> *"The build is deliberately lead-free: 20 cm borated polyethylene plus 180 cm magnetite heavy
> concrete. That closes the occupational-dose target…"*

The "Result:" label is **empty**, and the correct number only exists in the Turkish özet.

**Replace the body with:**

> Nine initiator groups are quantified sequence by sequence and summed: **Σ CDF ≈ 5.8 × 10⁻⁸ /ry**,
> against a design target of < 1 × 10⁻⁷ /ry. Every core-damage path requires at least two independent
> failures.

And fill "Result:" with **Σ CDF ≈ 5.8 × 10⁻⁸ /ry — below target**.

## B2 · The reference list is broken

Slide 38 lists **[1]–[8] only**. The deck cites **[9,10]**, **[7,8,12]** and **[14,15]** on slide 7.
**Five citation numbers point at nothing.**

Additionally, these are cited *in-text* on slides but appear nowhere in the list:
`ASME III` · `ASME V&V-20` · `SRP 4.2 / 4.4` · `10 CFR 50.46` · `10 CFR 100` · `IEEE 603` ·
`IEEE 384` · `10 CFR 73.54` · `ICRP-116` · `IAEA SSG-52` (in [4], ok).

**Fix:** extend the list to at least [15] and add entries for OpenMC (Romano et al. 2015),
ENDF/B-VIII.0 (Brown et al. 2018), OpenFOAM, ICSBEP, BEAVRS, ASME BPVC III, ASME V&V-20,
IEEE 603/384. Then re-check every bracket in the deck resolves.

Also add the edition to **[1]**: *"IAEA. Advances in Small Modular Reactor Technology Developments,
**2022 Edition**."* — that is the edition the comparison numbers came from.

## ~~B3 · Slide 21 "single turbine"~~ — **withdrawn, the slide is correct**

*Corrected 24 Aug. I read the DWSIM flowsheet's three turbine blocks as three machines. They are the
HP, IP and LP sections of **one tandem-compound turbine** on a single shaft — DWSIM has no multi-stage
turbine object, so each section must be modelled as a separate block. **No change needed.***

**Optional only:** writing *"single tandem-compound turbine"* would pre-empt a juror who compares the
slide against the appendix flowsheet and counts three blocks. Wording, not a correction.

## B4 · Power-density row: SMART and CAREM are swapped

Slide 35 column order is **Aegis · NuScale · SMART · CAREM**, but the values were pasted in a different
order:

| Column | Shows | Should be |
|---|---|---|
| SMART | 1.64 | **6.40** |
| CAREM-25 | 6.40 | **1.64** |

CAREM-25 is the low-power-density design (100 MWth / 61 FA); SMART is 365 MWth / 57 FA. As it stands
the slide claims SMART runs at half our power density, which is backwards and checkable.
*(My column ordering caused this — sorry.)*

## B5 · Slide 12 — one stress value is mislabelled

The slide reads *"(thick-wall Lamé inner-surface 123 MPa; …)"*. Working the numbers:

| Value | What it actually is |
|---|---|
| **142 MPa** | Lamé hoop at the inner surface, **design** pressure 14.1 MPa ✓ (I get 142.1) |
| **135 MPa** | von Mises at the inner surface, design pressure ✓ (I get 135.3) |
| **123 MPa** | **thin-wall membrane** p·r/t at **operating** pressure ✓ (I get 122.3) — *not* Lamé |

So 142 and 135 are correct and well-labelled; **123 is not a Lamé value.** Lamé at the inner surface
*is* 142 — a thick-wall hoop stress cannot be below the thin-wall estimate.

**Fix:** *"(thin-wall membrane at operating pressure 123 MPa; full ASME III stress report = detailed
design)"*. Also state the pressure case on each number — a mechanical reviewer will ask.

## B6 · Slide 20 — the DNBR sentence is technically wrong

> *"1.30 is a statistically protected correlation limit, so physical margin to departure from nucleate
> boiling is a further 30 % beyond it."*

The "30 %" does not follow from anything — it reads as if the **1.30 ratio** were a 30 % margin. A 95/95
limit means the correlation's uncertainty is *already inside* the 1.30; there is no separate additional
30 %.

**Replace with:**

> 1.30 is a 95/95 statistically protected limit — the correlation uncertainty is already contained
> within it. Operating at 1.33 is therefore above the *protected* limit, not merely above the onset of
> boiling crisis.

---

# HIGH — internal contradictions a juror can find

## H1 · Every page number from slide 16 onward is wrong

Your scheme is **footer = position − 1**, with dividers counted but not numbered (slide 11 → "10" ✓).
That holds up to slide 15. From slide 16 the footers are the *old* positions:

| Slide | Footer now | Should be | | Slide | Footer now | Should be |
|---|---|---|---|---|---|---|
| 16 Shielding | 29 | **15** | | 30 Shutdown | 25 | **29** |
| 17 Waste | 31 | **16** | | 31 Twin | 27 | **30** |
| 18 Fuel Cycle | 15 | **17** | | 32 Auxiliary | 28 | **31** |
| 19 Cooling | 16 | **18** | | 33 Layout | 30 | **32** |
| 20 Thermal | 17 | **19** | | 34 Economics | 32 | **33** |
| 21 Energy | 18 | **20** | | 35 Comparison | 33 | **34** |
| 22 Cogen Isol. | 19 | **21** | | 36 V&V | 34 | **35** |
| 23 Site Hazards | 21 | **22** | | 37 Summary | 35 | **36** |
| 25 Safety Criteria | 20 | **24** | | 38 References | 36 | **37** |
| 26 DiD | 22 | **25** | | 39–42 BACKUP | 35 ×4 | **38–41** |
| 27 Passive | 23 | **26** | | 43 I&C | 26 | **42** |
| 28 Event matrix | 24 | **27** | | | | |
| 29 CDF | 29 | **28** | | | | |

**29 and 35 each appear twice.** If renumbering 28 slides by hand is too much, the cheaper fix is to
**delete the footer numbers entirely** — no rule requires them, and wrong numbers are worse than none.

## H2 · Figure numbers are out of sequence, and Fig. 11 is used twice

Order of appearance is currently **1, 2, 3, 13, 15, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 11**.

| Slide | Now | Should be |
|---|---|---|
| 12 Reactor Vessel | Fig. 1 | Fig. 1 ✓ |
| 13 Core Config | Fig. 2 | Fig. 2 ✓ |
| 14 Cycle Results | Fig. 3 | Fig. 3 ✓ |
| **16 Shielding** | Fig. 13 | **Fig. 4** |
| **17 Waste** | Fig. 15 | **Fig. 5** |
| 19 Cooling | Fig. 4 | **Fig. 6** |
| 20 Thermal | Fig. 5 | **Fig. 7** |
| 21 Energy | Fig. 6 | **Fig. 8** |
| 22 Cogen Isolation | Fig. 7 | **Fig. 9** |
| 23 Site Hazards | Fig. 8 | **Fig. 10** |
| 26 Defence in Depth | Fig. 9 | **Fig. 11** |
| 27 Passive Safety | Fig. 10 | **Fig. 12** |
| **29 CDF** | Fig. 11 | **Fig. 13** ← duplicate today |
| 30 Shutdown | *(none)* | — |
| 31 Digital Twin | Fig. 12 | **Fig. 14** |
| 33 Layout | Fig. 14 | **Fig. 15** |
| **43 I&C** | Fig. 11 | **Fig. 16** ← duplicate today |

## H3 · Table of contents no longer matches the deck

Slide 3 says block **E · I&C AND PLANT SYSTEMS — "Protection, twin, auxiliaries, layout, waste"** and
block **B — "Parameters, vessel, core, fuel, cycle"**.

Waste is now in block B, and **shielding is not mentioned anywhere in the TOC**.

**Fix:** B → *"Parameters, vessel, core, fuel, shielding, waste, cycle"*; E → *"Protection, twin,
auxiliaries, layout"*.

## H4 · Divider slide 10 lists the wrong sections

*"§8.1 Facility · §8.2 Core · §8.3 Fuel & materials · §8.4 Cooling circuit"* — but shielding (§8.10)
and waste (§8.11) now sit in this block. Add them.

**Slide 24 has no subtitle at all** — divider I has one, divider II is bare. Add the matching line:
*"§8.5 Safety · §8.6 Passive systems · §8.7 I&C · §8.8 Auxiliary · §8.10 Layout · §8.12 Economics"*.

## H5 · Hot shutdown margin — "~4×" contradicts "≥ 1 %"

Slide 25 states the operating envelope as **hot shutdown margin ≥ 1 %**.
Slide 30 says rods carry hot shutdown with **"~4× the required margin"**.

7.85 % ÷ 1 % = **7.85×**, not 4×. The 4× only works against a 2 % criterion.

**Pick one and make both slides agree.** If the acceptance criterion really is ≥ 1 %, say **"~7.9× the
required margin"** — it is a stronger number and it is yours.

## H6 · Slide 28 — criterion and result don't match on the first row

| Event | Acceptance criterion | Result |
|---|---|---|
| Rod withdrawal (AOO) | **MDNBR ≥ 1.3** | *1.5 × 10⁻⁵ vs 7.5 × 10⁻⁴ Δk/k/s — 50× margin* |

The criterion is a thermal one; the result reported is a reactivity insertion rate. Either state the
criterion as **"insertion rate within the analysed envelope"**, or report the MDNBR reached in the
transient. As written the row does not close.

## H7 · Slide 14 — "EOC · 30.8" is past end of cycle

The table gives **discharge burnup 29.6 GWd/tHM** and the state row gives **EOC · 30.8** with
**k = 0.9910**. A state with k < 1 is beyond end of cycle, so labelling it EOC is inconsistent with the
29.6 above it.

Check: 125 MWth × 2224 EFPD ÷ 9.39 tHM = **29.6 GWd/tHM** ✓ — so 29.6 is the discharge value and 30.8
is the last depletion step. **Relabel that row "final step · 30.8"** or drop the burnup figure from it.

## H8 · Slide 21 özet claims something the slide does not say

Turkish: *"ısı depolama **veya** elektroliz, ikisi birlikte değil"* (heat storage **or** electrolysis,
not both together). Nothing in the English text says the two are mutually exclusive. Either add that
constraint to the English or soften the özet.

## H9 · Capacity factor — 95 % on slide 11, 90 % in the economics

Slide 11 states **95 % target capacity factor**; the LCOE on slide 34 is computed at **90 %**. Both come
from the FER (95 % design target, 90 % used conservatively in analysis) so neither is wrong — but a
juror who spots it will ask. **Add "(economics evaluated at 90 %)"** to slide 11 or to slide 34.

---

# MEDIUM — consistency and formatting

## M1 · Superscripts and subscripts are not applied consistently ⚠️ *global sweep*

Wrong in these places, correct elsewhere in the same deck:

| Slide | Reads | Should read |
|---|---|---|
| 4, 9 | `Gd2O3/Er2O3` | Gd₂O₃ / Er₂O₃ |
| 15 | `UO2 pellets` | UO₂ pellets |
| 11 | `< 10−7 / ry`, `< 10−8/ ry` | < 10⁻⁷ /ry, < 10⁻⁸ /ry |
| 16 | `3.02 × 1018`, `1.0 × 1019` | 3.02 × 10¹⁸, 1.0 × 10¹⁹ |
| 9 | `1.5 × 10 −5` *(space in exponent)* | 1.5 × 10⁻⁵ |
| 28 | `10−5`, `10−4`, `10−8`, `10−11` | 10⁻⁵, 10⁻⁴, 10⁻⁸, 10⁻¹¹ |

This is the single most visible polish item in the deck — exponents printed as `1018` look like a typo
for one thousand and eighteen.

## M2 · Small text fixes

| Slide | Fix |
|---|---|
| 6 | `Flexible operaation` → **operation** |
| 7 | `OpenFOAM CHT;W-3` → `CHT; W-3` (missing space) |
| 8 | `YERLILIK` → **YERLİLİK** · `HEDEF KITLE` → **HEDEF KİTLE** (Turkish dotted İ) |
| 16 | fluence result has no units; target says `n/cm²`. Put the unit on both or on the header |
| 25 | `dose ≤ 10 CFR 100` → `dose within 10 CFR 100 limits` |
| 30 | `…as SSR-2/1 Req. 46 demands` — missing full stop |
| 30 | `A standby-liquid-control principle Rods carry hot shutdown with…` — **run-on, no punctuation.** Rewrite as: *"A standby-liquid-control principle: rods carry hot shutdown with ~7.9× the required margin; boron injection carries cold shutdown with 3.8× margin on concentration."* |
| 32 | `self protecting` → `self-protecting` |
| 32 | `78 kg Pu` → **78.1 kg** (slide 18 says 78.1) |
| 35 | `$75/MWh` → `$74.8/MWh` to match slide 34 |
| 20, 14 | `F q`, `FQ` → `F_q` consistently |
| 38 | the team-ID block appears **twice** on this slide — delete one |

## M3 · Slide 5 — check the name↔role pairing visually

The extracted text shows six names but the roles read as a separate group, and **Samira has no role
adjacent to her name**. Also present are literal `&#11;` control characters inside three role labels
(`Safety & ⁠Auxiliary systems`, `Neutronics & ⁠NPP layout`, `Cogeneration &⁠Secondary cycle`) — these may
render as boxes or bad spacing.

**Open the slide and confirm each name sits above its own role**, and retype those three labels.

## M4 · Slide 13 — enrichment zoning is incomplete

Slide says **4.95 / 4.70 / 4.40 wt%**. The frozen basis is **4.95 / 4.70 / 4.40 / 4.00** with edge pins
de-rated to 4.00, core average **~4.43 wt%**. Slide 18 quotes the 4.43 average — which does not follow
from three values. **Add the 4.00 edge-pin value.**

Also consider adding the absorber rod counts (**20 Gd + 16 Er per assembly**); "6 wt% Gd₂O₃" without a
count is not a loading.

## M5 · Waste intensity now appears twice, back to back

Slide 17 leads with **4.40 tHM/TWhe, −32 %**; slide 18 has a **WASTE INTENSITY 4.40 tHM/TWhe · 32 %
below CAREM-25** tile. They were 15 slides apart before the reorder and are now adjacent.

**Drop the tile from slide 18** — Fuel Cycle already carries four tiles — and keep it on 17 where it is
the headline.

## M6 · Appendix letters — verify they exist

The deck cites **Appendix A** (slide 36, "input decks… indexed in Appendix A"), **Appendix C** (slide 37,
"listed in Appendix C") and **Appendix D** (slide 16, shielding figure). Confirm all three exist in the
digital appendix with those letters, or change the labels to match what was submitted.

---

# STILL OUTSTANDING from the earlier checklist

## S1 · Economics slide (34) — Part D was never applied ⭐

The nine table cells are **correct** (they match FER Table 8.12-6 exactly). Leave the table alone.
Change the tiles and the result line — full instructions in `13_SLIDES-MANUAL-EDIT-CHECKLIST` **Part D**:

- tile 1 → **`ELECTRICITY — OUR RANGE` / `$75–125` / `per MWh, 7 % real · NOAK → high capital`**
- tile 4 → **`BENCHMARK — AKKUYU` / `$123.5` / `per MWh, Turkey's contracted nuclear price`**
  *(the $18.3 fuel term moves into a new basis line — it is a component of $74.8, not a fourth product)*
- result line → capital dominance, cogeneration credit **$64.8/MWh**
- add the **BASIS** and **WHERE THE UNCERTAINTY SITS** blocks in the empty band

The current result line quotes **$57–193/MWh**, a range whose top comes from a fourth ($10,000/kWe) row
the slide never shows. Either show the row or move the range into the basis block.

## S2 · Slide 37 — open item never added

Add to "What remains detailed-design work":

> Definition of in-service inspection intervals and in-vessel component maintainability across the
> six-year cycle.

## S3 · Footprint and RPV weight never added

Slide 11 or 33: **plant footprint ≈ 31,600 m² (3.2 ha)** and **RPV weight ≈ 270 t** with internals and
fuel. Phrase as *"we calculate approximately…"* — these are engineering estimates, not FER values.

## S4 · Four empty BACKUP slides (39–42)

All blank, all footer 35. **Fill or delete.** Best candidates, in order: the LCOE sensitivity chart, the
CDF event tree, the BOC/MOC/EOC peaking maps, and the OTSG temperature-profile diagram (see S5).

## S5 · Consider a backup slide for the OTSG pinch

The evaporator pinch works out at **8.4 K**, requiring roughly **1,850 m²** of surface. That is tight
but affordable, and comparable to NuScale per unit power. It is the first thing a thermal engineer will
compute, and having the answer ready as a backup slide is much stronger than deriving it live.

## S6 · Figure check that still needs eyes on it

The **site-layout figure** (slide 23) was reported to read **"seismic gap ≥ 75 m"**. The FER says
**≥ 75 mm** — a factor of 1000. Open the image and confirm.

## S7 · Slide 43 — decide what I&C Architecture is

It sits after the four BACKUP slides *and* after the References / Teşekkürler closing slide, but it
still carries a figure caption and a body. **Either** move it above the closing slide into Azamkhon's
run, **or** label it explicitly as backup. As it stands it reads as stranded.

---

# What checked out correctly

Recorded so nobody "fixes" a number that is already right:

| Checked | Result |
|---|---|
| Equivalent core diameter 1483 mm | 37 FA × 21.6038 cm pitch → 148.3 cm ✓ |
| ~16 M active histories | (400 − 80 inactive) × 50,000 ✓ |
| Discharge burnup 29.6 GWd/tHM | 125 MWth × 2224 EFPD ÷ 9.39 tHM ✓ |
| Peak LHR 12.4 kW/m | 6.4 kW/m average × F_q 1.937 ✓ |
| COLR LHR 15.8 kW/m | 6.4 × 2.4675 ✓ |
| Condenser duty 82.6 MWth | DWSIM: 38.44 kg/s × 2147.6 kJ/kg ✓ |
| Primary inventory 26 t / 35 m³ | → 743 kg/m³, correct at 12.8 MPa / 283 °C ✓ |
| RPV hoop 142 MPa, von Mises 135 MPa | Lamé + von Mises at inner surface, 14.1 MPa ✓ |
| Sₘ ≈ 184 MPa | SA-508 Gr.3 Cl.1 at ~350 °C ✓ |
| Waste intensity 4.40 tHM/TWhe | 1000/(29.608 × 24 × 0.320) ✓ |
| MTC/DTC/void, bank worth, SDM, k_adj, β_eff | all match the frozen basis ✓ |
| ICSBEP bias −50 pcm | correct (the +20 pcm version was an error, since reverted) ✓ |
| LCOE table, all nine cells | match FER Table 8.12-6 exactly ✓ |
| Pu 78.1 kg at 61.6 % Pu-239 | matches the authoritative FER ✓ |

---

# Suggested order of work

1. **B1, B3, B4, B5, B6** — five text edits, each one a factual error. Half an hour.
2. **B2** — the reference list. This is the biggest single credibility item and needs someone to sit
   down with the deck and resolve every bracket.
3. **M1** — the superscript sweep. Highly visible, purely mechanical.
4. **H1, H2** — page and figure numbers. Tedious; if time is short, delete the footer numbers rather
   than leave them wrong.
5. **H3–H9, M2–M6** — consistency pass.
6. **S1** — the economics slide.
7. **S2–S7** — additions and the backup slides.
