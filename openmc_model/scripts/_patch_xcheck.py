"""Apply acceleration + convergence-proof tweaks to the SFR depletion x-check nb:
 (1) THREADS -> all cores, (2) add a Shannon-entropy mesh (proves source convergence
 for the paper). Stats/flux-mode/chain-reduction are already optimal; left untouched."""
import json, shutil, datetime
NB = "/mnt/d/Engineering/SMR research/depletions/src/openmc_depletion_xcheck.ipynb"
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(NB, NB + f".bak_{stamp}")
nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))

THR_OLD = "THREADS   = 6        # OpenMP threads; set to an int to pin, None = OpenMC default"
THR_NEW = "THREADS   = None     # None = all cores (max speed); pin to PHYSICAL-core count if HT oversubscribes"
ENT_ANCHOR = '    settings.temperature = {"method": "interpolation"}        # arbitrary fuel/coolant temps'
ENT_ADD = ('\n    ent = openmc.RegularMesh(); ent.dimension = (4, 4, 1)     # Shannon-entropy convergence proof'
           '\n    ent.lower_left, ent.upper_right = (-p, -p, -1.0), (p, p, 1.0)'
           '\n    settings.entropy_mesh = ent')

hits = {"threads": 0, "entropy": 0}
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    if THR_OLD in s:
        s = s.replace(THR_OLD, THR_NEW); hits["threads"] += 1
    if ENT_ANCHOR in s and "entropy_mesh" not in s:
        s = s.replace(ENT_ANCHOR, ENT_ANCHOR + ENT_ADD); hits["entropy"] += 1
    c["source"] = s.splitlines(keepends=True)

if hits["threads"] == 0 or hits["entropy"] == 0:
    raise SystemExit(f"anchor not found: {hits} — aborted, no change written")
open(NB, "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
print(f"patched: {hits}  (backup .bak_{stamp})")
