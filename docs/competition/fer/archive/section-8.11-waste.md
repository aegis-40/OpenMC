# FER §8.11 Nuclear Waste Management — Aegis-40 iPWR

> **Drafting status (2026-06-08).** FER-ready draft for Samira's §8.11. All numbers are generated
> outputs of the validated `aegis40.back_end` module (15/15 tests) on the LOCKED rev_3 design basis
> (`design-basis-locked.md`), OpenMC 0.15.3 + ENDF/B-VIII.0 depletion. Source artefacts:
> `waste/{waste_intensity, discharge_source_term, storage-criticality-interpretation}.md`.

---

## 8.11 Nuclear Waste Management

Aegis-40 addresses nuclear waste on three fronts mandated by the Technical Specification §4.3.2:
**(i)** an innovative fuel-cycle design that minimises the quantity and radioactivity of spent fuel
per unit energy; **(ii)** a back-end management plan with the three required safety analyses (source
term, decay heat, storage criticality); and **(iii)** minimisation of secondary radioactive waste.

### 8.11.1 Waste-minimisation by design (fuel-cycle)

The dominant waste lever is **discharge burnup**: extracting more energy per tonne of heavy metal
before discharge directly reduces the spent-fuel arisings per unit electricity. The Aegis-40
high-burnup soluble-boron-free (SBF) core discharges at **42.8 GWd/tHM** at **32.0 % net efficiency**,
versus ~24 GWd/tHM at ~27 % for the CAREM-25 reference. The once-through waste-intensity identity
(tHM/TWhe = 10⁶ / [BU·24·η]) depends only on burnup and efficiency, giving the comparison in
Table 8.11-1.

**Table 8.11-1 — Spent-fuel arisings and waste intensity vs CAREM-25**

| Quantity | Aegis-40 (rev_3) | CAREM-25 (reference) |
|---|---|---|
| Thermal / electric power | 125 MWth / 40 MWe | 100 MWth / 27 MWe |
| Net thermal efficiency | 0.320 | 0.270 |
| Discharge burnup | 42.8 GWd/tHM | 24.0 GWd/tHM |
| HM discharged per year | 0.91 tHM/yr | — |
| Assemblies discharged per year | 3.6 FA/yr | — |
| **Waste intensity** | **3.04 tHM/TWhe** | **6.43 tHM/TWhe** |

**Aegis-40 produces ~2.1× less heavy metal per unit electricity than CAREM-25 (~53 % reduction)** —
the combined effect of ~1.8× higher burnup and higher thermal efficiency. Absolute arisings are tiny:
**< 1 tHM/yr and < 4 assemblies/yr**. Dropping to a CAREM-like ~3.1 wt% / ~24 GWd/t point would roughly
double the arisings, which is the quantitative reason the high-burnup design is kept.

### 8.11.2 Back-end fuel-cycle management plan

Aegis-40 uses a **once-through** fuel cycle. Discharged assemblies (~3.6 FA/yr) are cooled in the
spent-fuel pool, then transferred to **on-site dry-cask interim storage** after the decay-heat and
dose criteria are met (§8.11.3). The very low arisings rate makes a single compact pool plus a small
cask pad sufficient for the plant lifetime, deferring any repository transfer. No reprocessing is
assumed; the discharged plutonium vector and safeguards attractiveness are addressed in the §5
proliferation-resistance assessment.

### 8.11.3 Spent-fuel source term and decay heat (§4.3.2 analysis)

The discharge source term and its decay are computed from the rev_3 depletion inventory
(5.04 tHM at discharge). At discharge the spent fuel is **heat-generating high-level waste (HLW)**
(heat density ≫ 2000 W/m³). The activity, decay heat, and ingestion radiotoxicity decline by ~2
orders of magnitude over the first 100 years (Table 8.11-2, Figure 8.11-1) — the basis for pool→cask
transfer timing and cask thermal sizing.

**Table 8.11-2 — Discharge source term vs cooling time**

| Cooling (yr) | Activity (Bq) | Decay heat (W) | Radiotoxicity (Sv) |
|---|---|---|---|
| 0 | 1.20 × 10¹⁷ | 18,220 | 2.18 × 10⁹ |
| 1 | 1.06 × 10¹⁷ | 15,240 | 1.93 × 10⁹ |
| 5 | 7.59 × 10¹⁶ | 9,333 | 1.41 × 10⁹ |
| 10 | 5.98 × 10¹⁶ | 7,003 | 1.16 × 10⁹ |
| 30 | 3.20 × 10¹⁶ | 4,247 | 7.44 × 10⁸ |
| 100 | 5.51 × 10¹⁵ | 1,188 | 2.43 × 10⁸ |
| 1000 | 1.87 × 10¹⁴ | 155 | 4.50 × 10⁷ |

