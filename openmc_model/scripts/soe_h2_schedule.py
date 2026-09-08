"""Aegis-40 cogeneration — SOE hydrogen + TCES district-heat seasonal schedule
and first-order economics for Sinop. Backs the FER §8.9 cogeneration report.

Sources:
- Steam cycle state points: docs/competition/cycle/cycle_state_points.csv (thermo_cycle.py)
- SOE energy demand: Milewski, Kupecki et al., Int. J. Hydrogen Energy 46 (2021)
  35765-35776 -> 37.55 kWh/kg (O2- SOE) vs 50 kWh/kg (PEM); steam fed from deaerator.
"""

# ---------------- plant baseline ----------------
P_NET_MWE      = 40.0          # net electric (power path always on)
MAIN_STEAM_KGS = 57.8         # OTSG main steam (state 1)

# ---------------- TCES district heat ----------------
DH_PEAK_MWTH   = 25.0          # store discharge to DH network (90/45 C)
CHARGE_MWE_PER_MWTH = 0.31     # electric penalty to charge (extraction steam off the turbine)

# ---------------- SOE hydrogen (replaces PEM) ----------------
SOE_KWH_PER_KG = 37.55         # O2- SOE electrical demand (Milewski 2021)
PEM_KWH_PER_KG = 50.0          # old PEM baseline (for comparison)
H2_ELEC_MWE    = 8.0           # off-peak electricity budget to electrolysis
H2O_PER_H2     = 9.0           # kg steam per kg H2 (stoichiometric)

def h2_rate(mwe, kwh_kg):
    return mwe * 1000.0 / kwh_kg          # kg/h

soe_kg_h = h2_rate(H2_ELEC_MWE, SOE_KWH_PER_KG)
pem_kg_h = h2_rate(H2_ELEC_MWE, PEM_KWH_PER_KG)
soe_steam_kgs = soe_kg_h * H2O_PER_H2 / 3600.0       # steam slipstream
steam_frac = soe_steam_kgs / MAIN_STEAM_KGS * 100.0

print("=== SOE vs PEM hydrogen (same 8 MWe off-peak budget) ===")
print(f"  SOE  {SOE_KWH_PER_KG} kWh/kg -> {soe_kg_h:6.1f} kg/h H2")
print(f"  PEM  {PEM_KWH_PER_KG} kWh/kg -> {pem_kg_h:6.1f} kg/h H2  (+{(soe_kg_h/pem_kg_h-1)*100:.0f}% more H2 with SOE)")
print(f"  SOE steam slipstream = {soe_steam_kgs:.2f} kg/s = {steam_frac:.2f}% of main steam (deaerator bleed, ~0.15 MPa)")

# ---------------- Sinop seasons (Black Sea coast; heating season ~Oct-Apr) ----------------
# Heating degree-day split: DH needed Oct-Apr (~212 d), not needed May-Sep (~153 d).
HEATING_DAYS    = 212
NONHEATING_DAYS = 153
# off-peak hours/day available for charge + H2 (night valley)
OFFPEAK_H_DAY   = 8            # TCES charging window
# SOE hydrogen: only the DEEPEST valley (~02:00-06:00), non-heating season only,
# net of outage/low-demand nights (DECIDED 2026-07-02: modest schedule -> ~120 t/yr)
SOE_H_NIGHT     = 4
SOE_NIGHTS      = 140

print("\n=== Seasonal operating schedule (Sinop) ===")
modes = [
 ("Winter (Dec-Feb)",  "DISCHARGE TCES -> DH 25 MWth; H2 reduced; 40 MWe to grid (peak)"),
 ("Shoulder (Oct,Nov,Mar,Apr)", "Partial DH from store; H2 at night; charge as needed"),
 ("Summer (May-Sep)",  "No DH -> charge store + MAX H2 (surplus night electricity)"),
]
for s, m in modes:
    print(f"  {s:30s}: {m}")

# ---------------- annual yields ----------------
# H2: runs off-peak year-round; winter reduced (electricity prioritised to grid+DH)
h2_hours = SOE_NIGHTS * SOE_H_NIGHT
h2_tyr   = soe_kg_h * h2_hours / 1000.0
# DH: store delivers DH over heating season, avg ~50% of peak
dh_avg_mwth = DH_PEAK_MWTH*0.5
dh_mwhth_yr = dh_avg_mwth * HEATING_DAYS*24
print("\n=== Annual yields ===")
print(f"  H2 (SOE):  {h2_tyr:5.0f} t/yr  over {h2_hours:.0f} electrolysis-hours")
print(f"  DH heat:   {dh_mwhth_yr/1000:5.1f} GWh-th/yr  (avg {dh_avg_mwth} MWth over heating season)")
print(f"  Electricity: {P_NET_MWE} MWe baseload (TCES keeps full 40 MWe during winter peaks)")

# ---------------- first-order economics (Turkey/Sinop, indicative) ----------------
PR_ELEC_PEAK, PR_ELEC_OFF = 100.0, 40.0     # $/MWh
PR_H2, PR_DH = 5.0, 40.0                     # $/kg ; $/MWh-th
elec_rev   = P_NET_MWE*8000*((PR_ELEC_PEAK+PR_ELEC_OFF)/2)/1e6
h2_rev     = h2_tyr*1000*PR_H2/1e6
h2_eleccost= H2_ELEC_MWE*h2_hours*PR_ELEC_OFF/1e6
dh_rev     = dh_mwhth_yr*PR_DH/1e6
print("\n=== First-order economics (indicative $/yr) ===")
print(f"  Electricity revenue : ${elec_rev:5.1f} M")
print(f"  H2 revenue          : ${h2_rev:5.1f} M  (electrolysis elec cost ${h2_eleccost:.1f} M -> margin ${h2_rev-h2_eleccost:.1f} M)")
print(f"  District-heat revenue: ${dh_rev:5.1f} M")
print(f"  Cogen uplift over electricity-only: ${(h2_rev-h2_eleccost)+dh_rev:.1f} M/yr (+{((h2_rev-h2_eleccost)+dh_rev)/elec_rev*100:.0f}%)")
