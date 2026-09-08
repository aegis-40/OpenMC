# Main Presentation — Rebuild Specification

**Deck:** jury defence, 30 minutes, six speakers · 16:9 (13.333 × 7.5 in)
**Status of the current file:** 40 slides, `Aegis40-draft-new.pptx`
**This document:** what to keep, what to cut, what is missing, and how every slide should be laid out.

---

## PART 1 — Gap analysis

### 1.1 FER content that has no slide at all

Checked mechanically against the FER's section structure. Nine areas are absent, and **three of them are numbered FER template sections** — the jury scores against that template, so a missing section is a missing mark, not just a missing slide.

| FER section | Status | Severity |
|---|---|---|
| **§3 Literature Review** | ✗ absent | **critical** — numbered template section |
| **§6 Project Work Plan** | ✗ absent | **critical** — numbered template section |
| **§7 Broader Impacts & Target Audience** | ✗ absent | **critical** — numbered template section |
| §8.5.2c Coastal external hazards (Sinop) | ✗ absent | high — a coastal site with no hazard slide invites the question |
| §8.5.3 Defence in depth | ✗ absent | high — the organising principle of the whole safety case |
| §8.6.6 Reactivity control limits (GDC-28) | ✗ absent | medium |
| §8.8.9 Cogeneration interface isolation | ✗ absent | high — "is the hydrogen radioactive?" is a certain question |
| §8.10.6 Critical piping arrangement | ✗ absent | low |
| §8.6.7 Fault-tree analysis | only a passing mention (slide 6) | medium |

### 1.2 What is over-represented and should be cut or merged

| Current | Problem | Action |
|---|---|---|
| Slides 12 + 13, both titled "Core Design" | Duplicate titles | Retitle: *Configuration* / *Cycle Results* |
| Slides 21 + 22, both "Reactor Safety Systems" | Duplicate titles | Retitle 22 → *Design-Basis Event Matrix* |
| Slide 23 MSLB re-analysis | Deep single-transient detail | → **backup** |
| Slides 26 + 27 twin + dashboard | Two slides for a non-credited advisory tool | Merge to **one** |
| Slides 33 + 34 economics | Two slides; reviewer capped economics at 2–3 min | Merge to one, tornado → backup |
| Slides 18 + 19 thermal | Overlapping | Merge to one *Thermal Margins* |
| Slides 28 + 31 aux / three islands | Overlapping content | Merge |
| Slide 4 Turkish summary | Belongs to the protocol deck | Remove from jury deck |

**Net effect:** −9 slides from merges and cuts, +6 from the missing FER sections.

---

## PART 2 — Target structure

**30 main slides + 10 backup.** Average 55 s per main slide, weighted so safety and core get more and dividers get less.

### Block A — Frame (§1–§7) · 8 slides · 5:30

| # | Slide | FER | Time | Speaker |
|---|---|---|---|---|
| 1 | Title | — | 0:15 | Samira |
| 2 | Outline | — | 0:20 | Samira |
| 3 | Project Summary | §1 | 1:15 | Samira |
| 4 | Team & Work Plan | §2, **§6** | 0:40 | Samira |
| 5 | **Literature Review & Positioning** | **§3** | 1:00 | Samira |
| 6 | Method & Feasibility | §4 | 0:50 | Samira |
| 7 | Originality, Domesticity & Broader Impact | §5, **§7** | 1:00 | Samira |
| 8 | Design Philosophy — Elimination before Mitigation | §8.6.1 | 0:50 | Samira |

### Block B — Plant & core (§8.1–8.3) · 7 slides · 6:30

| # | Slide | FER | Time |
|---|---|---|---|
| 9 | Divider — Detailed Design | — | 0:10 |
| 10 | Plant Design Parameters | §8.1.1–8.1.4 | 1:00 |
| 11 | Reactor Vessel & Mechanical Basis | §8.1.9, §8.3.6 | 0:55 |
| 12 | Core Design — Configuration | §8.2.2 | 1:20 |
| 13 | Core Design — Cycle Results | §8.2.3 | 1:30 |
| 14 | Fuel & Material Design | §8.3 | 1:00 |
| 15 | Fuel Cycle Strategy | §8.2.5, §8.11.1 | 0:55 |

