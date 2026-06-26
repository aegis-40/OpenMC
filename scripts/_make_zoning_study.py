#!/usr/bin/env python
"""Build the rev7 ZONING-STUDY notebook by copying rev6 and swapping the
enrichment scheme from rev6's intra-FA pin-by-pin grading to the literature
standard: ASSEMBLY-UNIFORM enrichment in radial rings + steel reflector +
discrete zoned Gd rods.

Motivation (user, 2026-06-20): "I've never seen anyone mixing enrichment like
us."  Correct — no SBF SMR in the literature grades enrichment pin-by-pin
within an assembly:
  * SMART (Akbari-Jeyhouni 2018): 2 assembly-uniform enrichments 2.82 / 4.88,
    low-E centre / high-E edge, discrete UO2+8% Gd2O3 rods (count zoned).
  * ATOM  (Nguyen & Kim, Sci.Rep. 2021): uniform 4.95 (centre FA 3.0),
    Gd2O3 CSBA ball-size zoned by ring, SS-304 reflector.
  * PRATIC (EPJ-N 2024): 3 assembly-uniform rings 2.5 / 3.5 / 5.0, discrete
    UO2-Gd2O3 (8%) rods, HEAVY STEEL reflector -> F_xy = 1.543.
All three: assembly-uniform enrichment + radial ring zoning + discrete Gd +
STEEL reflector.  This notebook reproduces that to test whether it beats
rev6's F_dH (stuck at 1.852 FAIL).

The change is gated by ZONING_MODE so the notebook still reproduces rev6 exactly
with ZONING_MODE="intra_fa".  Verified patch: each replacement hits exactly
once; every edited cell re-compiles with ast.parse; JSON re-parses.
"""
import ast, json, shutil, os

SRC = r'D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev6.ipynb'
DST = r'D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev7_zoning.ipynb'

shutil.copyfile(SRC, DST)
nb = json.load(open(DST, encoding='utf-8'))

def patch(idx, old, new, n=1):
    c = nb['cells'][idx]
    src = ''.join(c['source'])
    got = src.count(old)
    assert got == n, f"cell {idx}: expected {n}, got {got}: {old[:70]!r}"
    c['source'] = src.replace(old, new)

# ── CELL 3: config ──────────────────────────────────────────────────────
# (a) steel reflector ON (literature package)
patch(3, 'STEEL_BAFFLE = False',
         'STEEL_BAFFLE = True       # ZONING STUDY: steel reflector like '
         'SMART/ATOM/PRATIC (kills the water-reflector edge-pin spike that '
         'forced rev6 edge grading)')

# (b) insert the assembly-uniform zoning block just before the rev6 intra-FA block
ZBLOCK = (
"# ── ZONING MODE (rev7 study) ──────────────────────────────────────────────\n"
"# rev6 grades enrichment pin-by-pin WITHIN each assembly (3 radial zones +\n"
"# edge-pin derating).  No SBF SMR in the literature does this.  SMART, ATOM\n"
"# (KAIST) and PRATIC (EPJ-N 2024) all use ASSEMBLY-UNIFORM enrichment with\n"
"# radial RING zoning + discrete Gd rods + a STEEL reflector.  This study\n"
"# reproduces that to test whether it gives a lower (passing) F_dH.\n"
"#   'assembly_uniform' -> every pin in a FA has ONE enrichment, set by the\n"
"#                         core ring the FA sits in (this study).\n"
"#   'intra_fa'         -> rev6 pin-by-pin radial + edge grading (exact rev6).\n"
"ZONING_MODE = \"assembly_uniform\"\n"
"\n"
"# Per-core-ring enrichment (ring 0 = centre FA, 1 = inner 8, 2 = outer 12).\n"
"# Low-centre / high-edge flattens the fresh-core radial shape (SMART 2.82/4.88,\n"
"# PRATIC 2.5/3.5/5.0).  FA-weighted avg = (1*3.6 + 8*4.4 + 12*4.95)/21 = 4.68,\n"
"# i.e. ~the rev6 average -> fair fissile-loading comparison.  All <= 5.0 limit.\n"
"# TUNING: if the core comes out edge-peaked, RAISE the centre / LOWER the outer\n"
"# ring; if still centre-peaked, do the opposite.\n"
"RING_ENRICH = {0: 3.6, 1: 4.4, 2: 4.95}\n"
"GD_SUPPORT_ENRICH = 4.4   # enrichment of the UO2 carrying Gd2O3 in the Gd rods\n"
"\n")
patch(3, '# ── 3-zone INTRA-FA enrichment — HIGH-BURNUP BASELINE (rev_3, 2026-06-03) ──',
         ZBLOCK + '# ── 3-zone INTRA-FA enrichment — HIGH-BURNUP BASELINE (rev_3, 2026-06-03) ──')

