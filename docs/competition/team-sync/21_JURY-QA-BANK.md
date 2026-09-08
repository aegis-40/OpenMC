# Jury Q&A bank

**Written 24 Aug 2026 against the 45-slide deck.** Four to five questions per slide, of the kind a
working nuclear engineer, licensing reviewer or PSA analyst would actually ask — not the easy ones.

**How to use this.** Do not memorise answers. Read the question, decide whether you *know* the answer,
and if you do not, use the honest form: **"We have not analysed that; it is in our open items."** A
jury of practitioners respects that far more than a confident guess, and they will catch a guess.

Answers marked **⚠ WEAK** are places where the honest answer is a limitation. Know them before Tuesday
so you are never surprised by your own design.

---

# ⚠ THREE THINGS TO SETTLE — status as of 25 Aug

## 1 · W-3 below its validated mass-flux range — ✅ **CLOSED by backup slide 48**

The concern was that W-3 is qualified for roughly 1,350–6,800 kg/m²·s while your mass flux is 543, yet
it is presented as the *limiting* result.

**Backup slide 48, "Why 1.33, 2.13 and 6.18 agree", now handles this better than any answer I drafted.**
It states outright that W-3 is **not** valid at G = 542 (mass-flux floor 1356, quality range ±0.15),
labels it BINDING rather than validated, shows Bowring and Groeneveld as the in-range predictors, and
adds a correlation-independent Zuber pool-boiling check — 3.4 MW/m² against a local flux of 0.52 MW/m²,
a factor of 6.5 with zero credit for flow.

**Delivery:** if the question comes, jump to slide 48. Lead with *"W-3 is out of range at our mass flux
and we say so on the slide — it is a penalised bound, not our basis. Groeneveld is the applicable
predictor."* Do **not** defend W-3 as validated.

## 2 · SGTR and ATWS missing from the event matrix — ⚠ **FIX: add two rows**

Both events **are** analysed in the authoritative FER. Only the deck's matrix omits them.

**Steam-generator tube rupture** — FER §8.6.5d, classified DBA:
> RT → SI → isolate affected generator → cogeneration-interface isolation. Safety injection holds
> primary inventory; main-steam and affected-generator isolation stop the release path; the cogeneration
> interface isolates on the tube-rupture signal (§8.8.9). Acceptance: offsite dose ≤ 10 CFR 100.

**ATWS** — FER §8.6, Figure 8.6-3 fault tree, classified DEC-A:
> Negative moderator coefficient throttles power; the power-operated relief valve caps pressure; the
> diverse actuation system detects the ATWS signature; boron injection brings the core cold-subcritical.
> Acceptance: coolable core, RCS pressure within limit (10 CFR 50.62).

**Paste-ready rows** for slide 30, in the matrix's existing four-column format:

| Event (class) | Acceptance criterion | Result | Status |
|---|---|---|---|
| Steam-generator tube rupture (DBA) | Offsite dose ≤ 10 CFR 100 | Injection holds inventory; affected-generator and main-steam isolation; cogeneration interface isolates on the tube-rupture signal | PASS |
| Anticipated transient without scram (DEC-A) | Coolable core; RCS pressure within limit | Negative moderator feedback throttles power; PORV caps pressure; diverse actuation plus boron injection reach cold subcritical [10 CFR 50.62] | PASS |

That takes the matrix from seven rows to nine — **check it still fits** before pasting. If space is
tight, SGTR is the more glaring omission (it is a DBA, and you run a once-through steam generator where
tube duty is harsher than a U-tube unit); ATWS can be carried verbally.

## 3 · "Leaks flow inward" does not apply to Barrier 1 — ⚠ **FIX: reword slide 24**

At the steam generator the primary is at **12.8 MPa outside** the tubes and the secondary at **4.5 MPa
inside**, so a tube leak flows **primary → secondary** — the conventional SGTR direction. The
pressure-gradient argument is true for barriers 2 and 3, not for barrier 1.

**Current text:**
> *"The intermediate loop is held above reactor-side pressure at every interface exchanger, so any tube
> leak flows inward — clean water toward the reactor, never product outward."*

**Replace with:**
> At the steam generator the primary is the high-pressure side, so a tube leak is a conventional
> tube-rupture event — detected on secondary activity, isolated fail-closed, with the cogeneration
> interface isolating on the same signal. Beyond it the intermediate loop is held above the steam side
> at every interface exchanger, forming a clean pressurised buffer: activity cannot migrate outward
> across the remaining barriers.

**Why this is worth doing.** The claim as written is checkable and wrong at one of three barriers.
Stating the exception yourself converts it from a vulnerability into a demonstration that you know your
own pressure topology — and it links straight to the new SGTR row.

**Spoken version:**
> "Three barriers. The first is the steam generator, where the primary is the high-pressure side — so a
> tube leak there is a conventional rupture event, and we treat it as one: activity detection,
> fail-closed isolation, and the cogeneration interface trips on the same signal. Past that point
> pressure does the work for us: the intermediate loop is the clean, pressurised side, so nothing can
> migrate outward toward a customer."

---
---

# BLOCK A — Samira · slides 4–18

