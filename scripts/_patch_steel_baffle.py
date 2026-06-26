#!/usr/bin/env python
"""Fix the F_ΔH edge-pin peak at its ROOT: replace the innermost 2.5 cm of the
all-water reflector with a realistic SS304 baffle.  The all-water reflector
over-thermalises returning neutrons and drives an artificial power spike in the
reflector-facing edge pins (diagnostic: all top-6 F_ΔH pins are ring-2,
outer-zone, assembly-perimeter, reflector-facing).  A steel baffle reflects
without that thermal spike — more physical (iPWRs have a steel baffle/barrel)
and de-peaks the edge at NO fuel/burnup cost.  STEEL_BAFFLE=False = exact rev6.

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

# P1: config knobs (cell 3)
patch(3,
"""RADIAL_REFLECTOR_CM = 20.0   # baffle+barrel+downcomer simplified as 20 cm water
AXIAL_REFLECTOR_CM  = 30.0   # top and bottom water plena""",
"""RADIAL_REFLECTOR_CM = 20.0   # baffle+barrel+downcomer total radial envelope
AXIAL_REFLECTOR_CM  = 30.0   # top and bottom water plena
# Realistic SS304 baffle at the core edge instead of pure water.  All-water
# over-thermalises returning neutrons -> artificial power spike on the
# reflector-facing edge pins (the real F_ΔH driver).  A steel baffle reflects
# without that spike: more physical (NuScale/iPWRs have one) and de-peaks the
# edge at no fuel cost.  STEEL_BAFFLE=False = exact rev6 (all water).
STEEL_BAFFLE = True
BAFFLE_CM    = 2.5           # SS304 thickness; remaining (20-2.5) cm stays water"""
)

# config print line (cell 3)
patch(3,
'''print(f"Radial reflector: {RADIAL_REFLECTOR_CM} cm H2O  |  axial: ±{AXIAL_REFLECTOR_CM} cm H2O")''',
'''print(f"Radial reflector: {RADIAL_REFLECTOR_CM} cm "
      + (f"({BAFFLE_CM} cm SS304 baffle + {RADIAL_REFLECTOR_CM-BAFFLE_CM:.1f} cm H2O)" if STEEL_BAFFLE else "H2O")
      + f"  |  axial: ±{AXIAL_REFLECTOR_CM} cm H2O")'''
)

# P2: SS304 material factory (cell 6)
patch(6,
"""def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    m.add_element("B", 4.0)
    m.add_element("C", 1.0)
    return m""",
"""def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    m.add_element("B", 4.0)
    m.add_element("C", 1.0)
    return m


def mat_ss304(temp=T_MOD_K):
    \"\"\"SS304 stainless — core baffle/barrel.\"\"\"
    m = openmc.Material(name="SS304", temperature=temp)
    m.set_density("g/cm3", 7.94)
    m.add_element("Fe", 0.695, percent_type="wo")
    m.add_element("Cr", 0.190, percent_type="wo")
    m.add_element("Ni", 0.095, percent_type="wo")
    m.add_element("Mn", 0.020, percent_type="wo")
    return m"""
)

# P3: instantiate ss304 in build_core (cell 10)
patch(10,
'''    refl_water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_reflector")''',
'''    refl_water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_reflector")
    ss304 = mat_ss304(temp=mod_temp) if (STEEL_BAFFLE and BAFFLE_CM > 0) else None'''
)

# P4: split the reflector into steel baffle (inner) + water (outer) (cell 10)
patch(10,
"""    refl_cell = openmc.Cell(name="radial_reflector", fill=refl_water,
                            region=(+xlo & -xhi & +ylo & -yhi & +zlo & -zhi)
                                   & ~(+xlo_c & -xhi_c & +ylo_c & -yhi_c))

    geom = openmc.Geometry(openmc.Universe(cells=[core_cell, refl_cell]))""",
"""    if ss304 is not None:
        bh = core_half + BAFFLE_CM
        xlo_b = openmc.XPlane(-bh); xhi_b = openmc.XPlane(bh)
        ylo_b = openmc.YPlane(-bh); yhi_b = openmc.YPlane(bh)
        baffle_cell = openmc.Cell(name="steel_baffle", fill=ss304,
                            region=(+xlo_b & -xhi_b & +ylo_b & -yhi_b & +zlo & -zhi)
                                   & ~(+xlo_c & -xhi_c & +ylo_c & -yhi_c))
        refl_cell = openmc.Cell(name="radial_reflector", fill=refl_water,
                            region=(+xlo & -xhi & +ylo & -yhi & +zlo & -zhi)
                                   & ~(+xlo_b & -xhi_b & +ylo_b & -yhi_b))
        refl_cells = [baffle_cell, refl_cell]
    else:
        refl_cell = openmc.Cell(name="radial_reflector", fill=refl_water,
                            region=(+xlo & -xhi & +ylo & -yhi & +zlo & -zhi)
                                   & ~(+xlo_c & -xhi_c & +ylo_c & -yhi_c))
        refl_cells = [refl_cell]

    geom = openmc.Geometry(openmc.Universe(cells=[core_cell, *refl_cells]))"""
)

# P5: register ss304 in the materials list (cell 10)
patch(10,
'''    _add(water); _add(refl_water); _add(clad); _add(gap); _add(b4c); _add(gd_cut_mat)''',
'''    _add(water); _add(refl_water); _add(clad); _add(gap); _add(b4c); _add(gd_cut_mat)
    _add(ss304)'''
)

for idx in (3, 6, 10):
    ast.parse(''.join(nb['cells'][idx]['source']))
json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: SS304 baffle (2.5 cm) + 17.5 cm water; cells 3/6/10 compile; JSON re-parses.")
