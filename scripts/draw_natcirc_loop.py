"""
Aegis-40 — FER §8.4 figures: in-vessel primary natural-circulation loop.

Produces two diagrams the cooling-circuit section is missing (the secondary
side is already covered by the §8.9 PFD + T-s diagram):

  1) natcirc_loop_schematic.png  — labelled in-vessel loop (core -> riser ->
     OTSG -> downcomer -> lower plenum) with the buoyancy driving-head balance.
  2) natcirc_self_regulation.png — pumpless self-regulation curve m_dot ~ P^(1/3).

Numbers are the locked §8.4 values (cross-checked by natcirc_primary.py,
IAPWS-IF97). This script only draws them; it has no physics dependency.

Output: docs/competition/fer/ (next to the section text).
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch

OUT = Path(__file__).resolve().parents[1] / "docs" / "competition" / "fer"
OUT.mkdir(parents=True, exist_ok=True)

# ---- locked §8.4 conditions -------------------------------------------------
T_HOT, T_COLD = 308.0, 258.0          # degC, hot/cold legs
RHO_HOT, RHO_COLD = 703.1, 796.7      # kg/m^3 @ 12.8 MPa
H_TH = 2.85                           # m, core-mid -> OTSG-mid thermal height
DP_DRV = 2.62                         # kPa, buoyancy driving head
M_DOT = 483.0                         # kg/s, primary flow
V_CORE = 0.90                         # m/s, CFD core velocity
P_TH = 125.0                          # MWth

HOT = "#c0392b"
COLD = "#2471a3"
STEEL = "#34495e"
OTSGC = "#7d6608"
FUELC = "#b9770e"


def _arrow(ax, x0, y0, x1, y1, color, lw=3.2, ms=18):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, color=color,
                                 shrinkA=0, shrinkB=0, zorder=5))


def draw_schematic():
    fig, ax = plt.subplots(figsize=(7.4, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # ---- RPV outline (rounded vessel) --------------------------------------
    ax.add_patch(FancyBboxPatch((1.4, 0.8), 7.2, 10.4,
                 boxstyle="round,pad=0.0,rounding_size=1.1",
                 fill=False, ec=STEEL, lw=3.0, zorder=2))
    ax.text(5.0, 11.45, "Reactor Pressure Vessel  (12.8 MPa)",
            ha="center", va="bottom", fontsize=10.5, color=STEEL, weight="bold")

    # ---- core (heat source) -------------------------------------------------
    ax.add_patch(Rectangle((3.6, 1.5), 2.8, 1.9, fc=FUELC, ec="black",
                 lw=1.3, alpha=0.92, zorder=3))
    ax.text(5.0, 2.45, "CORE\n125 MWth\n21 FA", ha="center", va="center",
            fontsize=9.5, color="white", weight="bold", zorder=4)

    # ---- riser (central hot upflow) ----------------------------------------
    ax.add_patch(Rectangle((4.3, 3.4), 1.4, 4.6, fc=HOT, ec="none",
                 alpha=0.16, zorder=1))
    _arrow(ax, 5.0, 3.5, 5.0, 7.9, HOT, lw=4.0, ms=22)
    ax.text(5.0, 5.7, "RISER\n(hot)", ha="center", va="center", fontsize=9.5,
            color=HOT, weight="bold", rotation=90)

    # ---- OTSG (helical coil in upper annulus) ------------------------------
    for side in (2.05, 6.55):
        ax.add_patch(Rectangle((side, 8.0), 1.4, 2.2, fc=OTSGC, ec="black",
                     lw=1.0, alpha=0.22, zorder=2))
        # coil squiggle
        yy = np.linspace(8.1, 10.1, 60)
        xx = side + 0.7 + 0.45 * np.sin(yy * 7.0)
        ax.plot(xx, yy, color=OTSGC, lw=2.0, zorder=3)
    ax.text(5.0, 9.6, "OTSG\nhelical coil\n(heat sink\nABOVE core)",
            ha="center", va="center", fontsize=8.8, color=OTSGC, weight="bold")

    # ---- turn-around at top -------------------------------------------------
    _arrow(ax, 5.0, 8.0, 2.9, 9.2, HOT, lw=3.0, ms=16)
    _arrow(ax, 5.0, 8.0, 7.1, 9.2, HOT, lw=3.0, ms=16)

    # ---- downcomer (cold downflow on both sides) ---------------------------
    for x in (2.75, 7.25):
        ax.add_patch(Rectangle((x - 0.45, 3.4), 0.9, 4.5, fc=COLD, ec="none",
                     alpha=0.16, zorder=1))
        _arrow(ax, x, 7.9, x, 3.6, COLD, lw=3.6, ms=20)
    ax.text(2.0, 5.7, "DOWNCOMER\n(cold)", ha="center", va="center",
            fontsize=8.8, color=COLD, weight="bold", rotation=90)

    # ---- lower plenum return into core -------------------------------------
    _arrow(ax, 2.75, 3.5, 3.7, 2.1, COLD, lw=2.6, ms=14)
    _arrow(ax, 7.25, 3.5, 6.3, 2.1, COLD, lw=2.6, ms=14)
    ax.text(5.0, 1.05, "lower plenum / flow distributor", ha="center",
            va="center", fontsize=8.0, color=STEEL, style="italic")

    # ---- leg property callouts ---------------------------------------------
    ax.text(8.85, 7.4, f"HOT LEG\n{T_HOT:.0f} °C\nρ = {RHO_HOT:.0f} kg/m³",
            ha="left", va="center", fontsize=9.0, color=HOT, weight="bold")
    ax.text(8.85, 4.4, f"COLD LEG\n{T_COLD:.0f} °C\nρ = {RHO_COLD:.0f} kg/m³",
            ha="left", va="center", fontsize=9.0, color=COLD, weight="bold")

    # ---- thermal-height bracket (left) -------------------------------------
    xb = 0.95
    ax.annotate("", xy=(xb, 9.1), xytext=(xb, 2.45),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.6))
    ax.plot([xb, 3.6], [2.45, 2.45], color="black", lw=0.7, ls=":")
    ax.plot([xb, 2.05], [9.1, 9.1], color="black", lw=0.7, ls=":")
    ax.text(xb - 0.15, 5.8, f"$H_{{th}}$ = {H_TH:.2f} m\n(core-mid →\nOTSG-mid)",
            ha="center", va="center", fontsize=9.0, rotation=90)

    # ---- driving-head balance box ------------------------------------------
    txt = (r"$\Delta P_{drv} = (\rho_{cold}-\rho_{hot})\,g\,H_{th}$"
           f"\n        = {DP_DRV:.2f} kPa"
           f"\n$\\dot m$ = {M_DOT:.0f} kg/s   ·   $v_{{core}}$ = {V_CORE:.2f} m/s"
           f"\nself-regulating:  $\\dot m \\propto P^{{1/3}}$"
           "\nno pumps · no large primary piping")
    ax.text(5.0, 0.05, txt, ha="center", va="bottom", fontsize=9.0,
            bbox=dict(boxstyle="round,pad=0.5", fc="#f4f6f7", ec=STEEL, lw=1.2))

    ax.set_title("Aegis-40 — In-Vessel Primary Natural-Circulation Loop (§8.4)",
                 fontsize=12, weight="bold", pad=10)
    fig.tight_layout()
    p = OUT / "natcirc_loop_schematic.png"
    fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p)


def draw_self_regulation():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    pr = np.linspace(0.0, 1.2, 200)
    mr = pr ** (1.0 / 3.0)
    ax.plot(pr * 100, mr * 100, color=HOT, lw=2.6,
            label=r"natural circulation  $\dot m \propto P^{1/3}$")
    ax.plot(pr * 100, pr * 100, color="gray", lw=1.4, ls="--",
            label="linear (forced-flow reference)")
    ax.scatter([100], [100], s=70, color=STEEL, zorder=5)
    ax.annotate("full power\n483 kg/s, 308/258 °C", (100, 100),
                textcoords="offset points", xytext=(-95, -38), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=STEEL))
    ax.set_xlabel("Core power  P / P$_{nom}$  (%)")
    ax.set_ylabel("Primary flow  $\\dot m$ / $\\dot m_{nom}$  (%)")
    ax.set_title("Pumpless self-regulation of the primary loop (§8.4.2.3)",
                 fontsize=11, weight="bold")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 120)
    fig.tight_layout()
    p = OUT / "natcirc_self_regulation.png"
    fig.savefig(p, dpi=200)
    plt.close(fig)
    print("wrote", p)


if __name__ == "__main__":
    draw_schematic()
    draw_self_regulation()
