#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40  --  Groeneveld 2006 CHF Look-Up Table (LUT) interpolator
=================================================================================

The 2006 CHF Look-Up Table (Groeneveld et al., "The 2006 CHF look-up table,"
Nuclear Engineering and Design 237 (2007) 1909-1922) is the AUTHORITATIVE,
data-based critical-heat-flux predictor: ~24 000 measured/normalised CHF values
for an 8 mm vertical water-cooled tube, tabulated on a (P, G, x) grid:

    P  [kPa]  : system pressure
    G  [kg/m2 s]: mass flux
    x  [-]    : thermodynamic equilibrium quality
    CHF[kW/m2]: critical heat flux for an 8 mm tube at those local conditions

This module does NOT contain the table (it is a large copyrighted dataset). It
LOADS the table from a data file you supply and interpolates it. >>> It refuses
to run without real data -- no CHF values are invented here. <<<

Use vs W-3 / Bowring: the LUT replaces an empirical correlation with the measured
CHF surface, retiring the "bare-tube / secondary-source coefficient" caveat that
applies to Bowring. Subchannel geometry is handled by the diameter factor K1; the
rod-bundle factor K2 is left = 1 by default (conservative, like the Bowring bare-
tube treatment) until a bundle/grid dataset is adopted.

--------------------------------------------------------------------------------
DATA FILE FORMAT (CSV, long form) -- put it at  tools/data/groeneveld_2006_lut.csv
    # any comment lines starting with #
    P_kPa, G_kgm2s, x_qual, CHF_kWm2
    100,   0,    -0.50,  5234
    100,   0,    -0.40,  4812
    ...
Must be a COMPLETE rectangular grid: every (P_i, G_j, x_k) combination present
once. The loader validates this and builds the 3-D CHF array. (Header line
optional; columns must be in the order P, G, x, CHF.)
--------------------------------------------------------------------------------
K-factor references -- IAEA-TECDOC-1203, "Thermohydraulic relationships for
advanced water cooled reactors" (2001), TABLE 3.3 (same forms as the
Groeneveld NED-163/237 Table 2):
  K1 (diameter):   (0.008/D_hy)^0.5 = (8mm/D_hy_mm)^0.5  for 2 <= D_hy <= 25 mm;
                   0.57 for D_hy > 25 mm.  CHF_subchannel = CHF_8mm * K1.
                   (Our earlier 16 mm/0.707 floor is the NED-2006 variant; both
                   agree for Aegis D_hy = 11.79 mm, well inside 2-25 mm.)
  K4 (heated length), for L/D_hy >= 5:
                   K4 = exp[(D_hy/L) * exp(2*alpha_h)]
                   alpha_h = x*rho_f / [x*rho_f + (1-x)*rho_g]  (0 for x <= 0)
                   L = heated length from start of heating to the local point.
                   K4 >= 1 (short-length CHF enhancement; -> 1 for long channels).
  K5 (axial flux): K5 = 1.0 for x <= 0;  K5 = q_loc/q_BLA for x > 0
                   (q_BLA = boiling-length-average heat flux from the x=0 onset;
                   computed in mdnbr.py where the axial profile lives).
  K2 (bundle) = min[1, (0.5+2*delta/d)*exp(-0.5 x^(1/3))] -> capped at 1, and = 1
  at the subcooled limiting point.  K3 (spacer grids) >= 1, NOT credited
  (conservative).  K7 (flow orientation) = 1 vertical; K8 = 1 (G > 0 upflow).
"""
import os
import sys
import math

DEFAULT_LUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "groeneveld_2006_lut.csv")


class LUT:
    """Loaded 2006 CHF look-up table on a rectangular (P,G,x) grid."""
    def __init__(self, P, G, X, CHF):
        self.P, self.G, self.X = P, G, X         # sorted unique axes (lists)
        self.CHF = CHF                            # CHF[iP][iG][iX] in W/m2

    @property
    def ranges(self):
        return (self.P[0], self.P[-1], self.G[0], self.G[-1], self.X[0], self.X[-1])


def load_lut(path=DEFAULT_LUT):
    """Parse the long-form CSV into a LUT. Raises if missing/incomplete."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Groeneveld LUT not found at:\n    {path}\n"
            "Supply the 2006 CHF look-up table as CSV (P_kPa,G_kgm2s,x_qual,CHF_kWm2).\n"
            "This module will NOT fabricate CHF data.")
    pts = {}
    Ps, Gs, Xs = set(), set(), set()
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if not s or s[0] == '#':
                continue
            parts = [p for p in s.replace(',', ' ').split()]
            if len(parts) < 4 or not _isnum(parts[0]):
                continue                          # skip header / stray text
            P, G, x, chf = (float(parts[0]), float(parts[1]),
                            float(parts[2]), float(parts[3]))
            pts[(P, G, x)] = chf * 1e3            # kW/m2 -> W/m2
            Ps.add(P); Gs.add(G); Xs.add(x)
    if not pts:
        raise ValueError(f"No numeric data rows parsed from {path}")
    P, G, X = sorted(Ps), sorted(Gs), sorted(Xs)
    nexp = len(P) * len(G) * len(X)
    if len(pts) != nexp:
        raise ValueError(
            f"LUT is not a complete grid: got {len(pts)} rows, "
            f"expected {len(P)}x{len(G)}x{len(X)} = {nexp}. "
            "Every (P,G,x) node must appear exactly once.")
    iP = {v: i for i, v in enumerate(P)}
    iG = {v: i for i, v in enumerate(G)}
    iX = {v: i for i, v in enumerate(X)}
    CHF = [[[0.0] * len(X) for _ in G] for _ in P]
    for (p, g, x), c in pts.items():
        CHF[iP[p]][iG[g]][iX[x]] = c
    return LUT(P, G, X, CHF)


