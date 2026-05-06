"""
keff_calculation.py
===================
Criticality (k-effective) calculation for the Aegis-40 SMR using OpenMC.

Runs a fixed-source-free eigenvalue (k-eigenvalue) Monte Carlo simulation
to determine the effective multiplication factor (k-eff) of the reactor core
at hot full-power (HFP) operating conditions.

Usage
-----
    python src/criticality/keff_calculation.py

Output
------
statepoint.<batches>.h5  – OpenMC statepoint with k-eff and tally results.
"""

import os
import openmc
from src.geometry.core_geometry import build_model

# ---------------------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------------------
INACTIVE_BATCHES = 50    # batches discarded for source convergence
ACTIVE_BATCHES   = 150   # batches used for statistics
PARTICLES        = 10_000  # neutrons per batch


def make_settings(geometry):
    """Return an OpenMC Settings object configured for a k-eff calculation."""
    settings = openmc.Settings()
    settings.run_mode    = "eigenvalue"
    settings.inactive    = INACTIVE_BATCHES
    settings.batches     = INACTIVE_BATCHES + ACTIVE_BATCHES
    settings.particles   = PARTICLES

    # Initial source: uniform in the fuel region
    bbox = geometry.bounding_box
    lower = [bbox[0][0], bbox[0][1], 0.0]
    upper = [bbox[1][0], bbox[1][1], 365.76]
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box(lower, upper),
        constraints={"fissionable": True},
    )

    settings.output = {"tallies": False}
    return settings


def make_tallies():
    """Return an OpenMC Tallies object with basic k-eff convergence output."""
    # Track fission rate per batch for convergence diagnostics
    tally = openmc.Tally(name="Fission Rate")
    tally.scores = ["fission"]

    tallies = openmc.Tallies([tally])
    return tallies


def run_keff(output_dir=".", export_only=False):
    """
    Build the model and run the k-eff calculation.

    Parameters
    ----------
    output_dir  : str  Directory to write XML inputs and statepoint output.
    export_only : bool If True, only write XML files without running OpenMC.

    Returns
    -------
    keff_mean : float  Mean k-eff (only when not export_only)
    keff_unc  : float  1-sigma uncertainty on k-eff
    """
    os.makedirs(output_dir, exist_ok=True)
    orig_dir = os.getcwd()
    os.chdir(output_dir)

    try:
        materials, geometry = build_model()
        settings = make_settings(geometry)
        tallies  = make_tallies()

        model = openmc.Model(geometry=geometry, materials=materials,
                             settings=settings, tallies=tallies)
        model.export_to_model_xml()
        print(f"Model XML exported to: {output_dir}")

        if not export_only:
            sp_path = model.run()
            with openmc.StatePoint(sp_path) as sp:
                keff_mean = sp.keff.nominal_value
                keff_unc  = sp.keff.std_dev
            print(f"k-eff = {keff_mean:.5f} ± {keff_unc:.5f}")
            return keff_mean, keff_unc
    finally:
        os.chdir(orig_dir)

    return None, None


if __name__ == "__main__":
    run_keff()
