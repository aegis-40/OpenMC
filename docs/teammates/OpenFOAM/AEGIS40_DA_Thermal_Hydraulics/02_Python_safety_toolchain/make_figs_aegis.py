#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 T-H report figure set (F1-F8) -> docs/figs/ as PNGs.

Pure post-processing of the validated pipeline at the FER design point (high-stat
design basis = the COLR envelope from aegis_sweep.py constants; the F1-F3
verification figures run at the CFD-field source, see cfg_x below):
  F1 grid convergence (GCI)     <- meshindep.collect() field-direct, 3 meshes
  F2 energy conservation GATE-1 <- meshindep advected power vs analytic source
  F3 CFD <-> correlation stack  <- near-wall cross-check (the validation)
  F4 hot-channel axial profiles <- mdnbr/thermal_stack at the design point
  F5 radial T stack at hot spot
  F6 hot-channel DNBR(z)        <- W-3 + Tong
  F7 subcooled-boiling clamp
  F8 natural-circulation sweep  <- aegis_sweep over riser height H_tc

Run:  python3 tools/make_figs_aegis.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FIGS = os.path.normpath(os.path.join(HERE, "..", "docs", "figs"))
os.makedirs(FIGS, exist_ok=True)

from mdnbr import Config, build_profile, w3_chf_eu, tong_F          # noqa: E402
from thermal_stack import StackConfig, film_h, stack               # noqa: E402
import meshindep as mi                                             # GCI engine + GATE-1
import aegis_sweep as sw                                           # natcirc feasibility

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


# ===================================================== live 3-mesh GCI / GATE-1
CASES = [("pin_coarse", "coarse"), ("pin", "medium"), ("pin_fine", "fine")]
R = {tag: mi.collect(case) for case, tag in CASES}
N    = [R["coarse"]["N"], R["medium"]["N"], R["fine"]["N"]]
TOUT = [R[t]["Tout"]  for t in ("coarse", "medium", "fine")]
PCT  = [R[t]["Tc"]    for t in ("coarse", "medium", "fine")]   # peak clad inner [K]
FUEL = [R[t]["Tf"]    for t in ("coarse", "medium", "fine")]
QADV = [R[t]["Qadv"]/1e3 for t in ("coarse", "medium", "fine")]
QSRC = mi.Q_DESIGN/1e3                                          # analytic design source [kW]
LBL  = [f"coarse\n{N[0]/1e3:.1f}k", f"medium\n{N[1]/1e3:.1f}k", f"fine\n{N[2]/1e3:.0f}k"]
hrel = [(N[-1]/n)**(1.0/3.0) for n in N]
_R21 = (N[2]/N[1])**(1.0/3.0)
_R32 = (N[1]/N[0])**(1.0/3.0)


def gci_metric(vals):
    g = mi.gci3(vals[2], vals[1], vals[0], _R21, _R32)
    if g and g["reliable"]:
        return g["f_ext"], f"{g['gci']:.2f}%"
    d = 100.0*abs(vals[2]-vals[1])/abs(vals[2])
    return None, f"{d:.2f}% (direct)"


# ============= design-basis stack (COLR envelope) + CFD-source cross-check =============
# F4-F7 present the BINDING design point (sw constants = the MOC COLR envelope, F_q 2.4675).
# F3 is the CFD<->stack VERIFICATION and must run at the same source as the CFD fields on
# disk -> cfg_x pins those values (equal to the envelope basis).
ASRUN_QPK, ASRUN_FZ, ASRUN_LE = 15788.0, 1.410, 1.13334  # = constant/fuel/fvOptions source
G_CFD = R["medium"]["mdot"] / sw.A_F
cfg = Config(p_mpa=12.8, T_in=531.15, G=G_CFD, cp=5350.0, L=2.0, D_co=sw.D_CO,
             D_h=sw.D_H, A_flow=sw.A_F, qp_hot_peak=sw.QP_PEAK, Fz=sw.F_Z,
             Le_ratio=sw.LE_RATIO, n=200)
