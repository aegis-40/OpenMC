# The Aegis-40 safety case in plain words

**For Azamkhon — slides 23–33, plus I&C.** Written to be read start to finish. No assumed background
beyond school physics. Every number here appears on a slide you present.

Companion to `19_PLAIN-WORDS-GUIDE.md`, which covers Samira's half (cooling, temperatures, the sea,
shielding, waste).

> **The one idea behind your entire block:** a reactor is dangerous for exactly two reasons — it can
> make power faster than you want, and it keeps making heat after you stop it. Every slide you present
> is about one of those two problems.

---

# PART 1 — The vocabulary, before anything else

## 1.1 k, reactivity, and pcm

A reactor runs on a chain reaction. Each fission releases neutrons; some cause the next fission.

**k** = neutrons in this generation ÷ neutrons in the previous generation.

- **k < 1** — dying away. **Subcritical.**
- **k = 1** — steady. **Critical.** (This is *normal operation*, not an emergency. "Critical" in reactor
  language just means "steady".)
- **k > 1** — growing. **Supercritical.**

**Reactivity** is how far from steady you are, written **ρ = (k − 1)/k**, and it is measured in **pcm**
— *per cent mille*, meaning **10⁻⁵**. So 1,000 pcm = 1 % change in k.

Every reactivity number on your slides is in pcm: bank worth 21,509 · BOC excess ~13,100 · ejected rod
844–902 · β_eff 704.5.

## 1.2 Delayed neutrons — why reactors are controllable at all

Here is the fact that makes nuclear power possible.

**Most neutrons appear instantly** — within about a ten-thousandth of a second of the fission. These are
**prompt** neutrons.

**But about 0.7 % appear late.** They come from certain fission products that decay seconds to *minutes*
afterwards, emitting a neutron as they go. These are **delayed** neutrons.

That tiny 0.7 % is what makes a reactor a machine a human can operate. Because the chain reaction has to
wait for those stragglers, the *average* time between generations stretches from 10⁻⁴ seconds to about
**0.1 seconds** — a thousandfold slower. Power changes take seconds, not milliseconds.

**β_eff is that delayed fraction.** For this core we computed it rather than assuming the textbook
value:

> **β_eff = 704.5 ± 28 pcm** — that is 0.705 %.

## 1.3 The dollar — and why 1.20 $ is the number that matters

Because β_eff is such a natural threshold, reactivity gets measured in units of it:

> **1 dollar = reactivity equal to β_eff = 704.5 pcm for this core.**

**Below one dollar**, the chain reaction still needs the delayed neutrons to sustain itself. Power moves
on a timescale of seconds. Controllable.

**At one dollar**, the prompt neutrons alone are enough. The reactor no longer waits for anything. Power
can multiply on a **millisecond** timescale, faster than any mechanical system can respond. This is
**prompt criticality**, and it is the condition that destroyed Chernobyl.

Now read your own slide:

> *"The highest-worth ejected cluster is 844–902 pcm = **1.20–1.28 $**, above prompt critical."*

You are stating plainly that if one of your control rods were physically ejected from the core, the
excursion would be prompt-critical.

**Which is exactly the point.** You are allowed to have rods that strong **only because there is no
mechanism by which one can be ejected** — the drives are inside the pressure vessel, so there is no
head penetration to fail and nothing to blow a rod out. Slide 9 says rod ejection is *eliminated*; this
number is what proves that elimination is doing real work rather than being a slogan.

Deliver it as strength, not as a confession.

## 1.4 Why cooling a reactor makes it *more* dangerous ⚠️

This is the most counter-intuitive thing in your whole block, and two of your slides depend on it.

Neutrons from fission are born fast. They only cause the next fission efficiently once they have been
**slowed down**, by bouncing off hydrogen in the water. Water is the **moderator**.

Now: **cold water is denser than hot water.** More hydrogen atoms per cubic centimetre. Better
moderation. **More fission.**

> **Cooling the core adds reactivity.**

That is what a **negative moderator temperature coefficient** means — your **−26.87 pcm/K**. Every
degree hotter costs you 26.87 pcm; every degree *colder* gives it back.

