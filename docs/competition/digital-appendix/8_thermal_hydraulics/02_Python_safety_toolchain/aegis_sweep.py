#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 natural-circulation feasibility sweep.

Inputs are LOCKED to the OpenMC core model (aegis40_3d_core_notebook_rev6):
geometry, materials, T_avg and peaking all come from that run, so the T-H setup
is consistent with the neutronics 1-for-1.  For natural circulation the core
flow G is an OUTPUT of a 1-D buoyancy balance (natcirc) that depends on the loop
geometry (riser-to-SG thermal-centre height H_tc, lumped loss K_form) — the two
real design knobs.  We sweep them over a plausible range and, for each resulting
G, compute MDNBR (W-3 + Tong) and PCT (Dittus-Boelter + conduction + Jens-Lottes
boiling).  T_in is derived per point so the core-average T stays at the OpenMC
T_avg = 283 C (= 556 K) — the consistency link to the neutronics.

Run:  python3 tools/aegis_sweep.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import natcirc
import mdnbr
import thermal_stack as ts

# ─────────────────────────────────────────────── OpenMC-consistent inputs
P_TH   = 125.0e6          # W   core thermal power
P_MPA  = 12.8             # MPa system pressure (rho 748 @ 283 C => ~12.8)
T_AVG  = 556.0            # K   core-average coolant T  (OpenMC T_MOD_K)
# coolant @ 283 C / 12.8 MPa
RHO, CP, MU, KW, PR, BETA = 748.0, 5350.0, 9.1e-5, 0.566, 0.87, 2.7e-3
# pin geometry (cm in OpenMC -> m)
R_F, R_CI, R_CO = 0.40958e-2, 0.41873e-2, 0.476e-2     # pellet / clad in / clad out
D_CO  = 2 * R_CO
PITCH = 1.2623e-2
A_F   = PITCH**2 - math.pi * D_CO**2 / 4.0              # subchannel flow area
D_H   = 4 * A_F / (math.pi * D_CO)                      # hydraulic dia (rod-only)
N_PIN = 9768             # 264 fuel pins * 37 FA
L     = 2.0              # active length
# peaking — COLR design envelope (cycle-resolved OpenMC record, docs/neutronics_cycle_record.md):
# cycle-resolved BOC 1.937/1.513/1.280 · MOC-hump 2.435/1.729/1.408 · EOC 2.121/1.497/1.417;
# safety design basis = the MOC Gd-hump envelope F_dH 1.75 / F_z 1.41 (F_q = 2.4675).
# Real-shape check (cycle_mdnbr.py --shapes): cosine ~2-4 % optimistic -> binding quotes real-shape.
F_Q, F_DH, F_Z = 2.4675, 1.750, 1.410
LE_RATIO = 1.13334       # Le 2.2667 / L 2.0 -> F_z 1.410 (F_z = a/sin a, a = pi/2/LE_RATIO)
# solids
H_GAP, K_FUEL, K_CLAD = 5246.0, 3.5, 16.0              # h_gap=0.48/9.15e-5 (gap 91.5um) / UO2 / Zr-4

QP_AVG  = P_TH / (N_PIN * L)               # core-avg linear power [W/m]
QP_PEAK = QP_AVG * F_Q                      # hot-pin peak linear power
A_CORE  = N_PIN * A_F


def _coolant_cfg(G, T_in):
    return mdnbr.Config(p_mpa=P_MPA, T_in=T_in, G=G, cp=CP, L=L, D_co=D_CO,
                        D_h=D_H, A_flow=A_F, qp_hot_peak=QP_PEAK, Fz=F_Z,
                        Le_ratio=LE_RATIO, n=200)


def mdnbr_of(G, T_in):
    cfg = _coolant_cfg(G, T_in)
    prof = mdnbr.build_profile(cfg)
    dHsub = cfg.cp * (prof["Tsat"] - cfg.T_in)
    dn = []
    for i in range(len(prof["z"])):
        qeu = mdnbr.w3_chf_eu(cfg, prof["xq"][i], dHsub)
        F, _ = mdnbr.tong_F(cfg, prof, i)
        dn.append((qeu / F) / prof["qpp"][i])
    return min(dn), prof["Tsat"]


def pct_of(G, T_in):
    cc = _coolant_cfg(G, T_in)
    st = ts.StackConfig(r_f=R_F, r_ci=R_CI, r_co=R_CO, k_fuel=K_FUEL, k_clad=K_CLAD,
                        h_gap=H_GAP, mu=MU, k_w=KW, Pr=PR, corr="db")
    h, Re, Nu, _ = ts.film_h(cc, st)
    prof = ts.build_profile(cc)
    rows, _, _ = ts.stack(cc, st, prof, h, boiling=True)
    pct = max(r[3] for r in rows)              # clad inner
    tf = max(r[5] for r in rows)               # fuel centre
    return pct, tf, h, Re, Nu


