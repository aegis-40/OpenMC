#!/usr/bin/env python
"""Re-anchor the rev7 radial shielding model to the REAL CAD vessel dimensions.

The shield was already circular (nested ZCylinders) and multi-layer, but its
radii were placeholder/compact: it put the RPV inner wall at r=93 cm and gave
the downcomer only ~13 cm.  The CAD geometry spec (aegis40-geometry-spec.md
Tier B / B1) has the integral RPV inner wall at r=140 cm (ID 2800 mm) with a
~57 cm downcomer + helical-SG annulus in between — a large water/steel region
that is the dominant attenuator.  Using the real build LOWERS the bioshield
dose and makes the model defensible against "where did these radii come from?".

Only the radii VALUES change; the 9-shell structure, cell names, tallies and
post-processing (cell 41) are untouched.  Bioshield layer THICKNESSES
(cavity 15 / steel 5 / poly 10 / concrete 120 / finish 10 cm) are unchanged —
that is the shield design being evaluated; only their standoff is corrected.

Verified patch: replacement hits once; cell 39 compiles; JSON re-parses.
"""
import ast, json

NB = r'D:\projects\teknofest-2026-aegis-40-ipwr\openmc_model\rev7_shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

OLD = '''R_CORE_CYL = 57.0
R_BARREL = R_CORE_CYL + 5.0     # 62
R_DOWN   = R_BARREL   + 13.0    # 75
R_RPV    = R_DOWN     + 18.0    # 93   <- fast-flux tally here
R_CAV    = R_RPV      + 15.0    # 108
R_THSH   = R_CAV      + 5.0     # 113
R_POLY   = R_THSH     + 10.0    # 123
R_CONC   = R_POLY     + 120.0   # 243  magnetite (lead-free bulk shield)
R_OUT    = R_CONC     + 10.0    # 253'''

NEW = '''# CAD-anchored radial build (cm) — matches aegis40-geometry-spec.md Tier B / B1.
# Vessel radii are the real integral-RPV dimensions; bioshield layer THICKNESSES
# (cavity/steel/poly/concrete) are unchanged (that is the shield design).  The
# big downcomer + helical-SG annulus (82.5->140 cm) is the dominant attenuator
# the old compact radii (RPV at 93) had deleted.
R_CORE_CYL = 80.0               # core box 54 + 20 cm reflector water, out to barrel ID 1600 mm
R_BARREL = 82.5                 # core barrel SS304 (OD 1650 mm; 2.5 cm wall)
R_DOWN   = 140.0                # downcomer + integral helical-SG annulus water (RPV ID 2800 mm)
R_RPV    = 156.5                # RPV SA-508 wall +clad (160+5 mm, OD ~3130 mm)  <- fast-flux/fluence tally
R_CAV    = R_RPV  + 15.0        # 171.5  reactor-cavity air gap
R_THSH   = R_CAV  + 5.0         # 176.5  thermal / neutron steel shield
R_POLY   = R_THSH + 10.0        # 186.5  borated polyethylene (thermal-n capture)
R_CONC   = R_POLY + 120.0       # 306.5  magnetite heavy concrete (lead-free bulk bio-shield)
R_OUT    = R_CONC + 10.0        # 316.5  ordinary-concrete finish'''

c = nb['cells'][39]
src = ''.join(c['source'])
assert src.count(OLD) == 1, src.count(OLD)
c['source'] = src.replace(OLD, NEW)
ast.parse(''.join(c['source']))
json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: shield radii re-anchored to CAD (RPV inner 140 cm, OD 156.5 cm; downcomer 82.5->140).")
print("    9-shell structure, cell names, tallies, post-process (cell 41) unchanged.")
