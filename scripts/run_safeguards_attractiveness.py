#!/usr/bin/env python3
"""Safeguards & non-proliferation: attractiveness of discharge materials (FER 3S).

Quantifies the "attractive material" (special nuclear material) inventory in the
Aegis-40 spent fuel at discharge, to support the §8.5/§8.7 3S (Safety / Security /
Safeguards) case. The physics is produced here by [NEU] from the OpenMC depletion
discharge inventory; the prose/framing is [3S]'s (Azamhon).

Headline argument: a high-burnup (42.8 GWd/t) soluble-boron-free core **degrades
the plutonium** (low Pu-239, high Pu-240/Pu-238/Pu-241 -> reactor-grade, high
decay heat + neutron background) and leaves spent uranium far below any usable
enrichment. Both raise the *intrinsic* barriers. The dominant proliferation
resistance, however, remains *extrinsic* — the intense radiation field of the
intact spent-fuel assembly + safeguards — which is the honest, literature-
consistent reading of the material-attractiveness work (Bathke et al. 2009/2012).

Pure-Python + matplotlib — runs on Windows from the tracked discharge inventory
CSV (no OpenMC / WSL). Outputs tables (md/csv) + plots (png) to
docs/competition/safeguards/.

Usage:
    py scripts/run_safeguards_attractiveness.py
        [--inventory docs/competition/waste/discharge_inventory.csv]
        [--n-batches 4] [--outdir docs/competition/safeguards]

References (for the FER writeup):
  - Bathke et al., "The Attractiveness of Materials in Advanced Nuclear Fuel
    Cycles...", Nuclear Technology 179 (2012) 5-30 (FOM methodology).
  - Wu et al., Int. J. Energy Research (2020) — non-proliferation barriers review
    (in D:\\projects\\literature).
  - IAEA significant quantities: INFCIRC/153, IAEA Safeguards Glossary (Pu = 8 kg).
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import math
import os

DEFAULT_INVENTORY = os.path.join("docs", "competition", "waste", "discharge_inventory.csv")
DEFAULT_OUTDIR = os.path.join("docs", "competition", "safeguards")

PU = ["Pu238", "Pu239", "Pu240", "Pu241", "Pu242"]
U = ["U234", "U235", "U236", "U238"]
MINOR_ACTINIDES = ["Np237", "Am241", "Am243", "Cm244"]

# Specific decay heat, W per gram (standard isotopic thermal powers; Pu values
# e.g. 567 / 1.93 / 7.06 / 3.41 / 0.116 W/kg, Am-241 114.7 W/kg).
DECAY_HEAT_W_PER_G = {
    "Pu238": 0.5674, "Pu239": 1.929e-3, "Pu240": 7.06e-3, "Pu241": 3.41e-3,
    "Pu242": 1.159e-4, "Am241": 0.1147, "Am243": 6.4e-3, "Cm244": 2.83,
    "Np237": 2.07e-5, "U234": 1.78e-4, "U235": 6.0e-8, "U236": 1.75e-6,
    "U238": 8.5e-9,
}
# Spontaneous-fission neutron yield, n/s per gram (drives predetonation).
SF_NEUTRONS_N_PER_S_PER_G = {
    "Pu238": 2.59e3, "Pu239": 2.18e-2, "Pu240": 1.02e3, "Pu241": 5.0e-2,
    "Pu242": 1.72e3, "Cm244": 1.10e7, "Am241": 1.18, "Cm242": 2.10e7,
}
# Bare-sphere critical masses, kg (alpha-phase metal). Used only for the
# INDICATIVE Bathke FOM critical-mass term; the rigorous value for our exact
# vector wants an OpenMC bare-sphere k_eff search (see notes).
BARE_CRIT_MASS_KG = {
    "Pu238": 10.0, "Pu239": 10.2, "Pu240": 40.0, "Pu241": 12.3, "Pu242": 85.0,
    "U235": 47.0, "U233": 16.0, "Np237": 60.0,
}
SQ_PU_KG = 8.0           # IAEA significant quantity, total Pu
SELF_PROTECT_HEAT_WKG = 2.0     # ~W/kg above which weaponization is hampered (heat)

# Reference Pu vectors (wt%) for the comparison plot.
REF_VECTORS = {
    "Weapons-grade":  {"Pu238": 0.012, "Pu239": 93.8, "Pu240": 5.8, "Pu241": 0.35, "Pu242": 0.02},
    "Reactor-grade\n(typical LWR ~33 GWd/t)": {"Pu238": 1.3, "Pu239": 60.3, "Pu240": 24.3, "Pu241": 9.1, "Pu242": 5.0},
}


def load_inventory(path):
    g = {}
    for r in csv.DictReader(io.open(path, encoding="utf-8")):
        g[r["nuclide"]] = float(r["grams"])
    return g


def pu_grade(pu240_wo):
    if pu240_wo < 7.0:
        return "Weapons-grade"
    if pu240_wo < 19.0:
        return "Fuel-grade"
    return "Reactor-grade"


def compute(g, n_batches):
    pu_g = {p: g.get(p, 0.0) for p in PU}
    pu_tot = sum(pu_g.values())
    pu_wo = {p: 100.0 * pu_g[p] / pu_tot for p in PU}
    fissile = pu_g["Pu239"] + pu_g["Pu241"]

    # decay heat (Pu metal: Pu isotopes + in-grown Am-241; exclude Cm — chemically
    # separated out of a Pu product).
    pu_heat_W = sum(pu_g[p] * DECAY_HEAT_W_PER_G[p] for p in PU) \
        + g.get("Am241", 0.0) * DECAY_HEAT_W_PER_G["Am241"]
    pu_heat_wkg = pu_heat_W / (pu_tot / 1000.0)

    # spontaneous-fission neutrons: Pu-only (weapon predetonation) and total
    # (incl. Cm-244, which dominates the spent-fuel handling field).
    pu_sf = sum(pu_g[p] * SF_NEUTRONS_N_PER_S_PER_G.get(p, 0.0) for p in PU)
    pu_sf_nskg = pu_sf / (pu_tot / 1000.0)
    cm_sf = g.get("Cm244", 0.0) * SF_NEUTRONS_N_PER_S_PER_G["Cm244"]

    # spent uranium enrichment
    u_g = {x: g.get(x, 0.0) for x in U}
    u_tot = sum(u_g.values())
    u235_wo = 100.0 * u_g["U235"] / u_tot if u_tot else 0.0

    # INDICATIVE bare critical mass of the Pu vector (reciprocal-mass weighting of
    # pure-isotope bare-sphere critical masses) — transparent approximation.
    inv = sum((pu_wo[p] / 100.0) / BARE_CRIT_MASS_KG[p] for p in PU)
    m_crit_kg = 1.0 / inv

    # INDICATIVE Bathke FOM1 = 1 - log10[ M/800 + M*h/4500 + M*D/50 ].
    # M = bare critical mass (kg), h = heat (W/kg), D = dose rate (rad/h) at 1 m
    # from 0.2*M. We have M (indicative) and h; D needs the gamma-source calc, so
    # we report the heat+mass contribution and bound the effect of D.
    term_mass = m_crit_kg / 800.0
    term_heat = m_crit_kg * pu_heat_wkg / 4500.0
    bracket_no_dose = term_mass + term_heat
    fom1_no_dose = 1.0 - math.log10(bracket_no_dose)
    # illustrative dose sensitivity: a modest RGPu dose D ~ 1-5 rad/h
    fom1_dose5 = 1.0 - math.log10(bracket_no_dose + m_crit_kg * 5.0 / 50.0)

    return dict(
        pu_g=pu_g, pu_tot=pu_tot, pu_wo=pu_wo, fissile=fissile,
        fissile_frac=100.0 * fissile / pu_tot, grade=pu_grade(pu_wo["Pu240"]),
        pu_heat_W=pu_heat_W, pu_heat_wkg=pu_heat_wkg,
        pu_sf=pu_sf, pu_sf_nskg=pu_sf_nskg, cm_sf=cm_sf,
        u_g=u_g, u_tot=u_tot, u235_wo=u235_wo,
        m_crit_kg=m_crit_kg, term_mass=term_mass, term_heat=term_heat,
        fom1_no_dose=fom1_no_dose, fom1_dose5=fom1_dose5,
        sq_core=pu_tot / 1000.0 / SQ_PU_KG,
        pu_per_batch_kg=pu_tot / 1000.0 / n_batches,
        sq_per_batch=(pu_tot / 1000.0 / n_batches) / SQ_PU_KG,
        n_batches=n_batches,
        ma={m: g.get(m, 0.0) for m in MINOR_ACTINIDES},
    )


def make_plots(c, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Plot 1 — Pu isotopic vector vs reference grades
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = ["Aegis-40\n(42.8 GWd/t)"] + list(REF_VECTORS.keys())
    x = range(len(PU))
    width = 0.26
    series = [[c["pu_wo"][p] for p in PU]] + \
             [[REF_VECTORS[k].get(p, 0.0) for p in PU] for k in REF_VECTORS]
    colors = ["#b22222", "#444444", "#1f77b4"]
    for i, (lab, s) in enumerate(zip(labels, series)):
        ax.bar([xi + (i - 1) * width for xi in x], s, width, label=lab, color=colors[i])
    ax.set_xticks(list(x)); ax.set_xticklabels(PU)
    ax.set_ylabel("wt % of total Pu"); ax.set_title("Discharge plutonium vector")
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "pu_vector.png"), dpi=130)
    plt.close(fig)

    # Plot 2 — self-protection barriers vs thresholds
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 4))
    a1.bar(["Aegis-40 Pu"], [c["pu_heat_wkg"]], color="#b22222", width=0.5)
    a1.axhline(SELF_PROTECT_HEAT_WKG, ls="--", color="k")
    a1.text(0, SELF_PROTECT_HEAT_WKG * 1.1, "~2 W/kg self-protection", fontsize=8)
    a1.set_ylabel("Decay heat (W / kg-Pu)"); a1.set_title("Thermal barrier")
    a1.grid(axis="y", alpha=0.3)
    a2.bar(["Pu-only\n(predetonation)", "incl. Cm-244\n(handling field)"],
           [c["pu_sf_nskg"], (c["pu_sf"] + c["cm_sf"]) / (c["pu_tot"] / 1000.0)],
           color=["#b22222", "#777777"], width=0.6)
    a2.set_yscale("log"); a2.set_ylabel("SF neutrons (n/s / kg-Pu)")
    a2.set_title("Neutron barrier"); a2.grid(axis="y", alpha=0.3)
    fig.suptitle("Intrinsic self-protection of the discharge plutonium")
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "self_protection.png"), dpi=130)
    plt.close(fig)

    # Plot 3 — SNM mass / SQ inventory
    fig, ax = plt.subplots(figsize=(7, 4))
    masses = [c["pu_tot"] / 1000.0] + [c["ma"][m] / 1000.0 for m in MINOR_ACTINIDES]
    names = ["Pu (total)"] + MINOR_ACTINIDES
    ax.bar(names, masses, color="#4477aa")
    ax.set_ylabel("kg in core at discharge")
    ax.set_title(f"Heavy-metal SNM at discharge — Pu = {c['sq_core']:.1f} IAEA SQ "
                 f"(8 kg/SQ)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "snm_inventory.png"), dpi=130)
    plt.close(fig)
    return ["pu_vector.png", "self_protection.png", "snm_inventory.png"]


def write_report(c, outdir, plots, inv_path):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    with io.open(os.path.join(outdir, "pu_vector.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["isotope", "grams", "wt_percent_of_Pu"])
        for p in PU:
            w.writerow([p, f"{c['pu_g'][p]:.1f}", f"{c['pu_wo'][p]:.2f}"])
        w.writerow(["Pu_total", f"{c['pu_tot']:.1f}", "100.00"])

    L = []
    L.append("# Safeguards & non-proliferation — attractiveness of discharge "
             "materials (FER 3S, §8.5/§8.7)\n")
    L.append(f"- Generated: `{now}`")
    L.append(f"- Source inventory: `{inv_path}` (whole-core discharge, 42.8 GWd/t, "
             "OpenMC depletion). Produced by [NEU]; framing by [3S].")
    L.append("- Basis: whole 21-FA core at discharge; per-batch = /4 (4-batch reload).\n")

    L.append("## 1. Plutonium vector and grade\n")
    L.append("| Isotope | grams | wt % of Pu |")
    L.append("|---|---|---|")
    for p in PU:
        L.append(f"| {p} | {c['pu_g'][p]:,.0f} | {c['pu_wo'][p]:.2f} |")
    L.append(f"| **Total Pu** | **{c['pu_tot']:,.0f} g ({c['pu_tot']/1000:.1f} kg)** | 100.00 |")
    L.append("")
    L.append(f"- **Grade: {c['grade'].upper()}** (Pu-240 = {c['pu_wo']['Pu240']:.1f} wt%; "
             "weapons-grade is <7%, reactor-grade is >19%).")
    L.append(f"- Fissile fraction (Pu-239+Pu-241): **{c['fissile_frac']:.1f}%** "
             f"(weapons-grade Pu-239 alone is >93%).")
    L.append(f"- High burnup pushes Pu-239 down to {c['pu_wo']['Pu239']:.0f}% and "
             f"Pu-240/Pu-241/Pu-238 up — *more* degraded than a typical 33 GWd/t "
             "LWR discharge.\n")

    L.append("## 2. Intrinsic self-protection barriers\n")
    L.append("| Barrier | Value | Significance |")
    L.append("|---|---|---|")
    L.append(f"| Decay heat | **{c['pu_heat_wkg']:.1f} W/kg-Pu** ({c['pu_heat_W']:.0f} W total) | "
             f"≫ ~{SELF_PROTECT_HEAT_WKG:.0f} W/kg 'self-protection' level; heat damages a device |")
    L.append(f"| SF neutrons (Pu metal) | **{c['pu_sf_nskg']:.2e} n/s/kg-Pu** | "
             "predetonation background (Pu-240/238/242) |")
    L.append(f"| SF neutrons incl. Cm-244 | {(c['pu_sf']+c['cm_sf'])/(c['pu_tot']/1000):.2e} n/s/kg | "
             "Cm-244 dominates the spent-fuel handling field |")
    L.append("")

    L.append("## 3. Spent uranium (non-attractive)\n")
    L.append(f"- U-235 at discharge: **{c['u235_wo']:.2f} wt%** — far below the 20% "
             "LEU/HEU line and the ~90% weapons line. The recovered uranium is "
             "**not** a usable enrichment.\n")

    L.append("## 4. Significant-quantity accounting (IAEA, Pu = 8 kg/SQ)\n")
    L.append(f"- Whole-core Pu: {c['pu_tot']/1000:.1f} kg = **{c['sq_core']:.1f} SQ**.")
    L.append(f"- Per discharge batch (1/{c['n_batches']} core): "
             f"{c['pu_per_batch_kg']:.1f} kg = **{c['sq_per_batch']:.1f} SQ** — but "
             "embedded in intensely radioactive intact assemblies.")
    L.append("- Minor actinides (kg): " +
             ", ".join(f"{m} {c['ma'][m]/1000:.2f}" for m in MINOR_ACTINIDES) +
             " — Np-237/Am are materials of safeguards interest but require "
             "reprocessing to separate.\n")

    L.append("## 5. Material-attractiveness FOM (Bathke) — INDICATIVE\n")
    L.append("Bathke FOM₁ = 1 − log₁₀[ M/800 + M·h/4500 + M·D/50 ] "
             "(M = bare critical mass kg, h = heat W/kg, D = dose rate rad/h at 1 m "
             "from 0.2·M). Higher FOM = more attractive; FOM₁ > 1 ≈ weapons-usable.\n")
    L.append("| Input | Value | Basis |")
    L.append("|---|---|---|")
    L.append(f"| M (bare critical mass) | ~{c['m_crit_kg']:.1f} kg | **indicative** — "
             "reciprocal-mass weighting of pure-isotope bare spheres |")
    L.append(f"| h (decay heat) | {c['pu_heat_wkg']:.1f} W/kg | computed above (rigorous) |")
    L.append("| D (dose rate) | pending | needs the gamma-source calc (#7) |")
    L.append(f"| FOM₁ (heat+mass terms only) | **~{c['fom1_no_dose']:.2f}** | upper bound (no dose) |")
    L.append(f"| FOM₁ (with illustrative D=5 rad/h) | ~{c['fom1_dose5']:.2f} | dose lowers it |")
    L.append("")
    L.append("**Honest interpretation (this is the FER-credible reading):** even at "
             f"high burnup the reactor-grade Pu sits at FOM₁ ≈ {c['fom1_dose5']:.1f}–"
             f"{c['fom1_no_dose']:.1f}, i.e. still nominally 'attractive' by the "
             "intrinsic metric — this is Bathke's own finding that heat/neutron "
             "penalties alone do **not** render separated Pu unusable. The decisive "
             "proliferation resistance is therefore **extrinsic**: the Pu is locked "
             "inside self-protecting, intensely radioactive intact spent-fuel "
             "assemblies (whole-assembly dose ≫ the 1 Gy/h self-protecting "
             "threshold), under IAEA safeguards, in a once-through cycle with no "
             "reprocessing. High burnup *adds* to the intrinsic barriers (heat, "
             "neutrons, degraded vector) on top of that.\n")

    L.append("## Plots\n")
    for p in plots:
        L.append(f"![{p}]({p})")
    L.append("")

    L.append("## Method notes & open items\n")
    L.append("- Decay-heat / SF-neutron / critical-mass constants are standard "
             "isotopic values (encoded in the script with sources).")
    L.append("- **Rigorous FOM refinement (small WSL follow-up):** compute the bare "
             "critical mass M of the *actual* Pu vector with an OpenMC bare-sphere "
             "k_eff search, and the dose rate D from the gamma source term (#7). "
             "Both only *lower* the FOM, so the qualitative conclusion is unchanged.")
    L.append("- Burnup-trajectory view (Pu-239 fraction vs burnup) is a further "
             "option — needs the per-step Pu vector from the core depletion h5 (WSL).")
    L.append("- Cite: Bathke et al., *Nucl. Technol.* 179 (2012) 5; Wu et al., "
             "*Int. J. Energy Res.* (2020); IAEA Safeguards Glossary (SQ).\n")

    path = os.path.join(outdir, "safeguards_attractiveness.md")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", default=DEFAULT_INVENTORY)
    ap.add_argument("--n-batches", type=int, default=4)
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    args = ap.parse_args(argv)

    os.makedirs(args.outdir, exist_ok=True)
    g = load_inventory(args.inventory)
    c = compute(g, args.n_batches)
    plots = make_plots(c, args.outdir)
    path = write_report(c, args.outdir, plots, args.inventory)

    print("=== Safeguards / attractiveness ===")
    print(f"  Pu total : {c['pu_tot']/1000:.1f} kg  grade={c['grade']}  "
          f"Pu-239={c['pu_wo']['Pu239']:.1f}%  Pu-240={c['pu_wo']['Pu240']:.1f}%")
    print(f"  heat     : {c['pu_heat_wkg']:.1f} W/kg-Pu  SF(Pu)={c['pu_sf_nskg']:.2e} n/s/kg")
    print(f"  spent-U  : {c['u235_wo']:.2f} wt% U-235  |  SQ(core)={c['sq_core']:.1f}")
    print(f"  FOM1     : ~{c['fom1_no_dose']:.2f} (heat+mass, indicative; M~{c['m_crit_kg']:.1f} kg)")
    print(f"  report   : {path}")
    print(f"  plots    : {', '.join(plots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
