"""Run the Fridman/Ez-Aldeen NuScale-like benchmark, All-Rods-Out, in OpenMC with
ENDF/B-VII.1 (matching the benchmark library). Compares our k_eff to the published
Serpent reference (1.02768) and Ez Aldeen's OpenMC (1.02786).

Deck: Zenodo 15231335 (Ez Aldeen 2025); benchmark: Fridman et al., NET 2023 / RODARE 2457.
Reduced statistics vs the paper's 2.7e9 histories (env-overridable)."""
import os
import openmc
import openmc.stats
import nuscale.materials
from nuscale.core import core_geometry

B = int(os.environ.get("NS_BATCHES", "120"))
I = int(os.environ.get("NS_INACTIVE", "20"))
P = int(os.environ.get("NS_PARTICLES", "40000"))
T = int(os.environ.get("NS_THREADS", "8"))

geometry = core_geometry(control_rods="all_rods_out10")
ll, ur = geometry.bounding_box
try:
    src = openmc.IndependentSource(space=openmc.stats.Box(ll, ur),
                                   constraints={"fissionable": True})
except Exception:
    src = openmc.Source(space=openmc.stats.Box(ll, ur))
    src.space.only_fissionable = True

s = openmc.Settings()
s.batches, s.inactive, s.particles = B, I, P
s.source = src
s.output = {"tallies": False}
s.temperature = {"default": 900, "method": "interpolation", "range": (300.0, 1500.0)}

model = openmc.Model(geometry=geometry,
                     materials=openmc.Materials(nuscale.materials.mats.values()),
                     settings=s)
print(f"[nuscale-ARO] B={B} I={I} P={P} -> {(B-I)*P/1e6:.1f}M active histories | threads {T}")
sp = model.run(threads=T, output=True)
with openmc.StatePoint(sp) as st:
    k = st.keff
print(f"\nARO k_eff = {k.nominal_value:.5f} +/- {k.std_dev*1e5:.0f} pcm")
print(f"reference  : Serpent 1.02768 | Ez Aldeen OpenMC 1.02786  (ENDF/B-VII.1)")
print(f"our - Serpent : {(k.nominal_value-1.02768)*1e5:+.0f} pcm")
print(f"our - their OpenMC : {(k.nominal_value-1.02786)*1e5:+.0f} pcm")
