#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40 F2 -- AOO transient hot-channel MDNBR by the QUASI-STEADY envelope method.
====================================================================================

Most anticipated operational occurrences (AOOs) develop slowly compared with the
pin thermal time constant (~seconds) and trip in <=500 ms, so the transient MDNBR
is bounded by the STEADY MDNBR evaluated at the most adverse (power, flow, pressure)
point reached before scram. We sweep that envelope with the SAME validated
hot-channel + CHF stack as the steady case (mdnbr.py), using the low-flow-valid
Bowring CHF (W-3 is extrapolated at these reduced flows).

Conservatisms (all push MDNBR DOWN, i.e. safe):
  (1) natural-circulation flow self-help is NOT credited -- flow held <= nominal
      even under overpower, although rising buoyancy would actually raise it;
  (2) overpower taken up to the high-neutron-flux trip envelope (118 %);
  (3) Bowring is a bare-tube CHF (no bundle / spacer-grid enhancement).

Limitation: the hot-channel enthalpy rise is single-phase (mdnbr.py); past T_sat it
over-reads bulk T -> use the F1-ii two-phase cap to refine. Bowring uses inlet
subcooling + position, so it is largely insulated from that local over-read.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdnbr

# --- Aegis-40 design point = base 100 % power / 100 % flow (matches mdnbr.py run) ---
# qp_hot_peak = q'_avg(6398 W/m) * F_q.  COLR design envelope (cycle-resolved OpenMC record):
# F_dH 1.75 x F_z 1.41 -> F_q 2.4675 -> 15788 W/m (the MOC Gd-hump envelope = binding
# safety basis; bounds BOC 1.937 and EOC 2.121, so this AOO envelope covers the cycle).
BASE = dict(p_mpa=12.8, T_in=531.15, G=542.0, cp=5350.0, L=2.0,
            D_co=9.52e-3, D_h=11.79e-3, A_flow=88.2e-6,
            qp_hot_peak=15788.0, Fz=1.410, Le_ratio=1.13334, n=200)

LIMIT = 1.3


def mdnbr_at(power_f, flow_f, p_mpa=None, dTin=0.0, chf='bowring'):
    """MDNBR at scaled power/flow (and optional pressure / inlet-T shift)."""
    kw = dict(BASE)
    kw['qp_hot_peak'] = BASE['qp_hot_peak'] * power_f
    kw['G'] = BASE['G'] * flow_f
    kw['T_in'] = BASE['T_in'] + dTin
    if p_mpa is not None:
        kw['p_mpa'] = p_mpa
    cfg = mdnbr.Config(**kw)
    prof = mdnbr.build_profile(cfg)
    dHsub_in = cfg.cp * (prof['Tsat'] - cfg.T_in)
    m = float('inf')
    for i in range(len(prof['z'])):
        if chf == 'bowring':
            qchf = mdnbr.bowring_chf(cfg, prof, i, dHsub_in)
        else:
            X = prof['xq'][i]
            qeu = mdnbr.w3_chf_eu(cfg, X, dHsub_in)
            F, _ = mdnbr.tong_F(cfg, prof, i)
            qchf = qeu / F
        q_loc = prof['qpp'][i]
        if q_loc > 0:
            m = min(m, qchf / q_loc)
    return m


def main():
    powers = [1.00, 1.08, 1.12, 1.18]   # up to the high-neutron-flux trip envelope
    flows = [1.00, 0.90, 0.80]          # natural-circ degradation (no self-help credit)

    print("=" * 66)
    print(" Aegis-40  F2  AOO MDNBR envelope (quasi-steady, Bowring CHF)")
    print(f" base: P {BASE['p_mpa']} MPa, G {BASE['G']:.0f} kg/m2s, q'pk "
          f"{BASE['qp_hot_peak']/1e3:.1f} kW/m (COLR envelope F_q 2.4675);  DNBR limit {LIMIT}")
    print("=" * 66)
    head = " power \\ flow |" + "".join(f"{int(f * 100):>8}%" for f in flows)
    print(head)
    print("-" * len(head))
    worst = (float('inf'), None)
    for pf in powers:
        cells = []
        for ff in flows:
            m = mdnbr_at(pf, ff)
            cells.append(m)
            if m < worst[0]:
                worst = (m, (pf, ff))
        print(f" {int(pf * 100):>5} %      |" + "".join(f"{m:>9.2f}" for m in cells))
    wm, (wp, wf) = worst
    print("-" * len(head))
    verdict = "PASS" if wm > LIMIT else "FAIL"
    print(f" Bounding (Bowring) : MDNBR {wm:.2f} at {int(wp*100)} % power / {int(wf*100)} % flow"
          f"  -> {verdict} (> {LIMIT})")
    print(f" W-3 ref at that pt : {mdnbr_at(wp, wf, chf='w3'):.2f}"
          "   (extrapolated at low G -> conservative)")
    print(" pressure sensitivity at the bounding point (Bowring):")
    for p in (12.8, 12.2, 11.5):
        print(f"   P {p:>4.1f} MPa : MDNBR {mdnbr_at(wp, wf, p_mpa=p):.2f}")
    print(" inlet-T sensitivity at the bounding point (reduced subcooling):")
    for dT in (0.0, 5.0, 10.0):
        print(f"   T_in +{dT:>4.1f} K : MDNBR {mdnbr_at(wp, wf, dTin=dT):.2f}")
    print("=" * 66)


if __name__ == "__main__":
    main()
