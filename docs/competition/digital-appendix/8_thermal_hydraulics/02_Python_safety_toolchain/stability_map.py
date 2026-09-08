#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 natural-circulation FLOW-STABILITY screening (correlation-level).

Two classic checks at the
operating pressure (12.8 MPa), in the same correlation-stack spirit as
mdnbr.py / natcirc.py — a SCREEN, not a frequency-domain or system code.

1) LEDINEGG (excursive / static, loop frame). Stable if
       d(dp_demand)/dG - d(dp_supply)/dG > 0     at the operating point.
   For this loop: dp_loss ~ G^2 (demand) while the buoyancy head at fixed
   power ~ dT ~ 1/G (supply), so at the balance point the net slope is
       d(dp_loss - dp_buoy)/dG = (2*dp + dp)/G = 3*dp/G  > 0   — always.
   Single monotone intersection => excursion-stable by construction.

2) DENSITY-WAVE oscillations (DWO), parallel-channel frame (9 768 channels
   between common plena = the classic fixed-dp core case). Ishii–Zuber
   simplified criterion (HEM, uniformly heated, high-subcooling form):
       N_pch - N_sub  <  2*(K_in + LAM + K_ex) / (1 + 0.5*(LAM + 2*K_ex))
   with
       N_pch = Q_ch/(mdot*hfg) * (drho/rho_g)     (phase-change / Zuber no.)
       N_sub = dh_sub/hfg      * (drho/rho_g)     (subcooling number)
       LAM   = f*L/(2*D_h)                        (friction number)
   and identically  N_pch - N_sub = x_exit * (drho/rho_g)  (equilibrium exit
   quality — taken straight from mdnbr.build_profile, scheme-consistent).
   Refs: Ishii & Zuber (1970); Ishii ANL-thesis simple criterion; Todreas &
   Kazimi, *Nuclear Systems II*; Kakac & Bon, IJHMT 51 (2008) review.

Conservative screening choices (all push TOWARD instability):
 - K_in = core-inlet contraction only (0.441, b2_loss_budget.py) — omits the
   stabilizing spacer-grid and lower-internals restrictions;
 - LAM from the single-phase friction factor (a two-phase multiplier or grid
   friction would raise the boundary at high N_sub — stabilizing);
 - hot channel (F_dH 1.583). Average channels never reach saturation
   (x_exit < 0) => cannot sustain DWO at all.

SCOPE: at-pressure operation (design point + AOO corners). LOW-PRESSURE
START-UP (flashing / geysering class) is excluded by procedure — pressurize
before power ascension (NuScale-style heat-up) — and is flagged for the FER
start-up paragraph, not for this screen. Loop-mode (whole-circuit) DWO needs
a system code and is a licensing-stage item.

Run:  python3 tools/stability_map.py
      python3 tools/stability_map.py --png docs/figs/F10_stability_map.png
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mdnbr                                    # noqa: E402  sat_props, build_profile
import aegis_sweep as sw                        # noqa: E402  OpenMC-consistent constants

# ---------------------------------------------------------------- saturation ρ
# IAPWS-IF97 saturated densities on the same pressure grid as mdnbr._SAT_TABLE.
# (P[MPa], rho_f[kg/m3], rho_g[kg/m3])
_RHOSAT = [
    (10.0, 688.4, 55.46),
    (12.0, 654.9, 70.11),
    (13.0, 638.1, 78.24),
    (14.0, 620.9, 87.05),
    (15.0, 603.2, 96.71),
]


def sat_rho(p_mpa):
    """Linear-interpolate (rho_f, rho_g) at pressure p_mpa (same style as mdnbr.sat_props)."""
    t = _RHOSAT
    if p_mpa <= t[0][0]:
        return t[0][1], t[0][2]
    if p_mpa >= t[-1][0]:
        return t[-1][1], t[-1][2]
    for (p0, rf0, rg0), (p1, rf1, rg1) in zip(t, t[1:]):
        if p0 <= p_mpa <= p1:
            f = (p_mpa - p0) / (p1 - p0)
            return rf0 + f * (rf1 - rf0), rg0 + f * (rg1 - rg0)
    raise RuntimeError("interpolation failed")


# ------------------------------------------------------------------- criterion
K_IN = 0.441      # core-inlet contraction, channel-referenced (b2_loss_budget.py)
K_EX = 0.036      # core-exit expansion                        (b2_loss_budget.py)
GRID_K = 4.0      # 5 spacer grids x zeta~0.8, distributed -> added to LAM when credited
G_DESIGN = 542.0  # as-delivered natural-circulation flow (H_tc 4 m) — the canonical base


def friction_number(G):
    """LAM = f*L/(2*D_h) with the single-phase McAdams f (Darcy)."""
    Re = G * sw.D_H / sw.MU
    f = 0.184 * Re ** -0.2
    return f * sw.L / (2.0 * sw.D_H), f, Re


def boundary_rhs(G, K_in=K_IN, K_ex=K_EX, grids_K=0.0):
    lam, f, Re = friction_number(G)
    lam += grids_K
    rhs = 2.0 * (K_in + lam + K_ex) / (1.0 + 0.5 * (lam + 2.0 * K_ex))
    return rhs, lam, f, Re


