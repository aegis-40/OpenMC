# Proving the 6-year cycle — the answer to "you can't get 4× cycle from 1.28× specific power"

**The challenge, as put to us:** *Aegis-40 has 1.28× lower specific power than NuScale, so how do you get
a roughly 4× longer cycle?*

**The short answer:** the questioner used one of the two terms in the equation, and it is the smaller
one. Cycle length is set by **burnup-per-cycle divided by specific power**, and burnup-per-cycle is
dominated by **batch strategy**, not by power density. We are single-batch; NuScale is multi-batch.

**And the ratio is not 4×. It is 3.0×.**

---

# 1 · THE IDENTITY — this is not an argument, it is a definition

Burnup is energy per unit heavy metal. Over one cycle:

```
B_cycle [MWd/tHM]  =  P [MW] × T [d]  /  HM [tHM]
```

Specific power is `q = P / HM` [MW/tHM], so this collapses to:

```
B_cycle = q × T          ⟺          T = B_cycle / q
```

**Cycle length is burnup-per-cycle divided by specific power.** Two terms. Lower specific power
lengthens the cycle; higher burnup-per-cycle lengthens the cycle. The challenge accounted for only the
first.

## ⚠ First, be exact about where the cycle length comes from

**The cycle length is not produced by a formula. It is read off the depletion calculation.**

If asked "what formula gives you six years," the correct answer is: *"No formula — a Monte Carlo
depletion calculation."* The chain is:

```
1. OpenMC 0.15.3 solves neutron transport + Bateman depletion over successive burnup steps
2. This gives k_eff(t) through life
3. T = the point where k_eff crosses 1.0        →  T = 2,224 EFPD   ← THE PRIMARY RESULT
4. Burnup is then DERIVED from it:  B_d = q × T = 13.31 × 2,224 = 29,600 MWd/tHM = 29.6 GWd/tHM
```

**So `B = q × T` is a consistency identity relating the two quantities — not the thing that generates
the cycle length.** Burnup follows from cycle length, not the reverse. Do not present it backwards; a
reactor physicist on the panel will notice immediately.

## And why no closed-form formula exists here

`k_eff` is **not linear in burnup** in this core, because that is exactly what the burnable absorbers
are for:

| Point | k_eff | Burnup |
|---|---|---|
| BOC | ≈ 1.150 | 0 |
| Gd hump peak | ≈ 1.135 | 13.5 GWd/tHM |
| EOC (k = 1) | 1.000 | 29.6 GWd/tHM |
| Extended | 0.968 | 33.4 GWd/tHM |

Average slope ≈ **507 pcm per GWd/tHM**; near EOC ≈ **842 pcm per GWd/tHM** (from 1.000 → 0.968 across
29.6 → 33.4). **The Gd₂O₃/Er₂O₃ hold-down flattens the early curve, which is the whole design intent** —
and it is precisely why a linear hand formula cannot produce the baseline cycle length. That is a point
in our favour, not against us: it is why the number required a high-statistics depletion run.

## The identity is still what you use for *comparison*

Because both reactors' numbers are public in these units, `T = B_cycle / q` is the right tool for
comparing them — and it reproduces our own figures exactly:

```
q  = 125 / 9.39                    = 13.31 MW/tHM      ✓ FER §8.2
B  = 13.31 × 2,224                 = 29.6 GWd/tHM      ✓ FER: 29.6 GWd/tHM
     2,224 / 365.25                = 6.09 FPY          ✓ FER: 6.09 full-power years
```

---

# 2 · NOW TAKE THEIR 1.28 AS GIVEN

This is the rhetorically strong move: **do not argue about NuScale's parameters.** Accept the
questioner's own number and let the identity do the work.

Given `q_N / q_A = 1.28` (theirs), `T_A = 2,224 EFPD` (ours), `T_N = 730 d` (24 months):

```
q_N       = 1.28 × 13.31           = 17.04 MW/tHM
B_N       = q_N × T_N = 17.04 × 730 = 12,440 MWd/tHM  = 12.4 GWd/tHM per cycle
B_A / B_N = 29.6 / 12.4            = 2.39
```