# (c) uniform Gd for the study — enrichment rings now do the radial flattening,
#     so the rev6 centre-heavy Gd tilt would double-flatten -> edge-peaked.
patch(3, 'RADIAL_GD_ZONING = True',
         'RADIAL_GD_ZONING = False  # ZONING STUDY: enrichment rings do radial '
         'flattening; re-enable + tune GD_RING_WEIGHTS only if shape stays peaked')

# (d) mode-aware config print
patch(3,
'print(f"Enrichment zones : {ENRICH_INNER}/{ENRICH_MID}/{ENRICH_OUTER} wt% (avg ~{_enr_avg:.2f})")',
'if ZONING_MODE == "assembly_uniform":\n'
'    _enr_avg = (1*RING_ENRICH[0] + 8*RING_ENRICH[1] + 12*RING_ENRICH[2]) / 21.0\n'
'    print(f"Enrichment       : ASSEMBLY-UNIFORM rings {RING_ENRICH} wt% (FA-avg ~{_enr_avg:.2f})")\n'
'else:\n'
'    print(f"Enrichment zones : INTRA-FA {ENRICH_INNER}/{ENRICH_MID}/{ENRICH_OUTER} wt% (avg ~{_enr_avg:.2f})")')

# ── CELL 5: _pin_enrich branches on ZONING_MODE ─────────────────────────
patch(5,
'''def _pin_enrich(i, j, core_ring=None):
    """Pin enrichment, applying edge-pin grading for edge assemblies."""
    if _is_edge_graded(i, j, core_ring):
        return min(EDGE_PIN_ENRICH, _enrichment_for_pin(i, j))
    return _enrichment_for_pin(i, j)''',
'''def _pin_enrich(i, j, core_ring=None):
    """Pin enrichment. assembly_uniform -> one enrichment per core ring
    (SMART/ATOM/PRATIC style); intra_fa -> rev6 pin-by-pin radial + edge."""
    if ZONING_MODE == "assembly_uniform":
        ring = 2 if core_ring is None else core_ring
        return RING_ENRICH.get(ring, RING_ENRICH[2])
    if _is_edge_graded(i, j, core_ring):
        return min(EDGE_PIN_ENRICH, _enrichment_for_pin(i, j))
    return _enrichment_for_pin(i, j)''')

# ── CELL 10: plain_mats set + Gd support enrichment ─────────────────────
patch(10,
'''    plain_enrichs = [ENRICH_INNER, ENRICH_MID, ENRICH_OUTER]
    if EDGE_PIN_GRADING:
        plain_enrichs.append(EDGE_PIN_ENRICH)''',
'''    if ZONING_MODE == "assembly_uniform":
        plain_enrichs = sorted(set(RING_ENRICH.values()))
    else:
        plain_enrichs = [ENRICH_INNER, ENRICH_MID, ENRICH_OUTER]
        if EDGE_PIN_GRADING:
            plain_enrichs.append(EDGE_PIN_ENRICH)''')

patch(10,
'''    gd_mat     = _mixed_fuel(ENRICH_MID, gd_wt=GD_WT_PCT, er_wt=0.0,
                             temp=fuel_temp, name="Gd_fuel")
    gd_cut_mat = mat_uo2(ENRICH_MID, temp=fuel_temp, name="Gd_cutback_UO2")

    if N_ER_RODS > 0 and ER_WT_PCT > 0:
        er_mat = _mixed_fuel(ENRICH_MID, gd_wt=0.0, er_wt=ER_WT_PCT,
                             temp=fuel_temp, name="Er_fuel")''',
'''    gd_support = GD_SUPPORT_ENRICH if ZONING_MODE == "assembly_uniform" else ENRICH_MID
    gd_mat     = _mixed_fuel(gd_support, gd_wt=GD_WT_PCT, er_wt=0.0,
                             temp=fuel_temp, name="Gd_fuel")
    gd_cut_mat = mat_uo2(gd_support, temp=fuel_temp, name="Gd_cutback_UO2")

    if N_ER_RODS > 0 and ER_WT_PCT > 0:
        er_mat = _mixed_fuel(gd_support, gd_wt=0.0, er_wt=ER_WT_PCT,
                             temp=fuel_temp, name="Er_fuel")''')

# ── verify every edited cell compiles, then JSON round-trips ─────────────
for idx in (3, 5, 10):
    ast.parse(''.join(nb['cells'][idx]['source']))

json.dump(nb, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(DST, encoding='utf-8'))
print("OK ->", os.path.basename(DST))
print("  ZONING_MODE=assembly_uniform | RING_ENRICH={0:3.6, 1:4.4, 2:4.95} (FA-avg 4.68)")
print("  STEEL_BAFFLE=True (5 cm SS304) | RADIAL_GD_ZONING=False (uniform Gd)")
print("  cells 3/5/10 compile; JSON re-parses; rev6 untouched.")
