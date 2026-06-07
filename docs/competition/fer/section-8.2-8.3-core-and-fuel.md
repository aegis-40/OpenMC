# FER §8.2 Core Design & §8.3 Fuel and Material Design — Aegis-40 iPWR

> **Drafting status (2026-06-07).** FER-ready draft for Samira's sections. All neutronic
> numbers are the LOCKED rev_3 values from `design-basis-locked.md` (OpenMC 0.15.3 full-core
> run). Fuel-performance numbers in §8.3 are engineering estimates from **standard correlations
> and published data** (no new simulation), with every assumption stated. Figure/table callouts
> and `‹INSERT …›` notes mark where the CAD/3D images and the §8.4 thermal-hydraulic inputs go.
>
> **Resolved (2026-06-07):** outer-ring Gd count = **24** (as-run OpenMC model, confirmed by Samira).
> The draft uses 48 / 40 / 24 (core-average 32). `design-basis-locked.md` Table 1 updated to match.

---

## 8.2 Core Design

The Aegis-40 reactor core is the integral-PWR (iPWR) heat source for a 40 MWe / 125 MWth
soluble-boron-free (SBF) modular plant. The core is a compact light-water-moderated,
light-water-cooled lattice of 21 fuel assemblies (FAs) on a 17×17 square pin array, operated on
a four-batch reload to an equilibrium cycle of ~16 months. The defining design choice — operation
**without soluble boron** — removes the chemical-shim system and its dilution-accident pathway,
but transfers all excess-reactivity hold-down to **solid burnable absorbers (Gd₂O₃ + Er₂O₃)** and
**control-rod clusters**. The sections below present the material selection and its behaviour under
irradiation and temperature, the core geometry and layout and the criteria behind it, and the
neutronic analysis from beginning-of-cycle (BOC) toward the equilibrium cycle.

‹INSERT FIGURE 8.2-1 — Core isometric / RPV cutaway (3D CAD, in preparation in Fusion 360 / Creo).
Show the 21-FA array, core barrel, and reflector. Until the render is ready, the 2D core loading
map (Figure 8.2-4) carries this.›

### 8.2.1 Material Selection

Material selection follows three criteria, in priority order: (i) neutronic suitability for an SBF
high-burnup core, (ii) demonstrated in-pile performance and a qualified property database to
~50 GWd/MTU, and (iii) compatibility across the steady-state, transient (anticipated operational
occurrence, AOO), and accident temperature ranges. The selections are summarised in Table 8.2-1.

**Table 8.2-1 — Core material selection and rationale**

| Core component | Material | Selection rationale |
|---|---|---|
| Fuel | UO₂, enriched 4.95 / 4.70 / 4.40 wt% ²³⁵U (radial zones) | Reference LWR fuel; highest qualification base; high melting point (~2840 °C); enrichment ≤ 5.0 wt% keeps within the commercial LEU licensing/fabrication envelope. |
| Cladding | Zircaloy-4 (Zr-4) | Low thermal-neutron absorption, qualified to high burnup, well-characterised corrosion/creep database; locked design choice. |
| Burnable absorber (primary) | Gd₂O₃ at 8 wt%, admixed in UO₂, radially zoned | Strong BOC hold-down (Gd-155/157); burns out by ~10 GWd/t; integral (no separate hardware) — the SBF excess-reactivity solution. |
| Burnable absorber (secondary) | Er₂O₃ at 0.5 wt%, admixed in UO₂ | Slow-depleting "residual" hold-down that flattens reactivity through mid/late cycle and adds cold shutdown margin; the erbia-credit enabler of long SBF cycles. |
| Coolant / moderator | Light water (H₂O) | Reference PWR coolant and moderator; negative moderator temperature coefficient by design; self-regulating. |
| Reflector | Light water (radial 20 cm, axial 30 cm each end) | Returns leakage neutrons, flattens the power shape, and protects the barrel/vessel; no separate solid reflector required at this size. |

**Behaviour under irradiation and across the temperature range.** The materials are demonstrably
suitable across the operating envelope:

