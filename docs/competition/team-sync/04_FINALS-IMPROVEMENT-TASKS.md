# Aegis-40 — Finals Improvement Tasks (team assignment)

**To the team.** With the days we have before the finals presentation, extra effort should go where it
buys the most **jury points**: clear visuals and anything that turns a *stated* claim into a *shown*,
quantitative one. Below are concrete tasks with an owner, the recommended tool, rough effort, and a
"done =" test. Pick from the 🥇 tier first. Convert "by finals" to the real date when you claim a task.

Grading reality (from Mahmut's advice + the rubric): **figures win**, §8.2–8.6 are weighted most, and
"never leave a heading looking thin." Everything here serves that.

---

## 🥇 Tier 1 — highest return, do these first

### T1. 3D reactor-building cutaway (cross-section)
A labelled cutaway showing the integral story: RPV below grade in the steel-lined pool, in-vessel OTSG +
pressurizer + CRDMs, IRWST suppression pool, containment, and the three islands. This is the single most
impressive "facility overview" visual and lands on **slides 10 (Facility) and 24 (Layout)**.
- **Owner:** Samira (Creo model already exists).
- **Tool:** Creo *section view* + built-in render for the fast path. For a **presentation-grade cutaway**,
  export the assembly as **STEP → Blender** (free) — Blender does the best-looking sectioned/exploded
  renders with labels and soft lighting. (KeyShot if anyone has a licence; FreeCAD as a free CAD fallback.)
- **Effort:** 0.5–1.5 day. **Done =** one clean labelled cutaway PNG at ≥1600 px, plus one exploded/island view.

### T2. Event trees + one bow-tie for the dominant sequences
Right now the safety story is strong in words but the numbers ("CDF < 1×10⁻⁷") aren't *shown*. Draw
**event trees** for the 2–3 dominant sequences — **SBLOCA, loss of heat sink, LOOP/station-blackout** —
and one **bow-tie** (threats → barriers → consequences) for the top event. This is the biggest upgrade
available to the safety score and directly answers "where does 10⁻⁷ come from?" in Q&A. Lands on
**slides 17–18**.
- **Owner:** WP5 / Safety (Azamkhon).
- **Tool:** for clean diagrams, **Excalidraw** or **Figma** (far nicer than draw.io for these). For *real*
  PRA logic if you want defensibility, **SAPHIRE** (NRC, free) or **OpenFTA** (free) — heavier, use only
  if time allows. **Graphviz** (scriptable) is a good middle path for auto-laid-out trees.
- **Effort:** 1–2 days. **Done =** 2–3 event-tree figures with branch probabilities + 1 bow-tie; the
  sequence frequencies on the figure match slide 18's numbers.

### T3. I&C 5-layer architecture diagram (§8.7) + digital-twin data-flow
Slide 19's five defence layers are text — make them a **layered block diagram** with the *upward-only*
signal flow and the **one-way data diode** drawn explicitly (RPS → ESFAS → DAS → control → advisory).
Add a small **digital-twin data-flow** figure (OpenMC → GP/POD surrogate → dashboard, diode marked) for
slide 20. Lands on **slides 19–20**.
- **Owner:** WP5 / I&C.
- **Tool:** **Excalidraw** (clean, fast, hand-drawn feel that reads well) or **Figma**; **Mermaid**
  (text-to-diagram, version-controllable) if you want it reproducible in the appendix.
- **Effort:** 0.5–1 day. **Done =** one I&C layer diagram + one twin data-flow diagram, diode shown.

### T4. Dashboard: demo-ready + a safety net
The advisory dashboard (slide 21) is a differentiator **if it runs live**. Make it presentation-ready and
record a fallback so a network hiccup can't sink the demo.
- **Owner:** digital-twin owner (Samira), with my support on data.
- **Tool:** **Streamlit** (current). Deploy to **Streamlit Community Cloud** (free) so it opens from a URL
  on any machine; **record a 30–60 s screen-capture GIF/MP4** as the offline backup. Refresh with the
  fresh 16-CRA sweep numbers once that run is back.
- **Effort:** 0.5–1 day. **Done =** dashboard opens from a URL + a recorded clip in the deck's backup folder.

---

## 🥈 Tier 2 — strong, do if Tier 1 is moving

### T5. Converged Monte-Carlo shielding dose map
Upgrade the shielding section from point-kernel *estimate* to a *calculated* MC dose map (two-stage MAGIC
weight windows). Turns slide 22's dose number into a defended one. **Needs the OpenMC machine** (pair it
with the friend's-PC run).
- **Owner:** WP2 / Neutronics (Laziz). **Tool:** OpenMC. **Effort:** compute-bound. **Done =** a converged
  dose-vs-radius plot + a 2D dose heatmap.

### T6. Multi-batch fuel-use estimate (once-through defence)
A short 2- or 3-batch shuffle estimate (even on paper) showing what utilization we *trade away* by choosing
once-through — pre-empts the obvious Q&A jab and shows we chose deliberately.
- **Owner:** WP2 / Neutronics. **Tool:** OpenMC or a hand calc. **Effort:** 0.5 day. **Done =** one table
  or bar comparing once-through vs 2/3-batch discharge burnup + utilization.

### T7. LCOE sensitivity tornado
A tornado chart (capex, capacity factor, discount rate) makes §8.12 a defensible *range*, not one number.
Data already exists (`7_energy_cycle/.../lcoe_sensitivity.csv`).
- **Owner:** WP6 / Economics. **Tool:** matplotlib/Python (I can generate it — just ask) or Google Sheets.
  **Effort:** 1–2 h. **Done =** one tornado chart for slide 26.

---

## 🥉 Tier 3 — nice-to-have, only with spare time

- **T8. SFCOMPO measured-depletion benchmark** — validate depletion against real assay data (needs OpenMC).
- **T9. PFD / cycle diagram polish** — redraw the cogeneration PFD cleaner (Excalidraw/Figma) if the
  current one looks dated on slide 23.
- **T10. Neutron-flux / power-map figure** — a radial power-map heatmap from OpenMC for slide 12/13.

---

## Tool cheat-sheet (answering "what besides draw.io?")

| Job | Recommended | Why / notes |
|---|---|---|
| Architecture & flow diagrams | **Excalidraw** (free), **Figma** | Cleaner and more modern than draw.io; Excalidraw is fastest |
| Reproducible/versioned diagrams | **Mermaid**, **PlantUML** | Text-to-diagram, lives in the appendix, diffs in git |
| Event / fault trees (diagram) | **Excalidraw / Figma**; **Graphviz** for auto-layout | Bow-ties read best hand-styled |
| Event / fault trees (real PRA) | **SAPHIRE** (NRC, free), **OpenFTA** | Only if you want quantified logic, not just a picture |
| 3D cutaway render | **Blender** (STEP import, free), Creo render, KeyShot | Blender = best-looking free sectioned renders |
| Technical 2D cross-sections | **Inkscape** / Illustrator over a CAD export | Vector, crisp at any zoom |
| Charts / plots | **Python (matplotlib/Plotly)**, Google Sheets | Keep the palette consistent with the 3 charts already made |
| Live dashboard | **Streamlit** (+ Community Cloud) | Already built; just deploy + record a backup clip |

## Suggested sequencing (parallel across the team)
- **CAD/Samira:** T1 cutaway → then support T4 dashboard data.
- **Safety/Azamkhon:** T2 event trees → T3 I&C diagrams.
- **Neutronics/Laziz:** T5 shielding MC (with the friend's-PC sweep) → T6 multi-batch.
- **Economics/WP6:** T7 tornado (quick win).
- **Whoever owns the deck:** drop the 3 finished charts (`Final pptx/charts/`) into slides 13/16/26, then
  the new diagrams as they land.

**Rule of thumb for all of it:** every new figure should either *show a mechanism* (cutaway, data-flow,
event tree) or *show a margin* (bar vs limit, sensitivity range). Decorative slides don't score.
