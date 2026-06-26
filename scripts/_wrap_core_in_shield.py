#!/usr/bin/env python
"""Make the circular CAD shield part of build_core in the rev7 shielding notebook
so that EVERY analysis (k_eff, MTC/DTC/void, CR worth, peaking, depletion,
geometry plots) runs on the SAME shielded geometry — one consistent model, with
shielding present in the k_eff eigenvalue run (not just a side picture).

Approach (low-risk): keep the validated bare build_core untouched, and insert a
wrapper cell right after it that (a) defines the lead-free shield materials and
(b) redefines build_core to take the bare core's pin lattice and wrap it in the
CAD radial build (barrel / downcomer+SG annulus / RPV / cavity / steel / poly /
concrete) with vacuum at R_OUT.  Because Jupyter resolves build_core at call
time, every downstream cell automatically uses the shielded model.  Toggle
SHIELD_IN_CORE=False reverts to the bare leaky core.

Shield materials are depletable=False so the depletion cell stays valid.
§9 build_shielded_model still works (it rebuilds from the lattice).

Also adds shield colours to the §3 geometry-plot palette so the render is clean.

Verified: wrapper compiles; cell 14 patch hits once; JSON re-parses.
"""
import ast, json

NB = r'D:\projects\teknofest-2026-aegis-40-ipwr\openmc_model\rev7_shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

assert 'def build_core' in ''.join(nb['cells'][10]['source']), "cell 10 not build_core"

