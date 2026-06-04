#!/usr/bin/env python3
"""Rigorous chain-coupled decay-heat & activity curve for the Aegis-40 discharge.

RUN THIS IN WSL (the OpenMC environment), after a depletion run exists.

The curated ``source_term`` model only sums ~20 nuclides, so it under-counts the
short/medium-lived fission products at <5 yr cooling and ignores Pu-241->Am-241
in-growth. This script does the *authoritative* version: it exports the discharged
materials from the depletion ``Results`` and runs a zero-flux (decay-only)
``IndependentOperator`` over the FULL chain (~3820 nuclides), then reads decay heat
and activity straight from OpenMC's decay data. The two curves should agree from
~10 yr onward — a clean V&V point for the Digital Appendix.

It validates the two remaining ``# TODO(validate)`` sites in openmc_bridge.py
(``IndependentOperator``/``MicroXS`` construction and the ``get_decay_heat`` /
``get_activity`` accessors). If any OpenMC-API call mismatches this version, the
script prints the live signatures and the traceback so we fix it in one round.

Usage (from the repo root, in WSL):

    PYTHONPATH=src python3 scripts/run_decay_heat.py \
        [--results /mnt/d/.../08_depletion_baseline/depletion_results.h5] \
        [--chain /path/to/chain.xml] [--outdir docs/competition/waste]
"""

from __future__ import annotations

import argparse
import csv
import inspect
import io
import os
import sys
import traceback

DEFAULT_RESULTS = (
    "/mnt/d/conda-envs/openmc-py311/SMRs/Claude version/"
    "aegis40_3d_core_outputs/08_depletion_baseline/depletion_results.h5"
)
DEFAULT_OUTDIR = "docs/competition/waste"
YEAR_S = 365.25 * 24.0 * 3600.0
# cumulative cooling times to report (yr); decay-run intervals are their diffs
COOLING_YEARS = [0.0, 1.0, 3.0, 5.0, 10.0, 30.0, 50.0, 100.0,
                 300.0, 1000.0, 10000.0, 100000.0]


def _dump_signatures(*objs) -> str:
    """Best-effort signature dump for the named callables/classes."""
    lines = []
    for obj in objs:
        name = getattr(obj, "__qualname__", getattr(obj, "__name__", str(obj)))
        try:
            lines.append(f"  {name}{inspect.signature(obj)}")
        except (TypeError, ValueError):
            init = getattr(obj, "__init__", None)
            try:
                lines.append(f"  {name}.__init__{inspect.signature(init)}")
            except Exception:  # noqa: BLE001
                lines.append(f"  {name}: <signature unavailable>")
    return "\n".join(lines)


def _api_help() -> str:
    import openmc.deplete
    return _dump_signatures(
        openmc.deplete.IndependentOperator,
        openmc.deplete.MicroXS,
        openmc.deplete.PredictorIntegrator,
        openmc.deplete.Results.get_decay_heat,
        openmc.deplete.Results.get_activity,
        openmc.deplete.Results.export_to_materials,
    )


