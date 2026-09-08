#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NuScale - Natural-circulation validation against NuScale (and operating point).
=============================================================================

Overlays the natcirc.py mass-flow-vs-power curve on published NuScale data
(ASTEC model, Mahmoudi et al., Frontiers Energy Res. 2022, Table 3) and prints
the deviation. Writes a dependency-free SVG plot for slides + a CSV.

NuScale reference (full-scale, 160 MWt, 12.8 MPa, 2.0 m core) -- same class as
NuScale, so a direct full-scale comparison (NOT the 1/3-scale OSU-MASLWR facility).

Run:  python3 tools/validate_natcirc.py
Out:  docs/natcirc_validation.svg , docs/natcirc_validation.csv
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from natcirc import Config, solve  # noqa: E402

# NuScale published natural-circ data: P[MW] -> (mdot kg/s, dT K)
# Source: Frontiers Energy Res. 10:1036142 (2022), ASTEC NuScale model, Table 3.
NUSCALE = {24: (271.8, 17.7), 80: (440.2, 37.7),
           120: (530.6, 47.0), 160: (600.1, 54.1)}
DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")


def our_curve(pmin=10.0, pmax=170.0, n=80):
    pts = []
    for i in range(n + 1):
        P = pmin + (pmax - pmin) * i / n
        c = Config(); c.P_th = P * 1e6
        r = solve(c)
        pts.append((P, r["mdot"], r["dT"]))
    return pts


def comparison_table():
    rows = []
    for P in sorted(NUSCALE):
        c = Config(); c.P_th = P * 1e6
        r = solve(c)
        mn, dtn = NUSCALE[P]
        rows.append((P, mn, r["mdot"], 100 * (r["mdot"] - mn) / mn, dtn, r["dT"]))
    return rows


# ----------------------------- tiny SVG plotter ----------------------------
def _lin(v, v0, v1, p0, p1):
    return p0 + (v - v0) * (p1 - p0) / (v1 - v0)


def write_svg(path, curve, op_point):
    W, H = 760, 520
    ml, mr, mt, mb = 80, 30, 50, 70
    x0, x1 = 0.0, 170.0           # power axis [MW]
    y0, y1 = 0.0, 650.0           # mdot axis [kg/s]
    px = lambda P: _lin(P, x0, x1, ml, W - mr)
    py = lambda M: _lin(M, y0, y1, H - mb, mt)
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'font-family="Helvetica,Arial,sans-serif">')
    s.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    # title
    s.append(f'<text x="{W/2}" y="26" font-size="18" font-weight="bold" '
             f'text-anchor="middle">NuScale natural circulation: mass flow vs power</text>')
    s.append(f'<text x="{W/2}" y="44" font-size="12" fill="#555" '
             f'text-anchor="middle">1-D natcirc model vs NuScale (ASTEC, Frontiers 2022)</text>')
    # gridlines + axes ticks
    for P in range(0, 171, 20):
        gx = px(P)
        s.append(f'<line x1="{gx:.1f}" y1="{mt}" x2="{gx:.1f}" y2="{H-mb}" '
                 f'stroke="#eee"/>')
        s.append(f'<text x="{gx:.1f}" y="{H-mb+18}" font-size="11" '
                 f'text-anchor="middle">{P}</text>')
    for M in range(0, 651, 100):
        gy = py(M)
        s.append(f'<line x1="{ml}" y1="{gy:.1f}" x2="{W-mr}" y2="{gy:.1f}" '
                 f'stroke="#eee"/>')
        s.append(f'<text x="{ml-8}" y="{gy+4:.1f}" font-size="11" '
                 f'text-anchor="end">{M}</text>')
    # axis frame
    s.append(f'<rect x="{ml}" y="{mt}" width="{W-mr-ml}" height="{H-mb-mt}" '
             f'fill="none" stroke="#333"/>')
    # axis labels
    s.append(f'<text x="{(ml+W-mr)/2}" y="{H-18}" font-size="13" '
             f'text-anchor="middle">Core thermal power  P [MW]</text>')
    s.append(f'<text x="22" y="{(mt+H-mb)/2}" font-size="13" text-anchor="middle" '
             f'transform="rotate(-90 22 {(mt+H-mb)/2})">Primary mass flow  ṁ [kg/s]</text>')
    # our curve
    d = " ".join(f"{'L' if i else 'M'}{px(P):.1f},{py(M):.1f}"
                 for i, (P, M, _) in enumerate(curve))
    s.append(f'<path d="{d}" fill="none" stroke="#1f6fb4" stroke-width="2.5"/>')
    # NuScale points
    for P, (M, _) in sorted(NUSCALE.items()):
        s.append(f'<circle cx="{px(P):.1f}" cy="{py(M):.1f}" r="5.5" '
                 f'fill="#d1462f" stroke="white" stroke-width="1.2"/>')
    # NuScale operating point
    P, M = op_point
    s.append(f'<circle cx="{px(P):.1f}" cy="{py(M):.1f}" r="6.5" '
             f'fill="none" stroke="#1f6fb4" stroke-width="2.5"/>')
    s.append(f'<text x="{px(P)+10:.1f}" y="{py(M)-8:.1f}" font-size="11" '
             f'fill="#1f6fb4">NuScale op. pt ({P:.0f} MW, {M:.0f} kg/s)</text>')
    # legend
    lx, ly = ml + 20, mt + 18
    s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" '
             f'stroke="#1f6fb4" stroke-width="2.5"/>')
    s.append(f'<text x="{lx+34}" y="{ly+4}" font-size="12">natcirc.py (this work)</text>')
    s.append(f'<circle cx="{lx+14}" cy="{ly+22}" r="5.5" fill="#d1462f"/>')
    s.append(f'<text x="{lx+34}" y="{ly+26}" font-size="12">NuScale (ASTEC, Frontiers 2022)</text>')
    s.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(s))


def main():
    rows = comparison_table()
    print("=" * 64)
    print(" NuScale natural-circ validation vs NuScale (ASTEC, Frontiers 2022)")
    print("=" * 64)
    print(f"{'P[MW]':>6} {'NuScale m':>10} {'our m':>8} {'dm%':>7}  "
          f"{'NuScale dT':>11} {'our dT':>7}")
    err = []
    for P, mn, mo, dm, dtn, dto in rows:
        err.append(abs(dm))
        print(f"{P:6d} {mn:10.1f} {mo:8.1f} {dm:+7.1f}  {dtn:11.1f} {dto:7.1f}")
    print("-" * 64)
    print(f" mean |dm| = {sum(err)/len(err):.1f}%   (no tuning; NuScale-class placeholders)")
    print("=" * 64)

    curve = our_curve()
    op = Config(); r = solve(op)
    os.makedirs(DOCS, exist_ok=True)
    svg = os.path.normpath(os.path.join(DOCS, "natcirc_validation.svg"))
    csv = os.path.normpath(os.path.join(DOCS, "natcirc_validation.csv"))
    write_svg(svg, curve, (op.P_th / 1e6, r["mdot"]))
    with open(csv, "w") as f:
        f.write("P_MW,mdot_ours_kgps,dT_ours_K,mdot_nuscale_kgps,dT_nuscale_K\n")
        for P, mo, dto in [(P, m, d) for P, m, d in curve]:
            nu = NUSCALE.get(int(round(P)))
            f.write(f"{P:.1f},{mo:.1f},{dto:.1f},"
                    f"{nu[0] if nu else ''},{nu[1] if nu else ''}\n")
    print(f" wrote {svg}")
    print(f" wrote {csv}")


if __name__ == "__main__":
    main()
