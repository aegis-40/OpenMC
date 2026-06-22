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
- **Zircaloy-4 cladding.** Low thermal-neutron absorption with a property database qualified to high
  burnup; all clad damage mechanisms are bounded by the moderate **42.8 GWd/MTU** discharge burnup
  (below the 62 GWd/MTU rod-average Zr-4 ceiling) and are quantified in §8.3.4. Accident heat-up
  behaviour (oxidation, ballooning, the 1204 °C peak-clad-temperature limit) underlies the §8.5
  LOCA criteria.
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
| F_q (3D total pin power) | 3.62 | **3.48** | −4% |
| F_z (core-average axial) | — | 1.03 | — |
| F_z,hot (hot-pin axial = F_q / F_ΔH) | — | 1.53 | — |

> These are thermal-margin (DNBR) inputs, not stand-alone pass/fail gates. For context, the Jang
> SBF-SMPWR design limit is F_q < 5.09 and the KEPCO i-SMR (HIGA) SBF core runs F_q ≈ 2.08 — the
> Aegis-40 rev_3 value sits well inside the SBF-SMR class. The binding thermal limit is the §8.4/§8.5
> MDNBR analysis.
>
> **On the two axial factors.** F_q = 3.48 is read **directly** from the 3D pin-power tally (it is not
> reconstructed as a product). The **core-average** axial peaking F_z = 1.03 is flat because the ±30 cm
> water reflectors give near-symmetric end-savings on the radially-averaged power shape; it is *not* the
> factor that multiplies F_ΔH. The relevant axial factor for the hot pin is F_z,hot = F_q / F_ΔH =
> 3.48 / 2.27 = **1.53**, i.e. the hot channel carries a more peaked axial shape than the core average.
> Reporting only the flat 1.03 alongside F_q = 3.48 would appear inconsistent (2.27 × 1.03 ≠ 3.48), so
> both axial factors are stated.

**Enrichment and burnable-absorber zoning — design basis, trade study, and benchmarking.**
A boron-free core must flatten power with solid zoning alone, and Aegis-40 does so through a deliberate
**division of labour between two independent tools**, each correcting a different peaking mechanism:

- **Intra-assembly enrichment grading — the pin-peak tool.** Within *every* 17×17 assembly the pins are
  graded in three concentric zones, **4.95 wt% interior / 4.70 wt% intermediate / 4.40 wt% periphery**
  (assembly average 4.69 wt%). The periphery pins border the inter-assembly water gaps — and, for edge
  assemblies, the radial water reflector — where the excess moderation drives a local thermal-flux and
  hence pin-power peak. De-enriching the outer ring relative to the interior suppresses exactly that
  peak. This *inner-hot / outer-cool* grading is standard LWR assembly practice and is used in the
  NuScale reference design (radial enrichment zoning within the assembly, FSAR Tier 2 §4.3). It is
  applied identically to all 21 assemblies so that no assembly carries an unflattened corner pin.
- **Radial Gd zoning across assemblies — the core-radial tool.** The assembly-to-assembly tilt (centre
  hotter than edge — the Bessel-like radial shape) is flattened by zoning the **burnable absorber, not
  the enrichment**: 48 Gd rods in the centre assembly, 40 in the inner ring, 24 in the outer ring
  (core-average 32; Table 8.2-4). Because the per-ring weights are normalised to a fixed core-average
  Gd loading, this depresses central power **without relocating fissile mass and without changing BOC
  reactivity** — it substitutes for the soluble-boron radial trim a borated core would use. The combined
  effect (Table 8.2-5) is the 24% reduction in assembly radial peaking and 18% in F_ΔH at constant k_BOL.

**Why not "out-in" enrichment loading?** The standard large-PWR/NuScale radial-flattening technique is
*out-in* loading — higher-enrichment assemblies on the periphery. We evaluated it directly, in two
controlled full-core variants, against the locked rev_3 scheme (identical OpenMC statistics):

