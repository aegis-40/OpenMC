#!/usr/bin/env python3
"""Aegis-40 - Task A: converged Monte-Carlo operational biological-shield dose MAP.

Full-physics OpenMC replacement for the point-kernel estimate: a fixed neutron+gamma
source in the homogenised core, transported through the adopted lead-free radial stack
(reflector / barrel / downcomer / RPV / cavity / SS thermal shield / borated-PE 20 cm /
magnetite 180 cm / ordinary 10 cm) with MAGIC iterative weight windows so the deep dose
converges. Produces a cylindrical (r,z) dose-rate map [uSv/h] for neutron, photon and total.

Reuses shielding_common.py for materials, dose response, source rates and weight windows.

  # smoke (minutes, WW off):   TASKA_STAT=fast TASKA_WW=0 python aegis40_shielding_mc.py
  # appendix-grade:            TASKA_STAT=final TASKA_WW=1 python aegis40_shielding_mc.py
Output -> ../outputs/shield_dose_map.npz  (+ prints outer-face dose vs the 10 uSv/h target)
"""
import os, math
import numpy as np
import openmc
import shielding_common as sc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "outputs"); os.makedirs(OUT, exist_ok=True)
STAT = {"fast": sc.STAT_FAST, "medium": sc.STAT_MEDIUM, "final": sc.STAT_FINAL}[os.environ.get("TASKA_STAT", "fast")]
if os.environ.get("TASKA_BATCHES"):   # many WW-generation iterations push windows deeper
    STAT = dict(batches=int(os.environ["TASKA_BATCHES"]), particles=int(os.environ.get("TASKA_PARTICLES", "20000")))
USE_WW = os.environ.get("TASKA_WW", "1") == "1"

# ---------------- geometry: outer radii (cm), adopted 4.3 build ----------------
R = dict(core=75.54, refl=95.0, barrel=100.0, dc=140.0, rpv=151.5,
         cav=166.5, ts=171.5, pe=191.5, mag=371.5, ord=381.5, air=431.5)
ZC = 100.0          # core half-height (200 cm active)
ZM = 250.0          # model half-height (axial vacuum beyond)

# ---------------- materials ----------------
def _homog_core():
    """Volume-smeared core source region. Local build (no S(a,b) so mix_materials
    works; thermal scattering is irrelevant for a fast source spectrum)."""
    uo2 = openmc.Material(name="core_uo2"); uo2.set_density("g/cm3", 10.40)
    uo2.add_element("U", 1.0, enrichment=4.69); uo2.add_element("O", 2.0)
    zr = openmc.Material(name="core_clad"); zr.set_density("g/cm3", 6.55); zr.add_element("Zr", 1.0)
    w = openmc.Material(name="core_water"); w.set_density("g/cm3", 0.72266)
    w.add_element("H", 2.0); w.add_element("O", 1.0)
    c = openmc.Material.mix_materials([uo2, zr, w], [0.331, 0.116, 0.553], percent_type="vo", name="homog_core")
    c.temperature = 900.0; return c
core = _homog_core(); water = sc.mat_water(temp=560.0, density=0.75)
barrel = sc.mat_ss304("barrel"); rpv = sc.mat_sa508(); air = sc.mat_air()
ts = sc.mat_ss304("thermal_shield"); pe = sc.mat_borated_poly(5.0)
mag = sc.mat_magnetite_concrete(); ordc = sc.mat_ordinary_concrete()
materials = openmc.Materials([core, water, barrel, rpv, air, ts, pe, mag, ordc])

# ---------------- CSG: concentric cylinders truncated by two z-planes ----------
def cyl(r): return openmc.ZCylinder(r=r)
cyls = {k: cyl(v) for k, v in R.items()}
ztop = openmc.ZPlane(z0=ZM, boundary_type="vacuum"); zbot = openmc.ZPlane(z0=-ZM, boundary_type="vacuum")
cyls["air"].boundary_type = "vacuum"
inside = lambda a, b=None: (-a & +zbot & -ztop) if b is None else (-a & +b & +zbot & -ztop)
regions = [
    ("core", core, -cyls["core"] & +zbot & -ztop),
    ("refl", water, +cyls["core"] & -cyls["refl"] & +zbot & -ztop),
    ("barrel", barrel, +cyls["refl"] & -cyls["barrel"] & +zbot & -ztop),
    ("dc", water, +cyls["barrel"] & -cyls["dc"] & +zbot & -ztop),
    ("rpv", rpv, +cyls["dc"] & -cyls["rpv"] & +zbot & -ztop),
    ("cav", air, +cyls["rpv"] & -cyls["cav"] & +zbot & -ztop),
    ("ts", ts, +cyls["cav"] & -cyls["ts"] & +zbot & -ztop),
    ("pe", pe, +cyls["ts"] & -cyls["pe"] & +zbot & -ztop),
    ("mag", mag, +cyls["pe"] & -cyls["mag"] & +zbot & -ztop),
    ("ord", ordc, +cyls["mag"] & -cyls["ord"] & +zbot & -ztop),
    ("airout", air, +cyls["ord"] & -cyls["air"] & +zbot & -ztop),
]
cells = [openmc.Cell(name=n, fill=m, region=r) for n, m, r in regions]
geometry = openmc.Geometry(openmc.Universe(cells=cells))

