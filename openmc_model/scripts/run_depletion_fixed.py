#!/usr/bin/env python3
"""Depletion RERUN with the fixed Approach-B volume normalization (BUGFIX 2026-07-02).

Executes the def/config cells of the CLEANED notebook (openmc_model/
aegis40_neutronics_FER.ipynb - Er 0.75, 16 CRA, HM 9.39, ring-keyed volumes)
and calls run_core_depletion at STAT_MEDIUM. Outputs land on ext4 under
~/aegis_run/deplete_fixed/aegis40_neutronics_outputs/08_depletion_baseline_fixedvol.

Run in WSL:  OPENMC_THREADS=8 python run_depletion_fixed.py
"""
import json, os, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

NB = Path("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_neutronics_FER.ipynb")
WORK = Path(os.path.expanduser("~/aegis_run/deplete_fixed"))
WORK.mkdir(parents=True, exist_ok=True)
os.chdir(WORK)                                     # ROOT resolves on ext4

CELLS = [4, 6, 8, 10, 12, 13, 14, 15, 16, 31, 32]  # imports/config/builders/helpers/depletion defs
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|write_\w+|run_core_depletion|"
                  r"extract_absorber)\s*\(|\.(?:run|integrate)\s*\(")

def neutralize(src):
    out = []
    for l in src.splitlines():
        if l.lstrip().startswith("%") or "get_ipython()" in l:
            continue
        indented = l[:1] in (" ", "\t")
        isdef = l.lstrip().startswith(("def ", "class ", "import ", "from ", "@"))
        if (not indented) and (not isdef) and CALL.search(l):
            out.append("# [neutralized] " + l)
        else:
            out.append(l)
    return "\n".join(out)

nb = json.loads(NB.read_bytes().decode("utf-8-sig", "replace"))
g = {"results": {}, "runtime_log": []}
for idx in CELLS:
    c = nb["cells"][idx]
    assert c["cell_type"] == "code", f"cell {idx} not code"
    exec(compile(neutralize("".join(c["source"])), f"nbcell{idx}", "exec"), g)

# sanity: the fix must be present and the config final
sv = g["_assign_depletion_volumes"].__code__.co_consts
assert g["N_CR_CLUSTERS"] == 16 and g["ER_WT_PCT"] == 0.75 and g["N_BATCHES"] == 1
assert abs(g["HM_MASS_T"] - 9.39) < 1e-6
print("[deplete] config OK: 16 CRA, Er 0.75, once-through, HM 9.39; ring-keyed volumes", flush=True)

timesteps = [0.3]*10 + [7] + [50]*2 + [100]*22     # same schedule as STAT_FINAL run (~2310 EFPD)
stats = {"fast": g["STAT_FAST"], "medium": g["STAT_MEDIUM"],
         "final": g["STAT_FINAL"]}[os.environ.get("DEPLETE_STAT", "medium")]
print(f"[deplete] launching run_core_depletion at {stats} ...", flush=True)
m, dep, d = g["run_core_depletion"](timesteps, stats, tag="baseline_fixedvol",
                                    make_plots=False, verbose=True)
print("[deplete] run dir:", d, flush=True)
print("[deplete] k_BOL=%.5f  k_EOC=%.5f  B1=%.0f EFPD  discharge=%.1f GWd/t" % (
    m["k_bol"], m["k_eoc"], m.get("fresh_B1_efpd") or -1,
    m.get("discharge_burnup_GWd_t") or -1))
json.dump(m, open(WORK / "depletion_fixed_summary.json", "w"), indent=1, default=str)
print("DEPLETE_COMPLETE")
