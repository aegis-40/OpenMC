"""Discriminating test: is the production run's 722.5 pcm a NATURAL-boron rod?
Same state as the corrected case (T_fuel=900, ARO reference) but natural B4C."""
import os, sys, time
from pathlib import Path
os.environ["SAFETY_RUN"] = "none"
W = Path("/home/samira/aegis_run/rea_natB"); W.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("SAFETY_OUT", str(W))
SAF = Path(__file__).resolve().parents[2] / (
    "docs/competition/digital-appendix/4_safety_neutronics/code/aegis40_safety_neutronics.py")
import importlib.util
spec = importlib.util.spec_from_file_location("safmod", str(SAF))
saf = importlib.util.module_from_spec(spec); sys.modules["safmod"] = saf
spec.loader.exec_module(saf)
saf.THREADS = 8
STAT = dict(batches=250, inactive=60, particles=30000)
N = saf.N_CORE
base = [(i, j) for j in range(N) for i in range(N) if saf.CR_MAP[N-1-j, i] == 1]
CRA16 = base + [p for p in [(3,5),(1,3),(5,3),(3,1)] if p not in base]
cc = N // 2
central = min(CRA16, key=lambda q: (q[0]-cc)**2 + (q[1]-cc)**2)
saf.BORON_PPM = 0.0
saf.B10_ENRICH = 0.0                       # NATURAL boron
m, _, _ = saf.build_core(mod_temp=saf.T_MOD_K, water_density=saf._rho_at(saf.T_MOD_K),
                         fuel_temp=saf.T_FUEL_K, control_rod_state={central}, stats=STAT)
d = saf._run_dir("rea_natB"); t0 = time.time()
saf._run_model(m, d, tag="natB"); k1, s1 = saf._keff(d)
k0 = 1.150421
w = (1/k1 - 1/k0)*1e5
print(f"\n  natural-B4C single cluster, T_fuel=900: k = {k1:.6f} +/- {s1*1e5:.1f} pcm")
print(f"  worth = {w:.1f} pcm   (90% B-10 gives 902.2; production diagnostic says 722.5)")
print(f"  -> {'MATCHES production (natural boron explains the gap)' if abs(w-722.5) < 90 else 'does NOT match production'}")
