# -*- coding: utf-8 -*-
"""Fig. 4 - the soluble-boron-free control-rod design space."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (r"D:\projects\teknofest-2026-aegis-40-ipwr\docs\competition\papers"
       r"\01_rod-worth-invessel-crdm\figures\fig3_design_space.png")

NAVY, ACC, GREY, WARM = "#12355B", "#0B6FA4", "#6E7B87", "#B4451F"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.linewidth": 0.8, "axes.edgecolor": "#333333",
    "xtick.direction": "out", "ytick.direction": "out",
})

fig, (axa, axb) = plt.subplots(
    1, 2, figsize=(7.48, 3.30),
    gridspec_kw=dict(width_ratios=[1.0, 1.0], wspace=0.24))

# ================================================================= (a)
# two parallel lever lines: natural B4C (open) and 90 % B-10 (filled)
axa.plot([12, 16], [13409, 18853], color=ACC, lw=1.3, ls="--", zorder=2)
axa.plot([12, 16], [15673, 21509], color=ACC, lw=1.3, zorder=2)
axa.scatter([12, 16], [13409, 18853], s=48, facecolor="white",
            edgecolor=ACC, lw=1.5, zorder=4)
axa.scatter([12, 16], [15673, 21509], s=48, color=ACC, zorder=4)

# the enrichment lever, measured at both cluster counts
for x, lo, hi, dv in ((12, 13409, 15673, "+2,264"), (16, 18853, 21509, "+2,656")):
    axa.annotate("", xy=(x, hi), xytext=(x, lo),
                 arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.0))
    axa.text(x - 0.28, (lo + hi) / 2, dv, fontsize=6.6, color=NAVY,
             ha="right", va="center")

axa.scatter([29, 37], [14906, 20570], s=54, marker="s", facecolor="white",
            edgecolor=GREY, lw=1.5, zorder=4)
axa.plot([29, 37], [14906, 20570], color=GREY, lw=1.0, ls="--", zorder=2)

axa.text(16.55, 22150, "90 % B-10", fontsize=7.0, color=ACC,
         weight="bold", ha="left", va="center")
axa.text(17.0, 18853, "natural B$_4$C", fontsize=7.0, color=ACC,
         ha="left", va="center")
axa.text(21.0, 16900, "+4 clusters:\n+5,444 pcm (natural)\n+5,836 pcm (90 % B-10)",
         fontsize=6.6, color=NAVY, ha="center", va="center")

axa.annotate("", xy=(16.7, 21509), xytext=(28.2, 20800),
             arrowprops=dict(arrowstyle="<->", color=WARM, lw=1.0,
                             linestyle=(0, (3, 2))))
axa.text(23.0, 23100, "comparable bank worth\nfrom 16 clusters, not 37",
         fontsize=7.2, color=WARM, ha="center", va="bottom", weight="bold")

axa.text(39.4, 13900, "van der Merwe & Hah (2018)\n37-FA SBF core, Ag$-$In$-$Cd",
         fontsize=6.8, color=GREY, ha="right", va="top")

axa.set_xlabel("Number of control-rod clusters")
axa.set_ylabel("Total bank worth (pcm)")
axa.set_xlim(9.5, 40)
axa.set_ylim(11800, 26200)
axa.grid(alpha=0.18, lw=0.6)
axa.set_axisbelow(True)
axa.set_title("(a)  Attainable bank worth", fontsize=8.5, loc="left",
              weight="bold", color=NAVY, pad=6)

# ================================================================= (b)
vals = [1.28, 1.20, 1.13]
errs = [0.07, 0.13, 0.08]
ypos = [2, 1, 0]

axb.axvspan(0.60, 1.0, color="#E7EDF2", zorder=0)
axb.axvspan(1.0, 1.75, color="#F8E9E1", zorder=0)
axb.axvline(1.0, color=WARM, lw=1.5, zorder=3)

for y, v, e in zip(ypos, vals, errs):
    axb.errorbar(v, y, xerr=e, fmt="o", ms=6.8, mfc=ACC, mec=ACC,
                 mew=1.5, ecolor=ACC, elinewidth=1.2, capsize=3.0, zorder=5)

axb.text(1.335, 2.0, "16 CRA, 90 % B-10,\nhot fuel 900 K",
         fontsize=6.9, color=NAVY, ha="left", va="center")
axb.text(1.345, 1.0, "16 CRA, 90 % B-10, HZP",
         fontsize=6.9, color=NAVY, ha="left", va="center")
axb.text(1.225, 0.0, "16 CRA, natural B$_4$C\n(absorber sensitivity)",
         fontsize=6.9, color=NAVY, ha="left", va="center")

axb.text(0.795, 1.0, "published SBF cores\nare optimised to stay\nleft of this line [2,4]",
         fontsize=6.4, color="#4A5A68", ha="center", va="center", style="italic")
axb.text(1.375, 2.92, "prompt-critical $-$\nreachable only with\nin-vessel drives",
         fontsize=6.9, color=WARM, ha="center", va="center", style="italic")
axb.text(1.012, -0.66, "1 $", fontsize=8, color=WARM, weight="bold")

axb.set_xlim(0.60, 1.75)
axb.set_ylim(-0.85, 3.35)
axb.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
axb.set_yticks([])
axb.set_xlabel(r"Maximum single-cluster worth  ($\$$ = $\rho\,/\,\beta_{\mathrm{eff}}$)")
axb.grid(axis="x", alpha=0.18, lw=0.6)
axb.set_axisbelow(True)
axb.set_title("(b)  The rod-ejection constraint", fontsize=8.5, loc="left",
              weight="bold", color=NAVY, pad=6)

fig.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
print("saved:", OUT)
