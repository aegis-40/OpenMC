"""
Aegis-40 iPWR -- seawater once-through ultimate heat sink & thermal-plume impact.

Replaces the evaporative cooling-tower assumption with a once-through SEAWATER
condenser circuit (Black Sea, Sinop coastal site) and quantifies the effect on
sea temperature at three scales:

  1. Condenser circuit    : intake flow needed for a chosen condenser rise dT_cond.
  2. Outfall (pipe)       : the discharge temperature = ambient + dT_cond.
  3. Far-field / receiving: the excess temperature after near-field dilution,
                            which is the regulated environmental metric.

Heat load is the condenser duty from thermo_cycle.py (NOT the cooling tower).
No code is run against external services; pure local calc + matplotlib figure.

Outputs -> docs/competition/cycle/
  seawater_heat_sink.csv
  seawater_plume_dilution.png

Regulatory context (for the FER narrative, values are typical EU/Turkish coastal):
  - Edge-of-mixing-zone excess temperature   : <= 3 K above ambient
  - Absolute discharge / mixing-zone max     : <= ~35 C (summer-limiting)
  - No evaporative consumptive water use (vs. a wet cooling tower).
"""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Inputs
# ----------------------------------------------------------------------------
Q_COND_MW = 82.6          # condenser heat rejection, MWth (thermo_cycle.py)
Q_COND_W  = Q_COND_MW * 1e6

# Black Sea (Sinop) surface seawater -- brackish, salinity ~18 psu.
# cp and rho between fresh water and full ocean seawater.
CP_SW   = 4.00e3          # J/(kg.K)   brackish seawater specific heat
RHO_SW  = 1012.0          # kg/m^3     brackish seawater density (~18 psu, surface)

# Ambient intake temperatures (seasonal envelope, Sinop surface water)
T_AMB_WINTER = 8.0        # C
T_AMB_SUMMER = 25.0       # C   <- limiting case for absolute outfall temperature

# Condenser circuit design rise (intake -> outfall through the condenser)
DT_COND_DESIGN = 10.0     # K   design value (matches §8.4 "<= 10 K")
DT_COND_SUMMER = 7.0      # K   summer-managed value to cap absolute outfall temp

ABS_OUTFALL_CAP = 35.0    # C   typical regulatory absolute max
MIX_ZONE_DT_CAP = 3.0     # K   typical edge-of-mixing-zone excess-temperature cap

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "docs", "competition", "cycle")
OUTDIR = os.path.abspath(OUTDIR)


def intake_flow(dt_cond):
    """Mass and volume flow of seawater for a given condenser rise."""
    mdot = Q_COND_W / (CP_SW * dt_cond)      # kg/s
    vdot = mdot / RHO_SW                      # m^3/s
    return mdot, vdot


def far_field_excess(dt_outfall, dilution_N):
    """Excess temperature after mixing the outfall stream with N-fold ambient.

    Heat is conserved: discharge stream at +dt_outfall mixed into a total flow
    (1 + N) x discharge gives excess = dt_outfall / (1 + N).
    N is the dilution factor (ambient entrained per unit discharge).
    """
    return dt_outfall / (1.0 + dilution_N)


# ----------------------------------------------------------------------------
# 1) Condenser circuit sizing
# ----------------------------------------------------------------------------
mdot_d, vdot_d = intake_flow(DT_COND_DESIGN)
mdot_s, vdot_s = intake_flow(DT_COND_SUMMER)

print("=== Seawater once-through condenser circuit ===")
print(f"Condenser heat load           : {Q_COND_MW:.1f} MWth")
print(f"Design rise dT_cond           : {DT_COND_DESIGN:.0f} K")
print(f"  intake flow                 : {mdot_d:,.0f} kg/s  ({vdot_d:.2f} m^3/s)")
print(f"Summer-managed rise dT_cond   : {DT_COND_SUMMER:.0f} K")
print(f"  intake flow                 : {mdot_s:,.0f} kg/s  ({vdot_s:.2f} m^3/s)")
print()

# ----------------------------------------------------------------------------
# 2) Outfall (pipe-exit) absolute temperature, seasonal
# ----------------------------------------------------------------------------
print("=== Outfall (undiluted pipe) temperature ===")
rows_outfall = []
for label, t_amb, dt in [
    ("winter, design dT=10K", T_AMB_WINTER, DT_COND_DESIGN),
    ("summer, design dT=10K", T_AMB_SUMMER, DT_COND_DESIGN),
    ("summer, managed dT=7K", T_AMB_SUMMER, DT_COND_SUMMER),
]:
    t_out = t_amb + dt
    flag = "  *** exceeds abs cap" if t_out > ABS_OUTFALL_CAP else ""
    print(f"  {label:24s}: {t_amb:.0f} -> {t_out:.0f} C{flag}")
    rows_outfall.append((label, t_amb, dt, t_out))
print()

# ----------------------------------------------------------------------------
# 3) Far-field excess temperature vs near-field dilution
# ----------------------------------------------------------------------------
# A submerged multiport diffuser typically achieves dilution N = 10-50 within a
# few tens of metres; an unassisted surface discharge ~ 3-10. We report the band.
N = np.array([1, 2, 3, 5, 10, 20, 30, 50, 100], dtype=float)
dt_far_design = far_field_excess(DT_COND_DESIGN, N)

