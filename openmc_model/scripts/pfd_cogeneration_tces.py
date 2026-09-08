"""Aegis-40 — cogeneration PFD: single turbine + IHX-isolated TCES + district heat + H2.

FER §8.9 figure. Tells the integration story the design committee asked for:
  * ONE single tandem-compound turbine-generator (HP+LP on one shaft) — the
    conventional SMR arrangement, drawn so HP+LP cannot be misread as two turbines.
  * The thermochemical store (TCES) sits OUTSIDE the nuclear island as a non-safety
    auxiliary, coupled through an INTERMEDIATE HEAT EXCHANGER (IHX): HP-extraction
    steam charges the store via the IHX; there is no chemical/water-quality path
    back into the reactor steam cycle.
  * Discharge delivers reaction heat to a SEPARATE district-heating water loop
    (90/45 C). Store = ammine NiCl2-SrCl2/NH3 (primary) or zeolite-13X (ammonia-free).
  * Off-peak electricity drives an SOE electrolyser for H2 (4 h/night valley,
    ~140 nights/yr outside the heating season -> ~120 t H2/yr at 213 kg/h).

Numbers from thermo_cycle.py + tces_dh_balance.py.
Output: docs/competition/cycle/pfd_cogeneration_tces.png   Run: py scripts/pfd_cogeneration_tces.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, Ellipse

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cycle")
os.makedirs(OUT, exist_ok=True)

# palette
C_PRIM = "#c0392b"; C_STEAM = "#e67e22"; C_FEED = "#2471a3"
C_CHG = "#7e5109"; C_DH = "#ca6f1e"; C_ELEC = "#1e8449"; C_H2 = "#7d3c98"
INK = "#222222"; GRY = "#d5d8dc"

fig, ax = plt.subplots(figsize=(20, 11.5))
ax.set_xlim(0, 144); ax.set_ylim(0, 90); ax.axis("off")


def box(x, y, w, h, label, fc=GRY, ec=INK, fs=9, bold=False, tcol=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.5",
                                fc=fc, ec=ec, lw=1.4, zorder=4))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs,
            color=tcol, fontweight="bold" if bold else "normal", zorder=5)


def tag(x, y, t):
    ax.text(x, y, t, ha="center", va="center", fontsize=7, color="#566573",
            fontweight="bold", zorder=6)


def label(x, y, t, col=INK, fs=7.5, ha="center"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=fs, color=col, zorder=7,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.9))


def pipe(pts, col, lw=2.4, ls="-", arrow=True):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=2,
            solid_capstyle="round", solid_joinstyle="round")
    if arrow:
        x0, y0 = pts[-2]; x1, y1 = pts[-1]
        ax.annotate("", xy=(x1, y1), xytext=((x0 + x1) / 2, (y0 + y1) / 2),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, shrinkA=0, shrinkB=0), zorder=2)


def tee(x, y, col):
    ax.add_patch(Circle((x, y), 0.5, fc=col, ec=col, zorder=3))


def pump(x, y, tg, col=C_FEED, r=1.5):
    ax.add_patch(Circle((x, y), r, fc="white", ec=col, lw=1.8, zorder=5))
    ax.add_patch(Polygon([(x - r * 0.5, y - r * 0.5), (x - r * 0.5, y + r * 0.5),
                          (x + r * 0.7, y)], closed=True, fc=col, ec=col, zorder=6))
    tag(x, y - r - 1.2, tg)


def hx(x, y, w, h, name, tg, fc="#d6eaf8"):
    box(x, y, w, h, "", fc=fc)
    for i in range(4):
        yy = y + h * (i + 0.5) / 4
        ax.plot([x + 0.8, x + w - 0.8], [yy, yy], color="#5d6d7e", lw=0.9, zorder=5)
    ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=7.5,
            fontweight="bold", zorder=6)
    tag(x + w / 2, y - 1.6, tg)


def turbine(x, y, w, h, label_t):
    pts = [(x, y + h * 0.30), (x, y + h * 0.70), (x + w, y + h), (x + w, y)]
    ax.add_patch(Polygon(pts, closed=True, fc="#aeb6bf", ec=INK, lw=1.6, zorder=4))
    ax.text(x + w / 2, y + h / 2, label_t, ha="center", va="center", fontsize=8.5,
            fontweight="bold", zorder=5)


def gen(x, y, r=3.0):
    ax.add_patch(Circle((x, y), r, fc="#f9e79f", ec=INK, lw=1.7, zorder=5))
    ax.text(x, y, "G", ha="center", va="center", fontsize=15, fontweight="bold", zorder=6)
    tag(x, y - r - 1.3, "GEN")


def tank(x, y, w, h, name, fc, sub, tcol="white"):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.4, alpha=0.92, zorder=4))
    ax.add_patch(Ellipse((x + w / 2, y + h), w, h * 0.16, fc=fc, ec=INK, lw=1.4, zorder=4))
    ax.add_patch(Ellipse((x + w / 2, y), w, h * 0.16, fc=fc, ec=INK, lw=1.4, zorder=4))
    ax.text(x + w / 2, y + h * 0.60, name, ha="center", va="center", fontsize=8.2,
            fontweight="bold", color=tcol, zorder=5)
    ax.text(x + w / 2, y + h * 0.36, sub, ha="center", va="center", fontsize=6.8,
            color=tcol, zorder=5)


# ===================================================================== frame + title
ax.add_patch(Rectangle((2, 2), 140, 86, fill=False, ec=INK, lw=1.6))
ax.text(4, 85.4, "AEGIS-40 iPWR  —  Cogeneration PFD: single turbine + thermochemical store + district heat + H₂",
        fontsize=15, fontweight="bold")
ax.text(4, 82.6, "125 MWth core  →  40.0 MWe (one tandem-compound turbine-generator)   ·   "
        "co-products: district heat (TCES, 90/45 °C) + hydrogen   ·   TCES is a non-safety auxiliary (IHX-isolated)",
        fontsize=9.5, color="#555")

# ===================================================================== nuclear island boundary
ax.add_patch(Rectangle((4.5, 18), 22, 58, fill=False, ec=C_PRIM, lw=1.8, ls=(0, (7, 4)), zorder=1))
ax.text(5.6, 74.6, "NUCLEAR ISLAND  (safety)", fontsize=8.5, fontweight="bold", color=C_PRIM)

# integral RPV
ax.add_patch(FancyBboxPatch((8, 30), 13, 38, boxstyle="round,pad=0.1,rounding_size=5",
             fc="#fbeee6", ec=C_PRIM, lw=2.2, zorder=3))
box(10, 32, 9, 5, "Core", fc="#f5b7b1", fs=8.5, bold=True)
hx(10, 42, 9, 9, "helical\nOTSG", "", fc="#fadbd8")
box(11, 58, 7, 5, "self-\npressurizer", fc="#f6ddcc", fs=6.6)
ax.plot([14.5, 14.5], [37, 42], color=C_PRIM, lw=1.6, zorder=3)
ax.plot([14.5, 14.5], [51, 58], color=C_PRIM, lw=1.6, zorder=3)
tag(14.5, 28.4, "RPV (R-1)  ·  125 MWth")
ax.text(14.5, 22.2, "natural circulation\n12.8 MPa · 308→258 °C", ha="center", va="center",
        fontsize=6.8, color=C_PRIM, style="italic", zorder=6)

# passive heat removal: PRHR HX immersed in the IRWST pool (in-containment, safety)
ax.add_patch(Rectangle((27.5, 58.5), 14.5, 10.5, fill=False, ec=C_PRIM, lw=1.5,
                       ls=(0, (7, 4)), zorder=2))
box(28.5, 60, 12.5, 7.5, "PRHR HX in\nIRWST pool", fc="#d6eaf8", fs=7.4, tcol="#1a5276")
tag(34.7, 57.1, "in-containment passive UHS · ≥72 h grace")
ax.plot([21, 28.5], [66, 66], color=C_PRIM, lw=1.5, ls=(0, (4, 3)), zorder=3)
ax.plot([21, 28.5], [62, 62], color=C_PRIM, lw=1.5, ls=(0, (4, 3)), zorder=3)
label(24.6, 67.6, "PRHR (passive,\nsafety)", col=C_PRIM, fs=6.0)

# ===================================================================== single turbine train
pipe([(14.5, 68), (14.5, 78), (44, 78)], C_STEAM, lw=2.8)
label(30, 79.6, "main steam  4.5 MPa · 296 °C · 57.8 kg/s", col=C_STEAM, fs=8)
# single tandem-compound turbine: HP + LP on ONE shaft, shown inside one boundary
ax.add_patch(Rectangle((45, 67), 27, 13, fill=False, ec=INK, lw=1.2, ls=(0, (3, 2)), zorder=2))
ax.text(58.5, 81.0, "SINGLE tandem-compound turbine-generator  (one shaft, T-1)",
        ha="center", fontsize=7.6, fontweight="bold", color="#34495e")
turbine(46, 70, 8, 7, "HP")
box(55, 71.5, 3.5, 4.5, "MS", fc="#d4e6f1", fs=7.5, bold=True)
turbine(59.5, 69, 9, 9, "LP")
ax.plot([54, 55], [73.5, 73.5], color=C_STEAM, lw=2.4, zorder=3)
ax.plot([58.5, 59.5], [73.5, 73.5], color=C_STEAM, lw=2.4, zorder=3)
ax.plot([68.5, 72], [73.5, 73.5], color=INK, lw=3.0, zorder=3)         # common shaft
gen(75, 73.5)
pipe([(78, 73.5), (90, 73.5)], C_ELEC, lw=2.6)
label(85, 75.2, "40.0 MWe → grid", col=C_ELEC, fs=8.5)
label(85, 71.2, "(≈35.6 MWe while TCES charging; ≈27.6 MWe if SOE also on — night valley only)", col=C_ELEC, fs=6.2)

# ===================================================================== condenser + feedwater
pipe([(64, 69), (64, 60)], C_STEAM, lw=2.4)
box(56, 54, 16, 6, "Condenser  7 kPa · 39 °C", fc="#d6eaf8", fs=8.5, bold=True)
tag(64, 52.4, "COND (E-1)  ·  82.6 MWth → seawater")

# ---- seawater once-through ultimate heat sink (Black Sea, Sinop) -- NOT a cooling tower
C_SEA = "#1f6fb2"
box(74, 53, 16, 8, "SEAWATER sink\nBlack Sea (Sinop)", fc="#d4e6f1", ec=C_SEA, fs=7.6, bold=True, tcol=C_SEA)
ax.text(82, 51.0, "once-through · 2,065 kg/s (2.0 m³/s)\nΔT ≤ 10 K · diffuser → far-field ≤ 0.2 K",
        ha="center", va="center", fontsize=6.2, color=C_SEA, style="italic", zorder=6)
pipe([(72, 58), (74, 58)], C_SEA, lw=2.4)                       # warm outfall  cond -> sea
label(73.0, 59.4, "outfall +10 K", col=C_SEA, fs=6.0)
pipe([(74, 55.5), (72, 55.5)], C_SEA, lw=2.0, ls=(0, (4, 2)))   # cold intake  sea -> cond
label(73.0, 54.4, "intake 8–25 °C", col=C_SEA, fs=6.0)
pump(56, 48, "CP", col=C_FEED)
pipe([(56, 54), (56, 49.5)], C_FEED, lw=2.2, arrow=False)
pipe([(56, 46.5), (56, 45), (50, 45)], C_FEED, lw=2.2)
box(40, 42, 10, 6, "FWH / DA", fc="#d4efdf", fs=8)
pump(36, 45, "FP", col=C_FEED)
pipe([(40, 45), (37.5, 45)], C_FEED, lw=2.2, arrow=False)
pipe([(34.5, 45), (24, 45), (24, 40), (21, 40)], C_FEED, lw=2.2)
label(29, 46.4, "feedwater → OTSG  4.5 MPa", col=C_FEED, fs=7.4)

# ===================================================================== IHX isolation -> TCES auxiliary
# HP INTERMEDIATE-STAGE extraction (stage 14 of 24) -> TCES charge.
# A designed bleed port (NOT inlet steam): an extraction turbine, mechanically
# identical to the regenerative FWH bleeds -> no incremental turbine-life penalty.
tee(50, 70, C_STEAM)
pipe([(50, 70), (50, 38), (86, 38), (86, 37)], C_STEAM, lw=1.9, ls=(0, (5, 3)))
label(62, 39.2, "HP stage-14/24 extraction  1.0 MPa (9 barg) · 180 °C  → TCES charge", col=C_STEAM, fs=7.0)
ax.text(50, 67.8, "bleed @ stage 14/24", ha="center", fontsize=6.0, color=C_STEAM, style="italic", zorder=6)

# TCES auxiliary boundary (non-safety, outside island)
ax.add_patch(Rectangle((78, 6), 60, 30, fill=False, ec=C_CHG, lw=1.5, ls=(0, (6, 4)), zorder=1))
ax.text(79.5, 34.4, "TCES AUXILIARY  (non-safety, outside nuclear island)",
        fontsize=8.5, fontweight="bold", color=C_CHG)

# IHX = isolation boundary between reactor steam and the charge loop
hx(82, 28, 9, 8, "IHX", "E-3", fc="#fdf2e9")
ax.text(86.5, 26.0, "isolation\nboundary", ha="center", fontsize=6.2, color=C_CHG, style="italic", zorder=6)
# charge loop (isolated) IHX -> store
pipe([(91, 33), (98, 33)], C_CHG, lw=2.2)
label(94.5, 34.4, "charge loop\n168 °C (closed)", col=C_CHG, fs=6.3)

# the store (ammine primary; zeolite alternative)
tank(98, 11, 16, 21, "THERMOCHEMICAL\nSTORE  (TCS-1)",
     "#a04000", "REFERENCE: Zeolite-13X / H₂O (NH₃-free)\n1000 t · 1538 m³ · 200 MWh_th\n(compact alt.: ammine NiCl₂-SrCl₂/NH₃ 735 t)",)
ax.text(106, 9.0, "200 MWh_th · loss-free · seasonal-capable", ha="center",
        fontsize=6.4, color=C_CHG, style="italic", zorder=6)
pipe([(98, 30), (91, 30)], C_CHG, lw=1.5, ls=(0, (3, 3)), arrow=False)   # return leg

# discharge -> DH heat exchanger -> district-heat water loop
pipe([(114, 26), (120, 26)], C_DH, lw=2.4)
label(117, 27.6, "discharge\n150 °C", col=C_DH, fs=6.3)
hx(120, 20, 10, 10, "DH HX", "E-4", fc="#fdebd0")
# district heating network (separate water loop 90/45)
box(120, 9, 16, 7, "district heating\nnetwork", fc="#fef5e7", fs=8, tcol=C_DH)
tag(128, 7.4, "DH-1  ·  25 MWth peak")
pipe([(130, 24), (133, 24), (133, 16)], C_DH, lw=2.2)
label(135.5, 20, "supply\n90 °C", col=C_DH, fs=6.2, ha="center")
pipe([(124, 16), (124, 19)], C_DH, lw=1.6, ls=(0, (4, 3)))
label(120.5, 17.5, "return 45 °C\n133 kg/s", col=C_DH, fs=6.0, ha="center")

# ===================================================================== SOE H2 electrolyser
box(96, 58, 18, 9, "SOE electrolyser\n(solid-oxide O²⁻, ~800 °C)", fc="#ebdef0", fs=7.8, tcol=C_H2)
tag(105, 56.4, "EL-1  ·  8 MWe  ·  37.55 kWh/kg (vs PEM 50)")
tee(90, 73.5, C_ELEC)
pipe([(90, 73.5), (90, 67), (96, 67)], C_ELEC, lw=1.9)
label(91.5, 69.4, "off-peak power", col=C_ELEC, fs=6.6, ha="left")
# SOE steam = a LP turbine extraction (deaerator-inlet stream, per Milewski 2021).
# The cogeneration bleed is routed BY MODE to TCES (DH) OR SOE (H2) - never stacked:
# charging the store just to reheat H2 feed would double-convert and waste heat.
tee(57, 71.5, C_STEAM)
pipe([(57, 71.5), (57, 64), (96, 64)], C_STEAM, lw=1.6, ls=(0, (4, 2)))
label(75, 65.3, "LP turbine extraction → SOE feed  (0.15 MPa · 0.53 kg/s, deaerator stream)", col=C_STEAM, fs=6.2)
ax.text(50, 35.6, "cogeneration steam routed BY MODE:  → TCES (winter / DH)   or   → SOE (summer / H₂)",
        ha="left", fontsize=6.6, color=INK, style="italic", fontweight="bold", zorder=7)
pipe([(114, 62.5), (120, 62.5)], C_H2, lw=2.4)
box(120, 58, 16, 9, "H₂ storage / export\n213 kg/h · ≈120 t/yr\n(4 h/night × ~140 nights)", fc="#f4ecf7", fs=7.2, tcol=C_H2)

# ===================================================================== legend + titleblock
legends = [("primary coolant", C_PRIM), ("main / extraction steam", C_STEAM),
           ("feedwater / condensate", C_FEED), ("TCES charge loop (closed)", C_CHG),
           ("district heat water", C_DH), ("electricity", C_ELEC), ("hydrogen", C_H2)]
ax.text(5, 14.5, "LEGEND", fontsize=8, fontweight="bold")
for i, (t, c) in enumerate(legends):
    xx = 5 + (i % 2) * 30
    yy = 12.6 - (i // 2) * 2.0
    ax.plot([xx, xx + 2.6], [yy, yy], color=c, lw=3, solid_capstyle="round")
    ax.text(xx + 3.1, yy, t, fontsize=7.0, va="center")

ax.add_patch(Rectangle((5, 3.2), 40, 3.6, fill=False, ec=INK, lw=1.0))
ax.text(6, 5.6, "Fig 8.9-2  ·  Aegis-40 cogeneration (TCES district heat + H₂)", fontsize=7.4, fontweight="bold")
ax.text(6, 4.0, "single turbine · stage-14 HP extraction · IHX-isolated store · 90/45 °C DH · SOE H₂   ·   NTS", fontsize=6.4, color="#666")

out = os.path.join(OUT, "pfd_cogeneration_tces.png")
fig.savefig(out, dpi=170, bbox_inches="tight")
print("wrote", out)
