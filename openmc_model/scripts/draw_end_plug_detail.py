"""Dimensioned cross-section of the fuel-rod end plugs (Creo revolve reference).

Two panels: bottom end plug (bullet/chamfer nose) and top end plug (with plenum
spring + grip), both shown seated/welded in the Zr-4 clad. All mm.  Output:
docs/competition/cad/end_plug_detail.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cad")

# key radii (mm)
CLAD_OR = 9.520 / 2      # 4.760
CLAD_IR = 8.375 / 2      # 4.1875
SHANK_R = 8.300 / 2      # 4.150  (slip fit into clad bore, weld gap)
PELLET_R = 8.192 / 2     # 4.096

CLAD_FILL = "#9fb6c9"
PLUG_FILL = "#7f8c8d"
PELLET_FILL = "#3a3a3a"
SPRING_C = "#444"


def mirror(ax, pts, **kw):
    """Draw a polygon and its mirror about r=0 (the rod axis is vertical at x=0)."""
    ax.add_patch(Polygon(pts, closed=True, **kw))
    ax.add_patch(Polygon([(-x, y) for x, y in pts], closed=True, **kw))


def clad(ax, z0, z1):
    w = CLAD_OR - CLAD_IR
    for xleft in (CLAD_IR, -CLAD_OR):   # right wall, left wall
        ax.add_patch(Rectangle((xleft, z0), w, z1 - z0,
                               facecolor=CLAD_FILL, edgecolor="#333", lw=1, hatch="////"))


def dim(ax, x0, x1, y, text, off=0):
    ax.annotate("", (x1, y), (x0, y), arrowprops=dict(arrowstyle="<->", color="k", lw=0.8))
    ax.text((x0 + x1) / 2, y + off, text, ha="center", va="bottom", fontsize=7.5)


def vdim(ax, x, y0, y1, text):
    ax.annotate("", (x, y1), (x, y0), arrowprops=dict(arrowstyle="<->", color="k", lw=0.8))
    ax.text(x + 0.4, (y0 + y1) / 2, text, ha="left", va="center", fontsize=7.5)


# ---------------- bottom plug ----------------
def bottom_plug(ax):
    nose, body, shank = 2.5, 6.0, 10.0
    z = 0.0
    # nose (chamfer cone): tip on axis -> body radius
    mirror(ax, [(0, z), (CLAD_OR, z + nose), (0, z + nose)], facecolor=PLUG_FILL,
           edgecolor="#333", lw=1)
    z += nose
    mirror(ax, [(0, z), (CLAD_OR, z), (CLAD_OR, z + body), (0, z + body)],
           facecolor=PLUG_FILL, edgecolor="#333", lw=1)
    z += body
    shoulder_z = z
    mirror(ax, [(0, z), (SHANK_R, z), (SHANK_R, z + shank), (0, z + shank)],
           facecolor=PLUG_FILL, edgecolor="#333", lw=1)
    clad(ax, shoulder_z, shoulder_z + shank + 8)
    # pellet resting on shank top
    ax.add_patch(Rectangle((-PELLET_R, shoulder_z + shank), 2 * PELLET_R, 7,
                           facecolor=PELLET_FILL, edgecolor="none"))
    # girth weld marker
    ax.plot([CLAD_OR], [shoulder_z], marker=(3, 0, 0), ms=9, color="#c0392b")
    ax.text(CLAD_OR + 0.6, shoulder_z, "girth weld", fontsize=7, color="#c0392b", va="center")
    # dims
    dim(ax, -CLAD_OR, CLAD_OR, -2.2, "Ø9.520 (clad OD = body)")
    dim(ax, -SHANK_R, SHANK_R, shoulder_z + shank + 9.5, "Ø8.30 shank")
    vdim(ax, CLAD_OR + 3.2, 0, nose, "2.5")
    vdim(ax, CLAD_OR + 3.2, nose, nose + body, "6  body")
    vdim(ax, SHANK_R + 3.0, shoulder_z, shoulder_z + shank, "10  shank")
    ax.text(0, -4.6, "BOTTOM end plug\n(chamfer/bullet nose for loading)",
            ha="center", fontsize=9, weight="bold")
    ax.set_xlim(-15, 15)
    ax.set_ylim(-6, shoulder_z + shank + 8)
    ax.set_aspect("equal"); ax.axis("off")


# ---------------- top plug ----------------
def top_plug(ax):
    # built downward from top: grip nub, body, shank into clad, then spring + pellet
    grip, body, shank = 4.0, 8.0, 10.0
    top = grip + body + shank + 14  # total height of view
    z = top
    # grip nub
    mirror(ax, [(0, z), (2.0, z), (2.0, z - grip), (0, z - grip)],
           facecolor=PLUG_FILL, edgecolor="#333", lw=1)
    z -= grip
    mirror(ax, [(0, z), (CLAD_OR, z - 0.0), (CLAD_OR, z - body), (0, z - body)],
           facecolor=PLUG_FILL, edgecolor="#333", lw=1)
    z -= body
    shoulder_z = z
    mirror(ax, [(0, z), (SHANK_R, z), (SHANK_R, z - shank), (0, z - shank)],
           facecolor=PLUG_FILL, edgecolor="#333", lw=1)
    z -= shank
    clad(ax, 0, shoulder_z)
    # plenum spring (coil) between shank bottom and pellet
    spring_top = shoulder_z - shank
    spring_bot = 6
    import numpy as np
    n = 14
    zz = np.linspace(spring_bot, spring_top, n)
    xx = SHANK_R * 0.8 * (-1) ** np.arange(n)
    ax.plot(xx, zz, color=SPRING_C, lw=1.4)
    ax.text(SHANK_R + 1.2, (spring_bot + spring_top) / 2, "plenum spring\n(hold-down)",
            fontsize=7, va="center")
    # pellet below
    ax.add_patch(Rectangle((-PELLET_R, 0), 2 * PELLET_R, spring_bot,
                           facecolor=PELLET_FILL, edgecolor="none"))
    ax.text(0, -1.2, "pellet stack", ha="center", fontsize=7, color="#3a3a3a")
    # weld
    ax.plot([CLAD_OR], [shoulder_z], marker=(3, 0, 180), ms=9, color="#c0392b")
    ax.text(CLAD_OR + 0.6, shoulder_z, "girth weld", fontsize=7, color="#c0392b", va="center")
    dim(ax, -CLAD_OR, CLAD_OR, top + 1.2, "Ø9.520")
    vdim(ax, CLAD_OR + 3.0, shoulder_z, shoulder_z + body, "8  body")
    vdim(ax, SHANK_R + 3.0, shoulder_z - shank, shoulder_z, "10 shank")
    ax.text(0, -4.6, "TOP end plug\n(grip + gas-plenum spring below)",
            ha="center", fontsize=9, weight="bold")
    ax.set_xlim(-15, 15)
    ax.set_ylim(-6, top + 4)
    ax.set_aspect("equal"); ax.axis("off")


fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 8))
bottom_plug(a1)
top_plug(a2)
fig.suptitle("Aegis-40 fuel-rod end plugs  —  Zr-4, revolve profile  "
             "(shank Ø8.30 slips into clad bore Ø8.375, circumferential weld)",
             fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(OUT, "end_plug_detail.png"), dpi=150, bbox_inches="tight")
print("wrote", os.path.join(OUT, "end_plug_detail.png"))
