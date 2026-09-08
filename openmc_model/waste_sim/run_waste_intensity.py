#!/usr/bin/env python3
"""Aegis-40 spent-fuel arisings & waste-intensity vs the reference reactor (CAREM-25).

FER §8.11 deliverable #2 (spec §4.3.2): "Spent-fuel arisings — tHM & assemblies
per cycle and per year; tHM (or m3 HLW) per TWh vs. a reference reactor of the
team's choice."

All Aegis-40 parameters are taken from the OpenMC 3D-core depletion run
(depletion_results.h5, 08_depletion_baseline):
  - HM loading : 9.87 tHM  (37 FA × 17×17 pin lattice, as-modeled in Cell 6)
  - B1         : 2175 EFPD (k_eff crosses 1.0 at this point for a fresh, uniformly
                             loaded core — determined by interpolation from get_keff())
  - B1_BU      : 27.6 GWd/tHM  (= P_th/HM × B1)
  - LRM formula: cycle_EFPD = 2/(n+1) × B1 ;  discharge_BU = 2n/(n+1) × B1_BU

Three reload scenarios are compared:
  n=1 — factory-fuelled once-through (no on-site refuelling): 2175 EFPD, 27.6 GWd/t
  n=3 — 3-batch partial reload        :  1088 EFPD, 41.3 GWd/t
  n=4 — 4-batch partial reload        :   870 EFPD, 44.1 GWd/t

Pure-Python, zero-dependency — runs on Windows:
    py waste_sim/run_waste_intensity.py [--outdir output]
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from aegis40.back_end.fuel_cycle import CoreCycleSpec, compute_arisings  # noqa: E402

DEFAULT_OUTDIR = "output"

# ---------------------------------------------------------------------------
# Aegis-40 — values from OpenMC 3D-core depletion (08_depletion_baseline)
# ---------------------------------------------------------------------------
HM_MASS_T       = 9.87     # tHM  — 37 FA × 17×17 lattice (Cell 6 of notebook)
N_ASSEMBLIES    = 37       # total fuel assemblies in core
THERMAL_MWT     = 125.0    # MWth
ELECTRIC_MWE    = 40.0     # MWe
CAPACITY_FACTOR = 0.90

# From depletion run: interpolated point where k_eff crosses 1.0
B1_EFPD = 2175.45          # EFPD  (fresh-core criticality limit)
B1_BU   = THERMAL_MWT / HM_MASS_T * B1_EFPD / 1000.0  # GWd/tHM = 27.6


def _lrm(n: int) -> tuple[float, float]:
    """Return (cycle_EFPD, discharge_BU_GWd_t) for n-batch LRM."""
    cycle_efpd   = 2.0 / (n + 1) * B1_EFPD
    discharge_bu = 2.0 * n / (n + 1) * B1_BU
    return cycle_efpd, discharge_bu


# Three scenarios
SCENARIOS: dict[str, CoreCycleSpec] = {}
for _n, _label in [(1, "n1"), (3, "n3"), (4, "n4")]:
    _cyc, _bu = _lrm(_n)
    SCENARIOS[_label] = CoreCycleSpec(
        hm_mass_t           = HM_MASS_T,
        n_assemblies        = N_ASSEMBLIES,
        n_batches           = _n,
        thermal_power_mwt   = THERMAL_MWT,
        electric_power_mwe  = ELECTRIC_MWE,
        cycle_length_efpd   = _cyc,
        discharge_burnup_gwd_t = _bu,
        capacity_factor     = CAPACITY_FACTOR,
    )

# CAREM-25 reference (INVAP/CNEA, IAEA ARIS)
CAREM_BU_GWD_T       = 24.0
CAREM_PTH_MWT        = 100.0
CAREM_PE_CENTRAL_MWE = 27.0
CAREM_PE_BAND_MWE    = (25.0, 30.0)


def waste_intensity_thm_per_twhe(burnup_gwd_t: float, eta: float) -> float:
    """tHM per TWhe — once-through identity: 1e6 / (BU[MWd/t] × 24 × eta)."""
    return 1.0e6 / (burnup_gwd_t * 1000.0 * 24.0 * eta)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def build_rows():
    eta     = ELECTRIC_MWE / THERMAL_MWT
    carem_eta  = CAREM_PE_CENTRAL_MWE / CAREM_PTH_MWT
    carem_int  = waste_intensity_thm_per_twhe(CAREM_BU_GWD_T, carem_eta)
    carem_band = tuple(
        waste_intensity_thm_per_twhe(CAREM_BU_GWD_T, pe / CAREM_PTH_MWT)
        for pe in CAREM_PE_BAND_MWE
    )

    scenario_rows = []
    for key, spec in SCENARIOS.items():
        a      = compute_arisings(spec)
        intens = waste_intensity_thm_per_twhe(spec.discharge_burnup_gwd_t, eta)
        n      = spec.n_batches
        cyc_yr = spec.cycle_length_efpd / 365.25
        label_map = {
            1: f"Aegis-40 n=1 — once-through (no reload)  [{B1_EFPD:.0f} EFPD, {cyc_yr:.1f} yr]",
            3: f"Aegis-40 n=3 — 3-batch reload            [{spec.cycle_length_efpd:.0f} EFPD, {cyc_yr:.1f} yr]",
            4: f"Aegis-40 n=4 — 4-batch reload            [{spec.cycle_length_efpd:.0f} EFPD, {cyc_yr:.1f} yr]",
        }
        scenario_rows.append(dict(
            key=key, n=n, spec=spec, arisings=a,
            intensity=intens,
            ratio=carem_int / intens,
            reduction_pct=100.0 * (1.0 - intens / carem_int),
            label=label_map[n],
            cycle_yr=cyc_yr,
        ))

    carem_row = dict(
        reactor="CAREM-25 (reference, IAEA ARIS)",
        pth=CAREM_PTH_MWT, pe=CAREM_PE_CENTRAL_MWE,
        eta=carem_eta, bu=CAREM_BU_GWD_T,
        intensity=carem_int,
        note="SBF iPWR, Gd-only, ~3.1 wt%, 27 MWe central (25-30 band)"
    )
    return scenario_rows, carem_row, carem_band


def write_report(outdir: str):
    os.makedirs(outdir, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rows, carem, carem_band = build_rows()
    eta = ELECTRIC_MWE / THERMAL_MWT

    # --- CSV ---
    with io.open(os.path.join(outdir, "waste_intensity.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "n_batches", "cycle_EFPD", "cycle_yr",
                    "HM_tHM", "n_assemblies", "discharge_BU_GWd_t",
                    "tHM_per_TWhe", "vs_CAREM_ratio", "reduction_pct"])
        for r in rows:
            w.writerow([
                r["label"].split("—")[0].strip(),
                r["n"],
                f"{r['spec'].cycle_length_efpd:.1f}",
                f"{r['cycle_yr']:.2f}",
                f"{HM_MASS_T:.2f}",
                N_ASSEMBLIES,
                f"{r['spec'].discharge_burnup_gwd_t:.2f}",
                f"{r['intensity']:.3f}",
                f"{r['ratio']:.2f}",
                f"{r['reduction_pct']:.1f}",
            ])
        w.writerow(["CAREM-25 (reference)", "?", "—", "—", "—", "—",
                    f"{CAREM_BU_GWD_T:.1f}",
                    f"{carem['intensity']:.3f}", "1.00", "0.0"])

    # --- Markdown ---
    L: list[str] = []
    L.append("# Aegis-40 spent-fuel arisings & waste intensity vs CAREM-25 "
             "(FER §8.11) — generated\n")
    L.append(f"- Generated : `{now}`")
    L.append(f"- Source    : OpenMC 3D-core depletion (`08_depletion_baseline/depletion_results.h5`)")
    L.append(f"- Core      : {N_ASSEMBLIES} FA × 17×17, {THERMAL_MWT:.0f} MWth / "
             f"{ELECTRIC_MWE:.0f} MWe, HM = {HM_MASS_T:.2f} tHM")
    L.append(f"- B1        : **{B1_EFPD:.0f} EFPD** (k_eff crosses 1.0 for fresh uniform load) "
             f"= **{B1_BU:.2f} GWd/tHM**")
    L.append(f"- LRM       : cycle = 2/(n+1)×B1 ;  discharge BU = 2n/(n+1)×B1_BU\n")

    # Section 1 — per-scenario arisings
    L.append("## 1. Aegis-40 arisings — three reload scenarios\n")
    hdr = ("| Scenario | Cycle EFPD | Cycle yr | "
           "HM/cycle (tHM) | FA/cycle | HM/yr (tHM) | FA/yr | "
           "Electric TWhe/cycle | **tHM/TWhe** |")
    sep = "|---|---|---|---|---|---|---|---|---|"
    L.append(hdr); L.append(sep)
    for r in rows:
        a = r["arisings"]
        L.append(
            f"| {r['label']} "
            f"| {r['spec'].cycle_length_efpd:.0f} "
            f"| {r['cycle_yr']:.2f} "
            f"| {a.hm_per_cycle_t:.3f} "
            f"| {a.assemblies_per_cycle:.1f} "
            f"| {a.hm_per_year_t:.3f} "
            f"| {a.assemblies_per_year:.1f} "
            f"| {a.electric_twh_per_cycle:.3f} "
            f"| **{r['intensity']:.2f}** |"
        )
    L.append("")

    # Section 2 — comparison vs CAREM-25
    L.append("## 2. Waste intensity vs CAREM-25\n")
    L.append("Identity: `tHM/TWhe = 1e6 / (BU[MWd/tHM] × 24 × eta)` — "
             "depends only on burnup and thermal efficiency.\n")
    L.append("| Reactor | P_th | P_e | eta | BU (GWd/tHM) | **tHM/TWhe** | vs CAREM |")
    L.append("|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(
            f"| {r['label'].split('[')[0].strip()} "
            f"| {THERMAL_MWT:.0f} MWth | {ELECTRIC_MWE:.0f} MWe | {eta:.3f} "
            f"| {r['spec'].discharge_burnup_gwd_t:.1f} "
            f"| **{r['intensity']:.2f}** "
            f"| {r['ratio']:.1f}× lower ({r['reduction_pct']:.0f}% reduction) |"
        )
    lo, hi = min(carem_band), max(carem_band)
    L.append(
        f"| CAREM-25 (reference) "
        f"| {CAREM_PTH_MWT:.0f} MWth | {CAREM_PE_CENTRAL_MWE:.0f} MWe | {carem['eta']:.3f} "
        f"| {CAREM_BU_GWD_T:.1f} "
        f"| **{carem['intensity']:.2f}** (band {lo:.2f}–{hi:.2f}) "
        f"| baseline |"
    )
    L.append("")

    # Section 3 — design rationale
    L.append("## 3. Design rationale\n")
    n1 = rows[0]; n4 = rows[2]
    L.append(
        f"- **B1 = {B1_EFPD:.0f} EFPD** is the fundamental physical limit: "
        f"a fresh Aegis-40 core stays critical for {B1_EFPD/365.25:.1f} years. "
        f"All reload schemes derive from this one number via LRM."
    )
    L.append(
        f"- **n=1 (once-through, {n1['cycle_yr']:.1f} yr)**: factory loads the reactor, "
        f"operator runs it until EOL, reactor returns to factory — zero on-site refuelling. "
        f"Discharge BU = {n1['spec'].discharge_burnup_gwd_t:.1f} GWd/tHM, "
        f"intensity = {n1['intensity']:.2f} tHM/TWhe "
        f"({n1['ratio']:.1f}× better than CAREM-25)."
    )
    L.append(
        f"- **n=4 (4-batch, {n4['cycle_yr']:.1f} yr cycles)**: maximises burnup "
        f"({n4['spec'].discharge_burnup_gwd_t:.1f} GWd/tHM) and waste intensity "
        f"({n4['intensity']:.2f} tHM/TWhe, {n4['ratio']:.1f}× better) but requires "
        f"on-site refuelling every {n4['cycle_yr']:.1f} years."
    )
    L.append(
        f"- **SBF design** eliminates the borated-water secondary-waste stream "
        f"(spent resins, tritiated boron effluent) — a further waste reduction "
        f"not captured in tHM/TWhe (see §8.11 deliverable #12)."
    )
    L.append(
        f"- All Aegis-40 scenarios outperform CAREM-25 by ≥{rows[-1]['ratio']:.1f}× "
        f"on waste intensity, driven by higher discharge burnup "
        f"({n4['spec'].discharge_burnup_gwd_t:.1f} vs {CAREM_BU_GWD_T} GWd/tHM) "
        f"and better thermal efficiency ({eta:.2f} vs {carem['eta']:.2f}).\n"
    )

    L.append("## 4. Method notes\n")
    L.append(f"- HM mass {HM_MASS_T:.2f} tHM and B1 = {B1_EFPD:.0f} EFPD are taken "
             f"directly from the OpenMC depletion run (`get_keff()` interpolation).")
    L.append("- Cycle lengths and discharge burnups computed via Linear Reactivity Model (LRM).")
    L.append("- CAREM-25: 100 MWth, 25-30 MWe, ~24 GWd/tU (INVAP/CNEA, IAEA ARIS 2020).")
    L.append("- Waste intensity identity is per initial HM (iHM basis), "
             "standard fuel-cycle convention.\n")

    path = os.path.join(outdir, "waste_intensity.md")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path, rows, carem, carem_band


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir", default=DEFAULT_OUTDIR)
    args = p.parse_args(argv)

    path, rows, carem, carem_band = write_report(args.outdir)

    print(f"=== Aegis-40 waste intensity (from OpenMC depletion) ===")
    print(f"  Core: {N_ASSEMBLIES} FA, HM={HM_MASS_T:.2f} tHM, "
          f"B1={B1_EFPD:.0f} EFPD = {B1_BU:.2f} GWd/tHM\n")
    print(f"  {'Scenario':<38} {'Cycle':>8}  {'BU':>8}  {'tHM/TWhe':>9}  {'vs CAREM':>9}")
    print(f"  {'-'*38} {'-'*8}  {'-'*8}  {'-'*9}  {'-'*9}")
    for r in rows:
        name = {1:"n=1 (once-through)", 3:"n=3 (3-batch)", 4:"n=4 (4-batch)"}[r['n']]
        print(f"  {name:<38} {r['spec'].cycle_length_efpd:>6.0f} d  "
              f"{r['spec'].discharge_burnup_gwd_t:>6.1f} t  "
              f"{r['intensity']:>8.2f}   {r['ratio']:>6.1f}x lower")
    print(f"  {'CAREM-25 (reference)':<38} {'—':>8}  "
          f"{CAREM_BU_GWD_T:>6.1f} t  {carem['intensity']:>8.2f}   {'1.0x':>9}")
    print(f"\n  report : {path}")
    print(f"  csv    : {os.path.join(args.outdir, 'waste_intensity.csv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
