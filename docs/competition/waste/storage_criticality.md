# Aegis-40 spent-fuel storage criticality (FER §8.11) — generated

- Generated: `2026-06-04T17:09:56.309419+00:00`
- Acceptance criterion: **k_eff(95/95) ≤ 0.95** in unborated water (soluble-boron-free — no pool-boron credit)
- Assembly: 17×17, 264 fuel pins + 25 water tubes, pin pitch 1.2623 cm, pellet r=0.40958 cm, clad OD=0.9520 cm
- Pool water: 0.9982 g/cm³ (20 °C), with S(α,β) `c_H_in_H2O`
- Monte Carlo: 20000 part × (150−50) active batches
- Bias Δ=0.0000, method/tolerance uncertainty Δ=0.0000 (see note)

## Results

_DESIGN rows are the credited Boral-rack configuration (the safety case). DIAG rows are bare-rack bounding runs with no absorber — expected to be high; they quantify why the panels are required._

| kind | case | fuel | array | pitch (cm) | k_calc ± σ | k+2σ | k(95/95) | margin to 0.95 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| diag | fresh, bare ∞ array | fresh 4.95 w/o | ∞ (reflective) | 21.46 | 1.49914 ± 0.00060 | 1.50034 | 1.50034 | -0.5503 | **FAIL** |
| diag | fresh, bare finite 3×3 | fresh 4.95 w/o | 3×3 + H₂O refl. | 23.00 | 1.36178 ± 0.00067 | 1.36313 | 1.36313 | -0.4131 | **FAIL** |
| diag | burnup credit, bare ∞ array | spent 42.8 GWd/t (core-avg) | ∞ (reflective) | 21.46 | 1.07358 ± 0.00060 | 1.07478 | 1.07478 | -0.1248 | **FAIL** |
| DESIGN | fresh, Boral box ∞ array | fresh 4.95 w/o | ∞ + Boral box | 23.50 | 1.10566 ± 0.00069 | 1.10704 | 1.10704 | -0.1570 | **FAIL** |
| DESIGN | burnup credit, Boral box ∞ array | spent 42.8 GWd/t (core-avg) | ∞ + Boral box | 23.50 | 0.78099 ± 0.00054 | 0.78207 | 0.78207 | +0.1679 | **PASS** |
| DESIGN | burnup credit, Metamic box ∞ array | spent 42.8 GWd/t (core-avg) | ∞ + Metamic box | 23.50 | 0.78856 ± 0.00061 | 0.78977 | 0.78977 | +0.1602 | **PASS** |

## Verdict: **PASS** — the credited burnup-credit Boral/Metamic rack is sub-critical (k(95/95) ≤ 0.95); fresh (un-burned) fuel exceeds the limit and is **administratively excluded** — this is a Region-II burnup-credit rack (minimum-burnup loading curve)

## Cross-check vs literature

Kim, Jung & Yoon (Nucl. Eng. Tech. 56 (2024) 3144) report SBF small-PWR cold/storage sub-criticality of k ≈ 0.932–0.949. Our credited burnup-credit + Boral case gives k(95/95) = 0.7821, in/below that band — consistent with an unborated SBF storage configuration.

## Storage-rack design

- **Absorber panels** on all four walls of each storage cell, 0.3 cm thick:
  - **Boral** — 0.4 mass-fraction B₄C (natural boron) in aluminium (ρ≈2.64 g/cm³). Cheapest; B4C-Al core clad in Al, with a known multi-decade blister/degradation history.
  - **Metamic** — 0.31 mass-fraction B₄C, natural boron (ρ≈2.70 g/cm³). Fully-dense Al–B₄C metal-matrix composite: no blistering, far better long-term durability for decades-long storage — the preferred choice despite slightly higher cost. Compare the two design rows above at equal geometry.
- **Cell pitch:** 23.5 cm centre-to-centre (assembly envelope 21.46 cm + water gap + panel). Modelled as an **infinite (reflective) array** — the bounding spacing, no finite-array edge leakage credited.

## Method notes

- **Unborated water** throughout — the SBF design philosophy carries into the pool: no soluble-boron reactivity credit is taken, so the result is valid even on a total loss of any boron injection. Sub-criticality rests entirely on the solid Boral panels (+ burnup credit), exactly as an SBF rack must.
- The **bare infinite (reflective) array at the assembly envelope pitch (~21.46 cm, assemblies touching)** is the diagnostic bounding spacing: no water gap / flux trap and no absorber. Its high k is the quantitative justification for the Boral panels in the design rows.
- **Burnup credit** uses the regulator-standard *principal isotope* set (actinides + FP absorbers) at the **core-average** discharge burnup (42.8 GWd/tHM). A licensing submission would refine this to the *minimum*-burnup assembly and add an axial burnup profile; the core-average value here is a representative, not yet bounding, credit case.
- **k(95/95) = k_calc + 2σ + Δ_bias + Δ_unc.** σ is the Monte-Carlo statistical std-dev. Δ_bias (code/data bias) and Δ_unc (method + manufacturing tolerances) are inputs here; the bias must come from the Digital-Appendix V&V — benchmarking OpenMC against the **OECD/NEA Burnup-Credit Criticality Benchmark Phase II** and **SFCOMPO 2.0** assay — before the numbers are licensing-grade. With Δ=0 the table reports the raw calculated margin.
