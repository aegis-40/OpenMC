"""Aegis-40 integrated plant process-flow diagram (PFD) for FER Figure 8.9-1.

Technical-style PFD with orthogonal (right-angle) pipe routing, equipment tags,
a drawing border and title block. Shows the full energy-conversion + integrated
systems circuit on one sheet:
  * Integral RPV (natural circulation, in-vessel helical OTSG, self-pressurizer)
  * Secondary Rankine cycle: main-steam header + TCVs, HP turbine, moisture
    separator, LP turbine, generator, condenser, cooling tower, and the
    regenerative feedwater train (condensate pump, deaerator, booster pump,
    FWH-1, main feed pump) with turbine extractions
  * Two-tank sensible-heat TES (charge + discharge): TES bypass valves, IHX,
    hot/cold thermal-fluid (Therminol-66) tanks, transfer pumps, discharge boiler
  * SOE hydrogen co-generation off the generator + a steam tap; district heating

State-point numbers are the design point from thermo_cycle.py; TES sizing scaled
from Frick et al. (INL/JOU-17-43134). Output: docs/competition/cycle/plant_pfd.png
Run:  py scripts/plant_pfd.py
"""

import os
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
C_CW = "#5dade2"
C_ELEC = "#1e8449"
C_H2 = "#7d3c98"
C_DH = "#b9770e"
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


def cooling_tower(x, y, w, h):
    cx = x + w / 2
    n = 22
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        hw = (w / 2) * (0.55 + 0.45 * (2 * t - 1) ** 2)
        L.append((cx - hw, y + h * t)); R.append((cx + hw, y + h * t))
    ax.add_patch(Polygon(L + R[::-1], closed=True, fc="#dfe3e6", ec=INK, lw=1.5, zorder=4))
    ax.add_patch(Ellipse((cx, y + h), w * 0.55, h * 0.05, fc="#cfd4d7", ec=INK, lw=1.1, zorder=5))
    ax.text(cx, y + h * 0.5, "Cooling\nTower", ha="center", va="center",
            fontsize=8.5, fontweight="bold", zorder=5)
    tag(cx, y - 1.6, "CT-1")


def gen(x, y, r=3.0):
    ax.add_patch(Circle((x, y), r, fc="#f9e79f", ec=INK, lw=1.7, zorder=5))
    ax.text(x, y, "G", ha="center", va="center", fontsize=15, fontweight="bold", zorder=6)
    tag(x, y - r - 1.3, "GEN")


# ============================================================================
# frame + title
# ============================================================================
ax.add_patch(Rectangle((2, 2), 136, 82, fill=False, ec=INK, lw=1.6))
ax.text(4, 81.3, "AEGIS-40 iPWR  —  Integrated Plant Process Flow Diagram",
        fontsize=15, fontweight="bold")
ax.text(4, 78.4, "125 MWth  →  40.0 MWe net  (η = 32.0 %)   ·   secondary Rankine cycle  +  "
        "two-tank thermal energy storage  +  SOE hydrogen co-generation", fontsize=9.5, color="#555")

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
pipe([(93.5, 72.5), (106, 72.5)], C_ELEC, lw=2.4)
label(101, 74.0, "to grid  40 MWe", col=C_ELEC, fs=8)

# ============================================================================
# 3. CONDENSER + COOLING TOWER
# ============================================================================
pipe([(79, 68), (79, 60)], C_STEAM, lw=2.4)
label(83.5, 64, "x = 0.892", col=C_STEAM, fs=7.5)
box(71, 54, 17, 6, "Condenser   7 kPa · 39 °C", fc="#d6eaf8", fs=8.5, bold=True)
tag(79.5, 52.4, "COND  (E-1)   Q = 82.6 MWth")
cooling_tower(116, 38, 16, 24)
pipe([(88, 57), (116, 57)], C_CW, lw=2.2); label(102, 58.4, "warm", col=C_CW, fs=7)
pipe([(116, 42), (90, 42), (90, 55), (88, 55)], C_CW, lw=2.2)
pump(101, 42, "CWP", col=C_CW); label(108, 43.4, "cooled", col=C_CW, fs=7)

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
# 5. TWO-TANK THERMAL ENERGY STORAGE
# ============================================================================
ax.add_patch(Rectangle((28, 7), 74, 23, fill=False, ec=C_HOT, lw=1.2, ls=(0, (6, 4)), zorder=1))
ax.text(29.5, 28.4, "Thermal Energy Storage  (two-tank sensible heat · Therminol-66)",
        fontsize=8.5, fontweight="bold", color=C_HOT)
