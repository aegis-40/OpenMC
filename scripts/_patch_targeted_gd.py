#!/usr/bin/env python
"""TARGETED Gd placement for the rev7 zoning notebook.

rev7 (assembly-uniform + steel reflector) gave per-pin F_dH = 1.935, with every
hot pin GUIDE-TUBE-ADJACENT or on the ASSEMBLY EDGE — classic water-hole
thermalisation spikes.  rev7 (like rev6) scatters Gd at mid-radius (bias="mid"),
so the absorber isn't where the peaks are.  SMART/ATOM/PRATIC place Gd rods AT
those local hot spots to flatten pin power.

This patch adds a "hotspot" placement bias: each fuel pin is scored by how
strongly it locally peaks (orthogonally/diagonally next to a guide tube +
proximity to the assembly edge), and the Gd rods are filled into the highest-
scoring 8-fold-symmetric positions first.  Same Gd rod COUNT (N_GD_RODS) -> BOC
hold-down ~unchanged; only WHERE they sit changes.

No design-basis / geometry / CAD impact.  To revert: re-run _make_zoning_study.py.
Verified patch: each replacement hits once; cell 5 compiles; JSON re-parses.
"""
import ast, json

DST = r'D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev7_zoning.ipynb'
nb = json.load(open(DST, encoding='utf-8'))

def patch(idx, old, new, n=1):
    c = nb['cells'][idx]
    src = ''.join(c['source'])
    got = src.count(old)
    assert got == n, f"cell {idx}: expected {n}, got {got}: {old[:70]!r}"
    c['source'] = src.replace(old, new)

# (a) insert hot-spot scoring helpers just before _select_sym_positions
HELPERS = (
"# ── Local hot-spot scoring for TARGETED Gd placement ──────────────────────\n"
"# rev7 per-pin F_dH peaked at guide-tube-adjacent and assembly-edge pins\n"
"# (water-hole thermalisation).  SMART/ATOM/PRATIC place Gd rods AT those local\n"
"# hot spots to flatten pin power, not at mid-radius.  These score each fuel pin\n"
"# by how strongly it tends to locally peak so _select_sym_positions(bias=\n"
"# 'hotspot') fills Gd there first.\n"
"_GT_SET = set(GUIDE_ALL)\n"
"def _adjacent_to_guide(i, j):\n"
"    orth = any((i+di, j+dj) in _GT_SET for di, dj in ((1,0),(-1,0),(0,1),(0,-1)))\n"
"    diag = any((i+di, j+dj) in _GT_SET for di, dj in ((1,1),(1,-1),(-1,1),(-1,-1)))\n"
"    return orth, diag\n"
"def _local_peak_score(i, j):\n"
"    orth, diag = _adjacent_to_guide(i, j)\n"
"    s = 1.5 if orth else (0.75 if diag else 0.0)  # next to a guide-tube water hole\n"
"    depth = min(i, j, N_PIN - 1 - i, N_PIN - 1 - j)            # 0 = outermost pin ring\n"
"    s += 1.5 if depth == 0 else (0.75 if depth == 1 else 0.0)  # inter-assembly edge gap\n"
"    return s\n"
"\n\n")
patch(5, 'def _select_sym_positions(n, bias="mid", exclude=None):',
         HELPERS + 'def _select_sym_positions(n, bias="mid", exclude=None):')

# (b) add the "hotspot" scoring branch
patch(5,
'''        if   bias == "inner": score =  r_mean
        elif bias == "outer": score = -r_mean
        else:                 score = abs(r_mean - 5.2 * PIN_PITCH)''',
'''        if   bias == "inner":   score =  r_mean
        elif bias == "outer":   score = -r_mean
        elif bias == "hotspot": score = -sum(_local_peak_score(*p) for p in g) / len(g)
        else:                   score = abs(r_mean - 5.2 * PIN_PITCH)''')

# (c) steer the (uniform) Gd rods to the hot spots
patch(5, 'GD_POSITIONS = set(_select_sym_positions(N_GD_RODS, bias="mid"))',
         'GD_POSITIONS = set(_select_sym_positions(N_GD_RODS, bias="hotspot"))')

# (d) keep per-ring Gd targeting consistent if RADIAL_GD_ZONING is re-enabled
patch(5, 'return set(_select_sym_positions(_gd_count_for_ring(ring), bias="mid"))',
         'return set(_select_sym_positions(_gd_count_for_ring(ring), bias="hotspot"))')

# (e) placement diagnostic
patch(5,
'print(f"Gd rods/FA (avg): {len(GD_POSITIONS)}  |  Er rods/FA: {len(ER_POSITIONS)}")',
'_gd_gt = sum(1 for p in GD_POSITIONS if any(_adjacent_to_guide(*p)))\n'
'_gd_edge = sum(1 for p in GD_POSITIONS if min(p[0], p[1], N_PIN-1-p[0], N_PIN-1-p[1]) <= 1)\n'
'print(f"Gd rods/FA (avg): {len(GD_POSITIONS)} ({_gd_gt} GT-adjacent, {_gd_edge} edge)  |  Er rods/FA: {len(ER_POSITIONS)}")')

ast.parse(''.join(nb['cells'][5]['source']))
json.dump(nb, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(DST, encoding='utf-8'))
print("OK: targeted-Gd (bias='hotspot') applied to rev7_zoning; cell 5 compiles, JSON re-parses.")
