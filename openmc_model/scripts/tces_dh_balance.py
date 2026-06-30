"""Aegis-40 — TCES-for-district-heating energy/mass balance (FER §8.9).

Cogeneration concept
--------------------
Single tandem-compound turbine (one shaft, one generator) makes electricity.
A THERMOCHEMICAL energy store (TCES) is charged from turbine-extraction steam
through an INTERMEDIATE HEAT EXCHANGER (IHX) — so the store sits OUTSIDE the
nuclear island as a non-safety auxiliary, with no chemical/water-quality path
back into the reactor steam cycle (per the isolation-loop rule). On discharge the
store's reaction heat is delivered to a separate DISTRICT-HEATING (DH) water loop.
Off-peak electricity also drives a PEM electrolyser for H2 co-production.

The store is the load-shifter for HEAT: charge when DH demand is low (summer /
off-peak), discharge to the DH network when demand is high (winter / peak).
Because energy is held as chemical potential, storage is loss-free (seasonal-
capable) — the key advantage over hot-water tanks.

This script compares TWO candidate stores for the SAME duty:
  * AMMINE resorption  NiCl2-SrCl2/NH3   (Yan et al., Appl. Therm. Eng. 167, 2020)
  * ZEOLITE 13X / water adsorption        (Dahlberg DH study; review data)

Steam-side enthalpies via IAPWS-IF97 (consistent with thermo_cycle.py).
Outputs (docs/competition/cycle/):
  tces_dh_balance.csv        stream / sizing table
  tces_store_comparison.png  ammine vs zeolite mass+volume bar chart
Run:  py scripts/tces_dh_balance.py
"""
import os, csv
import numpy as np
from iapws import IAPWS97

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "docs", "competition", "cycle")
os.makedirs(OUT, exist_ok=True)
K = 273.15

# ============================================================ design inputs
Q_TH        = 125.0          # MWth core / secondary heat
P_BOIL, T_BOIL = 4.5, 296.0  # turbine inlet (thermo_cycle.py)
P_COND      = 0.007          # condenser
ETA_T       = 0.85           # turbine isentropic eff
ETA_GEN     = 0.985

# --- district-heating network ------------------------------------------------
T_DH_SUP, T_DH_RET = 90.0, 45.0     # C, 4th-gen low-temp DH (Turkish site)
Q_DH_PEAK   = 25.0           # MWth delivered to the network at design peak
STORE_HOURS = 8.0            # h of peak the store must cover by itself (daily block)

# --- charge side: HP extraction steam drives the IHX -------------------------
P_CHG       = 1.0            # MPa extraction (Tsat 180 C) -> charge loop via IHX
IHX_PINCH   = 12.0           # C, intermediate-HX approach (charge loop is 12 C colder)

# --- store round-trip (heat-in -> DH-heat-out), incl. IHX + DH-HX losses -----
# ammine resorption COPh~0.97 (Yan direct mode); zeolite adsorption COP~0.85
RT_AMMINE   = 0.88
RT_ZEOLITE  = 0.78

# --- store material data (system-level, charge/discharge-cycle basis) ---------
# AMMINE: Yan 2020 Table 2 + Fig (direct mode, X=0.85, mu=8): per 0.1 kmol NH3,
#   Q_out = 1692.84 kJ/kg_PRS * 5.795 kg_PRS = 9.81 MJ; salts = 5.795(PRS)+4.211(SRS)
AMMINE = dict(name="NiCl2-SrCl2/NH3 ammine",
              wh_per_kg=0.272,     # kWh per kg of salts (PRS+SRS), Yan direct mode
              bulk_kgm3=1000.0,    # packed reactive-salt/expanded-graphite bed
              t_discharge=150.0,   # C, adsorption heat-release (>=DH supply, margin)
              ref="Yan et al., Appl. Therm. Eng. 167 (2020) 114800")
ZEOLITE = dict(name="Zeolite-13X / H2O",
               wh_per_kg=0.20,     # kWh/kg zeolite (uptake ~0.22, dH~3500 kJ/kg-H2O)
               bulk_kgm3=650.0,    # packed bed
               t_discharge=130.0,  # C, adsorption front
               ref="Dahlberg et al. (zeolite DH); Banaei 2021 review")

# --- hydrogen co-production (charge/summer mode surplus power) ---------------
EL_KWH_PER_KG = 50.0         # PEM electrolyser, ~66% LHV efficiency
EL_POWER_MWE  = 8.0          # electrolyser block rating

