#!/usr/bin/env python
"""Reconcile the neutronics moderator conditions with the LOCKED §8.4 design
basis.  The notebook carried a stale large-PWR default triplet
(15.5 MPa / 575 K / 0.72266 g/cm³).  Our plant is 12.8 MPa with a core-average
moderator temperature of (308+258)/2 = 283 °C = 556 K (§8.4, design-basis-locked
line 230).  A single-temperature full-core model should use the core-average,
so:
    T_MOD_K        575 K (302 °C, ~hot leg)  ->  556 K (283 °C, core average)
    RHO_WATER_NOM  0.72266 (15.5 MPa)        ->  0.748 (IAPWS-IF97 @ 556 K, 12.8 MPa)
Same IAPWS source §8.4 uses for the cold-leg density (258 °C, 12.8 MPa = 0.7967).

Verified patch: each replacement hits exactly once; cell 3 compiles; JSON re-parses.
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

patch(3, 'T_MOD_K       = 575.0',
         'T_MOD_K       = 556.0   # core-average 283°C = (308+258)/2 @ 12.8 MPa (§8.4)')
patch(3, 'RHO_WATER_NOM = 0.72266    # g/cm³ @ 15.5 MPa, 575 K',
         'RHO_WATER_NOM = 0.74800    # g/cm³, IAPWS-IF97 @ 556 K, 12.8 MPa (§8.4 basis)')

ast.parse(''.join(nb['cells'][3]['source']))
json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: T_MOD_K 575->556 K, RHO_WATER_NOM 0.72266->0.748 (12.8 MPa); cell 3 compiles, JSON re-parses.")