**Table 8.2-6 — Enrichment-zoning trade study (full-core OpenMC, 180/50/20 000)**

| Quantity | rev_3 (adopted) | rev_4 (out-in) | rev_5 (out-in + intra-FA) |
|---|---|---|---|
| Radial enrichment scheme | intra-FA grade only (4.95/4.70/4.40); assemblies uniform across core | inter-assembly out-in (4.13/4.54/4.83); each FA single-enrichment | out-in ring base + intra-FA grade superposed |
| k_eff, BOL | 1.0264 | 1.0261 | 1.0225 |
| **F_q (3-D hot pin)** | **3.48** | 3.61 | 3.54 |
| F_ΔH (radial) | 2.27 | 2.17 | 2.14 |
| F_radial (assembly) | 1.23 | 1.17 | 1.15 |
| Discharge burnup (GWd/MTU) | **42.8** | 41.1 | 39.3 |
| Cycle length (EFPD) | **479** | 460 | 440 |
| Control-rod worth (pcm) | **15 226** | — | 14 382 |
| Shutdown margin (%Δk/k) | **12.4** | — | 11.9 |
| Max pin enrichment (wt%) | 4.95 (0.05 margin) | 4.84 | **5.00 (no margin)** |
| Gd-157 residual at EOC | 0.1% (burnt out) | — | 36% (unburnt) |

The out-in variants do flatten the **assembly-average** map (F_radial 1.23 → 1.15–1.17), but they
**regress the metric that actually governs thermal margin — the 3-D hot-pin F_q** — and they cost cycle
length and burnup:

- *rev_4* makes each assembly a single enrichment to realise the out-in tilt, which discards the
  intra-assembly pin grading; the local periphery pin-peak returns and F_q rises 3.48 → 3.61.
- *rev_5* keeps both (out-in base + intra-FA grade) and achieves the flattest assembly map, but F_q is
  still worse than rev_3 (3.54 > 3.48), discharge burnup falls to 39.3 GWd/MTU, the peak pin is pinned at
  exactly the 5.0 wt% LEU ceiling (zero licensing margin), and **36% of the Gd-157 is left unburnt at
  EOC** — reactivity locked up that never contributed to cycle length.

Two physics reasons explain why out-in helps NuScale but not Aegis-40:

1. **No soluble boron.** NuScale pairs out-in loading with chemical shim (equilibrium cycle ≈ 1235 ppm
   boron) that carries the bulk reactivity swing and provides fine radial trim, so its enrichment tilt
   only has to do gentle shaping. With no boron, our enrichment tilt must do the whole job and overshoots.
2. **A small, water-reflected core leaks.** Out-in pushes fissile mass toward the periphery. Behind a
   large core's steel/heavy reflector this is nearly free; in our 21-assembly core behind only a 20 cm
   water reflector (vacuum outer boundary) the periphery is neutronically leaky, so relocating fissile
   outward bleeds neutrons — directly the ~20–40 EFPD of lost cycle above.

The adopted division of labour — **Gd zoning for the core-radial shape, intra-assembly enrichment
grading for the pin peak** — therefore wins on every binding metric (F_q, discharge burnup, cycle length,
shutdown margin, and enrichment margin) and is retained as the locked rev_3 design.

**Re-confirmation with a steel reflector and targeted burnable-absorber placement (rev_7, 2026-06-20).**
A natural objection is that the out-in / assembly-uniform variants failed only because of Aegis-40's leaky
20 cm *water* reflector (reason 2 above), and that the reference designs' *steel* reflector plus optimised
Gd-rod placement would rescue them. We tested exactly that. A fourth full-core variant combined
assembly-uniform ring enrichment (centre 3.6 / inner 4.4 / outer 4.95 wt%, FA-average 4.68, as in
SMART/PRATIC), a 5 cm SS-304 radial reflector, and burnable-absorber rods placed *directly on the local
hot pins* — flanking the guide-tube water holes and the assembly edges (the placement strategy of SMART,
ATOM and PRATIC). The per-pin peaking did not improve; it regressed:

**Table 8.2-6a — Assembly-uniform enrichment with steel reflector + targeted Gd (per-pin reconstruction)**

| Quantity | rev_6 (intra-FA grade, water reflector) | uniform + steel, Gd mid-radius | uniform + steel, Gd on hot pins |
|---|---|---|---|
| **F_ΔH (per-pin)** | **1.85** | 1.94 | 2.05 |
| F_radial (assembly) | 1.23 | 1.45 | 1.48 |
| k_eff, BOL (ARO) | 1.026 | — | 1.064 |
| Hot-pin location | reflector-facing assembly edge | outer assembly edge | interior guide-tube neighbours |

The hot pin merely *relocated* — from the reflector-facing edge to the interior guide-tube neighbours as
the Gd was moved outward — because 32 discrete Gd rods cannot simultaneously de-peak all 24 guide-tube
water holes *and* the assembly periphery, whereas continuous per-pin enrichment grading sets every pin's
local power at once. The conclusion is robust to the reflector material and to burnable-absorber placement:
for a compact, soluble-boron-free 21-assembly core with 24 guide tubes per assembly, intra-assembly
enrichment grading is the *necessary* pin-peak tool, and assembly-uniform enrichment cannot meet the
per-pin F_ΔH limit regardless of how the Gd is arranged. This is the third independent confirmation
(after rev_4 out-in and rev_5 combined) that the locked design's enrichment strategy is the correct one.

**Benchmarking against reference iPWR/SMR cores.** Table 8.2-7 places the Aegis-40 design point against
two well-documented integral-PWR SMRs: NuScale (US, borated iPWR; FSAR Tier 2 §4.3) and RITM-200
(Russia, marine/land iPWR).

**Table 8.2-7 — Neutronic benchmarking against reference iPWR SMRs**

| Parameter | Aegis-40 (rev_3) | NuScale (FSAR) | RITM-200 |
|---|---|---|---|
| Thermal / electric power | 125 MWth / 40 MWe | 160 MWth / 50 MWe (per module) | 175 MWth / 55 MWe |
| Reactivity control | **boron-free** (Gd + Er + rods) | soluble boron + rods + Gd | soluble boron + rods |
| Max enrichment | 4.95 wt% (LEU) | < 4.95 wt% (LEU) | ~14–20 wt% (HALEU) |
| Burnable absorber | Gd₂O₃ (≤ 48/FA, zoned) + Er₂O₃ | Gd₂O₃ (≤ 32/FA) | structural / Gd |
| Refuelling interval | ~16 mo (479 EFPD), 4-batch | ~24 mo (12 GWd/MTU cycle) | up to ~6 yr |
| Discharge burnup | 42.8 GWd/MTU | ~30 GWd/MTU (class) | long-life HALEU |
| MTC (HFP) | −35.9 pcm/K (−19.9 pcm/°F) | 0 to −32.5 pcm/°F (design) | < 0 |
| Doppler coefficient | −1.84 pcm/K (−1.0 pcm/°F) | −1.63 to −2.07 pcm/°F | < 0 |
| Control-rod worth | 15 226 pcm | 14 414 → 15 553 pcm (BOC→EOC) | — |
| F_q / F_ΔH | 3.48 / 2.27 | 1.86 / 1.39 | — |

The comparison supports three defensible claims for the FER:

- **The coefficients and rod worth are in-family with a licensed iPWR.** The Aegis-40 MTC (−19.9 pcm/°F)
  sits inside NuScale's design band (0 to −32.5 pcm/°F); the total control-rod worth (15 226 pcm) sits
  between NuScale's BOC and EOC values (14 414–15 553 pcm); the Doppler coefficient is solidly negative,
  somewhat smaller in magnitude than NuScale's, consistent with the higher fuel enrichment (relatively
  less U-238 resonance absorber). The burnable-absorber strategy — integral gadolinia at a comparable
  per-assembly count — is the same.