- **UO₂ fuel.** Stable fluorite-structure ceramic with a high melting point (~2840 °C fresh,
  decreasing ~0.5 °C per GWd/t with burnup). Thermal conductivity degrades with both temperature
  and burnup (Lucuta/Halden correlations), which is bounded in §8.3 by the centerline-temperature
  analysis. At the Aegis-40 **low core specific power (~24 MW/tHM)** the linear heat rates are
  modest (§8.3), so fuel temperatures stay far below melting in steady state and in the bounding
  AOO. Fission-gas release and pellet swelling are accommodated by the as-built dish/chamfer and
  the gas plenum (§8.3).
- **Gd₂O₃ / Er₂O₃ absorbers.** Admixed in the UO₂ matrix; their only "transient" behaviour is
  intended burn-out, which is the reactivity-management mechanism itself (§8.2.3). The 8 wt% Gd
  loading is within qualified gadolinia-fuel practice; the small (≤1 wt%) reduction in local melting
  margin from gadolinia is bounded because Gd rods sit in the lower-power interior of the zoning map.
- **Zircaloy-4 cladding.** Qualified to high burnup; corrosion (oxide thickness), hydrogen pickup,
  irradiation creep and growth, and fast-fluence embrittlement are all bounded by the moderate
  discharge burnup of **42.8 GWd/MTU** — comfortably below the 62 GWd/MTU rod-average regulatory
  ceiling for Zr-4 — leaving margin on every clad damage mechanism (§8.3). Under accident heat-up,
  Zr-4 behaviour (oxidation kinetics, ballooning, the 1204 °C peak-clad-temperature limit) is the
  basis for the §8.5 LOCA criteria.
- **Light water.** Reference behaviour; the strongly negative moderator and void coefficients
  (Table 8.2-3) make the coolant a passive stabiliser under power and temperature excursions.

‹INSERT FIGURE 8.2-2 — Sectioned fuel-rod cutaway (pellet / gap / Zr-4 clad / end plugs / plenum).
Use the dimensioned end-plug cross-section `cad/end_plug_detail.png` now; replace with the 3D pin
cutaway when the Fusion model is rendered.›

### 8.2.2 Geometry and Layout

The core geometry is the standard Westinghouse-type 17×17 lattice, sized down to 21 assemblies for
the 125 MWth rating. Choosing a **qualified 17×17 geometry** (rather than a novel lattice) maximises
the credibility of the borrowed fuel/clad property database and the thermal-hydraulic correlations,
and concentrates the originality where it belongs — the boron-free reactivity scheme. Dimensions are
taken directly from the as-built OpenMC geometry and are listed in Table 8.2-2.

**Table 8.2-2 — Core and fuel geometry (as-modeled, LOCKED)**

| Feature | Value | Note |
|---|---|---|
| Lattice | 17 × 17 square, 289 positions/FA | 264 fuel + 24 guide + 1 instrument |
| Fuel pellet diameter | 8.192 mm | |
| Pellet–clad radial gap | 0.0915 mm | |
| Cladding OD / ID | 9.520 / 8.375 mm (0.573 mm wall) | Zr-4 |
| Pin pitch | 12.623 mm | |
| Active fuel height | 2000 mm | + 300 mm H₂O axial reflector each end |
| Guide / instrument tube OD / ID | 12.040 / 11.248 mm | control-rod & in-core channels |
| Assembly pitch (in core) | 216.038 mm | inter-assembly water gap ≈ 1.45 mm |
| Number of assemblies | 21 (5×5 lattice, 4 corners removed) | |
| Equivalent core diameter | ≈ 1117 mm | |
| Radial / axial reflector | 200 mm / 300 mm H₂O | |
| Control-rod clusters | 9 | insert into guide tubes; 9 CRDMs |
| Heavy-metal loading | ≈ 5.3 tHM | |

**Fuel-element quantity and dimensions.** The 264 fuel pins per FA, 2.0 m active height, and 21-FA
count are set jointly by the power rating and the fuel-efficiency target: the resulting low specific
power (~24 MW/tHM) is deliberate — it buys thermal-margin (low linear heat rate, §8.3) and supports
the long SBF cycle needed for high discharge burnup with a four-batch scheme.

**Power-control systems.** Reactivity is controlled by two integral mechanisms (no soluble boron):

- *Burnable absorbers.* Gd₂O₃ (8 wt%) provides the dominant BOC hold-down and is **radially zoned**
  — more Gd toward the core centre — to flatten the radial power shape (§8.2.3, Table 8.2-4). Er₂O₃
  (0.5 wt%) provides slow residual hold-down and cold shutdown margin. Per-FA absorber counts by
  core ring are given in Table 8.2-4. The three FA "recipes" (centre / inner ring / outer ring) are
  shown in Figure 8.2-3.
