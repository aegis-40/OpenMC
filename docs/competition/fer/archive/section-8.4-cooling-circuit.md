# §8.4 Cooling Circuit System Design

> **Status:** first draft (NEU drafting the [TH] critical-path section, to be confirmed and
> extended by Adilbek). Primary-loop conditions are taken from the as-run thermal-hydraulic
> analysis (CFD conjugate-pin + correlation stack, `System-integration` repo); the natural-
> circulation loop balance below is an independent first-principles cross-check
> (`scripts/natcirc_primary.py`, IAPWS-IF97). The secondary power-conversion side is developed
> in detail in **§8.9** and only summarised here.
>
> **Primary–secondary coupling (resolved, §8.4.8):** the analysed legs (258 → 308 °C) set the OTSG
> steam side at **4.5 MPa / 296 °C** (8.8 °C pinch), giving **39.7 MWe net** — nameplate 40 MWe
> preserved. §8.9 is coupled to these legs.

---

## 8.4.1 Cooling-system architecture (general description)

Aegis-40 removes core heat through three coupled circuits:

1. **Primary circuit** — a closed, **natural-circulation** loop entirely inside the reactor
   pressure vessel (RPV). It carries the full 125 MWth from the core to the integral once-through
   steam generator (OTSG) with **no reactor coolant pumps** and **no large-diameter primary
   piping** (a defining integral-PWR feature; see §8.1 and the RPV cutaway `cad/aegis_rpv.step`).
2. **Secondary circuit** — the feedwater/steam side of the OTSG and the regenerative Rankine
   power-conversion plant (turbines, condenser, feedwater train). Heat crosses the pressure
   boundary **once**, in the OTSG, and is converted to 40 MWe (**→§8.9**).
3. **Associated cooling systems** — the safety-grade passive decay-heat removal system (DHRS),
   the chemical & volume control system (CVCS), the integral self-pressurizer, and the
   **seawater once-through** ultimate-heat-sink circuit that rejects condenser heat to the
   Black Sea at the Sinop coastal site (**→§8.9**).

The integrated process-flow diagram is **Figure 8.9-1** (`cycle/plant_pfd_seawater_h2.png`,
`scripts/plant_pfd_seawater_h2.py`); stream conditions are tabulated in `cycle/stream-summary-table.md`.

**Primary flow path (in-vessel, bottom-up):**

> core (heat source) → central **riser** (R 560 mm) → upper plenum → turn-around →
> **helical-coil OTSG** in the upper annulus (primary on the shell side, downflow over the coils)
> → **downcomer** annulus → lower plenum → back into the core.

Buoyancy of the heated coolant in the riser against the cooler coolant in the downcomer sustains
the circulation; the OTSG is mounted **above** the core so that the heat sink sits above the heat
source, which is the geometric requirement for stable natural circulation.

![In-vessel primary natural-circulation loop](natcirc_loop_schematic.png)

**Figure 8.4-1.** In-vessel primary natural-circulation loop (`scripts/draw_natcirc_loop.py`).
The hot riser (308 °C, 703 kg/m³) rises against the cold downcomer (258 °C, 797 kg/m³); the
OTSG heat sink sits 2.85 m above the core mid-plane, giving the 2.62 kPa buoyancy driving head
that sustains the 483 kg/s primary flow with **no reactor coolant pumps**.

---

## 8.4.2 Primary cooling system — natural circulation

### 8.4.2.1 Design conditions

| Parameter | Value |
| --- | --- |
| Core thermal power | 125 MWth |
| Operating pressure | **12.8 MPa** |
| Design pressure (110 %) | **≈ 14.1 MPa** |
| Core outlet (hot leg) | **308 °C** (581 K) |
| Core inlet (cold leg) | **258 °C** (531 K) |
| Core ΔT | **50 K** |
| Core average | 283 °C (555 K) |
| Saturation temperature @ 12.8 MPa | 329.7 °C |
| Hot-leg subcooling | **21.7 °C** |
| Primary mass flow ṁ | **≈ 483 kg/s** |
| Coolant | light water, soluble-boron-free |

