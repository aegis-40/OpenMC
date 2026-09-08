# How the economics were calculated — method, formulas, assumptions

**For the jury question "how did you get these numbers?"** Everything here is from FER §8.12. I have
re-derived each headline figure independently and they reproduce.

---

# PART 1 — The one idea

You spend money at wildly different times: **billions up front** to build, a trickle each year for fuel
and staff, a lump at the end for decommissioning. Electricity comes out steadily for 60 years.

**Levelising** collapses all of that into a single price per megawatt-hour:

```
              all lifetime costs, discounted to today
LCOE   =   ────────────────────────────────────────────
            all lifetime electricity, discounted to today
```

The answer is in **$/MWh**, directly comparable to a wholesale power price.

---

# PART 2 — The formula, term by term

```
            OCC × IDC × CRF   +   Fixed O&M
LCOE  =  ─────────────────────────────────  +  Var O&M  +  Fuel  +  Decommissioning
                    8760 × CF
```

| Symbol | Meaning |
|---|---|
| **OCC** | Overnight capital cost — what the plant would cost if built instantly, $/kWe |
| **IDC** | Interest during construction — money spent early keeps accruing interest until start-up |
| **CRF** | Capital recovery factor — converts a lump sum into an equal annual payment |
| **CF** | Capacity factor — fraction of the year at full output |
| **8760** | Hours in a year |

## The capital recovery factor

This is the only piece of real maths, and it is the same formula a bank uses for a mortgage:

```
            r (1 + r)^N
CRF  =  ─────────────────
          (1 + r)^N − 1
```

With **r = 7 %** and **N = 60 years**:

```
(1.07)^60 = 57.95
CRF = 0.07 × 57.95 / 56.95 = 0.0712
```

**You must recover 7.12 % of the capital every year for 60 years.** Note how little the 60-year life
helps — at 7 %, money 40 years out is nearly worthless today, so stretching the life from 40 to 60
years barely moves LCOE. **The discount rate matters far more than the plant life.**

---

# PART 3 — The assumptions

| Input | Value |
|---|---|
| Net electric capacity | 40 MWe |
| Capacity factor | **0.90** (conservative; design target is 0.95) |
| Economic life | 60 years |
| Real discount rate | **7 %** (swept 3 % and 10 %) |
| Construction | 3 years |
| Overnight capital | **$3,500 / 5,000 / 8,250 / 10,000 per kWe** |
| Fixed O&M | $130 /kWe·yr |
| Variable O&M | $3 /MWh |
| Fuel | **$18.3 /MWh** (front end $17.3 + back end ~$1) |
| Decommissioning fund | $700 /kWe |
| Electricity price for NPV | $75 /MWh (swept $60–100) |

**"Real" discount rate means inflation is already removed**, so every figure is in constant 2024 dollars
and there is no inflation assumption to argue about.

---

# PART 4 — Worked example: the NOAK case

```
Capital            $3,500/kWe × 40,000 kWe        = $142 M  (incl. IDC → ~$157 M)
Annual charge      $157 M × 0.0712                = $11.2 M/yr
Annual generation  40 MW × 8760 h × 0.90          = 315,360 MWh

Capital component  $11.2 M ÷ 315,360 MWh          ≈ $35–37 /MWh
Fixed O&M          $130 × 40,000 ÷ 315,360        ≈ $16.5 /MWh
Variable O&M                                       = $3.0 /MWh
Fuel                                               = $18.3 /MWh
                                                     ─────────────
                                                     ≈ $74.8 /MWh
```

**Roughly half of every megawatt-hour is just repaying the build.** That is why capital dominates
everything else — and why a $3,500 → $8,250 swing moves LCOE by **$50/MWh**, more than fuel, O&M,
capacity factor and construction time **combined**.

## The fuel term, built from physics

Not assumed — derived from the core design:

```
Burn rate        1,465 kgHM/yr at 29.6 GWd/tHM
Enrichment       6.73 SWU and 9.07 kg natural U per kg of finished fuel
                 → about 13.3 tU and 9,860 SWU per year
Prices           U₃O₈ $85.75/lb  ·  SWU $176
Front-end cost   $3,976 per kgHM
                 → $17.3/MWh, plus ~$1/MWh once-through back end
                 → $18.3/MWh total
```

---

# PART 5 — How heat and hydrogen get priced ⭐

**This is the interesting part, and the most likely detailed question.**

One reactor makes three products from the same costs. Splitting those costs between them fairly is the
whole problem. Split by **energy** and heat looks unfairly expensive; split by **revenue** and the
answer is circular.

**We split by exergy.**

## What exergy is

**Exergy is the useful work potential of an energy stream** — how much of it you could actually turn
into work.

- **Electricity is 100 % work.** β = 1.0
- **Heat is not.** A joule of heat at 180 °C cannot all become work. The best any engine could do is the
  Carnot fraction against ambient:

```
β_heat = 1 − T_ambient / T_source = 1 − 293 K / 453 K = 0.35
```

- **Hydrogen is counted at 1.0** on its lower heating value — it is a storable chemical fuel.

