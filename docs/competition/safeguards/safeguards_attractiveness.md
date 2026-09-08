# Safeguards & non-proliferation — attractiveness of discharge materials (FER 3S, §8.5/§8.7)

- Generated: `2026-07-04T05:05:36.628388+00:00`
- Source inventory: `docs/competition/waste/discharge_inventory.csv` (whole-core discharge, 29.6 GWd/t, OpenMC depletion). Produced by [NEU]; framing by [3S].
- Basis: whole 37-FA core (9.39 tHM) at discharge; **once-through single batch** — the whole core is discharged once, so per-batch = whole-core.

## 1. Plutonium vector and grade

| Isotope | grams | wt % of Pu |
|---|---|---|
| Pu238 | 1,105 | 1.45 |
| Pu239 | 47,862 | 62.79 |
| Pu240 | 16,128 | 21.16 |
| Pu241 | 8,661 | 11.36 |
| Pu242 | 2,465 | 3.23 |
| **Total Pu** | **76,221 g (76.2 kg)** | 100.00 |

- **Grade: REACTOR-GRADE** (Pu-240 = 21.2 wt%; weapons-grade is <7%, reactor-grade is >19%).
- Fissile fraction (Pu-239+Pu-241): **74.2%** (weapons-grade Pu-239 alone is >93%).
- Burnup direction, stated honestly: at 29.6 GWd/tHM this core discharges at *lower* burnup than a conventional 3-batch PWR (~45–50 GWd/tHM), so its Pu is correspondingly **less** degraded — Pu-239 62.8% here versus ~50–55% at 3-batch discharge. The material is still firmly reactor-grade (Pu-240 21.2%, three times the <7% weapons-grade line), but the long single-batch cycle does **not** buy extra isotopic degradation; the decisive barriers are extrinsic (§5).

## 2. Intrinsic self-protection barriers

| Barrier | Value | Significance |
|---|---|---|
| Decay heat | **12.2 W/kg-Pu** (930 W total) | ≫ ~2 W/kg 'self-protection' level; heat damages a device |
| SF neutrons (Pu metal) | **3.09e+05 n/s/kg-Pu** | predetonation background (Pu-240/238/242) |
| SF neutrons incl. Cm-244 | 1.37e+07 n/s/kg | Cm-244 dominates the spent-fuel handling field |

## 3. Spent uranium (non-attractive)

- U-235 at discharge: **1.77 wt%** — far below the 20% LEU/HEU line and the ~90% weapons line. The recovered uranium is **not** a usable enrichment.

## 4. Significant-quantity accounting (IAEA, Pu = 8 kg/SQ)

- Whole-core Pu: 76.2 kg = **9.5 SQ**.
- Per discharge batch (1/1 core): 76.2 kg = **9.5 SQ** — but embedded in intensely radioactive intact assemblies.
- Minor actinides (kg): Np237 3.47, Am241 0.58, Am243 0.36, Cm244 0.09 — Np-237/Am are materials of safeguards interest but require reprocessing to separate.

## 5. Proliferation-resistance summary

- **Intrinsic barriers (moderate, and *not* enhanced by the long cycle):** reactor-grade Pu vector (Pu-239 62.8%, Pu-240 21.2%, fissile 74%); 12 W/kg-Pu decay heat and a high spontaneous-fission neutron background; spent U at 1.77% U-235. Because discharge burnup is 29.6 GWd/tHM, isotopic degradation is *less* than a 3-batch PWR achieves — this is a cost of the single-batch cycle, not a benefit.
- **Extrinsic barriers (decisive):** the Pu is locked inside self-protecting, intensely radioactive **intact spent-fuel assemblies** (whole-assembly dose ≫ the 1 Gy/h self-protecting threshold), under IAEA safeguards, in a **once-through** cycle with no reprocessing — there is no separated-Pu stream to divert.
- **Net:** proliferation resistance here is carried by the **extrinsic** barriers — sealed-for-life once-through operation, intact self-protecting assemblies, no reprocessing and no separated-fissile stream anywhere in the cycle. The intrinsic isotopic barrier is ordinary reactor-grade and is modestly *weaker* than a high-burnup multi-batch discharge; we state this rather than claim credit for it.

## Plots

![pu_vector.png](pu_vector.png)
![self_protection.png](self_protection.png)
![snm_inventory.png](snm_inventory.png)

## Method notes & open items

- Decay-heat and SF-neutron constants are standard isotopic values (encoded in the script with sources).
- Burnup-trajectory view (Pu-239 fraction vs burnup) is an optional extension — needs the per-step Pu vector from the core depletion h5 (WSL).
- Cite: Wu et al., *Int. J. Energy Res.* (2020) — proliferation-resistance barriers review; IAEA Safeguards Glossary (significant quantities).
