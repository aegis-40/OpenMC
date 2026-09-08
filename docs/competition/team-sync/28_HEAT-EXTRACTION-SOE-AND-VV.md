# Heat extraction, the electrolyser, and how the neutronics was validated

Three things a jury may push on, explained from zero. No background assumed.

---
---

# PART 1 — How heat is taken out of the turbine

## 1.1 The turbine has three sections

Your turbine is **one machine** — tandem-compound, three sections on a single shaft driving one
generator. Steam passes through them in series, losing pressure and giving up work at each:

| Section | Pressure in → out | Work |
|---|---|---|
| HP | 4.5 MPa → **1.0 MPa** | 14.74 MW |
| IP | **1.0 MPa** → 0.15 MPa | 13.36 MW |
| LP | 0.15 MPa → ~0.007 MPa | 14.69 MW |

**Between the HP and IP sections there is a pipe** — the *crossover*. That is where cogeneration steam
is taken: **1.0 MPa, about 180 °C**.

## 1.2 Why that exact point — the question to expect

**Too early** (main steam, 4.5 MPa / 296 °C): you would be taking steam that still has all three
sections of work left in it. Enormously wasteful.

**Too late** (LP exhaust, 0.15 MPa / 111 °C): electrically free — but **useless**. Regenerating the
zeolite store needs **130–180 °C**. At 111 °C you cannot dry the bed at all.

> **1.0 MPa is the coldest steam in the expansion that is still hot enough to be useful. Every bar
> above that is electricity given away for nothing.**

Taking it at the crossover also means tapping a **pipe between casings**, not a bleed from inside a
blade path — so nothing is disturbed aerodynamically.

## 1.3 What it costs

Steam taken at the crossover has done its HP work but will never do its IP or LP work. That is
**about 4.9 MWe** while charging — export falls from 40 MWe to roughly **35**.

> **You are not using waste heat. You are buying heat with electricity.**

It pays because heat sells at $50/MWh-th against a $26 production cost.

## 1.4 Does extraction make the steam wetter? No.

Common misconception, worth having straight. **Removing mass does not change the state of the steam
that continues.** Quality at any downstream pressure is set by the expansion line — enthalpy and
entropy — not by how many kilograms are flowing. The IP and LP sections start from exactly the same
conditions with or without extraction.

Your moisture (IP exhaust 0.872, LP exhaust 0.892) is inherent to a **saturated-steam cycle** with only
39 K of superheat — not caused by cogeneration. It is handled by the **moisture separator at 0.15 MPa**,
hardened blade leading edges and interstage drainage, exactly as every PWR secondary does.

## 1.5 Two different customers, two different takeoffs

**TCES takes heat.** Crossover steam → intermediate heat exchanger → a closed charge loop at ~168 °C
that dries the zeolite bed. The exchanger means the storage medium **never touches steam or feedwater
chemistry**.

**SOE takes steam as feedstock, not as a heat source.** A **DN150 branch of pressure-reduced
deaerator-inlet steam** — low-pressure steam already well down the expansion, the cheapest in the
cycle. Deliberately sized **larger than the hydrogen product line** because it must pass the full
electrolyser demand.

**And the dispatch rule: TCES charging OR SOE operation, never both.** Charging costs ~4.9 MWe and the
electrolyser draws 8 MWe — running both would spend the same headroom twice. A conservatism imposed on
ourselves.

---
---

# PART 2 — How the solid-oxide electrolyser works

## 2.1 Start from zero: what electrolysis is

Water does not split on its own. You must **push energy in** to break H–O bonds:

```
2 H₂O  +  energy  →  2 H₂  +  O₂
```

Put two electrodes in water, apply a voltage, and hydrogen appears at one, oxygen at the other. That is
electrolysis. The question is only **how much energy, and in what form.**

## 2.2 The key idea — energy comes in two forms ⭐

The total energy needed splits into two parts:

```
ΔH     =     ΔG      +     TΔS
 ↑            ↑             ↑
total      must be        can be
energy    ELECTRICITY     HEAT
```

- **ΔG** is the part that *must* be electrical. No way around it.
- **TΔS** can be supplied as **heat** — and heat is far cheaper than electricity.

**And here is the whole trick: as temperature rises, ΔG falls and TΔS grows.**

| | ΔH total | ΔG electrical | TΔS from heat |
|---|---|---|---|
| Liquid water, 25 °C | 286 kJ/mol | **237** (83 %) | 49 |
| Steam, 800 °C | 249 kJ/mol | **183** (73 %) | 66 |

> **Run it hot and a quarter of the energy can come from heat instead of electricity.** On a nuclear
> plant, heat is exactly what you have spare.

In voltage terms, the minimum cell voltage falls from **1.23 V at 25 °C to about 0.95 V at 800 °C**.

## 2.3 The second gain: feed steam, not water

If you fed **liquid** water, the cell would have to boil it using electricity — about 44 kJ/mol wasted
in the most expensive currency available.

