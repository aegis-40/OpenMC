"""
Aegis-40 — rev7 SHIELDING common library
=========================================
Shared materials, flux-to-dose response, source rates, and post-processing
helpers for the two shielding models:

  * aegis40_shielding_v7.py  — Task A, operational radial biological shield
  * aegis40_cask_v7.py       — Task B, spent-fuel dry-cask shield

DESIGN CHOICES (per team constraints, 2026-06-16)
-------------------------------------------------
* LEAD-FREE.  Lead is toxic (handling/disposal burden) — excluded everywhere.
* Tungsten is only used where compactness/weight truly dominates (transport).
  For the *stationary* biological shield (Task A) it is too expensive, so the
  bulk gamma+neutron shield is HEAVY (MAGNETITE) CONCRETE — cheap, lead-free,
  and contains bound water that also moderates fast neutrons.
* The layering follows the two optimization papers:
    - Ogul et al. (2026), SMART multilayer: steel / water / steel ... high-Z.
    - Bagheri & Khalafi (2023), GA shield: water+steel inner, poly outer,
      design criterion = total (n+gamma) dose < 10 uSv/h behind the last layer.
  We keep their *architecture* (steel+water inner -> borated-poly + concrete
  outer) but swap their lead/tungsten outer high-Z for heavy concrete.

Cross-section data: ENDF/B-VIII.0 with PHOTON data (photon transport ON).
"""

import math
import numpy as np
import openmc

# ----------------------------------------------------------------------------
# 0 · Physical constants / source normalisation
# ----------------------------------------------------------------------------
CORE_POWER_MWT   = 125.0
E_FISSION_J      = 200.0e6 * 1.602176634e-19          # J per fission (~3.204e-11)
NU_BAR           = 2.44                                # neutrons per fission
GAMMAS_PER_FISS  = 7.2                                 # prompt + short-lived FP gammas
FISSIONS_PER_S   = CORE_POWER_MWT * 1e6 / E_FISSION_J  # ~3.90e18 /s
NEUTRON_RATE     = NU_BAR        * FISSIONS_PER_S       # ~9.5e18 n/s  (Task A)
FISS_GAMMA_RATE  = GAMMAS_PER_FISS * FISSIONS_PER_S     # ~2.8e19 g/s  (Task A)

# Regulatory dose criteria ----------------------------------------------------
DOSE_TARGET_OPERATIONAL_USVH = 10.0     # Bagheri&Khalafi / ALARA design target
DOSE_CASK_SURFACE_USVH       = 2000.0   # IAEA SSR-6 / 10 CFR 71: 2 mSv/h surface
DOSE_CASK_2M_USVH            = 100.0    # IAEA SSR-6 / 10 CFR 71: 0.1 mSv/h @ 2 m

# ----------------------------------------------------------------------------
# 1 · Material library (lead-free)
# ----------------------------------------------------------------------------
def mat_water(temp=300.0, density=1.0, name="water"):
    m = openmc.Material(name=name, temperature=temp)
    m.set_density("g/cm3", density)
    m.add_element("H", 2.0)
    m.add_element("O", 1.0)
    m.add_s_alpha_beta("c_H_in_H2O")
    return m


def mat_air(name="air"):
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 0.001205)
    m.add_element("N", 0.7553, percent_type="wo")
    m.add_element("O", 0.2318, percent_type="wo")
    m.add_element("Ar", 0.0129, percent_type="wo")
    return m


def mat_ss304(name="SS304"):
    """Core barrel / thermal shield / cask gamma steel."""
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 8.00)
    m.add_element("Fe", 0.685, percent_type="wo")
    m.add_element("Cr", 0.190, percent_type="wo")
    m.add_element("Ni", 0.095, percent_type="wo")
    m.add_element("Mn", 0.020, percent_type="wo")
    m.add_element("Si", 0.010, percent_type="wo")
    return m


def mat_sa508(name="SA508_RPV"):
    """SA-508 Gr.3 low-alloy carbon steel — reactor pressure vessel wall."""
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 7.90)
    m.add_element("Fe", 0.9685, percent_type="wo")
    m.add_element("Mn", 0.0140, percent_type="wo")
    m.add_element("Ni", 0.0075, percent_type="wo")
    m.add_element("Mo", 0.0050, percent_type="wo")
    m.add_element("Si", 0.0025, percent_type="wo")
    m.add_element("Cr", 0.0003, percent_type="wo")
    m.add_element("C",  0.0022, percent_type="wo")
    return m


def mat_borated_poly(boron_wt=5.0, name="borated_PE"):
    """Borated polyethylene — thermal-neutron capture layer (low secondary gamma
    vs steel capture).  CH2 base + boron."""
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 0.95)
    pe = 1.0 - boron_wt / 100.0
    m.add_element("C", pe * 0.8563, percent_type="wo")
    m.add_element("H", pe * 0.1437, percent_type="wo")
    m.add_element("B", boron_wt / 100.0, percent_type="wo")
    return m


