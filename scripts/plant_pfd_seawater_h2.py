"""Aegis-40 iPWR — seawater-cooled polygeneration PFD (FER Figure 8.9-1).

Canonical balance-of-plant for the Aegis-40 polygeneration plant at the Sinop
coastal site: SEAWATER once-through cooling to the Black Sea, a THERMOCHEMICAL
sorption store (zeolite-13X / water) that supplies DISTRICT HEATING as a loss-free,
seasonal-capable co-product, and an off-peak (night-shift) hydrogen electrolyser.
The plant co-produces electricity + hydrogen + district heat.

  * Integral RPV (natural circulation, in-vessel helical OTSG, self-pressurizer)
  * Secondary Rankine cycle: main steam -> HP/MS/LP turbine -> generator
  * Condenser cooled by SEAWATER once-through (intake screens -> outfall)
  * Thermochemical zeolite-13X sorption store: extraction steam charges (regenerates)
    the bed; adsorption discharges 60-90 C heat to the district-heating network
  * Off-peak / night-shift electrolyser H2 co-generation (steam-preheat assisted)

State points from thermo_cycle.py; seawater duty Q=82.6 MWth, cp~3.99 kJ/kg.K,
dT~10 K -> ~2.1 m3/s. Co-product flows are illustrative (site-dependent).
Output: docs/competition/cycle/plant_pfd_seawater_h2.png    Run: py scripts/plant_pfd_seawater_h2.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Rectangle, Circle, Polygon, Ellipse)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cycle")

# ---- palette ----------------------------------------------------------------
C_PRIM = "#c0392b"
C_STEAM = "#e67e22"
C_FEED = "#2471a3"
C_HOT = "#8e2f1c"
C_COLD = "#138d75"
C_SEA = "#1a5276"     # seawater
C_WTR = "#21618c"     # fresh / process water
C_DH = "#ca6f1e"      # district heat
C_ELEC = "#1e8449"
C_H2 = "#7d3c98"
INK = "#222222"
GRY = "#d5d8dc"

fig, ax = plt.subplots(figsize=(20, 12))
ax.set_xlim(0, 140)
ax.set_ylim(0, 86)
ax.axis("off")


# ---- primitives -------------------------------------------------------------
def box(x, y, w, h, label, fc=GRY, ec=INK, fs=9, bold=False, tcol=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.5",
                                fc=fc, ec=ec, lw=1.4, zorder=4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
            color=tcol, fontweight="bold" if bold else "normal", zorder=5)


def tag(x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontsize=7, color="#566573",
            fontweight="bold", zorder=6)


def label(x, y, t, col=INK, fs=7.5, ha="center", style="normal"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=col, style=style, zorder=7,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.9))


def pipe(pts, col, lw=2.4, ls="-", arrow=True):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=2,
            solid_capstyle="round", solid_joinstyle="round")
    if arrow:
        x0, y0 = pts[-2]
        x1, y1 = pts[-1]
        ax.annotate("", xy=(x1, y1), xytext=((x0 + x1) / 2.0, (y0 + y1) / 2.0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw,
                                    shrinkA=0, shrinkB=0), zorder=2)


def tee(x, y, col):
    ax.add_patch(Circle((x, y), 0.5, fc=col, ec=col, zorder=3))


def turbine(x, y, w, h, label_t, tg):
    pts = [(x, y + h * 0.28), (x, y + h * 0.72), (x + w, y + h), (x + w, y)]
    ax.add_patch(Polygon(pts, closed=True, fc="#aeb6bf", ec=INK, lw=1.6, zorder=4))
    ax.text(x + w / 2, y + h / 2, label_t, ha="center", va="center", fontsize=8.5,
            fontweight="bold", zorder=5)
    tag(x + w / 2, y - 1.6, tg)


def pump(x, y, tg, col=C_FEED, r=1.5):
    ax.add_patch(Circle((x, y), r, fc="white", ec=col, lw=1.8, zorder=5))
    ax.add_patch(Polygon([(x - r * 0.5, y - r * 0.5), (x - r * 0.5, y + r * 0.5),
                          (x + r * 0.7, y)], closed=True, fc=col, ec=col, zorder=6))
    tag(x, y - r - 1.2, tg)


def tank(x, y, w, h, name, fc, sub):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.4, alpha=0.9, zorder=4))
    ax.add_patch(Ellipse((x + w / 2, y + h), w, h * 0.18, fc=fc, ec=INK, lw=1.4, zorder=4))
    ax.add_patch(Ellipse((x + w / 2, y), w, h * 0.18, fc=fc, ec=INK, lw=1.4, zorder=4))
    ax.text(x + w / 2, y + h * 0.62, name, ha="center", va="center", fontsize=8,
            fontweight="bold", color="white", zorder=5)
    ax.text(x + w / 2, y + h * 0.40, sub, ha="center", va="center", fontsize=7,
            color="white", zorder=5)


def hx(x, y, w, h, name, tg, fc="#d6eaf8"):
    box(x, y, w, h, "", fc=fc)
    for i in range(4):
        yy = y + h * (i + 0.5) / 4
        ax.plot([x + 0.8, x + w - 0.8], [yy, yy], color="#5d6d7e", lw=0.9, zorder=5)
    ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=7.5,
            fontweight="bold", zorder=6)
    tag(x + w / 2, y - 1.6, tg)


def valve(x, y, tg="", s=1.0, col=INK):
    ax.add_patch(Polygon([(x - s, y - s), (x - s, y + s), (x, y)], closed=True, fc="white", ec=col, lw=1.3, zorder=6))
    ax.add_patch(Polygon([(x + s, y - s), (x + s, y + s), (x, y)], closed=True, fc="white", ec=col, lw=1.3, zorder=6))
    if tg:
        ax.text(x, y + s + 1.1, tg, ha="center", va="bottom", fontsize=6.8, color="#566573", zorder=6)


def sea(x, y, w, h):
    """Open-sea heat sink — wavy-top water body."""
    n = 200
    xs = np.linspace(x, x + w, n)
    ytop = y + h - 1.0 + 0.6 * np.sin((xs - x) * 1.3)
    verts = list(zip(xs, ytop)) + [(x + w, y), (x, y)]
    ax.add_patch(Polygon(verts, closed=True, fc=C_SEA, ec=INK, lw=1.3, alpha=0.85, zorder=3))
    for k in range(3):
        yy = y + h * (0.25 + 0.22 * k)
        ax.plot(xs, yy + 0.35 * np.sin((xs - x) * 1.6 + k), color="white",
                lw=1.0, alpha=0.45, zorder=4)
    ax.text(x + w / 2, y + h * 0.35, "SEA", ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=5)
    tag(x + w / 2, y - 1.6, "ultimate heat sink")


def gen(x, y, r=3.0):
    ax.add_patch(Circle((x, y), r, fc="#f9e79f", ec=INK, lw=1.7, zorder=5))
    ax.text(x, y, "G", ha="center", va="center", fontsize=15, fontweight="bold", zorder=6)
    tag(x, y - r - 1.3, "GEN")


# ============================================================================
# frame + title
# ============================================================================
ax.add_patch(Rectangle((2, 2), 136, 82, fill=False, ec=INK, lw=1.6))
ax.text(4, 81.3, "AEGIS-40 iPWR  —  Seawater-Cooled Polygeneration Plant PFD",
        fontsize=15, fontweight="bold")
ax.text(4, 78.4, "125 MWth  →  40.0 MWe net (η = 32.0 %)   ·   co-products: electricity + hydrogen + district heat   ·   "
        "seawater once-through cooling  +  thermochemical sorption store", fontsize=9.5, color="#555")

# ============================================================================
# 1. INTEGRAL RPV
# ============================================================================
ax.add_patch(FancyBboxPatch((6, 26), 14, 40, boxstyle="round,pad=0.1,rounding_size=6",
             fc="#fbeee6", ec=C_PRIM, lw=2.2, zorder=3))
box(8, 28, 10, 6, "Core", fc="#f5b7b1", fs=8.5, bold=True)
hx(8, 39, 10, 10, "helical\nOTSG", "", fc="#fadbd8")
box(9.5, 57, 7, 6, "self-\npressurizer", fc="#f6ddcc", fs=6.8)
ax.plot([13, 13], [34, 39], color=C_PRIM, lw=1.6, zorder=3)
ax.plot([13, 13], [49, 57], color=C_PRIM, lw=1.6, zorder=3)
tag(13, 24.4, "RPV  (R-1)")
ax.text(13, 22.6, "natural circulation\n12.8 MPa · 308→258 °C",
        ha="center", va="center", fontsize=6.8, color=C_PRIM, style="italic", zorder=6)

# ============================================================================
# 2. STEAM HEADER -> HP -> MS -> LP -> GENERATOR
# ============================================================================
pipe([(13, 66), (13, 73), (59, 73)], C_STEAM, lw=2.8)
valve(44, 73, "TCV", col=C_STEAM)
label(34, 74.6, "main-steam header  4.5 MPa · 296 °C · 57.8 kg/s", col=C_STEAM, fs=8)
turbine(60, 69, 8, 7, "HP\nturbine", "HP-T")
box(69, 70.5, 4, 5, "MS", fc="#d4e6f1", fs=8, bold=True); tag(71, 69.0, "MS-1")
turbine(74, 68, 10, 9, "LP\nturbine", "LP-T")
pipe([(68, 72.5), (69, 72.5)], C_STEAM, lw=2.4, arrow=False)
pipe([(73, 72.5), (74, 72.5)], C_STEAM, lw=2.4, arrow=False)
ax.plot([84, 87.5], [72.5, 72.5], color=INK, lw=3.0, zorder=3)        # shaft
gen(90.5, 72.5)
pipe([(93.5, 72.5), (104, 72.5)], C_ELEC, lw=2.4)
label(99, 74.0, "to grid", col=C_ELEC, fs=8)

# ============================================================================
# 3. CONDENSER + SEAWATER ONCE-THROUGH
# ============================================================================
pipe([(79, 68), (79, 60)], C_STEAM, lw=2.4)
label(83.5, 64, "x = 0.892", col=C_STEAM, fs=7.5)
box(71, 54, 17, 6, "Condenser   7 kPa · 39 °C", fc="#d6eaf8", fs=8.5, bold=True)
tag(79.5, 52.4, "COND  (E-1)   Q = 82.6 MWth")
sea(117, 34, 18, 18)
# cold seawater intake: sea -> screens/pump -> condenser
box(108, 36, 7, 4.5, "intake\nscreens", fc="#d4e6f1", fs=6.8); tag(111.5, 34.6, "SCR-1")
pipe([(117, 38), (115, 38)], C_SEA, lw=2.4, arrow=False)
pipe([(108, 38), (101, 38), (101, 50), (90, 50), (90, 55), (88, 55)], C_SEA, lw=2.4)
pump(96, 38, "SWP", col=C_SEA)
label(99, 51.4, "cold seawater  ~18 °C · 2.1 m³/s", col=C_SEA, fs=7)
# warm seawater outfall: condenser -> sea
pipe([(88, 57), (104, 57), (104, 48), (122, 48), (122, 50)], C_SEA, lw=2.4)
label(112, 58.4, "warm outfall  ~28 °C  (ΔT 10 K)", col=C_SEA, fs=7)

# ============================================================================
# 4. REGENERATIVE FEEDWATER TRAIN
# ============================================================================
pump(79, 47, "CP", col=C_FEED)                                       # condensate pump
pipe([(79, 54), (79, 48.5)], C_FEED, lw=2.2, arrow=False)
pipe([(79, 45.5), (79, 44), (70, 44)], C_FEED, lw=2.2)
box(60, 41, 10, 6, "Deaerator", fc="#d4efdf", fs=8); tag(65, 39.4, "FWH-2 (DA)")
pump(56, 44, "BP", col=C_FEED)
pipe([(60, 44), (57.5, 44)], C_FEED, lw=2.2, arrow=False)
pipe([(54.5, 44), (52, 44)], C_FEED, lw=2.2)
box(42, 41, 10, 6, "FWH-1", fc="#d4efdf", fs=8); tag(47, 39.4, "HP heater")
pump(38, 44, "FP", col=C_FEED)
pipe([(42, 44), (39.5, 44)], C_FEED, lw=2.2, arrow=False)
pipe([(36.5, 44), (24, 44), (24, 38), (20, 38)], C_FEED, lw=2.2)
label(30, 45.4, "feedwater  4.5 MPa · 181 °C", col=C_FEED, fs=7.5)
# extractions
pipe([(64, 69), (64, 49.5), (47, 49.5), (47, 47)], C_STEAM, lw=1.5, ls=(0, (4, 3)))
label(55.5, 50.8, "HP extr. 1.0 MPa", col=C_STEAM, fs=6.8)
pipe([(77, 68), (77, 49.5), (65, 49.5), (65, 47)], C_STEAM, lw=1.5, ls=(0, (4, 3)))
label(71, 50.8, "extr. 0.15 MPa", col=C_STEAM, fs=6.8)
tee(64, 73, C_STEAM)

# ============================================================================
# 5. THERMOCHEMICAL SORPTION STORE + DISTRICT HEATING
# ============================================================================
ax.add_patch(Rectangle((28, 7), 80, 23, fill=False, ec=C_HOT, lw=1.2, ls=(0, (6, 4)), zorder=1))
ax.text(29.5, 28.4, "Thermochemical sorption store  (zeolite-13X / water)  +  district heating",
        fontsize=8.5, fontweight="bold", color=C_HOT)
# charge: turbine extraction regenerates (dries) the bed
valve(33, 70.5, "EXV", col=C_STEAM)
tee(33, 73, C_STEAM)
pipe([(33, 73), (33, 25)], C_STEAM, lw=1.8, ls=(0, (5, 3)))
label(33, 34, "extraction ~1.5 MPa\n200 °C  (charge)", col=C_STEAM, fs=6.6)
pipe([(33, 25), (38, 19)], C_STEAM, lw=1.8, ls=(0, (5, 3)), arrow=False)
# sorbent bed
box(38, 13, 16, 11, "zeolite-13X\nsorption bed\n~390 t", fc="#f6ddcc", fs=7.6, tcol=C_HOT)
tag(46, 11.4, "TCS-1")
# desorbed water back to cycle
pipe([(50, 13), (50, 9.5)], C_FEED, lw=1.5, ls=(0, (3, 3)))
label(50, 8.4, "desorbed H₂O → condensate", col=C_FEED, fs=6.2)
# discharge: adsorption heat to district-heat HX
pipe([(54, 18.5), (60, 18.5)], C_DH, lw=2.2)
label(57, 20.6, "adsorption heat\n60–90 °C", col=C_DH, fs=6.2)
hx(60, 13, 12, 11, "district-\nheat HX", "E-2", fc="#fdebd0")
# district heating network
box(78, 13, 22, 9, "district heating\nnetwork  (Sinop)", fc="#fef5e7", fs=8.0, tcol=C_DH)
tag(89, 11.4, "DH-1")
pipe([(72, 20), (78, 20)], C_DH, lw=2.2); label(75, 21.4, "supply", col=C_DH, fs=6.2)
pipe([(78, 15), (72, 15)], C_DH, lw=1.6, ls=(0, (4, 3)), arrow=False)
label(75, 13.6, "return", col=C_DH, fs=6.2)
ax.text(89, 24.8, "loss-free · seasonal storage", ha="center", fontsize=6.6,
        color=C_HOT, style="italic", zorder=6)

# ============================================================================
# 7. HYDROGEN CO-GENERATION
# ============================================================================
box(98, 63, 16, 10, "electrolyser\n(off-peak / night-shift)", fc="#ebdef0", fs=8.0, tcol=C_H2)
tag(106, 61.4, "EL-1")
pipe([(100, 72.5), (100, 73)], C_ELEC, lw=2.0); tee(100, 72.5, C_ELEC)
label(100, 70, "off-peak power", col=C_ELEC, fs=6.8)
pipe([(50, 73), (50, 76.2), (102, 76.2), (102, 73)], C_STEAM, lw=1.6, ls=(0, (4, 3)))
label(78, 76.2, "steam tap → feed preheat (HTSE assist)", col=C_STEAM, fs=6.8)
tee(50, 73, C_STEAM)
pipe([(114, 68), (119, 68)], C_H2, lw=2.4)
box(119, 64, 13, 8, "H₂ storage\n/ export", fc="#f4ecf7", fs=8, tcol=C_H2)

# ============================================================================
# legend + title block
# ============================================================================
legends = [("primary coolant", C_PRIM), ("main / extraction steam", C_STEAM),
           ("condensate / feedwater", C_FEED), ("district heat", C_DH),
           ("seawater", C_SEA), ("electricity", C_ELEC), ("hydrogen", C_H2)]
ax.text(4, 7.0, "LEGEND", fontsize=8, fontweight="bold")
for i, (t, c) in enumerate(legends):
    xx = 4 + (i % 3) * 27
    yy = 5.2 - (i // 3) * 1.7
    ax.plot([xx, xx + 2.6], [yy, yy], color=c, lw=3, solid_capstyle="round")
    ax.text(xx + 3.1, yy, t, fontsize=7.0, va="center")

ax.add_patch(Rectangle((110, 2.5), 27.5, 7.5, fill=False, ec=INK, lw=1.2))
ax.plot([110, 137.5], [6.0, 6.0], color=INK, lw=0.8)
ax.plot([124, 124], [2.5, 6.0], color=INK, lw=0.8)
ax.text(111, 8.4, "Aegis-40 iPWR — Polygeneration BoP", fontsize=8, fontweight="bold")
ax.text(111, 6.7, "Seawater + sorption store + H₂ + district heat", fontsize=6.6)
ax.text(111, 4.6, "Drawing", fontsize=6.5, color="#777")
ax.text(111, 3.3, "PFD-8.9-001", fontsize=8, fontweight="bold")
ax.text(125, 4.6, "Scale", fontsize=6.5, color="#777")
ax.text(125, 3.3, "NTS  ·  Fig 8.9-1", fontsize=8, fontweight="bold")

out = os.path.join(OUT, "plant_pfd_seawater_h2.png")
fig.savefig(out, dpi=170, bbox_inches="tight")
print("wrote", out)
