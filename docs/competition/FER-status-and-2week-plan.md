# Aegis-40 FER — Status Checklist & 2-Week Plan (as of 2026-06-08)

**Deadline:** 2026-07-10. **Strategy:** drive *every* §8 heading to a full first draft by **Jun 22**
(2-week sprint), leaving **~2.5 weeks (Jun 23 → Jul 10)** for internal review, the V&V Digital
Appendix, template-compliance audit, and an early-submission insurance buffer.

> **Guiding principles — from Mahmut Yıldırım (last year's team lead, 2026-06-06):**
> 1. **3D drawings / schematics are the single biggest "shine" lever** — invest in figures.
> 2. Judges (NET category) weigh **§8.2–§8.6 most heavily** — protect those sections.
> 3. **Never leave a heading blank** — a thin section beats an empty one (empty = lost points,
>    and template non-compliance is pass/fail).

---

## 1. Where we stand (status by section)

Legend: ✅ done · 🟡 drafted/partial · 🟠 analysis done, prose pending · ⬜ not started

| § | Section | Owner | Status | What exists / what's missing |
|---|---|---|---|---|
| A | Template `.docx` in repo + styling | LEAD | ⬜ | **Pass/fail. Do first.** Copy official template, set Arial 12 / Arial Black 14, margins, TOC/lists |
| B | Digital Appendix (V&V) | ALL | 🟡 | `digital-appendix-vv-plan.md` + `code-benchmark-matrix.md` exist; benchmark **not run/packaged** |
| §1 | Abstract / Scope | LEAD | ⬜ | content derivable from design-basis-locked.md |
| §2 | Team (schematic) | LEAD | ⬜ | quick, anonymized chart |
| §3 | Literature review | LEAD | 🟡 | `reference-reactors-comparison.md` + 6 lit PDFs (see §2 below) — needs ≥3 written paragraphs |
| §4 | Methodology/Feasibility | LEAD | ⬜ | tool chain known (OpenMC/cycle/back-end) |
| §5 | Originality / Domesticity | 3S/LEAD | 🟡 | `safeguards_attractiveness.md`; **CAREM 70%-domestic → Türkiye** angle ready |
| §6 | Work plan | LEAD | ⬜ | this file feeds it |
| §7 | Broader impacts | LEAD | ⬜ | short |
| §8.1 | General plant description | LEAD | 🟡 | `design-basis-locked.md` Table 1+2; **CAD RPV/core** figures ready. Missing: lifetime, pressures, EPZ, CDF/LRF, codes-&-standards + regulatory lists |
| §8.2 | Core design | NEU | 🟡 | **draft written** (`fer/section-8.2-8.3...md`); safety #s locked. Missing figures: k_eff-vs-burnup, radial/axial power maps |
| §8.3 | Fuel & material | NEU | 🟡 | **draft written** (LHR, centerline-temp stack-up). Optional: FRAPCON-style confirm |
| §8.4 | Cooling circuit | TH | 🟡 | **draft written** (`fer/section-8.4-cooling-circuit.md`): primary nat-circ loop balance (`natcirc_primary.py`, ṁ483 kg/s / driving head 2.62 kPa ↔ CFD 0.90 m/s), component+material tables, heat-removal analysis. ⚠ cold-leg 258 °C caps OTSG steam ≤3.98 MPa → §8.9 40 MWe must be re-run |
| §8.5 | Safety criteria (DBA/AOO) | 3S+TH | ⬜ | `safety_criteria.yaml` spine only; **no DBA modeling** — critical path |
| §8.6 | Safety systems + PRA | 3S+TH | ⬜ | **empty `safety_3s/`**; fault/event trees, CDF/LRF, 72-h grace not started |
| §8.7 | I&C + digital twin | 3S | ⬜ | **empty `digital_twin/`**; INL digital-twin paper now available as template |
| §8.8 | Auxiliary systems | LAY | ⬜ | not started |
| §8.9 | Energy cycle + TES/SOE | TH+LAY | ✅ | **draft + PFD + T-s + TES sizing done**; SOE needs a sizing paragraph |
| §8.10 | Plant layout (2D/3D) | LAY | 🟡 | CAD RPV/core help; **building arrangement** not started |
| §8.11 | Waste management | LAY+NEU | 🟠 | **analyses done** (`waste/`: intensity, decay heat, source term, storage criticality); needs FER prose |
| §8.12 | Economics (LCOE) | LAY | ⬜ | `reference-reactors-comparison.md` helps; no cost calc |
| E | wFOM optimization | 3S | ⬜ | **empty `optimization/`** |

**Headline:** NEU (Samira) is far ahead — §8.2, §8.3, §8.9, §8.11, safeguards, shielding, and the full
CAD suite are done or drafted. The gap is the **TH / safety / I&C / layout / economics** half of §8,
mostly empty. The two true critical-path items are **§8.4 primary T-H** and **§8.5–§8.7 safety/PRA/I&C**.

---

## 2. New literature → section mapping

| PDF | What it is | Feeds |
|---|---|---|
| `CAREM report.pdf` | IAEA status report, CAREM-25 (25 MWe integral PWR, natural circ, hydraulic CRDM, indirect cycle, **70% domestic**) | §3, §8.1, §8.4, §8.6 (passive safety), §8.10, **§5.2 domesticity** |
| `ipwr design.pdf` | Santinello PhD (PoliMi/Ricotti, 161 pp): submerged integral SMR, **passive-safety strategy**, critical issues | §8.1, §8.4 (nat-circ), §8.5 (critical issues), §8.6 (passive systems) |
| `digital twins.pdf` | INL digital-twin framework for remote reactor monitoring (AGN-201 + microreactor cases) | **§8.7 digital twin** architecture + data pipeline |
| `cycle1.pdf` | Tsinghua/TUM SMR electricity-steam **cogeneration** for industry decarbonization | §8.9 (cogeneration/TES), §5.1 originality, §7 impacts |
| `cycle2+tes.pdf` | INL Frick TES (Therminol-66 two-tank) | §8.9 TES (**already used** — Table 8.9-5) |
| `drawings-ipwr.pdf` | Kapernick MS thesis, mPower-like integral RPV | §8.1 CAD (**already used** — RPV model) |

---

## 3. Two-week sprint (Jun 9 → Jun 22): every heading to full draft

### Week A — Jun 9–15 — "critical path + front matter"
| Owner | Tasks | Exit criterion |
|---|---|---|
| **LEAD** | Copy template `.docx`; set styling/TOC/lists; draft **§1, §2, §3** (use CAREM/Santinello/NuScale paragraphs) | template live, front matter drafted |
| **TH (Adilbek)** | **§8.4 primary loop**: natural-circulation driving head, core ΔT, **heat-removal + MDNBR** (subchannel/W-3 if CFD blocked) | first MDNBR / PCT numbers |
| **3S (Azamhon)** | **§8.5** DBA/AOO list + bounding scenarios (LOCA, rod ejection, LOFA); start §8.6 fault/event trees | DBA set defined; tree skeletons |
| **NEU (Samira)** | Export **§8.2 figures** (k_eff-vs-burnup, power maps); write **§8.11 waste prose** from `waste/` analyses | §8.2 figures in; §8.11 drafted |
| **LAY (Elbek)** | **§8.10** building arrangement (reactor/turbine/aux buildings); start **§8.12** LCOE skeleton | layout sketch + cost framework |

### Week B — Jun 16–22 — "fill remaining headings + integrate"
| Owner | Tasks | Exit criterion |
|---|---|---|
| **LEAD** | §4, §5, §6, §7; assemble all drafts into the template; references | all front matter in template |
| **TH** | finish §8.4 component tables; support §8.5 PCT envelope; SOE paragraph in §8.9 | §8.4 complete |
| **3S** | **§8.6 PRA** (CDF<1e-7, LRF<1e-8, 72-h grace); **§8.7 I&C + digital twin** (INL framework) | §8.6 + §8.7 drafted |
| **NEU** | finish §8.1 params (lifetime/pressures/EPZ); §8.3 polish; **build V&V benchmark** (IAEA/OECD-NEA lattice) | §8.1 complete; benchmark run |
| **LAY** | §8.8 auxiliary systems; §8.10 2D/3D plans; §8.12 LCOE numbers | §8.8/§8.10/§8.12 drafted |

**Exit by Jun 22:** every §8 heading has a full first draft; no blank headings (Mahmut's rule).

---

## 4. Buffer phase (Jun 23 → Jul 10): review, harden, submit early

| Window | Focus |
|---|---|
| Jun 23–26 | wFOM trade-space → §5/§8.12; figure polish (3D renders, schematics — Mahmut's "shine"); fill any thin section |
| Jun 27–30 | **Cross-review**: each section read by a non-author; close gaps; lock numbers across sections |
| Jul 1–4 | **Digital Appendix ZIP**: one sample input per code + explanations + V&V evidence; verify cross-references |
| Jul 5–7 | **Template-compliance audit** (font/margins/≤120 pp/citations/no personal info/notes-page deleted); **upload complete draft as insurance** |
| Jul 8–10 | Final polish; re-upload; **submit well before the deadline hour** |

---

## 5. Top risks (start-now)
1. **§8.4 primary T-H** gates §8.5/§8.6 — if Adilbek is still blocked, fall back to **subchannel/correlation** methods (W-3 DNBR, 1-D hot channel, ANS-5.1 decay heat) and one CFD showcase figure. *(Claude can build a `src/aegis40/thermal_hydraulics` module to de-risk this.)*
2. **Template `.docx` not yet in repo** — pass/fail; copy it **Day 1**.
3. **PRA fault/event trees (§8.6)** are mandated and easy to underestimate — owner assigned Week A.
4. **V&V benchmark** for the Digital Appendix is required and slow — schedule it Week B, not the last days.
5. **§8.7 I&C / digital twin** was empty — now unblocked by the INL paper; still needs an owner.

> Cross-references: `FER-preparation-checklist.md` (full template bullets), `design-basis-locked.md`
> (locked params), `fer/section-8.2-8.3-core-and-fuel.md`, `fer/section-8.9-energy-cycle.md`.
