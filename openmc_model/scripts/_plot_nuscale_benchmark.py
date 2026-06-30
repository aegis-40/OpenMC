"""Plot the NuScale-like benchmark: (1) k_eff across CR states vs reference with
residuals, (2) control-rod-worth parity vs reference. Reads nuscale_states_results.json."""
import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/docs/competition/digital-appendix/nuscale_benchmark"
data = json.load(open(f"{D}/nuscale_states_results.json"))
lab = {"all_rods_out10": "ARO", "RE1": "RE1", "RE2": "RE2",
       "SH3": "SH3", "SH4": "SH4", "all_rods_in": "ARI\n(SCRAM)"}
x = np.arange(len(data))
ourk = np.array([d["k"] for d in data])
sig = np.array([d["sigma_pcm"] for d in data])
serp = np.array([d["ref_serpent"] for d in data])
their = np.array([d["ref_openmc"] for d in data])
dk = np.array([d["dk_serpent_pcm"] for d in data])
xl = [lab[d["state"]] for d in data]

# --- Fig 1: k_eff overlay + residuals ---
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6.6), height_ratios=[2, 1], sharex=True)
a1.plot(x, serp, "s", ms=9, mfc="none", mec="#1f6fb5", label="Serpent reference", zorder=2)
a1.plot(x, their, "^", ms=7, mfc="none", mec="#2a9d8f", label="Ez Aldeen OpenMC", zorder=2)
a1.errorbar(x, ourk, yerr=sig / 1e5, fmt="o", ms=6, capsize=4, color="#b5341f",
            label="Aegis-40 OpenMC (VII.1)", zorder=3)
a1.set_ylabel("$k_{eff}$"); a1.grid(alpha=0.3); a1.legend(fontsize=9)
a1.set_title("NuScale-like benchmark — $k_{eff}$ across control-rod states\n"
             "Aegis-40 OpenMC vs published reference (ENDF/B-VII.1)")
a2.axhline(0, color="0.5", lw=1)
a2.errorbar(x, dk, yerr=sig, fmt="o", ms=6, capsize=4, color="#b5341f")
for xi, d in zip(x, dk):
    a2.annotate(f"{d:+.0f}", (xi, d), textcoords="offset points",
                xytext=(0, 9), ha="center", fontsize=8)
a2.set_ylabel("our − Serpent\n(pcm)"); a2.grid(alpha=0.3)
a2.set_xticks(x); a2.set_xticklabels(xl)
fig.tight_layout(); fig.savefig(f"{D}/nuscale_keff_states.png", dpi=140)

# --- Fig 2: CRW parity ---
cs = [d for d in data if d["ref_crw"] is not None]
ourc = np.array([d["crw_pcm"] for d in cs])
refc = np.array([d["ref_crw"] for d in cs])
sig_aro = data[0]["sigma_pcm"]
csig = np.array([np.hypot(d["sigma_pcm"], sig_aro) for d in cs])
fig2, ax = plt.subplots(figsize=(6.6, 6))
lim = [min(refc.min(), ourc.min()) * 1.08, 0]
ax.plot(lim, lim, "--", color="0.5", label="y = x")
ax.errorbar(refc, ourc, yerr=csig, fmt="o", ms=9, capsize=4, color="#b5341f")
for d in cs:
    ax.annotate(lab[d["state"]].replace("\n", " "), (d["ref_crw"], d["crw_pcm"]),
                textcoords="offset points", xytext=(9, -4), fontsize=8.5)
ax.set_xlabel("reference control-rod worth (pcm)")
ax.set_ylabel("Aegis-40 OpenMC CRW (pcm)")
ax.set_title("NuScale-like benchmark — control-rod worths\nAegis-40 OpenMC vs reference")
ax.legend(); ax.grid(alpha=0.3); ax.set_aspect("equal", adjustable="box")
fig2.tight_layout(); fig2.savefig(f"{D}/nuscale_crw_parity.png", dpi=140)
print("wrote nuscale_keff_states.png + nuscale_crw_parity.png")
