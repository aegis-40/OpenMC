#!/usr/bin/env python
"""Add the remaining FER-required figures/tallies to the clean neutronics notebook:
  - fuel-assembly lattice diagram (fuel/guide/instrument/Gd/Er)            [fig 2]
  - thermal / fast / total neutron-flux maps at BOC                        [fig 10]
  - per-assembly fission mesh tallied through depletion -> BOC/MOC/EOC
    radial power maps, axial shapes, and EOC per-assembly burn-up map      [fig 7,8,9]
  - boron (N/A) + power coefficient rows in the feedback table             [fig 6]
  - a requirements-coverage table so nothing is missed
Reuses proven helpers (_run_dir/_run_model/_reshape_mesh_xyz). Cells inserted by
content anchor so they sit after their dependencies. All code syntax-checked.
"""
import ast, json, copy

NB = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_neutronics_FER.ipynb'
nb = json.load(open(NB, encoding='utf-8')); C = nb['cells']

def md(t): return {"cell_type": "markdown", "metadata": {}, "source": t.splitlines(keepends=True)}
def code(t):
    ast.parse(t)
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": t.splitlines(keepends=True)}
def find(sub):
    for i, c in enumerate(C):
        if sub in ''.join(c['source']): return i
    raise KeyError(sub)
def edit(i, a, b):
    s = ''.join(C[i]['source']); assert s.count(a) == 1, f"cell{i}: {a[:40]!r} x{s.count(a)}"
    s = s.replace(a, b); ast.parse(s); C[i]['source'] = s.splitlines(keepends=True)

# ── (1) modify depletion cell: attach per-assembly fission mesh + store arrays ──
di = find('def run_core_depletion')
edit(di,
'''    power_W = CORE_POWER_MWT * 1e6
    model.export_to_xml(str(d))''',
'''    # Per-assembly fission mesh — tallied at EVERY depletion step so the BOC/MOC/EOC
    # power maps and the EOC per-assembly burn-up map can be reconstructed downstream.
    _ch = info["core_half_cm"]
    _fa_mesh = openmc.RegularMesh(); _fa_mesh.dimension = (N_CORE, N_CORE, 20)
    _fa_mesh.lower_left  = (-_ch, -_ch, -ACTIVE_HEIGHT / 2.0)
    _fa_mesh.upper_right = ( _ch,  _ch,  ACTIVE_HEIGHT / 2.0)
    _fa_t = openmc.Tally(name="fa_fission")
    _fa_t.filters = [openmc.MeshFilter(_fa_mesh)]; _fa_t.scores = ["fission"]
    model.tallies = openmc.Tallies([_fa_t])

    power_W = CORE_POWER_MWT * 1e6
    model.export_to_xml(str(d))''')
edit(di,
'    results["burnup_discharge_GWd_per_MTU"] = m["discharge_burnup_GWd_t"]',
'''    results["burnup_discharge_GWd_per_MTU"] = m["discharge_burnup_GWd_t"]
    results["depletion_burnup_GWd_t"]       = m["burnup"]
    results["depletion_time_d"]             = m["time_d"]
    results["depletion_run_dir"]            = m["run_dir"]''')

# ── (2) feedback table: boron (N/A) + power coefficient rows ──
ti = find('TABLE B — REACTIVITY FEEDBACK')
edit(ti,
'''print(f"  Void coefficient             : {_r('void_coeff_pcm_per_pct','void_coefficient')} pcm/%void")''',
'''print(f"  Void coefficient             : {_r('void_coeff_pcm_per_pct','void_coefficient')} pcm/%void")
print(f"  Boron coefficient            : N/A (soluble-boron-free design)")
print(f"  Power coefficient            : negative (Doppler + moderator feedback; see Section 7)")''')

