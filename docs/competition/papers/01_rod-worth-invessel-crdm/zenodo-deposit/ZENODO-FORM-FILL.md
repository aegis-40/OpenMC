# Zenodo form — what to put in each field (v1.1.0)

For record **10.5281/zenodo.22878679**. Copy each block into the matching field.

Predecessor: **10.5281/zenodo.22657948** (v1.0.0).

---

## Files

Upload **`Aegis40-SBF-rod-worth-zenodo-v1.1.0.zip`** (23 files, 0.7 MB) from
`docs/competition/papers/01_rod-worth-invessel-crdm/`.

If the old `v1.0.0.zip` was carried over into this record, **remove it** — one
zip per record, otherwise readers get two overlapping copies.

## Resource type

```
Dataset
```

## Title

```
Model, scripts and results for: Relaxing the rod-ejection constraint in soluble-boron-free PWR cores (Aegis-40 integral PWR, OpenMC)
```

## Publication date

```
2026-09-21
```

## Authors / Creators

**Two authors.** Samira stays marked as Contact person.

| Family name | Given name | Affiliation |
|---|---|---|
| Achilova | Samira | New Uzbekistan University |
| Ismailov | Laziz | New Uzbekistan University |

⚠ **Fill Laziz's affiliation** — it was left blank on v1.0.0.

## Description

```
Model input, run scripts and complete result files for the study "Relaxing the rod-ejection constraint in soluble-boron-free PWR cores: attainable control-rod worth and residual boron dependency with in-vessel drives".

All results are continuous-energy Monte Carlo eigenvalue calculations with OpenMC 0.15.3 and ENDF/B-VIII.0 on a fully three-dimensional, pin-explicit model of a 125 MWth, 37-assembly, 17x17, 2.0 m active-height natural-circulation integral PWR with in-vessel control-rod drives. No assembly homogenisation or few-group condensation is used at any stage.

NEW IN VERSION 1.1.0

Adjoint-weighted effective delayed-neutron fraction by the iterated-fission-probability (IFP) method at 5, 10 and 20 IFP generations (data/ifp_beta_eff_g5.json, _g10, _g20), with the driver code/run_ifp_beta_eff.py. These confirm the prompt-k estimate used in version 1.0.0 to within 0.8 %:

    prompt-k, 1 - k_p/k      704.5 +/- 28.2 pcm
    IFP,  5 generations      708.1 +/-  5.4 pcm
    IFP, 10 generations      698.9 +/-  7.3 pcm
    IFP, 20 generations      700.0 +/-  9.8 pcm

The three IFP runs share the same neutron histories, so their spread is a convergence effect rather than an independent statistical test.

CONTENTS

code/aegis40_safety_neutronics.py - the core model and the published safety-neutronics case suite: rod-worth ladder, cooldown sequence, emergency-boron sizing and spent-fuel-pool criticality.

code/run_paper_extra_cases.py - single-cluster worth resolved by symmetry class, the 16-cluster natural-B4C corner of the absorber-enrichment x cluster-count matrix, and a boron sweep bracketing the cold-shutdown acceptance crossing.

code/run_ifp_beta_eff.py - adjoint-weighted beta_eff by iterated fission probability.

code/make_figures.py and code/fig3_design_space.py - generate the four manuscript figures.

data/ - every eigenvalue reported in the manuscript, as JSON, together with a run log that includes a model-reproduction check: six published states recomputed independently, of which four reproduce to 0 pcm and the worst deviates by 1.3 sigma.

figures/ - the four manuscript figures at 300 dpi.

MANIFEST.sha256 - SHA-256 of every file in the archive.

REPRODUCING

With OpenMC and an ENDF/B-VIII.0 cross-section library available:

    python run_paper_extra_cases.py all
    python run_ifp_beta_eff.py

Both import the locked model rather than redefining it, and checkpoint after every eigenvalue run, so they are safe to interrupt and restart.

LICENSING

Code under code/ is released under the MIT licence (see LICENSE-CODE.txt in the archive). Result files and figures are CC BY 4.0, which is the licence recorded for this record.

The reference core was developed for the TEKNOFEST 2026 Detailed Design Competition, Nuclear category, 40 MWe Modular PWR.
```

