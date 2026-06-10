"""Emit an editable draw.io (diagrams.net) PFD of the Aegis-40 integrated plant.

This re-expresses the matplotlib figure `plant_pfd.py` as a hand-editable
draw.io file so the diagram can be polished manually in diagrams.net (free,
https://app.diagrams.net) using proper PFD conventions.

The layout is taken DIRECTLY from `plant_pfd.py` (same tuned, non-overlapping
coordinates) via the transform below, so the .drawio opens looking like the PNG.
Equipment uses built-in draw.io shapes (always render everywhere); the user can
swap any of them for fancier PID stencils from the shape panel. Streams are
numbered S1..Sn (data lives in stream-summary-table.md) and colour-coded by fluid.

Design intent (see Frick et al. INL/JOU-17-43134): the two-tank TES is a PARALLEL
bypass off the steam header upstream of the TCVs, NOT in series with the turbine.
The 40 MWe net is the TES-idle design point.

Output: docs/competition/cycle/aegis40_pfd.drawio   (open in diagrams.net)
Run:    py scripts/generate_pfd_drawio.py
"""

import os
import xml.etree.ElementTree as ET

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "cycle", "aegis40_pfd.drawio")

# ---- palette (matches plant_pfd.py) -----------------------------------------
C_PRIM = "#c0392b"; C_STEAM = "#e67e22"; C_FEED = "#2471a3"
C_HOT = "#8e2f1c";  C_COLD = "#138d75";  C_CW = "#5dade2"
C_ELEC = "#1e8449"; C_H2 = "#7d3c98";    C_DH = "#b9770e"
INK = "#1b2631"

# ---- coordinate transform: plant_pfd (x in 0..140, y in 0..86, y UP) --------
# -> draw.io pixels (origin top-left, y DOWN).  s px per plant-unit.
S = 12
def px(x):            return round(x * S)
def py(y):            return round((86 - y) * S)     # flip y
def rect(x, y, w, h): return px(x), py(y + h), round(w * S), round(h * S)  # bottom-left+h
def cen(cx, cy, w, h):                                # centre-based -> top-left
    return px(cx) - round(w * S) / 2, py(cy) - round(h * S) / 2, round(w * S), round(h * S)

cells = []  # (id, value, style, x, y, w, h)  for vertices
edges = []  # (id, value, style, [(x,y)...], fontcolor)


def node(cid, value, style, geom):
    x, y, w, h = geom
    cells.append((cid, value, style, x, y, w, h))


def stream(eid, value, color, pts, width=2.4, dashed=False, fcol=None):
    ls = (";dashed=1;dashPattern=8 6" if dashed else "")
    fc = fcol or color
    style = ("endArrow=block;endFill=1;html=1;rounded=0;"
             "strokeColor=%s;strokeWidth=%s%s;"
             "fontSize=11;fontStyle=1;fontColor=%s;labelBackgroundColor=#ffffff"
             % (color, width, ls, fc))
    tp = [(px(x), py(y)) for x, y in pts]
    edges.append((eid, value, style, tp))


# ============================================================================
# EQUIPMENT
# ============================================================================
# --- Integral RPV (background) + internals ----------------------------------
node("rpv", "Integral RPV  (R-1)\nnatural circulation\n12.8 MPa - 305/265 C",
     "rounded=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=#fbeee6;strokeColor=%s;"
     "strokeWidth=2.5;verticalAlign=bottom;fontSize=11;fontStyle=2;fontColor=%s;spacingBottom=4"
     % (C_PRIM, C_PRIM), rect(6, 26, 14, 40))
node("core", "Core\n125 MWth", "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5b7b1;"
     "strokeColor=%s;fontStyle=1;fontSize=11" % INK, rect(8, 28, 10, 6))
node("otsg", "helical-coil\nOTSG", "rounded=0;whiteSpace=wrap;html=1;fillColor=#fadbd8;"
     "strokeColor=%s;fontSize=10;fontStyle=1" % INK, rect(8, 39, 10, 10))
node("pzr", "self-\npressurizer", "rounded=1;arcSize=40;whiteSpace=wrap;html=1;"
     "fillColor=#f6ddcc;strokeColor=%s;fontSize=9" % INK, rect(9.5, 57, 7, 6))