Decompose the cycle-length ratio:

```
T_A / T_N  =  (B_A / B_N) × (q_N / q_A)
           =     2.39     ×     1.28
           =     3.05                        ✓ and 2224 / 730 = 3.05
```

## The result, in one line

| Factor | Contribution | Source |
|---|---|---|
| **Burnup per cycle** | **× 2.39** | **single-batch vs multi-batch fuel management** |
| Specific power | × 1.28 | lower power density |
| **Total** | **× 3.05** | |

**Specific power alone takes 24 months to 30.7 months.** Everything beyond that — the large majority —
is the batch strategy. That is the whole answer.

*(Side note worth making: at 37 FA / 17×17 / 2.0 m, our core and NuScale's have essentially the same
heavy-metal loading. So the 1.28× in specific power is really just 160 MWth ÷ 125 MWth — same core,
different power rating.)*

---

# 3 · THE CLINCHER — our fuel burns *less*, not more

This is the sentence that ends the argument:

> **Our discharge burnup is 29.6 GWd/tHM. NuScale's is roughly 40–50. We do not extract more energy per
> kilogram of fuel than they do — we extract less. We simply extract it all in one sitting instead of
> over three or four reloads.**

A long cycle is not a claim of superior fuel performance. It is the arithmetic consequence of choosing
`n = 1`. Nobody can accuse us of overstating burnup, because we are **below** the comparator on the very
quantity that would matter.

And per §8.11, no assembly exceeds **42 GWd/tHM** — a >30 % margin to the 62 GWd/MTU qualification
ceiling even in the hottest position.

---

# 4 · THE METHOD BEHIND THE BATCH TERM — Linear Reactivity Model

For an equilibrium *n*-batch cycle with equal batch sizes and `k∞` falling linearly with burnup:

```
B_discharge(n) = [ 2n / (n+1) ] × B_1
B_cycle(n)     = B_discharge / n  =  [ 2 / (n+1) ] × B_1
```

where `B_1` is the once-through (single-batch) burnup to the same reactivity limit — **our 29.6 GWd/tHM**.

## This is verifiable against our own FER — use it

The FER quotes a 3-batch option of **≈ 44.4 GWd/tHM**. Check:

```
B_d(3) = [2×3 / 4] × 29.6 = 1.5 × 29.6 = 44.4 GWd/tHM        ✓ EXACT
```

**The FER's 44.4 is precisely the LRM prediction from 29.6.** That is not a coincidence — it is how the
number was produced, and it proves the standard method was used rather than a convenient assumption.

## The table that settles the whole question

Apply LRM to **our own core**, changing nothing but the batch number:

| n | B_cycle (GWd/tHM) | T = B_cycle/q | Cycle length | B_discharge |
|---|---|---|---|---|
| **1 (baseline)** | **29.6** | 2,224 EFPD | **6.09 yr** | **29.6** |
| 2 | 19.7 | 1,483 EFPD | 4.06 yr | 39.5 |
| 3 | 14.8 | 1,112 EFPD | 3.04 yr | 44.4 |
| 4 | 11.8 | 890 EFPD | 2.44 yr | 47.4 |
| **5** | **9.87** | **741 EFPD** | **2.03 yr ≈ 24 months** | **49.3** |

> **Run our identical core — same power, same specific power, same 1.28× — on a five-batch scheme and
> you get a 24-month cycle. NuScale's cycle. The physics did not change; only the fuel-management choice
> did.**

That is the proof that specific power is not what drives the answer. Same core, same 1.28×, cycle length
anywhere from 2 to 6 years depending purely on `n`.

---

# 5 · WHERE THEIR "4×" CAME FROM

`6.09 yr ÷ 24 months = 3.05`, not 4. If they got 4× they likely either used an **18-month** cycle for
NuScale (6.09/1.5 = 4.06) or compared our figure against a shorter reference.

**Correct them gently and precisely** — "the ratio is three, not four" — because it shows you have the
numbers and it shrinks the thing you have to explain.

---

# 6 · THE TRAP TO AVOID — EFPD vs calendar months

