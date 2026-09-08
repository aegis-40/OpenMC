#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 cycle MDNBR — BOC / MOC / EOC hot-channel analysis.

The cycle-resolved neutronics record (`docs/neutronics_cycle_record.md`) resolves the
peaking over the cycle (F_dH includes the x1.03 engineering allowance; separability
F_q = F_dH*F_z holds to 3 decimals in the record). The Gd-burnout hump at MOC
(~13.5 GWd/t) exceeds the generic screening values, so the record assigns the T-H
closure item: hot-channel analysis at the MOC peaking ENVELOPE (F_dH 1.75, F_z 1.41),
acceptance **MDNBR >= 1.30** and fuel/clad temperatures below limits.

Method (identical stack to the report; single-phase, linear-in-power):
  - q'_avg = P/(N_pin*L) = 6.398 kW/m — power, pin count and geometry are UNCHANGED
    over the cycle, so the validated CFD/mesh basis stands; only the peaking moves.
  - per state: qpeak = q'_avg * F_q, and the chopped-cosine extent Le is solved from
    F_z (F_z = a/sin a, a = pi*L/(2*Le)); the hot-channel enthalpy rise then carries
    F_dH = F_q / F_z automatically (separable, exactly as the record factorises).
  - MDNBR at the canonical natural-circulation flow G 542: W-3 + Tong (binding-
    conservative, EXTRAPOLATED at this low G — reads low) and Bowring-1972
    (in-range / low-flow-valid; the F2-AOO precedent: where extrapolated W-3
    falsely fails, the valid-range verdict rests on Bowring).
  - PCT / fuel centreline: thermal_stack (DB film + radial conduction + Jens-Lottes).
  - Density-wave margin: stability_map (Ishii-Zuber screen) at the state's power.

CAVEAT: the symmetric chopped cosine approximates the true MOC/EOC axial shape at
equal F_z. The rigorous refinement feeds the OpenMC axial q'(z) directly:
`python3 tools/mdnbr.py --csv <z,q'',Tbulk file>` (export from the notebook).

Run:  python3 tools/cycle_mdnbr.py           # cycle table at nominal flow
      python3 tools/cycle_mdnbr.py --aoo     # + the 118 % power / 80 % flow corner
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mdnbr                                     # noqa: E402
import thermal_stack as ts                       # noqa: E402
import aegis_sweep as sw                         # noqa: E402
import stability_map as st                       # noqa: E402

G_CANON = 542.0        # canonical natcirc-delivered flow (H_tc 4 m)
T_IN = 531.15

# Cycle-record peaking (F_dH incl. x1.03 eng. allowance; F_q = F_dH*F_z)
STATES = [
    # label                     F_dH   F_z
    ("BOC   0.0 GWd/t",         1.513, 1.280),
    ("MOC  13.5 GWd/t (hump)",  1.729, 1.408),
    ("EOC  30.8 GWd/t",         1.497, 1.417),
    ("MOC ENVELOPE (closure)",  1.750, 1.410),   # record spec F_dH 1.75 / F_z 1.41 -> F_q 2.468 = THE binding basis
]


def le_ratio_from_fz(fz):
    """Solve F_z = a/sin(a) for a (a = pi*L/(2*Le)) -> Le/L = pi/(2a). Bisection."""
    lo, hi = 1e-6, math.pi / 2 - 1e-9
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid / math.sin(mid) < fz:
            lo = mid
        else:
            hi = mid
    a = 0.5 * (lo + hi)
    return math.pi / (2.0 * a)


def minima(cfg, prof):
    """(MDNBR_W3, MDNBR_Bowring, z_min_bowring) over a hot-channel profile."""
    dHsub = cfg.cp * (prof["Tsat"] - cfg.T_in)
    w3, bow, zb = float("inf"), float("inf"), 0.0
    for i in range(len(prof["z"])):
        F, _ = mdnbr.tong_F(cfg, prof, i)
        w3 = min(w3, (mdnbr.w3_chf_eu(cfg, prof["xq"][i], dHsub) / F) / prof["qpp"][i])
        b = mdnbr.bowring_chf(cfg, prof, i, dHsub) / prof["qpp"][i]
        if b < bow:
            bow, zb = b, prof["z"][i]
    return w3, bow, zb


def load_shapes(path):
    """Record CSV: z_cm, relpow_BOC, relpow_MOC, relpow_EOC (bin centers, mean = 1)."""
    import csv
    zs, cols, names = [], {}, []
    with open(path) as fh:
        for row in csv.reader(fh):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if not names:
                names = row[1:]
                cols = {n: [] for n in names}
                continue
            zs.append(float(row[0]))
            for n, v in zip(names, row[1:]):
                cols[n].append(float(v))
    return zs, cols


