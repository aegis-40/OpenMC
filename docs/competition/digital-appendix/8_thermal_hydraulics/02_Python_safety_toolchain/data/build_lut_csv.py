#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build tools/data/groeneveld_2006_lut.csv from values TRANSCRIBED from the paper.

Source: D.C. Groeneveld et al., "The 2006 CHF look-up table," Nuclear Engineering
and Design 237 (2007) 1909-1922 -- pages 1919 (12000 kPa block) & 1920 (14000 kPa
block). CHF in kW/m2, 8 mm vertical tube, water.

SUBSET rationale: Aegis runs at P 12.8 MPa (brackets 12000/14000 kPa) and core
G 543 kg/m2s, with AOO down to ~G 434 (80% flow). The mass-flux rows
G = 300, 500, 750, 1000 bracket that whole envelope, so only those rows (x all 23
columns, both pressure planes) are transcribed = a complete 2 x 4 x 23 grid.
Extend with more G rows / the 10000 kPa plane (AOO depressurisation) if needed.

>>> VERIFY a few cells against the printed page before quoting as the final number
    (same spot-check discipline as Bowring vs Todreas & Kazimi).
"""
import os

# 23 thermodynamic-quality columns (the table header x->)
X = [-0.50, -0.40, -0.30, -0.20, -0.15, -0.10, -0.05, 0.00, 0.05, 0.10,
     0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]

# CHF [kW/m2], transcribed row-by-row. Key = (P_kPa, G_kgm2s).
DATA = {
    # ---- 12000 kPa (page 1919) ----
    (12000, 300):  [5366, 5081, 4741, 4434, 4269, 4138, 3950, 3838, 3516, 3199, 2912, 2701, 2467, 2285, 2108, 1940, 1830, 1630, 1250, 840, 500, 316, 0],
    (12000, 500):  [5647, 5188, 4869, 4445, 4298, 4131, 3988, 3819, 3555, 3240, 2951, 2724, 2500, 2310, 2160, 1875, 1678, 1474, 1011, 423, 296, 205, 0],
    (12000, 750):  [6233, 5596, 5072, 4528, 4310, 4067, 3904, 3659, 3418, 3067, 2773, 2526, 2277, 2039, 1798, 1396, 1180, 989, 312, 251, 211, 131, 0],
    (12000, 1000): [7031, 6267, 5500, 4700, 4430, 4100, 3855, 3447, 3243, 2878, 2516, 2291, 1905, 1640, 1420, 1073, 920, 310, 214, 118, 78, 76, 0],
    # ---- 14000 kPa (page 1920) ----
    (14000, 300):  [4479, 4268, 4074, 3858, 3727, 3586, 3448, 3301, 2996, 2701, 2358, 2100, 1970, 1756, 1651, 1481, 1308, 1143, 842, 615, 347, 217, 0],
    (14000, 500):  [4680, 4404, 4184, 3876, 3713, 3545, 3401, 3249, 3001, 2641, 2373, 2089, 1825, 1559, 1422, 1273, 1087, 1017, 319, 298, 192, 119, 0],
    (14000, 750):  [5155, 4929, 4487, 3917, 3666, 3417, 3241, 3056, 2841, 2505, 2177, 1849, 1591, 1332, 1131, 885, 769, 502, 265, 135, 79, 77, 0],
    (14000, 1000): [6001, 5588, 4980, 4089, 3670, 3378, 3049, 2693, 2399, 2051, 1731, 1466, 1244, 1017, 854, 745, 649, 295, 224, 102, 67, 49, 0],
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "groeneveld_2006_lut.csv")


def main():
    # integrity checks before writing
    for k, row in DATA.items():
        assert len(row) == len(X), f"{k}: {len(row)} values, expected {len(X)}"
        # CHF should be (weakly) monotone-decreasing in x within a row
        for a, b in zip(row, row[1:]):
            assert a >= b, f"{k}: non-monotone CHF at value {a}->{b} (transcription?)"
    with open(out, "w") as fh:
        fh.write("# Groeneveld 2006 CHF Look-Up Table -- SUBSET (P 12000/14000 kPa, G 300-1000)\n")
        fh.write("# Source: NED 237 (2007) 1909-1922, pp.1919-1920. CHF kW/m2, 8 mm tube.\n")
        fh.write("# Transcribed by build_lut_csv.py -- spot-check vs the paper before final quoting.\n")
        fh.write("P_kPa, G_kgm2s, x_qual, CHF_kWm2\n")
        for (P, G) in sorted(DATA):
            for x, chf in zip(X, DATA[(P, G)]):
                fh.write(f"{P}, {G}, {x:.2f}, {chf}\n")
    n = len(DATA) * len(X)
    print(f"wrote {out}\n  {len(DATA)} (P,G) rows x {len(X)} x-cols = {n} nodes "
          f"({len(set(p for p,_ in DATA))} P x {len(set(g for _,g in DATA))} G x {len(X)} x)")


if __name__ == "__main__":
    main()