def channel_numbers(G, T_in, q_mult=1.0, fz=None, le_ratio=None):
    """N_sub, N_pch (and x_exit) for a hot-type channel at (G, T_in, q_mult·q_peak).

    Uses mdnbr.build_profile so the exit quality is bit-identical to the DNBR
    tools (equilibrium x from the cp-enthalpy balance, F1-ii convention).
    fz/le_ratio override the sweep axial shape (per-cycle-state screening).
    """
    cfg = mdnbr.Config(p_mpa=sw.P_MPA, T_in=T_in, G=G, cp=sw.CP, L=sw.L,
                       D_co=sw.D_CO, D_h=sw.D_H, A_flow=sw.A_F,
                       qp_hot_peak=sw.QP_PEAK * q_mult,
                       Fz=fz if fz is not None else sw.F_Z,
                       Le_ratio=le_ratio if le_ratio is not None else sw.LE_RATIO, n=200)
    prof = mdnbr.build_profile(cfg)
    rho_f, rho_g = sat_rho(sw.P_MPA)
    R = (rho_f - rho_g) / rho_g
    n_sub = sw.CP * (prof["Tsat"] - T_in) / prof["hfg"] * R
    x_exit = prof["xq"][-1]
    n_pch = n_sub + x_exit * R
    return dict(n_sub=n_sub, n_pch=n_pch, x_exit=x_exit, R=R,
                Tsat=prof["Tsat"], hfg=prof["hfg"])


CASES = [
    # label                        G-mult  dTin[K]  q-mult
    ("design hot channel",          1.00,    0.0,   1.00),
    ("AOO bounding 118%P / 80%G",   0.80,    0.0,   1.18),
    ("AOO corner +10 K inlet",      0.80,   10.0,   1.18),
    ("core-average channel",        1.00,    0.0,   1.0 / sw.F_DH),
]


def evaluate(K_in=K_IN, K_ex=K_EX):
    rows = []
    for label, gm, dt, qm in CASES:
        G = G_DESIGN * gm
        ch = channel_numbers(G, 531.15 + dt, qm)
        rhs, lam, f, Re = boundary_rhs(G, K_in, K_ex)
        rhs_g, _, _, _ = boundary_rhs(G, K_in, K_ex, grids_K=GRID_K)
        lhs = ch["n_pch"] - ch["n_sub"]
        if lhs <= 0.0:
            verdict, ratio, ratio_g = "no boiling -> DWO N/A", float("inf"), float("inf")
        else:
            ratio, ratio_g = rhs / lhs, rhs_g / lhs
            verdict = "STABLE" if lhs < rhs else ("STABLE w/ grids" if lhs < rhs_g else "UNSTABLE")
        rows.append(dict(label=label, G=G, lam=lam, rhs=rhs, rhs_g=rhs_g, lhs=lhs,
                         ratio=ratio, ratio_g=ratio_g, verdict=verdict, **ch))
    return rows


# ------------------------------------------------------------------- reporting
def main(argv=None):
    ap = argparse.ArgumentParser(description="Aegis-40 flow-stability screening")
    ap.add_argument("--Kin", type=float, default=K_IN, help="inlet restriction K (channel-ref)")
    ap.add_argument("--Kex", type=float, default=K_EX, help="exit restriction K (channel-ref)")
    ap.add_argument("--png", help="also write the N_sub-N_pch stability map (matplotlib)")
    a = ap.parse_args(argv)

    rows = evaluate(a.Kin, a.Kex)
    d = rows[0]
    rho_f, rho_g = sat_rho(sw.P_MPA)

    bar = "=" * 78
    print(bar)
    print(" Aegis-40 FLOW-STABILITY SCREEN  (Ledinegg + Ishii-Zuber DWO, 12.8 MPa)")
    print(bar)
    print(f" sat props: Tsat {d['Tsat']:.1f} K, hfg {d['hfg']/1e3:.0f} kJ/kg, "
          f"rho_f/rho_g {rho_f:.0f}/{rho_g:.1f}  ->  drho/rho_g = {d['R']:.2f}")
    print(f" channel: L {sw.L} m, D_h {sw.D_H*1e3:.2f} mm; K_in {a.Kin} / K_ex {a.Kex} "
          f"(b2 loss budget; grids NOT credited -> conservative)")
    print("-" * 78)
    print(" 1) LEDINEGG (loop, excursive): demand ~ G^2 rises, buoyancy supply ~ 1/G")
    dp_buoy = sw.RHO * sw.BETA * 9.81 * 50.0 * 4.0        # rho*beta*g*dT*H_tc (design)
    print(f"    falls -> net slope 3*dp/G = {3.0*dp_buoy/G_DESIGN:+.1f} Pa/(kg/m2s) > 0"
          f"  (dp_buoy {dp_buoy:.0f} Pa, H_tc 4 m)")
    print("    => single monotone operating point: excursion-STABLE by construction.")
    print("-" * 78)
    print(" 2) DENSITY-WAVE (Ishii-Zuber simplified, parallel-channel, HEM):")
    print(f"    {'case':<28}{'G':>5}  {'N_sub':>6} {'N_pch':>6} {'x_exit':>7} "
          f"{'LHS':>6} {'RHS':>6} {'margin':>7} {'w/grids':>8}  verdict")
    for r in rows:
        m = f"x{r['ratio']:.2f}" if math.isfinite(r["ratio"]) else "    --"
        mg = f"x{r['ratio_g']:.2f}" if math.isfinite(r["ratio_g"]) else "    --"
        print(f"    {r['label']:<28}{r['G']:>5.0f}  {r['n_sub']:>6.2f} {r['n_pch']:>6.2f} "
              f"{r['x_exit']*100:>6.1f}% {r['lhs']:>6.2f} {r['rhs']:>6.2f} {m:>7} {mg:>8}  {r['verdict']}")
    print(f"    (w/grids = {GRID_K:.0f} added to LAM: 5 spacer grids x zeta~0.8, distributed —")
    print("     the base screen credits NO grids = deliberately conservative)")
    print("-" * 78)
    hot, aoo = rows[0], rows[1]
    print(f" VERDICT: design point {hot['ratio']:.1f}x inside the DWO boundary; bounding AOO")
    print(f"          corner {aoo['ratio']:.2f}x no-grid / {aoo['ratio_g']:.2f}x with grid credit.")
    print("          Average channels stay subcooled (x_exit < 0) -> no DWO mode.")
    print("          Ledinegg stable at all points.")
    print(" SCOPE:   at-pressure only. Low-P start-up = procedure (pressurize before")
    print("          power, NuScale-style); loop-mode DWO / frequency-domain check =")
    print("          licensing-stage refinement (system code).")
    print(bar)

    if a.png:
        plot_map(rows, a.png, a.Kin, a.Kex)