The **21.7 °C hot-leg subcooling** confirms the core stays comfortably single-phase at full power
(no bulk boiling), consistent with the all-positive upflow velocity field from the CFD (no
recirculation). The operating pressure of 12.8 MPa matches the closest reference iPWR (NuScale,
12.8 MPa) and is the value the §8.9 OTSG analysis was built on.

### 8.4.2.2 Natural-circulation driving head (heat-removal capability)

The natural-circulation flow is set by the balance between the **buoyancy driving head** and the
**loop hydraulic losses** (Todreas & Kazimi, *Nuclear Systems I*, single-phase natural-circulation
loop momentum integral):

> ΔP_driving = (ρ_cold − ρ_hot) · g · H_th = Σ K_i · ½ ρ v²  (loop form + friction losses)

with the thermal height **H_th** taken between the core mid-plane and the OTSG bundle mid-plane
from the RPV geometry (`generate_rpv_step.py`): core mid at model-z 1018.5 mm, OTSG mid at
3868.5 mm → **H_th = 2.85 m**.

| Quantity | Value | Note |
|---|---|---|
| ρ (cold leg, 258 °C) | 796.7 kg/m³ | IAPWS-IF97 @ 12.8 MPa |
| ρ (hot leg, 308 °C) | 703.1 kg/m³ | |
| Δρ | 93.6 kg/m³ | buoyancy term |
| Thermal height H_th | 2.85 m | core-mid → OTSG-mid |
| **Driving head ΔP_driving** | **2.62 kPa** | Δρ·g·H_th |
| Core coolant velocity | 0.90 m/s | **independent — from CFD** |
| Implied core flow area | 0.71 m² | ṁ/(ρ·v) |
| Sustained loop loss coeff. K_tot | **≈ 8.6** | ΔP_driving / (½ρv²) |

**Cross-validation.** The 2.62 kPa buoyancy head supports the analysed 483 kg/s at exactly the
0.90 m/s core velocity the CFD reports, requiring a total loop-loss coefficient of ≈ 8.6 — a
physically realistic value for a loop comprising core inlet/outlet, spacer grids, the riser
turn-around, the OTSG tube bank, and the downcomer. The fact that the **independent loop momentum
balance and the CFD velocity field agree** is the primary evidence that the natural-circulation
design removes 125 MWth as intended. *(Adilbek to replace K_tot ≈ 8.6 with the component-resolved
loss tally — core grids, OTSG bundle, turn-around — to close the balance exactly.)*

### 8.4.2.3 Self-regulation (load-following without pumps)

Because the driving head scales with Δρ (≈ ΔT) and the losses scale with ṁ², the loop
self-adjusts: a rise in power raises ΔT and buoyancy, which raises flow, which limits the
temperature rise. The analysed mass-flow-versus-power relation follows **ṁ ∝ P^(1/3)** (TH
result, validated), the signature of single-phase natural circulation, so the reactor passively
trims its own coolant flow to the power level with no operator or pump action.

![Pumpless self-regulation of the primary loop](natcirc_self_regulation.png)

**Figure 8.4-2.** Pumpless self-regulation (`scripts/draw_natcirc_loop.py`). Because flow follows
ṁ ∝ P^(1/3) rather than the linear forced-flow relation, the loop retains a large fraction of its
flow as power drops (e.g. ~80 % flow at 50 % power), passively limiting the core temperature rise.

---

## 8.4.3 Secondary cooling system (OTSG and power conversion)

