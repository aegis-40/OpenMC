"""Build-only sanity check for the Takahama pincell: construct model, run ONE
short eigenvalue solve (no depletion), print BOL k_inf. Validates geometry,
materials, temperatures and library before any long depletion run."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import openmc
import benchmark_takahama_pincell as bt

openmc.config["cross_sections"] = bt.XS
openmc.config["chain_file"] = bt.CHAIN

mats, fuel, clad, mod = bt.build_materials()
geom = bt.build_geometry(fuel, clad, mod)
model = openmc.Model(geometry=geom, materials=mats)
model.settings.particles = 2000
model.settings.batches = 25
model.settings.inactive = 8
model.settings.temperature = {"method": "interpolation"}

print("materials:")
for m in mats:
    print(f"  {m.name:32s} T={m.temperature}K  rho={m.get_mass_density():.4f} g/cc")
days, powers = bt.build_schedule()
print(f"schedule: {len(days)} steps, full-power days={sum(d for d,p in bt.HISTORY if p>0)}")

import shutil
wd = "/tmp/tk_build_test"
os.makedirs(wd, exist_ok=True)
os.chdir(wd)
sp = model.run(output=False)
with openmc.StatePoint(sp) as s:
    k = s.keff
print(f"\nBOL k_inf = {k.nominal_value:.5f} +/- {k.std_dev*1e5:.0f} pcm")