**Our 6.09 years is 2,224 EFPD — full-power years.** NuScale's "24 months" is normally quoted as a
*calendar* refuelling interval. These are not the same unit, and a sharp questioner will find it.

## The relation

```
EFPD = calendar days × CF          ⟺          calendar days = EFPD / CF
```

Since `CF ≤ 1`, **calendar time is always the larger number.** EFPD removes every hour the reactor was
not at 100 % power. Our 2,224 EFPD at CF = 0.90 is **2,471 calendar days ≈ 6.8 calendar years**.

**So quoting "6.09 years" is the conservative choice — it is the smaller, full-power figure.** Never let
anyone reframe it as though EFPD inflated the number; it does the opposite.

## What this does to the ratio

Convert consistently and it does not matter which unit you land in — but it does depend on the capacity
factor you attribute to their 24 months:

| Basis | Aegis-40 | NuScale (CF = 0.95) | Ratio |
|---|---|---|---|
| EFPD | 2,224 | 730 × 0.95 = 694 | **3.21** |
| Calendar days | 2,224 / 0.95 = 2,341 | 730 | **3.21** |
| *Mixed (our EFPD vs their calendar)* | 2,224 | 730 | *3.05* |

In general the ratio is `3.05 / CF`. **The consistent comparison gives ~3.2; the mixed one gives 3.05.**

**Quote 3.05 anyway.** It is the conservative end, it is the number that is hardest to attack, and
conceding the smaller figure while still being right is a strong position. Just state the basis before
someone else does:

> "To be precise, our 6.09 years is 2,224 effective full-power days, and their 24 months is a calendar
> refuelling interval. Compared consistently in EFPD the ratio is about 3.2; I am quoting 3.05, which is
> the conservative version."

---

# 7 · IF THEY PUSH FURTHER

**"So your fuel utilisation is worse."**
> "Yes, and we say so in the report. Section 8.12.3 records that the lower burnup is the accepted price
> of a safety- and nonproliferation-led once-through cycle, and §8.11 gives the 3-batch option that would
> cut waste intensity from 4.40 to about 2.9 tHM per TWh-electric. We chose thermal margin, no refuelling
> outage, and a simpler soluble-boron-free absorber problem over fuel economy. That is a design trade we
> made deliberately, not an oversight."

**"Then why not just run 3-batch and get better fuel economy?"**
> "Because refuelling reintroduces everything the once-through core removes: a refuelling outage, a
> shuffle scheme, re-optimised burnable absorbers, a new peaking analysis and fresh-assembly handling. In
> a boron-free core the absorber shaping is the hard part, and doing it once for a single loading is much
> more defensible than doing it every reload. The report keeps 3-batch as an extension, explicitly not
> part of the baseline safety, waste or economic case."

**"Is a 6-year cycle even realistic for fuel integrity?"**
> "The constraint is discharge burnup, not calendar time, and ours is low — 29.6 GWd/tHM core-average,
> with no assembly above 42, against a 62 GWd/MTU qualification ceiling. Cladding creep, oxide thickness
> and fission-gas release scale with burnup and fluence, and we are well inside the qualified database on
> all of them. The long cycle is not asking the fuel to do anything unusual."

**"Where does the excess reactivity for six years go?"**
> "Into burnable absorbers, because there is no soluble boron. Gd₂O₃ at 6 wt% handles early-life
> hold-down and Er₂O₃ at 0.75 wt% covers the slower residual, with ring enrichment grading at
> 4.95/4.70/4.40/4.0 wt%. The record depletion shows the mid-cycle hump peaking at k ≈ 1.135 around
> 13.5 GWd/tHM, which stays below the BOC value of ~1.150 — so beginning-of-cycle remains the bounding
> shutdown state. That was the design problem, and it is closed in §8.2."

---

# 8 · REFERENCES

**For the linear reactivity model and the batch formula** — the standard citation:
> Driscoll, M. J., Downar, T. J., & Pilat, E. E. (1990). *The Linear Reactivity Model for Nuclear Fuel
> Management.* American Nuclear Society, La Grange Park, IL.

