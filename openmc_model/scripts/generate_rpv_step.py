"""Generate STEP CAD of the Aegis-40 INTEGRAL reactor pressure vessel for Creo.

Tall, slender integral-iPWR vessel in the style of the Generation-mPower / NuScale
layout (Kapernick 2015, Fig. 2.5) and our own design basis: a single pressure
vessel containing core + primary loop, with NO large external penetrations and
NO reactor coolant pumps (natural circulation).

Architecture (bottom -> top), our locked Aegis-40 design:
  * Conical support SKIRT + base flange on the lower vessel
  * Lower hemispherical head + lower plenum / flow distributor plate
  * Reactor CORE (21 FA + radial reflector + core barrel) between lower & upper
    core support plates
  * In-vessel CRDM units (9) over the central + inner-ring CR clusters, each a
    lower housing + latch/motor housing + drive rod
  * Central RISER carrying hot coolant up out of the core
  * Integral helical-coil once-through STEAM GENERATOR (multi-layer counter-wound
    tube bundle between two tube sheets) in the upper annulus
  * Upper plenum + self-PRESSURIZER (body + dome + heater rods + surge line) on top
  * Two secondary nozzles (feedwater in / steam out) - the only shell penetrations

The vessel structure (shell / skirt / pressurizer / SG shroud / riser / tube sheets
/ core plates) is QUARTER-CUT (+X,+Y quadrant removed) so the internals show through,
like the reference cutaways. SG coils, CRDM, heater rods, nozzles and the core are
left whole. Fuel is SIMPLIFIED to envelope blocks by default (detailed=False).

Two outputs (docs/competition/cad/):
  aegis_rpv.step        light: detailed vessel + envelope-block core (open this)
  aegis_rpv_full.step   heavy: same vessel + 21 detailed FA bundles (large file)

Run:  py scripts/generate_rpv_step.py

DIMENSIONS: the Tier-A core geometry is LOCKED (geometry.xml). The VESSEL, riser,
SG, pressurizer, CRDM and elevations are Tier-B DESIGN-DEFINED (aegis40-geometry-spec.md,
RPV ID 2800 / wall 160 / ~10 m tall) -- recommended starting points, CONFIRM with
the TH/mechanical lead. All lengths in mm.
"""

import csv
import math
import os
import cadquery as cq
from cadquery import Assembly, Color

import generate_fa_step as fa
import generate_core_step as core

OUT = fa.OUT
CORE_MAP = os.path.join(OUT, "core_map.csv")

# ---- vessel envelope (mm), Tier B  CONFIRM ----------------------------------
R_IN = 1400.0
WALL = 160.0
R_OUT = R_IN + WALL                        # 1560

CORE_BOT = core.Z0                          # -281.5
CORE_TOP = core.Z0 + core.CORE_H           #  2318.5

LOWER_PLENUM = 800.0
Z_CYL_BOT = CORE_BOT - LOWER_PLENUM        # -1081.5

Z_RISER_TOP = CORE_TOP + 3000.0            #  5318.5
UPPER_PLENUM = 800.0
Z_CYL_TOP = Z_RISER_TOP + UPPER_PLENUM     #  6118.5

DOME_TOP = Z_CYL_TOP + R_OUT
BOT_POLE = Z_CYL_BOT - R_OUT

# riser
RISER_R = 560.0
RISER_WALL = 30.0

# steam generator (helical bundle + tube sheets + shroud)
SG_Z0 = CORE_TOP + 250.0
SG_Z1 = Z_RISER_TOP - 150.0
SG_SHROUD_R = 1180.0
SG_LAYER_R = (665.0, 750.0, 835.0, 920.0, 1005.0, 1075.0)
SG_TUBE_R = 17.0
SG_PITCH = 230.0
TUBESHEET_RO, TUBESHEET_RI = 1100.0, 630.0

# self-pressurizer
PZR_R = 470.0
PZR_Z0 = DOME_TOP - 250.0
PZR_BODY = 1100.0
PZR_HEATER_R = 26.0
PZR_HEATER_RING = 250.0
SURGE_R = 70.0

# in-vessel CRDM
CRDM_HOUS_R = 70.0
CRDM_LATCH_R = 98.0
CRDM_ROD_R = 28.0
CRDM_Z0 = CORE_TOP - 50.0
CRDM_HOUS_TOP = CRDM_Z0 + 900.0
CRDM_LATCH_TOP = CRDM_HOUS_TOP + 320.0
CRDM_ROD_TOP = CRDM_LATCH_TOP + 1300.0

# secondary nozzles
NOZ_R = 130.0
NOZ_X1 = R_OUT + 320.0

# support skirt
SKIRT_TOP = CORE_BOT + 150.0
SKIRT_BOT = Z_CYL_BOT - 80.0
SKIRT_FLARE = 330.0

# core support plates
PLATE_R = 760.0
PLATE_T = 80.0

