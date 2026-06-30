"""Extract a headless STATIC runner from aegis40_neutronics_FER.ipynb:
include only the setup/def cells + calc_keff_bol + calc_flux_peaking, skip the
shielding build_core override (cell 7) and all heavy analyses/plots. Append a
driver that overrides loading (Gd/Er, enrichment-zoning mode, EDGE grading,
STAT) from env, then runs BOC k_eff + per-pin F_q. ext4 XS via env."""
import json, re, os

NB  = "/home/samira/ref_neutronics.ipynb"
OUT = "/home/samira/aegis_run/ref_static/run_ref_static.py"

nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]

# Only the cells needed for build_core + calc_keff_bol + calc_flux_peaking.
# (cell 7 REDEFINES build_core for shielding -> excluded.)
INCLUDE = {0, 1, 2, 3, 4, 5, 6, 8, 13, 22}
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|write_\w+|build_shielded_model|"
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

parts = ["import matplotlib\nmatplotlib.use('Agg')\nimport os\n"]
for idx, c in enumerate(code):
    if idx not in INCLUDE:
        continue
    parts.append(f"\n# ===== ref cell #{idx} =====\n" + neutralize("".join(c["source"])) + "\n")

DRIVER = r'''
# ===== injected static driver =====
import os
def _truthy(v): return v not in ("0", "false", "False", "", None)
if os.environ.get("FER_GD_WT"):   GD_WT_PCT = float(os.environ["FER_GD_WT"])
if os.environ.get("FER_N_GD"):    N_GD_RODS = int(os.environ["FER_N_GD"])
if os.environ.get("FER_ER_WT"):   ER_WT_PCT = float(os.environ["FER_ER_WT"])
if os.environ.get("FER_N_ER"):    N_ER_RODS = int(os.environ["FER_N_ER"])
if os.environ.get("FER_RADIAL_ENRICH") is not None and os.environ.get("FER_RADIAL_ENRICH") != "":
    RADIAL_ENRICH_ZONING = _truthy(os.environ["FER_RADIAL_ENRICH"])
if os.environ.get("FER_EDGE_GRADE") is not None and os.environ.get("FER_EDGE_GRADE") != "":
    EDGE_PIN_GRADING = _truthy(os.environ["FER_EDGE_GRADE"])
if os.environ.get("FER_EDGE_ENRICH"):
    EDGE_ENRICH = float(os.environ["FER_EDGE_ENRICH"])
if os.environ.get("FER_RING_ENRICH"):   # "centre,...,edge" e.g. 4.95,4.7,4.4,4.0
    _re = [float(x) for x in os.environ["FER_RING_ENRICH"].split(",")]
    RING_ENRICH = {i: _re[i] for i in range(len(_re))}
if os.environ.get("FER_STAT"):
    STAT = {"fast": STAT_FAST, "medium": STAT_MEDIUM, "final": STAT_FINAL}[os.environ["FER_STAT"]]
# recompute BA positions for the (possibly) new counts
GD_POSITIONS = set(_select_sym_positions(N_GD_RODS, bias="mid"))
ER_POSITIONS = set(_select_sym_positions(N_ER_RODS, bias="outer", exclude=GD_POSITIONS))
_tag = os.environ.get("FER_TAG", "static")
print("="*64)
print(f"[static:{_tag}] gd={N_GD_RODS}@{GD_WT_PCT}wt  er={N_ER_RODS}@{ER_WT_PCT}wt  "
      f"RADIAL_ENRICH_ZONING={RADIAL_ENRICH_ZONING}  EDGE_PIN_GRADING={EDGE_PIN_GRADING}")
print(f"[static:{_tag}] RING_ENRICH={RING_ENRICH}  STAT={STAT}")
print("="*64, flush=True)
calc_keff_bol()
calc_flux_peaking()
print(f"[static:{_tag}] RESULT keff={results.get('k_eff_bol')}  "
      f"Fq={results.get('pin_peaking_factor_Fq')}  FdH={results.get('radial_peaking_FdeltaH')}  "
      f"Fz={results.get('axial_peaking_Fz')}  F_FA={results.get('assembly_peaking_F_radial')}")
import json as _json
open(os.path.join(os.environ.get("FER_OUTJSON_DIR","."), f"static_{_tag}.json"),"w").write(_json.dumps(results, default=str, indent=2))
print(f"[static:{_tag}] DONE")
'''
parts.append(DRIVER)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("".join(parts))
print(f"wrote {OUT} | included {sorted(INCLUDE)} of {len(code)} code cells")
