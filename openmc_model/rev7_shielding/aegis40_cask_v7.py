"""
Aegis-40 — rev7 · TASK B : Spent-fuel dry-cask shield (lead-free)
=================================================================
Self-contained OpenMC fixed-source coupled PHOTON+NEUTRON transport for the
discharged-core dry storage / transport cask.

SOURCE (this is the "everything in one place" upgrade) — built in this order:
  1. PRIMARY: regenerate the FULL decay-photon spectrum directly from the
     OpenMC depletion results (every emitter, every line) via
     material.get_decay_photon_energy().  Set DEPLETION_RESULTS to your
     depletion_results.h5 and COOLING_YEARS.
  2. FALLBACK: if that file is not found, read the repo group spectrum
     docs/competition/shielding/gamma_spectrum.csv (itself OpenMC-derived).
Spontaneous-fission neutron source = 2.99e9 n/s (Cm-244 dominated, ~2 MeV
Watt), from the discharge inventory (see source_spectra.md).

Cask radial stack (lead-free), from the fuel basket outward:
    homogenized spent-fuel basket   r <  80 cm   (source)
    steel canister      6 cm    80 ->  86
    gamma steel        20 cm    86 -> 106        (replaces lead — thick carbon steel)
    borated poly (5%B) 12 cm   106 -> 118        (neutron capture)
    concrete overpack  50 cm   118 -> 168        (gamma + neutron, cheap)
    air                        168 -> 380         (dose points: surface / 1 m / 2 m)

OUTPUTS -> ./out_taskB/:
  * doseB_vs_radius.csv     dose muSv/h vs radius (n + gamma + total)
  * doseB_vs_radius.png
  * doseB_summary.txt       surface / 1 m / 2 m dose, PASS/FAIL vs SSR-6 / 10 CFR 71

Run:  python aegis40_cask_v7.py
"""

import os
from pathlib import Path
import numpy as np
import openmc

import shielding_common as sc

OUT = Path("./out_taskB"); OUT.mkdir(exist_ok=True)
USE_WW = True

# --- source configuration ---------------------------------------------------
DEPLETION_RESULTS = os.environ.get(
    "AEGIS_DEPLETION_H5",
    "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
    "aegis40_rev6_outputs/depletion/depletion_results.h5")
COOLING_YEARS = 5.0
CSV_FALLBACK = Path(__file__).resolve().parents[2] / \
    "docs/competition/shielding/gamma_spectrum.csv"
SF_NEUTRON_RATE = 2.987e9            # n/s, whole-core SF (source_spectra.md)

# --- cask radial boundaries (cm) --------------------------------------------
R_FUEL  = 80.0
R_CAN   = R_FUEL + 6.0               # 86
R_GAMMA = R_CAN  + 20.0             # 106
R_POLY  = R_GAMMA + 12.0            # 118
R_CONC  = R_POLY + 50.0            # 168
R_AIR   = R_CONC + 212.0           # 380  (covers 2 m past surface)
H_FUEL  = 200.0
Z_HALF  = H_FUEL / 2.0
Z_BC    = Z_HALF + 120.0


# ----------------------------------------------------------------------------
# Source builders
# ----------------------------------------------------------------------------
def photon_source_from_depletion(h5, cooling_years):
    """Full decay-photon spectrum from the depletion results, decayed to the
    cooling time.  Returns (openmc.stats.Univariate energy dist, total ph/s)."""
    res = openmc.deplete.Results(h5)
    n_steps = len(res)
    mats = res.export_to_materials(n_steps - 1)      # discharged compositions
    # decay the depletable fuel to the cooling time at zero flux
    fuels = [m for m in mats if m.depletable]
    op = openmc.deplete.IndependentOperator(
        openmc.Materials(fuels), normalization_mode="source-rate")
    t = cooling_years * 365.25 * 24 * 3600
    integr = openmc.deplete.PredictorIntegrator(
        op, [t], source_rates=[0.0], timestep_units="s")
    cdir = OUT / "_decay"; cdir.mkdir(exist_ok=True)
    cwd0 = os.getcwd(); os.chdir(cdir)
    try:
        integr.integrate()
        dres = openmc.deplete.Results("depletion_results.h5")
        dmats = dres.export_to_materials(len(dres) - 1)
    finally:
        os.chdir(cwd0)

    energies, probs, total = [], [], 0.0
    for m in dmats:
        try:
            dist = m.get_decay_photon_energy()
        except Exception:
            dist = None
        if dist is None or len(getattr(dist, "x", [])) == 0:
            continue
        strength = float(dist.integral())            # ph/s for this material
        energies.append(np.asarray(dist.x))
        probs.append(np.asarray(dist.p) * strength)
        total += strength
    if total <= 0:
        raise RuntimeError("no decay photons from depletion results")
    e = np.concatenate(energies); p = np.concatenate(probs)
    return openmc.stats.Discrete(e, p / p.sum()), total