## Slide 4 — Project Summary

**Q1. "Is 32 % gross or net of house load?"**
Net. 42.4 MW mechanical → 41.6 MWe gross after the generator → 40.0 MWe net. House load is about 3.8 %,
which is low precisely because there are no reactor coolant pumps to feed.

**Q2. "Six years without refuelling — what about surveillance tests that require shutdown?"**
Most protection-channel surveillance is done online: 2-of-4 voting lets one channel be bypassed for
testing while the plant stays fully protected. The tests that genuinely need a shutdown — in-service
inspection of the OTSG tubes and in-vessel components — are **named in our open items**, and defining
those intervals is exactly the work that remains. **⚠ Do not pretend this is solved.**

**Q3. "The 240-hour grace period — does it credit any operator action?"**
None. No AC power, no seawater, no operator. 240 h is the conservative figure; nominal is about 286 h.
What it does assume is that the 250 m³ pool inventory is present at the start, which is why the pool is
a credited safety system with technical specifications.

**Q4. "What actually happens at hour 241?"**
Make-up to the pool. Ten days is long enough that recovery becomes a logistics problem rather than an
emergency-response one — that is the point of the number rather than the number itself.

## Slide 6 — Literature Review

**Q1. "NUWARD is boron-free in all design-basis conditions. You need boron for cold shutdown. Isn't
theirs the stronger claim?"** — *expect this one.*
On that specific metric, yes. NUWARD is forced-circulation and multi-batch, so it holds less excess
reactivity on rods alone. Our claim is the **combination** — boron-free operation, natural circulation
and a six-year single-batch cycle — and no announced design has all three. We would rather state our
cold-shutdown boron requirement openly than claim a parity we do not have.

**Q2. "CAREM has been under construction for over a decade. Why is your natural circulation more
credible than theirs?"**
We are not claiming it is easier. CAREM's schedule has been driven by programmatic and funding factors
rather than by the circulation physics, and their existence de-risks ours: they are demonstrating
natural circulation at a similar scale. We treat CAREM as the closest precedent, not as a
counter-example.

**Q3. "Have you looked at VBER-300 or KLT-40S?"**
VBER-300 is on slide 18 — it reaches 50 GWd/tHM on a comparable cycle length at similar enrichment,
because it uses soluble boron and is roughly seven times larger, so it also leaks fewer neutrons. It is
the honest counter-example to our burnup figure and we present it as such.

**Q4. "State your novelty in one sentence."**
A soluble-boron-free, natural-circulation integral PWR that holds an entire six-year single-batch cycle
on solid absorbers and rods alone — and sells three products.

## Slide 7 — Method & Feasibility

**Q1. "OpenMC is a research code. Would a regulator accept it for licensing?"** — **⚠ WEAK, answer
honestly.**
Not as it stands. OpenMC has published validation and is widely used in research, but a licensing
submission would need a code with an approved topical report and a formal quality-assurance pedigree.
What we claim is that our physics is verified and reproducible, not that this deck is a licensing
basis.

**Q2. "The −50 pcm ICSBEP bias — how many cases, and what spread?"**
LEU-COMP-THERM-008, whose benchmark eigenvalue is 1.0007 rather than unity. All cases fall within one
standard deviation of the benchmark uncertainty.

**Q3. "Did you do a nuclear-data sensitivity and uncertainty analysis?"** — **⚠ WEAK.**
No formal S/U analysis. We quantified statistical uncertainty (22–26 pcm on k) and benchmarked against
measured criticals, but we did not propagate cross-section covariances. That is a genuine limitation.

**Q4. "How did you establish mesh independence in the CFD?"**
ASME V&V-20 grid-convergence procedure, with the CHF result cross-checked against two independent
correlations rather than relying on the mesh study alone.

## Slide 9 — Design Philosophy

**Q1. "In-vessel CRDMs eliminate ejection but introduce their own failures. What about a stuck rod, or a
dropped rod?"**
Both are retained, not eliminated. A **stuck rod is assumed** in every shutdown-margin calculation —
that is where the 785 ppm cold boron requirement comes from. A dropped rod is an anticipated
operational occurrence covered by the flux-rate trip and the power-distribution limits.

**Q2. "How do you maintain an in-vessel drive over 60 years?"** — **⚠ WEAK.**
Access is at head removal, which for us means once every six years. Demonstrating that a drive can run
six years untouched, and defining the inspection scope when the head does come off, is in our open
items.

**Q3. "If large-break LOCA is eliminated, what is your largest break?"**
A small nozzle break. The integral vessel caps the break size **by construction** — there is no
large-bore primary pipe to break, so the limiting break area is set by the largest penetration.

**Q4. "You eliminated boron dilution but installed a boron system. Could it inject spuriously?"**
It could, and the consequence is benign: EBIS adds *negative* reactivity. The eliminated hazard is
dilution — unintended *removal* of boron — which cannot occur because the normal coolant contains none.

## Slide 11 — Plant Design Parameters

