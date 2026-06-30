"""Generate STEP CAD of the Aegis-40 17x17 fuel assembly (and a single fuel pin)
as an assembly-of-subassemblies, for import into Creo.

Outputs (docs/competition/cad/):
  aegis_fuel_pin.step       single detailed rod: Pellet + Cladding + 2 end plugs
  aegis_fuel_assembly.step  full 17x17 FA: 264 fuel-pin subassemblies (clad+pellet,
                            colour-coded by type) + 24 guide tubes + 1 instrument
                            tube + a simple skeleton (grid frames + nozzle plates)

Geometry is the LOCKED Tier-A design (geometry.xml -> aegis40-geometry-spec.md).
Pin (col,row,x,y,type) positions come from the centre-FA recipe pinmap_r0.csv, so
the colour map matches the neutronics model (Gd 48 / Er 16 / 3 enrichment zones).

Runs on Windows:  py scripts/generate_fa_step.py
Requires cadquery (OpenCASCADE).  All lengths in mm.
"""

import csv
import os
import cadquery as cq
from cadquery import Assembly, Location, Color, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "competition", "cad")
PINMAP = os.path.join(OUT, "pinmap_r0.csv")

# ---- dimensions (mm), LOCKED Tier A -----------------------------------------
PELLET_OD = 8.192
CLAD_OD, CLAD_ID = 9.520, 8.375
SHANK_OD, GRIP_OD = 8.300, 4.000
GT_OD, GT_ID = 12.040, 11.248     # guide / instrument tube
ACTIVE = 2000.0
CLAD_LEN = 2200.0
PIN_PITCH = 12.623

BP_BODY, BP_SHANK = 8.5, 10.0     # bottom plug: body + shank
TP_SHANK, TP_BODY, TP_GRIP = 10.0, 8.0, 4.0   # top plug: shank + body + grip

Z_CLAD0 = BP_BODY                 # 8.5  clad sits on the bottom-plug body
Z_PELLET0 = BP_BODY + BP_SHANK    # 18.5 pellet rests on the shank
Z_TOPPLUG0 = BP_BODY + CLAD_LEN - TP_SHANK   # 2198.5

# ---- colours ----------------------------------------------------------------
C_PELLET = Color(0.24, 0.24, 0.27)
C_PLUG = Color(0.50, 0.52, 0.55)
C_GUIDE = Color(0.78, 0.80, 0.85)
C_INSTR = Color(0.90, 0.55, 0.15)
C_SKEL = Color(0.42, 0.43, 0.48)
TYPE_COLOUR = {                    # clad colour by pin type (shows the BA layout)
    "plain_4.4": Color(0.74, 0.83, 0.90),
    "plain_4.7": Color(0.36, 0.61, 0.84),
    "plain_5.0": Color(0.12, 0.31, 0.48),
    "Gd": Color(0.75, 0.23, 0.17),
    "Er": Color(0.16, 0.68, 0.38),
}


# ---- primitive solids (built once, reused at each lattice site) -------------
def _cyl(od, z0, length):
    return cq.Workplane("XY").workplane(offset=z0).circle(od / 2.0).extrude(length)


def _tube(od, idd, z0, length):
    return (cq.Workplane("XY").workplane(offset=z0)
            .circle(od / 2.0).circle(idd / 2.0).extrude(length))


PELLET = _cyl(PELLET_OD, Z_PELLET0, ACTIVE).val()
CLAD = _tube(CLAD_OD, CLAD_ID, Z_CLAD0, CLAD_LEN).val()
GUIDE = _tube(GT_OD, GT_ID, Z_CLAD0, CLAD_LEN).val()
BPLUG = (_cyl(CLAD_OD, 0.0, BP_BODY)
         .union(_cyl(SHANK_OD, BP_BODY, BP_SHANK)).val())
TPLUG = (_cyl(SHANK_OD, Z_TOPPLUG0, TP_SHANK)
         .union(_cyl(CLAD_OD, Z_TOPPLUG0 + TP_SHANK, TP_BODY))
         .union(_cyl(GRIP_OD, Z_TOPPLUG0 + TP_SHANK + TP_BODY, TP_GRIP)).val())


def detailed_pin():
    """Single fuel rod as a 4-part subassembly."""
    a = Assembly(name="FuelPin")
    a.add(PELLET, name="Pellet", color=C_PELLET)
    a.add(CLAD, name="Cladding", color=C_GUIDE)
    a.add(BPLUG, name="BottomPlug", color=C_PLUG)
    a.add(TPLUG, name="TopPlug", color=C_PLUG)
    return a


def pin_subassembly(clad_colour):
    """clad + pellet subassembly, clad coloured by pin type (lighter for the full FA)."""
    a = Assembly(name="Pin")
    a.add(CLAD, name="Cladding", color=clad_colour)
    a.add(PELLET, name="Pellet", color=C_PELLET)
    return a


def _grid_frame(zc, h=30.0, outer=216.0, inner=212.0):
    return (cq.Workplane("XY").workplane(offset=zc - h / 2.0)
            .rect(outer, outer).rect(inner, inner).extrude(h).val())


def _nozzle(z0, t=22.0, side=216.0):
    return cq.Workplane("XY").workplane(offset=z0).rect(side, side).extrude(t).val()


def build_assembly():
    fa = Assembly(name="Aegis40_FuelAssembly_17x17")
    with open(PINMAP, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    n_fuel = n_guide = 0
    for r in rows:
        x, y = float(r["x_mm"]), float(r["y_mm"])
        loc = Location(Vector(x, y, 0))
        typ = r["type"]
        tag = "{}_{}".format(r["col"], r["row"])
        if typ == "guide":
            if abs(x) < 1e-6 and abs(y) < 1e-6:
                fa.add(GUIDE, name="InstrumentTube", color=C_INSTR, loc=loc)
            else:
                fa.add(GUIDE, name="GuideTube_" + tag, color=C_GUIDE, loc=loc)
            n_guide += 1
        else:
            colour = TYPE_COLOUR.get(typ, C_GUIDE)
            fa.add(pin_subassembly(colour), name="Pin_" + tag, loc=loc)
            n_fuel += 1

    skel = Assembly(name="Skeleton")
    for zc in (200, 600, 1000, 1400, 1800, 2100):
        skel.add(_grid_frame(float(zc)), name="SpacerGrid_z{}".format(zc), color=C_SKEL)
    skel.add(_nozzle(-22.0), name="BottomNozzle", color=C_SKEL)
    skel.add(_nozzle(CLAD_LEN + BP_BODY + 6.0), name="TopNozzle", color=C_SKEL)
    fa.add(skel, name="Skeleton")

    return fa, n_fuel, n_guide


def main():
    print("Building single detailed fuel pin ...")
    pin = detailed_pin()
    pin_path = os.path.join(OUT, "aegis_fuel_pin.step")
    pin.save(pin_path)
    print("  wrote", pin_path, "({:.1f} KB)".format(os.path.getsize(pin_path) / 1024))

    print("Building 17x17 fuel assembly ...")
    fa, n_fuel, n_guide = build_assembly()
    fa_path = os.path.join(OUT, "aegis_fuel_assembly.step")
    fa.save(fa_path)
    print("  fuel pins: {}   guide/instrument tubes: {}".format(n_fuel, n_guide))
    print("  wrote", fa_path, "({:.1f} MB)".format(os.path.getsize(fa_path) / 1024 / 1024))


if __name__ == "__main__":
    main()
