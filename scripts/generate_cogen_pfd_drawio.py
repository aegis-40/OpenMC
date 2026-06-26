"""Emit an editable draw.io (diagrams.net) PFD of the Aegis-40 COGENERATION plant:
single turbine + IHX-isolated thermochemical store (TCES) + district heat + H2.

Hand-editable counterpart to scripts/pfd_cogeneration_tces.py, laid out with extra
spacing so nothing overlaps (the matplotlib version is tight around the IHX/store).
Open in diagrams.net (free, https://app.diagrams.net) and fine-tune as needed.

Design intent: ONE single tandem-compound turbine-generator; the TCES is a non-safety
auxiliary OUTSIDE the nuclear island, coupled only through an intermediate heat
exchanger (IHX). Charge from HP-extraction steam; discharge to a separate 90/45 C
district-heating water loop. Two candidate media (ammine NiCl2-SrCl2/NH3 or zeolite).
Numbers from thermo_cycle.py + tces_dh_balance.py.

Output: docs/competition/cycle/aegis40_cogen_pfd.drawio    Run: py scripts/generate_cogen_pfd_drawio.py
"""
import os
import xml.etree.ElementTree as ET

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cycle", "aegis40_cogen_pfd.drawio")

# palette
C_PRIM = "#c0392b"; C_STEAM = "#e67e22"; C_FEED = "#2471a3"
C_CHG = "#7e5109"; C_DH = "#ca6f1e"; C_ELEC = "#1e8449"; C_H2 = "#7d3c98"
INK = "#1b2631"

# coordinate transform: plant units (x 0..144, y 0..86, y UP) -> draw.io px (y DOWN)
S = 12
def px(x): return round(x * S)
def py(y): return round((86 - y) * S)
def rect(x, y, w, h): return px(x), py(y + h), round(w * S), round(h * S)
def cen(cx, cy, w, h): return px(cx) - round(w * S) / 2, py(cy) - round(h * S) / 2, round(w * S), round(h * S)

cells, edges = [], []
def node(cid, value, style, geom):
    x, y, w, h = geom; cells.append((cid, value, style, x, y, w, h))
def stream(eid, value, color, pts, width=2.4, dashed=False, fcol=None):
    ls = (";dashed=1;dashPattern=8 6" if dashed else "")
    style = ("endArrow=block;endFill=1;html=1;rounded=1;strokeColor=%s;strokeWidth=%s%s;"
             "fontSize=11;fontStyle=1;fontColor=%s;labelBackgroundColor=#ffffff"
             % (color, width, ls, fcol or color))
    edges.append((eid, value, style, [(px(x), py(y)) for x, y in pts]))

# ===================================================================== nuclear island + RPV
node("ni", "NUCLEAR ISLAND  (safety)",
     "rounded=0;html=1;fillColor=none;strokeColor=%s;dashed=1;dashPattern=10 6;verticalAlign=top;"
     "align=left;spacingLeft=6;spacingTop=4;fontSize=12;fontStyle=1;fontColor=%s" % (C_PRIM, C_PRIM),
     rect(4.5, 18, 22, 58))
node("rpv", "Integral RPV  (R-1)\nnatural circulation\n12.8 MPa - 308/258 C - 125 MWth",
     "rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#fbeee6;strokeColor=%s;strokeWidth=2.5;"
     "verticalAlign=bottom;fontSize=11;fontStyle=2;fontColor=%s;spacingBottom=4" % (C_PRIM, C_PRIM),
     rect(8, 30, 13, 38))
node("core", "Core\n125 MWth", "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5b7b1;strokeColor=%s;"
     "fontStyle=1;fontSize=11" % INK, rect(9.5, 32, 9, 5))
node("otsg", "helical-coil\nOTSG", "rounded=0;whiteSpace=wrap;html=1;fillColor=#fadbd8;strokeColor=%s;"
     "fontSize=10;fontStyle=1" % INK, rect(9.5, 42, 9, 9))
