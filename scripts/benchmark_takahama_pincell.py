#!/usr/bin/env python3
"""Takahama-3 spent-fuel depletion benchmark — PIN-CELL calculation (Aegis-40 V&V).

EXPERIMENTAL VALIDATION (Tier 3) of our OpenMC depletion path against MEASURED
spent-fuel isotopics, per:

    OECD/NEA, "International Comparison of a Depletion Calculation Benchmark
    Devoted to Fuel Cycle Issues — Results from Phase 1 on UOx Fuels",
    NEA/NSC/DOC(2013)1 (Jan 2013).  Reference experiment: Takahama-3 PWR
    Post-Irradiation Examination (SFCOMPO), sample SF97-4, ~46 GWd/t.

EVERY number below is taken verbatim from Appendix B of that report (page/table
cited inline). Nothing is approximated. The only non-spec choice is SUBSTEPS
(how finely each constant-power irradiation period is sub-divided for the time
integrator) — that changes integration accuracy, NOT the specified physics
(power level and total duration per period are exact).

Run in WSL with the OpenMC conda env. ENDF/B-VIII.0 library + chain on ext4.
"""
from __future__ import annotations
import math
import os

import openmc
import openmc.deplete

# ----- data paths (ext4 = fast) ---------------------------------------------
EXT4 = os.path.expanduser("~/openmc_data")
XS = os.path.join(EXT4, "endfb-viii.0-hdf5", "cross_sections.xml")
CHAIN = os.path.join(EXT4, "chain_endfb80_pwr.xml")

# ----- knobs ----------------------------------------------------------------
PARTICLES = 10_000      # plenty: isotopics converge <1%, benchmark tol is 10%
BATCHES = 115
INACTIVE = 15
SEED = 1
SUBSTEPS = 6            # sub-divisions per full-power period (integrator only)
COOLING_YEARS = 3.96   # final decay step: samarium is measured at 3.96 y (Table A.5)
WORKDIR = os.path.join("docs", "competition", "digital-appendix", "takahama_pincell")


# ===== materials (NEA/NSC/DOC(2013)1, Appendix B) ===========================
def build_materials():
    # --- 4.1 wt% UO2 fuel — Table B.1 (p.114), atom/barn-cm -----------------
    fuel = openmc.Material(name="UO2 4.1% (Takahama SF97)")
    fuel.add_nuclide("U234", 9.1361e-06)
    fuel.add_nuclide("U235", 9.3472e-04)
    fuel.add_nuclide("U238", 2.1523e-02)
    fuel.add_element("O", 4.4935e-02)
    fuel.set_density("atom/b-cm", 9.1361e-06 + 9.3472e-04 + 2.1523e-02 + 4.4935e-02)
    fuel.temperature = 900.0          # §2.7 fuel temperature
    fuel.depletable = True

    # --- fuel clad (reduced-density Zircaloy) — Table B.3 (p.114) -----------
    clad = openmc.Material(name="Zircaloy clad (reduced density)")
    clad.add_element("Fe", 1.3225e-04)
    clad.add_element("Cr", 6.7643e-05)
    clad.add_element("Zr", 3.8310e-02)
    clad.set_density("atom/b-cm", 1.3225e-04 + 6.7643e-05 + 3.8310e-02)
    clad.temperature = 600.0          # §2.7 clad temperature

    # --- borated-water moderator — Table B.5 (p.115) -----------------------
    mod = openmc.Material(name="Borated water")
    mod.add_element("H", 4.8132e-02)
    mod.add_element("O", 2.4066e-02)
    mod.add_nuclide("B10", 3.6487e-06)
    mod.add_nuclide("B11", 1.4686e-05)
    mod.set_density("atom/b-cm", 4.8132e-02 + 2.4066e-02 + 3.6487e-06 + 1.4686e-05)
    mod.add_s_alpha_beta("c_H_in_H2O")
    mod.temperature = 576.0           # §2.7 moderator temperature

    return openmc.Materials([fuel, clad, mod]), fuel, clad, mod


