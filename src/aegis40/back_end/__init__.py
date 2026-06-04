"""Back-end fuel-cycle / waste-management analysis for Aegis-40 (FER §8.11).

Turns the discharge inventory from the OpenMC depletion run into the quantities
the competition's §4.3.2 requires:

* spent-fuel arisings (tHM & assemblies per cycle/year, tHM per TWhe) ............ ``fuel_cycle``
* discharge source term: activity, decay heat, radiotoxicity vs. cooling time .... ``source_term``
* indicative IAEA-style waste classification ..................................... ``classification``

The pure-Python parts above carry **no** OpenMC dependency and are unit-tested.
Everything that actually touches OpenMC (reading ``deplete.Results``, the
decay-only evolution, the spent-fuel storage-rack criticality model) lives in
``aegis40.back_end.openmc_bridge`` and imports ``openmc`` lazily, so this package
imports cleanly on machines without OpenMC installed.
"""

from __future__ import annotations

from .classification import WasteClass, classify
from .fuel_cycle import Arisings, CoreCycleSpec, compute_arisings
from .source_term import (
    NUCLIDE_DATA,
    DischargeInventory,
    NuclideData,
    SourceTermTotals,
    activity_bq,
    aggregate,
    decay,
    evolution,
)

__all__ = [
    # fuel_cycle
    "CoreCycleSpec",
    "Arisings",
    "compute_arisings",
    # source_term
    "NuclideData",
    "NUCLIDE_DATA",
    "DischargeInventory",
    "SourceTermTotals",
    "activity_bq",
    "aggregate",
    "decay",
    "evolution",
    # classification
    "WasteClass",
    "classify",
]
