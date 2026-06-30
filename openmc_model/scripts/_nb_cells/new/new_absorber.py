def extract_absorber_inventory(dep_results, run_dir):
    """Gd-157 / Er-167 atom-density evolution.

    FIX (Finding 6): the absorber inventory is now reported AT THE CYCLE EOC
    burnup (fresh-core B1, where k=1), not at the end of the full ~1900-EFPD
    depletion horizon.  Reading the last horizon step made Er-167 look ~3 %
    "remaining" because that point is ~170 GWd/t — far past the ~43 GWd/t the
    fuel actually sees.  Er is a slow burner, so a substantial residual at the
    real EOC is expected and supports cold shutdown margin."""
    run_dir = Path(run_dir)
    name_by_id = {}
    mats_xml = run_dir / "materials.xml"
    if mats_xml.is_file():
        try:
            for m in openmc.Materials.from_xml(str(mats_xml)):
                name_by_id[str(m.id)] = m.name
        except Exception as e:
            print(f"   could not parse materials.xml: {e}")
    gd_ids = [i for i, n in name_by_id.items() if "Gd" in n]
    er_ids = [i for i, n in name_by_id.items() if "Er" in n]

    def _sum_atoms(ids, nuc):
        tot = times = None
        for mid in ids:
            try:
                t, a = dep_results.get_atoms(mid, nuc)
            except Exception:
                continue
            a = np.array(a, float); times = np.array(t, float)
            tot = a if tot is None else tot + a
        return times, tot

    t_gd, gd157 = _sum_atoms(gd_ids, "Gd157")
    t_er, er167 = _sum_atoms(er_ids, "Er167")
    base_t = t_gd if t_gd is not None else t_er
    burnup = SPECIFIC_POWER * base_t / 86400.0 / 1000.0 if base_t is not None else None

    # cycle-relevant EOC burnup: fresh-core B1 (k=1 crossing) if known, else
    # the equilibrium discharge target.
    b1_efpd = results.get("fresh_core_B1_efpd")
    if b1_efpd:
        eoc_bu = SPECIFIC_POWER * float(b1_efpd) / 1000.0
    else:
        eoc_bu = results.get("burnup_discharge_GWd_per_MTU")

    def _at_eoc(frac):
        if burnup is None or eoc_bu is None:
            return None
        return float(np.interp(eoc_bu, burnup, frac) * 100.0)

    fig, ax = plt.subplots(figsize=(8, 5)); plotted = False
    if gd157 is not None and gd157[0] > 0:
        gdf = gd157 / gd157[0]
        ax.plot(burnup, gdf*100, "o-", color="navy", label="Gd-157 / Gd-157₀")
        results["gd157_eoc_fraction_pct"]      = round(_at_eoc(gdf), 1) if _at_eoc(gdf) is not None else None
        results["gd157_endhorizon_pct"]        = round(float(gdf[-1]*100), 1)
        plotted = True
    if er167 is not None and er167[0] > 0:
        erf = er167 / er167[0]
        ax.plot(burnup, erf*100, "s--", color="darkorange", label="Er-167 / Er-167₀")
        results["er167_eoc_fraction_pct"]      = round(_at_eoc(erf), 1) if _at_eoc(erf) is not None else None
        results["er167_endhorizon_pct"]        = round(float(erf[-1]*100), 1)
        plotted = True
    if plotted:
        if eoc_bu is not None:
            ax.axvline(eoc_bu, color="green", ls=":", lw=1.5,
                       label=f"cycle EOC ≈ {eoc_bu:.0f} GWd/t")
        ax.set_xlabel("Core-average burnup (GWd/tHM)")
        ax.set_ylabel("Remaining absorber inventory (%)")
        ax.set_title("Absorber Inventory Depletion — Aegis-40 (3D core)")
        ax.set_ylim(0, 110); ax.legend(); ax.grid(alpha=0.3)
        out = PLOTS / "absorber_inventory.png"
        fig.savefig(out, dpi=200, bbox_inches="tight"); print(f"   saved: {out}")
        plt.show()
        print(f"   Gd-157 @ EOC(~{eoc_bu:.0f} GWd/t) = {results.get('gd157_eoc_fraction_pct')}%"
              f"  (design: nearly depleted by EOC — fast burnout, holds BOC spike)")
        print(f"   Er-167 @ EOC(~{eoc_bu:.0f} GWd/t) = {results.get('er167_eoc_fraction_pct')}%"
              f"  (design: slow burner; notable residual expected — aids cold SDM)")
        print(f"   [diagnostic] end-of-horizon: Gd-157 {results.get('gd157_endhorizon_pct')}%, "
              f"Er-167 {results.get('er167_endhorizon_pct')}%")
    else:
        plt.close(fig); print("   no absorber atom data extracted.")
