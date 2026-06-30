"""Generate CAD reference figures + coordinate tables for the Creo 3D model.

Parses the as-run OpenMC geometry (openmc_model/sample_inputs/geometry.xml) and
emits, for each of the three fuel-assembly recipes (r0=centre, r1=inner ring,
r2=outer ring) and the 21-FA core map:

  * a coordinate CSV  (col, row, x_mm, y_mm, type, enrichment)  -> drive Creo patterns
  * a colour-coded reference PNG                                -> "this is what it looks like"

Pure-Python + matplotlib, runs on Windows (no OpenMC/WSL).  All geometry is read
straight from the locked model, so the picture matches the physics of record.

Output dir: docs/competition/cad/
"""

from __future__ import annotations

import csv
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEOM = os.path.join(ROOT, "openmc_model", "sample_inputs", "geometry.xml")
OUT = os.path.join(ROOT, "docs", "competition", "cad")
os.makedirs(OUT, exist_ok=True)

# ---- colour scheme (also the legend) ---------------------------------------
COLOURS = {
    "plain_4.4": "#bcd4e6",   # light blue  - low-enrichment edge pins
    "plain_4.7": "#5b9bd5",   # mid blue
    "plain_5.0": "#1f4e79",   # dark blue   - high-enrichment central pins
    "Gd":        "#c0392b",   # red         - Gd2O3 burnable-absorber pins
    "Er":        "#27ae60",   # green       - Er2O3 pins
    "guide":     "#ffffff",   # white/hollow- guide / instrument tubes
}
LABELS = {
    "plain_4.4": "Fuel 4.4 wt%",
    "plain_4.7": "Fuel 4.7 wt%",
    "plain_5.0": "Fuel 4.95 wt%",
    "Gd":        "Gd2O3 pin (8 wt%)",
    "Er":        "Er2O3 pin (0.5 wt%)",
    "guide":     "Guide / instr. tube",
}

# FA recipe -> (pin-lattice id, core-cell universe, human name)
FA_RECIPES = [
    ("r0", 485, 487, "Centre FA (x1)"),
    ("r1", 495, 497, "Inner-ring FA (x8)"),
    ("r2", 505, 507, "Outer-ring FA (x12)"),
]


def parse_geometry(path):
    tree = ET.parse(path)
    g = tree.getroot()

    # universe -> classification, by inspecting its named fuel cell
    univ_type = {}
    univ_has_cell = defaultdict(bool)
    for cell in g.findall("cell"):
        u = cell.get("universe")
        univ_has_cell[u] = True
        name = cell.get("name", "")
        if name.endswith("Gd_pin_fuel"):
            univ_type[u] = "Gd"
        elif name.endswith("Er_pin_fuel"):
            univ_type[u] = "Er"
        elif "_plain_" in name and name.endswith("_fuel"):
            enr = name.split("_plain_")[1].split("_")[0]  # "4.4" / "4.7" / "5.0"
            univ_type[u] = f"plain_{enr}"
    # any universe used in a pin grid but not classified == guide/water tube
    lattices = {lat.get("id"): lat for lat in g.findall("lattice")}
    return g, univ_type, lattices


def lattice_map(lat, univ_type):
    pitch = float(lat.find("pitch").text.split()[0])
    ll = float(lat.find("lower_left").text.split()[0])
    dim = int(lat.find("dimension").text.split()[0])
    rows = [r.split() for r in lat.find("universes").text.strip().splitlines()]
    cells = []  # (col, row, x_cm, y_cm, type)
    # OpenMC lists rows top (high y) -> bottom; row index 0 = top
    for jr, row in enumerate(rows):
        y = ll + (dim - 0.5 - jr) * pitch
        for ic, u in enumerate(row):
            x = ll + (ic + 0.5) * pitch
            typ = univ_type.get(u, "guide")
            cells.append((ic, dim - 1 - jr, x, y, typ))
    return pitch, dim, cells


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def draw_assembly(ax, cells, pitch, title):
    r = pitch * 10 * 0.40  # pin radius in mm-ish display units
    for (_, _, x_cm, y_cm, typ) in cells:
        x, y = x_cm * 10, y_cm * 10
        if typ == "guide":
            ax.add_patch(Rectangle((x - r, y - r), 2 * r, 2 * r,
                                   facecolor="white", edgecolor="#888", lw=0.6))
        else:
            ax.add_patch(Circle((x, y), r, facecolor=COLOURS[typ],
                                 edgecolor="#333", lw=0.3))
    span = pitch * 10 * 9
    ax.set_xlim(-span, span)
    ax.set_ylim(-span, span)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])


