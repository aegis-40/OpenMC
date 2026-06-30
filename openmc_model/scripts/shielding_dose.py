"""Aegis-40 radial biological-shield design + operating dose rates (FER radiation-protection section).

SEMI-ANALYTIC shield calc (point-kernel / removal-cross-section for fast neutrons,
broad-beam TVL + buildup for gammas), to be ANCHORED by an OpenMC fixed-source /
RPV-surface flux tally from the steel-internals core run. See shielding_dose.md.

Method & data sources
---------------------
* Fast-neutron attenuation: Albert-Welton removal cross sections Sigma_R [1/cm]
  (Shultis & Faw, "Radiation Shielding"; Lamarsh App. tables). Valid behind a
  hydrogenous medium (concrete + downcomer water provide this).
* Gamma attenuation: broad-beam tenth-value layers (TVL) with buildup folded in
  (NCRP-151 / IAEA SRS-47, ordinary concrete rho=2.3, Co-60-like ~1.25-1.5 MeV).
* Geometry: cylindrical core; radial divergence handled by (r_in/r_out) factor.
* Fluence-to-dose: ICRP-116 ambient dose equivalent H*(10) per unit fluence,
  representative ~1-2 MeV (neutron) and ~1.5 MeV (photon).

EVERY absolute flux below traces to ONE anchor: the fast flux leaving the core
edge (CORE_EDGE_FAST_FLUX). It is a physics-based first estimate flagged
'REPLACE WITH TALLY' -- swap in the value the steel-internals run tallies at the
core/baffle interface and the whole shield re-sizes self-consistently.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "competition", "shielding")
os.makedirs(OUT, exist_ok=True)

# ============================================================== CONFIG
CORE_POWER_MWT = 125.0          # matches notebook CORE_POWER_MWT
R_CORE         = 61.0           # cm, area-equivalent cyl radius of the 108 cm core box
ACTIVE_H       = 200.0          # cm

# --- anchor (to be replaced by the RPV-surface flux tally) -----------------
# Core-edge fast flux (E>1 MeV). Estimate from power density:
#   q''' = 125e6 W / (pi*61^2*200 cm3) ~ 53 W/cm3  -> ~half a large PWR (~100),
#   whose core fast flux ~5e13 -> scale ~2.5e13 n/cm2/s at the active-core edge.
CORE_EDGE_FAST_FLUX = 2.5e13    # n/cm2/s  *** REPLACE WITH TALLY ***
# Core-edge gamma flux: prompt+FP-decay+capture gammas are ~3x more numerous than
# fast neutrons leaving the core, ~1.5 MeV average.
CORE_EDGE_GAMMA_FLUX = 3.0 * CORE_EDGE_FAST_FLUX   # gamma/cm2/s

# --- dose targets (IAEA GSR Part 3 / ALARA design) -------------------------
TARGET_DOSE_uSvph = 10.0        # accessible outer shield surface, full power
PLANT_LIFE_Y      = 60.0
CAPACITY_FACTOR   = 0.90

# --- cavity + concrete choice ----------------------------------------------
CAVITY_GAP_CM     = 40.0        # RPV outer -> concrete inner (air/insulation)
CONCRETE          = "ordinary"  # "ordinary" (rho 2.3) or "heavy" (magnetite ~3.7)

# ============================================================== MATERIAL DATA
# Sigma_R [1/cm] fast-neutron removal ; mu_gamma broad-beam effective [1/cm]
#   (mu chosen so ln(10)/mu == broad-beam TVL incl. buildup)
TVL_concrete_ord = 25.0         # cm, ~1.25 MeV gamma, ordinary concrete (NCRP-151)
TVL_concrete_hvy = 16.0         # cm, magnetite/barite heavy concrete
MAT = {
    #               Sigma_R   mu_gamma(1/cm)
    "water":      (0.103,    0.0575),
    "ss304":      (0.158,    0.42),     # baffle / barrel / RPV clad
    "sa508":      (0.156,    0.41),     # RPV low-alloy steel
    "air":        (1.0e-5,   6.0e-5),
    "concrete":   (0.089 if CONCRETE == "ordinary" else 0.145,
                   np.log(10) / (TVL_concrete_ord if CONCRETE == "ordinary" else TVL_concrete_hvy)),
}

# fluence-to-H*(10) -> dose rate [uSv/h] per unit flux [1/cm2/s]   (ICRP-116)
DOSE_N = 1.44e-6     # ~1-2 MeV neutron : 400 pSv*cm2  -> 400e-12*3600*1e6
DOSE_G = 1.44e-8     # ~1.5 MeV photon  :   4 pSv*cm2  ->   4e-12*3600*1e6

# ============================================================== RADIAL BUILD
# (outer radius cm, material, label)  -- core barrel/RPV dims from geometry spec
build = [
    (R_CORE,   "source", "active core"),
    (63.2,     "ss304",  "baffle (2.2 cm SS-304)"),
    (80.0,     "water",  "bypass / reflector water"),
    (82.5,     "ss304",  "core barrel (2.5 cm SS-304)"),
    (140.0,    "water",  "downcomer + SG annulus"),
    (140.5,    "ss304",  "RPV clad (0.5 cm)"),
    (156.5,    "sa508",  "RPV wall (16 cm SA-508)"),
    (156.5 + CAVITY_GAP_CM, "air", "reactor cavity"),
    # concrete appended after sizing
]

def attenuate(layers, phi0_n, phi0_g):
    """Walk layers outward; return per-station radius, fast-n flux, gamma flux, dose."""
    r_prev = R_CORE
    phi_n, phi_g = phi0_n, phi0_g
    rs, fn, fg, dose = [r_prev], [phi_n], [phi_g], [phi_n * DOSE_N + phi_g * DOSE_G]
    for r_out, mat, _lbl in layers[1:]:
        sig_R, mu = MAT[mat]
        t = r_out - r_prev
        geom = r_prev / r_out                      # cylindrical radial divergence
        phi_n *= np.exp(-sig_R * t) * geom
        phi_g *= np.exp(-mu * t) * geom
        rs.append(r_out); fn.append(phi_n); fg.append(phi_g)
        dose.append(phi_n * DOSE_N + phi_g * DOSE_G)
        r_prev = r_out
    return map(np.asarray, (rs, fn, fg, dose))

# ---- 1) attenuate core -> RPV outer -> cavity (no concrete yet) ----------------
rs, fn, fg, dose = attenuate(build, CORE_EDGE_FAST_FLUX, CORE_EDGE_GAMMA_FLUX)
phi_n_cav, phi_g_cav = fn[-1], fg[-1]
r_cav = rs[-1]
# RPV-inner fast flux (for embrittlement) = station just before RPV clad
i_rpv_in = [b[2] for b in build].index("RPV clad (0.5 cm)") - 1
phi_fast_rpv_in = fn[i_rpv_in]

# ---- 2) size the concrete to hit the dose target -------------------------------
sig_R_c, mu_c = MAT["concrete"]
T = 0.0
while True:
    geom = r_cav / (r_cav + T)
    d_n = phi_n_cav * np.exp(-sig_R_c * T) * geom * DOSE_N
    d_g = phi_g_cav * np.exp(-mu_c   * T) * geom * DOSE_G
    if (d_n + d_g) <= TARGET_DOSE_uSvph or T > 400:
        break
    T += 1.0
T_design = T + 10.0     # +10 cm engineering margin
r_outer = r_cav + T_design

# full curve incl. sized concrete (sample through the wall for the plot)
build_full = build + [(r_outer, "concrete", f"biological concrete ({T_design:.0f} cm)")]
rs, fn, fg, dose = attenuate(build_full, CORE_EDGE_FAST_FLUX, CORE_EDGE_GAMMA_FLUX)

# ---- 3) RPV fast fluence (embrittlement) ---------------------------------------
seconds = PLANT_LIFE_Y * CAPACITY_FACTOR * 3.1536e7
rpv_fluence = phi_fast_rpv_in * seconds   # n/cm2  (E>1 MeV)

# ============================================================== REPORT
print("=" * 64)
print("AEGIS-40 RADIAL SHIELD  (semi-analytic; anchor = core-edge fast flux)")
print("=" * 64)
print(f"{'station':30s}{'r[cm]':>8s}{'phi_fast':>12s}{'dose[uSv/h]':>13s}")
for (r_out, mat, lbl), r, f, d in zip(build_full, rs, fn, dose):
    print(f"{lbl:30s}{r:8.1f}{f:12.2e}{d:13.2e}")
print("-" * 64)
print(f"concrete: {CONCRETE} (rho {'2.3' if CONCRETE=='ordinary' else '3.7'}), "
      f"sized {T:.0f} cm + 10 cm margin = {T_design:.0f} cm")
print(f"outer shield surface dose : {dose[-1]:.2f} uSv/h   (target {TARGET_DOSE_uSvph})")
print(f"RPV-inner fast flux       : {phi_fast_rpv_in:.2e} n/cm2/s  (E>1 MeV)")
print(f"RPV fluence @ {PLANT_LIFE_Y:.0f} y, CF {CAPACITY_FACTOR:.2f}: "
      f"{rpv_fluence:.2e} n/cm2   (PTS screen ~1e19)")
print("NOTE: absolute fluxes scale linearly with CORE_EDGE_FAST_FLUX -> "
      "replace with RPV-surface tally and re-run.")

# ---- save table ----------------------------------------------------------------
np.savetxt(os.path.join(OUT, "shield_dose_profile.csv"),
           np.column_stack([rs, fn, fg, dose]),
           header="r_cm,phi_fast_n,phi_gamma,dose_uSv_per_h", delimiter=",", comments="")

# ============================================================== FIGURE 1: dose vs r
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.semilogy(rs, dose, "o-", color="#b5462e", lw=2, ms=5)
ax.axhline(TARGET_DOSE_uSvph, color="#2471a3", ls="--", lw=1.5,
           label=f"design target {TARGET_DOSE_uSvph:.0f} uSv/h")
# shade material layers
colors = {"source": "#f7d7b5", "ss304": "#9aa0a6", "sa508": "#5f6368",
          "water": "#cfe3fb", "air": "#ffffff", "concrete": "#cdbfae"}
r_in = 0.0
for (r_out, mat, lbl) in build_full:
    ax.axvspan(r_in, r_out, color=colors.get(mat, "#eee"), alpha=0.5, zorder=-5)
    r_in = r_out
ax.set_xlabel("radius from core centre  [cm]")
ax.set_ylabel("dose rate  [uSv/h]  (n + gamma)")
ax.set_title("Aegis-40 radial shield — operating dose rate vs depth\n"
             f"(core -> baffle -> barrel -> downcomer -> RPV -> cavity -> "
             f"{T_design:.0f} cm {CONCRETE} concrete)")
ax.set_xlim(0, r_outer + 10)
ax.legend(loc="upper right")
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
p1 = os.path.join(OUT, "shield_dose_vs_radius.png")
fig.savefig(p1, dpi=150); print("wrote", p1)

# ============================================================== FIGURE 2: cross-section
fig, ax = plt.subplots(figsize=(8.5, 7.5))
# draw rings outer-first so inner ones sit on top
r_in_prev = [0.0] + [b[0] for b in build_full[:-1]]
for (r_out, mat, lbl), r_in in sorted(zip(build_full, r_in_prev),
                                      key=lambda x: -x[0][0]):
    ax.add_patch(plt.Circle((0, 0), r_out, color=colors.get(mat, "#eee")))
ax.add_patch(plt.Circle((0, 0), R_CORE, color=colors["source"]))
ax.text(0, 0, "CORE\n125 MWt", ha="center", va="center", fontsize=11, fontweight="bold")

# stacked labels on the right, evenly spread, leader to each layer mid-radius
labels = [(r_out, lbl) for (r_out, mat, lbl) in build_full if mat != "source"]
y_top, y_bot = r_outer * 0.95, -r_outer * 0.95
for k, (r_out, lbl) in enumerate(labels):
    r_mid = 0.5 * (r_out + (labels[k - 1][0] if k else R_CORE))
    y_lab = y_top - (y_top - y_bot) * k / (len(labels) - 1)
    ax.annotate(lbl, xy=(r_mid, 0), xytext=(r_outer * 1.12, y_lab),
                fontsize=8.5, va="center", ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.6, color="0.55",
                                connectionstyle="arc3,rad=0.0"))
ax.set_xlim(-r_outer * 1.05, r_outer * 2.0)
ax.set_ylim(-r_outer * 1.08, r_outer * 1.08)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Aegis-40 integral-RPV radial shield (to scale)")
fig.tight_layout()
p2 = os.path.join(OUT, "shield_cross_section.png")
fig.savefig(p2, dpi=150); print("wrote", p2)