- **Higher peaking is the expected, bounded cost of being boron-free.** Aegis-40's F_q (3.48) exceeds
  NuScale's (1.86) because soluble boron is the single most effective power-flattening tool and we have
  removed it by design. The value remains well within the SBF-SMR class (Jang SBF-SMPWR limit F_q < 5.09)
  and the binding check is the §8.4/§8.5 MDNBR analysis at our low core power density (~24 MW/tHM), not a
  borrowed peaking number.
- **LEU + high burnup is a deliberate non-proliferation / fuel-supply choice.** Where RITM-200 buys
  multi-year refuelling intervals with 14–20 wt% HALEU, Aegis-40 stays inside the < 5 wt% commercial LEU
  envelope (standard fabrication and supply, lower proliferation attractiveness) and still reaches
  42.8 GWd/MTU discharge — far above the boron-free peer CAREM-25 (~24 GWd/MTU).

‹INSERT FIGURE 8.2-5 — Cycle reactivity (k_eff and excess reactivity vs burnup, BOC → EOC) from the
full-core depletion run (cad/keff_vs_burnup.png). The three regimes described below are visible:
BOL ≈ 1.025, Gd-burnout dip ≈ 0.977 near 9 GWd/tHM, hump ≈ 1.046 near 20 GWd/tHM, and decline to
k_EOC ≈ 0.876 at the 42.8 GWd/tHM (479 EFPD) discharge.›

‹INSERT FIGURE 8.2-6 — BOC power distribution (cad/power_distribution_boc.png): radial pin-power map
(F_ΔH = 2.27, F_q = 3.48), per-assembly power map (F_radial = 1.23), and the core-average axial
profile (F_z = 1.03, flattened by the Gd cutback and the ±30 cm water reflectors).›

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

**Scope: first core through equilibrium cycle.** The depletion presented above is the **first
(all-fresh) core**, run from BOC to its 42.8 GWd/MTU / 479 EFPD end-of-cycle. The reactor reaches
its operating equilibrium through the **four-batch reload** (§8.2.2): at equilibrium the core holds
a mix of fresh, once-, twice- and thrice-burned assemblies, so the equilibrium cycle is **less
reactive at BOC and shorter** than the all-fresh first cycle, while the **per-batch discharge burnup
converges on the 42.8 GWd/MTU** design value. The first-core results therefore **bound** the
equilibrium cycle on the safety-relevant metrics — first-core BOC excess reactivity (hence required
hold-down and rod/SDM duty, Table 8.2-3) is the maximum the control system must cover, and the
first-core peaking (Table 8.2-5) is representative because the zoning is identical each reload. A
full equilibrium-core depletion (explicit fresh + burned shuffle) is identified as the next
depletion step for the final FER; it is expected to confirm the bounding argument and slightly
relax the BOC hold-down requirement.

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

**Code verification and statistical convergence.** All neutronic results above are produced with
**OpenMC** (continuous-energy Monte Carlo, ENDF/B-VIII.0) in full-core eigenvalue mode, with
depletion through the OpenMC depletion solver and the `chain_endfb80_pwr` chain. Following the
verification practice of comparable SMR neutronics studies (e.g. the SMART (U/Th)O₂ assessment of
Akbari-Jeyhouni et al. 2018, which benchmarks its MCNP model against the SMART SSAR before using it),
the Aegis-40 transport/depletion path is judged against **published, citable** validation of the same
code rather than re-derived (Table 8.2-8); the full evidence package is the Digital-Appendix V&V plan
(`docs/competition/digital-appendix-vv-plan.md`). The k_eff values quoted (BOL = 1.0264, k_EOC ≈ 0.876)
carry a production-statistics 1-σ at the few-×10 pcm level (Table 8.2-6 settings, 20 000 neutrons/batch).

**Table 8.2-8 — Neutronics verification & benchmarking (OpenMC)**

