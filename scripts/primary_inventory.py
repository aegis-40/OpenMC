"""Estimate the Aegis-40 primary coolant inventory from the LOCKED core geometry
and the (Tier-B) RPV geometry, for FER Table 8.1-2.

Method: sum the in-vessel primary water regions as documented cylindrical / annular /
hemispherical volumes, using the same constants the CAD scripts use
(generate_fa_step / generate_core_step / generate_rpv_step). The core region is computed
from the 17x17 lattice (water = lattice footprint - fuel-pin solid - guide-tube walls);
the loop regions (lower plenum + head, riser, SG shell-side, downcomer, upper plenum + head)
are geometric volumes with stated solid-blockage allowances.

This is an ENGINEERING ESTIMATE (±~25%) to replace the borrowed 1.82 Mkg reference value;
the precise inventory comes from the Section 8.4 steady-state thermal-hydraulic model.
All lengths mm, volumes converted to m^3. Density at ~285 C / 12.8 MPa ~ 740 kg/m^3.
"""
import math

PI = math.pi

# ---- locked lattice (generate_fa_step.py) ----
CLAD_OD = 9.520           # fuel-rod outer diameter
GT_OD, GT_ID = 12.040, 11.248   # guide / instrument tube
PIN_PITCH = 12.623
ACTIVE = 2000.0           # active fuel height
N_CELL = 17 * 17          # 289
N_GUIDE = 25              # 24 guide + 1 instrument
N_FUEL = N_CELL - N_GUIDE # 264
N_FA = 21

# ---- core barrel (generate_core_step.py) ----
REFL_OUT_R = 740.1        # radial-reflector outer radius (inside barrel)
CORE_H = 2600.0           # active 2000 + 300 axial reflector each end

# ---- RPV (generate_rpv_step.py, Tier-B) ----
R_IN = 1400.0             # vessel inner radius
CORE_BOT, CORE_TOP = -281.5, 2318.5
LOWER_PLENUM = 800.0
RISER_R, RISER_WALL = 560.0, 30.0
SG_Z0, SG_Z1 = 2568.5, 5168.5
SG_SHROUD_R = 1180.0
Z_RISER_TOP, Z_CYL_TOP = 5318.5, 6118.5
RHO = 740.0               # kg/m^3 at hot primary conditions

mm3_to_m3 = 1e-9

def cyl(r, h):       return PI * r * r * h
def annulus(ro, ri, h): return PI * (ro*ro - ri*ri) * h
def hemi(r):         return (2.0/3.0) * PI * r**3

rows = []

# --- A. core region: lattice water over the active height + reflector ---
foot = N_CELL * PIN_PITCH**2                       # lattice footprint per FA
solid_fuel = N_FUEL * (PI/4.0) * CLAD_OD**2        # fuel-rod cross-section
solid_gtwall = N_GUIDE * (PI/4.0) * (GT_OD**2 - GT_ID**2)   # tube walls (interior is water)
water_area_fa = foot - solid_fuel - solid_gtwall   # mm^2 of coolant per FA
core_active = water_area_fa * ACTIVE * N_FA        # active-height coolant
# radial reflector ring (barrel cross-section minus the 21 lattice footprints) + axial reflector
refl_radial = (PI * REFL_OUT_R**2 - N_FA * foot) * ACTIVE
refl_axial = PI * REFL_OUT_R**2 * (CORE_H - ACTIVE) * 0.90  # 300mm each end, ~90% water
rows.append(("Core: open lattice coolant (active)", core_active * mm3_to_m3))
rows.append(("Core: radial + axial reflector water", (refl_radial + refl_axial) * mm3_to_m3))

# --- B. lower plenum + lower hemispherical head (80% water, rest = distributor/support) ---
lower = (cyl(R_IN, LOWER_PLENUM) + hemi(R_IN)) * 0.80
rows.append(("Lower plenum + lower head", lower * mm3_to_m3))

# --- C. central riser interior ---
riser = cyl(RISER_R - RISER_WALL, Z_RISER_TOP - CORE_TOP)
rows.append(("Central riser (hot leg up)", riser * mm3_to_m3))

# --- D. SG shell-side: annulus riser-outer -> shroud-inner, 70% water (tubes block ~30%) ---
sg_shell = annulus(SG_SHROUD_R - 30.0, RISER_R, SG_Z1 - SG_Z0) * 0.70
rows.append(("SG shell-side primary (around tubes)", sg_shell * mm3_to_m3))

# --- E. downcomer: shroud-outer -> vessel, full height core-bot to SG top, 90% water ---
downcomer = annulus(R_IN, SG_SHROUD_R, SG_Z1 - CORE_BOT) * 0.90
rows.append(("Downcomer (cold leg down)", downcomer * mm3_to_m3))

# --- F. upper plenum + upper head, 50% water (rest = pressuriser steam space / internals) ---
upper = (cyl(R_IN, Z_CYL_TOP - Z_RISER_TOP) + hemi(R_IN)) * 0.50
rows.append(("Upper plenum + head (excl. pzr steam)", upper * mm3_to_m3))

total_m3 = sum(v for _, v in rows)
mass_t = total_m3 * RHO / 1000.0

w = max(len(n) for n, _ in rows)
print(f"Aegis-40 primary coolant inventory estimate (rho = {RHO:.0f} kg/m3)\n")
for n, v in rows:
    print(f"  {n:<{w}}  {v:7.2f} m3")
print("  " + "-" * (w + 12))
print(f"  {'TOTAL primary water volume':<{w}}  {total_m3:7.2f} m3")
print(f"\n  => primary coolant inventory ~ {mass_t:5.1f} t  ({total_m3*1000:.0f} L)")
print(f"     core open-lattice coolant fraction = "
      f"{water_area_fa / (N_CELL*PIN_PITCH**2):.3f} of the assembly footprint")