It is a **safety feature** in normal operation: if power rises, water heats, reactivity falls, power
comes back down. Self-correcting, with no operator and no instrument.

But it means **any accident that over-cools the core adds reactivity**. That is why a **steam-line
break** — which dumps secondary inventory and rapidly chills the primary — is the event that sizes your
shutdown margin. Cooling down is the hazard.

## 1.5 Why a boron-free reactor still has a boron system

Now the two ideas combine, and slide 30 makes complete sense.

**Hot, rods in:** the core is at ~280 °C, the water is thin, and 16 rods hold it down easily.
**Hot shutdown margin 7.85 %, k = 0.927.** Comfortable.

**Cold, rods in:** cool to 20 °C and the water density rises by roughly a quarter. That is a large
reactivity addition. On top of that, xenon — a strong neutron absorber that builds up during
operation — decays away over a day or two, adding *more* reactivity.

**And you must assume the worst single failure: the most reactive rod fails to insert.** That is the
**stuck-rod** criterion, and it is required, not conservative decoration.

Put those together — cold water, no xenon, one rod stuck — and the core **goes supercritical again**.
The rods, at 21,509 pcm, are not enough.

**So you need something else, and boron is it.** Boron-10 absorbs thermal neutrons voraciously. You need
**785 ppm** in the coolant to reach the k_adj ≤ 0.95 acceptance line; you carry **3,000 ppm**. A 3.8×
margin.

**This is why the answer to "why does a boron-free reactor have boron?" is not defensive:**

> "Boron-free is a statement about *normal operation* — that is where dilution accidents come from, and
> we have removed them. It is not a claim about the plant's total reactivity-control inventory. The rods
> carry hot shutdown with nearly eight times the required margin. Boron covers one specific state — deep
> cold with a stuck rod — where a boron-free core is inherently supercritical. We report that it needs
> 785 ppm and we credit three thousand."

---

# PART 2 — Plant states and the safety functions *(slide 24)*

## 2.1 The four states — a ladder of how bad things are

| State | What it means | How often |
|---|---|---|
| **Normal operation** | Running, or starting up, or shutting down | continuously |
| **AOO** — anticipated operational occurrence | Things that *will* happen during the plant's life. A turbine trip, a pump failure, loss of offsite power. | once every few years |
| **DBA** — design-basis accident | Serious faults the plant is *designed and licensed* to survive with no significant fuel damage. Pipe break, steam-line break. | ~10⁻² to 10⁻⁴ per year |
| **DEC-A** — design-extension condition | Beyond design basis, but still without core melt. Usually multiple failures at once. | very rare |

The ladder matters because **acceptance criteria tighten as frequency rises**. An AOO happens often, so
nothing at all may be damaged. A DBA is rare, so limited fuel damage is tolerable provided the core
stays coolable and doses stay within limits.

## 2.2 The three critical safety functions

Everything a nuclear plant must do reduces to three jobs:

1. **Control reactivity** — be able to stop the chain reaction and keep it stopped.
2. **Remove heat** — from the core and from the containment, including after shutdown.
3. **Confine radioactivity** — keep it inside physical barriers.

Your slide 24 is a **grid**: three functions × four states. Its entire purpose is to demonstrate that
**every box has an answer**. Not one is empty. That completeness is what a safety reviewer looks for
before reading a single number.

## 2.3 "Practically eliminated"

On your slide, large early release is *"practically eliminated"* in the DEC column. That is an **IAEA
term of art**, not casual language. It means the possibility has been shown to be either physically
impossible, or extremely unlikely with a high degree of confidence — not merely "we calculated a small
number".

Use it precisely, because a reviewer will know exactly what it means.

---

# PART 3 — Defence in depth *(slide 26)*

## 3.1 The idea: layers that do not share a weakness

Defence in depth means **independent successive layers**, so that failure of one does not compromise the
next. The classic analogy is slices of Swiss cheese: each has holes, but the holes do not line up.

| Level | Purpose | Your feature |
|---|---|---|
| **1** | Prevent abnormal operation | Negative coefficients — physics corrects itself |
| **2** | Detect and control it | Protection system: 21 channels, 2-of-4 voting |
| **3** | Control design-basis accidents | Passive injection, gravity feedwater, two RHR trains |
| **4** | Control severe conditions | ≥ 240 h grace, passive containment cooling |
| **5** | Off-site response | EPZ ≤ 0.5 km |

