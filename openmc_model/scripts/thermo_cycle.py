"""Aegis-40 secondary Rankine cycle — design-point heat balance and T-s diagram.

Regenerative superheated Rankine cycle for the integral helical-coil OTSG secondary
side. Design point: 125 MWth heat input -> 40 MWe net (32.0 % net), matching the
locked design basis. Two open feedwater heaters (LP deaerator + HP heater) raise the
mean temperature of heat addition to reach the target efficiency with realistic iPWR
steam conditions (superheated OTSG steam, vacuum condenser).

Constraints / assumptions (Tier-B, CONFIRM with TH lead):
  * Primary: 12.8 MPa, 265 -> 305 C (assumed pending Adilbek's TH).  Secondary
    superheated steam temperature is held >=10 C below the 305 C hot leg (OTSG
    superheater approach), so steam conditions below are primary-side-feasible.
  * No primary coolant pumps (natural circulation) -> no pump heat added to primary.
  * Condenser cooled by mechanical-draft cooling tower (vacuum back-pressure).

Steam properties: IAPWS-IF97 via the `iapws` package (P in MPa, T in K, h/s in kJ).
Outputs (docs/competition/cycle/):
  cycle_state_points.csv   numbered state-point table
  cycle_Ts_diagram.png     T-s diagram with the saturation dome + cycle path
  (a performance summary is printed to stdout)

Run:  py scripts/thermo_cycle.py
"""

import csv
import os
import numpy as np
from iapws import IAPWS97

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "competition", "cycle")
os.makedirs(OUT, exist_ok=True)

# ---- design inputs ----------------------------------------------------------
Q_TH = 125.0e6             # W, secondary heat input (= core thermal power)
# Primary side from the §8.4 natural-circulation analysis (natcirc_primary.py):
T_PRIM_HOT = 308.0         # C, primary hot leg (OTSG superheater hot end)
T_PRIM_COLD = 258.0        # C, primary cold leg (OTSG economizer cold end)

# Steam conditions re-coupled to the 308/258 legs (thermo_cycle_recouple.py):
P_BOIL = 4.5               # MPa, turbine-inlet steam pressure (8.8 C OTSG pinch)
T_BOIL = 296.0             # C,  turbine-inlet temperature (12 C below 308 C hot leg)
P_COND = 0.007             # MPa, condenser pressure (Tsat ~ 39 C, cooling tower)
P_EXT1 = 1.00              # MPa, HP extraction -> open FWH 1
P_EXT2 = 0.15              # MPa, LP extraction -> open FWH 2 (deaerator)

ETA_T = 0.85               # turbine isentropic efficiency (wet-steam SMR turbine)
ETA_P = 0.82               # pump isentropic efficiency
ETA_GEN = 0.985            # generator x mechanical
ETA_MOT = 0.95             # feed/condensate pump motor
F_BOP = 0.050              # balance-of-plant house load (cooling-tower fans,
                           # circ-water + condensate pumps, misc), frac. of gross

KELVIN = 273.15


# ---- component models -------------------------------------------------------
def expand(h_in, s_in, p_out, eta):
    """Adiabatic turbine stage: isentropic to p_out, then apply efficiency."""
    iso = IAPWS97(P=p_out, s=s_in)
    h_out = h_in - eta * (h_in - iso.h)
    st = IAPWS97(P=p_out, h=h_out)
    return st


def pump(h_in, p_in, p_out, eta):
    """Incompressible pump on saturated liquid; returns (h_out, work[kJ/kg])."""
    v = IAPWS97(P=p_in, x=0).v                  # m3/kg
    w = v * (p_out - p_in) * 1.0e3 / eta        # MPa*1e3 = kPa; kPa*m3/kg = kJ/kg
    return h_in + w, w


# ---- state points -----------------------------------------------------------
# 1: turbine inlet (OTSG superheated steam)
s1 = IAPWS97(P=P_BOIL, T=T_BOIL + KELVIN)
# turbine expansion with two extractions
s2 = expand(s1.h, s1.s, P_EXT1, ETA_T)          # HP extraction
s3 = expand(s2.h, s2.s, P_EXT2, ETA_T)          # crossover / moisture-separator inlet
s3g = IAPWS97(P=P_EXT2, x=1)                     # MS vapor outlet (dried, sat. vapour)
s4 = expand(s3g.h, s3g.s, P_COND, ETA_T)        # LP exhaust -> condenser (now dry start)
# condensate / feedwater train
s5 = IAPWS97(P=P_COND, x=0)                      # condenser outlet (sat liquid)
h6, wp1 = pump(s5.h, P_COND, P_EXT2, ETA_P)     # condensate pump -> FWH2 pressure
s6 = IAPWS97(P=P_EXT2, h=h6)
s7 = IAPWS97(P=P_EXT2, x=0)                      # FWH2 (deaerator) outlet, sat liq
h8, wp2 = pump(s7.h, P_EXT2, P_EXT1, ETA_P)     # booster pump -> FWH1 pressure
s8 = IAPWS97(P=P_EXT1, h=h8)
s9 = IAPWS97(P=P_EXT1, x=0)                      # FWH1 outlet, sat liquid
h10, wp3 = pump(s9.h, P_EXT1, P_BOIL, ETA_P)    # feed pump -> boiler pressure
s10 = IAPWS97(P=P_BOIL, h=h10)

