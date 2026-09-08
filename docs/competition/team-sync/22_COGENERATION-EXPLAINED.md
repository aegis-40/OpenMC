# How heat leaves the turbine — TCES and SOE hydrogen in detail

**Source: FER §8.9, Tables 8.9-1 to 8.9-5, and drawing AE-40-GA-005.** Everything below is in the
submitted report; this is the plain-language version plus the reasoning a juror will probe.

---

# 1 · Where the steam is taken from, and why exactly there

## The expansion, stage by stage

Your turbine is one **tandem-compound** machine with three sections on a single shaft:

| Section | Expands | Work |
|---|---|---|
| HP | 4.5 MPa → **1.0 MPa** | 14.740 MW |
| IP | **1.0 MPa** → 0.15 MPa | 13.364 MW |
| LP | 0.15 MPa → ~0.007 MPa | 14.689 MW |

**The cogeneration extraction is taken at the HP→IP crossover: 1.0 MPa, about 180 °C.**

## Why that point and not another — the question to expect

This is the sharpest question on the topic, and the answer is a genuine optimisation:

**Too early (main steam, 4.5 MPa / 296 °C)** — you would be throwing away steam that still has all
three sections of work left in it. Enormously wasteful: you would pay for heat in the most expensive
currency available.

**Too late (LP exhaust, 0.15 MPa / 111 °C)** — free in electrical terms, but **useless**. Zeolite
regeneration needs **130–180 °C**. At 111 °C you cannot dry the bed at all.

**1.0 MPa / 180 °C is the lowest point in the expansion that is still hot enough to regenerate the
store.** Extract any later and the heat is worthless; extract any earlier and you pay more electricity
than you need to.

> **Say it like this:** *"We take it at the crossover because that's the coldest steam that can still
> regenerate the store. Every bar of pressure above that is electricity we would be giving up for
> nothing."*

## What the extraction costs you

Steam taken at the crossover has already done its HP work but will never do its IP or LP work. The FER
puts the penalty at **about 4.9 MWe** while charging — export falls from 40 MWe to roughly **35 MWe**.

That is the honest trade: **you are not using waste heat, you are buying heat with electricity.** It is
worth it because heat sells at $50/MWh-th against a $26/MWh-th production cost.

---

# 2 · TCES — thermochemical storage, in detail

## The material

**Zeolite-13X** is a crystalline aluminosilicate with an enormous internal pore surface — a few grams
have roughly the surface area of a tennis court. Water molecules physically stick to that surface, and
**sticking releases heat**.

| Property | Value | What it decides |
|---|---|---|
| Adsorption enthalpy | **~3,500 kJ per kg of water** (band 3,300–3,600) | heat stored per kg adsorbed |
| Working uptake swing | **~0.20 kg water / kg zeolite** | how much of the bed is usable |
| Packed bulk density | **~650 kg/m³** | store mass → building volume |
| Energy density | **0.20 kWh/kg · 130 kWh/m³** | overall sizing |

## Charging — drying the bed

```
HP extraction steam, 1.0 MPa / 180 °C
        ↓  intermediate heat exchanger (IHX)
closed charge loop at ~168 °C
        ↓
hot gas passes through the zeolite bed
water is driven OFF the zeolite and condensed out
        ↓
bed is now DRY = "charged"
```

**The IHX is not optional and not decoration.** It means the zeolite working fluid never touches steam
or feedwater chemistry — a contamination boundary as well as a thermal one. That 12 K drop from 180 °C
to 168 °C is the exchanger approach temperature.

**Charge heat: 256 MWh_th to deliver 200 MWh_th.** Round-trip efficiency **0.78**.

## Discharging — letting the water back

```
humid stream admitted to the dry bed
        ↓
water RE-ADSORBS onto the zeolite, releasing ~3,500 kJ/kg
        ↓
bed heats to ~130 °C
        ↓  district-heat heat exchanger
90 °C flow / 45 °C return to the Sinop network
```

**25 MWth at peak, so the 200 MWh block gives about 8 hours of peak district heat.** Seasonal average
service is the 12.5 MWth class.

Note the temperature margin: discharge at **130 °C** against a network supply of **90 °C** — 40 K of
headroom, so the store still works late in a discharge when the bed is partly loaded.

## Why this beats a hot-water tank — the point that matters

**A charged zeolite bed is dry mineral at ambient temperature.** It is storing *chemical potential*, not
sensible heat.

A hot-water tank begins losing heat the moment you fill it. A dry zeolite bed loses **nothing** — it can
sit for a week and still hold its full 200 MWh. That is what turns heat output into a **scheduling
decision** rather than a constraint.

