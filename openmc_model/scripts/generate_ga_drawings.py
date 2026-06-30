"""Aegis-40 iPWR — engineering General-Arrangement (GA) drawing set.

Generates orthographic, dimensioned reference sheets for building the integral RPV in
Creo Parametric 11. Geometry constants are the SAME as the CAD scripts (generate_rpv_step /
core / fa), expressed in plant elevation EL (mm) where EL = model_z + 2641.5 (EL 0 = lower-head
outer pole = DATUM B). DATUM A = vessel axis (x = 0).

Sheets (docs/competition/cad/ga/):
  ga_sheet1_longitudinal.png   front + right-side half-cutaway longitudinal sections (+ rear note)
  ga_sheet2_sections.png       transverse sections A-A core, B-B steam generator, C-C pressuriser
  ga_sheet3_plan_crdm.png      top (plan) view, bottom view, CRDM layout
  ga_sheet4_exploded.png       exploded assembly (12 parts) + parts list
  ga_sheet5_flow_location.png  internal flow path + component location + pump config A/B

Run:  py scripts/generate_ga_drawings.py     (matplotlib only)
"""
import math
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, FancyArrowPatch, Wedge

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cad", "ga")
os.makedirs(OUT, exist_ok=True)

INK = "#1a1a1a"; GRY = "#9aa0a6"; RED = "#b5462e"; BLU = "#2471a3"
ORG = "#d6892b"; GRN = "#1e8449"; STL = "#c7ccd1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

# ---- geometry in EL (mm) ----------------------------------------------------
SHIFT = 2641.5
R_IN, R_OUT, WALL = 1400.0, 1560.0, 160.0
EL_CYL_BOT, EL_CYL_TOP, EL_DOME = 1560.0, 8760.0, 10320.0
SKIRT_T_R, SKIRT_B_R = 1560.0, 1890.0
EL_SKIRT_TOP, EL_SKIRT_BOT, EL_BASE = 2510.0, 1480.0, 1390.0
EL_DIST = (1710.0, 1780.0); DIST_R = 840.0
EL_LCP = (2280.0, 2360.0); EL_UCP = (4960.0, 5040.0); PLATE_R = 760.0
EL_CORE_BOT, EL_AF_BOT, EL_AF_MID, EL_AF_TOP, EL_CORE_TOP = 2360.0, 2660.0, 3660.0, 4660.0, 4960.0
REFL_R, BARREL_R = 740.1, 770.1; FUEL_R = 600.0
RISER_RO, RISER_RI = 560.0, 530.0; EL_RISER_TOP = 7960.0
EL_SG = (5210.0, 7810.0); SG_SHROUD_R = 1180.0
SG_LAYER = (665.0, 750.0, 835.0, 920.0, 1005.0, 1075.0); SG_TUBE_R = 17.0
TS_RO, TS_RI = 1100.0, 630.0
EL_FW, EL_MS, NOZ_R, NOZ_X1 = 5410.0, 7610.0, 130.0, 1880.0
PZR_RO, PZR_RI = 470.0, 430.0; EL_PZR = (10070.0, 11170.0); EL_PZR_TOP = 11640.0
PZR_HEAT_RING, PZR_HEAT_R = 250.0, 26.0; SURGE_R = 70.0; EL_SURGE = (8660.0, 10070.0)
CRDM_HR, CRDM_LR, CRDM_RR = 70.0, 98.0, 28.0
EL_CRDM = (4910.0, 5810.0); EL_LATCH = (5810.0, 6130.0); EL_ROD_TOP = 7430.0; EL_MNT = (6130.0, 6230.0)

# 21-assembly core map (mm) from cad/core_map.csv ; ring r0/r1/r2
CORE = [(-216.04,432.08,'r2'),(0,432.08,'r2'),(216.04,432.08,'r2'),(-432.08,216.04,'r2'),
        (-216.04,216.04,'r1'),(0,216.04,'r1'),(216.04,216.04,'r1'),(432.08,216.04,'r2'),
        (-432.08,0,'r2'),(-216.04,0,'r1'),(0,0,'r0'),(216.04,0,'r1'),(432.08,0,'r2'),
        (-432.08,-216.04,'r2'),(-216.04,-216.04,'r1'),(0,-216.04,'r1'),(216.04,-216.04,'r1'),
        (432.08,-216.04,'r2'),(-216.04,-432.08,'r2'),(0,-432.08,'r2'),(216.04,-432.08,'r2')]
RINGC = {'r0':'#c0392b','r1':'#e67e22','r2':'#f4d03f'}

# =====================================================================
#  drafting helpers
# =====================================================================

