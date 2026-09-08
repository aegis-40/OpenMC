#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40  F5 -- passive decay-heat removal (PRHR / IRWST) grace-period analysis.
================================================================================

After scram the core makes DECAY HEAT (ANS-5.1). With no pumps / no AC credited it
is rejected passively: core -> PRHR heat exchanger -> IRWST / reactor pool, which
heats up and boils off. Two safety questions (the F5 safety case):

  * prhr_capacity  >= 1.05  -- the PRHR HX can remove the decay-heat DUTY
  * operator_grace_period >= 72 h -- the pool inventory lasts >=72 h with no action

This is a lumped TRANSIENT ENERGY balance (companion to the steady natcirc.py),
NOT a pin-CFD job.

Decay heat: ANS-5.1 / Wigner-Way engineering curve, infinite operating time
(conservative, max heat):   P_d(t)/P0 = unc * 0.0622 * t^-0.2   (t in s, t>=1 s).
Integrated:  E(0..t) = unc * P0 * 0.0622 * (t^0.8 - t0^0.8)/0.8.

Pool capacity = sensible (T_init -> T_sat) + latent (boil-off).  Grace = time at
which the integrated decay energy equals the pool capacity.

Conservatisms: infinite operating time; no actinide/uncertainty bump unless --unc;
no credit for vessel/structure heat capacity or ambient losses; HX duty read at the
early peak.  Refine with the full tabulated ANS-5.1 curve + 2-sigma if needed.
"""
import argparse
import math

CP_W   = 4186.0       # J/kg K, liquid water
HFG_W  = 2.257e6      # J/kg, latent heat at ~100 C / atmospheric pool
TSAT_W = 373.15       # K, atmospheric saturation (vented pool)
A_ANS  = 0.0622       # ANS-5.1 / Wigner-Way coefficient
T0_REF = 1.0          # s, lower integration bound (curve valid t>=~1 s)


def p_decay(P0, t, unc):
    """Decay power [W] at time t [s] after shutdown."""
    return unc * P0 * A_ANS * t ** -0.2


def e_decay(P0, t, unc):
    """Integrated decay energy [J] from T0_REF to t."""
    return unc * P0 * A_ANS * (t ** 0.8 - T0_REF ** 0.8) / 0.8


def grace_period(P0, E_sink, unc):
    """Solve E(0..t) = E_sink for t [s] (analytic inverse)."""
    x = E_sink / (unc * P0 * A_ANS / 0.8) + T0_REF ** 0.8
    return x ** (1.0 / 0.8)


def main():
    ap = argparse.ArgumentParser(description="Aegis-40 F5 PRHR/IRWST grace period",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('--P0',   type=float, default=125.0, help="rated thermal power [MWth]")
    ap.add_argument('--vol',  type=float, default=250.0, help="IRWST/pool water volume [m3] (DESIGN input)")
    ap.add_argument('--Tinit',type=float, default=40.0,  help="pool initial temperature [C]")
    ap.add_argument('--unc',  type=float, default=1.0,   help="decay-heat conservatism factor (1.1-1.2 bounds ANS-5.1 unc.+actinides)")
    ap.add_argument('--target',type=float,default=72.0,  help="required grace period [h]")
    a = ap.parse_args()

    P0   = a.P0 * 1e6
    M    = a.vol * 1000.0                       # m3 -> kg (rho ~1000)
    dT   = TSAT_W - (a.Tinit + 273.15)
    e_sens = M * CP_W * dT                       # sensible capacity [J]
    e_lat  = M * HFG_W                           # full boil-off latent [J]

    print("=" * 64)
    print(" Aegis-40  F5  passive decay-heat removal (PRHR / IRWST)")
    print(f" P0 {a.P0:.0f} MWth | pool {a.vol:.0f} m3 @ {a.Tinit:.0f} C | unc x{a.unc:.2f}")
    print("=" * 64)

    # --- HX duty table (for prhr_capacity sizing) ---
    print(" Decay-heat DUTY the PRHR HX must remove (>= x1.05):")
    print(f"   {'time':>8} {'P_decay':>9} {'% P0':>7}")
    for t, lbl in [(10,"10 s"),(60,"1 min"),(600,"10 min"),(3600,"1 h"),
                   (28800,"8 h"),(86400,"24 h"),(259200,"72 h")]:
        pd = p_decay(P0, t, a.unc)
        print(f"   {lbl:>8} {pd/1e6:>7.2f} MW {100*pd/P0:>6.2f}%")
    print(f"   -> HX sized for the early peak (~{p_decay(P0,30,a.unc)/1e6:.1f} MW at ~30 s);"
          " ratio >=1.05 => rated >= that x1.05.")

    # --- integrated energy & grace period ---
    print("-" * 64)
    for h in (24, 72, 168):
        print(f"   integrated decay energy at {h:>3} h : {e_decay(P0,h*3600,a.unc)/1e9:7.1f} GJ")
    print("-" * 64)
    # grace for the given pool, two bounding pool-capacity assumptions
    g_full = grace_period(P0, e_sens + e_lat, a.unc) / 3600.0   # sensible + full boil-off
    g_sens = grace_period(P0, e_sens,         a.unc) / 3600.0   # sensible only (ultra-conservative)
    print(f" Grace period for {a.vol:.0f} m3 pool:")
    print(f"   sensible + boil-off : {g_full:7.1f} h   ({'PASS' if g_full>=a.target else 'FAIL'} >= {a.target:.0f} h)")
    print(f"   sensible only       : {g_sens:7.1f} h   ({'PASS' if g_sens>=a.target else 'FAIL'} >= {a.target:.0f} h, no boiling credit)")

    # --- required inventory for the target ---
    E_req = e_decay(P0, a.target * 3600.0, a.unc)
    cap_full = CP_W * dT + HFG_W
    print("-" * 64)
    print(f" Water REQUIRED for {a.target:.0f} h grace ({E_req/1e9:.0f} GJ):")
    print(f"   with boil-off (sensible+latent) : {E_req/cap_full/1000:7.0f} m3")
    print(f"   sensible only (heat to T_sat)   : {E_req/(CP_W*dT)/1000:7.0f} m3")
    print("=" * 64)


if __name__ == "__main__":
    main()
