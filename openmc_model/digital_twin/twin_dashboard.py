"""Aegis-40 Core Digital Twin - live dashboard (Day 5).

Loads the fitted surrogates (results/surrogate_*.pkl) and turns operating-input
sliders into a real-time core-state prediction (k_eff, reactivity, peaking,
radial power map, margin flags) in milliseconds - no OpenMC at run time.

Run:
    pip install streamlit matplotlib scikit-learn
    streamlit run twin_dashboard.py
"""
import os, pickle
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

RES = os.environ.get("TWIN_RESULTS", os.path.join(os.path.dirname(__file__), "results"))
# validated STAT_FINAL reference feedback (used for quantitative transients)
REF = dict(MTC=-27.1, DTC=-1.90, void=-166.0, rod_worth=13390.0)
FDH_LIMIT, FQ_LIMIT = 1.65, 2.32          # LCO peaking limits


@st.cache_resource
def load():
    L = {}
    for n in ("k_eff", "F_assembly", "powermap"):
        with open(os.path.join(RES, f"surrogate_{n}.pkl"), "rb") as f:
            L[n] = pickle.load(f)
    return L


def scalar(S, key, x):
    d = S[key]; xn = (np.array([x], float) - d["Xm"]) / d["Xs"]
    m, sd = d["gp"].predict(xn, return_std=True)
    return float(m[0]), float(sd[0])


def powermap(S, x):
    d = S["powermap"]; xn = (np.array([x], float) - d["Xm"]) / d["Xs"]
    c = np.array([g.predict(xn)[0] for g in d["mode_gps"]])
    flat = d["pca"].inverse_transform(c.reshape(1, -1))[0]
    n = int(d["shape"][0])
    return flat.reshape(n, n)


st.set_page_config(page_title="Aegis-40 Core Digital Twin", layout="wide")
S = load()

st.title("Aegis-40 Core Digital Twin")
st.caption("Surrogate reduced-order model trained on 120 OpenMC points (ENDF/B-VIII.0, ~45 pcm each). "
           "Predicts core state in milliseconds. Validated: k_eff R2 0.996, peaking R2 0.998, "
           "power-map POD R2 0.99, rod worth exact.")

with st.sidebar:
    st.header("Operating inputs")
    Tm = st.slider("Moderator temperature (K)", 294, 560, 556, help="core-average moderator T")
    Tf = st.slider("Fuel temperature (K)", 600, 1200, 900)
    nr = st.slider("Control rods inserted (of 16 CRA)", 0, 12, 0,
                   help="surrogate trained over 0-12 inserted; 16-CRA bank worth 21 437 pcm")
    vo = st.slider("Void fraction", 0.0, 0.20, 0.0, 0.01)
    st.divider()
    st.caption("Validated feedback (STAT_FINAL): "
               f"MTC {REF['MTC']:.0f}, DTC {REF['DTC']:.1f}, void {REF['void']:.0f} pcm/%")

x = [Tm, Tf, nr, vo]
k, ksd = scalar(S, "k_eff", x)
Fa, _ = scalar(S, "F_assembly", x)
rho = (1.0 - 1.0 / k) * 1e5

c1, c2, c3, c4 = st.columns(4)
c1.metric("k_eff", f"{k:.4f}", f"+/-{ksd*1e5:.0f} pcm")
c2.metric("Reactivity", f"{rho:+.0f} pcm")
c3.metric("Assembly peaking F", f"{Fa:.3f}",
          "OK" if Fa <= FDH_LIMIT else "over", delta_color="normal" if Fa <= FDH_LIMIT else "inverse")
state = "SUPERCRITICAL" if k > 1.002 else ("CRITICAL" if k > 0.998 else "SUBCRITICAL")
c4.metric("Core state", state)

left, right = st.columns([3, 2])
with left:
    st.subheader("Radial power distribution (normalized to core average)")
    M = powermap(S, x)
    core = M > (0.05 * M.max())
    Mn = np.where(core, M / M[core].mean(), np.nan)
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(np.ma.masked_invalid(Mn), cmap="inferno", origin="lower")
    for (i, j), v in np.ndenumerate(Mn):
        if not np.isnan(v):
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="white" if v < Mn[core.reshape(Mn.shape)].max()*0.75 else "black", fontsize=7)
    ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(im, ax=ax, label="assembly power / core avg")
    ax.set_title(f"peak/avg = {np.nanmax(Mn):.3f}")
    st.pyplot(fig)

with right:
    st.subheader("Margins & flags")
    def flag(ok): return "PASS" if ok else "CHECK"
    st.write(f"**Assembly radial peaking**: {Fa:.3f} vs F_dH limit {FDH_LIMIT}  ->  {flag(Fa <= FDH_LIMIT)}")
    st.progress(min(Fa / FDH_LIMIT, 1.0))
    fq_est = Fa * 1.29                      # F_q ~ F_dH x axial (nominal ~1.29)
    st.write(f"**Estimated F_q** (x nominal axial): {fq_est:.3f} vs {FQ_LIMIT}  ->  {flag(fq_est <= FQ_LIMIT)}")
    st.progress(min(fq_est / FQ_LIMIT, 1.0))
    st.write(f"**Core state**: k_eff {k:.4f} ({state})")
    st.progress(min(k / 1.20, 1.0))
    st.divider()
    st.caption("Radial power map is a POD(6-mode) reconstruction; axial shape is treated as "
               "nominal (cosine). Feedback coefficients for transient analysis use the validated "
               "STAT_FINAL values shown in the sidebar, not the surrogate slopes.")