def dim_v(ax, x, z0, z1, txt, tx=None, fs=7):
    """vertical dimension between EL z0,z1 with witness lines to x."""
    tx = x if tx is None else tx
    ax.annotate("", (x, z0), (x, z1), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
    ax.text(x + 40, (z0 + z1) / 2, txt, rotation=90, va="center", ha="left",
            fontsize=fs, color=INK, bbox=dict(fc="white", ec="none", pad=0.4))

def wit(ax, xa, z, xb):
    ax.plot([xa, xb], [z, z], color=GRY, lw=0.5, zorder=1)

def dim_h(ax, z, x0, x1, txt, tz=None, fs=7):
    tz = z if tz is None else tz
    ax.annotate("", (x0, z), (x1, z), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
    ax.text((x0 + x1) / 2, z + 50, txt, va="bottom", ha="center", fontsize=fs, color=INK,
            bbox=dict(fc="white", ec="none", pad=0.4))

def cl_v(ax, z0, z1, x=0):
    ax.plot([x, x], [z0, z1], color=BLU, lw=0.7, ls=(0, (8, 3, 1, 3)), zorder=1)

def cl_h(ax, x0, x1, z):
    ax.plot([x0, x1], [z, z], color=BLU, lw=0.6, ls=(0, (8, 3, 1, 3)), zorder=1)

def leader(ax, x, z, tx, tz, txt, fs=7, ha="left"):
    ax.annotate(txt, (x, z), (tx, tz), fontsize=fs, ha=ha, va="center", color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.6),
                bbox=dict(fc="white", ec=GRY, lw=0.4, pad=0.6))

def balloon(ax, x, z, n, tx, tz, fs=8):
    ax.annotate("", (x, z), (tx, tz), arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
    ax.add_patch(Circle((tx, tz), 95, fc="white", ec=INK, lw=1.0, zorder=6))
    ax.text(tx, tz, str(n), ha="center", va="center", fontsize=fs, fontweight="bold", zorder=7)

def sec_mark(ax, z, x0, x1, label):
    ax.plot([x0, x1], [z, z], color=INK, lw=1.4, ls=(0, (12, 3)))
    for xx, dd in ((x0, -1), (x1, 1)):
        ax.annotate("", (xx + dd * 260, z), (xx, z), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
        ax.text(xx + dd * 300, z, label, fontsize=9, fontweight="bold",
                ha="left" if dd > 0 else "right", va="center")

def hatch_poly(ax, pts, fc="none", hatch="////", ec=INK, lw=1.1, z=3, alpha=1):
    ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, hatch=hatch, lw=lw,
                         zorder=z, alpha=alpha))

def title_block(ax, num, title, scale="NTS", sheet="1/5"):
    x0, y0, w, h = ax.get_xlim()[0], ax.get_ylim()[0], 0, 0
    # placed by each sheet via axes coords
    ax.text(0.995, 0.012,
            f"AEGIS-40 iPWR  ·  {title}\nDWG {num}   SCALE {scale}   SHEET {sheet}   "
            f"DIMS mm   DATUM A=axis  B=EL0\nGENERAL ARRANGEMENT — reference for Creo Parametric 11",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5,
            bbox=dict(fc="#f4f6f7", ec=INK, lw=1.0, pad=0.6), family="monospace")

def frame(ax, title, sub=""):
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(0.006, 0.992, title, transform=ax.transAxes, ha="left", va="top",
            fontsize=14, fontweight="bold", color=INK)
    if sub:
        ax.text(0.006, 0.968, sub, transform=ax.transAxes, ha="left", va="top",
                fontsize=8.5, color="#555")

# vessel profile point sets ---------------------------------------------------
def profile(R):
    t = np.linspace(0, np.pi / 2, 40)
    low = np.column_stack([R * np.sin(t), EL_CYL_BOT - R * np.cos(t)])
    up = np.column_stack([R * np.cos(t), EL_CYL_TOP + R * np.sin(t)])
    cyl = np.array([[R, EL_CYL_BOT], [R, EL_CYL_TOP]])
    return np.vstack([low, cyl, up])

# =====================================================================
#  SHEET 1 — longitudinal half-cutaway sections (front + right-side)
# =====================================================================

def band(ax, x_in, x_out, z0, z1, fc, ec=INK, lw=0.9, hatch=None, label=None, lx=None):
    """left-half radial band (drawn at negative x)."""
    ax.add_patch(Rectangle((-x_out, z0), x_out - x_in, z1 - z0, fc=fc, ec=ec, lw=lw,
                           hatch=hatch, zorder=3))

def draw_section(ax, nozzle_in_plane=True):
    out = profile(R_OUT); inn = profile(R_IN)
    # outer profile (both halves) – external view on right, section edge on left
    ax.plot(out[:, 0], out[:, 1], color=INK, lw=1.6)
    ax.plot(-out[:, 0], out[:, 1], color=INK, lw=1.6)
    # left-half pressure-boundary wall = hatched
    wall = np.vstack([np.column_stack([-out[:, 0], out[:, 1]]),
                      np.column_stack([-inn[::-1, 0], inn[::-1, 1]])])
    hatch_poly(ax, wall, hatch="////", lw=1.4, z=2)
    ax.plot(-inn[:, 0], inn[:, 1], color=INK, lw=1.0)
    cl_v(ax, -2750, EL_PZR_TOP + 250)

    # ---- left-half internals (axis .. wall) by elevation ----
    # lower plenum / distributor
    band(ax, 0, DIST_R, EL_DIST[0], EL_DIST[1], "#aeb6bf")
    # lower core plate
    band(ax, 0, PLATE_R, EL_LCP[0], EL_LCP[1], "#9aa0a6")
    # core barrel + reflector + fuel (core region)
    band(ax, REFL_R, BARREL_R, EL_CORE_BOT, EL_CORE_TOP, "#7f8c8d")          # barrel
    band(ax, FUEL_R, REFL_R, EL_CORE_BOT, EL_CORE_TOP, "#d5dbdb")            # reflector
    band(ax, 0, FUEL_R, EL_AF_BOT, EL_AF_TOP, "#cde7d2", ec=GRN)            # active fuel
    # axial reflector slices
    band(ax, 0, FUEL_R, EL_CORE_BOT, EL_AF_BOT, "#eaf2ec", ec=GRY)
    band(ax, 0, FUEL_R, EL_AF_TOP, EL_CORE_TOP, "#eaf2ec", ec=GRY)
    for zz in (EL_AF_BOT, EL_AF_MID, EL_AF_TOP):
        ax.plot([-FUEL_R, 0], [zz, zz], color=GRN, lw=0.5, ls=":")
    # upper core plate
    band(ax, 0, PLATE_R, EL_UCP[0], EL_UCP[1], "#9aa0a6")
    # riser (hot leg)
    band(ax, RISER_RI, RISER_RO, EL_CORE_TOP, EL_RISER_TOP, "#8896a0")       # riser wall
    band(ax, 0, RISER_RI, EL_CORE_TOP, EL_RISER_TOP, "#dfe7ee", ec=RED)      # riser bore
    # SG region: shroud + tube layers
    band(ax, SG_SHROUD_R - 10, SG_SHROUD_R, EL_SG[0], EL_SG[1], "#7fb3c4")   # shroud
    for r in SG_LAYER:
        ax.add_patch(Rectangle((-r - SG_TUBE_R, EL_SG[0]), 2 * SG_TUBE_R, EL_SG[1] - EL_SG[0],
                               fc="#e08e3c", ec=ORG, lw=0.5, zorder=4))
    # tube sheets
    band(ax, TS_RI, TS_RO, EL_SG[0] - 120, EL_SG[0], "#6e7b87")
    band(ax, TS_RI, TS_RO, EL_SG[1], EL_SG[1] + 120, "#6e7b87")
    # CRDM (in-vessel, over core)
    for (a, b, r, c) in ((EL_CRDM[0], EL_CRDM[1], CRDM_HR, "#aab2b8"),
                         (EL_LATCH[0], EL_LATCH[1], CRDM_LR, "#8c949b"),
                         (EL_CORE_TOP, EL_ROD_TOP, CRDM_RR, "#5d6d7e")):
        for off in (0, -216.04, 216.04):
            ax.add_patch(Rectangle((-off - r, a), 2 * r, b - a, fc=c, ec=INK, lw=0.5, zorder=5))
    band(ax, 0, PLATE_R, EL_MNT[0], EL_MNT[1], "#95a5a6")                    # CRDM mount plate
    # pressuriser
    band(ax, PZR_RI, PZR_RO, EL_PZR[0], EL_PZR[1], "#8c949b")
    band(ax, 0, PZR_RI, EL_PZR[0], EL_PZR[1], "#dfe3e6", ec=INK)
    ax.add_patch(Wedge((0, EL_PZR[1]), PZR_RO, 90, 180, width=PZR_RO - PZR_RI, fc="#8c949b", ec=INK, lw=0.8, zorder=4))
    for s in (1, -1):  # heaters
        ax.add_patch(Rectangle((-PZR_HEAT_RING - PZR_HEAT_R, EL_PZR[0] + 40), 2 * PZR_HEAT_R, 800,
                               fc=RED, ec=INK, lw=0.4, zorder=5))
        break
    band(ax, 0, SURGE_R, EL_SURGE[0], EL_SURGE[1], "#dfe3e6", ec=BLU)        # surge line

    # downcomer arrows (cold leg) on far left
    for zz in np.linspace(3000, 7600, 5):
        ax.annotate("", (-1300, zz - 300), (-1300, zz), arrowprops=dict(arrowstyle="-|>", color=BLU, lw=1.2))
    ax.text(-1300, 8000, "downcomer\n(cold leg ↓)", color=BLU, ha="center", fontsize=7)
    ax.annotate("", (-280, 6600), (-280, 7200), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.text(-280, 7350, "riser\n(hot leg ↑)", color=RED, ha="center", fontsize=7)

    # ---- right-half EXTERNAL features ----
    # support skirt
    hatch_poly(ax, [(SKIRT_T_R, EL_SKIRT_TOP), (SKIRT_B_R, EL_SKIRT_BOT),
                    (SKIRT_B_R + 60, EL_BASE), (SKIRT_B_R - 90, EL_BASE), (R_OUT, EL_SKIRT_TOP)],
               hatch="\\\\", lw=1.0, z=2)
    ax.add_patch(Rectangle((SKIRT_B_R - 90, EL_BASE - 90), 240, 90, fc="#7f8c8d", ec=INK, lw=1.0, zorder=3))
    # nozzles (feedwater +, steam -) – on this view in-plane
    nz = [(EL_FW, BLU, "FW"), (EL_MS, RED, "MS")]
    for elz, c, _ in nz:
        ax.add_patch(Rectangle((R_OUT - 20, elz - NOZ_R), NOZ_X1 - R_OUT + 20, 2 * NOZ_R,
                               fc=c, ec=INK, lw=0.8, zorder=4, alpha=0.85))
    # flange
    ax.add_patch(Rectangle((-1800, EL_CYL_TOP - 130), 3600, 260, fc="#b3b6b7", ec=INK, lw=1.0, zorder=4))
    # lifting lugs
    for s in (1, -1):
        ax.add_patch(Rectangle((s * (R_OUT - 10), 8500), s * 200, 180, fc="#95a5a6", ec=INK, lw=0.8, zorder=4))

    # ---- ELEVATION dimension stack (far right) ----
    XD = 3050
    chain = [(0, "EL 0  lower head pole"), (EL_BASE, "1390 skirt base / support"),
             (EL_CYL_BOT, "1560 lower tangent"), (EL_CORE_BOT, "2360 core bottom"),
             (EL_AF_BOT, "2660 active fuel ↓"), (EL_AF_TOP, "4660 active fuel ↑"),
             (EL_CORE_TOP, "4960 core top"), (EL_SG[0], "5210 SG bottom"),
             (EL_FW, "5410 feedwater CL"), (EL_MS, "7610 main-steam CL"),
             (EL_SG[1], "7810 SG top"), (EL_RISER_TOP, "7960 riser top"),
             (EL_CYL_TOP, "8760 shell top / flange"), (EL_DOME, "10320 closure head"),
             (EL_PZR[0], "10070 pzr body"), (EL_PZR_TOP, "11640 pzr dome top")]
    for z, t in chain:
        wit(ax, 0, z, XD)
        ax.plot(XD, z, ">", color=INK, ms=3)
        ax.text(XD + 60, z, t, fontsize=6.6, va="center")
    ax.annotate("", (XD, 0), (XD, EL_PZR_TOP), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
    ax.text(XD - 70, EL_PZR_TOP / 2, "OVERALL  ≈ 11 640", rotation=90, va="center", ha="right", fontsize=7)

    # ---- radial dims at core level ----
    zc = 2160
    for r, lbl in ((R_OUT, "Ø3120 OD"), (R_IN, "Ø2800 ID")):
        wit(ax, -r, zc, -r); ax.plot([-r, -r], [zc, zc - 250], color=GRY, lw=0.5)
    dim_h(ax, zc - 350, -R_OUT, 0, "R1560 (Ø3120 OD)")
    dim_h(ax, zc - 620, -R_IN, 0, "R1400 (Ø2800 ID)")
    dim_h(ax, zc - 890, -BARREL_R, 0, "R770 barrel")
    # section indicators
    sec_mark(ax, EL_AF_MID, -R_OUT - 350, R_OUT + 350, "A")
    sec_mark(ax, (EL_SG[0] + EL_SG[1]) / 2, -R_OUT - 350, R_OUT + 350, "B")
    sec_mark(ax, (EL_PZR[0] + EL_PZR[1]) / 2, -PZR_RO - 350, PZR_RO + 1500, "C")

    # component labels (leaders, right side internals labels on left)
    L = [(-FUEL_R/2, EL_AF_MID, -2500, 3660, "REACTOR CORE\n21 FA · active 2000"),
         (-REFL_R, 4300, -2500, 4500, "radial reflector / baffle"),
         (-BARREL_R, 4750, -2500, 5100, "core barrel Ø1540"),
         (-RISER_RI/2, 6600, -2500, 6300, "core-outlet RISER Ø1120"),
         (-SG_LAYER[3], 6500, 2400, 6500, "helical-coil OTSG\n6 layers R665–1075"),
         (-SG_SHROUD_R, 5600, -2500, 5650, "SG shroud Ø2360"),
         (-1480, 5000, -2500, 4850, "downcomer annulus"),
         (-PZR_RI/2, 10620, 1700, 10620, "self-PRESSURISER\nØ940 · heaters ×8"),
         (-SURGE_R, 9300, -2500, 9300, "surge line Ø140"),
         (-216, 5400, -2500, 5500, "in-vessel CRDM ×9"),
         (DIST_R/2, EL_DIST[0]+20, 2200, 1745, "flow distributor"),
         (PLATE_R/2, EL_LCP[0]+20, 2200, 2320, "lower core plate"),
         (NOZ_X1-200, EL_FW, 2300, 5410, "feedwater nozzle Ø260"),
         (NOZ_X1-200, EL_MS, 2300, 7610, "main-steam nozzle Ø260"),
         (SKIRT_B_R, EL_SKIRT_BOT+150, 2300, 1800, "support skirt"),
         (0, EL_DOME, -2500, 10320, "upper closure head")]
    for x, z, tx, tz, t in L:
        leader(ax, x, z, tx, tz, t, fs=6.6, ha="left" if tx > x else "right")


def sheet1():
    fig, axs = plt.subplots(1, 2, figsize=(20, 18))
    titles = ["FRONT VIEW — half-cutaway longitudinal section (nozzles in plane)",
              "RIGHT-SIDE VIEW — half-cutaway longitudinal section (nozzles ⟂, lugs in plane)"]
    for ax, ti, inplane in zip(axs, titles, (True, False)):
        frame(ax, "")
        draw_section(ax, inplane)
        ax.text(0.5, 0.995, ti, transform=ax.transAxes, ha="center", va="top", fontsize=11, fontweight="bold")
        ax.set_xlim(-4200, 4200); ax.set_ylim(-2900, 12100)
    axs[1].text(0.5, 0.04,
                "REAR VIEW: identical external outline to FRONT, mirrored; nozzles hidden (dashed), "
                "lifting lugs & instrument penetrations at 180°. Vessel is axisymmetric about DATUM A.",
                transform=axs[1].transAxes, ha="center", fontsize=8,
                bbox=dict(fc="#fff7e6", ec=ORG, lw=0.8))
    title_block(axs[0], "GA-001", "Longitudinal Sections", sheet="1/5")
    fig.suptitle("AEGIS-40 iPWR  —  REACTOR VESSEL GENERAL ARRANGEMENT  —  SHEET 1 of 5",
                 fontsize=15, fontweight="bold", y=0.998)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    p = os.path.join(OUT, "ga_sheet1_longitudinal.png"); fig.savefig(p, dpi=120, bbox_inches="tight"); plt.close(fig)
    print("wrote", p)

# =====================================================================
#  SHEET 2 — transverse sections A-A, B-B, C-C
# =====================================================================

def ring_dim(ax, r, txt, ang=45, fs=7):
    a = math.radians(ang)
    ax.annotate("", (0, 0), (r * math.cos(a), r * math.sin(a)),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7))
    ax.text(r * 0.5 * math.cos(a), r * 0.5 * math.sin(a) + 30, txt, fontsize=fs,
            ha="center", bbox=dict(fc="white", ec="none", pad=0.4))

def sec_core(ax):
    frame(ax, "SECTION A–A", "core region · EL 3660")
    ax.add_patch(Circle((0, 0), R_OUT, fc="none", ec=INK, lw=1.6))
    ax.add_patch(Circle((0, 0), R_IN, fc="#eef2f3", ec=INK, lw=1.0))
    ax.add_patch(Wedge((0, 0), R_OUT, 0, 360, width=WALL, fc="none", ec=INK, hatch="////", lw=0.8))
    ax.add_patch(Circle((0, 0), BARREL_R, fc="#dfe3e6", ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), REFL_R, fc="#eaf2ec", ec=GRY, lw=0.8))
    for x, y, ring in CORE:
        ax.add_patch(Rectangle((x - 100, y - 100), 200, 200, fc=RINGC[ring], ec=INK, lw=0.6, zorder=4))
        if ring in ("r0", "r1"):  # CRDM clusters
            ax.add_patch(Circle((x, y), 38, fc="white", ec=INK, lw=0.6, zorder=5))
    cl_h(ax, -R_OUT - 200, R_OUT + 200, 0); cl_v(ax, -R_OUT - 200, R_OUT + 200)
    ring_dim(ax, R_OUT, "R1560", 35); ring_dim(ax, R_IN, "R1400", 20)
    ring_dim(ax, BARREL_R, "R770 barrel", 125); ring_dim(ax, REFL_R, "R740 refl", 160)
    ax.text(0, -R_OUT - 380, "downcomer = R770→R1400  ·  FA pitch 216.04  ·  21 assemblies (1/8/12)",
            ha="center", fontsize=7)
    ax.text(R_IN*0.62, R_IN*0.62, "downcomer", fontsize=7, color=BLU)
    ax.set_xlim(-2000, 2000); ax.set_ylim(-2050, 1950)

def sec_sg(ax):
    frame(ax, "SECTION B–B", "steam-generator region · EL 6510")
    ax.add_patch(Circle((0, 0), R_OUT, fc="none", ec=INK, lw=1.6))
    ax.add_patch(Wedge((0, 0), R_OUT, 0, 360, width=WALL, fc="none", ec=INK, hatch="////", lw=0.8))
    ax.add_patch(Circle((0, 0), R_IN, fc="#eef2f3", ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), SG_SHROUD_R, fc="#eaf6f9", ec=BLU, lw=1.0))
    for r in SG_LAYER:
        n = max(8, int(2 * math.pi * r / SG_PITCH_DEG(r)))
        for k in range(n):
            a = 2 * math.pi * k / n
            ax.add_patch(Circle((r * math.cos(a), r * math.sin(a)), SG_TUBE_R * 2.2,
                                fc="#e08e3c", ec=ORG, lw=0.3, zorder=4))
    ax.add_patch(Circle((0, 0), RISER_RO, fc="#fdece7", ec=RED, lw=1.0, zorder=5))
    ax.add_patch(Circle((0, 0), RISER_RI, fc="#fbe0d6", ec=RED, lw=0.6, zorder=5))
    # nozzles
    ax.add_patch(Rectangle((R_OUT - 20, -NOZ_R), 360, 2 * NOZ_R, fc=BLU, ec=INK, lw=0.8, zorder=6))
    ax.add_patch(Rectangle((-R_OUT - 340, -NOZ_R), 360, 2 * NOZ_R, fc=RED, ec=INK, lw=0.8, zorder=6))
    ax.text(R_OUT + 360, 0, "FW", color=BLU, fontsize=8, va="center")
    ax.text(-R_OUT - 360, 0, "MS", color=RED, fontsize=8, va="center", ha="right")
    cl_h(ax, -R_OUT - 200, R_OUT + 200, 0); cl_v(ax, -R_OUT - 200, R_OUT + 200)
    ring_dim(ax, SG_SHROUD_R, "R1180 shroud", 60); ring_dim(ax, RISER_RO, "R560 riser", 250)
    ring_dim(ax, R_IN, "R1400 ID", 18)
    ax.text(0, -R_OUT - 380, "6 helical layers R665–1075 · tube OD34 · primary over tubes ↓ · steam in tubes ↑",
            ha="center", fontsize=7)
    ax.set_xlim(-2100, 2100); ax.set_ylim(-2050, 1950)