# bypass-steam tap from header
valve(33, 70.5, "TBV ×4", col=C_STEAM)
pipe([(33, 73), (33, 26)], C_STEAM, lw=1.8, ls=(0, (5, 3)))
label(33, 33, "≤45 % steam\n≈26 kg/s", col=C_STEAM, fs=6.6)
tee(33, 73, C_STEAM)
hx(30, 15, 10, 10, "IHX", "E-2")
tank(45, 12, 8, 13, "Cold", C_COLD, "205 °C"); tag(49, 10.6, "TK-C")
tank(58, 12, 8, 13, "Hot", C_HOT, "260 °C"); tag(62, 10.6, "TK-H")
box(72, 14, 10, 10, "TES\ndischarge\nboiler", fc="#fcf3cf", fs=7.5); tag(77, 12.4, "E-3")
# charge: cold -> pump -> IHX (below) ; IHX -> hot (above)
pipe([(48, 12), (48, 10), (35, 10), (35, 15)], C_COLD, lw=2.0); pump(42, 10, "P-C", col=C_COLD)
pipe([(35, 25), (35, 27.5), (61, 27.5), (61, 25)], C_HOT, lw=2.0)
label(48, 27.5, "charge", col=C_HOT, fs=6.8)
# discharge: hot -> pump -> boiler ; boiler -> cold (below)
pipe([(66, 20), (72, 20)], C_HOT, lw=2.0); pump(69, 20, "P-H", col=C_HOT)
pipe([(78, 14), (78, 9), (49, 9), (49, 12)], C_COLD, lw=2.0)
label(63, 9, "discharge", col=C_COLD, fs=6.8)
# IHX condensate drain -> condenser (off-page connector)
pipe([(40, 18), (43, 18)], C_FEED, lw=1.5, ls=(0, (3, 3)))
label(47.5, 18, "→ condenser", col=C_FEED, fs=6.4, ha="left")
# discharge process steam -> header (off-page connector)
pipe([(77, 24), (77, 31)], C_STEAM, lw=1.8, ls=(0, (5, 3)))
label(77, 32.3, "process steam → cycle", col=C_STEAM, fs=6.6)
# district heating
pipe([(82, 18), (88, 18)], C_DH, lw=2.0)
box(88, 14, 11, 8, "District\nheating", fc="#fdf2e0", fs=8, tcol=C_DH)

# ============================================================================
# 6. SOE HYDROGEN CO-GENERATION
# ============================================================================
box(98, 63, 16, 10, "SOE electrolyser\n(solid-oxide)", fc="#ebdef0", fs=8.5, tcol=C_H2)
tag(106, 61.4, "SOE-1")
pipe([(100, 72.5), (100, 73)], C_ELEC, lw=2.0); tee(100, 72.5, C_ELEC)
label(104, 70, "off-peak power", col=C_ELEC, fs=6.8)
pipe([(50, 73), (50, 76.2), (106, 76.2), (106, 73)], C_STEAM, lw=1.6, ls=(0, (4, 3)))
label(82, 76.2, "steam tap → high-temperature electrolysis", col=C_STEAM, fs=6.8)
tee(50, 73, C_STEAM)
pipe([(114, 68), (119, 68)], C_H2, lw=2.4)
box(119, 64, 11, 8, "H₂\nstorage", fc="#f4ecf7", fs=8, tcol=C_H2)

# ============================================================================
# legend + title block
# ============================================================================
legends = [("primary coolant", C_PRIM), ("main / extraction steam", C_STEAM),
           ("condensate / feedwater", C_FEED), ("hot thermal fluid (Therminol-66)", C_HOT),
           ("cold thermal fluid", C_COLD), ("cooling water", C_CW),
           ("electricity", C_ELEC), ("hydrogen", C_H2), ("district heat", C_DH)]
ax.text(4, 7.0, "LEGEND", fontsize=8, fontweight="bold")
for i, (t, c) in enumerate(legends):
    xx = 4 + (i % 3) * 30
    yy = 5.2 - (i // 3) * 1.7
    ax.plot([xx, xx + 2.6], [yy, yy], color=c, lw=3, solid_capstyle="round")
    ax.text(xx + 3.1, yy, t, fontsize=7.2, va="center")

ax.add_patch(Rectangle((110, 2.5), 27.5, 7.5, fill=False, ec=INK, lw=1.2))
ax.plot([110, 137.5], [6.0, 6.0], color=INK, lw=0.8)
ax.plot([124, 124], [2.5, 6.0], color=INK, lw=0.8)
ax.text(111, 8.4, "Aegis-40 iPWR — Balance of Plant", fontsize=8, fontweight="bold")
ax.text(111, 6.7, "Integrated PFD", fontsize=7.5)
ax.text(111, 4.6, "Drawing", fontsize=6.5, color="#777")
ax.text(111, 3.3, "PFD-8.9-001", fontsize=8, fontweight="bold")
ax.text(125, 4.6, "Scale", fontsize=6.5, color="#777")
ax.text(125, 3.3, "NTS  ·  Fig 8.9-1", fontsize=8, fontweight="bold")

out = os.path.join(OUT, "plant_pfd.png")
fig.savefig(out, dpi=170, bbox_inches="tight")
print("wrote", out)
