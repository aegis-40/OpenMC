"""Generate STEP CAD of the full Aegis-40 reactor core for import into Creo.

Builds the 21-FA core inside its cylindrical structures:
  * RadialReflector  - a cylinder (R = 740.1 mm, the as-modeled reflector radius)
                       with the stepped 21-FA cavity booleaned out (translucent,
                       represents the 200 mm H2O radial reflector)
  * CoreBarrel       - steel cylindrical shell around the reflector
  * 21 fuel assemblies on the 5x5-minus-corners map (core_map.csv, pitch 216.038)

Two outputs (docs/competition/cad/):
  aegis_core_context.step   light: 21 FA envelope blocks (coloured by ring) +
                            reflector + barrel. Best for SEEING the cylinder wrap.
  aegis_core_full.step      heavy: 21 detailed FA bundles (reuses generate_fa_step)
                            + reflector + barrel. The full render (large file).

Run:  py scripts/generate_core_step.py
Reuses scripts/generate_fa_step.py for the pin/tube geometry. Lengths in mm.
"""

import csv
import os
import cadquery as cq
from cadquery import Assembly, Location, Color, Vector

import generate_fa_step as fa   # pin/tube solids + build_assembly()

OUT = fa.OUT
CORE_MAP = os.path.join(OUT, "core_map.csv")

FA_PITCH = 216.038
REFL_OUT_R = 740.1                  # geometry.xml radial-reflector outer radius
BARREL_WALL = 30.0
BARREL_OUT_R = REFL_OUT_R + BARREL_WALL

Z_MID = fa.Z_PELLET0 + fa.ACTIVE / 2.0       # active-fuel mid-plane (1018.5 mm)
CORE_H = 2600.0                              # active 2000 + axial reflector 300 each end
Z0 = Z_MID - CORE_H / 2.0
ENV_H = fa.CLAD_LEN                           # FA envelope-block height for context mode

RING_COLOUR = {
    "r0": Color(0.12, 0.31, 0.48),   # centre
    "r1": Color(0.36, 0.61, 0.84),   # inner ring
    "r2": Color(0.74, 0.83, 0.90),   # outer ring
}
C_REFL = Color(0.55, 0.78, 0.92, 0.40)   # translucent water
C_BARREL = Color(0.45, 0.46, 0.50)


def core_positions():
    with open(CORE_MAP, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def reflector_and_barrel():
    """Cylinder minus the stepped 21-FA cavity, plus the surrounding barrel shell."""
    cyl = cq.Workplane("XY").workplane(offset=Z0).circle(REFL_OUT_R).extrude(CORE_H)
    gap = 1.0
    box = FA_PITCH + 2 * gap
    cluster = None
    for r in core_positions():
        x, y = float(r["x_mm"]), float(r["y_mm"])
        b = (cq.Workplane("XY").workplane(offset=Z0 - 50.0)
             .rect(box, box).extrude(CORE_H + 100.0).translate((x, y, 0)))
        cluster = b if cluster is None else cluster.union(b)
    reflector = cyl.cut(cluster).val()
    barrel = (cq.Workplane("XY").workplane(offset=Z0)
              .circle(BARREL_OUT_R).circle(REFL_OUT_R).extrude(CORE_H).val())
    return reflector, barrel


def build_core(detailed):
    core = Assembly(name="Aegis40_Core_21FA")
    reflector, barrel = reflector_and_barrel()
    core.add(reflector, name="RadialReflector_H2O", color=C_REFL)
    core.add(barrel, name="CoreBarrel", color=C_BARREL)

    for r in core_positions():
        x, y, ring = float(r["x_mm"]), float(r["y_mm"]), r["ring"]
        loc = Location(Vector(x, y, 0))
        name = "FA_{}_{}_{}".format(r["col"], r["row"], ring)
        if detailed:
            one_fa, _, _ = fa.build_assembly()
            one_fa.name = name
            core.add(one_fa, name=name, loc=loc)
        else:
            env = (cq.Workplane("XY").workplane(offset=0)
                   .rect(FA_PITCH - 2.0, FA_PITCH - 2.0).extrude(ENV_H).val())
            core.add(env, name=name, color=RING_COLOUR[ring], loc=loc)
    return core


def main():
    print("Building CONTEXT core (21 FA blocks + reflector + barrel) ...")
    c = build_core(detailed=False)
    p = os.path.join(OUT, "aegis_core_context.step")
    c.save(p)
    print("  wrote", p, "({:.2f} MB)".format(os.path.getsize(p) / 1024 / 1024))

    print("Building FULL core (21 detailed FA bundles) ... this is the heavy one")
    c = build_core(detailed=True)
    p = os.path.join(OUT, "aegis_core_full.step")
    c.save(p)
    print("  wrote", p, "({:.2f} MB)".format(os.path.getsize(p) / 1024 / 1024))


if __name__ == "__main__":
    main()
