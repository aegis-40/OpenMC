# Aegis-40 iPWR — FER Preparation Checklist (deadline: 2026-07-10)

**Window:** 2026-06-02 → 2026-07-10 (~5.5 weeks). **Team:** 3–4 active members.
**Source of truth:** `2026_..._DETAILED_DESIGN_FER_T.docx` (template). FERs that don't follow the template **will not be evaluated**.

## Role legend
- **[NEU]** Neutronics / OpenMC (Samira) — §8.2, §8.3, §8.11 fuel-cycle, depletion
- **[TH]** Thermal-hydraulics / OpenFOAM — §8.4, §8.5 accidents, §8.6 capacities
- **[3S/IC]** 3S, I&C, Safety analysis, wFOM (Azamhon) — §8.5–§8.7, PRA, §5
- **[LAY]** Layout / Economics / Waste / Auxiliary (Elbek) — §8.8, §8.10, §8.11, §8.12
- **[ALL]** whole team / **[LEAD]** report owner-editor

---

## A. Report mechanics & compliance (do FIRST, enforce throughout) — [LEAD]
- [ ] Copy the official FER template `.docx` into the repo and write **only** inside it. Delete every instructional paragraph as you fill each section.
- [ ] Set styling: Arial 12 body / Arial Black 14 titles, line spacing 1.15, justified, 2.5 cm margins all sides.
- [ ] Reserve **3 separate pages** for Cover Page, Contents, References.
- [ ] Enforce **≤120 page** limit on body (cover/contents/references/appendix excluded).
- [ ] Fill cover fields: Team Name, Application ID, Team ID, Category (Detailed Design – 40 MWe Modular PWR), Team Type. Mark **one** box in each table.
- [ ] Set up auto-updating TOC, **List of Tables**, **List of Figures**, **Abbreviations** list.
- [ ] Citation discipline: every non-common-knowledge claim cited; reference format exactly per template (digital vs published source styles).
- [ ] Consecutive page numbering; **delete the "NOTES ON REPORT OUTLINE" page** before upload.
- [ ] No personal info anywhere (no names/photos/affiliations). Team contribution shown **schematically** only (§2).

## B. Digital Appendix (ZIP/RAR, uploaded separately) — [ALL]
> Required by §8 intro. This is a graded deliverable, not optional.
- [ ] One **sample input file per code** used (OpenMC, OpenFOAM, fuel-perf, PRA, economics).
- [ ] For each: written explanation of the case conditions, modeling approach, and the output results obtained.
- [ ] **V&V package**: repeatability + benchmarking + reproducibility evidence, using **IAEA / OECD-NEA** reference data (e.g. a benchmark lattice/criticality case). This is explicitly required.
- [ ] List all digital attachments in the report's **Appendices** section with cross-reference links from the main text.

---

## C. Front-matter sections (§1–§7) — mostly [LEAD] + [ALL] input
- [ ] **§1.1 Project Abstract** — concise concept description (Aegis-40, 40 MWe SBF iPWR + TES + SOE + digital twin).
- [ ] **§1.2 Scope** — explicit statement that the design meets each Competition Specification requirement.
- [ ] **§2 Team Introduction** — schematic contribution chart, anonymized.
- [ ] **§3 Literature Review** — ≥3 prior studies, each in its own paragraph, cited (e.g. NuScale, SMART, CAREM, BWRX-300, IRIS for SBF/iPWR).
- [ ] **§4.1 Methodology** — scientific principles + tool chain (OpenMC neutronics, OpenFOAM T-H, fuel perf, PRA, wFOM framework).
- [ ] **§4.2 Feasibility** — buildability under current conditions.
- [ ] **§5.1 Originality/Innovation** — SBF core, HIGA burnable absorber, integrated TES+SOE, digital-twin I&C, wFOM optimization.
- [ ] **§5.2 Domesticity** — contribution to Türkiye national targets + use of national resources.
- [ ] **§6 Work Plan** — work packages + sub-tasks in a table with weekly/monthly schedule (from project start through FER upload).
- [ ] **§7.1 Broader Impacts** + **§7.2 Target Audience**.

---

## D. §8 Technical core — the bulk of the grade