**You feed steam.** The latent heat is paid thermally, from the cycle. That is what the DN150 steam
branch is for.

## 2.4 What the cell physically is

Three ceramic layers, like a sandwich:

```
   AIR SIDE  ────────────────  oxygen electrode
   ELECTROLYTE ────────────  dense ceramic — YSZ
   STEAM SIDE ────────────  fuel electrode (nickel-ceramic)
```

The electrolyte is **yttria-stabilised zirconia (YSZ)** — a ceramic with a deliberate defect in its
crystal structure. Those defects let **oxide ions (O²⁻) hop through the solid**, but block electrons.

**That is why it must be hot.** Below about 700 °C the ions barely move and the cell has enormous
internal resistance. The 800 °C is not a preference — the material only works there.

## 2.5 The reactions

**Steam side (cathode):** steam meets electrons and splits.

```
H₂O  +  2e⁻   →   H₂  +  O²⁻
```

Hydrogen gas leaves. The oxide ion is left behind.

**Through the electrolyte:** the O²⁻ ion migrates across the ceramic — pulled by the applied voltage.

**Air side (anode):** oxide ions give up their electrons and pair off.

```
2 O²⁻   →   O₂  +  4e⁻
```

Oxygen gas leaves. The electrons return through the external circuit.

**Net: 2 H₂O → 2 H₂ + O₂.** And note the product streams are **physically separated by the ceramic** —
hydrogen on one side, oxygen on the other. They never mix.

## 2.6 The numbers

| | Electricity per kg H₂ | LHV efficiency |
|---|---|---|
| PEM / alkaline, ~80 °C | ~50 kWh/kg | ~67 % |
| **Solid oxide, ~800 °C** | **~39 kWh/kg** | **~85 %** |

**About 25 % less electricity per kilogram.**

Your module: **8 MWe**, drawing about 2 MWe averaged — 5 % of net electricity — giving **~427 t of
hydrogen a year**. That is roughly **6 hours a night at full power, every night**, with export dropping
40 → 32 MWe during those hours.

**Economically:** 39 kWh/kg at $75/MWh means **$2.93/kg of electricity in** against a **$5/kg** product.
A $2.07/kg margin. You make hydrogen because it is worth more than the electricity — not because the
electricity is spare.

## 2.7 Tritium — why it gets its own barrier

**Tritium is hydrogen.** It substitutes into water and permeates hot metal far more readily than any
other nuclide in the plant. At **800 °C the electrolyser is the most permeable point anywhere.**

So it is treated as its own pathway rather than left to the three-barrier chain: **permeation-barrier
coatings, a getter on the hydrogen product, and continuous monitoring** at the interface.

## 2.8 The honest downsides

If asked why SOE is not universal:

- **Ceramics crack when thermally cycled.** Daily start-stop is hard on the stack; degradation rates
  are the main commercial obstacle.
- **Stack life is shorter** than PEM — replacement is a consumable cost, not a lifetime component.
- **It needs a heat source at 800 °C.** Which is exactly why it belongs on a nuclear plant and not
  beside a wind farm.

---
---

# PART 3 — Verification and validation of the neutronics

## 3.1 The two words mean different things

| | Question it answers |
|---|---|
| **Verification** | *Did we solve the equations right?* Is the model built correctly, converged, free of mistakes? |
| **Validation** | *Did we solve the right equations?* Does the code reproduce **reality** — measured experiments? |

**A code that runs is not a code that is right.** Both legs are needed.

## 3.2 Verification — our own checks

- **Convergence**: 400 batches × 50,000 particles, 80 discarded while the fission source settles →
  ~16 million active histories, eigenvalue uncertainty **22–26 pcm**.
- **Volume checks** on every material region — catches geometry errors.
- **Coefficient-sign checks** before any result transfers downstream: if MTC came out positive, the
  model is wrong, and nothing proceeds.
- **Repeatability**: the depletion benchmark reruns with a different random seed to show the answer is
  not a statistical accident.

## 3.3 Validation leg 1 — ICSBEP measured criticals ⭐ *this is real experimental data*

**What it is.** The **OECD/NEA International Handbook of Evaluated Criticality Safety Benchmark
Experiments** — hundreds of real critical assemblies, physically built and measured, then carefully
evaluated so others can model them.

**What we used.** **LEU-COMP-THERM-008** — low-enriched uranium lattices in water. Chosen deliberately:
low-enriched UO₂ fuel rods in a water-moderated lattice is **the closest published measured geometry to
a PWR core**. Four cases (1, 2, 5, 7), each modelled as published and run in eigenvalue mode.

**The result, and the detail that matters:**

> The benchmark model k_eff is **1.0007 ± 0.0016 — NOT unity.**

Real experiments are not exactly critical, and the evaluators publish the corrected value. So the error
is `C − E = k_calc − 1.0007`, giving:

