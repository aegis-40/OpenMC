#!/usr/bin/env python3
"""Cycle-peaking verification (open item #1 / Adilbek Q1) - standalone.

BOC / MOC / EOC static eigenvalues with depleted compositions injected from the
STAT_FINAL depletion run (08_depletion_baseline). Verifies F_dH <= 1.65 and
F_q <= 2.32 hold through the cycle for the FINAL graded-Gd once-through core.
Retires the earlier per-step depletion-statepoint maps (non-physical edge collapse).

Run in WSL:  OPENMC_THREADS=8 STAT=medium python run_cycle_peaking.py
"""
import os, json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openmc, openmc.deplete

DEP = Path(os.environ.get("AEGIS_DEP_DIR",
      "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_neutronics_outputs/08_depletion_baseline"))
OUT = Path(os.environ.get("CYCPK_OUT", os.path.expanduser("~/aegis_run/cycle_peaking")))
OUT.mkdir(parents=True, exist_ok=True)
STAT = {"fast": dict(batches=80, inactive=25, particles=5000),
        "medium": dict(batches=180, inactive=50, particles=20000),
        "final": dict(batches=400, inactive=80, particles=50000)}[os.environ.get("STAT", "medium")]
THREADS = int(os.environ.get("OPENMC_THREADS", "8"))

# frozen basis + geometry constants (locked notebook cell 6)
N_CORE, N_PIN, FA_PITCH, ACTIVE_HEIGHT = 7, 17, 21.6038, 200.0
HM_T = 9.39; SPECIFIC_POWER = 125.0 / HM_T * 1000.0 / 1000.0  # MW/t -> W/g equiv factor used as GWd/t/day/1000
CORE_MAP = np.array([
 [0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],
 [1,1,1,1,1,1,1],[0,1,1,1,1,1,0],[0,0,1,1,1,0,0]])
PEAKING_UNC = 1.03
F_DH_LIMIT, F_Q_LIMIT = 1.65, 2.32

def reshape_xyz(flat, nx, ny, nz):
    return np.asarray(flat, float).reshape(nz, ny, nx).transpose(2, 1, 0)

dep = openmc.deplete.Results(str(DEP / "depletion_results.h5"))
t_d = np.array(dep.get_times())
bu = 0.125 * t_d / HM_T * 1000.0 / 1000.0 * 1000.0 / 1000.0  # GWd/tHM
bu = 0.125 * t_d / HM_T                                       # GW*d / tHM
kk = dep.get_keff(); kdep = kk[1][:, 0] if np.ndim(kk[1]) == 2 else np.array(kk[1])
ge = kdep >= 1.0
_downs = [i for i in range(len(kdep)-1) if ge[i] and not ge[i+1]]
_ieoc = _downs[-1] + 1 if _downs else len(bu) - 1
_imoc = 10 + int(np.argmax(kdep[10:])) if len(kdep) > 12 else len(bu)//2   # Gd hump peak
picks = {"BOC": 0, "MOC": int(_imoc), "EOC": int(_ieoc)}
print(f"[cycpk] STAT={STAT} threads={THREADS} -> {OUT}")
print(f"[cycpk] picks: " + ", ".join(f"{l}=step{i} ({bu[i]:.1f} GWd/t, k_dep={kdep[i]:.4f})" for l, i in picks.items()), flush=True)

ch = N_CORE * FA_PITCH / 2.0; NPX = N_CORE * N_PIN
rows, maps = [], {}
csv = OUT / "cycle_peaking.csv"
done = {}
if csv.exists():
    for ln in csv.read_text().splitlines()[1:]:
        p = ln.split(","); done[p[0]] = p
else:
    csv.write_text("state,burnup_GWd_t,k,k_sigma,k_dep,F_FA,F_dH,F_z,F_q\n")