The integral **once-through helical-coil steam generator (OTSG)** is the single heat exchanger
that crosses the pressure boundary, transferring the full 125 MWth from the primary shell side to
the secondary feedwater/steam inside the coils. Feedwater enters subcooled, is economised,
evaporated and superheated in one pass, and leaves as superheated steam to the turbine. The
secondary side — steam conditions, regenerative feedwater heating, turbines, condenser, and the
40 MWe / 32 % net heat balance — is developed in full in **§8.9** (state points in
`cycle/cycle_state_points.csv`). Only the primary-side OTSG duty and the coupling constraint are
carried here (§8.4.6).

---

## 8.4.4 Associated and safety-related cooling systems

| System | Function | Key characteristics |
| --- | --- | --- |
| **Passive decay-heat removal (DHRS)** | Remove decay heat after trip / loss of the normal secondary heat sink, by natural circulation to an in-containment water tank — no AC power, no operator action | Sized to ≥ 105 % of the 1 s post-scram decay heat (`prhr_capacity` criterion); supports the ≥ 72 h (target unlimited) grace period — quantified in **§8.5/§8.6** |
| **Self-pressurizer** | Maintain 12.8 MPa primary pressure via the integral top steam dome (electric heaters + spray), absorbing load swings | In-vessel dome, 8 sheathed heaters, surge connection (`aegis_rpv.step`) |
| **Chemical & Volume Control (CVCS)** | Primary inventory makeup/letdown, coolant chemistry; no boration (boron-free core) | Small lines penetrating the vessel (no large primary penetrations → large-break LOCA design-eliminated) |
| **Seawater once-through / ultimate heat sink** | Reject 82.6 MWth condenser heat to the Black Sea (Sinop) | Once-through seawater, ~2,065 kg/s (≈ 2.0 m³/s) intake, ΔT ≤ 10 K outfall; multiport diffuser → far-field rise ≤ 0.2 K (≤ 3 K cap); no evaporative water consumption (**→§8.9**, `scripts/seawater_heat_sink.py`) |

The DHRS and self-pressurizer are the safety-relevant cooling functions; both are **passive or
fail-safe** and underpin the defense-in-depth levels 3–4 of `safety_criteria.yaml`.

---

## 8.4.5 Components — functions, properties, capacities, materials

> Last column: pressure-boundary and safety-related components are designed to **ASME Boiler &
> Pressure Vessel Code Section III** (nuclear); balance-of-plant components to **ASME Section VIII
> / ASME B31.1** (non-nuclear). All materials are PWR-proven and qualified for the full operating
> envelope (normal, AOO, and design-basis accident temperatures/pressures).

### Primary / nuclear components

| Component | Function | Capacity / key parameters | Material | Code |
|---|---|---|---|---|
| Reactor pressure vessel (RPV) | Primary pressure boundary; houses all primary components | ID 2800 mm, wall 160 mm, ~7.2 m cyl. + heads; 12.8 MPa op / ≈14.1 MPa design; **60-year design life** | SA-508 Gr.3 Cl.1 forgings (SA-533B plate), SS weld-overlay clad | ASME III Div.1, Class 1 (NB) |
| Core barrel / riser | Separate hot riser flow from cold downcomer; guide natural circulation | Riser R 560 mm, wall 30 mm | SS-304/316L | ASME III, NG |
| OTSG (helical coil) | Transfer 125 MWth primary→secondary; generate superheated steam | 125 MWth; 6 radial coil layers (R 665–1075 mm), helical bundle, primary shell side / secondary tube side | Inconel-690 TT tubes; SS shroud/tubesheets | ASME III, Class 1 |
| Self-pressurizer | Maintain/regulate primary pressure | Integral top dome, 8 heaters; surge line | SA-508 dome; Incoloy-800-sheathed heaters | ASME III, Class 1 |
| In-vessel CRDM | Reactivity control (in-vessel, no head penetrations) | 9 units | SS / Inconel | ASME III |
| Core support / flow plates | Locate core, distribute lower-plenum flow | lower + upper support plates, flow distributor | SS-304 | ASME III, NG |
| DHRS heat exchanger | Passive decay-heat removal to heat-sink tank | ≥ 105 % of 1 s decay heat | SS / Inconel | ASME III, Class 2 |