def mat_magnetite_concrete(name="magnetite_concrete"):
    """Heavy (magnetite-aggregate) concrete, rho ~3.9 g/cm3.  Bulk lead-free
    gamma + neutron shield for the biological wall."""
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 3.90)
    m.add_element("H",  0.0036, percent_type="wo")
    m.add_element("O",  0.3100, percent_type="wo")
    m.add_element("Mg", 0.0089, percent_type="wo")
    m.add_element("Al", 0.0042, percent_type="wo")
    m.add_element("Si", 0.0223, percent_type="wo")
    m.add_element("Ca", 0.0628, percent_type="wo")
    m.add_element("Ti", 0.0067, percent_type="wo")
    m.add_element("Mn", 0.0010, percent_type="wo")
    m.add_element("Fe", 0.5805, percent_type="wo")
    return m


def mat_ordinary_concrete(name="ordinary_concrete"):
    """Ordinary (Portland) concrete, rho ~2.3 g/cm3 — outer finish / cask overpack."""
    m = openmc.Material(name=name)
    m.set_density("g/cm3", 2.30)
    m.add_element("H",  0.0056, percent_type="wo")
    m.add_element("O",  0.4983, percent_type="wo")
    m.add_element("Na", 0.0171, percent_type="wo")
    m.add_element("Mg", 0.0024, percent_type="wo")
    m.add_element("Al", 0.0456, percent_type="wo")
    m.add_element("Si", 0.3158, percent_type="wo")
    m.add_element("K",  0.0192, percent_type="wo")
    m.add_element("Ca", 0.0826, percent_type="wo")
    m.add_element("Fe", 0.0122, percent_type="wo")
    return m


def mat_homogenized_core(enrich=4.69, name="homog_core"):
    """Volume-smeared active core (UO2 fuel + Zr clad + borated-free water) used
    as the SOURCE region for the operational shielding model.  Standard practice:
    a shielding model does not need pin resolution, only the correct leakage
    spectrum and integrated source strength."""
    uo2 = openmc.Material(name="core_uo2")
    uo2.set_density("g/cm3", 10.40)
    uo2.add_element("U", 1.0, enrichment=enrich)
    uo2.add_element("O", 2.0)

    zr = openmc.Material(name="core_clad")
    zr.set_density("g/cm3", 6.55)
    zr.add_element("Zr", 1.0)

    h2o = mat_water(temp=575.0, density=0.72266, name="core_water")

    # 17x17 PWR pin-cell volume fractions (fuel/clad/moderator)
    frac_fuel, frac_clad, frac_water = 0.331, 0.116, 0.553
    core = openmc.Material.mix_materials(
        [uo2, zr, h2o], [frac_fuel, frac_clad, frac_water],
        percent_type="vo", name=name)
    core.temperature = 900.0
    return core


# ----------------------------------------------------------------------------
# 2 · Flux-to-dose (ICRP-116, anterior-posterior — conservative)
# ----------------------------------------------------------------------------
def dose_energy_filter(particle):
    """EnergyFunctionFilter that converts flux -> effective dose using ICRP-116
    AP fluence-to-dose coefficients shipped with OpenMC (units: pSv*cm^2)."""
    e, d = openmc.data.dose_coefficients(particle, geometry="AP")
    return openmc.EnergyFunctionFilter(e, d)


def flux_to_uSv_per_h(flux_tally_mean, cell_volume_cm3, source_rate_per_s):
    """Convert a dose-weighted flux tally (pSv*cm^3 per source particle) to uSv/h.

    tally(score='flux', filter=dose_energy_filter) = integral_V integral_E
        phi(E) * d(E) dE dV    [pSv*cm^2 * (cm per src)] = pSv*cm^3 / src
    -> /V (cm^3)               = pSv / src
    -> *source_rate (src/s)    = pSv / s
    -> *3600 / 1e6             = uSv / h
    """
    pSv_per_src = flux_tally_mean / cell_volume_cm3
    pSv_per_s = pSv_per_src * source_rate_per_s
    return pSv_per_s * 3600.0 / 1.0e6


# ----------------------------------------------------------------------------
# 3 · Statistics profiles  (LOWER stats by default — bump for report numbers)
# ----------------------------------------------------------------------------
STAT_FAST   = dict(batches=20,  particles=20_000)    # smoke test (~minutes)
STAT_MEDIUM = dict(batches=40,  particles=100_000)   # working draft
STAT_FINAL  = dict(batches=100, particles=500_000)   # appendix-grade

# Default for the handoff = FAST (Laziz bumps to MEDIUM/FINAL once it runs).
STAT = STAT_FAST


def add_weight_windows(settings, mesh, neutron=True, photon=True):
    """Attach MAGIC iterative weight-window generators so deep-penetration dose
    actually converges at low particle counts.  If your OpenMC build rejects
    this API, set USE_WW=False in the driver script and raise the stats."""
    e_n = np.logspace(-3, 7.2, 12)     # eV bounds for the WW energy groups
    gens = []
    if neutron:
        g = openmc.WeightWindowGenerator(
            mesh=mesh, energy_bounds=e_n, particle_type="neutron")
        g.update_parameters = {"ratio": 5.0, "threshold": 1.0, "value": "mean"}
        gens.append(g)
    if photon:
        g = openmc.WeightWindowGenerator(
            mesh=mesh, energy_bounds=e_n, particle_type="photon")
        g.update_parameters = {"ratio": 5.0, "threshold": 1.0, "value": "mean"}
        gens.append(g)
    settings.weight_window_generators = gens
    settings.weight_windows_on = True
    settings.max_history_splits = 1_000_000
    return settings
