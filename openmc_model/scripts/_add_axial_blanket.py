#!/usr/bin/env python
"""Add a reduced-enrichment AXIAL BLANKET to the rev7 shielding notebook so the
true 3-D F_q stops being driven by un-poisoned, full-enrichment pin ends.

Root cause of F_q ~ 3.4: GD_AXIAL_CUT_CM left the top/bottom 10 cm of the Gd
pins as plain 4.95/4.70% UO2 with NO poison, sitting against the 30 cm water
plena -> a thermal-flux end spike. Standard PWR fix = a reduced-enrichment
axial blanket at each end of EVERY pin. When AXIAL_BLANKET_CM>0 the blanket
supersedes the Gd cutback (it already removes Gd + lowers enrichment there).

Edits (each asserted to hit exactly once, each cell re-compiled):
  cell 3  : add AXIAL_BLANKET_CM / AXIAL_BLANKET_ENRICH config
  cell 8  : _make_pin_universe gains blanket_mat/blanket_cm (blanket end segments)
  cell 9  : _build_fa_universe threads blanket_mat into plain/Gd/Er pin universes
  cell 10 : build_core builds UO2_blanket, passes it in, registers the material

Toggle: AXIAL_BLANKET_CM=0 reverts to the bare-end (Gd-cutback) design.
"""
import ast, json

NB = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

def patch(idx, old, new, check_def=None):
    c = nb['cells'][idx]
    s = ''.join(c['source'])
    if check_def:
        assert check_def in s, f"cell {idx}: sanity '{check_def}' missing"
    assert s.count(old) == 1, f"cell {idx}: old hits {s.count(old)} (need 1)"
    s = s.replace(old, new)
    ast.parse(s)
    c['source'] = s.splitlines(keepends=True)

# ── cell 3: config ──────────────────────────────────────────────────────────
patch(3,
    'GD_AXIAL_CUT_CM = 10.0     # Gd cutback (plain UO₂) at each end, cm',
    'GD_AXIAL_CUT_CM = 10.0     # Gd cutback (plain UO₂) at each end, cm\n'
    '\n'
    '# ── Axial enrichment BLANKET (end-peaking suppression, 2026-06-20) ───────────\n'
    '# Reduced-enrichment fuel at the top & bottom of EVERY pin. The active ends sit\n'
    '# against the 30 cm water plena; with full 4.95% UO₂ there (and the Gd cutback\n'
    '# REMOVING poison) the thermal flux spikes → true 3-D F_q blew up to ~3.4. A\n'
    '# standard PWR axial blanket clips that end-peak. When AXIAL_BLANKET_CM>0 it\n'
    '# supersedes the Gd cutback (the blanket already removes Gd + lowers enrichment\n'
    '# at the ends). Set AXIAL_BLANKET_CM=0 to revert to the bare-end design.\n'
    'AXIAL_BLANKET_CM     = 15.0    # cm of reduced-enrichment fuel at each end\n'
    'AXIAL_BLANKET_ENRICH = 2.5     # wt% U-235 in the blanket (no Gd)',
    check_def='GD_AXIAL_CUT_CM = 10.0')

# ── cell 8: _make_pin_universe ──────────────────────────────────────────────
OLD8 = '''def _make_pin_universe(fuel_mat, water_mat, clad_mat, gap_mat,
                       name="pin", gd_cut_bot=0.0, gd_cut_top=0.0, cutback_mat=None):
    """Pin universe valid for **all z**. Inside z ∈ [-H/2, +H/2] is fuel+clad+gap+moderator;
       outside (axial plena) every radial position becomes water.
       Optional Gd axial cutback (plain UO₂) at the top/bottom of the active region."""
    fuel_cyl = openmc.ZCylinder(r=FUEL_RADIUS)
    clad_i   = openmc.ZCylinder(r=CLAD_INNER_R)
    clad_o   = openmc.ZCylinder(r=CLAD_OUTER_R)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)

    cutback_mat = cutback_mat or fuel_mat
    cells = []

    # — Active-region fuel column with optional Gd axial cutback —
    if gd_cut_bot > 0:
        zb = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0 + gd_cut_bot)
        cells.append(openmc.Cell(name=f"{name}_bot_cut", fill=cutback_mat,
                                 region=-fuel_cyl & +zbot & -zb))
    else:
        zb = zbot

    if gd_cut_top > 0:
        zt = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0 - gd_cut_top)
        cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                 region=-fuel_cyl & +zb & -zt))
        cells.append(openmc.Cell(name=f"{name}_top_cut", fill=cutback_mat,
                                 region=-fuel_cyl & +zt & -ztop))
    else:
        zt = ztop
        cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                 region=-fuel_cyl & +zb & -zt))
'''

