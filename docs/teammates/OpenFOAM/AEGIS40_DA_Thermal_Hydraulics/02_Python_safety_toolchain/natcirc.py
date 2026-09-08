#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 - Natural-circulation loop solver  (keystone: fixes the core flow G)
==========================================================================

The Aegis-40 primary loop has NO pumps: flow is driven only by the buoyancy head
between the cold downcomer column and the hot riser column. This 1-D steady
momentum-energy balance closes the loop and returns the ACTUAL core mass flux
G.

Balance (single-phase, Boussinesq density):

    driving head   Dp_dr   = g * H_tc * (rho_cold - rho_hot)
                           ~ g * H_tc * rho * beta * dT          [Pa]
    loop losses    Dp_loss = K_tot * mdot^2 / (2 * rho * A_core^2)
    core energy    dT      = P / (mdot * cp)

Eliminating dT gives the classic cube-root law:

    mdot = [ 2 rho^2 A_core^2 g H_tc beta P / (cp K_tot) ]^(1/3)   ~ P^(1/3)

H_tc = elevation between the thermal centroid of the heat SINK (steam generator)
and the heat SOURCE (core mid-plane). K_tot = total loss coefficient referenced
to the core flow velocity (core friction f*L/Dh + spacer grids + SG + plena +
turns). Both are NuScale/MASLWR-class placeholders -- the two real design knobs.

The core friction part of K_tot is computed self-consistently (f depends on Re
depends on mdot), so the solve iterates to convergence.

Outputs: mdot, G, u_core, core dT, T_out vs T_sat (boiling check), driving head,
Re, friction breakdown; plus a power sweep giving the mdot~P^(1/3) trend used to
validate against NuScale/MASLWR (OSU) data.

