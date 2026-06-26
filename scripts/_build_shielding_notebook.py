"""Generate a standalone 37-FA biological-shield simulation + optimization notebook.
Reuses the proven lead-free material set, coupled n-gamma eigenvalue + weight-window
approach, and dose/flux/heating tallies from aegis40_neutronics_FER.ipynb (cells 14/44-48),
re-anchored to the 37-FA core envelope, plus an attenuation-fit shield optimizer."""
import json
from pathlib import Path

OUT = Path(r"D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_shielding_FER.ipynb")

cells = []
def md(text):  cells.append(("markdown", text))
def code(text): cells.append(("code", text))

# ---------------------------------------------------------------- 0 title
md(r"""# Aegis-40 - Biological Shield Simulation & Optimization (37-FA core)

**TEKNOFEST 2026 - FER Digital Appendix - OpenMC 0.15.3 - ENDF/B-VIII.0 (coupled n-gamma)**

Standalone shielding study for the **37-assembly, 7-wide octagonal** Aegis-40 iPWR
(125 MWth). This notebook (1) **evaluates** the lead-free radial biological shield -
dose-rate vs radius, RPV fast-neutron fluence, layer heating, and interface spectra - and
(2) **optimizes** the borated-polyethylene + magnetite-concrete thicknesses to meet the
**< 10 uSv/h** ALARA design target at minimum wall thickness, mass and cost.

The neutron source is a **power-normalized homogenized core** (equal-area 17x17 smear) with
self-consistent secondary photons (coupled n-gamma transport); deep-penetration statistics
use **MAGIC weight windows**. The radial build is re-anchored to the 37-FA envelope
(the previous shield in the main notebook was still sized for the 21-FA core). The optimized
design should be cross-checked against the heterogeneous coupled run in
`aegis40_neutronics_FER.ipynb` (Section 14).""")

# ---------------------------------------------------------------- 1 design basis
md(r"""## 1 - Design basis, criteria and radial build

**Dose criterion.** Total (neutron + gamma) dose-rate **< 10 uSv/h** just outside the outer
concrete face (controlled-area boundary; ALARA basis - Bagheri & Khalafi 2023; Ogul et al.
2026). The shield is **designed to half that (5 uSv/h)** to hold engineering margin.

**Lead-free philosophy.** Lead is excluded (toxicity, decommissioning-waste burden) and
tungsten reserved for casks. The bulk gamma + neutron shield is **magnetite (heavy) concrete**
(~58 wt% Fe, bound water moderates fast neutrons), preceded by a **borated-polyethylene** layer
that captures thermalised neutrons with low secondary-gamma yield, and a steel **thermal/neutron
shield** that protects the concrete from gamma heating.

**Radial build (core outward).** Core -> 20 cm water reflector -> SS-304 core barrel ->
downcomer + integral helical-SG annulus water -> SA-508 RPV -> reactor-cavity air ->
**[thermal shield | borated poly | magnetite concrete]** (the optimization variables) ->
ordinary-concrete finish.

**Secondary constraint.** RPV (SA-508) 60-yr fast fluence (E > 1 MeV) <= ~1e19 n/cm2
(embrittlement screening) - met by the downcomer water + barrel, reported here for completeness.""")

# ---------------------------------------------------------------- 2 setup
code(r"""import os, math, time, json, csv
from pathlib import Path
import numpy as np
import openmc
import matplotlib.pyplot as plt
%matplotlib inline

THREADS = int(os.environ.get("OPENMC_THREADS", "6"))
os.environ["OMP_NUM_THREADS"] = str(THREADS)

XS = Path(os.environ.get("OPENMC_CROSS_SECTIONS",
        "/mnt/d/openmc_data/endfb-viii.0-hdf5/cross_sections.xml"))
if not XS.is_file():
    raise FileNotFoundError(f"Cross sections not found: {XS} (need photon data for coupled n-gamma)")
openmc.config["cross_sections"] = str(XS)

ROOT = Path("./aegis40_shielding_outputs").resolve(); ROOT.mkdir(parents=True, exist_ok=True)
PLOTS = ROOT / "plots"; PLOTS.mkdir(exist_ok=True)
print("OpenMC", openmc.__version__, "| XS:", XS, "| threads:", THREADS)
print("outputs ->", ROOT)""")

# ---------------------------------------------------------------- 3 methodology
md(r"""## 2 - Methodology

- **Transport:** OpenMC 0.15.3 coupled **neutron + photon** Monte-Carlo, eigenvalue mode;
  the homogenized fissile core self-determines the fission source, photons are generated
  self-consistently (capture + inelastic + prompt-fission gammas) by `photon_transport=True`.
- **Source:** equal-area homogenized 17x17 core (UO2 + Zr-4 + He + H2O volume smear), power-
  normalized to 125 MWth -> ~9.5e18 n/s.
- **Deep penetration:** MAGIC weight windows (`WeightWindowGenerator`) on a cylindrical
  neutron/photon mesh - mandatory to converge dose through ~1.5 m of concrete.
- **Dose:** ICRP-116 ambient-dose-equivalent flux-to-dose (AP), tallied on a fine radial
  cylindrical mesh at the core midplane.
- **Optimization:** from one well-converged baseline run, the effective attenuation
  coefficients mu_n, mu_g of the magnetite concrete are fitted (log-linear), then the
  minimum concrete thickness meeting the design dose is solved analytically (both components
  together) and **verified** with a fresh high-statistics run. Borated-poly sensitivity is
  reported as an n/gamma trade.""")

