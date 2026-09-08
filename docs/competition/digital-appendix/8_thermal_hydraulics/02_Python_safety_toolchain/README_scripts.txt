================================================================================
 AEGIS-40 THERMAL-HYDRAULIC PYTHON TOOLCHAIN — sample inputs & what they do
================================================================================
All scripts default to the Aegis-40 design point (OpenMC-consistent constants;
the COLR design envelope F_q 2.4675 as the safety basis), so a BARE RUN of each
script IS the sample input, and every number quoted in the FER is reproduced by
the commands below. Pure python3; only the figure/report builders need
matplotlib / python-docx (see requirements.txt).

--------------------------------------------------------------------------------
 SCRIPT                    RUN                         WHAT IT PRODUCES
--------------------------------------------------------------------------------
 natcirc.py                python3 natcirc.py          Natural-circulation loop
   1-D buoyancy/friction balance; cube-root law mdot ~ P^(1/3).
   Design point: H_tc 4.0 m -> mdot 467 kg/s, G 542 kg/m2 s, core dT 50 K.

 mdnbr.py                  python3 mdnbr.py            Hot-channel DNBR profile
   CHF correlations: --chf w3 (W-3 + Tong F), --chf bowring (low-flow-valid),
   --chf groeneveld (2006 LUT + K1/K4/K5 per IAEA-TECDOC-1203 Tab. 3.3).
   Envelope results: W-3 1.37 (cosine) / Bowring 2.20 / LUT 6.18.

 thermal_stack.py          python3 thermal_stack.py --boiling
   PCT & fuel centreline: Dittus-Boelter film + 1-D radial conduction +
   Jens-Lottes subcooled-boiling clamp (--boiling = the reported basis).
   Envelope: PCT 353 C, fuel centreline 828 C.  (Bare run = single-phase
   film only, over-predicts the clad where T_wall > Tsat.)

 cycle_mdnbr.py            python3 cycle_mdnbr.py --shapes --aoo
   BOC/MOC/EOC + COLR-envelope MDNBR with the record axial shapes
   (data/axial_profile_BOC_MOC_EOC.csv). Binding: 1.33 (W-3) / 2.13 (Bowring);
   AOO corner 1.57.

 aoo_dnbr.py               python3 aoo_dnbr.py         Bounding AOO envelope
   Quasi-steady power x flow sweep (118 % P / 80 % G bounding corner).

 stability_map.py          python3 stability_map.py    Flow-stability screen
   Ledinegg (excursive) + Ishii-Zuber density-wave map (N_sub-N_pch);
   design x4.2 inside the boundary without spacer-grid credit.

 f5_prhr.py                python3 f5_prhr.py --vol 250 --unc 1.15
   Passive decay-heat grace period (ANS-5.1-class decay + pool boil-off):
   >= 240 h for a 250 m3 vented pool.

 f6_suppression.py         python3 f6_suppression.py
   Suppression-containment SBLOCA screening (mass-energy balance):
   full-inventory blowdown into the IRWST -> quasi-static P 0.139 MPa
   (<= 0.414 MPa design, x3 margin); ~16.5 h to design P with zero
   heat-removal credit; no-pool counterfactual ~0.98 MPa (suppression
   required); IRWST gravity-head check -> staged-ADS end-state <= ~0.20 MPa.

 b2_loss_budget.py         python3 b2_loss_budget.py   Loop form-loss budget
   Per-component K referenced to core velocity (Idel'chik-class correlations);
   best-estimate K ~ 5-8 vs the assumed 12 (conservative).

 aegis_sweep.py            python3 aegis_sweep.py      H_tc feasibility sweep
   Riser-height sweep -> G, MDNBR, PCT (single source of shared constants).

 groeneveld.py             python3 groeneveld.py       CHF LUT interpolator
   Loads data/groeneveld_2006_lut.csv (NED 237 subset); refuses to fabricate.

 meshindep.py              python3 meshindep.py        GCI + GATE-1
   Field-direct mesh-independence (ASME V&V-20) + energy balance; needs the
   three completed CFD cases on disk (see 02_).

 make_figs_aegis.py        python3 make_figs_aegis.py  Report figures F1-F8
 make_paraview_figs.py     pvbatch make_paraview_figs.py   Figures F9a-c
 build_report_aegis.py     python3 build_report_aegis.py   The .docx report
--------------------------------------------------------------------------------
 Every tool prints its assumptions and validity-range warnings with the result.
================================================================================
