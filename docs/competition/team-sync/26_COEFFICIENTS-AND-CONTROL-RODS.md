# Reactivity coefficients and control rods — how they work in Aegis-40

Two related subjects. **Coefficients** are how the reactor controls itself with no equipment.
**Control rods** are how you control it deliberately. Together they are the reactivity-control story.

Companion to `24_SHUTDOWN-EVENTS-AND-IC-EXPLAINED.md` and `25_EVENT-MATRIX-EXPLAINED.md`.

---
---

# PART 1 — The reactivity coefficients

## 1.1 What a coefficient is

A coefficient answers: **when something changes, how much does reactivity change?**

```
MTC   = pcm per kelvin of MODERATOR (water) temperature
DTC   = pcm per kelvin of FUEL temperature
Void  = pcm per percent of steam in the coolant
```

**Negative means self-correcting.** Power rises → the thing changes → reactivity falls → power comes back
down. No operator, no instrument, no signal. Positive would mean runaway.

Your three values:

| | Value | Criterion |
|---|---|---|
| **MTC** — moderator temperature | **−26.87 pcm/K** | < 0 ✅ |
| **DTC** — Doppler / fuel temperature | **−1.91 pcm/K** | < 0 ✅ |
| **Void** | **−173.2 pcm/%void** | < 0 ✅ |

## 1.2 MTC — moderator temperature coefficient, −26.87 pcm/K

**Two effects, working together.**

### Effect 1 · Density — the dominant term

Neutrons from fission are born fast, and only cause the next fission efficiently once they have been
**slowed down**. Water does the slowing, because a neutron bouncing off a hydrogen nucleus — almost the
same mass — loses most of its energy in a single collision.

Heat the water → it expands → **fewer hydrogen atoms per cubic centimetre** → fewer collisions → fewer
neutrons reach thermal energy → less fission.

**Read backwards, this is the single most important fact in your safety case:**

> **A cooling reactor becomes more reactive, because cold water is a better moderator.**

That is why an **over-cooling** accident — the steam-line break — and not an overheating one is what
sizes your shutdown system.

### Effect 2 · Spectrum hardening — and why you carry erbium

With less moderation the neutron energy spectrum shifts upward ("harder"). That matters in **opposite
directions** for your two burnable absorbers:

| Absorber | Where it absorbs | When the water heats |
|---|---|---|
| **Gadolinium** | thermal neutrons | fewer thermal neutrons → Gd absorbs **less** → **positive** contribution |
| **Erbium** | resonance at ~0.46 eV, just above thermal | harder spectrum puts **more** neutrons into that resonance → absorbs **more** → **negative** contribution |

Heavy gadolinium loading pushes MTC *toward* positive. The erbia pushes it back. That is precisely what
your FER means by *"erbia hardens resonance absorption so the moderator temperature coefficient remains
negative at beginning of cycle."*

> **Erbium is not only a burnable absorber — it is an MTC stabiliser.** That is why you carry two
> absorbers instead of one.

### Why boron-free operation helps here

In a conventional PWR, heating the water expels **boron** along with it — and removing an absorber
*adds* reactivity. That positive term is why PWR technical specifications limit beginning-of-cycle MTC,
and why it can approach zero with fresh fuel and high boron concentration.

**You have no boron, so that term does not exist.** Your MTC is comfortably negative from day one — a
genuine safety advantage of the boron-free choice, and worth saying.

## 1.3 DTC — Doppler / fuel temperature coefficient, −1.91 pcm/K

Note this is the **fuel pellet** temperature, not the water.

### The mechanism: Doppler broadening of U-238 resonances

U-238 has enormous, narrow absorption resonances — spikes at 6.7 eV, 20.9 eV, 36.7 eV and so on. Cold,
they are tall and thin: a neutron at exactly that energy is captured, one slightly off passes straight
through.

Heat the fuel and the U-238 nuclei **vibrate faster**. From the neutron's point of view the relative
velocity is smeared out, so the resonance appears **broader and shorter** — same area, wider spread.

**Why broader means more absorption — self-shielding.** In a cold, narrow resonance the outer layer of
the pellet captures everything at that exact energy and the interior sees none: the resonance is
*saturated*. Broadening opens neighbouring energies that are **not** saturated. Net effect: more
capture, less fission.

### The property that matters is speed

The fuel heats within **milliseconds** of a power rise — long before any heat reaches the water. MTC
needs seconds; Doppler acts immediately.

> **Doppler terminates a fast excursion. MTC governs steady operation.**

That is why Doppler is the coefficient that matters for rod-ejection-type events, and it is the first
thing that acts in an **ATWS**, before any equipment.

*(−1.91 pcm/K sits at the lower end of the normal PWR band of roughly −2 to −4. If pressed: the sign
and the speed are what the safety case needs, and the ejection path is eliminated by design, so Doppler
is not the limiting feedback here.)*

## 1.4 Void coefficient — −173.2 pcm/%void

**Void** = the fraction of coolant volume occupied by steam.