# ---- colours ----------------------------------------------------------------
C_STEEL = Color(0.62, 0.64, 0.68)
C_SKIRT = Color(0.50, 0.51, 0.55)
C_RISER = Color(0.55, 0.57, 0.61)
C_SG_SHROUD = Color(0.60, 0.84, 0.90, 0.18)
C_TUBESHEET = Color(0.52, 0.53, 0.57)
C_COIL = Color(0.74, 0.47, 0.22)
C_COIL2 = Color(0.80, 0.55, 0.30)
C_PZR = Color(0.46, 0.47, 0.51)
C_HEATER = Color(0.85, 0.30, 0.20)
C_CRDM = Color(0.72, 0.74, 0.78)
C_LATCH = Color(0.58, 0.60, 0.64)
C_PLATE = Color(0.50, 0.52, 0.56)


# ---- primitive helpers ------------------------------------------------------
def _cyl(R, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).circle(R).extrude(h).val()


def _ring(R_o, R_i, z0, h):
    return (cq.Workplane("XY").workplane(offset=z0)
            .circle(R_o).circle(R_i).extrude(h).val())


def _sphere(R, zc):
    return cq.Workplane("XY").sphere(R).translate((0, 0, zc)).val()


def _frustum(zb, zt, rb, rt):
    return (cq.Workplane("XY").workplane(offset=zb).circle(rb)
            .workplane(offset=zt - zb).circle(rt).loft(ruled=True).val())


def _quarter_cut(solid):
    """Remove the +X,+Y quadrant (corner at the axis) for the cutaway view."""
    big = 13000.0
    box = (cq.Workplane("XY").workplane(offset=-5500.0)
           .box(big, big, big, centered=False).val())
    return solid.cut(box)


def _helix_coil(radius, z0, height, pitch, tube_r, phase_deg=0.0, lefthand=False):
    helix = cq.Wire.makeHelix(pitch, height, radius, lefthand=lefthand)
    path = cq.Workplane(obj=helix)
    prof = cq.Workplane("XZ").center(radius, 0).circle(tube_r)
    coil = prof.sweep(path, isFrenet=True).val()
    coil = coil.translate((0, 0, z0))
    if phase_deg:
        coil = coil.rotate((0, 0, 0), (0, 0, 1), phase_deg)
    return coil


# ---- vessel pieces ----------------------------------------------------------
def vessel_shell():
    outer = (_cyl(R_OUT, Z_CYL_BOT, Z_CYL_TOP - Z_CYL_BOT)
             .fuse(_sphere(R_OUT, Z_CYL_BOT)).fuse(_sphere(R_OUT, Z_CYL_TOP)))
    inner = (_cyl(R_IN, Z_CYL_BOT, Z_CYL_TOP - Z_CYL_BOT)
             .fuse(_sphere(R_IN, Z_CYL_BOT)).fuse(_sphere(R_IN, Z_CYL_TOP)))
    return outer.cut(inner)


def pressurizer_body():
    body = _ring(PZR_R, PZR_R - 40.0, PZR_Z0, PZR_BODY)
    dome = (_sphere(PZR_R, PZR_Z0 + PZR_BODY).cut(_sphere(PZR_R - 40.0, PZR_Z0 + PZR_BODY))
            .cut(_cyl(PZR_R + 10.0, PZR_Z0 + PZR_BODY - PZR_R, PZR_R)))
    surge = _cyl(SURGE_R, Z_CYL_TOP - 100.0, PZR_Z0 - (Z_CYL_TOP - 100.0) + 50.0)
    return body.fuse(dome).fuse(surge)


def pressurizer_heaters():
    rods = []
    for k in range(8):
        a = math.radians(k * 45.0)
        x, y = PZR_HEATER_RING * math.cos(a), PZR_HEATER_RING * math.sin(a)
        rods.append(_cyl(PZR_HEATER_R, PZR_Z0 + 40.0, 520.0).translate((x, y, 0)))
    return rods


def riser():
    return _ring(RISER_R, RISER_R - RISER_WALL, CORE_TOP, Z_RISER_TOP - CORE_TOP)


def steam_generator():
    coils, lefthand = [], False
    for i, r in enumerate(SG_LAYER_R):
        for phase in (0.0, 180.0):
            coils.append(_helix_coil(r, SG_Z0, SG_Z1 - SG_Z0, SG_PITCH, SG_TUBE_R,
                                     phase_deg=phase, lefthand=lefthand))
        lefthand = not lefthand                  # counter-wound adjacent layers
    sheets = [_ring(TUBESHEET_RO, TUBESHEET_RI, SG_Z0 - 60.0, 60.0),
              _ring(TUBESHEET_RO, TUBESHEET_RI, SG_Z1, 60.0)]
    shroud = _ring(SG_SHROUD_R, SG_SHROUD_R - 25.0, SG_Z0 - 60.0, (SG_Z1 + 60.0) - (SG_Z0 - 60.0))
    return coils, sheets, shroud


def skirt():
    outer = _frustum(SKIRT_BOT, SKIRT_TOP, R_OUT + SKIRT_FLARE, R_OUT)
    inner = _frustum(SKIRT_BOT - 2.0, SKIRT_TOP + 2.0,
                     R_OUT + SKIRT_FLARE - 60.0, R_OUT - 60.0)
    band = outer.cut(inner)
    base = _ring(R_OUT + SKIRT_FLARE + 60.0, R_OUT + SKIRT_FLARE - 90.0, SKIRT_BOT - 90.0, 90.0)
    return band.fuse(base)