| Capability | Citable benchmark / reference | Agreement | Status |
|---|---|---|---|
| Transport / k_eff method | Romano & Forget, *Ann. Nucl. Energy* 51 (2013) 274 (OpenMC code paper); ICSBEP handbook (OECD-NEA) | published; OpenMC tracks ICSBEP suite | Cite |
| Reactor-physics lattice/core | C5G7 (OECD-NEA); BEAVRS full-core PWR (MIT-CRPG) | published | Cite (our core deck = sample input) |
| Depletion / actinide & FP isotopics | OpenMC vs Serpent on BEAVRS 2.4 % pincell — Romano et al., *Ann. Nucl. Energy* 152 (2021) 107989 | **k_eff < 20 pcm; actinides < 1 %; FPs < 1 %** to 50 MWd/kg | Cite + confirmatory run |
| Statistical repeatability | re-run with independent RNG seeds | k_eff per step within combined Monte-Carlo σ | Run |

**Depleted-fuel inventory (BOC → EOC).** Table 8.2-9 gives the major-actinide inventory at beginning
of cycle (fresh UO₂ loading) and at the 42.8 GWd/MTU discharge — the quantitative basis for the
fuel-utilisation (§8.11) and non-proliferation (§8.7 / 3S assessment) claims. BOC values are the fresh
loading (core-average ≈ 4.7 wt% over ~5.28 tHM; ⚠CONFIRM exact step-0 mass against the depletion
`--step 0` extraction); EOC values are the exact whole-core OpenMC depletion result
(`docs/competition/waste/discharge_inventory.csv`).

**Table 8.2-9 — Whole-core actinide inventory, BOC → EOC (42.8 GWd/MTU discharge)**

| Nuclide | BOC mass (kg) | EOC mass (kg) | Note |
|---|---:|---:|---|
| U-234 | ~0.4 (trace) | 1.18 | enrichment-tail + Pu-238 α-decay chain |
| U-235 | **248** | **54.9** | 193 kg fissile consumed |
| U-236 | 0 | 33.2 | U-235 (n,γ) capture product |
| U-238 | ~5 030 | 4 892 | fertile; ~140 kg → Pu / fission |
| Np-237 | 0 | 3.34 | minor actinide build-up |
| Pu-238 | 0 | 1.51 | high-burnup; raises decay heat / SF-n (self-protection) |
| Pu-239 | 0 | 28.94 | bred fissile |
| Pu-240 | 0 | 13.62 | drives reactor-grade vector (24.6 wt% of Pu) |
| Pu-241 | 0 | 7.70 | fissile |
| Pu-242 | 0 | 3.57 | — |
| Am-241 | 0 | 0.37 | grows in storage from Pu-241 β-decay |
| Am-243 | 0 | 0.71 | — |
| Cm-244 | 0 | 0.27 | dominates the spent-fuel neutron field |
| **Total Pu** | **0** | **55.3** | reactor-grade (66.2 % fissile) — see §8.7 / 3S |
| **Fissile (U-235+Pu-239+Pu-241)** | **248** | **91.6** | net fissile drawdown over the cycle |

The inventory tells the design story in one table: **193 kg of U-235 is burned** while **55 kg of
plutonium is bred** (net fissile falls 248 → 92 kg), and the high discharge burnup degrades the bred
plutonium to a **reactor-grade, self-protecting** vector (Pu-240 = 24.6 wt%, Pu-238 and Cm-244 raising
the decay-heat and neutron background) — the quantitative root of both the §8.11 waste-intensity result
and the §8.7 non-proliferation assessment.

### 8.2.4 Steady-State Thermal-Hydraulic Analysis (inputs & interface to §8.4)

> **Owner interface:** the full steady-state T-H solution (the spatial coolant/clad temperature
> distributions and the natural-circulation loop pressure balance) is produced under §8.4/§8.5.
> This subsection records the core-side modelling assumptions and summarises the resulting thermal
> margins, so the neutronic, fuel-performance and T-H analyses stay consistent.

