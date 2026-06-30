#!/usr/bin/env python
"""(1) Revert the radial reflector to water (steel made F_ΔH worse in this small
center-peaked core — water has the higher thermal albedo and the Gd zoning was
tuned for water). (2) Add a hot-pin DIAGNOSTIC to the peaking cell so we see
WHERE the peak comes from (GT-adjacent / edge / core-facing) instead of guessing.
"""
import ast, json

NB = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

def patch(idx, old, new, check=None):
    c = nb['cells'][idx]; s = ''.join(c['source'])
    if check: assert check in s, f"cell {idx}: '{check}' missing"
    assert s.count(old) == 1, f"cell {idx}: old hits {s.count(old)}"
    s = s.replace(old, new); ast.parse(s)
    c['source'] = s.splitlines(keepends=True)

# (1) reflector -> water
patch(3,
    'RADIAL_REFLECTOR_MODE = "steel"     # "water" | "steel"',
    'RADIAL_REFLECTOR_MODE = "water"     # "water" | "steel"  (steel worsened F_ΔH; see review)')

# (2) hot-pin diagnostic in the peaking cell
DIAG = '''    print(f"   fuel pins counted = {int(good.sum())} (expect {n_fa}×264 = {n_fa*264})")

    # —— DIAGNOSTIC: where do the hottest pins live? (driver identification) ——
    _gt = set(GUIDE_ALL)
    _idx_g = np.where(good)[0]
    def _descr(gp):
        fid = fa_id[gp]; ci, cj = fa_ij[fid]; ring = _core_ring_of(ci, cj)
        pi, pj = FUEL_POS[gp % len(FUEL_POS)]
        gtadj = any((pi+di, pj+dj) in _gt for di, dj in ((1,0),(-1,0),(0,1),(0,-1)))
        edge  = (pi in (0, N_PIN-1) or pj in (0, N_PIN-1))
        # core-facing = pin sits on the half of the FA nearer the core centre
        cc = (N_PIN-1)/2.0; corefacing = ((ci-2)*(pi-cc) + (cj-2)*(pj-cc)) < 0
        return ring, (ci,cj), (pi,pj), gtadj, edge, corefacing
    _order = np.argsort(pin_col_g)[::-1]
    _mean = pin_col_g.mean()
    print("   hottest pins  [rel.pow | FAring | FA(i,j) | pin(i,j) | GTadj | edge | core-facing]:")
    for _r in _order[:8]:
        ring,(ci,cj),(pi,pj),gtadj,edge,cf = _descr(_idx_g[_r])
        print(f"     {pin_col_g[_r]/_mean:5.3f} | r{ring} | FA{(ci,cj)} | pin{(pi,pj)} | "
              f"{'GT-adj' if gtadj else '  -  '} | {'EDGE' if edge else '  -  '} | "
              f"{'CORE' if cf else 'refl'}")'''
patch(28,
    '    print(f"   fuel pins counted = {int(good.sum())} (expect {n_fa}×264 = {n_fa*264})")',
    DIAG, check='def calc_flux_peaking(')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: reflector reverted to water; hot-pin diagnostic added to peaking cell.")
print("    Run-all -> the [9/9] block now lists the 8 hottest pins and their identity.")