# ---- mass balances with a moisture separator at the crossover (P_EXT2) -------
# A moisture separator at P_EXT2 dries the crossover steam to saturated vapour
# before the final LP stage (limits last-stage moisture). The separated liquid
# (sat. liquid at P_EXT2) drains into the open deaerator at the same pressure.
x3 = s3.x                                        # quality at MS inlet
# FWH1 (open, P_EXT1): y1*h2 + (1-y1)*h8 = hf(P_EXT1)
y1 = (s9.h - s8.h) / (s2.h - s8.h)
# Deaerator (open, P_EXT2) fed by: wet bleed y2 (h3) + MS drain (1-y1-y2)(1-x3) at
# hf + condensate feed (1-y1-y2)*x3 at h6 -> out (1-y1) sat. liquid at hf(P_EXT2):
A = x3 * (s7.h - s6.h)
y2 = (1 - y1) * A / ((s3.h - s7.h) + A)
m_last = (1 - y1 - y2) * x3                      # dry-vapour flow through last LP stage

# ---- specific work / heat (per kg boiler steam) -----------------------------
w_turb = ((s1.h - s2.h)                          # full flow, 1 -> 2
          + (1 - y1) * (s2.h - s3.h)             # (1-y1), 2 -> 3 (crossover)
          + m_last * (s3g.h - s4.h))             # dry vapour, 3g -> 4 (final stage)
w_pump = m_last * wp1 + (1 - y1) * wp2 + 1.0 * wp3
q_in = s1.h - s10.h
w_net = w_turb - w_pump
eta_th = w_net / q_in

# ---- scale to 125 MWth ------------------------------------------------------
m_dot = Q_TH / (q_in * 1.0e3)                   # kg/s boiler steam
P_turb = m_dot * w_turb * 1.0e3                 # W (mechanical shaft)
P_pump = m_dot * w_pump * 1.0e3                 # W (feed/condensate pumps)
P_gross = P_turb * ETA_GEN                      # W gross at generator terminals
P_bop = F_BOP * P_gross                         # W balance-of-plant house load
P_elec = P_gross - P_pump / ETA_MOT - P_bop     # W net electric (sent-out)
eta_gross = P_gross / Q_TH
eta_net = P_elec / Q_TH
q_out = m_last * (s4.h - s5.h)                  # condenser rejects only last-stage flow
Q_rej = m_dot * q_out * 1.0e3

# ---- OTSG counterflow pinch check (primary vs secondary feasibility) ---------
# Primary heat-capacity rate from the core duty and primary leg temperatures.
mcp_prim = Q_TH / (T_PRIM_HOT - T_PRIM_COLD)    # W/K
Tsat_boil = IAPWS97(P=P_BOIL, x=1).T - KELVIN   # secondary saturation temperature
hf_boil = IAPWS97(P=P_BOIL, x=0).h              # sat-liquid enthalpy at boiler P
# Economizer duty (feedwater s10 -> sat liquid) sets how far the primary cools below
# the hot end before the secondary starts to boil -> primary T at start-of-boiling:
Q_econ = m_dot * (hf_boil - s10.h) * 1.0e3      # W
T_prim_boilstart = T_PRIM_COLD + Q_econ / mcp_prim
pinch = T_prim_boilstart - Tsat_boil            # evaporator-inlet pinch (deg C)
sh_approach = T_PRIM_HOT - T_BOIL               # superheater hot-end approach (deg C)


# ---- report -----------------------------------------------------------------
def line(*a):
    print(*a)


states = [
    ("1  Turbine inlet (OTSG steam)", P_BOIL, s1),
    ("2  HP extraction", P_EXT1, s2),
    ("3  Crossover / MS inlet", P_EXT2, s3),
    ("3g MS vapour outlet (dried)", P_EXT2, s3g),
    ("4  LP turbine exhaust", P_COND, s4),
    ("5  Condenser outlet (sat liq)", P_COND, s5),
    ("6  Condensate pump outlet", P_EXT2, s6),
    ("7  FWH-2 deaerator outlet", P_EXT2, s7),
    ("8  Booster pump outlet", P_EXT1, s8),
    ("9  FWH-1 outlet (sat liq)", P_EXT1, s9),
    ("10 Feed pump outlet -> OTSG", P_BOIL, s10),
]

line("\n================  AEGIS-40 SECONDARY RANKINE CYCLE  ================")
line("  Regenerative superheated cycle, 2 open FWHs + moisture separator  (Tier-B / CONFIRM)\n")
line("  %-30s %8s %8s %9s %8s %7s" %
     ("STATE", "P(MPa)", "T(C)", "h(kJ/kg)", "s(kJ/kgK)", "x"))