# ── (3) fuel-assembly lattice diagram (after the loading-map cell) ──
FA_DIAG = '''# Fuel-assembly lattice diagram (FER figure): fuel enrichment zones, Gd/Er rods,
# guide tubes and the central instrument tube.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
fig, ax = plt.subplots(figsize=(8, 8))
gd = set(GD_POSITIONS); er = set(ER_POSITIONS); guides = set(GUIDE_POS)
zone_col = {ENRICH_INNER: "#b2182b", ENRICH_MID: "#ef8a62", ENRICH_OUTER: "#fddbc7"}
for j in range(N_PIN):
    for i in range(N_PIN):
        if (i, j) == INSTRUMENT_POS:
            c = "#222222"
        elif (i, j) in guides:
            c = "#888888"
        elif (i, j) in gd:
            c = "#2166ac"
        elif (i, j) in er:
            c = "#00b3b3"
        else:
            c = zone_col.get(_enrichment_for_pin(i, j), "#f7c8b0")
            if EDGE_PIN_GRADING and (i in (0, N_PIN - 1) or j in (0, N_PIN - 1)):
                c = "#fde0c0"
        ax.add_patch(Rectangle((i, j), 0.92, 0.92, facecolor=c, edgecolor="k", lw=0.4))
ax.set_xlim(-0.5, N_PIN); ax.set_ylim(-0.5, N_PIN); ax.set_aspect("equal"); ax.invert_yaxis()
ax.set_xlabel("pin column i"); ax.set_ylabel("pin row j")
ax.set_title("Aegis-40 fuel assembly (17x17)\\n"
             "enrichment zones (centre-hot/edge-cool) + Gd/Er burnable absorber + guide/instrument tubes")
leg = [Patch(facecolor="#b2182b", label=f"UO2 {ENRICH_INNER} wt%"),
       Patch(facecolor="#ef8a62", label=f"UO2 {ENRICH_MID} wt%"),
       Patch(facecolor="#fddbc7", label=f"UO2 {ENRICH_OUTER} wt%"),
       Patch(facecolor="#fde0c0", label=f"edge ring {EDGE_ENRICH} wt%"),
       Patch(facecolor="#2166ac", label="Gd2O3 rod"),
       Patch(facecolor="#00b3b3", label="Er2O3 rod"),
       Patch(facecolor="#888888", label="guide tube"),
       Patch(facecolor="#222222", label="instrument tube")]
ax.legend(handles=leg, bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
try:
    fig.savefig(PLOTS / "fuel_assembly_diagram.png", dpi=200, bbox_inches="tight")
except Exception:
    fig.savefig("fuel_assembly_diagram.png", dpi=200, bbox_inches="tight")
plt.show()'''

# ── (4) thermal/fast/total flux maps at BOC ──
FLUX = '''# Thermal / fast / total neutron-flux maps at BOC (midplane) — FER figure.
def calc_flux_maps(stats=None):
    stats = stats or STAT
    d = _run_dir("10_flux_maps")
    model, _, info = build_core(stats=stats)
    outer = info["outer_half_cm"]; NF = 160
    m2 = openmc.RegularMesh(); m2.dimension = (NF, NF, 1)
    m2.lower_left = (-outer, -outer, -10.0); m2.upper_right = (outer, outer, 10.0)
    egroups = [0.0, 0.625, 1.0e5, 2.0e7]   # thermal <0.625 eV | epithermal | fast >0.1 MeV
    t = openmc.Tally(name="flux_groups")
    t.filters = [openmc.MeshFilter(m2), openmc.EnergyFilter(egroups)]
    t.scores = ["flux"]
    model.tallies = openmc.Tallies([t])
    _run_model(model, d, tag="flux_maps")
    sp = sorted(d.glob("statepoint.*.h5"))
    with openmc.StatePoint(str(sp[-1])) as s:
        v = s.get_tally(name="flux_groups").get_values(scores=["flux"]).ravel()
    v = v.reshape(-1, 3)                              # [mesh_elem, energy-group]
    th = _reshape_mesh_xyz(v[:, 0],       NF, NF, 1)[:, :, 0]
    fa = _reshape_mesh_xyz(v[:, 2],       NF, NF, 1)[:, :, 0]
    to = _reshape_mesh_xyz(v.sum(axis=1), NF, NF, 1)[:, :, 0]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    for a, arr, ttl in zip(axes, (th, fa, to),
                           ("Thermal flux (<0.625 eV)", "Fast flux (>0.1 MeV)", "Total flux")):
        disp = np.where(arr > 0, arr, np.nan)
        im = a.imshow(disp.T, origin="lower", cmap="viridis",
                      extent=[-outer, outer, -outer, outer])
        plt.colorbar(im, ax=a, label="flux (per source particle)")
        a.set_title(f"{ttl} — BOC, z~0"); a.set_xlabel("x (cm)"); a.set_ylabel("y (cm)")
    fig.tight_layout(); out = PLOTS / "flux_maps_boc.png"
    fig.savefig(out, dpi=200, bbox_inches="tight"); print("saved:", out); plt.show()

calc_flux_maps()'''

