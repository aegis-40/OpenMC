#!/usr/bin/env python
"""Add a radial-reflector MATERIAL toggle (water vs SS-304 heavy reflector) to
the rev7 shielding notebook, to test the #1 F_ΔH lever.

Physics: a light-water reflector thermalises leaked neutrons and reflects them
back into the peripheral pins -> a thermal-flux spike on the FA edge pins ->
high per-pin F_ΔH. An SS-304 heavy reflector (as on EPR / APR1400) returns a
HARDER spectrum with far less thermalisation -> the edge pins see less thermal
peaking -> flatter F_ΔH, and lower leakage lifts k_eff. microURANUS (Nguyen
2021) shows reflector choice is THE flattening lever for size-constrained SMRs.

When RADIAL_REFLECTOR_MODE=="steel" the 20 cm radial reflector AND the octagon-
corner reflector cells become SS-304 (idealised solid steel; a real heavy
reflector carries ~10% coolant holes). "water" restores the baseline.

Edits (each asserted once, each cell recompiled):
  cell 3  : RADIAL_REFLECTOR_MODE config
  cell 10 : build SS-304 reflector material; route refl_fill into the reflector
            cell, the corner 'water_FA' universe, and the lattice outer; register it
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
    'AXIAL_REFLECTOR_CM  = 30.0   # top and bottom water plena',
    'AXIAL_REFLECTOR_CM  = 30.0   # top and bottom water plena\n'
    '\n'
    '# ── Radial reflector MATERIAL (power-flattening lever, 2026-06-20) ───────────\n'
    '# "water" = 20 cm light-water reflector (baseline). "steel" = SS-304 heavy\n'
    '# reflector (EPR/APR1400-style) replacing that water: harder return spectrum →\n'
    '# less thermal-flux peaking on the peripheral pins → flatter F_ΔH, plus lower\n'
    '# leakage (k up). microURANUS (Nguyen 2021): reflector choice is THE SMR lever.\n'
    '# Idealised solid steel (a real heavy reflector has ~10% coolant holes).\n'
    'RADIAL_REFLECTOR_MODE = "steel"     # "water" | "steel"',
    check='AXIAL_REFLECTOR_CM  = 30.0')

# ── cell 10: material + routing ─────────────────────────────────────────────
patch(10,
    '    refl_water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_reflector")',
    '    refl_water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_reflector")\n'
    '    # Optional SS-304 heavy reflector replacing the water radial reflector\n'
    '    refl_steel = None\n'
    '    if RADIAL_REFLECTOR_MODE == "steel":\n'
    '        refl_steel = openmc.Material(name="SS304_reflector", temperature=mod_temp)\n'
    '        refl_steel.set_density("g/cm3", 7.90)\n'
    '        for _el, _f in (("Fe", .685), ("Cr", .190), ("Ni", .095),\n'
    '                        ("Mn", .020), ("Si", .010)):\n'
    '            refl_steel.add_element(_el, _f, "wo")\n'
    '        refl_steel.depletable = False\n'
    '    refl_fill = refl_steel if refl_steel is not None else refl_water',
    check='def build_core(')

patch(10,
    '    water_u = _water_assembly_universe(refl_water, name="water_FA")',
    '    water_u = _water_assembly_universe(refl_fill, name="water_FA")')

patch(10,
    '    refl_cell = openmc.Cell(name="radial_reflector", fill=refl_water,',
    '    refl_cell = openmc.Cell(name="radial_reflector", fill=refl_fill,')

patch(10,
    '    _add(water); _add(refl_water); _add(clad); _add(gap); _add(b4c); _add(gd_cut_mat)',
    '    _add(water); _add(refl_water); _add(refl_steel); _add(clad); _add(gap); _add(b4c); _add(gd_cut_mat)')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))   # roundtrip
print("OK: radial reflector toggle added; default RADIAL_REFLECTOR_MODE='steel'.")
print("    Reflector cell + octagon corners + lattice outer all follow the mode.")
print("    Revert with RADIAL_REFLECTOR_MODE='water'. Re-run: restart kernel -> run all.")