### §8.1 Design Preparation & General Plant Description — [LEAD]+[ALL]
- [ ] Codes & standards list for all systems/components/materials.
- [x] **General design parameters table** — locked rev_3 values in `design-basis-locked.md` (Table 1). Still need to add: lifetime, pressures, temps, EPZ, SSE, CDF/LRF (from T-H/PRA).
- [ ] **Reference regulatory documents list** proving nuclear safety integrated by design (IAEA Safety Standards, NRC GDC, etc.).

### §8.2 Core Design — [NEU] (notebook largely covers this)
- [ ] Material selection + justification (fuel UO₂, clad **Zr-4 [locked]**, coolant, moderator, reflector) incl. behavior under irradiation & temperature (steady/transient/accident).
- [ ] Geometry & layout: assembly count, dimensions, control rods + burnable poison (HIGA/Gd), modeling params.
- [x] **Neutronic analysis**: k-eff, feedback coefficients (MTC/DTC/void), reactivity control worths — locked in `design-basis-locked.md` (Table 2). Still to write up as prose+figures: flux/burnup distribution maps, **BOC → equilibrium cycle** narrative incl. the k_eff drop-then-rise explanation (covered in the locked doc).
  - [x] Notebook items done: **shutdown margin (12.4%)**, **MTC (−35.9)**, **void (−214)**, **DTC (−1.84)** — all PASS.
- [ ] Demonstrate compliance of neutronic safety criteria with national/international regs.
- [ ] **T-H analysis (steady-state)** assumptions + temperature distributions, pressure drops → coordinate with [TH].

### §8.3 Fuel & Material Design — [NEU]
- [ ] Fuel + structural material design and technical data.
- [ ] **Fuel performance & fuel safety** study (centerline temp, clad integrity, gap, fission gas) via analysis/calc — fuel-performance code (e.g. FRAPCON-style).
- [ ] Front-end fuel cycle structural-material properties.

### §8.4 Cooling Circuit System Design — [TH]
- [ ] Primary + secondary loop general description + connected systems.
- [ ] Component spec tables (pumps, valves, pipes, heat exchangers, SG): function, capacity, performance, material — show safety-criteria compliance in all operating conditions.
- [ ] **Heat-removal capacity analysis** (literature-accepted methods) + defined operating conditions.

### §8.5 Safety Criteria — [3S/IC] + [TH]
- [ ] Define AOOs, criticality accidents, and **design-basis accident (DBA)** scenarios.
- [ ] Model + report + evaluate each scenario (LOCA, rod ejection, loss of flow, etc.).
- [ ] **Operating limit conditions** + the calculations that set them (drive from `safety_criteria.yaml`).
- [ ] Show power control, cooling, and fission-product retention hold under normal / AOO / accident conditions, incl. worst case.
- [ ] Close open items in yaml: **AOO PCT envelope** (needs OpenFOAM hot-channel), MDNBR, containment peak P.

### §8.6 Reactor Safety Systems Design — [3S/IC] + [TH]
- [ ] Describe RPS/shutdown, RHR, ECCS, containment systems, PRHR/IRWST — functions + elements.
- [ ] Show auto-actuation logic keeps fuel design limits intact under AOOs; transitions to safe state on loss of power/air/adverse environment.
- [ ] Reactivity-control systems bounded so reactivity accidents don't breach RCS boundary or impair core cooling.
- [ ] **Fault trees + event trees** for all conditions; redundancy & requirement analysis; report results.
- [ ] **Schematic diagrams**: how protective actions derive from neutron flux / temperature / flow and are logically combined (link `trip_signals` / setpoints).
- [ ] PRA: estimate **CDF < 1e-7**, **LRF < 1e-8**; passive **72 h+ grace period** demonstration.

### §8.7 Instrumentation & Control (I&C) Design — [3S/IC]
- [ ] I&C architecture with **block / logic / flow diagrams**: components, subsystems, interconnections.
- [ ] Sensors/detectors/instruments; real-time data processing hardware+software; **HMI** design; secure comms protocols.
- [ ] Design criteria & principles incl. **redundancy, diversity, physical separation**; list critical monitored/controlled parameters; safety + operational requirements.
- [ ] Demonstrate **ergonomic main control room** panel design.
- [ ] (Project differentiator) **Digital-twin** predictive-monitoring architecture + data pipeline → `digital_twin/`.

