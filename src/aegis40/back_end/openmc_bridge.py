"""OpenMC bridge for the back-end analysis (lazy ``openmc`` import).

This is the ONLY back-end module that touches OpenMC, and it imports ``openmc``
*inside* each function so the rest of ``aegis40.back_end`` (and its tests) work on
machines without OpenMC. These functions run in the WSL/Linux OpenMC environment
alongside ``aegis40_3d_core_notebook.ipynb``.

Three jobs, matching the three §4.3.2-mandated waste analyses:

1. :func:`discharge_grams_from_results` — pull the discharged heavy-metal +
   fission-product inventory (grams/nuclide) out of a depletion ``Results`` file,
   to feed :mod:`aegis40.back_end.source_term`.
2. :func:`run_decay_only` — rigorous chain-coupled decay-heat / activity vs.
   cooling time (zero-power depletion of the discharged material).
3. :func:`build_storage_rack_model` — a spent-fuel storage-rack / cask OpenMC
   model for the storage-criticality (k_eff, burnup-credit) safety case.

NOTE: :func:`discharge_grams_from_results`, :func:`run_decay_only` and
:func:`decay_curves_from_results` are VALIDATED against live OpenMC 0.15.3
(2026-06-04, via ``scripts/extract_discharge_inventory.py`` and
``scripts/run_decay_heat.py``): the decay run reproduces ANS-consistent shutdown
decay heat (7.75 MW ≈ 6.2% of 125 MWth). Callers must set
``openmc.config['chain_file']`` so ``get_decay_heat``/``get_activity`` can load
decay data, and pass ``nuc_with_data`` to ``Results.export_to_materials`` to skip
the cross-sections lookup. :func:`build_storage_rack_model` is VALIDATED against
live OpenMC 0.15.3 (2026-06-04, via ``scripts/run_storage_criticality.py``): it
collects every geometry material (so the assembly fuel/clad survive into the
Model), gives the water bound-hydrogen thermal scattering, and wraps its root in
a Universe. All three §4.3.2 waste analyses now run end-to-end.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable, Sequence

if TYPE_CHECKING:  # pragma: no cover - typing only, no runtime openmc dependency
    import openmc
    import openmc.deplete


def discharge_grams_from_results(
    results_path: str,
    fuel_material_ids: Iterable[str | int] | None = None,
    step_index: int = -1,
    nuclides: Iterable[str] | None = None,
) -> dict[str, float]:
    """Sum grams of each nuclide across the fuel materials at a depletion step.

    Parameters
    ----------
    results_path:
        Path to ``depletion_results.h5``.
    fuel_material_ids:
        Material IDs to include. If ``None``, every depletable material in the
        results is summed (the whole discharged core inventory).
    step_index:
        Depletion step to read; ``-1`` = end of life (discharge).
    nuclides:
        Restrict to these nuclides; ``None`` = all nuclides in the results.

    Returns
    -------
    dict mapping nuclide name (OpenMC style, e.g. ``"Cs137"``) -> grams.
    """
    import openmc.deplete  # lazy

    results = openmc.deplete.Results(results_path)

    # Discover material ids present in the results if not supplied.
    if fuel_material_ids is None:
        mats = _result_material_ids(results)
    else:
        mats = [str(m) for m in fuel_material_ids]

    grams: dict[str, float] = {}
    for mat_id in mats:
        mat_id = str(mat_id)
        nuc_list = list(nuclides) if nuclides is not None else _result_nuclides(results, mat_id)
        for nuc in nuc_list:
            # get_mass returns (times, mass[g]) for a (material, nuclide).
            # Validated against OpenMC 0.15.3 (2026-06-04).
            try:
                _, mass = results.get_mass(mat_id, nuc)
            except Exception:
                continue
            g = float(mass[step_index])
            if g > 0.0:
                grams[nuc] = grams.get(nuc, 0.0) + g
    return grams


def _result_material_ids(results: "openmc.deplete.Results") -> list[str]:
    """Best-effort discovery of depletable material ids in a Results object."""
    # The materials are recoverable from the first StepResult's index map.
    # Validated against OpenMC 0.15.3 (2026-06-04): 6 depletable materials.
    try:
        return [str(m) for m in results[0].index_mat]
    except Exception as exc:  # pragma: no cover - depends on runtime object
        raise RuntimeError(
            "Could not enumerate materials from Results; pass fuel_material_ids "
            "explicitly (the depletable material ids from the build_core model)."
        ) from exc


def _result_nuclides(results: "openmc.deplete.Results", mat_id: str) -> list[str]:
    # Validated against OpenMC 0.15.3 (2026-06-04): 3820 nuclides in the chain.
    try:
        return list(results[0].index_nuc)
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Could not enumerate nuclides from Results; pass nuclides explicitly."
        ) from exc


def _zero_microxs(chain_file: str, n_materials: int) -> list:
    """A list of all-zero ``MicroXS`` (one per material) for a decay-only run.

    With ``fluxes=0`` the reaction rates are zero regardless of the cross
    sections, so we only need a *validly shaped* ``MicroXS``. Shape conventions
    differ across OpenMC versions (2-D ``(nuclides, reactions)`` vs legacy 3-D
    ``(nuclides, reactions, 1)``) so both are tried.
    """
    import numpy as np

    import openmc.deplete  # lazy

    chain = openmc.deplete.Chain.from_xml(chain_file)
    nuclides = [nuc.name for nuc in chain.nuclides]
    reactions = ["(n,gamma)"]
    errors = []
    for shape in ((len(nuclides), len(reactions)),
                  (len(nuclides), len(reactions), 1)):
        try:
            mx = openmc.deplete.MicroXS(np.zeros(shape), nuclides, reactions)
            return [mx] * n_materials
        except Exception as exc:  # noqa: BLE001
            errors.append(f"shape {shape}: {exc!r}")
    raise RuntimeError("MicroXS construction failed; tried " + " | ".join(errors))


def run_decay_only(
    discharged_materials: "openmc.Material | Iterable[openmc.Material]",
    cooling_times_s: Sequence[float],
    chain_file: str,
    out_dir: str = "back_end_decay",
) -> str:
    """Zero-power depletion of the discharged material(s) -> rigorous decay curves.

    Uses ``IndependentOperator`` with zero flux so no transport is run: the chain
    alone evolves the inventory, capturing in-growth (Pu-241 -> Am-241, etc.) and
    the full short-lived fission-product set that the curated
    :func:`aegis40.back_end.source_term.decay` omits. Post-process the resulting
    ``depletion_results.h5`` with :func:`decay_curves_from_results`.

    ``cooling_times_s`` are **interval** lengths between successive output points
    (PredictorIntegrator semantics), not cumulative times.

    Returns the path to the decay ``depletion_results.h5``.
    """
    import os

    import openmc  # lazy
    import openmc.deplete

    if isinstance(discharged_materials, openmc.Material):
        materials = openmc.Materials([discharged_materials])
    else:
        materials = openmc.Materials(list(discharged_materials))
    n = len(materials)

    operator = openmc.deplete.IndependentOperator(
        materials,
        fluxes=[0.0] * n,                  # zero flux -> decay only
        micros=_zero_microxs(chain_file, n),
        chain_file=chain_file,
        normalization_mode="source-rate",
    )
    integrator = openmc.deplete.PredictorIntegrator(
        operator,
        timesteps=list(cooling_times_s),
        source_rates=[0.0] * len(cooling_times_s),
        timestep_units="s",
    )
    old = os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)
    try:
        integrator.integrate()
    finally:
        os.chdir(old)
    return os.path.join(out_dir, "depletion_results.h5")


def decay_curves_from_results(results_path: str) -> dict:
    """Total decay heat (W) and activity (Bq) vs cooling time from a decay run.

    Sums ``Results.get_decay_heat`` and ``Results.get_activity`` over all
    materials in the decay ``depletion_results.h5``. Returns a dict with
    ``times_s``, ``decay_heat_w`` and ``activity_bq`` lists.
    """
    import numpy as np

    import openmc.deplete  # lazy

    results = openmc.deplete.Results(results_path)
    mats = [str(m) for m in results[0].index_mat]

    times = None
    heat_total = None
    act_total = None
    for mat in mats:
        t, h = results.get_decay_heat(mat, units="W")
        _, a = results.get_activity(mat, units="Bq")
        times = t
        heat_total = h if heat_total is None else heat_total + h
        act_total = a if act_total is None else act_total + a
    return {
        "times_s": list(np.asarray(times)),
        "decay_heat_w": list(np.asarray(heat_total)),
        "activity_bq": list(np.asarray(act_total)),
    }


def build_storage_rack_model(
    assembly_universe_factory: Callable[[], "openmc.Universe"],
    n_rows: int,
    n_cols: int,
    storage_pitch_cm: float,
    *,
    moderator_density_g_cm3: float = 1.0,
    boron_ppm: float = 0.0,
    reflective: bool = False,
    settings: dict[str, Any] | None = None,
) -> "openmc.Model":
    """Spent-fuel storage-rack criticality model (k_eff, FER §8.11 safety case).

    A ``n_rows`` x ``n_cols`` array of spent-fuel assemblies on ``storage_pitch_cm``
    in (optionally borated) water, used to demonstrate sub-criticality of the
    storage configuration. ``assembly_universe_factory`` returns one fuel-assembly
    universe — pass the *discharged* (burnup-credit) assembly for a credit case,
    or the fresh assembly for the conservative bounding case.

    ``reflective=True`` models an effectively infinite rack (most conservative);
    ``False`` puts a water reflector + vacuum BC around a finite array.
    """
    import openmc  # lazy

    water = openmc.Material(name="storage_water")
    water.add_nuclide("H1", 2.0)
    water.add_nuclide("O16", 1.0)
    if boron_ppm > 0.0:
        # ppm by mass of natural boron in the water
        water.add_element("B", boron_ppm * 1.0e-6, "wo")
    water.set_density("g/cm3", moderator_density_g_cm3)
    # Thermal scattering for bound hydrogen — essential for a correct k in a
    # water-moderated lattice (without it k is biased high by ~hundreds of pcm).
    water.add_s_alpha_beta("c_H_in_H2O")

    rack = openmc.RectLattice(name="storage_rack")
    rack.pitch = (storage_pitch_cm, storage_pitch_cm)
    rack.lower_left = (-n_cols * storage_pitch_cm / 2.0,
                       -n_rows * storage_pitch_cm / 2.0)
    rack.universes = [
        [assembly_universe_factory() for _ in range(n_cols)] for _ in range(n_rows)
    ]
    rack.outer = openmc.Universe(cells=[openmc.Cell(fill=water)])

    half_x = n_cols * storage_pitch_cm / 2.0
    half_y = n_rows * storage_pitch_cm / 2.0
    bc = "reflective" if reflective else "vacuum"
    margin = 0.0 if reflective else 30.0  # cm water reflector around a finite rack
    xlo = openmc.XPlane(-half_x - margin, boundary_type=bc)
    xhi = openmc.XPlane(+half_x + margin, boundary_type=bc)
    ylo = openmc.YPlane(-half_y - margin, boundary_type=bc)
    yhi = openmc.YPlane(+half_y + margin, boundary_type=bc)

    rack_cell = openmc.Cell(name="rack", fill=rack)
    root = openmc.Cell(name="storage_root", region=+xlo & -xhi & +ylo & -yhi)
    root.fill = openmc.Universe(cells=[rack_cell])
    geometry = openmc.Geometry(openmc.Universe(cells=[root]))

    s = openmc.Settings()
    s.run_mode = "eigenvalue"
    s.batches = (settings or {}).get("batches", 150)
    s.inactive = (settings or {}).get("inactive", 50)
    s.particles = (settings or {}).get("particles", 20000)

    # Collect every material referenced by the geometry (the assembly's fuel /
    # clad / gap / intra-assembly water from ``assembly_universe_factory`` plus
    # the rack water) — passing only ``[water]`` would drop the fuel materials
    # and OpenMC would fail to export a valid materials.xml.
    all_mats = list(geometry.get_all_materials().values())
    if water not in all_mats:
        all_mats.append(water)

    return openmc.Model(geometry=geometry, settings=s,
                        materials=openmc.Materials(all_mats))
