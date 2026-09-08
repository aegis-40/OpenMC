# Shutdown, design-basis events, core-damage frequency and I&C — in plain words

**Companion to `23_SAFETY-SIMULATIONS-EXPLAINED.md`.** That one lists the simulations and their
numbers. This one explains **why** they were run, what the words mean, and what to say out loud.

Read it in order. Each part builds on the one before.

---
---

# PART 1 — Shutdown, from first principles

## 1.1 What "shutting down a reactor" actually means

It is not switching something off. It means making **k < 1** — fewer neutrons in each generation than
the last — so the chain reaction dies away.

The hard part is not *getting* there. It is **staying** there, in every condition the plant can reach.

## 1.2 The one fact that makes it hard

**Cold water is a better moderator than hot water.**

Water slows neutrons down, and slow neutrons cause fission far more readily. Cold water is denser —
more hydrogen atoms per cubic centimetre — so it slows them better.

> **A cooling reactor becomes *more* reactive.**

That is your **−26.87 pcm/K** moderator coefficient read backwards.

During operation it is a safety feature: power rises → water heats → reactivity falls → power comes back
down. Self-correcting, with no operator and no instrument.

But it means **a reactor that is safely shut down while hot can wake up as it cools.**

## 1.3 Hot shutdown vs cold shutdown

| | Temperature | When |
|---|---|---|
| **Hot shutdown** | ~280–300 °C | Minutes after a trip. Rods in, still hot. |
| **Cold shutdown** | ~20–60 °C | Cooled right down — for maintenance or refuelling. |

**Cold shutdown is much harder, for two reasons stacked together:**

1. **The water is dense**, so moderation is at its most effective.
2. **Xenon has decayed away.** Xenon-135 is a powerful neutron absorber that builds up while the
   reactor runs — it has been quietly helping hold the core down. Over a day or two after shutdown it
   decays, and that help disappears.

So cold shutdown is the **worst case for reactivity**, and it is exactly where rods alone run out.

## 1.4 What MSLB is

**Main Steam Line Break** — the large steam pipe from the steam generator to the turbine ruptures.

```
pipe breaks
   → secondary side loses pressure fast
   → water in the steam generator flashes to steam
   → boiling removes heat extremely fast
   → the PRIMARY coolant is chilled
   → cold water moderates better
   → reactivity RISES
   → the reactor tries to restart — even with rods inserted
```

> **MSLB is the accident where the reactor cools itself too well.**

It is the test case because it is the worst *realistic* cooldown. Prove the rods hold through an MSLB
and they hold through anything gentler.

## 1.5 The stuck-rod rule

You are not allowed to assume all your rods work. Regulations require you to assume **one fails to
insert — and not a random one, the most reactive one.**

Otherwise a single mechanical failure would defeat the entire safety case. Every shutdown calculation
you ran has one rod deliberately left out.

## 1.6 Your results, told as a story

**Attempt 1 (N5).** 12 rods, ordinary boron carbide. With *every rod inserted* the reactor was **still
critical** — k = 1.0026. **Failed.**

**Attempt 2 (N5B).** Same 12 rods, absorber enriched to 90 % boron-10 — the isotope that actually
absorbs. Worth rose 13,409 → **15,672 pcm**. Hot shutdown worked, but barely.

**Attempt 3 (N5C) — the design.** Four extra rods added into guide tubes that already existed. Worth
rose to **21,509 pcm**, hot shutdown margin **7.85 %**. Comfortable.

**Then the cooldown test (N12C).** Final design, 15 of 16 rods in, worst rod stuck out, cool the core
step by step:

| 556 K (283 °C) | 473 K (200 °C) | **443 K (170 °C)** | 423 K (150 °C) | 294 K (20 °C) |
|---|---|---|---|---|
| k_adj 0.941 ✅ | 0.985 ✅ | **≈ 1.00 — crossover** | 1.010 ❌ | > 1.03 ❌ |

**The rods hold the core down to about 170 °C and then lose it.** Not because the design is poor —
because that is what physics does to a boron-free core as it cools.

**So you add boron (N12B).** EBIS injects 3,000 ppm. The same cold, stuck-rod case now gives
**k_adj 0.843** against a limit of 0.95.