Defaults consistent with mdnbr.py / thermal_stack.py.
"""

import argparse
import math
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdnbr import sat_props  # noqa: E402  (reuse the saturation table)

G_CONST = 9.80665  # m/s2


@dataclass
class Config:
    # --- plant / power (Aegis-40 FER, OpenMC-consistent aegis40_neutronics_FER.ipynb) ---
    P_th:  float = 125.0e6     # core thermal power [W]                 (OpenMC CORE_POWER_MWT)
    p_mpa: float = 12.8        # system pressure [MPa]                  (OpenMC)
    T_in:  float = 531.15      # core inlet temperature [K] (258 C)

    # --- coolant transport @ T_avg 556 K, 12.8 MPa (design basis) ---
    rho:   float = 748.0       # density [kg/m3]                        (OpenMC RHO_WATER_NOM)
    cp:    float = 5350.0      # specific heat [J/kg.K]
    mu:    float = 9.1e-5      # dynamic viscosity [Pa.s]
    beta:  float = 2.7e-3      # volumetric thermal expansion [1/K]

    # --- core flow geometry (OpenMC: 264*37 pins; A_f=pitch^2-piD^2/4) ---
    N_pin: int   = 9768        # total fuel pins                        (264 * 37)
    A_f:   float = 88.2e-6     # per-subchannel flow area [m2]
    D_h:   float = 11.79e-3    # hydraulic diameter [m]
    L_core: float = 2.0        # active (heated) length [m]             (OpenMC 200 cm)

    # --- LOOP geometry: the two NuScale/MASLWR-class design knobs ---
    H_tc:   float = 4.0        # thermal-centre elevation SINK-SOURCE [m]  (FER design point)
    # lumped loss coeff referenced to CORE velocity, EXCLUDING core wall friction
    # (grids + SG primary side + plena + riser/downcomer turns); core friction is
    # added on top, computed from Re each iteration.
    K_form: float = 12.0       # form/other losses [-]
    n_grid: int   = 7          # spacer grids
    K_grid: float = 0.7        # loss per grid [-]

    @property
    def A_core(self) -> float:
        return self.N_pin * self.A_f          # total core flow area [m2]


def friction_factor(Re: float) -> float:
    """Darcy f: laminar 64/Re, else Blasius (smooth, 4e3<Re<1e5)."""
    if Re < 2300.0:
        return 64.0 / max(Re, 1.0)
    return 0.316 / Re**0.25


def solve(cfg: Config, P=None, max_it=200, tol=1e-8):
    """Fixed-point solve for mdot. Returns a results dict."""
    P = cfg.P_th if P is None else P
    A = cfg.A_core
    Kg = cfg.n_grid * cfg.K_grid
    # initial guess: cube-root law with a nominal K_tot=18
    K0 = cfg.K_form + Kg + 4.0
    mdot = (2 * cfg.rho**2 * A**2 * G_CONST * cfg.H_tc * cfg.beta * P
            / (cfg.cp * K0))**(1.0 / 3.0)
    for _ in range(max_it):
        u = mdot / (cfg.rho * A)                       # core bulk velocity
        Re = cfg.rho * u * cfg.D_h / cfg.mu
        f = friction_factor(Re)
        K_fric = f * cfg.L_core / cfg.D_h              # core wall friction
        K_tot = cfg.K_form + Kg + K_fric
        mdot_new = (2 * cfg.rho**2 * A**2 * G_CONST * cfg.H_tc * cfg.beta * P
                    / (cfg.cp * K_tot))**(1.0 / 3.0)
        if abs(mdot_new - mdot) < tol * mdot:
            mdot = mdot_new
            break
        mdot = 0.5 * (mdot + mdot_new)                 # under-relax
    # final derived quantities
    u = mdot / (cfg.rho * A)
    Re = cfg.rho * u * cfg.D_h / cfg.mu
    f = friction_factor(Re)
    K_fric = f * cfg.L_core / cfg.D_h
    K_tot = cfg.K_form + Kg + K_fric
    G = mdot / A
    dT = P / (mdot * cfg.cp)
    T_out = cfg.T_in + dT
    Tsat, _ = sat_props(cfg.p_mpa)
    dp_loss = K_tot * mdot**2 / (2 * cfg.rho * A**2)
    dp_dr = G_CONST * cfg.H_tc * cfg.rho * cfg.beta * dT
    return dict(P=P, mdot=mdot, G=G, u=u, Re=Re, f=f,
                K_fric=K_fric, K_grid=Kg, K_form=cfg.K_form, K_tot=K_tot,
                dT=dT, T_out=T_out, Tsat=Tsat,
                dp_dr=dp_dr, dp_loss=dp_loss,
                head_m=dp_dr / (cfg.rho * G_CONST))


def main(argv=None):
    cfg = Config()
    ap = argparse.ArgumentParser(description="Aegis-40 natural-circulation loop solver")
    ap.add_argument('--P',     type=float, default=cfg.P_th / 1e6, help="thermal power [MW]")
    ap.add_argument('--Htc',   type=float, default=cfg.H_tc,  help="thermal-centre elevation [m]")
    ap.add_argument('--Kform', type=float, default=cfg.K_form, help="lumped form loss (excl. core friction & grids) [-]")
    ap.add_argument('--ngrid', type=int,   default=cfg.n_grid, help="number of spacer grids")
    ap.add_argument('--Kgrid', type=float, default=cfg.K_grid, help="loss per grid [-]")
    ap.add_argument('--beta',  type=float, default=cfg.beta,  help="thermal expansion [1/K]")
    ap.add_argument('--sweep', action='store_true', help="print mdot~P^1/3 power sweep")
    a = ap.parse_args(argv)
    cfg.P_th = a.P * 1e6
    cfg.H_tc, cfg.K_form, cfg.n_grid, cfg.K_grid, cfg.beta = a.Htc, a.Kform, a.ngrid, a.Kgrid, a.beta

    r = solve(cfg)
    print("=" * 72)
    print(" Aegis-40 natural-circulation loop  (1-D buoyancy balance, mdot~P^1/3)")
    print("=" * 72)
    print(f" Thermal power P_th     : {cfg.P_th/1e6:8.1f} MW")
    print(f" Pressure / T_in        : {cfg.p_mpa:8.2f} MPa / {cfg.T_in:.1f} K")
    print(f" Core flow area A_core  : {cfg.A_core:8.4f} m2   ({cfg.N_pin} pins x {cfg.A_f*1e6:.1f} mm2)")
    print(f" LOOP knobs  H_tc/K_form: {cfg.H_tc:8.2f} m / {cfg.K_form:.1f}  (+{cfg.n_grid} grids x {cfg.K_grid}, +core friction)")
    print("-" * 72)
    print(f" Driving head           : {r['dp_dr']/1e3:8.2f} kPa  ({r['head_m']*1e3:.1f} mm water col.)")
    print(f" Loop losses (=driving) : {r['dp_loss']/1e3:8.2f} kPa")
    print(f" K_tot breakdown        : form {r['K_form']:.1f} + grids {r['K_grid']:.1f} + core-fric {r['K_fric']:.2f} = {r['K_tot']:.2f}")
    print(f" Reynolds / f (Darcy)   : {r['Re']:8.0f} / {r['f']:.4f}")
    print("-" * 72)
    print(f" >>> Core mass flow mdot: {r['mdot']:8.1f} kg/s")
    print(f" >>> Core mass flux  G  : {r['G']:8.1f} kg/m2s   (u_core {r['u']:.3f} m/s)")
    print(f" >>> Core dT            : {r['dT']:8.1f} K   ->  T_out {r['T_out']:.1f} K")
    boil = r['T_out'] - r['Tsat']
    tag = "EXCEEDS Tsat -> onset of subcooled BOILING" if boil > 0 else "subcooled (no boiling)"
    print(f"     T_out vs Tsat      : {r['Tsat']:8.1f} K  (margin {-boil:+.1f} K)  {tag}")
    print("=" * 72)
    print(" Verdict: natural circulation sits on the LOW-flow / high-dT branch.")
    print(f"          G ~ {r['G']:.0f}  (NOT ~1800) -> feed this G into mdnbr.py / thermal_stack.py.")
    print("=" * 72)

    if a.sweep:
        print("\n Power sweep (mdot ~ P^1/3 trend, for NuScale/MASLWR validation):")
        print(f" {'P[MW]':>7} {'mdot[kg/s]':>11} {'G[kg/m2s]':>10} {'u[m/s]':>7} {'dT[K]':>7} {'Tout[K]':>8}")
        for Pf in (0.10, 0.25, 0.50, 0.75, 1.00):
            rr = solve(cfg, P=Pf * cfg.P_th)
            print(f" {Pf*cfg.P_th/1e6:7.1f} {rr['mdot']:11.1f} {rr['G']:10.1f} "
                  f"{rr['u']:7.3f} {rr['dT']:7.1f} {rr['T_out']:8.1f}")
    return r


if __name__ == "__main__":
    main()
