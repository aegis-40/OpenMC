#!/usr/bin/env python
"""Task-1 patch: edge-pin enrichment grading to fix the F_ΔH / F_q hot-pin failure.

De-rates the outer pin rows of the edge (ring-2) assemblies that face the 20 cm
water reflector — the real driver of F_ΔH 1.845 / F_q 3.583.  Toggle
EDGE_PIN_GRADING=False reproduces exact rev6.

Verified patch: every replacement must hit exactly once; every edited code cell
must still compile; the notebook must still parse as JSON/nbformat.
Operates on the parsed notebook (sets cell['source'] to a single string) so we
never wrestle raw JSON escaping.
"""
import ast
import json
import sys

NB = r'D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev6.ipynb'

nb = json.load(open(NB, encoding='utf-8'))


def patch(idx, old, new, n=1):
    c = nb['cells'][idx]
    src = ''.join(c['source'])
    got = src.count(old)
    assert got == n, f"cell {idx}: expected {n} hit(s), got {got} for:\n{old[:80]!r}"
    c['source'] = src.replace(old, new)


# ── R1: config — add edge-grading knobs (cell 3) ────────────────────────────
patch(3,
"""ZONE_R1_CM    = 4.5        # inner/mid boundary (cm from FA centre)
ZONE_R2_CM    = 8.5        # mid/outer boundary""",
"""ZONE_R1_CM    = 4.5        # inner/mid boundary (cm from FA centre)
ZONE_R2_CM    = 8.5        # mid/outer boundary

# ── Edge-pin grading: de-peak the outer pin rows of the edge (ring-2) FAs that
# face the 20 cm water reflector.  This fixes the *real* F_ΔH / F_q hot-pin
# failure (over-moderated edge pins).  Toggle False = exact rev6.
# TUNING: if F_ΔH still > 1.65 after a run -> lower EDGE_PIN_ENRICH or raise
# EDGE_PIN_DEPTH; if discharge burnup drops too far -> do the opposite.
EDGE_PIN_GRADING = True
EDGE_GRADE_RING  = 2       # core ring that gets grading (2 = outer 12 FAs)
EDGE_PIN_DEPTH   = 2       # number of outermost pin rows de-rated
EDGE_PIN_ENRICH  = 3.8     # wt% U-235 for those pins (down from ENRICH_OUTER 4.40)""")

# config print summary
patch(3,
'''print(f"Radial Gd zoning : {('ON ' + str(GD_RING_WEIGHTS)) if RADIAL_GD_ZONING else 'OFF (uniform)'}")''',
'''print(f"Radial Gd zoning : {('ON ' + str(GD_RING_WEIGHTS)) if RADIAL_GD_ZONING else 'OFF (uniform)'}")
print(f"Edge-pin grading : {'ON' if EDGE_PIN_GRADING else 'OFF'}"
      + (f"  (ring {EDGE_GRADE_RING}, outer {EDGE_PIN_DEPTH} row(s) -> {EDGE_PIN_ENRICH} wt%)" if EDGE_PIN_GRADING else ""))''')

# ── R2: pin-enrichment helper with edge grading (cell 5) ────────────────────
patch(5,
"""def _enrichment_for_pin(i, j):
    r = _pin_radius(i, j)
    if r < ZONE_R1_CM:   return ENRICH_INNER
    if r < ZONE_R2_CM:   return ENRICH_MID
    return ENRICH_OUTER""",
"""def _enrichment_for_pin(i, j):
    r = _pin_radius(i, j)
    if r < ZONE_R1_CM:   return ENRICH_INNER
    if r < ZONE_R2_CM:   return ENRICH_MID
    return ENRICH_OUTER


def _is_edge_graded(i, j, core_ring):
    \"\"\"True if pin (i,j) is in the de-rated outer rows of an edge (ring-2) FA.\"\"\"
    if not EDGE_PIN_GRADING or core_ring != EDGE_GRADE_RING:
        return False
    depth = min(i, j, N_PIN - 1 - i, N_PIN - 1 - j)   # 0 = outermost pin ring
    return depth < EDGE_PIN_DEPTH


def _pin_enrich(i, j, core_ring=None):
    \"\"\"Pin enrichment, applying edge-pin grading for edge assemblies.\"\"\"
    if _is_edge_graded(i, j, core_ring):
        return min(EDGE_PIN_ENRICH, _enrichment_for_pin(i, j))
    return _enrichment_for_pin(i, j)""")

# ── R3: _build_fa_universe signature — accept core_ring (cell 9) ────────────
patch(9,
"""                       insert_cr, name="FA",
                       gd_positions=None, er_positions=None):""",
"""                       insert_cr, name="FA",
                       gd_positions=None, er_positions=None, core_ring=None):""")

# ── R4: prebuild pin-universe loop uses graded enrichment (cell 9) ──────────
patch(9,
"""    for (i, j) in FUEL_POS:
        e = _enrichment_for_pin(i, j)
        ukey = f"plain_{e:.1f}\"""",
"""    for (i, j) in FUEL_POS:
        e = _pin_enrich(i, j, core_ring)
        ukey = f"plain_{e:.1f}\"""")

# ── R5: grid placement uses graded enrichment (cell 9) ─────────────────────
patch(9,
"""            else:
                e = _enrichment_for_pin(i, j)
                row.append(pin_universes[f"plain_{e:.1f}"])""",
"""            else:
                e = _pin_enrich(i, j, core_ring)
                row.append(pin_universes[f"plain_{e:.1f}"])""")

# ── R6: build_core registers the edge-enrichment material (cell 10) ────────
patch(10,
"""    plain_mats = {}
    for e in (ENRICH_INNER, ENRICH_MID, ENRICH_OUTER):
        plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")""",
"""    plain_enrichs = [ENRICH_INNER, ENRICH_MID, ENRICH_OUTER]
    if EDGE_PIN_GRADING:
        plain_enrichs.append(EDGE_PIN_ENRICH)
    plain_mats = {}
    for e in plain_enrichs:
        plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")""")

# ── R7: pass core_ring on the ARO universe build (cell 10) ─────────────────
patch(10,
"""            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er)""",
"""            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er, core_ring=ring)""")

# ── R8: pass core_ring on the ARI universe build (cell 10) ─────────────────
patch(10,
"""            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er)""",
"""            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er, core_ring=ring)""")

# ── R9: depletion volume bookkeeping keyed by ACTUAL pin material (cell 25) ─
patch(25,
"""        for nm, c in ((f"UO2_{ENRICH_INNER:.1f}", n_inner),
                      (f"UO2_{ENRICH_MID:.1f}",   n_mid),
                      (f"UO2_{ENRICH_OUTER:.1f}", n_outer)):
            counts_name[nm] = counts_name.get(nm, 0) + c * nfa""",
"""        # key plain fuel by the pin's ACTUAL material (handles edge grading);
        # n_inner/n_mid/n_outer are kept above only as radial diagnostics.
        for p in plain:
            nm = f"UO2_{_pin_enrich(p[0], p[1], ring):.1f}"
            counts_name[nm] = counts_name.get(nm, 0) + nfa""")

# ── validate: every edited code cell still compiles ─────────────────────────
for idx in (3, 5, 9, 10, 25):
    src = ''.join(nb['cells'][idx]['source'])
    ast.parse(src)   # raises SyntaxError if broken

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))   # re-parse to confirm valid JSON
print("OK: 9 replacements applied, cells 3/5/9/10/25 compile, notebook re-parses.")