node("pzr", "self-\npressurizer", "rounded=1;arcSize=40;whiteSpace=wrap;html=1;fillColor=#f6ddcc;"
     "strokeColor=%s;fontSize=9" % INK, rect(10.5, 58, 7, 5))

# ===================================================================== single turbine train
node("tgrp", "SINGLE tandem-compound turbine-generator  (one shaft, T-1)",
     "rounded=0;html=1;fillColor=none;strokeColor=#34495e;dashed=1;dashPattern=4 3;verticalAlign=top;"
     "fontSize=11;fontStyle=1;fontColor=#34495e;spacingTop=2", rect(44, 67, 28, 13))
node("hpt", "HP", "shape=trapezoid;perimeter=trapezoidPerimeter;direction=north;rotation=-90;"
     "whiteSpace=wrap;html=1;fillColor=#aeb6bf;strokeColor=%s;fontStyle=1;fontSize=11" % INK,
     rect(46, 70, 7, 7))
node("ms", "MS", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4e6f1;strokeColor=%s;fontStyle=1;"
     "fontSize=10" % INK, rect(54.5, 71.5, 3.5, 4.5))
node("lpt", "LP", "shape=trapezoid;perimeter=trapezoidPerimeter;direction=north;rotation=-90;"
     "whiteSpace=wrap;html=1;fillColor=#aeb6bf;strokeColor=%s;fontStyle=1;fontSize=11" % INK,
     rect(59.5, 69, 9, 9))
node("gen", "G", "ellipse;whiteSpace=wrap;html=1;fillColor=#f9e79f;strokeColor=%s;fontStyle=1;"
     "fontSize=20" % INK, cen(75, 73.5, 6, 6))
node("grid", "GRID\n40.0 MWe\n(~35.6 charging)", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4efdf;"
     "strokeColor=%s;fontStyle=1;fontSize=10;fontColor=%s" % (C_ELEC, C_ELEC), rect(86, 70.5, 12, 6))

# ===================================================================== condenser + feedwater
node("cond", "Condenser  (E-1)\n7 kPa - 39 C - 82.6 MWth",
     "rounded=0;whiteSpace=wrap;html=1;fillColor=#d6eaf8;strokeColor=%s;fontStyle=1;fontSize=11" % INK,
     rect(56, 54, 16, 6))
node("sea", "SEAWATER ultimate heat sink\nBlack Sea (Sinop) - once-through\n"
     "2,065 kg/s (2.0 m3/s) - dT <= 10 K\nmultiport diffuser -> far-field <= 0.2 K",
     "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fillColor=#d4e6f1;"
     "strokeColor=#1f6fb2;fontStyle=1;fontSize=9;fontColor=#1f6fb2", rect(74, 52.5, 18, 8))
node("da", "FWH / Deaerator", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4efdf;strokeColor=%s;"
     "fontStyle=1;fontSize=11" % INK, rect(40, 42, 10, 6))
PUMP = "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=%s;fontStyle=1;fontSize=9"
node("cp", "CP", PUMP % C_FEED, cen(56, 49.5, 2.6, 2.6))
node("fp", "FP", PUMP % C_FEED, cen(36, 45, 2.6, 2.6))

# ===================================================================== TCES auxiliary
node("tces", "TCES AUXILIARY  (non-safety, outside nuclear island)",
     "rounded=0;html=1;fillColor=none;strokeColor=%s;dashed=1;dashPattern=8 5;verticalAlign=top;"
     "align=left;spacingLeft=6;spacingTop=3;fontSize=12;fontStyle=1;fontColor=%s" % (C_CHG, C_CHG),
     rect(78, 6, 62, 30))
node("ihx", "IHX  (E-3)\nisolation\nboundary", "rounded=0;whiteSpace=wrap;html=1;fillColor=#fdf2e9;"
     "strokeColor=%s;fontStyle=1;fontSize=10" % INK, rect(82, 27, 9, 8))
