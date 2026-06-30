import glob, numpy as np, openmc
d = "/home/samira/aegis_run/shielding/aegis40_rev6_outputs/shielding_rev7"
sp = openmc.StatePoint(sorted(glob.glob(d + "/statepoint.*.h5"))[-1])

def relerr(t):
    m = t.mean.ravel(); s = t.std_dev.ravel()
    re = np.where(m > 0, s / np.maximum(m, 1e-300), np.nan)
    return m, s, re

print("=== dose_n / dose_g per radial bin (mean, rel.err) ===")
mn, sn, ren = relerr(sp.get_tally(name="dose_n"))
mg, sg, reg = relerr(sp.get_tally(name="dose_g"))
nr = len(mn)
for i in range(nr):
    flag = "  <-- OUTERMOST" if i == nr - 1 else ""
    print(f" bin {i:2d}: dose_n rel.err={ren[i]*100:6.1f}%   dose_g rel.err={reg[i]*100:6.1f}%{flag}")

for nm in ["rpv_fast_flux", "heating"]:
    try:
        m, s, re = relerr(sp.get_tally(name=nm))
        print(f"\n{nm}: " + ", ".join(f"[{i}] mean={m[i]:.3e} relerr={re[i]*100:.1f}%"
                                       for i in range(len(m))))
    except Exception as e:
        print(f"\n{nm}: {e}")
sp.close()