# --- turbine string ---------------------------------------------------------
node("hpt", "HP\nturbine", "shape=trapezoid;perimeter=trapezoidPerimeter;direction=north;"
     "rotation=-90;whiteSpace=wrap;html=1;fillColor=#aeb6bf;strokeColor=%s;fontStyle=1;"
     "fontSize=11" % INK, rect(60, 69, 8, 7))
node("ms", "MS", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4e6f1;strokeColor=%s;"
     "fontStyle=1;fontSize=11" % INK, rect(69, 70.5, 4, 5))
node("lpt", "LP\nturbine", "shape=trapezoid;perimeter=trapezoidPerimeter;direction=north;"
     "rotation=-90;whiteSpace=wrap;html=1;fillColor=#aeb6bf;strokeColor=%s;fontStyle=1;"
     "fontSize=11" % INK, rect(74, 68, 10, 9))
node("gen", "G", "ellipse;whiteSpace=wrap;html=1;fillColor=#f9e79f;strokeColor=%s;"
     "fontStyle=1;fontSize=20" % INK, cen(90.5, 72.5, 6, 6))
node("grid", "GRID\n40 MWe", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4efdf;"
     "strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_ELEC, C_ELEC),
     rect(106, 70, 10, 5))

# --- condenser + cooling tower + feed train ---------------------------------
node("cond", "Condenser  (E-1)\n7 kPa - 39 C - Q=82.2 MWth",
     "rounded=0;whiteSpace=wrap;html=1;fillColor=#d6eaf8;strokeColor=%s;fontStyle=1;fontSize=11"
     % INK, rect(71, 54, 17, 6))
node("ct", "Cooling Tower\n(mech. draft)  CT-1",
     "shape=trapezoid;perimeter=trapezoidPerimeter;direction=north;whiteSpace=wrap;html=1;"
     "fillColor=#dfe3e6;strokeColor=%s;fontStyle=1;fontSize=11" % INK, rect(116, 38, 16, 24))
node("da", "Deaerator\nFWH-2", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4efdf;"
     "strokeColor=%s;fontStyle=1;fontSize=11" % INK, rect(60, 41, 10, 6))
node("fwh1", "FWH-1\n(HP heater)", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d4efdf;"
     "strokeColor=%s;fontStyle=1;fontSize=11" % INK, rect(42, 41, 10, 6))

# --- pumps ------------------------------------------------------------------
PUMP = ("ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=%s;"
        "fontStyle=1;fontSize=9")
node("cp", "CP",  PUMP % C_FEED, cen(79, 47, 3, 3))
node("bp", "BP",  PUMP % C_FEED, cen(56, 44, 3, 3))
node("fp", "FP",  PUMP % C_FEED, cen(38, 44, 3, 3))
node("cwp", "CWP", PUMP % C_CW,  cen(101, 42, 3, 3))
node("pc", "P-C", PUMP % C_COLD, cen(42, 10, 3, 3))
node("ph", "P-H", PUMP % C_HOT,  cen(69, 20, 3, 3))

# --- TES (two-tank sensible heat) -------------------------------------------
node("tesbox", "Thermal Energy Storage  -  two-tank sensible heat (Therminol-66)  -  PARALLEL bypass, not in series",
     "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=%s;dashed=1;dashPattern=10 6;"
     "verticalAlign=top;fontSize=11;fontStyle=1;fontColor=%s;spacingTop=2;align=left;spacingLeft=6"
     % (C_HOT, C_HOT), rect(28, 7, 74, 23))
node("ihx", "IHX\nE-2", "rounded=0;whiteSpace=wrap;html=1;fillColor=#d6eaf8;"
     "strokeColor=%s;fontSize=10;fontStyle=1" % INK, rect(30, 15, 10, 10))
TANK = ("shape=cylinder3;boundedLbl=1;backgroundOutline=1;whiteSpace=wrap;html=1;"
        "fillColor=%s;strokeColor=%s;fontColor=#ffffff;fontStyle=1;fontSize=10")
node("tkc", "Cold\n205 C\nTK-C", TANK % (C_COLD, INK), rect(45, 12, 8, 13))
node("tkh", "Hot\n260 C\nTK-H", TANK % (C_HOT, INK), rect(58, 12, 8, 13))
node("boiler", "TES\ndischarge\nboiler  E-3", "rounded=0;whiteSpace=wrap;html=1;"
     "fillColor=#fcf3cf;strokeColor=%s;fontStyle=1;fontSize=10" % INK, rect(72, 14, 10, 10))
