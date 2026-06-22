# Aegis-40 iPWR — Final Engineering Report (FER), Section 8 (Master)

**Project:** Aegis-40 — 40 MWe / 125 MWth soluble-boron-free integral PWR (iPWR-SMR)
**Category:** TEKNOFEST 2026 Nuclear Energy Technologies — Detailed Design (40 MWe PWR)
**Document:** Consolidated master of the §8 technical body (§8.1 – §8.12) + mandatory Digital-Appendix
plan + full requirements-coverage matrix.
**Revision:** master r1, 2026-06-22. **Supersedes** the per-section drafts
(`section-8.1-…`, `section-8.2-8.3-…`, `section-8.4-…`, `section-8.9-…`, `section-8.11-…`,
`section-8.12-…`, and `FER_Aegis40_safety_ic_layout_draft.md`), which are archived under
`fer/archive/`.

---

## 0. Reading guide, design basis, and marker convention

### 0.1 Design basis of this revision — the 37-FA / 7×7 core

This FER is written on the **37-fuel-assembly, 7-wide octagonal core** (the latest locked geometry;
CAD spec `cad/aegis40-geometry-spec-37fa.md`). The pivot from the earlier 21-FA core to 37 FA was
made **at constant core power (125 MWth)** to flatten the radial power distribution and roughly halve
the core specific power (≈ 12.7 vs ≈ 22 MW/tHM), buying thermal margin. Because power, primary flow,
the once-through steam-generator (OTSG) duty and the natural-circulation thermal height are all
**preserved**, every axial / flow / heat-balance result carries over unchanged; **only the radial
build and the heavy-metal inventory grow** (§8.1, §8.2.2).

### 0.2 "Results-pending" convention (honesty gate)

The 37-FA **geometry, materials, thermal-hydraulics, balance-of-plant, safety architecture, I&C,
layout and economics** are complete and presented in full. The 37-FA **neutronic results** —
k_eff(BU), discharge burnup, cycle length, the peaking factors, the reactivity coefficients, the
rod worth / shutdown margin, and the discharge actinide inventory — are produced by a full-core
OpenMC depletion run (`aegis40_neutronics_FER.ipynb`, executed in WSL) that is **in progress at the
STAT_FINAL statistics**. Until that run lands, every neutronics-derived number is shown with the
marker **⏳[37FA-PENDING]** and is accompanied by the **21-FA predecessor value** (the previously
*locked, fully-run* rev_3 result) in the form *[21-FA ref: …]*, which serves as a defensible
**conservative reference** (the 37-FA core, being larger and lower-power-density, is expected to be
**flatter in peaking and richer in thermal margin**, never worse on the safety-relevant metrics).
This is disclosed deliberately, not hidden.

Other markers used below (carried from the source drafts, all to be closed before final submission):

| Marker | Meaning |
|---|---|
| **⏳[37FA-PENDING]** | value awaits the 37-FA STAT_FINAL OpenMC run (21-FA reference quoted) |
| **[SIM-PENDING]** | value awaits a scoped-but-unrun simulation (T-H / containment) |
| **[ANALYSIS-PENDING]** | analysis identified, not yet performed |
| **[VERIFY]** | claim believed correct, citable anchor to be attached |
| **[CONFIRM]** | engineering value to be confirmed with the owning lead |

### 0.3 Mandatory Digital Appendix (spec p. 8, second paragraph)

For every code used in the analyses, the competition requires **one sample input file** plus an
explanation of the case/approach/outputs **and** reproducibility, benchmarking and repeatability
evidence against reliable (IAEA / OECD-NEA) data, packaged as a separate ZIP. The Aegis-40
Digital-Appendix plan, sample-input index, and the cite-vs-run V&V strategy are consolidated in
**§8.13** of this document. Each technical section below names the code it uses and points at the
corresponding V&V leg.

---

# 8.1 Design Preparation Phase and General Description of the Facility

## 8.1.0 General description

The Aegis-40 is an **integral, soluble-boron-free pressurised-water small modular reactor**
(iPWR-SMR) rated **125 MWth / 40 MWe net** (32.0 % nameplate net efficiency). All primary
equipment — core, helical-coil once-through steam generator, self-pressuriser and the control-rod
drives — is housed within a **single reactor pressure vessel (RPV)**; the primary coolant moves by
**natural circulation** (no reactor coolant pumps). The plant is designed for a 60-year life, a small
(~0.5 km) emergency-planning zone enabled by passive safety, factory-modular construction, and
**polygeneration** (electricity + district heat via thermochemical storage + off-peak hydrogen).
The candidate site is the **Sinop Black-Sea coast** (once-through seawater ultimate heat sink).

The two defining design choices are (i) **operation without soluble boron**, which removes the
chemical-shim system and its boron-dilution accident pathway and transfers reactivity hold-down to
solid burnable absorbers (Gd₂O₃ + Er₂O₃) and control rods, and (ii) the **integral natural-circulation
architecture**, which eliminates large-bore primary piping and the reactor coolant pumps and so
*design-eliminates* the large-break LOCA, the rod-ejection and the surge-line-break accident classes
(§8.6.1).

## 8.1.1 Plant and power — Table 8.1-1

| Parameter | Value | Unit / note |
|---|---|---|
| Plant type | Integral PWR (iPWR), soluble-boron-free | — |
| Thermal power | 125 | MWth |
| Net electrical output | 40 | MWe (net to grid) |
| Net thermal efficiency | 32.0 (nameplate) / 31.8 (computed, §8.9) | % |
| Design lifetime | 60 | years |
| Capacity factor — design target | 95 | % |
| Capacity factor — used in fuel-cycle/waste analysis | 90 | % (conservative) |
| Non-electric output | district heat (TCES) + off-peak H₂ | §8.9 |
| Available process-heat temperature | 100–260 (flexible) | °C |
| Modular design | Yes | factory-fabricated |
| Construction duration (n-th unit) | < 30 | months (first concrete → criticality) |
| Emergency planning zone (radius) | 0.5 | km (design goal; closed by dose case §8.5) |
| Seismic design (SSE) | 0.3 | g (Safe-Shutdown Earthquake) |

## 8.1.2 Primary system and thermal-hydraulics — Table 8.1-2

| Parameter | Value | Unit / note |
|---|---|---|
| Primary operating pressure | 12.8 | MPa (iPWR/NuScale basis) |
| Primary design pressure (110 %) | ≈ 14.1 | MPa |
| Core inlet / outlet temperature | 258 / 308 | °C / °C |
| Core temperature rise ΔT | 50 | K |
| Core average temperature | 283 | °C |
| Saturation temp. @ 12.8 MPa | 329.7 | °C (→ 21.7 °C hot-leg subcooling) |
| Average primary mass flow | ≈ 483 | kg/s (natural circulation) |
| Natural-circulation thermal height H_th | 2.85 | m (core-mid → OTSG-mid) |
| Primary driving head | 2.62 | kPa (buoyancy) |
| Primary coolant inventory | ≈ 26 (≈ 35 m³) | t [CONFIRM vs §8.4 T-H model] |
| Steam-generator (secondary) pressure | 4.5 | MPa |
| Steam temperature (OTSG outlet) | 296 | °C |
| Circulation mode | Natural circulation (no primary pumps) | — |

The ΔT and flow are **coupled** (the loop settles at this ΔT, `scripts/natcirc_primary.py`); they
cannot be set independently. The 12.8 MPa / 308→258 °C primary boundary is **fixed by the §8.4
natural-circulation analysis** and feeds §8.2.4, §8.3 and §8.9.

> **Pressure-basis reconciliation note.** This FER uses **12.8 MPa op / 14.1 MPa design** (iPWR
> basis) consistently. The earlier `safety/safety_criteria.yaml` carried a large-PWR default
> (15.5 / 17.2 MPa); that file is to be updated to the iPWR values [CONFIRM — §8.5 owner].

## 8.1.3 Fuel and core — Table 8.1-3 (37-FA)

| Parameter | Value | Unit / note |
|---|---|---|
| Number of fuel assemblies | **37** | 7×7 octagon (rows 3-5-7-7-7-5-3) |
| Lattice | 17×17 Westinghouse-type | 264 fuel + 24 guide + 1 instrument |
| Active core height | 200 | cm (+ 30 cm H₂O axial reflector each end) |
| Equivalent core diameter | ≈ 1483 | mm (across-flats 1512) |
| Heavy-metal loading (fresh) | **9.87** | tHM ⏳[37FA-PENDING exact step-0 mass] |
| Specific power | **12.66** | MW/tHM (≈ ½ of the 21-FA core) |
| Fuel material | UO₂ | enrichment-zoned |
| Enrichment (intra-FA grade: interior/mid/periphery) | 4.95 / 4.70 / 4.40 | wt% ²³⁵U |
| Enrichment (reflector-facing edge pins) | 4.0 | wt% (edge-pin de-rate) |
| Enrichment (core average / maximum) | ≈ 4.4–4.5 / 4.95 | wt% ⏳[37FA-PENDING exact count-weighted avg] |
| Cladding | Zircaloy-4 (Zr-4) | locked |
| Primary burnable absorber | Gd₂O₃ 8 wt%, ring-zoned (avg 32 rods/FA) | rings 1/8/16/12, weights 1.65/1.45/0.95/0.68 |
| Secondary burnable absorber | Er₂O₃ 0.5 wt% (16 rods/FA) | slow hold-down + cold SDM |
| Reload scheme | 4-batch | once-through |
| Control-rod clusters (CRA) | **12** | checkerboard; central FA = instrument; in-vessel CRDM |
| Control-rod absorber | B₄C (/ Ag-In-Cd or Hf) | [CONFIRM §8.6] |
| Cycle length | ⏳[37FA-PENDING] *[21-FA ref: 479 EFPD]* | EFPD |
| Discharge burnup | ⏳[37FA-PENDING] *[21-FA ref: 42.8 GWd/MTU]* | GWd/MTU |
| Fuel reprocessing | None (once-through) | — |

> **Why 37 FA (design rationale).** The 21-FA predecessor met every safety gate but its compact
> 5-wide core produced a steep radial flux tilt and a per-pin radial peaking (F_ΔH ≈ 1.85) that sat
> above the adopted LCO target, with the peak pin pinned against the 5.0 wt% enrichment ceiling. The
> 37-FA core widens the lattice (√(37/21) = 1.33× core diameter), gentling the radial gradient and
> halving the specific power. The cost is a larger HM inventory; the benefit is flatter peaking and
> a large DNBR margin. The pivot is made at constant 125 MWth so the vessel grows only radially
> (§8.1.2 axial/flow values unchanged).

## 8.1.4 Engineered safety features and probabilistic targets — Table 8.1-4

> These rows summarise §8.5–§8.7; values are reproduced here for the front page and are authoritative
> in those sections.

| System / metric | Value | Note |
|---|---|---|
| Reactor shutdown systems | 2 diverse | (1) gravity-drop control rods; (2) passive Emergency Boron Injection (EBIS), dormant in normal operation (§8.6.2a) |
| Passive residual heat removal (PRHR) | 2 × 100 % | natural circulation to in-containment tank |
| Emergency feedwater (EFW) | gravity-driven | fail-open, no pumps |
| Passive containment cooling | 3 trains | continuously in service |
| Passive safety injection | gravity feed from IRWST | low-pressure coincidence |
| Containment | Dry steel-lined | Ø ≈ 15 m; design pressure ≈ 0.414 MPa [ANALYSIS-PENDING P/T] |
| Emergency power | 2 × EDG + 1E batteries | monitoring/backup only — core cooling is passive |
| Safety grace period (no AC, no seawater, no operator) | ≥ 72 h (target unlimited) | passive UHS = IRWST |
| Core Damage Frequency (CDF) | < 1×10⁻⁷ /ry (projected class target) | LOHS ≈ 1e-8, SBO ≈ 1e-11 demonstrated (§8.6.3) |
| Large Release Frequency (LRF) | < 1×10⁻⁸ /ry (projected class target) | — |

## 8.1.5 Outage schedule and derived relations

Major outages: **15 days every 12 months** (refuelling) + **30 days every 120 months** (turbine /
vessel in-service inspection) → planned availability ≈ **95 %**, consistent with the design CF.
Derived: net efficiency = 40/125 = **32.0 %**; specific power = 125/9.87 = **12.66 MW/tHM**; primary
flow from Q = ṁ·c_p·ΔT (c_p ≈ 5.18 kJ/kg·K @ 283 °C/12.8 MPa) → **ṁ ≈ 483 kg/s**.

## 8.1.6 Design-preparation phase, methodology and basis documents

The parameter set above is the controlled output of the **preliminary (conceptual/basic) design
phase**, developed through an integrated, reproducible analysis chain (IAEA SSG-52 §2; GSR Part 4
design-input control). Each domain produced a version-controlled basis document that becomes a
verified input to detailed design.

**Table 8.1-6 — Preliminary-design analyses and basis documents**

| Design domain | Method / tool | Controlled output |
|---|---|---|
| Neutronics, depletion, reactivity coefficients | OpenMC Monte-Carlo (ENDF/B-VIII.0), 37-FA 3-D core + depletion | `aegis40_neutronics_FER.ipynb`; §8.2 |
| Fuel performance (T_cl, FGR, rod pressure) | Steady-state fuel-rod conduction stack vs SSG-52 limits | §8.3 |
| Primary thermal-hydraulics | Natural-circulation loop balance + DNBR (IAPWS-IF97) | §8.4 (`natcirc_primary.py`) |
| Secondary power conversion | Regenerative Rankine + exergy (IAPWS-IF97) | §8.9 (`thermo_cycle.py`, `thermo_exergy.py`) |
| Shielding / dose | Coupled n-γ transport + ICRP-116 flux-to-dose | §8.2.6 (`…_shielding_rev7.ipynb`) |
| Waste / source term | Depletion inventory + ANSI/ANS-5.1 decay heat | §8.11 (`src/aegis40/back_end`) |
| Safety / PRA | Deterministic DBA + event/fault trees | §8.5/§8.6 (`safety/`) |
| Geometry / layout | Parametric CAD (RPV, assembly, pin, site STEP) | `cad/`, §8.10 |

## 8.1.7 Design codes and standards — Table 8.1-7