def SG_PITCH_DEG(r):
    return 230.0  # axial pitch reused as approx circumferential spacing for the section view

def sec_pzr(ax):
    frame(ax, "SECTION C–C", "pressuriser region · EL 10620")
    ax.add_patch(Circle((0, 0), PZR_RO, fc="#eef2f3", ec=INK, lw=1.6))
    ax.add_patch(Wedge((0, 0), PZR_RO, 0, 360, width=PZR_RO - PZR_RI, fc="none", ec=INK, hatch="////", lw=0.8))
    for k in range(8):
        a = 2 * math.pi * k / 8
        ax.add_patch(Circle((PZR_HEAT_RING * math.cos(a), PZR_HEAT_RING * math.sin(a)),
                            PZR_HEAT_R * 2.0, fc=RED, ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Circle((0, 0), SURGE_R, fc="#dfe3e6", ec=BLU, lw=0.8, zorder=5))
    cl_h(ax, -PZR_RO - 150, PZR_RO + 150, 0); cl_v(ax, -PZR_RO - 150, PZR_RO + 150)
    ring_dim(ax, PZR_RO, "R470", 40); ring_dim(ax, PZR_HEAT_RING, "R250 heater PCD", 135)
    ax.text(0, -PZR_RO - 180, "8 heater rods Ø52 on Ø500 PCD · surge line Ø140 on axis · wall 40",
            ha="center", fontsize=7)
    ax.set_xlim(-750, 750); ax.set_ylim(-780, 700)

def sheet2():
    fig, axs = plt.subplots(1, 3, figsize=(22, 9))
    sec_core(axs[0]); sec_sg(axs[1]); sec_pzr(axs[2])
    title_block(axs[2], "GA-002", "Transverse Sections", sheet="2/5")
    fig.suptitle("AEGIS-40 iPWR  —  TRANSVERSE SECTIONS A-A / B-B / C-C  —  SHEET 2 of 5",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(OUT, "ga_sheet2_sections.png"); fig.savefig(p, dpi=130, bbox_inches="tight"); plt.close(fig)
    print("wrote", p)

# =====================================================================
#  SHEET 3 — plan (top), bottom, CRDM layout
# =====================================================================

def top_view(ax):
    frame(ax, "TOP VIEW (plan)", "closure head · looking down")
    ax.add_patch(Circle((0, 0), R_OUT, fc="#f4f6f7", ec=INK, lw=1.6))
    ax.add_patch(Circle((0, 0), 1800, fc="none", ec=GRY, lw=0.8, ls=":"))  # flange bolt circle
    for k in range(24):
        a = 2 * math.pi * k / 24
        ax.add_patch(Circle((1800 * math.cos(a), 1800 * math.sin(a)), 45, fc="white", ec=INK, lw=0.6))
    ax.add_patch(Circle((0, 0), PZR_RO, fc="#dfe3e6", ec=INK, lw=1.2))  # pzr dome footprint
    ax.text(0, 0, "PZR", ha="center", va="center", fontsize=8, fontweight="bold")
    # CRDM penetrations over core map (r0,r1)
    for x, y, ring in CORE:
        if ring in ("r0", "r1"):
            ax.add_patch(Circle((x, y), CRDM_LR, fc="#aab2b8", ec=INK, lw=0.7, zorder=4))
    # nozzles & lugs clocking
    ax.add_patch(Rectangle((R_OUT - 20, -NOZ_R), 340, 2*NOZ_R, fc=BLU, ec=INK, lw=0.8)); ax.text(R_OUT+360,0,"FW 0°",color=BLU,va="center",fontsize=7)
    ax.add_patch(Rectangle((-R_OUT - 320, -NOZ_R), 340, 2*NOZ_R, fc=RED, ec=INK, lw=0.8)); ax.text(-R_OUT-360,0,"MS 180°",color=RED,va="center",ha="right",fontsize=7)
    for a, t in ((90, "lug"), (210, "lug"), (330, "lug")):
        aa = math.radians(a); ax.add_patch(Rectangle((R_OUT*math.cos(aa)-90, R_OUT*math.sin(aa)-90), 180,180, fc="#95a5a6", ec=INK, lw=0.7))
    cl_h(ax, -R_OUT-250, R_OUT+250, 0); cl_v(ax, -R_OUT-250, R_OUT+250)
    ring_dim(ax, R_OUT, "R1560", 50); ring_dim(ax, 1800, "bolt PCD R1800", 15)
    ax.text(0, -R_OUT-360, "24 closure studs · 9 CRDM penetrations (central+inner ring) · nozzles 0°/180°",
            ha="center", fontsize=7)
    ax.set_xlim(-2300, 2300); ax.set_ylim(-2150, 2050)

def bottom_view(ax):
    frame(ax, "BOTTOM VIEW", "lower head + support skirt · looking up")
    ax.add_patch(Circle((0, 0), SKIRT_B_R + 60, fc="#eef2f3", ec=INK, lw=1.4))  # skirt base ring
    ax.add_patch(Circle((0, 0), SKIRT_B_R - 90, fc="white", ec=INK, lw=1.0))
    ax.add_patch(Circle((0, 0), R_OUT, fc="none", ec=GRY, lw=0.8, ls="--"))      # head OD proj
    ax.add_patch(Circle((0, 0), 120, fc="#95a5a6", ec=INK, lw=0.8))             # drain nozzle
    ax.text(0, 180, "drain Ø80", ha="center", fontsize=6.5)
    for a in (45, 135, 225, 315):  # support pads
        aa = math.radians(a); X, Y = (SKIRT_B_R) * math.cos(aa), (SKIRT_B_R) * math.sin(aa)
        ax.add_patch(Rectangle((X-160, Y-110), 320, 220, fc="#7f8c8d", ec=INK, lw=0.8))
        ax.text(X*1.32, Y*1.32, "pad", ha="center", va="center", fontsize=6.5)
    cl_h(ax, -SKIRT_B_R-250, SKIRT_B_R+250, 0); cl_v(ax, -SKIRT_B_R-250, SKIRT_B_R+250)
    ring_dim(ax, SKIRT_B_R+60, "R1950 base", 50); ring_dim(ax, R_OUT, "R1560 head", 20)
    ax.text(0, -SKIRT_B_R-360, "4 support pads @45/135/225/315° · central drain nozzle", ha="center", fontsize=7)
    ax.set_xlim(-2300, 2300); ax.set_ylim(-2250, 2050)

def crdm_layout(ax):
    frame(ax, "CRDM LAYOUT", "9 drive units over central + inner-ring assemblies")
    ax.add_patch(Circle((0, 0), R_IN, fc="#f7f9fa", ec=GRY, lw=0.8, ls=":"))
    for x, y, ring in CORE:
        ax.add_patch(Rectangle((x-108, y-108), 216, 216, fc="#eef2f3", ec=GRY, lw=0.5))
        if ring in ("r0", "r1"):
            ax.add_patch(Circle((x, y), CRDM_HR, fc="#aab2b8", ec=INK, lw=0.9, zorder=4))
            ax.add_patch(Circle((x, y), CRDM_RR, fc="#5d6d7e", ec=INK, lw=0.6, zorder=5))
    leader(ax, 0, 0, 900, 900, "central cluster (r0)\nØ140 housing / Ø56 rod", fs=7)
    leader(ax, 216.04, 0, 1100, -700, "inner-ring clusters ×8 (r1)", fs=7)
    cl_h(ax, -1300, 1300, 0); cl_v(ax, -1300, 1300)
    dim_h(ax, -700, 0, 216.04, "216.04 pitch")
    ax.text(0, -1150, "9 CRDM units · housing Ø140 · latch Ø196 · drive rod Ø56 · in-vessel (no head penetration)",
            ha="center", fontsize=7)
    ax.set_xlim(-1500, 1500); ax.set_ylim(-1400, 1300)

def sheet3():
    fig, axs = plt.subplots(1, 3, figsize=(22, 9))
    top_view(axs[0]); bottom_view(axs[1]); crdm_layout(axs[2])
    title_block(axs[2], "GA-003", "Plan / Bottom / CRDM", sheet="3/5")
    fig.suptitle("AEGIS-40 iPWR  —  PLAN, BOTTOM & CRDM LAYOUT  —  SHEET 3 of 5",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(OUT, "ga_sheet3_plan_crdm.png"); fig.savefig(p, dpi=130, bbox_inches="tight"); plt.close(fig)
    print("wrote", p)

# =====================================================================
#  SHEET 4 — exploded assembly + parts list
# =====================================================================

EXPLODE = [
    (1, "Vessel lower head", "Ø3120 / Ø2800 · R1560 hemi"),
    (2, "Lower support structure + flow distributor", "Ø1680 · t70"),
    (3, "Lower core support plate", "Ø1520 · t80"),
    (4, "Core assembly (21 FA)", "env Ø1200 · active 2000"),
    (5, "Reflector + baffle assembly", "Ø1480 / Ø1200"),
    (6, "Core barrel", "Ø1540 / Ø1480 · t30"),
    (7, "Upper core plate + guide structure", "Ø1520 · t80"),
    (8, "Core-outlet riser", "Ø1120 / Ø1060 · L3000"),
    (9, "Steam-generator assembly (OTSG)", "shroud Ø2360 · H2600"),
    (10, "Pressuriser plate + body", "Ø940 / Ø860 · H1100"),
    (11, "Pressuriser dome", "R470 hemi"),
    (12, "CRDM assembly ×9 + closure head", "head Ø3120 · CRDM Ø140"),
]

def sheet4():
    fig, ax = plt.subplots(figsize=(13, 26)); frame(ax, "EXPLODED ASSEMBLY VIEW",
                                                     "stacked on DATUM A · 12 separable Creo parts")
    n = len(EXPLODE); gap = 1.0
    widths = [3120, 1680, 1520, 1200, 1480, 1540, 1520, 1120, 2360, 940, 940, 3120]
    heights = [1560, 350, 200, 2000, 2600, 2680, 300, 3000, 2840, 1100, 470, 1700]
    z = 0
    for (num, name, dim), w, h in zip(EXPLODE, widths, heights):
        hh = max(h, 600) * 0.45
        ww = w * 0.5
        ax.add_patch(Rectangle((-ww, z), 2 * ww, hh, fc="#eef2f3", ec=INK, lw=1.2, zorder=3))
        cl_v(ax, z - 250, z + hh + 250)
        balloon(ax, ww, z + hh / 2, num, ww + 900, z + hh / 2)
        ax.text(ww + 1050, z + hh / 2, f"{name}", fontsize=8.5, va="center", fontweight="bold")
        ax.text(ww + 1050, z + hh / 2 - 220, dim, fontsize=7, va="center", color="#555")
        z += hh + 850
    ax.annotate("", (0, -300), (0, z - 600), arrowprops=dict(arrowstyle="-", color=BLU, lw=0.8, ls=":"))
    ax.text(0, z + 200, "assembly axis = DATUM A", ha="center", color=BLU, fontsize=8)
    title_block(ax, "GA-004", "Exploded Assembly", sheet="4/5")
    ax.set_xlim(-3500, 4800); ax.set_ylim(-700, z + 700)
    fig.suptitle("AEGIS-40 iPWR  —  EXPLODED ASSEMBLY  —  SHEET 4 of 5", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.99])
    p = os.path.join(OUT, "ga_sheet4_exploded.png"); fig.savefig(p, dpi=120, bbox_inches="tight"); plt.close(fig)
    print("wrote", p)

# =====================================================================
#  SHEET 5 — internal flow path + component location + pump config
# =====================================================================

def flow_path(ax):
    frame(ax, "INTERNAL FLOW PATH", "natural circulation (Config A)")
    out = profile(R_OUT); ax.plot(out[:,0], out[:,1], color=INK, lw=1.3); ax.plot(-out[:,0], out[:,1], color=INK, lw=1.3)
    ax.add_patch(Rectangle((-FUEL_R, EL_AF_BOT), 2*FUEL_R, EL_AF_TOP-EL_AF_BOT, fc="#cde7d2", ec=GRN, lw=1)); ax.text(0, EL_AF_MID, "CORE", ha="center", fontsize=8, fontweight="bold")
    ax.add_patch(Rectangle((-RISER_RI, EL_CORE_TOP), 2*RISER_RI, EL_RISER_TOP-EL_CORE_TOP, fc="#fdece7", ec=RED, lw=1)); ax.text(0, 6600, "RISER", ha="center", fontsize=7, rotation=90)
    for r in (SG_LAYER[1], SG_LAYER[4]):
        ax.add_patch(Rectangle((-r-SG_TUBE_R, EL_SG[0]), 2*SG_TUBE_R, EL_SG[1]-EL_SG[0], fc="#e08e3c", ec=ORG, lw=0.5))
        ax.add_patch(Rectangle((r-SG_TUBE_R, EL_SG[0]), 2*SG_TUBE_R, EL_SG[1]-EL_SG[0], fc="#e08e3c", ec=ORG, lw=0.5))
    ax.text(900, 6500, "OTSG", fontsize=7, color=ORG)
    # hot (up) red arrows core->riser->sg top
    for z in np.linspace(EL_AF_MID, EL_RISER_TOP-300, 6):
        ax.annotate("", (0, z+350), (0, z), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.annotate("", (820, 7600), (820, 5400), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5))
    ax.text(560, 7750, "primary ↓ over SG tubes", fontsize=6.5, color=RED)
    # cold (down) blue arrows downcomer
    for z in np.linspace(7400, 2700, 6):
        ax.annotate("", (-1320, z-450), (-1320, z), arrowprops=dict(arrowstyle="-|>", color=BLU, lw=2))
    ax.text(-1320, 7700, "downcomer ↓", color=BLU, ha="center", fontsize=7)
    ax.annotate("", (-700, 2150), (700, 2150), arrowprops=dict(arrowstyle="-|>", color=BLU, lw=1.5))
    ax.text(0, 1950, "lower plenum → core inlet", ha="center", color=BLU, fontsize=6.5)
    # secondary
    ax.annotate("", (R_OUT+250, EL_FW), (900, EL_FW), arrowprops=dict(arrowstyle="-|>", color=BLU, lw=1.5)); ax.text(R_OUT+280, EL_FW, "feedwater in", color=BLU, fontsize=7, va="center")
    ax.annotate("", (900, EL_MS), (R_OUT+250, EL_MS), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5)); ax.text(R_OUT+280, EL_MS, "steam out", color=RED, fontsize=7, va="center")
    cl_v(ax, 0, EL_DOME)
    ax.text(0, 600, "Δz core↔SG ≈ 2.85 m\ndrives natural circulation", ha="center", fontsize=7,
            bbox=dict(fc="#eafaf1", ec=GRN, lw=0.7))
    ax.set_xlim(-2700, 2700); ax.set_ylim(0, EL_DOME+300)

def location(ax):
    frame(ax, "COMPONENT LOCATION", "key components vs elevation (EL mm)")
    items = [("Pressuriser dome", 11400, RED), ("Pressuriser body + heaters", 10600, RED),
             ("Closure head + flange", 9000, "#555"), ("Riser top / SG top", 7900, ORG),
             ("Main-steam nozzle", 7610, RED), ("Steam generator (OTSG)", 6500, ORG),
             ("Feedwater nozzle", 5410, BLU), ("Upper core plate / CRDM mount", 5000, "#555"),
             ("Active fuel (core)", 3660, GRN), ("Lower core plate", 2320, "#555"),
             ("Flow distributor / lower plenum", 1745, BLU), ("Lower head + skirt support", 700, "#555")]
    for name, el, c in items:
        ax.plot([0, 1.2], [el, el], color=c, lw=1.2)
        ax.plot(0, el, "o", color=c, ms=5)
        ax.text(1.35, el, f"EL {int(el)}  —  {name}", va="center", fontsize=8, color=INK)
    ax.annotate("", (0, 0), (0, 12000), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    ax.text(-0.25, 6000, "ELEVATION (DATUM B = EL 0)", rotation=90, va="center", fontsize=8)
    ax.set_xlim(-0.6, 7); ax.set_ylim(-300, 12300)

def pump_cfg(ax):
    frame(ax, "PUMP CONFIGURATION OPTIONS", "A natural circ (baseline) · B with RCPs")
    # A
    ax.text(0.25, 0.95, "A — NATURAL CIRCULATION (reference)", transform=ax.transAxes, fontweight="bold", ha="center", color=GRN)
    ax.text(0.25, 0.5,
            "• no pumps, no shaft seals\n• no pump penetration in\n  pressure boundary\n• loop driven by core↔SG\n  thermal-centre offset 2.85 m\n• simplest, safest",
            transform=ax.transAxes, ha="center", fontsize=8,
            bbox=dict(fc="#eafaf1", ec=GRN, lw=1))
    # B
    ax.text(0.75, 0.95, "B — REACTOR COOLANT PUMPS (alternate)", transform=ax.transAxes, fontweight="bold", ha="center", color=BLU)
    ax.text(0.75, 0.5,
            "• 2–4 canned-motor RCPs\n  in downcomer, Ø600×1400\n• glandless, primary-cooled\n• closure-head penetration\n  Ø650 + Ø900 motor pull\n• adds Δp → higher flow",
            transform=ax.transAxes, ha="center", fontsize=8,
            bbox=dict(fc="#eaf2f8", ec=BLU, lw=1))
    ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)

def sheet5():
    fig = plt.figure(figsize=(22, 13))
    ax1 = fig.add_axes([0.02, 0.06, 0.30, 0.88]); flow_path(ax1)
    ax2 = fig.add_axes([0.36, 0.40, 0.62, 0.54]); location(ax2)
    ax3 = fig.add_axes([0.36, 0.05, 0.62, 0.30]); pump_cfg(ax3)
    title_block(ax3, "GA-005", "Flow Path / Location / Pumps", sheet="5/5")
    fig.suptitle("AEGIS-40 iPWR  —  INTERNAL FLOW PATH, COMPONENT LOCATION & PUMP OPTIONS  —  SHEET 5 of 5",
                 fontsize=14, fontweight="bold")
    p = os.path.join(OUT, "ga_sheet5_flow_location.png"); fig.savefig(p, dpi=130, bbox_inches="tight"); plt.close(fig)
    print("wrote", p)

if __name__ == "__main__":
    sheet1(); sheet2(); sheet3(); sheet4(); sheet5()
    print("GA drawing set complete →", OUT)