### Block C — Cooling & energy (§8.4, §8.9) · 4 slides · 3:40

| # | Slide | FER | Time |
|---|---|---|---|
| 16 | Cooling Circuit — Natural Circulation | §8.4.1–8.4.2 | 1:05 |
| 17 | Thermal Margins *(merged)* | §8.4.4–8.4.5 | 1:15 |
| 18 | Energy Conversion & Cogeneration | §8.9 | 0:50 |
| 19 | **Cogeneration Isolation — no path to the user** | **§8.8.9** | 0:30 |

### Block D — Safety (§8.5–8.6) · 6 slides · 6:30 · **largest block**

| # | Slide | FER | Time |
|---|---|---|---|
| 20 | Safety Criteria & Plant States | §8.5.1–8.5.2 | 1:00 |
| 21 | **Site Hazards — Sinop** | **§8.5.2c** | 0:50 |
| 22 | **Defence in Depth — five levels** | **§8.5.3** | 1:00 |
| 23 | Passive Safety Systems | §8.6.2 | 1:10 |
| 24 | Design-Basis Event Matrix | §8.5.2b, §8.6.5 | 1:20 |
| 25 | Shutdown Architecture & Reactivity Limits | §8.6.2a, **§8.6.6** | 1:10 |

### Block E — I&C, plant systems (§8.7–8.11) · 6 slides · 5:20

| # | Slide | FER | Time |
|---|---|---|---|
| 26 | I&C Architecture | §8.7.1–8.7.4 | 1:10 |
| 27 | Advisory Digital Twin *(merged)* | §8.7.6 | 0:50 |
| 28 | Auxiliary Systems & Radiation Protection *(merged)* | §8.8 | 1:00 |
| 29 | Radiation Shielding | App D | 0:50 |
| 30 | Facility Layout & Scalability | §8.10 | 0:50 |
| 31 | Waste Management | §8.11 | 0:40 |

### Block F — Economics & close · 5 slides · 3:30

| # | Slide | FER | Time |
|---|---|---|---|
| 32 | Economic Evaluation *(merged)* | §8.12 | 1:15 |
| 33 | Reference Reactor Comparison | §8.12.4 | 0:45 |
| 34 | Verification, Validation & Reproducibility | App A | 0:50 |
| 35 | Design Summary & Open Items | App C | 1:00 |
| 36 | References · Glossary · Teşekkürler | — | 0:20 |

**Total ≈ 31:00** → trim the marked cut-candidates in §2.1 below to land at 28:30, leaving buffer.

### Backup (after the closing slide, never presented unless asked)

MSLB re-analysis · Advisory dashboard screenshot · LCOE tornado · Fault trees · Codes & standards table · Critical piping arrangement (§8.10.6) · Multi-batch comparison · Shielding dose map · Twin parity plots · Glossary EN–TR.

---

## PART 3 — Content spec for the six new/rebuilt slides

### Slide 5 — Literature Review & Positioning *(new, §3)*

**Layout:** archetype **D** (comparison table).
Table, 6 columns × 5 rows: *Design · Power · Coolant circulation · Boron · Cycle · Cogeneration*.
Rows: **NuScale · CAREM-25 · SMART · ACP100 · Aegis-40** (highlighted row, orange left edge).

Bottom band, one line: *"Our gap: no operating or announced iPWR combines soluble-boron-free operation, natural circulation and a six-year single-batch cycle. That is the space Aegis-40 occupies."*

**Why it matters:** this is the slide that proves you know the field. Without it, a juror assumes you designed in a vacuum.

### Slide 21 — Site Hazards, Sinop *(new, §8.5.2c)*

**Layout:** archetype **C** (figure left, content right). Map or coastline schematic left.
Right: four rows — *Seismic · Tsunami / coastal flooding · Extreme wind & temperature · External human-induced*.
Each row: the hazard, the design basis value, and the response.

Anchor number: **0.3 g SSE**, RPV below grade, seismic gaps between Category I and II.

