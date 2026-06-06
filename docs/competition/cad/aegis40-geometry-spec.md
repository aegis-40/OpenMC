# Aegis-40 — CAD Geometry Specification (for the 3D Creo model)

**Purpose.** Single source of dimensions for the 3D engineering model (RPV, internals,
fuel assembly, core) used in the FER drawings/renders. Two tiers:

- **Tier A — LOCKED.** Pulled *exactly* from the as-run OpenMC `geometry.xml`
  (rev_3, the model behind `summary_report.txt`). Draw these to the number — they
  are the design of record for §8.1/§8.2 and must not be changed unilaterally.
- **Tier B — DESIGN-DEFINED.** Vessel-scale hardware the neutronics model does **not**
  represent (it stops at the radial water reflector + vacuum BC). Values below are
  *recommended starting points* scaled from reference iPWRs (CAREM-25, NuScale, SMART).
  **Flagged `⚠CONFIRM`** — ratify with the TH/mechanical lead before they become "design of record,"
  because they drive the primary-loop / natural-circulation TH.

All lengths in **mm** unless noted. OpenMC works in cm; ×10 conversions already applied.

---

## Tier A — Fuel, assembly & core (LOCKED, from `geometry.xml`)

### A1. Fuel pin (standard 17×17)
| Feature | Value (mm) | OpenMC source |
|---|---|---|
| Fuel pellet diameter | **8.192** (r = 4.0958) | z-cyl 0.40958 cm |
| Pellet–clad gap (radial) | 0.0915 | 0.41873 − 0.40958 cm |
| Clad inner diameter | 8.375 (r = 4.1873) | z-cyl 0.41873 cm |
| Clad outer diameter | **9.520** (r = 4.760) | z-cyl 0.476 cm |
| Clad thickness | 0.573 | derived |
| Clad material | Zr-4 | locked |
| **Active fuel length** | **2000** | z = −1000 → +1000 mm |
| Pin pitch (lattice) | **12.623** | lattice pitch 1.2623 cm |

### A2. Guide / instrument tube (control-rod & in-core channels)
| Feature | Value (mm) | OpenMC source |
|---|---|---|
| Guide-tube inner diameter | 11.248 (r = 5.624) | z-cyl 0.5624 cm |
| Guide-tube outer diameter | 12.040 (r = 6.020) | z-cyl 0.602 cm |
| Guide-tube wall | 0.396 | derived |

### A3. Burnable-absorber & blanket detail (the "smart" features to show)
| Feature | Value | Note |
|---|---|---|
| Gd₂O₃ pins per FA (centre/inner/edge ring) | 48 / 40 / 26 | radially zoned, core-avg 32 |
| Er₂O₃ pins per FA | 16 | flat hold-down + cold SDM |
| Gd/Er **fueled length** | 1800 mm (z = −900 → +900) | **100 mm axial cutback each end** |
| Gd/Er end-cutback plug | 100 mm top + 100 mm bottom | natural/blanket caps — a real, drawable detail |

> The 100 mm axial cutbacks on the Gd/Er pins are a genuine design feature worth
> rendering in a pin cutaway — it shows axial sophistication, not just a uniform rod.

### A4. Assembly (17×17 square)
| Feature | Value (mm) | Note |
|---|---|---|
| Lattice | 17 × 17 | 289 positions |
| Active lattice span | 214.59 | 17 × 12.623 |
| Assembly pitch (in core) | **216.038** | core-lattice pitch 21.6038 cm |
| Inter-assembly water gap | ≈ 1.45 total (0.72/side) | pitch − span |
| Guide tubes per FA | 24 + 1 instrument | standard 17×17 |

### A5. Core map (LOCKED)
| Feature | Value | Note |
|---|---|---|
| Arrangement | 5 × 5 lattice, **4 corners removed** | = **21 FA** |
| Core across-flats | 1080.19 mm | 5 × 216.038 |
| Equivalent core diameter | **≈ 1117 mm** | 2√(A/π), A = 21 × 216.038² |
| Active height | 2000 mm | |
| Radial reflector | 200 mm H₂O | core box ±540.1 → reflector ±740.1 mm |
| Axial reflector | 300 mm H₂O each end | active ±1000 → ±1300 mm |
| Control-rod clusters | **9** | insert into guide tubes; 9 CRDMs |
| Total core+reflector height | 2600 mm | |

**Core loading pattern (place by ring for enrichment/Gd zoning):** the 5×5−corners map
in `geometry.xml` uses three FA recipes r0/r1/r2 (rings). Mirror that in the loading-map
drawing — central FA, inner ring, outer ring — with the 4.95/4.70/4.40 wt% + Gd 48/40/26 zoning.

---

## Tier B — Reactor vessel & internals (DESIGN-DEFINED — ⚠CONFIRM with TH/mech lead)

Not in the neutronics model. Sized for a **125 MWth integral PWR**, anchored to
CAREM-25 (100 MWth, integral, natural-circulation, self-pressurized) and NuScale
(160 MWth, integral, natural-circulation, helical SG). **Default architecture chosen:
natural circulation + integral once-through helical SG + self-pressurized steam dome +
in-vessel CRDM** — the strongest passive-safety story for a 40 MWe iPWR, and it removes
large-bore primary penetrations (a real selling point). If the team prefers pumped/loop,
the riser/SG numbers change — that's the main fork (see Open Decisions).