# ---------------------------------------------------------------- 4 constants
code(r"""# ====================== locked geometry / source constants ======================
# Core (37 FA, 7-wide octagon) - homogenized cylindrical source
N_FA      = 37
FA_PITCH  = 21.6038
N_PIN     = 17
FUEL_R    = 0.40958
CLAD_IR   = 0.41873
CLAD_OR   = 0.47600
ACTIVE_H  = 200.0
RADIAL_REFLECTOR_CM = 20.0

R_CORE_ACTIVE = math.sqrt(N_FA * FA_PITCH**2 / math.pi)   # equal-area core radius ~74.1 cm
R_CORE_CYL    = R_CORE_ACTIVE + RADIAL_REFLECTOR_CM       # core + water reflector ~94.1 cm

# Fixed reactor envelope OUTSIDE the reflector (mechanical; thicknesses preserved from the
# vetted iPWR build, re-anchored to the larger 37-FA core radius)
BARREL_T = 2.5      # SS-304 core barrel
DOWN_T   = 57.5     # downcomer + integral helical-SG annulus water
RPV_T    = 16.5     # SA-508 vessel wall + clad
CAV_T    = 15.0     # reactor-cavity air gap
FIN_T    = 10.0     # ordinary-concrete finish

R_BARREL = R_CORE_CYL + BARREL_T
R_DOWN   = R_BARREL  + DOWN_T
R_RPV    = R_DOWN    + RPV_T
R_CAV    = R_RPV     + CAV_T
Z_HALF   = ACTIVE_H / 2.0
Z_BC     = Z_HALF + 80.0

# Bio-shield layers (the OPTIMIZATION variables) - initial guess
THSH_T0 = 5.0       # thermal/neutron steel shield
POLY_T0 = 10.0      # borated polyethylene
CONC_T0 = 120.0     # magnetite (heavy) concrete - generous baseline so attenuation is measurable

# Source normalization + dose target
CORE_POWER_MWT   = 125.0
E_FISSION_J      = 200.0e6 * 1.602176634e-19
FISSIONS_PER_S   = CORE_POWER_MWT * 1e6 / E_FISSION_J
S_NEUTRON        = 2.44 * FISSIONS_PER_S
DOSE_TARGET_USVH = 10.0
DESIGN_MARGIN    = 2.0                  # design to target/margin = 5 uSv/h
DOSE_DESIGN      = DOSE_TARGET_USVH / DESIGN_MARGIN
RPV_FLUENCE_LIMIT = 1.0e19              # n/cm2, E>1 MeV, 60 yr
PLANT_LIFE_S      = 60 * 3.156e7

# Homogenized-core volume fractions (per 17x17 FA: 264 fuel pins)
_FA_AREA = FA_PITCH**2
F_FUEL = math.pi * FUEL_R**2 * 264 / _FA_AREA
F_CLAD = math.pi * (CLAD_OR**2 - CLAD_IR**2) * 264 / _FA_AREA
F_GAP  = math.pi * (CLAD_IR**2 - FUEL_R**2) * 264 / _FA_AREA
F_WATR = 1.0 - F_FUEL - F_CLAD - F_GAP
CORE_ENRICH = 4.4
T_FUEL_K, T_MOD_K, RHO_WATER = 900.0, 556.0, 0.748

# MC statistics profiles
STAT_FAST  = dict(batches=40,  inactive=15, particles=5_000)
STAT_OPT   = dict(batches=60,  inactive=20, particles=20_000)
STAT_FINAL = dict(batches=120, inactive=30, particles=50_000)
USE_WW = True

# material densities (g/cm3) + rough unit costs ($/kg) for the bio-shield mass/cost objective
RHO_MAT  = dict(thermal_shield=8.00, borated_PE=0.95, magnetite_concrete=3.90, ordinary_concrete=2.30)
COST_MAT = dict(thermal_shield=3.0,  borated_PE=4.0,  magnetite_concrete=0.10, ordinary_concrete=0.05)

print(f"37-FA homogenized core: R_active={R_CORE_ACTIVE:.1f} cm (+{RADIAL_REFLECTOR_CM:.0f} refl "
      f"-> {R_CORE_CYL:.1f}) | RPV outer {R_RPV:.1f} cm (OD {2*R_RPV/100:.2f} m)")
print(f"core smear (vol): UO2 {F_FUEL:.3f} | Zr {F_CLAD:.3f} | He {F_GAP:.3f} | H2O {F_WATR:.3f}")
print(f"S_neutron = {S_NEUTRON:.3e} n/s | dose target {DOSE_TARGET_USVH:.0f} uSv/h "
      f"(design to {DOSE_DESIGN:.0f})")""")

