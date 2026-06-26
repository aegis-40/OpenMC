"""Aegis-40 fuel pin -- Fusion 360 generator script.

Builds ONE 17x17 standard fuel rod as FOUR separate, named components so you can
assemble / section / render them individually:

    Pellet      solid UO2 stack          (active fuel, 2000 mm)
    Cladding    Zr-4 hollow tube         (2200 mm)
    BottomPlug  stepped end plug         (body + shank into clad bore)
    TopPlug     stepped end plug + grip  (above the gas plenum)

All dimensions come straight from the as-run OpenMC geometry.xml (Tier A, LOCKED).
The five values you are most likely to tweak are exposed as editable User
Parameters (Modify > Change Parameters): PELLET_OD, CLAD_ID, CLAD_OD, ACTIVE_LEN,
CLAD_LEN. Change one and the geometry rebuilds.

HOW TO RUN
----------
1. Fusion 360 -> open a new, empty Design (File > New Design).
2. Utilities tab -> ADD-INS -> "Scripts and Add-Ins" (or press Shift+S).
3. Scripts list -> green "+" -> "Script from existing" -> pick THIS file
   (scripts/fusion/aegis_pin.py).  Then select "aegis_pin" -> Run.
4. You should get 4 components stacked into a full fuel rod ~2.22 m tall.

NOTE on units: the Fusion API works internally in CENTIMETRES. geometry.xml is in
cm too, so the conversions are trivial; mm values below are /10 to cm.
"""

import adsk.core
import adsk.fusion
import traceback

# ---- dimensions (mm) -- LOCKED from geometry.xml unless noted ---------------
PELLET_OD = 8.192     # fuel pellet outer diameter
CLAD_ID   = 8.375     # cladding inner diameter (pellet-clad gap = 0.0915 mm radial)
CLAD_OD   = 9.520     # cladding outer diameter (Zr-4)
SHANK_OD  = 8.300     # end-plug shank dia -> slip-fit into clad bore, girth weld
GRIP_OD   = 4.000     # top-plug grip nub (handling/hold-down)
ACTIVE_LEN = 2000.0   # active fuel length (z = -1000..+1000 in the neutronics model)
CLAD_LEN   = 2200.0   # cladding tube length (CAD: +200 mm for plenum + plug seats)

# end-plug segment lengths (mm) -- CAD detail, not in the neutronics model
BP_BODY = 8.5         # bottom plug: body section at clad OD (closed end)
BP_SHANK = 10.0       # bottom plug: shank into clad bore
TP_SHANK = 10.0       # top plug: shank into clad bore
TP_BODY = 8.0         # top plug: body at clad OD
TP_GRIP = 4.0         # top plug: grip nub

MM = 0.1              # mm -> cm (Fusion internal unit)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('No active Design. Open the Design workspace (File > New Design) and run again.')
            return

        # parametric timeline so User Parameters + history exist
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent

        _add_params(design)

        # axial stack-up (mm), z = 0 at the very bottom tip of the rod:
        #   BottomPlug : body 0..8.5, shank 8.5..18.5            -> place at 0
        #   Cladding   : 8.5..2208.5                              -> place at 8.5
        #   Pellet     : 18.5..2018.5 (sits on shank top)         -> place at 18.5
        #   plenum     : 2018.5..2198.5 (180 mm, add Coil here)
        #   TopPlug    : shank 2198.5..2208.5, body+grip above    -> place at 2198.5
        bottom_plug = _make_comp(root, 'BottomPlug', 0.0)
        cladding    = _make_comp(root, 'Cladding', (BP_BODY) * MM)
        pellet      = _make_comp(root, 'Pellet', (BP_BODY + BP_SHANK) * MM)
        top_plug    = _make_comp(root, 'TopPlug', (BP_BODY + CLAD_LEN - TP_SHANK) * MM)

        _build_pellet(pellet)
        _build_cladding(cladding)
        _build_bottom_plug(bottom_plug)
        _build_top_plug(top_plug)

        _colour(pellet, 'UO2', 70, 70, 78)
        _colour(cladding, 'Zircaloy', 150, 170, 185)
        _colour(bottom_plug, 'Zircaloy', 120, 130, 140)
        _colour(top_plug, 'Zircaloy', 120, 130, 140)

        total = BP_BODY + CLAD_LEN + TP_BODY + TP_GRIP
        ui.messageBox(
            'Aegis-40 fuel pin built: 4 components.\n\n'
            'Pellet  Ø{:.3f} x {:.0f} mm\n'
            'Cladding  OD{:.3f}/ID{:.3f} x {:.0f} mm\n'
            'Plenum gap above pellet: ~180 mm (add Coil here, see chat)\n'
            'Overall rod height: ~{:.0f} mm\n\n'
            'Edit dims via Modify > Change Parameters.'.format(
                PELLET_OD, ACTIVE_LEN, CLAD_OD, CLAD_ID, CLAD_LEN, total))

    except:
        if ui:
            ui.messageBox('Script failed:\n{}'.format(traceback.format_exc()))