def photon_source_from_csv(path):
    """Fallback: group spectrum gamma_spectrum.csv (OpenMC-derived)."""
    rows = [l.split(",") for l in Path(path).read_text().splitlines()[1:] if l.strip()]
    elo = np.array([float(r[0]) for r in rows]) * 1e6
    ehi = np.array([float(r[1]) for r in rows]) * 1e6
    rate = np.array([float(r[2]) for r in rows])
    emid = np.sqrt(np.maximum(elo, 1e3) * ehi)
    mask = rate > 0
    total = rate[mask].sum()
    return openmc.stats.Discrete(emid[mask], rate[mask] / total), total


def build_photon_source(src_space):
    if Path(DEPLETION_RESULTS).is_file():
        try:
            dist, total = photon_source_from_depletion(DEPLETION_RESULTS, COOLING_YEARS)
            print(f"[source] depletion-derived photons: {total:.3e} ph/s "
                  f"@ {COOLING_YEARS:.0f} yr cooling")
        except Exception as e:
            print(f"[source] depletion path failed ({e}); using CSV fallback")
            dist, total = photon_source_from_csv(CSV_FALLBACK)
            print(f"[source] CSV photons: {total:.3e} ph/s")
    else:
        dist, total = photon_source_from_csv(CSV_FALLBACK)
        print(f"[source] depletion h5 not found; CSV photons: {total:.3e} ph/s")
    return openmc.IndependentSource(space=src_space, energy=dist,
                                    particle="photon", strength=total), total


# ----------------------------------------------------------------------------
# Materials
# ----------------------------------------------------------------------------
def mat_spent_fuel():
    """Smeared discharged fuel + Zr + steel basket (source region)."""
    uo2 = openmc.Material(name="spent_uo2")
    uo2.set_density("g/cm3", 10.40)
    uo2.add_element("U", 1.0, enrichment=1.2)        # degraded enrichment proxy
    uo2.add_element("O", 2.0)
    zr = openmc.Material(name="basket_zr"); zr.set_density("g/cm3", 6.55); zr.add_element("Zr", 1.0)
    ss = sc.mat_ss304("basket_steel")
    return openmc.Material.mix_materials(
        [uo2, zr, ss], [0.30, 0.10, 0.10], percent_type="vo", name="spent_fuel_smear")


fuel  = mat_spent_fuel()
canst = sc.mat_sa508("cask_canister")
gst   = sc.mat_sa508("cask_gamma_steel")
poly  = sc.mat_borated_poly(5.0, "cask_poly")
conc  = sc.mat_ordinary_concrete("cask_overpack")
air   = sc.mat_air("cask_air")
materials = openmc.Materials([fuel, canst, gst, poly, conc, air])

# ----------------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------------
cyl = {r: openmc.ZCylinder(r=r) for r in (R_FUEL, R_CAN, R_GAMMA, R_POLY, R_CONC, R_AIR)}
cyl[R_AIR].boundary_type = "vacuum"
ztop = openmc.ZPlane(z0= Z_BC, boundary_type="vacuum")
zbot = openmc.ZPlane(z0=-Z_BC, boundary_type="vacuum")
zspan = +zbot & -ztop


def shell(r_in, r_out, fill, name):
    reg = (-cyl[r_out] if r_in is None else (+cyl[r_in] & -cyl[r_out])) & zspan
    return openmc.Cell(name=name, fill=fill, region=reg)


cells = [
    shell(None,    R_FUEL,  fuel,  "fuel_basket"),
    shell(R_FUEL,  R_CAN,   canst, "canister"),
    shell(R_CAN,   R_GAMMA, gst,   "gamma_steel"),
    shell(R_GAMMA, R_POLY,  poly,  "borated_poly"),
    shell(R_POLY,  R_CONC,  conc,  "overpack"),
    shell(R_CONC,  R_AIR,   air,   "air"),
]
geometry = openmc.Geometry(openmc.Universe(cells=cells))

# ----------------------------------------------------------------------------
# Source
# ----------------------------------------------------------------------------
src_space = openmc.stats.CylindricalIndependent(
    r=openmc.stats.PowerLaw(0.0, R_FUEL, 1),
    phi=openmc.stats.Uniform(0.0, 2*np.pi),
    z=openmc.stats.Uniform(-Z_HALF, Z_HALF))

src_g, GAMMA_RATE = build_photon_source(src_space)
src_n = openmc.IndependentSource(
    space=src_space, energy=openmc.stats.Watt(), particle="neutron",
    strength=SF_NEUTRON_RATE)
S_TOTAL = GAMMA_RATE + SF_NEUTRON_RATE

# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
settings = openmc.Settings()
settings.run_mode = "fixed source"
settings.batches = sc.STAT["batches"]
settings.particles = sc.STAT["particles"]
settings.photon_transport = True
settings.source = [src_g, src_n]

ww_mesh = openmc.CylindricalMesh(
    r_grid=np.linspace(0.0, R_AIR, 30),
    z_grid=np.array([-Z_BC, -Z_HALF, 0.0, Z_HALF, Z_BC]),
    phi_grid=np.array([0.0, 2*np.pi]))
if USE_WW:
    sc.add_weight_windows(settings, ww_mesh, neutron=True, photon=True)

