"""Aegis-40 — re-couple the secondary Rankine cycle to the §8.4 primary result.

§8.4 fixes the primary natural-circulation legs at hot 308 C / cold 258 C (was the
§8.9 assumption 305 / 265). The OTSG secondary saturation temperature must sit a
practical pinch (>= ~8 C) below the 258 C cold leg, so the turbine-inlet steam
pressure is capped at ~3.98 MPa (vs 4.8 MPa in the current §8.9 draft).

This script re-runs the SAME cycle model as thermo_cycle.py (regenerative
superheated Rankine, 2 open FWHs + moisture separator, identical efficiencies and
extraction pressures) but:
  * sets the primary legs to 308 / 258 C,
  * sweeps the boiler (turbine-inlet) pressure across the feasible band, and
  * raises the superheat to a 12 C approach below the *higher* 308 C hot leg
    (steam ~296 C) to claw back the efficiency lost to the lower boiling pressure.

It prints a feasibility table and picks the best feasible point, answering: does
the 40 MWe / 32 % nameplate survive the §8.4 cold-leg correction?

Run:  py scripts/thermo_cycle_recouple.py
"""

from iapws import IAPWS97

KELVIN = 273.15

# ---- fixed cycle parameters (identical to thermo_cycle.py) ------------------
Q_TH   = 125.0e6
P_COND = 0.007
P_EXT1 = 1.00
P_EXT2 = 0.15
ETA_T  = 0.85
ETA_P  = 0.82
ETA_GEN = 0.985
ETA_MOT = 0.95
F_BOP  = 0.050

# ---- NEW primary boundary (from §8.4 / natcirc_primary.py) ------------------
T_PRIM_HOT  = 308.0
T_PRIM_COLD = 258.0
SH_APPROACH = 12.0                       # superheater hot-end approach (deg C)
T_BOIL = T_PRIM_HOT - SH_APPROACH        # = 296 C (was 293 against the 305 hot leg)
PINCH_MIN = 8.0


def expand(h_in, s_in, p_out, eta):
    iso = IAPWS97(P=p_out, s=s_in)
    h_out = h_in - eta * (h_in - iso.h)
    return IAPWS97(P=p_out, h=h_out)


def pump(h_in, p_in, p_out, eta):
    v = IAPWS97(P=p_in, x=0).v
    w = v * (p_out - p_in) * 1.0e3 / eta
    return h_in + w, w


def run_cycle(P_BOIL, T_BOIL):
    """Full regenerative cycle at the given boiler pressure/temperature.
    Returns a dict of the headline results (mirrors thermo_cycle.py exactly)."""
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

    x3 = s3.x
    y1 = (s9.h - s8.h) / (s2.h - s8.h)
    A = x3 * (s7.h - s6.h)
    y2 = (1 - y1) * A / ((s3.h - s7.h) + A)
    m_last = (1 - y1 - y2) * x3

    w_turb = ((s1.h - s2.h) + (1 - y1) * (s2.h - s3.h) + m_last * (s3g.h - s4.h))
    w_pump = m_last * wp1 + (1 - y1) * wp2 + 1.0 * wp3
    q_in = s1.h - s10.h
    eta_th = (w_turb - w_pump) / q_in

    m_dot = Q_TH / (q_in * 1.0e3)
    P_turb = m_dot * w_turb * 1.0e3
    P_pump = m_dot * w_pump * 1.0e3
    P_gross = P_turb * ETA_GEN
    P_bop = F_BOP * P_gross
    P_elec = P_gross - P_pump / ETA_MOT - P_bop
    eta_net = P_elec / Q_TH

    # OTSG pinch against the NEW primary legs
    mcp_prim = Q_TH / (T_PRIM_HOT - T_PRIM_COLD)
    Tsat_boil = IAPWS97(P=P_BOIL, x=1).T - KELVIN
    hf_boil = IAPWS97(P=P_BOIL, x=0).h
    Q_econ = m_dot * (hf_boil - s10.h) * 1.0e3
    T_prim_boilstart = T_PRIM_COLD + Q_econ / mcp_prim
    pinch = T_prim_boilstart - Tsat_boil

    return dict(P_BOIL=P_BOIL, Tsat=Tsat_boil, eta_net=eta_net * 100,
                MWe=P_elec / 1e6, eta_gross=P_gross / Q_TH * 100,
                m_dot=m_dot, pinch=pinch, x4=s4.x, y1=y1, y2=y2)


print("=" * 78)
print("AEGIS-40 OTSG RE-COUPLING  —  primary 308/258 C, steam T = %.0f C (12 C approach)" % T_BOIL)
print("=" * 78)
print("  %7s %7s %8s %8s %8s %7s %7s" %
      ("P_boil", "Tsat", "pinch", "NET MWe", "eta_net", "m_dot", "x_exh"))
print("  %7s %7s %8s %8s %8s %7s %7s" %
      ("(MPa)", "(C)", "(C)", "", "(%)", "(kg/s)", ""))

best = None
for i in range(40, 56):                 # 4.0 .. 5.5 MPa
    P = i * 0.1
    try:
        r = run_cycle(P, T_BOIL)
    except Exception as e:
        continue
    feas = r["pinch"] >= PINCH_MIN
    flag = "OK" if feas else ("tight" if r["pinch"] > 0 else "VIOL")
    print("  %7.2f %7.1f %8.1f %8.2f %8.2f %7.1f %7.3f  %s" %
          (r["P_BOIL"], r["Tsat"], r["pinch"], r["MWe"], r["eta_net"],
           r["m_dot"], r["x4"], flag))
    if feas and (best is None or r["MWe"] > best["MWe"]):
        best = r

print("-" * 78)
if best:
    print("BEST FEASIBLE POINT (pinch >= %.0f C):" % PINCH_MIN)
    print("  steam %.2f MPa / %.0f C  ->  NET %.2f MWe  (eta_net %.2f %%),  pinch %.1f C, m_dot %.1f kg/s"
          % (best["P_BOIL"], T_BOIL, best["MWe"], best["eta_net"], best["pinch"], best["m_dot"]))
    print("  vs §8.9 design point:        40.00 MWe (32.0 %), steam 4.80 MPa / 293 C")
    print("  delta vs nameplate:          %+.2f MWe" % (best["MWe"] - 40.0))
print("=" * 78)