print("=== Far-field excess temperature vs dilution (design dT=10K outfall) ===")
print("  dilution N   excess dT (K)   meets <=3K mix-zone?")
n_for_cap = None
for n, d in zip(N, dt_far_design):
    ok = "yes" if d <= MIX_ZONE_DT_CAP else "no"
    if d <= MIX_ZONE_DT_CAP and n_for_cap is None:
        n_for_cap = n
    print(f"  {n:7.0f}      {d:7.2f}          {ok}")
print(f"\n  -> dilution >= ~{n_for_cap:.0f}x meets the 3 K edge-of-mixing-zone cap")
print(f"     (a multiport diffuser reaches this within tens of metres).")
print()

# ----------------------------------------------------------------------------
# 4) Whole-water-body context: how big a current makes the rise negligible
# ----------------------------------------------------------------------------
# Far-field rise if the heat is mixed into a coastal current cross-section
# A = depth h x width w moving at longshore speed u: Q_dil = u*h*w.
print("=== Far-field rise vs longshore current (mixing depth 10 m, width 200 m) ===")
h_mix, w_mix = 10.0, 200.0      # m
A_mix = h_mix * w_mix           # m^2
rows_curr = []
for u in [0.02, 0.05, 0.10, 0.20]:   # m/s, typical Black Sea coastal band
    q_dil = u * A_mix                # m^3/s
    mdot_dil = q_dil * RHO_SW
    dt_far = Q_COND_W / (mdot_dil * CP_SW)
    print(f"  u={u:.2f} m/s  Q_dil={q_dil:6.1f} m^3/s  ->  far-field dT = {dt_far:.3f} K")
    rows_curr.append((u, q_dil, dt_far))
print()

# ----------------------------------------------------------------------------
# Write CSV
# ----------------------------------------------------------------------------
os.makedirs(OUTDIR, exist_ok=True)
csv_path = os.path.join(OUTDIR, "seawater_heat_sink.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["# Aegis-40 seawater once-through heat sink"])
    w.writerow(["Q_condenser_MWth", Q_COND_MW])
    w.writerow(["cp_seawater_J_kgK", CP_SW, "rho_seawater_kg_m3", RHO_SW])
    w.writerow([])
    w.writerow(["section", "case", "dT_cond_K", "mdot_kg_s", "vdot_m3_s"])
    w.writerow(["circuit", "design", DT_COND_DESIGN, f"{mdot_d:.0f}", f"{vdot_d:.2f}"])
    w.writerow(["circuit", "summer_managed", DT_COND_SUMMER, f"{mdot_s:.0f}", f"{vdot_s:.2f}"])
    w.writerow([])
    w.writerow(["section", "case", "T_ambient_C", "dT_cond_K", "T_outfall_C"])
    for label, t_amb, dt, t_out in rows_outfall:
        w.writerow(["outfall", label, t_amb, dt, f"{t_out:.1f}"])
    w.writerow([])
    w.writerow(["section", "dilution_N", "far_field_excess_dT_K"])
    for n, d in zip(N, dt_far_design):
        w.writerow(["far_field", int(n), f"{d:.3f}"])
    w.writerow([])
    w.writerow(["section", "current_u_m_s", "Q_dilution_m3_s", "far_field_dT_K"])
    for u, q_dil, dt_far in rows_curr:
        w.writerow(["current", u, f"{q_dil:.1f}", f"{dt_far:.3f}"])
print(f"wrote {csv_path}")

# ----------------------------------------------------------------------------
# Figure: dilution curve + mixing-zone cap
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.6))
Nfine = np.linspace(1, 100, 400)
ax.plot(Nfine, far_field_excess(DT_COND_DESIGN, Nfine), color="#c0392b", lw=2.2,
        label=f"design outfall +{DT_COND_DESIGN:.0f} K")
ax.plot(Nfine, far_field_excess(DT_COND_SUMMER, Nfine), color="#e67e22", lw=1.8,
        ls="--", label=f"summer-managed outfall +{DT_COND_SUMMER:.0f} K")
ax.axhline(MIX_ZONE_DT_CAP, color="#2c3e50", lw=1.2, ls=":",
           label=f"{MIX_ZONE_DT_CAP:.0f} K mixing-zone cap")
ax.axvspan(10, 50, color="#27ae60", alpha=0.10,
           label="diffuser dilution band (10-50x)")
ax.scatter(N, dt_far_design, color="#c0392b", s=18, zorder=5)
ax.set_xlabel("near-field dilution factor  N  (ambient entrained per unit discharge)")
ax.set_ylabel("far-field excess temperature  $\\Delta T$  (K)")
ax.set_title("Aegis-40 seawater outfall — far-field thermal impact\n"
             f"({Q_COND_MW:.0f} MWth to Black Sea, Sinop)", fontsize=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, 10.5)
ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc="upper right")
fig.tight_layout()
png_path = os.path.join(OUTDIR, "seawater_plume_dilution.png")
fig.savefig(png_path, dpi=150)
print(f"wrote {png_path}")
