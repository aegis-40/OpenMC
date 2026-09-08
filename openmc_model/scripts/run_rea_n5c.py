"""Ejected-rod (REA) worth envelope on the final N5C basis.

Single highest-worth CRA ejected from an otherwise all-rods-out HZP/HFP core --
the unshadowed single-rod worth, which bounds the ejected-rod worth used in
NUREG-0800 SRP 15.4.8 screening.  Compared against beta_eff to test the 1$
prompt-criticality line.

Uses the same safety-neutronics model that produced N5C, so the result is
directly comparable to the 21,509 pcm bank worth and the MSLB cases.
"""
import os, sys, json, time
from pathlib import Path

os.environ["SAFETY_RUN"] = "none"
WORK = Path(os.environ.get("REA_OUT", "/home/samira/aegis_run/rea_n5c")).resolve()
WORK.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("SAFETY_OUT", str(WORK))

SAF = Path(__file__).resolve().parents[2] / (
    "docs/competition/digital-appendix/4_safety_neutronics/code/aegis40_safety_neutronics.py")
import importlib.util
spec = importlib.util.spec_from_file_location("safmod", str(SAF))
saf = importlib.util.module_from_spec(spec); sys.modules["safmod"] = saf
spec.loader.exec_module(saf)

saf.THREADS = int(os.environ.get("OPENMC_THREADS", "8"))
STAT = saf.STAT_SAFETY
N = saf.N_CORE
base = [(i, j) for j in range(N) for i in range(N) if saf.CR_MAP[N - 1 - j, i] == 1]
extra = [(3, 5), (1, 3), (5, 3), (3, 1)]
CRA16 = base + [p for p in extra if p not in base]
cc = N // 2
central = min(CRA16, key=lambda q: (q[0] - cc) ** 2 + (q[1] - cc) ** 2)
print(f"[rea] {len(CRA16)} CRAs; most-central (highest-worth) CRA = {central}; STAT={STAT}", flush=True)

def krun(state, tag, b10):
    saf.BORON_PPM = 0.0; saf.B10_ENRICH = b10
    m, _, _ = saf.build_core(mod_temp=saf.T_MOD_K, water_density=saf._rho_at(saf.T_MOD_K),
                             fuel_temp=float(saf.T_MOD_K), control_rod_state=state, stats=STAT)
    d = saf._run_dir(tag); t0 = time.time(); saf._run_model(m, d, tag=tag)
    k, s = saf._keff(d); saf.B10_ENRICH = 0.0
    print(f"   {tag}: k = {k:.5f} +/- {s*1e5:.0f} pcm  [{time.time()-t0:.0f}s]", flush=True)
    return k, s

# all-rods-out reference (rod material irrelevant when withdrawn)
k0, s0 = krun("aro", "rea_aro", 0.0)
# single most-central rod inserted, 90 % enriched B-10 (final design)
k1, s1 = krun({central}, "rea_one_in", 0.90)

worth = (1.0 / k1 - 1.0 / k0) * 1e5
sig = ((s0 ** 2 + s1 ** 2) ** 0.5) * 1e5
BETA = 650.0                      # beta_eff, LEU UO2 PWR at BOC (typical 640-680 pcm)
dollars = worth / BETA
res = dict(case="REA_ejected_rod_worth_N5C",
           config=f"16 CRA @ 90 % B-10; single most-central CRA {central} ejected from ARO",
           k_aro=k0, k_aro_sigma_pcm=s0 * 1e5, k_one_in=k1, k_one_in_sigma_pcm=s1 * 1e5,
           ejected_rod_worth_pcm=round(worth), sigma_pcm=round(sig),
           beta_eff_pcm=BETA, worth_dollars=round(dollars, 2),
           prompt_critical=bool(dollars >= 1.0),
           criterion="NUREG-0800 SRP 15.4.8 / RG 1.77 screening: ejected worth < 1$ is benign",
           note=("unshadowed single-rod worth from ARO bounds the ejected-rod worth; "
                 "compare with total bank worth 21,509 pcm (N5C)"))
(WORK / "rea_n5c_results.json").write_text(json.dumps(res, indent=2))
print(f"\n[rea] ejected-rod worth = {worth:.0f} +/- {sig:.0f} pcm = {dollars:.2f}$ "
      f"(beta_eff {BETA:.0f} pcm)")
print(f"[rea] {'EXCEEDS 1$ - prompt-critical excursion, REA would be limiting' if dollars >= 1 else 'below 1$ - benign'}")
print("REA_N5C_COMPLETE ->", WORK / "rea_n5c_results.json")
