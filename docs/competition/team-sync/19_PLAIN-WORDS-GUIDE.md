# Aegis-40 in plain words

**For Samira.** Written to be read start to finish, as if you had never seen the design. No assumed
background beyond school physics. Every number here is one that actually appears on your slides.

You know the core physics. This guide covers **everything else** — where the heat goes, why the
temperatures are what they are, what the sea has to do with it, what the shielding simulation actually
computes, and what "waste" really means.

---

# PART 1 — Follow one joule of energy

The whole plant is one chain. If you understand the chain, every number on every slide has a place.

```
uranium fissions  →  heats water  →  water boils other water  →  steam spins turbine
   →  generator makes electricity  →  leftover heat goes to the sea
```

Everything else — shielding, waste, safety systems — is about the things that chain produces
**besides** electricity: radiation, spent fuel, and heat you cannot use.

---

## 1.1 Why the water is at 128 atmospheres

Water boils at 100 °C in your kitchen. Squeeze it and it boils hotter — that is all a pressure cooker
is. Our primary water sits at **12.8 MPa**, about **128 times atmospheric pressure**. At that pressure
water does not boil until **331 °C**.

We run the core outlet at **308 °C**. That is **23 degrees below boiling**, and those 23 degrees have a
name: **subcooling**.

**Why does staying liquid matter so much?** Because liquid water touching a hot fuel rod carries heat
away superbly. Steam does not — steam is a thermal insulator. If a film of steam ever forms on the
cladding, the heat stops leaving, and the rod temperature jumps by hundreds of degrees within seconds.
Almost the entire thermal-hydraulic design exists to prevent that one thing.

So when your slide says **258 / 308 °C, ΔT 50 K, ~23 K subcooling**, it is saying:

- water enters the core at 258 °C,
- picks up 50 degrees crossing it,
- leaves at 308 °C,
- and is still 23 degrees short of boiling, with margin to spare.

---

## 1.2 Why there are no pumps

Hot water is **less dense** than cold water. That is the entire mechanism.

```
        ┌──── steam generator ────┐     ← water is cooled here, gets heavy
        │  (high up in the vessel)│
        │                         │
     riser                    downcomer
   hot, light                 cold, heavy
        │                         │
        └──────── core ───────────┘     ← water is heated here, gets light
```

The heated column is lighter than the cooled column, so the heavy side falls and pushes the light side
up. A loop forms and keeps going by itself. It is exactly a chimney.

**The push depends on two things**: how big the density difference is (that is your 50 K ΔT), and how
far apart vertically the heating and cooling happen. That vertical separation is the **thermal centre
height, ~4.0 m** on your slide.

**And the push is genuinely tiny.** The driving head is **3.67 kPa** — the weight of about **37 cm of
water**. A domestic shower pump produces more. Everything downstream follows from that: you cannot force
much flow with such a gentle push, so the flow is modest and the temperature rise has to be large.

**Why bother, if it is so weak?** Because a pump is a machine that can stop. Bearings seize, power
fails, impellers crack. In a conventional PWR, "loss of flow" is a whole accident category with its own
analysis chapter. Here, buoyancy does not have an off switch. **Loss of offsite power is not a
loss-of-flow event** — that sentence on your slide is the payoff for accepting the weak driving force.

---

## 1.3 Mass flux — what 543 kg/m²·s means, and why it is small

**Mass flux** = how many kilograms of water pass through each square metre of flow area each second. It
is the number that decides how well the coolant scrubs heat off the fuel.

| | mass flux |
|---|---|
| Large commercial PWR | ~3,000–3,500 kg/m²·s |
| **Aegis-40** | **~543 kg/m²·s** |

**We are running at roughly one sixth of the flow of a normal PWR.** On its own, that would be
alarming — six times less coolant scrubbing the same fuel.

We get away with it because **we also put six times less power into each rod.**

| | linear heat rate |
|---|---|
| Large PWR | ~18–20 kW per metre of fuel rod |
| **Aegis-40** | **~12.4 kW/m** nominal |

This is the single most important trade in the whole design, and it is the one on slide 8:
**"we choose a low power density to gain thermal margin instead of maximising burnup."**

