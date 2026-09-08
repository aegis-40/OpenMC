#!/usr/bin/env python3
"""Operating biological-shield dose — 37-FA core, LATEST CAD radial build.

Fixed-source (coupled n+gamma) shield model normalised to 125 MWth. Core is
volume-smeared (standard shielding practice - only the leakage spectrum and
integrated source strength matter). Radial build uses the final CAD radii
(37-FA core envelope R755.4, barrel R975/1000, downcomer to RPV-in R1350,
RPV R1350/1515, then the unchanged shield layer thicknesses).

Reuses shielding_common (materials, ICRP-116 dose, MAGIC weight windows).
Run:  OPENMC_THREADS=8 python shield_37fa_cad.py
Output: shielding_37fa_outputs/
"""
import os, json
import numpy as np
import openmc
import shielding_common as sc

OUT = os.path.join(os.path.dirname(__file__), "mc_meshdose_out")
os.makedirs(OUT, exist_ok=True)

# ---- LATEST CAD radial build (cm) ----
R_CORE = 75.541    # 37-FA core envelope radius (CAD 755.41 mm)
R_REFL = 97.5      # radial water reflector out to barrel ID (CAD R975)
R_BAR  = 100.0     # core barrel OD (CAD R1000)
R_DOWN = 135.0     # downcomer + OTSG annulus (water, conservative) -> RPV inner (CAD 1350)
R_RPV  = 151.5     # RPV outer (wall 160 + clad 5 mm; CAD 1515)
R_CAV  = 166.5     # reactor cavity air (15 cm standoff)
R_TSH  = 171.5     # thermal / neutron shield SS-304 (5 cm)
R_POLY = 191.5     # borated polyethylene (20 cm) -- neutron layer (adopted 4.3)
R_MAG  = 371.5     # magnetite (heavy) concrete (180 cm) -- bulk (adopted 4.3)
R_ORD  = 381.5     # ordinary concrete finish (10 cm)
R_DET  = 411.5     # outer air detector shell (30 cm), vacuum beyond
HZ     = 180.0     # axial half-height (vacuum top/bottom)

# ---- materials ----
def homog_core(enrich=4.43):
    """Volume-smeared active core as the fixed-source region (no S(a,b) so it can
    be mixed; thermal scattering is irrelevant for the fast leakage source)."""
    uo2 = openmc.Material(); uo2.set_density("g/cm3", 10.40)
    uo2.add_element("U", 1.0, enrichment=enrich); uo2.add_element("O", 2.0)
    zr = openmc.Material(); zr.set_density("g/cm3", 6.55); zr.add_element("Zr", 1.0)
    h2o = openmc.Material(); h2o.set_density("g/cm3", 0.72266)
    h2o.add_element("H", 2.0); h2o.add_element("O", 1.0)
    m = openmc.Material.mix_materials([uo2, zr, h2o], [0.331, 0.116, 0.553],
                                      percent_type="vo", name="homog_core")
    m.temperature = 900.0; return m
core = homog_core()
water = sc.mat_water(temp=575.0, density=0.72266, name="annulus_water")
ss = sc.mat_ss304(); rpv = sc.mat_sa508(); air = sc.mat_air()
poly = sc.mat_borated_poly(); mag = sc.mat_magnetite_concrete(); ordc = sc.mat_ordinary_concrete()
radii = [R_CORE, R_REFL, R_BAR, R_DOWN, R_RPV, R_CAV, R_TSH, R_POLY, R_MAG, R_ORD, R_DET]
fills = [core, water, ss, water, rpv, air, ss, poly, mag, ordc, air]
materials = openmc.Materials([core, water, ss, rpv, air, poly, mag, ordc])

# ---- geometry: nested z-bounded annuli ----
zt = openmc.ZPlane(z0=HZ, boundary_type="vacuum")
zb = openmc.ZPlane(z0=-HZ, boundary_type="vacuum")
cyl = [openmc.ZCylinder(r=r) for r in radii]
cyl[-1].boundary_type = "vacuum"
cells = []
inner = None
rpv_cell = det_cell = None
for k, (c, f) in enumerate(zip(cyl, fills)):
    region = -c & +zb & -zt
    if inner is not None:
        region = region & +inner
    cell = openmc.Cell(fill=f, region=region, name=f"lay{k}")
    if abs(radii[k] - R_RPV) < 1e-6: rpv_cell = cell
    if k == len(radii) - 1: det_cell = cell
    cells.append(cell); inner = c
geom = openmc.Geometry(openmc.Universe(cells=cells))

# ---- coupled fixed source (neutron Watt + prompt fission gamma), 125 MWth ----
space = openmc.stats.CylindricalIndependent(
    r=openmc.stats.PowerLaw(0.0, R_CORE, 1.0),          # area-uniform in the core
    phi=openmc.stats.Uniform(0.0, 2*np.pi),
    z=openmc.stats.Uniform(-100.0, 100.0))
src_n = openmc.IndependentSource(space=space, energy=openmc.stats.Watt(),
                                 particle="neutron", strength=sc.NEUTRON_RATE)
