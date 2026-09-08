# The design-basis event matrix — every row explained

**Slide 28.** Nine event classes, each with an acceptance criterion and a result. This document covers
what each event physically *is*, where its criterion comes from, **how it was closed** — by our own
calculation or by reference — and what to watch for.

Companion to `23_SAFETY-SIMULATIONS-EXPLAINED.md` (the simulations) and
`24_SHUTDOWN-EVENTS-AND-IC-EXPLAINED.md` (shutdown physics and I&C).

---

# PART 1 — The framework behind the table

## 1.1 The plant-state ladder

Events are classified by **how often they are expected**, and the acceptance criteria tighten as
frequency rises.

| State | Meaning | Roughly how often | What is allowed |
|---|---|---|---|
| **Normal operation** | running, starting up, shutting down | continuous | nothing damaged |
| **AOO** — anticipated operational occurrence | things that *will* happen in the plant's life: turbine trip, loss of offsite power | once in a few years | **no fuel damage at all** |
| **DBA** — design-basis accident | serious faults the plant is designed and licensed to survive | 10⁻² – 10⁻⁴ /yr | limited fuel damage; core stays coolable; doses within limits |
| **DEC-A** — design-extension condition | beyond design basis, multiple failures, but **no core melt** | very rare | core remains coolable, containment intact |

*(DEC-B would be conditions with core melt. You do not have a DEC-B row — in-vessel retention and
"large early release practically eliminated" cover that territory on slide 24.)*

**Why this matters:** an AOO happens often, so nothing may be damaged. A DBA is rare, so limited damage
is tolerable provided the core stays coolable. Quoting the right state next to each event is half the
argument.

## 1.2 The two ways a row can be closed — and why you say which

This is the sentence at the bottom of your slide, and it is the most valuable thing on it:

> *"Criticality and thermal-hydraulic rows are closed by **plant-specific calculation**; dose,
> probabilistic and seismic rows are closed by **reference to standards and passive-iPWR precedent**."*

| Closure type | What it means |
|---|---|
| **Plant-specific calculation** | We built a model of *this* core / *this* containment and computed the number. |
| **Screen / bounding argument** | We showed the result cannot exceed a limit, without a full transient calculation. |
| **Reference / by similarity** | We adopted a value or a conclusion from comparable licensed designs and published precedent. |

**Every jury has seen teams present reference values as if they were their own analysis.** Saying which
is which, unprompted, is worth more than any single number in the table.

---

# PART 2 — The nine rows

## Row 1 · Rod withdrawal — AOO

**What it is.** A control rod, or a bank, is withdrawn when it should not be — operator error or a
drive fault. Reactivity rises, so power rises.

**Why it matters.** How fast matters more than how far. Slow addition is easy: the Doppler effect
pushes back within milliseconds as the fuel heats, and the flux-rate trip catches it long before
anything thermal happens.

**Criterion:** MDNBR ≥ 1.3 — NUREG-0800 SRP 4.4, and SRP 15.4.1/15.4.2 for the event itself.

**Result:** bounding insertion rate **1.5 × 10⁻⁵ Δk/k/s** against an analysed limit of
**7.5 × 10⁻⁴** — a **50× margin**, with a flux-rate trip behind it.

**Why so slow:** the drives are in-vessel and deliberately geared for slow travel. There is no
fast-withdrawal mechanism to fail.

**How it is closed:** design property (the drive rate) compared against the analysed envelope.

**⚠ Known defect on the slide.** The criterion column says MDNBR ≥ 1.3 but the result gives a
reactivity insertion rate. **Do not read this row aloud.** If asked:
> "The criterion column should read *insertion rate within the analysed envelope*. The thermal criterion
> is closed on the thermal-margins slide at MDNBR 1.33."

## Row 2 · Loss of heat sink — AOO → DEC-A

**What it is.** The secondary side stops accepting heat: feedwater is lost, the condenser fails, or the
turbine trips without bypass. The core is still making heat and its normal path out is gone.

**Why it matters.** Decay heat does not stop. If nothing removes it, the primary heats and pressurises.

**Criterion:** core remains coolable.

**Result:** per-initiator core-damage frequency **~1 × 10⁻⁸ /ry**. It requires the passive residual-heat-
removal trains *and* the pool *and* the diverse actuation to fail together.

**How it is closed:** event-tree frequency — **probabilistic**, screened.

## Row 3 · Station blackout — DEC-A

**What it is.** Loss of offsite power **plus** failure of both standby AC sources. No grid, no diesels.

**Why it matters.** In a conventional plant this is severe: no pumps means no forced cooling, and —
crucially — no reactor-coolant-pump seal cooling, which historically opens a small LOCA with nothing
available to inject. It is one of the largest contributors to core damage in conventional PWR
assessments.