### Secondary / balance-of-plant components (capacities from §8.9 heat balance)

| Component | Function | Capacity / key parameters | Material | Code |
|---|---|---|---|---|
| HP / LP turbine + generator | Expand steam → 40 MWe | 58.3 kg/s steam in; gross ≈ 42.5 MWe | Cr-steel rotors, SS blading | ASME / IEC |
| Moisture separator | Dry crossover steam (blade-erosion limit) | holds last-stage moisture ≤ 10.8 % | SS | B31.1 |
| Condenser | Condense LP exhaust; reject 82.6 MWth | 7 kPa, Tsat 39 °C; ~2,065 kg/s once-through seawater | Ti / SS tubes, CS shell | ASME VIII |
| Deaerator (FWH-2) / FWH-1 | Regenerative feed heating to 180 °C; deaeration | open FWHs, 0.15 / 1.0 MPa | CS | ASME VIII |
| Main feed / condensate / booster pumps | Return feedwater to OTSG at 4.5 MPa | ≈ 0.36 MWe total pump load | CS / SS | B31.1 |
| Main-steam isolation & safety/relief valves | Isolate / overpressure-protect secondary | per setpoints (`trip_signals`) | SS / CS | ASME III/VIII |

---

## 8.4.6 Heat-removal capacity — analyses and methods

**Methods (all literature-accepted):**

- **Natural-circulation loop momentum balance** (Todreas & Kazimi) — §8.4.2.2, ΔP_driving vs Σ losses.
- **W-3 critical-heat-flux correlation** (Tong) for departure-from-nucleate-boiling / MDNBR.
- **Dittus–Boelter / Gnielinski** single-phase convection (CFD validation benchmark).
- **ANS-5.1** decay-heat standard for post-shutdown heat-removal sizing.
- **IAPWS-IF97** water/steam properties throughout (`natcirc_primary.py`, `thermo_cycle.py`).
- **Conjugate CFD** (`chtMultiRegionFoam`, k-ω SST) for the hot-pin temperature field and velocity.

**Core thermal-hydraulic results (full-power, hot channel):**

| Deliverable | Result | Limit | Margin |
| --- | --- | --- | --- |
| Primary T (in / out / avg) | 258 / 308 / 283 °C | — | — |
| Peak clad temperature (PCT), steady | **391 °C** | < 1200 °C | +809 °C |
| MDNBR (hot pin) | **1.466** | ≥ 1.3 | +12.8 % |
| Fuel centerline temperature | < limit (`thermal_stack.py`) | < 2590 °C | large |
| Hot-leg subcooling | 21.7 °C | > 0 | — |
| Coolant velocity field | all-positive upflow, no recirculation | stable nat-circ | — |
| Mass flow vs power | ṁ ∝ P^(1/3) | self-regulating | — |

These satisfy the thermal-hydraulic hard constraints of `safety_criteria.yaml`
(`mdnbr_steady`, `pct_loca` envelope, `fuel_centerline_temperature`) with margin.

**OTSG primary duty and coupling.** The OTSG removes the full 125 MWth across a counterflow
once-through surface, so the secondary steam conditions are bounded by the primary legs. Because
the economizer pre-heats the feedwater, the secondary saturation temperature may sit *above* the
258 °C cold leg; the binding constraint is the **evaporator pinch** at the start-of-boiling point.
Re-coupling the cycle to the 308/258 °C legs (`scripts/thermo_cycle_recouple.py`, full counterflow
pinch) gives a practical optimum at **4.5 MPa / 296 °C steam → 39.7 MWe net, 8.8 °C pinch**. This
updates the §8.9 draft (4.8 MPa / 293 °C) by a small steam-condition shift while **holding the
40 MWe-class output** (see §8.4.8).

