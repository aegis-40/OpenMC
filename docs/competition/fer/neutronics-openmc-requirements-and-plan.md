# Aegis-40 Neutronics & OpenMC — FER Requirements, Parameter Recommendations, and Final-Days Plan

**Design:** 40 MWe integral PWR SMR for Türkiye · 125 MWth · 21 fuel assemblies · 17×17 · soluble-boron-free (SBF) · Gd+Er integral burnable absorber · ENDF/B-VIII.0
**Author:** neutronics (Samira) · **Status doc date:** 2026-06-19 · **Notebook:** `aegis40_3d_core_notebook_rev6.ipynb`

---

## 0. What the rev6 run actually produced (read before deciding anything)

| Metric | rev6 result | Gate | Verdict |
|---|---|---|---|
| k_eff BOC HFP ARO | 1.0264 (2516 pcm excess) | small +, rod-trimmable | ✅ |
| Discharge burnup (4-batch LRM) | **41.3 GWd/tHM** | 40–45 target, ≤62 hard | ✅ |
| Cycle length | **462.6 EFPD = 15.2 mo** | 12–18 mo | ✅ |
| Shutdown margin (N-1 stuck rod) | **12.38 %Δk/k** | ≥1.3% (design ≥2%) | ✅ |
| MTC / DTC / void | −35.9 / −1.84 / −214 | all < 0 | ✅ |
| CR bank worth (ARI) | 15 226 pcm | — | ✅ |
| Max enrichment | 4.95 wt% | ≤5.0 | ✅ |
| **F_ΔH (radial pin)** | **1.845** | ≤1.65 | ❌ **FAIL** |
| **F_q (3-D pin)** | **3.583** | ≤2.32 | ❌ **FAIL** |

**Conclusion: the ONLY failing metrics are the two peaking factors. Everything that governs safety and cycle economics already passes.** The "23 480 pcm reactivity swing" printed by the notebook is the *full-horizon* fuel-depletion drop to ~170 GWd/t — **not** the in-cycle swing. The in-cycle excess is only 2516 pcm BOC, which rods trim cleanly. So there is no swing problem and no criticality problem.

### Recommendation on the design pivot you raised

- **Do NOT switch to "regular enrichment / 37 assemblies / soluble boron."** That is a ground-up redesign (new geometry, new BA, new everything, re-benchmark) and we do not have the days. Our 21-FA SBF design is *deliberately* differentiated and is backed by peer-reviewed SBF cores (Korean **ATOM**, **CAREM-25**). Walking that back now throws away the strongest, best-documented part of the FER.
- **Keep enrichment at 4.95/4.70/4.40 (avg 4.69).** Burnup is already only 41.3 GWd/t; lowering enrichment pushes burnup *below* target. "Average 4.1–4.3" in the generic baseline is for boron-shimmed cores — we need the extra reactivity because we carry no boron.
- **Keep Er at 0.5 wt% — do NOT raise to 1.0 wt%.** The "Er-167 only 3.1% left" number was an artifact of reading inventory at the end of the ~1900-EFPD diagnostic horizon (~170 GWd/t), not at the 41 GWd/t the fuel actually sees; rev6 already fixed that read to interpolate at cycle EOC. Doubling Er would shorten cycle and cut burnup (the sweep proved Er rods are the dominant parasitic sink) to fix a reporting bug that's already fixed. If you want more cold margin you don't need it — SDM is 12.4%.
- **The real fix = edge-pin grading** to bring F_ΔH/F_q down (see Task 1). The hot pins are the periphery pins of the outer-ring assemblies, over-moderated against the 20 cm water reflector. That is a *local* fix, not a core redesign.

---

## 1. Speed (your 4-day run)

| Knob | Was | Now / recommended | Effect |
|---|---|---|---|
| Depletion integrator | `CECMIntegrator` (2 solves/step) | **`PredictorIntegrator`** ✅ done | ~2× faster |
| Stat profile in `calc_depletion()` | `STAT_MEDIUM` | use **`STAT`** (fast) for design iterations; only switch to `STAT_MEDIUM`/`STAT_FINAL` for the final publication run | ~2–4× faster |
| Timestep horizon | `[10,20,30,40]+[45]*16+[125]*9` (~1945 EFPD, 29 steps) | for iteration, stop near cycle EOC: `[10,20,30,40]+[45]*16+[125]*2` (~1450 EFPD) | fewer steps |

With Predictor + `STAT` + trimmed horizon you should be back to **well under a day**. Keep `STAT_MEDIUM` + full horizon **only** for the one final run you quote in the FER.

---

## 2. Every FER neutronics / OpenMC parameter — how to set it up, what value to expect

> Legend: **[have]** = already in rev6 and passing · **[fix]** = needs work · **[add]** = not yet in the model

