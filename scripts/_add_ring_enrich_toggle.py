#!/usr/bin/env python
"""Add an assembly-level RADIAL enrichment-zoning toggle to the 37-FA notebook so
we can run the intra-FA-grading design against the peer-SMR "onion" ring zoning
HEAD-TO-HEAD in the 37-FA core — the justification for our choice.

When RADIAL_ENRICH_ZONING=True, each FA gets ONE uniform enrichment by its core
ring (out-in: low centre, high edge — like ATOM/SMART/PRATIC), REPLACING the
intra-FA 3-zone grade. Core-average enrichment is conserved (~4.68) so it's a
fair redistribution, max ≤5.0. Default OFF = exact current design.

Edits (each asserted once, each cell recompiled):
  cell 3  : RADIAL_ENRICH_ZONING + RING_ENRICH config
  cell 9  : _build_fa_universe gains fa_enrich (uniform-per-FA override)
  cell 10 : plain_mats includes ring enrichments; pass fa_enrich per ring (aro+ari)
"""
import ast, json

NB = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_7x7_37FA.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

def patch(idx, old, new, check=None):
    c = nb['cells'][idx]; s = ''.join(c['source'])
    if check: assert check in s, f"cell {idx}: '{check}' missing"
    assert s.count(old) == 1, f"cell {idx}: old hits {s.count(old)}"
    s = s.replace(old, new); ast.parse(s)
    c['source'] = s.splitlines(keepends=True)

# ── cell 3: config ──────────────────────────────────────────────────────────
patch(3,
    'EDGE_ENRICH      = 4.0     # wt% U-235 on the outermost pin ring (perimeter)',
    'EDGE_ENRICH      = 4.0     # wt% U-235 on the outermost pin ring (perimeter)\n'
    '\n'
    '# ── Assembly-level RADIAL enrichment zoning ("onion" rings — ATOM/SMART/PRATIC) ─\n'
    '# When ON, each FA gets ONE uniform enrichment by its core ring (out-in: low\n'
    '# centre / high edge) to flatten the assembly-average power — the standard peer-\n'
    '# SMR approach — REPLACING the intra-FA 3-zone grade. Core-avg conserved (~4.68),\n'
    '# max ≤5.0. Run OFF then ON in the 37-FA core to justify the choice on the binding\n'
    '# per-pin F_ΔH/F_q (not just the cosmetic assembly map). OFF = exact current design.\n'
    'RADIAL_ENRICH_ZONING = True\n'
    'RING_ENRICH = {0: 4.0, 1: 4.4, 2: 4.7, 3: 4.95}   # out-in, FA-avg ~4.70 over 1/8/16/12 FAs',
    check='EDGE_ENRICH')

# ── cell 9: fa_enrich override ──────────────────────────────────────────────
patch(9,
    '''                       gd_positions=None, er_positions=None, blanket_mat=None,
                       waba_mat=None):''',
    '''                       gd_positions=None, er_positions=None, blanket_mat=None,
                       waba_mat=None, fa_enrich=None):''')

patch(9,
    '''    pin_universes = {}
    for (i, j) in FUEL_POS:
        e = _enrichment_for_pin(i, j)
        ukey = f"plain_{e:.1f}"''',
    '''    pin_universes = {}
    for (i, j) in FUEL_POS:
        e = fa_enrich if fa_enrich is not None else _enrichment_for_pin(i, j)
        ukey = f"plain_{e:.1f}"''')

patch(9,
    '''            else:
                e = _enrichment_for_pin(i, j)
                row.append(pin_universes[f"plain_{e:.1f}"])''',
    '''            else:
                e = fa_enrich if fa_enrich is not None else _enrichment_for_pin(i, j)
                row.append(pin_universes[f"plain_{e:.1f}"])''')

# ── cell 10: materials + per-ring fa_enrich ─────────────────────────────────
patch(10,
    '''    if EDGE_PIN_GRADING: _enr_levels.add(EDGE_ENRICH)
    plain_mats = {}''',
    '''    if EDGE_PIN_GRADING: _enr_levels.add(EDGE_ENRICH)
    if RADIAL_ENRICH_ZONING: _enr_levels.update(RING_ENRICH.values())
    plain_mats = {}''',
    check='def build_core(')

patch(10,
    '''            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            waba_mat=(waba_mat if ring in WABA_RINGS else None))''',
    '''            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            waba_mat=(waba_mat if ring in WABA_RINGS else None),
            fa_enrich=(RING_ENRICH[ring] if RADIAL_ENRICH_ZONING else None))''')

patch(10,
    '''            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat)''',
    '''            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            fa_enrich=(RING_ENRICH[ring] if RADIAL_ENRICH_ZONING else None))''')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: ring enrichment-zoning toggle added to 37-FA notebook (default OFF).")
print("    Baseline run (OFF) = intra-FA grade. Flip RADIAL_ENRICH_ZONING=True for the")
print("    onion-ring comparison; compare F_radial / F_dH / F_q / k_BOL head-to-head.")