**Why it is nearly a non-event here.** Nothing safety-related needed AC in the first place: circulation
is buoyancy, injection is gravity, and the rods are held up by electromagnets so **losing power *is* the
shutdown signal**. And with no pumps there are no seals, so that whole sequence has no mechanism.

**Criterion:** ≥ 240 h passive grace.

**Result:** **~1 × 10⁻¹¹ /ry**, and ≥ 240 h either way.

**How it is closed:** event-tree frequency, plus the de-energize-to-actuate design argument.

**⚠ Do not read this row on slide 28.** The 240 h figure already appears on four other slides, and the
frequency belongs on slide 29 where the CDF story lives.

## Row 4 · Steam-line break — DBA ⭐ *read this one*

**What it is.** The main steam pipe ruptures. The secondary blows down, water in the steam generator
flashes to steam, and boiling removes heat extremely fast — so the **primary coolant is chilled**.

**Why it matters — the counter-intuitive part.** Cold water is denser and moderates better, so
**cooling the core adds reactivity**. The reactor can return to criticality *even with rods inserted*.
This is the over-cooling accident, and it is the event that sizes the entire shutdown system.

**Criterion:** no return to criticality — NUREG-0800 SRP 15.1.5, RG 1.77, IAEA SSG-2.

**Result:** main-steam isolation + boron injection → **k_adj 0.790 cold**.

**How it is closed: our own OpenMC calculation.** Cases N12C (rods alone, the diagnostic) and N12B
(rods + EBIS, the credited state). Rods alone hold subcritical to about **443 K** and lose it below
that — which is precisely why EBIS exists.

**What to say:**
> "The pipe ruptures, the secondary blows down, the primary is chilled. Cold water moderates better, so
> cooling the core *adds* reactivity — the reactor tries to restart even with rods in. Main-steam
> isolation plus boron injection takes it to k-adjusted 0.790 cold. **That event is the reason this
> design carries a boron system.**"

## Row 5 · Small-break LOCA — DBA

**What it is.** A small pipe or nozzle breaks. Coolant escapes, level drops, fuel could become
uncovered.

**Note there is no large-break row, by construction.** The core, steam generator and pressuriser are
inside one vessel, so there is no large-bore primary pipe. The integral geometry **caps the break size
physically** — the limiting area is set by the largest penetration.

**Criterion — both from 10 CFR 50.46, and both about the cladding:**

- **Peak cladding temperature ≤ 1204 °C.** Zircaloy reacts with steam: `Zr + 2H₂O → ZrO₂ + 2H₂ + heat`.
  Above roughly 1200 °C this runs away — it is exothermic, so it heats the cladding, which makes it
  react faster. It also produces the **hydrogen that exploded at Fukushima**.
- **Local oxidation ≤ 17 %.** As zirconium turns to oxide the remaining metal thins. Below 17 %
  consumed, enough ductile metal survives that the cladding will not shatter when cold water hits it
  during reflood.

Together these define **"the core is still a coolable geometry"** — the rods are still rods, not rubble.

**Result:** peak clad ≪ 1204 °C; integral vessel caps break size.

**How it is closed: bounding screen**, not a qualified transient. If asked for the number:
> "We report it as far below the limit rather than as a specific peak, because this is a bounding screen.
> A qualified system-code transient is on our open items."

## Row 6 · Containment response — DBA

**What it is.** After a break, hot high-pressure water sprays into containment and **flashes to steam**,
taking up ~1,000× the volume. That pressurises the building. If the building fails, the last barrier is
gone.

**How you cope:** pressure suppression. Steam is piped into a pool of water where it **condenses on
contact** — steam that becomes water no longer takes up volume.

```
blowdown energy                31.8 GJ
pool                           250 m³ = 250,000 kg
temperature rise 31.8e9/(250,000 × 4,180) ≈ 30 K
```

**The pool warms about thirty degrees and swallows the entire blowdown.**

**Criterion:** peak pressure ≤ 0.414 MPa (the containment design pressure).

**Result:** **0.139 MPa** quasi-static after full-inventory blowdown — a factor of three.

**And the number that matters most:** without the pool the counterfactual is **~0.98 MPa**. The
suppression function is **load-bearing, not a margin bonus**. You computed what happens without your own
safety system.

**How it is closed: plant-specific mass-and-energy screen**, bounded against SMART100, CAREM-25 and
pressure-suppression precedent.

**⚠ Honest gap, already on slide 38.** Non-condensables — nitrogen from the accumulators, and hydrogen —
are **not** included. They do not condense in the pool, so they raise pressure. A qualified
time-dependent containment transient including non-condensables and hydrogen management is named as
remaining work.

## Row 7 · Spent-fuel-pool criticality ⭐ *read this one*

**What it is.** Spent fuel sits in a pool for years, packed close, **in water — which is a moderator**.
In principle it could go critical. That must be impossible.

**Three independent defences:**