def profile_from_shape(cfg, z_cm, rel, f_dh):
    """Hot-channel profile from the OpenMC axial tally (piecewise-constant bins,
    exactly conserving the tally normalisation -> F_dH), mdnbr-profile dict."""
    Tsat, hfg = mdnbr.sat_props(cfg.p_mpa)
    mdot = cfg.G * cfg.A_flow
    dz = cfg.L / cfg.n
    zb = [(zc + 100.0) / 100.0 for zc in z_cm]          # bin centres, m from inlet
    qp_avg_hot = sw.QP_AVG * f_dh
    z, qprime, qpp, Tb, xq = [], [], [], [], []
    T = cfg.T_in
    for i in range(cfg.n):
        zi = (i + 0.5) * dz
        k = min(range(len(zb)), key=lambda j: abs(zb[j] - zi))
        qp = qp_avg_hot * rel[k]
        T += qp * dz / (mdot * cfg.cp)                   # 1-phi-equivalent (uncapped)
        z.append(zi); qprime.append(qp); qpp.append(qp / (math.pi * cfg.D_co))
        Tb.append(T); xq.append(cfg.cp * (T - Tsat) / hfg)
    return dict(z=z, dz=dz, qprime=qprime, qpp=qpp, Tbulk=Tb, xq=xq,
                Tsat=Tsat, hfg=hfg, mdot=mdot, qp_avg=qp_avg_hot)


def state_case(f_dh, f_z, G, T_in=T_IN, power_mult=1.0):
    f_q = f_dh * f_z
    qpeak = sw.QP_AVG * f_q * power_mult
    cfg = mdnbr.Config(p_mpa=sw.P_MPA, T_in=T_in, G=G, cp=sw.CP, L=sw.L,
                       D_co=sw.D_CO, D_h=sw.D_H, A_flow=sw.A_F,
                       qp_hot_peak=qpeak, Fz=f_z,
                       Le_ratio=le_ratio_from_fz(f_z), n=200)
    prof = mdnbr.build_profile(cfg)
    w3, bow, _ = minima(cfg, prof)
    stc = ts.StackConfig(r_f=sw.R_F, r_ci=sw.R_CI, r_co=sw.R_CO, k_fuel=sw.K_FUEL,
                         k_clad=sw.K_CLAD, h_gap=sw.H_GAP, mu=sw.MU, k_w=sw.KW,
                         Pr=sw.PR, corr="db")
    h, _, _, _ = ts.film_h(cfg, stc)
    rows, _, _ = ts.stack(cfg, stc, ts.build_profile(cfg), h, boiling=True)
    pct = max(r[3] for r in rows) - 273.15
    fuel = max(r[5] for r in rows) - 273.15
    # DWO margin (Ishii-Zuber screen) at this state's hot-channel power AND shape
    ch = st.channel_numbers(G, T_in, q_mult=qpeak / sw.QP_PEAK,
                            fz=f_z, le_ratio=le_ratio_from_fz(f_z))
    rhs, _, _, _ = st.boundary_rhs(G)
    lhs = ch["n_pch"] - ch["n_sub"]
    dwo = rhs / lhs if lhs > 0 else float("inf")
    return dict(f_q=f_q, f_dh=f_dh, f_z=f_z, qpeak=qpeak, w3=w3, bow=bow,
                pct=pct, fuel=fuel, x_exit=prof["xq"][-1], dwo=dwo)


def table(title, G, power_mult=1.0, T_in=T_IN):
    print("-" * 100)
    print(f" {title}")
    print("-" * 100)
    print(f" {'state':<26}{'F_q':>6}{'F_dH':>6}{'F_z':>6} {'q`pk kW/m':>9}"
          f" {'x_exit':>7} {'W-3*':>6} {'Bowring':>8} {'PCT C':>6} {'fuel C':>7} {'DWO':>6}")
    for label, f_dh, f_z in STATES:
        r = state_case(f_dh, f_z, G, T_in, power_mult)
        dwo = f"x{r['dwo']:.1f}" if math.isfinite(r["dwo"]) else "1-phi"
        flag = "PASS" if r["bow"] >= 1.30 else "FAIL"
        w3flag = "" if r["w3"] >= 1.30 else " (<1.3 extrap)"
        print(f" {label:<26}{r['f_q']:>6.3f}{r['f_dh']:>6.3f}{r['f_z']:>6.3f}"
              f"{r['qpeak']/1e3:>10.2f} {r['x_exit']*100:>6.1f}% {r['w3']:>6.2f} "
              f"{r['bow']:>8.2f} {r['pct']:>6.0f} {r['fuel']:>7.0f} {dwo:>6}"
              f"  {flag}{w3flag}")