for lbl, idx in picks.items():
    if lbl in done:
        p = done[lbl]; rows.append((lbl, *[float(x) for x in p[1:]]))
        print(f"[cycpk] {lbl}: already done, skipping"); continue
    mats = dep.export_to_materials(idx, path=str(DEP / "materials.xml"))
    geom = openmc.Geometry.from_xml(str(DEP / "geometry.xml"), mats)
    st = openmc.Settings()
    st.batches, st.inactive, st.particles = STAT["batches"], STAT["inactive"], STAT["particles"]
    st.source = openmc.IndependentSource(space=openmc.stats.Box(
        (-ch, -ch, -ACTIVE_HEIGHT/2), (ch, ch, ACTIVE_HEIGHT/2), only_fissionable=True))
    st.temperature = {"method": "interpolation"}
    mfa = openmc.RegularMesh(); mfa.dimension = (N_CORE, N_CORE, 20)
    mfa.lower_left = (-ch, -ch, -ACTIVE_HEIGHT/2); mfa.upper_right = (ch, ch, ACTIVE_HEIGHT/2)
    tfa = openmc.Tally(name="fa"); tfa.filters = [openmc.MeshFilter(mfa)]; tfa.scores = ["fission"]
    mpx = openmc.RegularMesh(); mpx.dimension = (NPX, NPX, 1)
    mpx.lower_left = (-ch, -ch, -ACTIVE_HEIGHT/2); mpx.upper_right = (ch, ch, ACTIVE_HEIGHT/2)
    tpx = openmc.Tally(name="pin"); tpx.filters = [openmc.MeshFilter(mpx)]; tpx.scores = ["fission"]
    model = openmc.Model(geometry=geom, settings=st, tallies=openmc.Tallies([tfa, tpx]))
    d = OUT / f"run_{lbl}"; d.mkdir(exist_ok=True)
    for f in d.glob("*.xml"): f.unlink()
    model.export_to_xml(str(d))
    openmc.run(cwd=str(d), threads=THREADS, output=False)
    sp = sorted(d.glob("statepoint.*.h5"))[-1]
    with openmc.StatePoint(str(sp)) as spt:
        k, ksig = spt.keff.n, spt.keff.s
        afa = spt.get_tally(name="fa").get_values(scores=["fission"]).ravel()
        apx = spt.get_tally(name="pin").get_values(scores=["fission"]).ravel()
    fa3 = reshape_xyz(afa, N_CORE, N_CORE, 20)
    rad = fa3.sum(axis=2); axl = fa3.sum(axis=(0, 1))
    vals = [rad[i, j] for j in range(N_CORE) for i in range(N_CORE) if CORE_MAP[N_CORE-1-j, i] == 1]
    Ffa = float(np.max(vals) / np.mean(vals))
    Fz = float((axl / axl.mean()).max())
    pin = reshape_xyz(apx, NPX, NPX, 1)[:, :, 0]
    pin = (pin + pin[::-1] + pin[:, ::-1] + pin[::-1, ::-1]); pin = (pin + pin.T) / 8.0
    hot = pin > 0.10 * pin.max()
    Fdh = float(pin[hot].max() / pin[hot].mean()) * PEAKING_UNC
    Fq = Fdh * Fz
    rows.append((lbl, float(bu[idx]), float(k), float(ksig), float(kdep[idx]), Ffa, Fdh, Fz, Fq))
    with open(csv, "a") as f:
        f.write(f"{lbl},{bu[idx]:.2f},{k:.5f},{ksig:.5f},{kdep[idx]:.5f},{Ffa:.4f},{Fdh:.4f},{Fz:.4f},{Fq:.4f}\n")
    np.save(OUT / f"radial_{lbl}.npy", rad)
    np.save(OUT / f"axial_{lbl}.npy", axl / axl.mean())
    print(f"[cycpk] {lbl}: BU={bu[idx]:5.1f}  k={k:.4f}+/-{ksig*1e5:.0f}pcm (dep {kdep[idx]:.4f})"
          f"  F_FA={Ffa:.3f}  F_dH={Fdh:.3f}(x{PEAKING_UNC} unc)  F_z={Fz:.3f}  F_q={Fq:.3f}", flush=True)

print("\n[cycpk] %-4s %-6s %-8s %-7s %-7s %-7s %-7s  limits: F_dH<=1.65, F_q<=2.32" %
      ("st", "GWd/t", "k", "F_FA", "F_dH", "F_z", "F_q"))
# NOTE: 1.65/2.32 are GENERIC PWR screening values (COLR-type, unit-specific in practice),
# not Aegis-40 design-specific acceptance limits. Exceeding them = design-specific
# COLR/MDNBR closure item, not an automatic failure (cf. CAREM 2.56, SMART 2.48 at low LHR).
allpass = True
for r in rows:
    p = "passes screening" if (r[6] <= F_DH_LIMIT and r[8] <= F_Q_LIMIT) else "SCREEN-EXCEED -> COLR/MDNBR closure"
    allpass &= (r[6] <= F_DH_LIMIT and r[8] <= F_Q_LIMIT)
    print("[cycpk] %-4s %-6.1f %-8.4f %-7.3f %-7.3f %-7.3f %-7.3f  %s" % (r[0], r[1], r[2], r[5], r[6], r[7], r[8], p))
print("[cycpk] OVERALL:", "all states pass generic screening" if allpass
      else "screening exceeded at >=1 state -> design-specific COLR basis required (see FER 8.2)")

# figure
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
for kx, (lbl, idx) in enumerate(picks.items()):
    f = OUT / f"radial_{lbl}.npy"
    if not f.exists(): continue
    rad = np.load(f)
    vals = [rad[i, j] for j in range(N_CORE) for i in range(N_CORE) if CORE_MAP[N_CORE-1-j, i] == 1]
    mean = np.mean(vals); amap = np.full((N_CORE, N_CORE), np.nan)
    for j in range(N_CORE):
        for i in range(N_CORE):
            if CORE_MAP[N_CORE-1-j, i] == 1:
                amap[j, i] = rad[i, j] / mean
                axes[kx].text(i, j, f"{amap[j,i]:.2f}", ha="center", va="center", fontsize=7)
    im = axes[kx].imshow(amap, origin="lower", cmap="hot_r")
    plt.colorbar(im, ax=axes[kx], label="relative FA power")
    axes[kx].set_title(f"Radial power - {lbl} ({bu[idx]:.0f} GWd/t)\nF_FA={np.nanmax(amap):.2f}  [FINAL graded core]")
    axes[kx].set_xlabel("assembly i"); axes[kx].set_ylabel("assembly j")
fig.tight_layout(); fig.savefig(OUT / "cycle_peaking_BOC_MOC_EOC.png", dpi=200, bbox_inches="tight")
fig2, axp = plt.subplots(figsize=(7, 5))
z = np.linspace(-ACTIVE_HEIGHT/2, ACTIVE_HEIGHT/2, 20)
for lbl in picks:
    f = OUT / f"axial_{lbl}.npy"
    if f.exists():
        axn = np.load(f)
        axp.plot(z, axn, "-o", ms=3, label=f"{lbl} (F_z={axn.max():.2f})")
axp.axhline(1, color="gray", ls="--"); axp.set_xlabel("z (cm)"); axp.set_ylabel("relative axial power")
axp.set_title("Axial power shape - BOC / MOC / EOC"); axp.legend(); axp.grid(alpha=0.3)
fig2.savefig(OUT / "power_axial_BOC_MOC_EOC.png", dpi=200, bbox_inches="tight")
print("[cycpk] figures + csv in", OUT)
print("CYCPK_COMPLETE")
