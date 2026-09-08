# Google Slides — Manual Edit Checklist

**For:** the team, working directly in Google Slides
**Deck:** 37 slides, `Final presentation.pptx` structure
**Date:** 23 August 2026

> ⚠️ **Read this first.** Corrections in **Part A** were applied to the `.pptx` file on 22–23 August. If your Google Slides copy was not re-imported from that file, **Slides still has the old wrong numbers** and every Part A item must be done by hand. Check slide 26 — if it reads `15,672`, none of Part A is in Slides.

---

## PART A — Corrections (must be in Slides, or the deck states wrong physics)

These are not preferences. Each one is a number that is factually superseded.

### A1 · Slide 14 — Core Design, Cycle Results

| Find | Replace with |
|---|---|
| `15,672 pcm` | **`21,509 pcm`** |
| `~2.0 % Δk/k` | **`7.85 % Δk/k`** |

The row is labelled "16-CRA bank worth" but carried the **12-CRA** value.

### A2 · Slide 21 — Safety Criteria & Plant States

| Find | Replace with |
|---|---|
| `Gravity rod drop, 15,672 pcm bank worth` | **`Gravity rod drop, 21,509 pcm bank worth`** |
| `k adj 0.845 cold` | **`k_adj 0.790 cold`** |

### A3 · Slide 25 — Design-Basis Event Matrix

| Find | Replace with |
|---|---|
| `Per-initiator core-damage frequency ~1 × 10⁻⁷/ry` | **`~1 × 10⁻⁸/ry`** |
| `kadj 0.845 cold` | **`k_adj 0.790 cold`** |

The 10⁻⁷ contradicted the event-tree slide, which says 10⁻⁸.

### A4 · Slide 26 — Shutdown Architecture & Reactivity Limits

Four of the four stat tiles were wrong:

| Tile | Find | Replace with |
|---|---|---|
| Bank worth, 16 CRAs | `15,672` | **`21,509`** |
| Hot shutdown margin | `~2.0 %` | **`7.85 %`** |
| — sub-label | `k = 0.980` | **`k = 0.927`** |
| BOC excess reactivity | `~13,300` | **`~13,100`** |
| Cold subcritical, injection | `0.845` | **`0.790`** |

### A5 · Slide 30 — Radiation Shielding

| Find | Replace with |
|---|---|
| `3.35 × 10¹⁸` | **`3.02 × 10¹⁸`** |

This was *wrong*, not merely missing — the appendix gives 3.02 × 10¹⁸.

### A6 · Slide 15 — Fuel & Material Design *(addition)*

Add below the table:

> **Cladding temperature:** peak cladding temperature is 353 °C in normal operation, against the 1204 °C LOCA acceptance limit — the same low linear heat rate that holds the centreline at 828 °C keeps the cladding more than 850 °C clear of its limit.

PCT was absent from the entire deck.

### A7 · Slide 26 — GDC-28 band *(addition)*

The slide is titled "…& Reactivity Limits" but carried none. Add below the "Result:" line:

> **3 · Reactivity limits (GDC-28)** — β_eff computed for this core at 704.5 ± 28 pcm. The highest-worth ejected cluster is 844–902 pcm = 1.20–1.28 $, above prompt critical — a configuration reachable only because the in-vessel drives eliminate the ejection path. **Cold subcriticality needs 785 ppm against the 3,000 ppm credited: a 3.8× margin on the injection system.**

### A8 · Slide 24 — Passive Safety Systems *(figure)*

The slide had a **`FIGURE SLOT`** placeholder and an empty left-hand panel. The figure exists:
`D:\projects\Final pptx\charts\fig11_passive_esf_pool.png`
Insert it in the left panel and delete the placeholder text.

### A9 · Figure captions — renumber

Captions started at **Fig. 2**; there was no Fig. 1. Renumber sequentially by slide order:

| Slide | Caption number |
|---|---|
| 12 | Fig. 1 |
| 13 | Fig. 2 |
| 14 | Fig. 3 |
| 17 | Fig. 4 |
| 18 | Fig. 5 |
| 19 | Fig. 6 |
| 20 | Fig. 7 |
| 22 | Fig. 8 |
| 23 | Fig. 9 |
| 24 | Fig. 10 |
| 27 | Fig. 11 |
| 28 | Fig. 12 |
| 30 | Fig. 13 |
| 31 | Fig. 14 |
| 32 | Fig. 15 |

---

## PART B — New, from the IAEA booklet research

### B1 · Slide 6 — Literature Review · **add a NUWARD row** ⭐ *highest value*

There are **three** boron-free designs in the IAEA booklet, not two. Omitting the third looks like avoidance.

| Design | Power | Circulation | Boron | Cycle | Cogeneration |
|---|---|---|---|---|---|
| **NUWARD** *(add)* | 2 × 170 MWe | **Forced** | **Boron-free in all DBC** | 24 mo, half core | Flexible operation |