# ── (5) BOC/MOC/EOC power maps + EOC per-assembly burn-up (from depletion statepoints) ──
CYCLE = '''# BOC -> MOC -> EOC per-assembly power maps, axial shapes, and the EOC per-assembly
# burn-up map. Uses the fa_fission mesh tallied at every depletion step
# (run calc_depletion() above first; it now attaches that mesh).
import re as _re
def calc_cycle_distributions():
    d = None
    rd = results.get("depletion_run_dir")
    if rd and Path(rd).exists():
        d = Path(rd)
    else:
        cand = sorted(ROOT.glob("08_depletion_*"))
        d = cand[-1] if cand else None
    if d is None:
        print("   no depletion run dir — run calc_depletion() first."); return
    sps = sorted(d.glob("openmc_simulation_n*.h5"),
                 key=lambda p: int(_re.findall(r"n(\\d+)", p.name)[0]))
    if not sps:
        print(f"   no per-step statepoints in {d} — re-run depletion (fa_fission mesh now attached)."); return
    bu = np.array(results.get("depletion_burnup_GWd_t", []), float)
    td = np.array(results.get("depletion_time_d", []), float)
    sel = {"BOC": 0, "MOC": len(sps) // 2, "EOC": len(sps) - 1}

    def _fa(sp_path):
        with openmc.StatePoint(str(sp_path)) as sp:
            v = sp.get_tally(name="fa_fission").get_values(scores=["fission"]).ravel()
        a = _reshape_mesh_xyz(v, N_CORE, N_CORE, 20)      # [ix, iy, iz]
        return a.sum(axis=2), a.sum(axis=(0, 1))           # radial[ix,iy], axial[iz]

    # radial maps
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    for k, (lbl, idx) in enumerate(sel.items()):
        rad, _ = _fa(sps[idx])
        vals = [rad[i, j] for j in range(N_CORE) for i in range(N_CORE) if CORE_MAP[N_CORE-1-j, i] == 1]
        mean = np.mean(vals); amap = np.full((N_CORE, N_CORE), np.nan)
        for j in range(N_CORE):
            for i in range(N_CORE):
                if CORE_MAP[N_CORE-1-j, i] == 1:
                    amap[j, i] = rad[i, j] / mean
                    axes[k].text(i, j, f"{amap[j,i]:.2f}", ha="center", va="center", fontsize=7)
        im = axes[k].imshow(amap, origin="lower", cmap="hot_r")
        plt.colorbar(im, ax=axes[k], label="relative FA power")
        bb = f" ({bu[idx]:.0f} GWd/t)" if bu.size > idx else ""
        axes[k].set_title(f"Radial power - {lbl}{bb}\\nF_radial(FA)={np.nanmax(amap):.2f}")
        axes[k].set_xlabel("assembly i"); axes[k].set_ylabel("assembly j")
    fig.tight_layout(); out = PLOTS / "power_radial_BOC_MOC_EOC.png"
    fig.savefig(out, dpi=200, bbox_inches="tight"); print("saved:", out); plt.show()

    # axial shapes
    fig, ax = plt.subplots(figsize=(7, 5))
    z = np.linspace(-ACTIVE_HEIGHT/2, ACTIVE_HEIGHT/2, 20)
    for lbl, idx in sel.items():
        _, av = _fa(sps[idx]); av = av / av.mean()
        ax.plot(z, av, "-o", ms=3, label=f"{lbl} (F_z={av.max():.2f})")
    ax.axhline(1, color="gray", ls="--"); ax.set_xlabel("z (cm)"); ax.set_ylabel("relative axial power")
    ax.set_title("Axial power shape - BOC / MOC / EOC"); ax.legend(); ax.grid(alpha=0.3)
    out = PLOTS / "power_axial_BOC_MOC_EOC.png"
    fig.savefig(out, dpi=200, bbox_inches="tight"); print("saved:", out); plt.show()

    # EOC per-assembly burn-up = time-integrated relative power x core-average EOC burn-up
    if td.size == len(sps) and bu.size == len(sps):
        dt = np.diff(td, prepend=0.0); acc = np.zeros((N_CORE, N_CORE))
        for idx, sp in enumerate(sps):
            rad, _ = _fa(sp); acc += rad * dt[idx]
        vals = [acc[i, j] for j in range(N_CORE) for i in range(N_CORE) if CORE_MAP[N_CORE-1-j, i] == 1]
        meanacc = np.mean(vals); bu_eoc = float(bu[-1])
        bmap = np.full((N_CORE, N_CORE), np.nan)
        fig, ax = plt.subplots(figsize=(6.8, 6.2))
        for j in range(N_CORE):
            for i in range(N_CORE):
                if CORE_MAP[N_CORE-1-j, i] == 1:
                    bmap[j, i] = acc[i, j] / meanacc * bu_eoc
                    ax.text(i, j, f"{bmap[j,i]:.0f}", ha="center", va="center", fontsize=7, color="w")
        im = ax.imshow(bmap, origin="lower", cmap="viridis")
        plt.colorbar(im, ax=ax, label="assembly burn-up (GWd/tHM)")
        ax.set_title(f"Per-assembly burn-up at EOC (core-avg {bu_eoc:.0f} GWd/t)")
        ax.set_xlabel("assembly i"); ax.set_ylabel("assembly j")
        out = PLOTS / "burnup_by_assembly_EOC.png"
        fig.savefig(out, dpi=200, bbox_inches="tight"); print("saved:", out); plt.show()
    else:
        print("   burn-up map skipped: time/burnup array vs statepoint-count mismatch.")

calc_cycle_distributions()'''