### Slide 22 — Defence in Depth *(new, §8.5.3)*

**Layout:** archetype **F** (full-width diagram). Five stacked horizontal bands, same visual language as the Design Philosophy ladder so the two read as a pair.

Levels 1→5: *prevention of abnormal operation · control of abnormal operation · control of design-basis accidents · control of severe conditions · off-site emergency response*. Each band names the Aegis-40 feature that delivers it.

### Slide 19 — Cogeneration Isolation *(new, §8.8.9)*

**Layout:** archetype **F**, one horizontal barrier diagram.
Reactor → **[barrier 1: OTSG tube wall]** → steam → **[barrier 2: intermediate heat exchanger]** → **[barrier 3: monitored non-radioactive loop]** → district heat / hydrogen.

One line beneath: *"Three physical barriers and continuous radiation monitoring between the core and any product delivered to a user."*

**Why it matters:** "could the hydrogen or the district heat be contaminated?" is close to a certain question, and the answer is strong. Do not leave it to Q&A.

### Slide 4 — Team & Work Plan *(rebuilt, §2 + §6)*

Keep the six-person photo band across the top half. Add a **compact work-plan strip** across the bottom: WP1…WP6 as a horizontal timeline with month markers. Small, one row, ~1.2 in tall.

### Slide 7 — Originality, Domesticity & Broader Impact *(rebuilt, §5 + §7)*

Keep the five numbered originality cards. Replace the single domesticity band at the bottom with **two half-width bands**: *Domesticity* (left) and *Broader impact / target audience* (right — grid operator, industrial heat user, hydrogen offtake, academia).

---

## PART 4 — Design and layout specification

### 4.1 Canvas and grid

Slide **13.333 × 7.5 in**. Everything sits on a 12-column grid.

| Zone | Vertical extent | Notes |
|---|---|---|
| Title | 0.09 – 0.88 in | Left edge at 2.92 in when the corner mark is present, else 0.55 in |
| Rule | 0.94 in | 12.38 in wide hairline, `#c3c2b7` |
| **Content** | **1.20 – 6.45 in** | All body content lives here. Nothing may cross 6.5 in. |
| Footer | 6.70 – 7.30 in | Branding band + page number, right at 13.06 in |

**Margins:** left 0.55 in, right 0.55 in → usable width **12.23 in**.
**Column width:** 0.94 in, gutter 0.18 in.
Common spans: half = 6.02 in · third = 3.94 in · quarter = 2.90 in.

### 4.2 Typography

| Role | Size | Weight | Colour |
|---|---|---|---|
| Slide title | 28 pt | Bold | `#1b3d70` |
| Section divider title | 40 pt | Bold | white on navy |
| Body / bullet | 12–13 pt | Regular | `#16243b` |
| Table header | 11 pt | Bold | white on `#1b3d70` |
| Table cell | 10.5 pt | Regular | `#16243b` |
| Stat tile number | 26–30 pt | Bold | `#1b3d70` |
| Stat tile label | 8.5 pt | Bold, letterspaced, UPPERCASE | `#52514e` |
| Figure caption | 9.5 pt | Regular | `#52514e` |
| Footnote | 8.5 pt | Italic | `#52514e` |

One typeface throughout. **Never below 8.5 pt** — the Block I legibility complaint came from figures with embedded 6 pt labels.

### 4.3 Palette

| Token | Hex | Use |
|---|---|---|
| Navy | `#1b3d70` | Primary — titles, headers, key numbers |
| Green | `#12905a` | PASS, safety-credited, positive deltas |
| Orange | `#e0801e` | Emphasis, actuation, "look here" |
| Red | `#d1451f` | Limits, criticality lines, failure states |
| Ink | `#16243b` | Body text |
| Grey | `#52514e` | Secondary text, captions |
| Rule | `#c3c2b7` | Hairlines, table borders |
| Row tint | `#f5f8fc` | Alternating table rows |

Semantic colour is **separate from accent colour**: green/red always mean pass/fail, never decoration.

### 4.4 Slide archetypes

Build every slide from one of these seven. Consistency is what makes a deck look designed.

