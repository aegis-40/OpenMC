## 6 · 3D power peaking — per-pin reconstruction (Findings 1 & 3)
# F_ΔH and F_q are computed pin-by-pin from absolute coordinates, NOT from a
# coarse RegularMesh max/mean.  The old one-cell-per-pin mesh drifted ~0.7 cm
# (>½ pin) across the core because FA_PITCH/17 ≠ PIN_PITCH (0.072 cm water gap
# per side), and its `>0` mask kept water-gap/edge cells that deflated the mean
# and inflated F_ΔH to a non-physical 2.27.  Here every fuel pin's power is
# summed from a fine mesh by footprint, guide tubes / water gaps excluded by
# construction.  Reshape order is made explicit (Finding 2 root cause).

def _fuel_pin_geom():
    """Absolute (x,y) centres of every fuel pin + the FA id it belongs to.
       Excludes the 25 guide/instrument tubes per FA and non-fuel corner FAs.
       The 17×17 Westinghouse guide map is transpose-symmetric, so the SET of
       pin coordinates is independent of the (i,j) axis convention."""
    half    = (N_CORE - 1) / 2.0
    pin_off = (N_PIN  - 1) / 2.0
    px, py, fa = [], [], []
    fid = 0
    fa_ij = {}
    for j in range(N_CORE):
        for i in range(N_CORE):
            if CORE_MAP[N_CORE - 1 - j, i] != 1:
                continue
            fa_ij[fid] = (i, j)
            cx = (i - half) * FA_PITCH
            cy = (j - half) * FA_PITCH
            for (pi, pj) in FUEL_POS:
                px.append(cx + (pi - pin_off) * PIN_PITCH)
                py.append(cy + (pj - pin_off) * PIN_PITCH)
                fa.append(fid)
            fid += 1
    return np.array(px), np.array(py), np.array(fa, int), fid, fa_ij


def _reshape_mesh_xyz(flat, nx, ny, nz):
    """OpenMC mesh elements are ordered x-fastest, then y, then z
       (element id = ix + iy*nx + iz*nx*ny).  Reshape WITHOUT guessing:
       flat -> [iz, iy, ix] in C-order, then transpose to [ix, iy, iz].
       This removes the axial-reshape ambiguity flagged in the review."""
    return np.asarray(flat, float).reshape(nz, ny, nx).transpose(2, 1, 0)


# Engineering uncertainty on the raw MC peak (nuclear + measurement),
# per SSG-52 §3.18(f).  ~3 % is the NuScale-class allowance.
PEAKING_UNC = 1.03
F_DH_LIMIT, F_DH_DESIGN = 1.65, 1.55      # NUREG-1431 3.2.2 / our design target
F_Q_LIMIT,  F_Q_DESIGN  = 2.32, 2.00      # NUREG-1431 3.2.1 (K(z)=1 anchor)


