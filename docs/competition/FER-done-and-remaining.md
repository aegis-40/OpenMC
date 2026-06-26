# Aegis-40 FER — Status Summary: Done vs. Remaining

**Date:** 2026-06-24  **Deadline:** 2026-07-10  **Document:** Final Engineering Report (FER), Section 8 + front matter

## Owner key

| Code | Role | Person |
|---|---|---|
| LEAD | Team lead / front matter / assembly | (lead) |
| NEU | Neutronics & core | Samira |
| TH | Thermal-hydraulics & cycle | Adilbek |
| 3S | Safety, safeguards, I&C | Azamkhon |
| LAY | Layout, auxiliary, economics | Elbek |

---

## 1. Big picture

The **Section 8 technical body is complete in draft** — a single consolidated master
(`Aegis40-FER-master.md`, approx. 961 paragraphs / 47 tables), with **every heading filled and none left
blank** (the pass/fail rule from last year's lead). The two largest items *not* yet in the document are
the **front matter (§1–§7)** and the **template / submission packaging**. The single technical gate that
still blocks final numbers is the **STAT_FINAL OpenMC neutronics run**.

---

## 2. Done — drafted and internally consistent

| § | Section | Owner | What is done |
|---|---|---|---|
| 8.1 | General description | LEAD/NEU | All parameter tables, codes & standards, regulatory list, prep-phase docs |
| 8.2 | Core design | NEU | Materials, geometry, layout figures; neutronics V&V + NuScale anchor (Tables 8.2-6/8.2-7). Numeric neutronics values pending STAT_FINAL |
| 8.3 | Fuel & material | NEU | Linear heat rate, centerline-temperature stack-up (CFD-based, 734 °C), fission-gas release, clad integrity |
| 8.4 | Cooling circuit | TH | Natural-circulation loop re-derived (H_tc 4.0 m, flow 467 kg/s, driving head 3.67 kPa, ~10 m vessel); heat removal closed by conjugate CFD (MDNBR 1.56, PCT 349 °C); ASME V&V-20 verified; validated vs NuScale NPM-160 |
| 8.5 | Safety criteria | 3S/TH | Criteria framework, demonstrated-margins table, defence-in-depth, dual heat sinks |
| 8.6 | Safety systems | 3S/TH | Passive ESF, two diverse shutdown means (EBIS), event-tree results for LOHS and SBO |
| 8.7 | I&C | 3S | Architecture, RPS/ESFAS/DAS, control room & human factors, digital twin |
| 8.8 | Auxiliary systems | LAY | System table, cogeneration isolation, electrical summary |
| 8.9 | Energy conversion | TH/LAY | Rankine cycle, state points, OTSG feasibility, TCES district heat + charging-duty justification, hydrogen |
| 8.10 | Layout | LAY | Three-island scheme, building inventory, critical piping |
| 8.11 | Waste management | LAY/NEU | Back-end plan, source term, decay heat, storage criticality (15/15 unit tests) |
| 8.12 | Economics | LAY | LCOE methodology, result, reference-reactor comparison (literature CAPEX) |
| 8.13 | Digital Appendix (V&V index) | ALL | Structure complete; some confirmatory runs pending |
| — | Provenance table | ALL | Every headline number traced to a basis class |
| — | Requirements-coverage matrix | ALL | Every §8 requirement mapped, with an honest could-not-close list |

---

## 3. Remaining — what is left to do

### 3.1 The one true gate — neutronics STAT_FINAL

| Item | Owner | Note |
|---|---|---|
| Run STAT_FINAL OpenMC depletion; swap all ⏳[37FA-PENDING] markers (k_eff, burnup, cycle length, peaking, coefficients, rod worth, SDM, inventory) | NEU | Also triggers the MDNBR re-run on final per-pin peaking (≈1.4 expected — still PASS). Everything downstream is wired to drop these in |

### 3.2 Open analysis items (from the could-not-close list)

| Item | Owner |
|---|---|
| DBA spectrum depth — MSLB/SBLOCA event trees + quantitative CDF/LRF (2 initiators analysed today; rest screened; class-target CDF/LRF stated, not computed) | 3S/TH |
| Containment design pressure / P-T response — open dry-vs-pool concept decision | 3S |
| LOCA-transient PCT / clad-oxidation / ECR envelope (accident side, gated by DBA work) | TH/3S |
| Bottom-up CAPEX + cogeneration revenue credit (§8.12) — needs frozen equipment list | LAY |
| Site/interface studies — tritium permeation, Sinop coastal hazard, SKKY thermal discharge, EPZ dose | 3S/LAY |

### 3.3 Manual fixes (tool-specific, not code-fixable from the report)

| Item | Owner |
|---|---|
| CAD/Creo: vessel height to ~10 m / H_tc 4.0 m + STEP + general-arrangement drawing | NEU |
| DWSIM: secondary flowsheet primary flow 483→467 + cogeneration extraction tap | TH |
| ParaView: Adilbek's F9a/b/c field plots (currently placeholders) | TH |
| NuScale [verify] cells in Table 8.2-7 — pin 5 figures against the FSAR (HM loading, specific power, rod count, cycle length, discharge burnup) | NEU |
| §8.10: reactor-building height vs ~10 m vessel | LAY |

### 3.4 Figures / "shine" pass (the single biggest scoring lever)

| Item | Owner |
|---|---|
| Per-system P&IDs for §8.8; single-line electrical diagram for §8.8.10 | LAY |
| 2D/3D layout plans + structural/weight data for §8.10.5 (CAD held locally) | LAY/NEU |
| Neutronics figures (k_eff-vs-burnup, radial/axial power maps) once STAT_FINAL lands | NEU |

### 3.5 Front matter §1–§7 — NOT STARTED (largest gap outside §8)

The master is §8-only. The template also requires the following. Source material exists
(CAREM / Santinello / NuScale PDFs, safeguards and domesticity notes) but none of it is drafted into the
document yet.

| § | Section | Owner |
|---|---|---|
| 1 | Abstract / scope | LEAD |
| 2 | Team (schematic) | LEAD |
| 3 | Literature review | LEAD |
| 4 | Methodology / feasibility | LEAD |
| 5 | Originality / domesticity | 3S/LEAD |
| 6 | Work plan | LEAD |
| 7 | Broader impacts | LEAD |

### 3.6 Digital Appendix packaging

| Item | Owner |
|---|---|
| Run the cheap confirmatory benchmarks in WSL (BEAVRS pincell depletion, ICSBEP) — scripted, not yet executed | NEU |
| Assemble the ZIP: one sample input per code + explanations (T-H `th_cfd/` case ready; OpenMC decks + economics deck need bundling) | ALL |

### 3.7 Template compliance + submission (pass/fail logistics)

| Item | Owner |
|---|---|
| Official template .docx styling (Arial 12 / Arial Black 14, margins, TOC, ≤120 pp); merge citations into one list; remove personal info; delete notes page | LEAD |
| Cross-review (each section read by a non-author); lock numbers across sections | ALL |
| Early-submission insurance upload before the deadline hour | LEAD |

---

## 4. Housekeeping

The latest editing batch — FER `.md`/`.docx`, `docs/figs/`, `th_cfd/`, the provenance table and the
neutronics V&V — is **still uncommitted** in the working tree (branch `main`, 8 commits ahead of origin).
Pending decision: commit + push to the `fer-master-consolidation` branch.
