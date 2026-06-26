#!/usr/bin/env python3
"""Build the rev_6 'standards' notebook from rev_3, applying review fixes
1, 2, 3, 6.  rev_3 and its outputs are left untouched; rev_6 writes to its own
folder and its own ./aegis40_rev6_outputs.  Findings 4 (critical-rod search)
and 5 (batch-overlay) are deliberately NOT in this patch — they layer on top
and are added after one validating run."""
import json, copy, os

SRC = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_3d_core_notebook.ipynb"
DST_DIR = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/rev6_standards"
DST = os.path.join(DST_DIR, "aegis40_3d_core_notebook_rev6.ipynb")
NEW = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/scripts/_nb_cells/new"

os.makedirs(DST_DIR, exist_ok=True)
nb = json.load(open(SRC, encoding="utf-8"))
cells = nb["cells"]

def lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines(keepends=True)

def src_of(c):
    return "".join(c.get("source", []))

def set_src(c, text_lines):
    c["source"] = text_lines
    if c.get("cell_type") == "code":
        c["outputs"] = []
        c["execution_count"] = None

def find(marker):
    for idx, c in enumerate(cells):
        if c.get("cell_type") == "code" and marker in src_of(c):
            return idx
    raise SystemExit(f"marker not found: {marker}")

changes = []

# 1) config cell: isolate the output directory
i = find('ROOT  = Path("./aegis40_3d_core_outputs")')
s = src_of(cells[i]).replace('Path("./aegis40_3d_core_outputs")',
                             'Path("./aegis40_rev6_outputs")')
set_src(cells[i], s.splitlines(keepends=True)); changes.append(f"config ROOT (cell {i})")

# 2) peaking cell -> per-pin reconstruction (Findings 1, 2-reshape, 3)
i_peak = find("def calc_flux_peaking")
set_src(cells[i_peak], lines(os.path.join(NEW, "new_peaking.py")))
changes.append(f"peaking rewrite (cell {i_peak})")

# 3) insert axial verification cell right after the peaking cell (Finding 2)
verif = {"cell_type": "code", "metadata": {}, "execution_count": None,
         "outputs": [], "source": lines(os.path.join(NEW, "new_verification.py"))}
cells.insert(i_peak + 1, verif); changes.append(f"inserted verification (cell {i_peak+1})")

# 4) absorber inventory cell -> report at cycle EOC (Finding 6)
i_abs = find("def extract_absorber_inventory")
set_src(cells[i_abs], lines(os.path.join(NEW, "new_absorber.py")))
changes.append(f"absorber/Er fix (cell {i_abs})")

# 5) summary cell -> add F_q / F_ΔH as PASS/FAIL gates (Finding 3) + rev id
i_sum = find('"enrichment_max_pct":           (5.0,')
s = src_of(cells[i_sum])
anchor = '    "enrichment_max_pct":           (5.0,    "<=", "wt%",       "hard"),\n'
addition = (anchor +
            '    "radial_peaking_FdeltaH":       (1.65,   "<=", "-",         "hard"),\n'
            '    "pin_peaking_factor_Fq":        (2.32,   "<=", "-",         "hard"),\n')
assert anchor in s, "SAFETY_LIMITS anchor not found"
s = s.replace(anchor, addition)
s = s.replace("aegis40-3d-core-rev_0", "aegis40-3d-core-rev_6")
set_src(cells[i_sum], s.splitlines(keepends=True))
changes.append(f"SAFETY_LIMITS + F_q/F_ΔH gates (cell {i_sum})")

json.dump(nb, open(DST, "w", encoding="utf-8"), indent=1)
print("Wrote:", DST)
for c in changes:
    print("  -", c)

# syntax-check every code cell of the new notebook
import ast
bad = 0
for idx, c in enumerate(json.load(open(DST, encoding="utf-8"))["cells"]):
    if c.get("cell_type") != "code":
        continue
    code = "".join(c["source"])
    code = "\n".join(l for l in code.splitlines() if not l.lstrip().startswith(("%", "!")))
    try:
        ast.parse(code)
    except SyntaxError as e:
        bad += 1; print(f"  SYNTAX ERROR cell {idx}: {e}")
print("syntax check:", "ALL OK" if bad == 0 else f"{bad} cell(s) failed")
