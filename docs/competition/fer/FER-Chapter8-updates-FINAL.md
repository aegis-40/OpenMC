# Aegis-40 FER — Chapter 8 updated sections (paste-ready)

*Updated sections only (8.1, 8.2, 8.3, 8.4, 8.9, 8.11) at the frozen STAT_FINAL record basis, plus
the References list. Sections 8.5, 8.6, 8.7, 8.8, 8.10 and 8.12 are unchanged and are not reproduced
here.*

---

# 8.1 Design Preparation Phase and General Description of the Plant

## 8.1.1 Plant and power

Aegis-40 is a 125 MWth / 40 MWe net integral pressurized-water small modular reactor with a
soluble-boron-free (SBF) core cooled by natural circulation. The net thermal efficiency is 32.0 %.
The reactor building houses an integral reactor pressure vessel containing the core, a helical
once-through steam generator (OTSG) and a self-pressurizer; there are no large primary penetrations
below the top of the active core.

## 8.1.2 Fuel and core (general parameters)

| Parameter | Value |
|---|---|
| Thermal / electric power | 125 MWth / 40 MWe (32.0 %) |
| Core | 37 fuel assemblies, 17×17 lattice, 2.0 m active height |
| Fresh heavy-metal loading | 9.39 tHM |
| Core specific power | 125 / 9.39 = 13.31 MW/tHM |
| Enrichment (ring-zoned, centre→periphery) | 4.95 / 4.70 / 4.40 / 4.00 wt% ²³⁵U (core-average ~4.43 wt%) |
| Burnable absorber | integral Gd₂O₃ 6 wt% (20 rods/FA, ring-graded) + Er₂O₃ 0.75 wt% (16 rods/FA) |
| Control | 16 control-rod assemblies, 90 %-enriched B-10 B₄C |
| Primary conditions | 12.8 MPa, T_avg 283 °C (308 / 258 °C) |
| Main steam | 4.5 MPa, 296 °C, 57.8 kg/s |
| Fuel cycle | once-through (no refuelling), 2224 EFPD ≈ 6.09 FPY |
| Discharge burnup (core-average) | 29.6 GWd/tHM |

## 8.1.5 Operating cycle and derived relations

The core is loaded once and runs a single once-through cycle of approximately 2224 EFPD (≈ 6.09
full-power years); there is no batch refuelling during the cycle. Planned unavailability is set by
maintenance and in-service-inspection outages, sized for a planned availability of ~95 %. At end of
cycle the whole core is discharged. Derived values: net efficiency = 40 / 125 = 32.0 %; specific
power = 125 / 9.39 = 13.31 MW/tHM; primary flow from Q = ṁ·c_p·ΔT (c_p ≈ 5.35 kJ/kg·K at 283 °C /
12.8 MPa) → ṁ ≈ 467 kg/s (core mass flux G ≈ 543 kg/m²·s).

---

# 8.2 Core Design

## 8.2.1 Material selection

The fuel is UO₂ (pellet density 10.40 g/cm³) at a peak enrichment of 4.95 wt% ²³⁵U, clad in
Zircaloy-4. Reactivity hold-down is provided entirely by integral burnable absorbers — gadolinia
(Gd₂O₃ 6 wt%) for the fast early-cycle hold-down and a light erbia loading (Er₂O₃ 0.75 wt%) for
mid/late-cycle flattening and cold-shutdown margin — with no soluble boron in normal operation. The
control-rod absorber is B₄C enriched to 90 % ¹⁰B in solid rods, which provides the shutdown
reactivity without adding any soluble boron to the coolant, preserving the SBF claim. Materials are
selected for neutronic suitability in a high-burnup SBF core, demonstrated in-pile performance, and
compliance with the safety criteria of Section 8.5.

## 8.2.2 Geometry and layout

