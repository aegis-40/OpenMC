# Aegis-40 — CAD Geometry Specification, **37-FA / 7×7 core** (rev_37FA, **tight / NuScale-benchmarked**)

**Supersedes** the 21-FA radial build in `aegis40-geometry-spec.md` (Tier B §B1/§B2) and the
21-FA `ga/dimension-schedule.md`. **Fuel/assembly Tier-A dims are UNCHANGED** (same 17×17
Westinghouse pin, same FA pitch) — only the *core map* and everything radially outboard of the
core change. Companion 2-D sheets: `ga/37fa/ga37_sheet{1,2,3}_*.png`
(`scripts/generate_ga_drawings_37fa.py`).

> **Rev note (2026-06-21):** the vessel was **tightened** from a first-pass RPV OD 3630 mm to
> **3010 mm** after benchmarking against the **NuScale FSAR Ch. 4** (`D:\Engineering\optimization
> research\NuScale.pdf`). The first pass carried a placeholder *separate* fat SG shroud (OD 2360)
> with a 630 mm downcomer outside it — the SG actually lives **inside** the downcomer annulus
> (NuScale arrangement), so the vessel ID is set by core+barrel+downcomer, not by the SG. Anchored
> to real NuScale internals and to our **lower 125 MWth** (vs NuScale 160 MWt), the 37-FA vessel
> ends up **smaller than the original 21-FA RPV** (OD 3130) while holding 76 % more fuel.

---

## 0. Benchmark — NuScale FSAR Ch. 4 vs Aegis-40 (the reference we tightened against)

NuScale is the ideal benchmark: **same core class** — 37 assemblies, 17×17, half-length (2 m) fuel.

| Parameter | **NuScale** (FSAR Tbl 4.1-2/4.3-1) | **Aegis-40 37-FA (tight)** | Note |
|---|---|---|---|
| Core thermal power | 160 MWt | **125 MWth** | we are 78 % of NuScale → can be *tighter* |
| Fuel assemblies / array | 37 / 17×17 | 37 / 17×17 | identical class |
| Active fuel height | 78.74 in = **2000 mm** | **2000 mm** | identical |
| Core diameter (across flats) | 59.25 in = **1505 mm** | **1512 mm** (equiv Ø1483) | ~identical |
| FA pitch | 8.466 in = 215.0 mm | **216.04 mm** | ~identical |
| Burnable absorber | gadolinia ≤32/FA | Gd₂O₃ ≤32/FA (+Er) | identical Gd basis |
| **Radial reflector** | **heavy SS-304**, 2.5–12.2 in (63–310) | **heavy steel** ~190 (option) / 200 water (locked neutronics) | adopt NuScale concept |
| **Core barrel ID / OD** | 74 / 78 in = **1880 / 1981** | **1900 / 2000** (wall 50) | matched |
| Control-rod assemblies | 16 CRA | **12 CRA** | our `CR_MAP` |
| System pressure | 1850 psia = 12.76 MPa | **12.8 MPa** | identical |
| **RPV outer diameter** | NuScale-class (Ch. 5, n/a here) | **3010 mm** | tighter than NuScale-class |

> **Key NuScale lessons applied:** (1) the **helical SG sits in the downcomer annulus** above the
> core — no separate fat shroud, so the SG does not drive the vessel ID; (2) a **heavy stainless
> reflector** (not bulk water) makes the barrel compact *and* flattens radial power (NuScale's stated
> peaking benefit) — a lever worth re-testing on our 37-FA neutronics; (3) the barrel sits at
> ~Ø1.9–2.0 m for this 37-FA class regardless of builder.

---

## 0′. Why only the radial build changes (the "everything fits" argument)

The pivot 21→37 FA was made at **constant core power (125 MWth)**, so every axial / flow /
heat-exchange dimension is **preserved**; only the *radial* envelope changes:

| Driver | Quantity | 21-FA | 37-FA tight | Changes? |
|---|---|---:|---:|---|
| Core power | 125 MWth | 125 | 125 | **no** → source term, decay heat, OTSG duty fixed |
| Active fuel height | mm | 2000 | 2000 | **no** (NuScale-class) |
| Primary flow | kg/s | 483 | 483 | **no** → riser area unchanged |
| OTSG duty | MWth | 125 | 125 | **no** → helical cartridge unchanged |
| Nat-circ thermal height H_th | m | 2.85 | 2.85 | **no** (axial stack preserved) → 2.62 kPa head valid |
| HM loading | tHM | 5.6 | **9.87** | grows → specific power **12.66** MW/tHM (½ of 21-FA) |
| Core diameter | equiv Ø mm | 1117 | **1483** | grows ×√(37/21)=1.327 |
| **RPV OD** | mm | 3130 | **3010** | **shrinks** (tight annulus, NuScale packaging) |
| Vessel height | mm | 11 640 | **11 530** | ~unchanged (slightly shorter heads) |