**Q1. "14.1 MPa design against 12.8 operating is only a 10 % margin. Is that enough for pressuriser
transients?"**
It is the conventional PWR ratio, and our transients are milder than a large plant's: no pump coastdown,
low stored energy, and a large pressuriser volume relative to core power. The overpressure case is a
detailed-design confirmation item.

**Q2. "A 0.5 km emergency planning zone — on what basis?"**
It is a **design goal** substantiated by reference to comparable passive iPWR submissions. The
plant-specific dose and meteorology case that would confirm it is on our open-items slide. We state it
as a goal deliberately.

**Q3. "Core-damage frequency below 10⁻⁷ — internal events only?"**
Yes, and the slide says so. External hazards, seismic in particular, are screened by reference pending
the site-specific PSA.

**Q4. "Capacity factor 95 % on this slide, 90 % in the economics. Which is it?"**
95 % is the design target; 90 % is used in the economics as the conservative case. The note on the slide
says so, and using the lower figure means the LCOE is not flattered.

## Slide 12 — Reactor Vessel

**Q1. "What is your RT_NDT and its shift over 60 years?"** — **⚠ WEAK.**
We computed the fluence — 3.02 × 10¹⁸ n/cm², a factor of 3.3 below the 10¹⁹ screening threshold — but we
did not compute an RT_NDT shift or a pressurised-thermal-shock case. That requires the copper and
nickel content of the actual heat and belongs to detailed design.

**Q2. "How do you inspect OTSG tubes on a six-year interval?"** — **⚠ WEAK, and expect it.**
Access is at head removal. Defining the in-service inspection intervals and demonstrating in-vessel
maintainability across a six-year cycle is on our open-items slide. It is the single most practical
consequence of the long cycle.

**Q3. "Is a 3,047 mm forging with a 160 mm wall manufacturable?"**
Comfortably — it is well below large-PWR forging sizes, and that is one of the modularity arguments:
the vessel is within the capability of more suppliers, not fewer.

**Q4. "Your three stress numbers — which pressure case is each?"**
142 MPa is the Lamé hoop stress at the inner surface at **design** pressure; 135 MPa is von Mises at the
same point and pressure; 123 MPa is the thin-wall membrane value at **operating** pressure. Against
Sₘ ≈ 184 MPa that is a margin of about 1.3–1.4.

## Slide 13 — Core Configuration

**Q1. "36 absorber rods out of 264 positions — what does that do to local peaking?"**
The gadolinia is ring-graded across the assembly precisely to manage it, and the resulting F_ΔH stays
within the 1.75 operating-limits envelope at every state we evaluated.

**Q2. "Erbium leaves a residual penalty at end of cycle. Why accept it?"**
That is the trade. Erbia burns slowly by design — it is there to trim reactivity late in a very long
cycle, which gadolinia cannot do because it is gone by mid-life. The residual absorption is the price
of a flat reactivity trace over six years.

**Q3. "4.95 wt % is the LEU ceiling. You have no headroom for a longer cycle."**
Correct, and that is deliberate: staying under 5 % keeps us inside the commercial fuel-fabrication
envelope. A longer cycle would require above-5 % enrichment, which changes the fuel supply chain and
the licensing basis entirely.

**Q4. "Why a standard 17×17 lattice rather than an optimised one?"**
Because fuel integrity is then substantiated by the licensed envelope rather than by new qualification.
The design's risk is integration, not fuel.

## Slide 14 — Cycle Results

**Q1. "Is the moderator coefficient quoted at hot zero power? That is the limiting condition."**
The coefficients are from the full-power production run. Confirming MTC at hot zero power, which is
where a boron-free core is most likely to be least negative, is a state point we report separately.
**⚠ If you cannot confirm this, say so.**

**Q2. "F_q of 2.435 at mid-cycle is high. Is your envelope built around it?"**
Yes — the operating-limits envelope of F_q ≤ 2.4675 is set at the **mid-cycle limiting state**, not at
beginning of cycle, and the thermal margins are closed there rather than at the easier condition.

**Q3. "k = 0.9910 at 30.8 GWd/t means you have gone past criticality. What is the actual cycle end?"**
29.6 GWd/tHM, which is 2,224 effective full-power days. The 30.8 point is the last depletion step, past
end of cycle — the label on that row should read 'final step' rather than EOC.

**Q4. "22–26 pcm statistical uncertainty against a Doppler coefficient of −1.91 pcm/K — how do you
resolve that?"**
By differencing states from the same run, where correlated components cancel, and by taking the
coefficient over a wide enough temperature interval that the reactivity difference is many times the
statistical noise.

## Slide 15 — Fuel & Material Design

**Q1. "Did you run a qualified fuel-performance code?"** — **⚠ WEAK, and it is on the open-items slide.**
No. These are screening checks against licensed-envelope limits. Fuel-performance confirmation in a
qualified code is named as remaining work.

**Q2. "Fission-gas release and rod internal pressure at 42 GWd/t?"**
Qualitatively low, because linear heat rate is low throughout the cycle — fission-gas release is
strongly temperature-driven and our centreline peaks at 828 °C. We have not computed the end-of-life rod
pressure, which is part of the same open item.