**The word that matters is *independent*.** Level 3 must not depend on level 2 having worked. Your
answer to that is the **diverse actuation system** — a second, differently-built way to reach the same
safety actions, so a common fault in the protection system does not disable level 3 as well.

## 3.2 Level 1 is genuinely the strongest, and it is free

Notice that level 1 is not equipment. Negative moderator, Doppler and void coefficients are **properties
of the physics**. They need no signal, no power, no valve, no operator, and they cannot be maintained
incorrectly.

That is worth saying out loud: **the first line of defence has no failure mode.**

---

# PART 4 — Passive safety *(slide 27)* — your strongest slide

## 4.1 "De-energize-to-actuate" — the whole philosophy in one word

Ask: what holds the control rods up?

**Electromagnets.** Cut the current and they fall by gravity.

So **losing power does not prevent a shutdown — losing power *causes* one.** There is no such thing as
"failure to scram because the power went out."

The same idea runs through the plant: valves are held by springs in their safe position and pushed open
by power. Lose instrument air, lose DC, lose the signal — everything relaxes to safe.

> **"Loss of power is an actuation signal, not a challenge."**

That sentence on your slide is the single best summary of the design philosophy, and it is why station
blackout — the event that destroyed Fukushima — is listed on your event matrix as **benign**.

## 4.2 Removing decay heat with no pumps

**You cannot switch a reactor off.** The rods stop fission in about two seconds, but the fission
products already in the fuel keep decaying, and decay releases heat:

```
125 MW × ~6 %  ≈  7.95 MW   at the moment of shutdown
```

**Eight megawatts in a core you have just "shut down."** It decays away but never to zero:

| after shutdown | heat |
|---|---|
| immediately | **7.95 MW** |
| 1 hour | ~1 MW |
| 1 day | ~250 kW |
| 1 year | **48.4 kW** |

**This is what destroyed Fukushima.** The reactors scrammed correctly on the earthquake. The tsunami
then removed the ability to remove decay heat — and that alone melted three cores.

Your answer uses the same trick as the primary loop: **hot rises, cold falls.** Two 100 %
natural-circulation residual-heat-removal trains carry heat from the vessel to a **250 m³ pool inside
containment**. No pumps. The pool is the **ultimate heat sink**, and it is *inside the building* — not
the sea.

**"100 %" means each train alone is enough.** You have two so that one can fail or be under maintenance.

## 4.3 Gravity injection and staged depressurization

To push water into a vessel at 12.8 MPa you would need a powerful pump. So instead: **first let the
pressure down, then let water fall in.**

**Staged depressurization** opens valves in sequence to bring vessel pressure down in controlled steps.
Once it is low enough, water from an elevated tank simply flows in **under its own weight**.

Gravity has never failed to work, requires no power, and cannot be switched off.

## 4.4 Pressure suppression — and the number that proves it is necessary

In a pipe break, hot high-pressure water sprays into the containment building and **flashes to steam**.
Steam takes up ~1,000× the volume of the water it came from, and it pressurises the building. If the
building bursts, you have lost your last barrier.

Two ways to cope:

- **Dry containment** — build a huge, strong building and let it take the pressure. Big PWRs use
  ~60,000 m³ of volume.
- **Pressure suppression** — pipe the steam into a pool of water, where it **condenses on contact**.
  Steam that becomes water no longer takes up volume, so the pressure never builds.

You use suppression. The arithmetic:

```
blowdown energy                 31.8 GJ
pool                            250 m³ = 250,000 kg of water
temperature rise 31.8e9 / (250,000 × 4,180)  ≈  30 K
```

**The pool warms by about thirty degrees and swallows the entire blowdown.**

| | pressure |
|---|---|
| Containment design | **0.414 MPa** |
| Analysed peak, small-break LOCA | **0.139 MPa** |
| **Counterfactual — same event, no pool** | **~0.98 MPa** |

