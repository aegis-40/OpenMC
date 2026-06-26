"""Aegis-40 secondary cycle — exergy (2nd-law) analysis + labelled PFD figure.

Companion to thermo_cycle.py. Re-derives the SAME regenerative superheated Rankine
cycle (125 MWth -> ~40 MWe, IAPWS-IF97) and adds the two things a "simulation-grade"
heat-balance study needs (cf. Ogul et al. 2026, Cycle-Tempo SMART model, Fig. 2):

  1. A component-by-component EXERGY DESTRUCTION table (where the second-law losses
     live: OTSG finite-dT, turbine, condenser, pumps, feedwater heaters) and an
     overall exergetic (2nd-law) efficiency.
  2. A Cycle-Tempo-style LABELLED PFD — each node tagged with P, T, h, m_dot.

Dead state: T0 = 25 C, P0 = 0.101325 MPa (saturated/compressed liquid reference).
Heat-source exergy uses the primary-coolant log-mean temperature (308/258 C legs).

Outputs (docs/competition/cycle/):
  cycle_exergy.csv          per-component exergy destruction (kW, %)
  cycle_exergy_table.md     same as a Markdown table for the FER (Table 8.9-x)
  cycle_pfd_labeled.png     labelled process-flow diagram (state points P/T/h/mdot)

Run:  py scripts/thermo_exergy.py
"""

import csv
import os
import numpy as np
from iapws import IAPWS97

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "competition", "cycle")
os.makedirs(OUT, exist_ok=True)
KELVIN = 273.15

# ---- design inputs (identical to thermo_cycle.py) ---------------------------
Q_TH = 125.0e6
T_PRIM_HOT = 308.0
T_PRIM_COLD = 258.0
P_BOIL, T_BOIL = 4.5, 296.0
P_COND = 0.007
P_EXT1, P_EXT2 = 1.00, 0.15
ETA_T, ETA_P = 0.85, 0.82
ETA_GEN, ETA_MOT = 0.985, 0.95
F_BOP = 0.050

# ---- dead state -------------------------------------------------------------
T0 = 25.0 + KELVIN                       # K
P0 = 0.101325                            # MPa
dead = IAPWS97(P=P0, T=T0)
H0, S0 = dead.h, dead.s                  # kJ/kg, kJ/kg.K


def exergy(st):
    """Specific flow exergy  e = (h-h0) - T0(s-s0)   [kJ/kg]."""
    return (st.h - H0) - (T0 / 1.0) * (st.s - S0)


# ---- component models (same as thermo_cycle.py) -----------------------------
def expand(h_in, s_in, p_out, eta):
    iso = IAPWS97(P=p_out, s=s_in)
    h_out = h_in - eta * (h_in - iso.h)
    return IAPWS97(P=p_out, h=h_out)


def pump(h_in, p_in, p_out, eta):
    v = IAPWS97(P=p_in, x=0).v
    w = v * (p_out - p_in) * 1.0e3 / eta
    return h_in + w, w


# ---- state points -----------------------------------------------------------
s1 = IAPWS97(P=P_BOIL, T=T_BOIL + KELVIN)
s2 = expand(s1.h, s1.s, P_EXT1, ETA_T)
s3 = expand(s2.h, s2.s, P_EXT2, ETA_T)
s3g = IAPWS97(P=P_EXT2, x=1)
s4 = expand(s3g.h, s3g.s, P_COND, ETA_T)
s5 = IAPWS97(P=P_COND, x=0)
h6, wp1 = pump(s5.h, P_COND, P_EXT2, ETA_P)
s6 = IAPWS97(P=P_EXT2, h=h6)
s7 = IAPWS97(P=P_EXT2, x=0)
h8, wp2 = pump(s7.h, P_EXT2, P_EXT1, ETA_P)
s8 = IAPWS97(P=P_EXT1, h=h8)
s9 = IAPWS97(P=P_EXT1, x=0)
h10, wp3 = pump(s9.h, P_EXT1, P_BOIL, ETA_P)
s10 = IAPWS97(P=P_BOIL, h=h10)

# ---- mass balances ----------------------------------------------------------
x3 = s3.x
y1 = (s9.h - s8.h) / (s2.h - s8.h)
A = x3 * (s7.h - s6.h)
y2 = (1 - y1) * A / ((s3.h - s7.h) + A)
m_last = (1 - y1 - y2) * x3
m_drain = (1 - y1 - y2) * (1 - x3)        # moisture-separator liquid drain -> DA

q_in = s1.h - s10.h
m_dot = Q_TH / (q_in * 1.0e3)             # kg/s boiler steam (full flow = 1.0)

