# Safety simulations — every term, every case, every outcome

**Sources:** `digital-appendix/4_safety_neutronics/outputs/results/safety_neutronics_results.json`,
`openmc_model/results_mslb_n5c/*.json`, FER §8.5–8.6. Every number below is read from those files.

---

# PART 1 — The vocabulary

## Reactivity language

| Term | What it means |
|---|---|
| **k_eff** | Neutrons in one generation ÷ the previous generation. **k = 1** is steady ("critical"), **< 1** dying, **> 1** growing. |
| **k_inf** | The same, but for an infinite array — no leakage. Always higher than k_eff, and used to *bound* a real geometry. |
| **pcm** | *per cent mille*, 10⁻⁵. The unit reactivity is measured in. 1,000 pcm = 1 % change in k. |
| **σ (sigma)** | Statistical uncertainty of a Monte Carlo answer. Ours run 50–65 pcm on safety cases, 22–26 pcm on the production run. |
| **k_adj** | **The number we actually judge against.** `k_adj = k_mean + 2σ + 0.005`. Two sigma of statistics **plus a 0.005 bias allowance** for method error. It is deliberately pessimistic — we grade ourselves against the worst credible value, not the best estimate. |
| **β_eff** | The delayed-neutron fraction — the ~0.7 % of neutrons that arrive seconds later and make a reactor controllable. **704.5 ± 28.2 pcm** for this core, computed rather than assumed. |
| **dollar ($)** | Reactivity expressed in units of β_eff. **1 $ = 704.5 pcm.** At one dollar the chain reaction no longer needs delayed neutrons — power runs away in milliseconds. That is **prompt criticality**. |

## Reactor states

| Term | Meaning |
|---|---|
| **ARO** | All Rods Out — the reference unshut state. |
| **ARI** | All Rods In — everything inserted. |
| **HFP / HZP** | Hot Full Power / Hot Zero Power. Same temperature, different fuel condition. **Shutdown margins are conventionally reported at HZP.** |
| **Cold** | 294 K (20 °C). The *most reactive* state, because dense water moderates better. |
| **Stuck rod** | The mandatory single-failure assumption: **the most reactive rod fails to insert.** Not conservatism for its own sake — regulators require it. |
| **SDM** | Shutdown Margin — how far below critical you are with rods in. Reported **signed**, so a negative-looking number cannot hide a supercritical state. |

## Hardware

| Term | Meaning |
|---|---|
| **CRA** | Control Rod Assembly. You have **16**. |
| **B-10 enrichment** | Natural boron is 19.9 % B-10; the rest is B-11 and nearly useless as an absorber. Ours are **90 % B-10** — solid B₄C, so this does **not** break the boron-free claim. |
| **EBIS** | Emergency Boron Injection System — dormant, passive, **3,000 ppm**. The diverse second shutdown system required by IAEA SSR-2/1 Req. 46. |
| **ppm boron** | Parts per million of boron dissolved in the coolant. |
| **Flux trap / Boral** | Spent-fuel rack design: a water gap between cells plus a **B₄C-in-aluminium** panel, so neutrons leaving one assembly are absorbed before reaching its neighbour. |
| **Burnup credit** | Crediting the fact that used fuel is less reactive than fresh. Requires verifying each assembly's burnup before loading it. |

## Events

| Term | Meaning |
|---|---|
| **MSLB** | Main Steam Line Break. The pipe ruptures, the secondary blows down, and the primary is **chilled**. Because cold water moderates better, **cooling adds reactivity** — this is the over-cooling accident, and it is what sizes the shutdown system. |
| **REA** | Rod Ejection Accident. A drive housing fails and one rod is expelled. Bounded by the **worth of the single most reactive rod**. |
| **SFP criticality** | Can the spent-fuel pool go critical? It must be impossible. |
| **CDF / LRF** | Core Damage / Large Release Frequency, per reactor-year. |

## Method

| Term | Meaning |
|---|---|
| **Monte Carlo** | Simulate millions of individual neutrons with random scattering and absorption, then count. Statistical, so every answer has a σ. |
| **Batches / particles** | Safety cases: **180 × 20,000**. Production run: **400 × 50,000**, 80 inactive → ~16 M active histories. |
| **Inactive batches** | Discarded while the fission source converges to its true shape. |

---

# PART 2 — The simulations, one by one

## N5 / N5B / N5C — the rod-worth ladder ⭐

**Question:** can control rods alone shut this core down?

Three configurations, each a step in the design:

| Case | Configuration | Bank worth | k_ARI hot | Verdict |
|---|---|---|---|---|
| **N5** | 12 CRA, **natural** B₄C | 13,409 pcm | **1.0026** | ❌ hot trip **fails** — still critical with all rods in |
| **N5B** | 12 CRA, **90 % B-10** | 15,672 pcm | 0.9803 (k_adj 0.9866) | ⚠️ passes, but marginal |
| **N5C** | **16 CRA, 90 % B-10** | **21,509 pcm** | **0.9273** (k_adj 0.9334) | ✅ **the design** — hot SDM **7.85 %** |

**What it means.** The first configuration genuinely failed. Enriching the absorber bought +2,264 pcm;
adding four CRAs in existing guide tubes bought a further +5,836 pcm. **This is a design history, not a
single calculation** — and being able to show the failed step is a strength.

**And the honest part, recorded in the file itself:** even at 21,509 pcm the rods do **not** achieve
cold shutdown with a stuck rod — `k_stuck_cold = 1.0311`. That is why EBIS exists.

## N10 — EBIS boron sweep

**Question:** can boron alone shut down a cold, fresh, all-rods-out core? *(the deliberately extreme case)*

| Boron | k_eff |
|---|---|
| 0 ppm | 1.2357 |
| 1,000 | 1.1031 |
| 1,800 | 1.0211 |
| 2,400 | 0.9683 |
| **3,000 (credited)** | **0.9217** |
| 3,600 | 0.8807 |

**Outcome:** **2,040 ppm** reaches k = 1.00; **2,153 ppm** reaches k = 0.99. You carry **3,000**.

**What it means.** EBIS is a genuinely *independent* shutdown system — it holds the core down with **no
rods credited at all**. That is what satisfies SSR-2/1 Req. 46, and it is a stronger claim than "backup".

## N11 — spent-fuel-pool criticality

**Question:** can the storage rack go critical? Deliberately bounded: **fresh 4.95 % fuel, infinite
array, no burnable-absorber credit.**

| Rack | Boron | k_inf |
|---|---|---|
| Plain SS-304 | 0 | **1.3958** ❌ |
| Boral flux-trap | 0 | **1.0789** ⚠️ |
| Boral flux-trap | 2,000 ppm | **0.8854** ✅ |

**What it means.** The rack design alone drops k by 32,000 pcm. The borated case clears the ≤ 0.95
criterion comfortably.

**⚠️ Know this nuance.** The unborated Boral case is **1.079 — above 1.0**, so it does not meet the
10 CFR 50.68(b) unborated defence-in-depth criterion *on this bound*. The file says why: fresh 4.95 %
fuel in an infinite array with zero burnup credit is an extreme bound, and licensed storage of >4 wt %
fuel credits burnup plus soluble boron. **If asked, say that — don't let someone find it.**

## N12 / N12C / N12B — main steam line break ⭐

**Question:** during an over-cooling accident, can rods alone stop a return to power?

**N12C, on the final 16-CRA basis** — 15 of 16 rods in, most reactive rod stuck out:

| Temperature | k_adj |
|---|---|
| 556 K (hot) | **0.941** ✅ |
| 523 K | 0.963 ✅ |
| 473 K | 0.985 ✅ |
| **443 K** | **≈ 1.00 ← crossover** |
| 423 K | 1.010 ❌ |
| 294 K (cold) | > 1.03 ❌ |

**Outcome: rods hold the core subcritical from full power down to about 443 K, and lose it below that.**
This is the single most important safety-neutronics result you have, and it is the reason the design has
a boron system at all.

**N12B — the credited safe state, rods + EBIS at 3,000 ppm:**

| Temperature | k_adj |
|---|---|
| 556 K | 0.830 |
| 423 K | 0.843 |
| **294 K (cold)** | **0.843** ✅ vs ≤ 0.95 |

**What it means.** The credited response is **reactor trip + main-steam isolation + EBIS**. The
rods-alone case is the *diagnostic* that establishes the EBIS requirement — it was never meant to pass
on its own.

## REA — rod ejection

**Question:** how much reactivity does the single most reactive rod hold?

```
k (all rods out)      1.15826
k (that one rod in)   1.14705
ejected worth           844 ± 82 pcm
÷ β_eff 704.5      =  1.20 $     → ABOVE PROMPT CRITICAL
```

At full-power fuel temperature the same case gives **902 ± 34 pcm = 1.28 $**.

