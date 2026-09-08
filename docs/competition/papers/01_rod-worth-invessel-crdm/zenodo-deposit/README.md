# Zenodo deposit — soluble-boron-free control-rod worth study

Supplementary model, scripts and results for:

> **Relaxing the rod-ejection constraint in soluble-boron-free PWR cores:
> attainable control-rod worth and residual boron dependency with in-vessel drives**
> S. Achilova, L. Ismailov, A. Abdikarimov — New Uzbekistan University, Tashkent, Uzbekistan

Every number reported in the manuscript is reproducible from this archive.

---

## What is here

| Path | Contents |
|---|---|
| `code/aegis40_safety_neutronics.py` | The core model and the published safety-neutronics case suite — rod-worth ladder, cooldown sequence, emergency-boron sizing, spent-fuel-pool criticality. |
| `code/run_paper_extra_cases.py` | The three additional cases (R1–R3) described below. Imports the model above rather than redefining it. |
| `code/fig3_design_space.py` | Generates the design-space figure. |
| `data/*.json` | Every eigenvalue reported in the manuscript. |
| `data/RESULTS_R1-R3.md` | Run log for the R1–R3 cases, including a model-reproduction check. |
| `figures/*.png` | The four manuscript figures, 300 dpi. |
| `MANIFEST.sha256` | SHA-256 of every file in the archive. |

## Computational basis

- **OpenMC 0.15.3**, continuous-energy, **ENDF/B-VIII.0**
- Fully 3-D, pin-explicit across all 37 assemblies. No assembly homogenisation
  or few-group condensation at any stage.
- Ladder and shutdown cases: 180 batches x 20,000 particles, 50 inactive
  (sigma(k) ~ 50-65 pcm).
- beta_eff and the single-cluster worths: 400 batches x 50,000 particles,
  80 inactive (~1.6e7 active histories, sigma(k) ~ 22-26 pcm).
- Acceptance metric: `k_adj = k + 2 sigma + 0.005`. Shutdown margin is reported
  **signed**, `SDM = -(k - 1)/k`, so a supercritical state appears as a negative
  number.

## The three additional cases

| | Case | Closes |
|---|---|---|
| **R1** | Single-cluster worth by symmetry class | Identifies the bounding cluster rather than assuming it |
| **R2** | 16 clusters with natural B4C | Completes the 2x2 lever matrix and resolves the interaction term |
| **R3** | Boron sweep at 700 / 800 / 900 ppm | Brackets the cold-shutdown acceptance crossing directly |

R1 exploits the 8-fold dihedral symmetry of the core map: the sixteen cluster
positions fall into three equivalence classes, so one representative per class
is evaluated at full statistics together with an explicit symmetry check
(agreement 0.6 sigma).

## Reproducing

```bash
# OpenMC and an ENDF/B-VIII.0 library must already be configured
export OPENMC_THREADS=8
python run_paper_extra_cases.py all      # or R1 / R2 / R3 individually
```

The script checkpoints to JSON after every eigenvalue run, so it is safe to
interrupt and restart — completed cases are skipped. Run it from the folder
containing `aegis40_safety_neutronics.py`, or set `AEGIS_MODEL_DIR`.

To regenerate the published safety suite instead, run
`python aegis40_safety_neutronics.py` with `SAFETY_RUN=all`.

## Verifying integrity

```bash
sha256sum -c MANIFEST.sha256
```

## Licence

Code (`code/`) — MIT. Data and figures (`data/`, `figures/`) — CC BY 4.0.
See `LICENSE-CODE.txt` and `LICENSE-DATA.txt`.

## Citing

Please cite the article once published, together with this archive by its
Zenodo DOI. `zenodo-metadata.json` holds the deposition metadata; the
`related_identifiers` field must be updated with the article DOI on acceptance.