## The store is large, and you should say so first

| | Zeolite-13X / H₂O **(reference)** | NiCl₂-SrCl₂ / NH₃ (alternative) |
|---|---|---|
| Energy density | 0.20 kWh/kg | 0.272 kWh/kg |
| Mass for 200 MWh_th | **~1,000 t** | ~735 t |
| Volume | **~1,538 m³** | ~735 m³ |
| Round-trip | 0.78 | 0.88 |
| Discharge temperature | ~130 °C | ~150 °C |
| Working fluid | **water** | **ammonia** |

The ammine store is **twice as compact and more efficient**. It was rejected because an ammonia
inventory next to a nuclear island brings chemical-hazard zoning, ventilation, detection, relief and
emergency-isolation requirements.

> **Say it like this:** *"The ammine store is better on every number except one. We chose a thousand
> tonnes of zeolite and a benign working fluid over seven hundred tonnes and an ammonia licensing
> problem."*

Naming a rejected alternative and its advantage is far stronger than presenting only the winner.

## Verification

The plant-level balance was cross-checked against a first-principles adsorption calculation:

| | First principles | Plant balance | Δ |
|---|---|---|---|
| Gravimetric density | 0.194 kWh/kg | 0.20 kWh/kg | ~3 % |
| Volumetric density | 126 kWh/m³ | 130 kWh/m³ | ~3 % |
| Zeolite mass | ~1,029 t | ~1,000 t | ~3 % |
| Bed volume | ~1,582 m³ | ~1,538 m³ | ~3 % |

---

# 3 · SOE hydrogen, in detail

## Why high-temperature electrolysis, physically

Splitting water takes a fixed total energy, but it can be supplied as **electricity or as heat**:

```
ΔH  =  ΔG   +   TΔS
       ↑         ↑
   must be    can be
  electrical    HEAT
```

As temperature rises, **ΔG falls and TΔS rises** — so a larger share can arrive as heat instead of
electricity.

| | Electricity per kg H₂ |
|---|---|
| PEM / alkaline, ~80 °C | ~50 kWh/kg |
| **Solid oxide, ~800 °C** | **~39 kWh/kg** |

**About 25 % less electricity per kilogram**, and heat is exactly what you have spare. That is why the
electrolyser is solid-oxide and why it belongs on a nuclear plant rather than beside a wind farm.

## The steam feed — the second reason it is efficient

You feed the electrolyser **steam, not liquid water**. If you fed liquid, the electrolyser would have to
boil it using electricity. Feeding steam means the latent heat is paid for thermally, from the cycle.

Per the FER: a **DN150 branch of pressure-reduced deaerator-inlet steam**, taken from the reactor-
building / turbine header and run to the electrolyser unit, with isolation and flow control.

**Two design details worth quoting:**
- The steam branch is **deliberately larger than the hydrogen product line**, because it must pass the
  full electrolyser steam demand.
- The hydrogen side is **separated per NFPA 2**, the hydrogen technologies code.

## Electrical side

**8 MWe module**, drawing about **2 MWe averaged = 5 % of net electricity**, giving **~427 t of hydrogen
a year** at 39 kWh/kg. That is roughly **6 hours a night at full 8 MW, every night** — genuine off-peak
operation, with grid export dropping from 40 to 32 MWe during those hours.

Economically: 39 kWh/kg at $75/MWh means **$2.93/kg of electricity input** against a **$5/kg** product.
A $2.07/kg margin — you make hydrogen because it is worth more than the electricity, not because the
electricity is spare.

## Tritium — why it gets its own barrier

**Tritium is hydrogen.** It substitutes into water and permeates hot metal far more readily than any
other nuclide in the plant. At **800 °C** the electrolyser is the most permeable point anywhere in the
system.

So it is treated as its own pathway rather than being left to the three-barrier chain:
**permeation-barrier coatings**, a **getter on the hydrogen product**, and continuous monitoring at the
interface.

---

# 4 · The dispatch rule — "OR, not AND"

**FER Table 8.9-1: *"TCES charging OR SOE operation; simultaneous stacking not credited."***

This is the line in the Turkish özet on slide 21 — *"ısı depolama veya elektroliz, ikisi birlikte
değil"* — and a juror may ask why.

**Because both draw on the same headroom.** TCES charging costs ~4.9 MWe of export; the electrolyser
takes 8 MWe directly. Running both at once would spend the same margin twice.

Not crediting them together does two things: it **avoids double-counting** in the revenue model, and it
keeps grid export predictable. It is a conservatism, and it is worth saying that you imposed it on
yourself.