# absolute mass flows (kg/s)
M = m_dot                                  # full boiler flow
m_hp = M * y1                              # HP extraction -> FWH1
m_cross = M * (1 - y1)                     # crossover flow (2->3)
m_da = M * y2                              # wet bleed -> deaerator
m_ms = M * (1 - y1 - y2)                   # to moisture separator
m_lp = M * m_last                          # dry vapour, final stage / condenser
m_dr = M * m_drain                         # MS liquid drain -> deaerator
m_feed = M * (1 - y1)                      # deaerated feed (7->8->9 side)

# ---- shaft / electric (same accounting as thermo_cycle.py) ------------------
w_turb = (s1.h - s2.h) + (1 - y1) * (s2.h - s3.h) + m_last * (s3g.h - s4.h)
w_pump = m_last * wp1 + (1 - y1) * wp2 + 1.0 * wp3
P_turb = M * w_turb                       # kW shaft  (kg/s * kJ/kg = kW)
P_pump = M * w_pump                       # kW pump fluid work
P_gross = P_turb * ETA_GEN
P_bop = F_BOP * P_gross
P_elec = P_gross - P_pump / ETA_MOT - P_bop
W_net_elec = P_elec                        # kW net electric (sent-out)

# ---- exergy of the heat source (primary coolant, log-mean T) ----------------
Th, Tc = T_PRIM_HOT + KELVIN, T_PRIM_COLD + KELVIN
T_lm = (Th - Tc) / np.log(Th / Tc)         # log-mean primary temperature, K
Ex_source = Q_TH / 1.0e3 * (1.0 - T0 / T_lm)   # kW, Carnot exergy of supplied heat

# ---- per-component exergy destruction (kW) ----------------------------------
# stream exergy rate = m[kg/s] * e[kJ/kg]  ->  kW
e1, e2, e3, e3g, e4 = (exergy(s) for s in (s1, s2, s3, s3g, s4))
e5, e6, e7, e8, e9, e10 = (exergy(s) for s in (s5, s6, s7, s8, s9, s10))

# OTSG: primary heat-exergy in, secondary stream-exergy rise out
I_otsg = Ex_source - M * (e1 - e10)
# Turbine (full expander): in = full flow at state 1 + the dried last-stage flow
# re-entering at 3g; out = HP bleed (2) + crossover bleeds (3) + LP exhaust (4);
# minus the shaft work produced.  m_lp leaves the turbine only at state 4.
I_turb = (M * e1 + m_lp * e3g) \
    - (m_hp * e2 + (m_da + m_ms) * e3 + m_lp * e4) - P_turb
# Moisture separator: m_ms(e3) -> m_lp(e3g) + m_dr(e7_liq=e7)
I_ms = (m_ms * e3) - (m_lp * e3g + m_dr * e7)
# Condenser: m_lp(e4 -> e5); rejected-heat exergy leaves to sink (loss)
Q_cond = m_lp * (s4.h - s5.h)              # kW thermal rejected
Ex_q_cond = Q_cond * (1.0 - T0 / (s5.T))   # exergy carried by rejected heat
I_cond = m_lp * (e4 - e5) - Ex_q_cond      # internal destruction (heat-transfer dT)
L_cond = Ex_q_cond                         # exergy LOSS to cooling water
# Pumps (work in, raises stream exergy)
I_cp = (m_lp * e5 + m_lp * wp1) - m_lp * e6
I_bp = (m_feed * e7 + m_feed * wp2) - m_feed * e8
I_fp = (M * e9 + M * wp3) - M * e10
I_pumps = I_cp + I_bp + I_fp
# FWH-1 (open): y1*e2 + (1-y1)*e8 -> 1.0*e9
I_fwh1 = (m_hp * e2 + m_feed * e8) - M * e9
# Deaerator (open FWH-2): m_da*e3 + m_dr*e7 + m_lp*e6 -> m_feed*e7
I_da = (m_da * e3 + m_dr * e7 + m_lp * e6) - m_feed * e7

# generator + BOP losses (electromech.) as a lumped "conversion" loss
L_conv = (P_turb - P_gross) + P_pump * (1 / ETA_MOT - 1) + P_bop

components = [
    ("OTSG / steam generator (finite-dT)", I_otsg),
    ("Turbine + generator stages", I_turb),
    ("Condenser (internal dT)", I_cond),
    ("Condenser heat rejected to sea (loss)", L_cond),
    ("Feed / condensate / booster pumps", I_pumps),
    ("FWH-1 (closed-loop open heater)", I_fwh1),
    ("Deaerator (FWH-2)", I_da),
    ("Moisture separator", I_ms),
    ("Generator + BOP house load (loss)", L_conv),
]
I_total = sum(v for _, v in components)
eta_ex = W_net_elec / Ex_source            # 2nd-law efficiency vs supplied heat-exergy