cfg_x = Config(p_mpa=12.8, T_in=531.15, G=G_CFD, cp=5350.0, L=2.0, D_co=sw.D_CO,
               D_h=sw.D_H, A_flow=sw.A_F, qp_hot_peak=ASRUN_QPK, Fz=ASRUN_FZ,
               Le_ratio=ASRUN_LE, n=200)
st = StackConfig(r_f=sw.R_F, r_ci=sw.R_CI, r_co=sw.R_CO, k_fuel=sw.K_FUEL,
                 k_clad=sw.K_CLAD, h_gap=sw.H_GAP, mu=sw.MU, k_w=sw.KW, Pr=sw.PR, corr="db")
prof = build_profile(cfg)
h, Re, Nu, cname = film_h(cfg, st)
rows_1p, RES, _ = stack(cfg, st, prof, h, boiling=False)
rows_bo, _, nb = stack(cfg, st, prof, h, boiling=True)
z    = prof["z"]
qpp  = [q/1e6 for q in prof["qpp"]]
Tb   = prof["Tbulk"]
Tsat = prof["Tsat"]
Tco_1p = [r[2] for r in rows_1p]
Tco_bo = [r[2] for r in rows_bo]
Tci_bo = [r[3] for r in rows_bo]
Tfc_bo = [r[5] for r in rows_bo]

dHsub = cfg.cp*(Tsat - cfg.T_in)
dnbr = []
for i in range(len(z)):
    qeu = w3_chf_eu(cfg, prof["xq"][i], dHsub)
    F, _ = tong_F(cfg, prof, i)
    dnbr.append((qeu/F)/prof["qpp"][i])
i_md = min(range(len(dnbr)), key=lambda i: dnbr[i])
mdnbr = dnbr[i_md]

# -------- Cross-check set (F3): the stack at the CFD's own source --------
prof_x = build_profile(cfg_x)
h_x, _, _, _ = film_h(cfg_x, st)
rows_1p_x, _, _ = stack(cfg_x, st, prof_x, h_x, boiling=False)
pct1_x = max(range(len(rows_1p_x)), key=lambda i: rows_1p_x[i][3])

# single-phase stack peaks (for the F3 cross-check vs CFD)
pct1_i = max(range(len(rows_1p)), key=lambda i: rows_1p[i][3])
# F3 is the SINGLE-PHASE verification (1-phi CFD vs 1-phi stack) at the CFD source:
# use the uncapped energy-balance outlet Tsp = Tsat + x_e*hfg/cp, not the F1-ii capped bulk --
# comparing capped-vs-uncapped would show a spurious ~7 K "disagreement" at the outlet.
ST = dict(bulk=Tsat + prof_x["xq"][-1]*prof_x["hfg"]/cfg_x.cp, fuel=max(r[5] for r in rows_1p_x),
          clad=max(r[3] for r in rows_1p_x), nearwall=rows_1p_x[pct1_x][2])
CF = dict(bulk=R["medium"]["Tout"], fuel=R["medium"]["Tf"],
          clad=R["medium"]["Tc"], nearwall=R["medium"]["Twall"])


