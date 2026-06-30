"""Generate a self-contained OpenMC script for the three MISSING safety-neutronics
simulations (FER SIMULATION_ANALYSIS_PLAN §8.5-8.6):
  N10 - EBIS soluble-boron sizing (standalone cold-subcritical, no rods)
  N11 - SFP storage-rack criticality (k_inf, unborated, Boral panel)
  N12 - MSLB cooldown reactivity (k vs moderator-T, most-reactive rod stuck out)
Geometry/materials are reused verbatim from the LOCKED design notebook
(ref_neutronics.ipynb) by including its def cells {0..6,8}; cell 7 (shielding
build_core override) is skipped. ext4 XS + threads come from env (acceleration);
no weight windows - these are eigenvalue/criticality runs, WW is fixed-source-only."""
import json, re, os

NB  = "/home/samira/ref_neutronics.ipynb"
OUT = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/safety_85_86/aegis40_safety_neutronics.py"

nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
INCLUDE = {0, 1, 2, 3, 4, 5, 6, 8}
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|write_\w+|build_shielded_model|"
                  r"extract_absorber)\s*\(|\.(?:run|integrate)\s*\(")

def neutralize(src):
    out = []
    for l in src.splitlines():
        if l.lstrip().startswith("%") or "get_ipython()" in l:
            continue
        indented = l[:1] in (" ", "\t")
        isdef = l.lstrip().startswith(("def ", "class ", "import ", "from ", "@"))
        if (not indented) and (not isdef) and CALL.search(l):
            out.append("# [neutralized] " + l)
        else:
            out.append(l)
    return "\n".join(out)

parts = ["import matplotlib\nmatplotlib.use('Agg')\nimport os\n"]
for idx, c in enumerate(code):
    if idx not in INCLUDE:
        continue
    parts.append(f"\n# ===== ref cell #{idx} =====\n" + neutralize("".join(c["source"])) + "\n")

