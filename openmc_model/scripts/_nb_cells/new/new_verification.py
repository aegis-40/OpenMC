## 6b · Axial-shape VERIFICATION (Finding 2)
# Homogeneous core, NO burnable absorber, uniform enrichment.  The BOC axial
# fission shape MUST be a smooth chopped-cosine (leakage-dominated).  A
# saw-tooth or anomalously flat shape would indicate a tally reshape /
# axial-bin / statistics bug rather than physics.  We overlay a best-fit
# cosine and report the RMS deviation as the pass criterion.

def calc_axial_verification(enrich=4.0):
    print("[V] Axial-shape verification: homogeneous, no-BA core ...")
    g = globals()
    keys  = ["ENRICH_INNER", "ENRICH_MID", "ENRICH_OUTER",
             "GD_POSITIONS", "ER_POSITIONS", "RADIAL_GD_ZONING"]
    saved = {k: g[k] for k in keys}
    fz = None
    try:
        g["ENRICH_INNER"] = g["ENRICH_MID"] = g["ENRICH_OUTER"] = enrich
        g["GD_POSITIONS"] = []
        g["ER_POSITIONS"] = []
        g["RADIAL_GD_ZONING"] = False
        d = _run_dir("10_axial_verif")
        model, _, info = build_core()
        H = ACTIVE_HEIGHT
        S = N_CORE * FA_PITCH
        NZ = 60
        mz = openmc.RegularMesh(); mz.dimension = (1, 1, NZ)
        mz.lower_left  = (-S/2, -S/2, -H/2)
        mz.upper_right = ( S/2,  S/2,  H/2)
        t = openmc.Tally(name="axial_verif")
        t.filters = [openmc.MeshFilter(mz)]; t.scores = ["fission"]
        model.tallies = openmc.Tallies([t])
        _run_model(model, d, tag="axial_verif")
        sps = sorted(d.glob("statepoint.*.h5"))
        with openmc.StatePoint(str(sps[-1])) as sp:
            fz = sp.get_tally(name="axial_verif").get_values(scores=["fission"]).ravel()
    finally:
        g.update(saved)

    H  = ACTIVE_HEIGHT
    NZ = len(fz)
    z  = np.linspace(-H/2 + H/(2*NZ), H/2 - H/(2*NZ), NZ)
    fz_n = np.asarray(fz, float) / np.asarray(fz, float).mean()

    fit = None; He = float("nan"); rms = float("nan")
    try:
        from scipy.optimize import curve_fit
        def cosmod(zz, A, He_):  # chopped cosine with extrapolated height
            return A * np.cos(np.pi * zz / He_)
        popt, _ = curve_fit(cosmod, z, fz_n, p0=[fz_n.max(), H * 1.2],
                            bounds=([0.0, H], [5.0, 4.0 * H]))
        fit = cosmod(z, *popt); He = float(popt[1])
        rms = float(np.sqrt(np.mean((fz_n - fit) ** 2)))
    except Exception as e:
        print(f"   cosine fit unavailable ({e}); inspect the curve visually.")

    results["axial_verif_Fz"]          = round(float(fz_n.max()), 3)
    results["axial_verif_cosine_rms"]  = (round(rms, 4) if rms == rms else None)
    print(f"   no-BA F_z = {fz_n.max():.3f} | extrapolated height He = {He:.1f} cm "
          f"(active {H:.0f}) | cosine RMS = {rms:.4f}")
    print("   PASS if smooth & cosine-like (RMS < ~0.05); a saw-tooth / large RMS "
          "⇒ reshape or statistics bug, not physics.")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(z, fz_n, "ro-", lw=1.5, ms=4, label="OpenMC (homogeneous, no BA)")
    if fit is not None:
        ax.plot(z, fit, "b--", lw=2, label=f"cosine fit (He={He:.0f} cm)")
    ax.axhline(1.0, color="gray", ls=":")
    ax.set_xlabel("z (cm)"); ax.set_ylabel("Relative axial fission rate")
    ax.set_title(f"Axial verification (homogeneous, no BA)\nF_z={fz_n.max():.2f}, cosine RMS={rms:.4f}")
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
    out = PLOTS / "axial_verification.png"
    fig.savefig(out, dpi=200, bbox_inches="tight"); print(f"   saved: {out}")
    plt.show()
    return fz_n

calc_axial_verification()