# ---- report -----------------------------------------------------------------
print("\n==============  AEGIS-40 SECONDARY CYCLE — EXERGY ANALYSIS  ==============")
print("  Dead state T0 = %.1f C, P0 = %.4f MPa" % (T0 - KELVIN, P0))
print("  Primary log-mean T = %.1f C ;  supplied heat-exergy = %.0f kW" %
      (T_lm - KELVIN, Ex_source))
print("  Net electric (useful exergy out) = %.0f kW" % W_net_elec)
print("  Exergetic (2nd-law) efficiency   = %.1f %%" % (eta_ex * 100))
print("  (1st-law net efficiency          = %.1f %%)" % (W_net_elec / (Q_TH / 1e3) * 100))
print("\n  %-42s %10s %8s" % ("Component", "I (kW)", "share%"))
rows = []
for name, v in components:
    share = 100.0 * v / Ex_source
    print("  %-42s %10.0f %7.1f" % (name, v, share))
    rows.append([name, "%.0f" % v, "%.1f" % share])
print("  %-42s %10.0f %7.1f" % ("TOTAL destroyed + lost", I_total,
                                100.0 * I_total / Ex_source))
print("  %-42s %10.0f %7.1f" % ("Useful electric out", W_net_elec,
                                100.0 * W_net_elec / Ex_source))
print("  balance check (I+W)/Ex_source = %.3f" %
      ((I_total + W_net_elec) / Ex_source))
print("=========================================================================\n")