The 37 assemblies are arranged in a 7-wide octagonal core (rows 3-5-7-7-7-5-3). Radial enrichment
zoning across four assembly rings (4.95 / 4.70 / 4.40 / 4.00 wt% centre to periphery) combined with
heavier gadolinia loading in the central rings flattens the radial power without soluble-boron
shaping. Sixteen control-rod assemblies (twelve on a checkerboard plus four central-cross positions,
the NuScale-class configuration) act in the guide tubes; the central assembly carries the
instrument tube.

## 8.2.3 Neutronic analysis

All neutronic parameters were computed with OpenMC (continuous-energy Monte Carlo, ENDF/B-VIII.0) at
the STAT_FINAL record statistics (400 active-batch cycles × 50 000 neutrons, ~22–26 pcm standard
deviation on k_eff).

**Static parameters (beginning-of-life, hot full power, all rods out).**

| Parameter | Value | Limit | Status |
|---|---|---|---|
| k_eff (BOL, HFP, ARO) | 1.1503 ± 26 pcm | — | INFO |
| Moderator temperature coefficient | −26.9 pcm/K | < 0 | PASS |
| Doppler (fuel temperature) coefficient | −1.91 pcm/K | < 0 | PASS |
| Void coefficient | −173 pcm/%void | < 0 | PASS |
| Control-rod bank worth (16 CRA, ARO→ARI) | 21 479 pcm | ≥ 5 000 | PASS |
| Shutdown margin (most-reactive rod stuck out, hot) | +7.68 % Δk/k | ≥ 1 % | PASS |
| Maximum reactivity insertion rate | 1.5×10⁻⁵ Δk/k/s | ≤ 7.5×10⁻⁴ | PASS |
| Peak enrichment | 4.95 wt% | ≤ 5.0 | PASS |

All reactivity coefficients are negative across the operating range, and the shutdown margin with
the most-reactive rod stuck out satisfies the ≥ 1 % Δk/k requirement with substantial margin.

**Fuel-cycle behaviour.** The once-through core reaches its end-of-cycle criticality limit (k = 1)
at 2224 EFPD (≈ 6.09 FPY), corresponding to a core-average discharge burnup of 29.6 GWd/tHM. The
k-effective versus burnup curve shows the characteristic early xenon dip, a gadolinia/erbia
burnout hump (peak k = 1.135 at ≈ 13.5 GWd/tHM), and a smooth decline to k = 1. The hump peak
remains below the beginning-of-cycle value (1.150), so beginning-of-cycle is the bounding state for
the shutdown analysis (Section 8.6).

**Power distribution over the cycle.** Pin-resolved peaking factors were computed at the three
limiting cycle states by full-core criticality calculations with the exact depleted compositions of
the record depletion (the static k-effective reproduces the depletion curve within 70 pcm at each
state, verifying the method). The reference values F_ΔH ≤ 1.65 and F_q ≤ 2.32 are conservative
generic PWR screening limits, not Aegis-40 design-specific acceptance limits: in licensing practice
these are unit- and cycle-specific Core Operating Limits Report (COLR) parameters, and published
small-modular-reactor cores accept higher total peaking at low linear heat rate (for example, the
CAREM-25 equilibrium core reports a peaking factor of 2.56 with a minimum DNBR of 1.90, and SMART
reports a three-dimensional peaking factor of 2.48 at a low core-average linear power density).

Table 8.2-4. Cycle peaking factors (×1.03 engineering allowance applied).

| State | Burnup (GWd/tHM) | F_ΔH | F_z | F_q | Interpretation |
|---|---|---|---|---|---|
| BOC | 0.0 | 1.513 | 1.280 | 1.937 | passes generic screening |
| MOC (Gd-burnout hump) | 13.5 | 1.729 | 1.408 | 2.435 | exceeds generic screening — closed by design-specific basis |
| EOC | 30.8 | 1.497 | 1.417 | 2.121 | passes generic screening |