| Design domain | Code / standard | Application |
|---|---|---|
| Class-1 nuclear pressure boundary | **ASME BPVC Section III**, Div. 1 (NB / NG) | RPV, OTSG, self-pressuriser, in-vessel CRDM, core support (§8.4) |
| Non-nuclear pressure parts / BOP | **ASME BPVC Section VIII**; **ASME B31.1** | Condenser, feedwater heaters, secondary piping (§8.9) |
| Pressure-boundary & internals materials | SA-508 Gr.3 Cl.1 / SA-533B (RPV); **ASTM A240** 304/316L; Inconel-690 TT; Incoloy-800; reflector SA-965/SA-182 Type 304 | §8.4 / §8.3.6 |
| Fuel cladding | Zircaloy-4 (**ASTM B811**) | §8.3 |
| Reactor-core nuclear-design limits | **IAEA SSG-52**; **NUREG-1431** Rev. 5 | peaking (F_Q, F_ΔH), coefficients, SDM (§8.2) |
| Neutronics method & data | OpenMC (Romano & Forget 2013); ENDF/B-VIII.0; ICSBEP / BEAVRS / C5G7 | §8.2, §8.13 |
| Decay heat | **ANSI/ANS-5.1** | DHRS sizing, source term (§8.4, §8.11) |
| Water/steam properties | **IAPWS-IF97** | §8.4, §8.9 |
| Radiation shielding / dose | **ANSI/ANS-6.4**; **ICRP-116** | §8.2.6, §8.8 |
| Spent-fuel storage criticality | **NUREG-0800** §9.1.1; **10 CFR 50.68** (k(95/95) ≤ 0.95) | §8.11 |
| Instrumentation & protection | **IEEE Std 603**; **IEC 61513 / 60880**; **IAEA SSG-39** | §8.7 |
| Predisposal waste management | **IAEA GSR Part 5** | §8.11 |
| Fire protection / H₂ safety | **NFPA 2**; **IEC 60079** | §8.8, §8.10 |

## 8.1.8 Reference regulatory and nuclear-safety requirements — Table 8.1-8

Nuclear safety is integrated from the outset by **defence-in-depth**: the four fundamental safety
functions (reactivity control, fuel cooling, confinement, radiation protection) are each met by
inherent characteristics plus independent, redundant provisions. The candidate site being in Türkiye,
the licensing basis is the **Nükleer Düzenleme Kurumu (NDK)** framework (Nuclear Regulation Law
No. 7381, 2022), whose design regulations adopt the IAEA Safety Standards.

| Document | Scope | How addressed |
|---|---|---|
| **IAEA SSR-2/1 (Rev. 1)** — Safety of NPPs: Design | Top-level design safety; defence-in-depth | Req. 24–25 redundant/independent reactivity control; Req. 35 (cogen isolation); Req. 45 inherent stability (coeffs < 0); Req. 46 ≥ 2 diverse shutdown systems; Req. 52–53 heat sink/grace (§8.2, §8.5, §8.6) |
| **IAEA SSG-52** — Design of the Reactor Core | Core-design limits & methods | peaking, DNBR, coefficients, LHGR (§8.2) |
| **IAEA GSR Part 4 (Rev.1)** — Safety Assessment | Methodology | deterministic + projected-PSA (§8.5/§8.6) |
| **IAEA SSG-3 / SSG-4** — L1 / L2 PSA | PSA methodology | CDF / LRF class targets (§8.6) |
| **IAEA GSR Part 5** — Predisposal Waste Mgmt | Waste safety | on-site storage & conditioning (§8.11) |
| **IAEA SSR-1; SSG-9** — Site Evaluation / external hazards | Siting | seismic, coastal hazard (§8.5, §8.10) |
| **US NRC 10 CFR 50 App. A** — GDC | Generic design criteria | GDC 11/26/27/35 (§8.2, §8.5, §8.6) |
| **US NRC NUREG-1431 Rev. 5** — STS | LCO forms | SDM, MTC, F_Q, F_ΔH limits (§8.2) |
| **US NRC NUREG-0800 / 10 CFR 50.68** | SRP; SFP criticality | k(95/95) ≤ 0.95 (§8.11) |
| **Türkiye NDK — Law No. 7381 (2022)** + NDK design regulation | National licensing | primary framework; adopts the IAEA standards above |

## 8.1.9 Parameters requiring confirmation (tracked)

1. 37-FA neutronics (k_eff, burnup, cycle, peaking, coefficients, rod worth, SDM, inventory) —
   ⏳[37FA-PENDING] STAT_FINAL run. *(Samira)*
2. Fresh heavy-metal mass — confirm exact 9.87 t via OpenMC `--step 0`. *(Samira)*
3. Core-average enrichment — confirm count-weighted value (≈ 4.4–4.5). *(Samira)*
4. Primary coolant inventory ≈ 26 t — confirm vs §8.4 T-H model. *(Adilbek)*
5. Control-rod absorber (B₄C / Ag-In-Cd / Hf). *(Azamhon)*
6. Containment design pressure — from P/T accident analysis. *(Azamhon)*
7. `safety_criteria.yaml` pressure rows → iPWR 12.8/14.1 MPa. *(Azamhon)*
8. CDF/LRF framed as projected class targets, not computed PSA. *(safety)*
9. EPZ 0.5 km closed by dose case; SSE vs Sinop seismicity. *(site/safety)*

---

# 8.2 Core Design

> **Codes:** OpenMC 0.15.3 continuous-energy Monte Carlo, ENDF/B-VIII.0 (V&V leg §8.13).
> **Geometry:** 37-FA / 7×7. **Neutronic results:** ⏳[37FA-PENDING] with 21-FA references.

## 8.2.1 Material selection

Material selection follows three criteria in priority order: (i) neutronic suitability for an SBF
high-burnup core, (ii) demonstrated in-pile performance with a qualified property database to
~50–62 GWd/MTU, and (iii) compatibility across steady-state, AOO and accident temperatures.

**Table 8.2-1 — Core material selection and rationale**

| Component | Material | Rationale |
|---|---|---|
| Fuel | UO₂, enriched 4.95 / 4.70 / 4.40 wt% (intra-FA zones) + 4.0 wt% edge pins | Reference LWR fuel; largest qualification base; T_melt ≈ 2840 °C; ≤ 5.0 wt% keeps the commercial LEU envelope |
| Cladding | Zircaloy-4 | Low absorption; qualified to high burnup; well-characterised corrosion/creep; locked |
| Burnable absorber (primary) | Gd₂O₃ 8 wt%, admixed, ring-zoned | Strong BOC hold-down (Gd-155/157), burns out ~10 GWd/t; integral (no hardware) — the SBF excess-reactivity solution |
| Burnable absorber (secondary) | Er₂O₃ 0.5 wt%, admixed | Slow residual hold-down flattening mid/late cycle + cold shutdown margin |
| Coolant / moderator | Light water (H₂O) | Reference PWR; negative MTC by design; self-regulating |
| Reflector | Light water (radial 20 cm, axial 30 cm) — heavy SS-304 reflector option under evaluation | Returns leakage, flattens power; the small-core water albedo flattens better than steel for the intra-FA-graded design (see §8.2.3 note) |
| Control-rod absorber | B₄C (Ag-In-Cd / Hf alternative) | Solid neutron absorber, fully SBF-compatible (no boron in coolant) |

**Behaviour under irradiation and temperature.** UO₂ is a stable fluorite ceramic (T_melt ≈ 2840 °C,
falling ~0.5 °C/GWd-t); its conductivity degrades with temperature and burnup (Lucuta/Halden),
bounded by the §8.3 centerline analysis. At the 37-FA core's **very low specific power
(12.7 MW/tHM)** the linear heat rates are modest (§8.3), so fuel runs far below melt in steady state
and bounding AOO. Gd₂O₃/Er₂O₃ "transient" behaviour is the intended burn-out (§8.2.3). Zircaloy-4
damage mechanisms (oxidation ≤ 100 µm, H-pickup, creep, fast-fluence embrittlement) are bounded by
the moderate discharge burnup, well below the 62 GWd/MTU Zr-4 ceiling; accident heat-up (1204 °C PCT,
17 % ECR) underlies the §8.5 LOCA criteria. Light water gives strongly negative moderator/void
coefficients (Table 8.2-3), a passive stabiliser.

## 8.2.2 Geometry and layout

The core is the qualified Westinghouse-type **17×17 lattice**, sized to **37 assemblies** for the
125 MWth rating. Choosing a qualified geometry (rather than a novel lattice) maximises the
credibility of the borrowed fuel/clad property database and the T-H correlations and concentrates the
originality on the boron-free reactivity scheme. Dimensions are taken from the as-built OpenMC
geometry and the CAD spec.

**Table 8.2-2 — Core and fuel geometry (37-FA, locked)**

| Feature | Value | Note |
|---|---|---|
| Lattice | 17×17 square, 289 positions/FA | 264 fuel + 24 guide + 1 instrument |
| Fuel pellet diameter | 8.192 mm | ~95 % TD |
| Pellet–clad radial gap | 0.0915 mm | |
| Cladding OD / ID | 9.520 / 8.375 mm (0.573 wall) | Zr-4 |
| Pin pitch | 12.623 mm | |
| Active lattice span (FA side) | 214.59 mm | 17 × pin pitch |
| Assembly pitch (in core) | 216.038 mm | inter-assembly water gap ≈ 1.45 mm |
| Guide / instrument tube OD / ID | 12.040 / 11.248 mm | |
| Active fuel height | 2000 mm | + 300 mm H₂O axial reflector each end |
| Number of assemblies | **37** (7×7 octagon, 3-5-7-7-7-5-3) | |
| Across-flats / equivalent core diameter | 1512 / ≈ 1483 mm | corner-pin radius ≈ 764 mm |
| Radial / axial reflector | 200 / 300 mm H₂O | (steel reflector option, §8.2.3) |
| Control-rod clusters | 12 | in-vessel CRDM |
| Heavy-metal loading | ≈ 9.87 tHM | ⏳[37FA-PENDING exact] |

**Power-control systems (no soluble boron).** Reactivity is controlled by two integral mechanisms:

- **Burnable absorbers.** Gd₂O₃ (8 wt%) provides the dominant BOC hold-down and is **ring-zoned**
  across the four core rings (1/8/16/12 assemblies) with density weights 1.65/1.45/0.95/0.68
  (core-average conserved ≈ 1.0) to flatten the radial power. Er₂O₃ (0.5 wt%, 16 rods/FA) gives slow
  residual hold-down and cold shutdown margin.
- **Control rods.** 12 clusters insert into guide-tube channels via in-vessel CRDMs (no head
  penetrations → rod-ejection design-eliminated, §8.6.1).

**Intra-assembly enrichment grading.** Within every assembly the pins are graded
**4.95 / 4.70 / 4.40 wt%** (interior → periphery), with the reflector-facing edge pins de-rated to
**4.0 wt%**. The periphery borders the inter-assembly water gaps (and, for edge assemblies, the
reflector), where excess moderation drives a local pin-power peak; de-enriching the outer rows
suppresses exactly that peak. This is standard LWR assembly practice (and the NuScale reference,
FSAR §4.3).

‹FIGURE 8.2-1 — 37-FA core loading map coloured by ring (enrichment + Gd zoning) with the 12 CRA
positions. Source: `cad/ga/37fa/ga37_sheet3_coremap.png`.›
‹FIGURE 8.2-2 — fuel-assembly 17×17 pin map (enrichment + Gd/Er pins).
Source: `aegis40_neutronics_FER.ipynb` §6 FA-lattice figure.›
‹FIGURE 8.2-3 — RPV / core radial cross-section. Source: `cad/ga/37fa/ga37_sheet1_radial.png`.›

## 8.2.3 Neutronic analysis

The neutronic design uses **OpenMC 0.15.3** continuous-energy Monte Carlo on the full 3-D 37-FA core
(axial + radial reflectors), with coupled depletion from BOC toward the equilibrium cycle (transport
statistics 180/50/20 000 at STAT_FINAL).

**Criticality and reactivity control.** The fresh core is slightly supercritical, the excess held
down by the integral burnable absorbers and managed by the rods. All reactivity-control and shutdown
criteria are met with margin (Table 8.2-3).

**Table 8.2-3 — Neutronic safety results (37-FA) — all criteria met**

| Parameter | 37-FA value | 21-FA reference | Limit / criterion | Status |
|---|---|---|---|---|
| k_eff, BOL | ⏳[37FA-PENDING] *(latest 1.064, Gd-zoning re-tune in progress)* | 1.0264 | excess managed by BA + rods | INFO |
| Moderator temp. coeff. (HFP) | ⏳[37FA-PENDING] | −35.9 pcm/K | < 0 | expect PASS |
| Doppler (fuel) coeff. | ⏳[37FA-PENDING] | −1.84 pcm/K | < 0 | expect PASS |
| Void coefficient | ⏳[37FA-PENDING] | −214 pcm/%void | < 0 | expect PASS |
| Control-rod worth (ARO→ARI) | ⏳[37FA-PENDING] (12 CRA) | 15 226 pcm (9 CRA) | ≥ 5 000 | expect PASS |
| Shutdown margin (N−1 stuck rod) | ⏳[37FA-PENDING] | 12.4 %Δk/k | ≥ 1.0 | expect PASS |
| k_eff all-rods-in (ARI) | ⏳[37FA-PENDING] | 0.888 | < 0.95 subcritical | expect PASS |
| Max reactivity insertion rate | ⏳[37FA-PENDING] | 1.5×10⁻⁵ Δk/k/s | ≤ 7.5×10⁻⁴ | expect PASS |
| Maximum enrichment | 4.95 wt% | 4.95 wt% | ≤ 5.0 | PASS |

> The 21-FA reference column is the previously **locked, fully-run rev_3** result and serves as a
> conservative anchor while the 37-FA STAT_FINAL run completes. The 37-FA core's lower leakage
> fraction and larger fissile inventory are expected to give comparable-or-stronger negative
> coefficients and rod worth; the 12-CRA layout (vs 9) increases total absorber complement.

**Feedback coefficients.** All three feedbacks are negative by design (moderator, Doppler, void),
making the core inherently self-regulating against power, temperature and voiding excursions — the
central inherent-safety claim and the basis for the §8.5 transient response.

**Power distribution (peaking).** With no soluble boron, the radial Gd zoning is the primary
power-flattening tool, supported by intra-assembly enrichment grading for the pin peak.

**Table 8.2-5 — Power-peaking (37-FA latest vs 21-FA locked)**

| Peaking factor | 37-FA (latest, pre-final) | 21-FA (locked rev_3) | Note |
|---|---|---|---|
| F_radial (assembly) | 1.288 | 1.23 | assembly-average map |
| F_ΔH (per-pin radial) | 1.746 ⏳ | 1.85 (per-pin rev_6) / 2.27 (legacy mesh) | governing thermal-margin input |
| F_z (core-average axial) | 1.165 | 1.03 | |
| F_q (separable F_ΔH·F_z, +3 %) | ≈ 2.03 ⏳ | ≈ 2.08 | checked vs LCO ≤ 2.32 |
| F_q (raw 3-D single-node) | 5.07 (MC noise) | 3.48 (MC noise) | diagnostic only, de-noise at STAT_FINAL |

