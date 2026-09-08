"""Aegis-40 - LCOE one-at-a-time sensitivity (tornado), FER Section 8.12.

Drives the SAME discounted constant-annuity LCOE model as economics_lcoe.py and
swings each driver across a defensible band around the NOAK base case
(OCC 3500 $/kWe, r 7 %, 95 % CF, 3-yr build), holding the others fixed. Output:
a tornado PNG for the finals deck + a CSV of the swings.

  python lcoe_tornado.py
"""
import os, math, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory as bt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(os.path.dirname(HERE), "figures"); os.makedirs(FIG, exist_ok=True)
OUT = os.path.join(os.path.dirname(HERE), "outputs"); os.makedirs(OUT, exist_ok=True)
DECK = r"D:\projects\Final pptx\charts"; os.makedirs(DECK, exist_ok=True)

# ---- front-end fuel cost from physics (same as economics_lcoe.py) ----
XF, XT, XP = 0.00711, 0.0025, 0.0443
U3O8_PER_LB, CONV, SWU_PRICE, FAB = 85.75, 25.0, 176.0, 300.0
U_IN_U3O8, LB_PER_KG, HM_PER_YR = 0.8480, 2.20462, 1465.0
vfun = lambda x: (2*x-1)*math.log(x/(1-x))
FP = (XP-XT)/(XF-XT); TP = (XP-XF)/(XF-XT)
SWU = vfun(XP) + TP*vfun(XT) - FP*vfun(XF)
front_kgHM = FP/U_IN_U3O8*LB_PER_KG*U3O8_PER_LB + FP*CONV + SWU*SWU_PRICE + FAB
front_yr = front_kgHM*HM_PER_YR
GEN_SOLD, GEN_CAP = 316236.0, 299640.0
fuel_base = front_yr/GEN_SOLD + 1.0           # $/MWh
P_MWE, LIFE = 40.0, 60

crf = lambda r,n: r*(1+r)**n/((1+r)**n-1)
idc = lambda r,y: (1+r)**(y/2.0)

# base case
B = dict(occ=3500.0, r=0.07, cf=0.95, constr=3.0, oandm=19.64, fuelmult=1.0)
def lcoe(occ, r, cf, constr, oandm, fuelmult):
    cap = occ*idc(r,constr)*P_MWE*1e3*crf(r,LIFE)/(GEN_CAP*(cf/0.95))
    return cap + oandm + fuel_base*fuelmult
base = lcoe(**B)

# one-at-a-time bands (label, low_kwargs, high_kwargs, range-text)
def var(**kw):
    d = dict(B); d.update(kw); return lcoe(**d)
PARAMS = [
    ("Overnight capital",  var(occ=3500.0), var(occ=8250.0), "$3,500–8,250/kWe"),
    ("Discount rate",      var(r=0.03),     var(r=0.10),     "3–10 %"),
    ("Capacity factor",    var(cf=0.95),    var(cf=0.90),    "90–95 %"),
    ("Construction time",  var(constr=3.0), var(constr=6.0), "3–6 yr"),
    ("Fuel-cycle cost",    var(fuelmult=0.70), var(fuelmult=1.30), "±30 %"),
    ("O&M + back-end",     var(oandm=19.64*0.75), var(oandm=19.64*1.25), "±25 %"),
]
# sort by swing (largest at top)
PARAMS.sort(key=lambda p: abs(p[2]-p[1]))

# ---- style ----
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#0b0b0b"; SEC="#52514e"; MUT="#898781"; GRID="#e1e0d9"; BASE="#c3c2b7"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"figure.facecolor":"#ffffff",
    "axes.facecolor":"#ffffff","text.color":INK,"axes.labelcolor":SEC,"xtick.color":MUT,"ytick.color":MUT})
fig, ax = plt.subplots(figsize=(8.6,4.8), dpi=200)
for i,(name,lo,hi,rng) in enumerate(PARAMS):
    fav, unf = min(lo,hi), max(lo,hi)
    ax.barh(i, fav-base, left=base, height=0.62, color=BLUE, edgecolor="#fff", linewidth=1.2, zorder=3)
    ax.barh(i, unf-base, left=base, height=0.62, color=ORANGE, edgecolor="#fff", linewidth=1.2, zorder=3)
    ax.text(fav-1.2, i, f"${fav:.0f}", va="center", ha="right", fontsize=10, color=BLUE, fontweight="bold")
    ax.text(unf+1.2, i, f"${unf:.0f}", va="center", ha="left", fontsize=10, color=ORANGE, fontweight="bold")
ax.axvline(base, color=INK, lw=1.6, zorder=4)
ax.text(base, 1.01, f"base ${base:.1f}/MWh", transform=bt(ax.transData, ax.transAxes),
        ha="center", va="bottom", fontsize=10, fontweight="bold", color=INK)
ax.set_yticks(range(len(PARAMS)))
ax.set_yticklabels([f"{n}\n{r}" for n,_,_,r in PARAMS], fontsize=10, color=SEC)
ax.set_xlabel("LCOE  ($/MWh, 7 % discount)")
ax.set_xlim(46, 133)
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(BASE); ax.tick_params(length=0)
ax.xaxis.grid(True, color=GRID, lw=1.0); ax.set_axisbelow(True)
fig.suptitle("LCOE sensitivity — one driver at a time", x=0.14, y=0.98, ha="left", fontsize=15, fontweight="bold")
fig.text(0.14, 0.915, "blue = lowers cost · orange = raises cost · NOAK base case", fontsize=9.5, color=MUT)
fig.tight_layout(rect=(0,0,1,0.88))
fig.savefig(os.path.join(FIG,"lcoe_tornado.png")); fig.savefig(os.path.join(DECK,"chart_lcoe_tornado.png"))
print(f"base LCOE = {base:.2f} $/MWh ; fuel = {fuel_base:.2f}")
with open(os.path.join(OUT,"lcoe_tornado.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["parameter","range","lcoe_low","lcoe_high","swing"])
    for n,lo,hi,r in PARAMS: w.writerow([n,r,f"{min(lo,hi):.1f}",f"{max(lo,hi):.1f}",f"{abs(hi-lo):.1f}"])
print("wrote lcoe_tornado.png (+ deck copy) and lcoe_tornado.csv")