At the gadolinia-burnout hump the pin peaking exceeds the generic screening values by about 5 %.
Because Aegis-40 operates at a very low average linear heat rate (6.4 kW/m core-average, 12.8 kW/m
peak), acceptability is determined by the design-specific thermal limits. A dedicated hot-channel
thermal-hydraulic analysis at the bounding mid-cycle envelope (F_ΔH = 1.75, F_q = 2.47, mid-cycle
axial shape) confirms a minimum DNBR of 1.37 with the conservative W-3 correlation and 2.20 with the
Bowring correlation (within its validity range), against the ≥ 1.30 acceptance criterion, with a peak
fuel temperature of 828 °C — far below limits (Section 8.4). Aegis-40 therefore adopts a
design-specific COLR peaking limit of F_ΔH ≤ 1.75 for the 37-assembly SBF core, consistent with PWR
COLR practice and small-modular-reactor precedent; the mid-cycle screening exceedance is a documented
and closed design characteristic, not a safety-limit violation. Power-dependent insertion limits and
regulating-group power-distribution control are specified as an operating requirement providing
additional margin at this state (Section 8.5).

## 8.2.5 Depleted-fuel inventory (BOC → EOC)

At the end-of-cycle discharge state (29.6 GWd/tHM) the whole-core inventory contains ≈ 76.2 kg of
plutonium with the isotopic vector Pu-238 / 239 / 240 / 241 / 242 = 2.0 / 62.8 / 21.2 / 10.1 / 3.9
wt%, which is firmly reactor-grade (Pu-239 far below the 93 % weapons-grade threshold), with a
residual ²³⁵U content of ~1.8 wt%. The per-assembly discharge burnup ranges from 21 GWd/tHM at the
periphery to 42 GWd/tHM at the centre — the peak assembly remaining well below the 62 GWd/tHM
qualified-fuel limit. This inventory is the basis for the waste and non-proliferation assessments
(Section 8.11 and Section 7).

---

# 8.3 Fuel and Material Design

## 8.3.2 Linear heat rate and power density

The deliberately low specific power (13.31 MW/tHM) gives a core-average linear heat rate of 6.4 kW/m
and a beginning-of-cycle peak of 12.8 kW/m — roughly half that of a conventional large PWR — which is
the origin of the wide thermal margins reported below.

## 8.3.3–8.3.4 Fuel-performance screening

The fuel-performance metrics were screened against the qualified-fuel envelope using established
correlations and reference in-pile data. The low peak linear heat rate and the low once-through
discharge burnup place every metric far inside its limit.

Table 8.3-3. Fuel-performance screening (steady-state, bounded by qualified-envelope correlations).

| Parameter | Aegis-40 (bounding) | Limit / criterion | Status |
|---|---|---|---|
| Peak linear heat rate | 12.8 kW/m | ≈ 59 kW/m incipient melt (DNB-limited well above) | far inside |
| Peak fuel centreline temperature | 734 °C (BOL); 828 °C at the mid-cycle peaking envelope | < 2590 °C design (2840 °C melt) | ~1 900 °C margin |
| Fission-gas release | ≤ ~2 % | design < 10 % | low (LHR ≪ 20 kW/m threshold) |
| End-of-life rod internal pressure | < 12.8 MPa system (no clad lift-off) | ≤ system pressure | no lift-off |
| Peak cladding oxide thickness | ≤ ~20 µm | ≤ 100 µm | > 80 µm margin |
| Cladding hydrogen pickup | ≤ ~150 ppm | ≤ ~600 ppm | wide |
| Pellet-clad mechanical interaction / clad strain | small (gap not fully closed) | ≤ 1 % transient strain | wide |
| Rod-average discharge burnup | 29.6 GWd/tHM | ≤ 62 GWd/tHM (qualified LEU) | far inside |

A confirmatory FRAPCON-class fuel-performance calculation for the limiting hot rod at beginning of
life, the gadolinia-burnout peak and end of cycle is recommended to convert this screening into a
licensing-grade result. Even under the bounding mid-cycle peaking envelope (F_q = 2.47) the peak
fuel centreline temperature is 828 °C — more than 1 900 °C below the UO₂ melting point — confirming
that the screening remains bounding at every point in the once-through cycle.

## 8.3.5 Front-end fuel-cycle structural materials

