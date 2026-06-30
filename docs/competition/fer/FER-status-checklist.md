# Aegis-40 FER — Status Checklist (against the 2026 competition guideline)

Legend: ✅ done · 🟡 partial / needs update with new results · ⬜ missing / to write.
"New inputs" = results since the last FER revision to fold in.

## Front matter (currently MISSING from the master — Section-8-only) — must WRITE
| # | Guideline chapter | Status | Source / what to write |
|---|---|---|---|
| 1 | **Project Abstract / Scope** | ⬜ | 125 MWth/40 MWe SBF natural-circulation iPWR, Sinop; once-through, cogeneration (DH+H₂). 1-page pitch. |
| 2 | **Team Introduction** | ⬜ | from `team-roles` (NEU/3S/CAD/TH owners). |
| 3 | **Literature Review** | ⬜ | CAREM-25, NuScale NPM, RITM-200, integral-PWR + SBF + TCES/SOE refs (we have most). |
| 4 | **Methodology & Feasibility** | ⬜ | OpenMC (VIII.0) neutronics + V&V (BEAVRS/NuScale-like/shielding), OpenFOAM CHT, depletion, codes/standards. |
| 5 | **Originality / Innovation / Domesticity** | ⬜ | SBF + Gd/Er hybrid + EBIS, TCES district heat, SOE H₂, digital-twin, once-through proliferation resistance. |
| 6 | **Project Work Plan** | ⬜ | Gantt + the status of each WP. |
| 7 | **Broader Impacts & Target Audience** | ⬜ | Sinop DH, H₂, sustainability, economics. |

## Section 8 — technical
| # | Chapter | Status | New inputs to fold in / what's left |
|---|---|---|---|
| 8.1 | Design Prep & General Description | 🟡 | exists; refresh tables with **once-through** basis + final HM/power numbers. |
| 8.2 | **Core Design** | 🟡 | exists; **replace neutronics with STAT_FINAL once-through**: k(BU), B₁=27.6 GWd/t, peaking F_q/F_ΔH, MTC/DTC, SDM, **Pu vector <65% Pu-239**. Figures from `aegis40_neutronics_outputs (2)`. |
| 8.3 | Fuel & Material Design | 🟡 | exists; update LHR/centerline-T/fission-gas from **TH report (3)**; once-through residence/burnup. |
| 8.4 | **Cooling Circuit System** | 🟡 | exists; update with **TH report (3)** (MDNBR, PCT, nat-circ, OTSG). |
| 8.5 | Safety Criteria | 🟡 | fold in `safety_85_86` (k_adj table, limits PASS/FAIL). **graphs/diagrams left.** |
| 8.6 | Reactor Safety Systems | 🟡 | EBIS/rod-SDM/MSLB from `safety_85_86`; 16-CRA + enriched-B10 story. **event trees + diagrams left.** |
| 8.7 | I&C System | ✅🟡 | exists; minor refresh (RPS/ESFAS/DAS). |
| 8.8 | Auxiliary Systems | 🟡 | exists; cogen-isolation done; **add SFP (N11) + layout refs.** |
| 8.9 | **Energy Cycle & Integrated Systems** | 🟡→✅ | **results READY** in `cogen_TCES_SOE_FER.md` + PFD/drawio — drop in. Diagrams done. |
| 8.10 | Plant Layout | ⬜🟡 | **3D model DONE** → need rendered figures + layout description; RPV Ø3.44 m, bioshield radii. |
| 8.11 | **Nuclear Waste Management** | 🟡 | **results READY** (`waste_sim`): discharge inventory, Pu vector, activity/decay-heat, repository basis. Rewrite. |
| 8.12 | Economic Evaluation | 🟡 | exists; add cogen uplift (+18%/yr) + once-through fuel-cycle cost. |

## What's genuinely DONE (results in hand, just need writing-in)
- ✅ Neutronics STAT_FINAL (once-through, B₁ 27.6, Pu vector, peaking, coeffs)
- ✅ Safety §8.5–8.6 sims (EBIS/SFP/MSLB/rod-SDM, k_adj-graded)
- ✅ TH report (3) (MDNBR/PCT/nat-circ)
- ✅ Waste sim · ✅ Cogen TCES+SOE (8.9) · ✅ 3D CAD model · ✅ Shielding build

## What's LEFT (work, not just writing)
- ⬜ Front chapters 1–7 (write from scratch)
- ⬜ 8.10 plant-layout figures from the 3D model
- ⬜ 8.5/8.6 graphs (k_adj bars, event trees) + 8.11 waste plots
- ⬜ Final formatting pass to the guideline template (TOC, table/figure numbering, abbreviations)
