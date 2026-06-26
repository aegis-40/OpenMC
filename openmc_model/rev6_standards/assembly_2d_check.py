#!/usr/bin/env python3
"""
2D single-assembly infinite-lattice depletion check for the Aegis-40 core.

Purpose
-------
Confirm — cheaply, before committing the full 3D core run — that the depletion
fix now in the notebook (CECM integrator + ~1 GWd/t steps through the Gd burnout
window) produces a SMOOTH k_inf(burnup) curve instead of the sharp "mountain"
sawtooth. This is the same physics that drives the core curve, isolated to one
assembly, so it runs in a fraction of the time.

How it stays faithful
---------------------
It does NOT re-derive any geometry or materials. It execs the rev_6 notebook's
own definition cells (imports / config / materials / pin & assembly builders,
stopping right before any simulation cell) and reuses `_build_fa_universe`
exactly. The only thing added here is a reflective box around ONE assembly to
make it an infinite 2D lattice (k_inf), plus the depletion driver.

Run (WSL, openmc env):
    cd openmc_model/rev6_standards
    /mnt/d/conda-envs/openmc-py311/bin/python assembly_2d_check.py

Outputs (in ./assembly_2d_outputs/):
    kinf_vs_burnup_2D.png      the curve
    kinf_vs_burnup_2D.csv      burnup[GWd/t], k_inf, sigma
    depletion_results.h5       raw OpenMC depletion results

Cheap-fallback knob: set INTEGRATOR = "predictor" below to halve the transport
cost (fine steps alone remove most of the sawtooth).
"""
import os, sys, json, math, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openmc
import openmc.deplete

# ----------------------------------------------------------------------------- config
INTEGRATOR  = "cecm"     # "cecm" (matches notebook) or "predictor" (cheaper)
TIMESTEPS_D = [10, 20, 30, 40] + [45] * 16 + [125] * 9   # identical to the notebook
PARTICLES   = 3000       # per batch; shape is robust, no need for production stats
INACTIVE    = 15
BATCHES     = 55
Z_SLICE_CM  = 20.0       # reflective axial slice height (infinite-Z); mid-active
# -----------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
NB   = os.path.join(HERE, "aegis40_3d_core_notebook_rev6.ipynb")
OUT  = os.path.join(HERE, "assembly_2d_outputs")
os.makedirs(OUT, exist_ok=True)

# ── 1) exec the notebook's DEFINITION cells only (stop right after build_core) ──
print("[1/5] loading notebook definitions (materials + geometry builders)...")
ns = {}
nb = json.load(open(NB, encoding="utf-8"))
for c in nb["cells"]:
    if c.get("cell_type") != "code":
        continue
    src = "".join(c["source"])
    code = "\n".join(l for l in src.splitlines()
                     if not l.lstrip().startswith(("%", "!")))   # strip magics/shell
    exec(compile(code, "<nb-def>", "exec"), ns)
    if "def build_core" in src:           # everything we need is now defined
        break

# pull the names we use
FA_PITCH      = ns["FA_PITCH"];     PIN_PITCH = ns["PIN_PITCH"];  N_PIN = ns["N_PIN"]
FUEL_RADIUS   = ns["FUEL_RADIUS"];  RHO_UO2   = ns["RHO_UO2"]
T_FUEL_K      = ns["T_FUEL_K"];     T_MOD_K   = ns["T_MOD_K"];    RHO_WATER_NOM = ns["RHO_WATER_NOM"]
ENRICH_INNER  = ns["ENRICH_INNER"]; ENRICH_MID = ns["ENRICH_MID"]; ENRICH_OUTER = ns["ENRICH_OUTER"]
GD_WT_PCT     = ns["GD_WT_PCT"];    ER_WT_PCT = ns["ER_WT_PCT"];  N_ER_RODS = ns["N_ER_RODS"]
SPECIFIC_POWER = ns["SPECIFIC_POWER"]                              # W/gHM == MW/tHM
GD_POSITIONS  = ns["GD_POSITIONS"]; ER_POSITIONS = ns["ER_POSITIONS"]; GUIDE_ALL = set(ns["GUIDE_ALL"])
_enrichment_for_pin = ns["_enrichment_for_pin"]

# ── 2) materials: mirror build_core's HFP-nominal prep exactly ──────────────────
print("[2/5] building materials...")
mat_water    = ns["mat_water"];   mat_zircaloy = ns["mat_zircaloy"]; mat_helium = ns["mat_helium"]
mat_b4c      = ns["mat_b4c"];     mat_uo2      = ns["mat_uo2"];      _mixed_fuel = ns["_mixed_fuel"]
fuel_temp, mod_temp = T_FUEL_K, T_MOD_K

water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_active")
clad  = mat_zircaloy(temp=mod_temp)
gap   = mat_helium(temp=fuel_temp)
b4c   = mat_b4c(temp=600.0)
plain_mats = {}
for e in (ENRICH_INNER, ENRICH_MID, ENRICH_OUTER):
    plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")
gd_mat     = _mixed_fuel(ENRICH_MID, gd_wt=GD_WT_PCT, er_wt=0.0, temp=fuel_temp, name="Gd_fuel")
gd_cut_mat = mat_uo2(ENRICH_MID, temp=fuel_temp, name="Gd_cutback_UO2")
if N_ER_RODS > 0 and ER_WT_PCT > 0:
    er_mat = _mixed_fuel(ENRICH_MID, gd_wt=0.0, er_wt=ER_WT_PCT, temp=fuel_temp, name="Er_fuel")
else:
    er_mat = None

