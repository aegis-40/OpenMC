# Zenodo record status — checked 2026-09-22

> **Both records are already PUBLISHED and Open Access.** Verified against the
> Zenodo API on 22 Sep 2026. Nothing needs uploading; the deposit task is done.
>
> | DOI | Version | Access | Files | State |
> |---|---|---|---|---|
> | `10.5281/zenodo.22657948` | v1.0.0 | Open, CC BY 4.0 | 20 | superseded |
> | `10.5281/zenodo.22878679` | v1.1.0 | Open, CC BY 4.0 | 24 | **current — cited by the manuscript** |
>
> The v1.1.0 file list matches the built package exactly, including
> `ifp_beta_eff_g{5,10,20}.json` and `run_ifp_beta_eff.py`.
>
> **Files on a published record are immutable. Metadata is not** — the edits
> below can and should still be made.
>
> ### Metadata corrections outstanding on `22878679`
>
> 1. **Add the third creator:** `Sanetullaev, Alisher` —
>    `New Uzbekistan University, Tashkent, Uzbekistan`, third in order.
> 2. **Laziz's affiliation is blank on the live record.** Set it to
>    `Central Asian University of Environmental and Climate Change Studies (Green University), Tashkent, Uzbekistan` — taken from his ORCID employment record
>    (Chief Specialist, from July 2026). (The live record does *not* wrongly say
>    New Uzbekistan University — that error never reached Zenodo, and
>    “Independent researcher” was only ever a placeholder.)
> 3. **The notes field says "Nuclear Engineering and Design".** It should read
>    *Nuclear Engineering and Technology* — see the Additional notes section below.
> 4. **On acceptance:** add the article DOI as `isSupplementTo`.
>
> ### Same corrections on `22657948` (optional, tidiness only)
>
> Add Laziz's affiliation. Leave the creator list at two names if you prefer —
> that record is a snapshot of the pre-IFP state and is superseded.
>
> ### Restricting access is not an option
>
> Considered and ruled out: open files on a published Zenodo record cannot be
> pulled back to restricted, and v1.0.0 has been openly downloadable with the
> complete model since publication. The manuscript's *Data availability*
> section therefore stays as it is, citing `10.5281/zenodo.22878679`.

---

# Canonical metadata (reference copy)

Paste each field below into the Zenodo deposit form, top to bottom. This replaces the earlier scratchpad copy of this guide, which is gone; it also **supersedes** two earlier affiliations given for Laziz Ismailov: New Uzbekistan University (wrong) and *Independent researcher* (a placeholder). His affiliation is the Central Asian University of Environmental and Climate Change Studies (Green University), Tashkent, per his ORCID employment record.

**Upload the file:** `Aegis40-SBF-rod-worth-zenodo-v1.1.0.zip` (1.5 MB)

SHA-256: `6d273d4b522abb70226ad4bdec47161b7c561a6e7d397de82ab3e1d5431597ff`

---

## Upload type

**Dataset**

## Title

```
Model, scripts and results for: Relaxing the rod-ejection constraint in soluble-boron-free PWR cores (Aegis-40 integral PWR, OpenMC)
```

## Authors — exactly three, in this order

| # | Name (family, given) | Affiliation |
|---|---|---|
| 1 | `Achilova, Samira` | `New Uzbekistan University, Tashkent, Uzbekistan` |
| 2 | `Ismailov, Laziz` | `Central Asian University of Environmental and Climate Change Studies (Green University), Tashkent, Uzbekistan` |
| 3 | `Sanetullaev, Alisher` | `New Uzbekistan University, Tashkent, Uzbekistan` |

> ⚠ Do **not** put New Uzbekistan University against Laziz Ismailov — only against Achilova and Sanetullaev. The live v1.1.0 record still lists two creators with Laziz's affiliation blank, so both the third creator and his affiliation need adding. Metadata stays editable after publishing even though files do not.

> **ORCID iDs:** Zenodo accepts an ORCID per creator and Elsevier's submission system will ask for one. Laziz's affiliation above comes from his ORCID record, so the iD is to hand — add all three iDs here and on the record when you have them.