> **That is the entire argument for a boron system in a boron-free reactor.** Rods do the fast hot
> trip. Boron does the deep cold state. They are not redundant — they do different jobs.

## 1.7 The case names, decoded

Just labels. **N** = neutronics case, number = which study, **letter = which attempt**.

| Name | Study | Version |
|---|---|---|
| **N5** | Rod worth / shutdown margin | v1 — 12 rods, natural boron → **failed** |
| **N5B** | same | v2 — 12 rods, 90 % B-10 |
| **N5C** | same | **v3 — 16 rods, 90 % B-10 → the design** |
| **N10** | EBIS boron sweep | how much boron is needed |
| **N11** | Spent-fuel pool | can the storage rack go critical |
| **N12** | MSLB cooldown | v1, old 12-rod basis |
| **N12B** | same | with EBIS credited |
| **N12C** | same | **v3 — redone on the final 16-rod basis** |

**N5C** and **N12C** describe your actual reactor. The rest are the steps that got you there.

## 1.8 Two more terms

**k_adj** — you never judge against the raw answer. You add two standard deviations of statistical noise
**plus** a 0.005 allowance for method bias, then judge *that*:

```
k_adj = k_mean + 2σ + 0.005
```

You grade yourselves on the pessimistic end of your own uncertainty band. Say so — few teams do it.

**"Return to power"** — the reactor going critical again after it was supposedly shut down. That is what
MSLB threatens and what the whole exercise exists to prevent.

## 1.9 The one-paragraph version

> A reactor gets *more* reactive as it cools. A steam-line break cools it very fast, so the accident
> that most threatens shutdown is an over-cooling one. Assuming the worst rod sticks out, our 16 rods
> hold the core shut from full power down to about 170 °C — and below that a boron-free core inherently
> wakes up. That is why we carry a dormant boron system: rods for the fast hot trip, boron for the deep
> cold state.

---
---

# PART 2 — The design-basis event matrix (slide 28)

## 2.1 What the slide is for

Nine event classes, each against an explicit acceptance criterion, each with a result. Its job is to
demonstrate **completeness and rigour** — not to teach physics. The physics lives on the dedicated
slides.

You have about a minute. **You cannot read nine rows.** Read two properly, gesture at the rest.

## 2.2 Which two, and why

**Steam-line break** and **spent-fuel-pool criticality.**

### Why MSLB

- It is **design-defining** — the event that defeats the rods and creates the requirement for EBIS.
- It carries the counter-intuitive physics (cooling adds reactivity), which immediately shows the team
  understands its own core rather than reciting outputs.
- It **sets up slide 30** two slides later.

### Why spent-fuel pool

- It is the **only genuinely fresh row** — k_adj 0.892 appears nowhere else in the deck.
- It opens a **domain the presentation otherwise barely touches**: fuel *outside* the vessel. Slide 33
  mentions flux-trap racks in one clause and that is all.
- **Fukushima Unit 4** made spent-fuel pools a public concern. The association is already in the room.

### And the pairing is clean

> **MSLB** — reactivity accident *inside* the vessel, where rods alone are not enough.
> **SFP** — fuel *outside* the vessel, sitting in water, and it still cannot go critical.
>
> Together: **we control reactivity everywhere fuel exists.**

That is a better story than two comfortable passes. Reading one hard-won result and one elimination
sounds like a team that knows where its design is strong and where it is not. Juries reward that.

## 2.3 Delivery

> "Nine event classes, each against an explicit criterion. I will take two.
>
> **Steam-line break.** The pipe ruptures, the secondary blows down, the primary is chilled. Cold water
> moderates better, so **cooling the core adds reactivity** — the reactor tries to restart even with
> rods inserted. Main-steam isolation plus boron injection takes it to k-adjusted 0.790 cold. That
> event is the reason this design carries a boron system, and I will come back to it in two slides.
>
> **Spent-fuel-pool criticality.** Fuel outside the vessel, packed close, in water — which is a
> moderator. It must be impossible for it to go critical, and we show that with three independent
> defences: flux-trap racks with neutron-absorbing panels, two thousand ppm of pool boron, and burnup
> credit. Result 0.892 against a 0.95 limit.
>
> The remaining rows — rod withdrawal, loss of heat sink, station blackout, small-break LOCA,
> containment, tube rupture and ATWS — all close against their criteria and are in the report."