WRAP = r'''# ===========================================================================
# CIRCULAR CAD SHIELD wrapped around build_core
# ---------------------------------------------------------------------------
# Makes the biological shield part of THE model every cell uses: k_eff, the
# reactivity coefficients, CR worth, peaking, depletion and the geometry plots
# all run inside the same circular shield.  Radii (cm) follow
# aegis40-geometry-spec.md Tier B / shielding-radial-build.md.
# Set SHIELD_IN_CORE=False to revert to the bare leaky core (vacuum at reflector).
# Note: k_eff comes out a few hundred pcm HIGHER than the bare-core value because
# the real downcomer water + vessel reflect more than vacuum — this is the more
# physical number; the locked design basis keeps the bare-core convention.
# ===========================================================================
SHIELD_IN_CORE = True
SHIELD_RADII = dict(REFL=80.0, BARREL=82.5, DOWN=140.0, RPV=156.5,
                    CAV=171.5, THSH=176.5, POLY=186.5, CONC=306.5, OUT=316.5)

def _sh_ss304(temp, name):
    m = openmc.Material(name=name, temperature=temp); m.set_density("g/cm3", 8.00)
    for el, f in (("Fe", .685), ("Cr", .190), ("Ni", .095), ("Mn", .020), ("Si", .010)):
        m.add_element(el, f, "wo")
    m.depletable = False; return m

def _sh_sa508(temp, name="SA508_RPV"):
    m = openmc.Material(name=name, temperature=temp); m.set_density("g/cm3", 7.90)
    for el, f in (("Fe", .9685), ("Mn", .0140), ("Ni", .0075), ("Mo", .0050),
                  ("Si", .0025), ("Cr", .0003), ("C", .0022)):
        m.add_element(el, f, "wo")
    m.depletable = False; return m

def _sh_air(name="cavity_air"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.001205)
    for el, f in (("N", .7553), ("O", .2318), ("Ar", .0129)): m.add_element(el, f, "wo")
    m.depletable = False; return m

def _sh_poly(name="borated_PE", boron_wt=5.0):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.95); pe = 1 - boron_wt / 100
    m.add_element("C", pe * .8563, "wo"); m.add_element("H", pe * .1437, "wo")
    m.add_element("B", boron_wt / 100, "wo"); m.depletable = False; return m

def _sh_mconc(name="magnetite_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 3.90)
    for el, f in (("H", .0036), ("O", .3100), ("Mg", .0089), ("Al", .0042), ("Si", .0223),
                  ("Ca", .0628), ("Ti", .0067), ("Mn", .0010), ("Fe", .5805)):
        m.add_element(el, f, "wo")
    m.depletable = False; return m

def _sh_oconc(name="ordinary_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 2.30)
    for el, f in (("H", .0056), ("O", .4983), ("Na", .0171), ("Mg", .0024), ("Al", .0456),
                  ("Si", .3158), ("K", .0192), ("Ca", .0826), ("Fe", .0122)):
        m.add_element(el, f, "wo")
    m.depletable = False; return m

_build_core_bare = build_core
def build_core(*args, **kwargs):
    model, mat_dict, info = _build_core_bare(*args, **kwargs)
    if not SHIELD_IN_CORE:
        return model, mat_dict, info
    R = SHIELD_RADII
    core_cell = next(c for c in model.geometry.root_universe.cells.values()
                     if c.name == "core_lat_cell")
    core_lat = core_cell.fill
    Z = info["z_outer_cm"]
    zspan = +openmc.ZPlane(-Z, boundary_type="vacuum") & -openmc.ZPlane(Z, boundary_type="vacuum")
    barrel = _sh_ss304(T_MOD_K, "core_barrel"); rpv = _sh_sa508(T_MOD_K)
    downw = mat_water(temp=T_MOD_K, density=RHO_WATER_NOM, name="downcomer_water"); downw.depletable = False
    air = _sh_air(); thsh = _sh_ss304(T_MOD_K, "thermal_shield"); poly = _sh_poly()
    mconc = _sh_mconc(); oconc = _sh_oconc()
    order = [R["REFL"], R["BARREL"], R["DOWN"], R["RPV"], R["CAV"],
             R["THSH"], R["POLY"], R["CONC"], R["OUT"]]
    cyl = {r: openmc.ZCylinder(r=r) for r in order}; cyl[R["OUT"]].boundary_type = "vacuum"
    def shell(ri, ro, fill, nm):
        reg = (-cyl[ro] if ri is None else (+cyl[ri] & -cyl[ro])) & zspan
        return openmc.Cell(name=nm, fill=fill, region=reg)
    cells = [shell(None,        R["REFL"],   core_lat, "core_lat_cell"),
             shell(R["REFL"],    R["BARREL"], barrel,   "barrel"),
             shell(R["BARREL"],  R["DOWN"],   downw,    "downcomer"),
             shell(R["DOWN"],    R["RPV"],    rpv,      "rpv"),
             shell(R["RPV"],     R["CAV"],    air,      "cavity"),
             shell(R["CAV"],     R["THSH"],   thsh,     "thermal_shield"),
             shell(R["THSH"],    R["POLY"],   poly,     "borated_poly"),
             shell(R["POLY"],    R["CONC"],   mconc,    "magnetite_concrete"),
             shell(R["CONC"],    R["OUT"],    oconc,    "outer_concrete")]
    model.geometry = openmc.Geometry(openmc.Universe(cells=cells))
    model.materials = openmc.Materials(list(model.materials) +
                        [barrel, downw, rpv, air, thsh, poly, mconc, oconc])
    info = dict(info); info["outer_half_cm"] = R["OUT"]; info["shielded"] = True
    return model, mat_dict, info

print(f"build_core now wraps the CIRCULAR CAD shield (SHIELD_IN_CORE={SHIELD_IN_CORE}); "
      f"vacuum at r={SHIELD_RADII['OUT']} cm. k_eff and ALL analyses run shielded.")
'''

ast.parse(WRAP)
new_cell = {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": WRAP.splitlines(keepends=True)}
nb['cells'].insert(11, new_cell)

# add shield colours to the §3 geometry-plot palette (now cell 15 after insert)
PAL_OLD = '''        "UO2_4.0":        (255, 99, 71),
    }'''
PAL_NEW = '''        "UO2_4.0":        (255, 99, 71),
        "core_barrel":      (120, 120, 120),
        "downcomer_water":  (150, 190, 255),
        "SA508_RPV":        (60, 60, 60),
        "cavity_air":       (245, 245, 245),
        "thermal_shield":   (175, 175, 175),
        "borated_PE":       (110, 190, 115),
        "magnetite_concrete": (185, 150, 90),
        "ordinary_concrete":  (210, 190, 160),
    }'''
hit = 0
for c in nb['cells']:
    if c['cell_type'] != 'code':
        continue
    s = ''.join(c['source'])
    if PAL_OLD in s and 'plot_core_geometry' in s:
        c['source'] = s.replace(PAL_OLD, PAL_NEW)
        hit += 1
assert hit == 1, f"palette patch hits: {hit}"

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: build_core now shielded; wrapper inserted after build_core; plot palette updated.")
print("    k_eff cell, coefficients, peaking, depletion and §3 plots all run shielded & consistent.")