| # | Parameter | OpenMC setup | Expected / target value | Status |
|---|---|---|---|---|
| 1 | **k_eff — cold clean ARO** | eigenvalue mode, all temps 293.6 K, no rods, no Xe | ~1.08–1.10 (≈7000–8000 pcm cold excess, ATOM-like) | [add] run case |
| 2 | **k_eff — HZP ARO** | isothermal ~559 K, no Xe | ~1.05 | [add] |
| 3 | **k_eff — HFP ARO** | fuel 900 K / mod ~583 K / 0.71 g/cc, equilibrium Xe | **1.0264** (2516 pcm excess) | [have] |
| 4 | **k_eff — controlled critical** | insert control bank to k=1.000 | **1.00000 ± 50 pcm**, report critical bank position | [fix] add bank search (Finding 4) |
| 5 | **Enrichment & zoning** | 3 radial zones inside FA: 4.95/4.70/4.40 wt% U-235 | avg 4.69, max 4.95 ≤5.0; report zone radii | [have] |
| 6 | **Fuel assembly** | 17×17, 264 fuel pins, 24 guide + 1 instrument tube, pin pitch 1.2623 cm, active H = 200 cm | give full dimension table + lattice plot | [have] geometry; [add] table/figure |
| 7 | **Core loading map** | 21 FA, ring 0 (1) + ring 1 (8) + ring 2 (12); 20 cm water reflector | colour map: enrichment zones, Gd assemblies, CR positions, reflector | [add] figure |
| 8 | **Burnable absorber Gd** | Gd₂O₃ 8 wt% admixed, radial zoning 48/40/26 pins (centre/inner/edge) | BOC hold-down; Gd-157 ~burnt by ~10 GWd/t | [have] |
| 9 | **Burnable absorber Er** | Er₂O₃ 0.5 wt% × 32 rods | slow burner; residual at 41 GWd/t reported at cycle EOC (not horizon end) | [have] |
| 10 | **Control rod material & worth** | Ag-In-Cd (or B₄C) rod universes in guide tubes; ρ = (1/k_in − 1/k_out)·1e5 | total ARI worth **15 226 pcm**; per-bank worths; ARI k=0.888 | [have]; [add] per-bank table |
| 11 | **Reflector** | 20 cm light-water radial + axial water | report albedo effect; note edge-pin peaking driver | [have] |
| 12 | **Cladding** | Zircaloy-4, OD/ID per spec, ~583 K | dimension + composition table | [have] |
| 13 | **Coolant/moderator** | light water, S(α,β) `c_H_in_H2O`, ρ(T,P) at 12.8 MPa | ~0.71 g/cc HFP; confirm S(α,β) attached to every water cell | [have] — verify S(α,β) |
| 14 | **Doppler / FTC** | branch: fuel temp 900→1200 K, Δρ/ΔT | **−1.84 pcm/K** (ATOM −2.34, in family) | [have] |
| 15 | **MTC** | branch: moderator temp ±, Δρ/ΔT | **−35.9 pcm/K** (< 0 all cycle) | [have] |
| 16 | **Void coefficient** | branch: coolant density −%, Δρ | **−214 pcm/%** (negative) | [have] |
| 17 | **Boron coefficient** | N/A (SBF) — instead report **EBIS boron worth curve** (ρ vs ppm) for the diverse shutdown credit | monotonic negative; size to back up shutdown | [add] (ties to EBIS) |
| 18 | **Power coefficient** | combine FTC+MTC+void at power steps | negative across cycle | [have] (derivable) |
| 19 | **Shutdown margin (SDM)** | cold, N-1 most-reactive stuck rod, ARI-minus-one | **12.38 %Δk/k** (≥1.3% gate) | [have] |
| 20 | **F_ΔH (radial pin)** | per-pin fission-density tally, col max/mean | ≤1.65 — **currently 1.845** | [fix] Task 1 |
| 21 | **F_q (3-D pin)** | per-pin 3-D node max/mean | ≤2.32 — **currently 3.583** | [fix] Task 1 |
| 22 | **F_xy / F_z** | radial / axial components | F_xy ~1.24 ✅; F_z ~1.0–1.3 | [have] |
| 23 | **Flux maps** | mesh tally, 2 or 8 groups, normalize to 125 MWth | thermal/fast/total radial + axial maps | [add] figures |
| 24 | **Burnup distribution** | per-FA depletion material burnup at EOC | assembly burnup map; peak ≤62 GWd/t | [add] EOC map |
| 25 | **Depletion / cycle** | Predictor integrator, schedule in §1 | cycle 15.2 mo, discharge 41.3 GWd/t | [have] |
| 26 | **BOC→equilibrium** | simplified batch overlay: fresh / 1× / 2× / 3×-burned assemblies | equilibrium k, power map, discharge BU — replaces fresh-core LRM | [fix] Task 2 (Finding 5) |
| 27 | **Uncertainty** | report k σ, tally rel-err, inactive/active batches, particles/batch | k σ < 50 pcm; tally rel-err < 5% local | [add] table |
| 28 | **Benchmarking** | pin-cell + assembly vs published; core vs ATOM/NuScale/CAREM | document Δ; cite ENDF/B-VIII.0 (IAEA/OECD-grade) | [fix] Task 6 |
| 29 | **Safety states** | cold shutdown · cooldown · uncontrolled rod withdrawal · boron-dilution (EBIS) · max-reactivity state | each k_eff + margin to criticality | [add] Task 4 |

