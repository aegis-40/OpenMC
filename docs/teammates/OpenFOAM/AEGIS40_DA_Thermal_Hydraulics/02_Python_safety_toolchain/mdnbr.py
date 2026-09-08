#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 - MDNBR (Minimum Departure-from-Nucleate-Boiling Ratio) post-processor
============================================================================

Computes the hot-channel DNBR axial profile and its minimum (MDNBR) for the
Aegis-40 fuel pin, using the W-3 (Westinghouse-3 / Tong) critical-heat-flux
correlation with the Tong non-uniform axial-flux F-factor.

MDNBR is the primary thermal-safety metric (target > 1.3). It is NOT a native
OpenFOAM output: OpenFOAM gives the local wall heat flux q'' and the local
coolant state; this tool turns those into a CHF margin via a CHF correlation.

Two ways to supply the local conditions along the hot channel:

  (A) ANALYTIC (default) - build q'(z) as a chopped-cosine axial power shape
      from the hot-pin peak linear power, and get the coolant bulk T(z) from a
      1-D energy balance. Self-contained; no OpenFOAM run needed. Good for the
      design-point MDNBR number and for sensitivity studies.

  (B) FROM OPENFOAM - read an axial CSV (columns: x[m], qpp[W/m2], Tbulk[K])
      sampled from the chtMultiRegionFoam coolant_to_clad patch. Use
      --csv <file>. Then the *actual* simulated heat flux & coolant T drive
      the DNBR. (Requires the axial heat-source cosine to be active in the run
      for a physically meaningful MDNBR location.)

All inputs default to the Aegis-40 design point (OpenMC-consistent). Override
any of them on the command line: run with -h.

W-3 validity (check before trusting the number):
  P  6.9-15.9 MPa | G 1356-6800 kg/m2s | x -0.15..0.15 |
  De 5-18 mm | heated length 0.25-3.7 m