def main():
    g, univ_type, lattices = parse_geometry(GEOM)

    # ---- per-FA: CSV + counts, collect for the figure --------------------
    fa_cells = {}
    counts = {}
    for tag, lat_id, _core_u, name in FA_RECIPES:
        pitch, dim, cells = lattice_map(lattices[str(lat_id)], univ_type)
        fa_cells[tag] = (pitch, cells, name)
        c = defaultdict(int)
        for (_, _, _, _, typ) in cells:
            c[typ] += 1
        counts[tag] = c
        rows = [(ic, jr, round(x * 10, 3), round(y * 10, 3), typ,
                 typ.split("_")[1] if typ.startswith("plain") else "")
                for (ic, jr, x, y, typ) in cells]
        write_csv(os.path.join(OUT, f"pinmap_{tag}.csv"),
                  ["col", "row", "x_mm", "y_mm", "type", "enrichment_wt%"], rows)

    # ---- assembly figure (3 recipes side by side) ------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6))
    for ax, (tag, lat_id, _u, name) in zip(axes, FA_RECIPES):
        pitch, cells, _ = fa_cells[tag]
        c = counts[tag]
        sub = f"{name}\nGd {c['Gd']}  |  Er {c['Er']}  |  guide {c['guide']}"
        draw_assembly(ax, cells, pitch, sub)
    handles = [Line2D([0], [0], marker="o", color="w", label=LABELS[k],
                      markerfacecolor=COLOURS[k], markeredgecolor="#333", markersize=11)
               for k in ["plain_4.4", "plain_4.7", "plain_5.0", "Gd", "Er"]]
    handles.append(Line2D([0], [0], marker="s", color="w", label=LABELS["guide"],
                          markerfacecolor="white", markeredgecolor="#888", markersize=11))
    fig.legend(handles=handles, loc="lower center", ncol=6, fontsize=9,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Aegis-40  17x17 fuel-assembly recipes  (pin pitch 12.623 mm, "
                 "active 2000 mm)", fontsize=12)
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    fig.savefig(os.path.join(OUT, "fa_pinmaps.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- core map (5x5 minus corners = 21 FA) ----------------------------
    core = lattices["529"]
    pitch_c = float(core.find("pitch").text.split()[0])
    ll_c = float(core.find("lower_left").text.split()[0])
    dim_c = int(core.find("dimension").text.split()[0])
    rows_c = [r.split() for r in core.find("universes").text.strip().splitlines()]
    u2tag = {str(u): tag for tag, _l, u, _n in FA_RECIPES}
    ring_colour = {"r0": "#1f4e79", "r1": "#5b9bd5", "r2": "#bcd4e6"}
    core_rows = []
    fig2, ax2 = plt.subplots(figsize=(6.4, 6.4))
    half = pitch_c * 10 / 2
    for jr, row in enumerate(rows_c):
        y = ll_c + (dim_c - 0.5 - jr) * pitch_c
        for ic, u in enumerate(row):
            x = ll_c + (ic + 0.5) * pitch_c
            tag = u2tag.get(u)
            if tag is None:
                continue  # corner water -> no FA
            xm, ym = x * 10, y * 10
            ax2.add_patch(Rectangle((xm - half, ym - half), 2 * half, 2 * half,
                                    facecolor=ring_colour[tag], edgecolor="#222", lw=1.2))
            ax2.text(xm, ym, tag, ha="center", va="center",
                     color="white" if tag != "r2" else "#1f4e79", fontsize=10, weight="bold")
            core_rows.append((ic, dim_c - 1 - jr, round(xm, 2), round(ym, 2), tag))
    lim = pitch_c * 10 * 2.6
    ax2.set_xlim(-lim, lim)
    ax2.set_ylim(-lim, lim)
    ax2.set_aspect("equal")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title("Aegis-40 core loading map  -  21 FA (5x5 lattice, corners = reflector)\n"
                  "assembly pitch 216.04 mm   |   r0 centre / r1 inner / r2 outer ring",
                  fontsize=10)
    leg = [Line2D([0], [0], marker="s", color="w", markerfacecolor=ring_colour[k],
                  markeredgecolor="#222", markersize=13,
                  label={"r0": "Centre (Gd 48)", "r1": "Inner ring (Gd 40)",
                         "r2": "Outer ring (Gd 24)"}[k]) for k in ["r0", "r1", "r2"]]
    ax2.legend(handles=leg, loc="upper right", fontsize=8, frameon=True)
    fig2.tight_layout()
    fig2.savefig(os.path.join(OUT, "core_map.png"), dpi=150, bbox_inches="tight")
    plt.close(fig2)
    write_csv(os.path.join(OUT, "core_map.csv"),
              ["col", "row", "x_mm", "y_mm", "ring"], core_rows)

    # ---- console summary -------------------------------------------------
    print("Wrote to", OUT)
    print("  figures : fa_pinmaps.png, core_map.png")
    print("  tables  : pinmap_r0.csv, pinmap_r1.csv, pinmap_r2.csv, core_map.csv")
    print()
    print("  FA pin counts (verify against 48/40/26 Gd, 16 Er):")
    for tag, _l, _u, name in FA_RECIPES:
        c = counts[tag]
        tot = sum(c.values())
        print(f"    {tag} {name:22s}  Gd={c['Gd']:3d}  Er={c['Er']:3d}  "
              f"guide={c['guide']:3d}  fuel={tot - c['Gd'] - c['Er'] - c['guide']:3d}  "
              f"total={tot}")
    print(f"  core: {len(core_rows)} fuel assemblies placed")


if __name__ == "__main__":
    main()