```
case 1   −23 pcm
case 2   −28 pcm
case 5   − 8 pcm
case 7  −143 pcm
         ────────
mean bias  −50 pcm      every case inside the handbook uncertainty, worst 0.86σ
```

**Why this leg is the strongest one you have:** it is **measured data, not code-to-code**. It is the
"reliable-source IAEA/OECD-NEA data" gate the competition asks for.

**⚠ Know this:** if anyone says "your bias should be zero," the answer is that the benchmark eigenvalue
is 1.0007, not 1.0000, and the bias is computed against the evaluated value. We had this wrong once
internally and corrected it.

## 3.4 Validation leg 2 — depletion against Serpent

**Why a second leg.** ICSBEP validates *criticality at one instant*. It says nothing about whether the
code tracks fuel correctly as it **burns over six years** — which is most of what your design rests on.

**What we used.** The **BEAVRS 2.4 % PWR pincell**, built from OpenMC's internal model so there is no
external geometry file to get wrong — maximally reproducible. We reproduced the published
**Romano (2021)** OpenMC-versus-Serpent validation: identical model, identical burnup schedule,
identical depletion chain.

**Result:** k_eff within **~20 pcm** and actinide and fission-product inventories within **~1 %** of the
published reference, across the whole burnup range.

**Be precise about what this is:** **code-to-code**, against Serpent — a different Monte Carlo code with
an independent development history. It is not measured plant data.

## 3.5 Validation leg 3 — rod worth on an SMR-like core

**Why a third leg.** The first two say nothing about **control-rod worth**, which is the number your
entire shutdown case depends on.

**What we used.** A **NuScale-like SMR core** with a published Serpent reference. Six different rod
configurations, all reproduced within **±80 pcm**.

Chosen because it is the closest published core to yours in size and geometry — a compact integral PWR,
not a large commercial plant.

## 3.6 The three legs, and what each covers

| Leg | Type | Validates | Result |
|---|---|---|---|
| **ICSBEP LCT-008** | **measured experiment** | criticality, LEU-water lattice | −50 pcm mean bias, worst 0.86σ |
| **BEAVRS pincell / Romano 2021** | code-to-code (Serpent) | depletion over burnup | ~20 pcm, ~1 % on nuclides |
| **NuScale-like core** | code-to-code (Serpent) | control-rod worth | ±80 pcm across 6 rod states |

**Together they cover the three things the design actually needs: is it critical where we say, does it
burn the way we say, and are the rods as strong as we say.**

## 3.7 "Is there real reactor data?" — answer this carefully

> "Our measured-data validation is against **critical experiments** — the OECD-NEA ICSBEP handbook,
> which is physically built and measured hardware, and the standard validation basis for criticality
> worldwide. It is zero-power lattice experiments, not an operating power reactor.
>
> For depletion we use the BEAVRS pincell, which is derived from an operating PWR, but our comparison
> there is **code-to-code against Serpent**, not against measured plant data.
>
> Comparison against operating-plant measurements would be the next validation step and we do not claim
> to have done it."

**Do not say "we validated against an operating reactor."** Slide 7 says *"the BEAVRS operating-PWR
benchmark"*, which is easy to over-read. If pressed, be precise: BEAVRS is derived from an operating
reactor; your use of it is a pincell depletion comparison against a published code result.

## 3.8 What is NOT validated — know before you are asked

- **No nuclear-data sensitivity or uncertainty analysis.** Statistical uncertainty is quantified and the
  stack is benchmarked, but cross-section covariances were not propagated.
- **No external independent review.** The control is that each domain has an independent cross-check by
  a different method.
- **OpenMC is a research code**, not one with an approved licensing topical report. The claim is that
  the physics is verified and reproducible — not that this is a licensing basis.

## 3.9 The reproducibility claim — the strongest thing you own

Every table traces to a controlled record: input decks, run settings and outputs indexed in the digital
appendix with **SHA-256 checksums**, in twelve folders.

> **"Numbers on these slides come from the final production record. Nothing was re-derived for the
> presentation."**

Deliver that slowly. It is the sentence that earns trust.

---

# Numbers to have ready

| | |
|---|---|
| Extraction | **1.0 MPa / ~180 °C**, HP→IP crossover |
| Extraction penalty | **~4.9 MWe** while charging |
| Charge loop / discharge | ~168 °C → ~130 °C → 90/45 °C network |
| SOE | **8 MWe, 800 °C, 39 kWh/kg** → ~427 t/yr |
| SOE vs PEM | 39 vs ~50 kWh/kg — **25 % less electricity** |
| ICSBEP | LCT-008, **−50 pcm** mean bias, benchmark k = **1.0007** |
| Depletion | ~**20 pcm**, ~1 % nuclides vs Serpent |
| Rod worth | **±80 pcm**, 6 states, NuScale-like core |
| Statistics | 400 × 50,000, ~16 M histories, **22–26 pcm** |