def natcirc_G(Htc, Kform):
    cfg = natcirc.Config(P_th=P_TH, p_mpa=P_MPA, T_in=T_AVG, rho=RHO, cp=CP, mu=MU,
                         beta=BETA, N_pin=N_PIN, A_f=A_F, D_h=D_H, L_core=L,
                         H_tc=Htc, K_form=Kform, n_grid=7, K_grid=0.7)
    r = natcirc.solve(cfg)
    return r["G"], r["u"], r["dT"], r["Re"]


def run_point(Htc, Kform):
    G, u, dT, Re_loop = natcirc_G(Htc, Kform)
    T_in = T_AVG - dT / 2.0                     # hold core-avg T at OpenMC T_avg
    T_out = T_in + dT
    md, Tsat = mdnbr_of(G, T_in)
    pct, tf, h, Re, Nu = pct_of(G, T_in)
    return dict(Htc=Htc, Kform=Kform, G=G, u=u, dT=dT, T_in=T_in, T_out=T_out,
                Tsat=Tsat, mdnbr=md, pct=pct, tf=tf, h=h, Nu=Nu)


def main():
    print("=" * 94)
    print(" AEGIS-40 — natural-circulation feasibility sweep  (OpenMC-consistent T-H)")
    print("=" * 94)
    print(f" Power {P_TH/1e6:.0f} MWth | P {P_MPA} MPa | T_avg {T_AVG-273.15:.0f} C | "
          f"pins {N_PIN} | A_core {A_CORE:.3f} m2")
    print(f" Pin: pellet {2*R_F*1e3:.2f} / clad {D_CO*1e3:.2f} mm | pitch {PITCH*1e3:.2f} | "
          f"A_f {A_F*1e6:.1f} mm2 | D_h {D_H*1e3:.2f} mm")
    print(f" Power shape: q'_avg {QP_AVG/1e3:.2f} kW/m -> hot-pin peak {QP_PEAK/1e3:.2f} kW/m "
          f"(F_q {F_Q}, F_dH {F_DH}, F_z {F_Z}) | q''_peak {QP_PEAK/(math.pi*D_CO)/1e6:.3f} MW/m2")
    h0, Re0, Nu0 = pct_of(700, T_AVG)[2:]
    print(f" Film: Dittus-Boelter  Re~{Re0:,.0f}  Nu {Nu0:.0f}  (Tsat {mdnbr.sat_props(P_MPA)[0]-273.15:.0f} C)")

    # ---- main sweep over riser height at nominal losses ----
    print("-" * 94)
    print(f" SWEEP over H_tc (riser-to-SG elevation) at K_form = 12:")
    print(f"{'H_tc[m]':>8}{'G':>8}{'u[m/s]':>8}{'coreDT':>8}{'T_in[C]':>9}"
          f"{'T_out[C]':>9}{'MDNBR':>8}{'PCT[C]':>8}{'Tfuel[C]':>9}{'verdict':>9}")
    for Htc in (3, 4, 5, 6, 7, 8):
        r = run_point(Htc, 12.0)
        v = "PASS" if r["mdnbr"] > 1.3 else "FAIL"
        print(f"{Htc:>8.0f}{r['G']:>8.0f}{r['u']:>8.2f}{r['dT']:>8.1f}"
              f"{r['T_in']-273.15:>9.1f}{r['T_out']-273.15:>9.1f}"
              f"{r['mdnbr']:>8.2f}{r['pct']-273.15:>8.0f}{r['tf']-273.15:>9.0f}{v:>9}")

    # ---- MDNBR sensitivity grid (H_tc x K_form) ----
    print("-" * 94)
    print(" MDNBR sensitivity grid  (rows H_tc, cols K_form):")
    Ks = (8, 12, 18)
    hdr = "H_tc/K"
    print(f"{hdr:>8}" + "".join(f"{k:>10}" for k in Ks))
    for Htc in (3, 4, 5, 6, 7, 8):
        cells = []
        for K in Ks:
            r = run_point(Htc, float(K))
            cells.append(f"{r['mdnbr']:.2f}({r['G']:.0f})")
        print(f"{Htc:>8.0f}" + "".join(f"{c:>10}" for c in cells))
    print("   cell = MDNBR(G);  MDNBR>1.3 = PASS")
    print("=" * 94)
    print(" NOTE: T_in derived per point so core-avg T = OpenMC 283 C. Hot channel uses")
    print(" core-avg G (no flow redistribution) -> conservative. q'' peak & enthalpy rise")
    print(" both from the OpenMC F_q/F_dH (separable). beta, gap-h are property estimates.")
    print("=" * 94)


if __name__ == "__main__":
    main()
