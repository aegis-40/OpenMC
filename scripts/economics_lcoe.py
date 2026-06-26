"""Aegis-40 — levelised cost of electricity (LCOE) + fuel-cycle cost (LFCC).

First-cut techno-economics for FER §8.12, following the OECD-NEA (1994) / ORION
levelised-cost methodology (Ashley et al. 2014): a discounted constant-annuity
LCOE with a triangular CAPEX uncertainty (low / mid / high), broken into capital,
fixed-O&M, variable-O&M and fuel components. Numbers are FOAK-SMR Tier-B inputs
(⚠CONFIRM) chosen from the open SMR literature and scaled to a 40 MWe unit.

    LCOE = [ OCC*CRF + FixedOM ] / (8760*CF) + VarOM + Fuel        [$/MWh]
    CRF  = r(1+r)^N / ((1+r)^N - 1)        (capital recovery factor)

Outputs (docs/competition/economics/):
  lcoe_breakdown.csv     component $/MWh for low/mid/high CAPEX
  lcoe_summary.md        Markdown table for the FER (Table 8.12-x)

Run:  py scripts/economics_lcoe.py
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "competition", "economics")
os.makedirs(OUT, exist_ok=True)

# ---- plant / financial inputs (Tier-B, CONFIRM) -----------------------------
P_NET_MWE = 40.0           # net electric capacity
CF = 0.90                  # capacity factor (baseload SMR)
LIFE_YR = 60               # economic life
R = 0.07                   # real discount rate / WACC
CONSTR_YR = 4              # construction duration (for IDC)

# Overnight capital cost ($/kWe) — triangular (FOAK SMR; small-unit premium)
OCC_LOW, OCC_MID, OCC_HIGH = 5000.0, 7200.0, 10500.0
# Fixed O&M ($/kWe-yr) and variable O&M ($/MWh)
FOM = 130.0
VOM = 3.0
# Fuel / fuel-cycle cost ($/MWh) — levelised fuel-cycle cost (see LFCC note)
FUEL = 7.5
# Decommissioning sinking fund ($/kWe, levelised into FOM-equivalent)
DECOM = 700.0

HOURS = 8760.0


def crf(r, n):
    return r * (1 + r) ** n / ((1 + r) ** n - 1)


def idc_factor(r, years):
    """Interest-during-construction multiplier on OCC (uniform spend)."""
    # midpoint-of-construction compounding, simple approximation
    return (1 + r) ** (years / 2.0)


CRF = crf(R, LIFE_YR)
IDC = idc_factor(R, CONSTR_YR)
gen_MWh = P_NET_MWE * HOURS * CF                      # annual generation, MWh

# decommissioning levelised as an annuity over life, expressed $/MWh
decom_annuity = DECOM * P_NET_MWE * 1e3 * crf(R, LIFE_YR)   # $/yr (fund recovery)
decom_per_MWh = decom_annuity / (gen_MWh)

rows = []
for tag, occ in (("low", OCC_LOW), ("mid", OCC_MID), ("high", OCC_HIGH)):
    capex = occ * IDC                                # $/kWe incl. IDC
    cap_per_MWh = (capex * P_NET_MWE * 1e3 * CRF) / gen_MWh
    fom_per_MWh = (FOM * P_NET_MWE * 1e3) / gen_MWh
    lcoe = cap_per_MWh + fom_per_MWh + VOM + FUEL + decom_per_MWh
    rows.append((tag, occ, cap_per_MWh, fom_per_MWh, VOM, FUEL,
                 decom_per_MWh, lcoe))

# ---- report -----------------------------------------------------------------
print("\n=============  AEGIS-40 LCOE  (40 MWe, CF=%.2f, r=%.0f%%, N=%d yr)  ============="
      % (CF, R * 100, LIFE_YR))
print("  CRF = %.4f ;  IDC factor = %.3f ;  annual generation = %.0f MWh"
      % (CRF, IDC, gen_MWh))
print("\n  %-6s %9s %9s %8s %7s %7s %8s %9s" %
      ("CAPEX", "OCC$/kW", "capital", "fixOM", "varOM", "fuel", "decom", "LCOE"))
print("  %-6s %9s %9s %8s %7s %7s %8s %9s" %
      ("scen.", "", "$/MWh", "$/MWh", "$/MWh", "$/MWh", "$/MWh", "$/MWh"))
for tag, occ, cap, fom, vom, fuel, dec, lcoe in rows:
    print("  %-6s %9.0f %9.1f %8.1f %7.1f %7.1f %8.1f %9.1f" %
          (tag, occ, cap, fom, vom, fuel, dec, lcoe))
mid = rows[1]
print("\n  Mid LCOE = %.0f $/MWh  (capital %.0f%% of total)"
      % (mid[7], 100 * mid[2] / mid[7]))
print("===================================================================\n")

# ---- CSV --------------------------------------------------------------------
with open(os.path.join(OUT, "lcoe_breakdown.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["scenario", "OCC_usd_per_kWe", "capital_usd_per_MWh",
                "fixedOM_usd_per_MWh", "varOM_usd_per_MWh", "fuel_usd_per_MWh",
                "decom_usd_per_MWh", "LCOE_usd_per_MWh"])
    for r_ in rows:
        w.writerow(["%s" % r_[0]] + ["%.1f" % x for x in r_[1:]])

# ---- Markdown ---------------------------------------------------------------
with open(os.path.join(OUT, "lcoe_summary.md"), "w", encoding="utf-8") as f:
    f.write("# Aegis-40 LCOE breakdown (FER §8.12)\n\n")
    f.write("40 MWe net, CF = %.2f, real discount rate r = %.0f %%, life N = %d yr; "
            "CRF = %.4f, IDC factor = %.3f. Computed by "
            "`scripts/economics_lcoe.py`. Inputs are FOAK-SMR Tier-B (⚠CONFIRM).\n\n"
            % (CF, R * 100, LIFE_YR, CRF, IDC))
    f.write("| CAPEX scenario | OCC ($/kWe) | Capital | Fixed O&M | Var O&M | "
            "Fuel | Decom. | **LCOE ($/MWh)** |\n")
    f.write("|---|---:|---:|---:|---:|---:|---:|---:|\n")
    for tag, occ, cap, fom, vom, fuel, dec, lcoe in rows:
        f.write("| %s | %.0f | %.1f | %.1f | %.1f | %.1f | %.1f | **%.1f** |\n"
                % (tag, occ, cap, fom, vom, fuel, dec, lcoe))
    f.write("\n- **Mid-case LCOE ≈ %.0f $/MWh**; capital is %.0f %% of the total — "
            "the dominant lever, as expected for a capital-intensive SMR.\n"
            % (mid[7], 100 * mid[2] / mid[7]))

print("wrote", os.path.join(OUT, "lcoe_breakdown.csv"))
print("wrote", os.path.join(OUT, "lcoe_summary.md"))