def calc_flux_peaking():
    print("[9/9] Pin-power peaking (per-pin reconstruction) + 3D flux maps ...")
    d = _run_dir("09_flux_peaking")
    model, _, info = build_core()
    outer_half = info["outer_half_cm"]
    H = ACTIVE_HEIGHT
    S = N_CORE * FA_PITCH

    # Fine 3D fission mesh: ~3 cells per pin pitch so each pin footprint is
    # resolved from ABSOLUTE coordinates (immune to FA water-gap drift).
    CELLS_PER_PIN = 3
    NF = int(round(S / (PIN_PITCH / CELLS_PER_PIN)))
    NZ = 40
    mesh_3d = openmc.RegularMesh(); mesh_3d.dimension = (NF, NF, NZ)
    mesh_3d.lower_left  = (-S/2, -S/2, -H/2)
    mesh_3d.upper_right = ( S/2,  S/2,  H/2)
    t3d = openmc.Tally(name="fission_3d")
    t3d.filters = [openmc.MeshFilter(mesh_3d)]; t3d.scores = ["fission"]

    # Fine xy slice at z≈0 — cosmetic radial map only
    mesh_fine = openmc.RegularMesh(); mesh_fine.dimension = (200, 200, 1)
    mesh_fine.lower_left  = (-outer_half, -outer_half, -10)
    mesh_fine.upper_right = ( outer_half,  outer_half,  10)
    t_fine = openmc.Tally(name="fission_fine_xy")
    t_fine.filters = [openmc.MeshFilter(mesh_fine)]; t_fine.scores = ["fission"]

    model.tallies = openmc.Tallies([t3d, t_fine])
    _run_model(model, d, tag="flux_peaking")

    sps = sorted(d.glob("statepoint.*.h5"))
    with openmc.StatePoint(str(sps[-1])) as sp:
        flat3d = sp.get_tally(name="fission_3d").get_values(scores=["fission"]).ravel()
        flatxy = sp.get_tally(name="fission_fine_xy").get_values(scores=["fission"]).ravel()

    f3d = _reshape_mesh_xyz(flat3d, NF, NF, NZ)          # [ix, iy, iz]

    # —— per-pin fission-rate DENSITY by footprint (mean over captured cells:
    #    using mean not sum cancels the ±1-cell quantization in pin volume) ——
    px, py, fa_id, n_fa, fa_ij = _fuel_pin_geom()
    dx = S / NF
    xc = -S/2 + (np.arange(NF) + 0.5) * dx
    h  = PIN_PITCH / 2.0
    npins = len(px)
    pin_z = np.zeros((npins, NZ))
    for p in range(npins):
        ix = np.where((xc >= px[p] - h) & (xc < px[p] + h))[0]
        iy = np.where((xc >= py[p] - h) & (xc < py[p] + h))[0]
        if ix.size and iy.size:
            pin_z[p] = f3d[ix.min():ix.max()+1, iy.min():iy.max()+1, :].mean(axis=(0, 1))
    pin_col = pin_z.sum(axis=1)                          # axial-integrated column
    good = pin_col > 0
    pin_col_g = pin_col[good]; pin_z_g = pin_z[good]

    F_dh = float(pin_col_g.max() / pin_col_g.mean())     # radial enthalpy-rise
    F_q  = float(pin_z_g.max()   / pin_z_g.mean())       # true 3-D hot spot
    fz   = pin_z_g.sum(axis=0); fz_norm = fz / fz.mean()
    F_z  = float(fz_norm.max())

    F_dh_e = F_dh * PEAKING_UNC                           # design values vs limits
    F_q_e  = F_q  * PEAKING_UNC

    results["pin_peaking_factor_Fq"]      = round(F_q_e, 3)
    results["radial_peaking_FdeltaH"]     = round(F_dh_e, 3)
    results["pin_peaking_factor_Fq_raw"]  = round(F_q, 3)
    results["radial_peaking_FdeltaH_raw"] = round(F_dh, 3)
    results["axial_peaking_Fz"]           = round(F_z, 3)

    def _pf(v, lim): return "PASS" if v <= lim else "FAIL"
    print(f"   F_ΔH (radial, per-pin) = {F_dh:.3f} raw → {F_dh_e:.3f} (+{(PEAKING_UNC-1)*100:.0f}% unc)"
          f"  | limit {F_DH_LIMIT} [{_pf(F_dh_e, F_DH_LIMIT)}]  design {F_DH_DESIGN} [{_pf(F_dh_e, F_DH_DESIGN)}]")
    print(f"   F_q  (3-D, per-pin)    = {F_q:.3f} raw → {F_q_e:.3f} (+unc)"
          f"  | limit {F_Q_LIMIT} [{_pf(F_q_e, F_Q_LIMIT)}]  design {F_Q_DESIGN} [{_pf(F_q_e, F_Q_DESIGN)}]")
    print(f"   F_z  (axial)           = {F_z:.3f}")
    print(f"   fuel pins counted = {int(good.sum())} (expect {n_fa}×264 = {n_fa*264})")

    # —— assembly map derived from the SAME per-pin powers ——
    fa_pow = np.zeros(n_fa)
    np.add.at(fa_pow, fa_id[good], pin_col_g)
    fa_norm_v = fa_pow / fa_pow.mean()
    F_assembly = float(fa_norm_v.max())
    results["assembly_peaking_F_radial"] = round(F_assembly, 3)
    print(f"   Assembly peaking F_radial(FA) = {F_assembly:.3f}")

    # —— plots ——
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fine_xy = _reshape_mesh_xyz(flatxy, 200, 200, 1)[:, :, 0]
    fmask = fine_xy > 0.0
    fine_disp = np.where(fmask, fine_xy / fine_xy[fmask].mean(), np.nan)
    im0 = axes[0].imshow(fine_disp.T, origin="lower", cmap="hot_r",
                         extent=[-outer_half, outer_half, -outer_half, outer_half])
    plt.colorbar(im0, ax=axes[0], label="Relative fission rate")
    axes[0].set_title(f"Radial power (z≈0, BOC)\nF_ΔH={F_dh:.2f} raw, F_q={F_q:.2f} raw")
    axes[0].set_xlabel("x (cm)"); axes[0].set_ylabel("y (cm)")

    amap = np.full((N_CORE, N_CORE), np.nan)
    half = (N_CORE - 1) / 2.0
    for fid, (i, j) in fa_ij.items():
        amap[j, i] = fa_norm_v[fid]
    im1 = axes[1].imshow(amap, origin="lower", cmap="hot_r",
                         extent=[-S/2, S/2, -S/2, S/2])
    for fid, (i, j) in fa_ij.items():
        axes[1].text((i-half)*FA_PITCH, (j-half)*FA_PITCH, f"{fa_norm_v[fid]:.2f}",
                     ha="center", va="center", fontsize=8, color="white", weight="bold")
    plt.colorbar(im1, ax=axes[1], label="Relative FA power")
    axes[1].set_title(f"Per-assembly power (BOC)\nF_radial(FA)={F_assembly:.2f}")
    axes[1].set_xlabel("x (cm)"); axes[1].set_ylabel("y (cm)")

    z_c = np.linspace(-H/2 + H/(2*NZ), H/2 - H/(2*NZ), NZ)
    axes[2].plot(z_c, fz_norm, "r-", lw=2)
    axes[2].axhline(1.0, color="gray", ls="--")
    axes[2].set_xlabel("z (cm)"); axes[2].set_ylabel("Relative axial fission rate")
    axes[2].set_title(f"Axial power (BOC)\nF_z={F_z:.2f}")
    axes[2].grid(alpha=0.3)
    fig.tight_layout()
    out = PLOTS / "power_distribution_3d_boc.png"
    fig.savefig(out, dpi=200, bbox_inches="tight"); print(f"   saved: {out}")
    plt.show()
    return F_q_e

calc_flux_peaking()
