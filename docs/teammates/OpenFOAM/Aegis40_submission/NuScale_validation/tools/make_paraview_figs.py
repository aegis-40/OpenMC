#!/usr/bin/env pvbatch
"""
NuScale - ParaView figures F8a / F8b / F8c from the PRODUCTION medium mesh (pin_clean/, latest time).

Run headless (tested on ParaView 6.1, macOS):
    /Applications/ParaView-6.1.0.app/Contents/bin/pvbatch tools/make_paraview_figs.py
or, if pvbatch is on PATH:
    pvbatch tools/make_paraview_figs.py

Outputs (exact filenames the report embeds from docs/figs/):
  F8a_xsection_T.png - T on the sub-channel cross-section at the axial peak (z = L/2 = 1.0 m):
                       hot fuel core -> cooler coolant. Geometrically faithful (no exaggeration).
  F8b_axial_T.png    - axial T on the pin centre-plane (chopped-cosine); radial scale exaggerated
                       x26 so the thin pin (pitch 1.26 cm x L 2.0 m ~ 159:1) is legible.
  F8c_velocity.png   - coolant axial velocity U_z on the cross-section at z = 1.0 m: all-positive
                       upflow (no recirculation), peak in the open sub-channel, no-slip at the rod
                       wall (the fuel+clad rod carries no U -> shown grey).

ParaView 6.1 gotchas baked in (these broke the first version):
  * Multi-region (chtMultiRegionFoam): select the PER-REGION internal meshes
    MeshRegions=['/fuel/internalMesh','/clad/internalMesh','/coolant/internalMesh'].
    The merged root 'internalMesh' has GEOMETRY ONLY (no fields) -> flat/uncoloured plot.
    The '{region}.foam' filename trick from paraFoam is ignored by the 6.1 reader.
  * White background needs view.UseColorPaletteForBackground=0 (else palette grey overrides it).
  * ResetCamera fits the bounding SPHERE -> a long thin slice ends up tiny; set CameraParallelScale
    explicitly (setcam) to fill the frame and reserve a right gutter for the colour bar.
  * Fields load as CELL data only (POINT arrays empty) -> colour by ('CELLS', ...).

The case is loaded via a plain 'pin.foam' handle (gitignored by *.foam). Paths are derived from
this script's location, so CWD does not matter.
"""
import os, sys, traceback
from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CASE = os.path.join(ROOT, "pin_clean")           # production = medium mesh
FIGS = os.path.join(ROOT, "docs", "figs")
FOAM = os.path.join(CASE, "pin_clean.foam")
ZPK = 1.0                                         # axial peak z = L/2, L = 2.0 m
EXAG = 26.0                                       # lateral exaggeration for the axial slice (F8b)
REG3 = ['/fuel/internalMesh', '/clad/internalMesh', '/coolant/internalMesh']
GREY = [0.72, 0.72, 0.72]
os.makedirs(FIGS, exist_ok=True)
open(FOAM, "a").close()
T15 = [None]                                      # latest timestep, filled by first reader


def reader(regions):
    r = OpenFOAMReader(FileName=FOAM)
    r.CaseType = 'Reconstructed Case'
    r.MeshRegions = regions
    times = list(r.TimestepValues or [])
    t = times[-1] if times else 15.0
    if T15[0] is None:
        T15[0] = t
    r.UpdatePipeline(t)
    return r


def crange(src, name, comp=0):
    a = src.GetDataInformation().GetCellDataInformation().GetArrayInformation(name)
    return a.GetComponentRange(comp) if a else None


def newview(w, h):
    v = CreateView('RenderView')
    v.ViewSize = [w, h]
    v.UseColorPaletteForBackground = 0
    v.Background = [1, 1, 1]
    v.OrientationAxesVisibility = 0
    v.ViewTime = T15[0]
    return v


