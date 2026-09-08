"""Ejected-rod worth at the CORRECT nominal fuel temperature (900 K).

The safety-neutronics helpers pass fuel_temp = moderator temp, so every hot-state
result in that module (including the 2026-08-20 REA of 844 pcm) was computed with
fuel at 556 K instead of the nominal 900 K. This repeats the single-cluster case at
T_fuel = 900 K to compare against the 3 Jul production value of 722.5 pcm.

k(ARO, T_fuel=900) = 1.150421 +/- 23.9 pcm is already known from the beta_eff run.
"""
import os, sys, json, time
from pathlib import Path
os.environ["SAFETY_RUN"] = "none"
WORK = Path(os.environ.get("REAFIX_OUT", "/home/samira/aegis_run/rea_tfuel_fix")).resolve()
WORK.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("SAFETY_OUT", str(WORK))
SAF = Path(__file__).resolve().parents[2] / (
    "docs/competition/digital-appendix/4_safety_neutronics/code/aegis40_safety_neutronics.py")
import importlib.util
spec = importlib.util.spec_from_file_location("safmod", str(SAF))
saf = importlib.util.module_from_spec(spec); sys.modules["safmod"] = saf
spec.loader.exec_module(saf)
saf.THREADS = int(os.environ.get("OPENMC_THREADS", "8"))
STAT = dict(batches=400, inactive=80, particles=50000)
N = saf.N_CORE
base = [(i, j) for j in range(N) for i in range(N) if saf.CR_MAP[N - 1 - j, i] == 1]
CRA16 = base + [p for p in [(3,5),(1,3),(5,3),(3,1)] if p not in base]
cc = N // 2
central = min(CRA16, key=lambda q: (q[0]-cc)**2 + (q[1]-cc)**2)
print(f"[reafix] central CRA {central}; T_fuel = {saf.T_FUEL_K} K (NOMINAL); stat={STAT}", flush=True)
saf.BORON_PPM = 0.0; saf.B10_ENRICH = 0.90
m, _, _ = saf.build_core(mod_temp=saf.T_MOD_K, water_density=saf._rho_at(saf.T_MOD_K),
                         fuel_temp=saf.T_FUEL_K, control_rod_state={central}, stats=STAT)
d = saf._run_dir("rea_one_in_Tfuel900"); t0 = time.time()
saf._run_model(m, d, tag="rea900")
k1, s1 = saf._keff(d)
print(f"   k(one cluster in, T_fuel=900) = {k1:.6f} +/- {s1*1e5:.1f} pcm  [{time.time()-t0:.0f}s]", flush=True)
k0, s0 = 1.150421, 0.000239                     # from the beta_eff run, same state
worth = (1/k1 - 1/k0)*1e5
sig = ((s0**2 + s1**2)**0.5)*1e5
BETA, BSIG = 704.5, 28.2
dol = worth/BETA
dsig = dol*((sig/worth)**2 + (BSIG/BETA)**2)**0.5
res = dict(case="REA_ejected_rod_worth_Tfuel900",
           note="corrects the fuel-temperature error in the safety-module helpers",
           k_aro=k0, k_one_in=k1, ejected_rod_worth_pcm=round(worth,1), sigma_pcm=round(sig,1),
           beta_eff_pcm=BETA, beta_eff_sigma_pcm=BSIG,
           dollars=round(dol,3), dollars_sigma=round(dsig,3),
           production_run_value_pcm=722.5,
           superseded_value_pcm=844.0)
(WORK/"rea_tfuel900_results.json").write_text(json.dumps(res, indent=2))
print("\n" + "="*64)
print(f"  ejected-rod worth (T_fuel=900) = {worth:.1f} +/- {sig:.1f} pcm")
print(f"  production run (3 Jul)         = 722.5 pcm")
print(f"  superseded (T_fuel=556)        = 844 pcm")
print(f"  in dollars (beta 704.5)        = {dol:.3f} +/- {dsig:.3f} $")
print("="*64)
print("REAFIX_COMPLETE")
