#!/usr/bin/env python
"""Add WABA (Wet Annular Burnable Absorber) B4C rods in guide tubes — a SOLID,
SBF-compatible burnable poison to suppress the water-hole thermal-flux spikes
that drive per-pin F_ΔH (and add reactivity hold-down).

WABA = a B4C-in-Al2O3 annulus dropped into the empty guide tubes, water flowing
through the centre. SOLID poison (not soluble boron) → fully inside the SBF
envelope (same class as our B4C control rods + Gd/Er). Placed only in ring-2
assemblies (12 outer FAs, NO control rods) → no WABA/CR guide-tube conflict.

Edits (each asserted once, each cell recompiled):
  cell 3  : WABA config (enable, rings, B4C wt%, annulus radii)
  cell 6  : mat_waba() factory (B4C+Al2O3, depletable)
  cell 8  : _make_guide_universe gains waba_mat -> annular absorber geometry
  cell 9  : _build_fa_universe builds guide_waba_u + routes guide tubes to it
  cell 10 : build_core builds waba_mat, passes it to ring-2 FA universes, registers

Toggle: WABA_ENABLE=False reverts. WABA_RINGS=(0,1,2) for max effect.
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

# ── cell 3: config ──────────────────────────────────────────────────────────
patch(3,
    '''else:
    ER_WT_PCT = 0.0
    N_ER_RODS = 0''',
    '''else:
    ER_WT_PCT = 0.0
    N_ER_RODS = 0

# ── WABA burnable-poison rods in guide tubes (SBF-compatible: SOLID B4C) ─────
# Wet Annular Burnable Absorber: a B4C-in-Al2O3 annulus in the empty guide tubes
# (water flows through the centre). SOLID poison, NOT soluble boron → fully
# SBF-compatible (same class as our B4C control rods + Gd/Er). Suppresses the
# local thermal-flux spike at the 25 water holes → lowers per-pin F_ΔH, and adds
# reactivity hold-down (trade back some Gd afterwards if k drops too far).
# Placed only in ring-2 assemblies (12 outer FAs, NO control rods) → no WABA/CR
# guide-tube conflict. WABA_RINGS=(0,1,2) for max effect (then the central CR
# tubes become a design caveat to note). WABA_ENABLE=False reverts.
WABA_ENABLE  = True
WABA_RINGS   = (2,)      # core rings carrying WABA (0 centre, 1 inner-8, 2 outer-12)
WABA_B4C_WT  = 12.0      # wt% B4C in the Al2O3 absorber annulus (WABA-class loading)
WABA_R_IN    = 0.286     # absorber annulus inner radius (cm) — coolant inside
WABA_R_OUT   = 0.404     # absorber annulus outer radius (cm); guide-tube ID 0.5624''')

# ── cell 6: mat_waba factory ────────────────────────────────────────────────
patch(6,
    '''def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    m.add_element("B", 4.0)
    m.add_element("C", 1.0)
    return m''',
    '''def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    m.add_element("B", 4.0)
    m.add_element("C", 1.0)
    return m


def mat_waba(b4c_wt=None, temp=T_MOD_K, name="WABA_B4C_Al2O3"):
    """WABA absorber annulus: B4C dispersed in an Al2O3 matrix — a SOLID burnable
       poison (not soluble boron). Depletable so B-10 burns out like a real WABA."""
    if b4c_wt is None:
        b4c_wt = WABA_B4C_WT
    al2o3 = openmc.Material(name="Al2O3", temperature=temp)
    al2o3.set_density("g/cm3", 3.97)
    al2o3.add_element("Al", 2.0); al2o3.add_element("O", 3.0)
    m = openmc.Material.mix_materials([mat_b4c(temp=temp), al2o3],
                                      [b4c_wt / 100.0, 1.0 - b4c_wt / 100.0],
                                      percent_type="wo", name=name)
    m.temperature = temp
    m.depletable = True
    return m''')

# ── cell 8: _make_guide_universe gains waba_mat ─────────────────────────────
patch(8,
    '''def _make_guide_universe(water_mat, b4c_mat=None, name="guide"):
    """Guide tube; b4c_mat=None → water (ARO), b4c_mat=mat → B4C in active region (ARI).
       Like pins, axially open with water plena outside the active height."""
    gt_inner = openmc.ZCylinder(r=0.5624)
    gt_outer = openmc.ZCylinder(r=0.6020)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)
    inner_fill = b4c_mat if b4c_mat is not None else water_mat
    cells = [
        openmc.Cell(fill=inner_fill, region=-gt_inner & +zbot & -ztop),
        openmc.Cell(fill=water_mat,  region=+gt_inner & -gt_outer & +zbot & -ztop),
        openmc.Cell(fill=water_mat,  region=+gt_outer & +zbot & -ztop),
        openmc.Cell(fill=water_mat,  region=+ztop),
        openmc.Cell(fill=water_mat,  region=-zbot),
    ]
    return openmc.Universe(name=name, cells=cells)''',
    '''def _make_guide_universe(water_mat, b4c_mat=None, waba_mat=None, name="guide"):
    """Guide tube. b4c_mat → B4C control rod in active region (ARI). waba_mat →
       WABA burnable-poison annulus (water centre, B4C-Al2O3 ring, water gap).
       Neither → plain water (ARO). Axially open with water plena outside H."""
    gt_inner = openmc.ZCylinder(r=0.5624)
    gt_outer = openmc.ZCylinder(r=0.6020)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)
    cells = []
    if waba_mat is not None and b4c_mat is None:
        r_in  = openmc.ZCylinder(r=WABA_R_IN)
        r_out = openmc.ZCylinder(r=WABA_R_OUT)
        cells.append(openmc.Cell(fill=water_mat, region=-r_in & +zbot & -ztop))
        cells.append(openmc.Cell(fill=waba_mat,  region=+r_in & -r_out & +zbot & -ztop))
        cells.append(openmc.Cell(fill=water_mat, region=+r_out & -gt_inner & +zbot & -ztop))
    else:
        inner_fill = b4c_mat if b4c_mat is not None else water_mat
        cells.append(openmc.Cell(fill=inner_fill, region=-gt_inner & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+gt_inner & -gt_outer & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+gt_outer & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+ztop))
    cells.append(openmc.Cell(fill=water_mat, region=-zbot))
    return openmc.Universe(name=name, cells=cells)''')

# ── cell 9: signature + guide_waba_u + routing ──────────────────────────────
patch(9,
    '''                       gd_positions=None, er_positions=None, blanket_mat=None):''',
    '''                       gd_positions=None, er_positions=None, blanket_mat=None,
                       waba_mat=None):''')

patch(9,
    '''    guide_ari_u = _make_guide_universe(water, b4c_mat=b4c,
                                       name=f"{name}_guide_ari")
    instrument_u = guide_aro_u   # instrument tube never gets a rod''',
    '''    guide_ari_u = _make_guide_universe(water, b4c_mat=b4c,
                                       name=f"{name}_guide_ari")
    guide_waba_u = (_make_guide_universe(water, waba_mat=waba_mat,
                                         name=f"{name}_guide_waba")
                    if waba_mat is not None else None)
    instrument_u = guide_aro_u   # instrument tube never gets a rod''')

patch(9,
    '''            elif pos in set(GUIDE_POS):
                row.append(guide_ari_u if insert_cr else guide_aro_u)''',
    '''            elif pos in set(GUIDE_POS):
                if insert_cr:
                    row.append(guide_ari_u)
                elif guide_waba_u is not None:
                    row.append(guide_waba_u)
                else:
                    row.append(guide_aro_u)''')

# ── cell 10: build waba_mat, route per ring, register ───────────────────────
patch(10,
    '''    blanket_mat = (mat_uo2(AXIAL_BLANKET_ENRICH, temp=fuel_temp, name="UO2_blanket")
                   if AXIAL_BLANKET_CM > 0 else None)''',
    '''    blanket_mat = (mat_uo2(AXIAL_BLANKET_ENRICH, temp=fuel_temp, name="UO2_blanket")
                   if AXIAL_BLANKET_CM > 0 else None)
    waba_mat = mat_waba(temp=mod_temp) if WABA_ENABLE else None''',
    check='def build_core(')

patch(10,
    '    if blanket_mat is not None: mat_dict["blanket"] = blanket_mat',
    '    if blanket_mat is not None: mat_dict["blanket"] = blanket_mat\n'
    '    if waba_mat is not None: mat_dict["waba"] = waba_mat')

patch(10,
    '''            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat)''',
    '''            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            waba_mat=(waba_mat if ring in WABA_RINGS else None))''')

patch(10,
    '    _add(gd_mat); _add(er_mat); _add(blanket_mat)',
    '    _add(gd_mat); _add(er_mat); _add(blanket_mat); _add(waba_mat)')

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: WABA wired in — B4C-Al2O3 annulus in ring-2 guide tubes (SBF-compatible).")
print("    Tune in cell 3: WABA_B4C_WT, WABA_RINGS, WABA_R_IN/OUT. WABA_ENABLE=False reverts.")
print("    Re-run: restart kernel -> run all; watch [9/9] F_ΔH + hot-pin list + k_BOL.")