**Your claim still holds** — nobody combines boron-free + natural circulation + a six-year single-batch cycle. But be ready for: *"NUWARD is boron-free in all design-basis conditions; you need boron for cold shutdown — isn't theirs stronger?"* Answer is in `12_SMR-COMPARISON` §3.

### B2 · Slide 16 — Fuel Cycle Strategy · **reframe the burnup reason** ⭐

Currently the low burnup reads as a margin choice. The sharper, more defensible reason is the **boron coupling**:

> Why once-through: **the low burnup is the price of being boron-free, not of the long cycle.** VBER-300 runs the same six-year cycle at the same 4.95 % enrichment and reaches 50 GWd/tHM — but it uses soluble boron to hold the excess reactivity. Without boron the whole cycle must be held on burnable absorbers and rods, which is only feasible at low specific power.

This is stronger because it names the physical mechanism and cites a design that proves the alternative exists.

### B3 · Slide 34 — Reference Comparison · **add a power-density row**

| Dimension | Aegis-40 | NuScale | CAREM-25 | SMART | ACP100 |
|---|---|---|---|---|---|
| Thermal power per assembly | **3.38 MWth/FA** | 6.76 | 1.64 | 6.40 | 6.75 |

We are the **second-least power-dense design in the field**. This substantiates "margin over burnup" with an external reference instead of an assertion.

**Optional but strong:** note that NuScale has the **same 37 × 17×17 core** and runs it at **exactly twice our power**. One sentence that explains the whole design.

### B4 · Slide 11 or 12 — **add the two computed values**

Both were missing and are now calculated:

| Parameter | Value |
|---|---|
| Plant footprint | **≈ 31 600 m² (3.2 ha)** — governed by the 123 m hydrogen stand-off, not by the buildings |
| RPV weight | **≈ 270 t** with internals and fuel (215 t dry) |

Say *"we calculate approximately…"* — these are engineering estimates, not FER values.

### B5 · Slide 36 — Design Summary & Open Items · **add one open item**

Add to "What remains detailed-design work":

> Definition of in-service inspection intervals and in-vessel component maintainability across the six-year cycle.

**Why:** the six-year cycle means the OTSG tubes are examined every 6 years instead of every 1.5–2. Naming it is stronger than being asked. (Design life stays at **60 years** — the 60-year fluence is 3.02 × 10¹⁸ against a 1 × 10¹⁹ limit, a 3.3× margin, and long cycles *reduce* thermal fatigue.)

---

## PART C — One error to fix in a figure

### C1 · Site layout figure — `75 m` → `75 mm`

The FER states a seismic gap of **≥ 75 mm** between Category I and II structures. The site-layout figure appears to read **"seismic gap ≥ 75 m"** — a factor of 1000. Seventy-five metres between the reactor and turbine buildings is clearly not what the layout shows.

---

## PART D — Slide 33 Economic Evaluation, **rewritten 23 Aug** ⭐ *do this one*

Applied to `Final presentation.pptx` on 23 August (backup: `Final presentation.BACKUP-2026-08-23-econ.pptx`).
**If Google Slides was not re-imported, do it by hand.** Geometry is unchanged — every edit below is a
text replacement plus two new text boxes.

### Why the slide had to change

1. **It led with the best case.** `$74.8` is the *most optimistic* of four capital scenarios, shown as
   the headline. A juror who reads the table underneath sees $165 and concludes the headline was
   cherry-picked. Leading with the range removes that entirely.
2. **Tile 4 was a component of tile 1.** "FUEL CYCLE $18.3 per MWh" sat next to "$74.8 per MWh" at the
   same visual weight — but $18.3 is *inside* $74.8. It read like a fourth product.
3. **No external benchmark anywhere.** Four numbers with nothing to judge them against.
4. **The result line quoted a range not visible in the table.** It is genuine — it comes from the FER's
   *four*-row Table 8.12-6, which includes a $10,000/kWe case the slide never showed. The range now
   lives in the new uncertainty block (D5), where it has a home.


### D1 · Tile 1 — lead with the range

| | Old | New |
|---|---|---|
| Label | `ELECTRICITY, NTH-OF-A-KIND` | **`ELECTRICITY — OUR RANGE`** *(18 → 16 pt)* |
| Value | `$74.8` | **`$75–125`** |
| Sub | `per MWh at 7 %, $3,500/kWe` | **`per MWh, 7 % real · NOAK → high capital`** |

### D2 · Tile 4 — replace the fuel-cycle component with the benchmark ⭐ *highest value on the slide*

| | Old | New |
|---|---|---|
| Label | `FUEL CYCLE` | **`BENCHMARK — AKKUYU`** *(18 → 16 pt)* |
| Value | `$18.3` | **`$123.5`** |
| Sub | `per MWh, the design-anchored term` | **`per MWh, Turkey's contracted nuclear price`** |

Turkey has a contracted PPA at 12.35 ¢/kWh for Akkuyu. It is Turkish, checkable, and it makes our whole
range readable at a glance. The $18.3 fuel term moves into the new BASIS block (D5).

### D3 · Tile 2 sub-label

`per MWh-th, versus $50 price` → **`per MWh-th, versus $50 market price`**

