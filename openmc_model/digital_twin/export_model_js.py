#!/usr/bin/env python3
"""Export the fitted twin surrogates + record k(BU) to the static site's data/model.js.

Reproduces the site schema exactly (GP: y = yMean + yStd * sum_i alpha_i * c * rbf(x, xi)).
Run in WSL:
  TWIN_OUT=~/aegis_run/twin_merged DEP_H5="/path/depletion_results.h5" python export_model_js.py
"""
import json, os, pickle
import numpy as np

OUT = os.path.expanduser(os.environ.get("TWIN_OUT", "~/aegis_run/twin_merged"))
H5 = os.environ.get("DEP_H5",
    "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/aegis40_neutronics_outputs (2)/"
    "aegis40_neutronics_outputs/08_depletion_baseline/depletion_results.h5")
SITE = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/digital_twin/aegis40_digital_twin_site/data/model.js"
HM = 9.386

def gp_block(d):
    gp = d["gp"]
    k = gp.kernel_
    const = float(k.k1.k1.constant_value)          # C * RBF + White
    ls = np.atleast_1d(k.k1.k2.length_scale).tolist()
    return {"gp": {"X_train": gp.X_train_.tolist(),
                   "alpha": gp.alpha_.ravel().tolist(),
                   "constant": const,
                   "lengthScale": ls,
                   "yMean": float(np.ravel(gp._y_train_mean)[0]),
                   "yStd": float(np.ravel(gp._y_train_std)[0])},
            "Xm": np.asarray(d["Xm"], float).tolist(),
            "Xs": np.asarray(d["Xs"], float).tolist(),
            "inputs": d.get("inputs", ["T_mod_K", "T_fuel_K", "n_rods_in", "void"])}

def mode_gp_block(gp):
    k = gp.kernel_
    return {"X_train": gp.X_train_.tolist(),
            "alpha": gp.alpha_.ravel().tolist(),
            "constant": float(k.k1.k1.constant_value),
            "lengthScale": np.atleast_1d(k.k1.k2.length_scale).tolist(),
            "yMean": float(np.ravel(gp._y_train_mean)[0]),
            "yStd": float(np.ravel(gp._y_train_std)[0])}

model = {}
for name in ("k_eff", "F_assembly"):
    with open(os.path.join(OUT, f"surrogate_{name}.pkl"), "rb") as f:
        model[name] = gp_block(pickle.load(f))

with open(os.path.join(OUT, "surrogate_powermap.pkl"), "rb") as f:
    pm = pickle.load(f)
model["powermap"] = {
    "Xm": np.asarray(pm["Xm"], float).tolist(),
    "Xs": np.asarray(pm["Xs"], float).tolist(),
    "shape": [int(x) for x in pm["shape"]],
    "pcaMean": pm["pca"].mean_.tolist(),
    "components": pm["pca"].components_.tolist(),
    "explainedVariance": pm["pca"].explained_variance_ratio_.tolist(),
    "modeGPs": [mode_gp_block(g) for g in pm["mode_gps"]],
}

# record cycle curve
import openmc.deplete
r = openmc.deplete.Results(H5)
t = np.asarray(r.get_times(), float)
kk = r.get_keff()[1]
bu = 0.125 * t / HM
ge = kk[:, 0] >= 1.0
downs = [i for i in range(len(t)-1) if ge[i] and not ge[i+1]]
i = downs[-1]
B1 = float(t[i] + (1 - kk[i, 0]) / (kk[i+1, 0] - kk[i, 0]) * (t[i+1] - t[i]))
model["cycle"] = {
    "points": [{"efpd": float(t[j]), "burnup": float(bu[j]),
                "k": float(kk[j, 0]), "sigma_pcm": float(kk[j, 1] * 1e5)} for j in range(len(t))],
    "eoc_burnup": round(0.125 * B1 / HM, 2),
    "eoc_efpd": round(B1, 1),
    "h5_k1_cross_efpd": round(B1, 1),
}

js = "window.AEGIS40_MODEL = " + json.dumps(model) + ";\n"
open(SITE, "w").write(js)
print(f"wrote {SITE}  ({len(js)/1024:.0f} KB)  train={len(model['k_eff']['gp']['alpha'])} pts  "
      f"EOC={model['cycle']['eoc_burnup']} GWd/t / {model['cycle']['eoc_efpd']} EFPD")