# ---------------------------------------------------------------- 5 materials
code(r"""# ====================== materials (lead-free) + dose / normalization ======================
def mat_water(name="H2O", t=T_MOD_K, rho=RHO_WATER):
    m = openmc.Material(name=name, temperature=t); m.set_density("g/cm3", rho)
    m.add_element("H", 2.0); m.add_element("O", 1.0); m.add_s_alpha_beta("c_H_in_H2O"); return m

def _mat_uo2(e):
    m = openmc.Material(name=f"UO2_{e:.1f}", temperature=T_FUEL_K); m.set_density("g/cm3", 10.40)
    m.add_element("U", 1.0, enrichment=e); m.add_element("O", 2.0); return m

def _mat_zirc():
    m = openmc.Material(name="Zircaloy-4", temperature=T_MOD_K); m.set_density("g/cm3", 6.55)
    m.add_element("Zr", 0.9823, "wo"); m.add_element("Sn", 0.0145, "wo")
    m.add_element("Fe", 0.0021, "wo"); m.add_element("Cr", 0.0011, "wo"); return m

def _mat_he():
    m = openmc.Material(name="He", temperature=T_FUEL_K); m.set_density("g/cm3", 1.786e-4)
    m.add_element("He", 1.0); return m

def mat_core_homog():
    m = openmc.Material.mix_materials(
        [_mat_uo2(CORE_ENRICH), _mat_zirc(), _mat_he(), mat_water("core_mod")],
        [F_FUEL, F_CLAD, F_GAP, F_WATR], "vo", name="core_homog")
    m.temperature = T_FUEL_K
    m.add_s_alpha_beta("c_H_in_H2O")
    return m

def mat_ss304(name="SS304"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 8.00)
    for el, f in (("Fe", .685), ("Cr", .190), ("Ni", .095), ("Mn", .020), ("Si", .010)):
        m.add_element(el, f, "wo")
    return m

def mat_sa508(name="SA508_RPV"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 7.90)
    for el, f in (("Fe", .9685), ("Mn", .0140), ("Ni", .0075), ("Mo", .0050),
                  ("Si", .0025), ("Cr", .0003), ("C", .0022)):
        m.add_element(el, f, "wo")
    return m

def mat_air(name="cavity_air"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.001205)
    for el, f in (("N", .7553), ("O", .2318), ("Ar", .0129)): m.add_element(el, f, "wo")
    return m

def mat_borated_poly(boron_wt=5.0, name="borated_PE"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 0.95); pe = 1.0 - boron_wt / 100.0
    m.add_element("C", pe * .8563, "wo"); m.add_element("H", pe * .1437, "wo")
    m.add_element("B", boron_wt / 100.0, "wo"); return m

def mat_magnetite_concrete(name="magnetite_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 3.90)
    for el, f in (("H", .0036), ("O", .3100), ("Mg", .0089), ("Al", .0042), ("Si", .0223),
                  ("Ca", .0628), ("Ti", .0067), ("Mn", .0010), ("Fe", .5805)):
        m.add_element(el, f, "wo")
    return m

def mat_ordinary_concrete(name="ordinary_concrete"):
    m = openmc.Material(name=name); m.set_density("g/cm3", 2.30)
    for el, f in (("H", .0056), ("O", .4983), ("Na", .0171), ("Mg", .0024), ("Al", .0456),
                  ("Si", .3158), ("K", .0192), ("Ca", .0826), ("Fe", .0122)):
        m.add_element(el, f, "wo")
    return m

def dose_energy_filter(particle):
    e, d = openmc.data.dose_coefficients(particle, geometry="AP")   # eV, pSv*cm^2
    return openmc.EnergyFunctionFilter(e, d)

def flux_to_uSv_per_h(mean, vol_cm3, src_rate):
    # tally(flux x dose-coeff) = pSv*cm^3 / src ; /V * src -> pSv/s ; *3600/1e6 -> uSv/h
    return (mean / vol_cm3) * src_rate * 3600.0 / 1.0e6

print("materials + dose helpers ready.")""")

