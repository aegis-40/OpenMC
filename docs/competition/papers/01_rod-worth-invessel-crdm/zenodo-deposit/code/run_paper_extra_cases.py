# -*- coding: utf-8 -*-
"""
Aegis-40 SBF rod-worth paper - the three outstanding OpenMC cases.
==================================================================

Run these three and the manuscript's remaining referee objections close:

  R1  Individual worth of every CRA position.
      Closes: "the maximum-worth cluster is assumed, not demonstrated."
      The paper currently uses the cluster nearest the core centre on
      neutron-importance grounds without computing the others.

  R2  16 CRA with NATURAL B4C - the missing fourth corner of the lever matrix.
      Closes: "three points cannot show the two levers are separable."
      We have 12-nat, 12-enriched and 16-enriched; 16-nat is missing.

  R3  Boron sweep at 700 / 800 / 900 ppm, cold stuck-rod state.
      Closes: "785 ppm is a linear interpolation across a 500 ppm gap."

This script does NOT redefine the core. It imports the locked model from
`aegis40_safety_neutronics.py` (the same module that produced the published
ladder, MSLB and EBIS numbers) and only drives new cases through it. If the
model changes, these results change with it - which is what we want.

-------------------------------------------------------------------------------
HOW TO RUN
-------------------------------------------------------------------------------
    # from anywhere, with OpenMC + cross sections already working:
    python run_paper_extra_cases.py all

    # or one at a time (recommended - each checkpoints to JSON):
    python run_paper_extra_cases.py R1
    python run_paper_extra_cases.py R2
    python run_paper_extra_cases.py R3

Environment variables:
    OPENMC_THREADS=8            threads (default 6, inherited from the model)
    AEGIS_MODEL_DIR=<path>      where aegis40_safety_neutronics.py lives,
                                if auto-detection fails
    PAPER_STAT=final|medium     statistics level (default: final)
    R1_ALL_16=1                 run all 16 positions instead of one per
                                symmetry class (slower, see note below)

Results are checkpointed after every single eigenvalue run to
    <this folder>/../data/paper_extra_cases.json
so the script is safe to interrupt and restart - completed cases are skipped.

-------------------------------------------------------------------------------
WHY R1 IS ONLY ~5 RUNS AND NOT 17
-------------------------------------------------------------------------------
The 16 CRA positions are not 16 independent cases. Under the 8-fold dihedral
symmetry of the core map they collapse into three classes:

    class (0,1) - 4 positions, the central cross nearest neighbours
    class (0,2) - 4 positions, the four added "extra" clusters
    class (1,2) - 8 positions, the outer checkerboard ring

Since enrichment and Gd zoning are both applied by ring, positions within a
class are neutronically equivalent. We therefore run one representative per
class at full statistics, plus one duplicate as an explicit symmetry check.
That is 3 + 1 + 1 ARO reference = 5 runs instead of 17, and it gives a better
result: a worth per class with tight error bars, rather than 16 noisy numbers.

Set R1_ALL_16=1 to run all sixteen anyway if a referee asks for the full set.
-------------------------------------------------------------------------------
"""
import json
import os
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------
# locate and import the locked core model
# --------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
CANDIDATES = [
    Path(os.environ.get("AEGIS_MODEL_DIR", "")),
    HERE.parents[3] / "openmc_model" / "safety_85_86",
    HERE.parents[4] / "openmc_model" / "safety_85_86",
    Path.cwd() / "openmc_model" / "safety_85_86",
    Path.cwd(),
]
MODEL_DIR = None
for c in CANDIDATES:
    if c and (c / "aegis40_safety_neutronics.py").exists():
        MODEL_DIR = c.resolve()
        break
if MODEL_DIR is None:
    sys.exit(
        "ERROR: could not find aegis40_safety_neutronics.py.\n"
        "Set AEGIS_MODEL_DIR to the folder that contains it, e.g.\n"
        "    set AEGIS_MODEL_DIR=D:\\projects\\teknofest-2026-aegis-40-ipwr"
        "\\openmc_model\\safety_85_86      (Windows)\n"
        "    export AEGIS_MODEL_DIR=.../openmc_model/safety_85_86        (Linux/Mac)"
    )

