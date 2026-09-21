# -*- coding: utf-8 -*-
"""Assemble the Zenodo deposit package for the SBF rod-worth paper.

Lives in the repository (not a scratch directory) so it survives; an earlier
copy was lost when the session scratchpad was cleared.

    python code/build_zenodo.py

Produces  zenodo-deposit/  and  Aegis40-SBF-rod-worth-zenodo-v<VERSION>.zip
next to the manuscript, with a SHA-256 manifest over every file.

VERSION HISTORY
  1.0.0  published as doi:10.5281/zenodo.22657948 - R1-R3 results
  1.1.0  adds the R4 adjoint-weighted IFP beta_eff runs (5/10/20 generations)
         and run_ifp_beta_eff.py. Requires a NEW Zenodo version: files on a
         published record are immutable, so this cannot replace v1.0.0 in
         place. Use "New version" on the record; the concept DOI keeps
         resolving to the latest.
"""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

VERSION = "1.1.0"

PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[3]
MODEL = REPO / "openmc_model" / "safety_85_86"
DEP = PAPER / "zenodo-deposit"
ZIP = PAPER / ("Aegis40-SBF-rod-worth-zenodo-v%s.zip" % VERSION)

# figure scripts live inside the deposit tree itself (they were authored there)
KEEP_FROM_DEPOSIT = ("code/make_figures.py", "code/fig3_design_space.py")
stash = {}
for rel in KEEP_FROM_DEPOSIT:
    p = DEP / rel
    if p.exists():
        stash[rel] = p.read_bytes()

if DEP.exists():
    shutil.rmtree(DEP)
for sub in ("code", "data", "figures"):
    (DEP / sub).mkdir(parents=True)
for rel, blob in stash.items():
    (DEP / rel).write_bytes(blob)
    print("  = kept          %s" % rel)


def put(src, dest_sub, rename=None):
    src = Path(src)
    if not src.exists():
        print("  MISSING (skipped):", src)
        return
    shutil.copy2(src, DEP / dest_sub / (rename or src.name))
    print("  + %-14s %s" % (dest_sub + "/", rename or src.name))


print("[collect] code")
put(MODEL / "aegis40_safety_neutronics.py", "code")
put(PAPER / "code" / "run_paper_extra_cases.py", "code")
put(PAPER / "code" / "run_ifp_beta_eff.py", "code")

print("[collect] data")
for f in ("safety_neutronics_results.json", "beta_eff_results.json",
          "rea_n5c_results.json", "rea_tfuel900_results.json",
          "mslb_n5c_results.json", "paper_extra_cases.json",
          "ifp_beta_eff_g5.json", "ifp_beta_eff_g10.json",
          "ifp_beta_eff_g20.json"):
    src = PAPER / "data" / f
    if not src.exists():
        src = PAPER / "code" / f
    put(src, "data")
put(PAPER / "code" / "RESULTS_R1-R3.md", "data")

print("[collect] figures")
for f in sorted((PAPER / "figures").glob("*.png")):
    put(f, "figures")

# ---------------------------------------------------------------- licences
(DEP / "LICENSE-CODE.txt").write_text(
    "MIT License\n\n"
    "Copyright (c) 2026 S. Achilova and L. Ismailov,\n"
    "New Uzbekistan University, Tashkent, Uzbekistan.\n\n"
    "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
    "of this software and associated documentation files (the \"Software\"), to deal\n"
    "in the Software without restriction, including without limitation the rights\n"
    "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
    "copies of the Software, and to permit persons to whom the Software is\n"
    "furnished to do so, subject to the following conditions:\n\n"
    "The above copyright notice and this permission notice shall be included in all\n"
    "copies or substantial portions of the Software.\n\n"
    "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
    "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
    "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
    "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
    "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
    "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
    "SOFTWARE.\n", encoding="utf-8")

(DEP / "LICENSE-DATA.txt").write_text(
    "Creative Commons Attribution 4.0 International (CC BY 4.0)\n\n"
    "The result files under data/ and the figures under figures/ are licensed\n"
    "CC BY 4.0. You may share and adapt them for any purpose, including\n"
    "commercially, provided you give appropriate credit.\n\n"
    "Full text: https://creativecommons.org/licenses/by/4.0/legalcode\n",
    encoding="utf-8")

# ---------------------------------------------------------------- metadata
CREATORS = [
    dict(name="Achilova, Samira",
         affiliation="New Uzbekistan University, Tashkent, Uzbekistan"),
    dict(name="Ismailov, Laziz",
         affiliation="New Uzbekistan University, Tashkent, Uzbekistan"),
]