### §8.8 Auxiliary Systems Design — [LAY]
- [ ] Separate subsections: fission-product release control, ventilation, compressed air, fuel handling & storage, fire protection, radiation protection.
- [ ] Each: purpose, operating principle, layout, safety functions, performance, maintenance — with flow & instrumentation diagrams.
- [ ] On-site + off-site electrical systems incl. emergency & uninterruptible supplies, with diagrams/plans.

### §8.9 Energy Cycle & Integrated Systems — [TH] + [LAY]
- [ ] Energy-conversion system design + **flow diagrams** for electricity generation (Rankine cycle, turbine/condenser).
- [ ] **TES** (district heating) integration: definition, analysis, plant connection → `systems/tes/`.
- [ ] **SOE** (off-peak hydrogen) integration: definition, analysis, plant connection → `systems/soe/`.

### §8.10 Plant Layout Design — [LAY]
- [ ] Optimal general arrangement (constructability, economics, safety, operations).
- [ ] Describe reactor building, energy-conversion systems, O&M services, other buildings.
- [ ] **2D + 3D plans** of main buildings with interconnections; construction info (structures, steel, weights, structural requirements).
- [ ] Critical piping routing (main steam, feedwater, pressurizer, decay-heat-removal lines) within/between structures.

### §8.11 Nuclear Waste Management — [LAY] + [NEU]
- [ ] Innovative fuel-cycle design to reduce waste quantity & radioactivity.
- [ ] Back-end fuel-cycle management plan.
- [ ] Analyses/calcs per Technical Spec §4.3.2 + regulatory-compliance evaluation.
- [ ] **Secondary radioactive waste** management (best-available-technique minimization, segregation).

### §8.12 Economic Evaluation — [LAY]
- [ ] Compare economic advantage vs reference/similar reactors.
- [ ] Investment + operation + production cost calculations (LCOE-style).

---

## E. Cross-cutting / closeout
- [ ] **References** section assembled, formatted, complete.
- [ ] **wFOM** trade-space results integrated into §5 / §8.12 → `optimization/wfom/`.
- [ ] All figures/tables numbered, captioned, cross-referenced; appear in lists.
- [ ] Internal review pass (each section read by a non-author).
- [ ] Final template-compliance audit (font, margins, page count, citations, no personal info, notes page deleted).
- [ ] Build & verify Digital Appendix ZIP; cross-references resolve.
- [ ] **Submit before deadline** (don't wait for the last hour — upload a complete draft early as insurance).

---

## Suggested timeline (milestones)
| Week | Dates | Focus | Exit criterion |
|------|-------|-------|----------------|
| 1 | Jun 2–8 | Lock design basis (§8.1 params table); finish neutronics open items; OpenFOAM steady-state hot-channel running | k-eff, MTC, DTC, void, SDM finalized; MDNBR first number |
| 2 | Jun 9–15 | T-H steady-state done; start DBA/AOO accident modeling (§8.4–8.5); draft §1–§5 | PCT/MDNBR transient envelope; front-matter drafted |
| 3 | Jun 16–22 | Safety systems + PRA fault/event trees (§8.6); I&C + digital twin (§8.7); integrated TES/SOE (§8.9) | CDF/LRF estimates; I&C architecture diagrams |
| 4 | Jun 23–29 | Auxiliary (§8.8), layout 2D/3D (§8.10), waste (§8.11), economics (§8.12); fuel perf (§8.3) | All §8 sections have first full draft |
| 5 | Jun 30–Jul 6 | Assemble full report; build V&V Digital Appendix; internal cross-review | Complete draft, all figures/tables in place |
| 6 | Jul 7–10 | Template-compliance audit, polish, references, **submit** | FER uploaded + Digital Appendix ZIP |

## Biggest risks / start-now items
1. **OpenFOAM T-H is empty** — it gates §8.4, §8.5 (PCT/MDNBR), §8.6 capacities. Start immediately.
2. **Digital Appendix V&V** (IAEA/OECD-NEA benchmark) is required and time-consuming — assign an owner Week 1.
3. **PRA fault/event trees** (§8.6) are explicitly mandated and easy to underestimate.
4. **120-page limit** — plan section budgets early; §8 will dominate.
5. **Template compliance is pass/fail** — non-conforming reports are not evaluated.
