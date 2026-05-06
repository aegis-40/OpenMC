"""
test_geometry.py
================
Unit tests for the Aegis-40 core geometry module.

These tests verify that the geometry and materials are constructed correctly
without requiring a full OpenMC Monte Carlo run or nuclear data library.
"""

import sys
import os

# Ensure repo root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import openmc
from src.geometry.core_geometry import (
    make_materials,
    make_fuel_pin_universe,
    make_guide_tube_universe,
    make_assembly_universe,
    make_core_geometry,
    build_model,
    FUEL_OR,
    CLAD_IR,
    CLAD_OR,
    PIN_PITCH,
    ENRICHMENT,
    ACTIVE_HEIGHT,
    N_PINS,
    ASSEMBLY_PITCH,
)


class TestMaterials:
    """Tests for make_materials()."""

    def setup_method(self):
        self.materials = make_materials()

    def test_returns_materials_collection(self):
        assert isinstance(self.materials, openmc.Materials)

    def test_correct_number_of_materials(self):
        assert len(self.materials) == 5

    def test_material_names(self):
        names = {m.name for m in self.materials}
        assert "UO2 Fuel"     in names
        assert "Helium Gap"   in names
        assert "Zircaloy-4"   in names
        assert "Light Water"  in names
        assert "SS304"        in names

    def test_uo2_density(self):
        uo2 = next(m for m in self.materials if m.name == "UO2 Fuel")
        assert abs(uo2.density - 10.29640) < 1e-4

    def test_water_density(self):
        water = next(m for m in self.materials if m.name == "Light Water")
        assert abs(water.density - 0.7405) < 1e-4

    def test_uo2_has_uranium_nuclides(self):
        uo2 = next(m for m in self.materials if m.name == "UO2 Fuel")
        nuclide_names = [nuc for nuc, *_ in uo2.nuclides]
        assert "U235" in nuclide_names
        assert "U238" in nuclide_names

    def test_enrichment_order_of_magnitude(self):
        """U235 mass fraction should be close to the nominal enrichment."""
        uo2 = next(m for m in self.materials if m.name == "UO2 Fuel")
        # nuclides is list of (name, percent, percent_type)
        u235_entry = next(
            (n for n in uo2.nuclides if n[0] == "U235"), None
        )
        assert u235_entry is not None
        # wo fraction × 100 should be within ±1% of the enrichment value
        assert abs(u235_entry[1] * 100 - ENRICHMENT) < 1.0


class TestFuelPinUniverse:
    """Tests for make_fuel_pin_universe()."""

    def setup_method(self):
        materials = make_materials()
        uo2, he_gap, zirc4, water, ss304 = list(materials)
        self.pin_univ = make_fuel_pin_universe(uo2, he_gap, zirc4, water)

    def test_returns_universe(self):
        assert isinstance(self.pin_univ, openmc.Universe)

    def test_has_four_cells(self):
        assert len(self.pin_univ.cells) == 4

    def test_cell_names(self):
        names = {c.name for c in self.pin_univ.cells.values()}
        assert "Fuel Pellet" in names
        assert "Cladding"    in names


class TestGuideTubeUniverse:
    def setup_method(self):
        materials = make_materials()
        zirc4 = next(m for m in materials if m.name == "Zircaloy-4")
        water = next(m for m in materials if m.name == "Light Water")
        self.gt_univ = make_guide_tube_universe(zirc4, water)

    def test_returns_universe(self):
        assert isinstance(self.gt_univ, openmc.Universe)

    def test_has_two_cells(self):
        assert len(self.gt_univ.cells) == 2


class TestAssemblyUniverse:
    def setup_method(self):
        materials = make_materials()
        uo2, he_gap, zirc4, water, ss304 = list(materials)
        pin_univ = make_fuel_pin_universe(uo2, he_gap, zirc4, water)
        gt_univ  = make_guide_tube_universe(zirc4, water)
        self.asm_univ = make_assembly_universe(pin_univ, gt_univ)

    def test_returns_universe(self):
        assert isinstance(self.asm_univ, openmc.Universe)


class TestCoreGeometry:
    def setup_method(self):
        self.materials = make_materials()
        self.geometry  = make_core_geometry(self.materials)

    def test_returns_geometry(self):
        assert isinstance(self.geometry, openmc.Geometry)

    def test_root_universe_exists(self):
        assert self.geometry.root_universe is not None

    def test_bounding_box_z_span(self):
        bbox = self.geometry.bounding_box
        # Lower z should be at or below 0; upper at or above ACTIVE_HEIGHT
        assert bbox[0][2] <= 0.0
        assert bbox[1][2] >= ACTIVE_HEIGHT


class TestCoreConstants:
    """Sanity checks on the physical constants in core_geometry."""

    def test_fuel_radius_lt_clad_ir(self):
        assert FUEL_OR < CLAD_IR

    def test_clad_ir_lt_clad_or(self):
        assert CLAD_IR < CLAD_OR

    def test_clad_fits_in_pitch(self):
        assert CLAD_OR < PIN_PITCH / 2.0

    def test_enrichment_realistic_range(self):
        assert 0.71 < ENRICHMENT < 20.0  # above natural, below HEU

    def test_active_height_realistic(self):
        assert 200.0 < ACTIVE_HEIGHT < 500.0

    def test_n_pins_is_17(self):
        assert N_PINS == 17


class TestBuildModel:
    def test_build_returns_materials_and_geometry(self):
        materials, geometry = build_model(export=False)
        assert isinstance(materials, openmc.Materials)
        assert isinstance(geometry, openmc.Geometry)
