# Aegis-40 — radial shielding build (CAD-anchored)

**Model:** `openmc_model/rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb` (§9), lead-free.
**Source:** the real 21-FA core lattice (eigenvalue mode, photon transport ON), normalised to
125 MWth → 9.5×10¹⁸ n/s. ICRP-116 AP flux-to-dose; MAGIC weight windows for deep penetration.
**Geometry:** concentric `ZCylinder` shells (axisymmetric integral RPV), bounded ±180 cm in z.

## Radial layer stack (cylindrical, from centreline)

| # | Layer | Material | Inner r (cm) | Outer r (cm) | Thickness (cm) | Basis |
|---|---|---|---|---|---|---|
| 1 | Active core + radial reflector | real pin lattice + H₂O | 0 | 80.0 | — | core box 54 + 20 cm reflector → barrel ID 1600 mm (CAD B1) |
| 2 | Core barrel | SS-304 | 80.0 | 82.5 | 2.5 | barrel OD 1650 mm (CAD B1) |
| 3 | Downcomer + helical-SG annulus | H₂O (downcomer) | 82.5 | 140.0 | 57.5 | RPV ID 2800 mm (CAD B1) — **dominant attenuator** |
| 4 | Reactor pressure vessel | SA-508 + clad | 140.0 | 156.5 | 16.5 | wall 160 + 5 mm, OD ~3130 mm (CAD B1) — fast-flux/fluence tally here |
| 5 | Reactor cavity | air | 156.5 | 171.5 | 15.0 | standoff gap |
| 6 | Thermal / neutron shield | SS-304 | 171.5 | 176.5 | 5.0 | gamma + fast-n (Ogul SMART multilayer) |
| 7 | Borated polyethylene | 5 wt% B PE | 176.5 | 186.5 | 10.0 | thermal-n capture, low 2° gamma (Bagheri & Khalafi) |
| 8 | Bulk biological shield | magnetite (heavy) concrete | 186.5 | 306.5 | 120.0 | lead-free γ+n bulk; bound water moderates |
| 9 | Outer finish | ordinary concrete | 306.5 | 316.5 | 10.0 | structural / finish |

Total radial envelope ≈ **3.17 m** from centreline (≈ 6.3 m shield diameter).

## Design criteria
- **Operational dose target:** < 10 µSv/h just outside the bulk concrete (ALARA, Bagheri & Khalafi).
- **RPV fast fluence:** E > 1 MeV neutron flux at the vessel wall → 60-yr fluence (embrittlement / RTNDT).
- **Materials are LEAD-FREE by team constraint** (toxicity/disposal); tungsten reserved for transport casks only.

## Why the vessel dims matter (and why the model was corrected, 2026-06-20)
The earlier draft used placeholder compact radii (RPV inner at r=93 cm, ~13 cm downcomer). The CAD
integral RPV actually has a **57 cm downcomer + helical-SG annulus** (water + SG steel) before a
16.5 cm SA-508 wall. That annulus is the single largest attenuator between core and bioshield;
modelling it correctly **lowers** the predicted bioshield dose and removes a "where did these radii
come from?" question. Layer *thicknesses* (rows 5–9) are the shield design and are unchanged — only
their standoff was anchored to the real vessel.

## Relationship to the core neutronics model
The biological shield is **decoupled** from the core eigenvalue/peaking results: neutrons reaching
the shield (beyond the RPV) have already left the multiplying region, so adding the shield changes
k_eff by ≪ 100 pcm and the pin-peaking factors not at all. The core model's vacuum boundary at the
20 cm reflector is mildly conservative on k (the real vessel reflects marginally more). Shielding is
therefore correctly run as a **separate fixed-spectrum dose calculation** off the same lattice source.

_Dims source: `docs/competition/cad/aegis40-geometry-spec.md` Tier B §B1. Layer architecture:
Ogul et al. (2026) SMART multilayer; Bagheri & Khalafi (2023) GA-optimised water+steel→poly→concrete._