- *Control rods.* Nine control-rod clusters insert into the guide-tube channels, providing
  shutdown and operational control with a total worth of 15,226 pcm (Table 8.2-3).

‹INSERT FIGURE 8.2-3 — Fuel-assembly pin maps for the three core recipes (centre / inner / outer
ring), coloured by enrichment and by Gd/Er pin. Source figure ready: `cad/fa_pinmaps.png`.›

‹INSERT FIGURE 8.2-4 — Core loading map, 21 FA on the 5×5-minus-corners lattice, coloured by ring
(enrichment + Gd zoning). Source figure ready: `cad/core_map.png`. Optional companion:
`cad/guide_tube_map.png` showing the 24+1 guide/instrument-tube positions.›

**Table 8.2-4 — Burnable-absorber loading by core ring (radial Gd zoning)**

| Core ring | # of FAs | Gd₂O₃ rods / FA | Er₂O₃ rods / FA | Relative Gd density |
|---|---|---|---|---|
| Centre | 1 | 48 | 16 | 1.50 |
| Inner ring | 8 | 40 | 16 | 1.24 |
| Outer ring | 12 | 24 | 16 | 0.80 |
| **Core average** | 21 | **32** | 16 | 1.00 (conserved) |

> The zoning redistributes the **same core-average Gd** toward the centre (density weights
> 1.50 / 1.24 / 0.80), which conserves BOC reactivity while flattening the radial power — see the
> peaking result in Table 8.2-5.

### 8.2.3 Neutronic Analysis

The neutronic design was performed with **OpenMC 0.15.3** continuous-energy Monte Carlo on the
full 3D core (21 FAs, axial and radial water reflectors, vacuum outer boundary), with coupled
depletion from BOC through the approach to the equilibrium cycle. The transport statistics are
180 batches / 50 inactive / 20,000 neutrons per batch. Results are summarised in Tables 8.2-3 and
8.2-5; the cycle reactivity behaviour is in Figure 8.2-5.

**Criticality and reactivity control.** The fresh core is slightly supercritical (k_eff,BOL =
1.0264), with the excess reactivity held down by the integral burnable absorbers and managed by the
control-rod system. All reactivity-control and shutdown criteria are met with margin (Table 8.2-3).

**Table 8.2-3 — Neutronic safety results (LOCKED rev_3) — all criteria met**

| Parameter | Value | Limit / criterion | Status |
|---|---|---|---|
| k_eff, BOL | 1.0264 | excess managed by BA + rods | INFO |
| Moderator temperature coefficient (HFP) | −35.9 pcm/K | < 0 | PASS |
| Doppler (fuel) temperature coefficient | −1.84 pcm/K | < 0 | PASS |
| Void coefficient | −214 pcm/%void | < 0 | PASS |
| Control-rod worth (ARO → ARI) | 15,226 pcm | ≥ 5,000 | PASS |
| Shutdown margin | 12.4 %Δk/k | ≥ 1.0 | PASS |
| k_eff, all-rods-in (ARI) | 0.888 | < 0.95 (subcritical) | PASS |
| k_eff, worst-stuck-rod (N−1) | 0.890 | < 1.0 | PASS |
| Max reactivity insertion rate | 1.5 × 10⁻⁵ Δk/k/s | ≤ 7.5 × 10⁻⁴ | PASS |
| Maximum enrichment | 4.95 wt% | ≤ 5.0 | PASS |

**Feedback coefficients.** All three reactivity feedbacks are negative (Table 8.2-3): the moderator
(−35.9 pcm/K), Doppler (−1.84 pcm/K), and void (−214 pcm/%void) coefficients together make the core
inherently self-regulating against power, temperature, and voiding excursions — the central
inherent-safety claim and the basis for the §8.5 transient response.

**Power distribution (peaking).** Because there is no soluble boron to flatten the radial shape, the
radial Gd zoning (Table 8.2-4) is the primary power-flattening tool. It reduces the assembly radial
peaking by 24% relative to an unzoned core while conserving BOC reactivity (Table 8.2-5).

**Table 8.2-5 — Power-peaking, unzoned → radially-zoned core**

