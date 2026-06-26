#!/usr/bin/env python
"""Patch: (1) revert edge grading (it didn't help — peak is intra-assembly, not edge);
         (2) report F_q via the standard separable F_ΔH·F_z (robust) with the raw
             single-node 3-D max kept only as a noise-sensitive diagnostic;
         (3) add a hot-pin diagnostic that prints WHERE the F_ΔH / F_q peaks are
             (assembly, in-FA pin, radius, enrichment, guide-tube adjacency) so the
             de-peaking fix can be targeted.
Verified patch: each replacement hits once; edited cells compile; JSON re-parses.
"""
import ast, json
NB = r'D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev6.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

def patch(idx, old, new, n=1):
    c = nb['cells'][idx]
    src = ''.join(c['source'])
    got = src.count(old)
    assert got == n, f"cell {idx}: expected {n}, got {got}: {old[:70]!r}"
    c['source'] = src.replace(old, new)

# (1) revert edge grading to baseline (machinery stays for later repurpose)
patch(3, "EDGE_PIN_GRADING = True", "EDGE_PIN_GRADING = False")

# (2) F_q separable + raw-max diagnostic
patch(27,
"""    F_dh = float(pin_col_g.max() / pin_col_g.mean())     # radial enthalpy-rise
    F_q  = float(pin_z_g.max()   / pin_z_g.mean())       # true 3-D hot spot
    fz   = pin_z_g.sum(axis=0); fz_norm = fz / fz.mean()
    F_z  = float(fz_norm.max())""",
"""    F_dh = float(pin_col_g.max() / pin_col_g.mean())     # radial enthalpy-rise
    fz   = pin_z_g.sum(axis=0); fz_norm = fz / fz.mean()
    F_z  = float(fz_norm.max())
    # F_q gate value = STANDARD separable F_ΔH·F_z (robust, NUREG/COLR build-up).
    # The raw single-node 3-D max is kept only as a diagnostic: at STAT_MEDIUM it
    # is dominated by per-node Monte-Carlo noise (5544×NZ bins) and is NOT a
    # reliable F_q until STAT_FINAL.
    F_q_3dmax = float(pin_z_g.max() / pin_z_g.mean())
    F_q  = F_dh * F_z""")

# store the raw-max diagnostic alongside
patch(27,
'''    results["axial_peaking_Fz"]           = round(F_z, 3)''',
'''    results["axial_peaking_Fz"]           = round(F_z, 3)
    results["pin_peaking_factor_Fq_3dmax"] = round(F_q_3dmax * PEAKING_UNC, 3)''')

# clarify the F_q print + show the raw 3-D max
patch(27,
'''    print(f"   F_q  (3-D, per-pin)    = {F_q:.3f} raw → {F_q_e:.3f} (+unc)"
          f"  | limit {F_Q_LIMIT} [{_pf(F_q_e, F_Q_LIMIT)}]  design {F_Q_DESIGN} [{_pf(F_q_e, F_Q_DESIGN)}]")
    print(f"   F_z  (axial)           = {F_z:.3f}")''',
'''    print(f"   F_q  (separable F_ΔH·F_z) = {F_q:.3f} → {F_q_e:.3f} (+unc)"
          f"  | limit {F_Q_LIMIT} [{_pf(F_q_e, F_Q_LIMIT)}]  design {F_Q_DESIGN} [{_pf(F_q_e, F_Q_DESIGN)}]")
    print(f"        (raw 3-D single-node max = {F_q_3dmax:.3f} → {F_q_3dmax*PEAKING_UNC:.3f}; "
          f"noise-sensitive — confirm at STAT_FINAL)")
    print(f"   F_z  (axial)           = {F_z:.3f}")''')

# (3) hot-pin diagnostic — WHERE the peak is
patch(27,
'''    print(f"   fuel pins counted = {int(good.sum())} (expect {n_fa}×264 = {n_fa*264})")''',
'''    print(f"   fuel pins counted = {int(good.sum())} (expect {n_fa}×264 = {n_fa*264})")

    # —— hot-pin diagnostic: locate the peak so the de-peaking fix is targeted ——
    _NPFA = len(FUEL_POS)
    _guide = set(GUIDE_ALL)
    def _pininfo(p):
        fa = int(fa_id[p]); ci, cj = fa_ij[fa]; ring = _core_ring_of(ci, cj)
        pi, pj = FUEL_POS[p % _NPFA]
        r = _pin_radius(pi, pj); enr = _pin_enrich(pi, pj, ring)
        adj = any((pi+di, pj+dj) in _guide for di, dj in ((1,0),(-1,0),(0,1),(0,-1)))
        zone = "inner" if r < ZONE_R1_CM else ("mid" if r < ZONE_R2_CM else "outer")
        return (f"FA{fa} ring{ring} core{(ci,cj)} pin(i={pi},j={pj}) r={r:.1f} "
                f"{zone} enr={enr:.2f} {'GT-ADJ' if adj else 'no-GT'}")
    _mean = pin_col[pin_col > 0].mean()
    _order = np.argsort(pin_col)[::-1]
    print("   --- F_ΔH top radial pins ---")
    for p in _order[:6]:
        print(f"     {pin_col[p]/_mean:5.3f}x  {_pininfo(p)}")
    _pp, _pz = np.unravel_index(int(np.argmax(pin_z)), pin_z.shape)
    print(f"   --- raw F_q hot node ---  z-node {_pz}/{NZ}:  {_pininfo(_pp)}")''')

for idx in (3, 27):
    ast.parse(''.join(nb['cells'][idx]['source']))
json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: edge grading reverted; F_q separable + raw-max diagnostic; hot-pin locator added; cells 3/27 compile.")