**Q3. "Is there operating data for Er₂O₃ in Zircaloy-clad fuel?"**
Erbia is used commercially, most extensively in BWR fuel and in some long-cycle PWR designs. We checked
absorber compatibility for both gadolinia and erbia; the qualification base is smaller than for
gadolinia and we do not overstate it.

**Q4. "Cladding at 353 °C — is corrosion and hydrogen pickup an issue over six years?"**
353 °C is a low peak cladding temperature and the duty is base-load, so corrosion and hydriding are far
from limiting. The long residence time is a real question, and it is bounded by the 42 GWd/t discharge
against a 62 GWd/t qualification ceiling.

## Slide 16 — Radiation Shielding

**Q1. "Monte Carlo or point-kernel? What variance reduction did you use?"**
Monte Carlo for the transport result, with a point-kernel cross-check. Deep-penetration problems need
variance reduction to converge, and the statistical quality of the result is reported with it.

**Q2. "Borated polyethylene has a service-temperature limit around 80–100 °C. What is the temperature at
your inner shield face?"** — **⚠ sharp question, know it.**
The polyethylene sits outboard of the vessel and the reactor cavity, not against it. Confirming the
temperature at the inner face of the polyethylene layer, and the concrete dehydration temperature behind
it, is a detailed-design item — both materials have real temperature limits and the layer order matters.

**Q3. "Is your fluence quoted at the inner surface or at quarter-thickness?"**
Fluence is reported at the vessel inner surface, which is the conservative location for embrittlement
assessment.

**Q4. "Why two dose numbers?"**
Because the removal cross-section for heavy concrete has genuine spread in the literature, depending on
aggregate. 0.23 µSv/h is the best estimate and 5.5 µSv/h the pessimistic end. Both pass the 10 µSv/h
target, so the conclusion does not depend on which value you believe — which is why we show both.

## Slide 17 — Waste Management

**Q1. "Which decay-heat standard, and with what uncertainty?"**
ANSI/ANS-5.1. The 7.95 MW at shutdown is on the whole-inventory basis. Applying the standard's
uncertainty allowance is what a licensing calculation would add.

**Q2. "Six assemblies a year — what is the pool capacity in years, and when do casks start?"**
The arisings are very low, so a single compact pool plus a small cask pad covers the plant lifetime.
Fuel moves to dry storage once decay heat and dose criteria are met — casks are passively air-cooled, so
the threshold is a heat limit, not a schedule.

**Q3. "Your waste intensity beats CAREM. How does it compare with a modern PWR at 50 GWd/t?"** —
**answer honestly.**
Worse. A 50 GWd/t three-batch PWR at 34 % efficiency is around 2.4 tHM/TWhe against our 4.40. We beat
CAREM because of efficiency, not burnup, and we do not claim to beat the large fleet.

**Q4. "Is spent fuel from a six-year single-batch core harder to handle?"**
The whole core comes out at once, which is a logistics question rather than a safety one — 37
assemblies at a single outage instead of a third of a core every 18 months. Pool and handling capacity
are sized for it.

## Slide 18 — Fuel Cycle Strategy

**Q1. "78.1 kg of plutonium is roughly ten IAEA significant quantities. What is your safeguards
approach?"** — *expect this from anyone with a safeguards background.*
Correct on the quantity, and it is why we address it directly. The material is reactor-grade at 61.6 %
Pu-239 with 21.6 % Pu-240, it is never separated because the cycle is once-through, and it sits inside
intensely radioactive spent fuel. The sealed six-year core means there are no fuel movements to
account for between refuellings — one seal, one camera.

**Q2. "9,860 SWU per year — where does enrichment come from?"**
It is an imported service. Uzbekistan has uranium resources but no enrichment capacity, so the front end
is a commercial supply question, not a domestic one. We do not claim otherwise.

**Q3. "Why is the three-batch option not the baseline if it is better on waste and fuel cost?"**
Because it costs the thing the whole design is built around: a single-batch six-year cycle means zero
refuelling outages and no fuel shuffling, which is where the availability and the safeguards argument
come from. We report the option and its numbers rather than hiding it.

**Q4. "You claim higher burnup than CAREM on a cycle five times longer. Is that a fair comparison?"**
It is the fairest one available — CAREM is the other boron-free, natural-circulation design at
comparable scale. Against the larger soluble-boron designs our burnup is plainly lower, and slide 18
says so.

---

# BLOCK B — Alisher · slides 19–22

## Slide 19 — Cooling Circuit

**Q1. "Did you check natural-circulation flow stability — density-wave or flow-excursion
instability?"** — **⚠ the most serious question in this block.**
Natural-circulation systems at low pressure drop can oscillate, and this is a known issue for
natural-circulation SMRs. Our loop is subcooled throughout with no boiling in the riser, which removes
the density-wave mechanism at power. Confirming stability across the startup transient, where the system
passes through low-flow low-power conditions, requires a system code and is in our open items.

**Q2. "Is W-3 valid at 543 kg/m²·s?"** → **jump to backup slide 48**, which states it is not and
shows why the conclusion survives anyway. Lead with Groeneveld.

