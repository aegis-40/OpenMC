"""Re-run the MSLB cooldown cases on the FINAL N5C core basis.

Background
----------
The shipped N12 / N12B MSLB results were computed on the superseded rod basis:
12 CRAs, natural-boron B4C (bank ~13,400 pcm, k_ARI hot = 1.0026).  The design
we present is N5C: 16 CRAs with 90 % enriched B-10 (bank 21,509 pcm,
k_ARI hot = 0.9273) -- roughly 7,500 pcm more shutdown depth.

This script repeats both cases on the N5C basis so the MSLB numbers correspond
to the core actually being presented:

  N12C  MSLB cooldown, rods alone   (16 CRA @ 90 % B-10, most-reactive rod stuck OUT)
  N12D  MSLB cooldown + EBIS 3000 ppm credited, same configuration
  N12E  EBIS boron search at the cold stuck-rod endpoint (how much boron is
        actually still required at 16 CRA) -- the quantity of real interest.

It imports the shipped safety-neutronics module for the geometry/material model
(SAFETY_RUN=none suppresses that module's own driver) so the physics model is
identical to the one that produced N5C.

Usage
-----
  export OPENMC_CROSS_SECTIONS=.../endfb-viii.0-hdf5/cross_sections.xml
  export SAFETY_STAT=medium          # matches the original N12/N12B statistics
  python -u run_mslb_n5c.py
"""
import os, sys, json, time
from pathlib import Path

os.environ["SAFETY_RUN"] = "none"          # suppress the shipped module's driver
WORK = Path(os.environ.get("MSLB_OUT", "/home/samira/aegis_run/mslb_n5c")).resolve()
WORK.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("SAFETY_OUT", str(WORK))

SAF = Path(__file__).resolve().parents[2] / (
    "docs/competition/digital-appendix/4_safety_neutronics/code/aegis40_safety_neutronics.py")

import importlib.util
spec = importlib.util.spec_from_file_location("safmod", str(SAF))
saf = importlib.util.module_from_spec(spec)
sys.modules["safmod"] = saf
spec.loader.exec_module(saf)

THREADS = int(os.environ.get("OPENMC_THREADS", "8"))
saf.THREADS = THREADS
STAT = saf.STAT_SAFETY
print(f"[mslb-n5c] work={WORK}  stat={STAT}  threads={THREADS}", flush=True)

# ---- the N5C control-rod set: base 12 + 4 central-cross extras, 90 % B-10 ----
N = saf.N_CORE
base = [(i, j) for j in range(N) for i in range(N) if saf.CR_MAP[N - 1 - j, i] == 1]
extra = [(3, 5), (1, 3), (5, 3), (3, 1)]          # same as run_N5c_extra_cra
CRA16 = base + [p for p in extra if p not in base]
cc = (N - 1) // 2
STUCK = min(CRA16, key=lambda p: abs(p[0] - cc) + abs(p[1] - cc))   # most-reactive
INSERTED = [p for p in CRA16 if p != STUCK]
print(f"[mslb-n5c] {len(CRA16)} CRAs total; rod {STUCK} stuck OUT; {len(INSERTED)} inserted",
      flush=True)

RES = WORK / "mslb_n5c_results.json"
results = json.load(open(RES)) if RES.exists() else {}
def save():
    RES.write_text(json.dumps(results, default=str, indent=2))

def krun(T, ppm, tag):
    """One eigenvalue point at moderator temperature T with `ppm` soluble boron."""
    saf.BORON_PPM = float(ppm)
    saf.B10_ENRICH = 0.90                      # enriched-B10 SOLID rods (SBF intact)
    rho = saf._rho_at(T)
    m, _, _ = saf.build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=INSERTED, stats=STAT)
    d = saf._run_dir(tag)
    t0 = time.time()
    saf._run_model(m, d, tag=tag)
    k, s = saf._keff(d)
    saf.BORON_PPM = 0.0; saf.B10_ENRICH = 0.0
    print(f"   {tag}: T={T}K ppm={ppm} -> k={k:.5f} +/- {s*1e5:.0f} pcm  [{time.time()-t0:.0f}s]",
          flush=True)
    return k, s

# ------------------------- N12C : rods alone, N5C basis ---------------------
if "N12C_MSLB_rods_alone_N5C" not in results:
    print("\n[N12C] MSLB cooldown, rods alone, N5C basis (16 CRA @ 90% B-10)", flush=True)
    rows = []
    for T in [556, 523, 473, 423, 373, 323, 294]:
        k, s = krun(T, 0.0, f"N12C_mslb_T{T}")
        rows.append(dict(T_K=T, rho=saf._rho_at(T), keff=k, sigma_pcm=s * 1e5,
                         k_adj=round(k + 2 * s + 0.005, 5)))
    kmax = max(r["keff"] for r in rows)
    results["N12C_MSLB_rods_alone_N5C"] = dict(
        case="N12C_MSLB_cooldown_N5C_basis",
        config=f"{len(INSERTED)}/{len(CRA16)} CRAs inserted (16 CRA, 90% B-10); rod {STUCK} stuck OUT",
        basis="N5C (final): bank 21,509 pcm, k_ARI hot 0.9273 - supersedes N12 (12 CRA, natural B4C)",
        sweep=rows, keff_max_on_cooldown=kmax, return_to_power=bool(kmax >= 1.0),
        criterion="MSLB no return-to-power: k<1 with most-reactive rod stuck out",
        refs=["NUREG-0800 SRP 15.1.5", "IAEA SSG-2", "ANS-51.1"])
    save()