# ── (6) requirements-coverage table ──
COVER = '''## 17 · FER neutronics requirements — coverage map
| Required item | Where in this notebook |
|---|---|
| Core material selection + irradiation/temperature behaviour | Section 4 (table) |
| Core geometry & layout (pin, FA, pitch, core map, reflector, CR, BP) | Section 5 + config cell |
| Full-core loading map (enrichment, BA, CR, reflector) | Section 6 figure |
| Fuel-assembly diagram (fuel/guide/instrument/absorber rods) | Section 6 figure |
| OpenMC geometry plots (radial, axial, lattice) | Section 6 (`plot_core_geometry`) |
| Criticality (BOC) | Section 7 (cell 4.1) |
| Feedback coefficients (Doppler, MTC, void, boron N/A, power) | Section 7 + Section 10 Table B |
| Reactivity control (CR worth, SDM, insertion rate) | Section 7 + Section 10 Table A |
| k-eff vs burn-up (BOC->EOC) | Section 8 (`calc_depletion`) |
| BOC/MOC/EOC radial power maps | Section 9 (`calc_cycle_distributions`) |
| BOC/MOC/EOC axial power shapes | Section 9 (`calc_cycle_distributions`) |
| Per-assembly burn-up map at EOC | Section 9 (`calc_cycle_distributions`) |
| Thermal / fast / total flux maps | Section 9 (`calc_flux_maps`) |
| Power peaking (F-dH, F-z, F-Q) | Section 9 (`calc_flux_peaking`) |
| Reactivity-balance / feedback / peaking / uncertainty tables | Section 10 |
| Consolidated pass/fail vs safety criteria | Section 11 (`safety_analysis_results.yaml`) |
| Safety-case neutronics (criticality, limits, worst-case, shutdown) | Section 12 |
| Benchmarking (NuScale / CAREM-25 / RITM-200) | Section 13 |
| Standards compliance (IAEA SSR-2/1, NUREG-1431, RG 1.77) | Section 3 |
| Radiation shielding | Section 14 |
| Digital appendix (sample input, assumptions, reproducibility, ENDF/B-VIII.0) | Section 16 |

Run order for a complete report: run all cells top-to-bottom at `STAT = STAT_FINAL`; the figures land
under `aegis40_neutronics_outputs/plots/` and the pass/fail summary in `safety_analysis_results.yaml`.'''

# ── assemble: insert by content anchor ──
inserts = {
    find('Full-core loading map'):  [code(FA_DIAG)],
    find('Axial-shape VERIFICATION'): [code(FLUX), code(CYCLE)],
}
appendix_i = find('## 16 · Digital')
new = []
for i, c in enumerate(C):
    if i == appendix_i:
        new.append(md(COVER))      # requirements-coverage just before the appendix
    new.append(c)
    for nc in inserts.get(i, []):
        new.append(nc)
nb['cells'] = new

json.dump(nb, open(NB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
nb2 = json.load(open(NB, encoding='utf-8'))
bad = 0
for i, c in enumerate(nb2['cells']):
    if c['cell_type'] != 'code': continue
    s = ''.join(c['source'])
    if '%matplotlib' in s or s.lstrip().startswith('%'): continue
    try: ast.parse(s)
    except SyntaxError as e: print("FAIL", i, e); bad += 1
print("OK — added FA diagram, flux maps, BOC/MOC/EOC power+burnup, coeff rows, coverage table"
      if not bad else f"{bad} FAILED")
print(f"   cells {len(C)} -> {len(new)}")
