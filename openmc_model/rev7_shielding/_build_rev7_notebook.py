"""
Build aegis40_3d_core_shielding_rev7.ipynb = rev6 notebook (verbatim) + an
appended SHIELDING section that wraps the REAL 17x17 pin lattice in a lead-free
biological shield and adds the dose/flux/heating tallies.

Run:  python _build_rev7_notebook.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REV6 = HERE.parent / "rev6_standards" / "aegis40_3d_core_notebook_rev6.ipynb"
REV7 = HERE / "aegis40_3d_core_shielding_rev7.ipynb"

nb = json.loads(REV6.read_text(encoding="utf-8"))


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": text.splitlines(keepends=True)}


# ---------------------------------------------------------------------------
C_MD = r"""## 9 · rev7 — Radiation SHIELDING extension (real lattice source + biological shield)

Reuses **everything above** (materials, `build_core`, the real 17x17 pin lattice).
We wrap the actual core in a lead-free cylindrical biological shield and run a
**coupled neutron + photon, eigenvalue** transport (the real fission source drives
it; OpenMC generates the fission/capture gammas automatically — one normalisation
covers both).

**Lead-free** (lead is toxic; tungsten too expensive for a stationary wall): the
bulk gamma+neutron shield is **magnetite (heavy) concrete** plus a **borated-poly**
thermal-neutron layer. Design criterion (Bagheri & Khalafi 2023; Ogul 2026):
**total dose < 10 uSv/h behind the last layer.**

