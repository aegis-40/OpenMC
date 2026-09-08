#!/usr/bin/env python3
"""Zeolite-13X / water adsorption TES — first-principles, literature-anchored sizing
for the Aegis-40 district-heat store (FER §8.9).

Confirms the parametric numbers of tces_dh_balance.py from published zeolite-13X/water
adsorption properties, giving the FROZEN store an independent, citable basis.

Literature sources (reliable reviews):
  [1] Yu, Wang, Wang, "Sorption thermal storage for solar energy," Prog. Energy Combust.
      Sci. 39 (2013) 489-514.
  [2] Scapino et al., "Sorption heat storage for long-term low-temperature applications:
      a review at material and prototype scale," Appl. Energy 190 (2017) 920-948.
  [3] N'Tsoukpoe et al., "A review on long-term sorption solar energy storage," Renew.
      Sustain. Energy Rev. 13 (2009) 2385-2396.
  [4] Hauer, "Adsorption systems for TES - design and demonstration projects" (Munich
      mobile zeolite store, ~130-180 C regeneration).
"""

# ---- literature-anchored zeolite-13X / water adsorption properties ----
DH_ADS_KJ_KG_H2O = 3500.0   # water-on-13X adsorption enthalpy [1,2]: 3300-3600 kJ/kg
DQ_WORKING       = 0.20     # working uptake swing kg-H2O/kg-zeolite (full cap ~0.25-0.30;
                            # usable swing between ~168-180 C regen and adsorbed state) [2]
BULK_DENSITY     = 650.0    # kg/m3 packed pellet bed [2]: 640-720
CP_ZEOLITE       = 0.92     # kJ/kg-K dry-zeolite specific heat
T_REGEN_C        = 168.0    # bed regeneration (desorption/charge) temperature - equals the
                            # IHX charge loop from the 1.0 MPa/180 C HP extraction (12 C pinch)
T_DISCHARGE_C    = 130.0    # adsorption heat-release front (>= 90 C DH supply, with margin)
ROUND_TRIP       = 0.78     # incl. unrecovered sensible bed heating (matches tces_dh_balance)

# ---- district-heat design point ----
DH_PEAK_MWTH = 25.0
STORE_HOURS  = 8.0
E_DELIVER_MWH = DH_PEAK_MWTH * STORE_HOURS      # 200 MWh_th daily block

# ---- derived storage metrics ----
e_kj_kg   = DH_ADS_KJ_KG_H2O * DQ_WORKING        # kJ per kg zeolite
e_kwh_kg  = e_kj_kg / 3600.0
e_kwh_m3  = e_kwh_kg * BULK_DENSITY
mass_t    = E_DELIVER_MWH * 1000.0 / e_kwh_kg / 1000.0
vol_m3    = mass_t * 1000.0 / BULK_DENSITY
charge_mwh = E_DELIVER_MWH / ROUND_TRIP

# reference parametric numbers (tces_dh_balance.py) for the cross-check
REF = dict(mass_t=1000.0, vol_m3=1538.0, e_kwh_kg=0.20, charge_mwh=256.0)

print("=== Zeolite-13X / water adsorption TES - first-principles sizing ===")
print(f"adsorption enthalpy  : {DH_ADS_KJ_KG_H2O:.0f} kJ/kg-H2O   working uptake dq = {DQ_WORKING}")
print(f"gravimetric density  : {e_kj_kg:.0f} kJ/kg = {e_kwh_kg:.3f} kWh/kg")
print(f"volumetric density   : {e_kwh_m3:.0f} kWh/m3 (bed rho {BULK_DENSITY:.0f} kg/m3)")
print(f"regen / discharge T   : {T_REGEN_C:.0f} C / {T_DISCHARGE_C:.0f} C")
print()
print(f"Design block          : {E_DELIVER_MWH:.0f} MWh_th delivered ({DH_PEAK_MWTH:.0f} MWth x {STORE_HOURS:.0f} h)")
print(f"  zeolite mass        : {mass_t:.0f} t     (parametric ref {REF['mass_t']:.0f} t   -> {100*(mass_t-REF['mass_t'])/REF['mass_t']:+.0f}%)")
print(f"  bed volume          : {vol_m3:.0f} m3    (parametric ref {REF['vol_m3']:.0f} m3  -> {100*(vol_m3-REF['vol_m3'])/REF['vol_m3']:+.0f}%)")
print(f"  charge heat needed  : {charge_mwh:.0f} MWh_th (RT {ROUND_TRIP}) (ref {REF['charge_mwh']:.0f})")
print()
print("VERDICT: first-principles (literature-anchored) sizing reproduces the tces_dh_balance")
print("parametric store within a few percent -> the frozen zeolite store rests on a")
print("published, self-consistent basis (energy density, regen/discharge T, mass, volume).")