DESC = (
    "<p>Model input, run scripts and complete result files for the study "
    "<em>&ldquo;Relaxing the rod-ejection constraint in soluble-boron-free PWR "
    "cores: attainable control-rod worth and residual boron dependency with "
    "in-vessel drives&rdquo;</em>.</p>"
    "<p>All results are continuous-energy Monte Carlo eigenvalue calculations "
    "with <strong>OpenMC 0.15.3</strong> and <strong>ENDF/B-VIII.0</strong> on a "
    "fully three-dimensional, pin-explicit model of a 125 MW<sub>th</sub>, "
    "37-assembly, 17&times;17, 2.0 m active-height natural-circulation integral "
    "PWR with in-vessel control-rod drives. No assembly homogenisation or "
    "few-group condensation is used at any stage.</p>"
    "<p><strong>New in version 1.1.0</strong>: adjoint-weighted effective "
    "delayed-neutron fraction by the iterated-fission-probability method at 5, "
    "10 and 20 IFP generations (<code>data/ifp_beta_eff_g*.json</code>), with "
    "the driver <code>code/run_ifp_beta_eff.py</code>. These confirm the "
    "prompt-k estimate used in the first version to within 0.8 %.</p>"
    "<p><strong>Contents</strong></p><ul>"
    "<li><code>code/aegis40_safety_neutronics.py</code> &mdash; the core model "
    "and the published safety-neutronics case suite.</li>"
    "<li><code>code/run_paper_extra_cases.py</code> &mdash; single-cluster worth "
    "by symmetry class, the 16-cluster natural-B<sub>4</sub>C corner of the lever "
    "matrix, and the boron sweep bracketing the cold-shutdown crossing.</li>"
    "<li><code>code/run_ifp_beta_eff.py</code> &mdash; adjoint-weighted "
    "&beta;<sub>eff</sub> by IFP.</li>"
    "<li><code>code/make_figures.py</code>, <code>code/fig3_design_space.py</code> "
    "&mdash; generate the four manuscript figures.</li>"
    "<li><code>data/</code> &mdash; every eigenvalue reported in the manuscript, "
    "as JSON, plus a run log with a model-reproduction check.</li>"
    "<li><code>figures/</code> &mdash; the four manuscript figures at 300 dpi.</li>"
    "<li><code>MANIFEST.sha256</code> &mdash; SHA-256 of every file.</li></ul>"
    "<p>Code is released under the MIT licence; result files and figures under "
    "CC BY 4.0.</p>"
)

(DEP / "zenodo-metadata.json").write_text(json.dumps({"metadata": {
    "upload_type": "dataset",
    "title": ("Model, scripts and results for: Relaxing the rod-ejection "
              "constraint in soluble-boron-free PWR cores "
              "(Aegis-40 integral PWR, OpenMC)"),
    "creators": CREATORS,
    "description": DESC,
    "access_right": "open",
    "license": "cc-by-4.0",
    "language": "eng",
    "version": VERSION,
    "keywords": [
        "soluble-boron-free", "small modular reactor", "integral PWR",
        "control-rod worth", "rod-ejection accident", "shutdown margin",
        "effective delayed neutron fraction", "iterated fission probability",
        "Monte Carlo", "OpenMC", "ENDF/B-VIII.0", "reactor physics",
    ],
    "notes": ("Supplementary material for a manuscript submitted to Nuclear "
              "Engineering and Design. The reference core was developed for the "
              "TEKNOFEST 2026 Detailed Design Competition (Nuclear, 40 MWe "
              "Modular PWR)."),
    "related_identifiers": [
        {"relation": "isNewVersionOf",
         "identifier": "10.5281/zenodo.22657948",
         "resource_type": "dataset"},
        {"relation": "isSupplementTo",
         "identifier": "TO BE ADDED - the article DOI once accepted",
         "resource_type": "publication-article"},
    ],
}}, indent=2, ensure_ascii=False), encoding="utf-8")

(DEP / "README.md").write_text("""# Zenodo deposit v%s — soluble-boron-free control-rod worth study

Supplementary model, scripts and results for:

> **Relaxing the rod-ejection constraint in soluble-boron-free PWR cores:
> attainable control-rod worth and residual boron dependency with in-vessel drives**
> S. Achilova, L. Ismailov — New Uzbekistan University, Tashkent, Uzbekistan

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
""" % VERSION, encoding="utf-8")

# ---------------------------------------------------------------- manifest
lines = []
for p in sorted(DEP.rglob("*")):
    if p.is_file() and p.name != "MANIFEST.sha256":
        lines.append("%s  %s" % (hashlib.sha256(p.read_bytes()).hexdigest(),
                                 p.relative_to(DEP).as_posix()))
(DEP / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(DEP.rglob("*")):
        if p.is_file():
            z.write(p, p.relative_to(DEP.parent).as_posix())

total = sum(p.stat().st_size for p in DEP.rglob("*") if p.is_file())
print("\nversion : %s" % VERSION)
print("files   : %d  (%.1f MB)" % (len(lines), total / 1e6))
print("zip     : %s  (%.1f MB)" % (ZIP.name, ZIP.stat().st_size / 1e6))
