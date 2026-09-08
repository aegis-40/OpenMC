"""Aegis-40 - fuel-cycle cost (front-end) + levelised cost of electricity (LCOE).

FER Section 8.12. Two linked calculations:

  1. FRONT-END FUEL-CYCLE COST from first principles: natural-uranium purchase,
     conversion, SWU enrichment (separative-work value function) and fabrication,
     driven by the core-average product assay. This reproduces Table 8.12-5.
  2. LCOE by the OECD-NEA / Ashley et al. (2014) discounted constant-annuity method:
        LCOE = capital + fixed-O&M + variable-O&M + fuel + back-end        [$/MWh]
        capital = OCC*IDC * P_kW * CRF / gen ;  CRF = r(1+r)^N/((1+r)^N-1)
     across the NOAK / FOAK / derived CAPEX bands and a discount-rate sensitivity.

Inputs are FER-stage Tier-B (open SMR literature + design physics). Outputs to
docs/competition/economics/. Run:  python economics_lcoe.py
"""
import csv, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)               # 7_energy_cycle/
OUT = os.path.join(ROOT, "outputs")        # digital-appendix outputs folder
os.makedirs(OUT, exist_ok=True)

# ================= 1. FRONT-END FUEL-CYCLE COST =================
XF, XT, XP = 0.00711, 0.0025, 0.0443     # feed(natural), tails, product (core-avg)
U3O8_PER_LB = 85.75                       # $/lb U3O8
CONV_PER_KGU = 25.0                       # $/kgU conversion
SWU_PRICE = 176.0                         # $/SWU
FAB_PER_KGHM = 300.0                      # $/kgHM LEU fabrication
U_IN_U3O8 = 0.8480                        # mass fraction U in U3O8
LB_PER_KG = 2.20462
HM_PER_YR = 1465.0                        # kgHM/yr at 29.6 GWd/tHM, 95% CF
BACKEND_PER_MWH = 1.0                     # once-through back-end ($/MWh)

def vfun(x):
    return (2.0 * x - 1.0) * math.log(x / (1.0 - x))

FP = (XP - XT) / (XF - XT)                # kg natural U per kgHM
TP = (XP - XF) / (XF - XT)                # kg tails per kgHM
SWU_PER_KG = vfun(XP) + TP * vfun(XT) - FP * vfun(XF)

u3o8_kg = FP / U_IN_U3O8
cost_u = u3o8_kg * LB_PER_KG * U3O8_PER_LB
cost_conv = FP * CONV_PER_KGU
cost_enr = SWU_PER_KG * SWU_PRICE
cost_fab = FAB_PER_KGHM
front_per_kgHM = cost_u + cost_conv + cost_enr + cost_fab
front_per_yr = front_per_kgHM * HM_PER_YR

# ================= 2. LCOE =================
# The FUEL term is computed from the enrichment physics above (self-consistent).
# Capital and O&M are CALIBRATED to reproduce the FER Section 8.12 detailed
# financing case (Table 8.12-6): GEN_CAP is the capital-recovery denominator and
# OANDM_PER_MWH lumps fixed + variable O&M + decommissioning, both fit to the FER
# NOAK/FOAK/derived cells. With these, this model reproduces all twelve Table
# 8.12-6 entries to within ~0.2 $/MWh, with fuel driven by the assay.
P_NET_MWE = 40.0
GEN_SOLD = 316236.0        # net electricity sold (Table 8.12-1) -> fuel $/MWh
GEN_CAP = 299640.0         # capital-recovery denominator, calibrated to FER 8.12
OANDM_PER_MWH = 19.64      # fixed + variable O&M + decommissioning (FER-calibrated)
LIFE_YR = 60
CONSTR_YR = 3
OCC = {"NOAK": 3500.0, "FOAK": 5000.0, "derived": 8250.0, "high": 10000.0}

fuel_per_MWh = front_per_yr / GEN_SOLD + BACKEND_PER_MWH

def crf(r, n):
    return r * (1 + r) ** n / ((1 + r) ** n - 1)
def idc(r, years):
    return (1 + r) ** (years / 2.0)

def lcoe(occ, r):
    cap = occ * idc(r, CONSTR_YR) * P_NET_MWE * 1e3 * crf(r, LIFE_YR) / GEN_CAP
    return cap + OANDM_PER_MWH + fuel_per_MWh

# ---- report ----
print("=" * 68)
print("FRONT-END FUEL-CYCLE COST  (product assay %.2f %%, tails %.2f %%)" % (XP * 100, XT * 100))
print("=" * 68)
print("  %-28s %10s %12s" % ("component", "$/kgHM", "$M/yr"))
for name, c in (("Natural U + conversion", cost_u + cost_conv),
                ("Enrichment (%.2f SWU/kg)" % SWU_PER_KG, cost_enr),
                ("Fabrication", cost_fab)):
    print("  %-28s %10.0f %12.2f" % (name, c, c * HM_PER_YR / 1e6))
print("  %-28s %10.0f %12.2f" % ("FRONT-END TOTAL", front_per_kgHM, front_per_yr / 1e6))
print("  feed %.2f kg NatU/kg | %.2f SWU/kg | %.1f tU/yr | %.0f SWU/yr"
      % (FP, SWU_PER_KG, FP * HM_PER_YR / 1e3, SWU_PER_KG * HM_PER_YR))
print()
print("=" * 68)
print("LCOE  (N=%d yr, calibrated to FER 8.12; fuel from physics)" % LIFE_YR)
print("=" * 68)
print("  O&M (fixed+var+decom, FER-calibrated) %.1f | fuel %.1f  [$/MWh]"
      % (OANDM_PER_MWH, fuel_per_MWh))
for name, occ in OCC.items():
    print("  %-8s OCC $%d/kWe :  LCOE %.1f $/MWh (7%%)" % (name, occ, lcoe(occ, 0.07)))

# ---- CSVs ----
with open(os.path.join(OUT, "fuel_cycle_cost.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["component", "usd_per_kgHM", "usd_M_per_yr"])
    w.writerow(["natural_U_plus_conversion", "%.0f" % (cost_u + cost_conv), "%.2f" % ((cost_u + cost_conv) * HM_PER_YR / 1e6)])
    w.writerow(["enrichment", "%.0f" % cost_enr, "%.2f" % (cost_enr * HM_PER_YR / 1e6)])
    w.writerow(["fabrication", "%.0f" % cost_fab, "%.2f" % (cost_fab * HM_PER_YR / 1e6)])
    w.writerow(["front_end_total", "%.0f" % front_per_kgHM, "%.2f" % (front_per_yr / 1e6)])

with open(os.path.join(OUT, "lcoe_sensitivity.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["OCC_usd_per_kWe", "r_3pct", "r_7pct", "r_10pct"])
    for name, occ in OCC.items():
        w.writerow(["%s_%d" % (name, occ)] + ["%.1f" % lcoe(occ, r) for r in (0.03, 0.07, 0.10)])

print("\nwrote fuel_cycle_cost.csv + lcoe_sensitivity.csv")
