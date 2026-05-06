"""
core_geometry.py
================
Defines the Aegis-40 SMR core geometry using the OpenMC Python API.

Geometry hierarchy
------------------
Level 1 – Fuel pin cell (fuel pellet + gap + clad + coolant)
Level 2 – 17×17 fuel assembly (with guide tubes and instrument tube)
Level 3 – Full reactor core (assemblies + reflector + pressure vessel)

All dimensions are in centimetres (cm).
"""

import openmc

# ---------------------------------------------------------------------------
# Aegis-40 core parameters
# ---------------------------------------------------------------------------
FUEL_OR = 0.4096       # fuel pellet outer radius (cm)
CLAD_IR = 0.4180       # cladding inner radius (cm)
CLAD_OR = 0.4750       # cladding outer radius (cm)
PIN_PITCH = 1.26       # pin-to-pin pitch (cm)
GUIDE_OR = 0.6020      # guide-tube outer radius (cm)
INSTR_OR = 0.4394      # instrument-tube outer radius (cm)
ASSEMBLY_PITCH = 21.42 # assembly pitch (cm)
ACTIVE_HEIGHT = 365.76 # active fuel height (cm)
ENRICHMENT = 4.25      # 235U enrichment (wt%)

N_PINS = 17            # pins per side of a fuel assembly


def make_materials():
    """Return an OpenMC Materials collection for the Aegis-40 core."""

    # UO2 fuel
    uo2 = openmc.Material(name="UO2 Fuel")
    uo2.set_density("g/cm3", 10.29640)
    uo2.add_nuclide("U234",  ENRICHMENT * 0.01 * 0.008, "wo")
    uo2.add_nuclide("U235",  ENRICHMENT * 0.01,          "wo")
    uo2.add_nuclide("U238", (1.0 - ENRICHMENT * 0.01 * 1.008), "wo")
    uo2.add_element("O", 0.11851, "wo")

    # Helium gap
    he_gap = openmc.Material(name="Helium Gap")
    he_gap.set_density("g/cm3", 0.001598)
    he_gap.add_element("He", 1.0, "ao")

    # Zircaloy-4 cladding
    zirc4 = openmc.Material(name="Zircaloy-4")
    zirc4.set_density("g/cm3", 6.55)
    zirc4.add_element("Zr", 0.98115, "wo")
    zirc4.add_element("Sn", 0.01450, "wo")
    zirc4.add_element("Fe", 0.00209, "wo")
    zirc4.add_element("Cr", 0.00100, "wo")
    zirc4.add_element("O",  0.00125, "wo")

    # Light water coolant/moderator at operating conditions (~310 °C, 155 bar)
    water = openmc.Material(name="Light Water")
    water.set_density("g/cm3", 0.7405)
    water.add_element("H", 2.0, "ao")
    water.add_element("O", 1.0, "ao")
    water.add_s_alpha_beta("c_H_in_H2O")

    # Stainless steel 304 (guide tubes, structural)
    ss304 = openmc.Material(name="SS304")
    ss304.set_density("g/cm3", 8.03)
    ss304.add_element("Fe", 0.68932, "wo")
    ss304.add_element("Cr", 0.19000, "wo")
    ss304.add_element("Ni", 0.09250, "wo")
    ss304.add_element("Mn", 0.02000, "wo")
    ss304.add_element("Si", 0.00750, "wo")
    ss304.add_element("C",  0.00068, "wo")

    materials = openmc.Materials([uo2, he_gap, zirc4, water, ss304])
    return materials


def make_fuel_pin_universe(uo2, he_gap, zirc4, water):
    """Return an OpenMC Universe representing a single fuel pin."""
    fuel_cyl  = openmc.ZCylinder(r=FUEL_OR)
    gap_cyl   = openmc.ZCylinder(r=CLAD_IR)
    clad_cyl  = openmc.ZCylinder(r=CLAD_OR)

    fuel_cell = openmc.Cell(name="Fuel Pellet",  fill=uo2,    region=-fuel_cyl)
    gap_cell  = openmc.Cell(name="Helium Gap",   fill=he_gap, region=+fuel_cyl & -gap_cyl)
    clad_cell = openmc.Cell(name="Cladding",     fill=zirc4,  region=+gap_cyl  & -clad_cyl)
    cool_cell = openmc.Cell(name="Pin Coolant",  fill=water,  region=+clad_cyl)

    pin_universe = openmc.Universe(name="Fuel Pin",
                                   cells=[fuel_cell, gap_cell, clad_cell, cool_cell])
    return pin_universe


