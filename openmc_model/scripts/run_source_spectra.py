#!/usr/bin/env python3
"""Spent-fuel gamma & neutron source term for shielding / NPP layout (FER §8.11 #7).

Produces the radiation **source term** of the Aegis-40 spent fuel that feeds
shielding sizing and plant-layout separation distances (cask walls, pool depth,
ISFSI / building stand-off). Physics by [NEU] from the OpenMC discharge inventory;
shielding/layout use by [LAY/Elbek].

Two tiers:

  * **Estimate (this script, Windows, default):** neutron source from spontaneous
    fission of the discharge inventory (the dominant spent-fuel neutron mechanism)
    + a gamma source built from the principal decay lines of the governing emitters
    (Cs-137, Cs-134, Eu-154, Am-241). This is a sound first-order source term for
    **~5+ yr cooling** (dry-cask / ISFSI layout), where those nuclides dominate the
    field. It is a *lower bound at short cooling* (the curated 20-nuclide inventory
    omits Ce-144/Ru-106/Sb-125/Eu-155/short-lived emitters and (alpha,n)).

  * **Rigorous (OpenMC, WSL — documented below, not run here):** the full decay
    photon spectrum via `material.get_decay_photon_energy()` on the depleted+decayed
    materials, and SF+(alpha,n) neutrons, at each cooling time. This is the
    Digital-Appendix-grade number.

Pure-Python + matplotlib. Outputs to docs/competition/shielding/.

Usage:
    py scripts/run_source_spectra.py
        [--inventory docs/competition/waste/discharge_inventory.csv]
        [--n-assemblies 21] [--outdir docs/competition/shielding]
"""

from __future__ import annotations

import argparse
import csv
import datetime
import io
import os

DEFAULT_INVENTORY = os.path.join("docs", "competition", "waste", "discharge_inventory.csv")
DEFAULT_OUTDIR = os.path.join("docs", "competition", "shielding")
MEV_TO_J = 1.602176634e-13

# Spontaneous-fission neutron yield, n/s per gram (the dominant spent-fuel neutron
# source; Cm-244 governs). (alpha,n) in the oxide adds a secondary contribution
# that needs a dedicated calc (SOURCES4C / OpenMC) — flagged, not included here.
SF_NEUTRONS_N_PER_S_PER_G = {
    "Cm244": 1.10e7, "Cm242": 2.10e7, "Pu238": 2.59e3, "Pu240": 1.02e3,
    "Pu242": 1.72e3, "Pu239": 2.18e-2, "Pu241": 5.0e-2, "Cf252": 2.3e12,
}
AVG_SF_NEUTRON_ENERGY_MEV = 2.0   # ~Watt-spectrum mean for shielding

# Principal gamma lines: nuclide -> [(energy_MeV, photons per decay), ...].
# Curated to the dominant emitters present in the inventory; others (Co-60, Eu-155,
# Ce-144/Pr-144, Ru-106/Rh-106, Sb-125) contribute 0 unless the inventory lists
# them — add lines here if a fuller inventory is supplied.
GAMMA_LINES = {
    "Cs137": [(0.6617, 0.851)],                       # via Ba-137m
    "Cs134": [(0.6047, 0.976), (0.7958, 0.851), (0.5693, 0.154), (1.3650, 0.030)],
    "Eu154": [(0.1232, 0.404), (0.7232, 0.202), (1.2745, 0.355), (1.0048, 0.180)],
    "Am241": [(0.0595, 0.359)],
    "Eu155": [(0.0866, 0.307), (0.1053, 0.211)],      # 0 unless inventory has it
    "Co60":  [(1.1732, 0.999), (1.3325, 1.000)],      # activation product, if listed
    "Sb125": [(0.4276, 0.297), (0.6004, 0.178)],
    "Ce144": [(0.1335, 0.111)],                       # Pr-144 hard line omitted (beta)
}
# Energy-group edges (MeV) for the shielding spectrum.
GROUP_EDGES = [0.0, 0.1, 0.3, 0.6, 0.8, 1.0, 1.5, 3.0]


def load_inventory(path):
    g, a = {}, {}
    for r in csv.DictReader(io.open(path, encoding="utf-8")):
        g[r["nuclide"]] = float(r["grams"])
        a[r["nuclide"]] = float(r.get("activity_Bq", 0.0) or 0.0)
    return g, a


