"""Measured SF97-4 isotopics for the Takahama-3 depletion benchmark.

Source: OECD/NEA NEA/NSC/DOC(2013)1 — Appendix A result tables (experimental
column) and Appendix C (chemical-analysis uncertainties). Sample SF97-4,
~46 GWd/t. Units: grams per tonne of INITIAL uranium (g/tUi).

Comparison times (per report):
  - actinides + fission products: at discharge (zero cooling)
  - samarium isotopes (Table A.5): at 3.96 years cooling
Notes:
  - Pu239 "measured" = Pu239 + Np239 (Np239 short half-life -> counted at t=0).
  - Sm147 includes decay from Nd147; Sm151 includes decay from Pm151.
"""

# nuclide: (measured value [g/tUi], 1-sigma uncertainty [fraction], time tag)
MEASURED = {
    # --- actinides @ discharge (Table A.1) ---
    "U234":  (1.872e+02, 0.01,  "discharge"),
    "U235":  (8.179e+03, 0.001, "discharge"),
    "U236":  (5.528e+03, 0.02,  "discharge"),
    "U238":  (9.246e+05, 0.001, "discharge"),
    "Np237": (6.604e+02, 0.10,  "discharge"),
    "Pu238": (3.199e+02, 0.005, "discharge"),
    "Pu239": (6.037e+03, 0.003, "discharge+Np239"),   # measured = Pu239 + Np239
    "Pu240": (2.668e+03, 0.003, "discharge"),
    "Pu241": (1.770e+03, 0.003, "discharge"),
    "Pu242": (8.246e+02, 0.003, "discharge"),
    "Am241": (5.311e+01, 0.02,  "discharge"),
    "Am242m":(1.233e+00, 0.10,  "discharge"),
    "Am243": (1.924e+02, 0.005, "discharge"),
    "Cm242": (2.044e+01, 0.10,  "discharge"),
    "Cm243": (8.721e-01, 0.02,  "discharge"),
    "Cm244": (8.810e+01, 0.02,  "discharge"),
    "Cm245": (6.042e+00, 0.02,  "discharge"),
    "Cm246": (7.440e-01, 0.005, "discharge"),
    "Cm247": (1.098e-02, 0.10,  "discharge"),
    # --- fission products @ discharge (Table A.3) ---
    "Ru106": (1.936e+02, 0.05,  "discharge"),
    "Cs134": (2.139e+02, 0.03,  "discharge"),
    "Cs137": (1.749e+03, 0.03,  "discharge"),
    "Ce144": (3.756e+02, 0.10,  "discharge"),
    "Nd143": (1.048e+03, 0.001, "discharge"),
    "Nd144": (1.567e+03, 0.001, "discharge"),
    "Nd145": (9.118e+02, 0.001, "discharge"),
    "Nd146": (1.008e+03, 0.001, "discharge"),
    "Nd148": (5.204e+02, 0.001, "discharge"),
    "Nd150": (2.516e+02, 0.001, "discharge"),
    "Eu154": (3.739e+01, 0.03,  "discharge"),
    # --- samarium @ 3.96 y cooling (Table A.5) ---
    "Sm147": (2.468e+02, 0.001, "3.96y"),   # incl decay from Nd147
    "Sm148": (2.338e+02, 0.001, "3.96y"),
    "Sm149": (3.943e+00, 0.001, "3.96y"),
    "Sm150": (4.074e+02, 0.001, "3.96y"),
    "Sm151": (1.491e+01, 0.001, "3.96y"),   # incl decay from Pm151
    "Sm152": (1.298e+02, 0.001, "3.96y"),
    "Sm154": (5.252e+01, 0.001, "3.96y"),
}

# burnup of the SF97-4 sample (Nd-148 method), GWd/tU
SAMPLE_BURNUP_GWD_T = 46.05
