# Aegis-40 iPWR — Reactor Vessel General-Arrangement Dimension Schedule

> **Purpose.** Master dimensional reference for building the integral RPV assembly in Creo
> Parametric 11. Every value is taken from the locked CAD geometry (`scripts/generate_rpv_step.py`,
> `generate_core_step.py`, `generate_fa_step.py`) so a model built to this schedule matches
> `cad/aegis_rpv.step`. All dimensions in **millimetres** unless noted. Companion drawing sheets:
> `cad/ga/ga_sheet1..5_*.png`.

## Datums and conventions

- **DATUM A — Vessel axis:** the vertical centreline of the RPV (radial 0). All radial positions are
  radii from this axis; diameters are 2×radius.
- **DATUM B — Elevation zero (EL 0):** the outer pole of the lower hemispherical head (model
  z = −2641.5 mm). **EL = model-z + 2641.5.** All elevations below are EL (mm above DATUM B).
- **DATUM C — Core mid-plane:** active-fuel mid-plane, EL 3660 (model z = 1018.5) — neutronic reference.
- Vessel is **axisymmetric**; build each shell/ring as a revolve about DATUM A. The STEP cutaway is a
  quarter-cut for visualisation only — the real parts are full revolves.
- Architecture: **natural-circulation integral PWR** — core, riser, helical-coil OTSG, self-pressuriser
  and in-vessel CRDMs all inside one vessel; no external primary loop, no reactor coolant pumps
  (RCP option in §“Pump configuration”).

## Key elevations (EL, mm above DATUM B)

| EL | Feature |
|---:|---|
| 0 | Lower head outer pole (DATUM B) |
| 1390 | Support-skirt base ring (support plane) |
| 1560 | Lower head ↔ shell tangent line |
| 1710–1780 | Lower-plenum flow distributor plate |
| 2280–2360 | Lower core support plate |
| 2360 | Core structure bottom (incl. lower axial reflector) |
| 2660 | Active fuel bottom |
| 3660 | Active fuel mid-plane (DATUM C) |
| 4660 | Active fuel top |
| 4960 | Core structure top / upper core plate bottom |
| 4960–5040 | Upper core plate |
| 5210 | Steam-generator bundle bottom / lower tube sheet |
| 5410 | Feedwater inlet nozzle centreline |
| 7610 | Main-steam outlet nozzle centreline |
| 7810 | SG bundle top / upper tube sheet |
| 7960 | Core-outlet riser top |
| 8760 | Cylindrical shell top / main closure flange |
| 10320 | Upper (closure) head top, outer |
| 10070–11170 | Integral pressuriser body |
| 11640 | Pressuriser dome top, outer (overall height) |

**Overall envelope:** Ø3120 mm shell (Ø3900 over skirt base) × ~11.64 m tall (skirt base to pzr dome).

---

## 1. Reactor pressure vessel (pressure boundary)

| Component | OD | ID | Wall t | Height / extent | Elevation (EL) | Mates with |
|---|---:|---:|---:|---|---|---|
| Lower hemispherical head | 3120 | 2800 | 160 | R 1560 hemisphere | 0 → 1560 (pole→tangent) | shell (weld), skirt (outer), flow distributor (inner) |
| Cylindrical vessel shell | 3120 | 2800 | 160 | 7200 | 1560 → 8760 | both heads (welds), flange |
| Upper (closure) head, hemispherical | 3120 | 2800 | 160 | R 1560 hemisphere | 8760 → 10320 | flange (bolted), pressuriser (integral) |
| Main closure flange | ~3600 (bolt Ø) | 2800 | 250 (axial) | ring | 8760 (joint) | shell + closure head, stud bolts |
| Support skirt (cone) | 3780 → 3120 | — | 40 | 1030 | 1480 → 2510 | lower head (outer weld), base ring |
| Skirt base ring (support pad face) | 3900 | 3600 | 90 | ring | 1390 → 1480 | embedment / support steel |
| Feedwater inlet nozzle | 260 (+forging) | 130 bore→ | sched | proj. to R 1880 | 5410 (CL) | shell penetration, SG feed header |
| Main-steam outlet nozzle | 260 (+forging) | 130 bore | sched | proj. to R 1880 | 7610 (CL) | shell penetration, SG steam header |
| Safety-relief / vent nozzles | 100–160 | — | sched | on closure head / pzr | 10070+ | pzr steam space |
| Drain nozzle | 80 | — | sched | lower head pole | 0–200 | lower plenum |
| Instrument penetrations (typ.) | 40–60 | — | sched | multiple | various | guide tubes / sensors |
| Lifting lugs (×3, 120° apart) | — | — | 120 plate | — | ~8600 (below flange) | closure-head forging |
| Support pads (×4 on skirt base) | 400×300 | — | 60 | — | 1390 | skirt base ring |

---

## 2. Core region (core internals)

