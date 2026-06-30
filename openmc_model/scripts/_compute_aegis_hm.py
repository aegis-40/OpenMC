"""Geometric heavy-metal loading for the Aegis-40 37-FA core, from the actual
model constants (rev6/rev7 notebook). Replaces the provisional 21-FA value
(5.6 tHM) scaled x37/21 = 9.87 with a real 37-FA computation."""
import math, openmc

FUEL_RADIUS = 0.40958   # cm  (pellet radius, notebook)
RHO_UO2 = 10.40         # g/cm3 (RHO_UO2, notebook)
H_ACTIVE = 200.0        # cm  (2.0 m active fuel)
N_ROD_FA = 264          # 17x17 - 24 guide - 1 instrument
N_FA_37 = 37
N_FA_21 = 21
POWER_MWT = 125.0
ENRICH = 4.95           # wt% U235 (max ring; U-fraction ~insensitive)

# exact U mass fraction of UO2 from OpenMC
uo2 = openmc.Material()
uo2.add_element("U", 1.0, enrichment=ENRICH)
uo2.add_element("O", 2.0)
uo2.set_density("g/cm3", RHO_UO2)
dens = uo2.get_nuclide_atom_densities()        # atoms/b-cm
import openmc.data as od
mass = {n: dens[n] * od.atomic_mass(n) for n in dens}      # ~ g-equiv
u_frac = sum(m for n, m in mass.items() if n.startswith("U2")) / sum(mass.values())

vol_rod = math.pi * FUEL_RADIUS**2 * H_ACTIVE          # cm3 per rod
uo2_rod = vol_rod * RHO_UO2                              # g UO2 per rod
u_rod = uo2_rod * u_frac                                 # g U per rod
hm_fa = u_rod * N_ROD_FA / 1e3                           # kg... -> tHM per FA / 1e6
hm_fa_t = u_rod * N_ROD_FA / 1e6                         # tHM per FA
hm_37 = hm_fa_t * N_FA_37
hm_21 = hm_fa_t * N_FA_21

print(f"U mass fraction of UO2 (enr {ENRICH}%): {u_frac:.4f}")
print(f"pellet vol/rod   : {vol_rod:.3f} cm3")
print(f"UO2 mass/rod     : {uo2_rod:.1f} g   ({uo2_rod/453.592:.2f} lb)")
print(f"U mass/rod       : {u_rod:.1f} g")
print(f"HM per assembly  : {hm_fa_t*1e3:.2f} kgU  = {hm_fa_t:.4f} tHM/FA")
print(f"HM  21-FA        : {hm_21:.3f} tHM   (notebook hardcodes 5.6)")
print(f"HM  37-FA        : {hm_37:.3f} tHM   (table currently 9.87 = 5.6*37/21)")
print(f"specific power 37-FA: {POWER_MWT/hm_37:.2f} MW/tHM   (= 125/{hm_37:.2f})")
print(f"NuScale FSAR     : 8.13 tHM ; 549.48 lb UO2/FA = {549.48} lb")
print(f"  Aegis UO2/FA   : {uo2_rod*N_ROD_FA/453.592:.1f} lb  vs NuScale 549.48 lb")
