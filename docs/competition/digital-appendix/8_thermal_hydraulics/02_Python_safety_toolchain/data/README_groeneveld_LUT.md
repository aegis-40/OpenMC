# Groeneveld 2006 CHF Look-Up Table — data file needed for `--chf groeneveld`

> **Status.** The K-factor forms are taken from **IAEA-TECDOC-1203, "Thermohydraulic
> relationships for advanced water cooled reactors" (2001), Table 3.3**: K1 (diameter),
> **K4 (heated length) and K5 (axial-flux, boiling-length average)** are implemented in
> `groeneveld.py` + `mdnbr.py --chf groeneveld`; K2 is capped at 1 (and = 1 at x ≤ 0), K3
> (spacer grids) is not credited (conservative), K7/K8 = 1 for vertical upflow.
> Result at the MOC COLR envelope: **MDNBR 6.18** (z 1.115 m, x −0.096 — a physical
> mid-channel minimum; the limiting point is subcooled, so K5 = 1 and K4 ≈ 1.01 there).
> The LUT thus corroborates W-3/Bowring with ~4.7× margin over the 1.3 limit; the binding
> safety basis remains W-3/Bowring at the COLR envelope (real-shape 1.33 / 2.13).


`tools/groeneveld.py` and `mdnbr.py --chf groeneveld` need the **2006 CHF Look-Up
Table** as a data file. It is **not bundled** (large, copyrighted) and the code
**will not fabricate it** — it errors out if the file is missing.

## What to provide
Save the table here as:

    tools/data/groeneveld_2006_lut.csv

Long-form CSV, one row per grid node, columns in this order:

    # comments allowed
    P_kPa, G_kgm2s, x_qual, CHF_kWm2
    100,   0,    -0.50,  5234
    100,   0,    -0.40,  4812
    ...

Requirements:
- A **complete rectangular grid**: every (P_i, G_j, x_k) combination present once.
  The loader checks `n_rows == nP·nG·nx` and refuses partial grids.
- Units: **P in kPa, G in kg/m²·s, x dimensionless, CHF in kW/m²** (8 mm tube,
  the table's normalising diameter). The loader converts kW→W internally.
- Header line optional; extra comment lines (`#`) ignored.

## Minimum data subset (if the full table is hard to get)
Aegis runs at **P ≈ 12.8 MPa = 12800 kPa**. Trilinear interpolation only needs the
two pressure planes **bracketing 12.8 MPa** — in the standard 2006 grid these are
**12000 and 14000 kPa**. So a file containing just those two P-planes (each a full
G×x matrix) is sufficient for the design-point and AOO runs. The full table is
better (covers AOO depressurisation), but the two planes are sufficient.

## Where to source it
- **Primary:** Groeneveld, D.C., et al., *"The 2006 CHF look-up table,"* Nuclear
  Engineering and Design **237** (2007) 1909–1922 — the table is printed in the paper.
- IAEA-TECDOC / AECL distributions of the LUT (machine-readable versions exist).
- From a PDF/scan, extract the 12000 & 14000 kPa planes with
  `build_lut_csv.py`, then spot-check a few cells against the page.

## After the file is in place
```
python3 tools/groeneveld.py            # prints grid size + a sample CHF (sanity)
python3 tools/mdnbr.py --chf groeneveld   # bare run = the COLR-envelope design point
```
The K1 diameter factor (8→11.79 mm) and the K4/K5 axial corrections are applied
automatically; bundle factor K2 is capped at 1 (conservative). Verify the K1 form against IAEA-TECDOC-1203 Table 3.3 (the same spot-check
discipline as the Bowring verification vs Todreas & Kazimi).