node("store", "THERMOCHEMICAL STORE  (TCS-1)\nammine NiCl2-SrCl2/NH3  735 t / 735 m3\n"
     "- or zeolite-13X  1000 t / 1538 m3 -\n200 MWh_th - loss-free - seasonal",
     "shape=cylinder3;boundedLbl=1;backgroundOutline=1;whiteSpace=wrap;html=1;fillColor=#a04000;"
     "strokeColor=%s;fontColor=#ffffff;fontStyle=1;fontSize=10" % INK, rect(98, 11, 18, 21))
node("dhhx", "DH HX\n(E-4)", "rounded=0;whiteSpace=wrap;html=1;fillColor=#fdebd0;strokeColor=%s;"
     "fontStyle=1;fontSize=10" % INK, rect(122, 20, 10, 10))
node("dh", "District heating\nnetwork  (DH-1)\n25 MWth peak", "rounded=0;whiteSpace=wrap;html=1;"
     "fillColor=#fef5e7;strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_DH, C_DH),
     rect(120, 8.5, 16, 8))

# ===================================================================== H2
node("el", "SOE electrolyser\n(solid-oxide O2-, ~800 C)  EL-1\n8 MWe - 37.55 kWh/kg (vs PEM 50)", "rounded=0;whiteSpace=wrap;html=1;"
     "fillColor=#ebdef0;strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_H2, C_H2),
     rect(96, 58, 18, 9))
node("h2", "H2 storage / export\n213 kg/h - 441 t/yr", "rounded=0;whiteSpace=wrap;html=1;"
     "fillColor=#f4ecf7;strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_H2, C_H2),
     rect(120, 58, 16, 9))

# ===================================================================== streams
stream("S1", "main steam  4.5 MPa - 296 C - 57.8 kg/s", C_STEAM, [(14.5, 68), (14.5, 78), (46, 78)], width=2.8)
stream("", "", C_STEAM, [(53, 73.5), (54.5, 73.5)], width=2.0)              # HP->MS
stream("", "", C_STEAM, [(58, 73.5), (59.5, 73.5)], width=2.0)             # MS->LP
stream("", "", INK, [(68.5, 73.5), (72, 73.5)], width=3.0)                  # shaft
stream("Sel", "40.0 MWe -> grid", C_ELEC, [(78, 73.5), (86, 73.5)])
stream("S4", "LP exhaust  x=0.892", C_STEAM, [(64, 69), (64, 60)])
stream("SW2", "outfall +10 K", "#1f6fb2", [(72, 57.5), (74, 57.5)])         # cond->sea (warm)
stream("SW1", "intake 8-25 C", "#1f6fb2", [(74, 55), (72, 55)], dashed=True)  # sea->cond (cold)
stream("S5", "", C_FEED, [(56, 54), (56, 51)])                             # cond->CP
stream("S6", "", C_FEED, [(56, 48), (56, 45), (50, 45)])                   # CP->FWH/DA
stream("S7", "feedwater -> OTSG  4.5 MPa", C_FEED, [(40, 45), (37.4, 45)]) # FWH->FP
stream("S7b", "", C_FEED, [(34.6, 45), (24, 45), (24, 40), (21, 40)])
# HP INTERMEDIATE-STAGE extraction (stage 14/24) -> IHX: a designed bleed (NOT inlet
# steam) = an extraction turbine like the FWH bleeds -> no turbine-life penalty.
stream("Sx", "HP stage-14/24 extraction  1.0 MPa (9 barg) - 180 C  -> TCES charge", C_STEAM,
       [(50, 70), (50, 63), (86, 63), (86, 35)], dashed=True)
# SOE steam = LP turbine extraction (deaerator stream); cogen bleed routed BY MODE to TCES or SOE.
stream("Sxs", "LP extraction -> SOE feed  0.15 MPa (deaerator stream)", C_STEAM,
       [(57, 71.5), (57, 61), (96, 61)], dashed=True)
