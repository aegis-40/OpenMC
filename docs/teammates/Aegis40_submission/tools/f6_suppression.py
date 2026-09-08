#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40  F6 -- suppression-containment SBLOCA screening (mass-energy balance).
================================================================================

The Aegis-40 baseline containment is a compact LOW-PRESSURE PRESSURE-SUPPRESSION
containment (design pressure 0.414 MPa) with an internal IRWST pool (250 m3).
On an SBLOCA the released primary inventory is directed (spargers / vent lines)
into the IRWST, where direct-contact condensation suppresses the pressure rise;
long-term decay heat then follows the F5 PRHR/IRWST path (f5_prhr.py).

This is a lumped SCREENING energy balance (companion to f5_prhr.py), NOT a
containment transient code.  It answers four questions at FER level:

  Q1  Can the IRWST absorb the full primary-inventory blowdown?       (pool dT)
  Q2  Is the quasi-static containment pressure after blowdown, and while
      decay heat heats the pool, below the 0.414 MPa design pressure? (P vs t)
  Q3  What would the pressure be WITHOUT the suppression pool?  (motivates the
      suppression architecture: flash of the inventory into the free volume)
  Q4  What ADS end-state does IRWST GRAVITY INJECTION require?    (head check)

Conservatisms: the ENTIRE primary inventory is released at HOT-LEG enthalpy
(bounds the pressurizer steam fraction); no credit for structures, passive
containment cooling or PRHR during pool heat-up; decay heat at the ANS-5.1 /
Wigner-Way infinite-irradiation curve with the same x1.15 factor as F5.
NOT covered here (detailed-design scope, per FER Appendix B): short-term vent
clearing / chugging dynamics, non-condensable distribution, pool thermal
stratification, DF/scrubbing factors, hydrogen management (PARs).
"""
import argparse
import bisect
import math

CP_W   = 4186.0     # J/kg K liquid water
A_ANS  = 0.0622     # ANS-5.1 / Wigner-Way coefficient (as in f5_prhr.py)
P_ATM  = 101.325e3  # Pa

# Saturation pressure table, T [C] -> Psat [kPa]  (steam tables, screening use)
_T_SAT = [40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 145, 150]
_P_SAT = [7.38, 12.35, 19.94, 31.19, 47.39, 70.14, 101.35, 143.3,
          198.5, 270.1, 361.3, 415.5, 475.8]

# Saturated two-phase properties for the no-pool flash check:
# P [MPa], vf [m3/kg], vg [m3/kg], uf [kJ/kg], ufg [kJ/kg]
_FLASH = [(0.2, 0.001061, 0.8857, 504.5, 2025.0),
          (0.4, 0.001084, 0.4625, 604.3, 1949.3),
          (0.6, 0.001101, 0.3157, 669.9, 1897.5),
          (0.8, 0.001115, 0.2404, 720.2, 1856.6),
          (1.0, 0.001127, 0.1944, 761.7, 1822.0),
          (1.2, 0.001139, 0.1633, 797.3, 1791.5)]


def psat_kpa(T_c):
    """Saturation pressure [kPa] by linear interpolation, 40-150 C."""
    i = max(1, min(bisect.bisect_left(_T_SAT, T_c), len(_T_SAT) - 1))
    t0, t1 = _T_SAT[i - 1], _T_SAT[i]
    p0, p1 = _P_SAT[i - 1], _P_SAT[i]
    return p0 + (p1 - p0) * (T_c - t0) / (t1 - t0)


def tsat_c(P_kpa):
    """Saturation temperature [C] at pressure [kPa] (inverse of psat_kpa)."""
    i = max(1, min(bisect.bisect_left(_P_SAT, P_kpa), len(_P_SAT) - 1))
    p0, p1 = _P_SAT[i - 1], _P_SAT[i]
    t0, t1 = _T_SAT[i - 1], _T_SAT[i]
    return t0 + (t1 - t0) * (P_kpa - p0) / (p1 - p0)


def flash_pressure(u_kj, v_m3kg):
    """Equilibrium saturation pressure [MPa] for given specific u and v
    (two-phase flash of the inventory into the free volume, no pool credit)."""
    prev = None
    for P, vf, vg, uf, ufg in _FLASH:
        x = (v_m3kg - vf) / (vg - vf)
        u = uf + max(0.0, min(1.0, x)) * ufg
        if u >= u_kj and prev is not None:
            P0, u0 = prev
            return P0 + (P - P0) * (u_kj - u0) / (u - u0)
        prev = (P, u)
    return _FLASH[-1][0]  # off-table: report the last (still a FAIL vs 0.414)


def p_containment(T_pool_c, T_gas0_c, V_note=None):
    """Quasi-static containment pressure [kPa]: heated air + steam at pool T.
    Air is conservatively taken at the pool temperature (isochoric heat-up)."""
    p_air = (P_ATM / 1e3) * (T_pool_c + 273.15) / (T_gas0_c + 273.15)
    return p_air + psat_kpa(T_pool_c)


def t_from_energy(E_j, P0_w, unc):
    """Invert the integrated ANS-5.1 curve: time [s] at which decay energy = E."""
    x = E_j * 0.8 / (unc * P0_w * A_ANS) + 1.0
    return x ** 1.25


def main():
    ap = argparse.ArgumentParser(
        description="Aegis-40 F6 suppression-containment SBLOCA screening",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--P0',     type=float, default=125.0,
                    help="rated thermal power [MWth]")
    ap.add_argument('--Mp',     type=float, default=26000.0,
                    help="primary coolant inventory [kg] (FER: ~26 t / ~35 m3)")
    ap.add_argument('--hp',     type=float, default=1390.0,
                    help="release enthalpy [kJ/kg] (hot-leg liquid @ 308 C, bounding)")
    ap.add_argument('--Vpool',  type=float, default=250.0,
                    help="IRWST pool volume [m3] (same DESIGN input as F5)")
    ap.add_argument('--Tpool',  type=float, default=40.0,
                    help="IRWST initial temperature [C]")
    ap.add_argument('--Vfree',  type=float, default=2000.0,
                    help="containment free (gas) volume [m3] (layout estimate, D=15 m)")
    ap.add_argument('--Pdes',   type=float, default=0.414,
                    help="containment design pressure [MPa]")
    ap.add_argument('--unc',    type=float, default=1.15,
                    help="decay-heat conservatism factor (same as F5)")
    ap.add_argument('--head',   type=float, default=8.0,
                    help="IRWST water level above injection nozzle [m] (CAD input)")
    ap.add_argument('--dpline', type=float, default=20.0,
                    help="injection-line + check-valve loss allowance [kPa]")
    a = ap.parse_args()

    P0 = a.P0 * 1e6
    M_pool = a.Vpool * 1000.0
    h_pool0 = CP_W * a.Tpool / 1e3                       # kJ/kg (liquid, ~cp*T)

    print("=" * 72)
    print(" Aegis-40  F6  suppression-containment SBLOCA screening")
    print(f" P0 {a.P0:.0f} MWth | inventory {a.Mp/1e3:.0f} t @ {a.hp:.0f} kJ/kg"
          f" | IRWST {a.Vpool:.0f} m3 @ {a.Tpool:.0f} C")
    print(f" V_free {a.Vfree:.0f} m3 | design P {a.Pdes:.3f} MPa | unc x{a.unc:.2f}")
    print("=" * 72)

    # --- Q1: blowdown absorbed by the pool (enthalpy mixing) ---
    h_mix = (M_pool * h_pool0 + a.Mp * a.hp) / (M_pool + a.Mp)
    T_mix = h_mix * 1e3 / CP_W
    E_bd = a.Mp * (a.hp - h_pool0) * 1e3                 # J above pool datum
    print(" Q1  Blowdown into the IRWST (full inventory, direct-contact cond.):")
    print(f"     blowdown energy above pool datum : {E_bd/1e9:6.1f} GJ")
    print(f"     pool temperature 40 C -> {T_mix:5.1f} C  "
          f"(dT {T_mix - a.Tpool:+.1f} K, pool mass -> {(M_pool+a.Mp)/1e3:.0f} t)")

    # --- Q2: quasi-static pressure vs pool temperature / time ---
    P_bd = p_containment(T_mix, a.Tpool)
    T_lim = tsat_c(a.Pdes * 1e3 - P_ATM / 1e3 *
                   ((tsat_c(a.Pdes*1e3) + 273.15) / (a.Tpool + 273.15)))
    # iterate once: air partial pressure at the limiting pool temperature
    for _ in range(20):
        p_air = (P_ATM/1e3) * (T_lim + 273.15) / (a.Tpool + 273.15)
        T_new = tsat_c(a.Pdes * 1e3 - p_air)
        if abs(T_new - T_lim) < 0.01:
            break
        T_lim = T_new
    M_tot = M_pool + a.Mp
    E_100 = M_tot * CP_W * max(0.0, 100.0 - T_mix)
    E_lim = M_tot * CP_W * max(0.0, T_lim - T_mix)
    t_100 = t_from_energy(E_100, P0, a.unc) / 3600.0
    t_lim = t_from_energy(E_lim, P0, a.unc) / 3600.0
    ok_bd = P_bd / 1e3 <= a.Pdes
    print("-" * 72)
    print(" Q2  Quasi-static containment pressure (heated air + steam @ pool T):")
    print(f"     after blowdown ({T_mix:.1f} C)      : {P_bd/1e3:6.3f} MPa  "
          f"({'PASS' if ok_bd else 'FAIL'} <= {a.Pdes:.3f} MPa, "
          f"margin x{a.Pdes/(P_bd/1e3):.1f})")
    print(f"     pool @ 100 C (atm boiling)      : "
          f"{p_containment(100.0, a.Tpool)/1e3:6.3f} MPa  "
          f"reached at t = {t_100:5.1f} h (no heat removal credited)")
    print(f"     design P reached at pool T      : {T_lim:6.1f} C"
          f"  ->  t = {t_lim:5.1f} h  with ZERO heat-removal credit")
    print("     beyond that: PRHR + passive containment cooling / vented boiling")
    print("     carry decay heat per F5 (>= 240 h for the same 250 m3 pool).")

    # --- Q3: counterfactual -- no suppression pool ---
    u_p = a.hp - 12.8e3 * 0.00144                        # kJ/kg, h - P*v (12.8 MPa)
    P_flash = flash_pressure(u_p, a.Vfree / a.Mp)
    P_nopool = P_flash + P_ATM / 1e6
    print("-" * 72)
    print(" Q3  Counterfactual WITHOUT the suppression pool (flash into V_free):")
    print(f"     equilibrium steam P {P_flash:5.2f} + air ~0.10 = "
          f"{P_nopool:5.2f} MPa  ({'FAIL' if P_nopool > a.Pdes else 'PASS'}"
          f" vs {a.Pdes:.3f} MPa, x{P_nopool/a.Pdes:.1f} over)")
    print("     -> the suppression pool is REQUIRED, not decorative.")

    # --- Q4: IRWST gravity-injection head / ADS end-state requirement ---
    dp_head = 1000.0 * 9.81 * a.head / 1e3               # kPa
    p_rcs_max = P_bd + dp_head - a.dpline                # kPa abs
    print("-" * 72)
    print(" Q4  Gravity injection from the IRWST (head check):")
    print(f"     head {a.head:.1f} m -> {dp_head:5.1f} kPa; line allowance "
          f"{a.dpline:.0f} kPa; containment {P_bd/1e3:.3f} MPa")
    print(f"     => ADS end-state REQUIREMENT: RCS pressure <= "
          f"{p_rcs_max/1e3:.3f} MPa abs for injection to start")
    print("     => staged ADS to near-containment pressure (AP1000/CAREM-class);")
    print(f"     head is a CAD input -- confirm IRWST level >= {a.head:.1f} m above")
    print("     the injection nozzle in the reactor-building layout.")

    # --- sensitivity: containment free volume (no-pool case only) ---
    print("-" * 72)
    print(" Sensitivity (no-pool flash P vs free volume): " + "  ".join(
        f"{v:.0f} m3 -> {flash_pressure(u_p, v/a.Mp) + P_ATM/1e6:.2f} MPa"
        for v in (0.75 * a.Vfree, a.Vfree, 1.25 * a.Vfree)))
    print("=" * 72)
    verdict = ok_bd and t_lim > 8.0
    print(f" VERDICT: {'PASS' if verdict else 'CHECK'} -- suppression/IRWST "
          f"holds P <= {a.Pdes:.3f} MPa through blowdown and early decay heat;")
    print(" long-term heat removal = F5 path (f5_prhr.py).")
    print("=" * 72)


if __name__ == "__main__":
    main()