Then the credibility line, which is where the real credit sits:

> "The criticality and thermal rows are closed by **our own** calculation. The dose, probabilistic and
> seismic rows are closed by reference to standards and precedent. **We distinguish between the two.**"

## 2.4 ⚠ The one thing to have ready if you read the SFP row

The unborated bounding case is **k_inf = 1.079** — above 1.0, so it does *not* meet the
10 CFR 50.68(b) unborated defence-in-depth criterion **on that bound**. Have this fluent:

> "That bound is deliberately extreme — fresh 4.95 % fuel, an infinite array, and zero burnup credit.
> Licensed storage of fuel above four percent credits burnup plus pool boron, and the borated case is
> 0.885."

**If you cannot say that comfortably, read small-break LOCA instead.**

## 2.5 What not to read, and why

| Row | Why not |
|---|---|
| **Rod withdrawal** | The criterion column says MDNBR ≥ 1.3 but the result gives a reactivity insertion rate. Do not put a juror's eye on a row with a defect. |
| **Station blackout** | The 240 h grace period is already on **four other slides**. Its frequency belongs on slide 29 — see Part 3. |
| **Containment response** | Slide 27's 0.98 MPa counterfactual is a stronger version of the same point. |
| **Small-break LOCA** | "No large break by construction" is already the headline of slide 9. |

## 2.6 A discipline worth applying deck-wide

**"≥ 240 h" appears on six slides. "Seawater-independent" appears four or five times.**

Say each in full **twice** — once as a headline (slide 4), once where it is earned (slide 27) — and
reduce it to a passing clause everywhere else. Repeating a claim makes it sound defensive rather than
settled.

---
---

# PART 3 — Core-damage frequency (slide 29)

## 3.1 What a "frequency per reactor-year" is

A **reactor-year** is one reactor operating for one year.

**Σ CDF ≈ 5.8 × 10⁻⁸ per reactor-year** means: expect one core-damage event per **17 million**
reactor-years. Or: run a thousand of these for seventeen thousand years and expect one.

## 3.2 How the number is built — event trees

Start with an **initiator** and its frequency. Then branch at every safety system: does it work or not?

```
initiator ─┬─ RHR works ────────── OK
          └─ RHR fails ─┬─ pool works ──── OK
                        └─ pool fails ─ CORE DAMAGE
```

Multiply probabilities along each path. Sum every path ending in core damage. Repeat for all nine
initiator groups.

**"Every core-damage path requires at least two independent failures"** means no single branch reaches
core damage. That is defence in depth expressed numerically.

## 3.3 The nine groups, and the sum

Your Fig. 12 roll-up, and it closes exactly:

| Group | CDF /ry |
|---|---|
| SBLOCA ≤ DN100 | 2 × 10⁻⁸ |
| LOHS / loss of feedwater | 1 × 10⁻⁸ |
| Internal hazards (fire, flood) | 1 × 10⁻⁸ |
| **External hazards (seismic, flood)** | **1 × 10⁻⁸** |
| Shutdown & refuelling states | 5 × 10⁻⁹ |
| OTSG tube rupture | 2 × 10⁻⁹ |
| General transients / AOO | 1 × 10⁻⁹ |
| SBO (LOOP + 2×AC fail) | 1 × 10⁻¹¹ |
| LBLOCA > DN100 | *not a line item — designed out* |
| **Σ** | **5.8 × 10⁻⁸** ✅ |

**Seismic IS included**, at 1 × 10⁻⁸ — about 17 % of the total. The nuance is that this value is
**screened against passive-iPWR class results**, not derived from a site-specific seismic PSA with a
hazard curve and component fragilities. Your FER says exactly that: *"bounded by passive-iPWR class
results by similarity."*

**The LBLOCA entry is the best thing on the chart.** Most teams would silently omit it; you show the
absence. That is the elimination argument made visually.

## 3.4 Where "< 10⁻⁷" comes from — and why the slide undersells you

Your FER labels both targets **"Projected class target"**. It is a target you adopted from the passive-
SMR class, not a limit anyone imposed.