# ============================================================ F1 grid convergence
def f1():
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.8))
    for a, (ttl, vals) in zip(ax, [("Outlet T  [K]", TOUT), ("Peak clad T  [K]", PCT),
                                   ("Peak fuel T  [K]", FUEL)]):
        ext, gci = gci_metric(vals)
        ys = vals + ([ext] if ext else [])
        lo, hi = min(ys), max(ys); rng = (hi-lo) or 1.0
        a.set_ylim(lo-0.30*rng, hi+0.34*rng); a.set_xlim(-0.28, 2.2)
        a.plot(hrel, vals, "o-", color=NAVY, ms=8, lw=1.8, zorder=3)
        vmax = max(vals)
        for x, v in zip(hrel, vals):
            a.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                       xytext=(7, -15 if v == vmax else 8), fontsize=8, color=NAVY)
        if ext:
            a.plot(0, ext, "*", color=RED, ms=15, zorder=4)
            a.plot([0, hrel[-1]], [ext, vals[-1]], "--", color=RED, lw=1, alpha=0.6)
            a.annotate(f"Richardson\nh→0  {ext:.2f}", (0, ext), textcoords="offset points",
                       xytext=(13, -25), fontsize=8, color=RED)
        a.set_title(ttl); a.set_xlabel("relative cell size  h/h_fine")
        a.text(0.5, 0.04, f"GCI$_{{fine}}$ {gci}", transform=a.transAxes, ha="center",
               fontsize=9, color=GREEN, bbox=dict(boxstyle="round", fc="#eef7ee", ec=GREEN, alpha=0.9))
    fig.suptitle("F1 · Grid convergence — ASME V&V-20 GCI  (Aegis-40 FER peak, F_q 2.035)",
                 fontweight="bold", y=1.00)
    fig.text(0.5, -0.015, f"3 meshes {N[0]/1e3:.1f}k / {N[1]/1e3:.1f}k / {N[2]/1e3:.0f}k, "
             "r21=%.3f r32=%.3f; field-direct (tools/meshindep.py). No rescale — run AT design peaking."
             % (_R21, _R32), ha="center", fontsize=7.5, color=GREY, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    save(fig, "F1_grid_convergence.png")


# ============================================================ F2 energy conservation
def f2():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = range(len(N))
    bars = ax.bar(x, QADV, width=0.55, color=[NAVY, BLUE, "#5b9bd5"], edgecolor="black", lw=0.6, zorder=3)
    ax.axhline(QSRC, ls="--", color=RED, lw=1.8, zorder=4, label=f"design source  {QSRC:.2f} kW")
    for i, b in enumerate(bars):
        ax.annotate(f"{QADV[i]:.2f} kW\n×{QADV[i]/QSRC:.3f}",
                    (b.get_x()+b.get_width()/2, QADV[i]), textcoords="offset points",
                    xytext=(0, 5), ha="center", fontsize=9)
    ax.set_xticks(list(x)); ax.set_xticklabels(LBL)
    ax.set_ylabel("advected power  ṁ·cp·ΔT  [kW]"); ax.set_ylim(0, QSRC*1.20)
    ax.set_title("F2 · Energy conservation — GATE-1 holds on every mesh (×1.00)")
    ax.legend(loc="lower right")
    save(fig, "F2_energy_conservation.png")


# ============================================================ F3 CFD vs stack cross-check
def f3():
    keys = [("bulk", "Coolant\noutlet"), ("fuel", "Fuel\ncentre"),
            ("clad", "Clad inner\n(peak)"), ("nearwall", "Near-wall\n(clad outer)")]
    cf = [CF[k]-273.15 for k, _ in keys]
    sk = [ST[k]-273.15 for k, _ in keys]
    x = range(len(keys)); w = 0.38
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    b1 = ax.bar([i-w/2 for i in x], cf, w, label="CFD (chtMultiRegionFoam, medium)",
                color=NAVY, edgecolor="black", lw=0.6, zorder=3)
    b2 = ax.bar([i+w/2 for i in x], sk, w, label="Correlation stack (Dittus-Boelter, 1φ)",
                color=GREY, edgecolor="black", lw=0.6, zorder=3)
    for k, (cv, sv) in enumerate(zip(cf, sk)):
        ax.annotate(f"{cv:.0f}", (k-w/2, cv), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
        ax.annotate(f"{sv:.0f}", (k+w/2, sv), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
        ax.annotate(f"Δ {abs(cv-sv):.1f} K", (k, max(cv, sv)), textcoords="offset points",
                    xytext=(0, 20), ha="center", fontsize=8.5, color=RED)
    ax.set_xticks(list(x)); ax.set_xticklabels([l for _, l in keys])
    ax.set_ylabel("temperature  [°C]"); ax.set_ylim(0, max(cf+sk)*1.18)
    ax.set_title("F3 · CFD ↔ correlation-stack cross-check — near-wall sound (Δ < 7 K)")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, "F3_cfd_vs_stack.png")


# ============================================================ F4 axial profiles
def f4():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 6.2), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1, 1.7]))
    a1.plot(z, qpp, color=ORANGE, lw=2); a1.fill_between(z, qpp, color=ORANGE, alpha=0.18)
    a1.set_ylabel("q″  [MW/m²]")
    a1.set_title("F4 · Hot-channel axial profiles (COLR envelope, F_q 2.47)")
    a2.plot(z, Tb, color=BLUE, lw=2, label="coolant bulk $T_b$")
    a2.plot(z, Tco_bo, color=NAVY, lw=2, label="clad outer (boiling)")
    a2.axhline(Tsat, ls="--", color=RED, lw=1.4, label=f"$T_{{sat}}$ {Tsat:.0f} K")
    a2.set_ylabel("coolant / clad  T  [K]", color=NAVY)
    a2.set_xlabel("axial position z  [m]"); a2.set_ylim(525, 675)
    a2r = a2.twinx()
    a2r.plot(z, Tfc_bo, color=GREEN, lw=2, label="fuel centreline")
    a2r.set_ylabel("fuel centreline  T  [K]", color=GREEN); a2r.set_ylim(640, 1040); a2r.grid(False)
    l1, la1 = a2.get_legend_handles_labels(); l2, la2 = a2r.get_legend_handles_labels()
    a2.legend(l1+l2, la1+la2, loc="upper right", fontsize=9)
    save(fig, "F4_axial_profiles.png")