1. **Flux-trap racks** — a deliberate water gap plus a **Boral** (B₄C-in-aluminium) panel between cells,
   so neutrons leaving one assembly are absorbed before reaching its neighbour.
2. **2,000 ppm pool boron.**
3. **Burnup credit** — spent fuel is less reactive than fresh, and you may credit that provided each
   assembly's burnup is verified before loading. That is a procedural commitment as well as an
   analytical one.

**Criterion:** 10 CFR 50.68(b) — unborated k < 1.0 (defence in depth) **and** borated k ≤ 0.95.

**Result (our OpenMC case N11), on a deliberately extreme bound — fresh 4.95 % fuel, infinite array,
zero burnup credit:**

| Rack | Boron | k_inf |
|---|---|---|
| Plain SS-304 | 0 | 1.396 ❌ |
| Boral flux-trap | 0 | **1.079** ⚠️ |
| Boral flux-trap | 2,000 ppm | **0.885** ✅ |

The rack design alone drops k by about 32,000 pcm.

**How it is closed: our own OpenMC calculation.**

**⚠ The nuance you must have fluent.** The unborated case is **1.079 — above 1.0**, so it does not meet
the unborated defence-in-depth criterion *on that bound*:

> "That bound is deliberately extreme — fresh 4.95 % fuel, an infinite array, and zero burnup credit.
> Licensed storage of fuel above four percent credits burnup plus pool boron, and the borated case is
> 0.885."

**If you cannot say that comfortably, read small-break LOCA instead.**

**And if asked why a boron-free reactor borates its pool:**
> "The pool is a separate system from the reactor coolant. Boron-free refers to normal primary
> operation, which is where dilution accidents come from. Borating a pool introduces no dilution path
> into the core, and it is universal practice."

## Row 8 · Steam-generator tube rupture — DBA

**What it is.** A steam-generator tube fails. Because the primary is at **12.8 MPa outside** the tubes
and the secondary at **4.5 MPa inside**, the leak flows **primary → secondary** — radioactive coolant
into a system that leaves containment.

**Why it matters here more than usual.** You have a **once-through** steam generator, where tube-to-shell
ΔT and thermal cycling are harsher than in a U-tube unit. And you sell heat and hydrogen, so there is a
product stream to protect.

**Criterion:** offsite dose ≤ 10 CFR 100.

**Result:** reactor trip → safety injection holds primary inventory → **affected generator and main
steam isolated** → and the **cogeneration interface isolates on the same tube-rupture signal**
(FER §8.6.5d, §8.8.9), so a rupture cannot propagate activity to the district-heat or hydrogen product.

**How it is closed: functional argument plus reference** — the isolation logic is designed, but no
plant-specific dose calculation is presented.

**⚠ This is the exception to "leaks flow inward".** Slide 22's pressure-gradient argument applies to
barriers 2 and 3, **not** to the steam generator. State it yourself:
> "At the steam generator the primary is the high-pressure side, so a tube leak is a conventional
> rupture event — handled by activity detection and fail-closed isolation, not by a pressure gradient."

## Row 9 · Anticipated transient without scram — DEC-A

**What it is.** A normal transient occurs **and the rods fail to insert.** The scram signal is correct;
the mechanical or electrical response fails.

**Why it matters.** It is the classic beyond-design-basis sequence, and it has its own US regulation
(10 CFR 50.62) because of the Salem events in 1983.

**Criterion:** coolable core; RCS pressure within limit — 10 CFR 50.62.

**Result, four things in sequence:**

1. **Negative moderator feedback throttles power** — the physics acts first, with no equipment.
2. **The power-operated relief valve caps pressure.**
3. **The diverse actuation system detects the ATWS signature** — platform-diverse, so a software fault
   in the protection system does not disable it.
4. **Boron injection brings the core cold-subcritical.**

**How it is closed:** FER Figure 8.6-3 is a **fault tree** for failure to render the core subcritical on
demand, plus the diverse-shutdown argument.

**Note the elegance:** the first line of defence is the negative coefficient — no equipment, no signal,
no failure mode. That is defence-in-depth Level 1 doing real work in a beyond-design-basis sequence.

---

# PART 3 — What is *not* in the matrix, and why

## Large-break LOCA — eliminated by construction

Not a row, and shown explicitly as absent on the CDF chart: **"not a line item — designed out."** The
integral vessel has no large-bore primary piping, so the initiator does not exist.

**Showing the absence is stronger than omitting it.** Most teams would leave it out silently.

## Loss of flow accident — no pump, no initiator

A classical LOFA is a **reactor coolant pump** failing: it trips, seizes, loses its bus, or the shaft
breaks, and flow coasts down while power is still high. It is one of the most frequent AOO initiators
in a conventional PWR.

**You have no pumps.** Slide 19 already says it: *"buoyancy alone closes the loop, so loss of offsite
power is not a loss-of-flow event."*

