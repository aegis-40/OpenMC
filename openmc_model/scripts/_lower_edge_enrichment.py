#!/usr/bin/env python
"""Lower U-235 enrichment on the OUTER RING of pins (FA perimeter) to clip the
per-pin F_ΔH hot pins.

The outermost pin ring (i or j in {0, 16}) faces the inter-assembly water gaps,
where the thermal flux — and thus per-pin power — peaks. That ring is the main
driver of F_ΔH (1.79). It is currently lumped into the 4.40% radial 'outer zone'.
This gives the perimeter ring its OWN lower enrichment (EDGE_ENRICH, default 4.0%),
leaving the rest of the assembly untouched. All 64 perimeter positions are fuel
(no guide tubes are on rows/cols 0,1,15,16), so this targets exactly the hot ring.

Edits (each asserted once, each cell recompiled):
  cell 3  : add EDGE_PIN_GRADING / EDGE_ENRICH config
  cell 5  : _enrichment_for_pin returns EDGE_ENRICH on the perimeter ring
  cell 10 : build_core builds the extra UO2 enrichment material

Toggle: EDGE_PIN_GRADING=False reverts to the 3-zone radial scheme.
"""
import ast, json

NB = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

def patch(idx, old, new, check=None):
    c = nb['cells'][idx]
    s = ''.join(c['source'])
    if check:
        assert check in s, f"cell {idx}: sanity '{check}' missing"
    assert s.count(old) == 1, f"cell {idx}: old hits {s.count(old)} (need 1)"
    s = s.replace(old, new)
    ast.parse(s)
    c['source'] = s.splitlines(keepends=True)

# ── cell 3: config ──────────────────────────────────────────────────────────
patch(3,
    'ZONE_R2_CM    = 8.5        # mid/outer boundary',
    'ZONE_R2_CM    = 8.5        # mid/outer boundary\n'
    '\n'
    '# ── Outer-ring (FA-perimeter) enrichment grading (2026-06-20) ────────────────\n'
    '# The outermost pin ring (i or j in {0,16}) faces the inter-assembly water gaps,\n'
    '# where the thermal flux — and hence per-pin power — peaks. That ring is the main\n'
    '# driver of per-pin F_ΔH, so give it its own LOWER enrichment (rest of FA kept).\n'
    '# Set EDGE_PIN_GRADING=False to revert to the plain 3-zone radial scheme.\n'
    'EDGE_PIN_GRADING = True\n'
    'EDGE_ENRICH      = 4.0     # wt% U-235 on the outermost pin ring (perimeter)',
    check='ZONE_R2_CM    = 8.5')

# ── cell 5: _enrichment_for_pin ─────────────────────────────────────────────
patch(5,
    '''def _enrichment_for_pin(i, j):
    r = _pin_radius(i, j)
    if r < ZONE_R1_CM:   return ENRICH_INNER
    if r < ZONE_R2_CM:   return ENRICH_MID
    return ENRICH_OUTER''',
    '''def _enrichment_for_pin(i, j):
    # Outermost pin ring (FA perimeter) faces the inter-assembly water gaps, where
    # thermal flux — and hence per-pin power — peaks: the main driver of F_ΔH.
    # Give that ring its own, lower enrichment when EDGE_PIN_GRADING is on.
    if EDGE_PIN_GRADING and (i in (0, N_PIN - 1) or j in (0, N_PIN - 1)):
        return EDGE_ENRICH
    r = _pin_radius(i, j)
    if r < ZONE_R1_CM:   return ENRICH_INNER
    if r < ZONE_R2_CM:   return ENRICH_MID
    return ENRICH_OUTER''',
    check='def _enrichment_for_pin(')

# ── cell 10: build_core material set ────────────────────────────────────────
patch(10,
    '''    plain_mats = {}
    for e in (ENRICH_INNER, ENRICH_MID, ENRICH_OUTER):
        plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")''',
    '''    _enr_levels = {ENRICH_INNER, ENRICH_MID, ENRICH_OUTER}
    if EDGE_PIN_GRADING: _enr_levels.add(EDGE_ENRICH)
    plain_mats = {}
    for e in sorted(_enr_levels):
        plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")''',
    check='def build_core(')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))   # roundtrip
print("OK: outer pin ring -> EDGE_ENRICH (4.0 wt%); rest of FA unchanged.")
print("    Toggle in cell 3: EDGE_PIN_GRADING (False reverts) / EDGE_ENRICH.")
print("    Re-run: restart kernel -> run all (or cells 3,5,...,10 then the F_q cell).")