def neutron_source(grams):
    contrib = {n: grams.get(n, 0.0) * y
               for n, y in SF_NEUTRONS_N_PER_S_PER_G.items() if grams.get(n, 0.0) > 0}
    total = sum(contrib.values())
    return total, dict(sorted(contrib.items(), key=lambda kv: -kv[1]))


def gamma_source(activity):
    """Return total photons/s, energy rate (MeV/s), per-line and grouped spectra."""
    lines = []   # (nuclide, E_MeV, photons_per_s)
    for nuc, act in activity.items():
        for (e, inten) in GAMMA_LINES.get(nuc, []):
            if act > 0:
                lines.append((nuc, e, act * inten))
    total_ph = sum(p for _, _, p in lines)
    energy_rate = sum(e * p for _, e, p in lines)         # MeV/s
    groups = [0.0] * (len(GROUP_EDGES) - 1)
    for _, e, p in lines:
        for i in range(len(GROUP_EDGES) - 1):
            if GROUP_EDGES[i] <= e < GROUP_EDGES[i + 1]:
                groups[i] += p
                break
    return total_ph, energy_rate, sorted(lines, key=lambda t: -t[2]), groups


def make_plot(lines, groups, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    # grouped spectrum
    centers = [f"{GROUP_EDGES[i]:.1f}-{GROUP_EDGES[i+1]:.1f}"
               for i in range(len(GROUP_EDGES) - 1)]
    a1.bar(centers, groups, color="#cc8800")
    a1.set_yscale("log"); a1.set_ylabel("photons/s (whole core)")
    a1.set_xlabel("gamma energy group (MeV)")
    a1.set_title("Gamma source spectrum"); a1.tick_params(axis="x", rotation=30)
    a1.grid(axis="y", alpha=0.3)
    # top discrete lines
    top = lines[:8]
    labels = [f"{n}\n{e:.3f}" for n, e, _ in top]
    a2.bar(labels, [p for _, _, p in top], color="#b22222")
    a2.set_yscale("log"); a2.set_ylabel("photons/s")
    a2.set_title("Principal gamma lines"); a2.tick_params(axis="x", rotation=30, labelsize=7)
    a2.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    p = os.path.join(outdir, "gamma_source_spectrum.png")
    fig.savefig(p, dpi=130); plt.close(fig)
    return os.path.basename(p)


def write_report(outdir, grams, activity, n_assem, plotname):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    n_tot, n_contrib = neutron_source(grams)
    ph_tot, e_rate, lines, groups = gamma_source(activity)
    gamma_W = e_rate * MEV_TO_J
    mean_e = e_rate / ph_tot if ph_tot else 0.0
    n_per_fa = n_tot / n_assem
    ph_per_fa = ph_tot / n_assem

    # CSV — grouped gamma spectrum
    with io.open(os.path.join(outdir, "gamma_spectrum.csv"), "w",
                 encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["E_low_MeV", "E_high_MeV", "photons_per_s_core"])
        for i in range(len(GROUP_EDGES) - 1):
            w.writerow([GROUP_EDGES[i], GROUP_EDGES[i + 1], f"{groups[i]:.4e}"])

    L = []
    L.append("# Spent-fuel gamma & neutron source term for shielding / layout "
             "(FER §8.11 #7) — generated\n")
    L.append(f"- Generated: `{now}`")
    L.append("- Source: OpenMC discharge inventory (whole 21-FA core, 42.8 GWd/t). "
             "Produced by [NEU]; shielding/layout use by [LAY].")
    L.append("- **Estimate tier** (Windows): SF neutrons + principal-line gammas of "
             "the governing emitters. Valid as a first-order source term for **~5+ yr "
             "cooling** (dry-cask / ISFSI layout); a lower bound at short cooling.\n")

    L.append("## Neutron source (spontaneous fission)\n")
    L.append("| Nuclide | n/s (core) | share |")
    L.append("|---|---|---|")
    for n, v in list(n_contrib.items())[:6]:
        L.append(f"| {n} | {v:.3e} | {100*v/n_tot:.1f}% |")
    L.append(f"| **Total** | **{n_tot:.3e} n/s** | (~{n_per_fa:.2e} n/s per assembly) |")
    L.append("")
    L.append(f"- Mean SF neutron energy ~{AVG_SF_NEUTRON_ENERGY_MEV:.1f} MeV "
             "(Watt-like) for neutron-shield sizing.")
    L.append("- **Cm-244 dominates** the neutron field — the key driver of cask "
             "neutron shielding and stand-off. **(α,n)** in the oxide adds a "
             "secondary term (needs SOURCES4C / OpenMC; not included here).\n")

    L.append("## Gamma source\n")
    L.append("| Quantity | Value |")
    L.append("|---|---|")
    L.append(f"| Total photon emission | **{ph_tot:.3e} photons/s** ({ph_per_fa:.2e} per FA) |")
    L.append(f"| Gamma energy rate | {e_rate:.3e} MeV/s = **{gamma_W:.2e} W** |")
    L.append(f"| Mean photon energy | {mean_e:.3f} MeV |")
    L.append("")
    L.append("Principal lines (photons/s, whole core):\n")
    L.append("| Nuclide | E (MeV) | photons/s |")
    L.append("|---|---|---|")
    for n, e, p in lines[:8]:
        L.append(f"| {n} | {e:.4f} | {p:.3e} |")
    L.append("")
    L.append("- The **0.662 MeV Cs-137** and **0.6-0.8 MeV Cs-134** lines carry the "
             "penetrating gamma load → set the cask/pool gamma-shield thickness. "
             "Am-241 0.059 MeV is soft (self-shielded). Cs-134 (T½ 2.1 yr) decays "
             "away over the first decade, so the gamma field eases with cooling.\n")

    L.append("## Shielding / layout read-out\n")
    L.append("| Driver | Value | Use |")
    L.append("|---|---|---|")
    L.append(f"| Gamma source | {ph_tot:.2e} ph/s ({mean_e:.2f} MeV avg) | gamma wall thickness |")
    L.append(f"| Neutron source | {n_tot:.2e} n/s | neutron shield + stand-off |")
    L.append(f"| n / gamma ratio | {n_tot/ph_tot:.2e} | mixed-field weighting |")
    L.append(f"| Per assembly | {ph_per_fa:.2e} ph/s, {n_per_fa:.2e} n/s | single-cask basis |")
    L.append("")

    L.append("![gamma spectrum](%s)\n" % plotname)

    L.append("## Rigorous extraction (OpenMC, WSL — for the final/appendix numbers)\n")
    L.append("```")
    L.append("# from the core depletion results, at each cooling time:")
    L.append("results = openmc.deplete.Results('08_depletion_baseline/depletion_results.h5')")
    L.append("mats = results.export_to_materials(last_step)      # depleted compositions")
    L.append("# decay to cooling time t (zero-flux IndependentOperator, see run_decay_heat.py)")
    L.append("openmc.config['chain_file'] = chain")
    L.append("src = mat.get_decay_photon_energy()                # photons/s + full spectrum")
    L.append("# neutron: SF from nuclide yields (+ (alpha,n) via SOURCES4C)")
    L.append("```")
    L.append("This returns the **full** decay-photon spectrum (all emitters, all "
             "lines) at each cooling time — superseding the principal-line estimate "
             "above and giving the Digital-Appendix-grade gamma source. The neutron "
             "SF total here is already representative; add (α,n) for completeness.\n")

    L.append("## Notes\n")
    L.append("- Whole-core values; divide by 21 for per-assembly (single-cask) "
             "or scale to the chosen cask loading.")
    L.append("- Activities are at the inventory reference time; short-lived emitters "
             "(Ce-144/Ru-106/Eu-155 etc.) not in the curated set raise the gamma "
             "field at <5 yr cooling — use the OpenMC spectrum there.")
    L.append("- Cite: ANSI/ANS-6.1.1 (gamma) and shielding standards for the dose "
             "conversion in §8.11/§8.10.\n")

    path = os.path.join(outdir, "source_spectra.md")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return path, n_tot, ph_tot, gamma_W


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", default=DEFAULT_INVENTORY)
    ap.add_argument("--n-assemblies", type=int, default=21)
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    args = ap.parse_args(argv)

    os.makedirs(args.outdir, exist_ok=True)
    grams, activity = load_inventory(args.inventory)
    _, _, lines, groups = gamma_source(activity)
    plotname = make_plot(lines, groups, args.outdir)
    path, n_tot, ph_tot, gamma_W = write_report(
        args.outdir, grams, activity, args.n_assemblies, plotname)

    print("=== Source term for shielding / layout ===")
    print(f"  neutron : {n_tot:.3e} n/s (core)  ~{n_tot/args.n_assemblies:.2e} n/s/FA")
    print(f"  gamma   : {ph_tot:.3e} ph/s (core)  = {gamma_W:.2e} W")
    print(f"  report  : {path}")
    print(f"  note    : estimate tier (~5+ yr cooling); rigorous = OpenMC WSL (see md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