| Component | OD | ID | Wall t | Height | Elevation (EL) | Radial pos. | Mates with |
|---|---:|---:|---:|---:|---|---|---|
| Core barrel | 1540 | 1480 | 30 | ~2680 | 2360 → 5040 | 740–770 R | upper/lower core plates, baffle |
| Radial reflector (H₂O / structure) | 1480 | ~1200 | — | 2600 | 2360 → 4960 | 600–740 R | barrel (out), core baffle (in) |
| Core baffle / shroud | ~1200 | ~1180 | 10 | 2000 | 2660 → 4660 | ~590–600 R | reflector, fuel envelope |
| Active fuel region (21 FA envelope) | ~1200 (across flats) | — | — | 2000 (active) | 2660 → 4660 | ≤ 600 R | core plates (top/bottom nozzles) |
| Lower core support plate | 1520 | — | 80 | 80 | 2280 → 2360 | ≤ 760 R | barrel, FA bottom nozzles, lower plenum |
| Upper core plate | 1520 | — | 80 | 80 | 4960 → 5040 | ≤ 760 R | barrel, FA top nozzles, CRDM guide |
| Lower-plenum flow distributor | 1680 | perforated | 70 | 70 | 1710 → 1780 | ≤ 800 R | lower head, downcomer outlet |
| Lower plenum (coolant space) | — | — | — | ~720 | 1560 → 2280 | ≤ 1400 R | lower head, distributor, core inlet |
| Upper plenum (coolant space) | — | — | — | ~170 | 5040 → 5210 | ≤ 1400 R | upper core plate, riser inlet |

Fuel-assembly lattice (per `generate_fa_step.py`): 17×17, **pin pitch 12.623**, **assembly pitch
216.038**; rod OD 9.520 / clad ID 8.375 / pellet OD 8.192; guide-tube OD 12.040 / ID 11.248; active
2000, clad length 2200. 21 assemblies in rings r0/r1/r2 = 1/8/12 (see `cad/core_map.csv`).

---

## 3. Coolant-circulation path (natural circulation)

| Component | OD | ID | Wall t | Height | Elevation (EL) | Mates with |
|---|---:|---:|---:|---:|---|---|
| Core-outlet riser (hot-leg) | 1120 | 1060 | 30 | 3000 | 4960 → 7960 | upper plenum (bottom), SG inlet (top) |
| Downcomer annulus (cold-leg) | 2800 (vessel ID) | 1540 (barrel) / 2360 (shroud) | — | ~6250 | 2360 → 7810 | vessel wall (out), barrel+shroud (in) |
| Flow-return / core-inlet path | — | — | — | — | 1560 → 2660 | distributor → lower plenum → core |

**Natural-circulation loop:** core (heat in, ↑) → upper plenum → **riser ↑** → SG inlet → over SG tubes
(heat out, ↓, density ↑) → **downcomer ↓** → flow distributor → lower plenum → core inlet. Driving head
= elevation between core mid (EL 3660) and SG mid (EL 6510) ≈ 2.85 m thermal centres.

---

## 4. Steam-generation system (integral helical-coil OTSG)

| Component | OD | ID | t | Height | Elevation (EL) | Notes |
|---|---:|---:|---:|---:|---|---|
| SG shroud (bundle wrapper) | 2360 | 2340 | 10 | 2600 | 5210 → 7810 | separates riser/bundle from downcomer |
| Helical tube bundle (6 layers) | 2150 | 1330 | — | 2600 | 5210 → 7810 | layer radii 665/750/835/920/1005/1075 |
| SG tube (helical) | 34 | ~26 | 4 | coil | 5210 → 7810 | tube OD 34, axial pitch 230, counter-wound |
| Lower tube sheet | 2200 | 1260 | 120 | 120 | 5090 → 5210 | feedwater header face |
| Upper tube sheet | 2200 | 1260 | 120 | 120 | 7810 → 7930 | steam header face |
| Feedwater inlet header/nozzle | 260 | 130 | — | — | 5410 (CL) | secondary in (subcooled) |
| Main-steam outlet header/nozzle | 260 | 130 | — | — | 7610 (CL) | secondary out (dry steam) |

Secondary flow: feedwater in @ EL 5410 → up tube ID (boils) → dry steam out @ EL 7610. Primary flows
**downward over the tube OD** in the shell-side annulus (riser-outer 560 R → shroud-inner 1170 R).

---

## 5. Pressurisation system (integral self-pressuriser)

| Component | OD | ID | Wall t | Height | Elevation (EL) | Mates with |
|---|---:|---:|---:|---:|---|---|
| Pressuriser body (cylinder) | 940 | 860 | 40 | 1100 | 10070 → 11170 | closure head (bottom), pzr dome |
| Pressuriser dome (hemisphere) | 940 | 860 | 40 | R 470 | 11170 → 11640 | pzr body, relief nozzles |
| Pressuriser plate (separation) | 940 | — | 60 | 60 | ~10070 | divides pzr water/steam from vessel |
| Pressuriser heaters (×8 rods) | 52 | — | — | ~800 | 10120 → 10920 | on Ø500 bolt circle (R 250) |
| Surge line | 140 | — | sched | ~1450 | 8660 → 10070 | vessel upper plenum ↔ pzr water space |
| Spray nozzle | 60 | — | — | — | 11400 | pzr dome (top), spray header |
| Steam space (saturated) | — | — | — | upper ~⅓ | 10900 → 11640 | self-pressurising cushion |
| Water-inventory region | — | — | — | lower ~⅔ | 10070 → 10900 | connected to vessel via surge line |

