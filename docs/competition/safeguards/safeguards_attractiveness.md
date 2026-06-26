# Safeguards & non-proliferation — attractiveness of discharge materials (FER 3S, §8.5/§8.7)

- Generated: `2026-06-05T18:04:06.387055+00:00`
- Source inventory: `docs\competition\waste\discharge_inventory.csv` (whole-core discharge, 42.8 GWd/t, OpenMC depletion). Produced by [NEU]; framing by [3S].
- Basis: whole 21-FA core at discharge; per-batch = /4 (4-batch reload).

## 1. Plutonium vector and grade

| Isotope | grams | wt % of Pu |
|---|---|---|
| Pu238 | 1,507 | 2.72 |
| Pu239 | 28,935 | 52.29 |
| Pu240 | 13,623 | 24.62 |
| Pu241 | 7,697 | 13.91 |
| Pu242 | 3,571 | 6.45 |
| **Total Pu** | **55,334 g (55.3 kg)** | 100.00 |

- **Grade: REACTOR-GRADE** (Pu-240 = 24.6 wt%; weapons-grade is <7%, reactor-grade is >19%).
- Fissile fraction (Pu-239+Pu-241): **66.2%** (weapons-grade Pu-239 alone is >93%).
- High burnup pushes Pu-239 down to 52% and Pu-240/Pu-241/Pu-238 up — *more* degraded than a typical 33 GWd/t LWR discharge.

## 2. Intrinsic self-protection barriers

| Barrier | Value | Significance |
|---|---|---|
| Decay heat | **19.5 W/kg-Pu** (1076 W total) | ≫ ~2 W/kg 'self-protection' level; heat damages a device |
| SF neutrons (Pu metal) | **4.33e+05 n/s/kg-Pu** | predetonation background (Pu-240/238/242) |
| SF neutrons incl. Cm-244 | 5.40e+07 n/s/kg | Cm-244 dominates the spent-fuel handling field |

## 3. Spent uranium (non-attractive)

- U-235 at discharge: **1.10 wt%** — far below the 20% LEU/HEU line and the ~90% weapons line. The recovered uranium is **not** a usable enrichment.

## 4. Significant-quantity accounting (IAEA, Pu = 8 kg/SQ)

- Whole-core Pu: 55.3 kg = **6.9 SQ**.
- Per discharge batch (1/4 core): 13.8 kg = **1.7 SQ** — but embedded in intensely radioactive intact assemblies.
- Minor actinides (kg): Np237 3.34, Am241 0.37, Am243 0.71, Cm244 0.27 — Np-237/Am are materials of safeguards interest but require reprocessing to separate.

## 5. Proliferation-resistance summary

- **Intrinsic barriers (raised by high burnup):** reactor-grade, degraded Pu vector (Pu-239 52%, Pu-240 25%, fissile 66%); 19 W/kg-Pu decay heat and a high spontaneous-fission neutron background; spent U at 1.10% U-235.
- **Extrinsic barriers (decisive):** the Pu is locked inside self-protecting, intensely radioactive **intact spent-fuel assemblies** (whole-assembly dose ≫ the 1 Gy/h self-protecting threshold), under IAEA safeguards, in a **once-through** cycle with no reprocessing — there is no separated-Pu stream to divert.
- **Net:** high burnup + SBF + once-through compound the standard spent-fuel proliferation resistance; the design introduces no reprocessing or separated-fissile streams.

## Plots

![pu_vector.png](pu_vector.png)
![self_protection.png](self_protection.png)
![snm_inventory.png](snm_inventory.png)

## Method notes & open items

- Decay-heat and SF-neutron constants are standard isotopic values (encoded in the script with sources).
- Burnup-trajectory view (Pu-239 fraction vs burnup) is an optional extension — needs the per-step Pu vector from the core depletion h5 (WSL).
- Cite: Wu et al., *Int. J. Energy Res.* (2020) — proliferation-resistance barriers review; IAEA Safeguards Glossary (significant quantities).