**Q3. "What is the flow at hot standby, on decay heat alone?"**
Circulation continues — buoyancy scales with the heat being removed, so the loop self-regulates down
rather than stopping. That is the same mechanism the passive residual-heat-removal trains rely on.

**Q4. "Did you sweep riser height, or pick 4 m?"**
It was swept — the riser-height sensitivity is the figure on this slide. Four metres is where the
driving head is sufficient without making the vessel unreasonably tall.

## Slide 20 — Thermal Margins

**Q1. "Deterministic limit, or a statistical DNBR analysis?"**
We apply the 95/95 correlation limit deterministically. A full statistical DNBR methodology, propagating
plant and manufacturing uncertainties, is a licensing-level analysis we did not perform.

**Q2. "Which anticipated event gives MDNBR 1.57?"**
The bounding AOO corner of the operating envelope rather than a single named transient — we evaluate the
envelope corner rather than a specific event sequence.

**Q3. "Does your CFD resolve grid-spacer mixing?"** — **⚠ WEAK.**
No. The conjugate model resolves the hot channel without spacer-grid detail, which means we do not
credit spacer-enhanced mixing — conservative for DNBR, but it also means we cannot claim the benefit
real hardware would give.

**Q4. "Why is Groeneveld so much higher — 6.18 against 1.33?"**
Because the lookup table is built from a much broader experimental database including low mass flux,
where W-3 is extrapolated. The spread is itself informative: it tells you W-3 is being applied outside
the conditions it was fitted to.

## Slide 21 — Energy Conversion & Cogeneration

**Q1. "Your exhaust quality is 0.872 at IP and 0.892 at LP. That is a wet machine — what about blade
erosion?"**
There is no reheat, so moisture is inherent to a saturated-steam cycle. It is managed in three ways:
separation at 0.15 MPa, exhaust quality held above 0.89 at the last stage, and hardened leading edges
with interstage drainage — which is standard practice on every PWR secondary in operation.

**Q2. "TCES at 200 MWh thermal — what charge and discharge power, over what duration?"**
The store is fed from a ~1 MPa, 180 °C extraction, and the plant-level balance closes at about 0.78
round-trip efficiency, cross-checked against a first-principles adsorption calculation to within 3 %.
Charge and discharge rates are set by the district-heat duty rather than by the store.

**Q3. "An 8 MWe electrolyser on a 40 MWe unit is 20 % of output. What does that do to grid stability?"**
It runs off-peak by design, so it is a dispatchable load rather than a disturbance — and it is
non-safety, so it can be shed instantly with no consequence to the reactor. In practice it makes the
plant *better* for the grid, not worse: it is a controllable sink.

**Q4. "Zeolite degrades with cycling. What is the assumed life?"**
Zeolite-13X is a mature industrial adsorbent with well-documented cycling behaviour, but sixty years of
daily cycling is beyond typical industrial service and store replacement should be treated as a
consumable rather than a lifetime component. We have not assumed it lasts the plant life.

**Q5. "Why zeolite rather than an ammine store?"**
An ammine store was quantified and is roughly twice as compact by volume. It was rejected for the
reference design **on ammonia hazard grounds** — introducing a large ammonia inventory next to a nuclear
island is not a trade we were willing to make.

## Slide 22 — Cogeneration Isolation

**Q1. "At the steam generator the primary is at 12.8 MPa and the secondary at 4.5. Your leak does not
flow inward there."** → once slide 24 is reworded this is answered on the slide. Until then, concede
precisely: barrier 1 is a conventional rupture path handled by detection and isolation; the pressure
argument covers barriers 2 and 3.

**Q2. "Once-through steam generators have harder tube duty than U-tube units. What is your SGTR
analysis?"** — **⚠ and note SGTR is missing from the event matrix.**
The isolation signal is on slide 22 and the barrier chain is designed for it. Where the SGTR case is
quantitatively closed should be stated — if it is not in the event matrix, say that it is treated as a
detailed-design confirmation rather than implying an analysis that is not shown.

**Q3. "Tritium getter — what technology and what capacity?"**
Permeation barriers at the 800 °C interface plus a getter in the loop, with continuous monitoring.
Sizing the getter is a detailed-design item; the architectural point is that tritium is treated as its
own pathway rather than assumed to be caught by the three-barrier chain.

**Q4. "You extract at 180 °C and deliver district heat at 90 °C. Why the large drop?"**
Because the store sits between them. The extraction charges the thermochemical store, and the store
serves a conventional 90/45 °C network. The temperature drop is what buys the decoupling between when
heat is produced and when it is used.

---

# BLOCK C — Azamkhon · slides 24–33

## Slide 24 — Safety Criteria & Plant States

**Q1. "SSR-2/1 Req. 46 needs two diverse systems. Rods and boron injection are both armed by the diverse
actuation system — are they genuinely diverse?"**
The two systems are diverse in mechanism — mechanical gravity insertion versus chemical injection — and
the rods can be actuated by either the protection system or the diverse actuation system. A
common-cause failure of the actuation logic is the residual concern, which is why the rods are
de-energize-to-drop: cutting power to the DAS drops the rods rather than disabling them.

