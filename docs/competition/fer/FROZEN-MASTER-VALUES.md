# Aegis-40 — FROZEN MASTER VALUES (single source of truth)

*Every section, table, figure caption and appendix must use these values. Anything not matching is
an inconsistency to fix. Basis: STAT_FINAL record run + frozen design decisions, 2026-07-04.*

## Core / power
| Quantity | FROZEN value |
|---|---|
| Thermal / electric power | 125 MWth / 40 MWe |
| Net efficiency | 32.0 % |
| Assemblies / lattice / height | 37 FA / 17×17 / 2.0 m active |
| Fresh heavy-metal loading | **9.39 tHM** |
| Specific power | **13.31 MW/tHM** |
| Enrichment (rings, centre→edge) | 4.95 / 4.70 / 4.40 / 4.00 wt% (core-avg ~4.43, peak 4.95) |
| Burnable absorber | Gd₂O₃ 6 wt% × 20/FA (ring-graded) + Er₂O₃ 0.75 wt% × 16/FA |
| Control rods | **16 CRA**, 90 % enriched-B-10 B₄C |
| Concept | soluble-boron-free, natural circulation |

## Primary / secondary
| Quantity | FROZEN value |
|---|---|
| Primary pressure / T_avg | 12.8 MPa / 283 °C (258 in / 308 out) |
| Primary flow / mass flux | 467 kg/s / 543 kg/m²·s |
| Main steam | **4.5 MPa / 296 °C / 57.8 kg/s** |
| Condenser | 7 kPa / 39 °C (seawater once-through) |

## Fuel cycle (once-through)
| Quantity | FROZEN value |
|---|---|
| Cycle length | **2224 EFPD ≈ 6.09 FPY** |
| Discharge burnup (core-avg) | **29.6 GWd/tHM** |
| Peak-assembly burnup | 42 GWd/tHM (≪ 62 limit) |
| 3-batch equilibrium option | ~44.4 GWd/tHM |

## Neutronics (STAT_FINAL)
| Quantity | FROZEN value |
|---|---|
| k_BOL (HFP, ARO) | **1.1503 ± 26 pcm** |
| MTC / DTC / void | **−26.9 / −1.91 / −173** (pcm/K, pcm/K, pcm/%void) |
| Rod-bank worth (16 CRA) | **21 479 pcm** |
| Shutdown margin (stuck rod, hot) | **+7.68 % Δk/k** |
| Max reactivity insertion rate | 1.5×10⁻⁵ Δk/k/s |
| Gd/Er hump peak | k = 1.135 at ~13.5 GWd/tHM (< BOC 1.150) |

## Peaking (×1.03 allowance) & COLR
| State | F_ΔH | F_z | F_q |
|---|---|---|---|
| BOC | 1.513 | 1.280 | 1.937 |
| MOC (hump) | 1.729 | 1.408 | 2.435 |
| EOC | 1.497 | 1.417 | 2.121 |

- Generic screening limits: F_ΔH ≤ 1.65, F_q ≤ 2.32 (NOT design-specific)
- **Adopted design-specific COLR limit: F_ΔH ≤ 1.75**
- MDNBR at MOC envelope (F_ΔH 1.75): **1.37 (W-3) / 2.20 (Bowring)**; peak fuel 828 °C
- REA ejected-rod worth: **1.20 $** (full insertion) → PDIL requirement at power

## Cooling / DNBR by state
| State | MDNBR W-3 | MDNBR Bowring | Fuel T | Clad T |
|---|---|---|---|---|
| BOC | 1.60 | 2.72 | 722 °C | 348 °C |
| MOC | 1.38 | 2.23 | 822 °C | 352 °C |
| EOC | 1.51 | 2.56 | 759 °C | 350 °C |
- Peak LHR 12.8 kW/m (core-avg 6.4); MDNBR limit ≥ 1.30

## Safeguards / Pu vector (EOC, 29.6 GWd/t)
| Quantity | FROZEN value |
|---|---|
| Total Pu | **76.2 kg** |
| Pu vector (238/239/240/241/242) | 2.0 / **62.8** / 21.2 / 10.1 / 3.9 wt% (reactor-grade) |
| Residual U-235 | ~1.8 wt% |
| Self-protection | 12.2 W/kg-Pu ; 3.1×10⁵ n/s/kg |

## Waste (§8.11)
| Quantity | FROZEN value |
|---|---|
| Waste intensity | **4.40 tHM/TWhe** (~32 % below CAREM-25 6.43) |
| Decay heat (rigorous) | 7.95 MW shutdown / 48 kW @1 yr / 9 kW @10 yr |
| Total activity at discharge | 2.76×10¹⁹ Bq |
| Storage k(95/95) | Boral **0.837** / Metamic **0.847** (≤ 0.95) |
| Classification | HLW / SNF |

## Energy cycle (§8.9)
| Quantity | FROZEN value |
|---|---|
| TCES store (reference) | **Zeolite-13X / H₂O**, ~1000 t / 1538 m³ / 200 MWh_th |
| TCES discharge / round-trip | ~130 °C / ~0.78 |
| TCES alternative (evaluated, NOT adopted) | ammine NiCl₂–SrCl₂/NH₃ (validated, ~735 t, COPh 0.973 direct) |
| District heat | 25 MWth peak / 12.5 avg, 90/45 °C |
| Charge loop | 1.0 MPa/180 °C HP extraction → IHX → ~168 °C |
| H₂ (SOE) | 8 MWe, 37.55 kWh/kg, 213 kg/h, **120 t/yr** (560 h/yr) |

## Economics (§8.12)
| Quantity | value |
|---|---|
| Electricity / DH / H₂ revenue | ~$22.4 M / $2.5 M / $0.60 M |
| Cogeneration uplift | **+$2.9 M/yr (~+13 %)** |
| LCOE band / mid | 85–142 / ~108 $/MWh |

## V&V (§8.13 / appendix)
- OpenMC 0.15.3, ENDF/B-VIII.0
- ICSBEP LEU-COMP-THERM-008 (OECD/NEA): mean bias ≈ −50 pcm (all cases < 1σ)
- NuScale-like core benchmark: within ±80 pcm of Serpent (6 rod states)
- Depletion: Romano (2021) published validation + reproduced configuration

---

## ❌ STALE VALUES — replace on sight (these are WRONG)
| Wrong | Correct |
|---|---|
| 9.87 / 9.44 tHM | 9.39 tHM |
| 12.66 / 13.24 MW/tHM | 13.31 MW/tHM |
| 2175 EFPD | 2224 EFPD |
| 27.6 / 29.0 / 42.8 GWd/tHM | 29.6 GWd/tHM |
| 7.17 MPa (SG) | 4.5 MPa |
| 441 t/yr H₂ | 120 t/yr |
| 4.72 / 4.50 tHM/TWhe | 4.40 tHM/TWhe |
| Pu-239 63.6 % / 61.6 % | 62.8 % |
| Total Pu 76.6 / 78.1 kg | 76.2 kg |
| ammine as the reference store | zeolite-13X is reference (ammine = alternative) |
| "rev_3 / rev_4", "STAT_FINAL pending", "run pending" | drop (all runs complete) |
| any code/file path in report prose | remove (paths belong only in the appendix) |