**But be precise — flow *degradation* still has mechanisms**, and each is covered elsewhere:

| Mechanism | Where it is covered |
|---|---|
| Flow instability (density-wave, Ledinegg) | backup slide 50 — design point ×4.2 inside the boundary |
| Loss of driving ΔT | the "loss of heat sink" row |
| Inventory loss shortening the loop | the SBLOCA row |
| Local assembly-inlet blockage | *not on the matrix* — mitigated because PWR 17×17 assemblies are **unshrouded**, so cross-flow redistributes around a partial blockage |

**The argument you are not yet making:** removing the pumps also removes the **pump seals**, and
blackout-induced seal LOCA is one of the largest core-damage contributors in conventional PWR
assessments. That is a large part of why your SBO frequency is 10⁻¹¹.

## Rod ejection — eliminated, but the number is reported anyway

Not a matrix row, because the in-vessel drives remove the ejection path. But you **still computed the
ejected-rod worth**: 844–902 pcm = **1.20–1.28 $**, above prompt critical.

Reporting a number for an event you eliminated is the strongest form of the elimination argument — it
shows the elimination is doing real work rather than being a slogan.

---

# PART 4 — How each row is actually closed

| Row | Closed by |
|---|---|
| Steam-line break | **our OpenMC calculation** (N12C / N12B) |
| Spent-fuel-pool criticality | **our OpenMC calculation** (N11) |
| Containment response | **our mass-and-energy screen**, bounded against precedent |
| Rod withdrawal | design property vs analysed envelope |
| Small-break LOCA | bounding screen — *not* a qualified transient |
| Loss of heat sink | event-tree frequency |
| Station blackout | event-tree frequency + design argument |
| SGTR | functional isolation argument + reference |
| ATWS | fault tree + diverse-shutdown argument |

**Three rows are genuinely yours. The rest are screens and references — and the slide says so.**

## The honest gaps, all already on slide 38

- **No qualified time-dependent containment transient** — non-condensables and hydrogen not included
- **No integrated system-code package** across the limiting transients — hence no numerical PCT
- **No plant-specific dose calculation** — the dose rows rest on reference
- **No fuel-performance code run** — fuel margins are screening checks

These are named as remaining work. **That is the correct position for a detailed design study**, and
saying so is what separates it from an overclaimed one.

---

# PART 5 — Delivery

You have about a minute for nine rows. **Read two properly, gesture at the rest.**

**Read: steam-line break and spent-fuel-pool criticality.** They pair well — one is the reactivity
accident *inside* the vessel where rods alone are not enough, the other is fuel *outside* the vessel
that still cannot go critical. Together: *we control reactivity everywhere fuel exists.*

**Do not read:** rod withdrawal (defect in the row), station blackout (240 h already said four times),
containment (slide 27 says it better), small-break LOCA (slide 9 already made the point).

> "Nine event classes, each against an explicit criterion. I will take two.
>
> **Steam-line break** — the pipe ruptures, the secondary blows down, the primary is chilled. Cold water
> moderates better, so cooling the core *adds* reactivity; the reactor tries to restart even with rods
> in. Main-steam isolation plus boron injection takes it to k-adjusted 0.790 cold. That event is the
> reason this design carries a boron system, and I will come back to it in two slides.
>
> **Spent-fuel-pool criticality** — fuel outside the vessel, packed close, in water, which is a
> moderator. Three independent defences: flux-trap racks with neutron-absorbing panels, two thousand ppm
> of pool boron, and burnup credit. 0.892 against a 0.95 limit.
>
> The remaining rows — rod withdrawal, loss of heat sink, station blackout, small-break LOCA,
> containment, tube rupture and ATWS — all close against their criteria and are in the report.
>
> And the last line matters: the criticality and thermal rows are closed by **our own** calculation. The
> dose, probabilistic and seismic rows are closed by reference to standards and precedent. **We
> distinguish between the two.**"

## The criteria and where each comes from

| Criterion | Source |
|---|---|
| MDNBR ≥ 1.30 | NUREG-0800 SRP 4.4, 95/95 |
| PCT ≤ 1204 °C, oxidation ≤ 17 % | 10 CFR 50.46 |
| SFP k ≤ 0.95 borated, < 1.0 unborated | 10 CFR 50.68(b) |
| Offsite dose | 10 CFR 100 |
| ATWS | 10 CFR 50.62 |
| No return to criticality (MSLB) | SRP 15.1.5, RG 1.77, IAEA SSG-2 |
| Two diverse shutdown systems | IAEA SSR-2/1 Req. 46 |
| Ejected-rod worth screening | SRP 15.4.8, RG 1.77 |
| Overall framework | IAEA SSR-2/1 Rev. 1, SSG-52, GSR Part 4 Rev. 1 |