# ---------------------------------------------------------------- 6 builder
code(r"""# ====================== parametric shield model builder ======================
def build_shield(thsh_cm=THSH_T0, poly_cm=POLY_T0, conc_cm=CONC_T0,
                 stats=None, use_ww=None, tag="cfg"):
    # Full radial build with the 3 bio-shield layers parametric. Coupled n-gamma eigenvalue.
    stats  = stats or STAT_OPT
    use_ww = USE_WW if use_ww is None else use_ww

    R_THSH = R_CAV  + thsh_cm
    R_POLY = R_THSH + poly_cm
    R_CONC = R_POLY + conc_cm
    R_OUT  = R_CONC + FIN_T

    core   = mat_core_homog(); refl = mat_water("reflector_water")
    barrel = mat_ss304("core_barrel"); dwater = mat_water("downcomer_water"); rpv = mat_sa508()
    air    = mat_air(); thsh = mat_ss304("thermal_shield"); poly = mat_borated_poly()
    mconc  = mat_magnetite_concrete(); oconc = mat_ordinary_concrete()

    radii = [R_CORE_ACTIVE, R_CORE_CYL, R_BARREL, R_DOWN, R_RPV, R_CAV, R_THSH, R_POLY, R_CONC, R_OUT]
    cyl   = {r: openmc.ZCylinder(r=r) for r in radii}; cyl[R_OUT].boundary_type = "vacuum"
    ztop  = openmc.ZPlane(z0= Z_BC, boundary_type="vacuum")
    zbot  = openmc.ZPlane(z0=-Z_BC, boundary_type="vacuum")
    zspan = +zbot & -ztop
    def shell(ri, ro, fill, nm):
        reg = (-cyl[ro] if ri is None else (+cyl[ri] & -cyl[ro])) & zspan
        return openmc.Cell(name=nm, fill=fill, region=reg)
    cells = [shell(None,          R_CORE_ACTIVE, core,   "core"),
             shell(R_CORE_ACTIVE, R_CORE_CYL,    refl,   "reflector"),
             shell(R_CORE_CYL,    R_BARREL,      barrel, "barrel"),
             shell(R_BARREL,      R_DOWN,        dwater, "downcomer"),
             shell(R_DOWN,        R_RPV,         rpv,    "rpv"),
             shell(R_RPV,         R_CAV,         air,    "cavity"),
             shell(R_CAV,         R_THSH,        thsh,   "thermal_shield"),
             shell(R_THSH,        R_POLY,        poly,   "borated_poly"),
             shell(R_POLY,        R_CONC,        mconc,  "magnetite_concrete"),
             shell(R_CONC,        R_OUT,         oconc,  "outer_concrete")]
    cbn  = {c.name: c for c in cells}
    geom = openmc.Geometry(openmc.Universe(cells=cells))

    s = openmc.Settings(); s.run_mode = "eigenvalue"
    s.batches = stats["batches"]; s.inactive = stats["inactive"]; s.particles = stats["particles"]
    s.photon_transport = True
    s.temperature = {"method": "nearest", "tolerance": 1000.0}
    s.source = openmc.IndependentSource(
        space=openmc.stats.Box([-R_CORE_ACTIVE, -R_CORE_ACTIVE, -Z_HALF],
                               [ R_CORE_ACTIVE,  R_CORE_ACTIVE,  Z_HALF]),
        constraints={"fissionable": True})
    if use_ww:
        wwm = openmc.CylindricalMesh(r_grid=np.linspace(0.0, R_OUT, 30),
                                     z_grid=np.array([-Z_BC, -Z_HALF, 0.0, Z_HALF, Z_BC]),
                                     phi_grid=np.array([0.0, 2*np.pi]))
        ebt = np.logspace(-3, 7.2, 12); gens = []
        for pt in ("neutron", "photon"):
            g = openmc.WeightWindowGenerator(mesh=wwm, energy_bounds=ebt, particle_type=pt)
            g.update_parameters = {"ratio": 5.0, "threshold": 1.0, "value": "mean"}
            gens.append(g)
        s.weight_window_generators = gens; s.weight_windows_on = True
        s.max_history_splits = 1_000_000

    nr = 140
    dmesh = openmc.CylindricalMesh(r_grid=np.linspace(0.0, R_OUT, nr+1),
                                   z_grid=np.array([-50.0, 50.0]), phi_grid=np.array([0.0, 2*np.pi]))
    mf = openmc.MeshFilter(dmesh)
    t_dn = openmc.Tally(name="dose_n"); t_dn.scores = ["flux"]
    t_dn.filters = [mf, openmc.ParticleFilter("neutron"), dose_energy_filter("neutron")]
    t_dg = openmc.Tally(name="dose_g"); t_dg.scores = ["flux"]
    t_dg.filters = [mf, openmc.ParticleFilter("photon"), dose_energy_filter("photon")]
    t_fast = openmc.Tally(name="rpv_fast_flux"); t_fast.scores = ["flux"]
    t_fast.filters = [openmc.CellFilter(cbn["rpv"]), openmc.ParticleFilter("neutron"),
                      openmc.EnergyFilter([1.0e6, 2.0e7])]
    eg = np.logspace(-3, 7.3, 60); spec = []
    for cn in ("downcomer", "cavity", "outer_concrete"):
        for pt in ("neutron", "photon"):
            t = openmc.Tally(name=f"spec_{cn}_{pt}"); t.scores = ["flux"]
            t.filters = [openmc.CellFilter(cbn[cn]), openmc.ParticleFilter(pt), openmc.EnergyFilter(eg)]
            spec.append(t)
    t_heat = openmc.Tally(name="heating"); t_heat.scores = ["heating"]
    t_heat.filters = [openmc.CellFilter([cbn["rpv"], cbn["magnetite_concrete"]])]
    tallies = openmc.Tallies([t_dn, t_dg, t_fast, *spec, t_heat])

    mats  = openmc.Materials([core, refl, barrel, dwater, rpv, air, thsh, poly, mconc, oconc])
    model = openmc.Model(geom, mats, s, tallies)
    ginfo = dict(nr=nr, R_OUT=R_OUT, R_RPV=R_RPV, R_DOWN=R_DOWN, R_CAV=R_CAV,
                 R_THSH=R_THSH, R_POLY=R_POLY, R_CONC=R_CONC, Z_HALF=Z_HALF, cbn=cbn,
                 thsh_cm=thsh_cm, poly_cm=poly_cm, conc_cm=conc_cm, tag=tag, spec_eg=eg)
    return model, ginfo

def run_model(model, run_dir):
    run_dir = Path(run_dir); run_dir.mkdir(parents=True, exist_ok=True)
    for pat in ("*.xml", "statepoint.*.h5", "summary.h5", "weight_windows.h5"):
        for f in run_dir.glob(pat): f.unlink(missing_ok=True)
    model.export_to_xml(str(run_dir))
    old = Path.cwd(); os.chdir(run_dir)
    try:
        openmc.run(threads=THREADS, output=True)
    finally:
        os.chdir(old)
    return sorted(run_dir.glob("statepoint.*.h5"))[-1]

print("build_shield() + run_model() ready.")""")

