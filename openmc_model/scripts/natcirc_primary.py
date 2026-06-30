"""
Aegis-40 — primary natural-circulation loop balance (FER §8.4).

First-principles cross-check of the in-vessel natural-circulation primary loop
against Adilbek's CFD/correlation thermal-hydraulics results. Produces the
heat-removal numbers that §8.4 cites:

  - core flow from the heat balance  m_dot = Q / (cp * dT)
  - buoyancy driving head            dP_drv = (rho_cold - rho_hot) * g * H_th
  - subcooling margin to saturation at the operating pressure
  - implied loop loss coefficient that the driving head can sustain at m_dot
  - OTSG secondary saturation ceiling set by the cold leg (primary-secondary
    coupling check that feeds back to §8.9)

Water/steam properties: IAPWS-IF97 via the `iapws` package (same as thermo_cycle.py).

Geometry (thermal centres) from scripts/generate_rpv_step.py, in model-z (mm):
  core span  -281.5 .. 2318.5   -> midplane 1018.5
  OTSG span  2568.5 .. 5168.5   -> mid      3868.5
  H_th = 3868.5 - 1018.5 = 2850 mm
"""

from iapws import IAPWS97

g = 9.80665

# ---- primary design conditions (Adilbek's TH result; P = iPWR/NuScale class) ----
Q_th   = 125.0e6        # W, core thermal power
P_op   = 12.8           # MPa, primary operating pressure (NuScale-class iPWR)
T_hot  = 308.0          # degC, core outlet / hot leg (581 K)
T_cold = 258.0          # degC, core inlet  / cold leg (531 K)
T_avg  = 0.5 * (T_hot + T_cold)

H_th   = 2.850          # m, core-mid -> OTSG-mid thermal height (RPV geometry)

def water(P_MPa, T_C):
    return IAPWS97(P=P_MPa, T=T_C + 273.15)

cold = water(P_op, T_cold)
hot  = water(P_op, T_hot)
avg  = water(P_op, T_avg)
sat  = IAPWS97(P=P_op, x=0.0)          # saturation at operating pressure

rho_cold = cold.rho
rho_hot  = hot.rho
cp_avg   = avg.cp * 1000.0             # J/kg.K  (iapws cp is kJ/kg.K)
T_sat    = sat.T - 273.15

dT       = T_hot - T_cold
m_dot    = Q_th / (cp_avg * dT)        # kg/s

dP_drv   = (rho_cold - rho_hot) * g * H_th   # Pa

# implied loop loss the driving head sustains at m_dot, expressed as a total K
# referenced to the core coolant velocity. Core coolant flow area from the
# CFD velocity (~0.90 m/s in the open lattice) gives a consistency check.
v_core   = 0.90                         # m/s, from CFD developed-core velocity
A_core   = m_dot / (rho_avg := avg.rho * v_core)  # m^2 (effective core flow area)
# dP_loss = K_tot * 0.5*rho*v^2  ; set = dP_drv to back out K_tot
vel_head = 0.5 * avg.rho * v_core**2
K_tot    = dP_drv / vel_head

subcool_hot  = T_sat - T_hot
subcool_cold = T_sat - T_cold

# ---- OTSG secondary saturation ceiling: CONSERVATIVE bound only -------------
# Simple criterion (secondary boils below the bare cold leg). This IGNORES the
# economizer, so it is over-conservative — the true ceiling comes from the full
# counterflow pinch in thermo_cycle_recouple.py (~4.5 MPa, because the economizer
# lets the secondary boil ABOVE the cold leg). Kept here only as a sanity floor.
pinch_min = 8.0                         # degC, practical helical-OTSG pinch
T_sat_sec_max = T_cold - pinch_min      # conservative: below the bare cold leg
sec_sat_state = IAPWS97(T=T_sat_sec_max + 273.15, x=0.0)
P_sec_max = sec_sat_state.P             # MPa, conservative steam-pressure floor

print("="*70)
print("AEGIS-40 PRIMARY NATURAL-CIRCULATION LOOP BALANCE  (FER §8.4)")
print("="*70)
print(f"Operating pressure          {P_op:6.2f} MPa")
print(f"Saturation temperature      {T_sat:6.1f} °C")
print(f"Hot leg / cold leg / avg    {T_hot:.0f} / {T_cold:.0f} / {T_avg:.0f} °C   (dT = {dT:.0f} K)")
print(f"Subcooling  hot / cold leg  {subcool_hot:5.1f} / {subcool_cold:5.1f} °C")
print("-"*70)
print(f"rho cold (258 °C)           {rho_cold:7.1f} kg/m^3")
print(f"rho hot  (308 °C)           {rho_hot:7.1f} kg/m^3")
print(f"delta-rho                   {rho_cold-rho_hot:7.1f} kg/m^3")
print(f"cp (avg)                    {cp_avg/1000:7.3f} kJ/kg.K")
print("-"*70)
print(f"Primary mass flow  m_dot    {m_dot:7.1f} kg/s   = Q/(cp.dT)")
print(f"Thermal height     H_th     {H_th:7.3f} m")
print(f"Driving head       dP_drv   {dP_drv:7.0f} Pa    = {dP_drv/1000:.2f} kPa")
print(f"Core velocity (CFD)         {v_core:7.2f} m/s")
print(f"Effective core flow area    {A_core:7.3f} m^2")
print(f"Velocity head 0.5 rho v^2   {vel_head:7.0f} Pa")
print(f"Sustained loop loss K_tot   {K_tot:7.1f}   (driving head / vel head)")
print("-"*70)
print("PRIMARY-SECONDARY COUPLING (feeds §8.9 OTSG):")
print(f"  conservative floor: sec. Tsat <= {T_sat_sec_max:.0f} °C -> steam <= {P_sec_max:5.2f} MPa")
print(f"  TRUE ceiling (counterflow + economizer): ~4.5 MPa / 296 °C, 8.8 °C pinch")
print(f"  -> see thermo_cycle_recouple.py: 40 MWe-class PRESERVED (39.7 MWe net)")
print("="*70)
