"""Effective delayed-neutron fraction (beta_eff) for the Aegis-40 reference core.

Method
------
Prompt-k method: two eigenvalue calculations at the identical state, one with
delayed neutrons produced normally and one with every fission neutron forced
prompt (`create_delayed_neutrons = False`).  Then

    k_p = k (1 - beta_eff)   =>   beta_eff = 1 - k_p / k

This is the standard Monte-Carlo estimate of beta_eff.  It is *not* the
adjoint-weighted IFP value (OpenMC 0.15.3 exposes no IFP tally scores in the
Python API); the two typically agree to within a few per cent for LWR lattices.

State: BOC, fresh fuel, hot full power, all rods out -- the same state at which
the ejected-rod worth is evaluated, so the 1$ comparison is self-consistent.

Statistics: STAT_FINAL (400 batches x 50,000 particles, 80 inactive) on each
run, giving sigma(k) ~ 25 pcm and hence sigma(beta) ~ 30 pcm.

Usage
-----
  export OPENMC_CROSS_SECTIONS=.../endfb-viii.0-hdf5/cross_sections.xml
  OPENMC_THREADS=8 python -u run_beta_eff.py
"""
import os, sys, json, time
from pathlib import Path

os.environ["SAFETY_RUN"] = "none"
WORK = Path(os.environ.get("BETA_OUT", "/home/samira/aegis_run/beta_eff")).resolve()
WORK.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("SAFETY_OUT", str(WORK))

SAF = Path(__file__).resolve().parents[2] / (
    "docs/competition/digital-appendix/4_safety_neutronics/code/aegis40_safety_neutronics.py")
import importlib.util
spec = importlib.util.spec_from_file_location("safmod", str(SAF))
saf = importlib.util.module_from_spec(spec); sys.modules["safmod"] = saf
spec.loader.exec_module(saf)

saf.THREADS = int(os.environ.get("OPENMC_THREADS", "8"))
STAT = dict(batches=400, inactive=80, particles=50000)     # STAT_FINAL
print(f"[beta] work={WORK}  stat={STAT}  threads={saf.THREADS}", flush=True)


def krun(tag, delayed):
    saf.BORON_PPM = 0.0
    saf.B10_ENRICH = 0.0
    m, _, _ = saf.build_core(mod_temp=saf.T_MOD_K,
                             water_density=saf._rho_at(saf.T_MOD_K),
                             fuel_temp=saf.T_FUEL_K,
                             control_rod_state="aro", stats=STAT)
    m.settings.create_delayed_neutrons = bool(delayed)
    d = saf._run_dir(tag)
    t0 = time.time()
    saf._run_model(m, d, tag=tag)
    k, s = saf._keff(d)
    print(f"   {tag}: delayed={delayed}  k = {k:.6f} +/- {s*1e5:.1f} pcm  [{time.time()-t0:.0f}s]",
          flush=True)
    return k, s


k_tot, s_tot = krun("beta_total", True)     # normal: prompt + delayed
k_pmt, s_pmt = krun("beta_prompt", False)   # all fission neutrons forced prompt

beta = 1.0 - k_pmt / k_tot
# sigma propagation for beta = 1 - kp/kt
sig = (k_pmt / k_tot) * ((s_pmt / k_pmt) ** 2 + (s_tot / k_tot) ** 2) ** 0.5
beta_pcm, sig_pcm = beta * 1e5, sig * 1e5

REA_PROD = 722.5      # central-cluster worth, 3 Jul STAT_FINAL production run
REA_SAF = 844.0       # same quantity, safety-neutronics model (2026-08-20)

res = dict(case="beta_eff_prompt_method",
           method="prompt-k: beta_eff = 1 - k_prompt/k_total (create_delayed_neutrons=False)",
           state="BOC fresh, HFP, all rods out, 12.8 MPa, T_mod 556 K, T_fuel 900 K",
           statistics=STAT,
           k_total=k_tot, k_total_sigma_pcm=s_tot * 1e5,
           k_prompt=k_pmt, k_prompt_sigma_pcm=s_pmt * 1e5,
           beta_eff_pcm=round(beta_pcm, 1), beta_eff_sigma_pcm=round(sig_pcm, 1),
           ejected_rod_worth_production_pcm=REA_PROD,
           ejected_rod_worth_safety_model_pcm=REA_SAF,
           dollars_production=round(REA_PROD / beta_pcm, 3),
           dollars_safety_model=round(REA_SAF / beta_pcm, 3),
           note=("prompt-k estimate, not adjoint-weighted IFP; OpenMC 0.15.3 exposes no IFP "
                 "tally scores. Computed in the safety-neutronics model; beta_eff is a ratio of "
                 "prompt to total fission-neutron production and is far less sensitive to the "
                 "~590 pcm absolute-reactivity offset between the two core models than k itself."))
(WORK / "beta_eff_results.json").write_text(json.dumps(res, indent=2))

print("\n" + "=" * 66)
print(f"  k_total  = {k_tot:.6f} +/- {s_tot*1e5:.1f} pcm")
print(f"  k_prompt = {k_pmt:.6f} +/- {s_pmt*1e5:.1f} pcm")
print(f"  beta_eff = {beta_pcm:.1f} +/- {sig_pcm:.1f} pcm")
print("-" * 66)
print(f"  ejected-rod worth 722.5 pcm (production)   = {REA_PROD/beta_pcm:.3f} $")
print(f"  ejected-rod worth 844   pcm (safety model) = {REA_SAF/beta_pcm:.3f} $")
print("=" * 66)
print("BETA_EFF_COMPLETE ->", WORK / "beta_eff_results.json")