**A — Title.** Full-bleed or half-bleed hero image. Team name, IDs, competition line.

**B — Section divider.** Solid navy. Large white title, one grey subtitle line naming the FER sections covered. 0:10 only.

**C — Figure left / content right.** *Default archetype.* Figure 0.55–7.0 in wide (max 5.0 in tall), content column 7.3–12.8 in. Caption directly under the figure at 9.5 pt.

**D — Full-width table.** Table from 0.55 to 12.8 in, starting at 1.35 in. Header row navy/white, alternating row tint, ≤7 data rows. If more are needed, the slide is doing too much.

**E — Stat tiles + supporting content.** A row of 3–4 tiles (each 2.87 × 1.72 in, 0.25 in gap) across the top of the content zone, detail beneath. Use for parameter slides.

**F — Full-width diagram.** Diagram spans 0.42–12.85 in. Caption and one bold "Result:" line beneath. Use for architecture, ladders, barrier chains.

**G — Closing.** Centred, minimal.

### 4.5 Rules that apply to every slide

- **One archetype per slide.** Do not blend C and E.
- **Maximum four bullet lines**, each ≤ 2 printed lines.
- **Every figure gets a caption**, numbered `Fig. N.` sequentially by slide order, with no duplicates.
- **Every number that appears on a slide must exist in the FER** with the same value. This is what the 21,509 / 7.85 % episode cost two days.
- **No slide title may repeat.** Duplicate titles read as disorganisation to a jury.
- **Units always spaced:** `125 MWth`, `7.85 %`, `29.6 GWd/tHM`.
- **Citations** as `[n]` at the end of the line, matching the References slide.
- **Contrast:** never place `#52514e` text on `#f5f8fc` below 10 pt.

### 4.6 Figure standards

- Export at **200 dpi minimum**; native size ≥ 1600 px wide.
- Smallest text inside a figure ≥ **10 pt equivalent at final placed size**. Check by placing, then reading from 2 m.
- Use the deck palette inside figures — matplotlib defaults break the visual system.
- Wide figures scroll nothing: crop to the region with data. (The shielding map needed this.)
- **One figure per slide.** Two figures means two slides or a merged composite built as a single image.

---

## PART 5 — Build order

1. **Fix the structure first** — merges and cuts from §1.2. This alone removes 9 slides and all duplicate titles.
2. **Build the six new/rebuilt slides** from Part 3. These are the scored gaps.
3. **Apply archetypes** — reassign every existing slide to one of A–G and fix the ones that don't conform.
4. **Regenerate non-conforming figures** at the Part 4.6 standard.
5. **Renumber** figures and page numbers last, after all inserts and deletions.
6. **Timed rehearsal** against the Part 2 budget; move the cut-candidates to backup until it lands at 28:30.

### Cut candidates, in the order to drop them if you run long

1. Slide 33 Reference Comparison (0:45) — the content is implicit in the economics slide
2. Slide 31 Waste (0:40) → shorten to 0:20, keep only the two headline numbers
3. Slide 15 Fuel Cycle Strategy (0:55) → fold the "why once-through" reasons into slide 14
4. Slide 11 Reactor Vessel (0:55) → fold the drawing into slide 10

Never cut: **12, 13, 22, 24, 25, 35** — core physics, defence in depth, the event matrix, shutdown architecture, and the closing argument.

---

## PART 6 — Verification checklist before it is final

- [ ] All three missing FER template sections (§3, §6, §7) have a slide
- [ ] §8.5.2c, §8.5.3, §8.8.9 have slides
- [ ] No duplicate slide titles
- [ ] No duplicate figure numbers; captions sequential by slide order
- [ ] Every slide maps to exactly one archetype
- [ ] Every number cross-checked against the FER — especially bank worth **21,509 pcm** and hot SDM **7.85 %** (HZP basis, see `07_DATA-AUDIT`)
- [ ] No figure contains text below 10 pt at placed size
- [ ] Page numbers match slide positions
- [ ] Backup section present and clearly separated
- [ ] Timed run ≤ 28:30
- [ ] Exported to PDF as venue fallback