def colorbar(v, d, lut, title):
    d.SetScalarBarVisibility(v, True)
    sb = GetScalarBar(lut, v)
    sb.AutoOrient = 0
    sb.Orientation = 'Vertical'
    sb.WindowLocation = 'Any Location'
    sb.Position = [0.87, 0.18]
    sb.ScalarBarLength = 0.62
    sb.Title = title
    sb.ComponentTitle = ''
    sb.TitleColor = [0, 0, 0]
    sb.LabelColor = [0, 0, 0]
    sb.TitleFontSize = 18
    sb.LabelFontSize = 16


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def setcam(v, src, look, up, wpx, hpx, gutter=0.16, margin=1.05):
    """Fill the frame with the slice (explicit parallel scale) and reserve a right gutter."""
    b = src.GetDataInformation().GetBounds()
    c = [(b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2]
    ext = [b[1]-b[0], b[3]-b[2], b[5]-b[4]]
    rt = cross(look, up)
    horiz = abs(rt[0])*ext[0] + abs(rt[1])*ext[1] + abs(rt[2])*ext[2]
    vert = abs(up[0])*ext[0] + abs(up[1])*ext[1] + abs(up[2])*ext[2]
    full_aspect = float(wpx)/hpx
    eff_aspect = float(wpx)*(1-gutter)/hpx
    ps = max(vert/2.0, (horiz/2.0)/eff_aspect) * margin
    shift = (gutter/2.0)*ps*2.0*full_aspect
    focal = [c[i] + rt[i]*shift for i in range(3)]
    dist = (max(ext)+1.0)*3
    v.CameraParallelProjection = 1
    v.CameraFocalPoint = focal
    v.CameraPosition = [focal[i] - look[i]*dist for i in range(3)]
    v.CameraViewUp = list(up)
    v.CameraParallelScale = ps
    Render(v)


def slice_plane(src, origin, normal):
    s = Slice(Input=src); s.SliceType = 'Plane'
    s.SliceType.Origin = origin
    s.SliceType.Normal = normal
    s.UpdatePipeline(T15[0])
    return s


def color_scalar(d, src, name, comp, title, v, presets):
    ColorBy(d, ('CELLS', name) if comp is None else ('CELLS', name, comp))
    lut = GetColorTransferFunction(name)
    lut.NanColor = GREY
    lut.NanOpacity = 1.0
    r = crange(src, name, comp or 0)
    lut.RescaleTransferFunction(r[0], r[1])
    for p in presets:
        try:
            lut.ApplyPreset(p, True); break
        except Exception:
            continue
    colorbar(v, d, lut, title)
    return r


def save(v, fname, wpx, hpx):
    path = os.path.join(FIGS, fname)
    SaveScreenshot(path, v, ImageResolution=[wpx, hpx])
    print("  wrote", path)


def main():
    print("case:", CASE)
    rT = reader(REG3)
    b = rT.GetDataInformation().GetBounds()
    cx, cy = (b[0]+b[1])/2, (b[2]+b[3])/2
    print("  t =", T15[0], " reader cells =", rT.GetDataInformation().GetNumberOfCells())

    # F8a: cross-section T at the axial peak (faithful, top-down)
    sl = slice_plane(rT, [cx, cy, ZPK], [0, 0, 1])
    va = newview(1200, 1000)
    da = Show(sl, va); da.DiffuseColor = GREY
    rA = color_scalar(da, sl, 'T', None, 'T (K)', va, ('Turbo', 'Rainbow Uniform', 'Cool to Warm'))
    setcam(va, sl, [0, 0, -1], [0, 1, 0], 1200, 1000)
    save(va, "F8a_xsection_T.png", 1200, 1000)
    print("  F8a T range", rA)

    # F8b: axial T centre-plane, y exaggerated x26, inlet z=0 on the left
    tr = Transform(Input=rT); tr.Transform = 'Transform'; tr.Transform.Scale = [1, EXAG, 1]
    bb = tr.GetDataInformation().GetBounds()
    slb = slice_plane(tr, [0.0, (bb[2]+bb[3])/2, (bb[4]+bb[5])/2], [1, 0, 0])
    vb = newview(1600, 380)
    db = Show(slb, vb); db.DiffuseColor = GREY
    rB = color_scalar(db, slb, 'T', None, 'T (K)', vb, ('Turbo', 'Rainbow Uniform', 'Cool to Warm'))
    setcam(vb, slb, [1, 0, 0], [0, 1, 0], 1600, 380)
    save(vb, "F8b_axial_T.png", 1600, 380)
    print("  F8b T range", rB)

    # F8c: coolant U_z on the cross-section at z=1.0; fuel+clad rod has no U -> grey
    slc = slice_plane(rT, [cx, cy, ZPK], [0, 0, 1])
    vc = newview(1200, 1000)
    dc = Show(slc, vc); dc.DiffuseColor = GREY
    rC = color_scalar(dc, slc, 'U', 2, 'U_z (m/s)', vc, ('Cool to Warm', 'Viridis (matplotlib)'))
    setcam(vc, slc, [0, 0, -1], [0, 1, 0], 1200, 1000)
    save(vc, "F8c_velocity.png", 1200, 1000)
    print("  F8c U_z range", rC)

    print("DONE -> F8a_xsection_T.png  F8b_axial_T.png  F8c_velocity.png  in docs/figs/")
    print("Next: python3 tools/build_report_nuscale.py")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
