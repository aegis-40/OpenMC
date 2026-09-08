#!/usr/bin/env python3
"""Figure 3 - dose-rate radial profile through the Aegis-40 bio-shield.

Neutron dose anchored on the converged OpenMC RPV fast flux (1.59e9 n/cm2/s) and
attenuated outward with fast-neutron removal cross sections; gamma dose from the
core point-kernel, both through the adopted lead-free stack (SS thermal shield /
20 cm borated PE / 180 cm magnetite / finish). Shows the 10 uSv/h target line.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# outer bioshield layers (from RPV outer face): name, r_out cm, SigmaR_n, mu_g
R0 = 151.5                       # RPV outer face
LAYERS = [
    ("cavity (air)",         166.5, 0.0,   0.0),
    ("SS thermal shield",    171.5, 0.157, 0.336),
    ("borated PE",           191.5, 0.120, 0.047),
    ("magnetite concrete",   371.5, 0.100, 0.172),
    ("ordinary concrete",    381.5, 0.089, 0.101),
]
N_DOSE = 1.404                   # uSv/h per (n/cm2/s), ICRP-116 ~1-2 MeV
PHI_RPV = 1.59e9                 # n/cm2/s E>1 MeV at RPV (converged MC)
GDOSE_RPV = 1.255e9             # uSv/h gamma dose at RPV outer (core point-kernel)

def profile():
    r = [R0]; dn = [PHI_RPV * N_DOSE]; dg = [GDOSE_RPV]
    tau_n = tau_g = 0.0; r_prev = R0
    for _, r_out, sR, mu in LAYERS:
        for rr in np.linspace(r_prev, r_out, 60)[1:]:
            dr = rr - r_prev
            tau_n += sR * dr; tau_g += mu * dr
            geo = R0 / rr
            r.append(rr)
            dn.append(PHI_RPV * N_DOSE * np.exp(-tau_n) * geo)
            dg.append(GDOSE_RPV * np.exp(-tau_g) * geo)
            r_prev = rr
    return np.array(r), np.array(dn), np.array(dg)

r, dn, dg = profile()
fig, ax = plt.subplots(figsize=(9, 5.6))
ax.semilogy(r, dn, color="#c0392b", lw=2.4, label="fast-neutron dose")
ax.semilogy(r, dg, color="#2471a3", lw=2.4, ls="--", label="gamma dose")
ax.axhline(10.0, color="#27ae60", lw=1.8, ls=":", label="10 µSv/h ALARA target")

# layer bands + labels
cols = ["#eef2f5", "#d5dbdb", "#f4d35e", "#6b5b4e", "#9aa0a6"]
r_prev = R0
for (name, r_out, _, _), c in zip(LAYERS, cols):
    ax.axvspan(r_prev, r_out, color=c, alpha=0.28, zorder=0)
    ax.text((r_prev + r_out) / 2, 3e9, name, rotation=90, va="top", ha="center",
            fontsize=7.5, color="0.3")
    r_prev = r_out

ax.set_xlim(R0, 381.5); ax.set_ylim(1e-7, 1e10)
ax.set_xlabel("radius from core centreline  [cm]")
ax.set_ylabel("dose rate  [µSv/h]")
ax.set_title("Aegis-40 operating dose-rate profile through the lead-free bio-shield\n"
             "(neutron anchored on converged MC RPV flux; gamma point-kernel)",
             fontsize=11, fontweight="bold")
ax.legend(loc="upper right", fontsize=9)
ax.annotate("outer face:\nn %.2f · γ %.0e µSv/h" % (dn[-1], dg[-1]),
            (381.5, max(dn[-1], 1e-6)), textcoords="offset points", xytext=(-8, 40),
            ha="right", fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color="k", lw=1))
ax.grid(True, which="both", alpha=0.25)

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                   "docs", "competition", "shielding", "figures"))
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "shield_dose_profile.png")
fig.tight_layout(); fig.savefig(p, dpi=160, bbox_inches="tight")
print("wrote", p, "| outer n=%.3g g=%.3g uSv/h" % (dn[-1], dg[-1]))