# ---- CSV + Markdown ---------------------------------------------------------
with open(os.path.join(OUT, "cycle_exergy.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["component", "exergy_destruction_kW", "share_pct_of_supplied"])
    w.writerows(rows)
    w.writerow(["TOTAL_destroyed_lost", "%.0f" % I_total,
                "%.1f" % (100 * I_total / Ex_source)])
    w.writerow(["useful_electric_out", "%.0f" % W_net_elec,
                "%.1f" % (100 * W_net_elec / Ex_source)])

with open(os.path.join(OUT, "cycle_exergy_table.md"), "w", encoding="utf-8") as f:
    f.write("# Aegis-40 secondary cycle — exergy (2nd-law) balance\n\n")
    f.write("Dead state T0 = %.0f C, P0 = %.4f MPa. Heat-source exergy from the "
            "primary log-mean temperature (%.0f C). Computed by "
            "`scripts/thermo_exergy.py`.\n\n" % (T0 - KELVIN, P0, T_lm - KELVIN))
    f.write("| Component | Exergy destruction / loss (kW) | Share of supplied exergy |\n")
    f.write("|---|---:|---:|\n")
    for name, v in components:
        f.write("| %s | %.0f | %.1f %% |\n" % (name, v, 100 * v / Ex_source))
    f.write("| **Total destroyed + lost** | **%.0f** | **%.1f %%** |\n" %
            (I_total, 100 * I_total / Ex_source))
    f.write("| **Useful electric output** | **%.0f** | **%.1f %%** |\n" %
            (W_net_elec, 100 * W_net_elec / Ex_source))
    f.write("\n- Supplied heat-exergy (primary @ T_lm = %.0f C): **%.0f kW**\n"
            % (T_lm - KELVIN, Ex_source))
    f.write("- Net electric output: **%.1f MWe**\n" % (W_net_elec / 1e3))
    f.write("- **Exergetic (2nd-law) efficiency: %.1f %%**  "
            "(1st-law net: %.1f %%)\n" %
            (eta_ex * 100, W_net_elec / (Q_TH / 1e3) * 100))

# ---- labelled PFD (Cycle-Tempo style) ---------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13.5, 7.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis("off")

BOX = dict(boxstyle="round,pad=0.25", fc="#eef3f7", ec="#37536b", lw=1.6)
STEAM = "#b5462e"
WATER = "#2d6a9f"
TXT = dict(ha="center", va="center", fontsize=9)


def comp(x, y, w, h, label, fc="#eef3f7"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.2", fc=fc, ec="#37536b", lw=1.6, zorder=3))
    ax.text(x, y, label, zorder=4, **TXT)


def arrow(x1, y1, x2, y2, color, lw=2.0, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=14, color=color, lw=lw,
                 ls=ls, zorder=2, shrinkA=2, shrinkB=2))


def node(x, y, tag, st, mdot, dy=3.4):
    """State-point callout: tag + P/T + h + mdot."""
    T_C = st.T - KELVIN
    txt = ("%s\n%.3g MPa, %.0f C\nh=%.0f kJ/kg\nm=%.1f kg/s" %
           (tag, st.P, T_C, st.h, mdot))
    ax.text(x, y + dy, txt, ha="center", va="bottom", fontsize=6.6,
            color="#16344a", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#9bb3c4", lw=0.7))


# --- component layout --------------------------------------------------------
comp(12, 44, 12, 9, "OTSG\n(helical SG)", fc="#f3e2dc")     # steam generator
# turbine trapezoid (HP->LP)
ax.add_patch(Polygon([(34, 47), (60, 50), (60, 38), (34, 41)],
             closed=True, fc="#dfe9f1", ec="#37536b", lw=1.6, zorder=3))
ax.text(47, 44, "TURBINE  (HP–MS–LP)", zorder=4, **TXT)
ax.add_patch(Circle((66, 44), 3.4, fc="#fff2c6", ec="#37536b", lw=1.6, zorder=3))
ax.text(66, 44, "G", fontsize=12, fontweight="bold", ha="center", va="center", zorder=4)
ax.text(66, 38.6, "%.1f MWe" % (W_net_elec / 1e3), ha="center", fontsize=8,
        color="#7a5b00")
comp(80, 30, 13, 7, "CONDENSER", fc="#dfe9f1")              # condenser
comp(80, 16, 7, 5, "CP", fc="#e7eef4")                      # condensate pump
comp(58, 16, 13, 6, "DEAERATOR\n(FWH-2)", fc="#e7eef4")     # deaerator
comp(40, 16, 7, 5, "BP", fc="#e7eef4")                      # booster pump
comp(26, 16, 11, 6, "FWH-1", fc="#e7eef4")                  # HP heater
comp(11, 16, 7, 5, "FP", fc="#e7eef4")                      # feed pump

# --- steam path (red) --------------------------------------------------------
arrow(18, 44, 34, 44.5, STEAM, lw=2.6)                       # OTSG -> turbine (S1)
node(26, 46, "1 main steam", s1, M, dy=2.2)
arrow(60, 44, 62.6, 44, STEAM)                               # turbine -> generator
arrow(60, 41, 80, 33.5, STEAM, lw=2.2)                       # LP exhaust -> condenser
node(70, 36.5, "4 LP exhaust", s4, m_lp, dy=0.5)
# extractions (dashed red, downward)
arrow(40, 40.5, 26, 19, STEAM, lw=1.4, ls=(0, (4, 2)))       # HP ext -> FWH1 (S2)
node(30, 28, "2 HP extr.", s2, m_hp, dy=0.0)
arrow(50, 41.5, 58, 19, STEAM, lw=1.4, ls=(0, (4, 2)))       # LP ext -> deaerator (S3)
node(56, 29, "3 LP extr.", s3, m_da, dy=0.0)

# --- water/condensate path (blue, right->left along the bottom) --------------
arrow(80, 26.5, 80, 18.5, WATER)                             # condenser -> CP (S5)
node(86, 22, "5 cond.", s5, m_lp, dy=-1.0)
arrow(76.5, 16, 64.5, 16, WATER)                             # CP -> deaerator (S6)
arrow(51.5, 16, 43.5, 16, WATER)                             # deaerator -> BP (S7)
node(47, 12.5, "7 DA out", s7, m_feed, dy=-3.2)
arrow(36.5, 16, 31.5, 16, WATER)                             # BP -> FWH1 (S8)
arrow(20.5, 16, 14.5, 16, WATER)                             # FWH1 -> FP (S9)
node(20, 12.4, "9 FWH-1 out", s9, M, dy=-3.2)
arrow(11, 18.5, 11, 39.5, WATER, lw=2.2)                     # FP -> OTSG (S10)
node(5, 30, "10 feedwater", s10, M, dy=0.0)

ax.text(50, 57.5, "Aegis-40 iPWR — Secondary-Cycle PFD with state points",
        ha="center", fontsize=14, fontweight="bold", color="#16344a")
ax.text(50, 54.3,
        "125 MWth -> %.1f MWe net  |  eta_net = %.1f %%  |  eta_exergy = %.1f %%  "
        "|  steam %.1f kg/s @ %.1f MPa/%.0f C"
        % (W_net_elec / 1e3, W_net_elec / (Q_TH / 1e3) * 100, eta_ex * 100,
           M, P_BOIL, T_BOIL),
        ha="center", fontsize=9, color="#37536b")
# legend
ax.plot([7, 12], [4, 4], color=STEAM, lw=2.6)
ax.text(13, 4, "steam / extraction", va="center", fontsize=8.5)
ax.plot([35, 40], [4, 4], color=WATER, lw=2.6)
ax.text(41, 4, "condensate / feedwater", va="center", fontsize=8.5)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "cycle_pfd_labeled.png"), dpi=160)
print("wrote", os.path.join(OUT, "cycle_exergy.csv"))
print("wrote", os.path.join(OUT, "cycle_exergy_table.md"))
print("wrote", os.path.join(OUT, "cycle_pfd_labeled.png"))
