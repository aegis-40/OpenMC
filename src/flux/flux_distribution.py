"""
flux_distribution.py
====================
Flux distribution tallies for the Aegis-40 SMR using OpenMC.

Computes:
  * Axial flux profile (along z-axis)
  * Radial flux profile (along r from core centre)
  * 2-D (x-y) power / flux map at core mid-plane
  * Energy spectrum (thermal, epithermal, fast groups)

Usage
-----
    python src/flux/flux_distribution.py

Output
------
statepoint.<batches>.h5  – Tally results (flux, fission rate, power).
Flux plots saved as PNG files (if matplotlib is available).
"""

import os
import numpy as np
import openmc
from src.geometry.core_geometry import build_model, ACTIVE_HEIGHT

# ---------------------------------------------------------------------------
# Tally mesh parameters
# ---------------------------------------------------------------------------
N_AXIAL     = 50          # axial mesh divisions
N_RADIAL    = 40          # radial bins for 1-D profile
MESH_NXY    = 50          # 2-D mesh resolution (NXY × NXY)

PARTICLES       = 10_000
INACTIVE        = 50
ACTIVE_BATCHES  = 150


def make_flux_tallies(geometry):
    """
    Build OpenMC tallies for axial, radial, 2-D, and spectral flux.

    Returns
    -------
    tallies : openmc.Tallies
    """
    tallies = openmc.Tallies()
    bbox    = geometry.bounding_box

    # ------------------------------------------------------------------
    # 1-D Axial flux tally (uniform mesh along z)
    # ------------------------------------------------------------------
    axial_mesh = openmc.RegularMesh(name="Axial Mesh")
    axial_mesh.dimension = [1, 1, N_AXIAL]
    axial_mesh.lower_left  = [bbox[0][0], bbox[0][1], 0.0]
    axial_mesh.upper_right = [bbox[1][0], bbox[1][1], ACTIVE_HEIGHT]

    axial_filter = openmc.MeshFilter(axial_mesh)
    axial_tally  = openmc.Tally(name="Axial Flux")
    axial_tally.filters = [axial_filter]
    axial_tally.scores  = ["flux", "fission"]
    tallies.append(axial_tally)

    # ------------------------------------------------------------------
    # 1-D Radial flux tally (cylindrical mesh)
    # ------------------------------------------------------------------
    r_max = max(abs(bbox[0][0]), abs(bbox[1][0]),
                abs(bbox[0][1]), abs(bbox[1][1]))
    radial_mesh = openmc.CylindricalMesh(
        r_grid=np.linspace(0.0, r_max, N_RADIAL + 1).tolist(),
        z_grid=[0.0, ACTIVE_HEIGHT],
        phi_grid=[0.0, 2.0 * np.pi],
    )
    radial_mesh.name = "Radial Mesh"

    radial_filter = openmc.MeshFilter(radial_mesh)
    radial_tally  = openmc.Tally(name="Radial Flux")
    radial_tally.filters = [radial_filter]
    radial_tally.scores  = ["flux", "fission"]
    tallies.append(radial_tally)

    # ------------------------------------------------------------------
    # 2-D (x-y) power map at core mid-plane
    # ------------------------------------------------------------------
    xy_mesh = openmc.RegularMesh(name="XY Power Map")
    xy_mesh.dimension    = [MESH_NXY, MESH_NXY, 1]
    mid_z = ACTIVE_HEIGHT / 2.0
    xy_mesh.lower_left   = [bbox[0][0], bbox[0][1], mid_z - 5.0]
    xy_mesh.upper_right  = [bbox[1][0], bbox[1][1], mid_z + 5.0]

    xy_filter = openmc.MeshFilter(xy_mesh)
    xy_tally  = openmc.Tally(name="2D Power Map")
    xy_tally.filters = [xy_filter]
    xy_tally.scores  = ["flux", "fission", "heating"]
    tallies.append(xy_tally)

    # ------------------------------------------------------------------
    # Energy spectrum tally (broad group structure)
    # ------------------------------------------------------------------
    energy_bins = np.logspace(-2, 7, 201)  # 200 groups, 0.01 eV – 10 MeV
    energy_filter = openmc.EnergyFilter(energy_bins)

    spectrum_tally = openmc.Tally(name="Neutron Spectrum")
    spectrum_tally.filters = [energy_filter]
    spectrum_tally.scores  = ["flux"]
    tallies.append(spectrum_tally)

    return tallies


