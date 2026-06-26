"""Aegis-40 37-FA / 7x7 — 2-D general-arrangement drawing package.

Produces three dimensioned sheets into docs/competition/cad/ga/37fa/:
  sheet1  radial cross-section   (core -> barrel -> downcomer -> RPV -> bioshield)  "everything fits"
  sheet2  axial half-section     (heads, core, riser, OTSG, pressuriser + EL stack) "height/OTSG fit"
  sheet3  core loading map        (37-FA octagon, enrichment rings, Gd zoning, 12 CRA)

All dimensions from docs/competition/cad/aegis40-geometry-spec-37fa.md, which is anchored to the
locked neutronics constants in aegis40_neutronics_FER.ipynb (cell 5). Pure matplotlib (no cadquery).
Run:  C:/Windows/py.exe -3 scripts/generate_ga_drawings_37fa.py
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, Polygon, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "competition", "cad", "ga", "37fa")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------- locked parameters (mm)
FA_PITCH   = 216.038
N_PIN      = 17
PIN_PITCH  = 12.623
ACTIVE_H   = 2000.0
AX_REFL    = 300.0

CORE_MAP = np.array([
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
])
CR_MAP = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

# radial build (radii, mm) — TIGHT / NuScale-benchmarked build (RPV OD 3010)
R_FUEL_FLAT = 7 * FA_PITCH / 2.0           # 756.1
R_FUEL_CORN = 764.0
R_REFL      = 946.0                        # heavy-steel reflector to barrel ID (nom 190 mm; NuScale 64-310)
R_BARREL_I  = 950.0                        # barrel ID 1900 (NuScale 1880 = 74 in)
R_BARREL_O  = 1000.0                       # barrel OD 2000 (wall 50; NuScale 1981 = 78 in)
R_VESSEL_I  = 1350.0                       # RPV ID 2700 — SG lives in downcomer annulus (NuScale)
R_VESSEL_O  = 1505.0                       # RPV OD 3010 (wall 150 + 5 clad)
R_CAVITY    = 1655.0
R_TSHIELD   = 1705.0
R_POLY      = 1805.0
R_CONCRETE  = 3005.0
R_FINISH    = 3105.0
# OTSG cartridge (unchanged 125 MWth; sits in the upper annulus, NOT a separate fat shroud)
R_RISER     = 560.0
R_SG_I      = 665.0
R_SG_O      = 1075.0
R_SHROUD    = 1130.0

# axial ELs (mm above lower-head pole) — heads R = OD/2 = 1505; H_th preserved 2.85 m
EL_POLE      = 0
EL_SKIRT     = 1335
EL_LTAN      = 1505
EL_DISTRIB   = 1690
EL_LCSP      = 2265
EL_CORE_BOT  = 2305
EL_FUEL_BOT  = 2605
EL_FUEL_MID  = 3605
EL_FUEL_TOP  = 4605
EL_UCSP      = 4905
EL_SG_BOT    = 5155
EL_FW        = 5355
EL_SG_MID    = 6455
EL_STEAM     = 7555
EL_SG_TOP    = 7755
EL_RISER_TOP = 7905
EL_UTAN      = 8705
EL_UHEAD_TOP = 10210
EL_PZR_BOT   = 9960
EL_PZR_TOP   = 11530

# colours
C = dict(fuel="#b23b3b", refl="#cfe6f5", barrel="#8a8f98", water="#dff0fb",
         steel="#9aa0a8", rpv="#5f6b78", clad="#3f4a57", cav="#f2f2f2",
         tshield="#7d848c", poly="#f3e2a9", conc="#c9bfa8", finish="#e4ddca",
         sg="#3f7fb5", riser="#e7b7b7", pzr="#d98b8b", line="#222")

DIM = dict(color="#0b5", lw=0.9)


def dim_h(ax, x0, x1, y, txt, off=0, color="#0b6", fs=8):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    ax.text((x0 + x1) / 2, y + off, txt, ha="center", va="bottom" if off >= 0 else "top",
            fontsize=fs, color=color)


def dim_v(ax, x, y0, y1, txt, off=0, color="#0b6", fs=8):
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=color, lw=0.9))
    ax.text(x + off, (y0 + y1) / 2, txt, ha="left" if off >= 0 else "right", va="center",
            rotation=90, fontsize=fs, color=color)


# =============================================================================== SHEET 1: radial
def sheet1():
    fig, ax = plt.subplots(figsize=(13, 13))
    layers = [
        (R_FINISH,   C["finish"],  "Finish concrete 100"),
        (R_CONCRETE, C["conc"],    "Magnetite concrete 1200"),
        (R_POLY,     C["poly"],    "Borated PE 100"),
        (R_TSHIELD,  C["tshield"], "SS-304 thermal shield 50"),
        (R_CAVITY,   C["cav"],     "Reactor cavity (air) 150"),
        (R_VESSEL_O, C["rpv"],     "RPV wall 150+5"),
        (R_VESSEL_I, C["water"],   "Downcomer + integral OTSG (cold leg)"),
        (R_BARREL_O, C["barrel"],  "Core barrel 50"),
        (R_BARREL_I, C["refl"],    "Heavy-steel reflector ~190"),
    ]
    for r, col, _ in layers:
        ax.add_patch(Circle((0, 0), r, facecolor=col, edgecolor=C["line"], lw=0.8, zorder=1))

    # OTSG cartridge footprint (projected, dashed) + riser
    ax.add_patch(Circle((0, 0), R_SHROUD, fill=False, ec=C["sg"], ls="--", lw=1.0, zorder=3))
    ax.add_patch(Wedge((0, 0), R_SG_O, 0, 360, width=R_SG_O - R_SG_I,
                       facecolor=C["sg"], alpha=0.25, ec=C["sg"], lw=0.6, zorder=3))
    ax.add_patch(Circle((0, 0), R_RISER, facecolor=C["riser"], ec=C["line"], lw=0.6, zorder=4))
    ax.text(0, 0, "riser\nR560", ha="center", va="center", fontsize=7, zorder=5)
    ax.text(0, (R_SG_I + R_SG_O) / 2, "OTSG bundle\nR665–1075 (projected)", ha="center",
            va="center", fontsize=7, color=C["sg"], zorder=5)
    ax.text(R_SHROUD * 0.71, R_SHROUD * 0.71, "SG shroud ~OD2260", fontsize=7, color=C["sg"],
            rotation=-45, ha="center", va="center", zorder=5)

    # 37-FA octagon footprint inside reflector
    draw_core_octagon(ax, zorder=6, faces=True)

    # outer-layer dimension ladder along the lower-right diagonal (one rung per outer layer)
    outer = [(R_VESSEL_O, R_CAVITY, "cavity 150"),
             (R_CAVITY, R_TSHIELD, "SS thermal shield 50"),
             (R_TSHIELD, R_POLY, "borated-PE 100"),
             (R_POLY, R_CONCRETE, "magnetite concrete 1200"),
             (R_CONCRETE, R_FINISH, "finish 100")]
    yb = -R_FINISH - 380
    for i, (a, b, t) in enumerate(outer):
        yy = yb - (i % 2) * 300
        ax.plot([a, a], [0, yy], color="#999", lw=0.35, ls=":")
        ax.plot([b, b], [0, yy], color="#999", lw=0.35, ls=":")
        dim_h(ax, a, b, yy, t, off=22, fs=8.5)

    # diameter callouts on the right
    for r, lab in [(R_VESSEL_I, "RPV ID Ø2700"), (R_VESSEL_O, "RPV OD Ø3010"),
                   (R_FINISH, "shield Ø6210")]:
        ax.annotate(lab, (r, 0), (R_FINISH + 250, r * 0.9),
                    arrowprops=dict(arrowstyle="->", color="#444", lw=0.7),
                    fontsize=8.5, ha="left", va="center")

    ax.set_xlim(-R_FINISH - 400, R_FINISH + 1500)
    ax.set_ylim(-R_FINISH - 1250, R_FINISH + 400)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("AEGIS-40  •  SHEET 1 — RADIAL CROSS-SECTION (core mid-plane, EL 3605)\n"
                 "37-FA / 7×7 octagonal core  •  all dims mm  •  ⚠ Tier-B CONFIRM",
                 fontsize=12, fontweight="bold")
    legend(ax, layers)

    # ---- inset: zoom of the core -> RPV region (the layers the concrete dwarfs)
    axin = fig.add_axes([0.085, 0.085, 0.30, 0.30])
    inner = [(R_VESSEL_O, C["rpv"]), (R_VESSEL_I, C["water"]),
             (R_BARREL_O, C["barrel"]), (R_BARREL_I, C["refl"])]
    for r, col in inner:
        axin.add_patch(Circle((0, 0), r, facecolor=col, ec=C["line"], lw=0.8))
    axin.add_patch(Circle((0, 0), R_SHROUD, fill=False, ec=C["sg"], ls="--", lw=1.0))
    axin.add_patch(Wedge((0, 0), R_SG_O, 0, 360, width=R_SG_O - R_SG_I,
                  facecolor=C["sg"], alpha=0.25, ec=C["sg"], lw=0.5))
    axin.add_patch(Circle((0, 0), R_RISER, facecolor=C["riser"], ec=C["line"], lw=0.5))
    draw_core_octagon(axin, faces=True)
    rungs = [(0, R_FUEL_FLAT, "fuel 756"), (R_FUEL_FLAT, R_REFL, "refl 190"),
             (R_BARREL_O, R_VESSEL_I, "downcomer+SG 350"), (R_VESSEL_I, R_VESSEL_O, "RPV 155")]
    for i, (a, b, t) in enumerate(rungs):
        yy = -R_VESSEL_O - 150 - (i % 2) * 230
        axin.plot([a, a], [0, yy], color="#888", lw=0.4, ls=":")
        axin.plot([b, b], [0, yy], color="#888", lw=0.4, ls=":")
        dim_h(axin, a, b, yy, t, off=18, fs=7.5)
    axin.annotate("barrel ID Ø1900", (R_BARREL_I, 0), (R_VESSEL_O + 120, R_VESSEL_O * 0.5),
                  arrowprops=dict(arrowstyle="->", color="#444", lw=0.6), fontsize=7.5, va="center")
    axin.set_xlim(-R_VESSEL_O - 200, R_VESSEL_O + 900)
    axin.set_ylim(-R_VESSEL_O - 700, R_VESSEL_O + 200)
    axin.set_aspect("equal")
    axin.axis("off")
    axin.set_title("INSET — core → RPV detail", fontsize=8.5, fontweight="bold")
    for s in ("left", "right", "top", "bottom"):
        axin.spines[s].set_visible(False)

    fig.savefig(os.path.join(OUT, "ga37_sheet1_radial.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


def draw_core_octagon(ax, zorder=6, faces=False):
    """Draw the 37 FA squares on the FA_PITCH grid, octagonal map, centred at origin."""
    n = 7
    c = (n - 1) / 2.0
    for i in range(n):
        for j in range(n):
            if CORE_MAP[i, j] == 0:
                continue
            x = (j - c) * FA_PITCH
            y = (c - i) * FA_PITCH
            ax.add_patch(Rectangle((x - FA_PITCH / 2, y - FA_PITCH / 2), FA_PITCH, FA_PITCH,
                         facecolor="#f6d9d9" if faces else "none", ec=C["fuel"], lw=0.7, zorder=zorder))
            if CR_MAP[i, j] == 1:
                ax.add_patch(Circle((x, y), 26, facecolor=C["clad"], ec="none", zorder=zorder + 1))


def legend(ax, layers):
    from matplotlib.patches import Patch
    h = [Patch(facecolor=col, ec="#222", label=lab) for _, col, lab in layers]
    ax.legend(handles=h, loc="lower right", fontsize=7.5, framealpha=0.95, title="Radial layers")


# =============================================================================== SHEET 2: axial
def sheet2():
    fig, ax = plt.subplots(figsize=(11, 16))
    Rv_i, Rv_o = R_VESSEL_I, R_VESSEL_O

    # ---- vessel pressure boundary (right half: 0..Rv_o) as outline + heads
    # cylindrical shell walls
    ax.add_patch(Rectangle((Rv_i, EL_LTAN), Rv_o - Rv_i, EL_UTAN - EL_LTAN,
                 facecolor=C["rpv"], ec=C["line"], lw=1))
    # lower hemispherical head (right quarter)
    ax.add_patch(Wedge((0, EL_LTAN), Rv_o, 270, 360, width=Rv_o - Rv_i,
                 facecolor=C["rpv"], ec=C["line"], lw=1))
    # upper hemispherical head
    ax.add_patch(Wedge((0, EL_UTAN), Rv_o, 0, 90, width=Rv_o - Rv_i,
                 facecolor=C["rpv"], ec=C["line"], lw=1))

    # ---- internal water column (downcomer + plena), inside ID
    ax.add_patch(Rectangle((0, EL_LTAN - Rv_i), Rv_i, (EL_UTAN + Rv_i) - (EL_LTAN - Rv_i),
                 facecolor=C["water"], ec="none", zorder=0))
    ax.add_patch(Wedge((0, EL_LTAN), Rv_i, 270, 360, facecolor=C["water"], zorder=0))
    ax.add_patch(Wedge((0, EL_UTAN), Rv_i, 0, 90, facecolor=C["water"], zorder=0))

    # ---- core barrel + core
    ax.add_patch(Rectangle((0, EL_CORE_BOT), R_BARREL_O, EL_UCSP - EL_CORE_BOT,
                 facecolor=C["barrel"], ec=C["line"], lw=0.8, zorder=2))
    ax.add_patch(Rectangle((0, EL_CORE_BOT), R_BARREL_I, EL_UCSP - EL_CORE_BOT,
                 facecolor=C["refl"], ec="none", zorder=2))
    ax.add_patch(Rectangle((0, EL_FUEL_BOT), R_FUEL_FLAT, ACTIVE_H,
                 facecolor=C["fuel"], ec=C["line"], lw=0.8, zorder=3))
    ax.text(R_FUEL_FLAT / 2, EL_FUEL_MID, "ACTIVE\nCORE\n37 FA\n2000 mm", ha="center",
            va="center", color="white", fontsize=9, fontweight="bold", zorder=4)
    ax.text(R_FUEL_FLAT * 0.5, EL_FUEL_TOP + 150, "axial reflector 300", ha="center",
            fontsize=6.5, color="#3a6", zorder=4)

    # ---- riser
    ax.add_patch(Rectangle((0, EL_UCSP), R_RISER, EL_RISER_TOP - EL_UCSP,
                 facecolor=C["riser"], ec=C["line"], lw=0.8, zorder=3))
    ax.text(R_RISER / 2, (EL_UCSP + EL_RISER_TOP) / 2, "RISER\nR560\n(hot leg ↑)", ha="center",
            va="center", fontsize=7.5, zorder=4)

    # ---- OTSG bundle (both radial bands shown on right side)
    ax.add_patch(Rectangle((R_SG_I, EL_SG_BOT), R_SG_O - R_SG_I, EL_SG_TOP - EL_SG_BOT,
                 facecolor=C["sg"], alpha=0.55, ec=C["line"], lw=0.8, zorder=3))
    # helical hatch
    for k in range(int((EL_SG_TOP - EL_SG_BOT) / 120)):
        yy = EL_SG_BOT + k * 120
        ax.plot([R_SG_I, R_SG_O], [yy, yy + 120], color="#fff", lw=0.5, zorder=4)
    ax.text((R_SG_I + R_SG_O) / 2, EL_SG_MID, "OTSG\nhelical\n125 MWth", ha="center",
            va="center", fontsize=7.5, color="white", fontweight="bold", zorder=5)
    # shroud line
    ax.plot([R_SHROUD, R_SHROUD], [EL_SG_BOT - 120, EL_SG_TOP + 120], color=C["sg"], lw=1.2, zorder=4)
    ax.text(R_SHROUD + 20, EL_SG_TOP + 60, "shroud\nOD2360", fontsize=6.5, color=C["sg"], zorder=5)

    # ---- pressuriser
    ax.add_patch(Rectangle((0, EL_PZR_BOT), 470, EL_PZR_TOP - 470 - EL_PZR_BOT,
                 facecolor=C["pzr"], ec=C["line"], lw=0.8, zorder=3))
    ax.add_patch(Wedge((0, EL_PZR_TOP - 470), 470, 0, 90, facecolor=C["pzr"], ec=C["line"], lw=0.8, zorder=3))
    ax.text(235, EL_PZR_BOT + 500, "PZR", ha="center", fontsize=7.5, zorder=4)

    # ---- nozzles
    for el, lab, col in [(EL_FW, "FW in", "#1c6dd0"), (EL_STEAM, "steam out", "#c0392b")]:
        ax.add_patch(Rectangle((Rv_o, el - 65), 320, 130, facecolor=col, ec=C["line"], lw=0.6, zorder=4))
        ax.text(Rv_o + 340, el, lab, va="center", fontsize=7, color=col, zorder=5)

    # ---- skirt
    ax.add_patch(Polygon([(Rv_o - 60, EL_LTAN), (Rv_o + 100, EL_SKIRT), (Rv_o + 160, EL_SKIRT),
                          (Rv_o, EL_LTAN)], closed=True, facecolor=C["steel"], ec=C["line"], lw=0.7, zorder=2))

    # ---- centreline + axis
    ax.axvline(0, color=C["line"], lw=1.2, ls="-.")
    ax.text(8, EL_PZR_TOP + 120, "DATUM A (axis)", fontsize=7)

    # ---- EL ladder on the left
    els = [(EL_POLE, "EL 0  lower-head pole (DATUM B)"), (EL_LTAN, "1505  lower tangent"),
           (EL_CORE_BOT, "2305  core bottom"), (EL_FUEL_BOT, "2605  active fuel bottom"),
           (EL_FUEL_MID, "3605  fuel mid (DATUM C)"), (EL_FUEL_TOP, "4605  active fuel top"),
           (EL_SG_BOT, "5155  OTSG bottom"), (EL_SG_MID, "6455  OTSG mid"),
           (EL_SG_TOP, "7755  OTSG top"), (EL_UTAN, "8705  upper tangent / flange"),
           (EL_UHEAD_TOP, "10210  closure-head top"), (EL_PZR_TOP, "11530  PZR dome (overall)")]
    xL = -Rv_o - 900
    for el, lab in els:
        ax.plot([xL, 0], [el, el], color="#bbb", lw=0.4, ls=":")
        ax.plot([xL, xL + 40], [el, el], color="#333", lw=0.8)
        ax.text(xL - 30, el, lab, ha="right", va="center", fontsize=7)

    # ---- key vertical dims on the right
    dim_v(ax, Rv_o + 560, EL_FUEL_BOT, EL_FUEL_TOP, "active 2000", off=40, fs=8)
    dim_v(ax, Rv_o + 560, EL_SG_BOT, EL_SG_TOP, "OTSG 2600", off=40, fs=8)
    dim_v(ax, Rv_o + 780, EL_FUEL_MID, EL_SG_MID, "H_th = 2850\n(nat-circ)", off=40, fs=8, color="#b5009b")
    dim_v(ax, Rv_o + 1050, EL_POLE, EL_PZR_TOP, "overall ≈ 11 530", off=40, fs=8.5)
    # thermal-centre markers
    for el, c in [(EL_FUEL_MID, "#b5009b"), (EL_SG_MID, "#b5009b")]:
        ax.plot([0, Rv_o + 780], [el, el], color=c, lw=0.5, ls="--", zorder=1)

    ax.set_xlim(xL - 950, Rv_o + 1400)
    ax.set_ylim(-300, EL_PZR_TOP + 400)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("AEGIS-40  •  SHEET 2 — LONGITUDINAL HALF-SECTION\n"
                 "37-FA integral iPWR  •  height & OTSG fit  •  H_th preserved at 2.85 m  •  dims mm",
                 fontsize=12, fontweight="bold")
    fig.savefig(os.path.join(OUT, "ga37_sheet2_axial.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


# =============================================================================== SHEET 3: core map
def sheet3():
    fig, ax = plt.subplots(figsize=(12, 12))
    n = 7
    c = (n - 1) / 2.0
    ring_col = {0: "#7a1f1f", 1: "#b23b3b", 2: "#e08a5a", 3: "#f0c987"}
    ring_lab = {0: "centre 4.95", 1: "ring1 4.70", 2: "ring2 4.40", 3: "edge 4.0 wt%"}
    gd_w = {0: 1.65, 1: 1.45, 2: 0.95, 3: 0.68}

    def ring_of(i, j):
        return int(min(max(abs(i - c), abs(j - c)), 3))

    for i in range(n):
        for j in range(n):
            if CORE_MAP[i, j] == 0:
                continue
            x = (j - c) * FA_PITCH
            y = (c - i) * FA_PITCH
            r = ring_of(i, j)
            ax.add_patch(Rectangle((x - FA_PITCH / 2, y - FA_PITCH / 2), FA_PITCH * 0.97,
                         FA_PITCH * 0.97, facecolor=ring_col[r], ec="#222", lw=1.0))
            ax.text(x, y + 42, f"R{r}", ha="center", va="center", fontsize=8,
                    color="white", fontweight="bold")
            ax.text(x, y + 4, f"Gd×{gd_w[r]:.2f}", ha="center", va="center", fontsize=6.5, color="white")
            if CR_MAP[i, j] == 1:
                ax.add_patch(Circle((x, y - 52), 30, facecolor="#111", ec="white", lw=1.0))
                ax.text(x, y - 52, "CRA", ha="center", va="center", fontsize=5.5, color="white")
            else:
                ax.text(x, y - 52, "instr" if (i == 3 and j == 3) else "", ha="center",
                        va="center", fontsize=6, color="white")

    # octagon outline + across-flats / equiv-Ø
    half = R_FUEL_FLAT
    ax.add_patch(Circle((0, 0), 1483 / 2, fill=False, ec="#1c6dd0", ls="--", lw=1.2))
    ax.text(0, 1483 / 2 + 30, "equivalent Ø1483", color="#1c6dd0", ha="center", fontsize=8)
    ax.add_patch(Circle((0, 0), R_BARREL_I, fill=False, ec="#555", ls=":", lw=1.0))
    ax.text(R_BARREL_I * 0.7, -R_BARREL_I * 0.72, "barrel ID Ø1900", color="#555", fontsize=8)
    dim_h(ax, -half, half, -half - 130, "across flats 1512 (7 × 216.04)", off=20, fs=9)

    # legend
    from matplotlib.patches import Patch
    items = [Patch(facecolor=ring_col[k], ec="#222", label=ring_lab[k]) for k in range(4)]
    items.append(Circle((0, 0), 1, facecolor="#111", ec="white", label="12 CRA clusters"))
    ax.legend(handles=items, loc="upper right", fontsize=8.5, framealpha=0.95,
              title="Enrichment ring  /  Gd ring-weight")

    ax.set_xlim(-half - 320, half + 320)
    ax.set_ylim(-half - 320, half + 260)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("AEGIS-40  •  SHEET 3 — CORE LOADING MAP (37 FA, 7×7 octagon)\n"
                 "intra-FA enrichment grade + radial Gd ring-zoning  •  12 CRA (central FA = instrument)",
                 fontsize=12, fontweight="bold")
    fig.savefig(os.path.join(OUT, "ga37_sheet3_coremap.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    sheet1()
    sheet2()
    sheet3()
    print("wrote 3 sheets to", OUT)
    for f in sorted(os.listdir(OUT)):
        print("  ", f)
