"""Stop library results overwriting each other: run every depletion case in its own
timestamped per-library folder (chdir-isolated) + autosave the comparison table & plot."""
import json, shutil, datetime
NB = "/mnt/d/Engineering/SMR research/depletions/src/openmc_depletion_xcheck.ipynb"
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(NB, NB + f".bak_autosave_{stamp}")
nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))

RESULTS_BLOCK = (
    "\n\n# --- results folder: each library/case gets its own subdir (no overwrite) ---\n"
    "from pathlib import Path\n"
    "import datetime as _dt\n"
    "RESULTS_ROOT = Path('results') / f\"{STREAM}_{FEED}_{_dt.datetime.now():%Y%m%d_%H%M%S}\"\n"
    "RESULTS_ROOT.mkdir(parents=True, exist_ok=True)\n"
    "print('Results saved under:', RESULTS_ROOT.resolve())\n")

RC_OLD = """    clean_stale()
    increments = [BURNUP_GRID[0]] + list(np.diff(BURNUP_GRID))
    op = make_operator(model, chain, mode or REACTION_RATE_MODE)
    openmc.deplete.PredictorIntegrator(
        op, increments, power_density=SPECIFIC_POWER, timestep_units="MWd/kg").integrate()

    results = openmc.deplete.Results("depletion_results.h5")
    try:
        _, keff = results.get_keff()
    except Exception:
        keff = [(None, None)] * (len(BURNUP_GRID) + 1)
    atoms = {k: results.get_atoms(fuel_id, k)[1] for k in PU}"""
RC_NEW = """    if tag is None:                                          # unique folder per library/case
        import re as _re
        _m = _re.search(r"[\\\\/]([^\\\\/]+)[\\\\/]cross_sections", xs)
        tag = f"{(_m.group(1) if _m else 'lib')}_f{int(fuel_T)}_c{int(cool_T)}"
    rundir = RESULTS_ROOT / tag
    rundir.mkdir(parents=True, exist_ok=True)
    _cwd0 = os.getcwd(); os.chdir(rundir)                    # isolate -> nothing overwrites
    try:
        increments = [BURNUP_GRID[0]] + list(np.diff(BURNUP_GRID))
        op = make_operator(model, chain, mode or REACTION_RATE_MODE)
        openmc.deplete.PredictorIntegrator(
            op, increments, power_density=SPECIFIC_POWER, timestep_units="MWd/kg").integrate()
        results = openmc.deplete.Results("depletion_results.h5")
        try:
            _, keff = results.get_keff()
        except Exception:
            keff = [(None, None)] * (len(BURNUP_GRID) + 1)
        atoms = {k: results.get_atoms(fuel_id, k)[1] for k in PU}
    finally:
        os.chdir(_cwd0)                                      # always restore cwd
    print(f"   saved -> {rundir}")"""

CSV_ADD = (
    "\n\n    if records:                                         # autosave the comparison table\n"
    "        import pandas as _pd\n"
    "        _csv = RESULTS_ROOT / f\"comparison_{STREAM}_{FEED}.csv\"\n"
    "        _pd.DataFrame(records).to_csv(_csv, index=False)\n"
    "        print('Saved table ->', _csv)\n")

hits = dict(results=0, runcase_sig=0, runcase_body=0, libcall=0, csv=0, plot=0)
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    if "OMP_NUM_THREADS" in s and "RESULTS_ROOT" not in s:
        s += RESULTS_BLOCK; hits["results"] += 1
    if "def run_case(xs, chain, fuel_T, cool_T, mode=None):" in s:
        s = s.replace("def run_case(xs, chain, fuel_T, cool_T, mode=None):",
                      "def run_case(xs, chain, fuel_T, cool_T, mode=None, tag=None):")
        hits["runcase_sig"] += 1
    if RC_OLD in s:
        s = s.replace(RC_OLD, RC_NEW); hits["runcase_body"] += 1
    if "omc, kinf = run_case(xs, chain, REF_FUEL_T, REF_COOLANT_T)" in s:
        s = s.replace("omc, kinf = run_case(xs, chain, REF_FUEL_T, REF_COOLANT_T)",
                      "omc, kinf = run_case(xs, chain, REF_FUEL_T, REF_COOLANT_T, tag=name)")
        hits["libcall"] += 1
        if "RESULTS_ROOT / f\"comparison" not in s:
            s += CSV_ADD; hits["csv"] += 1
    if 'out = f"library_comparison_{STREAM}_{FEED}.png"' in s:
        s = s.replace('out = f"library_comparison_{STREAM}_{FEED}.png"',
                      'out = RESULTS_ROOT / f"library_comparison_{STREAM}_{FEED}.png"')
        hits["plot"] += 1
    c["source"] = s.splitlines(keepends=True)

missing = [k for k, v in hits.items() if v == 0]
if missing:
    raise SystemExit(f"anchors not found: {missing} (hits={hits}) — aborted, no change")
open(NB, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
print(f"patched autosave: {hits}  (backup .bak_autosave_{stamp})")
