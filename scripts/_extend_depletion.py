"""Extend the depletion horizon for the 37-FA core (cell 31 calc_depletion).
The 1945 EFPD schedule was inherited from the 21-FA core; at the 37-FA core's
12.7 MW/tHM specific power it reaches only 24.6 GWd/tHM, where k is still 1.009
(never crosses 1). New schedule reaches ~46 GWd/tHM so the k=1 crossing is captured."""
import json
from pathlib import Path

NB = Path(r"D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_neutronics_FER.ipynb")
nb = json.loads(NB.read_text(encoding="utf-8"))

def cell_text(idx):
    return "".join(nb["cells"][idx]["source"])

def sub(idx, old, new, count=1):
    txt = cell_text(idx)
    n = txt.count(old)
    if n != count:
        raise SystemExit(f"CELL {idx}: expected {count} of <<{old[:50]}...>>, found {n}")
    nb["cells"][idx]["source"] = txt.replace(old, new).splitlines(keepends=True)

# code part: 9x125d coarse tail -> 19x150d so the horizon reaches ~46 GWd/tHM
sub(31, "[45] * 16 + [125] * 9", "[45] * 16 + [150] * 19")
# comment: explain the horizon must scale with the (halved) 37-FA specific power
sub(31, "# ~1945 EFPD; fine (~1 GWd/t) steps through Gd burnout, then coarse",
        "# ~3670 EFPD (~46 GWd/tHM): fine (~0.5 GWd/t) through Gd burnout, then coarse. "
        "37-FA specific power 12.7 MW/tHM (half the old 21-FA) -> horizon must reach "
        "~46 GWd/t for fresh-core k to cross 1 (a 1945-EFPD run stopped at 24.6 GWd/t, k_EOC=1.009).")

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("Depletion horizon extended:", NB)