NEW8 = '''def _make_pin_universe(fuel_mat, water_mat, clad_mat, gap_mat,
                       name="pin", gd_cut_bot=0.0, gd_cut_top=0.0, cutback_mat=None,
                       blanket_mat=None, blanket_cm=0.0):
    """Pin universe valid for **all z**. Inside z ∈ [-H/2, +H/2] is fuel+clad+gap+moderator;
       outside (axial plena) every radial position becomes water.
       If blanket_mat/blanket_cm given, the top & bottom blanket_cm of the active
       column become reduced-enrichment blanket fuel (applies to EVERY pin and
       supersedes the Gd axial cutback). Otherwise the optional Gd axial cutback
       (plain UO₂) is applied at the top/bottom of the active region."""
    fuel_cyl = openmc.ZCylinder(r=FUEL_RADIUS)
    clad_i   = openmc.ZCylinder(r=CLAD_INNER_R)
    clad_o   = openmc.ZCylinder(r=CLAD_OUTER_R)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)

    cutback_mat = cutback_mat or fuel_mat
    cells = []

    if blanket_mat is not None and blanket_cm > 0:
        # — Reduced-enrichment axial blanket at each end (all pins) —
        zbb = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0 + blanket_cm)
        ztb = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0 - blanket_cm)
        cells.append(openmc.Cell(name=f"{name}_blk_bot", fill=blanket_mat,
                                 region=-fuel_cyl & +zbot & -zbb))
        cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                 region=-fuel_cyl & +zbb & -ztb))
        cells.append(openmc.Cell(name=f"{name}_blk_top", fill=blanket_mat,
                                 region=-fuel_cyl & +ztb & -ztop))
    else:
        # — Active-region fuel column with optional Gd axial cutback —
        if gd_cut_bot > 0:
            zb = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0 + gd_cut_bot)
            cells.append(openmc.Cell(name=f"{name}_bot_cut", fill=cutback_mat,
                                     region=-fuel_cyl & +zbot & -zb))
        else:
            zb = zbot

        if gd_cut_top > 0:
            zt = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0 - gd_cut_top)
            cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                     region=-fuel_cyl & +zb & -zt))
            cells.append(openmc.Cell(name=f"{name}_top_cut", fill=cutback_mat,
                                     region=-fuel_cyl & +zt & -ztop))
        else:
            zt = ztop
            cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                     region=-fuel_cyl & +zb & -zt))
'''
patch(8, OLD8, NEW8, check_def='def _make_pin_universe(')

# ── cell 9: _build_fa_universe signature + 3 pin-creation calls ──────────────
patch(9,
    'gd_positions=None, er_positions=None):',
    'gd_positions=None, er_positions=None, blanket_mat=None):',
    check_def='def _build_fa_universe(')

patch(9,
    '''            pin_universes[ukey] = _make_pin_universe(
                plain_mats[f"UO2_{e:.1f}"], water, clad, gap, name=f"{name}_{ukey}")''',
    '''            pin_universes[ukey] = _make_pin_universe(
                plain_mats[f"UO2_{e:.1f}"], water, clad, gap, name=f"{name}_{ukey}",
                blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)''')

patch(9,
    '''    gd_pin_u = _make_pin_universe(gd_mat, water, clad, gap, name=f"{name}_Gd_pin",
                                  gd_cut_bot=GD_AXIAL_CUT_CM,
                                  gd_cut_top=GD_AXIAL_CUT_CM,
                                  cutback_mat=gd_cut_mat)''',
    '''    gd_pin_u = _make_pin_universe(gd_mat, water, clad, gap, name=f"{name}_Gd_pin",
                                  gd_cut_bot=GD_AXIAL_CUT_CM,
                                  gd_cut_top=GD_AXIAL_CUT_CM,
                                  cutback_mat=gd_cut_mat,
                                  blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)''')

patch(9,
    '        er_pin_u = _make_pin_universe(er_mat, water, clad, gap, name=f"{name}_Er_pin")',
    '        er_pin_u = _make_pin_universe(er_mat, water, clad, gap, name=f"{name}_Er_pin",\n'
    '                                      blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)')

# ── cell 10: build_core — material + thread-through + register ───────────────
patch(10,
    '    gd_cut_mat = mat_uo2(ENRICH_MID, temp=fuel_temp, name="Gd_cutback_UO2")',
    '    gd_cut_mat = mat_uo2(ENRICH_MID, temp=fuel_temp, name="Gd_cutback_UO2")\n'
    '    blanket_mat = (mat_uo2(AXIAL_BLANKET_ENRICH, temp=fuel_temp, name="UO2_blanket")\n'
    '                   if AXIAL_BLANKET_CM > 0 else None)',
    check_def='def build_core(')

patch(10,
    '''    mat_dict = {"water": water, "refl_water": refl_water, "clad": clad,
                "gap": gap, "b4c": b4c, "gd_fuel": gd_mat, "gd_cutback": gd_cut_mat}''',
    '''    mat_dict = {"water": water, "refl_water": refl_water, "clad": clad,
                "gap": gap, "b4c": b4c, "gd_fuel": gd_mat, "gd_cutback": gd_cut_mat}
    if blanket_mat is not None: mat_dict["blanket"] = blanket_mat''')

patch(10,
    '''            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er)''',
    '''            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat)''')

patch(10,
    '''            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er)''',
    '''            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat)''')

patch(10,
    '    _add(gd_mat); _add(er_mat)',
    '    _add(gd_mat); _add(er_mat); _add(blanket_mat)')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))   # roundtrip
print("OK: axial blanket added (15 cm @ 2.5 wt%, supersedes Gd cutback).")
print("    Toggle in cell 3: AXIAL_BLANKET_CM (0 reverts) / AXIAL_BLANKET_ENRICH.")
print("    Re-run: restart kernel -> run all (or at least cells 3,8,9,10 then the F_q cell).")