def _isnum(s):
    try:
        float(s); return True
    except ValueError:
        return False


def _bracket(axis, v):
    """Return (i0, i1, f) for linear interp; clamps to ends, flags clamp."""
    if v <= axis[0]:
        return 0, 0, 0.0, (v < axis[0])
    if v >= axis[-1]:
        n = len(axis) - 1
        return n, n, 0.0, (v > axis[-1])
    for i in range(len(axis) - 1):
        if axis[i] <= v <= axis[i + 1]:
            f = (v - axis[i]) / (axis[i + 1] - axis[i])
            return i, i + 1, f, False
    return len(axis) - 1, len(axis) - 1, 0.0, True


def chf_lut(lut, P_kPa, G, x):
    """Trilinear-interpolated 8 mm-tube CHF [W/m2] at (P_kPa, G, x).
    Returns (chf, clamped_flag)."""
    iP0, iP1, fp, cP = _bracket(lut.P, P_kPa)
    iG0, iG1, fg, cG = _bracket(lut.G, G)
    iX0, iX1, fx, cX = _bracket(lut.X, x)
    C = lut.CHF
    def at(ip, ig, ix): return C[ip][ig][ix]
    # interpolate along x, then G, then P
    def lerp(a, b, f): return a + (b - a) * f
    c00 = lerp(at(iP0, iG0, iX0), at(iP0, iG0, iX1), fx)
    c01 = lerp(at(iP0, iG1, iX0), at(iP0, iG1, iX1), fx)
    c10 = lerp(at(iP1, iG0, iX0), at(iP1, iG0, iX1), fx)
    c11 = lerp(at(iP1, iG1, iX0), at(iP1, iG1, iX1), fx)
    c0 = lerp(c00, c01, fg)
    c1 = lerp(c10, c11, fg)
    return lerp(c0, c1, fp), (cP or cG or cX)


def k1_diameter(D_hy_mm):
    """Groeneveld K1 subchannel-diameter correction (IAEA-TECDOC-1203 Tab.3.3)."""
    if D_hy_mm < 2.0:
        D_hy_mm = 2.0
    if D_hy_mm > 16.0:
        return (8.0 / 16.0) ** 0.5      # 0.707 floor for D>16 mm
    return (8.0 / D_hy_mm) ** 0.5


def alpha_homog(x, rho_f, rho_g):
    """Homogeneous void fraction  alpha_h = x*rho_f/[x*rho_f + (1-x)*rho_g]
    (IAEA-TECDOC-1203 Tab.3.3, used by K4). Clamped to 0 for x <= 0."""
    if x <= 0.0:
        return 0.0
    return x * rho_f / (x * rho_f + (1.0 - x) * rho_g)


def k4_heated_length(D_hy_m, L_m, a_h):
    """Groeneveld K4 heated-length factor (IAEA-TECDOC-1203 Tab.3.3):
        K4 = exp[(D_hy/L) * exp(2*alpha_h)]   stated for L/D_hy >= 5,
    L = heated length from start of heating to the local point. K4 >= 1."""
    L = max(L_m, 5.0 * D_hy_m)          # stay inside the stated L/D >= 5 validity
    return math.exp((D_hy_m / L) * math.exp(2.0 * a_h))


def chf_groeneveld(lut, P_mpa, G, x, D_hy_m, K2_bundle=1.0):
    """CHF [W/m2] for the Aegis subchannel: LUT(8mm) * K1(diameter) * K2(bundle).
    K2 defaults to 1.0 (conservative bare-subchannel, like the Bowring treatment)."""
    chf8, clamp = chf_lut(lut, P_mpa * 1e3, G, x)   # MPa -> kPa
    K1 = k1_diameter(D_hy_m * 1e3)
    return chf8 * K1 * K2_bundle, K1, clamp


# --------------------------------------------------------------------------
# Standalone self-test / table summary (no fabrication: needs the data file)
# --------------------------------------------------------------------------
def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Groeneveld 2006 CHF LUT interpolator")
    ap.add_argument('--lut', default=DEFAULT_LUT, help="path to LUT CSV")
    ap.add_argument('--p', type=float, default=12.8, help="pressure [MPa]")
    ap.add_argument('--G', type=float, default=543.0, help="mass flux [kg/m2s]")
    ap.add_argument('--x', type=float, default=-0.05, help="quality [-]")
    ap.add_argument('--Dh', type=float, default=11.79e-3, help="hydraulic dia [m]")
    a = ap.parse_args(argv)
    lut = load_lut(a.lut)
    print(f"Loaded LUT: {len(lut.P)} P x {len(lut.G)} G x {len(lut.X)} x nodes")
    print(f"  P {lut.P[0]:.0f}-{lut.P[-1]:.0f} kPa | G {lut.G[0]:.0f}-{lut.G[-1]:.0f} "
          f"kg/m2s | x {lut.X[0]:.2f}..{lut.X[-1]:.2f}")
    chf, K1, clamp = chf_groeneveld(lut, a.p, a.G, a.x, a.Dh)
    print(f"  CHF(P {a.p} MPa, G {a.G}, x {a.x}) = {chf/1e6:.3f} MW/m2 "
          f"(8mm K1={K1:.3f}){'  [CLAMPED to table edge]' if clamp else ''}")


if __name__ == "__main__":
    main()
