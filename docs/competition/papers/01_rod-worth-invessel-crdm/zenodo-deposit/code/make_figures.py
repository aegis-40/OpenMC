# -*- coding: utf-8 -*-
"""All four manuscript figures, one consistent house style.

Fig 1  control-rod cluster layout, base 12-CRA and final 16-CRA
Fig 2  rod-worth ladder: lever decomposition and shutdown states
Fig 3  the SBF design space: attainable worth and the ejection constraint
Fig 4  cooldown reactivity response and the emergency-boron requirement
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from pathlib import Path

OUT = Path(r"D:\projects\teknofest-2026-aegis-40-ipwr\docs\competition\papers"
           r"\01_rod-worth-invessel-crdm\figures")

# ------------------------------------------------------------------ style
NAVY, ACC, GREY, WARM = "#12355B", "#0B6FA4", "#6E7B87", "#B4451F"
PALE, FUEL, EDGE = "#D8E6F0", "#F2F5F8", "#B8C4CE"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.linewidth": 0.8, "axes.edgecolor": "#333333",
    "axes.labelcolor": "#1A1A1A", "text.color": "#1A1A1A",
    "xtick.color": "#333333", "ytick.color": "#333333",
    "xtick.direction": "out", "ytick.direction": "out",
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.labelsize": 8.5, "legend.fontsize": 7,
    "figure.dpi": 300, "savefig.dpi": 300,
})
W = 7.48                                     # double-column width, inches


def panel(ax, letter, title):
    ax.set_title("(%s)  %s" % (letter, title), fontsize=8.5, loc="left",
                 weight="bold", color=NAVY, pad=6)
    ax.grid(alpha=0.18, lw=0.6)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(OUT / name, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  saved", name)


# ================================================================== FIG 1
CORE = np.array([[0, 0, 1, 1, 1, 0, 0],
                 [0, 1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1],
                 [0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 1, 1, 1, 0, 0]])
CRM = np.array([[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]])
N = 7
BASE12 = [(i, j) for j in range(N) for i in range(N) if CRM[N - 1 - j, i] == 1]
EXTRA4 = [(3, 5), (1, 3), (5, 3), (3, 1)]
INSTR = (3, 3)
BOUND = (3, 2)


def draw_core(ax, cras, extras=(), mark_bound=False):
    for j in range(N):
        for i in range(N):
            if CORE[N - 1 - j, i] == 0:
                continue
            p = (i, j)
            if p == INSTR:
                fc, ec, lw = "#FFFFFF", GREY, 0.9
            elif p in extras:
                fc, ec, lw = PALE, ACC, 1.6
            elif p in cras:
                fc, ec, lw = ACC, ACC, 0.9
            else:
                fc, ec, lw = FUEL, EDGE, 0.9
            ax.add_patch(Rectangle((i - .46, j - .46), .92, .92,
                                   facecolor=fc, edgecolor=ec, lw=lw, zorder=2))
            if p == INSTR:
                ax.plot([i], [j], marker="x", ms=4.5, mew=1.2, color=GREY, zorder=3)
            elif p in extras:
                ax.plot([i], [j], marker="+", ms=5, mew=1.3, color=ACC, zorder=3)
    if mark_bound:
        ax.add_patch(Rectangle((BOUND[0] - .46, BOUND[1] - .46), .92, .92,
                               facecolor="none", edgecolor=WARM, lw=1.9, zorder=5))
    ax.set_xlim(-0.75, N - 0.25)
    ax.set_ylim(-0.75, N - 0.25)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 3.45))
draw_core(a1, BASE12)
a1.set_title("(a)  Base configuration — 12 CRA", fontsize=8.5, loc="left",
             weight="bold", color=NAVY, pad=4)
draw_core(a2, BASE12 + EXTRA4, extras=EXTRA4, mark_bound=True)
a2.set_title("(b)  Final configuration — 16 CRA", fontsize=8.5, loc="left",
             weight="bold", color=NAVY, pad=4)

handles = [
    Rectangle((0, 0), 1, 1, fc=FUEL, ec=EDGE, lw=.9, label="Fuel assembly"),
    Rectangle((0, 0), 1, 1, fc=ACC, ec=ACC, lw=.9, label="Control-rod cluster"),
    Rectangle((0, 0), 1, 1, fc=PALE, ec=ACC, lw=1.6, label="Cluster added in (b)"),
    Rectangle((0, 0), 1, 1, fc="#FFFFFF", ec=GREY, lw=.9, label="Instrument position"),
    Rectangle((0, 0), 1, 1, fc="none", ec=WARM, lw=1.9, label="Bounding cluster (3,2)"),
]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
           bbox_to_anchor=(0.5, -0.02), handlelength=1.4, columnspacing=1.6)
save(fig, "fig1_cra_layout.png")

# ================================================================== FIG 2
cfg = ["12 CRA\nnatural B$_4$C", "12 CRA\n90 % B-10",
       "16 CRA\nnatural B$_4$C", "16 CRA\n90 % B-10"]
bank = [13409, 15673, 18853, 21509]
hot = [-0.25, 2.01, 5.20, 7.85]
cold = [-10.25, -8.92, -5.32, -3.02]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 3.25),
                             gridspec_kw=dict(wspace=0.30))

# grouped by cluster count: the enrichment lever is the within-group gap,
# the count lever is the between-group gap
gx = np.array([0.0, 1.0])
bw = 0.30
nat = [13409, 18853]
enr = [15673, 21509]
a1.bar(gx - bw / 2, nat, width=bw, color=PALE, edgecolor=ACC, lw=1.3,
       label="natural B$_4$C", zorder=3)
a1.bar(gx + bw / 2, enr, width=bw, color=ACC, edgecolor=ACC, lw=1.3,
       label="90 at % B-10", zorder=3)
for xi, v in zip(gx - bw / 2, nat):
    a1.text(xi, v + 450, "{:,}".format(v), ha="center", va="bottom",
            fontsize=7.0, color=NAVY, weight="bold")
for xi, v in zip(gx + bw / 2, enr):
    a1.text(xi, v + 450, "{:,}".format(v), ha="center", va="bottom",
            fontsize=7.0, color=NAVY, weight="bold")
for xi, d in zip(gx, ("+2,264 pcm", "+2,656 pcm")):
    a1.text(xi, 24500, "enrichment lever\n" + d, ha="center", va="center",
            fontsize=6.8, color=WARM, style="italic")
a1.text(0.5, 12600, "cluster-count lever\n+5,444 pcm (natural)\n+5,836 pcm (90 % B-10)",
        ha="center", va="center", fontsize=6.8, color=NAVY)
a1.set_xticks(gx)
a1.set_xticklabels(["12 clusters", "16 clusters"], fontsize=8)
a1.set_ylabel("Total bank worth (pcm)")
a1.set_ylim(0, 27000)
a1.set_xlim(-0.62, 1.62)
a1.legend(loc="lower right", frameon=True, framealpha=.95,
          edgecolor="#CCCCCC", fontsize=6.8, handlelength=1.3)
panel(a1, "a", "Attainable bank worth")

x = np.arange(4)
w = .36
a2.axhline(0, color=WARM, lw=1.3, zorder=4)
a2.bar(x - w / 2, hot, width=w, color=ACC, edgecolor=ACC, lw=.8,
       label="Hot, all rods in", zorder=3)
a2.bar(x + w / 2, cold, width=w, color="white", edgecolor=ACC, lw=1.3,
       hatch="////", label="Cold, most reactive rod stuck", zorder=3)
a2.text(3.62, 1.0, "subcritical", fontsize=6.6, color=WARM,
        ha="left", va="bottom", style="italic", rotation=90)
a2.text(3.62, -1.0, "supercritical", fontsize=6.6, color=WARM,
        ha="left", va="top", style="italic", rotation=90)
a2.set_xticks(x)
a2.set_xticklabels(["12\nnatural", "12\n90 % B-10", "16\nnatural",
                    "16\n90 % B-10"], fontsize=6.5)
a2.set_xlabel("Clusters / absorber", fontsize=8)
a2.set_ylabel("Signed shutdown margin (% $\\Delta k/k$)")
a2.set_xlim(-0.62, 4.15)
a2.set_ylim(-12.4, 10.4)
a2.legend(loc="upper left", frameon=True, framealpha=.95, edgecolor="#CCCCCC",
          fontsize=6.6, handlelength=1.3)
panel(a2, "b", "Shutdown states across the ladder")
save(fig, "fig2_rod_worth_ladder.png")

# ================================================================== FIG 4
T = np.array([556, 523, 473, 423, 373, 323, 294])
k_base = np.array([1.0183, 1.0377, 1.0611, 1.0867, 1.1011, 1.1110, 1.1142])
k_fin = np.array([0.93445, 0.95652, 0.97872, 1.00385, 1.01907, 1.02918, 1.03115])
ka_fin = np.array([0.9407, 0.96283, 0.98491, 1.0101, 1.02514, 1.03552, 1.03741])

ppm = np.array([0, 500, 700, 800, 900, 1000, 1500, 2000])
kadj = np.array([1.0374, 0.97814, 0.9566, 0.9473, 0.9383, 0.92881, 0.88893, 0.85103])
NEW = np.array([False, False, True, True, True, False, False, False])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(W, 3.25),
                             gridspec_kw=dict(wspace=0.28))

a1.axhline(1.0, color=WARM, lw=1.3, zorder=4)
a1.plot(T, k_base, "s--", color=GREY, ms=4.5, lw=1.1, mfc="white", mew=1.3,
        label="12 CRA, natural B$_4$C", zorder=3)
a1.plot(T, k_fin, "o-", color=ACC, ms=4.8, lw=1.3, zorder=3,
        label="16 CRA, 90 % B-10")
a1.plot(T, ka_fin, "^:", color=ACC, ms=4.0, lw=1.0, mfc="white", mew=1.1,
        label="16 CRA, 90 % B-10 ($k_{\\mathrm{adj}}$)", zorder=3)
a1.plot([443], [1.0], marker="*", ms=11, color=WARM, zorder=6,
        markeredgecolor="white", mew=.6)
a1.annotate("$k_{\mathrm{adj}}=1$\nat 443 K", xy=(443, 1.0), xytext=(408, 0.952),
            fontsize=7, color=WARM, weight="bold",
            arrowprops=dict(arrowstyle="->", color=WARM, lw=.9))
a1.text(549, 1.005, "$k=1$", fontsize=7, color=WARM, va="bottom")
a1.set_xlabel("Moderator temperature (K)")
a1.set_ylabel("$k_{\\mathrm{eff}}$")
a1.set_xlim(575, 275)
a1.set_ylim(0.918, 1.132)
a1.legend(loc="upper left", frameon=True, framealpha=.95,
          edgecolor="#CCCCCC", fontsize=6.6, handlelength=1.8)
panel(a1, "a", "Reactivity along the cooldown path")

a2.axhline(0.95, color=WARM, lw=1.3, zorder=4)
a2.plot(ppm, kadj, "-", color=ACC, lw=1.3, zorder=3)
a2.plot(ppm[~NEW], kadj[~NEW], "o", color=ACC, ms=5.0, zorder=4,
        label="500 ppm sweep")
a2.plot(ppm[NEW], kadj[NEW], "D", color="white", mec=WARM, mew=1.5, ms=5.2,
        zorder=5, label="Added 700 / 800 / 900 ppm")
a2.plot([771], [0.95], marker="*", ms=11, color=WARM, zorder=6,
        markeredgecolor="white", mew=.6)
a2.annotate("771 ppm", xy=(771, 0.95), xytext=(1010, 0.985),
            fontsize=7.2, color=WARM, weight="bold",
            arrowprops=dict(arrowstyle="->", color=WARM, lw=.9))
a2.text(1960, 0.9535, "$k_{\\mathrm{adj}} = 0.95$", fontsize=7, color=WARM,
        ha="right", va="bottom")
a2.text(1960, 0.872, "credited inventory 3,000 ppm\n= 3.9 $\\times$ the requirement",
        fontsize=6.7, color=NAVY, ha="right", va="center", style="italic")
a2.set_xlabel("Soluble boron (ppm)")
a2.set_ylabel("$k_{\\mathrm{adj}}$  (cold, most reactive rod stuck)")
a2.set_xlim(-90, 2090)
a2.set_ylim(0.838, 1.058)
a2.legend(loc="upper right", frameon=True, framealpha=.95,
          edgecolor="#CCCCCC", fontsize=6.6, handlelength=1.3)
panel(a2, "b", "Emergency-boron requirement")
save(fig, "fig4_mslb_and_ebis.png")

print("done")