**What it means — and say it as strength.** A cluster at 1.2 dollars would be limiting for an
externally mounted drive. It is benign for you **only because in-vessel drives remove the ejection path
entirely.** The number is evidence that the elimination on slide 9 is doing real work.

## β_eff — the delayed-neutron fraction

**Question:** what is one dollar worth in *this* core?

**Method:** prompt-k — two runs, one with delayed neutrons suppressed
(`create_delayed_neutrons=False`), then `β = 1 − k_prompt / k_total`.

```
k_total   1.150421 ± 23.9 pcm
k_prompt  1.142316 ± 22.2 pcm
β_eff  =  704.5 ± 28.2 pcm
```

**Why it matters:** the textbook default is 650 pcm. Yours is **8 % higher**, which makes every dollar
figure less alarming than the default would. **You computed it rather than borrowing it** — a
distinguishing detail.

**Limitation to state if asked:** this is a prompt-k estimate, not adjoint-weighted IFP. OpenMC 0.15.3
exposes no IFP tally scores.

## Non-neutronic safety simulations

| Simulation | Method | Outcome |
|---|---|---|
| **Thermal margin** | OpenFOAM conjugate hot channel + 3 CHF correlations | **MDNBR 1.33** (W-3, binding) · 2.13 Bowring · 6.18 Groeneveld · 1.57 bounding AOO — vs ≥ 1.30 |
| **Flow stability** | Ishii–Zuber subcooling/phase-change screen | Design point **×4.2 inside** the boundary; Ledinegg excluded by construction |
| **Containment** | Mass-and-energy screen, 31.8 GJ into 250 m³ | **0.139 MPa** vs 0.414 design. **Without the pool: 0.98 MPa** |
| **Shielding** | Monte Carlo transport | 60-y fluence **3.02 × 10¹⁸** vs 1 × 10¹⁹ · dose **0.23 µSv/h** (5.5 bounding) vs 10 |
| **CDF** | Event trees over 9 initiator groups | **Σ ≈ 5.8 × 10⁻⁸ /ry** vs < 1 × 10⁻⁷ target — internal events only |

---

# PART 3 — Outcomes at a glance

| Case | Criterion | Result | |
|---|---|---|---|
| N5C bank worth | ≥ 5,000 pcm | **21,509 pcm** | ✅ |
| N5C hot shutdown margin | ≥ 1 % | **7.85 %** (k_ARI 0.927) | ✅ |
| N10 EBIS alone, cold | k ≤ 0.99 | 2,153 ppm needed, **3,000 credited** | ✅ |
| N11 SFP, borated | k_adj ≤ 0.95 | **0.885** | ✅ |
| N11 SFP, unborated bound | k < 1.0 | **1.079** | ⚠️ extreme bound — see note |
| N12C MSLB, rods alone | no return to power | subcritical to **443 K**, then not | ⚠️ *diagnostic* |
| N12B MSLB + EBIS | k_adj ≤ 0.95 | **0.843** cold | ✅ |
| REA ejected worth | < 1 $ benign | **1.20–1.28 $** | ⚠️ above prompt critical — **ejection path eliminated** |
| MDNBR | ≥ 1.30 | **1.33** | ✅ |
| Containment | ≤ 0.414 MPa | **0.139** | ✅ |
| Σ CDF | < 1 × 10⁻⁷ /ry | **5.8 × 10⁻⁸** | ✅ |

---

# PART 4 — The three results that need careful handling

**1 · Rods alone cannot achieve cold shutdown.** `k_stuck_cold = 1.0311`. This is not a flaw — it is
the physics of a boron-free core, and it is *why* SSR-2/1 requires two diverse systems. Present EBIS as
the designed answer, not as a patch.

> *"Rods carry the hot trip with nearly eight times the required margin. Boron covers the deep cold
> state, where a boron-free core is inherently supercritical — it needs 785 ppm and we credit 3,000."*

**2 · The ejected-rod worth is above prompt critical.** 1.20–1.28 $. Deliver it as evidence that the
in-vessel drive decision matters, not as a confession.

**3 · The unborated spent-fuel-pool bound exceeds 1.0.** 1.079 with fresh 4.95 % fuel, infinite array,
no burnup credit. State the bounding assumptions yourself and note that licensed storage of >4 wt %
fuel credits burnup plus pool boron.

## And one thing to be proud of

**The k_adj convention.** Every criterion is judged against `k_mean + 2σ + 0.005`, not against the best
estimate. You are grading yourself on the pessimistic end of your own uncertainty band, and you say so.
Very few student teams do that, and a reviewer will notice.
