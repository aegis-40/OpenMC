#!/usr/bin/env python
"""Insert a §9.2b geometry-RENDER cell into the rev7 shielding notebook.

Problem: the notebook's only geometry plots (§3) render build_core() — they do
NOT contain the shield, which lives inside build_shielded_model() (§9). And §9
itself only plots dose-vs-radius (a line chart). So no plot cell ever drew the
shield. This adds an OpenMC material render of the FULL shielded model (out to
R_OUT) so the circular radial layers are visible. Geometry-only — no transport
run needed. Mirrors §3's plot_core_geometry API (export_to_xml + plot_geometry).

Inserted between cell 39 (build def) and cell 40 (run). Verified: new cell
compiles; JSON re-parses.
"""
import ast, json

NB = r'D:\projects\teknofest-2026-aegis-40-ipwr\openmc_model\rev7_shielding\aegis40_3d_core_shielding_rev7.ipynb'
nb = json.load(open(NB, encoding='utf-8'))

# sanity: cell 39 is the build def, cell 40 is the run
assert 'def build_shielded_model' in ''.join(nb['cells'][39]['source']), "cell 39 not the build def"
assert '9.3 Run the shielded model' in ''.join(nb['cells'][40]['source']), "cell 40 not the run cell"

SRC = '''# ── 9.2b Geometry RENDER of the shielded model (shows the circular layers) ──
# Geometry-only: NO transport run needed. The §3 plots render build_core() and
# do not include the shield; this renders the FULL shielded model out to R_OUT.
def plot_shield_geometry():
    sh_model, gi = build_shielded_model(stats=STAT_SHIELD)
    d = _run_dir("00_shield_geometry_plot")
    R = gi["R_OUT"]; ZH = gi["Z_HALF"]; ZBC = ZH + 80.0

    palette = {
        "core_barrel":        (120, 120, 120),
        "downcomer_water":    (150, 190, 255),
        "SA508_RPV":          (60, 60, 60),
        "cavity_air":         (245, 245, 245),
        "thermal_shield":     (175, 175, 175),
        "borated_PE":         (110, 190, 115),
        "magnetite_concrete": (185, 150, 90),
        "ordinary_concrete":  (210, 190, 160),
        "H2O_active":         (120, 170, 255),
        "H2O_reflector":      (190, 220, 255),
        "Gd_fuel":            (65, 105, 225),
        "Er_fuel":            (0, 206, 209),
    }
    cmap = {m: palette[m.name] for m in sh_model.materials if m.name in palette}
    for m in sh_model.materials:                       # any fuel -> red block
        if m not in cmap and m.name.startswith("UO2"):
            cmap[m] = (220, 70, 60)

    p_xy = openmc.Plot(); p_xy.filename = "shield_xy"; p_xy.basis = "xy"
    p_xy.origin = (0.0, 0.0, 0.0); p_xy.width = (2*R + 30, 2*R + 30)
    p_xy.pixels = (1400, 1400); p_xy.color_by = "material"; p_xy.colors = cmap

    p_xz = openmc.Plot(); p_xz.filename = "shield_xz"; p_xz.basis = "xz"
    p_xz.origin = (0.0, 0.0, 0.0); p_xz.width = (2*R + 30, 2*ZBC + 30)
    p_xz.pixels = (1200, int(1200 * ZBC / R)); p_xz.color_by = "material"; p_xz.colors = cmap

    sh_model.plots = openmc.Plots([p_xy, p_xz])
    sh_model.export_to_xml(str(d))
    old = Path.cwd(); os.chdir(d)
    try:
        openmc.plot_geometry(output=False)
    finally:
        os.chdir(old)

    for tag, w, h in (("xy", R, R), ("xz", R, ZBC)):
        img = None
        for ext in ("png", "ppm"):
            cand = d / f"shield_{tag}.{ext}"
            if cand.is_file(): img = cand; break
        if img is None:
            print(f"   render {tag}: no image produced"); continue
        arr = plt.imread(str(img))
        fig, ax = plt.subplots(figsize=(8, 8 * h / w))
        ax.imshow(arr, extent=[-w, w, -h, h])
        ax.set_xlabel("x (cm)"); ax.set_ylabel("y (cm)" if tag == "xy" else "z (cm)")
        ax.set_title(f"Aegis-40 \\u2014 shielded model, radial layers ({tag})", fontsize=11)
        out = PLOTS / f"shield_geometry_{tag}.png"
        fig.savefig(out, dpi=200, bbox_inches="tight"); print("saved:", out)
        plt.show()

plot_shield_geometry()
'''

ast.parse(SRC)   # compile-check before inserting
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": SRC.splitlines(keepends=True),
}
nb['cells'].insert(40, new_cell)

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(NB, encoding='utf-8'))
print("OK: inserted §9.2b shield geometry-render cell at index 40 (run cell -> 41).")
print("    Run it after §9.1/§9.2 — no transport needed; writes shield_geometry_xy/xz.png")