# ============================================================ steam-side calc
def expand(h, s, p, eta):
    iso = IAPWS97(P=p, s=s); return h - eta * (h - iso.h)

s1 = IAPWS97(P=P_BOIL, T=T_BOIL + K)
h_ext = expand(s1.h, s1.s, P_CHG, ETA_T)                 # extraction enthalpy
st_ext = IAPWS97(P=P_CHG, h=h_ext)
h_drain = IAPWS97(P=P_CHG, x=0).h                        # IHX drains to sat-liq (180 C)
h_cond  = expand(st_ext.h, st_ext.s, P_COND, ETA_T)      # if it had kept expanding
# charge heat available per kg of extracted steam (steam -> sat liquid in IHX):
q_chg_perkg = h_ext - h_drain                            # kJ/kg
# electricity given up per kg of extracted steam (work not made downstream):
w_lost_perkg = (st_ext.h - h_cond) * ETA_GEN            # kJ/kg ~ MWe penalty basis
z_factor = w_lost_perkg / q_chg_perkg                    # MWe lost per MWth charged
t_chg_loop = IAPWS97(P=P_CHG, x=0).T - K - IHX_PINCH     # charge-loop temp to store

# ============================================================ store sizing
E_STORE = Q_DH_PEAK * STORE_HOURS            # MWh_th delivered per discharge block
def size(mat, rt):
    e_charge = E_STORE / rt                  # MWh_th heat that must be charged in
    mass_t = E_STORE * 1e3 / mat["wh_per_kg"] / 1e3     # tonnes (delivered basis)
    vol_m3 = mass_t * 1e3 / mat["bulk_kgm3"]
    return dict(e_charge=e_charge, mass_t=mass_t, vol_m3=vol_m3,
                footprint=vol_m3 / 6.0)      # m2 at 6 m bed height

A = size(AMMINE, RT_AMMINE); Z = size(ZEOLITE, RT_ZEOLITE)

# charge steam flow + cogeneration penalty (to charge the daily block in ~16 off-peak h)
CHG_HOURS = 16.0
chg_power_A = A["e_charge"] / CHG_HOURS       # MWth charge rate (ammine)
chg_power_Z = Z["e_charge"] / CHG_HOURS
m_chg_A = chg_power_A * 1e3 / q_chg_perkg     # kg/s extraction steam (ammine)
mwe_pen_A = chg_power_A * z_factor            # MWe given up while charging (ammine)
mwe_pen_Z = (Z["e_charge"] / CHG_HOURS) * z_factor

# DH water-loop flow at the design peak (delivered by discharge)
m_dh = Q_DH_PEAK * 1e3 / (4.186 * (T_DH_SUP - T_DH_RET))   # kg/s (cp water ~4.186)

# ============================================================ hydrogen
h2_kg_h = EL_POWER_MWE * 1e3 / EL_KWH_PER_KG
h2_nm3_h = h2_kg_h / 0.08988                  # Nm3/h (H2 density 0.08988 kg/Nm3)

# ============================================================ report
def p(*a): print(*a)
p("\n==================  AEGIS-40  TCES-for-DISTRICT-HEAT  BALANCE  ==================")
p(f"  District-heat network : {T_DH_SUP:.0f}/{T_DH_RET:.0f} C   peak {Q_DH_PEAK:.0f} MWth"
  f"   ->  DH water {m_dh:.1f} kg/s")
p(f"  Store duty            : {STORE_HOURS:.0f} h peak block  =>  {E_STORE:.0f} MWh_th delivered\n")

p("  ---- CHARGE path (HP extraction {:.1f} MPa -> IHX -> store) -------------------".format(P_CHG))
p(f"    extraction steam      : {st_ext.T-K:6.1f} C   h={st_ext.h:7.1f} kJ/kg   x={st_ext.x:.3f}")
p(f"    charge-loop temp (IHX): {t_chg_loop:6.1f} C   (>= store desorption need)")
p(f"    charge heat / kg steam: {q_chg_perkg:6.1f} kJ/kg")
p(f"    elec. penalty z-factor: {z_factor:6.3f} MWe lost per MWth charged\n")

