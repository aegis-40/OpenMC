# Aegis-40 Core Digital Twin — 5–7 day plan (simple, real)

## What it is (and isn't)
A **surrogate-model digital twin of the reactor core**: a fast ML / reduced-order model trained on the
**physics you already ran** (OpenMC STAT_FINAL neutronics + the OpenFOAM/correlation thermal stack +
the depletion curve), wrapped in a **live interactive dashboard** that predicts the full core state
(k_eff, power map, fuel/clad temperatures, margins) in **milliseconds** as operating inputs change,
plus a **simple transient mode**. This is the NVIDIA-blog idea (PhysicsNeMo/neural-operator surrogates
replacing slow simulation for real-time prediction) at a one-person, one-week scale.

*It is NOT* a high-fidelity real-time coupled simulator or a sensor-connected plant twin (there is no
physical plant) — and we say so. It demonstrates the twin **concept**: physics → fast surrogate →
real-time state + monitoring, which is exactly §8.7.6.

## Architecture (4 layers)
1. **Physics/data layer** — a parameter sweep of the existing decks → training data.
2. **Surrogate layer** — scalar ML models (k, coeffs, peaking, MDNBR) + a POD/PCA reduced-order model
   for the *spatial* power map.
3. **State/dynamics layer** — point-kinetics + lumped fuel/coolant thermal feedback, driven by the
   surrogate's reactivity coefficients (MTC/DTC) → a transient that the twin "follows."
4. **Interface layer** — a Streamlit dashboard: input sliders → live core state, power heat-map, axial
   profile, margin gauges, PASS/FAIL flags, scenario playback.

## Inputs → Outputs the twin predicts
**Inputs (sliders):** power level (50–100 %), core inlet/moderator T, control-rod insertion (0–100 %),
burnup / time-in-life, void fraction.
**Outputs (instant):** k_eff & reactivity, per-assembly power map + axial shape, F_q / F_ΔH, MTC/DTC/void,
peak fuel-centerline & clad T, MDNBR, SDM/shutdown state, all vs their LCO limits.

## Day-by-day
**Day 1 — Data generation (neutronics sweep).** Reuse the `ref_static`/safety harness to run an OpenMC
eigenvalue + peaking sweep over a Latin-Hypercube design (~60–120 points) of {moderator-T, rod-insertion,
void, burnup-step from the existing depletion}. Each point ~1–3 min; log k, F_q/F_ΔH, coeffs, the
per-assembly fission map. *(Deliverable: `twin/data/core_sweep.csv` + per-point power maps.)*

**Day 2 — Data: thermal + burnup axis.** Pull the depletion k(BU)/inventory you already have; generate
the thermal responses by driving the **CFD correlation stack** (W-3/Jens-Lottes — instant) over the
power/flow grid → fuel/clad T, MDNBR. Assemble the clean `inputs→outputs` training table.

**Day 3 — Scalar surrogates.** Fit lightweight models per output (Gaussian-Process or small MLP via
scikit-learn / PyTorch): k_eff, F_q, F_ΔH, MTC, DTC, void, MDNBR, peak T. Hold-out validation (target
R² > 0.98, error < a few % / < ~50 pcm on k). *(Deliverable: `twin/surrogates/*.pkl` + a validation
plot.)*

**Day 4 — Spatial power-map ROM.** POD/PCA on the per-assembly power maps → 3–6 modes capture >99 % var;
regress the mode coefficients on the inputs. Now the twin reconstructs the **full radial power map +
axial profile**, not just scalars — the visual centerpiece.

**Day 5 — Dashboard (MVP complete).** Streamlit app: sliders → live k_eff, power heat-map, axial plot,
fuel/clad-T and MDNBR gauges, margin PASS/FAIL lights, all updating <1 s. This alone is a credible,
demoable digital twin.

**Day 6 — Transient mode (the "twin" dimension).** Point-kinetics (6 delayed groups) + lumped
fuel/coolant thermal model using the surrogate's MTC/DTC; play a scenario (load change, rod step,
overcooling) and watch power/T/MDNBR evolve in time — shows the twin *responding*, not just calculating.

**Day 7 — Validate, polish, write up.** Cross-check 3–5 dashboard points against fresh full OpenMC/CFD
runs (the twin's credibility claim); record a GIF; write the **§8.7.6 FER subsection** + an architecture
figure; note the **PhysicsNeMo / Fourier-Neural-Operator scale-up path** as the production roadmap.

## Tools
Python · scikit-learn (GP/PCA) or a small PyTorch MLP · Streamlit (dashboard) · plotly/matplotlib · your
existing OpenMC harness + CFD correlation stack. *(No GPU required; NVIDIA PhysicsNeMo/FNO is cited as
the scale-up, not built in week 1.)*

## Cut-lines (if behind)
- Drop Day 6 transient → static twin still stands (MVP = Days 1–5).
- Drop Day 4 spatial ROM → show per-assembly scalars only.
- Shrink the sweep to ~40 points (coarser but trains).

## FER value
- **§8.7.6 originality:** an AI-physics surrogate digital twin built on the team's own validated
  OpenMC/CFD — real, not hand-wave.
- **Sustainability/operations narrative:** real-time margin monitoring + operator-advisory + cheap
  what-if without re-running hours of simulation.
- **Honesty:** framed as a *surrogate/advisory* twin trained on plant-design physics, with the
  neural-operator path named for scale-up.