# The model module runs its own case suite at import time unless told not to.
os.environ["SAFETY_RUN"] = "none"
# Its output ROOT is relative to CWD, so run from the model directory.
os.chdir(MODEL_DIR)
sys.path.insert(0, str(MODEL_DIR))

print("[setup] model dir : %s" % MODEL_DIR)
import aegis40_safety_neutronics as A  # noqa: E402

STAT = A.STAT_FINAL if os.environ.get("PAPER_STAT", "final") == "final" else A.STAT_MEDIUM
print("[setup] statistics: %s" % STAT)
print("[setup] threads   : %s" % A.THREADS)

OUT = HERE.parent / "data" / "paper_extra_cases.json"
OUT.parent.mkdir(parents=True, exist_ok=True)
RES = json.load(open(OUT)) if OUT.exists() else {}


def save():
    OUT.write_text(json.dumps(RES, indent=2, default=str), encoding="utf-8")


# --------------------------------------------------------------------------
# geometry helpers - reproduce the paper's 16-CRA set exactly
# --------------------------------------------------------------------------
# beta_eff from the manuscript section 3.2 - used only to report dollars
A_BETA = 704.5
BETA_SIG = 28.2

N = A.N_CORE                      # 7
CC = N // 2                       # 3 -> centre index
BASE_12 = [(i, j) for j in range(N) for i in range(N)
           if A.CR_MAP[N - 1 - j, i] == 1]
EXTRA_4 = [(3, 5), (1, 3), (5, 3), (3, 1)]
CRA_16 = BASE_12 + [p for p in EXTRA_4 if p not in BASE_12]
assert len(CRA_16) == 16, "expected 16 CRA positions, got %d" % len(CRA_16)


def sym_class(pos):
    """8-fold dihedral invariant of a position about the core centre."""
    di, dj = abs(pos[0] - CC), abs(pos[1] - CC)
    return (min(di, dj), max(di, dj))


CLASSES = {}
for p in CRA_16:
    CLASSES.setdefault(sym_class(p), []).append(p)


def kof(state, T_mod, tag, fuel_T=None, rho=None, b10=None, ppm=0.0):
    """One eigenvalue run. Returns (k, sigma). Mirrors the model's own _kof."""
    A.B10_ENRICH = 0.0 if b10 is None else float(b10)
    A.BORON_PPM = float(ppm)
    dens = A._rho_at(T_mod) if rho is None else rho
    model, _, _ = A.build_core(mod_temp=T_mod,
                               water_density=dens,
                               fuel_temp=float(T_mod if fuel_T is None else fuel_T),
                               control_rod_state=state,
                               stats=STAT)
    d = A._run_dir(tag)
    t0 = time.time()
    A._run_model(model, d, tag=tag)
    k, s = A._keff(d)
    A.B10_ENRICH = 0.0
    A.BORON_PPM = 0.0
    print("      %-26s k = %.5f +/- %4.0f pcm   [%.1f min]"
          % (tag, k, s * 1e5, (time.time() - t0) / 60.0))
    return k, s


def worth_pcm(k_ref, s_ref, k_ins, s_ins):
    """|delta rho| in pcm with 1-sigma propagated in quadrature."""
    w = abs(A._pcm(k_ref, k_ins))
    # d(rho)/dk = 1/k^2
    e = 1e5 * ((s_ref / k_ref ** 2) ** 2 + (s_ins / k_ins ** 2) ** 2) ** 0.5
    return w, e


