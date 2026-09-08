# Aegis-40 — Verification & Validation matrix

Every code and correlation used in the thermal-hydraulic analysis, the V&V evidence for it, and where the
evidence lives in this appendix / the project repository. Reliability of the sources:
IAEA and OECD/NEA documents are marked **[IAEA]** / **[NEA]**; US NRC licensing
documents **[NRC]**; consensus standards **[STD]**; archival textbooks/journals **[LIT]**.

| # | Code / model | V&V activity | Result / acceptance | Evidence |
|---|---|---|---|---|
| 1 | OpenFOAM v2412 `chtMultiRegionFoam` conjugate-pin toolchain | **Code-to-published-data validation** against the NRC-licensed NuScale NPM-160 design **[NRC]** (same 37-FA core class): natural-circulation flow, core ΔT, temperature levels | toolchain reproduces the published NuScale operating point (ṁ(P) within 7 %, hot-leg T, saturation boundary — no tuning) | `NuScale_validation_report.docx` (this folder) + `NuScale_validation/` in the project repository |
| 2 | CFD energy conservation (GATE-1) | Advected power = analytic source integral, checked field-direct on EVERY mesh | ×0.992 / 0.996 / 0.998 (conserves ×1.00) | `01_OpenFOAM_CFD/energy_balance_verification.txt` |
| 3 | CFD discretisation error | ASME V&V-20 / Celik-2008 grid-convergence (GCI), 3 geometrically-similar meshes **[STD]** | GCI < 0.15 % on all temperatures | `01_OpenFOAM_CFD/mesh_independence_summary.csv` |
| 4 | CFD near-wall heat transfer | Cross-check vs the Dittus-Boelter correlation stack at the identical operating point | agreement < 9 K on every quantity (bulk/fuel < 1 K) | FER §6; `02_Python_safety_toolchain/make_figs_aegis.py` (F3) |
| 5 | W-3 CHF + Tong F-factor | Transcription verified against Tong (1972) / Todreas & Kazimi **[LIT]**; used as the conservative binding correlation (extrapolated at low G — reads low) | binding MDNBR 1.33 ≥ 1.30 | `02_Python_safety_toolchain/mdnbr.py` |
| 6 | Bowring-1972 CHF | **Term-for-term structural verification** vs the Todreas & Kazimi SI form **[LIT]** + numeric sanity + cross-check vs W-3 inside the W-3 validity window | coefficients verified; in-range at Aegis G | `docs/Aegis40_bowring_verification.md` (repo) |
| 7 | Groeneveld 2006 CHF look-up table | LUT planes transcribed from NED 237 (2007) with monotonicity assertions; interpolation hand-verified; K1/K4/K5 correction factors per **IAEA-TECDOC-1203 Table 3.3 [IAEA]** | corroborates W-3/Bowring: envelope MDNBR 6.18 | `02_Python_safety_toolchain/groeneveld.py`, `data/README_groeneveld_LUT.md` |
| 8 | Natural-circulation solver | Cube-root law ṁ ~ P^(1/3) verified against MASLWR/OSU test data trend and the published NuScale flow **[NRC/LIT]**; analytical loss budget (Idel'chik **[LIT]**) bounds K | delivered flow robust: worst-case K ≈ 17 still MDNBR ≥ 2.48 | `02_Python_safety_toolchain/natcirc.py`, `b2_loss_budget.py` |
| 9 | Thermal stack (PCT / fuel centreline) | Dittus-Boelter + Jens-Lottes **[LIT]** vs conjugate CFD (row 5); gap conductance consistent with the CFD contact resistance | PCT 353 °C, fuel 828 °C | `02_Python_safety_toolchain/thermal_stack.py` |
| 10 | Flow stability screen | Ishii-Zuber density-wave map + Ledinegg criterion per Todreas & Kazimi NS-II / Kakac & Bon review **[LIT]**; conservative choices documented in-code | design ×4.2 inside the boundary (no grid credit) | `02_Python_safety_toolchain/stability_map.py` |
| 11 | Decay heat / PRHR grace | ANS-5.1-class decay curve **[STD]** ×1.15 uncertainty; sensible + boil-off pool balance | ≥ 240 h grace (250 m³ vented pool) | `02_Python_safety_toolchain/f5_prhr.py` |
| 12 | SBLOCA / containment | Bounding-by-reference to the NRC-licensed NuScale envelope **[NRC]** (0.78× module power, same core, immersed steel CNV) | bounded; explicitly labelled as bounding | `docs/Aegis40_F3_F6_bounding.md` (repo) |
| 13 | Cycle peaking acceptance framing | COLR practice per NUREG-1431 **[NRC]**; SMR precedent: NuScale DCA, CAREM-25, SMART **[LIT/NRC]** | design-specific COLR envelope F_q 2.468 | FER §8.1 (peaking record: neutronics package) |

**Repeatability.** The CFD and every python tool are deterministic: identical inputs
reproduce identical outputs bit-for-bit (steady single-phase, fixed schemes/seeds not
applicable). The Monte Carlo neutronics is stochastic by nature; repeatability is
demonstrated by the quoted statistics (σ_k 22–26 pcm at 16 M active histories) and the
k-consistency checks. The mesh-independence tool audits field write-times to prove the
three CFD solutions are independent runs, and its mixing-cup/mass-flow reductions were
verified to reproduce the solver's own function objects to all printed digits.