> **Bottom line:** with NuScale-style packaging the 37-FA reactor is **no bigger than the 21-FA
> vessel** — same height class, ~Ø3.0 m — while holding 76 % more fuel. Lower specific power
> (12.7 vs 22 MW/tHM) is a thermal-margin / DNBR *bonus*.

---

## Tier A — Fuel, assembly (LOCKED, UNCHANGED)

Identical to `aegis40-geometry-spec.md` §A1–A4 (and matches NuScale Tbl 4.3-1 to <0.5 %):

| Feature | Value (mm) |
|---|---|
| Pellet Ø / clad ID / clad OD (Zr-4) | 8.192 / 8.375 / 9.520 |
| Pin pitch | 12.623 |
| Guide-tube ID / OD | 11.248 / 12.040 |
| Active fuel length | 2000 |
| Assembly lattice / pitch | 17×17 / **216.038** |
| Guide + instrument tubes per FA | 24 + 1 |
| Gd₂O₃ / Er₂O₃ rods (avg per FA) | 32 / 16, ring-zoned |

---

## Tier A′ — Core map (37-FA, 7-wide octagon, LOCKED from `aegis40_neutronics_FER.ipynb` cell 5)

| Feature | Value | Source |
|---|---|---|
| Arrangement | 7×7 octagon (rows **3-5-7-7-7-5-3**) | `CORE_MAP`, `N_CORE=7` |
| Assemblies | **37 FA** | `CORE_MAP.sum()` |
| Across-flats (full rows) | **1512.27** (7 × 216.038) | half = 756.1; corner-pin r = 764 |
| Equivalent core diameter | **1483** | area-equivalent |
| Active height | 2000 | Tier A |
| Radial reflector | **~190 heavy steel** (option) / **200 H₂O** (locked) | see §6 |
| Axial reflector | 300 H₂O each end | `AXIAL_REFLECTOR_CM=30` |
| Total core+axial-reflector height | 2600 | |
| **Control-rod clusters (CRA)** | **12** (checkerboard; central FA = instrument) | `CR_MAP.sum()` → 12 in-vessel CRDM |
| Enrichment rings | centre 4.95 / 4.70 / 4.40, edge-pin 4.0 wt% | intra-FA grade |
| Gd ring-weights (rings 1/8/16/12) | 1.65 / 1.45 / 0.95 / 0.68 | `GD_RING_WEIGHTS`, core-avg≈1.0 |

---

## Tier B — Radial build (tight, ⚠CONFIRM with TH/mech lead)

From the vessel axis outward. Radii in **mm**.

| # | Component | Inner r | Outer r | Thick. | Basis |
|---|---|---:|---:|---:|---|
| — | Fuel envelope (across flats) | 0 | **756** | — | 7×FA_pitch/2 (corner pin 764) |
| 1 | Radial reflector (heavy steel / water) | 756 | 950 | ~190 | NuScale SS reflector concept (their 63–310) |
| 2 | **Core barrel** | **950** | **1000** | 50 | ID **1900** / OD **2000** (NuScale 74/78 in = 1880/1981) |
| 3 | Downcomer **+ integral helical OTSG** | 1000 | 1350 | **350** | cold leg; **SG cartridge sits in this annulus above the core** (NuScale) |
| 4 | **Reactor pressure vessel** | **1350** | **1505** | **150** (+5 clad) | ID **2700** / OD **3010**; ASME-III thick-wall hoop @14.1 MPa design, r1.35 m, SA-508 → t=147 mm |
| 5 | Reactor cavity (air) | 1505 | 1655 | 150 | standoff |
| 6 | Thermal / neutron shield (SS-304) | 1655 | 1705 | 50 | γ + fast-n |
| 7 | Borated polyethylene (5 wt% B) | 1705 | 1805 | 100 | thermal-n capture |
| 8 | Bulk bioshield (magnetite concrete) | 1805 | 3005 | **1200** | baseline — refine via `aegis40_shielding_FER.ipynb` (same 125 MWth source ⇒ ≈ unchanged) |
| 9 | Outer finish (ordinary concrete) | 3005 | 3105 | 100 | structural/finish |

**OTSG cartridge (UNCHANGED, in the upper annulus):** riser R560 → helical bundle R665–1075 (6 layers,
Inconel-690) → thin shroud R~1130 → SG-level downcomer R1130→1350 (≈ 220 mm). The bundle is **inside**
the vessel ID, so it adds *zero* to the envelope. Total radial envelope (incl. bioshield) ≈
**3.10 m radius / 6.21 m dia.**

---

## Tier B — Axial stack (37-FA tight): height **preserved**

Heads hemispherical, R = OD/2 = **1505**. The cylindrical-shell internal stack (core + plena + riser +
OTSG) is **length-unchanged** (power/flow/duty unchanged). EL = mm above DATUM B (lower-head outer pole).
**EL = model-z + 2361.5.**