rows = []
for name, p, st in states:
    T_C = st.T - KELVIN
    x = st.x if 0 <= st.x <= 1 else float("nan")
    xs = "%.3f" % x if x == x else "  -"
    line("  %-30s %8.4f %8.1f %9.1f %8.4f %7s" % (name, p, T_C, st.h, st.s, xs))
    rows.append([name, "%.4f" % p, "%.1f" % T_C, "%.1f" % st.h, "%.4f" % st.s, xs])

line("\n  ---- extraction fractions ----")
line("    y1 (HP -> FWH1)         = %.4f" % y1)
line("    y2 (-> FWH2/deaerator)  = %.4f" % y2)
line("    last-stage (dry) flow   = %.4f" % m_last)
line("    LP exhaust quality x    = %.3f   (moisture %.1f %%)" %
     (s4.x, (1 - s4.x) * 100))

line("\n  ---- performance ----")
line("    q_in  (boiler)          = %8.1f kJ/kg" % q_in)
line("    w_turbine               = %8.1f kJ/kg" % w_turb)
line("    w_pumps                 = %8.2f kJ/kg" % w_pump)
line("    w_net                   = %8.1f kJ/kg" % w_net)
line("    cycle thermal eff.      = %8.2f %%" % (eta_th * 100))
line("    steam mass flow         = %8.2f kg/s" % m_dot)
line("    gross turbine (shaft)   = %8.2f MW" % (P_turb / 1e6))
line("    gross electric (gen.)   = %8.2f MWe  (eff %.2f %%)" %
     (P_gross / 1e6, eta_gross * 100))
line("    - feed/condensate pumps = %8.2f MWe" % (P_pump / ETA_MOT / 1e6))
line("    - BOP house load        = %8.2f MWe" % (P_bop / 1e6))
line("    NET electric (sent-out) = %8.2f MWe" % (P_elec / 1e6))
line("    NET plant efficiency    = %8.2f %%   (target 32.0)" % (eta_net * 100))
line("    heat rejected (cond.)   = %8.2f MWth" % (Q_rej / 1e6))
line("    condenser Tsat          = %8.1f C" % (IAPWS97(P=P_COND, x=0).T - KELVIN))

line("\n  ---- OTSG primary/secondary feasibility (primary %.0f -> %.0f C) ----"
     % (T_PRIM_HOT, T_PRIM_COLD))
line("    secondary Tsat          = %8.1f C" % Tsat_boil)
line("    superheater approach    = %8.1f C   (hot leg - steam, >0 ok)" % sh_approach)
line("    evaporator pinch dT     = %8.1f C   (target >= ~8 C)  %s" %
     (pinch, "OK" if pinch >= 8 else "TIGHT" if pinch > 0 else "VIOLATION"))
line("===================================================================\n")

# ---- state-point CSV --------------------------------------------------------
with open(os.path.join(OUT, "cycle_state_points.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "P_MPa", "T_C", "h_kJ_kg", "s_kJ_kgK", "x"])
    w.writerows(rows)

# ---- T-s diagram ------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8.0, 6.0))

# saturation dome
Ts = np.linspace(0.011, 22.0, 250)             # MPa up toward critical
sf, sg, Tf = [], [], []
for P in Ts:
    try:
        lf = IAPWS97(P=P, x=0)
        vg = IAPWS97(P=P, x=1)
        sf.append(lf.s); sg.append(vg.s); Tf.append(lf.T - KELVIN)
    except Exception:
        pass
ax.plot(sf, Tf, color="0.5", lw=1.2)
ax.plot(sg, Tf, color="0.5", lw=1.2, label="saturation dome")

# cycle path: expansion 1->2->3, moisture separation 3->3g, final stage 3g->4,
# condenser 4->5, feedwater train 5->7->9->10, then the OTSG heat addition along
# the boiler-pressure isobar (economizer -> evaporator -> superheater) back to 1
boil_f = IAPWS97(P=P_BOIL, x=0)                  # sat. liquid at boiler pressure
boil_g = IAPWS97(P=P_BOIL, x=1)                  # sat. vapour at boiler pressure
path = [s1, s2, s3, s3g, s4, s5, s7, s9, s10, boil_f, boil_g, s1]
sx = [st.s for st in path]
Tx = [st.T - KELVIN for st in path]
ax.plot(sx, Tx, "o-", color="#b5462e", lw=2.0, ms=5, label="cycle path")

for name, p, st in states:
    ax.annotate(name.split()[0], (st.s, st.T - KELVIN),
                textcoords="offset points", xytext=(5, 4), fontsize=8)

ax.set_xlabel("specific entropy  s  [kJ/kg·K]")
ax.set_ylabel("temperature  T  [°C]")
ax.set_title("Aegis-40 Secondary Rankine Cycle  —  T–s diagram\n"
             "125 MWth → %.1f MWe  (η_net = %.1f %%)" % (P_elec / 1e6, eta_net * 100))
ax.set_xlim(0, 8.5)
ax.set_ylim(0, 360)
ax.grid(alpha=0.3)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "cycle_Ts_diagram.png"), dpi=150)
print("wrote", os.path.join(OUT, "cycle_state_points.csv"))
print("wrote", os.path.join(OUT, "cycle_Ts_diagram.png"))