| Source | CDF |
|---|---|
| NRC safety goal, subsidiary objective | ~1 × 10⁻⁴ /ry |
| IAEA INSAG-12 — existing plants | ~1 × 10⁻⁴ /ry |
| **IAEA INSAG-12 — future plants** ⭐ | **< 1 × 10⁻⁵ /ry** |
| EUR / EPRI utility requirements | 1 × 10⁻⁵ /ry |
| Modern passive Gen III+ designs report | ~10⁻⁷ – 10⁻⁸ /ry |
| **Your self-imposed target** | 1 × 10⁻⁷ /ry |
| **Your result** | **5.8 × 10⁻⁸ /ry** |

**The binding international guidance for a new plant is 10⁻⁵.** As written, the slide reads
"5.8 × 10⁻⁸ against 10⁻⁷" — a factor of **1.7**, which sounds thin. Against the guidance that
actually applies, it is a factor of about **170**.

> **You are presenting a 170× result as a 1.7× result.**

**Suggested slide edit:** change *"a design target of < 1 × 10⁻⁷"* to
**"IAEA new-plant guidance of < 1 × 10⁻⁵, and a self-imposed passive-class target of < 1 × 10⁻⁷."**
Two numbers, and the flattering one first.

## 3.5 Move the station-blackout argument here

Slide 28 should not spend time on SBO. Slide 29 should — because this is where the frequency story
lives, and because the reason behind 10⁻¹¹ is **nowhere in the deck**:

**No reactor coolant pumps means no pump seals — and therefore no seal LOCA.** In conventional PWR
assessments, station blackout leading to seal leakage is one of the largest single contributors to core
damage: you lose AC, you lose seal cooling, the seals degrade, and a small LOCA opens with nothing to
inject. It drove much of the post-Fukushima SBO rulemaking.

You have no pumps. That sequence has **no mechanism** here.

## 3.6 Delivery for slide 29

> "Nine initiator groups, quantified sequence by sequence and summed: about **5.8 times ten to the minus
> eight** per reactor-year. IAEA guidance for new plants is ten to the minus five, so that is roughly
> **170 times inside** the applicable criterion. We hold ourselves to a tighter self-imposed target of
> ten to the minus seven, which is where modern passive designs land, and we are inside that too.
>
> The interesting part is what is **not** in the sum. In conventional PWR assessments one of the largest
> contributors is blackout leading to **reactor-coolant-pump seal leakage**. We have no pumps, so no
> seals, so that sequence has no mechanism here — which is why our blackout branch sits at ten to the
> minus eleven.
>
> Internal events are quantified plant-specifically. External hazards are in the roll-up at ten to the
> minus eight, screened against passive-iPWR class results — the site-specific seismic PSA is on our
> open items."

## 3.7 Two things a PSA specialist will probe

**Internal hazards at 1 × 10⁻⁸.** In operating PWR assessments **fire is frequently comparable to or
larger than all internal events combined**. Putting fire and flood at the same level as everything else
implies screening rather than a fire PSA. Do not defend the number — say it is screened, and that the
three-hour division barriers are the physical argument behind the screen.

**The ×1.7 margin is drawn on the slide in red.** That invites *"what happens when the screened groups
are replaced by real analysis?"* Three of your top four — internal hazards, external hazards, shutdown
states — are exactly the ones that grow under detailed treatment. Which is why you lead with the
10⁻⁵ comparison, where no plausible refinement threatens the conclusion.

**Optional improvement:** split "External hazards (seismic, flood)" into two bars. Seismic deserves its
own line because it is a **common-cause** initiator — it can defeat multiple trains at once, which flood
generally cannot.

---
---

# PART 4 — I&C architecture (slide 31), term by term

Bottom-up, because that is the order the signal travels.

## Layer 1 — Field instrumentation

**"21 measurement channels."** A **channel** is one complete measurement path: sensor, wiring, and the
electronics that turn it into a usable signal. Pressure transmitters, temperature elements, neutron
flux detectors, level and flow instruments.

**"14 of them Class 1E."** **Class 1E** is the safety-grade electrical classification. Such equipment
must be:

- **environmentally qualified** — proven to still work after being inside containment during an
  accident (IEEE 323: your 150 °C, 0.5 MPa, 100 % steam, 1 MGy)