> **In plain words: heat is worth about a third of electricity per joule, because that is the fraction
> you could ever convert to work. So it should carry about a third of the cost per joule.**

## The allocation

Annual exergy of each product:

| Product | Annual output | × β | Exergy (MWh) | Share |
|---|---|---|---|---|
| Electricity | 316,236 MWh | 1.00 | 316,236 | **93.3 %** |
| District heat | ~24,000 MWh-th | 0.35 | 8,400 | 2.5 % |
| Hydrogen | 427 t × 33.3 kWh/kg = 14,220 MWh | 1.00 | 14,220 | 4.2 % |
| | | | **338,856** | 100 % |

**Electricity carries 93 % of the exergy, so it bears 93 % of the shared cost.** The by-products carry
the rest — and because their share is small, they come out cheap.

## And the numbers close

Total annualised cost ≈ **$25.4 M/yr**:

```
Heat      $25.4 M × 2.5 %  = $0.63 M  ÷ 24,000 MWh-th  = $26 /MWh-th   ✅
Hydrogen  $25.4 M × 4.2 %  = $1.06 M  ÷ 427,000 kg      = $2.49 /kg     ✅
```

**Both reproduce the FER exactly.** That is a good sign the method is applied consistently.

## Why they beat market price

| | Our cost | Market |
|---|---|---|
| District heat | **$26** /MWh-th | ~$50 |
| Hydrogen | **$2.49** /kg | $3–6 green H₂ |

Not because they are subsidised — because **exergy allocation charges each product for the quality of
energy it consumes**, and low-grade heat is genuinely low-quality energy.

## The cogeneration credit

The other way of expressing the same thing. Take the heat and hydrogen revenue (~$3.3 M/yr, about 12 %
of total revenue), subtract it from total cost, re-levelise:

```
$74.8/MWh − ($3.3 M ÷ 316,236 MWh)  =  $74.8 − $10.4  ≈  $64.8 /MWh
```

**That is where the $64.8 comes from.**

---

# PART 6 — What to say

**"How did you calculate LCOE?"**
> "Standard discounted cash flow. We annuitise the capital with a capital recovery factor — seven
> percent real over sixty years gives 0.0712, so we recover just over seven percent of the capital each
> year — divide by annual generation at ninety percent capacity factor, then add O&M, fuel and
> decommissioning. Capital is about half the total."

**"How did you price the heat and hydrogen?"** ⭐
> "By exergy allocation. Electricity is pure work so it carries a factor of one. Heat at 180 degrees
> carries 0.35 — that is the Carnot fraction against ambient, the most of it you could ever convert to
> work. Hydrogen counts at one on its heating value. On that basis electricity holds ninety-three
> percent of the exergy stream, so it bears ninety-three percent of the shared cost, and the
> by-products come out at twenty-six dollars a megawatt-hour thermal and $2.49 a kilogram. They are
> below market because low-grade heat is genuinely low-quality energy, not because we subsidised them."

**"Isn't allocation arbitrary?"**
> "Any joint-product allocation involves a choice, and we say which we made. Exergy is the
> thermodynamically defensible one because it charges for energy quality rather than quantity. Splitting
> by raw energy would make heat look artificially cheap; splitting by revenue would be circular. We
> report the method, so anyone can re-allocate."

**"Why 7 percent?"**
> "It is the conventional real discount rate for this kind of comparison, and we sweep three and ten
> percent on the same slide. At three percent our nth-of-a-kind case is $55.5; at ten percent it is
> $92.1. Same plant — the difference is entirely the cost of capital."

---

# PART 7 — The honest limitations

Know these before you are asked.

| Limitation | The honest answer |
|---|---|
| **Capital cost is a literature parameter, not a bottom-up estimate** | Our own 0.6-power scaling gives $8,250/kWe — *above* the headline — and we carry it as the upper band |
| **No identified hydrogen offtaker** | The hydrogen case assumes a market that would need to develop. Independent validation of cogeneration revenue is on our open-items slide |
| **District heat assumes a Sinop network exists** | A siting and commercial precondition, not a technical one |
| **Decommissioning at $700/kWe is a literature figure** | At roughly $6/MWh it is ~8 % of LCOE, so the answer is not sensitive to it |
| **Capacity factor 0.90 vs 0.95 design target** | We used the lower one deliberately so the cost is not flattered |

**And never say it is cheap.** The credibility is entirely in naming the condition:

> "Conditionally economic, and the condition is whether a forty-megawatt unit can be built serially at
> nth-of-a-kind capital cost. That is a financing and manufacturing question, not a reactor-physics one."

---

# Numbers to have on instant recall

| | |
|---|---|
| CRF at 7 %, 60 yr | **0.0712** |
| Annual generation | **315,360 MWh** at 90 % CF |
| Cost split | capital **49 %** · O&M **26 %** · fuel **24 %** |
| LCOE range | **$74.8 – 124.7** /MWh at 7 % |
| Cogeneration credit | → **$64.8** /MWh |
| Exergy shares | electricity **93 %** · H₂ 4 % · heat 2.5 % |
| β for 180 °C heat | **0.35** = 1 − 293/453 |
| Akkuyu benchmark | **$123.5** /MWh contracted |
