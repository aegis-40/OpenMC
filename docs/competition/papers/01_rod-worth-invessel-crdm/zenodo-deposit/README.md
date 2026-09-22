# Zenodo deposit v1.1.0 — soluble-boron-free control-rod worth study

Supplementary model, scripts and results for:

> **Relaxing the rod-ejection constraint in soluble-boron-free PWR cores:
> attainable control-rod worth and residual boron dependency with in-vessel drives**
> S. Achilova (New Uzbekistan University, Tashkent, Uzbekistan) and L. Ismailov (independent researcher)

Version 1.0.0 is archived at doi:10.5281/zenodo.22657948. This version adds the
adjoint-weighted beta_eff runs.

## Contents

| Path | Contents |
|---|---|
| `code/aegis40_safety_neutronics.py` | Core model and the published safety-neutronics case suite. |
| `code/run_paper_extra_cases.py` | R1-R3: single-cluster worth by symmetry class, the 16-cluster natural-B4C lever corner, the boron sweep. |
| `code/run_ifp_beta_eff.py` | R4: adjoint-weighted beta_eff by iterated fission probability. |
| `code/make_figures.py`, `code/fig3_design_space.py` | Generate the four manuscript figures. |
| `data/*.json` | Every eigenvalue reported in the manuscript. |
| `data/RESULTS_R1-R3.md` | Run log, including a model-reproduction check. |
| `figures/*.png` | The four manuscript figures, 300 dpi. |
| `MANIFEST.sha256` | SHA-256 of every file. |

## Computational basis

- **OpenMC 0.15.3**, continuous-energy, **ENDF/B-VIII.0**
- Fully 3-D, pin-explicit across all 37 assemblies. No assembly homogenisation
  or few-group condensation at any stage.
- Ladder and shutdown cases: 180 batches x 20,000 particles, 50 inactive.
- beta_eff, single-cluster worths and the IFP runs: 400 batches x 50,000
  particles, 80 inactive (~1.6e7 active histories).
- Acceptance metric `k_adj = k + 2 sigma + 0.005`; shutdown margin reported
  **signed**, `SDM = -(k - 1)/k`, so a supercritical state is negative.

## beta_eff

| Method | Value (pcm) |
|---|---|
| prompt-k, `1 - k_p/k` | 704.5 +/- 28.2 |
| IFP, 5 generations | 708.1 +/- 5.4 |
| IFP, 10 generations | 698.9 +/- 7.3 |
| IFP, 20 generations | 700.0 +/- 9.8 |

The three IFP runs share the same neutron histories, so their spread is a
convergence effect rather than an independent statistical test. The manuscript
adopts the 5-generation value for its dollar figures because it is the highest
of the three and therefore least favourable to the conclusion that the ejected
cluster exceeds one dollar.

## Reproducing

```bash
export OPENMC_THREADS=8
python run_paper_extra_cases.py all     # R1-R3
python run_ifp_beta_eff.py              # R4
```

Both import the locked model rather than redefining it, and checkpoint after
every eigenvalue run, so they are safe to interrupt and restart. Run from the
folder holding `aegis40_safety_neutronics.py`, or set `AEGIS_MODEL_DIR`.

## Verifying integrity

```bash
sha256sum -c MANIFEST.sha256
```

## Licence

Code (`code/`) — MIT. Data and figures (`data/`, `figures/`) — CC BY 4.0.
