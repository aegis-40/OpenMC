"""Discharge source term: activity, decay heat and radiotoxicity vs. cooling time.

Given a discharge inventory (grams of each nuclide, from the OpenMC depletion
run via :mod:`aegis40.back_end.openmc_bridge`), this computes the back-end source
term the FER §8.11 needs: total activity (Bq), decay-heat power (W) and ingestion
radiotoxicity (Sv), and their evolution over cooling time.

Fidelity note
-------------
The :func:`decay` evolution here is **independent exponential decay** of each
nuclide — a transparent quick-look. It deliberately ignores chain in-growth
(e.g. Pu-241 -> Am-241, which matters around 10-100 yr). The short-lived
secular-equilibrium daughters that dominate near-term heat (Y-90 with Sr-90,
Ba-137m with Cs-137) are folded into their parent's per-decay energy so the
near-term decay-heat curve is realistic. For the *rigorous* chain-coupled
evolution use ``openmc_bridge.run_decay_only`` (a zero-power depletion). Keep
both in the report and note the agreement.

``NUCLIDE_DATA`` is a curated subset of the nuclides that dominate LWR spent-fuel
heat, activity and radiotoxicity. Half-lives, per-decay recoverable energies and
ICRP-72 adult ingestion dose coefficients are rounded literature values; the
authoritative numbers for the submission come from the OpenMC decay/chain data.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

AVOGADRO = 6.02214076e23          # 1/mol
MEV_TO_J = 1.602176634e-13        # J per MeV
LN2 = math.log(2.0)
YEAR_S = 365.25 * 24.0 * 3600.0   # s in a Julian year
DAY_S = 24.0 * 3600.0


@dataclass(frozen=True)
class NuclideData:
    """Per-nuclide decay constants used by the source-term aggregation.

    ``decay_heat_mev`` is the *recoverable* energy deposited per parent decay,
    including short-lived secular-equilibrium daughters where folded in.
    """

    half_life_s: float
    molar_mass: float                 # g/mol (mass number is fine here)
    decay_heat_mev: float             # MeV per decay (recoverable)
    ingestion_sv_per_bq: float        # ICRP-72 adult ingestion dose coefficient

    @property
    def decay_constant(self) -> float:
        return LN2 / self.half_life_s


# nuclide: (T_half [yr], A [g/mol], E_recoverable [MeV/decay], ingestion [Sv/Bq])
_RAW: dict[str, tuple[float, float, float, float]] = {
    # --- dominant short/medium-term heat & activity (fission products) ---
    "Sr90":  (28.79, 90.0, 1.13, 2.8e-8),   # incl. Y-90 daughter
    "Cs137": (30.08, 137.0, 0.60, 1.3e-8),  # incl. Ba-137m daughter
    "Cs134": (2.065, 134.0, 1.55, 1.9e-8),
    "Eu154": (8.60, 154.0, 1.50, 2.0e-9),
    "Sm151": (90.0, 151.0, 0.0197, 9.8e-11),
    # --- long-lived mobile fission products (repository dose drivers) ---
    "Tc99":  (2.111e5, 99.0, 0.0846, 6.4e-10),
    "I129":  (1.57e7, 129.0, 0.19, 1.1e-7),
    # --- actinides (long-term heat & radiotoxicity) ---
    "Pu238": (87.7, 238.0, 5.59, 2.3e-7),
    "Pu239": (24110.0, 239.0, 5.24, 2.5e-7),
    "Pu240": (6561.0, 240.0, 5.26, 2.5e-7),
    "Pu241": (14.33, 241.0, 0.0052, 4.7e-9),   # beta; feeds Am-241 in-growth
    "Pu242": (3.75e5, 242.0, 4.98, 2.4e-7),
    "Am241": (432.6, 241.0, 5.49, 2.0e-7),
    "Am243": (7370.0, 243.0, 5.36, 2.0e-7),
    "Cm244": (18.1, 244.0, 5.90, 1.2e-7),
    "Np237": (2.144e6, 237.0, 4.96, 1.1e-7),
    "U234":  (2.455e5, 234.0, 4.86, 4.9e-8),
    "U235":  (7.04e8, 235.0, 4.68, 4.7e-8),
    "U236":  (2.342e7, 236.0, 4.57, 4.7e-8),
    "U238":  (4.468e9, 238.0, 4.27, 4.5e-8),
}

NUCLIDE_DATA: dict[str, NuclideData] = {
    name: NuclideData(half_life_s=t_yr * YEAR_S, molar_mass=m,
                      decay_heat_mev=e, ingestion_sv_per_bq=dose)
    for name, (t_yr, m, e, dose) in _RAW.items()
}


@dataclass
class DischargeInventory:
    """Grams of each nuclide at discharge (zero cooling time)."""

    grams: dict[str, float]
    hm_mass_t: float | None = None
    burnup_gwd_t: float | None = None

    def known(self) -> dict[str, float]:
        """Subset of the inventory for which decay data is available."""
        return {n: g for n, g in self.grams.items() if n in NUCLIDE_DATA}

    def unknown(self) -> list[str]:
        """Nuclides present in the inventory but missing from NUCLIDE_DATA."""
        return [n for n in self.grams if n not in NUCLIDE_DATA]


@dataclass(frozen=True)
class SourceTermTotals:
    """Aggregated source term at one cooling time."""

    cooling_time_s: float
    activity_bq: float
    decay_heat_w: float
    radiotoxicity_sv: float
    by_nuclide_activity_bq: dict[str, float] = field(default_factory=dict)

    @property
    def cooling_time_yr(self) -> float:
        return self.cooling_time_s / YEAR_S


def _atoms(grams: float, nd: NuclideData) -> float:
    return grams / nd.molar_mass * AVOGADRO


def activity_bq(grams: float, nuclide: str) -> float:
    """Activity (Bq) of ``grams`` of ``nuclide``; 0.0 if no decay data."""
    nd = NUCLIDE_DATA.get(nuclide)
    if nd is None or grams <= 0.0:
        return 0.0
    return nd.decay_constant * _atoms(grams, nd)


def aggregate(grams: dict[str, float], cooling_time_s: float = 0.0) -> SourceTermTotals:
    """Total activity / decay heat / radiotoxicity for an inventory.

    Only nuclides present in :data:`NUCLIDE_DATA` contribute; unknown nuclides
    are ignored (inspect with :meth:`DischargeInventory.unknown`).
    """
    act_total = heat_total = radtox_total = 0.0
    by_nuclide: dict[str, float] = {}
    for nuclide, g in grams.items():
        nd = NUCLIDE_DATA.get(nuclide)
        if nd is None or g <= 0.0:
            continue
        a = nd.decay_constant * _atoms(g, nd)
        by_nuclide[nuclide] = a
        act_total += a
        heat_total += a * nd.decay_heat_mev * MEV_TO_J
        radtox_total += a * nd.ingestion_sv_per_bq
    return SourceTermTotals(
        cooling_time_s=cooling_time_s,
        activity_bq=act_total,
        decay_heat_w=heat_total,
        radiotoxicity_sv=radtox_total,
        by_nuclide_activity_bq=by_nuclide,
    )


def decay(grams: dict[str, float], cooling_time_s: float) -> dict[str, float]:
    """Independent exponential decay of each known nuclide after ``cooling_time_s``.

    Nuclides without decay data pass through unchanged (no information to evolve
    them). See the module docstring for the in-growth caveat.
    """
    if cooling_time_s < 0.0:
        raise ValueError("cooling_time_s must be non-negative")
    out: dict[str, float] = {}
    for nuclide, g in grams.items():
        nd = NUCLIDE_DATA.get(nuclide)
        if nd is None:
            out[nuclide] = g
        else:
            out[nuclide] = g * math.exp(-nd.decay_constant * cooling_time_s)
    return out


def evolution(grams: dict[str, float], cooling_times_s: list[float]) -> list[SourceTermTotals]:
    """Source-term totals at each requested cooling time (quick-look decay curve)."""
    return [aggregate(decay(grams, t), cooling_time_s=t) for t in cooling_times_s]