### B1. Radial build (bottom of stack-up outward)
| Component | Recommended (mm) | Basis / reasoning |
|---|---|---|
| Equivalent core diameter | 1117 | Tier A (fixed) |
| Reflector envelope (across flats) | 1480 | Tier A (fixed) |
| **Core barrel** ID / OD | 1600 / 1650 (25 wall) | cylindrical shroud enclosing 21-FA cluster + reflector water |
| **Downcomer / SG annulus** gap | 120 | feedwater downflow + helical-coil SG tube bundle in upper annulus |
| **RPV** inner diameter | **2800** ⚠CONFIRM | barrel OD + 2× annulus + margin for helical SG bundle |
| RPV wall thickness | 160 (+ ~5 SS clad) ⚠CONFIRM | hoop stress: t≈P·r/σ, P≈12.5 MPa, r≈1.4 m, σ_allow≈138 MPa (SA-508) → ~122 + corrosion/clad |
| **RPV outer diameter** | ≈ 3130 ⚠CONFIRM | ID + 2×165 |

### B2. Axial stack-up (tan-to-tan), bottom → top
| Region | Height (mm) ⚠CONFIRM | Note |
|---|---|---|
| Lower head (hemispherical) | 800 | |
| Lower plenum / flow distributor | 800 | inlet flow turn-around |
| **Active core + axial reflectors** | 2600 | Tier A (fixed) |
| Riser + integral helical SG (annulus) | 3000 | drives natural-circulation head; SG wraps riser |
| Upper plenum | 800 | outlet collection |
| Steam dome / self-pressurizer + upper head | 2500 | CAREM-style self-pressurization |
| **RPV overall height (tan-to-tan)** | **≈ 10 500** | sum |

### B3. Internals to represent (level of detail for a good render)
- **Core barrel + lower core plate / support** (fuel sits on lower plate).
- **Upper core plate / hold-down** + the **9 control-rod guide structures** rising into the riser.
- **In-vessel CRDM** region (hydraulic/EM, CAREM-style) at the upper internals — 9 units.
- **Integral helical-coil once-through SG** bundle in the riser annulus (a coil sweep is enough).
- **Self-pressurizer steam dome** at the top (no separate pressurizer vessel).
- **Inlet/outlet** for the secondary (feedwater in / steam out) nozzles on the upper shell.

---

## What to model in Creo — scope (don't over-build)

Three deliverable models, in priority order. Aim for **clean, dimensioned, professional**,
not photoreal:

1. **Fuel assembly + pin cutaway** (Tier A, exact). Highest credibility-per-hour: a 17×17
   FA with guide tubes, Gd/Er pins highlighted by colour, and one pin sectioned to show
   pellet / gap / clad / the 100 mm axial cutback. → §8.2/§8.3.
2. **RPV cutaway (half-section)** showing the integral architecture: core → riser → helical SG →
   steam dome → in-vessel CRDM, with the core barrel/downcomer. This is the "wow" image
   (matches Mahmut's first two reference renders). → §8.1.
3. **Core loading map** (3D or 2.5D): 21 FA placed on the 5×5−corners map, coloured by
   enrichment ring + Gd zoning. → §8.2.

**Out of scope** (diminishing returns for the report): individual spacer grids, every
helical tube, bolt-level fasteners, secondary-side piping. Represent SG as a swept coil
band, grids as simple rings if at all.

---

## Creo build plan (parametric, bottom-up — a few days)

You know Creo well, so build it **parametric** so a dimension change ripples through:

1. **Parameters / relations first.** Put every Tier A + B number into a single
   `parameters` table (or a top-level skeleton part) — `PELLET_OD`, `CLAD_OD`,
   `PIN_PITCH`, `ACTIVE_LEN`, `ASSY_PITCH`, `RPV_ID`, etc. Drive all geometry from these.
2. **Pin part** (revolve/extrude): pellet stack → gap → clad, length = `ACTIVE_LEN`.
   Make a second config for Gd/Er pins with the 1800 mm fueled length + 100 mm cutbacks.
3. **Guide-tube part.**
4. **Assembly (17×17):** pattern the pin part on a 12.623 mm grid; replace the 24+1
   guide-tube positions; colour Gd (48/40/26) and Er (16) pins distinctly. Save as a
   subassembly.
5. **Core assembly:** pattern the FA on the 216.038 mm grid, delete the 4 corners → 21 FA.
   Apply the r0/r1/r2 ring recipes by colour.
6. **Vessel + internals (Tier B):** core barrel → lower/upper plates → riser → helical SG
   sweep → steam dome → RPV shell (revolve) → in-vessel CRDM. Build the RPV as a revolve
   so a **half-section view** gives the cutaway for free.
7. **Drawings/renders:** (a) FA + sectioned pin, (b) RPV half-section, (c) core map.
   Export PNG/PDF for the report; keep a Creo drawing (.drw) with dimensions for the appendix.

**Sequencing tip:** do model #1 (assembly) fully first — it's self-contained on Tier A and
needs zero `⚠CONFIRM` decisions, so you can start *today* while Tier B is being ratified.

---

## Open design decisions to ratify (blocks only Tier B / model #2)
1. **Circulation:** natural (CAREM/NuScale — recommended, passive story) vs pumped (changes riser height + adds pumps).
2. **SG type:** helical-coil once-through (recommended) vs straight/other.
3. **Pressurizer:** integral self-pressurized dome (recommended, CAREM) vs separate pressurizer.
4. **CRDM:** in-vessel (recommended, fewer penetrations) vs top-mounted external.
5. **RPV ID / wall** final values (B1) once SG bundle envelope is fixed.

> Models #1 and #3 (assembly + core map) depend on **zero** of these — start there.
</content>
</invoke>
