# Aegis-40 radial shielding build — adopted CAD build (sample input)

37-FA core, lead-free stack, axisymmetric integral RPV, bounded ±180 cm in z.
Source: 125 MWth fission emission (Watt neutrons + Maienschein prompt-fission gammas).
All radii from the core centreline. This is the input geometry for `code/shield_37fa_cad.py`
and `code/point_kernel_dose.py`.

| # | Layer | Material | Inner r (cm) | Outer r (cm) | Thickness (cm) |
|---|---|---|---|---|---|
| 1 | Active core + radial reflector | homogenised core + H₂O | 0 | 97.5 | — (core env. R = 75.54) |
| 2 | Core barrel | SS-304 | 97.5 | 100.0 | 2.5 |
| 3 | Downcomer + OTSG annulus | H₂O (conservative) | 100.0 | 135.0 | 35.0 |
| 4 | Reactor pressure vessel | SA-508 + clad | 135.0 | 151.5 | 16.5 |
| 5 | Reactor cavity | air | 151.5 | 166.5 | 15.0 |
| 6 | Thermal / neutron shield | SS-304 | 166.5 | 171.5 | 5.0 |
| 7 | Borated polyethylene (neutron layer) | 5 wt% B PE | 171.5 | 191.5 | **20.0** |
| 8 | Bulk biological shield | magnetite (heavy) concrete | 191.5 | 371.5 | **180.0** |
| 9 | Outer finish | ordinary concrete | 371.5 | 381.5 | 10.0 |

Total radial envelope ≈ **3.82 m** (outer shield diameter ≈ 7.63 m).

Rows 7–8 are the **adopted §4.3 neutron sizing** (was 10 cm PE / 120 cm magnetite): the
hydrogen-poor magnetite is a weak fast-neutron shield, so the borated-PE and bulk were resized
to close the < 10 µSv/h dose across the removal-cross-section band. See `../README_results.md`.

Materials are **lead-free** by team constraint (tungsten reserved for the transport cask only).