**Q2. "10 CFR 100 or the modern 10 CFR 50.34 dose criteria?"**
The slide cites 10 CFR 100. Which dose basis is applied matters for the source-term calculation, and the
plant-specific dose case is on our open items.

**Q3. "F_q ≤ 2.4675 is oddly precise for an operating limit. Where does it come from?"**
It is the design-specific envelope value derived from the record axial shape at the mid-cycle limiting
state, not a rounded standard number — which is why it carries four decimals.

**Q4. "A 1 % hot shutdown margin criterion is low; many PWRs use more. Why?"**
It is the minimum acceptance value; what matters is that we deliver 7.85 %, nearly eight times it. If
the jury's reference standard requires more, our margin covers it comfortably.

## Slide 25 — Site Hazards

**Q1. "What return period does your 0.3 g correspond to?"** — **⚠ WEAK.**
0.3 g is adopted as a design envelope, not derived from a site-specific probabilistic seismic hazard
assessment. That assessment is on our open items.

**Q2. "The Black Sea has a documented tsunami history. What runup did you assume?"**
We treat the potential as low but non-zero and place safety structures on dry-site grade above the
design-basis flood level, which combines still-water level, storm surge and wave runup. The specific
elevation is a site-layout input.

**Q3. "39 °C condensing assumes 25 °C seawater. What about extreme summers, or climate trend?"**
It is the summer design point and it sets our rated output; winter operation gives more. A hotter summer
reduces electrical output — it is a *performance* sensitivity, not a safety one, because the sea has no
safety role.

**Q4. "How long can you operate with the intake fully blocked?"**
Indefinitely from a safety standpoint, and not at all from a generation standpoint. Blockage removes the
condenser, so you lose power conversion; core cooling transfers to the in-containment pool, which is
independent of the sea.

## Slide 26 — Defence in Depth

**Q1. "Levels 3 and 4 both rely on the same 250 m³ pool. Is that genuinely independent?"** — **⚠ sharp,
and fair.**
They share the heat sink, which is a real coupling. The independence is in the *actuation and delivery*
paths rather than in the sink itself. A jury may reasonably press on this, and the honest answer is that
pool inventory is a common element protected by making it a credited system with technical
specifications rather than by duplication.

**Q2. "21 channels — how many are functionally diverse rather than merely redundant?"**
Four divisions of redundancy with composite overtemperature and overpower functions gives diversity in
the *trip parameter*, not only in channel count. Fourteen of the 21 are Class 1E.

**Q3. "What is the difference in assumptions between 240 h and 286 h?"**
286 h is the nominal calculation; 240 h applies conservative margins on pool inventory, initial
conditions and decay heat. We quote the conservative one.

**Q4. "Has any regulator accepted an EPZ at the site boundary?"**
Several passive SMR designs have proposed it and the concept is under active regulatory consideration
internationally. None is licensed and operating on that basis, which is why we call it a goal.

## Slide 27 — Passive Safety Systems

**Q1. "Two 100 % trains — what is the common-cause failure between them?"**
They are identical in design, so common-cause is a genuine contributor and is treated inside the
initiator groups in the PSA. The mitigating argument is that each train is passive with very few active
components, so the population of things that can commonly fail is small.

**Q2. "Gravity injection needs depressurization first. What if depressurization fails?"**
Staged depressurization is itself redundant and de-energize-to-actuate. Failure of depressurization is
one of the sequences that must be quantified in the event trees, and it is one reason no single failure
reaches core damage.

**Q3. "Is 0.139 MPa the blowdown peak or the long-term pressure?"**
It is the quasi-static peak after full-inventory blowdown. The long-term behaviour, as the pool heats
and boils, is exactly what the qualified time-dependent containment transient in our open items would
establish.

**Q4. "Did you include non-condensables — nitrogen from the accumulators, and hydrogen?"** —
**⚠ WEAK, and it is on the open-items slide.**
No. Non-condensables raise containment pressure because they do not condense in the pool, and hydrogen
management is named as remaining work. Our present number is a mass-and-energy screen, not a qualified
transient.

**Q5. "Why does the counterfactual matter?"**
Because it shows the pool is load-bearing rather than a comfort margin — 0.98 MPa without it against a
0.414 MPa design pressure. We computed what happens without our own safety system.

## Slide 28 — Design-Basis Event Matrix

**Q1. "Where is steam-generator tube rupture? Where is ATWS?"** → both are analysed in FER §8.6.5d and
§8.6 respectively. Add the two rows (warning 2 above); until then, say where each is closed rather than
implying the matrix is complete.

**Q2. "Row one gives a thermal criterion and a reactivity result."**
The criterion column should read 'insertion rate within the analysed envelope'. The thermal criterion is
closed on the thermal-margins slide at MDNBR 1.33.

**Q3. "'Peak clad ≪ 1204 °C' — what is the number?"**
We report it as far below the limit rather than as a specific peak because the SBLOCA case is a bounding
screen, not a qualified transient calculation. **If you do have the number, use it; if not, say this.**

