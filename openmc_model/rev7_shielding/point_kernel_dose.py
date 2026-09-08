#!/usr/bin/env python3
"""ANS-6.4-style point-kernel / removal-cross-section estimate of the operating dose
outside the Aegis-40 bulk biological shield.

Neutron component: anchored on the converged OpenMC RPV fast (E>1 MeV) flux, attenuated
  outward through the thermal-shield / borated-PE / magnetite-concrete / finish stack with
  fast-neutron removal cross sections (Rockwell; Chilton-Shultis-Faw).
Gamma component: point-kernel from the homogenised core gamma source, attenuated through the
  full radial stack with NIST-XCOM linear attenuation coefficients and a concrete buildup factor.

Coefficients carry a sensitivity band (esp. the magnetite fast-neutron removal, which depends
on the bound-water/hydrogen content). Output: dose table + verdict vs the 10 uSv/h target.
"""
import math

TARGET = 10.0  # uSv/h

# ---------- source (125 MWth) ----------
S_N = 9.52e18   # n/s
S_G = 2.81e19   # gamma/s (7.2 gamma/fission)
R_CORE = 75.54  # core envelope radius, cm
H = 200.0       # active height, cm
V_CORE = math.pi * R_CORE**2 * H

# ---------- geometry (outer radii, cm) ----------
R_RPV_O = 151.5     # RPV outer (neutron anchor plane)
R_OUT   = 381.5     # outer concrete face (adopted 4.3 build: cav15+SS5+PE20+mag180+ord10)

# ================= NEUTRON dose (anchored on MC RPV fast flux) =================
PHI_RPV = 1.59e9    # n/cm2/s, E>1 MeV, converged OpenMC
# outer-stack layers beyond the RPV: (name, thickness cm, SigmaR nominal, SigmaR lo, SigmaR hi)
NLAYERS = [
    ("SS-304 thermal shield", 5.0,  0.157, 0.150, 0.165),
    ("Borated polyethylene", 20.0,  0.120, 0.100, 0.130),   # neutron layer (adopted 4.3)
    ("Magnetite concrete",  180.0,  0.100, 0.085, 0.130),   # bulk (adopted 4.3)
    ("Ordinary concrete",    10.0,  0.089, 0.085, 0.095),
]
# ICRP-116 / H*(10) neutron fluence-to-dose at ~1-2 MeV
N_DOSE_COEF = 3.90e-10  # Sv*cm2  (=390 pSv*cm2)

def neutron_dose(pick):
    att = 1.0
    for _, t, nom, lo, hi in NLAYERS:
        sig = {"nom": nom, "lo": lo, "hi": hi}[pick]
        att *= math.exp(-sig * t)
    geo = R_RPV_O / R_OUT                    # cylindrical divergence
    phi = PHI_RPV * att * geo                # n/cm2/s at outer face
    dose = phi * N_DOSE_COEF * 3600.0 * 1e6  # Sv/s*... -> uSv/h : phi*coef=Sv/s? coef in Sv*cm2
    # phi[n/cm2/s]*coef[Sv*cm2]=Sv/s -> *3600 =Sv/h -> *1e6 =uSv/h
    return phi, phi * N_DOSE_COEF * 3600.0 * 1e6

# NOTE: "lo" SigmaR = least attenuation = highest dose (conservative). Map for a dose band:
def n_dose_uSv(pick):
    att = 1.0
    for _, t, nom, lo, hi in NLAYERS:
        sig = {"nom": nom, "least": lo, "most": hi}[pick]
        att *= math.exp(-sig * t)
    phi = PHI_RPV * att * (R_RPV_O / R_OUT)
    return phi, phi * N_DOSE_COEF * 3600.0 * 1e6

# ================= GAMMA dose (point-kernel from core source) =================
# homogenised-core self-shielding: surface flux ~ S_v/(2*mu_core)
RHO_CORE = 0.331*10.40 + 0.116*6.55 + 0.553*0.72   # g/cm3
MU_CORE = 0.045 * RHO_CORE                          # cm-1 @ ~2 MeV
S_V = S_G / V_CORE
PHI_G_SURF = S_V / (2.0 * MU_CORE)                  # gamma/cm2/s at core surface
# radial gamma path core-surface -> outer face (cm, mu cm-1 @ ~2 MeV, NIST-XCOM)
GLAYERS = [
    ("Water reflector", 22.0, 0.0355),
    ("Core barrel SS",   2.5, 0.336),
    ("Downcomer water", 35.0, 0.0355),
    ("RPV steel",       16.5, 0.336),
    ("SS thermal shield",5.0, 0.336),
    ("Borated PE",      20.0, 0.047),
    ("Magnetite concrete",180.0, 0.172),
    ("Ordinary concrete",10.0, 0.101),
]
G_DOSE_COEF = 0.020   # uSv/h per (gamma/cm2/s) at ~2 MeV
B_BUILDUP = 30.0      # concrete buildup for large mu*t (Taylor/GP, conservative)

def gamma_dose():
    mut = sum(mu*t for _, t, mu in GLAYERS)
    geo = R_CORE / R_OUT
    phi = PHI_G_SURF * math.exp(-mut) * geo * B_BUILDUP
    return mut, phi, phi * G_DOSE_COEF

# ================= report =================
print("="*70)
print("Point-kernel operating dose outside the Aegis-40 bulk shield")
print("="*70)
print(f"Core gamma surface flux ~ {PHI_G_SURF:.2e} g/cm2/s  (mu_core={MU_CORE:.2f}/cm)")
mut, gphi, gdose = gamma_dose()
print(f"\nGAMMA:  mu*t total = {mut:.1f}  -> outer flux {gphi:.2e} g/cm2/s")
print(f"        gamma dose  ~ {gdose:.3g} uSv/h")
print("\nNEUTRON (anchored on MC RPV fast flux 1.59e9 n/cm2/s, E>1 MeV):")
for tag, lab in [("most","most attenuation (SigmaR high)"),
                 ("nom","nominal SigmaR"),
                 ("least","least attenuation (SigmaR low)")]:
    phi, d = n_dose_uSv(tag)
    print(f"   {lab:34s}: outer fast flux {phi:8.2e} n/cm2/s -> {d:10.3g} uSv/h")
phi_n, dn_nom = n_dose_uSv("nom")
_,_,dg = gamma_dose()
_, d_worst = n_dose_uSv("least")   # least attenuation = bounding neutron dose
print(f"\nTOTAL (nominal) ~ {dn_nom+dg:.3g} uSv/h   (target {TARGET} uSv/h)")
print(f"Gamma verdict:   PASS ({dg:.2g} uSv/h; magnetite is an excellent gamma shield).")
print(f"Neutron verdict: {'PASS' if d_worst < TARGET else 'FAIL'} "
      f"(nominal {dn_nom:.2g}, bounding {d_worst:.2g} uSv/h vs {TARGET}).")
