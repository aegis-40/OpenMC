#!/usr/bin/env python3
"""RESUME the fixed depletion from the last completed step (openmc prev_results).

Reads the partial depletion_results.h5 in the run dir, rebuilds the identical
model (same deterministic cell path as run_depletion_fixed.py), and integrates
only the REMAINING timesteps. Prior steps are carried into the final results.

Run in WSL:  OPENMC_THREADS=8 DEPLETE_STAT=fast python resume_depletion_fixed.py
"""
import json, os, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")

NB = Path("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_neutronics_FER.ipynb")
WORK = Path(os.path.expanduser("~/aegis_run/deplete_fixed"))
RUN = WORK / "aegis40_neutronics_outputs" / "08_depletion_baseline_fixedvol"
H5 = RUN / "depletion_results.h5"
assert H5.is_file(), f"no partial results at {H5}"
os.chdir(WORK)

CELLS = [4, 6, 8, 10, 12, 13, 14, 15, 16, 31, 32]
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|write_\w+|run_core_depletion|"
                  r"extract_absorber)\s*\(|\.(?:run|integrate)\s*\(")
def neutralize(src):
    out = []
    for l in src.splitlines():
        if l.lstrip().startswith("%") or "get_ipython()" in l: continue
        if l[:1] not in (" ", "\t") and not l.lstrip().startswith(("def ","class ","import ","from ","@")) and CALL.search(l):
            out.append("# [x] " + l)
        else: out.append(l)
    return "\n".join(out)

nb = json.loads(NB.read_bytes().decode("utf-8-sig", "replace"))
g = {"results": {}, "runtime_log": []}
for idx in CELLS:
    exec(compile(neutralize("".join(nb["cells"][idx]["source"])), f"c{idx}", "exec"), g)
assert g["N_CR_CLUSTERS"] == 16 and g["ER_WT_PCT"] == 0.75 and g["N_BATCHES"] == 1

import openmc, openmc.deplete
prev = openmc.deplete.Results(str(H5))
t_done = prev.get_times()          # days, includes t=0
PLAN = [0.3]*10 + [7] + [50]*2 + [100]*22
cum = np.cumsum(PLAN)
n_done = int(np.sum(cum <= t_done[-1] + 1e-6))
remaining = PLAN[n_done:]
print(f"[resume] last completed t = {t_done[-1]:.1f} d -> {n_done}/{len(PLAN)} steps done, "
      f"{len(remaining)} remaining", flush=True)
if not remaining:
    print("[resume] nothing to do"); raise SystemExit

model, _, _ = g["build_core"]()
g["_assign_depletion_volumes"](model, verbose=True)
# same FA fission mesh tally as run_core_depletion attaches
ch = g["N_CORE"] * g["FA_PITCH"] / 2.0
m = openmc.RegularMesh(); m.dimension = (g["N_CORE"], g["N_CORE"], 20)
m.lower_left = (-ch, -ch, -g["ACTIVE_HEIGHT"]/2); m.upper_right = (ch, ch, g["ACTIVE_HEIGHT"]/2)
tly = openmc.Tally(name="fa_fission"); tly.filters = [openmc.MeshFilter(m)]; tly.scores = ["fission"]
model.tallies = openmc.Tallies([tly])
stats = {"fast": g["STAT_FAST"], "medium": g["STAT_MEDIUM"], "final": g["STAT_FINAL"]}[
    os.environ.get("DEPLETE_STAT", "fast")]
model.settings.batches = stats["batches"]; model.settings.inactive = stats["inactive"]
model.settings.particles = stats["particles"]

os.chdir(RUN)
op = openmc.deplete.CoupledOperator(model, chain_file=os.environ["OPENMC_CHAIN_FILE"],
                                    prev_results=prev)
integ = openmc.deplete.PredictorIntegrator(op, remaining, power=125.0e6, timestep_units="d")
integ.integrate()
print("[resume] done - full results in", RUN / "depletion_results.h5")

r = openmc.deplete.Results(str(RUN / "depletion_results.h5"))
t = np.array(r.get_times()); k = r.get_keff()[1][:, 0]
print(f"[resume] final: {len(t)} steps, k_EOC={k[-1]:.4f} at {t[-1]:.0f} d")
print("DEPLETE_COMPLETE")