Outputs: dose-vs-radius **plot** + CSV, RPV fast flux (E>1 MeV), n/gamma spectra at
3 interfaces, heating (W). Statistics are LOW by default — bump `STAT_SHIELD`."""

C_MATS = r'''# ── 9.1 Shield materials (lead-free) + flux->dose + source rate ──────────────
def mat_ss304(name="SS304"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 8.00)
    m.add_element("Fe",0.685,"wo"); m.add_element("Cr",0.190,"wo")
    m.add_element("Ni",0.095,"wo"); m.add_element("Mn",0.020,"wo")
    m.add_element("Si",0.010,"wo"); return m

def mat_sa508(name="SA508_RPV"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 7.90)
    m.add_element("Fe",0.9685,"wo"); m.add_element("Mn",0.0140,"wo")
    m.add_element("Ni",0.0075,"wo"); m.add_element("Mo",0.0050,"wo")
    m.add_element("Si",0.0025,"wo"); m.add_element("Cr",0.0003,"wo")
    m.add_element("C",0.0022,"wo"); return m

def mat_air(name="air"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.001205)
    m.add_element("N",0.7553,"wo"); m.add_element("O",0.2318,"wo")
    m.add_element("Ar",0.0129,"wo"); return m

def mat_borated_poly(boron_wt=5.0, name="borated_PE"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.95)
    pe = 1.0 - boron_wt/100.0
    m.add_element("C", pe*0.8563,"wo"); m.add_element("H", pe*0.1437,"wo")
    m.add_element("B", boron_wt/100.0,"wo"); return m

def mat_magnetite_concrete(name="magnetite_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 3.90)
    for el,f in [("H",0.0036),("O",0.3100),("Mg",0.0089),("Al",0.0042),
                 ("Si",0.0223),("Ca",0.0628),("Ti",0.0067),("Mn",0.0010),
                 ("Fe",0.5805)]:
        m.add_element(el,f,"wo")
    return m

def mat_ordinary_concrete(name="ordinary_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 2.30)
    for el,f in [("H",0.0056),("O",0.4983),("Na",0.0171),("Mg",0.0024),
                 ("Al",0.0456),("Si",0.3158),("K",0.0192),("Ca",0.0826),
                 ("Fe",0.0122)]:
        m.add_element(el,f,"wo")
    return m

def dose_energy_filter(particle):
    e, d = openmc.data.dose_coefficients(particle, geometry="AP")  # eV, pSv*cm^2
    return openmc.EnergyFunctionFilter(e, d)

def flux_to_uSv_per_h(mean, vol_cm3, src_rate):
    # tally(flux, EnergyFunctionFilter[dose]) = pSv*cm^3 / src ; /V*src_rate -> pSv/s
    return (mean / vol_cm3) * src_rate * 3600.0 / 1.0e6

# Absolute source normalisation (125 MWth -> neutrons/s)
E_FISSION_J    = 200.0e6 * 1.602176634e-19
FISSIONS_PER_S = CORE_POWER_MWT * 1e6 / E_FISSION_J
S_NEUTRON      = 2.44 * FISSIONS_PER_S          # ~9.5e18 n/s (photons are secondary)
DOSE_TARGET_USVH = 10.0

# LOWER statistics for the shielding run (bump for report numbers)
STAT_SHIELD = dict(batches=60, inactive=20, particles=10_000)
USE_WW = True
print(f"Shield source rate: {S_NEUTRON:.3e} n/s @ {CORE_POWER_MWT} MWth")
'''

C_BUILD = r'''# ── 9.2 Wrap the REAL core lattice in the lead-free shield ──────────────────
# Radial layers (cm). The pin lattice already tiles water beyond the 21 FAs, so
# filling a cylinder of radius R_CORE_CYL with the lattice gives fuel in the FA
# footprint and reflector water elsewhere.
R_CORE_CYL = 57.0
R_BARREL = R_CORE_CYL + 5.0     # 62
R_DOWN   = R_BARREL   + 13.0    # 75
R_RPV    = R_DOWN     + 18.0    # 93   <- fast-flux tally here
R_CAV    = R_RPV      + 15.0    # 108
R_THSH   = R_CAV      + 5.0     # 113
R_POLY   = R_THSH     + 10.0    # 123
R_CONC   = R_POLY     + 120.0   # 243  magnetite (lead-free bulk shield)
R_OUT    = R_CONC     + 10.0    # 253
Z_HALF   = ACTIVE_HEIGHT / 2.0  # 100
Z_BC     = Z_HALF + 80.0        # 180

def build_shielded_model(control_rod_state="aro", stats=None):
    stats = stats or STAT_SHIELD
    # 1) build the real core, extract its pin lattice
    core_model, mat_dict, info = build_core(control_rod_state=control_rod_state,
                                             stats=stats)
    root = core_model.geometry.root_universe
    core_lat_cell = next(c for c in root.cells.values() if c.name == "core_lat_cell")
    core_lat = core_lat_cell.fill

    # 2) shield materials
    barrel = mat_ss304("core_barrel"); rpv = mat_sa508()
    air = mat_air("cavity_air"); thsh = mat_ss304("thermal_shield")
    poly = mat_borated_poly(5.0); mconc = mat_magnetite_concrete()
    oconc = mat_ordinary_concrete()
    dwater = mat_water(temp=T_MOD_K, density=RHO_WATER_NOM, name="downcomer_water")

    # 3) geometry — nested cylinders bounded in z
    cyl = {r: openmc.ZCylinder(r=r) for r in
           (R_CORE_CYL,R_BARREL,R_DOWN,R_RPV,R_CAV,R_THSH,R_POLY,R_CONC,R_OUT)}
    cyl[R_OUT].boundary_type = "vacuum"
    ztop = openmc.ZPlane(z0= Z_BC, boundary_type="vacuum")
    zbot = openmc.ZPlane(z0=-Z_BC, boundary_type="vacuum")
    zspan = +zbot & -ztop
    def shell(ri, ro, fill, name):
        reg = (-cyl[ro] if ri is None else (+cyl[ri] & -cyl[ro])) & zspan
        return openmc.Cell(name=name, fill=fill, region=reg)
    cells = [
        shell(None,       R_CORE_CYL, core_lat, "core_lattice"),
        shell(R_CORE_CYL, R_BARREL,   barrel,   "barrel"),
        shell(R_BARREL,   R_DOWN,     dwater,   "downcomer"),
        shell(R_DOWN,     R_RPV,      rpv,      "rpv"),
        shell(R_RPV,      R_CAV,      air,      "cavity"),
        shell(R_CAV,      R_THSH,     thsh,     "thermal_shield"),
        shell(R_THSH,     R_POLY,     poly,     "borated_poly"),
        shell(R_POLY,     R_CONC,     mconc,    "magnetite_concrete"),
        shell(R_CONC,     R_OUT,      oconc,    "outer_concrete"),
    ]
    cbn = {c.name: c for c in cells}
    geom = openmc.Geometry(openmc.Universe(cells=cells))

    # 4) settings — eigenvalue + photon transport, fission source in the core
    s = openmc.Settings()
    s.run_mode  = "eigenvalue"
    s.batches   = stats["batches"]; s.inactive = stats["inactive"]
    s.particles = stats["particles"]
    s.photon_transport = True
    s.temperature = {"method": "nearest", "tolerance": 1000.0}
    ch = info["core_half_cm"]
    s.source = openmc.IndependentSource(
        space=openmc.stats.Box([-ch,-ch,-Z_HALF],[ch,ch,Z_HALF]),
        constraints={"fissionable": True})
    if USE_WW:
        wwm = openmc.CylindricalMesh(
            r_grid=np.linspace(0.0, R_OUT, 30),
            z_grid=np.array([-Z_BC,-Z_HALF,0.0,Z_HALF,Z_BC]),
            phi_grid=np.array([0.0, 2*np.pi]))
        ebt = np.logspace(-3, 7.2, 12)
        gens = []
        for pt in ("neutron","photon"):
            g = openmc.WeightWindowGenerator(mesh=wwm, energy_bounds=ebt, particle_type=pt)
            g.update_parameters = {"ratio":5.0,"threshold":1.0,"value":"mean"}
            gens.append(g)
        s.weight_window_generators = gens
        s.weight_windows_on = True
        s.max_history_splits = 1_000_000

    # 5) tallies
    nr = 120
    dmesh = openmc.CylindricalMesh(
        r_grid=np.linspace(0.0, R_OUT, nr+1),
        z_grid=np.array([-50.0, 50.0]), phi_grid=np.array([0.0, 2*np.pi]))
    mf = openmc.MeshFilter(dmesh)
    t_dn = openmc.Tally(name="dose_n"); t_dn.scores=["flux"]
    t_dn.filters=[mf, openmc.ParticleFilter("neutron"), dose_energy_filter("neutron")]
    t_dg = openmc.Tally(name="dose_g"); t_dg.scores=["flux"]
    t_dg.filters=[mf, openmc.ParticleFilter("photon"),  dose_energy_filter("photon")]
    t_fast = openmc.Tally(name="rpv_fast_flux"); t_fast.scores=["flux"]
    t_fast.filters=[openmc.CellFilter(cbn["rpv"]), openmc.ParticleFilter("neutron"),
                    openmc.EnergyFilter([1.0e6, 2.0e7])]
    eg = np.logspace(-3, 7.3, 60); spec=[]
    for cn in ("downcomer","cavity","outer_concrete"):
        for pt in ("neutron","photon"):
            t = openmc.Tally(name=f"spec_{cn}_{pt}"); t.scores=["flux"]
            t.filters=[openmc.CellFilter(cbn[cn]), openmc.ParticleFilter(pt),
                       openmc.EnergyFilter(eg)]
            spec.append(t)
    t_heat = openmc.Tally(name="heating"); t_heat.scores=["heating"]
    t_heat.filters=[openmc.CellFilter([cbn["rpv"], cbn["magnetite_concrete"]])]
    tallies = openmc.Tallies([t_dn,t_dg,t_fast,*spec,t_heat])

    mats = openmc.Materials(list(core_model.materials) +
                            [barrel,dwater,rpv,air,thsh,poly,mconc,oconc])
    model = openmc.Model(geom, mats, s, tallies)
    geo_info = dict(nr=nr, R_OUT=R_OUT, R_RPV=R_RPV, R_DOWN=R_DOWN, R_POLY=R_POLY,
                    R_CONC=R_CONC, Z_HALF=Z_HALF, cbn=cbn)
    return model, geo_info
'''

C_RUN = r'''# ── 9.3 Run the shielded model (LOW stats — bump STAT_SHIELD for report) ────
shield_model, ginfo = build_shielded_model(control_rod_state="aro")
shield_dir = _run_dir("shielding_rev7")
_run_model(shield_model, shield_dir, tag="shielding_rev7")
print("shielding run complete ->", shield_dir)
'''

C_POST = r'''# ── 9.4 Post-process: dose-vs-radius PLOT + CSV, fast flux, spectra, heating ─
sps = sorted(Path(shield_dir).glob("statepoint.*.h5"))
sp = openmc.StatePoint(str(sps[-1]))
nr = ginfo["nr"]; R_OUT = ginfo["R_OUT"]
redges = np.linspace(0.0, R_OUT, nr+1); rcen = 0.5*(redges[:-1]+redges[1:])
dz = 100.0; vol = np.pi*(redges[1:]**2 - redges[:-1]**2)*dz
dn = sp.get_tally(name="dose_n").mean.ravel()
dg = sp.get_tally(name="dose_g").mean.ravel()
dose_n = np.array([flux_to_uSv_per_h(dn[i], vol[i], S_NEUTRON) for i in range(nr)])
dose_g = np.array([flux_to_uSv_per_h(dg[i], vol[i], S_NEUTRON) for i in range(nr)])
dose_t = dose_n + dose_g

import csv
with open(Path(shield_dir)/"doseA_vs_radius.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["r_cm","dose_n_uSv_h","dose_g_uSv_h","dose_total_uSv_h"])
    for i in range(nr): w.writerow([f"{rcen[i]:.3f}",f"{dose_n[i]:.4e}",f"{dose_g[i]:.4e}",f"{dose_t[i]:.4e}"])

fig, ax = plt.subplots(figsize=(8,5))
ax.semilogy(rcen, dose_t, "k-", lw=2, label="total")
ax.semilogy(rcen, dose_n, "b--", label="neutron")
ax.semilogy(rcen, dose_g, "r:",  label="gamma")
ax.axhline(DOSE_TARGET_USVH, color="green", ls="-.", label="10 uSv/h target")
for r,lab in [(ginfo["R_RPV"],"RPV"),(ginfo["R_POLY"],"poly"),(ginfo["R_CONC"],"concrete")]:
    ax.axvline(r, color="grey", lw=0.6, alpha=0.5)
ax.set_xlabel("radius (cm)"); ax.set_ylabel("dose rate (uSv/h)")
ax.set_title("Aegis-40 rev7 — operational radial shield (real lattice source)")
ax.legend(); ax.grid(True, which="both", alpha=0.3); fig.tight_layout()
fig.savefig(Path(shield_dir)/"doseA_vs_radius.png", dpi=140); plt.show()

# fast flux + heating
ft = sp.get_tally(name="rpv_fast_flux").mean.ravel()[0]
vrpv = np.pi*(ginfo["R_RPV"]**2 - ginfo["R_DOWN"]**2)*(2*ginfo["Z_HALF"])
fast_flux = ft/vrpv*S_NEUTRON
ht = sp.get_tally(name="heating").mean.ravel()*S_NEUTRON*1.602176634e-19
outside = dose_t[-1]
verdict = "PASS" if outside < DOSE_TARGET_USVH else "FAIL (raise stats / shield)"
print(f"dose just outside concrete: {outside:.3e} uSv/h -> {verdict}")
print(f"RPV fast flux (E>1 MeV): {fast_flux:.3e} n/cm2/s | 60-yr fluence {fast_flux*60*3.156e7:.3e} n/cm2")
print(f"heating  RPV: {ht[0]:.3e} W | magnetite concrete: {ht[1]:.3e} W")

# spectra CSV
eg = np.logspace(-3, 7.3, 60); ecen = np.sqrt(eg[:-1]*eg[1:])
with open(Path(shield_dir)/"doseA_spectra.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["E_eV"]+[f"{cn}_{p}" for cn in ("downcomer","cavity","outer_concrete") for p in ("n","g")])
    cols = {}
    for cn in ("downcomer","cavity","outer_concrete"):
        for pt,tag in (("neutron","n"),("photon","g")):
            cols[f"{cn}_{tag}"] = sp.get_tally(name=f"spec_{cn}_{pt}").mean.ravel()
    for i,e in enumerate(ecen):
        w.writerow([f"{e:.4e}"]+[f"{cols[f'{cn}_{t}'][i]:.4e}" for cn in ("downcomer","cavity","outer_concrete") for t in ("n","g")])
sp.close()
print("outputs in", shield_dir)
'''

C_CASK = r"""### 9.5 · Spent-fuel cask (Task B)

The dry-cask shield (decay-photon source built from the depletion results) is the
companion script **`aegis40_cask_v7.py`** in this folder — run it separately:

```bash
export AEGIS_DEPLETION_H5=.../aegis40_rev6_outputs/depletion/depletion_results.h5
python aegis40_cask_v7.py     # -> out_taskB/  (surface / 1 m / 2 m dose vs SSR-6)
```"""

nb["cells"] += [md(C_MD), code(C_MATS), code(C_BUILD), code(C_RUN), code(C_POST), md(C_CASK)]
REV7.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", REV7, "| cells:", len(nb["cells"]))