At discharge: total activity **1.20 × 10¹⁷ Bq**, decay heat **18.2 kW** (3,615 W/tHM). The dominant
early-time nuclides are Cs-134, Pu-241, Cs-137, and Sr-90; the long-term radiotoxicity is set by the
transuranics (Pu, Am). The decay-heat curve is the input to the pool cooling-load and the dry-cask
passive-cooling design.

‹INSERT FIGURE 8.11-1 — decay heat and ingestion radiotoxicity vs cooling time (log–log).
Generated: `waste/decay_heat_vs_cooling.png`.›

### 8.11.4 Spent-fuel storage criticality safety (§4.3.2 analysis)

Storage criticality is evaluated under the SBF philosophy — **cold (20 °C), unborated water, no
soluble-boron credit** — so the result holds even on total loss of any boron source. The acceptance
criterion is the regulatory **k_eff(95/95) ≤ 0.95** (NUREG-0800 / 10 CFR 50.68). The design-basis
configuration is burnup-credited (discharged) fuel in a Region-II absorber rack (17×17 cell, 23.5 cm
pitch), modelled as a bounding infinite reflective array.

**Table 8.11-3 — Storage-rack criticality (burnup-credited spent fuel, infinite array)**

| Configuration | k_calc ± σ | k(95/95) | Verdict |
|---|---|---|---|
| Spent fuel + Boral box (0.40 B₄C) | 0.78099 ± 0.00054 | **0.782** | ✅ PASS |
| Spent fuel + Metamic box (0.31 B₄C) | 0.78856 ± 0.00061 | **0.790** | ✅ PASS |

Both credited designs sit **~0.16 below the 0.95 limit**, confirmed by two independent absorber
materials. The reactivity ladder shows why: fresh bare touching fuel (1.50) → **burnup credit**
(1.075, −0.425) → **absorber panels + pitch** (0.782, −0.293). Burnup credit removes most of the
excess for free; the panels carry it well under the limit. Because the high-density rack relies on
burnup credit, fresh/low-burnup assemblies are administratively excluded by a minimum-burnup loading
curve and held in a separate Region-I (flux-trap) rack — the standard two-region pool layout. The
result is consistent with, and more conservative than, the published SBF small-PWR storage envelope
(Kim, Jung & Yoon 2024, k ≈ 0.93–0.95 for racks designed up to the limit).

> **V&V note (Digital Appendix).** The reported margins use Δ_bias = Δ_unc = 0 (raw calculated
> margin). A licensing-grade result adds the OpenMC + ENDF/B-VIII.0 bias from the **OECD/NEA Burnup-
> Credit Criticality Benchmark (Phase II)** and **SFCOMPO 2.0** assay validation; even a conservative
> Δ ≈ 0.02–0.05 leaves the 0.78 design comfortably under 0.95.

### 8.11.5 Secondary radioactive waste minimisation

The **soluble-boron-free** design eliminates the borated-water secondary-waste streams that a
boron-controlled PWR generates — spent ion-exchange resins, evaporator concentrates, and tritiated
boron effluent from the chemical-and-volume-control system. This is a "reduce waste quantity" benefit
not captured in the tHM/TWhe metric. Remaining operational wastes (filters, dry active waste, spent
resins from coolant clean-up) are managed by best-available-technique segregation, volume reduction,
and conditioning per IAEA GSR Part 5; the integral-vessel layout with no large primary penetrations
further limits contaminated-component arisings.

---

## References for §8.11

- [W-1] OpenMC 0.15.3 (Romano et al., *Ann. Nucl. Energy* 82 (2015) 90) + ENDF/B-VIII.0 (Brown et al.,
  *Nucl. Data Sheets* 148 (2018) 1) — depletion / inventory and storage-criticality transport.
- [W-2] CAREM-25 parameters: INVAP/CNEA, IAEA ARIS / IAEA SMR Book — waste-intensity reference point.
- [W-3] US NRC, NUREG-0800 §9.1.1 and 10 CFR 50.68 — spent-fuel storage criticality (k_eff(95/95) ≤ 0.95).
- [W-4] OECD/NEA, *Burnup Credit Criticality Benchmark* (Phase II) and **SFCOMPO 2.0** — burnup-credit
  V&V basis (Digital Appendix).
- [W-5] IAEA GSR Part 5, *Predisposal Management of Radioactive Waste* — secondary-waste management.
- [W-6] Kim, Jung & Yoon, *Nucl. Eng. Tech.* 56 (2024) 3144 — SBF small-PWR storage subcriticality
  envelope (cross-check).
