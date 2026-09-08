"""Aegis-40 - multi-batch fuel-utilisation estimate (Linear Reactivity Model).

Purpose: quantify what once-through 'leaves on the table' vs an n-batch reload,
so the deliberate once-through choice can be defended with a number.

Method: the Linear Reactivity Model (Driscoll, Downar & Pilat, 'The Linear
Reactivity Model for Nuclear Fuel Management', ANS 1990). For a core reloaded in
n equal batches, discharge burnup

        B_n = [ 2n / (n+1) ] * B_1

where B_1 is the single-batch (once-through) reactivity-limited discharge burnup.
Natural-uranium utilisation at fixed feed enrichment scales with discharge burnup,
so the fractional NatU saving of n batches vs once-through is  1 - B_1/B_n.

B_1 is taken from our own OpenMC once-through result: the core reaches k=1 at
~30.8 GWd/tHM (STAT_FINAL EOC), i.e. the reactivity-limited single-batch burnup.

  python multibatch_lrm.py
"""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(HERE), "figures"); os.makedirs(FIG, exist_ok=True)
OUT = os.path.join(os.path.dirname(HERE), "outputs"); os.makedirs(OUT, exist_ok=True)
DECK = r"D:\projects\Final pptx\charts"; os.makedirs(DECK, exist_ok=True)

B1 = 29.6                      # GWd/tHM, once-through design discharge at EOC k=1 (FER value)
N = [1, 2, 3, 4]
Bn = [2*n/(n+1)*B1 for n in N]
asymptote = 2*B1               # n -> infinity
save = [(1 - B1/b)*100 for b in Bn]   # % NatU saving vs once-through

# ---- style ----
BLUE="#2a78d6"; AMBER="#eda100"; INK="#0b0b0b"; SEC="#52514e"; MUT="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"figure.facecolor":"#ffffff",
    "axes.facecolor":"#ffffff","text.color":INK,"axes.labelcolor":SEC,"xtick.color":MUT,"ytick.color":MUT})
fig, ax = plt.subplots(figsize=(8.2,4.6), dpi=200)
colors = [AMBER] + [BLUE]*(len(N)-1)     # highlight the once-through design point
bars = ax.bar(range(len(N)), Bn, width=0.6, color=colors, edgecolor="#fff", linewidth=1.5, zorder=3)
for i,(b,s) in enumerate(zip(Bn,save)):
    ax.text(i, b+0.8, f"{b:.1f}", ha="center", va="bottom", fontsize=12, fontweight="bold", color=INK)
    if i>0: ax.text(i, b/2, f"−{s:.0f}%\nNatU/MWh", ha="center", va="center", fontsize=10, color="#fff", fontweight="bold")
ax.axhline(asymptote, color=MUT, lw=1.4, ls=(0,(5,3)), zorder=2)
ax.text(len(N)-1, asymptote+0.7, f"n→∞ limit  {asymptote:.1f}", ha="right", va="bottom", fontsize=9, color=MUT)
ax.text(0, 2.0, "design\n(once-through)", ha="center", va="bottom", fontsize=9, color="#6b4e00", fontweight="bold")
ax.set_xticks(range(len(N))); ax.set_xticklabels([f"{n}-batch" for n in N], fontsize=11, color=SEC)
ax.set_ylabel("Discharge burnup  (GWd/tHM)"); ax.set_ylim(0, asymptote*1.12)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.spines["left"].set_color(BASE); ax.spines["bottom"].set_color(BASE); ax.tick_params(length=0)
ax.yaxis.grid(True, color=GRID, lw=1.0); ax.set_axisbelow(True)
fig.suptitle("Fuel utilisation — once-through vs multi-batch (LRM)", x=0.125, y=0.98, ha="left", fontsize=15, fontweight="bold")
fig.text(0.125, 0.915, "B_n = 2n/(n+1)·B_1 (LRM, fixed enrichment) · B_1 = 29.6 GWd/tHM (OpenMC once-through)", fontsize=9.5, color=MUT)
fig.tight_layout(rect=(0,0,1,0.88))
fig.savefig(os.path.join(FIG,"multibatch_utilisation.png")); fig.savefig(os.path.join(DECK,"chart_multibatch.png"))

print("n-batch  discharge(GWd/tHM)  NatU-saving vs once-through")
for n,b,s in zip(N,Bn,save): print(f"  {n}       {b:6.1f}            {s:5.1f} %")
with open(os.path.join(OUT,"multibatch_lrm.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["n_batch","discharge_GWd_tHM","natU_saving_pct"])
    for n,b,s in zip(N,Bn,save): w.writerow([n,f"{b:.1f}",f"{s:.1f}"])
print("wrote multibatch_utilisation.png (+ deck copy) and multibatch_lrm.csv")