# ----------------------------------------------------------------------------
# Tallies — dose vs radius + the surface/1 m/2 m points
# ----------------------------------------------------------------------------
nr = 120
dose_mesh = openmc.CylindricalMesh(
    r_grid=np.linspace(0.0, R_AIR, nr + 1),
    z_grid=np.array([-50.0, 50.0]),
    phi_grid=np.array([0.0, 2*np.pi]))
dmesh_filter = openmc.MeshFilter(dose_mesh)

t_dose_n = openmc.Tally(name="dose_n")
t_dose_n.filters = [dmesh_filter, openmc.ParticleFilter("neutron"),
                    sc.dose_energy_filter("neutron")]
t_dose_n.scores = ["flux"]

t_dose_g = openmc.Tally(name="dose_g")
t_dose_g.filters = [dmesh_filter, openmc.ParticleFilter("photon"),
                    sc.dose_energy_filter("photon")]
t_dose_g.scores = ["flux"]

tallies = openmc.Tallies([t_dose_n, t_dose_g])
model = openmc.Model(geometry, materials, settings, tallies)


# ----------------------------------------------------------------------------
# Post-process
# ----------------------------------------------------------------------------
def _dose_at(rcen, dose_t, r_target):
    i = int(np.argmin(np.abs(rcen - r_target)))
    return dose_t[i]


def postprocess(sp_path):
    sp = openmc.StatePoint(sp_path)
    redges = np.linspace(0.0, R_AIR, nr + 1)
    rcen = 0.5 * (redges[:-1] + redges[1:])
    dz = 100.0
    vol = np.pi * (redges[1:]**2 - redges[:-1]**2) * dz

    dn = sp.get_tally(name="dose_n").mean.ravel()
    dg = sp.get_tally(name="dose_g").mean.ravel()
    dose_n = np.array([sc.flux_to_uSv_per_h(dn[i], vol[i], S_TOTAL) for i in range(nr)])
    dose_g = np.array([sc.flux_to_uSv_per_h(dg[i], vol[i], S_TOTAL) for i in range(nr)])
    dose_t = dose_n + dose_g

    with open(OUT / "doseB_vs_radius.csv", "w") as f:
        f.write("r_cm,dose_neutron_uSv_h,dose_gamma_uSv_h,dose_total_uSv_h\n")
        for i in range(nr):
            f.write(f"{rcen[i]:.3f},{dose_n[i]:.4e},{dose_g[i]:.4e},{dose_t[i]:.4e}\n")

    surf = _dose_at(rcen, dose_t, R_CONC + 1.0)
    d1m  = _dose_at(rcen, dose_t, R_CONC + 100.0)
    d2m  = _dose_at(rcen, dose_t, R_CONC + 200.0)
    v_surf = "PASS" if surf < sc.DOSE_CASK_SURFACE_USVH else "FAIL"
    v_2m   = "PASS" if d2m  < sc.DOSE_CASK_2M_USVH else "FAIL"

    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.semilogy(rcen, dose_t, "k-", lw=2, label="total")
        ax.semilogy(rcen, dose_n, "b--", label="neutron")
        ax.semilogy(rcen, dose_g, "r:", label="gamma")
        ax.axhline(sc.DOSE_CASK_SURFACE_USVH, color="orange", ls="-.", label="2 mSv/h surface")
        ax.axhline(sc.DOSE_CASK_2M_USVH, color="green", ls="-.", label="0.1 mSv/h @2 m")
        for r in (R_CONC,): ax.axvline(r, color="grey", lw=0.6)
        ax.set_xlabel("radius (cm)"); ax.set_ylabel("dose rate (uSv/h)")
        ax.set_title("Aegis-40 spent-fuel cask — dose vs radius (lead-free)")
        ax.legend(); ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout(); fig.savefig(OUT / "doseB_vs_radius.png", dpi=140)
    except Exception as e:
        print("plot skipped:", e)

    lines = [
        "Aegis-40 rev7 — TASK B spent-fuel cask summary (lead-free)",
        f"  source: {GAMMA_RATE:.3e} gamma/s + {SF_NEUTRON_RATE:.3e} n/s "
        f"(total {S_TOTAL:.3e} /s)",
        f"  surface (r={R_CONC:.0f} cm): {surf:.3e} uSv/h -> {v_surf} "
        f"(limit {sc.DOSE_CASK_SURFACE_USVH:.0f} = 2 mSv/h)",
        f"  1 m : {d1m:.3e} uSv/h",
        f"  2 m : {d2m:.3e} uSv/h -> {v_2m} (limit {sc.DOSE_CASK_2M_USVH:.0f} = 0.1 mSv/h)",
        "  refs: IAEA SSR-6 / 10 CFR 71",
    ]
    summary = "\n".join(lines)
    print(summary)
    (OUT / "doseB_summary.txt").write_text(summary, encoding="utf-8")
    sp.close()


if __name__ == "__main__":
    model.export_to_xml(str(OUT))
    openmc.run(cwd=str(OUT))
    sps = sorted(Path(OUT).glob("statepoint.*.h5"))
    postprocess(str(sps[-1]))
    print(f"\nOutputs in {OUT.resolve()}")