Gentle flow **and** gentle heating balance out. The price is that you need more fuel sitting in the core
to make the same power — which is why the core is physically large for 125 MW, why the heavy-metal
loading is 9.39 tonnes, and ultimately why the burnup is low. **Every one of those numbers traces back
to the decision to run without pumps.**

---

## 1.4 DNBR — the number the whole thermal case turns on

Put a hot surface in water and turn the power up gradually:

1. **Low power** — water just heats up. Boring, and not very effective.
2. **Medium power — nucleate boiling.** Small bubbles form on the surface, detach, and are swept away.
   This is *superb* heat transfer: each bubble carries away the latent heat of vaporisation. You want to
   be here.
3. **Too much power — boiling crisis.** Bubbles form faster than they can leave. They merge into a
   continuous vapour film. The surface is now insulated by steam, and its temperature **jumps by
   hundreds of degrees almost instantly.**

Step 3 is **DNB** — Departure from Nucleate Boiling. It is a cliff edge, not a slope.

**DNBR** is simply:

```
DNBR  =  the heat flux that WOULD cause DNB
         ──────────────────────────────────
              the heat flux you ACTUALLY have
```

**Your slide says MDNBR = 1.33.** In plain words: *at the worst spot, in the worst state of the cycle,
we are running at 75 % of the heat flux that would trigger boiling crisis.*

**Why is the limit 1.30 and not 1.0?** Because nobody can predict DNB exactly. The correlations are
fitted to thousands of experiments and they scatter. **1.30 is set so that 95 % of the time, with 95 %
confidence, DNB does not occur.** The uncertainty is already inside the 1.30.

That is why the sentence on your slide was corrected. The old wording implied 1.30 gave you "30 % extra
margin". It does not — 1.30 is *already* the protected number. Being at 1.33 means you are above the
protected limit, which is the correct and sufficient claim.

**Why three correlations?** W-3, Bowring and Groeneveld are three independent empirical fits from three
different experimental programmes. Using one would be trusting one dataset. Using three and reporting
the **most pessimistic** (W-3, 1.33) is a cross-check. Groeneveld gives 6.18 — far more optimistic. We
quote the harshest.

---

## 1.5 The secondary side — where electricity actually comes from

**The primary water never leaves the vessel.** It cannot: it is slightly radioactive, having been in the
core. Instead it flows over the outside of a coil of tubes, and a **completely separate** water supply
flows inside those tubes. Heat crosses the tube wall; nothing else does.

That coil is the **OTSG — once-through steam generator**. "Once-through" means the secondary water
enters as liquid at one end and leaves as steam at the other, in one pass, with no recirculation drum.

Secondary side numbers on your slides:

- **4.5 MPa** — at that pressure water boils at **257 °C**
- **296 °C** at the OTSG outlet — so the steam is **39 degrees hotter than its boiling point**. That is
  **superheat**, and it matters: a little superheat keeps liquid droplets out of the first turbine
  stage, where they would erode the blades.

Steam then spins the turbine, the turbine spins the generator, and you have electricity.

---

## 1.6 Why only 32 %, and why that is not a weakness

**125 MW of heat in, 40 MW of electricity out.** Where did the other 85 MW go?

Into the sea. Unavoidably.

Any heat engine is limited by the temperature difference between its hot source and its cold sink. It
is a law, not an engineering shortfall. A coal plant reaches 45 % because it superheats steam to 600 °C.
We cannot: to get water hotter you must raise the pressure, and the vessel wall thickness grows until
it becomes unbuildable. **At 296 °C, roughly a third is what thermodynamics allows.**

Every water-cooled reactor on Earth is in the 32–36 % range. So when a juror says "only 32 %?", the
answer is: *that is what a water reactor gives you, and the 68 % is not waste we chose — it is the
price of using water, which is also why the plant is cheap, well-understood and licensable.*

**And you sell some of that leftover heat.** That is what cogeneration is for: district heat at 90/45 °C
and hydrogen are made from heat that would otherwise go into the sea.

---

# PART 2 — The sea

