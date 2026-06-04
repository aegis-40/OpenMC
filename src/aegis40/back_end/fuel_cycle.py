"""Spent-fuel arisings and waste-intensity bookkeeping (FER §8.11, fuel efficiency).

Pure arithmetic on top of the equilibrium fuel-cycle parameters that come out of
the OpenMC depletion / LRM analysis (``aegis40_3d_core_notebook.ipynb``). The
headline metric for the "reduce waste quantity" argument is **tHM discharged per
TWh of electricity**: higher burnup and longer cycles drive it down, which is
exactly the comparison to make against the reference reactor (CAREM-25).
"""

from __future__ import annotations

from dataclasses import dataclass

DAYS_PER_YEAR = 365.25


@dataclass(frozen=True)
class CoreCycleSpec:
    """Equilibrium fuel-cycle description for one core design point.

    ``cycle_length_efpd`` and ``discharge_burnup_gwd_t`` are the equilibrium
    (not fresh-core) values from the linear-reactivity model.
    """

    hm_mass_t: float                 # total heavy-metal loading of the core (tHM)
    n_assemblies: int                # fuel assemblies in the core
    n_batches: int                   # reload batches (n in the LRM)
    thermal_power_mwt: float
    electric_power_mwe: float
    cycle_length_efpd: float         # equilibrium cycle length, effective full-power days
    discharge_burnup_gwd_t: float    # equilibrium discharge burnup
    capacity_factor: float = 0.90    # EFPD -> calendar days (outages, deratings)

    @property
    def thermal_efficiency(self) -> float:
        return self.electric_power_mwe / self.thermal_power_mwt


@dataclass(frozen=True)
class Arisings:
    """Spent-fuel arisings derived from a :class:`CoreCycleSpec`."""

    hm_per_cycle_t: float
    assemblies_per_cycle: float
    calendar_days_per_cycle: float
    cycles_per_year: float
    hm_per_year_t: float
    assemblies_per_year: float
    electric_twh_per_cycle: float
    thermal_twh_per_cycle: float
    hm_t_per_twhe: float             # <-- waste-intensity headline metric
    hm_t_per_twhth: float

    def as_dict(self) -> dict[str, float]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


def compute_arisings(spec: CoreCycleSpec) -> Arisings:
    """Compute per-cycle and per-year spent-fuel arisings and waste intensity."""
    if spec.n_batches <= 0:
        raise ValueError("n_batches must be positive")
    if not 0.0 < spec.capacity_factor <= 1.0:
        raise ValueError("capacity_factor must be in (0, 1]")

    hm_per_cycle_t = spec.hm_mass_t / spec.n_batches
    assemblies_per_cycle = spec.n_assemblies / spec.n_batches

    # EFPD -> calendar time (refuelling outages reduce the realised duty)
    calendar_days_per_cycle = spec.cycle_length_efpd / spec.capacity_factor
    cycles_per_year = DAYS_PER_YEAR / calendar_days_per_cycle

    hm_per_year_t = hm_per_cycle_t * cycles_per_year
    assemblies_per_year = assemblies_per_cycle * cycles_per_year

    # Energy produced over one cycle. EFPD are full-power days, so thermal energy
    # is power x EFPD directly; electric via the plant efficiency.
    mwh_per_cycle_th = spec.thermal_power_mwt * spec.cycle_length_efpd * 24.0
    mwh_per_cycle_e = spec.electric_power_mwe * spec.cycle_length_efpd * 24.0
    thermal_twh_per_cycle = mwh_per_cycle_th / 1.0e6
    electric_twh_per_cycle = mwh_per_cycle_e / 1.0e6

    hm_t_per_twhe = hm_per_cycle_t / electric_twh_per_cycle
    hm_t_per_twhth = hm_per_cycle_t / thermal_twh_per_cycle

    return Arisings(
        hm_per_cycle_t=hm_per_cycle_t,
        assemblies_per_cycle=assemblies_per_cycle,
        calendar_days_per_cycle=calendar_days_per_cycle,
        cycles_per_year=cycles_per_year,
        hm_per_year_t=hm_per_year_t,
        assemblies_per_year=assemblies_per_year,
        electric_twh_per_cycle=electric_twh_per_cycle,
        thermal_twh_per_cycle=thermal_twh_per_cycle,
        hm_t_per_twhe=hm_t_per_twhe,
        hm_t_per_twhth=hm_t_per_twhth,
    )