node("dh", "District\nheating", "rounded=0;whiteSpace=wrap;html=1;fillColor=#fdf2e0;"
     "strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_DH, C_DH), rect(88, 14, 11, 8))

# --- SOE hydrogen co-generation ---------------------------------------------
node("soe", "SOE electrolyser\n(solid-oxide)  SOE-1", "rounded=0;whiteSpace=wrap;html=1;"
     "fillColor=#ebdef0;strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_H2, C_H2),
     rect(98, 63, 16, 10))
node("h2", "H2\nstorage", "rounded=0;whiteSpace=wrap;html=1;fillColor=#f4ecf7;"
     "strokeColor=%s;fontStyle=1;fontSize=11;fontColor=%s" % (C_H2, C_H2), rect(119, 64, 11, 8))

# --- valves (bowtie = two triangles) ----------------------------------------
def valve(idb, cx, cy, tag, color):
    h = 1.1
    node(idb + "L", "", "triangle;direction=east;html=1;fillColor=#ffffff;strokeColor=%s"
         % color, cen(cx - h / 2, cy, h, 2 * h))
    node(idb + "R", "", "triangle;direction=west;html=1;fillColor=#ffffff;strokeColor=%s"
         % color, cen(cx + h / 2, cy, h, 2 * h))
    node(idb + "T", tag, "text;html=1;align=center;fontSize=9;fontColor=#566573;fontStyle=1",
         cen(cx, cy + 2.4, 6, 1.5))

valve("tcv", 44, 73, "TCV", C_STEAM)
valve("tbv", 33, 70.5, "TBV x4", C_STEAM)

# ============================================================================
# STREAMS  (numbered process streams + named utility/TES lines)
# ============================================================================
# main process steam & power
stream("S1", "S1", C_STEAM, [(13, 66), (13, 73), (59, 73)], width=2.8)
stream("S2", "S2", C_STEAM, [(64, 69), (64, 49.5), (47, 49.5), (47, 47)], dashed=True)  # HP extr -> FWH1
stream("S3", "S3", C_STEAM, [(77, 68), (77, 49.5), (65, 49.5), (65, 47)], dashed=True)  # LP extr -> DA
stream("S4", "S4  x=0.892", C_STEAM, [(79, 68), (79, 60)])                              # LP exhaust -> cond
stream("",   "",   C_STEAM, [(68, 72.5), (69, 72.5)], width=2.0)                        # HP->MS
stream("",   "",   C_STEAM, [(73, 72.5), (74, 72.5)], width=2.0)                        # MS->LP
stream("Sel", "to grid  40 MWe", C_ELEC, [(93.5, 72.5), (106, 72.5)])
# condensate / feedwater
stream("S5", "S5", C_FEED, [(79, 54), (79, 45.5)])                  # cond -> CP
stream("",   "",   C_FEED, [(79, 44), (70, 44)])                    # CP -> DA
stream("S6", "S6", C_FEED, [(60, 44), (52, 44)])                    # DA -> FWH1
stream("S7", "S7  feedwater 4.8 MPa", C_FEED, [(42, 44), (24, 44), (24, 38), (20, 38)])  # FWH1 -> OTSG
# cooling water
stream("CWa", "warm", C_CW, [(88, 57), (116, 57)])
stream("CWb", "cooled", C_CW, [(116, 42), (90, 42), (90, 55), (88, 55)])
# primary loop (in-vessel, indicative)
stream("P1", "primary", C_PRIM, [(13, 34), (13, 39)], width=2.0)
stream("P2", "", C_PRIM, [(13, 49), (13, 57)], width=2.0)
# TES charging (parallel bypass)
stream("S8", "S8  <=45% steam  ~26 kg/s", C_STEAM, [(33, 73), (33, 25)], dashed=True)
stream("Tc1", "charge", C_COLD, [(48, 12), (48, 10), (35, 10), (35, 15)])   # cold -> IHX
stream("Tc2", "", C_HOT, [(35, 25), (35, 27.5), (61, 27.5), (61, 25)])      # IHX -> hot
stream("Td1", "discharge", C_HOT, [(66, 20), (72, 20)])                     # hot -> boiler
stream("Td2", "", C_COLD, [(78, 14), (78, 9), (49, 9), (49, 12)])           # boiler -> cold
stream("Tdr", "to condenser", C_FEED, [(40, 18), (47, 18)], width=1.6, dashed=True)
stream("Tps", "process steam", C_STEAM, [(77, 24), (77, 31)], dashed=True)
stream("Tdh", "", C_DH, [(82, 18), (88, 18)])
# hydrogen co-gen
stream("Sh1", "steam tap -> HT electrolysis", C_STEAM, [(50, 73), (50, 76.2), (106, 76.2), (106, 73)],
       width=1.6, dashed=True)
stream("Sh2", "off-peak power", C_ELEC, [(100, 72.5), (100, 73)], width=2.0)
stream("Sh3", "H2", C_H2, [(114, 68), (119, 68)])

# ============================================================================
# title + legend (as text nodes)
# ============================================================================
node("title", "AEGIS-40 iPWR  -  Integrated Plant Process Flow Diagram",
     "text;html=1;align=left;fontSize=22;fontStyle=1;fontColor=%s" % INK, rect(4, 81, 90, 3))
node("sub", "125 MWth  ->  40.0 MWe net  (eta = 32.0 %)   -   secondary Rankine cycle  +  "
     "two-tank thermal energy storage  +  SOE hydrogen co-generation",
     "text;html=1;align=left;fontSize=12;fontColor=#555555", rect(4, 78.3, 110, 2.5))

LEG = [("primary coolant", C_PRIM), ("main / extraction steam", C_STEAM),
       ("condensate / feedwater", C_FEED), ("hot thermal fluid (Therminol-66)", C_HOT),
       ("cold thermal fluid", C_COLD), ("cooling water", C_CW),
       ("electricity", C_ELEC), ("hydrogen", C_H2), ("district heat", C_DH)]
node("leg", "LEGEND", "text;html=1;align=left;fontStyle=1;fontSize=11", rect(4, 6.4, 12, 1.6))
for i, (t, c) in enumerate(LEG):
    lx = 4 + (i % 3) * 30
    ly = 5.0 - (i // 3) * 1.7
    stream("lg%d" % i, "", c, [(lx, ly), (lx + 2.6, ly)], width=4)
    node("lgt%d" % i, t, "text;html=1;align=left;fontSize=10", rect(lx + 3.0, ly - 0.7, 26, 1.4))

# title block
node("tb", "", "rounded=0;html=1;fillColor=none;strokeColor=%s" % INK, rect(110, 2.3, 27.5, 7.7))
node("tb1", "Aegis-40 iPWR - Balance of Plant\nIntegrated PFD",
     "text;html=1;align=left;fontStyle=1;fontSize=10", rect(111, 7.0, 26, 2.5))
node("tb2", "Drawing\nPFD-8.9-001", "text;html=1;align=left;fontSize=10", rect(111, 3.0, 12, 3))
node("tb3", "Scale\nNTS - Fig 8.9-1", "text;html=1;align=left;fontSize=10", rect(124, 3.0, 13, 3))

# ============================================================================
# serialize to draw.io XML
# ============================================================================
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

parts = ['<mxfile host="app.diagrams.net" type="device">',
         '  <diagram id="aegis40pfd" name="Aegis-40 Plant PFD">',
         '    <mxGraphModel dx="1422" dy="800" grid="1" gridSize="10" guides="1" '
         'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
         'pageWidth="1700" pageHeight="1120" math="0" shadow="0">',
         '      <root>',
         '        <mxCell id="0" />',
         '        <mxCell id="1" parent="0" />']

for cid, value, style, x, y, w, h in cells:
    parts.append(
        '        <mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
        % (cid, esc(value), style)
        + '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
        % (x, y, w, h))

for i, (eid, value, style, tp) in enumerate(edges):
    cid = eid if eid else "e%d" % i
    src = '<mxPoint x="%d" y="%d" as="sourcePoint"/>' % tp[0]
    tgt = '<mxPoint x="%d" y="%d" as="targetPoint"/>' % tp[-1]
    mids = "".join('<mxPoint x="%d" y="%d"/>' % p for p in tp[1:-1])
    arr = ('<Array as="points">%s</Array>' % mids) if mids else ""
    parts.append(
        '        <mxCell id="%s" value="%s" style="%s" edge="1" parent="1">' % (cid, esc(value), style)
        + '<mxGeometry relative="1" as="geometry">%s%s%s</mxGeometry></mxCell>' % (src, tgt, arr))

parts += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>']
xml = "\n".join(parts)

# validate well-formedness before writing
ET.fromstring(xml)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(xml)
print("wrote", OUT)
print("  %d equipment cells, %d streams" % (len(cells), len(edges)))
