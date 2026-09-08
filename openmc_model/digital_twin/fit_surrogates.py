"""Digital-Twin Day-3: fit ML surrogates on the sweep (core_sweep.csv + maps/).
Pure sklearn — no OpenMC. Re-run any time as more sweep points land.

Produces:
  surrogate_k_eff.pkl, surrogate_F_assembly.pkl   scalar Gaussian-Process surrogates
  surrogate_powermap.pkl                          POD(PCA)+GP radial power-map ROM
  reactivity coefficients (MTC/DTC/void/rod worth) via dk/dinput, checked vs STAT_FINAL
  validation.txt / validation.png                 hold-out R2 + coeff comparison
"""
import os, glob, pickle
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel as C, RBF, WhiteKernel
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA

OUT = os.environ.get("TWIN_OUT", "/home/samira/aegis_run/twin_sweep")
INS = ["T_mod_K", "T_fuel_K", "n_rods_in", "void"]
# STAT_FINAL direct-computed reference (final locked design) for the coefficient sanity check.
# rod_worth is the 16-CRA 90%-enriched-B10 bank worth = 21,509 pcm (DA-4 N5C).
REF = dict(MTC=-26.87, DTC=-1.91, void=-173.2, rod_worth=21509.0)
REF_NOTE = "rod_worth = 0->16-rod 90%-enriched-B10 sweep basis; final 16-CRA = 21,509 pcm (DA-4 N5C)"

df = pd.read_csv(os.path.join(OUT, "core_sweep.csv"))
df = df.dropna(subset=["k_eff"]).reset_index(drop=True)
X = df[INS].values.astype(float)
Xm, Xs = X.mean(0), X.std(0); Xn = (X - Xm) / Xs
print(f"[fit] {len(df)} sweep points loaded")

def _gp():
    return GaussianProcessRegressor(
        kernel=C(1.0) * RBF([1.0]*4) + WhiteKernel(1e-4),
        normalize_y=True, n_restarts_optimizer=4, random_state=0)

# ---- scalar surrogates (leave-one-out-ish CV R2, then refit on all) ----
models, lines = {}, []
for tgt in ["k_eff", "F_assembly"]:
    y = df[tgt].values.astype(float)
    yhat = cross_val_predict(_gp(), Xn, y, cv=min(5, len(df)))
    r2 = r2_score(y, yhat); rmse = float(np.sqrt(np.mean((y - yhat)**2)))
    gp = _gp().fit(Xn, y)
    models[tgt] = gp
    pickle.dump({"gp": gp, "Xm": Xm, "Xs": Xs, "inputs": INS},
                open(os.path.join(OUT, f"surrogate_{tgt}.pkl"), "wb"))
    lines.append(f"{tgt:12s}  CV R2={r2:.4f}  RMSE={rmse:.4g}")
    print("[fit] " + lines[-1])

# ---- reactivity coefficients: degree-2 response surface (smooth, edge-robust) ----
# A global GP gives noisy gradients at the domain edge (operating T_mod=556 K is the
# top of the sweep box), which inflates the small differential coefficients. A degree-2
# response surface in the inputs yields stable derivatives; differences are taken strictly
# in-domain (MTC backward, void forward). Rod worth stays on the GP (large, interior).
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
_pf = PolynomialFeatures(2, include_bias=True)
_lr = LinearRegression().fit(_pf.fit_transform(Xn), df["k_eff"].values.astype(float))
def k_at(Tm, Tf, nr, vo):
    return float(_lr.predict(_pf.transform((np.array([[Tm, Tf, nr, vo]]) - Xm) / Xs))[0])
def kg(Tm, Tf, nr, vo):
    return float(models["k_eff"].predict(((np.array([[Tm, Tf, nr, vo]]) - Xm) / Xs))[0])