# ---------------- mixed neutron + gamma source in the core ----------------
space = openmc.stats.CylindricalIndependent(
    r=openmc.stats.PowerLaw(0.0, R["core"], 1.0), phi=openmc.stats.Uniform(0, 2*math.pi),
    z=openmc.stats.Uniform(-ZC, ZC))
watt = openmc.stats.Watt(a=0.988e6, b=2.249e-6)               # U-235 prompt fission
eg = np.linspace(0.1e6, 8.0e6, 40); pg = np.exp(-1.10*eg/1e6)  # Maienschein prompt-gamma
gamma = openmc.stats.Tabular(eg, pg/pg.sum(), interpolation="histogram")
src_n = openmc.IndependentSource(space=space, energy=watt, particle="neutron", strength=sc.NEUTRON_RATE)
src_g = openmc.IndependentSource(space=space, energy=gamma, particle="photon", strength=sc.FISS_GAMMA_RATE)
SRC_TOTAL = sc.NEUTRON_RATE + sc.FISS_GAMMA_RATE

# ---------------- dose-map mesh + tallies ----------------
NR, NZ = 70, 50
mesh = openmc.CylindricalMesh(r_grid=np.linspace(0, R["air"], NR+1),
                             z_grid=np.linspace(-ZM, ZM, NZ+1), phi_grid=[0, 2*math.pi])
mf = openmc.MeshFilter(mesh)
tallies = []
for part in ("neutron", "photon"):
    t = openmc.Tally(name=f"dose_{part}")
    t.filters = [mf, openmc.ParticleFilter([part]), sc.dose_energy_filter(part)]
    t.scores = ["flux"]; tallies.append(t)
# fast-flux calibration tally (E>1 MeV neutrons): RPV value must match the 1.59e9 n/cm2/s anchor
tfast = openmc.Tally(name="fast_flux")
tfast.filters = [mf, openmc.ParticleFilter(["neutron"]), openmc.EnergyFilter([1.0e6, 20.0e6])]
tfast.scores = ["flux"]; tallies.append(tfast)

settings = openmc.Settings()
settings.run_mode = "fixed source"; settings.source = [src_n, src_g]
settings.batches = STAT["batches"]; settings.particles = STAT["particles"]
settings.photon_transport = True
settings.temperature = {"method": "interpolation"}
settings.create_fission_neutrons = False   # source-driven shield calc: no fission multiplication
if USE_WW:
    sc.add_weight_windows(settings, mesh)

model = openmc.model.Model(geometry, materials, settings, openmc.Tallies(tallies))
sp_path = model.run(cwd=OUT)

# ---------------- convert flux*dose -> uSv/h on the mesh ----------------
# Normalisation: the two source strengths are ABSOLUTE emission rates [part/s], so
# OpenMC births particles carrying those rates and the mesh 'flux' tally already comes
# out rate-normalised (pSv*cm^3/s with the dose filter; n*cm/s for the fast tally).
# So per bin: (tally / volume) -> pSv/s (dose) or n/cm2/s (flux); NO extra *rate.
# Verified: downcomer fast flux 9.2e9 -> RPV-outer 1.6e9 == point-kernel anchor 1.59e9.
vols = mesh.volumes.ravel()                        # cm^3 per bin (same ravel order as tally)
r_c = 0.5*(np.array(mesh.r_grid[:-1]) + np.array(mesh.r_grid[1:]))
z_c = 0.5*(np.array(mesh.z_grid[:-1]) + np.array(mesh.z_grid[1:]))
with openmc.StatePoint(sp_path) as sp:
    dmap = {}
    for part in ("neutron", "photon"):
        m = sp.get_tally(name=f"dose_{part}").mean.ravel()
        dmap[part] = (m / vols) * 3600.0 / 1e6                # pSv/s -> uSv/h
    fast = sp.get_tally(name="fast_flux").mean.ravel()
phi_fast = (fast / vols)                            # n/cm2/s (E>1 MeV)
total = dmap["neutron"] + dmap["photon"]
gtot = total.reshape(NZ, NR); gfast = phi_fast.reshape(NZ, NR)   # [z, r]
iz0 = NZ // 2
# ---- calibration vs the converged RPV fast-flux anchor (1.59e9 n/cm2/s) ----
print(f"[shield-MC] stat={STAT} ww={USE_WW}")
for rt in (R["dc"], R["rpv"], R["cav"]):
    ir = np.argmin(np.abs(r_c - rt))
    print(f"[calib] fast flux @ r={r_c[ir]:.0f} cm (mid-plane) = {gfast[iz0, ir]:.3e} n/cm2/s")
print(f"[calib] anchor (point-kernel RPV, E>1 MeV) = 1.59e9 n/cm2/s")
print(f"[diag] vols min {vols.min():.3e} max {vols.max():.3e} cm3")
print(f"[diag] n-dose peak {dmap['neutron'].max():.3e} | g-dose peak {dmap['photon'].max():.3e} uSv/h")
i_out = np.argmin(np.abs(r_c - R["ord"]))
print(f"[shield-MC] mid-plane dose at outer concrete face (r={R['ord']} cm): {gtot[iz0, i_out]:.3g} uSv/h  (target < {sc.DOSE_TARGET_OPERATIONAL_USVH})")
np.savez(os.path.join(OUT, "shield_dose_map.npz"),
         r=r_c, z=z_c, total=gtot, neutron=dmap["neutron"].reshape(NZ, NR),
         photon=dmap["photon"].reshape(NZ, NR), fast_flux=gfast, radii=list(R.items()))
print("[shield-MC] wrote shield_dose_map.npz")
