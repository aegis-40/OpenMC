# Decay heat & activity — interpretation for FER §8.11 (and §8.5/§8.6)

Hand-authored interpretation of the two generated artifacts (which are
overwritten on each script run, so the prose lives here):
- `decay_heat_rigorous.{md,csv}` — chain-coupled (full ~3820-nuclide chain,
  in-growth) from `scripts/run_decay_heat.py`.
- `discharge_source_term.{md,csv}` + `discharge_inventory.csv` — curated
  20-nuclide quick-look from `scripts/extract_discharge_inventory.py`.

Basis: rev_3 discharge inventory, whole 21-FA core, **5.04 tHM at discharge**
(≈5.3 tHM fresh), 42.8 GWd/t, OpenMC 0.15.3 + ENDF/B-VIII.0 PWR chain.

## Headline numbers (rigorous)

| Cooling | Decay heat (whole core) | per tHM | per FA (÷21) |
|---|---|---|---|
| 0 (shutdown) | **7.75 MW** | 1.54 MW/tHM | 369 kW |
| 1 yr | 50.9 kW | 10.1 kW/tHM | 2.42 kW |
| 5 yr | 12.1 kW | 2.40 kW/tHM | 577 W |
| 10 yr | 8.32 kW | 1.65 kW/tHM | 396 W |
| 50 yr | 3.93 kW | 0.78 kW/tHM | 187 W |
| 100 yr | 2.09 kW | 0.41 kW/tHM | 99 W |

Total activity: **2.78e19 Bq (27.8 EBq) at shutdown** → 4.5e17 Bq at 1 yr →
1.0e17 Bq at 10 yr.

## Two distinct engineering uses
1. **Post-shutdown decay-heat removal (§8.5/§8.6 RHR / passive cooling sizing):**
   the whole-core **7.75 MW at shutdown = 6.2% of 125 MWth** is the source term
   the residual-heat-removal and passive-cooling cases must reject. This matches
   the ANS-5.1 ~6.5% rule of thumb → cross-validates the depletion. **Hand this
   number to [TH]/[3S/IC].**
2. **Spent-fuel storage / cask thermal (§8.11):** intensive numbers (per tHM /
   per FA) transfer to any loading. One **discharged batch** (4-batch scheme,
   ≈5.25 FA ≈ 1.26 tHM) dissipates ≈ **3.0 kW at 5 yr**, ≈ 2.1 kW at 10 yr —
   the basis for cask/pool spacing and the storage-criticality model that follows.

> **Batch caveat:** the depletion modelled one fresh core irradiated continuously
> to EOC, so the absolute whole-core figures (7.75 MW etc.) are *one core at
> shutdown*, not one reload batch. For per-discharge-batch waste arisings, scale
> by the discharged HM (~1.26 t/cycle), as in `fuel_cycle.compute_arisings`.

## Rigorous vs curated — the V&V story (for the Digital Appendix)

| Cooling | rigorous / curated (heat) | dominant physics |
|---|---|---|
| 0 | 425× | short-lived FPs (the curated set omits them) |
| 1 yr | 3.3× | Cm-242, Ce-144/Pr-144, Ru-106, Pm-147 still hot |
| 5 yr | 1.30× | Sr-90 + Cs-137 take over (both tracked) |
| 10–30 yr | 1.2–1.3× | **closest agreement** — Sr/Cs regime |
| 100–300 yr | 1.8–3.2× | **Pu-241→Am-241 in-growth** (curated does independent decay, structurally can't grow Am-241) |
| 10 kyr | 1.04× | long-lived actinides only (both tracked) |

This is exactly the expected behaviour and makes a clean validation narrative:
**the transparent 20-nuclide model agrees with the full chain solver precisely in
the regimes where its two documented assumptions hold (dominant nuclides in the
curated set; in-growth negligible), and diverges precisely where they don't
(<5 yr short-lived FPs; ~100 yr Am-241 in-growth).** Use the **rigorous column**
for all §8.11 quantitative claims; cite the curated model as the independent
cross-check.

## Top activity contributors at discharge (curated inventory)
Cs-134, Pu-241, Cs-137, Sr-90 lead, then Eu-154, Pu-238, Cm-244 — a textbook PWR
spent-fuel signature. Full list: `discharge_inventory.csv`.

## Waste classification
Bulk spent fuel screens to **HLW** (heat density ~3e4 W/m³ ≫ 2 kW/m³ threshold) —
expected; drives the geological-disposal route in the §8.11 narrative.