# charge loop (closed) + return
stream("Tc", "charge loop  168 C (closed)", C_CHG, [(91, 31.5), (98, 31.5)])
stream("Tcr", "", C_CHG, [(98, 28.5), (91, 28.5)], dashed=True)
# discharge -> DH HX -> network
stream("Td", "discharge  150 C", C_DH, [(116, 25), (122, 25)])
stream("Tdh", "supply 90 C", C_DH, [(127, 20), (127, 16.5)])
stream("Tdr", "return 45 C  (133 kg/s)", C_DH, [(124, 12.5), (124, 19.9)], dashed=True)
# H2
stream("Sp", "off-peak power", C_ELEC, [(90, 73.5), (90, 67)])
stream("", "", C_ELEC, [(90, 64), (96, 64)], width=2.0)
stream("Sh", "H2", C_H2, [(114, 62.5), (120, 62.5)])

# ===================================================================== title + legend
node("title", "AEGIS-40 iPWR  -  Cogeneration PFD: single turbine + thermochemical store (district heat) + H2",
     "text;html=1;align=left;fontSize=20;fontStyle=1;fontColor=%s" % INK, rect(4, 81.5, 120, 3))
node("sub", "125 MWth -> 40.0 MWe (one tandem-compound turbine-generator)   -   co-products: "
     "district heat (TCES, 90/45 C) + H2   -   TCES is IHX-isolated, non-safety",
     "text;html=1;align=left;fontSize=12;fontColor=#555555", rect(4, 78.6, 130, 2.5))
LEG = [("primary coolant", C_PRIM), ("main / extraction steam", C_STEAM),
       ("feedwater / condensate", C_FEED), ("TCES charge loop (closed)", C_CHG),
       ("district heat water", C_DH), ("electricity", C_ELEC), ("hydrogen", C_H2)]
node("leg", "LEGEND", "text;html=1;align=left;fontStyle=1;fontSize=11", rect(4, 15.4, 12, 1.6))
for i, (t, c) in enumerate(LEG):
    lx = 4 + (i % 2) * 30; ly = 13.8 - (i // 2) * 1.8
    stream("lg%d" % i, "", c, [(lx, ly), (lx + 2.6, ly)], width=4)
    node("lgt%d" % i, t, "text;html=1;align=left;fontSize=10", rect(lx + 3.0, ly - 0.7, 26, 1.4))
node("tb", "Fig 8.9-3  -  Aegis-40 cogeneration (TCES district heat + SOE H2)\n"
     "single turbine - stage-14 HP extraction - IHX-isolated store - 90/45 C DH - SOE H2 (routed by mode)   -   NTS",
     "text;html=1;align=left;fontSize=10;fontStyle=1", rect(4, 3.0, 82, 3))

# ===================================================================== serialize
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))
parts = ['<mxfile host="app.diagrams.net" type="device">',
         '  <diagram id="aegis40cogen" name="Aegis-40 Cogeneration PFD">',
         '    <mxGraphModel dx="1422" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" '
         'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1760" pageHeight="1120" '
         'math="0" shadow="0">', '      <root>',
         '        <mxCell id="0" />', '        <mxCell id="1" parent="0" />']
for cid, value, style, x, y, w, h in cells:
    parts.append('        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                 % (cid, esc(value), style)
                 + '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
                 % (x, y, w, h))
for i, (eid, value, style, tp) in enumerate(edges):
    cid = eid if eid else "e%d" % i
    src = '<mxPoint x="%d" y="%d" as="sourcePoint"/>' % tp[0]
    tgt = '<mxPoint x="%d" y="%d" as="targetPoint"/>' % tp[-1]
    mids = "".join('<mxPoint x="%d" y="%d"/>' % p for p in tp[1:-1])
    arr = ('<Array as="points">%s</Array>' % mids) if mids else ""
    parts.append('        <mxCell id="%s" value="%s" style="%s" edge="1" parent="1">'
                 % (cid, esc(value), style)
                 + '<mxGeometry relative="1" as="geometry">%s%s%s</mxGeometry></mxCell>' % (src, tgt, arr))
parts += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>']
xml = "\n".join(parts)
ET.fromstring(xml)                                   # validate well-formedness
with open(OUT, "w", encoding="utf-8") as f:
    f.write(xml)
print("wrote", OUT)
print("  %d equipment cells, %d streams" % (len(cells), len(edges)))