## Licenses

```
Creative Commons Attribution 4.0 International
```

Zenodo records one licence; the code inside the archive is MIT, stated in the
description and in `LICENSE-CODE.txt`. That is the normal way to handle a
mixed-licence deposit.

## Copyright

```
Copyright (C) 2026 S. Achilova and L. Ismailov, New Uzbekistan University. Code MIT; data and figures CC BY 4.0.
```

## Keywords and subjects

Add one at a time — twelve, one more than v1.0.0:

```
soluble-boron-free
small modular reactor
integral PWR
control-rod worth
rod-ejection accident
shutdown margin
effective delayed neutron fraction
iterated fission probability
Monte Carlo
OpenMC
ENDF/B-VIII.0
reactor physics
```

## Languages

```
eng
```

## Version

```
1.1.0
```

## Publisher

```
Zenodo
```

## Related works

| Relation | Identifier | Scheme | Resource type |
|---|---|---|---|
| **Is new version of** | `10.5281/zenodo.22657948` | DOI | Dataset |
| **Is derived from** | `https://github.com/aegis-40/OpenMC` | URL | Software |
| *Is supplement to* | *the article DOI, once accepted* | DOI | Publication / Article |

If Zenodo created this record through **New version** on the old one, the first
row may already be implicit — add it only if the field is empty. The third row
waits for journal acceptance; metadata stays editable after publishing.

## Software section

| Field | Value |
|---|---|
| Repository URL | `https://github.com/aegis-40/OpenMC` |
| Programming language | `Python` |
| Development status | `Active` |

## References

Optional. The works this archive is positioned against:

```
Ingremeau, J.-J., & Cordiez, M. (2015). Flexblue core design: optimisation of fuel poisoning for a soluble boron free core with full or half core refuelling. EPJ Nuclear Sciences & Technologies, 1, 11. https://doi.org/10.1051/epjn/e2015-50025-3
```
```
van der Merwe, L., & Hah, C. J. (2018). Reactivity balance for a soluble boron-free small modular reactor. Nuclear Engineering and Technology, 50(4), 648-653. https://doi.org/10.1016/j.net.2018.01.019
```
```
Alzaben, Y., Sanchez-Espinoza, V. H., & Stieglitz, R. (2019). Analysis of a control rod ejection accident in a boron-free small modular reactor with coupled neutronics/thermal-hydraulics code. Annals of Nuclear Energy, 134, 114-124. https://doi.org/10.1016/j.anucene.2019.06.009
```
```
Peng, X., Liang, J., Forget, B., & Smith, K. (2019). Calculation of adjoint-weighted reactor kinetics parameters in OpenMC. Annals of Nuclear Energy, 128, 231-235.
```
```
Fridman, E. (2023). Dataset for neutronics benchmark of a NuScale-like core. RODARE, Helmholtz-Zentrum Dresden-Rossendorf. https://rodare.hzdr.de/record/2457
```

---

## Leave empty

**Funding / Awards**, **Alternate identifiers**, **Journal**, **Imprint**,
**Thesis**, **Conference**, **Dates**, **Contributors**. None applies. Do not
fill *Journal* — that section is for a record that *is* an article; this record
is its supplement, which the *Related works* row expresses.

## After publishing

- The manuscript's *Data availability* and the repository `CITATION.cff` now
  cite **10.5281/zenodo.22878679**. Confirm it resolves in a browser.
- **Also edit v1.0.0** and add Laziz's affiliation there; it stays public and is
  currently missing it. Authorship on v1.0.0 is already correct.
- If you would rather the paper cite the **concept DOI** (the one under "Cite
  all versions", which always resolves to the newest version) instead of this
  version DOI, send it over and it takes one edit.