# ---------------------------------------------------------------- 7 geometry md
md(r"""## 3 - Geometry verification

Render the re-anchored 37-FA radial build (xy at z=0 and xz at y=0) before committing to the
long transport runs - confirms the homogenized core, reflector, vessel and the three bio-shield
layers tile correctly out to the vacuum boundary.""")

# ---------------------------------------------------------------- 8 geometry render
code(r"""def plot_geometry(thsh=THSH_T0, poly=POLY_T0, conc=CONC_T0):
    model, gi = build_shield(thsh, poly, conc, stats=STAT_FAST, use_ww=False, tag="geom")
    d = ROOT / "00_geometry"; d.mkdir(exist_ok=True)
    R = gi["R_OUT"]
    palette = {"core_homog": (220, 70, 60), "reflector_water": (150, 190, 255),
               "core_barrel": (120, 120, 120), "downcomer_water": (150, 190, 255),
               "SA508_RPV": (60, 60, 60), "cavity_air": (245, 245, 245),
               "thermal_shield": (175, 175, 175), "borated_PE": (110, 190, 115),
               "magnetite_concrete": (185, 150, 90), "ordinary_concrete": (210, 190, 160)}
    cmap = {m: palette[m.name] for m in model.materials if m.name in palette}
    p_xy = openmc.Plot(); p_xy.filename = "geom_xy"; p_xy.basis = "xy"
    p_xy.width = (2*R+20, 2*R+20); p_xy.pixels = (1200, 1200)
    p_xy.color_by = "material"; p_xy.colors = cmap
    p_xz = openmc.Plot(); p_xz.filename = "geom_xz"; p_xz.basis = "xz"
    p_xz.width = (2*R+20, 2*Z_BC+20); p_xz.pixels = (1000, int(1000*Z_BC/R))
    p_xz.color_by = "material"; p_xz.colors = cmap
    model.plots = openmc.Plots([p_xy, p_xz])
    model.export_to_xml(str(d))
    old = Path.cwd(); os.chdir(d)
    try: openmc.plot_geometry(output=False)
    finally: os.chdir(old)
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    for ax, tag in zip(axes, ("xy", "xz")):
        for ext in ("png", "ppm"):
            f = d / f"geom_{tag}.{ext}"
            if f.is_file():
                try: ax.imshow(plt.imread(str(f)));
                except Exception: pass
                break
        ax.set_title(f"Aegis-40 shield - {tag}"); ax.axis("off")
    fig.tight_layout(); fig.savefig(PLOTS / "shield_geometry.png", dpi=150); plt.show()
    print(f"radial build (cm): core {R_CORE_ACTIVE:.1f} | refl {R_CORE_CYL:.1f} | barrel {R_BARREL:.1f} "
          f"| downcomer {R_DOWN:.1f} | RPV {R_RPV:.1f} | cavity {R_CAV:.1f} | "
          f"thsh {gi['R_THSH']:.1f} | poly {gi['R_POLY']:.1f} | conc {gi['R_CONC']:.1f} | out {R:.1f}")

plot_geometry()""")

# ---------------------------------------------------------------- 9 baseline md
md(r"""## 4 - Baseline shield performance

Run the initial build (thermal 5 / poly 10 / concrete 120 cm) and report the radial dose
profile, the dose just outside the concrete vs the 10 uSv/h target, the RPV 60-yr fast fluence,
and the RPV / concrete heating.""")

