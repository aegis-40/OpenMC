import openmc.deplete as d
import numpy as np

r = d.Results("/home/samira/aegis_run/pincell_10k/depletion_results.h5")
t, k = r.get_keff()  # (N,2)
steps = [0.1, 0.4, 0.5] + [1.0] * 5 + [5.0] * 5
bu = np.concatenate([[0.0], np.cumsum(steps)])
n = len(k)
print(f"completed steps with k: {n} of {len(bu)} ({bu[n-1]:.1f} MWd/kg reached)")
for i in range(n):
    print(f"  step {i:2d}  BU={bu[i]:6.2f}  k={k[i,0]:.5f}  +/- {k[i,1]*1e5:4.0f} pcm")
