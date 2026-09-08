#!/usr/bin/env python3
"""Radial shielding cross-section — Aegis-40 37-FA, adopted CAD build (Figure 1).
Concentric top-down view + labelled radial-build legend. Lead-free stack."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

# (name, outer radius cm, facecolor)  -- drawn outermost first
LAYERS = [
    ("Ordinary concrete (finish)", 381.5, "#9aa0a6"),
    ("Magnetite concrete (bulk γ+n shield, 180 cm)", 371.5, "#6b5b4e"),
    ("Borated polyethylene (neutron layer, 20 cm)", 191.5, "#f4d35e"),
    ("SS-304 thermal shield (5 cm)", 171.5, "#7f8c8d"),
    ("Reactor cavity (air, 15 cm)", 166.5, "#eef2f5"),
    ("Reactor pressure vessel SA-508 (135–151.5)", 151.5, "#3a4a5a"),
    ("Downcomer + OTSG annulus (water)", 135.0, "#8ecae6"),
    ("Core barrel SS-304 (97.5–100)", 100.0, "#7f8c8d"),
    ("Radial water reflector", 97.5, "#a8dadc"),
    ("Active core (37 FA, R = 75.54)", 75.541, "#e63946"),
]

fig, (ax, axl) = plt.subplots(1, 2, figsize=(13, 7.0),
                              gridspec_kw={"width_ratios": [1.35, 1]})

# ---- concentric cross-section ----
for name, r, c in LAYERS:
    ax.add_patch(Circle((0, 0), r, facecolor=c, edgecolor="white", linewidth=0.8, zorder=1))
ax.set_xlim(-400, 400); ax.set_ylim(-400, 400); ax.set_aspect("equal")
ax.set_title("Aegis-40 radial shielding cross-section\n(37-FA core, adopted CAD build, lead-free)",
             fontsize=12, fontweight="bold")
ax.set_xlabel("radius (cm)"); ax.set_ylabel("radius (cm)")
# radius ticks / rings
for r in [75.541, 100, 135, 151.5, 191.5, 371.5, 381.5]:
    ax.plot([0, r*np.cos(np.deg2rad(-38))], [0, r*np.sin(np.deg2rad(-38))],
            color="none")
ax.annotate("", xy=(381.5*np.cos(np.deg2rad(35)), 381.5*np.sin(np.deg2rad(35))),
            xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="k", lw=1.2))
ax.text(250*np.cos(np.deg2rad(35)), 250*np.sin(np.deg2rad(35)),
        "3.82 m", rotation=35, ha="center", va="bottom", fontsize=9)

# ---- radial-build legend table ----
axl.axis("off")
# (swatch color, layer, r_in, r_out, t)
data = [
    ("#e63946", "Active core + reflector", "0", "97.5", "—"),
    ("#7f8c8d", "Core barrel (SS-304)", "97.5", "100.0", "2.5"),
    ("#8ecae6", "Downcomer + OTSG (H₂O)", "100.0", "135.0", "35.0"),
    ("#3a4a5a", "RPV (SA-508 + clad)", "135.0", "151.5", "16.5"),
    ("#eef2f5", "Cavity (air)", "151.5", "166.5", "15.0"),
    ("#7f8c8d", "Thermal shield (SS-304)", "166.5", "171.5", "5.0"),
    ("#f4d35e", "Borated PE (neutron)", "171.5", "191.5", "20.0"),
    ("#6b5b4e", "Magnetite concrete (bulk)", "191.5", "371.5", "180.0"),
    ("#9aa0a6", "Ordinary concrete (finish)", "371.5", "381.5", "10.0"),
]
cellText = [["", lay, ri, ro, t] for _, lay, ri, ro, t in data]
col_labels = ["", "Layer", "r_in", "r_out", "t (cm)"]
tbl = axl.table(cellText=cellText, colLabels=col_labels, loc="center",
                colWidths=[0.06, 0.52, 0.14, 0.14, 0.14])
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.6)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor("#2b3a55"); cell.set_text_props(color="white", fontweight="bold")
    else:
        if col == 0:
            cell.set_facecolor(data[row-1][0])          # colour swatch
        elif col == 1:
            cell.get_text().set_ha("left"); cell.PAD = 0.03
        else:
            cell.get_text().set_ha("center")
axl.set_title("Radial build (cm)\nRPV fluence 3.0×10¹⁸ n/cm² (PASS) · dose ≤ 0.23 µSv/h (PASS)",
              fontsize=10, fontweight="bold")

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "competition", "shielding", "figures")
OUT = os.path.abspath(OUT); os.makedirs(OUT, exist_ok=True)
fig.tight_layout()
p = os.path.join(OUT, "shield_cross_section_37fa.png")
fig.savefig(p, dpi=160, bbox_inches="tight")
print("wrote", p)