**Modelling assumptions (steady state).** The core is evaluated at full power (125 MWth, the BOC
power shape of Table 8.2-5), single-phase pressurised water at ≈ 12.8 MPa cooled by **natural
circulation** (no reactor coolant pumps). The primary boundary conditions, fixed by the §8.4 loop
analysis, are core inlet 258 °C, core outlet 308 °C (ΔT 50 K), core-average 283 °C, and primary
flow ≈ 483 kg/s; hot-channel departure-from-nucleate-boiling is evaluated with the W-3 CHF
correlation (Tong) applied to the Table 8.2-5 peaking factors.

**Results.** The low core specific power (~24 MW/tHM) and moderate peaking give large margin on
every steady-state thermal limit (full distributions and the loop pressure balance in §8.4):

**Table 8.2-10 — Core steady-state thermal-hydraulic summary (from §8.4)**

| Quantity | Result | Limit | Margin |
|---|---|---|---|
| Primary T (in / out / avg) | 258 / 308 / 283 °C | — | single-phase |
| Hot-leg subcooling | 21.7 °C | > 0 | no bulk boiling |
| MDNBR (hot pin, W-3) | 1.466 | ≥ 1.3 | +12.8 % |
| Peak clad temperature (steady) | 391 °C | < 1200 °C | +809 °C |
| Peak fuel centerline (BOL) | ≈ 1 750 °C (§8.3) | < melt (~2840 °C) | ≈ 1 090 °C |
| Primary driving head / flow | 2.62 kPa / ≈ 483 kg/s | self-sustaining | stable upflow |

The natural-circulation loop self-regulates (ṁ ∝ P^1/3, §8.4.2.3) with all-positive upflow and no
recirculation, confirming the cooling system extracts the full 125 MWth from the core with margin.

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

### 8.3.6 Reactor-Vessel and Radiation-Shielding Materials

Outside the active core, the structural and shielding material set is selected for pressure-boundary
integrity, fast-neutron-fluence tolerance, and combined neutron/gamma attenuation. The radial stack
and its materials are the basis of the OpenMC coupled neutron–photon shielding model (rev7;
digital appendix), which sizes the biological shield to the **< 10 µSv/h** total-dose design target
behind the last layer (ALARA basis; Bagheri & Khalafi 2023; Oğul et al. 2026) and feeds the §8.8
radiation-protection zoning and the §8.10 reactor-building footprint.

The shield is deliberately **lead-free**. Lead is excluded for toxicity and decommissioning-waste
burden; tungsten is excluded as uneconomic for a stationary wall. The bulk gamma + neutron shield is
therefore **magnetite (heavy) concrete** — inexpensive, lead-free, and carrying bound water that also
moderates fast neutrons — preceded by a **borated-polyethylene** layer that captures thermalised
neutrons with low secondary-gamma yield. This keeps the published multilayer architecture
(steel + water inner → neutron-capture + high-density outer) while replacing its lead/tungsten outer
high-Z with heavy concrete.

**Table 8.3-3 — Reactor-vessel and shielding materials (radial stack, core outward)**