# --------------------- N12D : + EBIS 3000 ppm, N5C basis --------------------
if "N12D_MSLB_EBIS_N5C" not in results:
    print("\n[N12D] MSLB cooldown + EBIS 3000 ppm, N5C basis", flush=True)
    rows = []
    for T in [556, 423, 294]:
        k, s = krun(T, 3000.0, f"N12D_mslb_ebis_T{T}")
        rows.append(dict(T_K=T, boron_ppm=3000, keff=k, sigma_pcm=s * 1e5,
                         k_adj=round(k + 2 * s + 0.005, 5)))
    kadj_cold = [r["k_adj"] for r in rows if r["T_K"] == 294][0]
    results["N12D_MSLB_EBIS_N5C"] = dict(
        case="N12D_MSLB_EBIS_credited_N5C_basis",
        config=f"{len(INSERTED)}/{len(CRA16)} CRAs in (16 CRA, 90% B-10), rod {STUCK} stuck OUT, EBIS 3000 ppm",
        ebis_ppm=3000, sweep=rows, k_adj_cold=kadj_cold,
        subcritical_with_margin=bool(kadj_cold <= 0.95),
        criterion="credited MSLB termination (RT+MSI+EBIS): cold/stuck-rod k_adj <= 0.95",
        refs=["NUREG-0800 SRP 15.1.5", "IAEA SSR-2/1 Req.46", "RG 1.77"])
    save()

# ---------- N12E : how much EBIS boron is still needed at 16 CRA? -----------
if "N12E_EBIS_requirement_N5C" not in results:
    print("\n[N12E] EBIS boron requirement at the cold (294 K) stuck-rod endpoint", flush=True)
    rows = []
    for ppm in [0, 500, 1000, 1500, 2000]:
        if ppm == 0:
            prev = results.get("N12C_MSLB_rods_alone_N5C", {})
            hit = [r for r in prev.get("sweep", []) if r["T_K"] == 294]
            if hit:
                rows.append(dict(boron_ppm=0, keff=hit[0]["keff"],
                                 sigma_pcm=hit[0]["sigma_pcm"], k_adj=hit[0]["k_adj"]))
                print(f"   (reusing N12C cold point: k={hit[0]['keff']:.5f})", flush=True)
                continue
        k, s = krun(294, float(ppm), f"N12E_ebis_{ppm}ppm")
        rows.append(dict(boron_ppm=ppm, keff=k, sigma_pcm=s * 1e5,
                         k_adj=round(k + 2 * s + 0.005, 5)))
    # linear interpolation on k_adj for the 0.95 acceptance line
    need = None
    for a, b in zip(rows, rows[1:]):
        if a["k_adj"] > 0.95 >= b["k_adj"]:
            f = (a["k_adj"] - 0.95) / (a["k_adj"] - b["k_adj"])
            need = a["boron_ppm"] + f * (b["boron_ppm"] - a["boron_ppm"])
            break
    results["N12E_EBIS_requirement_N5C"] = dict(
        case="N12E_EBIS_boron_requirement_N5C_basis",
        state="cold 294 K, MSLB endpoint, 15/16 CRAs in, most-reactive rod stuck OUT",
        sweep=rows, ppm_for_kadj_0p95=(round(need, 0) if need else None),
        note=("EBIS boron still required for the cold stuck-rod state at the final 16-CRA "
              "basis; this is the residual soluble-boron dependency of the SBF design"),
        refs=["IAEA SSR-2/1 Req.46", "NUREG-0800 SRP 15.1.5"])
    save()

# --------------------------------- summary ----------------------------------
print("\n" + "=" * 72, flush=True)
a = results["N12C_MSLB_rods_alone_N5C"]
b = results["N12D_MSLB_EBIS_N5C"]
c = results["N12E_EBIS_requirement_N5C"]
print(f"N12C rods alone   k_max on cooldown = {a['keff_max_on_cooldown']:.5f}"
      f"   -> {'RETURN TO POWER' if a['return_to_power'] else 'stays subcritical'}")
print(f"N12D + EBIS 3000  k_adj cold        = {b['k_adj_cold']:.4f}"
      f"   -> {'PASS' if b['subcritical_with_margin'] else 'FAIL'} (<=0.95)")
print(f"N12E EBIS needed for k_adj<=0.95    = {c['ppm_for_kadj_0p95']} ppm")
print("=" * 72, flush=True)
print("MSLB_N5C_COMPLETE ->", RES, flush=True)