Same mechanism as MTC but far more extreme — you are not thinning the water, you are **removing it
locally**. That is why the number is 173 pcm per percent rather than 27 pcm per kelvin.

Negative means: bubbles form → moderation drops → fission drops → power falls → **the bubbles stop
forming.** Self-limiting.

### This is the Chernobyl coefficient

Worth knowing, because it is the association a non-technical audience has.

RBMK was moderated by **graphite**, not water — so the water was a net neutron **absorber**. Boiling it
away *removed* an absorber and **added** reactivity: a **positive** void coefficient. Power rose, more
boiling, more power.

Every water-moderated reactor has a negative void coefficient, because in a PWR **the water is the
moderator**. Losing it can only reduce fission.

## 1.5 How they combine — the power coefficient

Operationally, all three act together. Raise power and:

```
fuel heats immediately        → Doppler acts        (milliseconds)
coolant heats seconds later   → MTC acts            (seconds)
if boiling starts             → void coefficient acts
                       ↓
        net reactivity change is NEGATIVE
```

That combined response is the **power coefficient**, and it is why the reactor holds itself at a stable
power without anyone doing anything.

It is also **defence-in-depth Level 1** on slide 26 — *"inherently negative moderator, Doppler and void
coefficients"* — the only level with no equipment and therefore **no failure mode**.

## 1.6 Why "not marginally negative — strongly negative"

That phrase in the speaker notes is doing real work. Regulators do not only want the sign right; they
want **margin to the sign changing** across the cycle, across temperature, across burnup.

Your three sit comfortably negative at every state evaluated. In a conventional PWR the beginning-of-
cycle MTC is the anxious one, precisely because of the boron term — and that is the term you removed by
design.

## 1.7 Two sentences to have ready

> **"Cooling adds reactivity because cold water is denser and moderates better — that is the moderator
> coefficient read backwards, and it is why an over-cooling accident, not an overheating one, sizes our
> shutdown system."**

> **"Doppler is the fast one. The fuel heats in milliseconds, U-238 resonances broaden, capture
> increases — it acts before any heat reaches the water, which is why it is the feedback that
> terminates an excursion."**

---
---

# PART 2 — How the control rods work

## 2.1 What a control rod assembly physically is

A **17×17 fuel assembly** has 289 lattice positions:

```
264  fuel pins
 24  guide tubes      ← empty channels running the full height
  1  instrument tube
───
289
```

The **guide tubes are in every assembly**, whether or not it has a control rod. They are part of the
standard Westinghouse-type design.

A **control rod assembly (CRA)** is a "spider" — a top hub carrying **24 slender absorber rodlets** that
slide down into those guide tubes. Withdraw the spider and the tubes fill with water; insert it and
they fill with absorber.

> **This is why adding four more CRAs was cheap.** The guide tubes already existed in every assembly.
> Going from 12 to 16 CRAs cost four more drive mechanisms — not a new fuel design.

## 2.2 The absorber — and why it is enriched

**B₄C, boron carbide, enriched to 90 % B-10.**

Natural boron is only **19.9 % B-10** — and B-10 is the isotope that actually absorbs neutrons. B-11 is
very nearly transparent.

So enriching from 19.9 % to 90 % gives roughly **4.5× the absorption per unit volume**, in exactly the
same geometry. No bigger rods, no new guide tubes, no change to the fuel assembly.

**This is a solid absorber inside a sealed rodlet.** It does **not** put boron in the coolant, so the
soluble-boron-free claim is untouched. Say that explicitly if challenged — it is a fair question.

Your rod-worth ladder shows exactly what enrichment bought:

| Configuration | Bank worth |
|---|---|
| 12 CRA, natural B₄C | 13,409 pcm — **hot trip failed** |
| 12 CRA, 90 % B-10 | 15,672 pcm (**+2,264** from enrichment) |
| **16 CRA, 90 % B-10** | **21,509 pcm** (**+5,836** from four more rods) |

## 2.3 The layout — 12 peripheral + 4 central-cross

Sixteen CRAs across 37 assemblies: **12 in peripheral positions and 4 in a central cross**, all using
existing guide tubes.

**Why both regions.** Peripheral rods are efficient for total worth because the flux is high in a
compact core, but they leave the centre under-controlled. The central cross suppresses the middle,
which is also where your gadolinium is heaviest (33 rods/FA at the centre ring versus 14 at the edge).
Rods and burnable absorber are doing the same radial-flattening job by different means.

## 2.4 In-vessel drives — and what that buys

The drive mechanisms are **inside the pressure vessel**, in the upper-head envelope together with the
self-pressuriser — not on top of the head in external housings.

**What is eliminated:**

- **No head penetration for the drives** → no pressure housing to fail → **no rod-ejection path.** This
  is the elimination on slide 9.
- **No CRDM seals** → one fewer leak path.
- **No dedicated CRDM cooling system** to support and to fail.

**The price:** you can only reach a drive at **head removal**, which for a six-year cycle means once
every six years. That is exactly the maintainability open item on slide 38, and it is honest to say so.