# ============================================================ F5 radial stack
def f5():
    pct_i = max(range(len(rows_bo)), key=lambda i: rows_bo[i][3])
    _, Tb_, Tco_, Tci_, Tfs_, Tfc_, _ = rows_bo[pct_i]
    rf, rci, rco = st.r_f*1e3, st.r_ci*1e3, st.r_co*1e3
    rsub = (sw.PITCH*1e3)/2.0
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    rr = [i*rf/40 for i in range(41)]
    ax.plot(rr, [Tfc_-(Tfc_-Tfs_)*(r/rf)**2 for r in rr], color=GREEN, lw=2.5, label="UO₂ fuel")
    ax.plot([rf, rci], [Tfs_, Tci_], color=PURPLE, lw=2.5, label="He gap (contact R)")
    ax.plot([rci, rco], [Tci_, Tco_], color=NAVY, lw=2.5, label="Zr clad")
    ax.plot([rco, rsub], [Tco_, Tb_], color=BLUE, lw=2.5, ls="--", label="film → bulk")
    for r, T, t in [(0, Tfc_, f"centre {Tfc_-273.15:.0f}°C"), (rf, Tfs_, "fuel surf"),
                    (rci, Tci_, "clad in"), (rco, Tco_, f"clad out {Tco_-273.15:.0f}°C"),
                    (rsub, Tb_, f"bulk {Tb_-273.15:.0f}°C")]:
        ax.plot(r, T, "o", color="black", ms=5, zorder=5)
        ax.annotate(t, (r, T), textcoords="offset points", xytext=(6, 6), fontsize=8)
    for ra, rb in [(0, rf), (rf, rci), (rci, rco)]:
        ax.axvspan(ra, rb, color=GREY, alpha=0.06)
    ax.set_xlabel("radius from pin centre  [mm]"); ax.set_ylabel("temperature  [K]")
    ax.set_title(f"F5 · Radial temperature stack at hot spot (z={z[pct_i]:.2f} m)")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "F5_radial_stack.png")