References: L.S. Tong, "Boiling Crisis and Critical Heat Flux" (1972);
Todreas & Kazimi, "Nuclear Systems I", W-3 form & Tong F-factor.
"""

import argparse
import math
import sys
from dataclasses import dataclass

# --------------------------------------------------------------------------
# Unit conversions (SI <-> British, since W-3 is defined in British units)
# --------------------------------------------------------------------------
PA_PER_PSI      = 6894.757
G_SI_TO_BRIT    = 737.343          # (kg/m2 s) -> (lb/hr ft2)
M_TO_INCH       = 1.0 / 0.0254
J_PER_KG_TO_BTU_LB = 1.0 / 2326.0  # (J/kg) -> (BTU/lb)
BTUHRFT2_TO_WM2 = 3.154591         # (BTU/hr ft2) -> (W/m2)


# --------------------------------------------------------------------------
# Saturation water properties (interpolated from steam tables, 10-14 MPa)
# Used to get T_sat, h_fg for the thermodynamic quality. Liquid Cp is taken
# from the case (hConst) so it is consistent with the OpenFOAM thermo model.
# --------------------------------------------------------------------------
# (P[MPa], Tsat[K], hf[kJ/kg], hfg[kJ/kg])
_SAT_TABLE = [
    (10.0, 584.15, 1407.9, 1317.1),
    (12.0, 597.83, 1491.3, 1193.6),
    (13.0, 604.07, 1531.5, 1130.8),
    (14.0, 609.82, 1570.9, 1066.5),
    (15.0, 615.31, 1610.5, 1000.5),
]


def sat_props(p_mpa):
    """Linear-interpolate (Tsat[K], hfg[J/kg]) at pressure p_mpa."""
    t = _SAT_TABLE
    if p_mpa <= t[0][0]:
        a = t[0]
        return a[1], a[3] * 1e3
    if p_mpa >= t[-1][0]:
        a = t[-1]
        return a[1], a[3] * 1e3
    for (p0, ts0, hf0, hfg0), (p1, ts1, hf1, hfg1) in zip(t, t[1:]):
        if p0 <= p_mpa <= p1:
            f = (p_mpa - p0) / (p1 - p0)
            tsat = ts0 + f * (ts1 - ts0)
            hfg = (hfg0 + f * (hfg1 - hfg0)) * 1e3
            return tsat, hfg
    raise RuntimeError("interpolation failed")


# --------------------------------------------------------------------------
# Configuration (defaults matching the OpenFOAM case)
# --------------------------------------------------------------------------
@dataclass
class Config:
    # Defaults = Aegis-40 FER design point, OpenMC-consistent (aegis40_neutronics_FER.ipynb)
    # so a bare `mdnbr.py` run reproduces the design case. aegis_sweep/aoo override per-point.
    # Operating point
    p_mpa: float       = 12.8        # system pressure [MPa]                  (OpenMC)
    T_in: float        = 531.15      # coolant inlet T [K] (258 C; T_avg 556 - dT/2)
    G: float           = 542.0       # core mass flux [kg/m2 s] (as-delivered natcirc, H_tc 4 m = the binding base)
    # Coolant thermophysics @ 283 C / 12.8 MPa (= design basis / aegis_sweep)
    cp: float          = 5350.0      # liquid Cp [J/kg K]
    # Geometry (derived from OpenMC: clad OD 2*0.476cm; A_f=pitch^2-piD^2/4)
    L: float           = 2.0         # active heated length [m]               (OpenMC 200 cm)
    D_co: float        = 9.52e-3     # clad outer diameter (heated perimeter) [m]
    D_h: float         = 11.79e-3    # subchannel hydraulic diameter [m]
    A_flow: float      = 88.2e-6     # subchannel flow area [m2]
    # Hot-channel power — COLR design envelope (q'_avg 6.398 * F_q 2.4675;
    # MOC Gd-hump envelope F_dH 1.75 x F_z 1.41. Bare run = the binding case.)
    qp_hot_peak: float = 15788.0     # hot-pin PEAK linear power q'_max [W/m]
    Fz: float          = 1.410       # axial peaking F_z (MOC COLR envelope)
    Le_ratio: float    = 1.13334     # Le 2.2667 / L 2.0 -> F_z 1.410
    # Numerics
    n: int             = 200         # axial nodes


# --------------------------------------------------------------------------
# Axial power shape: chopped cosine
#   q'(z) = qp_avg * Fz * cos( pi*(z - L/2) / Le )
# normalised so that the axial average over [0,L] equals qp_avg.
# --------------------------------------------------------------------------
def axial_qprime(cfg, z):
    qp_avg = cfg.qp_hot_peak / cfg.Fz
    Le = cfg.L * cfg.Le_ratio
    shape = math.cos(math.pi * (z - cfg.L / 2.0) / Le)
    # renormalise the peak so the *mesh-average* of Fz*cos == Fz*<cos>;
    # for Le=L, <cos> over [0,L] = 2/pi, so true peak/avg = pi/2 ~ 1.571.
    # We instead scale the cosine so its own mean is 1, then multiply by qp_avg*Fz_eff.
    return qp_avg, shape, Le


def build_profile(cfg):
    """Return dict with axial arrays z, qprime, qpp, Tbulk, x_quality."""
    n = cfg.n
    z = [cfg.L * (i + 0.5) / n for i in range(n)]   # cell-centred
    dz = cfg.L / n
    Le = cfg.L * cfg.Le_ratio

    # raw cosine shape and its discrete mean over the active length
    raw = [math.cos(math.pi * (zz - cfg.L / 2.0) / Le) for zz in z]
    mean_raw = sum(raw) / n
    qp_avg = cfg.qp_hot_peak / cfg.Fz
    # scale so that mean(qprime) == qp_avg and peak == qp_avg*Fz
    qprime = [qp_avg * (r / mean_raw) for r in raw]

    # wall heat flux q'' = q' / (pi * D_co)
    perim = math.pi * cfg.D_co
    qpp = [q / perim for q in qprime]

    # coolant bulk enthalpy by 1-D energy balance up the channel, with a TWO-PHASE
    # cap (F1-ii): while subcooled the bulk T rises; once the bulk enthalpy reaches
    # saturation the *physical* bulk T is clamped at Tsat and the surplus becomes
    # equilibrium quality  x_e = cp*(T_sp - Tsat)/hfg  (T_sp = single-phase-equiv. T).
    # The CHF correlations use x_e (not the bulk T), so DNBR is unchanged by the cap.
    mdot = cfg.G * cfg.A_flow                       # [kg/s]
    Tbulk = []; xq = []
    Tsat, hfg = sat_props(cfg.p_mpa)
    cumQ = 0.0
    for q in qprime:
        cumQ += q * dz                              # W added up to this node
        Tsp = cfg.T_in + cumQ / (mdot * cfg.cp)     # single-phase-equivalent T
        Tbulk.append(min(Tsp, Tsat))                # physical bulk T (capped at Tsat)
        xq.append(cfg.cp * (Tsp - Tsat) / hfg)      # equilibrium quality (subcooled<0)
    return dict(z=z, dz=dz, qprime=qprime, qpp=qpp, Tbulk=Tbulk, xq=xq,
                Tsat=Tsat, hfg=hfg, mdot=mdot, qp_avg=qp_avg)


# --------------------------------------------------------------------------
# W-3 critical heat flux (uniform / equivalent-uniform), British units in,
# W/m2 out. X = local thermodynamic quality, dHsub_in = (hf - h_inlet) [J/kg].
# --------------------------------------------------------------------------
def w3_chf_eu(cfg, X, dHsub_in_J):
    P  = cfg.p_mpa * 1e6 / PA_PER_PSI               # psia
    G6 = cfg.G * G_SI_TO_BRIT / 1e6                 # Mlb/hr-ft2
    De = cfg.D_h * M_TO_INCH                        # inch
    dHsub = dHsub_in_J * J_PER_KG_TO_BTU_LB         # BTU/lb

    term_p   = ((2.022 - 0.0004302 * P)
                + (0.1722 - 0.0000984 * P)
                * math.exp((18.177 - 0.004129 * P) * X))
    term_g   = ((0.1484 - 1.596 * X + 0.1729 * X * abs(X)) * G6 + 1.037)
    term_x   = (1.157 - 0.869 * X)
    term_de  = (0.2664 + 0.8357 * math.exp(-3.151 * De))
    term_sub = (0.8258 + 0.000794 * dHsub)

    q_eu_brit = term_p * term_g * term_x * term_de * term_sub * 1.0e6  # BTU/hr-ft2
    return q_eu_brit * BTUHRFT2_TO_WM2              # W/m2


# --------------------------------------------------------------------------
# Tong non-uniform axial-flux correction factor F (per axial location).
#   q''_DNB(nonuniform) = q''_DNB,EU / F
#   C [1/inch] = 0.44 (1 - X_loc)^7.9 / G6^1.72
#   F = C/(q''_loc (1-e^{-C l})) * INT_0^l q''(l') e^{-C(l-l')} dl'
# l measured from start of heated length, in inches.
# --------------------------------------------------------------------------
def tong_F(cfg, prof, i):
    G6 = cfg.G * G_SI_TO_BRIT / 1e6
    Xl = prof['xq'][i]
    C = 0.44 * (1.0 - Xl) ** 7.9 / (G6 ** 1.72)     # 1/inch
    z = prof['z']; qpp = prof['qpp']; dz = prof['dz']
    l_dnb = z[i] * M_TO_INCH
    q_loc = qpp[i]
    integ = 0.0
    for j in range(i + 1):
        lj = z[j] * M_TO_INCH
        integ += qpp[j] * math.exp(-C * (l_dnb - lj)) * (dz * M_TO_INCH)
    denom = q_loc * (1.0 - math.exp(-C * l_dnb))
    if denom <= 0:
        return 1.0, C
    F = C / denom * integ
    # F is bounded ~[0.5, 1.5]; guard pathological ends
    return max(F, 1e-3), C


# --------------------------------------------------------------------------
# Bowring (1972) CHF correlation -- VALID AT LOW MASS FLUX, unlike W-3.
#   Range: P 2-190 bar, G 50-4000 kg/m2s, D 2-45 mm  =>  covers Aegis (G~543).
#   SI inlet / boiling-length form (Todreas & Kazimi, "Nuclear Systems I"):
#       q"_cr(Z) = [A + (D_h*G/4)*dHsub_in] / (C + Z)               [W/m2]
#   reduced pressure  pr = P[bar]/69 ;  exponent n = 2.0 - 0.5*pr
#   A = 2.317*(h_fg*D*G/4)*F1 / (1 + 0.0143*F2*sqrt(D)*G)
#   C = 0.077*F3*D*G / (1 + 0.347*F4*(G/1356)^n)
#   F1..F4 piecewise in pr.  dHsub_in = h_f,sat - h_in [J/kg], Z from inlet [m].
#   Form/coeffs transcribed from secondary refs -> cross-checked against W-3 in
#   the W-3 validity window (run with --chf-xcheck). Confirm A/C vs Todreas &
#   Kazimi before quoting as the final safety number.
# --------------------------------------------------------------------------
def bowring_F(pr):
    if pr <= 1.0:
        F1 = (pr ** 18.942 * math.exp(20.89 * (1.0 - pr)) + 0.917) / 1.917
        F2 = 1.309 * F1 / (pr ** 1.316 * math.exp(2.444 * (1.0 - pr)) + 0.309)
        F3 = (pr ** 17.023 * math.exp(16.658 * (1.0 - pr)) + 0.667) / 1.667
        F4 = F3 * pr ** 1.649
    else:
        F1 = pr ** (-0.368) * math.exp(0.648 * (1.0 - pr))
        F2 = F1 / (pr ** (-0.448) * math.exp(0.245 * (1.0 - pr)))
        F3 = pr ** 0.219
        F4 = F3 * pr ** 1.649
    return F1, F2, F3, F4


def bowring_chf(cfg, prof, i, dHsub_in_J):
    """Bowring CHF [W/m2] at axial node i (Z measured from channel inlet)."""
    pr   = (cfg.p_mpa * 10.0) / 69.0          # MPa -> bar -> reduced pressure
    G    = cfg.G                               # kg/m2 s
    D    = cfg.D_h                             # m
    hfg  = prof['hfg']                         # J/kg
    Z    = prof['z'][i]                        # m, from inlet
    nexp = 2.0 - 0.5 * pr
    F1, F2, F3, F4 = bowring_F(pr)
    A = 2.317 * (hfg * D * G / 4.0) * F1 / (1.0 + 0.0143 * F2 * math.sqrt(D) * G)
    C = 0.077 * F3 * D * G / (1.0 + 0.347 * F4 * (G / 1356.0) ** nexp)
    return (A + (D * G / 4.0) * dHsub_in_J) / (C + Z)


# --------------------------------------------------------------------------
# CSV ingest (OpenFOAM-sampled hot channel: x[m], qpp[W/m2], Tbulk[K])
# --------------------------------------------------------------------------
def load_csv(path, cfg):
    z, qpp, Tb = [], [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line[0] in '#"' or line.lower().startswith('x'):
                continue
            parts = [p for p in line.replace(',', ' ').split()]
            if len(parts) < 3:
                continue
            z.append(float(parts[0])); qpp.append(float(parts[1]))
            Tb.append(float(parts[2]))
    n = len(z)
    if n < 2:
        sys.exit("CSV must contain >=2 rows of: x[m] qpp[W/m2] Tbulk[K]")
    # uniform dz approximation for the Tong integral
    dz = (z[-1] - z[0]) / (n - 1)
    Tsat, hfg = sat_props(cfg.p_mpa)
    xq = [-cfg.cp * (Tsat - T) / hfg for T in Tb]
    qprime = [q * math.pi * cfg.D_co for q in qpp]
    return dict(z=z, dz=dz, qprime=qprime, qpp=qpp, Tbulk=Tb, xq=xq,
                Tsat=Tsat, hfg=hfg, mdot=cfg.G * cfg.A_flow,
                qp_avg=sum(qprime) / n)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def run(cfg, csv=None, use_tong=True, table=False, chf='w3', lut_path=None):
    prof = load_csv(csv, cfg) if csv else build_profile(cfg)
    Tsat = prof['Tsat']; hfg = prof['hfg']
    # inlet subcooling enthalpy (hf - h_in) using liquid Cp
    dHsub_in = cfg.cp * (Tsat - cfg.T_in)

    lut = None; g_clamped = False
    if chf == 'groeneveld':
        import groeneveld
        from stability_map import sat_rho
        lut = groeneveld.load_lut(lut_path) if lut_path else groeneveld.load_lut()
        rho_f, rho_g = sat_rho(cfg.p_mpa)
        # cumulative wall-flux integral + boiling-onset node for the K5
        # boiling-length-average (IAEA-TECDOC-1203 Tab.3.3: K5=q_loc/q_BLA, x>0)
        g_cumq = []
        _s = 0.0
        for _q in prof['qpp']:
            _s += _q * prof['dz']
            g_cumq.append(_s)
        g_onset = next((j for j, xv in enumerate(prof['xq']) if xv > 0.0), None)

    rows = []
    mdnbr = float('inf'); z_min = None; i_min = None
    for i in range(len(prof['z'])):
        X = prof['xq'][i]
        if chf == 'bowring':
            q_chf = bowring_chf(cfg, prof, i, dHsub_in)
            F = 1.0
        elif chf == 'groeneveld':
            import groeneveld
            q_chf, _K1, clamp = groeneveld.chf_groeneveld(lut, cfg.p_mpa, cfg.G, X, cfg.D_h)
            g_clamped = g_clamped or clamp
            # K4 heated-length (local upstream heated length) + K5 axial-flux
            a_h = groeneveld.alpha_homog(X, rho_f, rho_g)
            K4 = groeneveld.k4_heated_length(cfg.D_h, prof['z'][i], a_h)
            K5 = 1.0
            if X > 0.0 and g_onset is not None and i > g_onset:
                Lb = (i - g_onset) * prof['dz']         # boiling length
                q_bla = (g_cumq[i] - g_cumq[g_onset]) / Lb
                if q_bla > 0.0:
                    # declining-flux memory penalty; >1 credit NOT taken (conservative)
                    K5 = min(prof['qpp'][i] / q_bla, 1.0)
            q_chf *= K4 * K5
            F = K4 * K5                                  # report in the F column
        else:
            q_eu = w3_chf_eu(cfg, X, dHsub_in)
            F, _C = (tong_F(cfg, prof, i) if use_tong else (1.0, 0.0))
            q_chf = q_eu / F
        q_loc = prof['qpp'][i]
        dnbr = q_chf / q_loc if q_loc > 0 else float('inf')
        rows.append((prof['z'][i], prof['Tbulk'][i], X, q_loc, q_chf, F, dnbr))
        if dnbr < mdnbr:
            mdnbr = dnbr; z_min = prof['z'][i]; i_min = i

    # ----- report -----
    print("=" * 72)
    if chf == 'bowring':
        print(" Aegis-40 hot-channel DNBR  (Bowring-1972 CHF, low-flow valid)")
    elif chf == 'groeneveld':
        print(" Aegis-40 hot-channel DNBR  (Groeneveld CHF LUT, K1-dia + K4-length + K5-axial)")
    else:
        print(" Aegis-40 hot-channel DNBR  (W-3 CHF correlation"
              + (", Tong F-factor)" if use_tong else ", uniform)"))
    print("=" * 72)
    print(f" Pressure              : {cfg.p_mpa:8.2f} MPa")
    print(f" Inlet T / Tsat        : {cfg.T_in:8.1f} / {Tsat:6.1f} K"
          f"  (inlet subcooling {Tsat - cfg.T_in:.1f} K)")
    print(f" Mass flux G           : {cfg.G:8.1f} kg/m2s"
          f"   (mdot_ch {prof['mdot']*1e3:.2f} g/s)")
    print(f" Hydraulic dia D_h     : {cfg.D_h*1e3:8.2f} mm")
    print(f" Heated length / D_co  : {cfg.L:8.2f} m / {cfg.D_co*1e3:.2f} mm")
    if not csv:
        print(f" Hot q' peak / avg     : {cfg.qp_hot_peak/1e3:8.2f}"
              f" / {prof['qp_avg']/1e3:.2f} kW/m  (Fz={cfg.Fz})")
        Tout = prof['Tbulk'][-1]
        x_out = prof['xq'][-1]
        if x_out > 0:
            tail = f"   -> SATURATED, exit quality x={x_out*100:.1f}% (two-phase cap)"
        else:
            tail = f"   (subcooled, {Tsat-Tout:.1f} K to Tsat)"
        print(f" Hot-channel outlet T  : {Tout:8.1f} K"
              f"  ({Tout-273.15:.1f} C, rise {Tout-cfg.T_in:.1f} K)" + tail)
    qpp_pk = max(prof['qpp'])
    print(f" Peak wall heat flux   : {qpp_pk/1e6:8.3f} MW/m2")
    # validity flags
    xmax = max(prof['xq']); xmin = min(prof['xq'])
    warn = []
    if chf == 'bowring':
        if not (2.0 <= cfg.p_mpa * 10.0 <= 190.0): warn.append("P out of Bowring range")
        if not (50.0 <= cfg.G <= 4000.0):          warn.append(f"G={cfg.G:.0f} out of Bowring range")
        if not (2e-3 <= cfg.D_h <= 45e-3):         warn.append("D_h out of Bowring range")
    elif chf == 'groeneveld':
        warn.append("K1+K4+K5 per IAEA-TECDOC-1203 Tab.3.3; K2=1 (capped, =1 at x<=0), "
                    "K3 grids NOT credited (conservative), K7/K8=1 (vertical upflow, G>0). "
                    "Corroboration of W-3/Bowring -- binding basis unchanged.")
        if g_clamped: warn.append("(P,G,x) hit a table edge -> clamped to LUT range (check coverage)")
    else:
        if not (6.9 <= cfg.p_mpa <= 15.9): warn.append("P out of W-3 range")
        if not (1356 <= cfg.G <= 6800):    warn.append("G out of W-3 range")
        if xmax > 0.15:                    warn.append(f"x_exit={xmax:.3f} > 0.15")
        if xmin < -0.15:                   warn.append(
            f"x={xmin:.3f} < -0.15 (deeply subcooled: W-3 extrapolated, CHF/DNBR "
            f"likely conservative-high -> read as 'large margin', not exact)")
    print("-" * 72)
    if table:
        print(f"{'z[m]':>7} {'Tb[K]':>7} {'x[-]':>8} "
              f"{'qpp[MW/m2]':>10} {'qCHF[MW/m2]':>12} {'F':>6} {'DNBR':>7}")
        step = max(1, len(rows) // 25)
        for r in rows[::step]:
            print(f"{r[0]:7.3f} {r[1]:7.1f} {r[2]:8.4f} "
                  f"{r[3]/1e6:10.3f} {r[4]/1e6:12.3f} {r[5]:6.3f} {r[6]:7.3f}")
        print("-" * 72)
    print(f" >>> MDNBR = {mdnbr:.3f}  at z = {z_min:.3f} m"
          f"  (Tb={rows[i_min][1]:.1f} K, x={rows[i_min][2]:.4f})")
    target = 1.3
    margin = (mdnbr / target - 1.0) * 100.0
    verdict = "PASS" if mdnbr > target else "FAIL"
    print(f" >>> Limit {target}:  {verdict}   (margin {margin:+.1f}% vs limit)")
    if warn:
        _lbl = {'w3': 'W-3', 'bowring': 'Bowring', 'groeneveld': 'Groeneveld-LUT'}.get(chf, chf)
        print(f" !!! {_lbl} validity warnings: " + "; ".join(warn))
    print("=" * 72)
    return mdnbr, rows


def maybe_write_csv(path, rows):
    with open(path, 'w') as fh:
        fh.write("z_m,Tbulk_K,quality,qpp_Wm2,qCHF_Wm2,Ffactor,DNBR\n")
        for r in rows:
            fh.write(f"{r[0]:.5f},{r[1]:.3f},{r[2]:.5f},{r[3]:.1f},"
                     f"{r[4]:.1f},{r[5]:.4f},{r[6]:.4f}\n")
    print(f" (wrote DNBR profile -> {path})")


def main(argv=None):
    cfg = Config()
    ap = argparse.ArgumentParser(
        description="Aegis-40 MDNBR (W-3 CHF) post-processor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--p',    type=float, default=cfg.p_mpa, help="pressure [MPa]")
    ap.add_argument('--Tin',  type=float, default=cfg.T_in,  help="inlet T [K]")
    ap.add_argument('--G',    type=float, default=cfg.G,     help="mass flux [kg/m2s]")
    ap.add_argument('--cp',   type=float, default=cfg.cp,    help="liquid Cp [J/kgK]")
    ap.add_argument('--L',    type=float, default=cfg.L,     help="heated length [m]")
    ap.add_argument('--Dco',  type=float, default=cfg.D_co,  help="clad OD [m]")
    ap.add_argument('--Dh',   type=float, default=cfg.D_h,   help="hydraulic dia [m]")
    ap.add_argument('--Aflow',type=float, default=cfg.A_flow,help="flow area [m2]")
    ap.add_argument('--qpeak',type=float, default=cfg.qp_hot_peak,
                    help="hot-pin PEAK linear power [W/m]")
    ap.add_argument('--Fz',   type=float, default=cfg.Fz,    help="axial peaking")
    ap.add_argument('--Le',   type=float, default=cfg.Le_ratio,
                    help="extrapolated/active length ratio (1.0 full cosine, 1.2 chopped)")
    ap.add_argument('--n',    type=int,   default=cfg.n,     help="axial nodes")
    ap.add_argument('--csv',  type=str,   default=None,
                    help="OpenFOAM axial CSV: x[m] qpp[W/m2] Tbulk[K]")
    ap.add_argument('--no-tong', action='store_true', help="disable Tong F-factor")
    ap.add_argument('--chf', choices=['w3', 'bowring', 'groeneveld'], default='w3',
                    help="CHF: w3 (default) | bowring (low-flow) | groeneveld (2006 LUT, authoritative)")
    ap.add_argument('--lut', type=str, default=None,
                    help="path to Groeneveld LUT CSV (default tools/data/groeneveld_2006_lut.csv)")
    ap.add_argument('--table', action='store_true', help="print axial table")
    ap.add_argument('--out',  type=str,   default=None, help="write DNBR profile CSV")
    a = ap.parse_args(argv)

    cfg = Config(p_mpa=a.p, T_in=a.Tin, G=a.G, cp=a.cp, L=a.L, D_co=a.Dco,
                 D_h=a.Dh, A_flow=a.Aflow, qp_hot_peak=a.qpeak, Fz=a.Fz,
                 Le_ratio=a.Le, n=a.n)
    _, rows = run(cfg, csv=a.csv, use_tong=not a.no_tong, table=a.table,
                  chf=a.chf, lut_path=a.lut)
    if a.out:
        maybe_write_csv(a.out, rows)


if __name__ == "__main__":
    main()