p("  ---- STORE comparison (same {:.0f} MWh_th delivered) --------------------------".format(E_STORE))
p(f"    {'':22s}{'AMMINE':>16s}{'ZEOLITE':>16s}")
p(f"    {'round-trip eff.':22s}{RT_AMMINE:>16.2f}{RT_ZEOLITE:>16.2f}")
p(f"    {'energy dens (kWh/kg)':22s}{AMMINE['wh_per_kg']:>16.2f}{ZEOLITE['wh_per_kg']:>16.2f}")
p(f"    {'discharge temp (C)':22s}{AMMINE['t_discharge']:>16.0f}{ZEOLITE['t_discharge']:>16.0f}")
p(f"    {'store mass (t)':22s}{A['mass_t']:>16.0f}{Z['mass_t']:>16.0f}")
p(f"    {'store volume (m3)':22s}{A['vol_m3']:>16.0f}{Z['vol_m3']:>16.0f}")
p(f"    {'footprint @6m (m2)':22s}{A['footprint']:>16.0f}{Z['footprint']:>16.0f}")
p(f"    {'heat to charge (MWh)':22s}{A['e_charge']:>16.0f}{Z['e_charge']:>16.0f}")
p(f"    {'charge penalty (MWe)':22s}{mwe_pen_A:>16.2f}{mwe_pen_Z:>16.2f}")
p(f"    {'charge steam (kg/s)':22s}{m_chg_A:>16.2f}{Z['e_charge']/CHG_HOURS*1e3/q_chg_perkg:>16.2f}")

p("\n  ---- HYDROGEN co-production (off-peak surplus) ------------------------------")
p(f"    electrolyser          : {EL_POWER_MWE:.0f} MWe @ {EL_KWH_PER_KG:.0f} kWh/kg")
p(f"    H2 output             : {h2_kg_h:.0f} kg/h   ({h2_nm3_h:.0f} Nm3/h)")
p(f"    H2 (annual, 4000 h)   : {h2_kg_h*4000/1e3:.0f} t/yr")
p("\n  Ammine is ~{:.1f}x more compact (volume) than zeolite for the same store."
  .format(Z['vol_m3'] / A['vol_m3']))
p("================================================================================\n")

# ---- CSV --------------------------------------------------------------------
with open(os.path.join(OUT, "tces_dh_balance.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "ammine", "zeolite", "unit"])
    w.writerow(["round_trip_eff", RT_AMMINE, RT_ZEOLITE, "-"])
    w.writerow(["energy_density", AMMINE["wh_per_kg"], ZEOLITE["wh_per_kg"], "kWh/kg"])
    w.writerow(["discharge_temp", AMMINE["t_discharge"], ZEOLITE["t_discharge"], "C"])
    w.writerow(["store_mass", round(A["mass_t"]), round(Z["mass_t"]), "t"])
    w.writerow(["store_volume", round(A["vol_m3"]), round(Z["vol_m3"]), "m3"])
    w.writerow(["heat_to_charge", round(A["e_charge"]), round(Z["e_charge"]), "MWh_th"])
    w.writerow(["charge_penalty", round(mwe_pen_A, 2), round(mwe_pen_Z, 2), "MWe"])
    w.writerow(["store_delivered", E_STORE, E_STORE, "MWh_th"])
    w.writerow(["dh_peak", Q_DH_PEAK, Q_DH_PEAK, "MWth"])
    w.writerow(["h2_rate", round(h2_kg_h), round(h2_kg_h), "kg/h"])

# ---- comparison figure ------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
labels = ["ammine\nNiCl₂-SrCl₂/NH₃", "zeolite-13X\n/ H₂O"]
cols = ["#b5462e", "#2471a3"]
a1.bar(labels, [A["mass_t"], Z["mass_t"]], color=cols)
a1.set_ylabel("store mass  [t]"); a1.set_title("Store mass for %.0f MWh_th DH block" % E_STORE)
for i, v in enumerate([A["mass_t"], Z["mass_t"]]):
    a1.text(i, v, f"{v:.0f} t", ha="center", va="bottom", fontsize=9)
a2.bar(labels, [A["vol_m3"], Z["vol_m3"]], color=cols)
a2.set_ylabel("store volume  [m³]"); a2.set_title("Store volume (bulk packed bed)")
for i, v in enumerate([A["vol_m3"], Z["vol_m3"]]):
    a2.text(i, v, f"{v:.0f} m³", ha="center", va="bottom", fontsize=9)
for ax in (a1, a2): ax.grid(axis="y", alpha=0.3)
fig.suptitle("Aegis-40 district-heat thermochemical store — ammine vs zeolite "
             f"({T_DH_SUP:.0f}/{T_DH_RET:.0f} °C network, {Q_DH_PEAK:.0f} MWth peak)",
             fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "tces_store_comparison.png"), dpi=150)
print("wrote", os.path.join(OUT, "tces_dh_balance.csv"))
print("wrote", os.path.join(OUT, "tces_store_comparison.png"))
