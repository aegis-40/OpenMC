# Aegis-40 — radial shielding build (CAD-anchored, adopted)

> **Authoritative results:** see `core-shielding-results.md` (dose, RPV fluence, figures,
> references). This file is the geometry/basis summary only.

**Model:** `openmc_model/rev7_shielding/shield_37fa_cad.py` (fixed-source coupled n+γ) +
`point_kernel_dose.py` (ANS-6.4 dose), lead-free.
**Source:** 125 MWth fission emission — Watt neutrons (~9.5×10¹⁸ n/s) + Maienschein prompt-fission
gammas (~2.8×10¹⁹ γ/s), volume-smeared core emitter. ICRP-116 AP flux-to-dose; MAGIC weight windows.
**Geometry:** concentric `ZCylinder` shells (axisymmetric integral RPV), bounded ±180 cm in z.

## Radial layer stack (cylindrical, from centreline) — adopted CAD build

| # | Layer | Material | Inner r (cm) | Outer r (cm) | Thickness (cm) | Basis |
|---|---|---|---|---|---|---|
| 1 | Active core + radial reflector | homogenised core + H₂O | 0 | 97.5 | — | core env. R = 75.54 → barrel ID R975 (CAD) |
| 2 | Core barrel | SS-304 | 97.5 | 100.0 | 2.5 | barrel OD R1000 (CAD) |
| 3 | Downcomer + OTSG annulus | H₂O (conservative) | 100.0 | 135.0 | 35.0 | RPV ID 1350 mm (CAD) |
| 4 | Reactor pressure vessel | SA-508 + clad | 135.0 | 151.5 | 16.5 | wall 160 + clad 5 mm, OD 1515 mm (CAD) — fluence tally here |
| 5 | Reactor cavity | air | 151.5 | 166.5 | 15.0 | standoff gap |
| 6 | Thermal / neutron shield | SS-304 | 166.5 | 171.5 | 5.0 | γ + fast-n (Ogul SMART multilayer) |
| 7 | Borated polyethylene (neutron layer) | 5 wt% B PE | 171.5 | 191.5 | **20.0** | fast/thermal-n; sized in §4.3 (Bagheri & Khalafi) |
| 8 | Bulk biological shield | magnetite (heavy) concrete | 191.5 | 371.5 | **180.0** | lead-free γ bulk; sized in §4.3 |
| 9 | Outer finish | ordinary concrete | 371.5 | 381.5 | 10.0 | structural / finish |

Total radial envelope ≈ **3.82 m** from centreline (≈ **7.6 m** shield outer diameter).

## Design criteria & result
- **Operational dose:** < 10 µSv/h just outside the bulk concrete (ALARA) — **met** (~0.23 µSv/h
  nominal, ≤ 5.5 µSv/h bounding; PASS).
- **RPV fast fluence:** E > 1 MeV, 60-yr < 1×10¹⁹ n/cm² (embrittlement / RTₙdt) — **met**
  (3.0×10¹⁸ n/cm²; PASS).
- **Materials are LEAD-FREE by team constraint** (toxicity/disposal); tungsten reserved for
  transport casks only.

## Neutron-layer sizing (§4.3)
Rows 7–8 were resized from the earlier **10 cm PE / 120 cm magnetite** stack. Magnetite is an
excellent gamma shield but hydrogen-poor, so the earlier stack did not robustly meet the
fast-neutron dose target across the removal-cross-section band. Increasing the borated-PE
neutron layer to **20 cm** and the magnetite bulk to **180 cm** closes the dose with ~40× margin,
at the cost of **+70 cm** radial growth (shield OD ≈ 6.2 m → ≈ 7.6 m — feeds plant-layout / civil
estimates). Vessel standoff and the RPV-fluence result are unaffected.

## Relationship to the core neutronics model
The biological shield is **decoupled** from the core eigenvalue/peaking results: neutrons reaching
the shield (beyond the RPV) have already left the multiplying region, so adding the shield changes
k_eff by ≪ 100 pcm and the pin-peaking factors not at all. Shielding is therefore run as a
**separate fixed-source dose calculation** off the same core source.

_Dims source: final 37-FA CAD. Layer architecture: Ogul et al. (2026) SMART multilayer; Bagheri &
Khalafi (2023) GA-optimised water+steel→poly→concrete. Method/coefficients: Rockwell TID-7004,
Chilton-Shultis-Faw, NIST-XCOM, ICRP-116._