# ---------------------------------------------------------------- 10 evaluate + baseline run
code(r"""def evaluate(ginfo, sp_path, label="shield", make_plot=True, save_csv=True):
    sp = openmc.StatePoint(str(sp_path))
    nr = ginfo["nr"]; R_OUT = ginfo["R_OUT"]
    redges = np.linspace(0.0, R_OUT, nr+1); rcen = 0.5*(redges[:-1] + redges[1:])
    dz = 100.0; vol = np.pi*(redges[1:]**2 - redges[:-1]**2)*dz
    dn = sp.get_tally(name="dose_n").mean.ravel(); dg = sp.get_tally(name="dose_g").mean.ravel()
    dose_n = np.array([flux_to_uSv_per_h(dn[i], vol[i], S_NEUTRON) for i in range(nr)])
    dose_g = np.array([flux_to_uSv_per_h(dg[i], vol[i], S_NEUTRON) for i in range(nr)])
    dose_t = dose_n + dose_g
    ft = sp.get_tally(name="rpv_fast_flux").mean.ravel()[0]
    vrpv = np.pi*(ginfo["R_RPV"]**2 - ginfo["R_DOWN"]**2)*(2*ginfo["Z_HALF"])
    fast_flux = ft/vrpv*S_NEUTRON; fluence = fast_flux*PLANT_LIFE_S
    ht = sp.get_tally(name="heating").mean.ravel()*S_NEUTRON*1.602176634e-19
    res = dict(rcen=rcen, dose_n=dose_n, dose_g=dose_g, dose_t=dose_t,
               surface_n=float(dose_n[-1]), surface_g=float(dose_g[-1]), surface=float(dose_t[-1]),
               rpv_fast_flux=float(fast_flux), rpv_fluence_60y=float(fluence),
               heat_rpv_W=float(ht[0]), heat_conc_W=float(ht[1]))
    if save_csv:
        with open(ROOT / f"dose_vs_radius_{label}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["r_cm", "dose_n_uSv_h", "dose_g_uSv_h", "dose_total_uSv_h"])
            for i in range(nr): w.writerow([f"{rcen[i]:.2f}", f"{dose_n[i]:.4e}",
                                            f"{dose_g[i]:.4e}", f"{dose_t[i]:.4e}"])
    if make_plot:
        fig, ax = plt.subplots(figsize=(8.5, 5))
        ax.semilogy(rcen, dose_t, "k-", lw=2, label="total")
        ax.semilogy(rcen, dose_n, "b--", lw=1.3, label="neutron")
        ax.semilogy(rcen, dose_g, "r:", lw=1.3, label="gamma")
        ax.axhline(DOSE_TARGET_USVH, color="green", ls="-.", label="10 uSv/h target")
        ax.axhline(DOSE_DESIGN, color="seagreen", ls=":", lw=1, label=f"{DOSE_DESIGN:.0f} uSv/h design")
        for r, lab in ((ginfo["R_RPV"], "RPV"), (ginfo["R_POLY"], "poly"), (ginfo["R_CONC"], "conc")):
            ax.axvline(r, color="grey", lw=0.6, alpha=0.5); ax.text(r, ax.get_ylim()[1], lab, fontsize=7)
        ax.set_xlabel("radius (cm)"); ax.set_ylabel("dose rate (uSv/h)")
        ax.set_title(f"Aegis-40 radial bio-shield dose - {label}")
        ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.3); fig.tight_layout()
        fig.savefig(PLOTS / f"dose_vs_radius_{label}.png", dpi=150); plt.show()
    sp.close()
    return res

def report(res, ginfo):
    ok_d = res["surface"] < DOSE_TARGET_USVH
    ok_f = res["rpv_fluence_60y"] < RPV_FLUENCE_LIMIT
    print(f"  bio-shield: thsh {ginfo['thsh_cm']:.0f} / poly {ginfo['poly_cm']:.0f} / "
          f"conc {ginfo['conc_cm']:.0f} cm | R_out {ginfo['R_OUT']:.0f} cm")
    print(f"  surface dose : {res['surface']:.3e} uSv/h  (n {res['surface_n']:.2e} + g {res['surface_g']:.2e})"
          f"  [{'PASS' if ok_d else 'FAIL'} vs {DOSE_TARGET_USVH:.0f}]")
    print(f"  RPV fast flux: {res['rpv_fast_flux']:.3e} n/cm2/s | 60-yr fluence "
          f"{res['rpv_fluence_60y']:.3e} n/cm2  [{'PASS' if ok_f else 'FAIL'} vs {RPV_FLUENCE_LIMIT:.0e}]")
    print(f"  heating: RPV {res['heat_rpv_W']:.2e} W | magnetite concrete {res['heat_conc_W']:.2e} W")
    return ok_d and ok_f

print("[baseline] building + running coupled n-gamma shield (STAT_OPT, weight windows on)...")
t0 = time.time()
base_model, base_gi = build_shield(THSH_T0, POLY_T0, CONC_T0, stats=STAT_OPT, tag="baseline")
base_sp = run_model(base_model, ROOT / "01_baseline")
base = evaluate(base_gi, base_sp, label="baseline")
report(base, base_gi)
print(f"  [runtime {time.time()-t0:.0f} s]")""")

# ---------------------------------------------------------------- 11 optimization md
md(r"""## 5 - Shield optimization (attenuation-fit)

Inside the magnetite concrete the dose falls log-linearly, `D(r) ~ D_in * exp(-mu_eff * r)`,
separately for neutrons and gammas. Fitting `mu_n`, `mu_g` from the baseline profile and the
dose entering the concrete (`D_in` at the poly/concrete interface), the minimum concrete
thickness that brings **total** surface dose to the design value (5 uSv/h) is solved as

`D_in_n * exp(-mu_n * t) + D_in_g * exp(-mu_g * t) = D_design`  ->  `t_opt` (bisection).

The result is rounded up to a 5 cm construction increment and **verified** with a fresh
high-statistics run. A borated-poly sensitivity (neutron attenuation per cm of poly vs concrete)
is reported so the n/gamma split can be retuned if the surface dose is neutron-dominated.""")