**Q4. "Spent-fuel-pool k of 0.892 — fresh fuel or credited burnup?"**
With burnup credit, plus flux-trap racks and 2,000 ppm. Burnup credit requires verifying each assembly's
burnup before placement, which is a procedural commitment as well as an analytical one.

## Slide 29 — Core-Damage Frequency

**Q1. "Where is seismic?"** → the answer is in your speaker notes. Name it as an open item; never
improvise a number.

**Q2. "Which nine initiator groups?"**
Be able to list them. If you cannot, say the roll-up is documented in the digital appendix rather than
inventing categories on the spot.

**Q3. "What are your uncertainty bounds — mean, median, 95th percentile?"** — **⚠ WEAK.**
We report a point estimate. A full PSA would carry an uncertainty distribution, and we do not.

**Q4. "What human-error probability model did you use?"**
Human error is a small contributor because very little operator action is credited — the design is
de-energize-to-actuate with a ten-day grace period. We did not apply a formal HRA method.

## Slide 30 — Shutdown Architecture

**Q1. "How did you compute β_eff — IFP, or the prompt-k approximation?"**
The prompt-k method: two runs, one with delayed neutrons suppressed. OpenMC 0.15.3 exposes no
iterated-fission-probability tally scores, so IFP was not available. The result is 704.5 ± 28 pcm, about
8 % above the 650 pcm literature default — we used our own value rather than the default.

**Q2. "3,000 ppm on gravity head and nitrogen — what is the injection time?"**
Injection rate and the time to reach the required concentration are what determine whether the system
outruns the cooldown transient. This is a sizing calculation that belongs to detailed design; the
architectural claim is that the driving force is stored, not powered.

**Q3. "Boric acid solubility at cold shutdown temperature — will 3,000 ppm precipitate?"** — *good
question, and the answer is comfortable.*
No. Boric acid solubility at 20 °C corresponds to well above 8,000 ppm boron, so 3,000 ppm is far from
saturation even at the coldest state.

**Q4. "Did you check all 16 rods for the stuck-rod case, or assume one?"**
The most reactive cluster is the stuck-rod assumption, identified from the individual worths rather than
assumed by position.

**Q5. "The system is dormant for six years. How do you test it?"**
Surveillance of a dormant passive system is exactly the kind of technical-specification question the
long cycle makes harder, and it belongs with the in-service inspection open item. Pressure, level and
concentration are monitorable continuously; actuation testing is the difficult part.

## Slide 31 — Advisory Digital Twin

**Q1. "Validated against what?"**
Parity against the analysis models, documented in the digital appendix. It is not validated against
plant data, because there is no plant.

**Q2. "If it is credited for nothing, what is it for?"**
Trend monitoring, early anomaly detection and operator training. Its value is that it changes nothing
about the safety case — that is what makes it deployable rather than a licensing burden.

**Q3. "A diode is one-way. How do you update the model?"**
Model updates are an offline, administratively controlled action, not a live write-back. That is the
point: there is no automated path in.

**Q4. "What is its cyber classification?"**
Non-safety, outside the Class 1E boundary, with 10 CFR 73.54 as the framework. The architectural
argument is that the protection system has no inbound digital path at all.

## Slide 32 — Auxiliary Systems

**Q1. "Why two diesels for a plant that claims not to need AC?"**
For investment protection and for monitoring loads, not for safety. Losing both is a design-extension
condition the plant survives passively — which is why station blackout appears on the event matrix at
10⁻¹¹ per reactor-year.

**Q2. "IEEE 323 at 150 °C — your containment peak is 0.139 MPa, around 110 °C. Why qualify higher?"**
Because the qualification envelope should bound the accident condition with margin, and because the
long-term containment transient is not yet qualified. Qualifying to a wider envelope is the
conservative choice.

**Q3. "A fire in the main control room — do you have a remote shutdown station?"**
Three-hour division barriers preserve at least one safety division, and the plant's safe state is
reached by de-energization. A dedicated remote shutdown capability is a detailed-design item.

**Q4. "Ten significant quantities of plutonium under one seal for six years — would the IAEA accept
that?"**
Containment-and-surveillance regimes with sealed cores are established practice, and a core with no
fuel movements is easier to verify continuously than one that is shuffled. The approach would be agreed
with the IAEA in the design phase.

## Slide 33 — Facility Layout

**Q1. "31,600 m² is driven by hydrogen stand-off. Could you not move the hydrogen plant?"**
Yes, and that is the point of quoting it — the footprint is set by an offsite-consequence separation
distance for a non-nuclear facility, not by the nuclear island. Relocating hydrogen production shrinks
the site substantially.

**Q2. "Five to ten units sharing intake, discharge and switchyard — is that not a common-cause risk?"**
For power conversion, yes, and that is accepted because none of those services is safety-related. Each
unit's safety heat sink is its own in-containment pool.

**Q3. "The reactor building is below grade — what about groundwater and flotation?"**
Below-grade placement lowers the centre of gravity for seismic and provides shielding. Groundwater
control and buoyancy are civil design items.

**Q4. "Where is the spent-fuel building in the arrangement?"**
Within the nuclear island, inside the protected area. Arisings are very low, so the pool and cask pad
are small relative to a conventional plant.

---