### D4 · Table — five cells were wrong

Correct against `digital-appendix/7_energy_cycle/outputs/lcoe_sensitivity.csv`:

**The nine table cells are unchanged — the originals were right.** They match FER Table 8.12-6
(`Aegis40_FER_submission_ready_compact_final.docx`, 15 Jul) exactly: 55.5 / 74.8 / 92.1 ·
63.1 / 90.6 / 115.2 · 79.5 / 124.7 / 165.2. Two intermediate edits on 23 Aug moved them to the digital
appendix CSV and then to a superseded 7 Jul FER; both were reverted. **Leave the table alone.**

### D5 · Two new text blocks in the empty band

There was ~1.6 in of dead space between the result line and the footer. Two blocks, side by side,
15 pt Arial, heading in `#1B3D70` bold and body in `#52514E`:

**Left (x 0.82 in, y 8.62, w 8.9)** — heading `BASIS`:
> 40 MWe net · 90 % capacity factor · 60-year life · 4-year build · 7 % real discount · decommissioning
> fund included · 2024 USD. Fuel is $18.3/MWh of the total, 24 % — front end $17.3 plus ~$1 back-end,
> the price of a once-through, boron-free core.

**Right (x 10.19 in, y 8.62, w 8.99)** — heading `WHERE THE UNCERTAINTY SITS`:
> Overnight capital swings LCOE by $50/MWh; a fourth case at $10,000/kWe reaches $143, and the full
> 3–10 % discount spread is $56–192. The next-largest lever, fuel cycle at ±30 %, moves it $11/MWh.
> Competitiveness is a financing and serial-build question.

### D6 · Result line

Replace with:
> **Result: capital sets the answer, not reactor physics — $3,500→$8,250/kWe moves LCOE by $50/MWh,
> more than fuel, O&M, capacity factor and build time combined. Cogeneration adds ~12 % of revenue,
> crediting electricity down to $64.8/MWh.** *(19.5 → 17 pt to fit)*

### D7 · Turkish özet line

> **Özet — 75–125 $/MWh aralığımız, Akkuyu'nun sözleşmeli 123,5 $/MWh fiyatını kapsıyor.
> Belirleyici olan sermaye maliyeti, reaktör fiziği değil.**

---

## PART F — The FER is BEHIND the deck on safety neutronics *(no slide change — Q&A prep)*

**New finding, 23 Aug.** The authoritative FER —
`docs/Aegis40_FER_submission_ready_compact_final.docx`, **15 Jul** — still carries the **12-CRA**
values. `02_FER-DOCX-EDITS.md` §A has listed the replacements since **14 Aug with every box
unchecked**, and the document confirms they were never applied.

| FER (15 Jul) | Correct | Slides |
|---|---|---|
| rod worth **15,672 pcm** | 21,509 pcm | ✅ Part A |
| hot SDM **~2.0 %** | 7.85 % | ✅ Part A |
| k_ARI **0.980** | 0.927 | ✅ Part A |
| k_adj cold **0.845** | 0.790 | ✅ Part A |
| vessel fluence **3.35 × 10¹⁸** | 3.02 × 10¹⁸ | ✅ Part A |

So Part A of this checklist did **not** make the slides disagree with the FER by accident — it moved
them ahead of it deliberately. A juror reading the report sees 15,672 pcm and 2.0 % shutdown margin.

**Rehearse this. It is an upgrade, so lead with it:**
> "The report carries the 12-rod configuration. We finalised at 16 control-rod assemblies, which raises
> bank worth to 21,509 pcm and hot shutdown margin to 7.85 % — about four times the acceptance
> criterion. The digital appendix carries the final run."

Also open from §C: FER **Table 8.12-2 reads $65.9/MWh** cogeneration-credited while §8.12.3 prose reads
**$64.8**. Applied to the prose, missed in the table.

**On economics and waste there is no mismatch at all** — slides and FER agree exactly.
See `docs/competition/WHICH-FER-IS-AUTHORITATIVE.md`.

---

## Priority order if time is short

1. **A1–A5** — wrong numbers. Non-negotiable.
1b. **PART D** — the economics slide rewrite. Same class of problem: numbers that don't match the appendix, plus a headline that reads as cherry-picked.
2. **A6, A7** — missing PCT and the entire GDC-28 content on a slide titled "Reactivity Limits".
3. **B1** — the NUWARD row.
4. **A8, A9** — the missing figure and caption numbering.
5. **B2** — the burnup reframe.
6. **B5, C1** — open item and the figure error.
7. **B3, B4** — nice to have.

## Verification when done

Search the whole deck for these strings. **Every one should return zero hits:**

`15,672` · `~2.0 %` · `0.845` · `0.980` · `3.35 ×` · `10⁻⁷/ry` · `FIGURE SLOT` · `FUEL CYCLE`

And these should each appear at least once:

`21,509` · `7.85 %` · `0.790` · `785 ppm` · `704.5` · `353 °C` · `3.02 ×` · `$123.5` · `$75–125` · `124.7`
