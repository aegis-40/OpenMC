"""Run all NuScale-like benchmark CR states, compute k_eff + control-rod worths,
compare to the Fridman/Ez-Aldeen reference (Serpent + OpenMC, ENDF/B-VII.1).
Writes nuscale_states_results.json for plotting."""
import os, json
import openmc, openmc.stats
import nuscale.materials
from nuscale.core import core_geometry

B = int(os.environ.get("NS_BATCHES", "100"))
I = int(os.environ.get("NS_INACTIVE", "20"))
P = int(os.environ.get("NS_PARTICLES", "80000"))
T = int(os.environ.get("NS_THREADS", "8"))

# state: (Serpent k, their OpenMC k, reference CRW vs ARO [pcm])
REF = {
    "all_rods_out10": (1.02768, 1.02786, None),
    "RE1": (1.00723, 1.00751, -1975),
    "RE2": (1.00313, 1.00333, -2381),
    "SH3": (0.98978, 0.98994, -3726),
    "SH4": (0.98971, 0.98993, -3733),
    "all_rods_in": (0.85791, 0.85822, -19255),
}
STATES = os.environ.get("NS_STATES",
                        "all_rods_out10,RE1,RE2,SH3,SH4,all_rods_in").split(",")
rho = lambda k: (k - 1.0) / k * 1e5

res = {}
for st in STATES:
    print(f"\n========== state {st} ==========", flush=True)
    geom = core_geometry(control_rods=st)
    ll, ur = geom.bounding_box
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
    m = openmc.Model(geometry=geom,
                     materials=openmc.Materials(nuscale.materials.mats.values()),
                     settings=s)
    sp = m.run(threads=T, output=True)
    with openmc.StatePoint(sp) as stt:
        k = stt.keff
    res[st] = (k.nominal_value, k.std_dev * 1e5)
    print(f"[{st}] k = {k.nominal_value:.5f} +/- {k.std_dev*1e5:.0f} pcm", flush=True)

rho_aro = rho(res["all_rods_out10"][0])
out = []
for st in STATES:
    k, sg = res[st]
    crw = rho(k) - rho_aro
    rf = REF.get(st, (None, None, None))
    out.append(dict(state=st, k=k, sigma_pcm=sg, crw_pcm=crw,
                    ref_serpent=rf[0], ref_openmc=rf[1], ref_crw=rf[2],
                    dk_serpent_pcm=((k - rf[0]) * 1e5) if rf[0] else None))
json.dump(out, open("nuscale_states_results.json", "w"), indent=2)

print("\n================ SUMMARY ================")
print(f"{'state':16s} {'k_eff':>9} {'sig':>5} {'dk_vs_Serpent':>14} {'CRW':>8} {'refCRW':>8}")
for r in out:
    dk = f"{r['dk_serpent_pcm']:+.0f}" if r['dk_serpent_pcm'] is not None else "  ref"
    rc = f"{r['ref_crw']}" if r['ref_crw'] is not None else "  --"
    print(f"{r['state']:16s} {r['k']:.5f} {r['sigma_pcm']:5.0f} {dk:>11}pcm "
          f"{r['crw_pcm']:+8.0f} {rc:>8}")
print("wrote nuscale_states_results.json")
