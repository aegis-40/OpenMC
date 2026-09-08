# Aegis-40 — Authoritative Numbers (single source of truth)

**Updated:** 2026-08-14. If any doc/slide disagrees with a value here, **this file wins** — fix the other doc.
Values are STAT_FINAL OpenMC (ENDF/B-VIII.0) unless noted. 💡 = how we could strengthen it before finals.

---

## 1. Plant & core (design point)
| Parameter | Value | Note |
|---|---|---|
| Thermal / electric power | **125 MWth / 40 MWe** | net |
| Net thermal efficiency | **32.0 %** (31.8 % computed) | Rankine, OTSG |
| Reactor type | Integral PWR (iPWR), **soluble-boron-free** | in-vessel CRDMs, OTSG, pressurizer |
| Primary flow | **Natural circulation** (no RCP) | ~467 kg/s, ΔP ≈ 3.67 kPa |
| Assemblies / lattice / height | **37 FA · 17×17 · 2.0 m** active | |
| Heavy-metal loading | **9.39 tHM** | |
| Specific power | **13.31 MW/tHM** | |
| Fuel cycle | **Once-through**, single batch | |
| Discharge burnup | **29.6 GWd/tHM** (core avg) | assembly-peak higher; ≤ 62 GWd/MTU limit |
| Cycle length | **2224 EFPD (6.09 FPY)** | |

💡 *A short multi-batch (2- or 3-batch) shuffle study would cut discharge-burnup peaking and raise fuel utilization — even a paper estimate strengthens the "once-through is a deliberate choice" answer.*

## 2. Fuel & materials
| Parameter | Value |
|---|---|
| Pellet / clad | UO₂ / Zircaloy-4 |
| Enrichment zones | **4.95 / 4.70 / 4.40 wt%** + 4.0 wt% edge |
| Core-average enrichment | **4.43 wt%** (drives economics) |
| Burnable poison | **Gd₂O₃ 6 wt% ×20 pins/FA + Er₂O₃ 0.75 wt% ×16 pins/FA** |
| Peak linear heat rate | ~**15.8 kW/m** (avg ~6.4) |

💡 *Add a cladding-alternative sentence (e.g., ATF — Cr-coated Zr or FeCrAl) as a "future upgrade path"; jurors reward awareness even if the baseline stays Zr-4.*

## 3. Neutronics (STAT_FINAL)
| Parameter | Value | Target / basis |
|---|---|---|
| k_eff BOL | **1.1503** | BOC excess ≈ 13,300 pcm |
| Moderator temp coeff (MTC) | **−26.87 pcm/°C** | must be < 0 ✓ |
| Doppler / fuel temp coeff (DTC) | **−1.91 pcm/°C** | < 0 ✓ |
| Void coefficient | **−173.2 pcm/%void** | < 0 ✓ |
| **Control rods** | **16 CRA** (12 + 4 central-cross), 90 %-enriched B-10 B₄C | ← **UPDATED** |
| Rod bank worth | **21,509 pcm** | was 15,672 (12-CRA) |
| Hot shutdown margin | **7.85 %** (k_ARI = 0.927, k_adj = 0.933) | was ~2.0 % |
| Cold shutdown | **EBIS** (boron injection) — credited | k_stuck_cold = 1.031 → rods alone insufficient cold |
| Peaking F_ΔH / F_q, BOC | 1.513 / 1.937 | |
| Peaking F_ΔH / F_q, MOC | 1.729 / 2.435 | closed under COLR envelope |
| Peaking F_ΔH / F_q, EOC | 1.497 / 2.121 | |
| COLR envelope | **F_ΔH 1.75 · F_q 2.4675** | licensing basis |

💡 *The MOC F_q (2.435) sits just under the COLR limit (2.4675) — a ~1 % margin. A fresh sweep with slightly re-graded Gd could open that margin; worth mentioning we know it's the tightest point. Also: run the **fresh 16-CRA digital-twin sweep** to replace the ±40 % indicative coefficients with tight ones.*

