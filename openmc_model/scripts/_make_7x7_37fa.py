#!/usr/bin/env python
"""Create the 7-wide / 37-FA core variant from the current 21-FA notebook.

Root cause of the stuck F_ΔH was the small (5-wide) core: steep flux tilt piling
power into the centre FA + 25 water holes per FA. A 7-wide (37-FA) octagon spreads
the power over more assemblies (lower F_radial) and flattens the intra-assembly
tilt, so the water-hole peak rides on a flatter base. Power held at 125 MWth, so
power density drops (HM 5.6 -> 9.87 t, specific power ~12.7 MW/t).

Copies the notebook, then changes ONLY the core-size parameters:
  N_CORE 5->7 ; CORE_MAP 3-5-7-7-7-5-3 (37) ; CR_MAP (12 CRAs, centre free) ;
  _core_ring_of cap 2->3 ; GD_RING_WEIGHTS gains ring 3 ; build_core ring loops
  ->(0,1,2,3) ; HM_MASS_T -> 9.87.
Everything else (materials, geometry builders, peaking, diagnostic) is unchanged.
NOTE: SHIELD_IN_CORE stays False; the shield radii (cell 11) would need re-anchoring
before enabling the shield for the bigger core — irrelevant for the peaking run.
"""
import ast, json, shutil

SRC = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_shielding_rev7.ipynb'
DST = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_7x7_37FA.ipynb'
shutil.copyfile(SRC, DST)
nb = json.load(open(DST, encoding='utf-8'))

def patch(idx, old, new, check=None):
    c = nb['cells'][idx]; s = ''.join(c['source'])
    if check: assert check in s, f"cell {idx}: '{check}' missing"
    assert s.count(old) == 1, f"cell {idx}: old hits {s.count(old)}"
    s = s.replace(old, new); ast.parse(s)
    c['source'] = s.splitlines(keepends=True)

# N_CORE
patch(3, 'N_CORE        = 5', 'N_CORE        = 7')

# CORE_MAP -> 37-FA octagon (3-5-7-7-7-5-3)
patch(3,
'''CORE_MAP = np.array([
    [0, 1, 1, 1, 0],   # j=4 (top)
    [1, 1, 1, 1, 1],   # j=3
    [1, 1, 1, 1, 1],   # j=2 (middle)
    [1, 1, 1, 1, 1],   # j=1
    [0, 1, 1, 1, 0],   # j=0 (bottom)
])''',
'''CORE_MAP = np.array([
    [0, 0, 1, 1, 1, 0, 0],   # j=6 (top)     3
    [0, 1, 1, 1, 1, 1, 0],   # j=5           5
    [1, 1, 1, 1, 1, 1, 1],   # j=4           7
    [1, 1, 1, 1, 1, 1, 1],   # j=3 (middle)  7
    [1, 1, 1, 1, 1, 1, 1],   # j=2           7
    [0, 1, 1, 1, 1, 1, 0],   # j=1           5
    [0, 0, 1, 1, 1, 0, 0],   # j=0 (bottom)  3
])''')

# CR_MAP -> 12 CRAs (checkerboard, centre instrument = rod-free)
patch(3,
'''CR_MAP = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
])''',
'''CR_MAP = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])''')

# Gd ring weights: add ring 3 (rings now 1/8/16/12 FAs; avg ~1.0)
patch(3,
    'GD_RING_WEIGHTS  = {0: 1.50, 1: 1.24, 2: 0.80}',
    'GD_RING_WEIGHTS  = {0: 1.50, 1: 1.30, 2: 1.00, 3: 0.75}   # 37 FA: rings 1/8/16/12, avg~1.0')

# HM mass scales with FA count (same FA design): 5.6 * 37/21
patch(3,
    'HM_MASS_T      = 5.6',
    'HM_MASS_T      = 9.87      # 37 FA × (5.6/21) — power held at 125 MWth, density drops')

# _core_ring_of: cap 2 -> 3
patch(5,
'''def _core_ring_of(i, j):
    """Radial ring of a 5×5 core position: 0 = centre FA, 1 = inner 8, 2 = outer."""
    cc = (N_CORE - 1) // 2                          # centre index = 2
    return min(max(abs(i - cc), abs(j - cc)), 2)    # Chebyshev distance, capped''',
'''def _core_ring_of(i, j):
    """Radial ring of a core position: 0=centre, 1=inner8, 2=mid16, 3=outer12."""
    cc = (N_CORE - 1) // 2                          # centre index = 3 for 7-wide
    return min(max(abs(i - cc), abs(j - cc)), 3)    # Chebyshev distance, capped at 3''')

# build_core: extend ring loops to all 4 rings (aro all; ari for any CR ring)
patch(10, 'for ring in (0, 1, 2):', 'for ring in (0, 1, 2, 3):')
patch(10,
'''    for ring in (0, 1):
        gd, er = _ring_ba(ring)
        fa_ari_by_ring[ring] = _build_fa_universe(''',
'''    for ring in (0, 1, 2, 3):
        gd, er = _ring_ba(ring)
        fa_ari_by_ring[ring] = _build_fa_universe(''')

json.dump(nb, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(DST, encoding='utf-8'))
print("OK: 37-FA 7x7 notebook created:")
print("   ", DST)
print("    N_CORE=7, 37-FA octagon, 12 CRAs, rings 0-3, HM 9.87 t, 125 MWth.")
print("    Restart kernel -> run all. Watch [1/9] k_BOL and [9/9] F_ΔH / hot-pin list.")
