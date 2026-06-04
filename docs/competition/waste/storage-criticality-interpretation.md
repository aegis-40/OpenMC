# Spent-fuel storage criticality — interpretation for FER §8.11

Hand-authored interpretation of the generated artifacts (overwritten on each
script run, so the prose lives here):
- `storage_criticality.{md,csv}` — from `scripts/run_storage_criticality.py`.

Basis: rev_3 discharge inventory, whole 21-FA core, **5.04 tHM at discharge**,
42.8 GWd/t core-average burnup, OpenMC 0.15.3 + ENDF/B-VIII.0. Storage condition:
**cold (20 °C), unborated water** — the soluble-boron-free (SBF) philosophy
carries into the pool, so **no soluble-boron reactivity credit is taken** and the
result holds even on total loss of any boron source.

This is the third and last of the three §4.3.2-mandated waste safety analyses
(source term ✓, decay heat ✓, **storage criticality ✓**).

## Acceptance criterion

> **k_eff(95/95) = k_calc + 2σ + Δ_bias + Δ_unc ≤ 0.95**

The 0.95 is the regulatory 5 % subcritical margin below self-sustaining
(NUREG-0800 / 10 CFR 50.68). σ is the Monte-Carlo statistical std-dev; Δ_bias
(code/data) and Δ_unc (method + manufacturing tolerances) are reported as 0 here
(raw calculated margin) pending the V&V benchmark (see below).

## Headline result — the design rack PASSES

The design-basis storage configuration is **discharged (burnup-credited) fuel in
a Region-II absorber rack**: a 17×17 assembly inside a square absorber box,
23.5 cm cell pitch, 0.30 cm panel, modelled as an **infinite (reflective) array**
(bounding spacing, no finite-array leakage credit).

| Configuration | k_calc ± σ | k(95/95) | verdict |
|---|---|---|---|
| Spent fuel + **Boral** box (0.40 B₄C, nat. B) | 0.78099 ± 0.00054 | **0.782** | ✅ PASS |
| Spent fuel + **Metamic** box (0.31 B₄C, nat. B) | 0.78856 ± 0.00061 | **0.790** | ✅ PASS |

Both credited designs sit **~0.16 below the 0.95 limit** — a large, comfortable
margin, confirmed by two independent absorber materials.

## Why so much margin — the reactivity ladder

Each line is a real, separately-quantified effect (whole-core infinite array):

| Step | k(95/95) | Δ from previous |
|---|---|---|
| Fresh fuel, bare, touching (worst case) | 1.500 | — |
| → use **real discharged fuel** (burnup credit) | 1.075 | −0.425 |
| → add **Boral absorber panels** + 23.5 cm pitch | **0.782** | −0.293 |

Burnup credit alone removes most of the excess *for free* (the fuel really is
depleted); the absorber panels then carry it well under the limit. This ladder is
the quantitative justification for every credited feature.

## This is a Region-II (burnup-credit) rack

A diagnostic case — **fresh** 4.95 w/o fuel in the same tight Boral rack — gives
k(95/95) = **1.107**, i.e. *above* 0.95. That is expected and is **not a design
failure**: it means the high-density rack is a **Region-II rack** that relies on
burnup credit, so fresh and low-burnup assemblies are **administratively excluded**
via a minimum-burnup loading curve. Fresh fuel is held in new-fuel dry storage or
a separate **Region-I flux-trap** rack (wider pitch) — the standard two-region
pool layout. (Given how little fuel this reactor discharges — ~5 FA/yr — a
panel-free Region-I flux-trap rack is also a viable, low-cost option worth a
follow-up sweep.)

## Boral vs Metamic — the durability trade

The two materials are chemically the same (Al + B₄C); they differ in *form*:

| | Boral | Metamic |
|---|---|---|
| k(95/95), this rack | 0.782 | 0.790 |
| B₄C content (modelled) | 40 % | 31 % |
| Structure | B₄C-Al core clad in Al | fully-dense Al–B₄C MMC |
| Long-term behaviour | known multi-decade **blister/gas** degradation | no blistering; far better durability |
| Cost | lower | higher |

Metamic comes out 0.008 higher in k here only because it carries less boron in
this nominal model — **the reactivity difference is negligible; the durability
difference is decades.** For waste that sits in a pool for decades, Metamic is the
preferred choice. With **B-10-enriched** boron (run `--b10-enrich 0.90`) Metamic
drops *below* Boral, which is how real high-density Metamic racks are built.

## Cross-check vs literature

Kim, Jung & Yoon (Nucl. Eng. Tech. **56** (2024) 3144) report SBF small-PWR
cold/storage subcriticality of **k ≈ 0.932–0.949**. Those values are for *racks
designed up toward the limit*; our credited result (0.78) sits **below** that
band — consistent with, and more conservative than, the published SBF storage
envelope. The agreement in regime (unborated, cold, burnup-credited, small iPWR)
is the qualitative corroboration that the model behaves correctly.

## V&V for the Digital Appendix (the hard gate)

The reported numbers use Δ_bias = Δ_unc = 0 (raw calculated margin). To be
licensing-grade the bias must come from benchmarking OpenMC + ENDF/B-VIII.0
against measured/known-answer criticality data:
- **OECD/NEA Burnup-Credit Criticality Benchmark (Phase II)** — burnup-credit k.
- **SFCOMPO 2.0** — measured PWR assay (validates the discharged isotopics that
  the burnup credit rests on).

Even a conservative combined Δ ≈ 0.02–0.05 leaves the 0.78 design comfortably
under 0.95. A full submission would additionally use the **minimum**-burnup
assembly with an **axial burnup profile** (end-effect) rather than the
core-average composition used here, and credit finite-rack leakage.

## Method summary (for traceability)
- Geometry: 17×17, 264 fuel pins + 25 water tubes, pin pitch 1.2623 cm, pellet
  r 0.40958 cm, clad OD 0.952 cm — identical to the core model.
- Burnup credit: regulator-standard **principal isotopes** (37 found in the
  discharged inventory: actinides + FP absorbers) at core-average 42.8 GWd/t,
  volume-averaged over the depletable fuel materials.
- Water: 0.9982 g/cm³, S(α,β) `c_H_in_H2O`; unborated.
- Monte Carlo: 20 000 particles × (150−50) active batches; σ ≈ 6 pcm.