# Maienschein prompt-fission-gamma spectrum (MeV) -> intensity
eg = np.array([0.1, 0.4, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0, 7.0]) * 1e6
ig = np.array([6.6, 6.6, 8.0, 5.5, 2.6, 1.5, 0.55, 0.09, 0.015])
src_g = openmc.IndependentSource(space=space,
                                 energy=openmc.stats.Tabular(eg, ig, interpolation="linear-linear"),
                                 particle="photon", strength=sc.FISS_GAMMA_RATE)
TOTAL_RATE = sc.NEUTRON_RATE + sc.FISS_GAMMA_RATE

settings = openmc.Settings()
settings.run_mode = "fixed source"
settings.temperature = {"method": "interpolation"}
# source already IS the normalised fission emission -> no in-medium multiplication
settings.create_fission_neutrons = False
settings.source = [src_n, src_g]
settings.photon_transport = True
st = dict(batches=int(os.environ.get("SB", "40")), particles=int(os.environ.get("SP", "100000")))
settings.batches = st["batches"]; settings.particles = st["particles"]
# MAGIC weight windows on a radial mesh (deep bioshield dose only). Disable with
# USE_WW=0 for a clean analog near-field run (RPV fast fluence converges without WW;
# the outer dose then reads ~0 and must be obtained from a two-stage WW run).
if os.environ.get("USE_WW", "1") == "1":
    mesh = openmc.CylindricalMesh(r_grid=np.linspace(0, R_DET, 60),
                                  z_grid=np.array([-HZ, HZ]),
                                  phi_grid=np.array([0.0, 2*np.pi]))
    sc.add_weight_windows(settings, mesh, neutron=True, photon=True)

# ---- tallies: dose outside the shield (n + gamma) + RPV fast flux ----
def dose_tally(name, cell, particle):
    t = openmc.Tally(name=name)
    t.filters = [openmc.CellFilter(cell), openmc.ParticleFilter([particle]),
                 sc.dose_energy_filter(particle)]
    t.scores = ["flux"]; return t
tallies = openmc.Tallies([
    dose_tally("dose_n", det_cell, "neutron"),
    dose_tally("dose_g", det_cell, "photon"),
])
tf = openmc.Tally(name="rpv_fast")
tf.filters = [openmc.CellFilter(rpv_cell), openmc.ParticleFilter(["neutron"]),
              openmc.EnergyFilter([1.0e6, 20.0e6])]
tf.scores = ["flux"]; tallies.append(tf)

# radial mesh neutron-dose tally -> dose(r) profile through the shield
NR = 24
dmesh = openmc.CylindricalMesh(r_grid=np.linspace(R_RPV, R_ORD, NR + 1),
                               z_grid=np.array([-HZ, HZ]), phi_grid=np.array([0.0, 2 * np.pi]))
tmp = openmc.Tally(name="dose_profile")
tmp.filters = [openmc.MeshFilter(dmesh), openmc.ParticleFilter(["neutron"]),
               sc.dose_energy_filter("neutron")]
tmp.scores = ["flux"]
tallies.append(tmp)

model = openmc.Model(geom, materials, settings, tallies)
model.export_to_xml(OUT)
openmc.run(cwd=OUT, threads=int(os.environ.get("OPENMC_THREADS", "8")), output=True)

# ---- post-process: radial dose profile ----
sp = openmc.StatePoint(os.path.join(OUT, f"statepoint.{st['batches']}.h5"))
tm = sp.get_tally(name="dose_profile")
mean = tm.mean.flatten(); err = tm.std_dev.flatten()
r_edges = np.linspace(R_RPV, R_ORD, 25); r_mid = 0.5 * (r_edges[:-1] + r_edges[1:])
vols = np.pi * (r_edges[1:] ** 2 - r_edges[:-1] ** 2) * (2 * HZ)
dose_r = mean / vols * 3600.0 / 1.0e6                # uSv/h (mean already rate-scaled)
rel = np.where(mean > 0, err / mean, 1.0)
rows = []
print("\n=== MC radial neutron-dose profile (WW) ===")
print(f"{'r_mid cm':>9} {'dose uSv/h':>12} {'rel_err':>8}")
for rm, d, re in zip(r_mid, dose_r, rel):
    conv = "converged" if re < 0.30 else ("noisy" if re < 0.60 else "unconverged")
    print(f"{rm:9.1f} {d:12.3e} {re:8.2f}  {conv}")
    rows.append(dict(r_cm=float(rm), dose_uSv_h=float(d), rel_err=float(re)))
last_ok = max([r for r in rows if r["rel_err"] < 0.30], key=lambda x: x["r_cm"], default=None)
import json
json.dump(dict(profile=rows, stats=st,
               deepest_converged=last_ok,
               note="MC (weight-window) radial neutron-dose profile to confirm the ANS-6.4 point-kernel"),
          open(os.path.join(OUT, "mc_dose_profile.json"), "w"), indent=2)
print("MC_MESHDOSE_DONE")