Cladding and structural components are Zircaloy-4 and stainless steel qualified for the moderate
discharge burnup; oxide, hydrogen pickup, creep and irradiation growth are all bounded by the low
once-through burnup.

---

# 8.4 Cooling Circuit System Design

## 8.4.6 Heat-removal capacity — cycle-state DNBR verification

The hot-channel thermal-hydraulic analysis was performed at the three limiting cycle states using the
neutronic pin peaking factors and axial shapes. The core power (125 MWth) and coolant mass flux
(G ≈ 543 kg/m²·s) are constant; only the peak linear heat rate, axial shape and enthalpy-rise factor
change with cycle state.

Table 8.4-6. Hot-channel results over the once-through cycle.

| State | F_q | MDNBR (W-3, conservative) | MDNBR (Bowring, in-range) | Peak cladding temperature | Peak fuel temperature |
|---|---|---|---|---|---|
| BOC | 1.937 | 1.60 | 2.72 | 348 °C | 722 °C |
| MOC (Gd-burnout hump) | 2.435 | 1.38 | 2.23 | 352 °C | 822 °C |
| EOC | 2.121 | 1.51 | 2.56 | 350 °C | 759 °C |
| MOC COLR envelope (F_ΔH 1.75) | 2.468 | 1.37 | 2.20 | 353 °C | 828 °C |

The minimum DNBR remains at or above 1.30 at every cycle state, including the bounding COLR envelope.
The W-3 correlation is reported as the conservative value (evaluated below its formal mass-flux range
by extrapolation), and the Bowring-1972 correlation, which is valid at the Aegis-40 low mass flux, is
reported alongside it; a Groeneveld-2006 critical-heat-flux look-up-table cross-check confirms the
margin. Separability of the peaking factors (F_q = F_ΔH × F_z) is satisfied by the neutronic inputs.
Under the anticipated-operational-occurrence envelope (118 % power / 80 % flow) at the mid-cycle
state the Bowring MDNBR is 1.63; the density-wave-oscillation screening ratio is comfortably above
unity with the five spacer grids credited, and the power-distribution-control requirement of
Section 8.5 provides additional margin.

---

# 8.9 Energy Conversion and Integrated Systems

## 8.9.1 Energy-conversion architecture

A single tandem-compound turbine-generator converts the 125 MWth core output to 40.0 MWe net (net
efficiency 32.0 %) through a saturated-steam Rankine cycle: the helical once-through steam generator
delivers main steam at 4.5 MPa / 296 °C / 57.8 kg/s to a high-pressure/low-pressure turbine on one
shaft, exhausting to a seawater-cooled condenser (7 kPa, 39 °C; Black Sea once-through cooling). Two
co-products are taken from the secondary side on a non-safety, balance-of-plant branch, isolated from
the nuclear island by an intermediate heat exchanger: thermochemical district heat and off-peak
hydrogen.

## 8.9.5 Thermochemical energy storage (TCES) for district heating

**Storage medium.** The reference storage medium is a zeolite-13X / water adsorption store. Zeolite-13X
is adopted because it is ammonia-free (no toxic or flammable working-fluid inventory, and hence no
ammonia hazard analysis, simplifying licensing of a nuclear-plant auxiliary), uses a benign water
working fluid, is a mature commercially deployed adsorbent, and is thermally stable over many cycles.
Heat is stored by desorbing (drying) the zeolite bed during charge and released when water vapour
re-adsorbs during discharge, liberating the adsorption enthalpy; because energy is held as a
dry-versus-hydrated material state, the store has no standby thermal loss.

**Sizing.** For the district-heat design block (25 MWth peak delivery over an 8-hour discharge, i.e.
200 MWh_th), the store contains approximately 1000 t of zeolite-13X (≈ 1538 m³ of packed bed). This
sizing was obtained from a first-principles calculation using published zeolite-13X/water adsorption
data (adsorption enthalpy ≈ 3500 kJ/kg-H₂O, working uptake ≈ 0.20 kg-H₂O/kg-zeolite, bed density
≈ 650 kg/m³ → gravimetric energy density ≈ 0.19 kWh/kg, ≈ 126 kWh/m³) and independently confirmed by
a plant-level charge/discharge energy balance, the two methods agreeing within 3 %.

