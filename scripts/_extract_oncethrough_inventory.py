"""Extract whole-core actinide inventory at the ONCE-THROUGH discharge (~27.6 GWd/tHM,
2175 EFPD) from depletion_results.h5, vs the depletion endpoint, for FER §8.2.5/§8.11."""
import openmc.deplete, numpy as np
R = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/depletion_results.h5"
SP = 12.664640324214794   # W/g (= MW/tHM) from STAT_FINAL YAML
r = openmc.deplete.Results(R)
t_d = np.asarray(r.get_times(time_units="d"))
bu = SP * t_d / 1000.0
print(f"steps={len(t_d)}  EFPD {t_d[0]:.0f}..{t_d[-1]:.0f}  burnup {bu[0]:.1f}..{bu[-1]:.1f} GWd/t")
i_ot = int(np.argmin(np.abs(bu - 27.6)))
mats = [str(m) for m in r[0].index_mat.keys()]
acts = ["U235","U238","U236","Pu238","Pu239","Pu240","Pu241","Pu242","Np237","Am241","Cm244"]

def mass_g(nuc, step):
    tot = 0.0
    for m in mats:
        try:
            tot += r.get_mass(m, nuc)[1][step]
        except Exception:
            pass
    return tot

for step, lbl in [(i_ot, f"ONCE-THROUGH (step {i_ot}, {t_d[i_ot]:.0f} EFPD, {bu[i_ot]:.1f} GWd/t)"),
                  (len(t_d)-1, f"endpoint ({bu[-1]:.1f} GWd/t)")]:
    mm = {n: mass_g(n, step) for n in acts}
    pu = sum(mm[n] for n in ("Pu238","Pu239","Pu240","Pu241","Pu242"))
    print(f"\n=== {lbl} ===")
    print(f"  U-235 spent = {mm['U235']/1000:.1f} kg   total Pu = {pu/1000:.1f} kg")
    print("  Pu vector: " + "  ".join(
        f"{n}={100*mm[n]/pu:.1f}%" for n in ("Pu239","Pu240","Pu241","Pu238","Pu242")))
    print(f"  Np-237={mm['Np237']/1000:.2f} kg  Am-241={mm['Am241']/1000:.2f} kg  Cm-244={mm['Cm244']/1000:.3f} kg")
