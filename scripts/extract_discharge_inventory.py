#!/usr/bin/env python3
"""Extract the Aegis-40 discharge inventory and build the FER §8.11 source term.

RUN THIS IN WSL (the OpenMC environment), not Windows. It does two jobs:

  1. **Validate the openmc_bridge accessors.** The bridge in
     ``src/aegis40/back_end/openmc_bridge.py`` was written against the documented
     OpenMC 0.15.x API but never executed (every risky line is marked
     ``# TODO(validate)``). This script probes the live ``deplete.Results`` object,
     reports which accessor names actually work, and tells you exactly what (if
     anything) to change in the bridge.

  2. **Produce the §8.11 source term.** It pulls grams/nuclide of the discharged
     core, feeds them through ``aegis40.back_end.source_term`` and
     ``classification``, and writes a Markdown report + CSV tables (FP/actinide
     inventory, decay-heat & radiotoxicity vs cooling time, waste class) into
     ``docs/competition/waste/``.

Usage (from the repo root, in WSL):

    PYTHONPATH=src python3 scripts/extract_discharge_inventory.py \
        [--results /mnt/d/.../08_depletion_baseline/depletion_results.h5] \
        [--hm-tonnes 5.6] [--outdir docs/competition/waste]

All paths default to the known WSL mount locations, so plain
``PYTHONPATH=src python3 scripts/extract_discharge_inventory.py`` should work.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import os
import sys

# --- defaults (WSL /mnt mounts of the Windows drives) -----------------------
DEFAULT_RESULTS = (
    "/mnt/d/conda-envs/openmc-py311/SMRs/Claude version/"
    "aegis40_3d_core_outputs/08_depletion_baseline/depletion_results.h5"
)
DEFAULT_OUTDIR = "docs/competition/waste"
DEFAULT_HM_T = 5.6  # core heavy-metal loading [t], for the sanity check

# Cooling times for the decay curves: discharge -> 100 kyr (repository horizon).
YEAR_S = 365.25 * 24.0 * 3600.0
COOLING_YEARS = [0.0, 1.0, 3.0, 5.0, 10.0, 30.0, 50.0, 100.0,
                 300.0, 1000.0, 10000.0, 100000.0]


# ---------------------------------------------------------------------------
# Bridge-accessor validation
# ---------------------------------------------------------------------------
def validate_accessors(results) -> dict:
    """Probe the live Results object; return a dict of what works.

    Mirrors every ``# TODO(validate)`` site in openmc_bridge.py.
    """
    report: dict[str, object] = {}

    # (1) enumerate materials -- bridge uses results[0].index_mat
    mats = None
    for expr, getter in (
        ("results[0].index_mat", lambda: list(results[0].index_mat)),
        ("results.get_depletable_materials()",
         lambda: list(results.get_depletable_materials())),
    ):
        try:
            mats = getter()
            report["materials_accessor"] = expr
            report["n_materials"] = len(mats)
            report["material_ids_sample"] = [str(m) for m in mats[:8]]
            break
        except Exception as exc:  # noqa: BLE001
            report.setdefault("materials_tried", []).append(f"{expr} -> {exc!r}")
    report["materials"] = mats

    # (2) enumerate nuclides -- bridge uses results[0].index_nuc
    nucs = None
    for expr, getter in (
        ("results[0].index_nuc", lambda: list(results[0].index_nuc)),
    ):
        try:
            nucs = getter()
            report["nuclides_accessor"] = expr
            report["n_nuclides"] = len(nucs)
            break
        except Exception as exc:  # noqa: BLE001
            report.setdefault("nuclides_tried", []).append(f"{expr} -> {exc!r}")
    report["nuclides"] = nucs

    # (3) per-(material,nuclide) mass -- bridge uses results.get_mass(mat, nuc)
    if mats and nucs:
        test_mat = str(mats[0])
        # pick a nuclide we expect to exist
        test_nuc = "U238" if "U238" in nucs else nucs[0]
        report["mass_probe_target"] = (test_mat, test_nuc)
        try:
            times, mass = results.get_mass(test_mat, test_nuc)
            report["mass_accessor"] = "results.get_mass(mat, nuc) -> (times, mass[g])"
            report["mass_probe_value_g"] = float(mass[-1])
            report["n_timesteps"] = len(times)
        except Exception as exc:  # noqa: BLE001
            report.setdefault("mass_tried", []).append(
                f"results.get_mass -> {exc!r}")
            # fallback: get_atoms * molar mass
            try:
                import openmc.data
                _, atoms = results.get_atoms(test_mat, test_nuc)
                m = openmc.data.atomic_mass(test_nuc)
                report["mass_accessor"] = (
                    "FALLBACK: results.get_atoms(mat, nuc) * "
                    "openmc.data.atomic_mass(nuc) / N_A")
                report["mass_probe_value_g"] = (
                    float(atoms[-1]) * m / 6.02214076e23)
            except Exception as exc2:  # noqa: BLE001
                report.setdefault("mass_tried", []).append(
                    f"results.get_atoms -> {exc2!r}")
    return report


# ---------------------------------------------------------------------------
# Inventory extraction
# ---------------------------------------------------------------------------
def extract_whole_core_grams(results, step_index: int = -1) -> dict:
    """Sum grams/nuclide over every depletable material at ``step_index``.

    Uses get_mass when available, else get_atoms * atomic_mass. Returns the
    whole-core inventory in grams (the depletion volumes were scaled to the full
    core in the notebook, so no extra pin-count scaling is applied here).
    """
    import openmc.data

    try:
        mats = [str(m) for m in results[0].index_mat]
    except Exception:
        mats = [str(m) for m in results.get_depletable_materials()]
    nucs = list(results[0].index_nuc)

    have_get_mass = hasattr(results, "get_mass")
    grams: dict[str, float] = {}
    for mat in mats:
        for nuc in nucs:
            try:
                if have_get_mass:
                    _, series = results.get_mass(mat, nuc)
                    g = float(series[step_index])
                else:
                    _, atoms = results.get_atoms(mat, nuc)
                    g = (float(atoms[step_index])
                         * openmc.data.atomic_mass(nuc) / 6.02214076e23)
            except Exception:  # noqa: BLE001
                continue
            if g > 0.0:
                grams[nuc] = grams.get(nuc, 0.0) + g
    return grams


def _heavy_metal_grams(grams: dict) -> float:
    """Total U+Np+Pu+Am+Cm grams (the actinide 'heavy metal')."""
    hm_elems = ("U", "Np", "Pu", "Am", "Cm", "Th", "Pa")
    total = 0.0
    for nuc, g in grams.items():
        sym = "".join(c for c in nuc if c.isalpha())
        if sym in hm_elems:
            total += g
    return total


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def write_report(grams, validation, outdir, results_path, hm_t_nominal):
    from aegis40.back_end import (
        DischargeInventory,
        aggregate,
        classify,
        evolution,
    )
    from aegis40.back_end.source_term import NUCLIDE_DATA

    os.makedirs(outdir, exist_ok=True)
    inv = DischargeInventory(grams=grams, hm_mass_t=hm_t_nominal)
    known = inv.known()
    unknown = inv.unknown()

    hm_g = _heavy_metal_grams(grams)
    total_g = sum(grams.values())

    # source term at discharge + the cooling-time curve
    t0 = aggregate(grams, 0.0)
    curve = evolution(grams, [y * YEAR_S for y in COOLING_YEARS])

    # bulk classification of the spent fuel (UO2 ~ 10.4 g/cc fuel density)
    fuel_density_g_cm3 = 10.4
    vol_cm3 = total_g / fuel_density_g_cm3 if total_g else 1.0
    spec_act = t0.activity_bq / total_g if total_g else 0.0          # Bq/g
    heat_density = t0.decay_heat_w / (vol_cm3 * 1e-6) if vol_cm3 else 0.0  # W/m3
    cls = classify(spec_act, decay_heat_w_per_m3=heat_density)

    # ---- CSV: per-nuclide activity at discharge (known nuclides) ----
    by_act = sorted(t0.by_nuclide_activity_bq.items(),
                    key=lambda kv: kv[1], reverse=True)
    with io.open(os.path.join(outdir, "discharge_inventory.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["nuclide", "grams", "activity_Bq", "half_life_yr"])
        for nuc, act in by_act:
            nd = NUCLIDE_DATA[nuc]
            w.writerow([nuc, f"{grams.get(nuc, 0.0):.6e}", f"{act:.6e}",
                        f"{nd.half_life_s / YEAR_S:.4g}"])

    # ---- CSV: source term vs cooling time ----
    with io.open(os.path.join(outdir, "source_term_vs_cooling.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cooling_yr", "activity_Bq", "decay_heat_W",
                    "radiotoxicity_Sv"])
        for yr, st in zip(COOLING_YEARS, curve):
            w.writerow([f"{yr:g}", f"{st.activity_bq:.6e}",
                        f"{st.decay_heat_w:.6e}", f"{st.radiotoxicity_sv:.6e}"])

    # ---- Markdown report ----
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    L: list[str] = []
    L.append("# Aegis-40 discharge source term (FER §8.11) — generated\n")
    L.append(f"- Generated: `{now}`")
    L.append(f"- Depletion results: `{results_path}`")
    L.append(f"- Nominal core HM loading: {hm_t_nominal} t\n")

    L.append("## Bridge-accessor validation\n")
    L.append("| probe | result |")
    L.append("|---|---|")
    L.append(f"| materials accessor | `{validation.get('materials_accessor', 'FAILED')}` "
             f"({validation.get('n_materials', '?')} materials) |")
    L.append(f"| nuclides accessor | `{validation.get('nuclides_accessor', 'FAILED')}` "
             f"({validation.get('n_nuclides', '?')} nuclides) |")
    L.append(f"| mass accessor | `{validation.get('mass_accessor', 'FAILED')}` |")
    L.append(f"| timesteps in results | {validation.get('n_timesteps', '?')} |")
    if validation.get("materials_tried"):
        L.append(f"\n_materials fallbacks tried:_ {validation['materials_tried']}")
    if validation.get("mass_tried"):
        L.append(f"\n_mass fallbacks tried:_ {validation['mass_tried']}")
    L.append("")

    L.append("## Inventory totals\n")
    L.append(f"- Total mass tracked: **{total_g / 1e6:.4f} t** "
             f"({total_g:.3e} g)")
    L.append(f"- Heavy metal (U+Np+Pu+Am+Cm): **{hm_g / 1e6:.4f} t** "
             f"(nominal {hm_t_nominal} t — ratio {hm_g / 1e6 / hm_t_nominal:.3f})")
    L.append(f"- Nuclides tracked: {len(grams)}; "
             f"with decay data: {len(known)}; without: {len(unknown)}")
    if abs(hm_g / 1e6 / hm_t_nominal - 1.0) > 0.1:
        L.append(f"- ⚠️ HM mass is off nominal by >10% — check whether the "
                 f"depletion volumes are whole-core or need pin-count scaling.")
    L.append("")

    L.append("## Source term at discharge (0 yr cooling)\n")
    L.append(f"- Total activity: **{t0.activity_bq:.3e} Bq** "
             f"({t0.activity_bq / 3.7e10:.3e} Ci)")
    L.append(f"- Decay heat: **{t0.decay_heat_w:.3e} W** "
             f"({t0.decay_heat_w / max(hm_g / 1e6, 1e-9):.3e} W/tHM)")
    L.append(f"- Ingestion radiotoxicity: **{t0.radiotoxicity_sv:.3e} Sv**")
    L.append(f"- Bulk specific activity: {spec_act:.3e} Bq/g; "
             f"heat density ~{heat_density:.3e} W/m³")
    L.append(f"- **Waste class (bulk SNF): {cls.waste_class.name}** "
             f"— {getattr(cls, 'rationale', '')}")
    L.append("")

    L.append("### Top nuclides by activity at discharge\n")
    L.append("| nuclide | grams | activity (Bq) | T½ (yr) |")
    L.append("|---|---|---|---|")
    for nuc, act in by_act[:15]:
        nd = NUCLIDE_DATA[nuc]
        L.append(f"| {nuc} | {grams.get(nuc, 0.0):.3e} | {act:.3e} "
                 f"| {nd.half_life_s / YEAR_S:.4g} |")
    L.append("")

    if unknown:
        L.append("### Nuclides present but missing decay data "
                 "(extend NUCLIDE_DATA if any are significant)\n")
        # show the heaviest-mass unknowns first
        u_sorted = sorted(((n, grams[n]) for n in unknown),
                          key=lambda kv: kv[1], reverse=True)
        L.append(", ".join(f"{n}" for n, _ in u_sorted[:40]))
        L.append("")

    L.append("## Decay heat & radiotoxicity vs cooling time\n")
    L.append("| cooling (yr) | activity (Bq) | decay heat (W) | radiotox (Sv) |")
    L.append("|---|---|---|---|")
    for yr, st in zip(COOLING_YEARS, curve):
        L.append(f"| {yr:g} | {st.activity_bq:.3e} | {st.decay_heat_w:.3e} "
                 f"| {st.radiotoxicity_sv:.3e} |")
    L.append("")
    L.append("_Quick-look independent-decay model (source_term.decay). For the "
             "rigorous chain-coupled curve (Pu-241→Am-241 in-growth) run "
             "openmc_bridge.run_decay_only and overlay._\n")

    report_path = os.path.join(outdir, "discharge_source_term.md")
    with io.open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return report_path, t0, hm_g, cls


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", default=DEFAULT_RESULTS)
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--hm-tonnes", type=float, default=DEFAULT_HM_T)
    ap.add_argument("--step", type=int, default=-1,
                    help="depletion step index (-1 = discharge/EOL)")
    args = ap.parse_args(argv)

    if not os.path.exists(args.results):
        print(f"ERROR: results file not found: {args.results}", file=sys.stderr)
        print("Pass --results <path to depletion_results.h5>", file=sys.stderr)
        return 2

    try:
        import openmc.deplete
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not import openmc ({exc}). Run this in WSL with the "
              f"OpenMC env active.", file=sys.stderr)
        return 2

    print(f"[1/4] Opening {args.results}")
    results = openmc.deplete.Results(args.results)

    print("[2/4] Validating bridge accessors against live Results ...")
    validation = validate_accessors(results)
    print(f"      materials : {validation.get('materials_accessor', 'FAILED')} "
          f"({validation.get('n_materials', '?')})")
    print(f"      nuclides  : {validation.get('nuclides_accessor', 'FAILED')} "
          f"({validation.get('n_nuclides', '?')})")
    print(f"      mass      : {validation.get('mass_accessor', 'FAILED')}")

    print(f"[3/4] Extracting whole-core grams at step {args.step} ...")
    grams = extract_whole_core_grams(results, step_index=args.step)
    print(f"      {len(grams)} nuclides, "
          f"{_heavy_metal_grams(grams) / 1e6:.4f} tHM")

    print(f"[4/4] Building source term + report into {args.outdir} ...")
    report_path, t0, hm_g, cls = write_report(
        grams, validation, args.outdir, args.results, args.hm_tonnes)

    print("\n=== DONE ===")
    print(f"  discharge activity : {t0.activity_bq:.3e} Bq")
    print(f"  discharge heat     : {t0.decay_heat_w:.3e} W")
    print(f"  heavy metal        : {hm_g / 1e6:.4f} t (nominal {args.hm_tonnes})")
    print(f"  bulk waste class   : {cls.waste_class.name}")
    print(f"  report             : {report_path}")
    print(f"  CSVs               : {args.outdir}/discharge_inventory.csv, "
          f"source_term_vs_cooling.csv")
    print("\nIf the 'mass accessor' line above shows FALLBACK or any probe shows "
          "FAILED, tell me and I'll patch openmc_bridge.py to match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
