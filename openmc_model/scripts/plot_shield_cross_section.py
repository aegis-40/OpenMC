#!/usr/bin/env python
"""Draw the Aegis-40 circular biological-shield cross-section from the
CAD-anchored radii (matches the rev7 shielding model, cell 39, and
docs/competition/shielding/shielding-radial-build.md).  Pure matplotlib —
no OpenMC needed.  Saves a labelled radial-layer figure for the FER.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import os

# (inner r, outer r, name, colour)  — cm, CAD-anchored
LAYERS = [
    (0.0,   80.0,  "Core + radial reflector\n(fuel lattice + H₂O)", "#d83b3b"),
    (80.0,  82.5,  "Core barrel (SS-304)",                               "#7a7a7a"),
    (82.5,  140.0, "Downcomer + helical-SG\nannulus (H₂O)",          "#4f8fd6"),
    (140.0, 156.5, "RPV (SA-508, 160+5 mm)",                            "#404040"),
    (156.5, 171.5, "Reactor cavity (air)",                              "#eaeaea"),
    (171.5, 176.5, "Thermal/neutron shield (SS-304)",                   "#9a9a9a"),
    (176.5, 186.5, "Borated polyethylene",                             "#6fbf73"),
    (186.5, 306.5, "Magnetite heavy concrete\n(lead-free bulk shield)", "#b9975b"),
    (306.5, 316.5, "Ordinary concrete (finish)",                        "#cdbb9a"),
]

fig, ax = plt.subplots(figsize=(10, 10))
R_OUT = LAYERS[-1][1]

# draw from outside in so inner layers sit on top
for ri, ro, name, col in reversed(LAYERS):
    ax.add_patch(plt.Circle((0, 0), ro, facecolor=col, edgecolor="k", lw=0.8, zorder=1))

# half-section radius callouts along +x
for ri, ro, name, col in LAYERS:
    ax.plot([ro, ro], [0, -8], color="k", lw=0.6, zorder=5)
    ax.text(ro, -14, f"{ro:.1f}", ha="center", va="top", fontsize=7, rotation=90, zorder=5)

# leader labels stacked on the right, each arrow pointing at its own ring
import math
y0 = R_OUT * 0.95
dy = (2 * R_OUT * 0.95) / (len(LAYERS) - 1)
for k, (ri, ro, name, col) in enumerate(LAYERS):
    rmid = 0.5 * (ri + ro)
    theta = math.radians(75 - k * (150.0 / (len(LAYERS) - 1)))   # fan +75°..-75°
    xr, yr = rmid * math.cos(theta), rmid * math.sin(theta)
    ax.annotate(f"{name}\n[{ri:.1f}–{ro:.1f} cm, {ro-ri:.1f} cm]",
                xy=(xr, yr),
                xytext=(R_OUT * 1.20, y0 - k * dy),
                ha="left", va="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.25", fc=col, ec="k", lw=0.5, alpha=0.9),
                arrowprops=dict(arrowstyle="->", lw=0.7, color="k",
                                connectionstyle="arc3,rad=0.0"),
                xycoords="data")

ax.plot(0, 0, marker="+", color="white", ms=14, mew=2, zorder=6)
ax.set_xlim(-R_OUT * 1.05, R_OUT * 1.75)
ax.set_ylim(-R_OUT * 1.12, R_OUT * 1.12)
ax.set_aspect("equal")
ax.set_xlabel("radius (cm)")
ax.set_title("Aegis-40 — circular biological shield (CAD-anchored, lead-free)\n"
             "125 MWth integral RPV — axisymmetric radial build, total ø ≈ 6.3 m",
             fontsize=11)
ax.grid(True, alpha=0.25)
fig.tight_layout()

out = r"D:\projects\teknofest-2026-aegis-40-ipwr\docs\competition\shielding\shield_radial_layers_cad.png"
fig.savefig(out, dpi=160)
print("saved:", os.path.basename(out))
print(f"layers: {len(LAYERS)} | outer radius {R_OUT:.1f} cm (shield dia {2*R_OUT/100:.2f} m)")
