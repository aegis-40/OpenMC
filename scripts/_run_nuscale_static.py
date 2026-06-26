"""Static neutronics of the NuScale-like DISCRETE loading pattern (the figure),
made BORON-FREE for Aegis-40. Step 1: BOC k_eff + F_q (peaking). MTC/DTC next.
Uses the Fridman/Ez-Aldeen deck (exact 7-type pattern + heavy reflector), VII.1."""
import os
import numpy as np
import openmc
import openmc.stats
import nuscale.materials
from nuscale.core import core_geometry

# --- make it boron-free: strip soluble boron from the coolant ---
c = nuscale.materials.mats["coolant"]
for nuc in ("B10", "B11"):
    try:
        c.remove_nuclide(nuc)
    except Exception:
        pass
print("[static] coolant now:", [n[0] for n in c.nuclides], "(boron-free)")

geom = core_geometry(control_rods="all_rods_out10")
ll, ur = geom.bounding_box

# fission mesh for peaking (fine ~sub-pin radial)
mesh = openmc.RegularMesh()
mesh.dimension = (170, 170, 8)
mesh.lower_left = (ll[0], ll[1], ll[2])
mesh.upper_right = (ur[0], ur[1], ur[2])
ft = openmc.Tally(name="fission")
ft.filters = [openmc.MeshFilter(mesh)]
ft.scores = ["fission"]

try:
    src = openmc.IndependentSource(space=openmc.stats.Box(ll, ur),
                                   constraints={"fissionable": True})
except Exception:
    src = openmc.Source(space=openmc.stats.Box(ll, ur)); src.space.only_fissionable = True

s = openmc.Settings()
s.batches, s.inactive, s.particles = 120, 30, 40000
s.source = src
s.temperature = {"method": "interpolation", "range": (290.0, 1500.0)}

model = openmc.Model(geometry=geom,
                     materials=openmc.Materials(nuscale.materials.mats.values()),
                     settings=s, tallies=openmc.Tallies([ft]))
print("[static] running BOC eigenvalue + F_q mesh ...", flush=True)
sp = model.run(threads=8, output=True)
with openmc.StatePoint(sp) as st:
    k = st.keff
    fis = st.get_tally(name="fission").mean.ravel()

nz = fis[fis > 0]
Fq = nz.max() / nz.mean()
# axial F_z: collapse to axial, radial F_xy: collapse to radial
g = fis.reshape(170, 170, 8)
axial = g.sum(axis=(0, 1)); Fz = axial.max() / axial[axial > 0].mean()
radial = g.sum(axis=2); rr = radial[radial > 0]; Fxy = rr.max() / rr.mean()

print(f"\n[static] BOC k_inf-ish (ARO, boron-free) = {k.nominal_value:.5f} "
      f"+/- {k.std_dev*1e5:.0f} pcm")
print(f"[static] F_q  (mesh max/avg)  = {Fq:.3f}   (limit ~2.32)")
print(f"[static] F_xy (radial peak)   = {Fxy:.3f}")
print(f"[static] F_z  (axial peak)    = {Fz:.3f}")
print(f"[static] (mesh-based, includes intra-assembly/Gd-pin local peaking)")