Table 8.9-5. Frozen TCES district-heat store.

| Parameter | Value |
|---|---|
| Storage medium | zeolite-13X / H₂O adsorption |
| Energy density | 0.19 kWh/kg ; ≈ 126 kWh/m³ |
| Store mass / volume | ≈ 1000 t / ≈ 1538 m³ |
| Delivered block | 200 MWh_th (≈ 8 h at 25 MWth peak) |
| District-heat delivery | 25 MWth peak / 12.5 MWth seasonal-average, 90/45 °C |
| Discharge (adsorption) temperature | ≈ 130 °C |
| Charge loop | high-pressure extraction 1.0 MPa / 180 °C → intermediate heat exchanger → ≈ 168 °C bed regeneration |
| Round-trip efficiency | ≈ 0.78 |
| Standby loss | none (adsorbed state holds indefinitely) |
| Classification | non-safety balance-of-plant, intermediate-heat-exchanger isolated |

**Evaluated higher-density alternative.** A higher-density ammoniate resorption store using the
NiCl₂–SrCl₂/NH₃ pair was quantitatively evaluated against the zeolite reference with a thermodynamic
model that reproduces the published performance of Yan et al. (2020) exactly (direct-mode coefficient
of performance 0.973). At the same 200 MWh_th design point it is about twice as compact (≈ 735 t)
with a higher round-trip efficiency, but the ammonia inventory adds a hazard-analysis and licensing
burden that the compactness gain does not justify for a nuclear balance-of-plant. The ammonia-free
zeolite-13X is therefore adopted as the reference, a choice supported by a quantitative trade study
rather than an assumption.

## 8.9.7 Hydrogen co-generation (off-peak)

The hydrogen branch converts off-peak electrical output into storable hydrogen while the reactor
remains at stable thermal power. The technology is an 8 MWe solid-oxide electrolysis module in the
industrial island (specific energy 37.55 kWh/kg-H₂, versus 50 for a PEM unit), producing 213 kg/h.
The electrolyser operates only in the deepest night valley — approximately 4 hours per night, outside
the district-heat season, on roughly 140 nights per year — giving about 560 electrolysis-hours per
year (a ~6 % capacity factor) and an annual production of approximately 120 t-H₂/year. The steam
slipstream is 0.53 kg/s (0.9 % of main steam, a deaerator-level bleed). The electrolyser is
electrically coupled and non-safety classified; a trip sheds the industrial load and returns the
plant to electricity-priority operation. Capacity headroom exists to increase production if the grid
off-peak valley deepens, but the reported design and economics use 120 t/year.

## 8.9.6 Mode-exclusive dispatch and grid balance

The cogeneration extraction (high-pressure stage bleed, 1.0 MPa / 180 °C) is routed by mode — to the
thermochemical store in the district-heat season or to the electrolyser feed in the non-heating
season — and never to both simultaneously. Grid export is the full 40.0 MWe at peak, approximately
35.6 MWe while the store is charging (a ~4.9 MWe charge penalty), and approximately 27.6 MWe in the
night valley if the electrolyser is also operating.

---

# 8.11 Nuclear Waste Management

## 8.11.1 Waste-minimization by design (fuel cycle)

The once-through waste basis is 2224 EFPD (6.09 full-power years), a core-average discharge burnup of
29.6 GWd/tHM and a fresh heavy-metal loading of 9.39 tHM. The calculated waste intensity is 4.40 tHM
per TWhe (based on ≈ 2.14 TWhe lifetime electrical generation). The low-power-density long-cycle
design eliminates refuelling and supports a simple once-through baseline.

Table 8.11-1. Fuel-cycle waste comparison.