def core_plates():
    lower = _cyl(PLATE_R, CORE_BOT - PLATE_T, PLATE_T)
    upper = _cyl(PLATE_R, CORE_TOP, PLATE_T)
    distributor = _cyl(PLATE_R + 40.0, Z_CYL_BOT + 150.0, 70.0)   # lower-plenum flow plate
    return [lower, upper, distributor]


def crdm_unit(x, y):
    housing = _cyl(CRDM_HOUS_R, CRDM_Z0, CRDM_HOUS_TOP - CRDM_Z0)
    latch = _cyl(CRDM_LATCH_R, CRDM_HOUS_TOP, CRDM_LATCH_TOP - CRDM_HOUS_TOP)
    rod = _cyl(CRDM_ROD_R, CRDM_LATCH_TOP, CRDM_ROD_TOP - CRDM_LATCH_TOP)
    return [(housing.translate((x, y, 0)), C_CRDM),
            (latch.translate((x, y, 0)), C_LATCH),
            (rod.translate((x, y, 0)), C_CRDM)]


def nozzle(sign, z):
    if sign > 0:
        return (cq.Workplane("YZ").workplane(offset=R_IN - 80.0)
                .center(0, z).circle(NOZ_R).extrude(NOZ_X1 - (R_IN - 80.0)).val())
    return (cq.Workplane("YZ").workplane(offset=-NOZ_X1)
            .center(0, z).circle(NOZ_R).extrude(NOZ_X1 - (R_IN - 80.0)).val())


def crdm_positions():
    pos = []
    with open(CORE_MAP, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["ring"] in ("r0", "r1"):
                pos.append((float(r["x_mm"]), float(r["y_mm"])))
    return pos


# ---- assembly ---------------------------------------------------------------
def build_rpv(detailed):
    rpv = Assembly(name="Aegis40_RPV_Integral")

    # structural shells (quarter-cut for the cutaway)
    rpv.add(_quarter_cut(vessel_shell()), name="PressureVessel", color=C_STEEL)
    rpv.add(_quarter_cut(skirt()), name="SupportSkirt", color=C_SKIRT)
    rpv.add(_quarter_cut(pressurizer_body()), name="Pressurizer", color=C_PZR)
    rpv.add(_quarter_cut(riser()), name="Riser", color=C_RISER)

    # pressurizer heater rods
    for i, rod in enumerate(pressurizer_heaters(), 1):
        rpv.add(rod, name="PzrHeater_{:02d}".format(i), color=C_HEATER)

    # steam generator (coils whole, tube sheets + shroud quarter-cut)
    coils, sheets, shroud = steam_generator()
    for i, c in enumerate(coils, 1):
        rpv.add(c, name="SG_Coil_{:02d}".format(i),
                color=C_COIL if i % 2 else C_COIL2)
    rpv.add(_quarter_cut(sheets[0]), name="SG_TubeSheet_Lower", color=C_TUBESHEET)
    rpv.add(_quarter_cut(sheets[1]), name="SG_TubeSheet_Upper", color=C_TUBESHEET)
    rpv.add(_quarter_cut(shroud), name="SG_Shroud", color=C_SG_SHROUD)

    # core support plates (quarter-cut)
    for nm, pl in zip(("LowerCorePlate", "UpperCorePlate", "FlowDistributor"),
                      core_plates()):
        rpv.add(_quarter_cut(pl), name=nm, color=C_PLATE)

    # in-vessel CRDM units
    for i, (x, y) in enumerate(crdm_positions(), 1):
        for j, (solid, col) in enumerate(crdm_unit(x, y)):
            rpv.add(solid, name="CRDM_{:02d}_{}".format(i, j), color=col)

    # secondary nozzles
    rpv.add(nozzle(+1, SG_Z0 + 200.0), name="Nozzle_Feedwater", color=Color(0.20, 0.50, 0.85))
    rpv.add(nozzle(-1, SG_Z1 - 200.0), name="Nozzle_MainSteam", color=Color(0.85, 0.33, 0.18))

    # core internals (reflector + barrel + assemblies)
    internals = core.build_core(detailed=detailed)
    internals.name = "CoreInternals"
    rpv.add(internals, name="CoreInternals")
    return rpv


def main():
    print("Building DETAILED integral RPV (vessel internals + envelope-block core) ...")
    a = build_rpv(detailed=False)
    p = os.path.join(OUT, "aegis_rpv.step")
    a.save(p)
    print("  wrote", p, "({:.2f} MB)".format(os.path.getsize(p) / 1024 / 1024))

    print("Building DETAILED RPV FULL (+ 21 detailed FA bundles) ... heavy")
    a = build_rpv(detailed=True)
    p = os.path.join(OUT, "aegis_rpv_full.step")
    a.save(p)
    print("  wrote", p, "({:.2f} MB)".format(os.path.getsize(p) / 1024 / 1024))


if __name__ == "__main__":
    main()
