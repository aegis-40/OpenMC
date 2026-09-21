# -*- coding: utf-8 -*-
"""
R4 - adjoint-weighted beta_eff by iterated fission probability (IFP).
=====================================================================

WHY THIS RUN EXISTS
-------------------
Section 3.2 of the manuscript reports beta_eff = 704.5 +/- 28.2 pcm from the
prompt-k estimator:

    beta_eff = 1 - k_p / k

An earlier draft claimed OpenMC could not do better than that. **That claim was
wrong** - OpenMC implements the iterated-fission-probability method and returns
adjoint-weighted beta_eff and Lambda_eff directly. Since the whole
one-dollar comparison rests on beta_eff, the honest thing is to compute it the
better way rather than argue around it.

This script does exactly one thing: the same BOC / HFP / all-rods-out state as
Section 3.2, with IFP tallies enabled, and prints the adjoint-weighted value
beside the prompt-k one.

WHAT IT SETTLES
---------------
The manuscript currently argues that the conclusion survives even a 10 % error
in beta_eff, because reversing it needs beta_eff 20-28 % higher. That argument
becomes unnecessary the moment a direct adjoint-weighted number exists. If IFP
agrees with 704.5 pcm to within a few per cent, Section 3.2 gets shorter and
Section 6.3 loses a limitation entirely.

HOW TO RUN
----------
    python run_ifp_beta_eff.py

Environment variables:
    OPENMC_THREADS=8         threads
    AEGIS_MODEL_DIR=<path>   folder holding aegis40_safety_neutronics.py,
                             if auto-detection fails
    IFP_GENERATIONS=5        IFP generations to carry (default 5). Must be > 0
                             and <= the number of inactive batches (80 here).
    PAPER_STAT=final|medium  statistics (default final: 400 x 50,000, 80 inactive)

Runtime is one eigenvalue calculation - comparable to a single R1 case.
Results are written to ../data/ifp_beta_eff.json.

IF IT FAILS WITH "no IFP support"
---------------------------------
The kinetics API landed in recent OpenMC. If your build predates it, upgrade
OpenMC and re-run; nothing else in this study needs to change, because this
script only reads the locked model rather than modifying it.
"""
import json
import os
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------
# locate and import the locked core model (same pattern as run_paper_extra_cases)
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
    sys.exit("ERROR: could not find aegis40_safety_neutronics.py. "
             "Set AEGIS_MODEL_DIR to the folder that contains it.")

os.environ["SAFETY_RUN"] = "none"      # do not re-run the published case suite
os.chdir(MODEL_DIR)
sys.path.insert(0, str(MODEL_DIR))

import openmc                                            # noqa: E402
import aegis40_safety_neutronics as A                    # noqa: E402

print("[setup] OpenMC   :", openmc.__version__)
print("[setup] model dir:", MODEL_DIR)

STAT = A.STAT_FINAL if os.environ.get("PAPER_STAT", "final") == "final" else A.STAT_MEDIUM
NGEN = int(os.environ.get("IFP_GENERATIONS", "5"))
print("[setup] statistics:", STAT)
print("[setup] IFP generations:", NGEN)

if NGEN < 1 or NGEN > STAT["inactive"]:
    sys.exit("ERROR: IFP_GENERATIONS must be > 0 and <= inactive batches (%d)."
             % STAT["inactive"])

# --------------------------------------------------------------------------
# build the Section 3.2 state: BOC, hot full power, all rods out
# --------------------------------------------------------------------------
A.B10_ENRICH = 0.0
A.BORON_PPM = 0.0
model, _, _ = A.build_core(mod_temp=A.T_MOD_K,
                           water_density=A.RHO_WATER_NOM,
                           fuel_temp=A.T_FUEL_K,
                           control_rod_state="aro",
                           stats=STAT)

# --------------------------------------------------------------------------
# enable IFP
# --------------------------------------------------------------------------
if not hasattr(model, "add_kinetics_parameters_tallies"):
    sys.exit(
        "ERROR: this OpenMC build has no Model.add_kinetics_parameters_tallies().\n"
        "The adjoint-weighted kinetics API is not present. Upgrade OpenMC and\n"
        "re-run. Nothing else in the study depends on this script."
    )

model.settings.ifp_n_generation = NGEN
model.add_kinetics_parameters_tallies(num_groups=6)
print("[setup] IFP tallies added (6 delayed groups)")

