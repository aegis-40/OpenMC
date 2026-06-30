"""Laziz decision: Er 0.5 -> 0.75 wt%. Patch the locked FER notebook config
(both the D: working copy and the ~/ref_neutronics.ipynb the safety generator reads)."""
import json, shutil, datetime

NB  = "/mnt/d/conda-envs/openmc-py311/SMRs/Shielding/aegis40_neutronics_FER.ipynb"
REF = "/home/samira/ref_neutronics.ipynb"
OLD, NEW = "ER_WT_PCT = 0.5", "ER_WT_PCT = 0.75"

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(NB, NB + f".bak_er_{stamp}")
nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
hits = 0
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    if OLD in s and "DESIGN" in s:               # the hybrid-branch config cell
        c["source"] = s.replace(OLD, NEW).splitlines(keepends=True)
        hits += 1
if hits == 0:
    raise SystemExit("ER_WT_PCT = 0.5 not found in config cell — aborted")
out = json.dumps(nb, ensure_ascii=False, indent=1)
open(NB, "w", encoding="utf-8").write(out)
open(REF, "w", encoding="utf-8").write(out)
print(f"patched ER_WT_PCT 0.5 -> 0.75 in {hits} cell(s); wrote NB + REF (backup .bak_er_{stamp})")