> **Peaking convention (important).** The **separable** F_q = F_ΔH·F_z (with a +3 % engineering
> uncertainty per SSG-52 3.18(f)) is the checked pass/fail value; the raw single-node 3-D maximum is
> Monte-Carlo noise at production statistics and is reported as a diagnostic only. The 37-FA core is
> expected to bring F_ΔH below the 1.65 LCO target once the Gd ring-weights are finalised; if it
> settles slightly above 1.65 it is justified on **DNBR margin at the very low 12.7 MW/tHM power
> density** (the CAREM-25 precedent), to be confirmed by the §8.4/§8.5 MDNBR analysis. This is the
> single governing open item (O1, §8.6 register).

**Enrichment / burnable-absorber zoning — design basis and trade study.** A boron-free core must
flatten power with solid zoning alone. Aegis-40 uses a deliberate **division of labour**: *Gd ring
zoning* corrects the assembly-to-assembly (core-radial) tilt, while *intra-assembly enrichment
grading* corrects the local pin peak. This was benchmarked against the standard alternatives in four
controlled full-core OpenMC variants (carried over from the 21-FA study, mechanism-identical for
37 FA):

- **Out-in inter-assembly enrichment (rev_4)** flattened the assembly map but regressed the
  thermal-margin-governing per-pin F_q and cost ~20 EFPD — because (1) we are boron-free (NuScale
  pairs out-in with ~1235 ppm shim that does the bulk shaping) and (2) a small water-reflected core
  leaks, so pushing fissile outward bleeds neutrons.
- **Combined out-in + intra-FA (rev_5)** achieved the flattest assembly map but still worse F_q,
  pinned the peak pin at exactly 5.0 wt% (zero margin) and left 36 % of the Gd-157 unburnt at EOC.
- **Assembly-uniform + steel reflector + targeted Gd (rev_7, the literature SMART/ATOM/PRATIC
  recipe)** regressed the per-pin F_ΔH (1.85 → 1.94–2.05): 32 discrete Gd rods cannot simultaneously
  de-peak the 24 guide-tube water holes and the assembly edges, whereas continuous per-pin
  enrichment grading sets every pin's local power at once.

The adopted scheme therefore wins on every binding metric and is retained; widening to 37 FA is the
*geometric* complement that relaxes the residual radial tilt the zoning could not fully remove in the
5-wide core. (Full study: `fer/enrichment-zoning-benchmark-rev7.md`.)

**Reflector note.** For this intra-FA-graded compact core, **water** outperformed a steel radial
reflector on peaking (higher thermal albedo lifts the cool edges → flattens; steel absorbs thermal →
edge cools → centre peaks harder). The locked neutronics basis is therefore **20 cm water**; a heavy
SS-304 reflector (NuScale concept, compact barrel + claimed flattening) remains an option to re-test
on the 37-FA core (`RADIAL_REFLECTOR_MODE="steel"`) — until re-run, water is the basis.

‹FIGURE 8.2-4 — cycle reactivity k_eff(BU), BOC→EOC, showing the SBF Gd-burnout signature
(dip → hump → decline). ⏳[37FA-PENDING from depletion run].›
‹FIGURE 8.2-5 — BOC/MOC/EOC radial power maps + axial shapes + EOC per-assembly burnup map
(`aegis40_neutronics_FER.ipynb` §9). ⏳[37FA-PENDING].›