- **seismically qualified** — proven to work through the design earthquake
- **independent** of non-safety equipment (IEEE 384)
- fed from qualified power supplies

It is expensive, so you classify only what needs it. The other **seven channels are indication and
monitoring** — useful to the operator, credited for nothing.

## Layer 2 — Reactor protection system

The system that decides to **scram**. Four terms, each carrying real content.

### "Four divisions"

A **division** is not a spare sensor. It is a complete, physically separate copy of the whole chain —
sensor → processing → logic → actuation — with **its own power supply, its own cable routes, its own
room.**

> Four channels in one cabinet on one power supply is **one** channel wearing four hats.

Separation is what makes redundancy real: a fire, a flood or a cabinet failure takes out **one**
division. That is the subject of IEEE 384, which is why it is cited on the slide.

### "2-of-4 coincidence voting"

Four divisions each measure the same parameter. The reactor trips when **at least two** say the limit
has been crossed.

| Logic | Spurious trip | Failure to trip |
|---|---|---|
| 1-of-4 | one faulty sensor trips the plant ❌ | very unlikely ✅ |
| **2-of-4** | **needs 2 to fail high** ✅ | **needs 3 to fail low** ✅ |
| 3-of-4 | very unlikely ✅ | needs only 2 to fail ❌ |

Spurious trips are not harmless — they are a transient, they cycle equipment, and they cost
availability.

**Why four rather than three:** bypass one channel for testing and the logic becomes **2-of-3, still
valid**. You test each channel in rotation, online, and never lose protection. **That is how a six-year
cycle stays fully protected without a shutdown** — and it quietly answers the surveillance question
hanging over the whole deck.

### "De-energize-to-trip breakers"

The rods are held up by **electromagnets**, powered through these breakers. To scram you **open** them —
cutting the current — and the rods fall under gravity.

> The safe action is caused by the **loss** of power, not the application of it.

A broken wire, a blown fuse, a dead battery, a station blackout — every one produces a scram. **There is
no credible electrical failure that prevents shutdown**, which is why SBO sits at 10⁻¹¹ on the CDF
chart.

### "Sensor threshold to breaker ≤ 500 ms"

The **total response-time budget**: from the instant the parameter crosses its setpoint to the instant
the breaker contacts open — no more than half a second.

Inside it: sensor response, signal conditioning, analogue-to-digital conversion, logic processing, the
vote, the output relay, and the breaker's mechanical opening. Your FER splits it — **sensor-to-vote
≤ 100 ms, sensor-to-breaker ≤ 500 ms**.

**Why it matters:** the safety analysis *assumes* a trip time. If the equipment is slower, the analysis
is invalid. So 500 ms is not a description — it is a **requirement flowed down to the hardware.**

It does **not** include rod fall time; the rods then take a couple of seconds to drop.

## Layer 3 — Safety-feature actuation

RPS shuts the reactor **down**. This system starts the safety equipment **up**. Two jobs, two systems.

| Function | What it does |
|---|---|
| **Injection** | passive safety injection — gravity feed after staged depressurisation |
| **Isolation** | containment isolation valves close |
| **Feedwater** | gravity-driven emergency feedwater starts |
| **Residual-heat removal** | the two 100 % passive RHR trains start |
| **Main-steam isolation** | the MSIVs close — **this is what stops an MSLB cooldown** |

That last one links directly to Part 1. Same 2-of-4 structure, but with **latching** actuations — once
triggered they stay triggered until an operator deliberately resets, so a transient signal cannot undo
a safety action.

## Layer 4 — Distributed control, non-safety

The ordinary plant control system — feedwater, pressuriser, turbine. Not safety-grade, because nothing
in the safety analysis relies on it.

**"Taps sensor circuits through qualified one-way isolation only."** The control system needs to read
the *same* sensors the protection system uses. You cannot simply wire them together: an electrical
fault on the non-safety side could travel back and disable the safety channel.

So the signal passes through a **qualified isolation device** — an isolation amplifier or optical
isolator that passes the measurement forward and **blocks any fault propagating backward**. "Qualified"
means tested and approved to do that *under fault conditions*, not merely in normal operation.

## Layer 5 — Digital twin