| Peaking factor | Unzoned (rev_2) | Zoned (rev_3) | Δ |
|---|---|---|---|
| F_radial (assembly) | 1.62 | **1.23** | −24% |
| F_ΔH (radial enthalpy-rise) | 2.77 | **2.27** | −18% |
| F_q (3D total) | 3.62 | **3.48** | −4% |
| F_z (axial) | — | 1.03 | — |

> These are thermal-margin (DNBR) inputs, not stand-alone pass/fail gates. For context, the Jang
> SBF-SMPWR design limit is F_q < 5.09 and the KEPCO i-SMR (HIGA) SBF core runs F_q ≈ 2.08 — the
> Aegis-40 rev_3 value sits well inside the SBF-SMR class. The binding thermal limit is the §8.4/§8.5
> MDNBR analysis.

‹INSERT FIGURE 8.2-5 — Cycle reactivity (k_eff vs burnup, BOC → EOC) from the depletion run.
Source: the depletion-curve plot in `aegis40_3d_core_outputs/` (export PNG from the notebook).
Annotate the three regimes described below.›

‹INSERT FIGURE 8.2-6 — Radial assembly-power map (BOC) and axial flux/power profile, illustrating
the flattened shape after zoning. Export from the notebook tallies.›

**BOC → equilibrium cycle behaviour.** The depletion k_eff curve **dips, then rises, then declines**
(k_BOL 1.0264 → dip ≈ 0.98 → Gd-burnout hump → k_EOC ≈ 0.876 at the 479 EFPD cycle). This shape is
the expected signature of a Gd-controlled boron-free core, and is intended:

1. **Dip (first days):** equilibrium xenon builds in (~−2700 pcm).
2. **Rise (~0–400 EFPD):** fresh Gd-155/157 hold k down at BOL; as they burn out their absorption
   disappears faster than the fuel depletes, so net k climbs — the reactivity "stored" in the Gd is
   released to sustain the long SBF cycle.
3. **Decline (post-burnout):** normal fuel-depletion fall-off to EOC.

This is consistent with published integral-Gd SBF behaviour (Kim, Jung & Yoon, *Nucl. Eng. Tech.*
56 (2024) 3144), which describes the reactivity "holding" and the engineered control of the
"reactivity upswing following gadolinia depletion." In a boron-controlled core the curve only falls;
the hump is the distinguishing feature of integral-Gd SBF control.

**Compliance with safety criteria / regulations.** The neutronic safety parameters (Table 8.2-3)
meet the adopted criteria, which map directly onto national (Türkiye NDK) and international
(IAEA, US NRC) requirements:

| Neutronic result | Criterion met | Regulatory basis |
|---|---|---|
| MTC, DTC, void all < 0 | inherent negative power/temperature feedback | NDK *Nuclear Power Plant Design Regulation* (reactivity-feedback provisions) [ref T-1]; IAEA SSR-2/1 Rev.1 Req. 35 [ref I-1]; US NRC 10 CFR 50 App. A GDC 11 [ref N-1] |
| Two independent control means (rods + integral BA), CR worth 15,226 pcm | redundant, independent reactivity control | IAEA SSR-2/1 Req. 24–25 [ref I-1]; GDC 26 & 27 [ref N-1] |
| SDM 12.4 %Δk/k; k_ARI 0.888; worst-stuck-rod (N−1) 0.890 < 1.0 | shutdown margin with most-reactive rod stuck; subcriticality with single failure | IAEA SSR-2/1 Req. 25; GDC 26 [ref N-1] |
| Max enrichment 4.95 wt% ≤ 5.0 | LEU fabrication/licensing limit | commercial LEU limit; IAEA fuel-safety guidance |

Türkiye's nuclear activities are licensed by the **Nükleer Düzenleme Kurumu (NDK)** under the
Nuclear Regulation Law (No. 7381, 2022), whose design framework adopts the IAEA Safety Standards;
the criteria above are therefore satisfied under the national regime as well as the IAEA/NRC
references. ‹Confirm the exact NDK regulation title/article the team standardises on and align with
the §8.1 codes-and-standards list.›

### 8.2.4 Steady-State Thermal-Hydraulic Analysis (inputs & interface to §8.4)