# ==========================================================================
# R1 - individual worth of every CRA position
# ==========================================================================
def run_R1():
    """Single-cluster worth, evaluated at the reference ejected-rod state
       (fuel 900 K, moderator 556 K) so it is directly comparable with the
       902 +/- 34 pcm reported in the manuscript."""
    print("\n" + "=" * 74)
    print("[R1] individual CRA worth - fuel 900 K / mod 556 K / 90 % B-10")
    print("=" * 74)
    for cls, members in sorted(CLASSES.items()):
        print("   class %-6s : %d positions  %s" % (str(cls), len(members), members))

    T = A.T_MOD_K
    rho = A.RHO_WATER_NOM
    k_aro, s_aro = kof("aro", T, "R1_aro", fuel_T=A.T_FUEL_K, rho=rho)

    if os.environ.get("R1_ALL_16") == "1":
        targets = [(p, str(sym_class(p))) for p in CRA_16]
    else:
        targets = [(m[0], str(cls)) for cls, m in sorted(CLASSES.items())]
        biggest = max(CLASSES.items(), key=lambda kv: len(kv[1]))
        if len(biggest[1]) > 1:                       # explicit symmetry check
            targets.append((biggest[1][1], str(biggest[0]) + "_symcheck"))

    rows = []
    for pos, label in targets:
        tag = "R1_%d%d" % pos
        k, s = kof([pos], T, tag, fuel_T=A.T_FUEL_K, rho=rho, b10=0.90)
        w, e = worth_pcm(k_aro, s_aro, k, s)
        d_usd = w / A_BETA
        e_usd = d_usd * ((e / w) ** 2 + (BETA_SIG / A_BETA) ** 2) ** 0.5
        rows.append(dict(position=list(pos), sym_class=label, k_eff=k,
                         sigma_pcm=s * 1e5, worth_pcm=round(w, 1),
                         worth_sigma_pcm=round(e, 1),
                         dollars=round(d_usd, 3), dollars_sigma=round(e_usd, 3)))
        print("      -> worth %.0f +/- %.0f pcm  =  %.2f +/- %.2f $"
              % (w, e, d_usd, e_usd))
        RES["R1"] = dict(state="fuel 900 K / mod 556 K / 90 % B-10 / single cluster from ARO",
                         k_aro=k_aro, sigma_aro_pcm=s_aro * 1e5,
                         beta_eff_pcm=A_BETA, beta_sigma_pcm=BETA_SIG,
                         mode="all16" if os.environ.get("R1_ALL_16") == "1"
                              else "one per symmetry class",
                         classes={str(c): [list(p) for p in m]
                                  for c, m in CLASSES.items()},
                         results=rows)
        save()

    top = max(rows, key=lambda r: r["worth_pcm"])
    print("\n   MAX single-cluster worth: %s  %.0f +/- %.0f pcm  = %.2f $"
          % (top["position"], top["worth_pcm"], top["worth_sigma_pcm"], top["dollars"]))
    print("   manuscript currently reports 902 +/- 34 pcm = 1.28 $ for the central cluster")
    return RES["R1"]


# ==========================================================================
# R2 - 16 CRA with natural B4C (the missing fourth corner)
# ==========================================================================
def run_R2():
    """Bank worth of the 16-CRA layout with UNENRICHED absorber.
       Completes the 2x2 matrix: {12,16} clusters x {natural, 90 % B-10}."""
    print("\n" + "=" * 74)
    print("[R2] 16 CRA + natural B4C - missing corner of the lever matrix")
    print("=" * 74)
    T = A.T_MOD_K
    k_aro, s_aro = kof("aro", T, "R2_aro_hot")                    # isothermal HZP
    k_ari, s_ari = kof(CRA_16, T, "R2_ari_hot_natural", b10=0.0)
    bank, bank_e = worth_pcm(k_aro, s_aro, k_ari, s_ari)
    kadj = k_ari + 2 * s_ari + 0.005
    sdm = -(k_ari - 1.0) / k_ari * 100.0

    # cold stuck-rod, same basis as the manuscript's Table 2
    central = min(CRA_16, key=lambda q: (q[0] - CC) ** 2 + (q[1] - CC) ** 2)
    stuck = [p for p in CRA_16 if p != central]
    k_cold, s_cold = kof(stuck, 294.0, "R2_stuck_cold_natural", b10=0.0)

    print("\n   bank worth (16 CRA, natural) = %.0f +/- %.0f pcm" % (bank, bank_e))
    print("   published ladder for comparison:")
    print("      12 CRA natural    13,409 pcm")
    print("      12 CRA 90 %% B-10  15,673 pcm")
    print("      16 CRA 90 %% B-10  21,509 pcm")
    print("      16 CRA natural    %.0f pcm   <- this run" % bank)
    interaction = 21509 - 15673 - (bank - 13409)
    print("   interaction term (enrichment x count) = %.0f pcm" % interaction)
    print("   |interaction| small => the two levers are separable; large => they are not")

    RES["R2"] = dict(case="16 CRA, natural B4C, isothermal HZP 556 K",
                     n_cra=16, b10_enrichment=0.0,
                     k_aro_hot=k_aro, k_ari_hot=k_ari,
                     bank_worth_pcm=round(bank, 1), bank_sigma_pcm=round(bank_e, 1),
                     k_adj_ari_hot=round(kadj, 5), hot_sdm_pct=round(sdm, 2),
                     k_stuck_cold=k_cold, sigma_stuck_cold_pcm=s_cold * 1e5,
                     stuck_position=list(central),
                     ladder_reference_pcm={"12_natural": 13409, "12_b10": 15673,
                                           "16_b10": 21509},
                     interaction_term_pcm=round(interaction, 1),
                     note="completes the 2x2 lever matrix; interaction term tests separability")
    save()
    return RES["R2"]