This is where three of your slides connect, and it is worth seeing them as one story.

## 2.1 Why the condenser needs to be cold, and why it is a vacuum

A turbine produces work from a **pressure drop**. Steam enters high-pressure and leaves
low-pressure, and the bigger that drop, the more work you extract.

So you want the turbine exit pressure as low as possible. How do you make it low?

**By condensing the steam.** When steam turns back into water it shrinks by roughly **1,000×**. That
collapse *creates* the vacuum. The condenser is not a vacuum pump — the vacuum is a by-product of
condensation.

**How cold you can go is set by your cooling water.** Steam condenses at whatever temperature the
cooling water lets it reach, and its pressure is then just the vapour pressure of water at that
temperature:

| condensing at | pressure |
|---|---|
| 45 °C | 9.6 kPa |
| **39 °C** | **7.0 kPa** |
| 30 °C | 4.2 kPa |

So the chain on your Sinop slide reads:

```
Black Sea in summer          25 °C
  + warms ~9 K in condenser  34 °C
  + ~5 K to transfer heat    39 °C  ← steam condenses here
                          →  7 kPa  ← turbine exit pressure
```

**This is why the sea temperature is on a safety-hazards slide.** It is not decoration. Summer seawater
temperature sets your condenser pressure, which sets your turbine work, which sets your 40 MWe. In
winter, with 8 °C water, you get *more* power from the same reactor.

## 2.2 The thermal plume — what your dilution figure means

You pump seawater through the condenser and put it back warmer. **82.6 MW of heat** goes into the Black
Sea continuously.

**Why anyone cares:** warm water holds less dissolved oxygen, and shifts which species can live there.
So environmental rules do not cap the *heat* — they cap **how much you are allowed to warm the sea
beyond a defined "mixing zone"**, typically **3 K**.

**The discharge itself is much warmer than 3 K.** Your design outfall is **+10 K**. The fix is a
**diffuser**: instead of one big pipe, you use a manifold with many small holes. Fast jets drag in a lot
of ambient water and mix almost immediately.

**Dilution factor N** = how many parts of ambient seawater get entrained per part of discharge. And
because the heat is fixed, the temperature rise simply divides:

```
ΔT_far-field  ≈  ΔT_discharge / (N + 1)
```

That is the curve in your figure — a simple 1/N decay:

| dilution N | far-field ΔT |
|---|---|
| 1 (no diffuser) | ~5 K ❌ over the cap |
| **10** | **~0.9 K** ✓ |
| **50** | **~0.2 K** ✓ |

A normal diffuser gives **N = 10–50**, which is the shaded band on the chart. So the figure's message in
one sentence: **"with an ordinary diffuser we are comfortably inside the 3 K limit, with a factor of
three to fifteen in hand."**

⚠️ The chart says **83 MWth** and slide 11 says **82.6**. Make them match before you show it.

## 2.3 And the punchline your safety case needs

The sea does **three** jobs in this plant — and the third one is the one that matters:

1. It cools the condenser. *(makes electricity)*
2. It receives the waste heat. *(environmental)*
3. **Nothing.** It has no safety role at all.

If the sea disappeared tomorrow, you would lose all your electricity output and **nothing else**. The
safety heat sink is the 250 m³ pool inside containment. That is what "even permanent intake blockage is
a power-conversion event" means, and it is the single strongest distinction between this design and
Fukushima, where the ultimate heat sink was lost.

---

# PART 3 — Shielding

## 3.1 What is actually coming out of the core

Two kinds of radiation matter here, and they are stopped by **opposite** materials.

**Neutrons.** Uncharged, so they pass straight through electron clouds and only interact when they hit
a nucleus directly. To stop them you must first **slow them down**, and slowing happens best in
collisions with nuclei of *similar mass* — think billiard balls. The best target is **hydrogen**, which
weighs the same as a neutron. Once slow, they are easily absorbed — **boron** is superb at this.

→ **Borated polyethylene**: polyethylene is full of hydrogen to slow them, boron to swallow them.
**20 cm** of it.

**Gamma rays.** Pure energy, no mass. Stopped by sheer electron density — you want as many heavy atoms
per cubic metre as possible.