def _locate_materials_xml(results_path: str, override: str | None) -> str:
    """Find the fresh materials.xml that the depletion run wrote."""
    if override:
        if not os.path.exists(override):
            raise FileNotFoundError(f"--materials not found: {override}")
        return override
    here = os.path.dirname(os.path.abspath(results_path))
    candidates = [
        os.path.join(here, "materials.xml"),
        os.path.join(os.path.dirname(here), "materials.xml"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError(
        "Could not find materials.xml next to the results. Pass "
        "--materials /path/to/materials.xml (the one the depletion wrote).")


def export_discharged_materials(results, step_index: int, results_path: str,
                                materials_xml: str | None, outdir: str):
    """Return the *depletable* materials at ``step_index`` with volumes set.

    ``Results.export_to_materials`` READS the fresh materials.xml and overlays the
    depleted densities, so we locate it and pass a *copy* (never clobber the
    canonical file). We then keep only the depletable (fuel) materials -- the
    materials.xml also holds water/clad/reflector that must not enter the decay
    run -- and set volumes (mandatory, or absolute decay heat is wrong).
    """
    import shutil

    n = len(results)
    idx = step_index if step_index >= 0 else n + step_index

    src_xml = _locate_materials_xml(results_path, materials_xml)
    os.makedirs(outdir, exist_ok=True)
    copy_xml = os.path.join(outdir, "_materials_base.xml")
    shutil.copyfile(src_xml, copy_xml)
    print(f"      materials.xml: {src_xml}")
    # Pass nuc_with_data explicitly (= the full inventory) so export_to_materials
    # does NOT try to load cross_sections.xml to auto-filter. Decay-only needs no
    # transport data; we want to keep every nuclide that contributes decay.
    all_nucs = list(results[0].index_nuc)
    materials = results.export_to_materials(idx, nuc_with_data=all_nucs,
                                            path=copy_xml)

    depletable_ids = {str(m) for m in results[0].index_mat}
    fuel = [m for m in materials if str(m.id) in depletable_ids]

    vol_map = {}
    try:
        vol_map = {str(k): float(v) for k, v in results[0].volume.items()}
    except Exception:  # noqa: BLE001
        pass
    for mat in fuel:
        if mat.volume is None:
            v = vol_map.get(str(mat.id))
            if v is not None:
                mat.volume = v
    missing = [m.id for m in fuel if m.volume is None]
    if missing:
        print(f"  WARNING: no volume for materials {missing} -- decay-heat "
              f"magnitude for those will be wrong.", file=sys.stderr)

    import openmc  # lazy
    return openmc.Materials(fuel)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results", default=DEFAULT_RESULTS)
    ap.add_argument("--chain", default=None,
                    help="chain.xml; defaults to openmc.config['chain_file']")
    ap.add_argument("--materials", default=None,
                    help="fresh materials.xml; defaults to the one next to --results")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--step", type=int, default=-1)
    args = ap.parse_args(argv)

    if not os.path.exists(args.results):
        print(f"ERROR: results not found: {args.results}", file=sys.stderr)
        return 2

    try:
        import openmc
        import openmc.deplete  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: import openmc failed ({exc}). Run in WSL.", file=sys.stderr)
        return 2

    from aegis40.back_end import openmc_bridge
    from aegis40.back_end import aggregate, evolution
    from aegis40.back_end.source_term import decay  # noqa: F401

    # resolve chain file
    chain = args.chain
    if chain is None:
        chain = openmc.config.get("chain_file") if hasattr(openmc, "config") else None
    if not chain or not os.path.exists(str(chain)):
        print("ERROR: no chain file. Pass --chain /path/to/chain.xml (the one the "
              "depletion used). Current openmc.config chain_file = "
              f"{chain!r}", file=sys.stderr)
        return 2
    # Set the chain globally so Results.get_decay_heat / get_activity can load
    # decay-energy and half-life data (they read openmc.config['chain_file']).
    openmc.config["chain_file"] = chain
    print(f"[1/5] chain: {chain}")

    print(f"[2/5] Opening results + exporting discharged materials ...")
    results = openmc.deplete.Results(args.results)
    try:
        materials = export_discharged_materials(
            results, args.step, args.results, args.materials, args.outdir)
    except Exception:  # noqa: BLE001
        print("FAILED to export discharged materials. Live API signatures:\n"
              + _api_help(), file=sys.stderr)
        traceback.print_exc()
        return 1
    print(f"      {len(materials)} materials, volumes "
          f"{[round(m.volume, 1) if m.volume else None for m in materials]}")

    # cumulative cooling years -> interval seconds for the integrator
    cum_s = [y * YEAR_S for y in COOLING_YEARS]
    intervals_s = [cum_s[i + 1] - cum_s[i] for i in range(len(cum_s) - 1)]

    print(f"[3/5] Running decay-only IndependentOperator "
          f"({len(intervals_s)} steps) ...")
    decay_dir = os.path.join(args.outdir, "decay_run")
    try:
        decay_h5 = openmc_bridge.run_decay_only(materials, intervals_s, str(chain),
                                                out_dir=decay_dir)
    except Exception:  # noqa: BLE001
        print("FAILED in run_decay_only. Live API signatures:\n" + _api_help(),
              file=sys.stderr)
        traceback.print_exc()
        print("\nPaste the signatures + traceback above and I'll fix the bridge.",
              file=sys.stderr)
        return 1

    print(f"[4/5] Reading rigorous decay heat / activity from {decay_h5} ...")
    try:
        curves = openmc_bridge.decay_curves_from_results(decay_h5)
    except Exception:  # noqa: BLE001
        print("FAILED reading decay curves. Live API signatures:\n" + _api_help(),
              file=sys.stderr)
        traceback.print_exc()
        return 1

    # curated cross-check at the same cumulative times (from the discharge grams)
    grams = openmc_bridge.discharge_grams_from_results(args.results, step_index=args.step)
    curated = evolution(grams, cum_s)

    print(f"[5/5] Writing overlay report into {args.outdir} ...")
    os.makedirs(args.outdir, exist_ok=True)
    rig_t = curves["times_s"]
    rig_h = curves["decay_heat_w"]
    rig_a = curves["activity_bq"]

    with io.open(os.path.join(args.outdir, "decay_heat_rigorous.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cooling_yr", "rigorous_decay_heat_W", "rigorous_activity_Bq",
                    "curated_decay_heat_W", "curated_activity_Bq"])
        for i, yr in enumerate(COOLING_YEARS):
            rh = rig_h[i] if i < len(rig_h) else ""
            ra = rig_a[i] if i < len(rig_a) else ""
            w.writerow([f"{yr:g}", f"{rh:.6e}" if rh != "" else "",
                        f"{ra:.6e}" if ra != "" else "",
                        f"{curated[i].decay_heat_w:.6e}",
                        f"{curated[i].activity_bq:.6e}"])

    L = ["# Aegis-40 decay heat & activity — rigorous (chain-coupled) vs curated\n",
         f"- Decay run: `{decay_h5}`",
         f"- Chain: `{chain}`",
         "- Rigorous = zero-flux IndependentOperator over the full chain "
         "(all nuclides + in-growth); curated = source_term 20-nuclide quick-look.\n",
         "| cooling (yr) | decay heat W (rigorous) | decay heat W (curated) "
         "| activity Bq (rigorous) | activity Bq (curated) |",
         "|---|---|---|---|---|"]
    for i, yr in enumerate(COOLING_YEARS):
        rh = f"{rig_h[i]:.3e}" if i < len(rig_h) else "—"
        ra = f"{rig_a[i]:.3e}" if i < len(rig_a) else "—"
        L.append(f"| {yr:g} | {rh} | {curated[i].decay_heat_w:.3e} "
                 f"| {ra} | {curated[i].activity_bq:.3e} |")
    L.append("\n_If rigorous >> curated at <5 yr (expected — short-lived FPs) but "
             "the two converge by ~10-30 yr, that convergence is the V&V check. "
             "Use the rigorous column for §8.11 and the cask thermal design._\n")
    report = os.path.join(args.outdir, "decay_heat_rigorous.md")
    with io.open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print("\n=== DONE ===")
    print(f"  rigorous discharge heat : {rig_h[0]:.3e} W  "
          f"(curated {curated[0].decay_heat_w:.3e} W)")
    print(f"  rigorous heat @ ~10 yr  : "
          f"{rig_h[4]:.3e} W (curated {curated[4].decay_heat_w:.3e} W)")
    print(f"  report : {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