> **Owner interface:** the steady-state T-H solution (temperature distributions, pressure drops,
> MDNBR) is produced under §8.4/§8.5 (T-H lead). This subsection records the **core-side boundary
> conditions** the neutronic and fuel-performance analyses assume, so the two stay consistent.

The fuel-performance evaluation in §8.3 adopts the following representative primary-side conditions
(to be **confirmed by the §8.4 analysis**): system pressure ≈ 12.8 MPa; core inlet ≈ 265 °C; core
outlet ≈ 305 °C; core-average coolant ≈ 285 °C. The low core specific power (~24 MW/tHM) and the
moderate peaking (Table 8.2-5) give large subcooling and DNBR margin characteristic of the low
power-density SBF-SMR class. ‹INSERT the §8.4 results table (radial/axial coolant & clad temperature
distributions, core pressure drop, MDNBR) when available.›

---

## 8.3 Fuel and Material Design

This section presents the fuel and structural-material design and the fuel-performance / fuel-safety
demonstration. Consistent with the brief, the analysis uses **established correlations and published
in-pile data** rather than new simulation; each calculation states its method, inputs, and
assumptions, and all conditions are bounded by the core design of §8.2.

### 8.3.1 Fuel and Structural Material — Technical Data

**Table 8.3-1 — Fuel and cladding property summary (literature)**

| Property | UO₂ fuel | Zircaloy-4 cladding |
|---|---|---|
| Form / dimensions | Sintered pellet, Ø8.192 mm, ~95% TD | Tube OD 9.520 / ID 8.375 mm, 0.573 mm wall |
| Density | ~10.4–10.5 g/cm³ (95% TD) | 6.55 g/cm³ |
| Melting point | ~2840 °C (fresh; ↓ ~0.5 °C/GWd-t with burnup) | ~1850 °C (β-phase); design heat-up limit 1204 °C (LOCA PCT) |
| Thermal conductivity | ~3–8 W/m·K, decreasing with T and burnup (Lucuta/Halden) | ~17 W/m·K (≈ const. over range) |
| Coeff. thermal expansion | ~10 × 10⁻⁶ /K | ~6 × 10⁻⁶ /K |
| Neutronic role | fissile/fertile matrix; Doppler broadening (−1.84 pcm/K) | low absorption (~0.2 b) |
| Qualified burnup | reference LEU practice to ~62 GWd/t | rod-avg ≤ 62 GWd/t (regulatory ceiling) |

Property sources to cite: IAEA-TECDOC thermophysical properties of UO₂/Zr-4; Todreas & Kazimi,
*Nuclear Systems I*; Halden Reactor Project fuel-behaviour data. ‹Insert exact references.›

### 8.3.2 Linear Heat Rate and Power Density (design basis for fuel performance)

The fuel-duty inputs follow directly from §8.2:

- Fuel rods in core: 21 FA × 264 = **5,544 rods**; active length 2.0 m → 11,088 m of fuel.
- **Core-average linear heat rate** q′_avg = 125 MW / 11,088 m ≈ **11.3 kW/m**.
- **Peak linear heat rate** q′_peak = q′_avg × F_q = 11.3 × 3.48 ≈ **39.2 kW/m**.
- Core specific power ≈ 125 MW / 5.3 tHM ≈ **23.6 MW/tHM**.

The peak linear heat rate (~39 kW/m) is below the classic LWR design guideline (~43 kW/m / 13 kW/ft),
and the core-average value is well under a large-PWR average (~17.5 kW/m) — a direct consequence of
the low-power-density, fuel-efficiency-driven design. This is the root of the thermal margin claimed
throughout §8.2–§8.5.

### 8.3.3 Fuel-Performance Analysis — Centerline Temperature

The peak-rod steady-state fuel centerline temperature is built up from the coolant through each
thermal resistance using standard one-dimensional conduction relations (Todreas & Kazimi). Inputs:
q′_peak = 39.2 kW/m; pellet Ø8.192 mm; gap 0.0915 mm; clad as Table 8.2-2; coolant boundary from
§8.2.4. Heat-transfer coefficient h ≈ 34,000 W/m²·K; BOL gap conductance h_gap ≈ 6,000 W/m²·K;
k_clad ≈ 17 W/m·K; effective k_fuel ≈ 3 W/m·K (high-temperature value, conservative).

**Table 8.3-2 — Peak-rod temperature stack-up (BOL, steady state, engineering estimate)**