---

## 6. Control-rod drive system (in-vessel CRDM)

| Component | OD | ID | Wall t | Height | Elevation (EL) | Notes |
|---|---:|---:|---:|---:|---|---|
| CRDM housing (lower) | 140 | 124 | 8 | 900 | 4910 → 5810 | over checkerboard CRA positions (per `CR_MAP`) |
| CRDM latch / motor housing | 196 | — | — | 320 | 5810 → 6130 | latch mechanism |
| Drive shaft / drive rod | 56 | — | — | to EL 7430 | 4910 → 7430 | couples to RCCA spider |
| CRDM mounting plate / upper support | 1520 | — | 100 | 100 | 6130 → 6230 | carries 12 CRDM units |
| Control-rod guide tubes (in-core) | 12.04 | 11.25 | 0.4 | 2200 | 2660 → 4860 | 25 per FA, guide RCCA into fuel |
| Guide structure (above core) | — | — | — | — | 5040 → 6130 | continuous CR guidance, plenum |
| Instrumentation guide tubes | 40 | — | — | — | core → top | in-core detectors / TC |

**CRDM count:** 12 units in a checkerboard pattern across the 37-FA core; the **central assembly is
instrumented (no rod)**, so there is **no CRDM on the vessel axis**. Positions follow `CR_MAP`
(37-FA geometry spec, `CR_MAP.sum()` → 12). Each unit = lower housing + latch housing + drive rod
on DATUM A-parallel axes at the respective assembly centres. ⚠ Take the per-axis CRDM coordinates
from `CR_MAP` (checkerboard) — **not** the former r0+r1 central-plus-inner-ring layout, which placed
a CRDM on the axis and is superseded.

---

## 7. Instrumentation (penetrations & sensors)

| Item | Size | Location (EL / radial) | Function |
|---|---|---|---|
| Thermocouple penetrations | Ø40 | core outlet, EL 4960, several radii | core-exit temperature |
| Neutron detectors (in-core) | Ø50 guide | through instrument tubes, EL 2660–4660 | flux / power distribution |
| Ex-core detectors | — | downcomer / outside vessel, core mid EL 3660 | power-range monitoring |
| Pressure taps | Ø20 | pzr EL 11000, vessel head | primary pressure |
| Flow-measurement ports | Ø25 | riser EL 6500, downcomer | natural-circ flow |
| Vessel-level instrumentation | Ø25 ×2 | EL 5000 & EL 8500 (Δp) | coolant inventory / level |

---

## 8. Pump configuration (design option)

**Configuration A — natural circulation (baseline).** No pumps; loop driven by the core↔SG thermal
centre offset (≈2.85 m). No pump nozzles/penetrations in the pressure boundary — a key safety/simplicity
advantage. **This is the Aegis-40 reference design.**

**Configuration B — reactor coolant pumps (alternate, for trade study).** If forced circulation is
required, add canned-motor RCPs in the downcomer:

| Component | OD | Height | Elevation (EL) | Qty | Notes |
|---|---:|---:|---|---:|---|
| Reactor coolant pump (canned-motor) | 600 | 1400 | 7900 → 9300 (in/above downcomer) | 2–4 | glandless, no shaft seal |
| Pump motor (integral can) | 600 | included | — | — | wet-stator, primary-cooled |
| Pump casing / volute | 700 | 500 | 7800 | — | discharges into downcomer |
| Pump penetration (closure head) | 650 | — | 8760 (flange) | 2–4 | head nozzle + flange |
| Pump support | bracket | — | downcomer ledge | — | seismic restraint |
| Maintenance clearance | Ø900 envelope | 1600 above head | — | — | motor withdrawal over each pump |

In Config B the riser/downcomer flow areas are unchanged; the pumps add ~Δp to raise flow above the
natural-circulation value.

---

## CAD build order (recommended Creo part/assembly tree)

1. **Lower head** (revolve, Ø3120/Ø2800 hemisphere) → 2. **Support skirt + base ring** (revolved cone
on lower head OD) → 3. **Flow distributor** + **lower core plate** → 4. **Core barrel** (revolved tube)
→ 5. **Radial/axial reflector + baffle** → 6. **Fuel-assembly envelopes** (pattern 21 on `core_map`)
→ 7. **Upper core plate + CRDM guide structure** → 8. **Core-outlet riser** → 9. **SG shroud + tube
sheets + helical bundle** (helical sweep, pattern layers) → 10. **Cylindrical shell** (revolve) +
**feedwater/steam nozzles** → 11. **Main flange + closure head** → 12. **Pressuriser body + dome +
heaters + surge line** → 13. **CRDM housings + latch + drive rods** (pattern 12) → 14. nozzles /
instrument penetrations / lugs.

Each numbered item is a separate Creo part; mate on the coincident faces / axes given in the “Mates
with” columns. Use DATUM A (axis) + DATUM B (EL 0 plane) as the assembly skeleton references.