| EL (mm) | Feature | Note |
|---:|---|---|
| 0 | Lower-head outer pole (DATUM B) | |
| 1335 | Support-skirt base ring | |
| **1505** | Lower head ↔ shell tangent | hemisphere R = OD/2 |
| 1655–1725 | Lower-plenum flow distributor | |
| 2305 | Core structure bottom | |
| 2605 | Active fuel bottom | 300 axial reflector |
| **3605** | Active fuel mid-plane (DATUM C) | neutronic reference |
| 4605 | Active fuel top | |
| 4905 | Upper core plate | |
| 5155 | OTSG bundle bottom / lower tubesheet | |
| 5355 | Feedwater inlet nozzle CL | |
| **6455** | OTSG bundle mid (heat-sink centre) | **H_th = 6455 − 3605 = 2850 mm = 2.85 m ✓** |
| 7555 | Main-steam outlet nozzle CL | |
| 7755 | OTSG bundle top / upper tubesheet | |
| 7905 | Core-outlet riser top | |
| **8705** | Cylindrical shell top / main flange | shell length 7200 unchanged |
| 10210 | Upper (closure) head top, outer | |
| 9960–11060 | Integral pressuriser body | |
| **11530** | Pressuriser dome top (overall height) | overall **≈ 11.53 m** |

**H_th preserved at exactly 2.85 m** ⇒ the validated natural-circulation balance (Δρ 93.6 kg/m³,
ΔP_driving 2.62 kPa, 483 kg/s, K_tot≈8.6 from §8.4) **carries over unchanged** — no loop re-analysis.

---

## 3. Volumes / inventory (for §8.1 / §8.11 / standards)

| Quantity | 21-FA | **37-FA tight** |
|---|---:|---:|
| Heavy-metal loading | 5.6 tHM | **9.87 tHM** |
| Specific power | ~22 MW/tHM | **12.66 MW/tHM** |
| Core active envelope volume | 1.96 m³ | **3.45 m³** |
| Equivalent core diameter | 1117 mm | **1483 mm** |
| RPV ID / OD | 2800 / 3130 | **2700 / 3010** |
| RPV wall (struct + clad) | 160 + 5 | **150 + 5** |
| Overall vessel height | 11.64 m | **11.53 m** |
| Bioshield outer diameter | 6.33 m | **6.21 m** |

---

## 4. OTSG fit check (the "OTSG can fit inside" requirement)

Same **125 MWth** ⇒ unchanged required surface ⇒ the helical cartridge is reused verbatim (riser R560,
6 layers R665–1075, axial pitch 230 mm, Inconel-690). It now sits in the **upper downcomer annulus**
(NuScale arrangement): primary rises in the central riser, turns at the top, flows **down over the coils**
in the annulus, then continues down the downcomer to the core. Because we run **125 < NuScale's 160 MWt**
in the same core diameter, the bundle has *more* surface margin per metre of height. **The OTSG fits with
margin in the unchanged 2600 mm (EL 5155–7755) bundle envelope, entirely inside the Ø2700 RPV ID.**

---

## 5. Standards / fit conformance summary

| Check | Result |
|---|---|
| Active fuel length | 2000 mm — NuScale-identical (pre-empts "looks short") |
| RPV pressure boundary | ASME III Div.1 Class 1; wall 150 mm = thick-wall hoop @ 14.1 MPa design, r 1.35 m |
| **RPV OD 3010 mm** | **rail-shippable** (under ~3.4 m clearance); smaller than CAREM-25 (Ø3.2 m) and our own 21-FA (Ø3.13 m) |
| Vessel height 11.53 m | between CAREM (~11 m) and NuScale (~17.7 m) — reasonable |
| Natural circulation | H_th 2.85 m **preserved** → §8.4 balance valid unchanged |
| OTSG | 125 MWth cartridge fits inside Ø2700 ID with surface margin |
| Reflector ≥ ~185 mm at every core face | flat 950−756=194, corner 950−764=186 ✓ |
| Codes (barrel/internals/SG/pzr/CRDM) | unchanged from §8.4 component table; reflector SA-965/SA-182 Type 304 (NuScale Tbl 4.5-2) |

**Open ⚠CONFIRM (TH/mech/layout):**
1. **OTSG-in-downcomer packing** at 350 mm core-level / ~220 mm SG-level annulus — confirm coil-bundle
   envelope + downcomer flow area (target velocity <0.3 m/s) with the TH lead.
2. **Wall 150 mm** against the detailed ASME-III stress report.
3. **Heavy-steel reflector** — adopt NuScale's SS reflector (compactness + peaking) vs the locked 20 cm
   water? This **changes neutronics** (re-run the 37-FA notebook with `RADIAL_REFLECTOR_MODE="steel"`);
   NuScale reports it *flattens* power — worth testing against our F_ΔH item, but note the 21-FA core
   preferred water (small-core albedo). Until re-run, the locked neutronics basis stays **20 cm water**.
4. **Bioshield concrete 1200 mm** pending `aegis40_shielding_FER.ipynb` optimisation.
5. **12-CRDM** head / upper-internals layout (NuScale uses 16; ours is 12 per `CR_MAP`).