def _add_params(design):
    up = design.userParameters
    wanted = [
        ('PELLET_OD', '{} mm'.format(PELLET_OD)),
        ('CLAD_ID', '{} mm'.format(CLAD_ID)),
        ('CLAD_OD', '{} mm'.format(CLAD_OD)),
        ('ACTIVE_LEN', '{} mm'.format(ACTIVE_LEN)),
        ('CLAD_LEN', '{} mm'.format(CLAD_LEN)),
        ('PIN_PITCH', '12.623 mm'),  # used later for the 17x17 assembly pattern
    ]
    for name, expr in wanted:
        existing = up.itemByName(name)
        if existing:
            existing.expression = expr
        else:
            up.add(name, adsk.core.ValueInput.createByString(expr), 'mm', '')


def _make_comp(root, name, z_cm):
    """New child component translated to z_cm (cm) along the rod axis."""
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(0.0, 0.0, z_cm)
    occ = root.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ.component


def _circle(comp, dia_cm):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), dia_cm / 2.0)
    return sk


def _extrude(comp, profile, start_mm, length_value, join_body=None):
    ext = comp.features.extrudeFeatures
    op = (adsk.fusion.FeatureOperations.JoinFeatureOperation if join_body
          else adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp = ext.createInput(profile, op)
    if start_mm:
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(
            adsk.core.ValueInput.createByReal(start_mm * MM))
    inp.setDistanceExtent(False, length_value)
    if join_body:
        inp.participantBodies = [join_body]
    return ext.add(inp)


def _build_pellet(comp):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    circ = sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), PELLET_OD / 2.0 * MM)
    dim = sk.sketchDimensions.addDiameterDimension(
        circ, adsk.core.Point3D.create(PELLET_OD * MM, 0, 0))
    dim.parameter.expression = 'PELLET_OD'
    _extrude(comp, sk.profiles.item(0), 0.0,
             adsk.core.ValueInput.createByString('ACTIVE_LEN'))


def _build_cladding(comp):
    sk = comp.sketches.add(comp.xYConstructionPlane)
    c = adsk.core.Point3D.create(0, 0, 0)
    inner = sk.sketchCurves.sketchCircles.addByCenterRadius(c, CLAD_ID / 2.0 * MM)
    outer = sk.sketchCurves.sketchCircles.addByCenterRadius(c, CLAD_OD / 2.0 * MM)
    di = sk.sketchDimensions.addDiameterDimension(
        inner, adsk.core.Point3D.create(CLAD_ID / 2.0 * MM, CLAD_ID / 2.0 * MM, 0))
    di.parameter.expression = 'CLAD_ID'
    do = sk.sketchDimensions.addDiameterDimension(
        outer, adsk.core.Point3D.create(CLAD_OD * MM, CLAD_OD * MM, 0))
    do.parameter.expression = 'CLAD_OD'
    ring = None
    for p in sk.profiles:
        if p.profileLoops.count == 2:   # the annulus has outer + inner loops
            ring = p
            break
    _extrude(comp, ring, 0.0, adsk.core.ValueInput.createByString('CLAD_LEN'))


def _build_bottom_plug(comp):
    sk = _circle(comp, CLAD_OD * MM)
    body = _extrude(comp, sk.profiles.item(0), 0.0,
                    adsk.core.ValueInput.createByReal(BP_BODY * MM))
    target = body.bodies.item(0)
    sk2 = _circle(comp, SHANK_OD * MM)
    _extrude(comp, sk2.profiles.item(0), BP_BODY,
             adsk.core.ValueInput.createByReal(BP_SHANK * MM), join_body=target)


def _build_top_plug(comp):
    sk = _circle(comp, SHANK_OD * MM)
    shank = _extrude(comp, sk.profiles.item(0), 0.0,
                     adsk.core.ValueInput.createByReal(TP_SHANK * MM))
    target = shank.bodies.item(0)
    sk2 = _circle(comp, CLAD_OD * MM)
    _extrude(comp, sk2.profiles.item(0), TP_SHANK,
             adsk.core.ValueInput.createByReal(TP_BODY * MM), join_body=target)
    sk3 = _circle(comp, GRIP_OD * MM)
    _extrude(comp, sk3.profiles.item(0), TP_SHANK + TP_BODY,
             adsk.core.ValueInput.createByReal(TP_GRIP * MM), join_body=target)


def _colour(comp, name, r, g, b):
    """Best-effort: tag bodies with a simple coloured appearance; skip on failure."""
    try:
        body = comp.bRepBodies.item(0)
        body.name = name
    except:
        pass
