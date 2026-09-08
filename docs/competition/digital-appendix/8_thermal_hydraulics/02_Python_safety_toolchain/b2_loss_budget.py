#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aegis-40  --  Natural-circulation loop FORM-LOSS BUDGET (analytical)
=========================================================================

Purpose: replace the *assumed* lumped K_form = 12 in `tools/natcirc.py` with a
geometry-built estimate, AND set the validation target for the eventual loop CFD
(see docs/Aegis40_B2_natcirc_K_CFD_plan.md). This is the "lock the geometry" step:
every segment dimension is made explicit here, so the CFD and natcirc share one
geometry of record.

Method (single-phase, rho const, mass-conservative):
  - The loop is split into segments. The CORE friction + spacer grids are EXCLUDED
    (they already live in natcirc.py as K_fric + K_grid); this budget is exactly
    the "K_form" that natcirc.py takes as an input.
  - Each segment's local loss zeta_i is referenced to the LOCAL velocity, then
    converted to the CORE-velocity reference by  K_i = zeta_i * (A_core/A_i)^2
    (continuity: u_i = u_core * A_core/A_i).  Friction K = f*L/Dh, same referral.
  - K_form = sum(K_i).

Handbook zeta values (Idel'chik / Crane TP-410), all standard:
  - sudden expansion (area ratio sigma=A_small/A_large): zeta = (1 - sigma)^2  (on small-side V)
  - sudden contraction:                                   zeta ~ 0.5*(1 - sigma) (on small-side V)
  - 180-deg turn (plenum crossover):                      zeta ~ 1.5 - 2.2       (use 2.0)
  - tube-bundle shell-side (helical SG), crossflow:       N_eff rows * zeta_row  (zeta_row ~0.4-1.0)

STATUS OF EACH DIMENSION is tagged [firm] / [scope] / [assumed]. The [scope]/
[assumed] ones are what a loop CFD (or the mechanical layout) must lock. The SG
shell-side bundle loss and the two plenum turns are the dominant + most uncertain
terms -> they are the CFD's main job to pin down.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

G_RHO = 748.0          # kg/m3  coolant @ 283 C / 12.8 MPa  [firm, design basis]
MU    = 9.1e-5         # Pa.s                                  [firm]

# ---- core (reference) ----------------------------------------------------
N_PIN   = 9768
A_F     = 88.2e-6      # subchannel flow area [m2]            [firm]
A_CORE  = N_PIN * A_F  # 0.8617 m2  total core flow area      [firm]
DH_CORE = 11.79e-3

def darcy(Re):
    return 64.0/max(Re,1.0) if Re < 2300 else 0.316/Re**0.25

# ---- loop segment geometry of record -------------------------------------
# area [m2] from bore diameters (design-basis Section B-B reads + elevation budget).
# tag: firm = locked geometry; scope = scoping number in design basis; assumed = my estimate.
def circ(d):  # area of a circle of bore d [m]
    return math.pi*0.25*d*d
def annulus(do, di):
    return math.pi*0.25*(do*do - di*di)

D_RISER_ABOVE = 0.960     # [scope] riser ID above core (B-B 960/1000)
D_RISER_NECK  = 0.760     # [scope] upper-neck ID (B-B 760/800) (design decision: kept at 760)
D_STANDPIPE   = 1.315     # [scope] upper standpipe ID under dome (B-B 1315/1400)
D_RISER_OD    = 1.000     # [scope] riser OD above core
D_VESSEL_ID   = 3.200     # [scope] vessel ID ~3.0-3.5 m (binding dimension); nominal 3.2
L_RISER       = 1.5       # [scope] core-outlet to SG bottom (elev 2.9->4.4)
L_SG          = 3.0       # [scope] SG primary-side height (elev 4.4->7.4)
L_DOWNCOMER   = 3.5       # [assumed] SG bottom -> lower plenum return path

# SG shell-side (helical bundle in the downcomer annulus)
A_SG_ANNULUS  = annulus(D_VESSEL_ID, D_RISER_OD)   # gross annulus area
SG_BLOCKAGE   = 0.55      # [assumed] fraction of annulus blocked by tubes -> free-flow factor
A_SG_FREE     = A_SG_ANNULUS * (1.0 - SG_BLOCKAGE)
SG_N_ROWS     = 14        # [assumed] effective tube rows crossed (helical) -> form loss
SG_ZETA_ROW   = 0.6       # [assumed] loss per row (Idel'chik staggered bank, low Re)

# plenum turns
ZETA_TURN_TOP = 2.0       # [assumed] 180-deg riser->annulus crossover at top
ZETA_TURN_BOT = 1.8       # [assumed] 180-deg lower-plenum turn into core inlet


def k_to_core(zeta, A_local):
    """Refer a local-velocity zeta to the CORE velocity."""
    return zeta * (A_CORE / A_local)**2


def friction_K(L, Dh, A_local, mdot):
    u = mdot/(G_RHO*A_local)
    Re = G_RHO*u*Dh/MU
    f = darcy(Re)
    return (f*L/Dh) * (A_CORE/A_local)**2, Re, f


def budget(mdot):
    """Return list of (name, K_core, note) and the total, at a given core mdot."""
    rows = []
    # 1) core exit -> riser (expansion: A_core -> riser_above)
    sig = min(A_CORE, circ(D_RISER_ABOVE))/max(A_CORE, circ(D_RISER_ABOVE))
    rows.append(("core-exit expansion", k_to_core((1-sig)**2, min(A_CORE,circ(D_RISER_ABOVE))), "(1-sig)^2"))
    # 2) riser neck contraction then expansion (760 neck)
    A_neck = circ(D_RISER_NECK); A_ab = circ(D_RISER_ABOVE)
    sig_c = A_neck/A_ab
    rows.append(("riser neck contraction", k_to_core(0.5*(1-sig_c), A_neck), "0.5(1-sig)"))
    rows.append(("riser neck re-expansion", k_to_core((1-sig_c)**2, A_neck), "(1-sig)^2"))
    # 3) riser friction (use above-core bore)
    Kf_r, Re_r, f_r = friction_K(L_RISER, D_RISER_ABOVE, A_ab, mdot)
    rows.append(("riser friction", Kf_r, f"f*L/Dh Re={Re_r:.0f}"))
    # 4) top crossover 180-deg turn (referenced to riser velocity)
    rows.append(("top crossover turn", k_to_core(ZETA_TURN_TOP, A_ab), "180-deg"))
    # 5) SG shell-side bundle (dominant) -- referenced to SG free-flow velocity
    rows.append(("SG bundle (crossflow)", k_to_core(SG_N_ROWS*SG_ZETA_ROW, A_SG_FREE),
                 f"{SG_N_ROWS}rows x {SG_ZETA_ROW}"))
    # 6) SG friction along the annulus (hydraulic dia ~ gap)
    Dh_sg = 4*A_SG_FREE / (math.pi*(D_VESSEL_ID + D_RISER_OD))   # rough wetted-perim Dh
    Kf_sg, Re_sg, f_sg = friction_K(L_SG, Dh_sg, A_SG_FREE, mdot)
    rows.append(("SG annulus friction", Kf_sg, f"Dh={Dh_sg*1e3:.0f}mm Re={Re_sg:.0f}"))
    # 7) downcomer friction (below SG)
    A_dc = annulus(D_VESSEL_ID, D_RISER_OD)
    Dh_dc = D_VESSEL_ID - D_RISER_OD
    Kf_dc, Re_dc, f_dc = friction_K(L_DOWNCOMER, Dh_dc, A_dc, mdot)
    rows.append(("downcomer friction", Kf_dc, f"Re={Re_dc:.0f}"))
    # 8) lower-plenum turn into core (contraction + 180)
    rows.append(("lower-plenum turn", k_to_core(ZETA_TURN_BOT, A_dc), "180-deg"))
    sig_in = A_CORE/A_dc
    rows.append(("core-inlet contraction", k_to_core(0.5*(1-sig_in), A_CORE), "0.5(1-sig)"))
    total = sum(r[1] for r in rows)
    return rows, total


def main():
    # iterate mdot with natcirc to be self-consistent: start from K=12 guess
    import natcirc
    # nominal natcirc mdot at H_tc 4, K_form 12 -> ~467 kg/s
    cfg = natcirc.Config(); cfg.H_tc = 4.0; cfg.K_form = 12.0
    r0 = natcirc.solve(cfg)
    mdot = r0['mdot']
    rows, K = budget(mdot)

    print("="*72)
    print(" Aegis-40  --  natural-circ loop FORM-LOSS budget (analytical)")
    print(f" referenced to core velocity; core A {A_CORE:.4f} m2; mdot {mdot:.0f} kg/s")
    print("="*72)
    print(f" {'segment':<26}{'K(core-ref)':>12}   note")
    print("-"*72)
    for name, k, note in rows:
        print(f" {name:<26}{k:>12.3f}   {note}")
    print("-"*72)
    print(f" {'K_form (sum)':<26}{K:>12.3f}   vs assumed 12.0 in natcirc.py")
    print("="*72)
    # feed back into natcirc + MDNBR
    cfg.K_form = K
    r = natcirc.solve(cfg)
    print(f" With K_form={K:.1f}:  G {r['G']:.0f} kg/m2s  (was {r0['G']:.0f} at K=12),  "
          f"core dT {r['dT']:.1f} K")
    try:
        import mdnbr
        m = mdnbr.Config(p_mpa=12.8, T_in=531.15, G=r['G'], cp=5350.0, L=2.0,
                         D_co=9.52e-3, D_h=11.79e-3, A_flow=88.2e-6,
                         qp_hot_peak=13024.0, Fz=1.286, Le_ratio=1.3125, n=200)
        prof = mdnbr.build_profile(m); dHsub = m.cp*(prof['Tsat']-m.T_in)
        mn = min(mdnbr.bowring_chf(m, prof, i, dHsub)/prof['qpp'][i]
                 for i in range(len(prof['z'])) if prof['qpp'][i] > 0)
        print(f" -> MDNBR (Bowring) {mn:.2f} at the budget-K flow.")
    except Exception as e:
        print(f" (MDNBR step skipped: {e})")
    print("-"*72)
    print(" DOMINANT + MOST UNCERTAIN (the CFD's job to pin down): SG bundle loss")
    print(" and the two 180-deg plenum turns. [scope]/[assumed] dims must be locked")
    print(" against the vessel layout before trusting the absolute K.")
    print("="*72)


if __name__ == "__main__":
    main()