# BLOCK D — Samira · slides 34–38

## Slide 34 — Economic Evaluation

**Q1. "Nobody has built a 40 MWe unit at $3,500/kWe. Why should we believe the NOAK case?"** — *expect
this, and never claim it is cheap.*
You should not believe it as a promise — it is a nth-of-a-kind assumption, and our own sensitivity shows
overnight capital swings the answer by $50/MWh, more than every other parameter combined. That is why we
present a range and put the high-capital case on the same slide. It is also exactly what happened to
NuScale: their physics did not change, their capital estimate did.

**Q2. "Your own bottom-up scaling gives $8,250/kWe, above your headline. Does that not undercut you?"**
It is in the FER and on the slide as the upper band, deliberately. The honest statement is that
competitiveness is a bet on modular production driving cost below the scaling curve, and we say so
rather than presenting only the favourable end.

**Q3. "90 % capacity factor for a plant with a six-year outage — how long is that outage?"**
Whole-core discharge at one outage rather than partial refuelling every 18 months. Planned unavailability
is set by maintenance and balance-of-plant work, not by fuel shuffling, and the six-year interval means
far fewer outages over the life.

**Q4. "Who buys 120 tonnes of hydrogen a year at Sinop?"** — **⚠ WEAK.**
There is no identified offtaker. The hydrogen case rests on a market that would need to develop, and
independent validation of cogeneration revenue is on our open-items slide.

**Q5. "Decommissioning at $700/kWe — on what basis?"**
A literature parameter rather than a bottom-up estimate. At about $6/MWh it is roughly 8 % of the LCOE,
so the answer is not sensitive to it.

## Slide 35 — Reference Comparison

**Q1. "You compare against licensed and under-construction designs. Is a paper design a fair
comparator?"**
No, and that asymmetry runs against us, not for us — they have design certification and construction
experience we do not. We compare on design attributes, not on maturity.

**Q2. "MWth per assembly is an unusual metric. What is your power density in kW per litre?"**
It is a proxy chosen because assembly counts are published for every design in the booklet, whereas core
volumes often are not. Core power density is the more standard measure and follows from the 13.31 W/gHM
specific power.

**Q3. "Load following with thermal storage — what ramp rate can you actually offer?"**
Storage shifts *thermal* output without moving reactor power, so the ramp is set by the store and the
turbine rather than by the core. Quantifying the deliverable ramp is a plant-control study we have not
performed.

**Q4. "Revenue stacking assumes a district-heat customer exists at Sinop."**
Correct — it assumes a network and an offtaker. That is a siting and commercial precondition, and it is
part of what independent validation of the revenue case would establish.

## Slide 36 — Verification & Validation

**Q1. "Has any of this been independently reviewed outside the team?"** — answer honestly.
Not by an external body. Our internal control is that each domain has an independent cross-check by a
different method, and that every table traces to a controlled record.

**Q2. "Could a third party reproduce your results from the appendix?"**
That is the intent — input decks, run settings and outputs are indexed, with checksums. It is the claim
we are most confident in.

**Q3. "Which BEAVRS cycle and which metrics?"**
Be specific if you know; if not, say the benchmark configuration is documented in the appendix rather
than guessing a cycle number.

**Q4. "You have no system code. How do you close transients?"** — **⚠ WEAK, and it is on slide 37.**
We do not. Transients are closed by bounding screens and by reference to precedent. An integrated
system-code package across the limiting events is named as remaining work.

## Slide 37 — Design Summary & Open Items

**Q1. "Which open item worries you most?"**
The integrated system-code analysis, because it is the one that could move a number rather than merely
confirm one — particularly the time-dependent containment transient with non-condensables.

**Q2. "How far is this from a licensable design?"**
Years, and the gap is analysis and qualification rather than concept. Everything in the design uses
proven light-water technology; what is missing is the qualified codes, the site-specific cases and the
component qualification.

**Q3. "What would you change if you started again?"**
A genuine answer is worth more than a polished one. A defensible version: fixing the operating-limits
envelope earlier, because peaking propagated into thermal margins, shielding and fuel performance and
had to be reconciled late.

**Q4. "What is the single biggest risk to this design?"**
Capital cost at 40 MWe. Not the physics — the physics is conventional. Whether a unit this small can be
built serially at nth-of-a-kind cost is the question the whole economic case rests on.

---

# The five hardest questions in the whole deck

Rehearse these until they are automatic.

1. **"Is W-3 valid at your mass flux?"** → lead with Groeneveld, concede W-3 is a bound.
2. **"Why does a boron-free reactor carry a boron system?"** → 785 ppm against 3,000 credited.
3. **"Nobody has built 40 MWe at $3,500/kWe."** → name the condition, never claim it is cheap.
4. **"Where is seismic in your core-damage frequency?"** → name it as an open item.
5. **"Your report says 15,672 pcm."** → the 16-CRA upgrade line.

# When you do not know

> **"We have not analysed that. It is in our open items, and I would rather tell you that than
> speculate."**

Then stop. Do not fill the silence. A jury of practitioners will mark that higher than a confident
answer they can dismantle in two follow-ups.
