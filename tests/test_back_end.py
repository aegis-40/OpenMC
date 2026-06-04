"""Tests for the pure-Python back-end waste-analysis modules (no OpenMC needed)."""

from __future__ import annotations

import math

import pytest

from aegis40.back_end import (
    CoreCycleSpec,
    DischargeInventory,
    NUCLIDE_DATA,
    WasteClass,
    activity_bq,
    aggregate,
    classify,
    compute_arisings,
    decay,
    evolution,
)
from aegis40.back_end.source_term import YEAR_S


# ----------------------------- fuel_cycle ---------------------------------

def _aegis_spec(burnup: float = 46.0, **kw) -> CoreCycleSpec:
    base = dict(
        hm_mass_t=5.6,
        n_assemblies=21,
        n_batches=4,
        thermal_power_mwt=125.0,
        electric_power_mwe=40.0,
        cycle_length_efpd=500.0,
        discharge_burnup_gwd_t=burnup,
        capacity_factor=0.9,
    )
    base.update(kw)
    return CoreCycleSpec(**base)


def test_arisings_basic_bookkeeping() -> None:
    a = compute_arisings(_aegis_spec())
    assert a.hm_per_cycle_t == pytest.approx(5.6 / 4)
    assert a.assemblies_per_cycle == pytest.approx(21 / 4)
    # electric energy: 40 MW * 500 d * 24 h / 1e6 = 0.48 TWh
    assert a.electric_twh_per_cycle == pytest.approx(40.0 * 500.0 * 24.0 / 1e6)
    assert a.hm_t_per_twhe == pytest.approx(a.hm_per_cycle_t / a.electric_twh_per_cycle)
    assert a.calendar_days_per_cycle == pytest.approx(500.0 / 0.9)


def test_higher_burnup_lowers_waste_intensity() -> None:
    """The core waste-reduction argument: more burnup -> less tHM per TWhe.

    Longer burnup means a proportionally longer cycle for the same core, so each
    discharged tHM yields more energy.
    """
    low = compute_arisings(_aegis_spec(burnup=33.0, cycle_length_efpd=360.0))
    high = compute_arisings(_aegis_spec(burnup=46.0, cycle_length_efpd=500.0))
    assert high.hm_t_per_twhe < low.hm_t_per_twhe


def test_arisings_rejects_bad_inputs() -> None:
    with pytest.raises(ValueError):
        compute_arisings(_aegis_spec(n_batches=0))
    with pytest.raises(ValueError):
        compute_arisings(_aegis_spec(capacity_factor=0.0))


# ----------------------------- source_term --------------------------------

def test_cs137_specific_activity() -> None:
    """1 g of Cs-137 ~ 3.2 TBq (known specific activity)."""
    a = activity_bq(1.0, "Cs137")
    assert a == pytest.approx(3.2e12, rel=0.05)


def test_unknown_nuclide_has_zero_activity() -> None:
    assert activity_bq(1.0, "Xx999") == 0.0


def test_aggregate_sums_and_reports_components() -> None:
    grams = {"Cs137": 1.0, "Sr90": 1.0}
    tot = aggregate(grams)
    assert tot.activity_bq > 0.0
    assert tot.decay_heat_w > 0.0
    assert tot.radiotoxicity_sv > 0.0
    assert set(tot.by_nuclide_activity_bq) == {"Cs137", "Sr90"}
    assert tot.activity_bq == pytest.approx(
        sum(tot.by_nuclide_activity_bq.values())
    )


def test_decay_one_half_life_halves_mass() -> None:
    t_half = NUCLIDE_DATA["Cs137"].half_life_s
    out = decay({"Cs137": 1.0}, t_half)
    assert out["Cs137"] == pytest.approx(0.5, rel=1e-9)


def test_decay_preserves_unknown_nuclides() -> None:
    out = decay({"Xx999": 2.0}, 1.0e9)
    assert out["Xx999"] == 2.0


def test_evolution_activity_monotonic_for_single_nuclide() -> None:
    times = [0.0, YEAR_S, 10 * YEAR_S, 100 * YEAR_S]
    curve = evolution({"Cs137": 10.0}, times)
    acts = [c.activity_bq for c in curve]
    assert acts == sorted(acts, reverse=True)  # strictly decreasing
    assert curve[0].cooling_time_yr == pytest.approx(0.0)


def test_discharge_inventory_known_unknown_split() -> None:
    inv = DischargeInventory(grams={"Cs137": 1.0, "FooBar": 2.0})
    assert inv.known() == {"Cs137": 1.0}
    assert inv.unknown() == ["FooBar"]


# ----------------------------- classification -----------------------------

def test_heat_generating_is_hlw() -> None:
    res = classify(specific_activity_bq_per_g=1e9, decay_heat_w_per_m3=3000.0)
    assert res.waste_class is WasteClass.HLW


def test_long_lived_low_heat_is_ilw() -> None:
    res = classify(
        specific_activity_bq_per_g=1e3,
        decay_heat_w_per_m3=0.0,
        dominant_half_life_s=24110 * YEAR_S,  # Pu-239
    )
    assert res.waste_class is WasteClass.ILW


def test_short_lived_moderate_is_llw() -> None:
    res = classify(
        specific_activity_bq_per_g=1e4,
        decay_heat_w_per_m3=0.0,
        dominant_half_life_s=5.0 * YEAR_S,
    )
    assert res.waste_class is WasteClass.LLW


def test_negligible_activity_is_exempt() -> None:
    assert classify(0.0).waste_class is WasteClass.EW


def test_classify_rejects_negative() -> None:
    with pytest.raises(ValueError):
        classify(-1.0)