**That third row is the most valuable number on the slide.** It says: the pool is not a comfort margin,
it is *load-bearing*. Without it the containment design pressure would be exceeded by more than a factor
of two. You computed what happens without your own safety system — that is the mark of a real analysis
rather than an assertion.

---

# PART 5 — The event matrix *(slide 28)*, event by event

Each row is a specific physical scenario. Here is what is actually happening in each.

## 5.1 Rod withdrawal — reactivity too fast

A control rod, or a bank, is withdrawn when it should not be. Reactivity rises, power rises.

The question is **how fast**. Your bounding rate is **1.5 × 10⁻⁵ Δk/k per second** against an analysed
limit of **7.5 × 10⁻⁴** — a **fiftyfold margin**. Slow reactivity addition is easy to handle: the
Doppler effect pushes back within milliseconds as the fuel heats, and the flux-rate trip catches it long
before anything thermal matters.

**Why so slow?** Because the drives are in-vessel and deliberately geared for slow travel. There is no
fast-withdrawal mechanism to fail.

## 5.2 Loss of heat sink — the secondary side stops taking heat

Feedwater is lost, or the condenser fails, or the turbine trips without bypass. The core is still making
heat and the normal path for it is gone.

Closed by **frequency**: ~1 × 10⁻⁸ per reactor-year, because it needs the passive RHR trains *and* the
pool *and* the diverse actuation to fail together.

## 5.3 Station blackout — all AC power lost

No grid, no diesels. In a conventional plant this is severe: no pumps means no cooling.

**Here it is nearly a non-event**, because nothing safety-related needed AC in the first place.
Circulation is buoyancy, injection is gravity, actuation is de-energize-to-actuate. Frequency
**~1 × 10⁻¹¹/ry**, and ≥ 240 hours of grace either way.

## 5.4 Steam-line break — the over-cooling accident ⚠️

A main steam pipe ruptures. Secondary inventory blows out, the steam generator boils dry rapidly, and
the primary is **chilled**.

**Re-read Part 1.4.** Cooling the core *adds reactivity*. So the core can return to criticality even
with rods inserted.

This is the event that sizes your shutdown system, and the answer is two-fold: **isolate** the broken
line to stop the cooldown, and **inject boron** to hold the core down. Result: **k_adj 0.790 cold** —
subcritical with margin.

## 5.5 Small-break LOCA — and where 1204 °C comes from

A small pipe or nozzle breaks. Coolant escapes, level drops, fuel could become uncovered.

**Note there is no large-break case, by construction.** The core, steam generator and pressuriser are
inside one vessel, so there is no large-bore primary pipe. The integral geometry **caps the break size**
physically.

The two acceptance numbers come from **10 CFR 50.46**, and both are about the *cladding*:

**Peak cladding temperature ≤ 1204 °C.** Zircaloy reacts with steam:

```
Zr + 2H₂O  →  ZrO₂ + 2H₂ + heat
```

Above roughly 1200 °C this runs away — it is **exothermic**, so it heats the cladding, which makes it
react faster. It also produces **hydrogen**, which is what exploded at Fukushima.

**Local oxidation ≤ 17 %.** As zirconium turns to oxide, the remaining metal thins. Below 17 % consumed,
enough ductile metal survives that the cladding will not shatter when cold water hits it during reflood.

Together these two numbers define **"the core is still a coolable geometry"** — the rods are still rods,
not rubble.

## 5.6 Spent-fuel-pool criticality — fuel outside the reactor

Spent fuel sits in a pool for years. Packed close, in water — which moderates — it could in principle go
critical. That must be impossible.