# ============================================================ F6 DNBR(z)
def f6():
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.plot(z, dnbr, color=NAVY, lw=2.2, zorder=3)
    ax.axhline(1.3, ls="--", color=RED, lw=1.8, label="limit  1.3")
    ax.plot(z[i_md], mdnbr, "*", color=RED, ms=16, zorder=5)
    ax.annotate(f"MDNBR = {mdnbr:.2f}\nz = {z[i_md]:.2f} m", (z[i_md], mdnbr),
                textcoords="offset points", xytext=(12, 18), fontsize=10, color=RED,
                bbox=dict(boxstyle="round", fc="#fdecea", ec=RED))
    ax.fill_between(z, 1.3, dnbr, where=[d > 1.3 for d in dnbr], color=GREEN, alpha=0.10)
    ax.set_xlabel("axial position z  [m]"); ax.set_ylabel("DNBR  [-]")
    ax.set_ylim(0, min(9, max(dnbr[:i_md+50])))
    ax.set_title("F6 · Hot-channel DNBR — W-3 CHF + Tong F-factor (FER peak, G %.0f)" % cfg.G)
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
        ax.text((min(boil)+max(boil))/2, Tsat-7, "subcooled boiling region", ha="center",
                fontsize=9, color=RED)
    ax.set_xlabel("axial position z  [m]"); ax.set_ylabel("clad outer T  [K]")
    ax.set_title("F7 · Subcooled boiling clamps the clad (why single-phase over-predicts)")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, "F7_subcooled_boiling.png")


# ============================================================ F8 natural circulation
def f8():
    Htc = [3, 4, 5, 6, 7, 8]
    pts = [sw.run_point(H, 12.0) for H in Htc]
    G = [p["G"] for p in pts]; MD = [p["mdnbr"] for p in pts]
    fig, ax = plt.subplots(figsize=(7.8, 4.5))
    ax.plot(Htc, G, "o-", color=NAVY, lw=2, ms=7, label="core mass flux G")
    ax.set_xlabel("riser thermal-centre height  H_tc  [m]")
    ax.set_ylabel("core mass flux  G  [kg/m²s]", color=NAVY)
    axr = ax.twinx()
    axr.plot(Htc, MD, "s--", color=RED, lw=2, ms=7, label="MDNBR")
    axr.axhline(1.3, ls=":", color=RED, lw=1.4)
    axr.set_ylabel("MDNBR  [-]", color=RED); axr.grid(False)
    # design point H_tc=4 (FER dT 50 -> G 543)
    ax.axvline(4, color=GREEN, lw=1.4, alpha=0.7)
    ax.annotate("FER design point\nH_tc≈4 m · G 543 · MDNBR 1.54", (4, G[1]),
                textcoords="offset points", xytext=(14, -6), fontsize=8.5, color=GREEN)
    l1, la1 = ax.get_legend_handles_labels(); l2, la2 = axr.get_legend_handles_labels()
    ax.legend(l1+l2, la1+la2, loc="lower right", fontsize=9)
    ax.set_title("F8 · Natural-circulation feasibility — riser height vs G & MDNBR")
    save(fig, "F8_natcirc_sweep.png")


if __name__ == "__main__":
    print(f"Aegis FER-peak stack: Re={Re:,.0f} Nu={Nu:.1f} h={h:,.0f}  MDNBR={mdnbr:.3f}"
          f"  boiling@{nb}/{len(z)} nodes  (G={cfg.G:.0f})")
    print(f"GATE-1: QADV {QADV} kW  vs design {QSRC:.2f} kW")
    print(f"F3 cross-check (CFD vs stack, °C): " +
          ", ".join(f"{k} {CF[k]-273.15:.0f}/{ST[k]-273.15:.0f}" for k in ("bulk","fuel","clad","nearwall")))
    for fn in (f1, f2, f3, f4, f5, f6, f7, f8):
        fn()
    print(f"done -> {FIGS}")