# ===== geometry — cell calculation, Fig. B3 (p.113) =========================
def build_geometry(fuel, clad, mod):
    R_FUEL = 0.4025      # UO2 pellet radius (Fig. B3)
    R_CLAD = 0.475       # clad outer radius (Fig. B3)
    PITCH = 1.32485      # equivalent cell pitch (Fig. B3)

    r1 = openmc.ZCylinder(r=R_FUEL)
    r2 = openmc.ZCylinder(r=R_CLAD)
    box = openmc.model.RectangularPrism(PITCH, PITCH, boundary_type="reflective")

    c_fuel = openmc.Cell(name="fuel", fill=fuel, region=-r1)
    c_clad = openmc.Cell(name="clad", fill=clad, region=+r1 & -r2)
    c_mod = openmc.Cell(name="moderator", fill=mod, region=+r2 & -box)
    geom = openmc.Geometry([c_fuel, c_clad, c_mod])

    fuel.volume = math.pi * R_FUEL ** 2   # per 1 cm pin height (for power norm)
    return geom


# ===== irradiation history — Table B.7 (p.116) ==============================
# (start, stop, days, power W/gU). 3 cycles @ 38.6 W/gU, 2 downtimes @ 0.
HISTORY = [
    (385, 38.6),   # 26/01/90 -> 15/02/91  full power
    (88, 0.0),     # 15/02/91 -> 14/05/91  downtime
    (402, 38.6),   # 14/05/91 -> 19/06/92  full power
    (62, 0.0),     # 19/06/92 -> 20/08/92  downtime
    (406, 38.6),   # 20/08/92 -> 30/09/93  full power
]


def build_schedule():
    """Exact days/power from Table B.7; full-power periods sub-divided into
    SUBSTEPS equal pieces for integrator accuracy (total days & power exact)."""
    days, powers = [], []
    for ndays, p in HISTORY:
        if p > 0:
            for _ in range(SUBSTEPS):
                days.append(ndays / SUBSTEPS)
                powers.append(p)
        else:
            days.append(ndays)   # decay-only step, one piece
            powers.append(0.0)
    assert abs(sum(days) - sum(d for d, _ in HISTORY)) < 1e-6
    # discharge state is now the last step boundary; append a decay-only step to
    # 3.96 y so the samarium isotopics (Table A.5) can be compared.
    days.append(COOLING_YEARS * 365.25)
    powers.append(0.0)
    return days, powers


def main():
    openmc.config["cross_sections"] = XS
    openmc.config["chain_file"] = CHAIN

    mats, fuel, clad, mod = build_materials()
    geom = build_geometry(fuel, clad, mod)

    model = openmc.Model(geometry=geom, materials=mats)
    model.settings.particles = PARTICLES
    model.settings.batches = BATCHES
    model.settings.inactive = INACTIVE
    model.settings.seed = SEED
    # 576 K moderator is not a tabulated library temperature -> interpolate
    model.settings.temperature = {"method": "interpolation"}

    days, powers = build_schedule()
    print(f"[takahama] {len(days)} depletion steps; full-power days "
          f"{sum(d for d, p in HISTORY if p>0)}; target burnup ~46 GWd/t")

    os.makedirs(WORKDIR, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(WORKDIR)
    try:
        op = openmc.deplete.CoupledOperator(model, chain_file=CHAIN)
        # power_density in W/gHM == W/gU at BOL (spec gives 38.6 W/gU)
        integ = openmc.deplete.PredictorIntegrator(
            op, days, power_density=powers, timestep_units="d")
        integ.integrate()
    finally:
        os.chdir(cwd)
    print(f"[takahama] done -> {WORKDIR}/depletion_results.h5")


if __name__ == "__main__":
    raise SystemExit(main())
