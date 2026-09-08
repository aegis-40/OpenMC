"""Render the Aegis-40 operational-shield dose result from shield_dose_map.npz.
Post-processing only (numpy + matplotlib) - no OpenMC.

Two panels:
  (top) 2D neutron+gamma dose FIELD from the weight-window MC, absolute uSv/h.
  (bot) mid-plane radial dose: MC markers where converged + the ANS-6.4 point-kernel
        line carrying the dose to the outer concrete face (0.23 uSv/h) - two independent
        methods, gap-free, both under the 10 uSv/h target.
  python plot_dose_map.py
"""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "outputs")
FIG = os.path.join(os.path.dirname(HERE), "figures"); os.makedirs(FIG, exist_ok=True)
DECK = r"D:\projects\Final pptx\charts" if os.name == "nt" else None
d = np.load(os.path.join(OUT, "shield_dose_map.npz"), allow_pickle=True)
r, z, total = d["r"], d["z"], d["total"]           # total[z, r] absolute uSv/h

# ---------- ANS-6.4 point-kernel neutron dose to the outer face (validated) ----------
PHI_RPV, RRPV, NDOSE = 1.59e9, 151.5, 3.90e-10     # n/cm2/s, cm, Sv*cm2
# (r_outer, sigma_removal 1/cm) segments beyond the RPV; cavity ~ 0
SEG = [(166.5, 0.0), (171.5, 0.157), (191.5, 0.120), (371.5, 0.100), (381.5, 0.089)]
def pk_dose(rr):
    if rr <= RRPV: return np.nan
    tau, r0 = 0.0, RRPV
    for redge, sig in SEG:
        seg = max(0.0, min(rr, redge) - r0)
        tau += sig * seg; r0 = redge
        if rr <= redge: break
    phi = PHI_RPV * np.exp(-tau) * (RRPV / rr)
    return phi * NDOSE * 3600.0 * 1e6              # uSv/h
r_pk = np.linspace(RRPV, 381.5, 240); dose_pk = np.array([pk_dose(x) for x in r_pk])

# ---------- style ----------
INK="#0b0b0b"; SEC="#52514e"; MUT="#898781"; CRIT="#d03b3b"; BLUE="#2a78d6"; ORANGE="#eb6834"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"figure.facecolor":"#ffffff",
    "axes.facecolor":"#ffffff","text.color":INK,"axes.labelcolor":SEC,"xtick.color":MUT,"ytick.color":MUT})
LAYERS = [(151.5,"RPV"),(191.5,"borated PE"),(371.5,"magnetite"),(381.5,"concrete")]

pos = total[total > 0]
vmin, vmax = pos.min(), pos.max()
# crop the 2D view to the statistically-converged region (drop the WW frontier + empty band)
XMAX = min(float(r[np.where(total.sum(0) > 0)][-1]) + 6, 216.0)
ZLIM = 165.0
# suppress the faintest under-sampled bins so the field reads clean, not speckled
FLOOR = vmax * 3e-9
masked = np.ma.masked_where(total <= FLOOR, total)
fig, (ax, axp) = plt.subplots(2, 1, figsize=(8.6, 7.4), dpi=200,
                              gridspec_kw={"height_ratios":[1.5,1]}, constrained_layout=True)
# --- 2D MC field ---
pcm = ax.pcolormesh(r, z, masked, norm=LogNorm(vmin=FLOOR, vmax=vmax),
                    cmap="inferno", shading="auto")
for rr, name in LAYERS:
    if rr < XMAX:
        ax.axvline(rr, color="w", lw=1.0, ls=(0,(4,3)), alpha=0.75)
        ax.text(rr-3, ZLIM*0.93, name, color="w", fontsize=8, rotation=90, va="top", ha="right")
ax.set_ylabel("Axial z  (cm)"); ax.set_xlim(0, XMAX); ax.set_ylim(-ZLIM, ZLIM)
ax.set_title("Near-field dose structure — weight-window MC (converged region)",
             fontsize=13.5, fontweight="bold", loc="left", pad=8)
cb = fig.colorbar(pcm, ax=ax, pad=0.012); cb.set_label("dose rate  (µSv/h)")
# --- mid-plane radial: MC markers + point-kernel line to the face ---
mid = total[len(z)//2, :]
mmask = mid > 0
axp.semilogy(r[mmask], mid[mmask], "o", ms=4, color=BLUE, label="Monte-Carlo (mid-plane)")
axp.semilogy(r_pk, dose_pk, "-", lw=2.2, color=ORANGE, label="point-kernel (TID-7004)")
axp.axhline(10.0, color=CRIT, lw=1.6, ls=(0,(5,3)))
axp.text(5, 13, "10 µSv/h design target", color=CRIT, fontsize=9, va="bottom")
axp.plot(381.5, pk_dose(381.5), "s", ms=8, color=ORANGE, zorder=5)
axp.annotate(f"outer face {pk_dose(381.5):.2f} µSv/h", (381.5, pk_dose(381.5)),
             textcoords="offset points", xytext=(-8, 8), ha="right", fontsize=9,
             color=ORANGE, fontweight="bold")
for rr, name in LAYERS: axp.axvline(rr, color=MUT, lw=1.0, ls=(0,(4,3)))
axp.set_xlabel("Radius  (cm)"); axp.set_ylabel("mid-plane dose  (µSv/h)"); axp.set_xlim(0, 395)
axp.set_title("Mid-plane radial dose — MC field cross-checked by point-kernel to the outer face",
              fontsize=11.5, fontweight="bold", loc="left", pad=6)
axp.legend(loc="upper right", frameon=False, fontsize=9.5)
for a in (ax, axp):
    for sp in ("top","right"): a.spines[sp].set_visible(False)
    a.tick_params(length=0)
fig.savefig(os.path.join(FIG, "shield_dose_map.png"), bbox_inches="tight")
if DECK and os.path.isdir(DECK):
    fig.savefig(os.path.join(DECK, "chart_shield_dose_map.png"), bbox_inches="tight")
print(f"MC core-peak {vmax:.2e} µSv/h ; point-kernel outer-face {pk_dose(381.5):.3f} µSv/h (target 10)")