# ── 3) one assembly universe (ARO), wrapped in a reflective box -> 2D k_inf ─────
print("[3/5] building single-assembly geometry (reflective BCs)...")
fa_u = ns["_build_fa_universe"](fuel_temp, mod_temp, water, clad, gap, b4c,
                                plain_mats, gd_mat, gd_cut_mat, er_mat,
                                insert_cr=False, name="FA2D",
                                gd_positions=GD_POSITIONS, er_positions=ER_POSITIONS)
half = FA_PITCH / 2.0
hz   = Z_SLICE_CM / 2.0
xlo = openmc.XPlane(-half, boundary_type="reflective"); xhi = openmc.XPlane(half, boundary_type="reflective")
ylo = openmc.YPlane(-half, boundary_type="reflective"); yhi = openmc.YPlane(half, boundary_type="reflective")
zlo = openmc.ZPlane(-hz,  boundary_type="reflective");  zhi = openmc.ZPlane(hz,  boundary_type="reflective")
root = openmc.Cell(fill=fa_u, region=+xlo & -xhi & +ylo & -yhi & +zlo & -zhi)
geom = openmc.Geometry([root])

# depletable-material volumes (mirror _build_fa_universe's pin precedence) ───────
pin_vol = math.pi * FUEL_RADIUS**2 * Z_SLICE_CM
gd_n = er_n = 0
plain_n = {}
for j in range(N_PIN):
    for i in range(N_PIN):
        pos = (i, j)
        if pos in GUIDE_ALL:                              # guide / instrument tube
            continue
        elif pos in GD_POSITIONS:
            gd_n += 1
        elif pos in ER_POSITIONS and er_mat is not None:
            er_n += 1
        else:
            e = _enrichment_for_pin(i, j)
            plain_n[e] = plain_n.get(e, 0) + 1

gd_mat.volume = gd_n * pin_vol; gd_mat.depletable = True
for e, n in plain_n.items():
    m = plain_mats[f"UO2_{e:.1f}"]; m.volume = n * pin_vol; m.depletable = True
if er_mat is not None and er_n > 0:
    er_mat.volume = er_n * pin_vol; er_mat.depletable = True
n_fuel = gd_n + er_n + sum(plain_n.values())
print(f"      pins: {n_fuel} fuel  (Gd {gd_n}, Er {er_n}, plain {sum(plain_n.values())})"
      f" + {len(GUIDE_ALL)} guide  | specific power {SPECIFIC_POWER:.2f} W/gHM")

# ── 4) settings + depletion ─────────────────────────────────────────────────────
settings = openmc.Settings()
settings.particles = PARTICLES
settings.inactive  = INACTIVE
settings.batches   = BATCHES
settings.temperature = {"method": "interpolation"}
settings.source = openmc.IndependentSource(
    space=openmc.stats.Box((-half, -half, -hz), (half, half, hz), only_fissionable=True))
settings.output = {"tallies": False}
mats  = openmc.Materials(geom.get_all_materials().values())
model = openmc.Model(geometry=geom, settings=settings, materials=mats)

os.chdir(OUT)   # keep all transport scratch + results in the output folder
print(f"[4/5] depleting: {INTEGRATOR.upper()} integrator, {len(TIMESTEPS_D)} steps, "
      f"~{SPECIFIC_POWER*sum(TIMESTEPS_D)/1000:.0f} GWd/t horizon ...")
t0 = time.time()
op = openmc.deplete.CoupledOperator(model)      # chain comes from openmc.config (set by notebook)
Integrator = (openmc.deplete.CECMIntegrator if INTEGRATOR == "cecm"
              else openmc.deplete.PredictorIntegrator)
Integrator(op, TIMESTEPS_D, power_density=SPECIFIC_POWER, timestep_units="d").integrate()
print(f"      depletion finished in {(time.time()-t0)/60:.1f} min")

# ── 5) read, save, plot ─────────────────────────────────────────────────────────
print("[5/5] writing curve...")
res = openmc.deplete.Results(os.path.join(OUT, "depletion_results.h5"))
t_d, kff = res.get_keff(time_units="d")
kmean = np.asarray(kff)[:, 0]; ksig = np.asarray(kff)[:, 1]
bu = SPECIFIC_POWER * np.asarray(t_d) / 1000.0          # GWd/tHM

np.savetxt(os.path.join(OUT, "kinf_vs_burnup_2D.csv"),
           np.column_stack([bu, kmean, ksig]),
           header="burnup_GWd_t,k_inf,sigma", delimiter=",", comments="")

dk = np.diff(kmean)
sign_flips = int(np.sum(np.diff(np.sign(dk)) != 0))     # smoothness proxy
print("\n   burnup[GWd/t]   k_inf     sigma")
for b, k, s in zip(bu, kmean, ksig):
    print(f"   {b:9.2f}   {k:8.5f}  {s:7.5f}")
print(f"\n   peak k_inf = {kmean.max():.5f} at {bu[np.argmax(kmean)]:.1f} GWd/t"
      f"  | monotonic-after-peak slope changes = {sign_flips}"
      f"  ({'SMOOTH' if sign_flips <= 2 else 'still jagged'})")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.errorbar(bu, kmean, yerr=ksig, fmt="-o", ms=3, lw=1.3, capsize=2, color="#c0392b")
ax.axhline(1.0, color="grey", ls="--", lw=0.8)
ax.set_xlabel("Burnup (GWd/tHM)"); ax.set_ylabel(r"$k_\infty$  (2D assembly, ARO)")
ax.set_title(f"Aegis-40 single-assembly depletion — {INTEGRATOR.upper()}, "
             f"{len(TIMESTEPS_D)} steps")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "kinf_vs_burnup_2D.png"), dpi=150)
print(f"\n   saved -> {os.path.join(OUT, 'kinf_vs_burnup_2D.png')}")