| Resistance | ΔT (K) | Method |
|---|---|---|
| Bulk coolant (local hot) | — (≈ 315 °C) | from §8.2.4 / §8.4 |
| Film (convective), q″≈1.3 MW/m² | ~39 | ΔT = q″/h |
| Clad conduction | ~47 | ΔT = q′·ln(r_o/r_i)/(2πk_clad) |
| Pellet–clad gap (BOL) | ~250 | ΔT = q″_gap/h_gap |
| Fuel pellet (surface → centre) | ~1,100 | ∫k dT = q′/4π, k_fuel≈3 |
| **Peak centerline (estimate)** | **≈ 1,750 °C** | sum |

**Result and margin.** The estimated peak fuel centerline temperature (~1,750 °C, BOL hot rod) sits
roughly **1,090 °C below the UO₂ melting point** (~2,840 °C) — i.e. the hot-spot fuel runs at ~62%
of melt on an absolute scale, a large no-melt margin. The gap term dominates and shrinks as the gap
closes with burnup; fuel-conductivity degradation with burnup partially offsets this, so the peak
centerline is not expected to exceed the BOL estimate through life. ‹Refine with the §8.4 coolant
boundary and, if desired, a FRAPCON-class run for the Digital Appendix; current value is a bounding
hand-calculation.›

### 8.3.4 Fission-Gas Release, Rod Internal Pressure, and Clad Integrity

- **Fission-gas release (FGR).** With most of the pellet volume below ~1,000 °C, FGR is governed by
  the Halden threshold (onset ~1% below ~1,000 °C, rising with temperature and burnup). At the
  Aegis-40 moderate linear heat rates and 42.8 GWd/MTU discharge burnup, peak-rod EOL FGR is expected
  to be modest (order ≤ 10–15%). The fuel rod includes a **gas plenum** (~180 mm, with hold-down
  spring) sized so that the end-of-life rod internal pressure stays below the system pressure
  (no clad lift-off / no gap re-opening). ‹Confirm plenum sizing against the FGR estimate.›
- **Cladding stress and corrosion.** The Zr-4 clad carries the coolant-to-rod pressure differential
  (compressive at BOL) within primary-membrane allowables; waterside corrosion (oxide-thickness
  limit ~100 µm), hydrogen pickup, irradiation creep/growth, and fast-fluence embrittlement are all
  bounded by the moderate **42.8 GWd/MTU** discharge burnup — well below the 62 GWd/MTU Zr-4 ceiling —
  leaving margin on every clad damage mechanism. Accident-condition clad behaviour (oxidation,
  ballooning, 1204 °C PCT and 17% ECR limits) is carried in §8.5.
- **Pellet–clad mechanical interaction (PCMI).** Mitigated by the dished/chamfered pellet geometry
  and the low-ramp operating strategy of a base-load SMR; bounded by the low peak linear heat rate.

‹INSERT FIGURE 8.3-1 — Fuel-rod construction / end-plug cross-section. Ready now:
`cad/end_plug_detail.png` (pellet stack, gap, Zr-4 clad, stepped end plugs, plenum spring). Replace
with the 3D sectioned-pin render when available.›

### 8.3.5 Front-End Fuel-Cycle Structural Materials

The front-end fuel-cycle hardware (assembly skeleton: top/bottom nozzles, guide/instrument thimbles,
spacer grids, hold-down springs) uses the qualified LWR material set: **Zircaloy-4 / Zirlo-class**
guide thimbles and grids for low parasitic absorption in the active region, and **stainless steel
(304/308) / Inconel-718** for the nozzles and hold-down springs where strength and relaxation
resistance dominate over neutronics (outside the active height). Selection criteria: low neutron
absorption in-core, corrosion compatibility with the primary coolant chemistry, dimensional
stability under irradiation growth, and spring-force retention over life. ‹Add a short table of
skeleton components × material × function if page budget allows; cross-reference the §8.10/§8.8 fuel
handling & storage hardware.›

---

## References for §8.2 / §8.3 (assemble into the FER reference list)

> Citation discipline is template pass/fail — every non-common-knowledge claim above is keyed here.
> Fill in volume/page/DOI in the team's reference style before upload.