run_dir = A._run_dir("R4_ifp_beta_eff")
t0 = time.time()
A._run_model(model, run_dir, tag="R4_ifp")
mins = (time.time() - t0) / 60.0

# --------------------------------------------------------------------------
# retrieve
# --------------------------------------------------------------------------
sps = sorted(Path(run_dir).glob("statepoint.*.h5"))
if not sps:
    sys.exit("ERROR: no statepoint written in %s" % run_dir)
sp_path = sps[-1]

with openmc.StatePoint(str(sp_path)) as sp:
    k = sp.keff
    lam, beta = sp.get_kinetics_parameters()

beta_pcm = float(beta.n) * 1e5
beta_sd = float(beta.s) * 1e5
lam_s = float(lam.n)
lam_sd = float(lam.s)

PROMPT_K, PROMPT_K_SD = 704.5, 28.2
diff = beta_pcm - PROMPT_K
pct = 100.0 * diff / PROMPT_K
comb = (beta_sd ** 2 + PROMPT_K_SD ** 2) ** 0.5

print("\n" + "=" * 68)
print("  k_eff (this run)      : %.6f +/- %.6f" % (k.n, k.s))
print("  Lambda_eff (IFP)      : %.4e +/- %.2e s" % (lam_s, lam_sd))
print("  beta_eff  (IFP)       : %.1f +/- %.1f pcm" % (beta_pcm, beta_sd))
print("  beta_eff  (prompt-k)  : %.1f +/- %.1f pcm   [manuscript S3.2]" % (PROMPT_K, PROMPT_K_SD))
print("  difference            : %+.1f pcm  (%+.1f %%,  %.1f sigma)"
      % (diff, pct, abs(diff) / comb if comb else 0.0))
print("=" * 68)

# --------------------------------------------------------------------------
# what it does to the dollar values
# --------------------------------------------------------------------------
print("\n  ejected-rod worth re-expressed on the IFP beta_eff:")
rows = []
for label, w, w_sd in (("HZP, isothermal 556 K", 844.0, 82.0),
                       ("hot fuel 900 K", 902.0, 34.0)):
    d_old = w / PROMPT_K
    d_new = w / beta_pcm
    sd_new = d_new * ((w_sd / w) ** 2 + (beta_sd / beta_pcm) ** 2) ** 0.5
    rows.append(dict(case=label, worth_pcm=w, worth_sigma_pcm=w_sd,
                     dollars_promptk=round(d_old, 3),
                     dollars_ifp=round(d_new, 3),
                     dollars_ifp_sigma=round(sd_new, 3),
                     still_above_one_dollar=bool(d_new - sd_new > 1.0)))
    print("    %-24s %.0f pcm -> %.2f $ (prompt-k)  |  %.2f +/- %.2f $ (IFP)  %s"
          % (label, w, d_old, d_new, sd_new,
             "ABOVE 1 $" if d_new > 1.0 else "*** BELOW 1 $ ***"))

if any(r["dollars_ifp"] <= 1.0 for r in rows):
    print("\n  !! At least one case falls to or below one dollar on the IFP value.")
    print("     That would change the manuscript's central claim - report it before")
    print("     editing anything else.")
else:
    print("\n  Both cases remain above one dollar. Section 3.2's robustness argument")
    print("  can be replaced by this direct value, and the Section 6.3 limitation")
    print("  on beta_eff methodology can be removed.")

out = Path(HERE).parent / "data" / "ifp_beta_eff.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(dict(
    state="BOC / HFP / all rods out - same state as manuscript section 3.2",
    openmc_version=openmc.__version__,
    statistics=STAT, ifp_n_generation=NGEN, runtime_min=round(mins, 1),
    k_eff=k.n, k_sigma=k.s,
    Lambda_eff_s=lam_s, Lambda_eff_sigma_s=lam_sd,
    beta_eff_ifp_pcm=round(beta_pcm, 2), beta_eff_ifp_sigma_pcm=round(beta_sd, 2),
    beta_eff_promptk_pcm=PROMPT_K, beta_eff_promptk_sigma_pcm=PROMPT_K_SD,
    difference_pcm=round(diff, 2), difference_percent=round(pct, 2),
    ejected_rod_dollars=rows,
), indent=2), encoding="utf-8")
print("\nwritten: %s   (%.1f min)" % (out, mins))
