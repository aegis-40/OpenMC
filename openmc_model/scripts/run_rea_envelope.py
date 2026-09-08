#!/usr/bin/env python3
"""REA ejected-rod worth envelope (Adilbek Q3, NUREG-0800 SRP 15.4.8).

Worth of the single most-central CRA from the nominal HFP BOC critical state
(ARO vs that one rod inserted) with the FINAL design: 16 CRA, 90% enriched-B10
B4C. If ejected worth < 1$ (beta_eff ~ 650 pcm) the excursion is benign - no
prompt criticality - and a point-kinetics envelope suffices for the FER.

Reuses build_core from digital_twin/twin_sweep.py (source-patched to the final
rod absorber + 16-CRA map before exec).

Run in WSL:  OPENMC_THREADS=8 python run_rea_envelope.py
"""
import os, re
from pathlib import Path
import numpy as np

TW = Path(__file__).resolve().parent.parent / "digital_twin" / "twin_sweep.py"
src = TW.read_text()
src = src[:src.index("# DIGITAL-TWIN sweep (Day 1)")]              # drop the sweep driver
src = src.rsplit("# =", 1)[0]                                       # drop the dangling header line
# FINAL design patch 1: 90% enriched-B10 B4C control rods
src = re.sub(r'(\w+)\.add_element\(\s*"B"\s*,\s*4\.0\s*\)',
             r'\1.add_nuclide("B10", 3.6); \1.add_nuclide("B11", 0.4)  # 90% B-10 (LOCKED)', src)
g = {}
exec(compile(src, str(TW), "exec"), g)

# FINAL design patch 2: 16-CRA map (12 checkerboard + 4 central-cross, N5C)
CR_MAP, N_CORE = g["CR_MAP"], g["N_CORE"]
for (r, c) in ((1, 3), (3, 1), (3, 5), (5, 3)):
    CR_MAP[r, c] = 1
assert int(CR_MAP.sum()) == 16, CR_MAP.sum()

STAT = dict(batches=180, inactive=50, particles=20000)              # STAT_MEDIUM
build_core, _run_dir, _run_model, _keff = g["build_core"], g["_run_dir"], g["_run_model"], g["_keff"]

# most-central CRA (array coords -> lattice (i,j) as used by control_rod_state)
_cra = [(i, j) for j in range(N_CORE) for i in range(N_CORE) if CR_MAP[N_CORE - 1 - j, i] == 1]
_cc = (N_CORE - 1) // 2
central = min(_cra, key=lambda p: (p[0] - _cc) ** 2 + (p[1] - _cc) ** 2)
print(f"[rea] 16-CRA map OK; most-central CRA at lattice {central}; STAT={STAT}", flush=True)

ks = {}
for lbl, state in (("aro", "aro"), ("one_in", {central})):
    model, _, _ = build_core(control_rod_state=state, stats=STAT)
    d = _run_dir(f"rea_{lbl}")
    _run_model(model, d, tag=f"rea_{lbl}")
    ks[lbl] = _keff(d)
    print(f"[rea] {lbl}: k = {ks[lbl][0]:.5f} +/- {ks[lbl][1]*1e5:.0f} pcm", flush=True)

k0, s0 = ks["aro"]; k1, s1 = ks["one_in"]
worth = (1 / k1 - 1 / k0) * 1e5
sig = ((s0 ** 2 + s1 ** 2) ** 0.5) * 1e5
beta = 650.0
dollars = worth / beta
verdict = "BENIGN (<1$, no prompt criticality)" if dollars < 1.0 else "REQUIRES transient analysis (>1$)"
print(f"\n[rea] ejected-rod worth = {worth:.0f} +/- {sig:.0f} pcm = {dollars:.2f}$ (beta_eff {beta:.0f} pcm)")
print(f"[rea] VERDICT: {verdict}")
out = Path(os.path.expanduser("~/aegis_run/rea_envelope.txt"))
out.write_text(f"central_cra={central}\nk_aro={k0:.5f}+/-{s0*1e5:.0f}pcm\nk_one_in={k1:.5f}+/-{s1*1e5:.0f}pcm\n"
               f"worth_pcm={worth:.0f}+/-{sig:.0f}\ndollars={dollars:.2f}\nverdict={verdict}\n")
print("REA_COMPLETE")