SHAPES_CSV = os.path.join(HERE, "data", "axial_profile_BOC_MOC_EOC.csv")
SHAPE_COL = {  # state label prefix -> (csv column, F_dH)
    "BOC": ("relpow_BOC", 1.513),
    "MOC ": ("relpow_MOC", 1.729),   # trailing space: matches "MOC  13.5", not the envelope
    "EOC": ("relpow_EOC", 1.497),
    "MOC ENVELOPE": ("relpow_MOC", 1.750),
}


def shapes_table(path, G, T_in=T_IN):
    z_cm, cols = load_shapes(path)
    print("-" * 100)
    print(f" REAL AXIAL SHAPES (record tally, {len(z_cm)} bins) vs chopped cosine — {os.path.basename(path)}")
    print("-" * 100)
    print(f" {'state':<26}{'F_z':>6}{'F_q':>7} {'x_exit':>7} "
          f"{'W-3 cos':>8}{'W-3 real':>9} {'Bow cos':>8}{'Bow real':>9}  {'z_min':>5}")
    for label, (col, f_dh) in (("BOC   0.0 GWd/t", SHAPE_COL["BOC"]),
                               ("MOC  13.5 GWd/t (hump)", SHAPE_COL["MOC "]),
                               ("EOC  30.8 GWd/t", SHAPE_COL["EOC"]),
                               ("MOC ENVELOPE (closure)", SHAPE_COL["MOC ENVELOPE"])):
        rel = cols[col]
        f_z = max(rel)
        f_q = f_dh * f_z
        cfg = mdnbr.Config(p_mpa=sw.P_MPA, T_in=T_in, G=G, cp=sw.CP, L=sw.L,
                           D_co=sw.D_CO, D_h=sw.D_H, A_flow=sw.A_F,
                           qp_hot_peak=sw.QP_AVG * f_q, Fz=f_z,
                           Le_ratio=le_ratio_from_fz(f_z), n=200)
        w3c, bowc, _ = minima(cfg, mdnbr.build_profile(cfg))
        prof = profile_from_shape(cfg, z_cm, rel, f_dh)
        w3r, bowr, zbr = minima(cfg, prof)
        flag = "PASS" if min(bowr, bowc) >= 1.30 else "FAIL"
        print(f" {label:<26}{f_z:>6.3f}{f_q:>7.3f} {prof['xq'][-1]*100:>6.1f}% "
              f"{w3c:>8.2f}{w3r:>9.2f} {bowc:>8.2f}{bowr:>9.2f}  {zbr:>5.2f}  {flag}")
    print(" (cos = chopped cosine at the same F_z; real = piecewise-constant record tally;")
    print("  W-3 minima sit low in the channel where it is extrapolated -> compare trends, not absolutes)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Aegis-40 BOC/MOC/EOC cycle MDNBR (cycle record)")
    ap.add_argument("--G", type=float, default=G_CANON, help="core mass flux kg/m2s")
    ap.add_argument("--aoo", action="store_true", help="add the 118%%P / 80%%G AOO corner table")
    ap.add_argument("--shapes", nargs="?", const=SHAPES_CSV, default=None,
                    help=f"real-axial-shape comparison table (default CSV: {SHAPES_CSV})")
    a = ap.parse_args(argv)

    print("=" * 100)
    print(" Aegis-40 CYCLE MDNBR — cycle-record peaking (BOC/MOC/EOC)  "
          f"[G {a.G:.0f} kg/m2s, T_in 258 C, 12.8 MPa]")
    print("=" * 100)
    print(" * W-3 is EXTRAPOLATED at G 542 (range starts 1356) -> conservative-low; the")
    print("   in-range verdict is Bowring-1972 (F2-AOO precedent). Acceptance: MDNBR >= 1.30.")
    table("Nominal (natural-circulation design flow)", a.G)
    if a.aoo:
        table("AOO corner: 118 % power / 80 % flow (quasi-steady bounding)",
              a.G * 0.80, power_mult=1.18)
    if a.shapes:
        shapes_table(a.shapes, a.G)
    print("-" * 100)
    print(" NOTE: chopped cosine at the record F_z; rigorous shape check = OpenMC axial")
    print("       profile via `mdnbr.py --csv`. Geometry/power unchanged -> CFD basis stands;")
    print("       a CFD re-run at the MOC envelope is linear-in-power scaling (optional).")
    print("=" * 100)


if __name__ == "__main__":
    main()
