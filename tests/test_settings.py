"""
test_settings.py
================
Unit tests for the Settings objects produced by each simulation module.

These tests verify that the OpenMC Settings are constructed with the expected
parameters without requiring a live OpenMC installation to run simulations.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import openmc
from src.geometry.core_geometry import build_model
from src.criticality.keff_calculation import (
    make_settings as make_keff_settings,
    INACTIVE_BATCHES,
    ACTIVE_BATCHES,
    PARTICLES,
)
from src.flux.flux_distribution import (
    make_flux_settings,
    make_flux_tallies,
    N_AXIAL,
    N_RADIAL,
    MESH_NXY,
)


@pytest.fixture(scope="module")
def geometry():
    """Shared geometry object for all settings tests."""
    _, geom = build_model(export=False)
    return geom


class TestKeffSettings:
    def test_run_mode_is_eigenvalue(self, geometry):
        s = make_keff_settings(geometry)
        assert s.run_mode == "eigenvalue"

    def test_inactive_batches(self, geometry):
        s = make_keff_settings(geometry)
        assert s.inactive == INACTIVE_BATCHES

    def test_total_batches(self, geometry):
        s = make_keff_settings(geometry)
        assert s.batches == INACTIVE_BATCHES + ACTIVE_BATCHES

    def test_particles(self, geometry):
        s = make_keff_settings(geometry)
        assert s.particles == PARTICLES

    def test_source_is_independent(self, geometry):
        s = make_keff_settings(geometry)
        assert isinstance(s.source[0], openmc.IndependentSource)


class TestFluxSettings:
    def test_run_mode_is_eigenvalue(self, geometry):
        s = make_flux_settings(geometry)
        assert s.run_mode == "eigenvalue"

    def test_source_configured(self, geometry):
        s = make_flux_settings(geometry)
        assert len(s.source) > 0


class TestFluxTallies:
    def test_returns_tallies_object(self, geometry):
        t = make_flux_tallies(geometry)
        assert isinstance(t, openmc.Tallies)

    def test_tally_names_present(self, geometry):
        t = make_flux_tallies(geometry)
        names = {tally.name for tally in t}
        assert "Axial Flux"       in names
        assert "Radial Flux"      in names
        assert "2D Power Map"     in names
        assert "Neutron Spectrum" in names

    def test_axial_tally_has_flux_score(self, geometry):
        tallies = make_flux_tallies(geometry)
        axial = next(t for t in tallies if t.name == "Axial Flux")
        assert "flux" in axial.scores

    def test_xy_tally_has_fission_and_heating(self, geometry):
        tallies = make_flux_tallies(geometry)
        xy = next(t for t in tallies if t.name == "2D Power Map")
        assert "fission" in xy.scores
        assert "heating" in xy.scores
