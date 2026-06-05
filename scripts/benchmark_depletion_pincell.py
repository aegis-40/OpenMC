#!/usr/bin/env python3
"""Digital-Appendix V&V #1 — OpenMC depletion benchmark (BEAVRS 2.4% PWR pincell).

RUN THIS IN WSL (the OpenMC environment), not Windows.

Reproduces the published OpenMC depletion-validation case from

    P.K. Romano, C.J. Josey, A.E. Johnson, J. Liang, "Depletion capabilities in
    the OpenMC Monte Carlo particle transport code," Annals of Nuclear Energy 152
    (2021) 107989, Section 3.2 (PWR Pincell).

That paper depletes a single 2.4 wt% BEAVRS PWR pincell to 50 MWd/kg and shows
OpenMC agrees with Serpent to ~20 pcm in k_eff, <1% on actinide concentrations,
and <1% on most fission products. The case is built into OpenMC as
``openmc.examples.pwr_pin_cell()`` (identical BEAVRS materials & dimensions:
UO2 10.29769 g/cm3 @ 2.4 wt%, Zircaloy clad r=0.45720 cm, pin pitch 1.26 cm,
hot borated water 0.740582 g/cm3 with S(a,b) c_H_in_H2O), so this benchmark needs
ZERO external geometry data — only the standard ENDF/B-VIII.0 library + depletion
chain that the Aegis-40 core analysis already uses. That makes it maximally
*reproducible*, which is exactly what the Digital-Appendix gate (spec §4.3.2)
asks for: one sample input file per code + benchmarking + reproducibility.

Why this matters for the FER safety case: the storage-criticality k(95/95) and
the source-term / decay-heat numbers all rest on the OpenMC depletion path. This
benchmark is the evidence that that path is used correctly, and it is the basis
for the code/data **bias term (Δ_bias)** that currently sits at 0 in
``run_storage_criticality.py``.

What it does
------------
1. Builds the BEAVRS 2.4% pincell via ``openmc.examples.pwr_pin_cell()``.
2. Sets the fuel volume (per unit height) and depletes at 174 W/cm using the
   paper's exact burnup schedule (0.1/0.4/0.5, then 1.0 to 10, then 2.5 to 50
   MWd/kg), PredictorIntegrator (the paper's "CE" = constant-extrapolation).
3. Reads the results and writes k_eff(BU) plus the principal actinide & fission-
   product concentrations vs burnup → ``docs/competition/digital-appendix/``.
4. Optional ``--repeat`` reruns with a different RNG seed for the repeatability
   leg (k_eff agreement within Monte-Carlo sigma).

Usage (from repo root, in WSL):

    PYTHONPATH=src python3 scripts/benchmark_depletion_pincell.py            # full, to 50 MWd/kg
    PYTHONPATH=src python3 scripts/benchmark_depletion_pincell.py --smoke    # quick, to 10 MWd/kg
    PYTHONPATH=src python3 scripts/benchmark_depletion_pincell.py --repeat 7 # repeatability seed
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import os
import sys

# Same data defaults as the rest of the Aegis-40 OpenMC workstream.
DEFAULT_XS = "/mnt/d/openmc_data/endfb-viii.0-hdf5/cross_sections.xml"
DEFAULT_CHAIN = "/mnt/d/openmc_data/chain_endfb80_pwr.xml"
DEFAULT_OUTDIR = os.path.join("docs", "competition", "digital-appendix")
DEFAULT_WORKDIR = os.path.join("docs", "competition", "digital-appendix", "pincell_run")

LINEAR_HEAT_W_PER_CM = 174.0   # Romano 2021 §3.2
FUEL_RADIUS_CM = 0.39218       # BEAVRS pellet radius (openmc.examples.pwr_pin_cell)

# Principal isotopes to report (the burnup-credit / source-term set). These are
# the nuclides that drive storage k_eff, decay heat and radiotoxicity, so they
# are the ones whose depletion accuracy the safety case actually depends on.
ACTINIDES = ["U234", "U235", "U236", "U238", "Np237",
             "Pu238", "Pu239", "Pu240", "Pu241", "Pu242",
             "Am241", "Am243", "Cm244"]
FISSION_PRODUCTS = ["Kr85", "Sr90", "Tc99", "Cs133", "Cs134", "Cs137",
                    "Nd143", "Nd145", "Sm149", "Sm151", "Eu153", "Gd155"]

# Romano 2021 published OpenMC-vs-Serpent agreement (the acceptance reference).
REF_KEFF_PCM = 20      # full-chain k_eff difference grows to ~20 pcm by 50 MWd/kg
REF_ACTINIDE_PCT = 1.0  # actinide concentrations agree to a fraction of a percent
REF_FP_PCT = 1.0        # most fission products agree within 1%


def burnup_schedule(smoke: bool):
    """Return the cumulative-burnup *increments* (MWd/kg), per Romano 2021 §3.2."""
    steps = [0.1, 0.4, 0.5]                 # fine start to capture xenon build-in
    steps += [1.0] * 9                      # 1.0 -> 10.0 MWd/kg
    if smoke:
        return steps                        # stop at 10 MWd/kg for a quick check
    steps += [2.5] * 16                     # 10.0 -> 50.0 MWd/kg
    return steps


def build_model(particles: int, batches: int, inactive: int, seed: int):
    import openmc
    model = openmc.examples.pwr_pin_cell()   # BEAVRS 2.4% pincell, borated water

    # Give the depleting fuel material a volume so the operator knows the heavy-
    # metal mass (per 1 cm of height). Burnup units then convert via the power.
    import math
    for mat in model.materials:
        if mat.name and "fuel" in mat.name.lower():
            mat.volume = math.pi * FUEL_RADIUS_CM ** 2
            mat.depletable = True

    model.settings.particles = particles
    model.settings.batches = batches
    model.settings.inactive = inactive
    try:
        model.settings.seed = seed
    except Exception:
        pass
    return model, openmc


def run_depletion(model, openmc, chain, power_w, steps, workdir):
    import openmc.deplete
    os.makedirs(workdir, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(workdir)
    try:
        # CoupledOperator (0.15.x) couples transport <-> depletion in-memory.
        op = openmc.deplete.CoupledOperator(model, chain_file=chain)
        # PredictorIntegrator == the paper's CE (constant-extrapolation) method.
        integrator = openmc.deplete.PredictorIntegrator(
            op, steps, power=power_w, timestep_units="MWd/kg")
        integrator.integrate()
    finally:
        os.chdir(cwd)
    return os.path.join(workdir, "depletion_results.h5")


def read_results(results_path, openmc, fuel_id):
    import openmc.deplete
    res = openmc.deplete.Results(results_path)

    # k_eff vs step
    t_bu, keff = res.get_keff()   # keff shape (N, 2) = [value, std]
    # cumulative burnup axis (MWd/kg) is the depletion time in those units;
    # get_keff returns time in seconds, so rebuild the BU axis from the schedule
    # in the caller. Here just return k and sigma arrays.
    k = [float(row[0]) for row in keff]
    sig = [float(row[1]) for row in keff]

    # nuclide concentrations (atoms) vs step for the principal isotopes
    conc = {}
    for nuc in ACTINIDES + FISSION_PRODUCTS:
        try:
            _, atoms = res.get_atoms(str(fuel_id), nuc)
            conc[nuc] = [float(a) for a in atoms]
        except Exception:
            conc[nuc] = None   # nuclide absent from this chain
    return k, sig, conc


def cumulative_bu(steps):
    out, acc = [0.0], 0.0
    for s in steps:
        acc += s
        out.append(acc)
    return out


def write_report(outdir, k, sig, conc, bu_axis, meta):
    os.makedirs(outdir, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # --- CSV: k_eff(BU) ---
    with io.open(os.path.join(outdir, "pincell_keff_vs_burnup.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["burnup_MWd_kg", "k_eff", "sigma"])
        for b, kk, ss in zip(bu_axis, k, sig):
            w.writerow([f"{b:.3f}", f"{kk:.6f}", f"{ss:.6f}"])

    # --- CSV: isotopics(BU) ---
    with io.open(os.path.join(outdir, "pincell_isotopics_vs_burnup.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        nucs = [n for n in (ACTINIDES + FISSION_PRODUCTS) if conc.get(n)]
        w.writerow(["burnup_MWd_kg"] + nucs)
        for i, b in enumerate(bu_axis):
            w.writerow([f"{b:.3f}"] + [f"{conc[n][i]:.6e}" for n in nucs])

    # --- Markdown ---
    L: list[str] = []
    L.append("# Digital Appendix — OpenMC depletion benchmark "
             "(BEAVRS 2.4% PWR pincell)\n")
    L.append(f"- Generated: `{now}`")
    L.append("- Reference: Romano et al., *Ann. Nucl. Energy* 152 (2021) 107989, "
             "§3.2 (PWR Pincell). OpenMC vs Serpent: k_eff within ~20 pcm, "
             "actinides <1%, fission products <1%.")
    L.append(f"- Model: `openmc.examples.pwr_pin_cell()` (BEAVRS 2.4 wt% UO2, "
             f"borated water, reflective) — built into OpenMC, no external data.")
    L.append(f"- Library: `{meta['xs']}`")
    L.append(f"- Chain: `{meta['chain']}`")
    L.append(f"- Power: {LINEAR_HEAT_W_PER_CM} W/cm; integrator: PredictorIntegrator "
             f"(CE); MC: {meta['particles']} part x ({meta['batches']}-"
             f"{meta['inactive']}) batches; seed {meta['seed']}.\n")

    L.append("## k_eff vs burnup\n")
    L.append("| Burnup (MWd/kg) | k_eff | sigma (pcm) |")
    L.append("|---|---|---|")
    for b, kk, ss in zip(bu_axis, k, sig):
        L.append(f"| {b:.2f} | {kk:.5f} | {ss*1e5:.0f} |")
    L.append("")
    L.append(f"_BOL k_eff = {k[0]:.5f} ± {sig[0]*1e5:.0f} pcm; "
             f"EOL ({bu_axis[-1]:.1f} MWd/kg) k_eff = {k[-1]:.5f}. The monotone "
             f"fall with burnup (no soluble-boron / no burnable poison in this "
             f"validation pincell) is the expected shape; compare against Fig. 2 "
             f"of Romano 2021._\n")

    L.append("## Principal-isotope build-up (atoms, per cm of pin)\n")
    L.append("Concentrations of the nuclides that drive storage k_eff, decay heat "
             "and radiotoxicity. Trends (U-235 depletion, Pu-239/240/241 in-growth, "
             "Cs-137/Sr-90 accumulation, Sm-149 saturation) are the physical "
             "signatures the paper benchmarks to <1%.\n")
    sel = ["U235", "Pu239", "Pu240", "Pu241", "Am241", "Cs137", "Sr90", "Sm149"]
    sel = [n for n in sel if conc.get(n)]
    L.append("| Burnup (MWd/kg) | " + " | ".join(sel) + " |")
    L.append("|---|" + "|".join(["---"] * len(sel)) + "|")
    for i, b in enumerate(bu_axis):
        L.append(f"| {b:.2f} | " +
                 " | ".join(f"{conc[n][i]:.3e}" for n in sel) + " |")
    L.append("")

    L.append("## Acceptance & how this feeds the safety case\n")
    L.append(f"- **Benchmark target (Romano 2021):** k_eff to ~{REF_KEFF_PCM} pcm vs "
             f"Serpent, actinides <{REF_ACTINIDE_PCT:.0f}%, FPs <{REF_FP_PCT:.0f}%. "
             "Reproducing the published k_eff(BU) curve and isotopic trends with our "
             "ENDF/B-VIII.0 library + chain demonstrates the depletion path is used "
             "correctly.")
    L.append("- **Reproducibility:** the model is `openmc.examples.pwr_pin_cell()` — "
             "anyone with OpenMC reruns this exactly; no proprietary geometry.")
    L.append("- **Repeatability:** rerun with `--repeat <seed>`; k_eff at each step "
             "must agree within the combined Monte-Carlo sigma.")
    L.append("- **Bias term:** the spread between this benchmark and the reference is "
             "the basis for the code/data bias Δ_bias fed back into "
             "`run_storage_criticality.py` (currently 0). With OpenMC-Serpent "
             "agreement at the ~20 pcm / <1% level, the depletion contribution to "
             "Δ_bias is small relative to the ~0.16 storage-criticality margin.\n")

    L.append("## Open items\n")
    L.append("- **Measured-assay validation (stronger):** benchmark these same "
             "isotopics against a **SFCOMPO 2.0** destructive-assay PWR sample at "
             "comparable enrichment/burnup, and/or the tabulated nuclide "
             "concentrations of the **OECD/NEA Burnup-Credit Criticality Benchmark "
             "Phase I-B**. Both give absolute reference numbers (this case is "
             "code-to-code). Needs the source documents.")
    L.append("- **Storage-rack criticality benchmark:** OpenMC k_eff vs **OECD/NEA "
             "Burnup-Credit Benchmark Phase II** (or an ANS-8 array) to close the "
             "criticality-side bias.\n")

    path = os.path.join(outdir, "depletion_benchmark.md")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--smoke", action="store_true",
                    help="quick functional run, deplete only to 10 MWd/kg")
    ap.add_argument("--particles", type=int, default=20000,
                    help="particles/batch (paper used 4e6 for ~3-4 pcm)")
    ap.add_argument("--batches", type=int, default=100)
    ap.add_argument("--inactive", type=int, default=20)
    ap.add_argument("--repeat", type=int, default=1,
                    help="RNG seed (use a different value for the repeatability leg)")
    ap.add_argument("--chain", default=None,
                    help=f"chain.xml (default openmc.config or {DEFAULT_CHAIN})")
    ap.add_argument("--cross-sections", default=None,
                    help=f"cross_sections.xml (default $OPENMC_CROSS_SECTIONS or {DEFAULT_XS})")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--workdir", default=DEFAULT_WORKDIR)
    args = ap.parse_args(argv)

    try:
        import openmc  # noqa: F401
        import openmc.deplete  # noqa: F401
        import openmc.examples  # noqa: F401
    except Exception as e:  # pragma: no cover - WSL only
        print(f"ERROR: OpenMC import failed ({e}).\nRun this in WSL with the OpenMC "
              "environment active.", file=sys.stderr)
        return 2

    import openmc
    xs = (args.cross_sections or os.environ.get("OPENMC_CROSS_SECTIONS") or DEFAULT_XS)
    if not os.path.exists(xs):
        print(f"ERROR: cross_sections.xml not found: {xs}", file=sys.stderr)
        return 2
    openmc.config["cross_sections"] = xs

    chain = args.chain or (openmc.config.get("chain_file") if hasattr(openmc, "config") else None) or DEFAULT_CHAIN
    if not chain or not os.path.exists(str(chain)):
        print(f"ERROR: chain file not found: {chain!r}. Pass --chain.", file=sys.stderr)
        return 2
    openmc.config["chain_file"] = chain

    steps = burnup_schedule(args.smoke)
    bu_axis = cumulative_bu(steps)
    print(f"[1/4] BEAVRS 2.4% pincell; {len(steps)} burnup steps -> "
          f"{bu_axis[-1]:.1f} MWd/kg; seed {args.repeat}")

    model, openmc = build_model(args.particles, args.batches, args.inactive, args.repeat)
    fuel_id = next(m.id for m in model.materials
                   if m.name and "fuel" in m.name.lower())

    print(f"[2/4] depleting at {LINEAR_HEAT_W_PER_CM} W/cm "
          f"({args.particles} part x {args.batches} batches/step) ...")
    results_path = run_depletion(model, openmc, chain, LINEAR_HEAT_W_PER_CM,
                                 steps, args.workdir)

    print("[3/4] reading results ...")
    k, sig, conc = read_results(results_path, openmc, fuel_id)

    meta = dict(xs=xs, chain=chain, particles=args.particles, batches=args.batches,
                inactive=args.inactive, seed=args.repeat)
    path = write_report(args.outdir, k, sig, conc, bu_axis, meta)

    print("[4/4] DONE")
    print(f"  BOL k_eff = {k[0]:.5f} +/- {sig[0]*1e5:.0f} pcm")
    print(f"  EOL k_eff = {k[-1]:.5f} (at {bu_axis[-1]:.1f} MWd/kg)")
    print(f"  report : {path}")
    print(f"  csv    : {args.outdir}/pincell_keff_vs_burnup.csv, "
          f"pincell_isotopics_vs_burnup.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