**"Unidirectional data diode."** A step beyond isolation. Physically it is a fibre-optic **transmitter**
on the plant side and a **receiver** on the twin side, and nothing else. No transmitter on the twin
side, no receiver on the plant side.

> Light travels one way because **there is no component capable of sending it the other way.** It is
> not a rule that could be misconfigured — it is a missing part.

**"No credited safety function."** "Credited" is a licensing word. If the safety analysis relies on
something, that thing must be Class 1E, qualified, tested and written into the technical
specifications. Saying the twin is *not credited* means **if it fails, nothing in the safety case
changes** — which is what makes it deployable at all.

## The result line

**"No software path exists from non-safety systems into Class 1E equipment."**

The concern behind it is **software common-cause failure**: if the same code runs in all four
divisions, one bug defeats all four at once. Redundancy protects against *random* failures, not
against a *design* fault. That is why you also need a **platform-diverse** actuation system — different
technology, different code, so the same bug cannot be in both.

**⚠ The DAS is not on this slide.** Mention it verbally; it is the single biggest I&C licensing
question:

> "And the diverse actuation system I mentioned is **platform-diverse** — different technology, a
> qualified FPGA or PLC to IEC 60880 — so a software fault in the protection system cannot disable the
> backup as well."

## The three standards

| | |
|---|---|
| **IEEE 603** | Criteria for safety systems — single-failure criterion, independence, qualification, testability |
| **IEEE 384** | Independence of Class 1E equipment — physical separation, electrical isolation, barriers |
| **10 CFR 73.54** | Cyber-security rule for digital systems at nuclear plants |

## Delivery for slide 31 (~50 s)

Do **not** read the table — it is legible and the audience reads faster than you speak.

> "Five layers, ordered by safety importance, and the rule is that information flows **upward only** —
> from sensors toward the operator and the twin, never downward from non-safety into safety.
>
> Layer four taps sensor circuits through qualified one-way isolation. Layer five, the twin, sits behind
> a data diode. A firewall is software — configurable, and therefore mis-configurable. A diode is a
> transmitter on one side and a receiver on the other, with no return path in the hardware. **You cannot
> attack across a diode.**
>
> Two-of-four voting balances the two ways a protection system fails: one channel drifting high does not
> trip the plant, and a failure to trip would need three channels to fail the same way. We use four
> rather than three so one channel can be bypassed for testing while the plant still runs a valid
> two-of-three — which is how a six-year cycle stays fully protected without a shutdown.
>
> The result: no software path exists from any non-safety system into Class 1E equipment. That is
> architectural, not procedural."

## Q&A for slide 31

**"What about common-cause failure of the digital protection software?"** ⭐ *expect this*
> "That is what the diverse actuation system is for, and it is platform-diverse rather than merely
> redundant — different technology, qualified FPGA or PLC to IEC 60880. A software fault in the
> protection system does not propagate to it."

**"Why are only 14 of 21 channels Class 1E?"**
> "Because only channels that actuate protection need safety-grade qualification. The other seven are
> monitoring and indication — useful to the operator, credited for nothing."

**"Cyber security?"**
> "Ten CFR 73.54 is the framework. The architectural answer is that the highest-value target — the
> protection system — has no inbound digital path at all."

**"How do you test the protection system on a six-year cycle?"**
> "Channel by channel, online. Two-of-four lets one be bypassed while the remaining three still give
> valid two-of-three protection. The tests that genuinely need a shutdown are in-service inspection of
> in-vessel components, and that is on our open items."

**"Is ≤ 500 ms sensor-to-breaker, or does it include rod release?"**
> "Sensor threshold to breaker. Rod release follows on de-energisation."

---
---

# Appendix — corrections recorded

Kept so nobody re-litigates them.

**Seismic IS in the CDF roll-up.** I initially said it was not. Fig. 12 carries *External hazards
(seismic, flood)* at 1 × 10⁻⁸, about 17 % of the total, and the nine groups sum exactly to
5.8 × 10⁻⁸. The real nuance is *screened* versus *computed*, not present versus absent.

**Slide 29 is not thin.** Its body text is one sentence, but Fig. 12 carries the slide and is one of
the better graphics in the deck.

**"Single turbine" on slide 21 is correct.** It is one tandem-compound machine; DWSIM shows three
blocks only because it has no multi-stage turbine object.
