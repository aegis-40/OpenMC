#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NuScale - Correlation thermal stack  (Variant 1 post-processor)
=============================================================

Turns the CFD-trusted quantities (axial power shape, coolant bulk T(z), flow)
into the PHYSICALLY CORRECT solid temperatures and PCT, using a Nusselt
correlation for the clad->coolant film coefficient instead of the
RANS-laminarized CFD wall h.

This is the standard subchannel-code approach (COBRA/VIPRE/CTF): never trust a
CFD-resolved near-wall h for a thin developing channel; impose a validated
correlation. The 1-D radial conduction stack at each axial level z:

    T_bulk(z)                               <- coolant mixed-mean (energy bal.)
      + q''(z) / h_corr                     <- convective film  (Dittus-Boelter)
      = T_clad,outer(z)
      + q'(z)*ln(r_co/r_ci)/(2 pi k_clad)   <- clad conduction
      = T_clad,inner(z)
      + q'(z)/(2 pi r_f  h_gap)             <- He gap (interface resistance)
      = T_fuel,surface(z)
      + q'(z)/(4 pi k_fuel)                 <- UO2 solid cylinder, uniform gen
      = T_fuel,centre(z)

Outputs: peak clad temperature (PCT) and peak fuel centreline, with axial
locations and margins. Optional --csv cross-checks T_bulk(z) (and the CFD clad
temperature) against an OpenFOAM axial sample.