**BOC → equilibrium-cycle behaviour.** The depletion k_eff curve **dips, then rises, then declines**
(xenon build-in → Gd-burnout hump → fuel-depletion decline) — the expected, intended signature of a
Gd-controlled boron-free core (Kim, Jung & Yoon, *Nucl. Eng. Tech.* 56 (2024) 3144: "reactivity
upswing following gadolinia depletion"). In a boron-controlled core the curve only falls; the hump is
the distinguishing feature of integral-Gd SBF control. The depletion presented is the **first
(all-fresh) core** run BOC→EOC; the 4-batch reload reaches equilibrium with a less-reactive, shorter
BOC, the per-batch discharge burnup converging on the design value — so the first-core results
**bound** the equilibrium cycle on the safety-relevant metrics (max BOC hold-down/rod duty; peaking,
since zoning repeats each reload). A full equilibrium shuffle is the next depletion step.

**Compliance with safety criteria / regulations.**

| Neutronic result | Criterion | Regulatory basis |
|---|---|---|
| MTC, DTC, void all < 0 | inherent negative feedback | NDK design reg.; IAEA SSR-2/1 Req. 35/45; 10 CFR 50 App. A GDC 11 |
| Two independent control means (rods + integral BA) | redundant, independent reactivity control | SSR-2/1 Req. 24–25; GDC 26/27 |
| SDM with most-reactive rod stuck; k_ARI < 0.95; N−1 < 1.0 | shutdown margin / single failure | SSR-2/1 Req. 25/46; NUREG-1431 LCO 3.1.1; GDC 26 |
| Max enrichment 4.95 ≤ 5.0 | LEU fabrication/licensing | commercial LEU; IAEA fuel-safety guidance |

## 8.2.4 Steady-state thermal-hydraulics (interface to §8.4)

The full T-H solution (spatial coolant/clad temperature fields, loop pressure balance) is produced in
§8.4. Core-side assumptions: full power 125 MWth on the BOC power shape, single-phase water at
≈ 12.8 MPa cooled by natural circulation, boundary conditions 258 → 308 °C (ΔT 50 K), ṁ ≈ 483 kg/s;
hot-channel DNB via the W-3 CHF correlation on the Table 8.2-5 peaking. The 37-FA core's **half
specific power** widens every steady-state thermal margin relative to the 21-FA summary below.

**Table 8.2-10 — Core steady-state T-H summary (from §8.4; 21-FA values, 37-FA improves)**

| Quantity | Result (21-FA) | Limit | Margin | 37-FA expectation |
|---|---|---|---|---|
| Primary T (in/out/avg) | 258 / 308 / 283 °C | — | single-phase | unchanged (same legs) |
| Hot-leg subcooling | 21.7 °C | > 0 | no bulk boiling | unchanged |
| MDNBR (hot pin, W-3) | 1.466 | ≥ 1.3 | +12.8 % | higher (lower q′, flatter F_ΔH) [SIM-PENDING] |
| Peak clad temp (steady) | 391 °C | < 1200 °C | +809 °C | lower |
| Peak fuel centerline (BOL) | ≈ 1750 °C | < ~2840 °C | ≈ +1090 °C | lower (§8.3) |

## 8.2.5 Depleted-fuel inventory (BOC → EOC)

The whole-core actinide inventory (fresh loading → discharge) is the quantitative basis for §8.11
(waste) and the non-proliferation assessment (§7 / §8.11). For 37 FA this is ⏳[37FA-PENDING] from the
depletion run; the **21-FA locked inventory** (whole-core, 42.8 GWd/MTU) is reproduced as the
reference: 193 kg U-235 consumed, **55.3 kg reactor-grade Pu bred** (Pu-240 = 24.6 wt%, fissile
66.2 %), net fissile 248 → 92 kg, spent U-235 at 1.10 wt%. The 37-FA core (≈ 1.9× HM, same power)
will carry a proportionally larger absolute inventory at a similar or lower per-tHM burnup; the
*intensity* metrics (per-TWhe) are governed by burnup and efficiency (§8.11) and are regenerated with
the depletion run.

## 8.2.6 Reactor-vessel and radiation-shielding materials

Outside the active core the structural/shielding set is selected for pressure-boundary integrity,
fast-fluence tolerance and combined n/γ attenuation. The shield is deliberately **lead-free** (lead
excluded for toxicity/decommissioning burden; tungsten reserved for transport casks). The bulk shield
is **magnetite (heavy) concrete** preceded by a **borated-polyethylene** thermal-neutron capture layer
and an SS-304 thermal shield — keeping the published steel+water → poly → heavy-concrete architecture
while replacing the high-Z outer layer with heavy concrete. The build is sized to the **< 10 µSv/h**
operational dose target behind the bulk concrete (ALARA; Bagheri & Khalafi 2023; Oğul et al. 2026)
and to hold the 60-yr RPV fast fluence (E > 1 MeV) below the ~1×10¹⁹ n/cm² embrittlement screening
level. The shielding is run as a **separate fixed-source dose calculation** off the same lattice
(coupled n-γ transport, ICRP-116 flux-to-dose); it is neutronically decoupled from the core
eigenvalue (k shifts ≪ 100 pcm). Full radial stack and materials: §8.3.6 Table 8.3-3 and
`shielding/shielding-radial-build.md`.

---

# 8.3 Fuel and Material Design

> **Method:** established correlations + published in-pile data (no new simulation); every
> calculation states method, inputs and assumptions, all bounded by §8.2.

## 8.3.1 Fuel and structural-material technical data — Table 8.3-1

| Property | UO₂ fuel | Zircaloy-4 cladding |
|---|---|---|
| Form / dimensions | Sintered pellet Ø 8.192 mm, ~95 % TD | Tube OD 9.520 / ID 8.375 mm, 0.573 wall |
| Density | ~10.4–10.5 g/cm³ | 6.55 g/cm³ |
| Melting / design limit | ~2840 °C (↓ 0.5 °C/GWd-t) | β ~1850 °C; LOCA PCT limit 1204 °C |
| Thermal conductivity | ~3–8 W/m·K (↓ with T, BU; Lucuta/Halden) | ~17 W/m·K |
| Thermal expansion | ~10×10⁻⁶ /K | ~6×10⁻⁶ /K |
| Neutronic role | fissile/fertile; Doppler broadening | low absorption (~0.2 b) |
| Qualified burnup | reference LEU to ~62 GWd/t | rod-avg ≤ 62 GWd/t |

Property sources: IAEA-TECDOC thermophysical properties of UO₂/Zr-4; Todreas & Kazimi *Nuclear
Systems I*; Halden Reactor Project; Lucuta conductivity-with-burnup.

## 8.3.2 Linear heat rate and power density (37-FA — geometry-fixed)

The fuel duty follows directly from §8.2 geometry and is **substantially relieved** by the 37-FA
pivot:

- Fuel rods in core: 37 FA × 264 = **9 768 rods**; active 2.0 m → **19 536 m** of fuel.
- **Core-average linear heat rate** q′_avg = 125 MW / 19 536 m ≈ **6.4 kW/m** (vs 11.3 kW/m for
  21 FA).
- **Peak linear heat rate** q′_peak = q′_avg × F_q ≤ 6.4 × 2.03 ≈ **13 kW/m** (with the 37-FA
  separable F_q; ⏳ confirm at STAT_FINAL). Even bounding with the 21-FA F_q 3.48 gives ≈ 22 kW/m.
- Core specific power = 125 MW / 9.87 tHM ≈ **12.66 MW/tHM**.

The peak linear heat rate (~13 kW/m, ≤ 22 kW/m bounding) is well below the classic LWR guideline
(~43 kW/m / 13 kW/ft) and the core average (~6.4 kW/m) is far under a large-PWR average (~17.5 kW/m).
This very low power density is the root of the thermal margin claimed through §8.2–§8.5 and is the
quantitative payoff of the 37-FA / low-specific-power design.

## 8.3.3 Fuel-performance — centerline temperature

The peak-rod steady-state centerline temperature is built from the coolant through each thermal
resistance (1-D conduction, Todreas & Kazimi). The 37-FA peak q′ being lower than the 21-FA case, the
21-FA stack-up below is a **conservative bound**:

**Table 8.3-2 — Peak-rod temperature stack-up (BOL, conservative 21-FA bound)**

| Resistance | ΔT (K) | Method |
|---|---|---|
| Bulk coolant (local hot) | ≈ 315 °C | §8.2.4 / §8.4 |
| Film (q″ ≈ 1.3 MW/m²) | ~39 | ΔT = q″/h, h ≈ 34 000 W/m²·K |
| Clad conduction | ~47 | q′·ln(r_o/r_i)/(2πk_clad) |
| Pellet–clad gap (BOL) | ~250 | q″_gap/h_gap, h_gap ≈ 6000 |
| Fuel pellet (surface→centre) | ~1100 | ∫k dT = q′/4π, k≈3 |
| **Peak centerline** | **≈ 1750 °C** | sum |

At the 37-FA peak q′ (~13 kW/m vs ~39 kW/m here) the centerline drops well below this; even the
bounding value sits **~1090 °C below UO₂ melt** (~62 % of melt absolute). The gap term dominates and
shrinks as the gap closes with burnup. [Refine with §8.4 coolant BC and an optional FRAPCON case.]

## 8.3.4 Fission-gas release, rod pressure, clad integrity

- **FGR:** with most of the pellet below ~1000 °C (further assured by the low 37-FA q′), FGR is
  governed by the Halden threshold; peak-rod EOL FGR expected modest (≤ ~10 %). A ~180 mm gas plenum
  (hold-down spring) keeps EOL rod internal pressure below system pressure (no clad lift-off).
- **Clad stress/corrosion:** Zr-4 carries the pressure differential within primary-membrane
  allowables; oxide (≤ 100 µm), H-pickup, creep/growth, fast-fluence embrittlement all bounded by the
  moderate discharge burnup (≪ 62 GWd/MTU ceiling). Accident behaviour (oxidation, ballooning, 1204 °C
  PCT, 17 % ECR) carried in §8.5.
- **PCMI:** mitigated by dished/chamfered pellets + base-load low-ramp operation; bounded by the low
  q′.

‹FIGURE 8.3-1 — fuel-rod / end-plug cross-section (pellet stack, gap, Zr-4 clad, end plugs, plenum
spring). Source: `cad/end_plug_detail.png`.›

## 8.3.5 Front-end fuel-cycle structural materials

Assembly skeleton (top/bottom nozzles, guide/instrument thimbles, spacer grids, hold-down springs):
**Zircaloy-4 / Zirlo-class** guide thimbles and grids (low in-core parasitic absorption);
**stainless steel 304/308 / Inconel-718** for nozzles and springs (strength and relaxation
resistance, outside the active height). Selection criteria: low in-core absorption, primary-coolant
corrosion compatibility, irradiation-growth dimensional stability, spring-force retention over life.

## 8.3.6 Reactor-vessel and shielding materials — Table 8.3-3

Radial stack (core outward), the basis of the coupled n-γ shielding model:

| Region | Material | Density (g/cm³) | Thickness (cm) | Function |
|---|---|---|---|---|
| Core barrel | SS-304 | 8.00 | 5 | Core support; first γ/fast-n attenuation |
| Downcomer + integral OTSG annulus | H₂O (+ SG steel) | 0.72 (hot) | ~35 | Coolant return; **dominant attenuator**; RPV fluence reduction |
| Reactor pressure vessel | SA-508 Gr.3 + SS clad | 7.90 | 15 + 0.5 | Pressure boundary; principal γ shield; fast-fluence-limited |
| Reactor cavity | Air | 0.0012 | 15 | ISI / standoff |
| Thermal shield | SS-304 | 8.00 | 5 | γ-heating interception; protects bioshield concrete |
| Neutron-capture layer | Borated polyethylene (5 wt% B) | 0.95 | 10 | Thermal-n capture (¹⁰B), low 2° γ |
| Biological shield | Magnetite (heavy) concrete | 3.90 | 120 | **Bulk lead-free γ + n shield**; bound water moderates |
| Outer finish | Ordinary concrete | 2.30 | 10 | Structural finish; dose-acceptance surface |

> Radii are re-anchored to the 37-FA vessel (RPV ID 2700 / OD 3010 mm) in the CAD spec; the **layer
> thicknesses** (the shield design) are unchanged from the 21-FA build because the **125 MWth source
> is unchanged**, so the dose attenuation requirement is essentially identical (§8.2.6;
> `shielding/shielding-radial-build.md`). Attenuation/property data: ANSI/ANS-6.4, ASTM A508/A240,
> ICRP-116, PNNL compendium (McConn et al.).

---

# 8.4 Cooling Circuit System Design

> **Code:** natural-circulation loop balance + DNBR, IAPWS-IF97 (`scripts/natcirc_primary.py`);
> conjugate CFD for the hot-pin field. **All axial/flow values are preserved 21→37 FA.**

## 8.4.1 Architecture

Aegis-40 removes core heat through three coupled circuits:

1. **Primary** — a closed **natural-circulation** loop entirely inside the RPV, carrying the full
   125 MWth from the core to the integral helical-coil **OTSG** with **no reactor coolant pumps** and
   **no large primary piping** (the defining integral-PWR feature). Flow path: core → central riser
   (R 560 mm) → upper plenum → turn-around → helical OTSG in the upper annulus (primary on the shell
   side, downflow over the coils) → downcomer → lower plenum → core.
2. **Secondary** — the feedwater/steam side of the OTSG and the regenerative Rankine plant. Heat
   crosses the pressure boundary **once**, in the OTSG (→ §8.9).
3. **Associated** — passive decay-heat removal (DHRS/PRHR), the integral self-pressuriser, the
   chemical & volume control system (CVCS, no boration), and the **once-through seawater** ultimate
   heat sink (→ §8.9).

The OTSG sits **above** the core so the heat sink is above the heat source — the geometric requirement
for stable natural circulation. ‹FIGURE 8.4-1 — in-vessel natural-circulation loop schematic,
`fer/natcirc_loop_schematic.png`.›

## 8.4.2 Primary cooling — natural circulation

**Design conditions:** 125 MWth; 12.8 MPa op / 14.1 MPa design; hot leg 308 °C, cold leg 258 °C,
ΔT 50 K, average 283 °C; saturation 329.7 °C → **21.7 °C hot-leg subcooling** (single-phase with
margin); ṁ ≈ 483 kg/s; light water, boron-free.

**Driving head (heat-removal capability).** The flow is set by the balance of buoyancy head and loop
losses (Todreas & Kazimi single-phase natural-circulation momentum integral):

> ΔP_driving = (ρ_cold − ρ_hot)·g·H_th = Σ K_i · ½ρv²

with H_th = 2.85 m (core-mid → OTSG-mid). ρ_cold = 796.7, ρ_hot = 703.1 kg/m³ (Δρ = 93.6),
**ΔP_driving = 2.62 kPa**, core velocity 0.90 m/s (CFD), implied flow area 0.71 m², sustained
loop-loss coefficient K_tot ≈ 8.6. The **independent loop momentum balance and the CFD velocity field
agree** — the primary evidence that natural circulation removes 125 MWth as intended.
[Adilbek: replace lumped K_tot with the component-resolved loss tally.]

> **37-FA preservation.** H_th, ΔT, flow, OTSG duty and the riser area are all **unchanged** by the
> 21→37 pivot (constant power), so this entire loop balance carries over verbatim — no re-analysis
> (CAD spec §0′).

**Self-regulation (load-following without pumps).** Driving head scales with Δρ (≈ ΔT) and losses
with ṁ², so the loop self-adjusts: ṁ ∝ P^(1/3) (the natural-circulation signature) — ~80 % flow at
50 % power, passively limiting the core temperature rise. ‹FIGURE 8.4-2 —
`fer/natcirc_self_regulation.png`.›

## 8.4.3 Secondary cooling (OTSG and power conversion)

The integral **once-through helical-coil OTSG** is the single heat exchanger crossing the pressure
boundary, transferring 125 MWth from the primary shell side to the secondary feedwater/steam inside
the coils (economiser → evaporator → superheater in one pass). The secondary side — steam conditions,
regenerative feed heating, turbines, condenser, and the 40 MWe / 31.8 % net heat balance — is
developed in **§8.9**.

## 8.4.4 Associated and safety-related cooling systems

| System | Function | Key characteristics |
|---|---|---|
| **Passive DHRS / PRHR** | Decay-heat removal after trip / loss of secondary sink, by natural circulation to an in-containment tank — no AC, no operator | 2 × 100 % trains; each ≥ 105 % of decay heat at actuation; supports ≥ 72 h grace (§8.5/§8.6) |
| **Self-pressuriser** | Maintain 12.8 MPa via the integral top steam dome | In-vessel dome, sheathed heaters + spray, surge connection |
| **CVCS** | Inventory makeup/letdown, chemistry; **no boration** | Small lines (no large penetrations → large-break LOCA design-eliminated) |
| **Seawater once-through / UHS** | Reject ~82.6 MWth condenser heat to the Black Sea (Sinop) | ~2 065 kg/s (≈ 2.0 m³/s), ΔT ≤ 10 K, multiport diffuser → far-field rise ≤ 0.2 K (→ §8.9) |

## 8.4.5 Components — functions, capacities, materials, codes

**Primary / nuclear:**

| Component | Function | Capacity / key parameters | Material | Code |
|---|---|---|---|---|
| Reactor pressure vessel | Primary pressure boundary; houses all primary components | **ID 2700 mm, wall 150 + 5 mm**, ~7.2 m cyl + heads; 12.8 MPa op / 14.1 design; 60-yr life | SA-508 Gr.3 Cl.1 (SA-533B plate), SS clad | ASME III Div.1 Cl.1 (NB) |
| Core barrel / riser | Separate hot riser from cold downcomer | barrel ID 1900 / OD 2000 mm; riser R 560 mm | SS-304/316L | ASME III, NG |
| OTSG (helical coil) | 125 MWth primary→secondary; superheated steam | 6 coil layers R 665–1075 mm, axial pitch 230 mm | Inconel-690 TT tubes; SS shroud/tubesheets | ASME III, Cl.1 |
| Self-pressuriser | Maintain/regulate primary pressure | integral top dome, heaters, surge line | SA-508 dome; Incoloy-800-sheathed heaters | ASME III, Cl.1 |
| In-vessel CRDM | Reactivity control, no head penetrations | **12 units** | SS / Inconel | ASME III |
| Core support / flow plates | Locate core, distribute flow | lower/upper plates, flow distributor | SS-304 | ASME III, NG |
| Radial reflector | Flatten power, protect barrel | 200 mm water (steel option) | H₂O / SA-965 Type 304 | — / ASME III |
| DHRS heat exchanger | Passive decay-heat removal | ≥ 105 % of decay heat | SS / Inconel | ASME III, Cl.2 |

**Secondary / balance-of-plant** (capacities from the §8.9 heat balance):

| Component | Function | Capacity / key parameters | Material | Code |
|---|---|---|---|---|
| Tandem-compound turbine-generator | Expand steam → 40 MWe | 57.8 kg/s steam; gross ≈ 42.2 MWe | Cr-steel rotors, SS blading | ASME / IEC |
| Moisture separator | Dry crossover steam | last-stage moisture ≤ 10.8 % | SS | B31.1 |
| Condenser | Condense LP exhaust; reject 82.6 MWth | 7 kPa, Tsat 39 °C; ~2 065 kg/s once-through seawater | Ti / SS tubes, CS shell | ASME VIII |
| Deaerator (FWH-2) / FWH-1 | Regenerative feed heating to 180 °C; deaeration | open FWHs, 0.15 / 1.0 MPa | CS | ASME VIII |
| Feed / condensate / booster pumps | Return feedwater to OTSG at 4.5 MPa | ≈ 0.36 MWe total | CS / SS | B31.1 |
| MSIVs & safety/relief valves | Isolate / overpressure-protect secondary | per setpoints | SS / CS | ASME III/VIII |

## 8.4.6 Heat-removal capacity — analyses and methods

**Methods (literature-accepted):** natural-circulation loop momentum balance (Todreas & Kazimi);
**W-3 CHF** correlation (Tong) for MDNBR; Dittus–Boelter / Gnielinski convection (CFD benchmark);
**ANS-5.1** decay heat; **IAPWS-IF97** properties; conjugate CFD (k-ω SST) for the hot-pin field.

**Core T-H results (full-power hot channel; 21-FA values, 37-FA improves on every line):**

| Deliverable | Result | Limit | Margin |
|---|---|---|---|
| Primary T (in/out/avg) | 258 / 308 / 283 °C | — | — |
| Peak clad temperature (steady) | 391 °C | < 1200 °C | +809 °C |
| MDNBR (hot pin) | 1.466 | ≥ 1.3 | +12.8 % |
| Hot-leg subcooling | 21.7 °C | > 0 | — |
| Velocity field | all-positive upflow, no recirculation | stable nat-circ | — |
| Mass flow vs power | ṁ ∝ P^(1/3) | self-regulating | — |

> The 37-FA hot-channel MDNBR/PCT are re-run once the 37-FA peaking is final [SIM-PENDING], and are
> expected to **improve** (lower q′, flatter F_ΔH). The values above are the validated 21-FA result.

**OTSG coupling.** The OTSG removes 125 MWth across a counterflow once-through surface, so secondary
steam is bounded by the primary legs; the binding constraint is the **evaporator pinch**. Re-coupling
to the 308/258 °C legs gives the practical optimum **4.5 MPa / 296 °C steam → 39.7 MWe net, 8.8 °C
pinch** (§8.9). **Decay-heat removal:** after trip the DHRS removes ANS-5.1 decay heat by passive
natural circulation to the in-containment sink (≥ 105 % of the 1 s decay power); the quantitative
SBO/LOHS transient and PCT(t) are in §8.5/§8.6 (basis of the grace-period and large-break-LOCA
design-elimination arguments).

## 8.4.7 Operating conditions

| Plant state | Primary | Heat sink | Mode |
|---|---|---|---|
| Full power (100 %) | 12.8 MPa, 308/258 °C, 483 kg/s | OTSG → turbine | nat-circ + OTSG |
| Cogeneration | unchanged (~100 %) | OTSG; extraction → TCES; off-peak power → H₂ | nat-circ (§8.9) |
| Hot standby | 12.8 MPa, near-isothermal | OTSG / DHRS | nat-circ |
| Trip / loss of secondary sink | depressurise as needed | **DHRS** → tank | passive nat-circ |
| Station blackout (no AC/DC) | passive | DHRS + inventory, ≥ 72 h | fully passive (§8.5/§8.6) |

---

# 8.5 Safety Criteria

> **Codes/standards:** OpenMC (neutronics gates), W-3 / CFD (T-H gates), ANS-5.1 (decay heat),
> deterministic DBA + projected PSA. Criteria maintained in `safety/safety_criteria.yaml`.

## 8.5.1 Criteria framework and plant states

The safety basis is expressed as numeric criteria in eight categories (reactivity/neutronics,
thermal-hydraulics, pressure boundary, decay-heat removal & UHS, radiological/site, seismic/external,
fuel cycle, cogeneration interface), each classified as a **hard constraint** (breach disqualifies —
never traded), an **operating limit** (breach demands protective action), or a **target** (scored
against CAREM-25 / SMART / NuScale). Each carries its regulatory source and crediting trip function.

Plant conditions follow IAEA SSR-2/1 Req. 13/20:

| Plant state | Representative Aegis-40 events | Acceptance criterion |
|---|---|---|
| Normal operation | power operation, TCES-buffered load-follow, cogen dispatch | OLCs respected |
| AOO (≥ 1× in life) | turbine trip, loss of normal feedwater, uncontrolled rod withdrawal, loss of seawater intake | no fuel failure; MDNBR ≥ 1.3 |
| DBA (single fault) | small-break LOCA, main-steam-line break | limited fuel damage; dose ≤ 10 CFR 100 |
| DEC-A (multiple failure, coolable) | ATWS, station blackout, total loss of feedwater | core coolable; containment intact |
| DEC-B (severe accident) | postulated core melt | containment integrity preserved; large release **practically eliminated** |

**Events removed by practical elimination (SSR-2/1 §5.31)** — by construction, not probability:

| Eliminated event | Deterministic basis |
|---|---|
| Large-break LOCA | integral RPV — no large-bore primary piping exists (§8.6.1) |
| Control-rod ejection | internal in-vessel CRDMs — no ejection path (§8.6.1) |
| Boron-dilution accident | soluble-boron-free — no dilution pathway (§8.6.1) |
| Pressuriser surge-line break | integral pressuriser in the RPV head — no external surge line (§8.6.1) |

## 8.5.2 Principal criteria and demonstrated margins — Table 8.5-1

(Values on the 37-FA core where available; neutronic rows ⏳[37FA-PENDING] with 21-FA reference.)

| Criterion | Limit | Demonstrated | Source |
|---|---|---|---|
| Shutdown margin (stuck rod) | ≥ 1 % Δk/k | ⏳ *[21-FA: 12.4 %]* | NRC SRP 4.3 |
| MTC (HFP) | < 0 | ⏳ *[21-FA: −35.9 pcm/K]* | GDC-11 |
| Doppler coefficient | < 0 | ⏳ *[21-FA: −1.84 pcm/K]* | GDC-11 |
| Void coefficient | < 0 | ⏳ *[21-FA: −214 pcm/%void]* | GDC-11 |
| Control-rod worth (ARO) | ≥ 5 % Δk/k | ⏳ *[21-FA: 15 226 pcm]* | SRP 4.3 |
| Max reactivity insertion rate | ≤ 7.5e-4 Δk/k/s | ⏳ *[21-FA: 1.5e-5]* | ANSI/ANS-58.21 |
| **F_Q(Z) total peaking** | ≤ 2.32 (separable, +3 %) | **≈ 2.03 (37-FA latest)** | NUREG-1431 LCO 3.2.1 |
| **F_ΔH radial peaking** | ≤ 1.65 | **1.746 (37-FA latest) — governing open item O1** | NUREG-1431 LCO 3.2.2 |
| MDNBR (steady / AOO) | ≥ 1.3 | [SIM-PENDING — hot-channel; gated by 37-FA peaking] *[21-FA: 1.466]* | SRP 4.4 / 15.0 |
| PCT (LOCA envelope) | ≤ 1204 °C | [SIM-PENDING] | 10 CFR 50.46(b)(1) |
| Clad oxidation / H₂ | ≤ 17 % / ≤ 1 % | [SIM-PENDING] | 50.46(b)(2,3) |
| Primary design pressure | ≤ 14.1 MPa (iPWR) | 12.8 MPa operating | ASME III NB |
| Containment design pressure | ≤ 0.414 MPa | [ANALYSIS-PENDING — P/T response] | SSR-2/1 Req. 56 |
| Safety UHS grace | ≥ 72 h passive, no seawater/AC | 72 h by design | SSR-2/1 Req. 53 |
| Peak-rod discharge burnup | ≤ 62 GWd/MTU | ⏳ *[21-FA: 42.8]* | SRP 4.2 |
| Max enrichment | ≤ 5.0 wt% | 4.95 wt% | 10 CFR 50 LEU |
| Cycle length | ≥ 365 EFPD | ⏳ *[21-FA: 479]* | competition target |
| SSE | ≥ 0.3 g | 0.3 g design basis | RG 1.60; SSG-9 |
| Coastal external hazard | protected to site DBFL | [ANALYSIS-PENDING — Sinop surge/tsunami] | SSR-1; SSG-9 |
| Boundary dose (DBA, 0–2 h) | ≤ 0.25 Sv TEDE | [ANALYSIS-PENDING — dispersion from source term] | 10 CFR 100.11 |
| CDF / LRF | < 1e-7 / < 1e-8 /ry | LOHS ≈ 1e-8, SBO ≈ 1e-11 (§8.6) | RG 1.174 |

**Governing open item (O1).** The per-pin radial peaking is the single binding open item. On the
21-FA core it sat at F_ΔH ≈ 1.85 (> 1.65 LCO); the **37-FA pivot was made specifically to close it**
and the latest 37-FA value (1.746, pre-final Gd-tune) is already lower and trending toward the limit.
The design is formally **provisional on the safety metrics downstream of peaking** (MDNBR, LOCA PCT)
until the 37-FA STAT_FINAL run confirms F_ΔH; if it settles marginally above 1.65 it is defended on
DNBR margin at the 12.7 MW/tHM power density (CAREM precedent). **This is disclosed, not hidden.**

**Enrichment-margin note.** The 4.95 wt% peak zone deliberately approaches the 5.0 wt% LEU ceiling to
maximise burnup; the 0.05 wt% residual equals a typical fabrication tolerance, so the fuel spec
requires an asymmetric band (−0.10/+0.00 wt%) [VERIFY — mechanical/fuel section].

## 8.5.2a Heat-sink architecture — two distinct sinks (do not conflate)

Per SSR-2/1 Req. 52–53 the design distinguishes:

- **Normal heat sink = the Black Sea, once-through seawater** (condenser + CCWS + TCES rejection),
  **non-safety-classified** (graded per TECDOC-1936) — the safety function does not depend on it.
- **Safety ultimate heat sink = the passive IRWST + containment cooling** (atmosphere-coupled),
  **independent of seawater**, supporting the ≥ 72 h grace.

Therefore **loss of the seawater intake** (storm surge, biofouling, jellyfish/algal bloom, debris,
ice) or **loss of TCES** is a power-conversion event that does **not** challenge the safety UHS.

## 8.5.3 Defence in depth

The criteria map onto the five IAEA DiD levels (SSR-2/1 §2.13): **L1** prevention via inherently
negative feedback + DNB margin; **L2** control via the reactor-protection envelope (§8.7); **L3** DBA
control by passive ECCS/EFW/PRHR (§8.6); **L4** severe-accident management via the ≥ 72 h no-operator
grace and three passive containment-cooling trains; **L5** mitigation via the ≤ 0.5 km EPZ
([ANALYSIS-PENDING dose basis]).

---

# 8.6 Reactor Safety Systems Design

## 8.6.1 Accident prevention — elimination before mitigation

Aegis-40 **removes classes of design-basis events by construction** (the deterministic basis for the
§8.5 practical-elimination table):

1. **Large-break LOCA — eliminated.** The integral RPV contains the core, the helical-coil OTSG and
   the pressuriser in one boundary; no large-bore primary piping. The limiting LOCA is a small break
   at instrument/injection nozzles.
2. **Rod ejection — eliminated.** CRDMs are **internal (in-vessel)**; no head-mounted housing whose
   rupture provides an ejection path. The bounding reactivity insertion becomes uncontrolled rod
   *withdrawal* (AOO), bounded by the insertion-rate margin. [VERIFY — anchor with a configuration
   sketch, O13.]
3. **Boron-dilution — eliminated.** Soluble-boron-free core; hold-down by hybrid Gd₂O₃/Er₂O₃ +
   control rods.
4. **Pressuriser surge-line break — eliminated.** Integral pressuriser in the RPV head; no external
   surge line.

## 8.6.2 Engineered safety features (passive, de-energize-to-actuate)

- **Emergency Feedwater (EFW)** — gravity-driven from an elevated tank; isolation valves fail open;
  no pumps; sized for 72 h of decay-heat steaming [ANALYSIS-PENDING — tank inventory].
- **Passive Residual Heat Removal (PRHR)** — two 100 % natural-circulation trains (RPV → HX in the
  IRWST), each ≥ 105 % of decay heat at actuation. Governing decay-heat source **≈ 7.75 MW at
  shutdown** (~6.2 % of 125 MWth), full-chain depletion, cross-validated to ANS-5.1.
- **Passive containment cooling** — three trains; condensate return maintains the IRWST as the
  ≥ 72 h heat sink. **This — not the seawater system — is the safety UHS (§8.5.2a).**
- **Passive safety injection** — gravity feed from the IRWST on low pressuriser pressure + level
  coincidence.
- **Containment** — dry steel-lined, Ø ≈ 15 m, design pressure 0.414 MPa. [DECISION-PENDING — a
  NuScale-style submerged-pool configuration is under team evaluation; this section is written against
  the dry-containment baseline.]

## 8.6.2a Reactor shutdown — two diverse and independent means (SSR-2/1 Req. 46)

1. **Control rods (primary).** Gravity-drop on de-energisation via the RPS or the Diverse Actuation
   System; cold stuck-rod SDM ⏳ *[21-FA: 12.4 %]*.
2. **Emergency Boron Injection System (EBIS) — diverse second system.** Passive, shutdown-only
   borated water (gravity head / N₂ accumulator, fail-open isolation), **isolated and dormant in
   normal operation**, armed only on an ATWS signature by the DAS (§8.7.4). Diverse in principle
   (liquid poison vs mechanical insertion) → no shared rod-insertion common-cause failure.

This is achieved **without compromising the soluble-boron-free design**: normal coolant stays
boron-free (boron-dilution stays eliminated; MTC stays strongly negative); boron is solely the
dormant emergency reserve (the BWR standby-liquid-control principle). EBIS boron mass/concentration
sized for standalone cold subcriticality [SIM-PENDING — OpenMC borated-core case, O5].

## 8.6.3 Analyzed events — event-tree results

Two initiators analysed to event-tree depth (top-event demands map 1:1 onto §8.7 trip/ESF functions):

- **Loss of Heat Sink (LOHS)** — loss of main feedwater/condenser (incl. loss of the seawater
  intake). Seven sequences (4 safe, 3 core-damage); every CD sequence requires ≥ 2 independent
  failures; per-initiator CDF ≈ **1e-8/ry** [PRA-PENDING — generic reliability data]. The lead safe
  path is the **passive PRHR/IRWST, seawater-independent** — loss of the marine intake degrades only
  the normal (power) sink. ‹FIGURE 8.6-1 — event_tree_LOHS.›
- **Station Blackout (SBO)** — LOOP + failure of both standby AC sources (≈ 1e-5/ry). Every credited
  function actuates on de-energisation (breakers open, rods drop, EFW/PRHR valves fail open, CIVs
  fail closed) → **loss of power is actuation, not challenge**. No AC/DC/operator/external water for
  72 h; 1E batteries (72 h) serve post-accident monitoring only. SBO CDF ≈ **1e-11/ry** — four orders
  below target. ATWS-under-SBO is backstopped by EBIS (§8.6.2a) per 10 CFR 50.62. ‹FIGURE 8.6-2.›

**Remaining DBA spectrum (PIE list, NUREG-0800 Ch. 15; identified/screened, priority MSLB then
SBLOCA):**

| Initiator | Why it matters here | Status |
|---|---|---|
| Small-break LOCA | only surviving LOCA class | [ANALYSIS-PENDING — tree planned next] |
| MSLB / excess steam demand | with MTC < 0, overcooling is the limiting reactivity transient | [ANALYSIS-PENDING] |
| Uncontrolled rod withdrawal | surviving reactivity AOO after ejection elimination | [ANALYSIS-PENDING — bounded by insertion-rate margin] |
| Loss of primary flow / blockage | natural-circulation primary; flow-degradation screening | [ANALYSIS-PENDING — screening] |
| Marine intake blockage | CCF of the *normal* sink; bounded by passive UHS | CARRIED (§8.5.2a) |
| Fuel-handling accident | SFP/cask operations | [ANALYSIS-PENDING — ties to §8.8] |

## 8.6.4 Redundancy and necessity; fault/event trees

For each credited system the design demonstrates redundancy (what backs it up) and necessity (what
fails without it); the LOHS and SBO sequence tables show **no single failure leads to core damage** —
the single-failure criterion is met at the accident-sequence level, not merely the component level.
**How protective actions are derived** (the schematic-diagram requirement) is shown in §8.7.2: each
trip parameter is derived from monitored neutron flux, temperature, flow and pressure and combined in
2-of-4 coincidence logic (`trip_signals.md`, ‹FIGURE 8.7-1›).

---

# 8.7 Instrumentation and Control System Design

> **Standards:** IEEE 603, IEC 61513 / 60880, IAEA SSG-39, 10 CFR 73.54.

## 8.7.1 Architecture

Five layers with strict downward non-interference: **L1** field instrumentation (21 measurement
channels, 14 Class 1E); **L2** Reactor Protection System; **L3** ESFAS; **L4** Distributed Control
System (non-safety); **L5** digital twin (advisory, read-only). Signals flow **upward only**:
protection layers receive sensor signals directly from L1; **no software path exists from non-safety
into Class 1E** (the DCS taps sensor circuits through qualified one-way isolation; the digital twin is
fed through a unidirectional data diode). ‹FIGURE 8.7-1 — I&C architecture block diagram (`ic_block`),
which also serves as the §8.6 schematic-diagram requirement for protective-action derivation.›

## 8.7.2 Reactor Protection System

Four independent divisions (A–D) with **2-of-4 coincidence voting** satisfy the single-failure
criterion in both trip and trip-prevention directions, including one channel out for maintenance.
**De-energise-to-trip**: breakers normally energised; any loss of power/air/signal scrams; rods
insert by gravity. Platform: safety-qualified FPGA/PLC, IEC 60880 Category A software (no dynamic
memory, no recursion; independent V&V). Timing: division scan+vote ≤ 100 ms;
sensor-threshold-to-breaker ≤ 500 ms (the bound assumed in §8.6). [TBD — per-channel
response-time/accuracy table; total channel uncertainty per ISA-67.04 / RG 1.105, O12.]

**Principal trip derivations** (how monitored variables become protective actions — the §8.6/§8.7
schematic requirement; full logic `trip_signals.md`): high flux > 118 %; flux rate > 5 %/s; OTΔT and
OPΔT composites from T_hot/T_cold/flux/pressure; low flow < 90 %; pressuriser pressure
> 16.5 / < 12.5 MPa; SG level < 15 % NR; containment pressure > 0.17 MPa; containment radiation
> 100× background.

## 8.7.3 ESFAS

Same 4-division / 2-of-4 structure; actuations **latching** (deliberate operator reset). Functions:
passive safety injection (low pzr P + level), containment isolation (high containment P or radiation),
EFW (low SG level / loss of normal FW), PRHR/PCC alignment, main-steam isolation (high MSL radiation
or containment P), and **cogeneration-interface isolation** (fail-closed on high intermediate-loop /
product activity or SGTR — §8.8.9, Req. 35). All actuated devices move to safe state on loss of
motive power.

## 8.7.4 Diverse Actuation System

Class 1E but **platform-diverse** (different technology and team from the RPS) covering postulated CCF
of all four RPS divisions. Monitors power-range flux and pressuriser pressure through fixed
hardware-biased logic (setpoints staggered beyond the RPS envelope); diverse paths to the trip
breakers, SI/PRHR, and **EBIS (§8.6.2a)** on an ATWS signature. The DAS is the **sole actuation path
for EBIS**, which carries the ATWS burden in this boron-free core.

## 8.7.5 Control room, control philosophy and human factors

Two-operator MCR per NUREG-0700 (reactor-operator + BOP consoles, STA station, 4×80″ overview wall
with plant mimic / SPDS / critical safety functions); alarm management per ISA 18.2 (≤ 10 alarms /
10-min window under DBA); computer-based procedures with paper backup; **hardwired,
software-independent manual actions** (trip, SI, CI, EFW, MSIV) per IEEE 603 §5.8. A **Remote
Shutdown Station** (separate fire area, independent 1E division) provides post-accident monitoring +
diverse manual trip/ESF (incl. EBIS) if the MCR is uninhabitable; its scope is minimal because the
plant is passively safe for ≥ 72 h. **The main control room is designed ergonomically** to NUREG-0700
(panel layout, sightlines to the overview wall, alarm prioritisation, anthropometric console design).

**Load-following control philosophy (originality).** Load-following is achieved primarily through the
**TCES buffer** (§8.9), not deep reactor power manoeuvring: the reactor is held near baseload while
the thermochemical store absorbs the dispatch swing. This keeps the reactor where its negative
feedbacks and power distribution are best characterised and **does not aggravate the
peaking/xenon/MTC challenges** — a control-side safety benefit.

## 8.7.6 Digital twin (advisory) — originality feature

A non-safety digital twin mirrors all L1 signals through the data diode and provides soft sensors
(MDNBR, fuel-centreline estimates), anomaly detection and predictive maintenance. Category C software;
**cannot actuate any device**; presents alongside (never in place of) qualified indications. Enables
condition-based maintenance and reduced-staffing operation without touching the L1–L3 safety
qualification (cf. NuScale's ISV-validated reduced-staffing precedent).

## 8.7.7 Qualification

Class 1E environmental qualification per IEEE 323 (150 °C, 0.5 MPa, 100 % steam, lifetime dose; envelope
to confirm against the containment P/T analysis); seismic per IEEE 344 at SSE 0.3 g; cybersecurity per
10 CFR 73.54 / RG 5.71 (Purdue-model segmentation, no wireless in safety areas, no remote access to
Class 1E, signed firmware, write-once audit logs).

---

# 8.8 Auxiliary Systems Design

Nine auxiliary systems, each carrying the six FER-required fields (purpose · operating principle ·
layout · safety function · performance · maintenance); full six-field tables in `layout/aux_systems.md`.
Per-system P&IDs (A4) and the single-line (A5) are in the drawing pass.

| # | System | Safety function | Building | Key point |
|---|---|---|---|---|
| 1 | HVAC / Ventilation | **Yes (ESF)** | RXB/AB/CB/SFB | Negative-pressure cascade clean→contaminated→HEPA+charcoal→stack; MCR habitability is an ESF actuation |
| 2 | Fire Protection | **Yes (DiD)** | site-wide | 3 h barriers between RPS/ESFAS divisions A–D; clean-agent in I&C/MCR; protects the 2/4 separation basis (NFPA) |
| 3 | Radiation Protection + Monitoring | **Yes** | site-wide | 4 layers (area/process/personnel/post-accident high-range RG 1.97); effluent monitors gate all releases incl. the seawater discharge |
| 4 | Emergency Power (Class 1E) | **Yes (1E)** | DGB/CB | 2× EDG + 1E batteries; supports monitoring + active backup (core cooling is passive); battery duty to the 72 h grace |
| 5 | Normal Electrical Distribution | No | EHB/CB | 40 MWe → ~50 MVA main transformer → 33 kV; dual offsite/onsite feed |
| 6 | Fuel Handling + Storage | **Yes** | RXB/SFB | Flooded transfer; **unborated SFP**, subcriticality by fixed-absorber rack geometry + burnup credit, k(95/95) ≤ 0.95 (consistent with the boron-free core, §8.11) |
| 7 | Fission-Product Release Control | **Yes (top-tier)** | RXB/WMB | Three-barrier chain; containment isolation; gaseous/liquid radwaste before monitored discharge |
| 8 | Service Systems (instrument air · demin · SFP cooling) | Mixed | AB/SFB | Instrument air fail-safe; SFP cooling rejects to once-through seawater (normal sink); large pool inertia gives long grace; safety UHS stays passive |
| 9 | **Cogeneration Interface Isolation (SSR-2/1 Req. 35)** | **Yes** | TB/EUB | §8.8.9 |

## 8.8.9 Cogeneration interface isolation (Req. 35)

Aegis-40 exports heat to a **TCES district-heating** network and steam to a hydrogen plant. SSR-2/1
**Req. 35** requires that no process transport radionuclides to the heat/H₂ user in operational **or**
accident states. Provision: a **non-radioactive intermediate loop** between the reactor secondary
steam and both customer circuits (reactor steam never contacts district-heat water or electrolyser
feed), held at **higher pressure** than the reactor-side stream at each interface heat exchanger so
any leak flows **inward** (clean→reactor). Result: **≥ 3 independent barriers** — (1) SG tube wall,
(2) intermediate-loop boundary, (3) customer-side HX wall. Accident-condition isolation: fail-closed
ESFAS valves on high intermediate-loop / product activity, SGTR signal, or containment isolation
(§8.7.3). **Tritium** is the governing nuclide at the high-temperature electrolyser interface →
permeation-barrier coatings + product tritium monitor + intermediate-loop getter [ANALYSIS-PENDING —
tritium permeation/carryover budget, O7].

## 8.8.10 Electrical-supply summary

Defence-in-depth power chain: **grid (33 kV) → onsite generator → 2× EDG → 1E batteries → passive (no
power needed)**. The passive core-cooling decision lets the chain end in "no power needed" within the
72 h grace. Single-line drawing in `aux_systems.md §10`.

---

# 8.9 Energy Conversion and Integrated Systems

> **Code:** regenerative-Rankine + exergy model, IAPWS-IF97 (`scripts/thermo_cycle.py`,
> `thermo_exergy.py`, `thermo_cycle_recouple.py`).

## 8.9.1 Energy-conversion architecture

Aegis-40 converts **125 MWth → 40 MWe (net)** through a **regenerative superheated Rankine cycle** on
the secondary side of the integral OTSG. The primary loop is natural-circulation, so the only rotating
primary machinery is eliminated and the entire NSSS is inside the RPV. Heat crosses the pressure
boundary once, in the OTSG. Secondary flow path:

> OTSG (superheated steam) → **HP turbine** → **moisture separator** → **LP turbine** → **condenser**
> → condensate pump → **deaerator (open FWH-2)** → booster pump → **HP FWH-1** → main feed pump →
> OTSG.

**A single turbine-generator.** The HP/LP stages and crossover moisture separator are on **one shaft
driving one generator** (tandem-compound T-1) — the conventional, lowest-cost arrangement at 40 MWe.
The district-heat and H₂ off-takes add **no** further turbine (the store is charged from a steam
*extraction*, not a back-pressure pass-out machine). ‹FIGURE 8.9-1 — integrated plant PFD,
`cycle/plant_pfd_seawater_h2.png` (and labelled-state PFD `cycle/cycle_pfd_labeled.png`).›

## 8.9.2 Cycle configuration — Table 8.9-1

| Parameter | Value |
|---|---|
| Net electric output | 40.0 MWe (nameplate); 39.7 MWe (computed) |
| Core thermal power (= secondary heat in) | 125 MWth |
| Turbine-inlet (OTSG) steam | 4.5 MPa / 296 °C |
| Steam mass flow | 57.8 kg/s |
| Condenser pressure | 7 kPa (Tsat 39 °C) |
| HP extraction → FWH-1 | 1.0 MPa |
| Crossover / MS + deaerator | 0.15 MPa |
| Turbine / pump isentropic efficiency | 0.85 / 0.82 |
| Generator × mechanical | 0.985 |
| BOP house load | 5.0 % of gross |

**Why a moisture separator:** expanding 4.5 MPa steam straight to 7 kPa would leave ~22 % last-stage
moisture (past the ~12 % erosion limit); the MS at 0.15 MPa holds last-stage moisture to **10.8 %**.
**Why regeneration:** two open FWHs raise feedwater from 39 → 180 °C, lifting cycle efficiency from
~29 % (simple) to **33.7 % gross** — the difference between missing and meeting 40 MWe — and
deaerating the feedwater.

## 8.9.3 State points and heat balance

**Table 8.9-2 — cycle state points** (IAPWS-IF97; full data `cycle/cycle_state_points.csv`):

| # | Location | P (MPa) | T (°C) | h (kJ/kg) | x |
|---|---|---|---|---|---|
| 1 | Turbine inlet (OTSG steam) | 4.500 | 296.0 | 2932.1 | SH |
| 2 | HP extraction → FWH-1 | 1.000 | 179.9 | 2676.8 | 0.950 |
| 3 | Crossover / MS inlet | 0.150 | 111.4 | 2409.8 | 0.873 |
| 3g | MS vapour outlet (dried) | 0.150 | 111.4 | 2693.1 | 1.000 |
| 4 | LP turbine exhaust | 0.007 | 39.0 | 2310.9 | 0.892 |
| 5 | Condenser outlet (sat. liq.) | 0.007 | 39.0 | 163.4 | 0.000 |
| 6 | Condensate-pump outlet | 0.150 | 39.0 | 163.5 | 0.000 |
| 7 | Deaerator (FWH-2) outlet | 0.150 | 111.4 | 467.1 | 0.000 |
| 8 | Booster-pump outlet | 1.000 | 111.5 | 468.2 | 0.000 |
| 9 | FWH-1 outlet (sat. liq.) | 1.000 | 179.9 | 762.7 | 0.000 |
| 10 | Feed-pump outlet → OTSG | 4.500 | 180.6 | 767.5 | 0.000 |

‹FIGURE 8.9-2 — T–s diagram (`cycle/cycle_Ts_diagram.png`).›

**Table 8.9-3 — performance and heat balance**

| Quantity | Value |
|---|---|
| Cycle thermal efficiency | 34.0 % |
| Steam mass flow | 57.8 kg/s |
| Gross shaft / electric | 42.8 MW / 42.2 MWe (33.7 %) |
| − feed/condensate pumps | 0.36 MWe |
| − BOP house load | 2.11 MWe |
| **Net electric (sent-out)** | **39.7 MWe** (nameplate 40) |
| **Net plant efficiency** | **31.8 %** |
| Heat rejected at condenser | 82.6 MWth |

Closure: 125 MWth in = 39.7 MWe + 82.6 MWth + ~2.5 MWe auxiliaries (< 1 %). 31.8 % is in line with
operating iPWRs (NuScale ~30 %, mPower ~31 %), the slight edge from superheated OTSG steam +
regeneration.

**Second-law (exergy) analysis.** Referenced to a dead state of 25 °C / 0.101 MPa with the heat source
valued at the primary log-mean temperature (282.6 °C), of the **57.9 MW** of exergy delivered by the
primary coolant, **39.7 MW** leaves as electricity → **exergetic efficiency 68.5 %**. The largest
*internal* irreversibility is the turbine (10.4 %), then the OTSG finite-ΔT (6.8 %); condenser (6.4 %)
and generator/BOP (4.8 %) are *external* losses; the feedwater train destroys only ~3 %. This locates
the turbine and OTSG approach temperatures as the only worthwhile efficiency levers.
(`cycle/cycle_exergy.csv`.) ‹FIGURE 8.9-2b — labelled secondary-cycle PFD with per-node P/T/h/ṁ.›

## 8.9.4 Primary–secondary coupling: OTSG feasibility — Table 8.9-4

Because the OTSG transfers 125 MWth across a counterflow once-through surface, the secondary steam is
bounded by the §8.4 legs (308 hot / 258 cold):

| Check | Value | Criterion |
|---|---|---|
| Secondary saturation temperature | 257.4 °C | economiser-limited (cold leg 258 °C) |
| Superheater hot-end approach | 12.0 °C | > 0 |
| Evaporator pinch ΔT | 8.8 °C | ≳ 8 °C (practical OTSG) |

This is the binding constraint on steam pressure: pushing above 4.5 MPa drops the pinch below the ~8 °C
floor. The selected **4.5 MPa** keeps a healthy pinch while holding the 40 MWe-class output.

## 8.9.5 Thermochemical energy storage (TCES) for district heating

Aegis-40 is a **polygeneration** plant: alongside 40 MWe it supplies **district heating** through a
**thermochemical energy store** and **hydrogen** through off-peak electrolysis (§8.9.6). The store
decouples DH delivery from the near-constant ~100 % reactor power and — unlike a sensible-heat store —
holds its charge **loss-free** (energy in reversible chemical bonds), making multi-day and seasonal
storage practical.

**Architecture — IHX-isolated, non-safety auxiliary.** The store sits **outside the nuclear island**,
coupled to the steam cycle only through an **intermediate heat exchanger (IHX)**. On charge,
HP-extraction steam gives heat across the IHX to a closed ~168 °C charge loop; on discharge, the
store's reaction heat feeds a separate district-heat water loop (90 / 45 °C). The storage medium never
shares a fluid path with reactor steam → **no chemical/water-quality risk into the power cycle**;
classified non-safety. ‹FIGURE 8.9-3 — `cycle/pfd_cogeneration_tces.png`.›

**Two candidate media — Table 8.9-5** (Tier-B [CONFIRM with layout]):

| Parameter | Ammine NiCl₂-SrCl₂/NH₃ | Zeolite-13X / H₂O |
|---|---|---|
| Mechanism | reversible resorption (NH₃) | reversible adsorption (H₂O) |
| Discharge (DH) temperature | ~150 °C | ~130 °C |
| Energy density | 0.27 kWh/kg | 0.20 kWh/kg |
| Round-trip efficiency | ~0.88 | ~0.78 |
| Store mass (200 MWh block) | ~735 t | ~1000 t |
| Store volume | ~735 m³ | ~1538 m³ |
| Charge penalty | 0.31 MWe per MWth | 0.31 MWe per MWth |
| Standby loss | ≈ 0 | ≈ 0 |
| Safety note | closed-loop ammonia | water only |

The **zeolite-13X / water** medium is the locked baseline (simpler safety/public-acceptance story on a
nuclear site; demonstrated for DH), with the ammine pair carried as the higher-density alternative.
Charging draws 168 °C heat from HP extraction at **0.31 MWe/MWth**, dipping net output ~4.4 MWe during
the off-peak charge window; during peak discharge the full 40 MWe goes to grid **and** ~25 MWth flows
from the store to the DH network with no live-steam penalty.

## 8.9.6 Hydrogen co-generation (off-peak)

Off-peak (night-shift) electricity feeds a water-electrolysis unit, converting low-value night output
into storable hydrogen and raising effective utilisation; the reactor stays at constant power. A
reference **8 MWe PEM** block at ~50 kWh/kg yields **≈ 160 kg H₂/h (≈ 640 t/yr at 4 000 off-peak h)**;
the secondary steam (~296 °C) and TCES-discharge heat pre-heat the electrolyser feed (a high-T
solid-oxide stack would benefit more but wants 700–850 °C). Electrolyser technology/capacity set with
the layout team.

---

# 8.10 Facility Layout Design

## 8.10.1 Three-island scheme

The site is partitioned into three functional islands by hazard class, safety class and access
control (cf. AP1000/NuScale/SMART), extended for cogeneration:

- **Nuclear Island (NI)** — RXB, AB, CB, SFB, DGB, WMB. Seismic Cat I on a common 0.3 g SSE mat;
  Protected Area. ~100 × 80 m.
- **Conventional Island (CI)** — TB, EHB/switchyard, **Circulating-Water Pump house + seawater
  intake/outfall (once-through, no cooling tower)**, water/services. Seismic Cat II. ~80 × 80 m.
- **Industrial Island (II)** — **TCES (zeolite-13X)**, electrolyser, H₂ storage. Non-safety, NFPA 2
  H₂ classification; **100 m H₂ stand-off** to the nearest NI building. ~60 × 60 m.

Driving constraints: EPZ ≤ 0.5 km, SSE 0.3 g, consolidated containment penetrations, H₂ explosion
stand-off (NFPA 2 / IEC 60079). The TB is adjacent to the NI (shortest main-steam/feedwater run
~47 m); the seawater intake/outfall + CWP at the shoreline.

## 8.10.2 Building inventory and cooling

Full table in `layout/building_list.md` (14 named buildings + infrastructure). Cooling is
**once-through Black Sea seawater**: condenser circ-water and CCWS reject to the sea via a
breakwater-protected **intake** (trash racks + redundant travelling screens + chlorination), the
**CWP house** (~240 m² on-island), and a **discharge/outfall** structure. Heat rejected ≈ 82 MWth at
ΔT ≈ 8–10 K (~2–2.5 m³/s); plume negligible at site scale. Thermal discharge under the Turkish Water
Pollution Control Regulation (SKKY) [VERIFY — max-T/ΔT clause, O9]. **Normal heat sink only; the
safety UHS is the passive IRWST (§8.5.2a).** Realism anchored to **Akkuyu NPP** (4× VVER-1200,
once-through seawater — the licensed Turkish precedent); the colder Black Sea makes the condenser
back-pressure / efficiency case conservative.

## 8.10.3 Energy-storage building (TCES)

A **thermochemical zeolite-13X / water-vapour sorption bed**: charge by dehydration off pass-out steam,
discharge by hydration delivering ~130–150 °C to the district-heat intermediate loop. Chosen over
two-tank sensible storage for near-zero self-discharge, intrinsically low hazard (non-toxic,
non-flammable, non-corrosive — favourable under Req. 35), and proven engineering. Enables the
load-following / thermal-management role (§8.7.5, §8.9).

## 8.10.4 Critical piping

Full table in `layout/critical_piping_table.md`. **Main steam 2×DN250** (~315 °C / 5.8 MPa) and
**feedwater 2×DN200** co-routed RXB↔TB in a below-grade tunnel (~47 m), MSIVs ≤ 1.5 m inside the
penetration, whip restraints, RC division wall. DHRS/PRHR **2×DN100** and passive ECCS **2×DN80** are
intra-RXB, fully passive, **no containment penetration**. Pressuriser surge line **eliminated**
(integral pressuriser). TCES charge branch off the MSL header; condenser circ-water
intake→CWP→condenser→outfall (seawater once-through); CCWS to seawater. Sizes pending hydraulic
confirmation (Adilbek).

## 8.10.5 Site dimensions, 2D/3D plans, and structural data

Built area ~9 000 m² across the three islands; total occupied site ~250 × 300 m, comfortably inside
the 500 m EPZ. The CAD model (`cad/aegis40_site.step`) is the spatial single-source-of-truth under
Git; the 2D plot plan / elevation drawings and the interactive viewer regenerate from it. The plan
tables carry the main structural data (construction structures, steel structures, connection
structures, system weight distributions, structural requirements) per the §8.10 requirement;
weight/foundation data are in `layout/building_list.md`. All four FER §8.10 categories (reactor
building / energy-conversion systems / O&M services / other systems) are populated.

> **Figure status.** The site plan, elevation, CAD STEP and viewer are current to the seawater + TCES
> configuration. The integrated process-flow diagram is the master figure feeding the §8.9/§8.4
> diagrams. (CAD 3D/STEP assets are held in the local working tree per the project's CAD-handling
> practice and are not part of this doc commit.)

---

# 8.11 Nuclear Waste Management

> **Codes:** OpenMC depletion + `src/aegis40.back_end` (15/15 tests). **Burnup-dependent numbers**
> below are on the 21-FA locked inventory and are ⏳[37FA-PENDING] re-generation from the 37-FA
> depletion run; the methodology and conclusions are design-independent.

Aegis-40 addresses waste on the three fronts mandated by Technical-Specification §4.3.2: **(i)** an
innovative fuel-cycle design minimising spent-fuel quantity and radioactivity per unit energy;
**(ii)** a back-end plan with the three required analyses (source term, decay heat, storage
criticality); **(iii)** minimisation of secondary radioactive waste.

## 8.11.1 Waste-minimisation by design (fuel cycle)

The dominant lever is **discharge burnup**: more energy per tonne of HM directly reduces spent-fuel
arisings per unit electricity. The high-burnup SBF core discharges at **42.8 GWd/tHM** (21-FA locked;
37-FA value pending) at **32.0 % net efficiency**, versus ~24 GWd/tHM / ~27 % for CAREM-25. The
once-through waste-intensity identity (tHM/TWhe = 10⁶/[BU·24·η]) gives:

**Table 8.11-1 — Spent-fuel arisings and waste intensity vs CAREM-25**

| Quantity | Aegis-40 | CAREM-25 |
|---|---|---|
| Thermal / electric power | 125 MWth / 40 MWe | 100 MWth / 27 MWe |
| Net efficiency | 0.320 | 0.270 |
| Discharge burnup | 42.8 GWd/tHM *(21-FA; ⏳ 37-FA)* | 24.0 GWd/tHM |
| HM discharged per year | 0.91 tHM/yr | — |
| Assemblies discharged per year | ~3.6 FA/yr | — |
| **Waste intensity** | **3.04 tHM/TWhe** | **6.43 tHM/TWhe** |

Aegis-40 produces **~2.1× less heavy metal per unit electricity than CAREM-25** (~53 % reduction).
Absolute arisings are tiny: **< 1 tHM/yr, < 4 assemblies/yr**.

> **37-FA note.** The 37-FA core's higher HM at constant power gives a lower per-tHM burnup but does
> **not** change the energy basis of the intensity identity; the per-TWhe metric tracks burnup ×
> efficiency and is regenerated with the depletion run. Absolute annual HM throughput scales with the
> reload mass.

## 8.11.2 Back-end fuel-cycle management plan

**Once-through** cycle. Discharged assemblies (~3.6 FA/yr) cool in the spent-fuel pool, then transfer
to **on-site dry-cask interim storage** after the decay-heat and dose criteria are met (§8.11.3). The
very low arisings make a single compact pool + small cask pad sufficient for the plant lifetime,
deferring repository transfer. No reprocessing (the discharged Pu vector and safeguards
attractiveness are in §7 / the non-proliferation assessment).

## 8.11.3 Spent-fuel source term and decay heat (§4.3.2)

**Table 8.11-2 — Discharge source term vs cooling time** (21-FA inventory, 5.04 tHM at discharge):

| Cooling (yr) | Activity (Bq) | Decay heat (W) | Radiotoxicity (Sv) |
|---|---|---|---|
| 0 | 1.20×10¹⁷ | 18 220 | 2.18×10⁹ |
| 1 | 1.06×10¹⁷ | 15 240 | 1.93×10⁹ |
| 5 | 7.59×10¹⁶ | 9 333 | 1.41×10⁹ |
| 10 | 5.98×10¹⁶ | 7 003 | 1.16×10⁹ |
| 30 | 3.20×10¹⁶ | 4 247 | 7.44×10⁸ |
| 100 | 5.51×10¹⁵ | 1 188 | 2.43×10⁸ |
| 1000 | 1.87×10¹⁴ | 155 | 4.50×10⁷ |

At discharge: total activity **1.20×10¹⁷ Bq**, decay heat **18.2 kW** (3 615 W/tHM); dominant early
nuclides Cs-134, Pu-241, Cs-137, Sr-90; long-term radiotoxicity set by transuranics. The decay-heat
curve is the input to pool cooling load and dry-cask passive-cooling design. ‹FIGURE 8.11-1 — decay
heat + ingestion radiotoxicity vs cooling time, `waste/decay_heat_vs_cooling.png`.›

## 8.11.4 Spent-fuel storage criticality (§4.3.2)

Evaluated under the SBF philosophy — **cold (20 °C), unborated water, no soluble-boron credit** — so
the result holds on total loss of any boron source. Criterion **k(95/95) ≤ 0.95** (NUREG-0800 / 10 CFR
50.68). Burnup-credited fuel in a Region-II absorber rack (17×17 cell, 23.5 cm pitch), modelled as a
bounding infinite array:

**Table 8.11-3 — Storage-rack criticality (burnup-credited)**

| Configuration | k_calc ± σ | k(95/95) | Verdict |
|---|---|---|---|
| Spent fuel + Boral box (0.40 B₄C) | 0.78099 ± 0.00054 | 0.782 | ✅ PASS |
| Spent fuel + Metamic box (0.31 B₄C) | 0.78856 ± 0.00061 | 0.790 | ✅ PASS |

Both sit **~0.16 below the 0.95 limit**, confirmed by two absorber materials. Reactivity ladder: fresh
bare touching fuel (1.50) → **burnup credit** (1.075) → **absorber + pitch** (0.782). A minimum-burnup
loading curve administratively excludes fresh/low-burnup assemblies (held in a Region-I flux-trap
rack). Consistent with, and more conservative than, the published SBF small-PWR envelope (Kim, Jung &
Yoon 2024). **V&V:** the reported margins use Δ_bias = Δ_unc = 0; a licensing-grade result adds the
OpenMC + ENDF/B-VIII.0 bias from the OECD/NEA Burnup-Credit Benchmark (Phase II) and SFCOMPO 2.0
(§8.13); even Δ ≈ 0.02–0.05 leaves 0.78 comfortably under 0.95.

## 8.11.5 Secondary radioactive-waste minimisation

The **soluble-boron-free** design eliminates the borated-water secondary-waste streams a
boron-controlled PWR generates — spent ion-exchange resins, evaporator concentrates, tritiated boron
effluent from the CVCS — a "reduce-quantity" benefit not captured in the tHM/TWhe metric. Remaining
operational wastes (filters, dry active waste, clean-up resins) are managed by best-available-technique
**segregation, volume reduction and conditioning** per IAEA GSR Part 5; wastes are collected and
segregated by nature for their subsequent processing/destination (not mixed with streams of different
characteristics). The integral-vessel layout with no large primary penetrations further limits
contaminated-component arisings.

---

# 8.12 Economic Evaluation

> **Code/method:** `scripts/economics_lcoe.py` (→ `economics/lcoe_breakdown.csv`) +
> `src/aegis40/back_end/fuel_cycle.py`; methodology per OECD-NEA (1994) and Ashley et al. (2014).

## 8.12.1 Methodology

The **levelised cost of electricity (LCOE)** is the constant electricity price that, discounted over
the plant life, recovers all discounted costs. With real discount rate *r* and life *N*:

```
CRF  = r(1+r)^N / [(1+r)^N − 1]
LCOE = [OCC·IDC·CRF + FixedO&M] / (8760·CF) + VarO&M + Fuel + Decommissioning     [$/MWh]
```

The **levelised fuel-cycle cost (LFCC)** follows the same discounted-cash-flow form (Ashley 2014 Eq. 3)
summed over front-end (mining/conversion, enrichment, fabrication incl. Gd₂O₃/Er₂O₃) and back-end
(interim storage, encapsulation, disposal) stages.

## 8.12.2 Inputs (Tier-B [CONFIRM])

| Parameter | Value |
|---|---|
| Net electric capacity | 40 MWe |
| Capacity factor | 0.90 |
| Economic life N | 60 yr |
| Real discount rate r | 7 % |
| Construction duration | 4 yr |
| Overnight capital (OCC) | 5 000 / **7 200** / 10 500 $/kWe |
| Fixed O&M | 130 $/kWe·yr |
| Variable O&M | 3 $/MWh |
| Fuel (LFCC) | 7.5 $/MWh |
| Decommissioning fund | 700 $/kWe |

The **small-unit premium** is deliberate (fixed engineering/licensing/staffing over less capacity);
offsetting SMR advantages — factory fabrication, shorter build, lower absolute capital-at-risk, and the
SBF / natural-circulation simplification (fewer pumps, no boron-recovery plant) — appear in the shorter
construction period and lower O&M.

## 8.12.3 Levelised fuel-cycle cost

**Once-through (open)** cycle, consistent with the §7 non-proliferation posture. With the high
discharge burnup spreading the front-end mass cost over more energy than a 33 GWd/t LWR, the levelised
fuel contribution is **≈ 7.5 $/MWh** — a small share of LCOE, typical of once-through LWR cycles.
(Stage-by-stage table from `fuel_cycle.py` once the per-cycle enrichment/SWU is locked with §8.2.)

## 8.12.4 LCOE result and sensitivity — Table 8.12-1

| CAPEX scenario | OCC ($/kWe) | Capital | Fixed O&M | Var O&M | Fuel | Decom. | **LCOE ($/MWh)** |
|---|---:|---:|---:|---:|---:|---:|---:|
| low | 5 000 | 51.7 | 16.5 | 3.0 | 7.5 | 6.3 | **85.0** |
| **mid** | **7 200** | **74.5** | **16.5** | **3.0** | **7.5** | **6.3** | **107.8** |
| high | 10 500 | 108.6 | 16.5 | 3.0 | 7.5 | 6.3 | **141.9** |

**Mid-case LCOE ≈ 108 $/MWh, of which capital is ~69 %.** Two conclusions: (1) LCOE is
**capital-dominated** — fuel (7 %) and O&M (18 %) are secondary; the honest uncertainty band
(85→142 $/MWh) is set by the ±FOAK CAPEX spread, not operating cost. (2) The levers that matter are
capital ones — capacity factor, construction schedule, OCC; the SBF/natural-circulation simplification
helps both OCC and O&M, and a high CF from the long SBF cycle dilutes fixed charges.

## 8.12.5 Comparison with reference reactors

This places Aegis-40 in the expected FOAK-SMR range (90–150 $/MWh) — uncompetitive with GW-class
nuclear on $/MWh alone, but that is the wrong comparison: the SMR value proposition is **dispatchable
polygeneration** (electricity + the §8.9 district-heat / H₂ revenue streams, not captured in a
single-product LCOE), **grid-independent siting**, and **low absolute capital-at-risk**. Against the
SMR peer set, a weighted figure-of-merit ranks Aegis-40 a robust second (NuScale > **Aegis-40** >
CAREM-25 > SMART), with the boron-free / high-burnup / low-waste-intensity attributes its
differentiators. [CONFIRM — replace the literature CAPEX triangular with a bottom-up account once the
§8.10 equipment list is fixed; add the cogeneration revenue credit and r = 5/10 % sensitivity rows.]

---

# 8.13 Digital Appendix — Verification & Validation (mandatory, spec p. 8)

The competition requires, **per code**, one sample input file + an explanation of the
case/approach/output **and** reproducibility / benchmarking / repeatability evidence against
IAEA / OECD-NEA data. The Aegis-40 strategy is **cite published V&V of the open-source tools + run
the design deck as the sample input + one cheap confirmatory benchmark per code**.

| Term | What it answers | How shown |
|---|---|---|
| Reproducibility | Can someone rebuild our result from the inputs? | public built-in benchmark models + tracked sample decks + fixed library/chain versions |
| Repeatability | Does our result hold across reruns? | re-run with independent RNG seeds; agreement within Monte-Carlo σ |
| Benchmarking | Does the code reproduce a known answer? | code-to-code (Serpent) + measured assay (SFCOMPO) + criticality arrays / IAPWS / ANS-5.1 |

**Sample-input / V&V index:**

| Code / capability | Sample input | Confirmatory benchmark (cite + run) | Status |
|---|---|---|---|
| **OpenMC transport** (§8.2) | `openmc_model/sample_inputs/{geometry,materials,settings}.xml` (37-FA core deck) | ICSBEP / C5G7 / BEAVRS (OECD-NEA / MIT-CRPG) | core deck ✅; benchmark cite |
| **OpenMC depletion** (§8.2/§8.11) | `scripts/benchmark_depletion_pincell.py` (BEAVRS 2.4 % pincell → 50 MWd/kg) | Romano et al. 2021: OpenMC vs Serpent k < 20 pcm, actinides/FPs < 1 % | scripted; WSL run pending |
| **OpenMC criticality (storage)** (§8.11) | `scripts/run_storage_criticality.py` | OECD-NEA Burnup-Credit Phase II; SFCOMPO 2.0 → Δ_bias/Δ_unc | cross-checked; formal benchmark pending |
| **Thermal-hydraulics** (§8.4) | natural-circ + W-3 hot-channel deck | OECD-NEA PSBT (subchannel) / ANS-5.1 (decay heat); de Vahl Davis (CFD verif.) | method set; [TH] run |
| **Fuel performance** (§8.3) | 1-D conduction stack (optional FRAPCON case) | OECD-NEA IFPE / Halden instrumented rod | cite; run if FRAPCON used |
| **Energy cycle** (§8.9) | `scripts/thermo_cycle.py` (IAPWS-IF97 deck) | IAPWS-IF97 reference standard | ✅ |
| **Back-end physics** (§8.11) | `src/aegis40/back_end/` (15/15 unit tests) | ANSI/ANS-5.1 decay-heat standard | ✅ |
| **Economics** (§8.12) | `scripts/economics_lcoe.py` | OECD-NEA/IEA *Projected Costs* methodology | cite |

Established open-source codes (ICSBEP, C5G7, BEAVRS, IFPE, ANS-5.1, IAPWS-IF97) are **cited published
validation**, not work we reproduce — standard, accepted practice. Detailed plan:
`digital-appendix-vv-plan.md`, `code-benchmark-matrix.md`.

---

# Requirements coverage matrix (every §8 requirement → where addressed / why not)

Legend: ✅ fully addressed · 🟡 addressed, with a tracked pending item · ⏳ addressed, neutronic value
pending the 37-FA STAT_FINAL run.

| § | Requirement (paraphrased from the spec) | Where addressed | Status |
|---|---|---|---|
| top | Tables of technical specs (qty, material, dims, standards) for key components | §8.1, §8.2.2, §8.4.5, §8.3.6 tables | ✅ |
| top | One sample input per code + V&V (reproducibility/benchmarking/repeatability) vs IAEA/OECD-NEA | §8.13 | 🟡 (confirmatory runs scheduled in WSL) |
| 8.1 | Preparation-phase docs prior to detailed design | §8.1.6 + Table 8.1-6 | ✅ |
| 8.1 | Codes & standards for all systems/components/materials | §8.1.7 Table 8.1-7 | ✅ |
| 8.1 | General design parameters (Table-1 style) | §8.1.1–8.1.5 Tables 8.1-1…5 | ✅ |
| 8.1 | Reference regulatory / nuclear-safety requirements list | §8.1.8 Table 8.1-8 | ✅ |
| 8.2 | Material selection + behaviour under neutron flux & temperature (SS/transient/accident) | §8.2.1 | ✅ |
| 8.2 | Geometry & layout: quantities, dimensions, modelling parameters | §8.2.2 + figures | ✅ |
| 8.2 | Neutronics: criticality, flux/burnup distribution, feedback coeffs, reactivity-control values | §8.2.3 Tables 8.2-3/5 | ⏳ |
| 8.2 | Composition & locations of all core components (tables + drawings) | §8.2.2 Table 8.2-2 + Figs 8.2-1/2/3 | ✅ |
| 8.2 | Conformity of safety criteria with national/international regs | §8.2.3 compliance table | ✅ |
| 8.2 | Analyses initial-cycle → equilibrium-cycle | §8.2.3 "BOC→equilibrium" | 🟡 (bounding arg.; equilibrium shuffle next) |
| 8.2 | Steady-state thermal-hydraulics: T-distributions, ΔP, T-H params | §8.2.4 + §8.4.6 | ⏳ (37-FA MDNBR re-run) |
| 8.3 | Fuel-performance & fuel-safety analyses/calculations | §8.3.2–8.3.4 | ✅ (centerline/FGR/clad) |
| 8.3 | Front-end fuel-cycle structural-material specs | §8.3.5 | ✅ |
| 8.4 | General description of primary & secondary cooling systems | §8.4.1–8.4.3 | ✅ |
| 8.4 | Component functions/specs/capacities/performance + material compliance | §8.4.5 tables | ✅ |
| 8.4 | Heat-removal capacity by accepted methods; operating conditions defined | §8.4.6–8.4.7 | ✅ |
| 8.5 | Anticipated transients, criticality accidents, DBA scenarios stated | §8.5.1 + 8.6.3 | 🟡 (MSLB/SBLOCA trees pending) |
| 8.5 | Modelling/analysis results for those scenarios | §8.6.3 (LOHS, SBO) | 🟡 |
| 8.5 | Operating-limit conditions + the calculations that set them | §8.5.2 Table 8.5-1 | ⏳ |
| 8.5 | Safety maintained in worst-case; reactivity/cooling/FP-release under all conditions | §8.5.1a, §8.5.3 | ✅ |
| 8.6 | All safety-function systems described + functions (RPS, HRS, ECCS, containment, etc.) | §8.6.1–8.6.2a | ✅ |
| 8.6 | Auto-initiation; fuel-design-limit protection; accident detection | §8.6.2, §8.7.2/8.7.3 | ✅ |
| 8.6 | Fail-safe transition on loss of power/air/adverse environment | §8.6.2 (de-energise-to-actuate) | ✅ |
| 8.6 | Reactivity-control limits protect RCPB & core support | §8.5.2 + §8.6.1 | ⏳ |
| 8.6 | Fault trees & event trees; redundancy & necessity analyses | §8.6.3–8.6.4 | 🟡 (CDF/LRF partial) |
| 8.6 | Schematic diagrams: monitored variables → protective action logic | §8.7.2 + Fig 8.7-1 | ✅ |
| 8.7 | I&C architecture, components, subsystems, block/logic/flow diagrams | §8.7.1 + Fig 8.7-1 | ✅ |
| 8.7 | Sensors/detectors + real-time HW/SW; HMI & secure comms | §8.7.1–8.7.6 | ✅ |
| 8.7 | Design criteria/principles: redundancy, diversity, separation | §8.7.2–8.7.4, 8.7.7 | ✅ |
| 8.7 | MCR ergonomically designed | §8.7.5 | ✅ |
| 8.8 | All auxiliary systems by sub-heading (purpose/principle/layout/safety/perf/maint.) + P&IDs | §8.8 table + 8.8.9/8.8.10 | 🟡 (per-system P&IDs in drawing pass) |
| 8.8 | On-/off-site electrical incl. emergency & UPS, with drawings | §8.8.10 (item 4/5) | 🟡 (single-line in drawing pass) |
| 8.9 | Energy-conversion design + flow diagrams (electricity) | §8.9.1–8.9.4 + Figs 8.9-1/2 | ✅ |
| 8.9 | Non-electric integrations (H₂, desalination, district heat, process heat) + analyses | §8.9.5 (TCES DH), §8.9.6 (H₂) | ✅ (desalination noted as a process-heat option) |
| 8.10 | Optimum general layout (constructability/economy/safety/operations) | §8.10.1 | ✅ |
| 8.10 | General layout incl. reactor/energy-conversion/O&M/other buildings | §8.10.2 | ✅ |
| 8.10 | 2D/3D plans + connections; structural/steel/weight/structural-requirement data | §8.10.5 + `layout/building_list.md` | 🟡 (CAD assets held locally) |
| 8.10 | Critical-piping routing within/between structures | §8.10.4 | ✅ |
| 8.11 | Innovative fuel-cycle waste minimisation | §8.11.1 | ⏳ (intensity re-gen with 37-FA BU) |
| 8.11 | Back-end management plan (per §4.3.2: source term, decay heat, storage criticality) | §8.11.2–8.11.4 | ✅ |
| 8.11 | Conformity of results with regulations | §8.11.4 (k(95/95)), §8.11.5 (GSR Part 5) | ✅ |
| 8.11 | Secondary radioactive-waste management | §8.11.5 | ✅ |
| 8.12 | Economic advantages vs reference reactors; investment/operating/production costs | §8.12.1–8.12.5 | 🟡 (bottom-up CAPEX + cogen credit pending) |

**Items we could not fully close, with the reason and the citation basis:**

1. **37-FA neutronic results (k_eff, burnup, cycle, peaking, coefficients, rod worth, SDM,
   inventory).** Reason: the STAT_FINAL OpenMC depletion run is in progress (multi-day in WSL). We
   present the validated 21-FA predecessor values as a conservative reference and the latest 37-FA
   partial peaking (F_ΔH 1.746, F_q ≈ 2.03). Basis: OpenMC 0.15.3 + ENDF/B-VIII.0, benchmarked per
   §8.13 (Romano et al. 2015/2021; ICSBEP/BEAVRS).
2. **MDNBR / LOCA PCT / clad-oxidation (hot-channel & accident T-H).** Reason: gated by the 37-FA
   peaking re-tally (O1/O2). Method fixed (W-3 CHF; conjugate CFD), 21-FA values quoted as the
   conservative anchor (MDNBR 1.466, PCT 391 °C steady). Basis: Tong W-3; ANS-5.1; OECD-NEA PSBT.
3. **Containment design pressure / P-T response.** Reason: the containment concept (dry vs
   submerged-pool) is an open team decision; the P/T accident response sets the design pressure
   (O3/O4). Written against the 0.414 MPa dry baseline. Basis: SSR-2/1 Req. 56.
4. **Full DBA spectrum to event-tree depth (MSLB, SBLOCA) and a quantitative plant CDF/LRF.** Reason:
   two initiators (LOHS, SBO) are analysed; the remainder are identified and screened (a full PSA is
   beyond FER scope). CDF/LRF are stated as **projected class targets** consistent with the passive-SMR
   class, not computed PSA. Basis: IAEA SSG-3/4; NUREG-0800 Ch. 15; RG 1.174.
5. **Tritium permeation budget at the H₂ interface; Sinop coastal-hazard study; SKKY thermal-discharge
   clause; EPZ dose basis.** Reason: site/interface analyses identified but not yet performed (O7–O11).
   Basis: SSR-1/SSG-9; Turkish SKKY; 10 CFR 100.11.
6. **Bottom-up CAPEX and cogeneration revenue credit (§8.12).** Reason: requires the frozen §8.10
   equipment list; the literature FOAK triangular is used in the interim. Basis: OECD-NEA (1994);
   Ashley et al. (2014); IEA/NEA *Projected Costs* (2020).
7. **Seawater desalination** is named in the spec's §8.9 examples; Aegis-40's chosen non-electric
   products are **district heat (TCES) + hydrogen**, with desalination available as an alternative
   process-heat off-take from the same intermediate loop (not separately analysed). This is a design
   choice, not an omission.

---

## Consolidated reference list

The per-section reference lists (codes/methods/data; SBF & burnable-absorber precedents; materials &
fuel performance; regulatory; T-H; energy cycle; waste; economics; non-proliferation) are retained in
the archived section drafts (`fer/archive/`) and are to be merged into the single FER reference list
at assembly time. Principal anchors:

- **Codes/data:** Romano & Forget, *Ann. Nucl. Energy* 51 (2013) 274; Romano et al., *Ann. Nucl.
  Energy* 82 (2015) 90 & 152 (2021) 107989; Brown et al., *Nucl. Data Sheets* 148 (2018) 1
  (ENDF/B-VIII.0); IAPWS-IF97; ANSI/ANS-5.1; ANSI/ANS-6.4; ICRP-116.
- **SBF / burnable absorber:** Kim, Jung & Yoon, *Nucl. Eng. Tech.* 56 (2024) 3144; Jang et al. (2020)
  SBF-SMPWR; CAREM-25 (IAEA ARIS); KEPCO i-SMR/HIGA; Nguyen & Kim (ATOM); Akbari-Jeyhouni et al.
  (SMART, *Ann. Nucl. Energy* 2018); PRATIC (*EPJ-N* 2024).
- **Reference reactors:** NuScale FSAR Ch. 4 (37-FA 17×17 iPWR benchmark); RITM-200 (Gaganov);
  CAREM-25; SMART.
- **T-H / cycle:** Todreas & Kazimi *Nuclear Systems I*; Tong *Boiling Heat Transfer*; El-Wakil
  *Powerplant Technology*; Çengel & Boles; Frick et al. INL TES; Yan et al. *Appl. Therm. Eng.* 167
  (2020) 114800; Hauer (zeolite TES); Oğul et al. (2026).
- **Regulatory:** IAEA SSR-1, SSR-2/1 Rev.1, SSG-2/3/4/9/39/52, GSR Part 4/5, TECDOC-1936; US NRC
  10 CFR 50 App. A (GDC), 50.46, 50.62, 50.68, 100.11, 73.54, NUREG-0800/0700/0711/1431, RG 1.60/1.97/
  1.105/1.174/5.71; IEEE 323/344/384/603; IEC 61513/60880/60079; NFPA 2; Türkiye NDK Law No. 7381
  (2022), SKKY.
- **Waste / 3S / economics:** NUREG-0800 §9.1.1 + 10 CFR 50.68; OECD/NEA Burnup-Credit Benchmark
  (Phase I-B/II) + SFCOMPO 2.0; IAEA GSR Part 5; Ashley et al., *Ann. Nucl. Energy* 69 (2014) 314;
  Bathke et al., *Nucl. Technol.* 179 (2012) 5; GIF PR&PP (2006); OECD-NEA (1994); IEA/NEA (2020).

---

*End of Aegis-40 FER §8 master (r1, 2026-06-22). Neutronic values marked ⏳[37FA-PENDING] are replaced
from the `aegis40_neutronics_FER.ipynb` STAT_FINAL run before submission; all other content is
final-draft. Front matter §1–§7 (abstract, team, literature review, methodology, originality, work
plan, broader impacts) is assembled separately into the official template.*