| Quantity | Aegis-40 (once-through) | CAREM-25 |
|---|---|---|
| Thermal / electric power | 125 MWth / 40 MWe | 100 MWth / 27 MWe |
| Net efficiency | 0.320 | 0.270 |
| Discharge burnup | 29.6 GWd/tHM | 24.0 GWd/tHM |
| Peak-assembly burnup | 42 GWd/tHM (≪ 62 limit) | — |
| Waste intensity | 4.40 tHM/TWhe | 6.43 tHM/TWhe |

Even at the deliberately low once-through burnup, Aegis-40 produces about 32 % less heavy metal per
unit electricity than CAREM-25, driven by the higher net efficiency. No assembly exceeds 42 GWd/tHM,
preserving a margin of more than 30 % to the 62 GWd/tHM fuel-qualification ceiling even in the hottest
position.

## 8.11.2 Back-end fuel-cycle management plan

Aegis-40 uses a once-through baseline with no reprocessing. At end of cycle the whole core is
discharged to the spent-fuel pool, cooled and shielded on site, then transferred to dry storage or a
national spent-fuel management pathway.

## 8.11.3 Spent-fuel source term and decay heat

The rigorous whole-inventory decay heat governs the immediate pool-cooling load: 7.95 MW at shutdown
(about 6.4 % of rated thermal power), falling to 48 kW at 1 year and 9 kW at 10 years. The curated
long-lived nuclide set governs the long-term planning basis.

Table 8.11-2. Long-lived source term versus cooling time (curated nuclide set).

| Cooling (yr) | Activity (Bq) | Decay heat (W) | Radiotoxicity (Sv) |
|---|---|---|---|
| 0 | 1.23×10¹⁷ | 16 550 | 2.11×10⁹ |
| 1 | 1.12×10¹⁷ | 14 230 | 1.92×10⁹ |
| 5 | 8.49×10¹⁶ | 9 519 | 1.48×10⁹ |
| 10 | 6.87×10¹⁶ | 7 497 | 1.25×10⁹ |
| 30 | 3.73×10¹⁶ | 4 643 | 8.01×10⁸ |
| 100 | 6.42×10¹⁵ | 1 272 | 2.54×10⁸ |
| 1000 | 2.76×10¹⁴ | 209 | 6.64×10⁷ |

The total whole-inventory activity at discharge is 2.76×10¹⁹ Bq, dominated by short-lived
fission/activation products that decay within the first year; the long-term source is set by Cs-137,
Sr-90 and the transuranics. The bulk specific activity and heat density exceed the heat-generating-
waste threshold, so the spent fuel is classified as high-level waste / spent nuclear fuel. The
discharge plutonium vector (76.2 kg total, Pu-239 62.8 wt%) is reactor-grade; the decay heat
(12.2 W/kg-Pu) and spontaneous-fission neutron output (3.1×10⁵ n/s/kg) act as intrinsic technical
barriers, so the once-through fuel cycle itself is the first waste-and-safeguards barrier.

## 8.11.4 Spent-fuel storage criticality

Spent-fuel storage criticality is evaluated separately from the soluble-boron-free reactor-coolant
concept. The credited storage basis uses flux-trap absorber racks, burnup credit and approximately
2000 ppm soluble boron in the spent-fuel pool as a defence-in-depth measure; this does not contradict
the SBF operating concept because soluble boron is not used for reactor-coolant reactivity control.
The acceptance criterion is k(95/95) ≤ 0.95.

Table 8.11-3. Storage-rack criticality (burnup-credited, 29.6 GWd/tHM composition).

| Configuration | k_calc ± σ | k(95/95) | Verdict |
|---|---|---|---|
| Spent fuel + Boral box | 0.83537 ± 0.00065 | 0.837 | PASS |
| Spent fuel + Metamic box | 0.84521 ± 0.00064 | 0.847 | PASS |

Both configurations sit at least 0.10 below the 0.95 limit, confirmed with two absorber materials. A
minimum-burnup loading curve administratively excludes fresh and low-burnup assemblies. The result is
consistent with, and more conservative than, the published soluble-boron-free small-PWR storage
envelope.