SAFETY = r'''
# ============================================================================
# SAFETY NEUTRONICS  (FER §8.5-8.6)  - N10 EBIS / N11 SFP rack / N12 MSLB cooldown
# ============================================================================
import json as _json
import numpy as _np
import matplotlib.pyplot as _plt

# --- redirect all run dirs + plots into this project's results/ folder ---
ROOT = Path(os.environ.get("SAFETY_OUT", os.path.join(os.path.dirname(__file__), "results"))).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
PLOTS = ROOT / "plots"; PLOTS.mkdir(exist_ok=True)

STAT_SAFETY = {"fast": STAT_FAST, "medium": STAT_MEDIUM, "final": STAT_FINAL}[
    os.environ.get("SAFETY_STAT", "medium")]
print(f"[safety] outputs -> {ROOT} | STAT={STAT_SAFETY}")

# water density vs T at 12.8 MPa (IAPWS-IF97), (T_K, rho g/cc); 556 K anchors the design
_RHO_T = [(294, 1.003), (323, 0.994), (373, 0.963), (423, 0.922),
          (473, 0.870), (523, 0.803), (556, 0.748)]
def _rho_at(T):
    return float(_np.interp(T, [t for t, _ in _RHO_T], [r for _, r in _RHO_T]))

# --- borate-able moderator: build_core looks up mat_water at call-time, so a
#     module-level redefinition + a BORON_PPM global injects soluble boron ---
BORON_PPM = 0.0
def mat_water(temp=T_MOD_K, density=RHO_WATER_NOM, name="H2O"):
    m = openmc.Material(name=name, temperature=temp)
    m.set_density("g/cm3", density)
    if BORON_PPM > 0:
        wB = BORON_PPM * 1e-6; wW = 1.0 - wB
        m.add_element("H", 0.111894 * wW, percent_type="wo")
        m.add_element("O", 0.888106 * wW, percent_type="wo")
        m.add_element("B", wB, percent_type="wo")     # natural B -> B10/B11
    else:
        m.add_element("H", 2.0); m.add_element("O", 1.0)
    m.add_s_alpha_beta("c_H_in_H2O")
    return m

# --- enriched-B10 control-rod absorber (SOLID B4C - NOT soluble; SBF preserved) ---
B10_ENRICH = 0.0   # 0 = natural boron (19.9% B-10); else B-10 atom fraction (e.g. 0.90)
def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    if B10_ENRICH > 0:
        m.add_nuclide("B10", 4.0 * B10_ENRICH)
        m.add_nuclide("B11", 4.0 * (1.0 - B10_ENRICH))
        m.add_element("C", 1.0)
    else:
        m.add_element("B", 4.0); m.add_element("C", 1.0)
    return m

def _interp_cross(xs, ys, target):
    """x where y crosses target (ys monotone over the bracket)."""
    for a in range(len(xs) - 1):
        y0, y1 = ys[a], ys[a + 1]
        if (y0 - target) * (y1 - target) <= 0 and y0 != y1:
            return float(xs[a] + (xs[a + 1] - xs[a]) * (target - y0) / (y1 - y0))
    return None


# --- RESUME: skip the transport if a statepoint already exists on disk ---
_orig_run_model = _run_model
def _run_model(model, run_dir, threads=THREADS, clean=True, tag=""):
    import glob as _g
    if _g.glob(os.path.join(str(run_dir), "statepoint.*.h5")):
        print("   [resume] %s: cached statepoint" % os.path.basename(str(run_dir)))
        return 0.0
    return _orig_run_model(model, run_dir, threads=threads, clean=clean, tag=tag)


# ----------------------------- N10 : EBIS boron -----------------------------
def run_N10_ebis(stat):
    global BORON_PPM
    print("\n[N10] EBIS soluble-boron sizing - cold 294 K / BOC / ARO / standalone (no rods)")
    T = 294.0; rho = _rho_at(T); rows = []
    for ppm in [0, 1000, 1800, 2400, 3000, 3600]:
        BORON_PPM = float(ppm)
        model, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=T,
                                 control_rod_state="aro", stats=stat)
        d = _run_dir(f"N10_ebis_{ppm}ppm"); _run_model(model, d, tag=f"ebis{ppm}")
        k, s = _keff(d); rows.append(dict(boron_ppm=ppm, keff=k, sigma_pcm=s * 1e5))
        print(f"   {ppm:5d} ppm -> k = {k:.5f} +/- {s*1e5:.0f} pcm")
    BORON_PPM = 0.0
    ppms = [r["boron_ppm"] for r in rows]; ks = [r["keff"] for r in rows]
    ppm100 = _interp_cross(ppms, ks, 1.00); ppm99 = _interp_cross(ppms, ks, 0.99)
    _plt.figure(figsize=(6, 4)); _plt.plot(ppms, ks, "o-", color="#1a6faf")
    _plt.axhline(1.0, color="k", ls="--", lw=1, label="critical")
    _plt.axhline(0.99, color="r", ls=":", lw=1, label="1% margin")
    _plt.xlabel("Soluble boron (ppm)"); _plt.ylabel("k_eff (cold, ARO)")
    _plt.title("N10 EBIS boron sizing"); _plt.legend(); _plt.grid(alpha=.3)
    _plt.savefig(PLOTS / "N10_ebis_boron.png", dpi=160, bbox_inches="tight"); _plt.close()
    print(f"   -> k=1.00 at ~{ppm100:.0f} ppm ; k=0.99 (1% SDM) at ~{ppm99:.0f} ppm")
    return dict(case="N10_EBIS",
                state="cold 294 K / BOC fresh / ARO (rods out) / soluble-boron only",
                sweep=rows, boron_for_keff_1p00_ppm=ppm100, boron_for_keff_0p99_ppm=ppm99,
                criterion="independent_shutdown_systems (EBIS alone cold-subcritical, k<=0.99)",
                refs=["IAEA SSR-2/1 Req.46 (two diverse shutdown systems)",
                      "10 CFR 50.68 / NUREG-0800 4.3"])


# --------------------------- N11 : SFP rack k_inf ---------------------------
def run_N11_sfp(stat):
    global BORON_PPM
    print("\n[N11] SFP storage-rack criticality - bounding fresh 4.95% FA (no BA credit),"
          " infinite array; per 10 CFR 50.68(b): unborated k<1.0 + borated k<=0.95")
    T = 294.0; rho = _rho_at(T)
    enr = ENRICH_INNER                                   # 4.95 = most reactive
    clad = mat_zircaloy(temp=T); gap = mat_helium(temp=T); b4c = mat_b4c(temp=600.0)
    # poison rack: flux-trap-style Boral (B4C-in-Al) sheet, tight pitch
    al = openmc.Material(name="Al6061", temperature=T); al.set_density("g/cm3", 2.70)
    al.add_element("Al", 1.0)
    boral = openmc.Material.mix_materials([mat_b4c(temp=T), al], [0.50, 0.50],
                                          percent_type="wo", name="Boral_B4C_Al")   # 50 wt% B4C
    boral.temperature = T
    ss = openmc.Material(name="SS304_rack", temperature=T); ss.set_density("g/cm3", 7.94)
    for el, f in (("Fe", .70), ("Cr", .19), ("Ni", .095), ("Mn", .015)):
        ss.add_element(el, f, percent_type="wo")
    RACK_PITCH = FA_PITCH + 1.4; WALL_T = 0.45        # tighter pitch, thicker poison

    def _build_model(rmat, ppm):
        global BORON_PPM; BORON_PPM = float(ppm)
        water = mat_water(temp=T, density=rho, name=f"SFP_water_{int(ppm)}ppm")
        plain = {f"UO2_{enr:.1f}": mat_uo2(enr, temp=T, name=f"UO2_{enr:.1f}")}
        gd_mat = _mixed_fuel(ENRICH_MID, gd_wt=GD_WT_PCT, er_wt=0.0, temp=T, name="SFP_Gd")
        gd_cut = mat_uo2(ENRICH_MID, temp=T, name="SFP_Gdcut")
        er_mat = _mixed_fuel(ENRICH_MID, gd_wt=0.0, er_wt=ER_WT_PCT, temp=T, name="SFP_Er")
        fa = _build_fa_universe(T, T, water, clad, gap, b4c, plain, gd_mat, gd_cut, er_mat,
                                insert_cr=False, name=f"SFP_FA_{int(ppm)}",
                                gd_positions=set(), er_positions=set(), fa_enrich=enr)
        hf = FA_PITCH/2.0; hw = RACK_PITCH/2.0; hi = hw - WALL_T; H = ACTIVE_HEIGHT/2.0
        bc = "reflective"
        xlo = openmc.XPlane(-hw, boundary_type=bc); xhi = openmc.XPlane(hw, boundary_type=bc)
        ylo = openmc.YPlane(-hw, boundary_type=bc); yhi = openmc.YPlane(hw, boundary_type=bc)
        zlo = openmc.ZPlane(-H, boundary_type=bc);  zhi = openmc.ZPlane(H, boundary_type=bc)
        fx0 = openmc.XPlane(-hf); fx1 = openmc.XPlane(hf)
        fy0 = openmc.YPlane(-hf); fy1 = openmc.YPlane(hf)
        ix0 = openmc.XPlane(-hi); ix1 = openmc.XPlane(hi)
        iy0 = openmc.YPlane(-hi); iy1 = openmc.YPlane(hi)
        zr = +zlo & -zhi; fa_box = +fx0 & -fx1 & +fy0 & -fy1; in_box = +ix0 & -ix1 & +iy0 & -iy1
        cell_fa = openmc.Cell(name="sfp_fa", fill=fa, region=fa_box & zr)
        cell_w  = openmc.Cell(name="sfp_water", fill=water, region=(in_box & zr) & ~fa_box)
        cell_wall = openmc.Cell(name="sfp_wall", fill=rmat,
                                region=(+xlo & -xhi & +ylo & -yhi & zr) & ~in_box)
        geom = openmc.Geometry(openmc.Universe(cells=[cell_fa, cell_w, cell_wall]))
        s = openmc.Settings(); s.batches = stat["batches"]; s.inactive = stat["inactive"]
        s.particles = stat["particles"]; s.temperature = {"method": "nearest", "tolerance": 400.0}
        s.source = openmc.IndependentSource(space=openmc.stats.Box([-hf]*3, [hf]*3),
                                            constraints={"fissionable": True})
        allm = [water, clad, gap, b4c, gd_mat, gd_cut, er_mat, rmat] + list(plain.values())
        return openmc.Model(geometry=geom, settings=s,
                            materials=openmc.Materials([m for m in allm if m]))

    cases = [("SS304_unborated", ss, 0),
             ("Boral_unborated", boral, 0),
             ("Boral_2000ppm_SFP_boron", boral, 2000)]
    rows = []
    for label, rmat, ppm in cases:
        model = _build_model(rmat, ppm)
        d = _run_dir(f"N11_sfp_{label}"); _run_model(model, d, tag=f"sfp_{label}")
        k, sg = _keff(d); rows.append(dict(rack=label, boron_ppm=ppm, k_inf=k, sigma_pcm=sg * 1e5))
        print(f"   {label:26s}: k_inf = {k:.5f} +/- {sg*1e5:.0f} pcm")
    BORON_PPM = 0.0
    return dict(case="N11_SFP_rack",
                fuel="bounding fresh 4.95% UO2 assembly, NO burnable-absorber credit",
                array="infinite (fully reflective) -> k_inf (bounds any finite rack)",
                rack="flux-trap Boral (50 wt% B4C-in-Al, 0.45 cm), pitch FA+1.4 cm",
                rack_pitch_cm=RACK_PITCH, wall_thickness_cm=WALL_T, results=rows,
                criterion="10 CFR 50.68(b): unborated k<1.0 (defence-in-depth) AND borated k<=0.95",
                note=("fresh 4.95% infinite array is the extreme bound; licensed storage of >4 wt%"
                      " fuel credits BURNUP + SFP soluble boron - the borated case is the design demo"),
                refs=["10 CFR 50.68(b)", "NUREG-0800 SRP 9.1.1", "ANSI/ANS-8.1", "IAEA SSG-15"])


# ------------------------- N12 : MSLB cooldown ------------------------------
def run_N12_mslb(stat):
    print("\n[N12] MSLB cooldown reactivity - most-reactive rod stuck OUT, hot -> cold")
    cra = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
           if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = (N_CORE - 1) // 2
    stuck = min(cra, key=lambda p: abs(p[0] - cc) + abs(p[1] - cc))   # most central ~ highest worth
    inserted = [p for p in cra if p != stuck]
    print(f"   {len(inserted)} of {len(cra)} CRAs inserted; rod {stuck} stuck OUT")
    rows = []
    for T in [556, 523, 473, 423, 373, 323, 294]:
        rho = _rho_at(T)
        model, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                                 control_rod_state=inserted, stats=stat)
        d = _run_dir(f"N12_mslb_T{T}"); _run_model(model, d, tag=f"mslb{T}")
        k, s = _keff(d); rows.append(dict(T_K=T, rho=rho, keff=k, sigma_pcm=s * 1e5))
        print(f"   T={T} K  rho={rho:.3f} -> k = {k:.5f} +/- {s*1e5:.0f} pcm")
    kmax = max(r["keff"] for r in rows)
    Ts = [r["T_K"] for r in rows]; ks = [r["keff"] for r in rows]
    _plt.figure(figsize=(6, 4)); _plt.plot(Ts, ks, "o-", color="#c0392b")
    _plt.axhline(1.0, color="k", ls="--", lw=1, label="critical")
    _plt.xlabel("Moderator temperature (K)"); _plt.ylabel("k_eff (rod stuck out)")
    _plt.title("N12 MSLB cooldown"); _plt.gca().invert_xaxis()
    _plt.legend(); _plt.grid(alpha=.3)
    _plt.savefig(PLOTS / "N12_mslb_cooldown.png", dpi=160, bbox_inches="tight"); _plt.close()
    print(f"   -> k_max on cooldown = {kmax:.5f}  "
          f"({'RETURN TO POWER' if kmax >= 1 else 'stays subcritical'})")
    return dict(case="N12_MSLB_cooldown",
                config=f"{len(inserted)}/{len(cra)} CRAs inserted; most-reactive rod {stuck} stuck OUT",
                sweep=rows, keff_max_on_cooldown=kmax, return_to_power=bool(kmax >= 1.0),
                criterion="MSLB no return-to-power: k<1 with most-reactive rod stuck out",
                refs=["NUREG-0800 SRP 15.1.5 (steam-line break)",
                      "IAEA SSG-2 (deterministic safety analysis)", "ANS-51.1 cooldown event"])


# --------------------- N5 : rod worth + shutdown margin ---------------------
def run_N5_sdm(stat):
    print("\n[N5] Control-rod worth + shutdown margin (SIGNED; hot trip & cold SDM)")
    all_cr = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
              if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = N_CORE // 2
    central = min(all_cr, key=lambda p: (p[0] - cc) ** 2 + (p[1] - cc) ** 2)
    stuck = [p for p in all_cr if p != central]   # all rods in except most-reactive
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(f"N5_{tag}"); _run_model(m, d, tag=tag)
        return _keff(d)[0]
    Th, Tc = T_MOD_K, 294.0
    k_aro_h   = _kof("aro",  Th, "aro_hot")
    k_ari_h   = _kof("ari",  Th, "ari_hot")
    k_ari_c   = _kof("ari",  Tc, "ari_cold")
    k_stuck_c = _kof(stuck,  Tc, "stuck_cold")
    bank = abs(_pcm(k_aro_h, k_ari_h))             # total bank worth, pcm
    def _sdm(k): return -(k - 1.0) / k * 100.0     # SIGNED: +ve = subcritical margin
    out = dict(case="N5_rod_worth_SDM",
               k_aro_hot=k_aro_h, k_ari_hot=k_ari_h, total_bank_worth_pcm=bank,
               k_ari_cold=k_ari_c, k_stuck_cold=k_stuck_c,
               sdm_all_rods_cold_pct=_sdm(k_ari_c),
               sdm_stuck_rod_cold_pct=_sdm(k_stuck_c),
               hot_trip_all_rods_subcritical=bool(k_ari_h < 1.0),
               rods_alone_cold_subcritical=bool(k_ari_c < 1.0),
               note=("boron-free high-excess core: control rods give the fast hot trip; "
                     "EBIS soluble boron (N10) provides/holds cold subcriticality - the "
                     "diverse 2nd shutdown system (SSR-2/1 Req.46). SDM reported SIGNED "
                     "(notebook calc uses abs() which masks a supercritical stuck-rod state)."),
               criterion="hot trip subcritical by rods; cold shutdown by rods+EBIS; SDM>=1%",
               refs=["IAEA SSR-2/1 Req.46 (two diverse shutdown systems)",
                     "NUREG-0800 SRP 4.3", "RG 1.77"])
    print(f"   bank worth (hot ARO->ARI) = {bank:.0f} pcm")
    print(f"   k_ARI hot   = {k_ari_h:.5f}   ({'subcritical' if k_ari_h<1 else 'SUPERCRIT'})")
    print(f"   k_ARI cold  = {k_ari_c:.5f}   ({'subcritical' if k_ari_c<1 else 'SUPERCRIT -> EBIS'})")
    print(f"   k_stuck cold= {k_stuck_c:.5f}  SDM(stuck,cold) = {_sdm(k_stuck_c):+.2f}% dk/k")
    return out


# ---------------- N12-B : MSLB cooldown + EBIS credited ---------------------
def run_N12b_mslb_ebis(stat, ebis_ppm=3000):
    global BORON_PPM
    print("\n[N12B] MSLB cooldown + EBIS (%d ppm) credited - stuck rod, hot->cold" % ebis_ppm)
    cra = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
           if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = (N_CORE - 1) // 2
    stuck = min(cra, key=lambda p: abs(p[0] - cc) + abs(p[1] - cc))
    inserted = [p for p in cra if p != stuck]
    rows = []
    for T in [556, 423, 294]:                      # hot, mid, cold (limiting) endpoint
        rho = _rho_at(T); BORON_PPM = float(ebis_ppm)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=inserted, stats=stat)
        d = _run_dir("N12B_mslb_ebis_T%d" % T); _run_model(m, d, tag="mslbE%d" % T)
        k, s = _keff(d); kadj = k + 2 * s + 0.005       # +2sigma + 500 pcm allowance
        rows.append(dict(T_K=T, boron_ppm=ebis_ppm, keff=k, sigma_pcm=s * 1e5, k_adj=round(kadj, 5)))
        print("   T=%dK +%dppm -> k=%.5f  k_adj=%.4f" % (T, ebis_ppm, k, kadj))
    BORON_PPM = 0.0
    kadj_cold = [r["k_adj"] for r in rows if r["T_K"] == 294][0]
    print("   -> cold (294 K) k_adj = %.4f  (%s 0.95)" % (kadj_cold, "<=" if kadj_cold <= 0.95 else ">"))
    return dict(case="N12B_MSLB_EBIS_credited",
                config="%d/%d CRAs in, rod %s stuck OUT, EBIS %d ppm" % (len(inserted), len(cra), stuck, ebis_ppm),
                ebis_ppm=ebis_ppm, sweep=rows, k_adj_cold=kadj_cold,
                subcritical_with_margin=bool(kadj_cold <= 0.95),
                criterion="credited MSLB termination (RT+MSI+EBIS): cold/stuck-rod k_adj <= 0.95",
                note=("credited safe state = reactor trip + main-steam isolation + EBIS; the rods-alone "
                      "N12 is the diagnostic limiting case that establishes the EBIS requirement"),
                refs=["NUREG-0800 SRP 15.1.5", "IAEA SSR-2/1 Req.46", "RG 1.77"])


# --------- N5-B : rod worth + SDM with ENRICHED B-10 solid rods -------------
def run_N5b_enriched_rods(stat, b10=0.90):
    global B10_ENRICH
    print("\n[N5B] Rod worth + SDM with ENRICHED B-10 (%.0f%%) SOLID B4C rods (SBF intact)" % (b10 * 100))
    all_cr = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
              if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = N_CORE // 2
    central = min(all_cr, key=lambda p: (p[0] - cc) ** 2 + (p[1] - cc) ** 2)
    stuck = [p for p in all_cr if p != central]
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(tag); _run_model(m, d, tag=tag); return _keff(d)
    B10_ENRICH = 0.0
    k_aro_h, _ = _kof("aro", T_MOD_K, "N5b_aro_hot")      # rods out -> enrichment irrelevant
    B10_ENRICH = float(b10)
    k_ari_h, s_ari_h = _kof("ari", T_MOD_K, "N5b_ari_hot")
    k_ari_c, _ = _kof("ari", 294.0, "N5b_ari_cold")
    k_stuck_c, s_st = _kof(stuck, 294.0, "N5b_stuck_cold")
    B10_ENRICH = 0.0
    bank = abs(_pcm(k_aro_h, k_ari_h))
    def _sdm(k): return -(k - 1.0) / k * 100.0
    kadj_ari_h = k_ari_h + 2 * s_ari_h + 0.005
    print("   bank worth (enriched) = %.0f pcm  (was 13287 natural)" % bank)
    print("   k_ARI hot = %.5f  k_adj = %.4f  (%s)" %
          (k_ari_h, kadj_ari_h, "subcritical TRIP OK" if kadj_ari_h <= 0.99 else "still supercrit"))
    print("   k_ARI cold = %.5f | k_stuck cold = %.5f  SDM(stuck) = %+.2f%%" %
          (k_ari_c, k_stuck_c, _sdm(k_stuck_c)))
    return dict(case="N5B_enriched_B10_rods", b10_enrichment=b10,
                k_aro_hot=k_aro_h, k_ari_hot=k_ari_h, total_bank_worth_pcm=bank,
                k_adj_ari_hot=round(kadj_ari_h, 5),
                k_ari_cold=k_ari_c, k_stuck_cold=k_stuck_c,
                sdm_all_rods_cold_pct=_sdm(k_ari_c), sdm_stuck_rod_cold_pct=_sdm(k_stuck_c),
                hot_trip_subcritical=bool(kadj_ari_h <= 0.99),
                note=("enriched-B10 SOLID B4C control rods - does NOT add soluble boron, SBF claim intact; "
                      "EBIS remains the diverse cold/standalone shutdown backup"),
                criterion="rod-based hot trip k_adj<=0.99 with SDM; cold shutdown by rods + EBIS",
                refs=["IAEA SSR-2/1 Req.46", "NUREG-0800 SRP 4.3"])


# ------- N5-C : enriched rods + extra CRA locations (margin booster) --------
def run_N5c_extra_cra(stat, b10=0.90):
    global B10_ENRICH
    base = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
            if CR_MAP[N_CORE - 1 - j, i] == 1]
    extra = [(3, 5), (1, 3), (5, 3), (3, 1)]      # 4 central-cross fuel FAs (NOT instrument (3,3))
    ext = base + [p for p in extra if p not in base]
    cc = N_CORE // 2
    print("\n[N5C] enriched B-10 rods + %d extra CRAs (%d total) - hot-trip margin booster"
          % (len(extra), len(ext)))
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(tag); _run_model(m, d, tag=tag); return _keff(d)
    B10_ENRICH = 0.0
    k_aro, _ = _kof("aro", T_MOD_K, "N5c_aro_hot")
    B10_ENRICH = float(b10)
    k_ari, s_ari = _kof(ext, T_MOD_K, "N5c_ari_hot")
    central = min(ext, key=lambda q: (q[0] - cc) ** 2 + (q[1] - cc) ** 2)
    stuck = [p for p in ext if p != central]
    k_stuck_c, _ = _kof(stuck, 294.0, "N5c_stuck_cold")
    B10_ENRICH = 0.0
    bank = abs(_pcm(k_aro, k_ari)); kadj = k_ari + 2 * s_ari + 0.005
    print("   %d CRAs enriched: bank = %.0f pcm | k_ARI hot = %.5f  k_adj = %.4f" %
          (len(ext), bank, k_ari, kadj))
    return dict(case="N5C_enriched_plus_extraCRA", n_cra=len(ext), n_extra=len(extra),
                b10_enrichment=b10, extra_cra=extra, k_aro_hot=k_aro, k_ari_hot=k_ari,
                total_bank_worth_pcm=bank, k_adj_ari_hot=round(kadj, 5), k_stuck_cold=k_stuck_c,
                hot_sdm_pct=round(-(k_ari - 1) / k_ari * 100, 2),
                note=("4 extra CRAs in central-cross fuel FAs (existing guide tubes; +4 CRDMs vs 12); "
                      "enriched-B10 SOLID rods, SBF intact; EBIS still the diverse cold backup"),
                criterion="hot trip k_adj<=0.98 (jury 'Good'); cold by rods + EBIS",
                refs=["IAEA SSR-2/1 Req.46", "NUREG-0800 SRP 4.3"])


# --------------------------------- driver -----------------------------------
_which = os.environ.get("SAFETY_RUN", "all")
_resfile = ROOT / "safety_neutronics_results.json"
_results = _json.load(open(_resfile)) if _resfile.exists() else {}   # merge / resume
def _save():
    open(_resfile, "w").write(_json.dumps(_results, default=str, indent=2))
_plan = [("N5", "N5_SDM", run_N5_sdm), ("N10", "N10_EBIS", run_N10_ebis),
         ("N11", "N11_SFP", run_N11_sfp), ("N12", "N12_MSLB", run_N12_mslb),
         ("N12B", "N12B_MSLB_EBIS", run_N12b_mslb_ebis),
         ("N5B", "N5B_enriched_rods", run_N5b_enriched_rods),
         ("N5C", "N5C_extra_cra", run_N5c_extra_cra)]
for _sel, _key, _fn in _plan:
    if _key in _results:
        print("[safety] %s already complete - skipping" % _key); continue
    if _which in ("all", _sel):
        _results[_key] = _fn(STAT_SAFETY); _save()       # checkpoint after each sim
_save()
_need = [k for _, k, _ in _plan]
if all(k in _results for k in _need):
    print("\nSAFETY_ALL_COMPLETE ->", _resfile)
else:
    print("\n[safety] partial:", [k for k in _need if k in _results], "->", _resfile)
'''
parts.append(SAFETY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("".join(parts))
print(f"wrote {OUT} | included cells {sorted(INCLUDE)}")