**And the number that proves the elimination matters:** the most reactive single rod is worth
**844–902 pcm = 1.20–1.28 dollars** — above prompt critical. A cluster that strong would be limiting for
an externally mounted drive. It is benign for you **only** because there is no mechanism to eject it.

## 2.5 How they move — slowly, on purpose

Withdrawal rate is bounded at **1.5 × 10⁻⁵ Δk/k/s**, against an analysed limit of **7.5 × 10⁻⁴** — a
**50× margin**.

The drives are deliberately geared for slow travel. There is **no fast-withdrawal mechanism to fail**,
which is why the rod-withdrawal event is comfortably bounded rather than being a design driver.

*(The ARIS overview describes the drives as internal **hydraulic** CRDMs — the CAREM-25 approach. If
asked for the specific mechanism, that is the reference; the FER commits to in-vessel drives with
gravity drop on de-energisation without specifying the latch technology.)*

## 2.6 How they trip — de-energize to drop

The rods are **held up**. To scram, you **stop holding them**.

```
protection system (or diverse actuation system) reaches its 2-of-4 vote
        ↓
breakers OPEN — the holding power is cut
        ↓
rods fall into the core UNDER GRAVITY
```

> **The safe action is caused by the loss of power, not the application of it.**

A broken wire, a blown fuse, a dead battery, a station blackout — every one of them produces a scram.
**There is no credible electrical failure that prevents shutdown.** That is why station blackout sits at
10⁻¹¹ /ry on your CDF chart.

**Two independent ways to trigger it:** the reactor protection system, *or* the platform-diverse
actuation system. A software fault in one does not disable the other.

**Timing:** the **≤ 500 ms** on slide 31 is *sensor threshold to breaker opening*. Rod fall time is
separate and follows — a couple of seconds under gravity.

## 2.7 What the rods can and cannot do

**They can:**

| | |
|---|---|
| Total bank worth | **21,509 pcm** vs a ≥ 5,000 pcm criterion |
| Hot shutdown margin | **7.85 %** Δk/k, k_ARI = 0.927 — nearly **8×** the ≥ 1 % requirement |
| Hold through an MSLB cooldown | down to about **443 K** |

**They cannot:** reach cold shutdown with the most reactive rod stuck out. `k_stuck_cold = 1.031` — the
core is **supercritical**.

**That is not a flaw. It is the physics of a boron-free core**, and it is exactly why IAEA SSR-2/1
Req. 46 demands two diverse shutdown systems. EBIS covers the deep cold state, needing **785 ppm**
against the **3,000 ppm** credited — a 3.8× margin.

> **Rods do the fast hot trip. Boron does the deep cold state. They are not redundant — they do
> different jobs.**

## 2.8 The stuck-rod rule

Every shutdown calculation assumes **one rod fails to insert — and not a random one, the most reactive
one.** Regulations require it, because otherwise a single mechanical failure would defeat the whole
safety case.

That single assumption is what drives the EBIS requirement. Without it, rods alone would look adequate.

---
---

# PART 3 — Q&A

**"Your control rods contain boron. How is this a boron-free reactor?"** ⭐ *expect this*
> "Boron-free refers to **soluble** boron dissolved in the coolant, which is where dilution accidents
> come from. Our absorber is solid B₄C sealed inside rodlets — it never enters the coolant chemistry.
> The distinction matters because it is the *dilution* pathway we eliminated, not the element."

**"Why enrich the boron? That is unusual."**
> "Because only B-10 absorbs, and natural boron is under twenty percent B-10. Enriching to ninety gives
> about four and a half times the absorption in the same geometry — no bigger rods, no new guide tubes.
> Our first configuration with natural boron could not achieve hot shutdown at all; enrichment plus four
> extra assemblies took bank worth from thirteen thousand four hundred to twenty-one thousand five
> hundred pcm."

**"Sixteen rods in thirty-seven assemblies is a lot of rodded positions."**
> "It is, and that is the cost of being boron-free — the entire cycle's excess reactivity has to be held
> on solid absorbers and rods. The four extra assemblies used guide tubes that already existed in the
> standard seventeen-by-seventeen design, so the cost was four drive mechanisms, not a fuel redesign."

**"In-vessel drives eliminate ejection, but how do you maintain them?"** ⚠️
> "Access is at head removal, which for us is once every six years. Demonstrating that a drive runs six
> years untouched, and defining the inspection scope when the head does come off, is on our open-items
> slide. It is the most practical consequence of the long cycle."

**"Is your moderator coefficient negative at hot zero power?"**
> "The values reported come from the full-power production run. Hot zero power is where a boron-free
> core is least negative, and it is reported separately." *(If you cannot confirm on the day, say so.)*

**"Why is your Doppler coefficient on the low side?"**
> "It is within the normal band. What matters for the safety case is the sign and the speed — Doppler
> acts in milliseconds, before any heat reaches the coolant. And because the ejection path is
> eliminated, Doppler is not our limiting feedback."

**"What actually holds the rods up?"**
> "They are held by the drive mechanism and released on de-energisation — losing power drops them by
> gravity. Two independent paths can command it: the protection system and the platform-diverse
> actuation system."