# ---------------------------------------------------------------- 12 optimizer
code(r"""def fit_mu(rcen, dose, r_lo, r_hi):
    m = (rcen >= r_lo) & (rcen <= r_hi) & (dose > 0) & np.isfinite(dose)
    if m.sum() < 4: return None
    a, b = np.polyfit(rcen[m], np.log(dose[m]), 1)
    return dict(mu=-a, intercept=b, n=int(m.sum()))

# fit attenuation in the baseline magnetite-concrete band (trim 8 cm off each interface)
band_lo, band_hi = base_gi["R_POLY"] + 8.0, base_gi["R_CONC"] - 5.0
fn = fit_mu(base["rcen"], base["dose_n"], band_lo, band_hi)
fg = fit_mu(base["rcen"], base["dose_g"], band_lo, band_hi)
mu_n = fn["mu"] if fn else None
mu_g = fg["mu"] if fg else None
print(f"magnetite-concrete attenuation fit ({band_lo:.0f}-{band_hi:.0f} cm):")
print(f"  mu_n = {mu_n:.4f} /cm (1/e {1/mu_n:.1f} cm)" if mu_n and mu_n>0 else "  mu_n: fit FAILED (raise stats/WW)")
print(f"  mu_g = {mu_g:.4f} /cm (1/e {1/mu_g:.1f} cm)" if mu_g and mu_g>0 else "  mu_g: fit FAILED (raise stats/WW)")

# dose ENTERING the concrete (inner edge of the magnetite layer)
i_in = int(np.argmin(np.abs(base["rcen"] - base_gi["R_POLY"])))
Din_n = max(base["dose_n"][i_in], 1e-30); Din_g = max(base["dose_g"][i_in], 1e-30)
print(f"dose entering concrete @ r={base_gi['R_POLY']:.0f} cm: n {Din_n:.3e} | g {Din_g:.3e} uSv/h")

def surf_dose(t):
    dn = Din_n*math.exp(-mu_n*t) if (mu_n and mu_n>0) else Din_n
    dg = Din_g*math.exp(-mu_g*t) if (mu_g and mu_g>0) else Din_g
    return dn + dg

if (mu_n and mu_n>0) or (mu_g and mu_g>0):
    if surf_dose(0.0) <= DOSE_DESIGN:
        conc_req = 0.0
    else:
        lo, hi = 0.0, 400.0
        for _ in range(100):
            mid = 0.5*(lo+hi)
            if surf_dose(mid) > DOSE_DESIGN: lo = mid
            else: hi = mid
        conc_req = hi
    CONC_OPT = max(5.0, math.ceil(conc_req/5.0)*5.0)
    print(f"\nrequired magnetite concrete for {DOSE_DESIGN:.0f} uSv/h (n+g): {conc_req:.1f} cm "
          f"-> rounded to {CONC_OPT:.0f} cm")
    print(f"  (baseline was {CONC_T0:.0f} cm -> "
          f"{'SAVE' if CONC_OPT<CONC_T0 else 'ADD'} {abs(CONC_OPT-CONC_T0):.0f} cm)")
    dn_s = Din_n*math.exp(-mu_n*CONC_OPT) if (mu_n and mu_n>0) else Din_n
    dg_s = Din_g*math.exp(-mu_g*CONC_OPT) if (mu_g and mu_g>0) else Din_g
    print(f"  predicted surface dose @ {CONC_OPT:.0f} cm: n {dn_s:.2e} + g {dg_s:.2e} = "
          f"{dn_s+dg_s:.2e} uSv/h  ({'neutron' if dn_s>dg_s else 'gamma'}-limited)")
else:
    CONC_OPT = CONC_T0
    print("\nattenuation fit failed - keep baseline concrete; raise STAT/WW and re-run baseline.")

# borated-poly sensitivity: neutron attenuation per cm of poly vs concrete
fp = fit_mu(base["rcen"], base["dose_n"], base_gi["R_THSH"]+1.0, base_gi["R_POLY"]-0.5)
if fp and fp["mu"] > 0 and mu_n and mu_n > 0:
    print(f"\nborated-poly neutron attenuation mu_n,poly = {fp['mu']:.3f} /cm vs "
          f"mu_n,conc = {mu_n:.3f} /cm")
    print(f"  -> 1 cm poly removes the neutron dose that ~{fp['mu']/mu_n:.1f} cm of concrete would; "
          f"raise POLY_T0 if the optimum stays neutron-limited.")""")

# ---------------------------------------------------------------- 13 verification
code(r"""# ====================== verify the optimized build (fresh high-stat run) ======================
print(f"[verify] optimized build: thsh {THSH_T0:.0f} / poly {POLY_T0:.0f} / conc {CONC_OPT:.0f} cm "
      f"(STAT_FINAL)...")
t0 = time.time()
opt_model, opt_gi = build_shield(THSH_T0, POLY_T0, CONC_OPT, stats=STAT_FINAL, tag="optimized")
opt_sp = run_model(opt_model, ROOT / "02_optimized")
opt = evaluate(opt_gi, opt_sp, label="optimized")
ok = report(opt, opt_gi)
print(f"  [runtime {time.time()-t0:.0f} s]")

def layer_mass_cost(name, R_in, t):
    vol_cm3 = math.pi*((R_in+t)**2 - R_in**2)*(2*Z_HALF)
    mass_kg = RHO_MAT[name]*vol_cm3/1000.0   # g/cm3 * cm3 = g -> /1000 = kg
    return mass_kg, mass_kg*COST_MAT[name]

mb, cb = layer_mass_cost("magnetite_concrete", base_gi["R_POLY"], CONC_T0)
mo, co = layer_mass_cost("magnetite_concrete", opt_gi["R_POLY"], CONC_OPT)
print("\n================ baseline vs optimized ================")
print(f"  {'quantity':28s}{'baseline':>14s}{'optimized':>14s}")
print(f"  {'magnetite concrete (cm)':28s}{CONC_T0:>14.0f}{CONC_OPT:>14.0f}")
print(f"  {'shield outer radius (cm)':28s}{base_gi['R_OUT']:>14.1f}{opt_gi['R_OUT']:>14.1f}")
print(f"  {'concrete mass (t)':28s}{mb/1000:>14.1f}{mo/1000:>14.1f}")
print(f"  {'concrete cost (k$)':28s}{cb/1000:>14.1f}{co/1000:>14.1f}")
print(f"  {'surface dose (uSv/h)':28s}{base['surface']:>14.2e}{opt['surface']:>14.2e}")
print(f"  {'vs 10 uSv/h target':28s}{'PASS' if base['surface']<DOSE_TARGET_USVH else 'FAIL':>14s}"
      f"{'PASS' if opt['surface']<DOSE_TARGET_USVH else 'FAIL':>14s}")
print("=======================================================")
print(f"OVERALL: {'PASS' if ok else 'FAIL (raise stats / adjust layers)'}")""")

