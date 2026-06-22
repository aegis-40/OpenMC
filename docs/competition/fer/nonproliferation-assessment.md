# Non-proliferation assessment (3S)

> **Placement:** slots into §7 (broader impacts — Safety/Security/Safeguards) and is
> cross-referenced from §8.11 (back-end). Owner: [3S], data from NEU.
> Data: `docs/competition/safeguards/safeguards_attractiveness.md` +
> `docs/competition/waste/discharge_inventory.csv` (whole-core discharge, 42.8 GWd/tHM,
> OpenMC depletion). Method follows the NNL proliferation-resistance scoring as applied by
> Ashley et al. (2014, *Ann. Nucl. Energy* 69, 314), itself built on the Generation-IV
> PR&PP framework (GIF 2006) and the IAEA significant-quantity definitions.

A proliferation-resistance assessment is a **qualitative judgement of quantitative data**
(Ashley et al. 2014). We adopt the NNL resistance score

```
U(x) = − log [ V(x) · A(x) ]            (higher U  →  more proliferation-resistant)
```

where the **value function** V(x) is the significant quantities (SQ) of special nuclear
material discharged per unit energy, and the **access function** A(x) discounts that value
by the accessibility barriers an adversary must overcome. The two are developed below for
the Aegis-40 once-through discharge.

## 1. Value function — significant quantities discharged

The discharged plutonium vector (whole 21-FA core, 42.8 GWd/tHM) and its SQ accounting
(1 SQ Pu = 8 kg, IAEA):

| Isotope | grams | wt % of Pu |
|---|---:|---:|
| Pu-238 | 1 507 | 2.72 |
| Pu-239 | 28 935 | 52.29 |
| Pu-240 | 13 623 | 24.62 |
| Pu-241 | 7 697 | 13.91 |
| Pu-242 | 3 571 | 6.45 |
| **Total Pu** | **55 334 (55.3 kg)** | 100.00 |

- **Whole-core Pu = 55.3 kg = 6.9 SQ**; per reload batch (¼ core) = 13.8 kg = **1.7 SQ**.
- Normalised to energy: **≈ 37 SQ-Pu / GWy(e)** (11.7 SQ / GWy-th) — the same order as a
  conventional LWR once-through discharge (~25–31 SQ/GWy(e)). The value function is therefore
  **not** anomalously low; the resistance of this design lives in the access function, not
  in a small SNM inventory.
- Spent uranium is **non-attractive**: U-235 at discharge is **1.10 wt %**, far below the
  20 % LEU/HEU line — the recovered uranium is not a usable enrichment.
- Minor actinides (Np-237 3.34 kg, Am-241 0.37 kg, Am-243 0.71 kg) are materials of
  safeguards interest but require reprocessing to separate — see access function.

## 2. Access function — accessibility barriers

The access function multiplies five PR&PP barrier terms (GIF 2006), each scored on a
Likert scale (higher score = stronger barrier; lower A = higher resistance):

| Barrier | Aegis-40 condition | Assessment |
|---|---|---|
| **Material type (MT)** | Pu-240 = 24.6 wt %, fissile (Pu-239+241) = **66.2 %** → **reactor-grade** Pu (weapons-grade is ≥ 93 % fissile, < 7 % Pu-240). High burnup *degrades* the vector relative to a 33 GWd/t LWR. | Modest intrinsic barrier — reactor-grade Pu remains weapons-usable in principle, so MT alone is **not** decisive. |
| **Detectability (TD)** | Pu locked inside **intact, intensely radioactive spent-fuel assemblies**; whole-assembly dose ≫ the 1 Gy/h self-protecting threshold. | Strong — diversion of an assembly is readily detectable. |
| **Process / concealment cost (PC)** | Recovery requires **reprocessing**; the plant has **no reprocessing and no separated-fissile stream** (once-through). | Strong — there is nothing to divert without building a reprocessing capability. |
| **Proliferation time (PT)** | Self-protecting decay heat **19.5 W/kg-Pu** (≫ ~2 W/kg) and a high spontaneous-fission neutron background (4.3 × 10⁵ n/s/kg-Pu bare; 5.4 × 10⁷ n/s/kg incl. Cm-244) degrade any device and lengthen handling. | Strong intrinsic barrier (the Bathke-FOM "self-protection" terms). |
| **Detection probability (DP)** | Whole core under **IAEA safeguards**, item-counted intact assemblies, continuity-of-knowledge maintained in wet/dry storage (§8.11). | Strong — extrinsic, institutional. |

The **Bathke figure-of-merit (FOM)** inputs are exactly the PT/MT terms above: the
combination of reactor-grade isotopics, 19.5 W/kg-Pu decay heat and the Cm-244-dominated
neutron field place the discharged material in the **low-attractiveness** band of the
Bathke attractiveness scale (the material is "unattractive/protected", not "attractive").

## 3. Resistance score and honest framing

Combining the two functions, the Aegis-40 discharge scores **high U(x)** — proliferation-
resistant — but the assessment must be honest about *why*:

- **Intrinsic barriers (raised by high burnup, SBF long cycle):** reactor-grade, degraded
  Pu vector (Pu-239 52 %, Pu-240 25 %, fissile 66 %); 19 W/kg-Pu decay heat; high SF-neutron
  background; spent U at 1.10 % U-235. These are *real but modest* — reactor-grade Pu is not
  a usable enrichment barrier the way LEU is.
- **Extrinsic barriers (decisive):** the value is gated almost entirely by the access
  function — Pu is immobilised in **self-protecting intact assemblies**, in a **once-through
  cycle with no reprocessing and no separated-Pu stream**, under **IAEA safeguards**. There
  is no diversion pathway that does not require a state-level reprocessing capability and
  defeat of item accountancy.

**Net:** the design adds proliferation resistance the cheapest possible way — by *not
creating* an attractive material stream. High burnup + soluble-boron-free long cycle +
once-through compound the standard spent-fuel resistance; the plant introduces no
reprocessing, no separated fissile material, and no fresh-fuel HEU. The honest headline for
the FER is: **resistance here is dominated by the extrinsic/institutional barriers (no
reprocessing, safeguards, self-protecting assemblies), with the intrinsic isotopic barriers
a real but secondary contributor.**

## References

- S.F. Ashley et al., *Ann. Nucl. Energy* **69** (2014) 314–330 — NNL value×access scoring.
- Generation IV International Forum, *Evaluation Methodology for PR&PP*, Rev. 5 (2006).
- C.G. Bathke et al., "The Attractiveness of Materials in Advanced Nuclear Fuel Cycles,"
  *Nucl. Technol.* **179** (2012) 5–30 — attractiveness FOM.
- IAEA, *Safeguards Glossary*, 2001 Ed. — significant quantities.