## 8.11.5 Secondary radioactive-waste minimization

The soluble-boron-free design eliminates the borated-water secondary-waste streams that a
boron-controlled PWR generates — spent ion-exchange resins, evaporator concentrates and tritiated
boron effluent from the chemical and volume control system — a reduce-at-source benefit not captured
in the mass-per-energy metric. Remaining operational wastes are managed by best-available-technique
segregation, volume reduction and conditioning, collected and segregated by nature for subsequent
processing. The integral-vessel layout with no large primary penetrations further limits
contaminated-component arisings.

---

# References (updated)

1. P. K. Romano, C. J. Josey, A. E. Johnson, J. Liang, "Depletion capabilities in the OpenMC Monte Carlo particle transport code," *Annals of Nuclear Energy* 152 (2021) 107989.
2. OECD/NEA, *International Handbook of Evaluated Criticality Safety Benchmark Experiments (ICSBEP)*, NEA/NSC/DOC(95)03 (LEU-COMP-THERM-008).
3. E. Fridman et al., NuScale-like SMR core benchmark model (RODARE dataset 2457; companion OpenMC deck, Zenodo 15231335).
4. J. Cabrera et al., "Criticality calculation with burnup credit of a PWR spent-fuel pool," 2023.
5. S. Kim, Y. Jung, J. Yoon, *Nuclear Engineering and Technology* 56 (2024) 3144.
6. N. E. Todreas, M. S. Kazimi, *Nuclear Systems I*, 2nd ed., CRC Press.
7. K. J. Geelhood, W. G. Luscher et al., *FRAPCON-3.5* fuel-performance code, PNNL / NUREG-CR-7022.
8. D. C. Groeneveld et al., "The 2006 CHF look-up table," *Nuclear Engineering and Design* 237 (2007) 1909–1922.
9. R. W. Bowring, *A Simple but Accurate Round Tube, Uniform Heat Flux, Dryout Correlation*, AEEW-R 789 (1972).
10. T. Yan, Z. H. Kuai, S. F. Wu, "Multi-mode solid–gas thermochemical resorption heat transformer using NiCl₂–SrCl₂/NH₃," *Applied Thermal Engineering* 167 (2020) 114800.
11. N. Yu, R. Z. Wang, L. W. Wang, "Sorption thermal storage for solar energy," *Progress in Energy and Combustion Science* 39 (2013) 489–514.
12. L. Scapino et al., "Sorption heat storage for long-term low-temperature applications: a review at material and prototype scale," *Applied Energy* 190 (2017) 920–948.
13. K. E. N'Tsoukpoe et al., "A review on long-term sorption solar energy storage," *Renewable and Sustainable Energy Reviews* 13 (2009) 2385–2396.
14. A. Hauer, "Adsorption systems for thermal energy storage — design and demonstration projects," in *Thermal Energy Storage for Sustainable Energy Consumption*, Springer.
15. J. Milewski, J. Kupecki et al., "Hydrogen production in solid oxide electrolysers," *International Journal of Hydrogen Energy* 46 (2021) 35765–35776.
16. IAPWS, *Industrial Formulation 1997 for the Thermodynamic Properties of Water and Steam (IF97)*.
17. IAEA, *Safety of Nuclear Power Plants: Design*, SSR-2/1 (Rev. 1); *Design of the Reactor Core* SSG-52; *Design of Fuel Handling and Storage Systems* SSG-63; *Storage of Spent Nuclear Fuel* SSG-15; *Criticality Safety* SSG-27.
18. U.S. NRC, *Standard Review Plan* NUREG-0800; *Standard Technical Specifications* NUREG-1431; *Control of Heavy Loads* NUREG-0612; *Single-Failure-Proof Cranes* NUREG-0554.
19. U.S. NRC, *10 CFR 50.68* (criticality accident requirements); ANSI/ANS-5.1 (decay-heat power).
20. ASME NOG-1, *Rules for Construction of Overhead and Gantry Cranes (Nuclear)*.