def make_flux_settings(geometry):
    """Return Settings for the flux calculation (more particles for accuracy)."""
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
    settings.output = {"tallies": True}
    return settings


def plot_flux_results(sp_path, output_dir="."):
    """
    Read the statepoint and generate flux distribution plots.

    Parameters
    ----------
    sp_path    : str  Path to the statepoint HDF5 file.
    output_dir : str  Directory to save PNG plots.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available – skipping plots.")
        return

    with openmc.StatePoint(sp_path) as sp:
        # Axial flux
        axial_t = sp.get_tally(name="Axial Flux")
        flux_ax = axial_t.get_values(scores=["flux"]).ravel()
        z_centres = np.linspace(0.0, ACTIVE_HEIGHT, N_AXIAL)

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(z_centres, flux_ax / flux_ax.max(), color="steelblue", linewidth=2)
        ax.set_xlabel("Axial position z (cm)")
        ax.set_ylabel("Normalised flux (a.u.)")
        ax.set_title("Aegis-40 – Axial Flux Distribution")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(output_dir, "axial_flux.png"), dpi=150)
        plt.close(fig)
        print(f"Saved: {os.path.join(output_dir, 'axial_flux.png')}")

        # 2-D power map
        xy_t = sp.get_tally(name="2D Power Map")
        fiss_xy = xy_t.get_values(scores=["fission"]).reshape(MESH_NXY, MESH_NXY)

        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(fiss_xy, origin="lower", cmap="hot",
                       interpolation="nearest")
        plt.colorbar(im, ax=ax, label="Fission rate (a.u.)")
        ax.set_title("Aegis-40 – Radial Fission Rate (mid-plane)")
        ax.set_xlabel("x mesh index")
        ax.set_ylabel("y mesh index")
        fig.tight_layout()
        fig.savefig(os.path.join(output_dir, "power_map_2d.png"), dpi=150)
        plt.close(fig)
        print(f"Saved: {os.path.join(output_dir, 'power_map_2d.png')}")

        # Energy spectrum
        spec_t = sp.get_tally(name="Neutron Spectrum")
        flux_spec = spec_t.get_values(scores=["flux"]).ravel()
        energy_bins = np.logspace(-2, 7, 201)
        e_mid = 0.5 * (energy_bins[:-1] + energy_bins[1:])

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.loglog(e_mid, flux_spec, color="darkorange", linewidth=1.5)
        ax.set_xlabel("Neutron energy (eV)")
        ax.set_ylabel("Flux per unit lethargy (a.u.)")
        ax.set_title("Aegis-40 – Neutron Energy Spectrum")
        ax.grid(True, which="both", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(output_dir, "neutron_spectrum.png"), dpi=150)
        plt.close(fig)
        print(f"Saved: {os.path.join(output_dir, 'neutron_spectrum.png')}")


def run_flux_distribution(output_dir=".", export_only=False):
    """
    Build the model, run the eigenvalue calculation with flux tallies, and
    optionally plot the results.

    Parameters
    ----------
    output_dir  : str  Working directory.
    export_only : bool If True, only write XML files.
    """
    os.makedirs(output_dir, exist_ok=True)
    orig = os.getcwd()
    os.chdir(output_dir)

    try:
        materials, geometry = build_model()
        settings = make_flux_settings(geometry)
        tallies  = make_flux_tallies(geometry)

        model = openmc.Model(geometry=geometry, materials=materials,
                             settings=settings, tallies=tallies)
        model.export_to_model_xml()
        print(f"Model XML exported to: {output_dir}")

        if not export_only:
            sp_path = model.run()
            plot_flux_results(sp_path, output_dir)
    finally:
        os.chdir(orig)


if __name__ == "__main__":
    run_flux_distribution()
