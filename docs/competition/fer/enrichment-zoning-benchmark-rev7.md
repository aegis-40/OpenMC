# Enrichment-zoning benchmark — assembly-uniform (literature) vs intra-FA grading (Aegis-40)

**Date:** 2026-06-20 · **Owner:** Samira (neutronics) · **Status:** complete — locked design *retained*

## Purpose
Test, head-to-head and under the reference designs' own conditions, whether Aegis-40's intra-assembly
enrichment grading should be replaced by the standard SBF-SMR recipe (assembly-uniform enrichment +
radial ring zoning + discrete zoned Gd rods + steel reflector). Triggered by the question: *"no one
mixes enrichment within an assembly like us — is it wrong?"*

## Reference designs reproduced
| Design | Power / FAs | Enrichment scheme | Burnable absorber | Reflector | Reported peak |
|---|---|---|---|---|---|
| **ATOM** (Nguyen & Kim, *Sci. Rep.* 11:12891, 2021) | 450 MWth / 69 | assembly-uniform 4.95 (centre FA 3.0) | Gd₂O₃ CSBA, ball-size zoned by ring + B₄C DiBA | SS-304 | F_xy ≈ 1.5 (EOC) |
| **SMART** (Akbari-Jeyhouni et al., *Ann. Nucl. Energy* 120, 2018) | 330 MWth / 57 | 2 assembly-uniform: 2.82 / 4.88 | UO₂+8 wt% Gd₂O₃ rods, count zoned 4–24/FA | baffle | PPF 1.19 |
| **PRATIC** (EPJ-N 2024) | 350 MWth / 57 | 3 rings: 2.5 / 3.5 / 5.0 (assembly-uniform) | UO₂-Gd₂O₃ (8 wt%) rods, count zoned 8/36/28 | heavy steel | F_xy 1.543 (BOC, pin) |

Common principle in all three: **assembly-uniform enrichment + radial ring zoning + discrete zoned Gd +
steel reflector.** None grades enrichment pin-by-pin within an assembly.

## Configurations run (full-core OpenMC, per-pin reconstruction, STAT_MEDIUM 180/50/20 000)
- **rev_6 (locked):** intra-FA 3-zone grade 4.95/4.70/4.40, radial Gd zoning (48/40/26), 20 cm water reflector.
- **rev_7-A:** assembly-uniform rings 3.6 / 4.4 / 4.95 (FA-avg 4.68), **5 cm SS-304 reflector**, Gd uniform at mid-radius.
- **rev_7-B:** as rev_7-A but Gd rods placed on the local hot spots (bias="hotspot": guide-tube-adjacent + assembly-edge; 12 GT + 20 edge of 32).

Notebook: `D:\conda-envs\openmc-py311\SMRs\Revised\aegis40_3d_core_notebook_rev7_zoning.ipynb`
(built from rev6 by `scripts/_make_zoning_study.py`; targeted-Gd by `scripts/_patch_targeted_gd.py`; rev6 untouched).

## Results
| Quantity | rev_6 intra-FA (water) | rev_7-A uniform+steel, mid Gd | rev_7-B uniform+steel, targeted Gd |
|---|---|---|---|
| **F_ΔH (per-pin, raw)** | **1.852** | 1.935 → 1.993 (+unc) | 2.047 → 2.109 (+unc) |
| F_q (separable F_ΔH·F_z) | 2.098 **PASS** | 2.200 → 2.266 | 2.408 → 2.480 **FAIL** |
| F_z (axial) | ~1.13 | 1.137 | 1.176 |
| F_radial (assembly) | **1.23** | 1.450 | 1.481 |
| k_eff, BOL (ARO, no Xe) | 1.0264 | — | **1.06379** ± 60 pcm |
| Hot-pin family | reflector-facing assembly edge | outer assembly edge (no-GT) | interior guide-tube neighbours |

**Limit:** F_ΔH ≤ 1.65 (design 1.55); F_q ≤ 2.32 (design 2.0).

## Findings
1. **rev_6 wins on both peaking metrics** (F_ΔH 1.85 vs 1.94/2.05; F_radial 1.23 vs 1.45/1.48). The
   literature assembly-uniform recipe is worse *even when given a steel reflector and Gd placed on the
   hot pins* — i.e. its failure is not an artefact of our water reflector.
2. **Targeted Gd made it worse, not better.** Moving the 32 Gd rods to the periphery relocated the peak
   from the assembly edge to the interior guide-tube neighbours (2.05). With 24 guide-tube water holes
   per assembly, 32 discrete Gd rods cannot de-peak all the local hot spots at once — a *discrete* tool
   cannot do what *continuous* per-pin enrichment grading does.
3. **k_BOL rose to 1.064** with peripheral Gd: edge positions have low neutron importance, so the same
   Gd holds down *less* reactivity. The core is **under-held-down, not over-poisoned** — directly
   answering the "too much Gd?" concern. Gd material cost is trivial (~52 kg Gd₂O₃ core-wide ≈ a few
   thousand $); its real cost is the residual-Gd reactivity penalty that pushes enrichment up.

## Decision
**Retain the locked rev_6 / rev_3 design** (intra-FA enrichment grading + radial Gd zoning). This is the
third independent confirmation (after rev_4 out-in and rev_5 combined) that, for a compact soluble-boron-free
21-assembly core, continuous intra-assembly enrichment grading is the necessary pin-peak tool. Written into
FER §8.2.3 as Table 8.2-6a.

**Open item:** rev_6 F_ΔH 1.85 still exceeds the 1.65 limit. Mitigation path (in order): (i) confirm at
STAT_FINAL to remove Monte-Carlo noise; (ii) **rev_6 intra-FA + steel baffle** — the one untested 1-line
config predicted to reach 1.5–1.65 (the live rev_6 baseline is still all-water); (iii) equilibrium-cycle
model (burnup flattens the BOC peak the references quote at EOC); (iv) DNBR/thermal-margin analysis to show
acceptable margin at the moderate ~112 W/cm linear heat rate. The reflector — not guide-tube inserts or more
Gd — is rev_6's lever, because rev_6's hot pin is reflector-facing, not guide-tube-driven.