def plot_map(rows, path, K_in, K_ex):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    NAVY, RED, GREEN, ORANGE, GREY = "#1f4e79", "#c0392b", "#2e7d32", "#e08a1e", "#888888"
    plt.rcParams.update({"figure.dpi": 160, "savefig.dpi": 160, "font.size": 11,
                         "axes.titlesize": 12, "axes.titleweight": "bold",
                         "axes.grid": True, "grid.alpha": 0.30, "savefig.bbox": "tight"})
    rhs, _, _, _ = boundary_rhs(G_DESIGN, K_in, K_ex)
    rhs_g, _, _, _ = boundary_rhs(G_DESIGN, K_in, K_ex, grids_K=GRID_K)
    ns = [0.0, 6.0]
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    # regions
    ax.fill_between(ns, [n + rhs for n in ns], [12, 12], color=RED, alpha=0.10)
    ax.fill_between(ns, ns, [n + rhs for n in ns], color=GREEN, alpha=0.10)
    ax.fill_between(ns, [0, 0], ns, color=GREY, alpha=0.12)
    ax.plot(ns, [n + rhs for n in ns], color=RED, lw=2.2,
            label=f"Ishii–Zuber boundary, NO grid credit (K_in {K_in}, K_ex {K_ex})")
    ax.plot(ns, [n + rhs_g for n in ns], color=RED, lw=1.6, ls=":",
            label="boundary with 5 spacer grids credited (Λ+4)")
    ax.plot(ns, ns, color=GREY, lw=1.4, ls="--", label="x_exit = 0  (single-phase below)")
    ax.text(0.6, 9.8, "UNSTABLE\n(density-wave)", color=RED, fontsize=11, weight="bold")
    ax.text(4.2, 5.6, "STABLE\n(boiling channel)", color=GREEN, fontsize=11, weight="bold")
    ax.text(4.9, 1.0, "single-phase\n(no DWO mode)", color=GREY, fontsize=10, ha="center")
    PURPLE = "#7d3c98"
    marks = ["o", "s", "^", "D"]
    cols = [NAVY, ORANGE, PURPLE, GREY]
    offs = [(12, -4, "left"), (12, -14, "left"), (-12, 8, "right"), (12, -16, "left")]
    for r, mk, c, (dx, dy, ha) in zip(rows, marks, cols, offs):
        ax.plot(r["n_sub"], r["n_pch"], mk, ms=9, color=c, mec="black", mew=0.7, zorder=5)
        ax.annotate(f"{r['label']}\n(x{r['ratio']:.1f})" if math.isfinite(r["ratio"])
                    else f"{r['label']}\n(subcooled)",
                    (r["n_sub"], r["n_pch"]), textcoords="offset points", xytext=(dx, dy),
                    fontsize=8.5, color=c, ha=ha)
    ax.set_xlim(0, 6); ax.set_ylim(0, 12)
    ax.set_xlabel("subcooling number  N_sub")
    ax.set_ylabel("phase-change number  N_pch")
    ax.set_title("F10 · Density-wave stability map — Aegis-40 hot channel (12.8 MPa)")
    ax.legend(loc="upper left", fontsize=9)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path)
    print(" wrote", path)


if __name__ == "__main__":
    main()