def make_guide_tube_universe(zirc4, water):
    """Return an OpenMC Universe representing a guide tube (empty, water-filled)."""
    gt_cyl = openmc.ZCylinder(r=GUIDE_OR)

    water_cell = openmc.Cell(name="Guide Tube Water", fill=water,  region=-gt_cyl)
    cool_cell  = openmc.Cell(name="Guide Tube Cool",  fill=water,  region=+gt_cyl)

    gt_universe = openmc.Universe(name="Guide Tube",
                                  cells=[water_cell, cool_cell])
    return gt_universe


def make_assembly_universe(pin_univ, gt_univ):
    """
    Return a 17×17 fuel assembly Universe.

    The standard 17×17 PWR layout has 264 fuel rods, 24 guide tubes, and
    1 instrument tube at the centre.  Guide tube positions are approximated
    here using the standard Westinghouse-type map.
    """
    # Guide tube lattice indices (row, col), 0-based in a 17×17 grid
    guide_positions = {
        (2, 5), (2, 8), (2, 11),
        (5, 2), (5, 5), (5, 8), (5, 11), (5, 14),
        (8, 2), (8, 5),          (8, 11), (8, 14),
        (11, 2), (11, 5), (11, 8), (11, 11), (11, 14),
        (14, 5), (14, 8), (14, 11),
        (2, 14), (14, 2),
        (8, 8),   # instrument tube (centre)
    }

    lattice = openmc.RectLattice(name="17x17 Assembly Lattice")
    lattice.lower_left = [-PIN_PITCH * N_PINS / 2.0] * 2
    lattice.pitch = [PIN_PITCH, PIN_PITCH]

    universes = []
    for row in range(N_PINS):
        row_univs = []
        for col in range(N_PINS):
            if (row, col) in guide_positions:
                row_univs.append(gt_univ)
            else:
                row_univs.append(pin_univ)
        universes.append(row_univs)
    lattice.universes = universes

    # Bounding box for the assembly
    half = ASSEMBLY_PITCH / 2.0
    assembly_box = openmc.model.RectangularPrism(ASSEMBLY_PITCH, ASSEMBLY_PITCH)

    assembly_cell    = openmc.Cell(name="Assembly Lattice", fill=lattice,
                                   region=-assembly_box)
    assembly_universe = openmc.Universe(name="Fuel Assembly",
                                        cells=[assembly_cell])
    return assembly_universe


def make_core_geometry(materials):
    """
    Build and return the full Aegis-40 core Geometry.

    A 3×3 array of fuel assemblies is used as a simplified representative
    core.  For full-core analysis replace with the actual core loading map.
    """
    uo2, he_gap, zirc4, water, ss304 = (
        materials[0], materials[1], materials[2], materials[3], materials[4]
    )

    pin_univ  = make_fuel_pin_universe(uo2, he_gap, zirc4, water)
    gt_univ   = make_guide_tube_universe(zirc4, water)
    asm_univ  = make_assembly_universe(pin_univ, gt_univ)

    N_ASM = 3  # assemblies per side (simplified; full core uses more)
    core_pitch = ASSEMBLY_PITCH * N_ASM

    core_lattice = openmc.RectLattice(name="Core Lattice")
    core_lattice.lower_left = [-core_pitch / 2.0] * 2
    core_lattice.pitch = [ASSEMBLY_PITCH, ASSEMBLY_PITCH]
    core_lattice.universes = [[asm_univ] * N_ASM for _ in range(N_ASM)]

    # Axial bounds
    bot_plane = openmc.ZPlane(z0=0.0,            boundary_type="vacuum")
    top_plane = openmc.ZPlane(z0=ACTIVE_HEIGHT,  boundary_type="vacuum")

    # Radial boundary – cylindrical reactor vessel (simplified)
    vessel_r = core_pitch * 0.72
    vessel_cyl = openmc.ZCylinder(r=vessel_r, boundary_type="vacuum")

    core_region = -vessel_cyl & +bot_plane & -top_plane

    core_cell = openmc.Cell(name="Core", fill=core_lattice, region=core_region)
    root_universe = openmc.Universe(name="Root Universe", cells=[core_cell])

    geometry = openmc.Geometry(root_universe)
    return geometry


def build_model(export=False):
    """
    Build and optionally export the complete Aegis-40 geometry model.

    Parameters
    ----------
    export : bool
        If True, write materials.xml and geometry.xml to the working directory.

    Returns
    -------
    materials : openmc.Materials
    geometry  : openmc.Geometry
    """
    materials = make_materials()
    geometry  = make_core_geometry(materials)

    if export:
        materials.export_to_xml()
        geometry.export_to_xml()
        print("Exported materials.xml and geometry.xml")

    return materials, geometry


if __name__ == "__main__":
    build_model(export=True)
    print("Aegis-40 core geometry built successfully.")