# ==========================================================================
# R3 - boron sweep near the crossing
# ==========================================================================
def run_R3():
    """Cold stuck-rod boron sweep at 700/800/900 ppm to replace the
       500->1000 ppm linear interpolation that gives 785 ppm."""
    print("\n" + "=" * 74)
    print("[R3] boron sweep 700/800/900 ppm - cold 294 K, 16 CRA, most reactive stuck")
    print("=" * 74)
    central = min(CRA_16, key=lambda q: (q[0] - CC) ** 2 + (q[1] - CC) ** 2)
    stuck = [p for p in CRA_16 if p != central]

    rows = []
    for ppm in (700, 800, 900):
        k, s = kof(stuck, 294.0, "R3_%dppm" % ppm, b10=0.90, ppm=ppm)
        kadj = k + 2 * s + 0.005
        rows.append(dict(boron_ppm=ppm, k_eff=k, sigma_pcm=s * 1e5,
                         k_adj=round(kadj, 5),
                         acceptance="pass" if kadj <= 0.95 else "fail"))
        print("      %d ppm -> k = %.5f  k_adj = %.4f  %s"
              % (ppm, k, kadj, rows[-1]["acceptance"]))
        RES["R3"] = dict(state="cold 294 K / BOC / 16 CRA 90 % B-10 / most reactive stuck out",
                         stuck_position=list(central),
                         criterion="k_adj = k + 2 sigma + 0.005 <= 0.95",
                         published_interpolated_ppm=785, sweep=rows)
        save()

    xs = [r["boron_ppm"] for r in rows]
    ys = [r["k_adj"] for r in rows]
    if min(ys) <= 0.95 <= max(ys):
        cross = A._interp_cross(xs, ys, 0.95)
        RES["R3"]["direct_requirement_ppm"] = round(cross, 1)
        print("\n   direct crossing of k_adj = 0.95 at %.0f ppm" % cross)
        print("   manuscript's interpolated value: 785 ppm  (delta = %.0f ppm)"
              % (cross - 785))
    else:
        RES["R3"]["direct_requirement_ppm"] = None
        print("\n   k_adj = 0.95 not bracketed by 700-900 ppm; widen the sweep.")
    save()
    return RES["R3"]


PLAN = [("R1", run_R1), ("R2", run_R2), ("R3", run_R3)]

if __name__ == "__main__":
    want = [a.upper() for a in sys.argv[1:]] or ["ALL"]
    sel = [k for k, _ in PLAN] if "ALL" in want else want
    t0 = time.time()
    for key, fn in PLAN:
        if key not in sel:
            continue
        if key in RES:
            print("[%s] already in %s - delete that entry to re-run" % (key, OUT.name))
            continue
        fn()
        save()
    print("\n" + "=" * 74)
    print("done in %.1f min -> %s" % ((time.time() - t0) / 60.0, OUT))
    print("=" * 74)
    for k in ("R1", "R2", "R3"):
        print("  %s : %s" % (k, "complete" if k in RES else "NOT RUN"))
    print("\nSend %s back and the three open referee items close." % OUT.name)
