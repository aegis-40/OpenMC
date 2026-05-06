"""
reactivity_coefficients.py
===========================
Reactivity coefficient calculations for the Aegis-40 SMR using OpenMC.

Calculates:
  * Moderator Temperature Coefficient (MTC)  – dk/dT_mod  (pcm/°C)
  * Fuel Temperature / Doppler Coefficient   – dk/dT_fuel (pcm/°C)
  * Void Coefficient                         – dk/d(void%) (pcm/%void)

Method
------
Each coefficient is estimated by performing two eigenvalue calculations at
perturbed conditions and applying a finite-difference formula:

    α ≈ Δρ / ΔT  where  ρ = (k-1)/k  and  Δρ is in pcm (= ×10⁵)

Usage
-----
    python src/reactivity/reactivity_coefficients.py

Output
------
Prints coefficient values to stdout.
statepoint files for each perturbed calculation.
"""

import os
import copy
import openmc
from src.geometry.core_geometry import (
    build_model,
    ACTIVE_HEIGHT,
    FUEL_OR,
    CLAD_OR,
)

# ---------------------------------------------------------------------------
# Perturbation magnitudes
# ---------------------------------------------------------------------------
DELTA_T_MOD  = 10.0   # moderator temperature step (°C)
DELTA_T_FUEL = 100.0  # fuel temperature step (°C) – larger for Doppler
DELTA_VOID   = 10.0   # void fraction step (%)

# Nominal operating conditions
T_MOD_NOM  = 583.15   # K  (~310 °C)
T_FUEL_NOM = 900.0    # K  (average fuel temperature)
VOID_NOM   = 0.0      # % void (PWR nominal – no void)

PARTICLES      = 5_000
INACTIVE       = 30
ACTIVE_BATCHES = 70


def _run_keff(materials, geometry, run_dir, tag):
    """Export and run a single k-eff calculation; return (k, σ)."""
    os.makedirs(run_dir, exist_ok=True)
    orig = os.getcwd()
    os.chdir(run_dir)
    try:
        settings = openmc.Settings()
        settings.run_mode  = "eigenvalue"
        settings.inactive  = INACTIVE
        settings.batches   = INACTIVE + ACTIVE_BATCHES
        settings.particles = PARTICLES

        bbox = geometry.bounding_box
        settings.source = openmc.IndependentSource(
            space=openmc.stats.Box(
                [bbox[0][0], bbox[0][1], 0.0],
                [bbox[1][0], bbox[1][1], ACTIVE_HEIGHT],
            ),
            constraints={"fissionable": True},
        )
        model = openmc.Model(geometry=geometry, materials=materials,
                             settings=settings)
        model.export_to_model_xml()
        sp_path = model.run()
        with openmc.StatePoint(sp_path) as sp:
            k   = sp.keff.nominal_value
            sig = sp.keff.std_dev
        print(f"  [{tag}] k = {k:.5f} ± {sig:.5f}")
        return k, sig
    finally:
        os.chdir(orig)


def _reactivity(k):
    """Convert k-eff to reactivity in pcm."""
    return (k - 1.0) / k * 1e5


def calc_moderator_temperature_coefficient(base_dir="."):
    """
    Estimate the Moderator Temperature Coefficient (MTC).

    Perturbs the water density and temperature to simulate a ±ΔT change.
    """
    print("\n--- Moderator Temperature Coefficient (MTC) ---")
    results = {}
    for delta, tag in [(-DELTA_T_MOD / 2, "low"), (+DELTA_T_MOD / 2, "high")]:
        t_new = T_MOD_NOM + delta
        # Approximate density change: ρ ∝ (1 - 0.0004·ΔT) for water near 310 °C
        rho_new = 0.7405 * (1.0 - 0.0004 * delta)

        materials, geometry = build_model()
        for mat in materials:
            if mat.name == "Light Water":
                mat.set_density("g/cm3", max(rho_new, 0.01))
                mat.temperature = t_new

        run_dir = os.path.join(base_dir, f"mtc_{tag}")
        k, sig = _run_keff(materials, geometry, run_dir, f"MTC {tag}")
        results[tag] = (k, sig)

    k_lo, _ = results["low"]
    k_hi, _ = results["high"]
    mtc = (_reactivity(k_lo) - _reactivity(k_hi)) / DELTA_T_MOD
    print(f"MTC ≈ {mtc:+.1f} pcm/°C")
    return mtc


def calc_doppler_coefficient(base_dir="."):
    """
    Estimate the Fuel Temperature (Doppler) Coefficient.

    Perturbs the fuel temperature while keeping moderator unchanged.
    """
    print("\n--- Fuel Temperature (Doppler) Coefficient ---")
    results = {}
    for delta, tag in [(-DELTA_T_FUEL / 2, "low"), (+DELTA_T_FUEL / 2, "high")]:
        t_new = T_FUEL_NOM + delta

        materials, geometry = build_model()
        for mat in materials:
            if "Fuel" in mat.name:
                mat.temperature = t_new

        run_dir = os.path.join(base_dir, f"doppler_{tag}")
        k, sig = _run_keff(materials, geometry, run_dir, f"Doppler {tag}")
        results[tag] = (k, sig)

    k_lo, _ = results["low"]
    k_hi, _ = results["high"]
    dpc = (_reactivity(k_lo) - _reactivity(k_hi)) / DELTA_T_FUEL
    print(f"Doppler coefficient ≈ {dpc:+.1f} pcm/°C")
    return dpc


def calc_void_coefficient(base_dir="."):
    """
    Estimate the Void Coefficient.

    Perturbs the void fraction of the moderator (water density × (1 - void%)).
    """
    print("\n--- Void Coefficient ---")
    results = {}
    for void_pct, tag in [(VOID_NOM, "nominal"), (VOID_NOM + DELTA_VOID, "voided")]:
        rho_new = 0.7405 * (1.0 - void_pct / 100.0)

        materials, geometry = build_model()
        for mat in materials:
            if mat.name == "Light Water":
                mat.set_density("g/cm3", max(rho_new, 0.001))

        run_dir = os.path.join(base_dir, f"void_{tag}")
        k, sig = _run_keff(materials, geometry, run_dir, f"Void {tag}")
        results[tag] = (k, sig)

    k_nom, _ = results["nominal"]
    k_voi, _ = results["voided"]
    vc = (_reactivity(k_voi) - _reactivity(k_nom)) / DELTA_VOID
    print(f"Void coefficient ≈ {vc:+.1f} pcm/%void")
    return vc


def run_all_coefficients(base_dir="reactivity_runs"):
    """Run all three reactivity coefficient calculations."""
    os.makedirs(base_dir, exist_ok=True)
    mtc = calc_moderator_temperature_coefficient(base_dir)
    dpc = calc_doppler_coefficient(base_dir)
    vc  = calc_void_coefficient(base_dir)

    print("\n========== Reactivity Coefficient Summary ==========")
    print(f"  MTC (Moderator Temperature)  : {mtc:+.1f} pcm/°C")
    print(f"  DPC (Doppler / Fuel Temp)    : {dpc:+.1f} pcm/°C")
    print(f"  Void Coefficient             : {vc:+.1f} pcm/%void")
    print("====================================================")
    return {"MTC": mtc, "DPC": dpc, "Void": vc}


if __name__ == "__main__":
    run_all_coefficients()
