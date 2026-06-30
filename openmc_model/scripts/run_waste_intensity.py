#!/usr/bin/env python3
"""Aegis-40 spent-fuel arisings & waste-intensity vs the reference reactor (CAREM-25).

FER §8.11 deliverable #2 (spec §4.3.2): "Spent-fuel arisings — tHM & assemblies
per cycle and per year; tHM (or m3 HLW) per TWh vs. a reference reactor of the
team's choice." This is the headline "minimize waste quantity per unit energy"
table that the fuel-efficiency / waste-intensity score keys on.

Pure-Python, zero-dependency — runs on Windows (`py scripts/run_waste_intensity.py`),
no OpenMC / WSL needed. It uses the validated `aegis40.back_end.fuel_cycle` module
(the same arithmetic, 15/15 unit tests) for the Aegis-40 arisings, and the
burnup x thermal-efficiency identity for the head-to-head intensity comparison.

The waste-intensity identity (once-through, per initial heavy metal):

    tHM / TWhe = 1e6 / (BU[MWd/tHM] * 24 * eta)        eta = P_e / P_th

depends only on discharge burnup and plant thermal efficiency, so the comparison
is robust to uncertainty in the reference reactor's exact HM loading / batch count.

Usage:
    py scripts/run_waste_intensity.py [--outdir docs/competition/waste]
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

DEFAULT_OUTDIR = os.path.join("docs", "competition", "waste")


# ---------------------------------------------------------------------------
# Design points
# ---------------------------------------------------------------------------
# Aegis-40 — LOCKED rev_3 design basis (docs/competition/design-basis-locked.md).
AEGIS40 = CoreCycleSpec(
    hm_mass_t=5.3,            # as-modeled initial HM (confirm exact via --step 0)
    n_assemblies=21,
    n_batches=4,
    thermal_power_mwt=125.0,
    electric_power_mwe=40.0,
    cycle_length_efpd=479.0,
    discharge_burnup_gwd_t=42.8,
    capacity_factor=0.90,
)

# CAREM-25 — published parameters (INVAP/CNEA, IAEA ARIS). Integral PWR, boron-free
# normal operation + Gd burnable poison: the named SBF small-iPWR twin. Electric
# output is quoted variously 25-30 MWe across sources; we take 27 MWe (gross) as the
# central case and report the 25-30 MWe band on the intensity. Discharge burnup ~24
# GWd/tU (low-enrichment 1.8 / 3.1 wt% UO2). HM loading / batch count are NOT used
# for the intensity (it is burnup x efficiency only), so their uncertainty does not
# enter the comparison.
CAREM_BU_GWD_T = 24.0
CAREM_PTH_MWT = 100.0
CAREM_PE_CENTRAL_MWE = 27.0
CAREM_PE_BAND_MWE = (25.0, 30.0)   # net-ish low .. gross high


def waste_intensity_thm_per_twhe(burnup_gwd_t: float, eta: float) -> float:
    """tHM (initial heavy metal) per TWh-electric, once-through identity."""
    return 1.0e6 / (burnup_gwd_t * 1000.0 * 24.0 * eta)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def build_rows():
    """Return (aegis_arisings, comparison_rows) for the report/CSV."""
    a = compute_arisings(AEGIS40)

    aegis_eta = AEGIS40.thermal_efficiency
    aegis_int_module = a.hm_t_per_twhe
    aegis_int_id = waste_intensity_thm_per_twhe(AEGIS40.discharge_burnup_gwd_t, aegis_eta)

    carem_eta = CAREM_PE_CENTRAL_MWE / CAREM_PTH_MWT
    carem_int = waste_intensity_thm_per_twhe(CAREM_BU_GWD_T, carem_eta)
    carem_band = tuple(
        waste_intensity_thm_per_twhe(CAREM_BU_GWD_T, pe / CAREM_PTH_MWT)
        for pe in CAREM_PE_BAND_MWE
    )  # (low-eta -> high intensity, high-eta -> low intensity)

    comparison = [
        dict(reactor="Aegis-40 (ours, rev_3)", pth=125.0, pe=40.0, eta=aegis_eta,
             bu=AEGIS40.discharge_burnup_gwd_t, intensity=aegis_int_id,
             note="SBF iPWR, Gd+Er, 4-batch, 479 EFPD"),
        dict(reactor="CAREM-25 (reference)", pth=CAREM_PTH_MWT, pe=CAREM_PE_CENTRAL_MWE,
             eta=carem_eta, bu=CAREM_BU_GWD_T, intensity=carem_int,
             note="SBF iPWR, Gd-only, ~3.1 wt%, 27 MWe central (25-30 band)"),
    ]
    extras = dict(
        aegis_int_module=aegis_int_module,
        aegis_int_id=aegis_int_id,
        carem_band=carem_band,
        ratio=carem_int / aegis_int_id,
        reduction_pct=100.0 * (1.0 - aegis_int_id / carem_int),
    )
    return a, comparison, extras


def write_report(outdir: str):
    os.makedirs(outdir, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    a, comparison, x = build_rows()

    # --- CSV (machine-readable comparison) ---
    with io.open(os.path.join(outdir, "waste_intensity.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["reactor", "P_th_MWt", "P_e_MWe", "thermal_efficiency",
                    "discharge_burnup_GWd_t", "tHM_per_TWhe", "note"])
        for r in comparison:
            w.writerow([r["reactor"], f"{r['pth']:.1f}", f"{r['pe']:.1f}",
                        f"{r['eta']:.4f}", f"{r['bu']:.1f}",
                        f"{r['intensity']:.3f}", r["note"]])

    # --- Markdown ---
    L: list[str] = []
    L.append("# Aegis-40 spent-fuel arisings & waste intensity vs CAREM-25 "
             "(FER §8.11) — generated\n")
    L.append(f"- Generated: `{now}`")
    L.append("- Source: `aegis40.back_end.fuel_cycle` (validated, 15/15 tests) on the "
             "LOCKED rev_3 design basis (`docs/competition/design-basis-locked.md`).")
    L.append("- Headline metric: **tonnes initial heavy metal discharged per TWh "
             "electric (tHM/TWhe)** — lower = less waste per unit energy.\n")

    L.append("## 1. Aegis-40 spent-fuel arisings (once-through)\n")
    L.append("| Quantity | Value |")
    L.append("|---|---|")
    L.append(f"| HM discharged per cycle | {a.hm_per_cycle_t:.3f} tHM |")
    L.append(f"| Assemblies discharged per cycle | {a.assemblies_per_cycle:.2f} FA |")
    L.append(f"| Calendar days per cycle (CF {AEGIS40.capacity_factor:.2f}) | "
             f"{a.calendar_days_per_cycle:.0f} d |")
    L.append(f"| Cycles per year | {a.cycles_per_year:.3f} |")
    L.append(f"| **HM discharged per year** | **{a.hm_per_year_t:.3f} tHM/yr** |")
    L.append(f"| **Assemblies discharged per year** | **{a.assemblies_per_year:.2f} FA/yr** |")
    L.append(f"| Electric energy per cycle | {a.electric_twh_per_cycle:.3f} TWhe |")
    L.append(f"| Thermal energy per cycle | {a.thermal_twh_per_cycle:.3f} TWhth |")
    L.append(f"| **Waste intensity** | **{a.hm_t_per_twhe:.2f} tHM/TWhe** "
             f"({a.hm_t_per_twhth:.2f} tHM/TWhth) |\n")
    L.append(f"_The module value ({a.hm_t_per_twhe:.2f} tHM/TWhe) uses the as-modeled "
             f"initial HM of {AEGIS40.hm_mass_t:.1f} t; the burnup x efficiency identity "
             f"gives {x['aegis_int_id']:.2f}. The ~5% spread is the known 5.3-vs-5.6 tHM / "
             f"42.8-vs-~45 GWd/t self-consistency band (confirm exact fresh iHM via "
             f"`--step 0`). Both round to ~3 tHM/TWhe._\n")

    L.append("## 2. Waste intensity vs the reference reactor (CAREM-25)\n")
    L.append("Once-through identity `tHM/TWhe = 1e6 / (BU[MWd/tHM] x 24 x eta)`, "
             "`eta = P_e/P_th` — depends only on discharge burnup and thermal "
             "efficiency, so the comparison does not hinge on CAREM's exact HM "
             "loading or batch scheme.\n")
    L.append("| Reactor | P_th (MWth) | P_e (MWe) | eta | Discharge burnup (GWd/tHM) | "
             "tHM/TWhe | note |")
    L.append("|---|---|---|---|---|---|---|")
    for r in comparison:
        L.append(f"| {r['reactor']} | {r['pth']:.0f} | {r['pe']:.0f} | {r['eta']:.3f} | "
                 f"{r['bu']:.1f} | **{r['intensity']:.2f}** | {r['note']} |")
    L.append("")
    lo, hi = min(x["carem_band"]), max(x["carem_band"])
    L.append(f"- CAREM-25 intensity band over 25-30 MWe: **{lo:.2f}-{hi:.2f} tHM/TWhe** "
             f"(central {comparison[1]['intensity']:.2f}).")
    L.append(f"- **Aegis-40 is ~{x['ratio']:.1f}x lower waste intensity than CAREM-25 "
             f"(~{x['reduction_pct']:.0f}% reduction in tHM/TWhe)** — less than half the "
             f"heavy-metal arisings per unit electricity.\n")

    L.append("## 3. Why — the high-burnup + SBF design choice\n")
    L.append("- **Discharge burnup 42.8 vs ~24 GWd/tHM** is the dominant lever: ~1.8x "
             "more energy extracted per tonne of fuel before discharge.")
    L.append("- **Thermal efficiency 0.32 vs ~0.27** (higher steam conditions) adds a "
             "further factor.")
    L.append("- Together they roughly halve tHM/TWhe. Dropping Aegis-40 to a CAREM-like "
             "~3.1 wt% / ~24 GWd/t point would roughly double our arisings and forfeit "
             "the fuel-efficiency / waste score — this is the quantitative reason the "
             "high-burnup choice is kept (see `reference-reactors-comparison.md`).")
    L.append("- **SBF (soluble-boron-free)** additionally eliminates the borated-water "
             "secondary-waste stream (spent resins, evaporator concentrates, tritiated "
             "boron effluent) that a boron-controlled PWR generates — a separate "
             "'reduce waste quantity' win not captured in the tHM/TWhe number "
             "(see deliverable #12).\n")

    L.append("## Method notes & caveats\n")
    L.append("- **Initial heavy metal (iHM)** basis throughout (tonnes charged), the "
             "standard fuel-cycle convention for waste intensity.")
    L.append("- CAREM-25 parameters are published figures (INVAP/CNEA, IAEA ARIS): "
             "100 MWth, ~25-30 MWe, ~24 GWd/tU, boron-free + Gd. Electric output is "
             "quoted variously across sources; the 25-30 MWe band brackets it.")
    L.append("- The comparison is **per-unit-energy**, which is the fair basis for "
             "reactors of different size. Absolute arisings (Section 1) are tiny in "
             "any case: <1 tHM/yr and <4 FA/yr for Aegis-40.")
    L.append("- Jang SBF-SMPWR (ultra-long 1555 EFPD) would also score very low "
             "intensity but its published burnup is not tabulated here; CAREM-25 is "
             "the team's chosen named reference per spec p.17.\n")

    path = os.path.join(outdir, "waste_intensity.md")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path, a, comparison, x


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir", default=DEFAULT_OUTDIR)
    args = p.parse_args(argv)

    path, a, comparison, x = write_report(args.outdir)

    print("=== Aegis-40 waste intensity ===")
    print(f"  arisings   : {a.hm_per_year_t:.3f} tHM/yr, "
          f"{a.assemblies_per_year:.2f} FA/yr")
    print(f"  intensity  : {x['aegis_int_id']:.2f} tHM/TWhe (identity), "
          f"{x['aegis_int_module']:.2f} (module/iHM {AEGIS40.hm_mass_t:.1f}t)")
    print(f"  CAREM-25   : {comparison[1]['intensity']:.2f} tHM/TWhe "
          f"(band {min(x['carem_band']):.2f}-{max(x['carem_band']):.2f})")
    print(f"  result     : Aegis-40 ~{x['ratio']:.1f}x lower "
          f"(~{x['reduction_pct']:.0f}% reduction)")
    print(f"  report     : {path}")
    print(f"  csv        : {os.path.join(args.outdir, 'waste_intensity.csv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