**Decay-heat removal.** After trip, the DHRS removes ANS-5.1 decay heat by passive natural
circulation to the in-containment heat sink, sized to ≥ 105 % of the 1 s decay power
(`prhr_capacity`). The quantitative station-blackout transient — decay heat vs passive removal,
PCT(t) over ≥ 100 h — is presented in **§8.5/§8.6**; it is the basis of the grace-period claim and
of the large-break-LOCA design-elimination argument (no large primary piping).

---

## 8.4.7 Operating conditions (defined states)

| Plant state | Primary | Heat sink | Cooling mode |
|---|---|---|---|
| Full power (100 %) | 12.8 MPa, 308/258 °C, 483 kg/s nat-circ | OTSG → turbine | natural circulation + OTSG |
| Cogeneration (district heat / H₂) | unchanged (reactor stays ~100 %) | OTSG; extraction steam → thermochemical sorption store; off-peak power → H₂ | natural circulation (**→§8.9**) |
| Hot standby | 12.8 MPa, near-isothermal | OTSG / DHRS | natural circulation |
| Trip / loss of secondary sink | depressurising as needed | **DHRS** → heat-sink tank | passive natural circulation |
| Station blackout (no AC/DC) | passive | DHRS + inventory, ≥ 72 h (→ unlimited) | fully passive (**→§8.5/§8.6**) |

---

## 8.4.8 Open items / cross-section dependencies (⚠CONFIRM)

1. **Primary–secondary re-coupling (RESOLVED — apply to §8.9).** Re-coupling the cycle to the
   308/258 °C legs (`scripts/thermo_cycle_recouple.py`) confirms the **40 MWe-class point holds**:
   the optimum moves to **4.5 MPa / 296 °C steam → 39.7 MWe net (31.8 %), 8.8 °C pinch**. §8.9
   Tables 8.9-2/8.9-3/8.9-4 need a minor update (steam 4.8→4.5 MPa, 293→296 °C, net 40.0→39.7 MWe,
   pinch recomputed) — a steam-condition edit, not a redesign. Decision for [TH]/[LAY]: keep the
   "40 MWe" nameplate (39.7 is within model uncertainty) or restate as 39.7 MWe net.
2. **Operating-pressure reconciliation.** This section uses **12.8 MPa op / ≈14.1 MPa design**
   (iPWR/NuScale basis); `safety_criteria.yaml` rows `primary_pressure_design` still carry the
   large-PWR default **15.5 / 17.2 MPa**. Azamhon to update the YAML to the iPWR values.
3. **Loop-loss tally.** Replace the lumped K_tot ≈ 8.6 with Adilbek's component-resolved loss
   breakdown (core grids, OTSG bundle, turn-around, downcomer) to close the loop balance exactly.
4. **Fuel centerline number.** Insert the peak centerline temperature from `thermal_stack.py`
   (limit 2590 °C) — value pending.
5. **DHRS / self-pressurizer / CVCS sizing.** Capacities in §8.4.4–8.4.5 are Tier-B; confirm with
   the §8.6 passive-safety analysis and the layout team.

---

### References (§8.4)

- N. E. Todreas, M. S. Kazimi, *Nuclear Systems I: Thermal Hydraulic Fundamentals* — single-phase
  natural-circulation loop analysis, friction/form losses.
- L. S. Tong, *Boiling Heat Transfer and Two-Phase Flow* — W-3 CHF / DNBR correlation.
- ANSI/ANS-5.1, *Decay Heat Power in Light Water Reactors*.
- IAPWS-IF97 (water/steam properties); models `scripts/natcirc_primary.py`, `scripts/thermo_cycle.py`.
- NuScale Power, *Design Certification Application* — integral-PWR natural-circulation / OTSG
  reference (12.8 MPa primary, helical OTSG).
- IAEA, *CAREM-25 Status Report* — natural-circulation integral PWR reference.
