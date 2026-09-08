"""Decay heat + ingestion radiotoxicity vs cooling time for FER Figure 8.11-1.
Data from the rev_3 discharge source term (waste/discharge_source_term.md)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "waste")

yr = [1e-3, 1, 3, 5, 10, 30, 50, 100, 300, 1000, 10000, 100000]
heat = [18220, 15240, 11450, 9333, 7003, 4247, 2820, 1188, 264.8, 154.6, 77.95, 3.859]
rtox = [2.175e9, 1.930e9, 1.607e9, 1.413e9, 1.163e9, 7.442e8, 5.112e8, 2.433e8,
        7.247e7, 4.497e7, 2.297e7, 1.070e6]

fig, ax1 = plt.subplots(figsize=(8, 5.2))
c1, c2 = "#b5462e", "#2471a3"
ax1.loglog(yr, heat, "o-", color=c1, lw=2, ms=5, label="decay heat")
ax1.set_xlabel("cooling time after discharge  [years]")
ax1.set_ylabel("decay heat  [W]", color=c1)
ax1.tick_params(axis="y", labelcolor=c1)
ax1.grid(True, which="both", alpha=0.3)

ax2 = ax1.twinx()
ax2.loglog(yr, rtox, "s--", color=c2, lw=2, ms=5, label="ingestion radiotoxicity")
ax2.set_ylabel("ingestion radiotoxicity  [Sv]", color=c2)
ax2.tick_params(axis="y", labelcolor=c2)

ax1.set_title("Aegis-40 spent fuel — decay heat & radiotoxicity vs cooling time\n"
              "(once-through discharge inventory, ~9.1 tHM, 29.6 GWd/tHM — STAT_FINAL record)")
ax1.axvline(5, color="0.6", ls=":", lw=1)
ax1.text(5.5, 30, "pool→cask\nwindow", fontsize=7.5, color="0.4")
fig.tight_layout()
p = os.path.join(OUT, "decay_heat_vs_cooling.png")
fig.savefig(p, dpi=150)
print("wrote", p)
