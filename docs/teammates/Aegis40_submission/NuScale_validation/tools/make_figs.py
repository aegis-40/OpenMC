#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NuScale VALIDATION figure set for the competition report.
Generates F1-F7 as PNGs in docs/figs/. Pure post-processing: GCI/conservation
numbers come from the 3-mesh chtMultiRegionFoam study (field-direct, see
tools/meshindep.py); axial/radial/DNBR profiles are rebuilt from the validated
correlation stack (mdnbr.py + thermal_stack.py) at the NuScale-calibrated peak
(F_q 1.923).  Run:  python3 tools/make_figs.py
"""
import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIGS = os.path.normpath(os.path.join(HERE, "..", "docs", "figs"))
os.makedirs(FIGS, exist_ok=True)

from mdnbr import (Config, build_profile, w3_chf_eu, tong_F)          # noqa: E402
from thermal_stack import StackConfig, film_h, stack                  # noqa: E402
import meshindep as mi                                                # GCI engine

# ---- house style ----
NAVY, RED, GREEN, ORANGE, GREY = "#1f4e79", "#c0392b", "#2e7d32", "#e08a1e", "#888888"
BLUE, PURPLE = "#2e6fb7", "#7d3c98"
plt.rcParams.update({"figure.dpi": 160, "savefig.dpi": 160, "font.size": 11,
                     "axes.titlesize": 12, "axes.titleweight": "bold",
                     "axes.grid": True, "grid.alpha": 0.30, "savefig.bbox": "tight",
                     "axes.prop_cycle": plt.cycler(color=[NAVY, RED, GREEN, ORANGE])})


def save(fig, name):
    p = os.path.join(FIGS, name)
    fig.savefig(p)
    plt.close(fig)
    print("  wrote", os.path.relpath(p, os.path.join(HERE, "..")))


# ============================================================ 3-mesh GCI data
# Mesh study run NATIVELY at the NuScale-calibrated F_q 1.923 (qpeak 2.99e8;
# field-direct values from tools/meshindep.py).
N      = [35700, 103600, 279888]                  # coarse, medium, fine
TOUT   = [603.60, 604.16, 604.43]
PCT    = [660.03, 660.43, 660.64]                 # clad inner peak [K]
FUEL   = [1108.36, 1110.58, 1112.66]
QADV   = [23.05, 23.15, 23.20]                    # advected power [kW]
QSRC   = 23.25                                    # analytic design source [kW]
LBL    = ["coarse\n35.7k", "medium\n103.6k", "fine\n279.9k"]
hrel   = [(N[-1] / n) ** (1.0 / 3.0) for n in N]   # cell size, fine=1
_R21   = (N[2] / N[1]) ** (1.0 / 3.0)
_R32   = (N[1] / N[0]) ** (1.0 / 3.0)


def gci_metric(vals):
    """vals=[coarse,med,fine] -> (Richardson extrap or None, GCI% label)."""
    g = mi.gci3(vals[2], vals[1], vals[0], _R21, _R32)
    if g and g["reliable"]:
        return g["f_ext"], f"{g['gci']:.2f}%"
    d = 100.0 * abs(vals[2] - vals[1]) / abs(vals[2])   # degenerate -> direct change
    return None, f"{d:.2f}% (direct)"


# ============================================================ NuScale-peak stack
cfg = Config(p_mpa=12.8, T_in=531.0, G=684.0, cp=5250.0, L=2.0, D_co=9.5e-3,
             D_h=11.77e-3, A_flow=87.9e-6, qp_hot_peak=15750.0, Fz=1.355,
             Le_ratio=1.2, n=200)
st = StackConfig()
prof = build_profile(cfg)
h, Re, Nu, cname = film_h(cfg, st)
rows_1p, R, _ = stack(cfg, st, prof, h, boiling=False)
rows_bo, _, nb = stack(cfg, st, prof, h, boiling=True)
z   = prof["z"]
qpp = [q / 1e6 for q in prof["qpp"]]              # MW/m2
Tb  = prof["Tbulk"]
Tsat = prof["Tsat"]
Tco_1p = [r[2] for r in rows_1p]
Tco_bo = [r[2] for r in rows_bo]
Tci_bo = [r[3] for r in rows_bo]
Tfc_bo = [r[5] for r in rows_bo]

# DNBR(z)
dHsub = cfg.cp * (Tsat - cfg.T_in)
dnbr = []
for i in range(len(z)):
    qeu = w3_chf_eu(cfg, prof["xq"][i], dHsub)
    F, _ = tong_F(cfg, prof, i)
    dnbr.append((qeu / F) / prof["qpp"][i])
i_md = min(range(len(dnbr)), key=lambda i: dnbr[i])
mdnbr = dnbr[i_md]


# ============================================================ F1 grid convergence
def f1():
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.8))
    sets = [("Outlet T  [K]", TOUT), ("Peak clad T  [K]", PCT), ("Peak fuel T  [K]", FUEL)]
    for a, (ttl, vals) in zip(ax, sets):
        ext, gci = gci_metric(vals)
        ys = vals + ([ext] if ext else [])
        lo, hi = min(ys), max(ys); rng = (hi - lo) or 1.0
        a.set_ylim(lo - 0.30 * rng, hi + 0.34 * rng)   # headroom so labels clear borders
        a.set_xlim(-0.28, 2.2)
        a.plot(hrel, vals, "o-", color=NAVY, ms=8, lw=1.8, zorder=3)
        vmax = max(vals)
        for x, v in zip(hrel, vals):
            dy = -15 if v == vmax else 8               # topmost label drops below its point
            a.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                       xytext=(7, dy), fontsize=8, color=NAVY, ha="left")
        if ext:
            a.plot(0, ext, "*", color=RED, ms=15, zorder=4)
            a.plot([0, hrel[-1]], [ext, vals[-1]], "--", color=RED, lw=1, alpha=0.6)
            a.annotate(f"Richardson\nh→0  {ext:.2f}", (0, ext),
                       textcoords="offset points", xytext=(13, -25),
                       fontsize=8, color=RED, ha="left")
        a.set_title(ttl)
        a.set_xlabel("relative cell size  h/h_fine")
        a.text(0.5, 0.04, f"GCI$_{{fine}}$ {gci}", transform=a.transAxes,
               ha="center", fontsize=9, color=GREEN,
               bbox=dict(boxstyle="round", fc="#eef7ee", ec=GREEN, alpha=0.9))
    fig.suptitle("F1 · Grid convergence — ASME V&V-20 GCI  (NuScale peak, F_q 1.923)",
                 fontweight="bold", y=1.00)
    fig.text(0.5, -0.015, "Mesh study run natively at the NuScale-calibrated F_q 1.923 "
             "(field-direct values, tools/meshindep.py).",
             ha="center", fontsize=7.5, color=GREY, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save(fig, "F1_grid_convergence.png")


# ============================================================ F2 energy conservation
def f2():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = range(len(N))
    bars = ax.bar(x, QADV, width=0.55, color=[NAVY, BLUE, "#5b9bd5"],
                  edgecolor="black", lw=0.6, zorder=3)
    ax.axhline(QSRC, ls="--", color=RED, lw=1.8, zorder=4,
               label=f"design source  {QSRC:.2f} kW")
    for i, b in enumerate(bars):
        ax.annotate(f"{QADV[i]:.2f} kW\n×{QADV[i]/QSRC:.3f}",
                    (b.get_x() + b.get_width() / 2, QADV[i]),
                    textcoords="offset points", xytext=(0, 5), ha="center", fontsize=9)
    ax.set_xticks(list(x)); ax.set_xticklabels(LBL)
    ax.set_ylabel("advected power  ṁ·cp·ΔT  [kW]")
    ax.set_ylim(0, QSRC * 1.20)
    ax.set_title("F2 · Energy conservation — GATE-1 holds on every mesh (×1.00)")
    ax.legend(loc="lower right")
    fig.text(0.5, -0.01, "F_q 1.923 (NuScale peak), native source 23.25 kW/hot-pin.",
             ha="center", fontsize=7.5, color=GREY, style="italic")
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    save(fig, "F2_energy_conservation.png")


# ============================================================ F3 CFD vs NuScale
def f3():
    labels = ["Core inlet", "Core-avg outlet\n(hot leg)", "Hot-channel\noutlet (≈Tsat)",
              "Clad max"]
    nuscale = [258, 310, 331, 360]
    ours    = [258, 310, 331, 352]
    x = range(len(labels)); w = 0.38
    fig, ax = plt.subplots(figsize=(8, 4.3))
    b1 = ax.bar([i - w/2 for i in x], nuscale, w, label="NuScale (published)",
                color=GREY, edgecolor="black", lw=0.6, zorder=3)
    b2 = ax.bar([i + w/2 for i in x], ours, w, label="This work (CFD + stack)",
                color=NAVY, edgecolor="black", lw=0.6, zorder=3)
    for bb in (b1, b2):
        for b in bb:
            ax.annotate(f"{b.get_height():.0f}", (b.get_x()+b.get_width()/2, b.get_height()),
                        textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_ylabel("temperature  [°C]")
    ax.set_title("F3 · Validation vs published NuScale (NPM-160)")
    ax.legend(loc="upper left")
    ax.set_ylim(0, 430)
    save(fig, "F3_vs_nuscale.png")


# ============================================================ F4 axial profiles
def f4():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 6.2), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1, 1.7]))
    a1.plot(z, qpp, color=ORANGE, lw=2)
    a1.fill_between(z, qpp, color=ORANGE, alpha=0.18)
    a1.set_ylabel("q″  [MW/m²]")
    a1.set_title("F4 · Hot-channel axial profiles (NuScale peak, F_q 1.923)")
    # temperatures: bulk & clad on left, fuel centre on right
    a2.plot(z, Tb, color=BLUE, lw=2, label="coolant bulk $T_b$")
    a2.plot(z, Tco_bo, color=NAVY, lw=2, label="clad outer (boiling)")
    a2.axhline(Tsat, ls="--", color=RED, lw=1.4, label=f"$T_{{sat}}$ {Tsat:.0f} K")
    a2.set_ylabel("coolant / clad  T  [K]", color=NAVY)
    a2.set_xlabel("axial position z  [m]")
    a2.set_ylim(525, 680)
    a2r = a2.twinx()
    a2r.plot(z, Tfc_bo, color=GREEN, lw=2, label="fuel centreline")
    a2r.set_ylabel("fuel centreline  T  [K]", color=GREEN)
    a2r.set_ylim(660, 1130); a2r.grid(False)
    l1, la1 = a2.get_legend_handles_labels()
    l2, la2 = a2r.get_legend_handles_labels()
    a2.legend(l1 + l2, la1 + la2, loc="upper right", fontsize=9)
    save(fig, "F4_axial_profiles.png")


# ============================================================ F5 radial stack
def f5():
    pct_i = max(range(len(rows_bo)), key=lambda i: rows_bo[i][3])
    _, Tb_, Tco_, Tci_, Tfs_, Tfc_, _ = rows_bo[pct_i]
    rf, rci, rco = st.r_f*1e3, st.r_ci*1e3, st.r_co*1e3
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    # fuel (parabola centre->surface)
    rr = [i*rf/40 for i in range(41)]
    ax.plot(rr, [Tfc_ - (Tfc_-Tfs_)*(r/rf)**2 for r in rr], color=GREEN, lw=2.5, label="UO₂ fuel")
    ax.plot([rf, rci], [Tfs_, Tci_], color=PURPLE, lw=2.5, label="He gap (contact R)")
    ax.plot([rci, rco], [Tci_, Tco_], color=NAVY, lw=2.5, label="Zr clad")
    ax.plot([rco, 6.2], [Tco_, Tb_], color=BLUE, lw=2.5, ls="--", label="film → bulk")
    for r, T, t in [(0, Tfc_, f"centre {Tfc_-273.15:.0f}°C"), (rf, Tfs_, "fuel surf"),
                    (rci, Tci_, "clad in"), (rco, Tco_, f"clad out {Tco_-273.15:.0f}°C"),
                    (6.2, Tb_, f"bulk {Tb_-273.15:.0f}°C")]:
        ax.plot(r, T, "o", color="black", ms=5, zorder=5)
        ax.annotate(t, (r, T), textcoords="offset points", xytext=(6, 6), fontsize=8)
    for ra, rb, lbl in [(0, rf, "fuel"), (rf, rci, "gap"), (rci, rco, "clad")]:
        ax.axvspan(ra, rb, color=GREY, alpha=0.06)
    ax.set_xlabel("radius from pin centre  [mm]")
    ax.set_ylabel("temperature  [K]")
    ax.set_title(f"F5 · Radial temperature stack at hot spot (z={z[pct_i]:.2f} m)")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "F5_radial_stack.png")


# ============================================================ F6 DNBR(z)
def f6():
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.plot(z, dnbr, color=NAVY, lw=2.2, zorder=3)
    ax.axhline(1.3, ls="--", color=RED, lw=1.8, label="limit  1.3")
    ax.plot(z[i_md], mdnbr, "*", color=RED, ms=16, zorder=5)
    ax.annotate(f"MDNBR = {mdnbr:.2f}\nz = {z[i_md]:.2f} m",
                (z[i_md], mdnbr), textcoords="offset points", xytext=(12, 18),
                fontsize=10, color=RED,
                bbox=dict(boxstyle="round", fc="#fdecea", ec=RED))
    ax.fill_between(z, 1.3, dnbr, where=[d > 1.3 for d in dnbr], color=GREEN, alpha=0.10)
    ax.set_xlabel("axial position z  [m]")
    ax.set_ylabel("DNBR  [-]")
    ax.set_ylim(0, max(dnbr[:i_md+40]) if i_md < 160 else 9)
    ax.set_title("F6 · Hot-channel DNBR — W-3 CHF + Tong F-factor (NuScale peak)")
    ax.legend(loc="upper center")
    save(fig, "F6_dnbr_profile.png")


# ============================================================ F7 subcooled boiling
def f7():
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.plot(z, Tco_1p, color=ORANGE, lw=2, label="clad outer — single-phase film")
    ax.plot(z, Tco_bo, color=NAVY, lw=2.2, label="clad outer — subcooled-boiling (Jens-Lottes)")
    ax.axhline(Tsat, ls="--", color=RED, lw=1.6, label=f"$T_{{sat}}$ {Tsat:.0f} K")
    boil = [zz for zz, t in zip(z, Tco_1p) if t > Tsat]
    if boil:
        ax.axvspan(min(boil), max(boil), color=RED, alpha=0.07)
        ax.text((min(boil)+max(boil))/2, Tsat-6, "subcooled boiling region",
                ha="center", fontsize=9, color=RED)
    ax.set_xlabel("axial position z  [m]")
    ax.set_ylabel("clad outer T  [K]")
    ax.set_title("F7 · Subcooled boiling clamps the clad (why single-phase over-predicts)")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, "F7_subcooled_boiling.png")


if __name__ == "__main__":
    print(f"NuScale-peak stack: Re={Re:,.0f} Nu={Nu:.1f} h={h:,.0f}  MDNBR={mdnbr:.3f}"
          f"  boiling@{nb}/{len(z)} nodes")
    for fn in (f1, f2, f3, f4, f5, f6, f7):
        fn()
    print(f"done -> {FIGS}")