# ---------------------------------------------------------------- 14 summary md
md(r"""## 6 - Results, optimized radial build, and digital appendix

The cell below writes the optimized radial-build table and a machine-readable summary
(`shielding_summary.yaml` + `radial_build.csv`). Reportable artefacts:

- `plots/shield_geometry.png` - radial build render
- `plots/dose_vs_radius_baseline.png`, `..._optimized.png` + matching CSVs
- `shielding_summary.yaml` - dose, RPV fluence, heating, layer thicknesses, PASS/FAIL

**Assumptions & limitations.** Homogenized equal-area core source (per-pin detail not needed
for a bio-shield); attenuation-fit extrapolates the baseline concrete `mu_eff` to the optimized
thickness (geometric/buildup drift is second-order and is closed by the verification run). For
the licensing-grade number, re-run the optimized thicknesses against the **heterogeneous** coupled
core in `aegis40_neutronics_FER.ipynb` Section 14. Data: ENDF/B-VIII.0 (n + photon); dose ICRP-116 AP.""")

# ---------------------------------------------------------------- 15 outputs
code(r"""build = [("core (homogenized)", 0.0, R_CORE_ACTIVE, "UO2/Zr/H2O smear"),
         ("water reflector", R_CORE_ACTIVE, R_CORE_CYL, "H2O"),
         ("core barrel", R_CORE_CYL, R_BARREL, "SS-304"),
         ("downcomer + SG annulus", R_BARREL, R_DOWN, "H2O"),
         ("reactor pressure vessel", R_DOWN, R_RPV, "SA-508"),
         ("reactor cavity", R_RPV, R_CAV, "air"),
         ("thermal shield", R_CAV, opt_gi["R_THSH"], "SS-304"),
         ("borated polyethylene", opt_gi["R_THSH"], opt_gi["R_POLY"], "5 wt% B-PE"),
         ("magnetite concrete", opt_gi["R_POLY"], opt_gi["R_CONC"], "heavy concrete"),
         ("ordinary-concrete finish", opt_gi["R_CONC"], opt_gi["R_OUT"], "Portland")]
with open(ROOT / "radial_build.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["layer", "r_in_cm", "r_out_cm", "thickness_cm", "material"])
    for nm, ri, ro, mt in build: w.writerow([nm, f"{ri:.1f}", f"{ro:.1f}", f"{ro-ri:.1f}", mt])

summary = dict(
    design="aegis40-37FA-shield",
    core=dict(n_fa=N_FA, r_active_cm=round(R_CORE_ACTIVE, 2), power_MWth=CORE_POWER_MWT,
              s_neutron_per_s=S_NEUTRON),
    optimized=dict(thermal_shield_cm=THSH_T0, borated_poly_cm=POLY_T0,
                   magnetite_concrete_cm=CONC_OPT, r_out_cm=round(opt_gi["R_OUT"], 1)),
    dose=dict(surface_uSv_h=opt["surface"], neutron=opt["surface_n"], gamma=opt["surface_g"],
              target_uSv_h=DOSE_TARGET_USVH, pass_=bool(opt["surface"] < DOSE_TARGET_USVH)),
    rpv=dict(fast_flux_n_cm2_s=opt["rpv_fast_flux"], fluence_60y_n_cm2=opt["rpv_fluence_60y"],
             limit_n_cm2=RPV_FLUENCE_LIMIT, pass_=bool(opt["rpv_fluence_60y"] < RPV_FLUENCE_LIMIT)),
    heating_W=dict(rpv=opt["heat_rpv_W"], magnetite_concrete=opt["heat_conc_W"]),
)
with open(ROOT / "shielding_summary.yaml", "w") as f:
    try:
        import yaml; yaml.safe_dump(summary, f, sort_keys=False)
    except Exception:
        json.dump(summary, f, indent=2)

print("optimized radial build (cm):")
for nm, ri, ro, mt in build:
    print(f"  {nm:26s} {ri:7.1f} -> {ro:7.1f}  ({ro-ri:5.1f} cm)  {mt}")
print("\nsaved:", ROOT / "radial_build.csv", "|", ROOT / "shielding_summary.yaml")""")

# ----------------------------------------------------------------- assemble notebook
nb = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
      "name": "python3"}, "language_info": {"name": "python", "version": "3.11"}},
      "nbformat": 4, "nbformat_minor": 5}
for kind, text in cells:
    src = text.splitlines(keepends=True)
    if kind == "markdown":
        nb["cells"].append({"cell_type": "markdown", "metadata": {}, "source": src})
    else:
        nb["cells"].append({"cell_type": "code", "metadata": {}, "execution_count": None,
                            "outputs": [], "source": src})

OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {OUT}  ({len(nb['cells'])} cells)")