Three defences: **flux-trap racks** (a deliberate water gap plus absorber panels between cells, so
neutrons leaving one assembly are absorbed before reaching its neighbour), **2,000 ppm boron** in the
pool, and **burnup credit** (spent fuel is less reactive than fresh, and you may credit that provided
you verify each assembly's burnup before loading).

Result **k_adj = 0.892** against **≤ 0.95**.

**If asked why a boron-free reactor borates its pool:** the pool is a completely separate system.
Boron-free refers to the *reactor coolant*, which is where dilution accidents come from. Borating a pool
introduces no dilution path into the core, and it is universal practice.

---

# PART 6 — Core-damage frequency *(slide 29)*

## 6.1 What a "frequency per reactor-year" is

A **reactor-year** = one reactor operating for one year.

**Σ CDF ≈ 5.8 × 10⁻⁸ per reactor-year** means: expect one core-damage event per **17 million** reactor
years. Or: operate a thousand of these for seventeen thousand years, and expect one.

For scale, IAEA guidance suggests below **10⁻⁵/ry** for existing plants and below **10⁻⁶/ry** for new
designs. Your internal-events number is roughly **twenty times better** than the new-design target.

## 6.2 How the number is built — event trees

Start with an **initiator** and its frequency (say, loss of offsite power at 0.1 per year). Then branch
at every safety system: does it work, or not?

```
initiator ─┬─ RHR works ────────────── OK
           └─ RHR fails ─┬─ pool works ──────── OK
                         └─ pool fails ──── CORE DAMAGE
```

Multiply the probabilities along each path. Sum every path that ends in core damage. Repeat for all
**nine initiator groups**, and add them up: **5.8 × 10⁻⁸**.

**"Every core-damage path requires at least two independent failures"** means no single branch reaches
core damage — every route needs at least two things to fail together. That is defence in depth expressed
numerically.

## 6.3 The honest limitation — say it before you are asked ⚠️

The nine groups are **internal events**. They do **not** include earthquakes.

That matters, because for a passive plant **seismic frequently dominates core-damage frequency** —
passive systems already handle the internal events so well that external hazards become the largest
remaining contributor. Quantifying it needs a site-specific seismic hazard curve, which is on your open
items.

So the qualifier is not optional:

> "Internal events are quantified plant-specifically. External-hazard contributions are screened by
> reference to passive iPWR precedent, pending the site-specific PSA."

Without that sentence, a slide titled *"arithmetic"* promises more than it delivers, and a PSA
specialist will find the gap in one question. With it, you look like someone who knows exactly what
their own number does and does not cover.

---

# PART 7 — Instrumentation and control *(slide 45 — Q&A only)*

## 7.1 2-of-4 voting — why four, why two

Four independent measurement divisions watch the same parameter. A trip needs **two of them to agree**.

This balances the two ways a protection system can fail:

- **Spurious trip** — one channel drifts high. With 2-of-4 the plant does not trip. Good: unnecessary
  trips cause their own transients.
- **Failure to trip** — three channels would have to fail *in the same direction*. Vanishingly unlikely.

**Why four rather than three?** So you can take one channel out for maintenance and still be running a
valid 2-of-3. The plant stays fully protected during testing.

## 7.2 Upward-only signal flow, and the diode

The five layers are ordered by safety importance, and information may only flow **upward** — from
sensors toward the operator and the twin — never downward from non-safety systems into safety ones.

- **Layer 4** (non-safety control) taps sensor circuits through **qualified one-way isolation**.
- **Layer 5** (the digital twin) sits behind a **data diode**.

A **data diode** is not a firewall. A firewall is software — configurable, and therefore
mis-configurable. A diode is a **transmitter on one side and a receiver on the other, with no return
path in the hardware.** A signal cannot travel backward because there is nothing to carry it.

> "No software path exists from any non-safety system into Class 1E equipment. That is architectural,
> not procedural. **You cannot attack across a diode.**"

## 7.3 Class 1E and IEEE 323

**Class 1E** is the safety-grade electrical classification: qualified equipment, seismically mounted,
environmentally tested, with its own power supplies.

**IEEE 323 qualification at 150 °C, 0.5 MPa, 100 % steam and 1 MGy** means, in plain words: *this
equipment was tested in a chamber replicating conditions inside containment during an accident, and it
still worked.* You are not assuming it survives — someone put one in a chamber and proved it.

---

# PART 8 — Auxiliary systems and layout *(slides 32–33)*

## 8.1 The ventilation cascade

Air is drawn from clean areas → through potentially contaminated areas → to a filtered stack. Each zone
is held at slightly **lower** pressure than the one before it.

So when a door opens or a seal leaks, air moves **inward, toward the dirtier side**, never outward.

This is exactly the same trick as the cogeneration interface, where the intermediate loop is held above
reactor pressure so leaks flow inward. **Both make the safe direction the natural one, so no valve has
to work for containment to hold.**

## 8.2 Fire protection — divisions, not extinguishers

The safety systems are built in redundant **divisions**. Fire protection's job is to guarantee that a
fire cannot take out more than one.

**Three-hour rated barriers** between divisions means at least one full division survives any single
fire, for long enough to fight it. **Clean-agent suppression in I&C rooms** because water on electronics
would defeat the purpose.

## 8.3 Seismic categories and the gap

- **Category I** — must survive the safe-shutdown earthquake **and still perform its safety function**.
- **Category II** — need not survive, but **must not collapse onto Category I structures.**

That is why the turbine island is separated from the nuclear island by a **seismic gap**: two adjacent
buildings sway at different frequencies, and without a gap they hammer each other. The gap lets them
move independently.

**⚠️ Check the site-layout figure.** The FER says the gap is **≥ 75 mm**. The figure has been reported as
reading **"≥ 75 m"** — a factor of 1000. Seventy-five metres between reactor and turbine buildings is
plainly not what the drawing shows.

## 8.4 Safeguards — the argument nobody else can make

**"A core sealed for six years with no shuffling is one seal, one camera, and no fuel movements to
account for."**

Inspectors verify that no material has been diverted. Normally that means tracking every assembly
through every refuelling — a continuous accounting problem, every 12 to 24 months.

You refuel **once, after six years**. Between those events there is nothing to account for. The
verification problem essentially disappears.

Combine that with fuel that is **self-protecting** — 78.1 kg of plutonium at only 61.6 % Pu-239, against
the >93 % of weapons-grade, with 21.6 % Pu-240 that spontaneously fissions and would make any device
pre-detonate — and the proliferation argument is made by physics rather than by procedure.

---

# PART 9 — One line for each of your slides

| Slide | In one sentence |
|---|---|
| 23 Divider | Now the safety case, the instrumentation and the plant systems. |
| **24 Safety Criteria** | Three jobs — stop it, cool it, contain it — answered across four levels of how bad the day is, with no empty boxes. |
| **25 Site Hazards** | Hazards screened; the sea makes our power but has no safety role. |
| **26 Defence in Depth** | Five independent layers, and the first one is physics that has no failure mode. |
| **27 Passive Safety** | Losing power *causes* shutdown; without the pool, containment would see 0.98 MPa instead of 0.139. |
| **28 Event Matrix** | Every event class has an explicit criterion and an explicit result — and we say which are ours and which are by reference. |
| **29 CDF** | Nine initiator groups summed: one core-damage event per 17 million reactor-years, internal events only. |
| **30 Shutdown** | Rods carry hot shutdown with nearly eight times the margin; boron covers the one cold state where a boron-free core is inherently supercritical. |
| **31 Digital Twin** | A working advisory tool behind a one-way diode, credited for nothing. |
| **32 Auxiliary** | Everything fails to the safe position, and a core sealed for six years is a safeguards inspector's easiest job. |
| **33 Layout** | Three islands, the safety one below grade, and the energy island entirely outside the barrier set. |
| 45 I&C *(Q&A)* | Five layers, signals upward only — you cannot attack across a diode. |

---

# The six sentences worth memorising

1. **"Losing power does not prevent shutdown — losing power causes it. The rods are held up by
   electromagnets."**
2. **"Cooling the core adds reactivity, because cold water is denser and moderates better. That is why
   over-cooling, not overheating, sizes our shutdown system."**
3. **"Boron-free is a statement about normal operation. Rods carry hot shutdown with nearly eight times
   the margin; boron covers deep cold with a stuck rod, where it needs 785 ppm and we credit 3,000."**
4. **"Without the suppression pool the same accident gives 0.98 megapascals against a 0.414 design
   pressure. The pool is load-bearing, not a margin bonus."**
5. **"You cannot switch off a reactor. Eight megawatts of decay heat remain at the moment of shutdown —
   that is what destroyed Fukushima, and it is what our pool is sized for."**
6. **"Our core-damage frequency covers internal events. Seismic is not in it, and at a coastal site
   seismic can dominate — that is why the site-specific PSA is on our open-items list."**