Tm0, Tf0 = 556.0, 900.0
mtc = (k_at(Tm0, Tf0, 0, 0) - k_at(Tm0-40, Tf0, 0, 0)) / 40 * 1e5        # in-domain backward
dtc = (k_at(Tm0, Tf0+100, 0, 0) - k_at(Tm0, Tf0-100, 0, 0)) / 200 * 1e5
vco = (k_at(Tm0, Tf0, 0, 0.10) - k_at(Tm0, Tf0, 0, 0.0)) / 10 * 1e5      # in-domain forward, per %void
karo, kari = kg(Tm0, Tf0, 0, 0), kg(Tm0, Tf0, 12, 0)                     # rod worth from GP
rw = (1/kari - 1/karo) * 1e5
coef = dict(MTC=mtc, DTC=dtc, void=vco, rod_worth=rw)
lines.append("\nReactivity coefficients (surrogate dk/dinput vs STAT_FINAL):")
for k_ in ("MTC", "DTC", "void", "rod_worth"):
    lines.append(f"  {k_:10s} surrogate={coef[k_]:+9.2f}   STAT_FINAL={REF[k_]:+9.2f}"
                 f"   ({100*(coef[k_]-REF[k_])/REF[k_]:+.0f}%)")
    print("[fit] " + lines[-1].strip())

# ---- POD (PCA) + GP surrogate for the RADIAL power map ----
mp = sorted(glob.glob(os.path.join(OUT, "maps", "map_*.npy")))
ids = [int(os.path.basename(f).split("_")[1].split(".")[0]) for f in mp]
keep = [j for j, i in enumerate(ids) if i in set(df["id"])]        # align maps to loaded rows
R = np.array([np.load(mp[j]).sum(0).ravel() for j in keep])        # N x 49 radial power
Xr = Xn[[list(df["id"]).index(ids[j]) for j in keep]]
n_modes = min(6, R.shape[0] - 1)
pca = PCA(n_components=n_modes).fit(R)
Cc = pca.transform(R)
mode_gps = [_gp().fit(Xr, Cc[:, k]) for k in range(n_modes)]
# reconstruction CV R2
recon = np.vstack([cross_val_predict(_gp(), Xr, Cc[:, k], cv=min(5, len(Xr))) for k in range(n_modes)]).T
R_hat = pca.inverse_transform(recon)
pod_r2 = r2_score(R.ravel(), R_hat.ravel())
pickle.dump({"pca": pca, "mode_gps": mode_gps, "Xm": Xm, "Xs": Xs, "shape": (int(R.shape[1]**0.5), int(R.shape[1]**0.5))},
            open(os.path.join(OUT, "surrogate_powermap.pkl"), "wb"))
lines.append(f"\npower-map POD ({n_modes} modes, var {pca.explained_variance_ratio_.sum():.3f})  CV R2={pod_r2:.4f}")
print("[fit] " + lines[-1].strip())

open(os.path.join(OUT, "validation.txt"), "w").write("\n".join(lines) + "\n")

# ---- validation plot: k parity + coefficient bars ----
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
y = df["k_eff"].values; yh = cross_val_predict(_gp(), Xn, y, cv=min(5, len(df)))
ax[0].scatter(y, yh, s=14); lim = [y.min(), y.max()]
ax[0].plot(lim, lim, "k--", lw=1); ax[0].set_xlabel("OpenMC k_eff"); ax[0].set_ylabel("surrogate k_eff")
ax[0].set_title(f"k_eff parity (CV R2={r2_score(y,yh):.3f})")
kk = ["MTC", "DTC", "void", "rod_worth"]; xi = np.arange(len(kk))
ax[1].bar(xi-0.2, [coef[k] for k in kk], 0.4, label="surrogate")
ax[1].bar(xi+0.2, [REF[k] for k in kk], 0.4, label="STAT_FINAL")
ax[1].set_xticks(xi); ax[1].set_xticklabels(kk); ax[1].legend(); ax[1].set_title("coefficients check")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "validation.png"), dpi=150)
print(f"[fit] wrote surrogates + validation.txt/png in {OUT}")