Axial power / T_bulk come from mdnbr.py's chopped-cosine builder (same
defaults), so this tool and the MDNBR number stay consistent.
"""

import argparse
import math
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdnbr import Config as CoolantConfig, build_profile, load_csv  # noqa: E402


# --------------------------------------------------------------------------
# Solid / film configuration (defaults from docs/parameters.md)
# --------------------------------------------------------------------------
@dataclass
class StackConfig:
    # radii [m]
    r_f:   float = 4.095e-3     # fuel pellet radius (gap collapsed to here)
    r_ci:  float = 4.18e-3      # clad inner radius
    r_co:  float = 4.75e-3      # clad outer radius (= heated perimeter)
    # solid conductivities [W/m.K]
    k_fuel: float = 3.5         # UO2
    k_clad: float = 16.0        # Zircaloy-4
    # He gap conductance [W/m2.K] referenced to pellet surface (2 pi r_f)
    h_gap:  float = 5647.0      # = kappaLayers/thicknessLayers = 0.48/8.5e-5
    # coolant transport (for h correlation)
    mu:     float = 9.4e-5      # dynamic viscosity [Pa.s]
    k_w:    float = 0.59        # water thermal conductivity [W/m.K]
    Pr:     float = 0.84        # Prandtl
    # correlation: 'db' = Dittus-Boelter, 'weisman' = rod-bundle (P/D aware)
    corr:   str   = 'db'
    PD:     float = 1.326       # pitch/diameter (= 12.6/9.5) for Weisman


# --------------------------------------------------------------------------
# Film coefficient from a Nusselt correlation
# --------------------------------------------------------------------------
def film_h(cool: CoolantConfig, st: StackConfig):
    Re = cool.G * cool.D_h / st.mu
    Pr = st.Pr
    if st.corr == 'weisman':
        # Weisman square-lattice rod bundle: Nu = C Re^0.8 Pr^(1/3),
        # C = 0.042*(P/D) - 0.024
        C = 0.042 * st.PD - 0.024
        Nu = C * Re ** 0.8 * Pr ** (1.0 / 3.0)
        name = f"Weisman (P/D={st.PD:.3f}, C={C:.4f})"
    else:
        # Dittus-Boelter, heating (n=0.4)
        Nu = 0.023 * Re ** 0.8 * Pr ** 0.4
        name = "Dittus-Boelter"
    h = Nu * st.k_w / cool.D_h
    return h, Re, Nu, name


# --------------------------------------------------------------------------
# Radial conduction stack
# --------------------------------------------------------------------------
def stack(cool: CoolantConfig, st: StackConfig, prof, h, boiling=False):
    z   = prof['z']
    qp  = prof['qprime']      # W/m
    Tb  = prof['Tbulk']       # K
    Tsat = prof['Tsat']
    twoPi = 2.0 * math.pi

    R_film = 1.0 / (twoPi * st.r_co * h)               # K per (W/m)
    R_clad = math.log(st.r_co / st.r_ci) / (twoPi * st.k_clad)
    R_gap  = 1.0 / (twoPi * st.r_f * st.h_gap)
    R_fuel = 1.0 / (4.0 * math.pi * st.k_fuel)         # centre-to-surface

    rows = []
    n_boil = 0
    for i in range(len(z)):
        q = qp[i]
        qpp = q / (twoPi * st.r_co)                    # wall heat flux [W/m2]
        T_co = Tb[i] + q * R_film                      # single-phase film
        if boiling:
            # Subcooled nucleate boiling: the wall follows whichever mode is more
            # effective (lower wall T) for the IMPOSED q'' -> single-phase until the
            # boiling curve Tsat + Jens-Lottes superheat becomes the limiter. Taking
            # the min gives a CONTINUOUS onset (no jump) and the physical clad T,
            # below the single-phase (and single-phase-CFD) over-prediction.
            # Jens-Lottes: dTsat[K] = 25*(q''[MW/m2])^0.25 * exp(-P[MPa]/6.2)
            dT_JL = 25.0 * (qpp / 1.0e6) ** 0.25 * math.exp(-cool.p_mpa / 6.2)
            T_boil = Tsat + dT_JL
            if T_boil < T_co:
                T_co = T_boil
                n_boil += 1
        T_ci = T_co + q * R_clad
        T_fs = T_ci + q * R_gap
        T_fc = T_fs + q * R_fuel
        rows.append((z[i], Tb[i], T_co, T_ci, T_fs, T_fc, qpp))
    return rows, (R_film, R_clad, R_gap, R_fuel), n_boil


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------
def run(cool, st, csv=None, table=False, boiling=False):
    prof = load_csv(csv, cool) if csv else build_profile(cool)
    h, Re, Nu, cname = film_h(cool, st)
    rows, R, n_boil = stack(cool, st, prof, h, boiling=boiling)

    # peaks
    pct_i   = max(range(len(rows)), key=lambda i: rows[i][3])   # max clad inner
    fuel_i  = max(range(len(rows)), key=lambda i: rows[i][5])   # max fuel centre
    pct     = rows[pct_i][3]
    fuel_pk = rows[fuel_i][5]
    Tout    = prof['Tbulk'][-1]

    print("=" * 74)
    print(" NuScale correlation thermal stack  (Variant 1: CFD flow + correlation h)")
    print("=" * 74)
    print(f" Film correlation      : {cname}")
    print(f"   Re = {Re:,.0f}   Pr = {st.Pr}   Nu = {Nu:.1f}"
          f"   ->  h = {h:,.0f} W/m2K")
    print(f" Resistances [K/(W/m)] : film {R[0]:.5f}  clad {R[1]:.5f}"
          f"  gap {R[2]:.5f}  fuel {R[3]:.5f}")
    print(f" Coolant bulk          : in {cool.T_in:.1f} K  ->  out {Tout:.1f} K"
          f"  (rise {Tout-cool.T_in:.1f} K)")
    if boiling:
        print(f" Subcooled boiling     : Jens-Lottes wall clamp ON  (Tsat"
              f" {prof['Tsat']:.1f} K, active at {n_boil}/{len(rows)} axial nodes)")
    else:
        print(f" Subcooled boiling     : OFF (single-phase film everywhere ->"
              f" over-predicts clad where T_wall>Tsat)")
    print("-" * 74)
    if table:
        print(f"{'z[m]':>7}{'Tbulk':>8}{'Tclad_o':>9}{'Tclad_i':>9}"
              f"{'Tfuel_s':>9}{'Tfuel_c':>9}{'qpp[MW]':>9}")
        step = max(1, len(rows) // 25)
        for r in rows[::step]:
            print(f"{r[0]:7.3f}{r[1]:8.1f}{r[2]:9.1f}{r[3]:9.1f}"
                  f"{r[4]:9.1f}{r[5]:9.1f}{r[6]/1e6:9.3f}")
        print("-" * 74)

    def line(label, T, zat):
        print(f" {label:<26}: {T:7.1f} K  ({T-273.15:6.1f} C)  at z = {zat:.3f} m")
    line("PCT (peak clad, inner)", pct, rows[pct_i][0])
    print(f"   clad outer at PCT z      : {rows[pct_i][2]:7.1f} K"
          f"  ({rows[pct_i][2]-273.15:.1f} C)")
    line("Peak fuel centreline", fuel_pk, rows[fuel_i][0])
    print("-" * 74)
    pct_C = pct - 273.15
    print(f" PCT limit 1200 C (accident) : margin {1200 - pct_C:+.0f} C"
          f"   [{'PASS' if pct_C < 1200 else 'FAIL'}]")
    print(f" UO2 melt ~2840 C            : margin {2840 - (fuel_pk-273.15):+.0f} C"
          f"   [{'PASS' if fuel_pk-273.15 < 2840 else 'FAIL'}]")

    # optional CFD cross-check
    if csv:
        print("-" * 74)
        print(" (CSV mode: T_bulk(z) above is the OpenFOAM-sampled coolant bulk;")
        print("  compare PCT here vs the raw CFD clad temp to see the film offset.)")
    print("=" * 74)
    return rows, pct, fuel_pk


def main(argv=None):
    cc = CoolantConfig(); st = StackConfig()
    ap = argparse.ArgumentParser(
        description="NuScale correlation thermal stack (PCT, fuel centreline)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # coolant / power (mirror mdnbr.py)
    ap.add_argument('--p',    type=float, default=cc.p_mpa)
    ap.add_argument('--Tin',  type=float, default=cc.T_in)
    ap.add_argument('--G',    type=float, default=cc.G)
    ap.add_argument('--cp',   type=float, default=cc.cp)
    ap.add_argument('--L',    type=float, default=cc.L)
    ap.add_argument('--Dco',  type=float, default=cc.D_co)
    ap.add_argument('--Dh',   type=float, default=cc.D_h)
    ap.add_argument('--Aflow',type=float, default=cc.A_flow)
    ap.add_argument('--qpeak',type=float, default=cc.qp_hot_peak)
    ap.add_argument('--Fz',   type=float, default=cc.Fz)
    ap.add_argument('--Le',   type=float, default=cc.Le_ratio,
                    help="extrap/active length ratio (1.0 full cosine, 1.2 chopped)")
    ap.add_argument('--n',    type=int,   default=cc.n)
    # solids / film
    ap.add_argument('--rf',   type=float, default=st.r_f)
    ap.add_argument('--rci',  type=float, default=st.r_ci)
    ap.add_argument('--rco',  type=float, default=st.r_co)
    ap.add_argument('--kfuel',type=float, default=st.k_fuel)
    ap.add_argument('--kclad',type=float, default=st.k_clad)
    ap.add_argument('--hgap', type=float, default=st.h_gap)
    ap.add_argument('--mu',   type=float, default=st.mu)
    ap.add_argument('--kw',   type=float, default=st.k_w)
    ap.add_argument('--Pr',   type=float, default=st.Pr)
    ap.add_argument('--corr', type=str,   default=st.corr, choices=['db', 'weisman'])
    ap.add_argument('--PD',   type=float, default=st.PD)
    ap.add_argument('--csv',  type=str,   default=None,
                    help="OpenFOAM axial CSV: x[m] qpp[W/m2] Tbulk[K] (cross-check)")
    ap.add_argument('--table', action='store_true')
    ap.add_argument('--boiling', action='store_true',
                    help="apply Jens-Lottes subcooled-boiling wall clamp where T_wall>Tsat")
    a = ap.parse_args(argv)

    cc = CoolantConfig(p_mpa=a.p, T_in=a.Tin, G=a.G, cp=a.cp, L=a.L, D_co=a.Dco,
                       D_h=a.Dh, A_flow=a.Aflow, qp_hot_peak=a.qpeak, Fz=a.Fz,
                       Le_ratio=a.Le, n=a.n)
    st = StackConfig(r_f=a.rf, r_ci=a.rci, r_co=a.rco, k_fuel=a.kfuel,
                     k_clad=a.kclad, h_gap=a.hgap, mu=a.mu, k_w=a.kw, Pr=a.Pr,
                     corr=a.corr, PD=a.PD)
    run(cc, st, csv=a.csv, table=a.table, boiling=a.boiling)


if __name__ == "__main__":
    main()