---

## 3. Required figures & tables (FER neutronics section)

1. Full-core loading map (enrichment zones, Gd assemblies, CR locations, reflector) — **[add]**
2. Fuel-assembly diagram (fuel rods, guide tubes, instrument tube, BA rods) — **[have CAD; add OpenMC lattice plot]**
3. OpenMC geometry plots: radial slice, axial slice, assembly lattice — **[add]**
4. k_eff vs burnup, BOC→EOC — **[have from depletion]**
5. Reactivity-balance table (excess, BA worth, CR worth, SDM) — **[assemble]**
6. Feedback-coefficient table (Doppler, MTC, void, [EBIS boron], power) — **[have]**
7. Radial power map at BOC/MOC/EOC — **[add MOC/EOC]**
8. Axial power shape at BOC/MOC/EOC — **[add]**
9. Assembly burnup map at EOC — **[add]**
10. Flux maps (thermal/fast/total) — **[add]**
11. Uncertainty table (k σ, rel-err, batches, particles) — **[add]**
12. Benchmark table (OpenMC vs ATOM / NuScale / CAREM) — **[assemble]**

---

## 4. To-do list — divided, prioritised for the final days

**Priority order = fix the only failing gate first, then fill the BOC→equilibrium gap, then figures/benchmarks/writing.**

### Task 1 — Peaking fix (edge-pin grading) — **BLOCKING, do first**
- Owner: **Samira runs**, Claude drafts the code patch.
- Lower enrichment (or add a Gd skin) on the *outer pin row* of ring-2 (edge) assemblies facing the reflector; this de-peaks the hot pins driving F_ΔH 1.845 / F_q 3.583.
- Target: F_ΔH ≤ 1.65, F_q ≤ 2.32. Expect to trade a little burnup (~1 GWd/t).
- Verify with the rev6 per-pin tally; one fast `STAT` depletion to confirm.

### Task 2 — BOC-to-equilibrium (Finding 5) — **required by FER, currently only fresh-core LRM**
- Owner: **Claude drafts** simplified batch-overlay (fresh/1×/2×/3×-burned mixed loading), **Samira runs**.
- Deliver equilibrium k, equilibrium radial power map, equilibrium discharge burnup. Cite that this replaces the screening LRM.

### Task 3 — Controlled-critical + critical-config peaking (Finding 4)
- Owner: Samira (Claude adds partial-insertion geometry + bank-search helper).
- Report critical bank position at HFP and re-evaluate F_q/F_ΔH at that config (not just ARO).

### Task 4 — Safety-state cases
- Owner: Samira. Run: cold shutdown, cooldown, uncontrolled rod withdrawal, max-reactivity state, EBIS boron worth curve. One table of k_eff + margin.

### Task 5 — Figures
- Owner: Samira (OpenMC `plot_geometry` + mesh tallies). Loading map, lattice plot, radial/axial slices, flux maps, BOC/MOC/EOC power maps, EOC burnup map.

### Task 6 — Benchmarking + uncertainty
- Owner: **Claude assembles** the benchmark table (ATOM, NuScale FSAR, CAREM-25, RITM-200 — numbers already pulled into §8.2) and the uncertainty table; Samira supplies the run statistics (batches/particles/σ).

### Task 7 — Digital appendix (reproducibility)
- Owner: **Claude assembles**. One sample OpenMC input (materials+geometry+settings), assumptions/conditions list, ENDF/B-VIII.0 provenance, repeatability note (fixed seed / σ), how-to-rerun (WSL python path + `cross_sections.xml`).

### Task 8 — FER §8.2/§8.3 neutronics write-up
- Owner: **Claude drafts**, Samira reviews. Fold all tables/figures above into the section; update the stale notebook markdown header (still says old 2.6/3.0/3.4 + Gd 6 — cosmetic but must match the real 4.95/4.70/4.40 + Gd 8 for appendix credibility).

---

## 5. Benchmark / "copy a working design" strategy

We are **already anchored** to the right peers — use them, don't restart:

- **Korean ATOM** (Nguyen et al., *Sci. Rep.* 11:12891, 2021) — closest SBF peer: 4.95 w/o, integral Gd-type BA, **no soluble boron**, swing <1000 pcm, MTC −41 / FTC −2.34 pcm/K, radial peak ~1.5, (N-1) stuck-rod cold shutdown. **Our coefficients sit inside its band.** Primary benchmark row.
- **CAREM-25** — SBF integral PWR, ~24 GWd/t. We beat it on burnup; good "SBF is licensable" precedent.
- **NuScale FSAR Ch.4.3** — boron-shimmed iPWR; use for cross-checking coefficient *form* and CR worth (14.4–15.6 kpcm vs our 15.2), not for the SBF claim.
- **RITM-200** — 60-yr-life iPWR reference for long-life framing.

The benchmarking requirement is met by: (a) pin-cell/assembly k vs published values, (b) core coefficients vs ATOM, (c) ENDF/B-VIII.0 evaluated nuclear data (IAEA/OECD-grade). That satisfies "evidence that reliable IAEA/OECD-type data or benchmarks were used."