| Region | Material | Nominal composition (wt%) | Density (g/cm³) | Radial thickness (cm) | Function |
|---|---|---|---|---|---|
| Core barrel | Stainless steel 304 | Fe 68.5, Cr 19.0, Ni 9.5, Mn 2.0, Si 1.0 | 8.00 | 5 | Core support; first gamma/fast-neutron attenuation |
| Downcomer | Light water (H₂O) | H₂O | 0.72 (hot) | 13 | Coolant return; fast-neutron moderation, RPV fluence reduction |
| Reactor pressure vessel | SA-508 Gr.3 low-alloy steel | Fe 96.85, Mn 1.40, Ni 0.75, Mo 0.50, Si 0.25, C 0.22, Cr 0.03 | 7.90 | 18 | Pressure boundary; principal gamma shield; fast-fluence-limited (60-yr ≤ ~1×10¹⁹ n/cm², E > 1 MeV) |
| Reactor cavity | Air | N 75.5, O 23.2, Ar 1.3 | 0.0012 | 15 | Inspection/insulation gap; ISI access |
| Thermal shield | Stainless steel 304 | Fe 68.5, Cr 19.0, Ni 9.5, Mn 2.0, Si 1.0 | 8.00 | 5 | Gamma heating interception; protects the bio-shield concrete |
| Neutron-capture layer | Borated polyethylene (5 wt% B) | C 81.4, H 13.6, B 5.0 | 0.95 | 10 | Thermal-neutron capture (¹⁰B) with low secondary gamma |
| Biological shield | Magnetite (heavy) concrete | Fe 58.1, O 31.0, Ca 6.3, Si 2.2, Mg 0.9, Ti 0.7, Al 0.4, H 0.4 | 3.90 | 120 | **Bulk lead-free gamma + neutron shield**; bound water moderates fast neutrons |
| Outer finish | Ordinary (Portland) concrete | O 49.8, Si 31.6, Ca 8.3, Al 4.6, Fe 1.2, K 1.9, Na 1.7, H 0.6 | 2.30 | 10 | Structural finish; dose-acceptance surface (controlled-area boundary) |

**Behaviour under irradiation.** The SA-508 RPV is the fluence-limited component: the downcomer water
plus barrel hold the 60-yr fast fluence (E > 1 MeV) at the vessel inner wall below the
~1×10¹⁹ n/cm² embrittlement screening level (confirmed by the §8.3 fast-flux tally and cross-checked
against the OpenMC eigenvalue model). Steel internals (barrel, thermal shield) are austenitic 304 for
corrosion compatibility and dimensional stability. Borated polyethylene is non-structural and sits in
the cool cavity region (no thermal/irradiation-creep duty). Concrete shields are kept below their
~90 °C aggregate-dehydration limit by the air gap and thermal shield. Property/attenuation data to
cite: ANSI/ANS-6.4 (concrete shielding), ASTM A508/A240 (steels), ICRP-116 (flux-to-dose);
composition basis for the heavy/ordinary concretes is the PNNL compendium (McConn et al.).

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
| Table 8.2-1…8.2-9, 8.3-1, 8.3-2, 8.3-3 | all in this draft | ✅ ready |
| Fig 8.2-3 | `cad/fa_pinmaps.png` | ✅ generated |
| Fig 8.2-4 | `cad/core_map.png` (+ `cad/guide_tube_map.png`) | ✅ generated |
| Fig 8.3-1 | `cad/end_plug_detail.png` | ✅ generated |
| Fig 8.2-5 | k_eff vs burnup depletion curve | ✅ cad/keff_vs_burnup.png (full burnup, embedded) |
| Fig 8.2-6 | radial assembly-power map + axial profile | ✅ cad/power_distribution_boc.png (embedded) |
| Fig 8.2-1 | core isometric / RPV cutaway (3D) | ⏳ Fusion/Creo render (CAD effort) |
| Fig 8.2-2 / 8.3-1 (3D) | sectioned fuel-pin render | ⏳ Fusion/Creo render |

## Notes / to-resolve
- **Gd outer-ring 24 vs 26** — reconcile `design-basis-locked.md` Table 1 with the as-run model (this
  draft uses 24).
- **§8.2.4 coolant boundary conditions** (12.8 MPa / 258 → 308 °C) are now fixed by the §8.4 T-H
  result; the §8.3 centerline calc depends on them — keep them synchronised with Adilbek's analysis.
- **Regulatory citations** for §8.2.3 compliance paragraph — insert the exact IAEA/NRC/national
  references the team standardises on (cross-reference §8.1 codes-and-standards list).
- Fuel-performance numbers in §8.3.3 are bounding hand-calculations; a FRAPCON-class confirmation
  case would strengthen the Digital Appendix if time allows.
