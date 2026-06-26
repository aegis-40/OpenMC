"""Extract a headless smoke-depletion runner from aegis40_neutronics_FER (4).ipynb:
include the definition/constant cells, skip the heavy top-level analysis runs,
append a driver that (1) overrides Gd/Er loading from env, (2) prints HM mass,
(3) runs a short depletion at STAT_FAST. ext4 XS via OPENMC_CROSS_SECTIONS."""
import json, re
NB = "/home/samira/fer4.ipynb"
OUT = "/home/samira/aegis_run/fer_smoke/run_fer_smoke.py"

nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]

# Keep ALL defs/consts; skip the shielding cells; and NEUTRALIZE every top-level
# analysis/run *call* (the cells are def+immediate-call, so the call must be muted).
SKIP = {31, 32}
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|build_shielded_model|_run_dir|"
                  r"_run_model|extract_absorber)\s*\(|\.(?:run|integrate)\s*\(")

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

parts = ["import matplotlib\nmatplotlib.use('Agg')\nimport os\n"]
for idx, c in enumerate(code):
    if idx in SKIP:
        continue
    parts.append(f"\n# ===== fer4 code cell #{idx} =====\n" + neutralize("".join(c["source"])) + "\n")

DRIVER = r'''
# ===== injected smoke driver =====
import math, openmc
# --- point at ext4 VIII.0 (fast) instead of the notebook's /mnt/d 9p path ---
_ext4 = os.path.expanduser("~/openmc_data")
_xs = os.path.join(_ext4, "endfb-viii.0-hdf5", "cross_sections.xml")
_ch = os.path.join(_ext4, "chain_endfb80_pwr.xml")
if os.path.exists(_xs):
    openmc.config["cross_sections"] = _xs; print("[fer-smoke] XS(ext4):", _xs)
if os.path.exists(_ch):
    CHAIN = _ch; print("[fer-smoke] CHAIN(ext4):", _ch)
# --- Gd/Er overrides from env (reduce absorber) ---
if os.environ.get("FER_GD_WT"):    GD_WT_PCT  = float(os.environ["FER_GD_WT"])
if os.environ.get("FER_N_GD"):     N_GD_RODS  = int(os.environ["FER_N_GD"])
if os.environ.get("FER_ER_WT"):    ER_WT_PCT  = float(os.environ["FER_ER_WT"])
if os.environ.get("FER_N_ER"):     N_ER_RODS  = int(os.environ["FER_N_ER"])
if os.environ.get("FER_RADIAL_GD") is not None:   # "0" -> uniform/regular Gd pattern
    RADIAL_GD_ZONING = os.environ["FER_RADIAL_GD"] not in ("0", "false", "False", "")
if os.environ.get("FER_FLAT_ENRICH"):             # all rings one enrichment
    ENRICH_INNER = ENRICH_MID = ENRICH_OUTER = float(os.environ["FER_FLAT_ENRICH"])
# recompute Gd/Er positions with the new counts
GD_POSITIONS = set(_select_sym_positions(N_GD_RODS, bias="mid"))
ER_POSITIONS = set(_select_sym_positions(N_ER_RODS, bias="outer", exclude=GD_POSITIONS)) if N_ER_RODS else set()
print(f"[fer-smoke] GD_WT={GD_WT_PCT} N_GD={N_GD_RODS} ER_WT={ER_WT_PCT} N_ER={N_ER_RODS}")

# depletion schedule (days) -> ~25 GWd/t so it reaches end-of-cycle
SMOKE_STEPS = [1.0, 9.0, 40.0, 100.0, 150.0, 200.0, 200.0, 200.0,
               250.0, 250.0, 250.0, 250.0]
_STATS = {"fast": STAT_FAST, "medium": STAT_MEDIUM, "final": STAT_FINAL}
_lvl = os.environ.get("FER_STAT", "fast")
_stat = _STATS[_lvl]
_tag = os.environ.get("FER_TAG", "smoke")
print(f"[fer-smoke] STAT={_lvl} {_stat} | {len(SMOKE_STEPS)} steps "
      f"-> ~{sum(SMOKE_STEPS)*SPECIFIC_POWER/1000:.0f} GWd/t | tag={_tag}")
metrics, dep, rundir = run_core_depletion(SMOKE_STEPS, _stat, tag=_tag, verbose=True)
print("[fer-smoke] DONE ->", rundir)
'''
parts.append(DRIVER)

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("".join(parts))
print(f"wrote {OUT} | included {len(INCLUDE)} of {len(code)} code cells")
