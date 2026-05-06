"""
burnup_simulation.py
====================
Burnup / depletion simulation for the Aegis-40 SMR using OpenMC.

Uses the OpenMC coupled neutronics–depletion solver (CoupledOperator) to
evolve the fuel composition through a series of irradiation and decay steps.

Usage
-----
    python src/depletion/burnup_simulation.py

Output
------
depletion_results.h5  – OpenMC depletion results file containing nuclide
                         inventories, k-eff, and source rates at each step.
"""

import os
import numpy as np
import openmc
import openmc.deplete
from src.geometry.core_geometry import build_model, ACTIVE_HEIGHT, ENRICHMENT

# ---------------------------------------------------------------------------
# Reactor operating parameters
# ---------------------------------------------------------------------------
THERMAL_POWER_MW  = 300.0          # total thermal power (MWt)
N_ASSEMBLIES      = 157            # number of fuel assemblies (full core)
POWER_PER_ASM_W   = (THERMAL_POWER_MW * 1e6) / N_ASSEMBLIES  # W per assembly

# Depletion schedule (days)
# 18-month fuel cycle → ~547 days; use coarse steps for speed
TIMESTEPS_DAYS = np.array([
    1, 5, 10, 20,          # startup / short-term
    30, 60, 90,            # first month
    180, 365,              # mid-cycle
    547,                   # end-of-cycle
])
TIMESTEP_SECONDS = TIMESTEPS_DAYS * 86400.0  # convert to seconds

PARTICLES       = 5_000
INACTIVE        = 30
ACTIVE_BATCHES  = 70


def make_depletion_settings(geometry):
    """Return Settings configured for depletion (eigenvalue + low particles)."""
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
    return settings(output_dir=".", export_only=False):
    """
    Build the model and execute the depletion calculation.

    Parameters
    ----------
    output_dir  : str  Working directory for XML input/output files.
    export_only : bool If True, export XML only (do not run OpenMC).

    Returns
    -------
    results : openmc.deplete.Results (only when not export_only)
    """
    os.makedirs(output_dir, exist_ok=True)
    orig_dir = os.getcwd()
    os.chdir(output_dir)

    try:
        materials, geometry = build_model()
        settings = make_depletion_settings(geometry)

        # Mark fuel material as depletable
        for mat in materials:
            if "Fuel" in mat.name:
                mat.depletable = True

        model = openmc.Model(geometry=geometry, materials=materials,
                             settings=settings)
        model.export_to_model_xml()
        print(f"Model XML exported to: {output_dir}")

        if export_only:
            return None

        # Build the coupled operator
        operator = openmc.deplete.CoupledOperator(
            model,
            chain_file=openmc.config.get("chain_file", "chain_endfb80.xml"),
        )

        # Predictor–corrector (CE/LI) integrator
        integrator = openmc.deplete.CELIIntegrator(
            operator,
            timesteps=TIMESTEP_SECONDS.tolist(),
            power=POWER_PER_ASM_W,
        )

        integrator.integrate()

        results = openmc.deplete.Results.from_hdf5("depletion_results.h5")
        print(f"Depletion complete – {len(results)} time steps saved.")

        # Print k-eff vs. burnup summary
        times, keffs = results.get_keff()
        burnups = times / 86400.0  # seconds → days
        print("\n{:<10s} {:<12s} {:<12s}".format("Day", "k-eff", "±1σ"))
        for day, (k, sig) in zip(burnups, keffs):
            print(f"{day:<10.1f} {k:<12.5f} {sig:<12.5f}")

        return results
    finally:
        os.chdir(orig_dir)


if __name__ == "__main__":
    run_depletion()