**Codes, methods & nuclear data**
- [C-1] P. K. Romano et al., "OpenMC: A state-of-the-art Monte Carlo code for research and
  development," *Ann. Nucl. Energy* 82 (2015) 90–97. — transport/depletion solver (OpenMC 0.15.3).
- [C-2] D. A. Brown et al., "ENDF/B-VIII.0," *Nucl. Data Sheets* 148 (2018) 1–142. — cross-section
  library used. ‹confirm the exact library/version run in the notebook.›
- [C-3] N. E. Todreas, M. S. Kazimi, *Nuclear Systems I: Thermal Hydraulic Fundamentals* — linear
  heat rate, conduction stack-up, centerline-temperature method (§8.3.2–8.3.3).

**SBF / burnable-absorber precedents**
- [S-1] Kim, Jung & Yoon, "…gadolinia reactivity holding / upswing control," *Nucl. Eng. Tech.* 56
  (2024) 3144. — integral-Gd SBF reactivity behaviour (the k-hump, §8.2.3).
- [S-2] Jang et al. (2020), SBF-SMPWR 17×17 design — F_q < 5.09 peaking limit, 8 wt% Gd precedent.
- [S-3] CAREM-25 (CNEA) — reference boron-free integral PWR with Gd₂O₃ absorbers.
- [S-4] KEPCO i-SMR / HIGA SBF core — F_q ≈ 2.08 / F_r ≈ 1.35 SBF peaking precedent.
- [S-5] A gadolinia/erbia burnable-absorber modeling reference (e.g. IAEA-TECDOC on Gd-bearing fuel).
  ‹from `D:\projects\literature\gadolinia burnable absorbers.pdf` — add full citation.›

**Materials & fuel-performance data**
- [M-1] IAEA-TECDOC, *Thermophysical Properties of Materials for Nuclear Engineering* (UO₂ & Zr-4
  conductivity, melting point, expansion — Tables 8.3-1, 8.3-2).
- [M-2] Halden Reactor Project fuel-behaviour data — FGR threshold, fuel-conductivity degradation.
- [M-3] Lucuta et al., UO₂ thermal-conductivity-with-burnup correlation (§8.2.1, §8.3.3).

**Regulatory**
- [T-1] Türkiye NDK, *Nuclear Power Plant Design Regulation* (under Nuclear Regulation Law No. 7381,
  2022). ‹insert exact title/date/article.›
- [I-1] IAEA SSR-2/1 (Rev. 1), *Safety of Nuclear Power Plants: Design* — Req. 24, 25, 35.
- [N-1] US NRC 10 CFR 50 Appendix A, *General Design Criteria* — GDC 11, 26, 27.

---

## Figure / table checklist (for the report assembler)

| Ref | Asset | Status |
|---|---|---|
| Table 8.2-1…8.2-5, 8.3-1, 8.3-2 | all in this draft | ✅ ready |
| Fig 8.2-3 | `cad/fa_pinmaps.png` | ✅ generated |
| Fig 8.2-4 | `cad/core_map.png` (+ `cad/guide_tube_map.png`) | ✅ generated |
| Fig 8.3-1 | `cad/end_plug_detail.png` | ✅ generated |
| Fig 8.2-5 | k_eff vs burnup depletion curve | ⏳ export PNG from notebook `aegis40_3d_core_outputs/` |
| Fig 8.2-6 | radial assembly-power map + axial profile | ⏳ export from notebook tallies |
| Fig 8.2-1 | core isometric / RPV cutaway (3D) | ⏳ Fusion/Creo render (CAD effort) |
| Fig 8.2-2 / 8.3-1 (3D) | sectioned fuel-pin render | ⏳ Fusion/Creo render |

## Notes / to-resolve
- **Gd outer-ring 24 vs 26** — reconcile `design-basis-locked.md` Table 1 with the as-run model (this
  draft uses 24).
- **§8.2.4 coolant boundary conditions** (12.8 MPa / 265 → 305 °C) are assumed pending the §8.4 T-H
  result; the §8.3 centerline calc depends on them — keep them synchronised with Adilbek's analysis.
- **Regulatory citations** for §8.2.3 compliance paragraph — insert the exact IAEA/NRC/national
  references the team standardises on (cross-reference §8.1 codes-and-standards list).
- Fuel-performance numbers in §8.3.3 are bounding hand-calculations; a FRAPCON-class confirmation
  case would strengthen the Digital Appendix if time allows.