## Description

Switch the description box to HTML/rich text and paste:

```html
<p>Model input, run scripts and complete result files for the study <em>&ldquo;Relaxing the rod-ejection constraint in soluble-boron-free PWR cores: attainable control-rod worth and residual boron dependency with in-vessel drives&rdquo;</em>.</p><p>All results are continuous-energy Monte Carlo eigenvalue calculations with <strong>OpenMC 0.15.3</strong> and <strong>ENDF/B-VIII.0</strong> on a fully three-dimensional, pin-explicit model of a 125 MW<sub>th</sub>, 37-assembly, 17&times;17, 2.0 m active-height natural-circulation integral PWR with in-vessel control-rod drives. No assembly homogenisation or few-group condensation is used at any stage.</p><p><strong>New in version 1.1.0</strong>: adjoint-weighted effective delayed-neutron fraction by the iterated-fission-probability method at 5, 10 and 20 IFP generations (<code>data/ifp_beta_eff_g*.json</code>), with the driver <code>code/run_ifp_beta_eff.py</code>. These confirm the prompt-k estimate used in the first version to within 0.8 %.</p><p><strong>Contents</strong></p><ul><li><code>code/aegis40_safety_neutronics.py</code> &mdash; the core model and the published safety-neutronics case suite.</li><li><code>code/run_paper_extra_cases.py</code> &mdash; single-cluster worth by symmetry class, the 16-cluster natural-B<sub>4</sub>C corner of the lever matrix, and the boron sweep bracketing the cold-shutdown crossing.</li><li><code>code/run_ifp_beta_eff.py</code> &mdash; adjoint-weighted &beta;<sub>eff</sub> by IFP.</li><li><code>code/make_figures.py</code>, <code>code/fig3_design_space.py</code> &mdash; generate the four manuscript figures.</li><li><code>data/</code> &mdash; every eigenvalue reported in the manuscript, as JSON, plus a run log with a model-reproduction check.</li><li><code>figures/</code> &mdash; the four manuscript figures at 600 dpi.</li><li><code>MANIFEST.sha256</code> &mdash; SHA-256 of every file.</li></ul><p>Code is released under the MIT licence; result files and figures under CC BY 4.0.</p>
```

## Version

`1.1.0`

## Language

`English`

## Keywords — 12, one per box

- `soluble-boron-free`
- `small modular reactor`
- `integral PWR`
- `control-rod worth`
- `rod-ejection accident`
- `shutdown margin`
- `effective delayed neutron fraction`
- `iterated fission probability`
- `Monte Carlo`
- `OpenMC`
- `ENDF/B-VIII.0`
- `reactor physics`

## Licence / access

- Access right: **Open Access**
- Licence: **Creative Commons Attribution 4.0 International (CC BY 4.0)**
- The code inside the archive is **MIT** — stated in `LICENSE-CODE.txt`, not settable as a second licence in the Zenodo form.

## Related / alternate identifiers

| Relation | Identifier | Resource type |
|---|---|---|
| isNewVersionOf | `10.5281/zenodo.22657948` | dataset |
| isSupplementTo | `TO BE ADDED - the article DOI once accepted` | publication-article |

The `isSupplementTo` row is a placeholder: leave it out now, and add the article DOI once *Nuclear Engineering and Technology* accepts the paper.

## Additional notes

```
Supplementary material for a manuscript submitted to Nuclear Engineering and Technology. The reference core was developed for the TEKNOFEST 2026 Detailed Design Competition (Nuclear, 40 MWe Modular PWR).
```

---

## After publishing

1. Open <https://doi.org/10.5281/zenodo.22878679> and confirm it resolves to a **published** record — a reserved DOI 404s until you press Publish.
2. Check that the author list on the live page reads *Achilova, Samira; Ismailov, Laziz* with the two different affiliations.
3. Edit the v1.0.0 record's affiliation for Laziz.
4. The manuscript's *Data availability* section already cites this DOI; no edit needed there.
5. Keep the record **public** — NET requires the data statement to point at something a reviewer can open.