## 4. Thermal-hydraulics
| Parameter | Value | Limit / note |
|---|---|---|
| MDNBR (steady) | **1.33 (W-3) / 2.13 (Bowring)** | ≥ 1.30 W-3 ✓ |
| MDNBR (AOO transient) | **1.57** | |
| Riser-height MDNBR sweep | 3 m→1.12 · **4 m (design)→1.37** · 5 m→1.58 · 6 m→1.78 · 8 m→2.11 | 6 m fixes a 2.78 typo |
| Peak clad temp (PCT) | **353 °C** | |
| Peak fuel centerline | **828 °C** | |
| OTSG steam | **4.5 MPa / 296 °C**, feed 57.75 kg/s | |
| Turbine shaft → net | **42.8 MW → 40 MWe** | |

💡 *W-3 is conservative but old; citing a modern CHF correlation (or the 2006 Groeneveld look-up table) as a cross-check would harden the DNB case. The 4 m riser at MDNBR 1.37 is the tightest design choice — be ready to defend why not 5 m.*

## 5. Safety
| Parameter | Value |
|---|---|
| Safety approach | Fully passive; in-vessel retention |
| IRWST inventory | **250 m³** |
| Grace period (no operator/AC) | **≥ 240 h** |
| Core damage frequency (CDF) | **< 1×10⁻⁷ /ry** |
| Large release frequency (LRF) | **< 1×10⁻⁸ /ry** |
| SBLOCA peak (bounding) | **0.139 MPa vs 0.414 limit** |
| Spent-fuel-pool k (95/95) | **0.892** |

💡 *CDF/LRF are currently order-of-magnitude/qualitative. A simple event-tree for the 2–3 dominant sequences (SBLOCA, SGTR-equivalent, LOOP) would turn "< 10⁻⁷" into a defensible number — high-value for the safety score.*

## 6. Shielding (lead-free, adopted §4.3 build)
| Parameter | Value |
|---|---|
| Shield stack | **20 cm borated polyethylene + 180 cm magnetite concrete** |
| RPV fast fluence (E>1 MeV, EOL) | **3.0×10¹⁸ n/cm²** (PASS) |
| Contact dose (nominal / bounding) | **0.23 / 5.5 µSv/h** |
| Shield outer diameter | **≈ 7.6 m** |

💡 *Dose is point-kernel (ANS-6.4). A converged Monte-Carlo dose map (two-stage MAGIC weight-window, needs the OpenMC machine) would upgrade this from "estimate" to "calculated" — the single strongest shielding credibility boost.*

## 7. Waste & back-end
| Parameter | Value |
|---|---|
| Cycle | Once-through |
| HM discharge rate | **4.40 tHM/TWhe** |
| Decay heat | **7.95 MW (shutdown) / 48.4 kW (1 yr) / 9.0 kW (10 yr)** |
| Discharge Pu | **78.1 kg, reactor-grade (Pu-239 61.6 %)** |

💡 *We already frame proliferation resistance as extrinsic + high burnup. A one-line Bathke figure-of-merit number (already computed in the safeguards work) belongs in the FER/slide to make it quantitative.*

## 8. Energy cycle & cogeneration
| Parameter | Value |
|---|---|
| Secondary cycle | Rankine, 40 MWe, 32 % |
| Thermal storage | **TCES zeolite-13X** for district heat |
| Hydrogen (SOE) | **427 t/yr @ 39 kWh/kg** |

💡 *State the district-heat delivered MWth and the round-trip TCES efficiency explicitly — right now the cogen story is strong on concept but thin on delivered-energy numbers.*

## 9. Economics
| Parameter | Value |
|---|---|
| Fuel assay basis | 4.43 wt% → 6.73 SWU/kg, 9.07 kg NatU/kg |
| Front-end fuel cost | **$5.47 M/yr → $17.3/MWh** |
| **LCOE (NOAK, 7 %)** | **$74.8/MWh** |
| LCOE cogen-credited | **$64.8/MWh** |
| LCOE FOAK / derived | **$90.6 / $124.7 /MWh** |
| Table 8.12-6 (3/7/10 %) | NOAK 55.5/74.8/92.1 · FOAK 63.1/90.6/115.2 · derived 79.5/124.7/165.2 · high 88.4/143.1/192.2 |

💡 *Add one sensitivity tornado (capex, capacity factor, discount rate) — jurors love seeing which lever dominates LCOE. The DA-7 model already outputs `lcoe_sensitivity.csv`; just needs a chart.*