**For burnup, specific power and cycle-length definitions** — any of:
> Lamarsh, J. R., & Baratta, A. J. *Introduction to Nuclear Engineering* (3rd or 4th ed.), Ch. 4 & 8.
> Stacey, W. M. *Nuclear Reactor Physics* (2nd ed.), Ch. on fuel burnup and in-core fuel management.
> Duderstadt, J. J., & Hamilton, L. J. *Nuclear Reactor Analysis*, Ch. 15.

**For NuScale comparison parameters** — cite a neutral source, not a vendor page:
> IAEA. *Advances in Small Modular Reactor Technology Developments* (ARIS supplement, latest edition) —
> gives thermal power, core configuration, heavy-metal loading and refuelling interval for NuScale,
> CAREM, SMART and others in one comparable format.
> NuScale Power. *Design Certification Application / Final Safety Analysis Report*, Chapter 4 (Reactor),
> as docketed with the U.S. NRC.

**For our own numbers:** FER §8.2 (core and depletion basis), §8.2.3 (once-through rationale), §8.11
(waste basis, 3-batch LRM option), §8.12.3 (fuel economy trade). Underlying calculation: OpenMC 0.15.3,
ENDF/B-VIII.0, STAT_FINAL — 400 batches × 50,000 particles, 80 inactive, ≈16 M active histories,
σ(k) ≈ 22–26 pcm.

**⚠ Verify before quoting NuScale's discharge burnup or heavy-metal loading.** I have used ~40–50
GWd/tHM and ~9.4 tHM as representative values. The argument in §2 above **does not depend on them** —
it uses the questioner's own 1.28× — so if you are unsure, run the §2 version and leave NuScale's
burnup out.

---

# 9 · THE SPOKEN ANSWER (≈ 60 seconds)

> "Let me take your 1.28 as given, because the answer works out from your own number.
>
> Cycle length is burnup-per-cycle divided by specific power — that is a definition, not a model. So
> there are two terms, and specific power is only one of them. Ours: 29,600 megawatt-days per tonne
> divided by 13.31 megawatts per tonne gives 2,224 effective full-power days, which is the 6.09 years in
> our report.
>
> **Your 1.28 accounts for a factor of 1.28. The remaining factor of about 2.4 is burnup per cycle, and
> that comes entirely from fuel management: we are single-batch, once-through. NuScale is multi-batch.**
> In an n-batch core each cycle only spends about one-nth of the fuel's reactivity; we spend all of it at
> once.
>
> And the check on that: **our discharge burnup is 29.6 gigawatt-days per tonne, which is lower than
> theirs, not higher.** We are not claiming better fuel — we are burning it less far, all in one go. Our
> fuel utilisation is genuinely worse, and section 8.12.3 says so.
>
> If you take our identical core and apply the linear reactivity model at five batches, you get a
> twenty-four-month cycle. Same core, same specific power, same 1.28. **The cycle length is a
> fuel-management choice, not a power-density consequence.**
>
> One correction, if I may — the ratio is three, not four. 6.09 years against 24 months is 3.05."

---

# 10 · NUMBERS TO HAVE COLD

| Quantity | Value | Where |
|---|---|---|
| Thermal power | 125 MWth | FER §8.1 |
| Heavy metal | 9.39 tHM | FER §8.2 |
| Specific power | 13.31 MW/tHM | 125 / 9.39 |
| Cycle length | 2,224 EFPD = 6.09 FPY | STAT_FINAL, k = 1 crossing |
| Discharge burnup | 29.6 GWd/tHM core-average | STAT_FINAL |
| Peak assembly burnup | < 42 GWd/tHM | FER §8.11 |
| Qualification ceiling | 62 GWd/MTU | FER §8.3 |
| Batches | 1 (once-through) | FER §8.2.3 |
| 3-batch LRM option | 44.4 GWd/tHM | = 1.5 × 29.6 |
| Enrichment rings | 4.95 / 4.70 / 4.40 / 4.0 wt% | FER §8.2 |
| Extended depletion | 2,510 EFPD → 33.4 GWd/tHM, k = 0.968 | STAT_FINAL |
| Cycle-length ratio vs 24 mo | **3.05×**, = 2.39 (burnup) × 1.28 (specific power) | this document |