→ **Magnetite concrete.** Magnetite is an iron ore; the concrete comes out around **3.5 t/m³** instead
of 2.3 for ordinary concrete. **180 cm** of it.

**Why no lead**, which everyone expects? Three reasons, and they are all about sixty years of
operation: lead is a **toxic heavy-metal waste** at decommissioning, it **creeps** — slowly deforms
under its own weight over decades — and it **melts at 327 °C**, which is a temperature a severe accident
can reach. Concrete and polyethylene do none of those things. This is "elimination before mitigation"
applied to shielding.

## 3.2 What the simulation actually does

**Monte Carlo** means: instead of solving an equation, you **simulate individual particles**.

The computer launches one neutron with a random starting direction and energy drawn from the real
fission spectrum. It travels a random distance (drawn from the material's cross-sections), then
scatters, or is absorbed, or escapes. Then you do it again. And again. **Millions of times.**

Count how many get to the far side, and you have your answer. It is statistical, so the answer comes
with an uncertainty bar that shrinks as you run more particles. That is why your neutronics slide says
"~16 million active histories" — more histories, tighter answer.

## 3.3 The two results, and what each protects

**(a) Vessel fluence — 3.02 × 10¹⁸ n/cm² over 60 years, limit 1 × 10¹⁹**

Fast neutrons hitting steel knock atoms out of the crystal lattice. Over decades this makes the steel
**brittle** — it loses toughness and becomes more likely to crack rather than deform. This is
**embrittlement**, and it is the single thing that most limits how long a reactor vessel can operate.

**Fluence** is total neutrons per cm² accumulated over the whole life. **We are at 3.02 × 10¹⁸ against a
1 × 10¹⁹ limit — a factor of 3.3 in hand.** That is the number that lets you claim a 60-year vessel
life.

Our low power density helps here too: fewer fissions per unit volume means fewer neutrons reaching the
wall.

**(b) Dose rate outside — 0.23 µSv/h, target ≤ 10 µSv/h**

This one is about **people**, not steel. It is what a worker standing against the outside face of the
shield would receive.

**For scale: natural background radiation is about 0.1–0.3 µSv/h everywhere on Earth.** So the outside
of your shield reads roughly the same as standing in a field. That is the claim.

**Why two numbers, 0.23 and 5.5?** The "removal cross-section" — how strongly heavy concrete absorbs
radiation — has genuine spread in the published literature, because it depends on the exact aggregate.
**0.23 µSv/h uses the best estimate; 5.5 µSv/h uses the pessimistic end of the band.** Both are under
the 10 µSv/h target.

That is the real point: **the conclusion does not depend on which value you believe.** Quoting only the
optimistic number would have hidden a real uncertainty. Quoting both, and passing on both, is stronger.

---

# PART 4 — Waste

## 4.1 What "waste intensity 4.40 tHM/TWhe" means

**tHM** = tonnes of heavy metal — the uranium, plus the plutonium and other heavy elements bred inside
it. It is a mass accounting unit, not a radioactivity one.

**tHM per TWhe** = tonnes of spent fuel produced per terawatt-hour of electricity delivered. In plain
words: **how much spent fuel do you make per unit of useful energy?** Lower is better.

Two things drive it, and only two:

```
                       1000
waste intensity  =  ───────────────────
                    burnup × 24 × efficiency
```

- **Burnup** — how much energy you squeeze from each tonne before discharging it.
- **Efficiency** — how much of that heat becomes electricity.

For us: `1000 / (29.6 × 24 × 0.320) = 4.40` ✓

## 4.2 The honest version of the CAREM comparison — read this twice

| | Aegis-40 | CAREM-25 |
|---|---|---|
| Burnup | **29.6** GWd/tHM | 24.0 |
| Efficiency | **32.0 %** | 27.0 % |
| **Waste intensity** | **4.40** | **6.43** |

We are **32 % better**. But **be very clear about why**, because this is exactly where a juror will
push:

**Our burnup is low.** 29.6 against 45 for NuScale and 54 for SMART. Low burnup *normally* means *more*
waste per unit energy — it is a disadvantage, not an advantage.

**We win on efficiency, not on burnup.** 32 % versus CAREM's 27 %. That is the whole margin.

If you claim a waste advantage without naming efficiency, and a juror knows the burnup numbers, you
look either careless or evasive. **Say it yourself first:** *"per tonne of fuel we extract less energy
than the large designs; per terawatt-hour delivered we still beat CAREM, and the reason is efficiency."*

## 4.3 Decay heat — why the reactor stays hot after you switch it off

**You cannot switch off a reactor.** You can stop the chain reaction in about two seconds by dropping
the rods, but the fission products already sitting in the fuel keep decaying, and decay releases heat.

At the instant of shutdown that is roughly **6 % of full power**:

```
125 MW × ~6 %  ≈  7.95 MW   ← your slide's number
```

**Eight megawatts, in a core you have just "shut down."** It falls off quickly but never reaches zero:

| after shutdown | decay heat |
|---|---|
| immediately | **7.95 MW** |
| 1 hour | ~1 MW |
| 1 day | ~250 kW |
| **1 year** | **48.4 kW** |

**This is what destroyed Fukushima.** The reactors scrammed correctly on the earthquake. The tsunami
then removed the ability to cool decay heat, and that alone melted three cores.

So decay heat is the number that sizes everything protective in the plant:

- the **250 m³ pool** and its ≥ 240 hours of grace,
- the **spent-fuel pool** cooling,
- the **dry casks** — a cask is passively air-cooled, so fuel can only go in once decay heat is low
  enough, which is why fuel sits in the pool for years first.

## 4.4 What happens to the fuel, and what "once-through" means

**Once-through** means: use the fuel once, then store it. Take it out, cool it in the pool, move it to a
dry cask, and eventually to a deep geological repository.

The alternative is **reprocessing** — dissolving spent fuel chemically and separating the plutonium to
make new fuel. France and Russia do this. **We deliberately do not**, for two reasons: it is not
economic at our tiny arisings (about six assemblies a year), and it creates a stream of separated
plutonium, which is the one thing non-proliferation policy most wants to avoid.

**Spent fuel is classified as high-level waste** — intensely radioactive, needs shielding *and* active
cooling, and remains hazardous for a very long time.

## 4.5 The plutonium number, and why it is genuinely reassuring

**78.1 kg of plutonium at 61.6 % Pu-239.**

Uranium-238 absorbs a neutron and, after two beta decays, becomes plutonium-239. This happens in every
uranium reactor — you cannot avoid breeding plutonium.

The question is always: **could someone make a weapon from it?**

| | Pu-239 content |
|---|---|
| Weapons-grade | **> 93 %** |
| **Aegis-40 discharge** | **61.6 %** |

The rest is mostly **Pu-240, at 21.6 %** — and Pu-240 is what makes reactor plutonium unattractive:

- It **fissions spontaneously**, spitting out neutrons at random. In a weapon that means the chain
  reaction starts *before* the assembly is fully compressed — the device **pre-detonates and fizzles**.
- It generates significant **heat** and **neutron radiation**, making the material genuinely difficult
  and dangerous to handle.

This is what **"self-protecting"** means on slide 32, and it is a physics property of the fuel cycle,
not a security measure someone has to maintain.

**And the long-cycle design adds a second layer.** A core sealed for six years with no refuelling means
**no fuel movements to account for** — one seal and one camera covers the whole period. Every
multi-batch competitor has to account for fuel shuffling every 18 months. That argument is uniquely
yours.

---

# PART 5 — Cogeneration and its three barriers

## 5.1 What you are actually selling

Two extra products, both made from heat that would otherwise go into the sea:

- **District heat** — hot water at **90 °C out, 45 °C back**, piped to buildings.
- **Hydrogen** — a **solid-oxide electrolyser** splitting water. High-temperature electrolysis is more
  efficient than the ordinary kind because some of the energy is supplied as *heat* instead of
  electricity — and heat is exactly what you have spare.

**TCES** — thermochemical energy storage — is the buffer between them. **Zeolite-13X** is a mineral with
an enormous internal surface area. Push hot steam through and it dries out — that is "charging". Let
water vapour back in and it releases heat — that is "discharging".

Its advantage over a hot-water tank is that the charged state sits at **ambient temperature** and loses
nothing over time. A hot tank cools down; charged zeolite does not. **200 MWh of thermal storage** lets
you shift heat output without touching reactor power.

## 5.2 The three barriers, and the trick with pressure

You are selling heat and hydrogen to real customers. Nothing radioactive can ever reach them.

```
CORE  →│ 1. OTSG tube wall │→  │ 2. intermediate loop │→  │ 3. customer HX wall │→  PRODUCT
```

Three separate metal walls, each fully enclosing.

**But the clever part is not the barriers — it is the pressure.** The intermediate loop is deliberately
held at **higher pressure than the reactor side** at every exchanger.

So if a tube ever leaks, which way does fluid go? **From high pressure to low** — from the clean
intermediate loop *toward* the reactor. Clean water leaks in; product never leaks out.

**Leakage direction is guaranteed by physics rather than by a valve that has to work.** That is the same
philosophy as gravity rod drop and de-energize-to-actuate, applied to the customer interface.

---

# PART 6 — One-line answer for each of your slides

| Slide | In one sentence |
|---|---|
| 4 Project Summary | 125 MW of heat, 40 MW of electricity, six years without refuelling, and it cools itself for ten days with no power. |
| 6 Literature Review | Others are boron-free, or natural-circulation, or long-cycle — nobody is all three. |
| 9 Design Philosophy | Four accident classes cannot happen because the hardware that would cause them does not exist. |
| 11 Plant Parameters | The pressure keeps the water liquid; everything else follows from that. |
| 12 Reactor Vessel | One vessel holds core, steam generator and pressuriser, so there is no big pipe to break. |
| 13 Core Configuration | 37 assemblies with graded enrichment and two absorbers doing different jobs over time. |
| 14 Cycle Results | Every feedback is negative, the rods are strong, and the cycle lasts 2,224 days. |
| 15 Fuel & Materials | Ordinary licensed LWR fuel, run gently — 828 °C centreline, cladding 850 °C below its limit. |
| **16 Shielding** | **Hydrogen and boron stop neutrons, iron-rich concrete stops gammas, no lead anywhere — and the vessel sees a third of its embrittlement allowance in 60 years.** |
| **17 Waste** | **We make less spent fuel per unit of electricity than CAREM — because of efficiency, not burnup — and the plutonium is unusable for weapons.** |
| 18 Fuel Cycle | One core, one six-year load, no shuffling, no reprocessing. |
| **19 Cooling Circuit** | **Hot water rises and cold water falls; that is the whole pump system.** |
| **20 Thermal Margins** | **At the worst spot we are at 75 % of the heat flux that would cause boiling crisis.** |
| 21 Energy Conversion | Steam at 296 °C makes 40 MWe, and the leftover heat is sold instead of dumped. |
| 22 Cogeneration Isolation | Three metal walls, and the pressure gradient pushes any leak inward. |
| 34 Economics | $75–125 per MWh; Turkey already pays $123.5 at Akkuyu. Capital decides it, not physics. |
| 35 Comparison | Smallest and lowest burnup by choice; only design selling three products. |
| 36 V&V | Every number traces to a controlled record, and every domain has an independent cross-check. |
| 37 Summary | The design basis is closed and consistent; what remains is named licensing work. |

---

# The five sentences worth memorising

1. **"The pressure keeps the water liquid — 23 degrees below boiling — because liquid water cools fuel
   and steam does not."**
2. **"Hot water rises, cold water falls. That is our pump, and it cannot fail."**
3. **"At the limiting spot we are at 75 % of the heat flux that would cause boiling crisis, against a
   limit that already contains its own uncertainty."**
4. **"The sea makes our electricity and takes our waste heat, but it has no safety role — lose it and
   you lose power output, nothing else."**
5. **"Our burnup is low and we say so. We still make less waste per terawatt-hour than CAREM, and the
   reason is efficiency, not burnup."**