---

# 5 · The isolation chain, and the one honest exception

```
CORE →│ 1. OTSG tube wall │→ │ 2. intermediate loop │→ │ 3. customer HX wall │→ PRODUCT
```

The intermediate loop is **non-radioactive** and held at **higher pressure than the reactor-side stream
at each interface exchanger**, so it is a clean pressurised buffer — activity cannot migrate outward
across barriers 2 or 3.

**The exception, which you state yourself:** at the steam generator the primary is at **12.8 MPa outside**
the tubes and the secondary at **4.5 MPa inside**, so a tube leak there flows *primary → secondary* —
the conventional tube-rupture direction. That barrier is covered by **activity detection and fail-closed
isolation**, not by a pressure gradient, and the cogeneration interface trips on the same tube-rupture
signal.

**Layout:** the three secondary-side consumers — turbine, TCES, SOE — are co-located on a single
**Cogen (Industrial) Island, Seismic Category III, non-safety**, fed from **one main-steam corridor**
leaving the reactor building. One corridor means minimum reactor-building penetrations. Drawing
**AE-40-GA-005**.

---

# 6 · Q&A

**"Where exactly do you extract, and why there?"**
HP/IP crossover, 1.0 MPa and about 180 °C. It is the coldest steam in the expansion that can still
regenerate the zeolite, which needs 130 to 180 degrees. Anything later is too cold to be useful;
anything earlier costs electricity we do not need to spend.

**"What does the extraction cost you in electricity?"**
About 4.9 megawatts of export while charging — 40 down to roughly 35. We are not using waste heat, we
are buying heat with electricity, and it pays because heat sells at fifty dollars a megawatt-hour
thermal against a production cost of twenty-six.

**"How does a zeolite actually store heat?"**
Water sticks to its internal surface and sticking releases about 3,500 kilojoules per kilogram of
water. Drive the water off with heat and it is charged. The important part is that the charged state is
dry mineral at ambient temperature, so it loses nothing over time — a hot tank starts cooling
immediately.

**"A thousand tonnes of zeolite is a lot."**
It is, and we chose it deliberately. An ammine store is twice as compact and more efficient, but it
requires an ammonia inventory next to a nuclear island. We took the volume rather than the chemical
hazard.

**"Why solid-oxide rather than PEM?"**
Because at 800 degrees part of the splitting energy can be supplied as heat rather than electricity —
39 kilowatt-hours per kilogram against about 50. Heat is what we have spare. We also feed steam rather
than liquid water, so the latent heat is paid for thermally.

**"Can you run heat and hydrogen at the same time?"**
No, and we do not credit it. Both draw on the same margin — charging costs about 5 megawatts of export
and the electrolyser takes 8 — so crediting both would spend the same headroom twice.

**"How do you know the district-heat water is not contaminated?"**
Three physical barriers, plus an intermediate loop held above the reactor-side pressure at each
exchanger, so it is a clean pressurised buffer. The steam generator is the exception — there the
primary is the high-pressure side, so we treat a tube leak as a conventional rupture event with
activity detection and fail-closed isolation, and the cogeneration interface trips on the same signal.

**"What about tritium?"**
Tritium is hydrogen, so it permeates hot metal far more easily than anything else in the plant, and at
800 degrees the electrolyser is the most permeable point. It gets its own treatment — permeation-barrier
coatings, a getter on the hydrogen product, and continuous monitoring.

**"What happens to the reactor if the whole energy island trips?"**
Nothing. Every cogeneration function is non-safety balance of plant on a Seismic Category III island.
Losing it costs revenue and availability, never a safety function, and the plant returns to
electricity-priority operation.

---

## Numbers to have ready

| | |
|---|---|
| Extraction | **1.0 MPa / ~180 °C**, HP→IP crossover, through an IHX |
| Charge loop | **~168 °C** closed loop; regeneration band 130–180 °C |
| Discharge | **~130 °C** → 90/45 °C district-heat network |
| Store | **200 MWh_th** · ~1,000 t · ~1,538 m³ · 0.20 kWh/kg |
| Round-trip | **0.78** — 256 MWh_th charged for 200 delivered |
| Heat service | **25 MWth peak ≈ 8 h**; 12.5 MWth seasonal average |
| Charging penalty | **~4.9 MWe** export reduction |
| Electrolyser | **8 MWe SOE, 800 °C, 39 kWh/kg** → ~427 t H₂/yr |
| Steam feed | **DN150**, pressure-reduced deaerator-inlet steam, NFPA 2 on the H₂ side |
