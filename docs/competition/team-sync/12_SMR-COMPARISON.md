# Aegis-40 vs the SMR Field

**Source for all competitor data:** IAEA, *Advances in Small Modular Reactor Technology Developments*, 2022 Edition (ARIS supplement). Every competitor number below is taken from that booklet's "Major Technical Parameters" datasheets — not from memory.
**Source for Aegis-40:** our frozen basis (3 July production run + FER).

> **Read this before quoting anything.** The IAEA booklet is vendor-supplied data reproduced without independent review. It publishes **no economics** — no LCOE, no capital cost — so the economics section below is honest about what cannot be compared.

---

## 1. Master comparison

| | **Aegis-40** | CAREM-25 | ACP100 | SMART | NuScale VOYGR | NUWARD | SMR-160 | BWRX-300 | Rolls-Royce SMR |
|---|---|---|---|---|---|---|---|---|---|
| Country | Türkiye *(student)* | Argentina | China | Korea / Saudi | USA | France | USA | USA / Japan | UK |
| Type | Integral PWR | Integral PWR | Integral PWR | Integral PWR | Integral PWR | Integral PWR | PWR | BWR | 3-loop PWR |
| **MWth / MWe** | **125 / 40** | 100 / ~30 | 385 / 125 | 365 / 107 | 250 / 77 *(gross, per module)* | 2×540 / 2×170 | 525 / 174 g, 160 net | 870 / 270–290 | 1358 / 470 |
| **Circulation** | **Natural** | **Natural** | Forced | Forced | **Natural** | Forced | **Natural** | **Natural** | Forced |
| Pressure, pri/sec (MPa) | 12.8 / 4.5 | 12.25 / 4.7 | 15 / 4.6 | 15 / 5.8 | 13.8 / 4.3 | 15 / 4.5 | 15.5 / 3.4 | 7.2 direct cycle | 15.5 / 7.8 |
| Core in/out (°C) | 258 / 308 | 284 / 326 | 286.5 / 319.5 | 296 / 322 | 249 / 316 | 280 / 307 | 243 / 321 | 270 / 288 | 295 / 325 |
| Fuel / array | UO₂ 17×17 | UO₂ hexagonal | UO₂ 17×17 | UO₂ 17×17 | UO₂ 17×17 | UO₂ 17×17 | UO₂ square | UO₂ 10×10 | UO₂ 17×17 |
| **Assemblies** | **37** | 61 | 57 | 57 | **37** | 76 | 57 | 240 | 121 |
| Enrichment (%) | 4.95 max / 4.43 avg | 3.1 | < 4.95 | < 5 | ≤ 4.95 | < 5 | 4.0 avg | 3.81 avg / 4.95 max | < 4.95 |
| **Burnup (GWd/t)** | **29.6** | 24 | < 52 | < 54 | ≥ 45 | — | 45 | 49.6 | 50–60 |
| **Refuelling cycle** | **73 mo (6.09 y), single batch** | 14 mo, 50 % core | 24 mo | 30 mo | 18 mo | 24 mo, half core | 24 mo | 12–24 mo | 18 mo |
| **Reactivity control** | **CRDM + Gd/Er, no soluble boron** | **CRDM only** | CRDM + Gd₂O₃ + boron | CRDM + boron | CRD + boron | **CRDM + solid BP, boron-free in all DBC** | rods + boron | rods + solid BA | control rods |
| Safety approach | Passive | Passive | Passive | Passive | Passive | Passive | Fully passive | Fully passive | Passive + active |
| Design life (y) | 60 | 40 | 60 | 60 | 60 | 60 | **80** | 60 | 60 |
| Plant footprint (m²) | **~31 600** *(3.2 ha, est.)* | 36 000 | 200 000 | 90 000 | 140 000 *(12-module)* | 3 500 *(NI only)* | 28 000 | **9 800** | 40 000 |
| RPV h / d (m) | ~11 / 3.05 | 11 / 3.2 | 10 / 3.35 | 18.5 / 6.5 | 17.7 / 2.7 | 15 / 5 | 15 / 3 | 26 / 4 | 7.9 / 4.2 |
| RPV weight (t) | **~270** *(est., w/ internals)* | 267 | 300 | 1070 | TBC | 310 | 295 | 485 | 150 |
| Seismic SSE | 0.3 g | 0.25 g | 0.3 g | > 0.3 g | **0.5 g** | 0.3 g | **0.5 g** | 0.3 g | > 0.3 g |
| Cogeneration | **Heat + hydrogen** | Desalination | Heating, steam, desal | Desalination + process heat | — | Flexible operation | Optional | — | — |
| Status | Student detailed design | **Under construction** | **Construction in progress** | Detailed design | Equipment manufacturing | Conceptual | PSAR 2023 | Detailed design | Detailed design |

---

## 2. The single most useful comparison: Aegis-40 vs NuScale

**We and NuScale have geometrically almost the same core** — 37 assemblies, 17×17 lattice, ~2 m active height.

| | NuScale NPM | Aegis-40 |
|---|---|---|
| Assemblies | 37 × 17×17 | 37 × 17×17 |
| Thermal power | 250 MWth | **125 MWth** |
| Burnup | ≥ 45 GWd/t | **29.6 GWd/t** |
| Reactivity control | rods + soluble boron | **rods + Gd/Er, no boron** |
| Refuelling | 18 months | **73 months** |

**We run the same core at exactly half the power.** That one sentence explains the entire design: half the power density is where the thermal margin comes from, and it's what makes a boron-free six-year cycle possible — but it's also why our burnup is a third lower and why we produce 40 MWe from a core NuScale gets 77 from.

If a juror asks "why is your power so low for that core size?", this is the answer, and it's a *choice*, not a limitation.

### Power density across the field

Thermal power per fuel assembly — a clean proxy:

| Design | MWth/FA |
|---|---|
| CAREM-25 | 1.64 |
| **Aegis-40** | **3.38** |
| BWRX-300 | 3.62 |
| SMART | 6.40 |
| ACP100 | 6.75 |
| NuScale | 6.76 |
| NUWARD | 7.11 |
| SMR-160 | 9.21 |
| Rolls-Royce SMR | 11.22 |

We are the **second-least power-dense design in the field**, behind only CAREM. This substantiates the "margin over burnup" claim with an external reference rather than an assertion.

---

## 3. ⚠️ The boron-free field — read this before slide 6

There are **three** boron-free designs in the booklet, not two, and one of them has a *stronger* claim than ours.

| Design | Boron-free claim | Circulation | Cycle |
|---|---|---|---|
| **CAREM-25** | "Control rod driving mechanism (CRDM) **only**" | Natural | 14 mo, 50 % core replacement |
| **NUWARD** | "**boron-free in normal operation and in all Design Basis Conditions (DBC)**" | **Forced** | 24 mo, half core |
| **Aegis-40** | Boron-free **normal operation**; EBIS for cold shutdown | Natural | 73 mo, single batch |

**Our slide 6 claim survives** — no design combines boron-free + natural circulation + a six-year single-batch cycle. CAREM is boron-free and natural circulation but refuels every 14 months; NUWARD is boron-free but forced circulation.

**But be ready for this question:**

> *"NUWARD claims boron-free in all design-basis conditions. You need boron injection for cold shutdown. Isn't theirs the stronger design?"*

**Honest answer:**
> "On that specific axis, yes — their claim is stronger than ours, and we don't dispute it. Ours is boron-free in normal operation, with a diverse boron system for the cold shutdown state. But NUWARD is forced circulation at 540 MWth per unit with a 24-month half-core refuelling cycle. We're holding a six-year single-batch reactivity inventory under natural circulation, which is a much larger inventory to control with rods alone. Different trade."

**Do not** claim to be the only boron-free SMR. Claim the *combination*.

---

## 4. Where we lead

| | Us | Field |
|---|---|---|
| **Cycle length without refuelling** | **73 months** | next longest 30 (SMART) |
| **Cogeneration breadth** | electricity + heat + hydrogen | most are electricity-only; desalination is the common second product |
| **Power density (margin)** | 3.38 MWth/FA | only CAREM lower |
| **Boron-free + natural circulation together** | yes | only CAREM |
| Enrichment headroom | 4.43 % average | most sit at 4.0–4.95 |

## 5. Where we lag

| | Us | Field | Honest read |
|---|---|---|---|
| **Burnup** | **29.6 GWd/t** | 45–60 typical | Lowest but one (CAREM 24). Deliberate — see §2 — but it *is* poorer uranium utilisation. |
| **Electrical output** | **40 MWe** | 77–470 | Smallest land-based design in the booklet except CAREM. Worst $/kW exposure. |
| **Design maturity** | student detailed design | 2 under construction | CAREM and ACP100 are being built. We are a paper design and should say so. |
| **Seismic basis** | 0.3 g | NuScale and SMR-160 at 0.5 g | Adequate but not leading. |
| **Design life** | 60 y | SMR-160 at 80 y | Middle of the field. |
| **Efficiency** | 32.0 % | typically 30–33 % | Comparable; low pressure and low outlet temperature cap it. |

---

## 6. Footprint — *superseded by §10.2 below, which computes it*

The IAEA booklet's "plant footprint" is a **site/plot area**. Our FER gives **per-building footprints only**:

Reactor Building ~625 m² · Spent Fuel Pool Building ~450 · Auxiliary/Radwaste ~500 · Control ~375 · Turbine ~600 · Hydrogen yard ~625 · Others ~1 665
→ **~4 800 m² of buildings**

That is **not comparable** to CAREM's 36 000 m² or BWRX-300's 9 800 m², which include the whole plot, roads, switchyard and exclusion arrangements.

**Action:** the FER states no total site area. It should. If asked, say *"our building footprints total about 4 800 square metres; we quote a 0.5 km emergency planning zone goal, and the total site area is a layout item we have not fixed."* **Do not** compare 4 800 to 36 000 — you would be claiming a 7× advantage that isn't real.

---

## 7. Economics — what can and cannot be compared

**The IAEA booklet publishes no economics for any design.** No LCOE, no capital cost, no O&M. Public figures for NuScale, BWRX-300 and Rolls-Royce exist but come from different years, currencies, discount rates, capacity factors and scopes — they are **not comparable on a common basis**, and quoting them beside our number would be misleading.

**What we can say:**

| | Aegis-40 |
|---|---|
| LCOE, NOAK ($3 500/kWe) | **$74.8/MWh** — capital 49 %, O&M 26 %, fuel 24 % |
| LCOE, FOAK ($5 000/kWe) | $90.5/MWh |
| LCOE, high capital ($8 250/kWe) | $124.8/MWh |
| District heat | $26/MWh-th |
| Hydrogen | $2.49/kg |

**The comparable statements are structural, not numerical:**

- **We have three revenue streams; most of the field has one.** Only ACP100 and SMART list a second product (desalination/heat). None lists hydrogen.
- **Our fuel cost is structurally higher per MWh** because of lower burnup — roughly $5/MWh above what a 44 GWd/t three-batch scheme would give, ~6 % of the electricity price.
- **Our capital exposure is structurally worse** because 40 MWe is the smallest output in the class. This dominates everything: a $3 500 → $8 250/kWe swing moves LCOE by $50/MWh, far more than any fuel-cycle choice.

**If asked "how does your cost compare to NuScale?":**
> "I can't give you a like-for-like answer, and I'd rather say so than quote a number from a press release. The IAEA booklet publishes no economics for any of these designs. What I can tell you is the structure of ours: capital is half our cost, fuel a quarter, and the whole answer turns on whether a 40-megawatt unit can be built at nth-of-a-kind capital cost."

---

## 7b. External LCOE benchmarks — the numbers that do exist

Added 23 August 2026. **None of these is on a common basis with ours** — different currency years,
discount rates, capacity factors, scopes (financing during construction? decommissioning? grid
connection?) and, critically, some are *targets* while others are *outturns*. Use them as anchors, not
as a league table, and say so if you quote one.

### Large reactors — contracted or built

| Plant / study | $/MWh | What the number is |
|---|---:|---|
| **Akkuyu (Turkey, VVER-1200)** | **123.5** | Contracted PPA, 12.35 ¢/kWh guaranteed 15 yr. **The Turkish anchor.** |
| Hinkley Point C (UK, EPR) | ~165 | £92.5/MWh 2012 money, index-linked ≈ £128/MWh today, 35-yr CfD |
| Vogtle 3&4 (US, AP1000) | ~110–190 | Outturn ≈ $35 bn / 2.2 GWe ≈ $15,900/kWe |
| Barakah (UAE, APR-1400) | ~50–65 | ≈ $24.4 bn / 5.6 GWe ≈ $4,400/kWe — cheap end of Western-financed new build |
| Korea domestic APR-1400 | ~40–55 | Serial construction, ~$2,000–3,000/kWe |
| **IEA/NEA *Projected Costs* 2020** | **~69 median** | 7 % discount. The neutral reference if you want one number. |
| Existing plant, long-term operation | 30–40 | Capital sunk — *not* a new-build comparator |
| Lazard v17 (2024), US merchant | 142–222 | Highest published; US financing assumptions |

### SMRs — targets, not outturns

| Design | $/MWh | Status |
|---|---:|---|
| **NuScale / UAMPS CFPP** | 58 (2021) → **89 (Jan 2023)** | **Project cancelled Nov 2023 at that price** |
| Rolls-Royce SMR | ~£60 FOAK target, ~£40–50 NOAK | Vendor target, unbuilt |
| BWRX-300 (OPG Darlington) | no public LCOE | ~CAD 6.1 bn first unit, capital only |
| **Aegis-40** | **74.8 NOAK · 90.5 FOAK · 124.8 high-capital** | Own model, $3,500 / $5,000 / $8,250 per kWe at 7 % |

### The two things to say

**1 — Akkuyu is the honest benchmark, and it favours us.** Turkey has contractually agreed to pay
**$123.5/MWh** for large-reactor nuclear at a site 300 km from ours. Our nth-of-a-kind case is $74.8
and even our **high-capital** case is $124.8 — i.e. our pessimistic case is roughly the price Turkey
has already accepted. That is a locally grounded, checkable framing, and much stronger than comparing
against a vendor press release.

**2 — Name NuScale before a juror does.** A real SMR with a real customer went 58 → 89 $/MWh and was
cancelled. If asked why $74.8 is credible:

> "It isn't a promise — it's a nth-of-a-kind number at an assumed $3,500 per kilowatt. Our own
> sensitivity shows overnight capital swings the answer by fifty dollars a megawatt-hour, more than
> every other parameter combined. That is exactly what happened to NuScale: the physics didn't change,
> the capital estimate did. So the honest claim is a range, $75 to $125, and the question is whether a
> 40-megawatt unit can be built serially."

**Sinop history — know it.** The Mitsubishi–Areva ATMEA1 project planned for *our site* was cancelled
in 2018 when the estimate roughly doubled to ~$44 bn. A juror may raise it. The answer is that it
failed on absolute capital-at-risk for a 4.4 GWe project, which is the argument *for* a 40 MWe unit,
not against it.

---

### FER vs deck — resolved 23 Aug, **on the third attempt**

*Two earlier versions of this section were wrong. Both quoted a superseded FER. The rule that came out
of it now lives in `docs/competition/WHICH-FER-IS-AUTHORITATIVE.md` — read that first.*

**The authoritative FER is `docs/Aegis40_FER_submission_ready_compact_final.docx`, 15 Jul 2026.**
There are six other FER files on disk; none of them should be cited.

**On economics and waste the deck and the FER agree exactly** — they always did:

| | FER (15 Jul) | Deck |
|---|---|---|
| LCOE 7 %, NOAK / FOAK / derived | 74.8 / 90.6 / 124.7 | same |
| Full sensitivity, 3–10 % | 55.5–192.2 | same |
| Cogeneration-credited LCOE | $64.8/MWh | same |
| Fuel cycle | $17.3 front end + ~$1 back end = **$18.3/MWh** | same |
| Waste intensity | 4.40 tHM/TWhe, −32 % | same |
| Discharge Pu | 78.1 kg, Pu-239 61.6 %, Pu-240 21.6 % | same |

**What the superseded files say, and why:** `Aegis40-FER-master.md` §§8.11/8.12 were written **30 Jun**,
before the **4 Jul basis freeze** moved discharge burnup 27.6 → 29.6 GWd/tHM and heavy metal
9.87 → 9.39 tHM. That single change is the whole waste-intensity difference:
`1000 / (29.608 × 24 × 0.320) = 4.40`. `FROZEN-MASTER-VALUES.md` (4 Jul) already lists
`4.72 / 4.50 → 4.40` under **"❌ STALE VALUES — replace on sight"**. The 7 Jul intermediate
(`Aegis40_FER_latest_submission_ready.md`) carries LCOE 75.9 / cogen 65.9, corrected to 74.8 / 64.8 on
15 Jul. Both files now carry a **SUPERSEDED** banner.

---

### The real mismatch runs the other way: the FER is **behind** the deck on safety neutronics

Checking the 15 Jul FER properly turned up something that does matter for the finals. It still carries
the **12-CRA** values. `02_FER-DOCX-EDITS.md` §A has listed the replacements since **14 Aug with every
box unchecked**, and the document confirms they were never applied:

| FER (15 Jul) | Should be | Slides |
|---|---|---|
| rod worth **15,672 pcm** | 21,509 pcm | ✅ corrected 22–23 Aug |
| hot SDM **~2.0 %** | 7.85 % | ✅ |
| k_ARI **0.980** | 0.927 | ✅ |
| k_adj cold **0.845** | 0.790 | ✅ |
| vessel fluence **3.35 × 10¹⁸** | 3.02 × 10¹⁸ | ✅ |

A juror reading the FER sees 15,672 pcm and 2.0 % shutdown margin while the slide says 21,509 and
7.85 %. **It is an upgrade, so lead with it rather than being caught by it:**

> "The report carries the 12-rod configuration. We finalised at 16 control-rod assemblies, which raises
> bank worth to 21,509 pcm and hot shutdown margin to 7.85 % — about four times the acceptance
> criterion. The digital appendix carries the final run."

Also open from §C: FER **Table 8.12-2 still reads $65.9/MWh** for the cogeneration-credited LCOE while
§8.12.3 prose reads **$64.8** — applied to the prose, missed in the table.

---

## 8. Slide-by-slide implications

| Slide | Current claim | Verdict |
|---|---|---|
| **6** Literature Review | "no operating or announced iPWR combines SBF + natural circulation + six-year single-batch cycle" | ✅ **Holds.** But add NUWARD to the table, or be ready for it in Q&A (§3). |
| **6** table row for SMART | "107 MWe, forced, soluble, multi-batch 54 GWd/tHM" | ✅ Matches IAEA exactly. |
| **6** table row for ACP100 | "125 MWe, forced, soluble, heat/steam" | ✅ Matches. |
| **6** table row for CAREM | "30 MWe, natural, boron-free, 24 GWd/tHM" | ✅ Matches. |
| **6** table row for NuScale | "77 MWe/module, natural, soluble, 45 GWd/tHM" | ✅ Matches. |
| **34** Reference Comparison | four-way comparison on output, burnup, reactivity control, revenue streams | ✅ All four rows verified against IAEA data. |

**Recommended additions:**
1. Add a **NUWARD** row to slide 6 — it's the closest competitor on reactivity control and omitting it looks like avoidance.
2. Consider adding **power density (MWth/FA)** as a row — it's the number that best substantiates "margin over burnup", and we're second-best in the field.
3. State a **total site area** somewhere, or stop implying a footprint advantage.

---

## 9. One-line positioning

> *Aegis-40 sits at the low-power-density, long-cycle corner of the SMR field: essentially NuScale's core geometry run at half the power, controlled without soluble boron like CAREM but for six years instead of fourteen months, and selling heat and hydrogen alongside electricity. It is the smallest and least fuel-efficient design in its class, and the most thermally conservative.*

---

## 10. Computed: RPV weight and plant footprint

Both were missing from the FER. Calculated here from the CAD geometry in FER Table 8.1.

### 10.1 Reactor pressure vessel — **≈ 270 t** with internals and fuel

| Component | Volume | Mass |
|---|---|---|
| Lower shell (R_i 1.350 m, h 4.15 m) | 5.99 m³ | |
| Upper shell (R_i 1.523 m, h 7.01 m) | 11.34 m³ | |
| Bottom head + top head (hemispherical) | 4.67 m³ | |
| Support skirt (577.8 × 3 414 × 90 mm) | 0.54 m³ | |
| **Structural steel** (SA-508/533, 7 850 kg/m³) | **22.54 m³** | **177.0 t** |
| **Stainless cladding** (5 mm, 7 900 kg/m³) | 0.64 m³ | **5.1 t** |
| Bare pressure shell | | **182.0 t** |
| Nozzles, flange, closure studs (+18 %) | | 32.8 t |
| **Dry vessel** | | **≈ 215 t** |
| Core barrel (lower + upper, 25 mm) | | 7.6 t |
| OTSG helical bundle (Inconel, ~25 % packing) | | 12.9 t |
| ICRDM, rod guides, pressuriser internals | | 20.0 t |
| Fuel (UO₂ + cladding/structure) | | 15.2 t |
| **RPV WITH INTERNALS AND FUEL** | | **≈ 270 t** |

**Cross-check:** CAREM-25 is 267 t at 11.0 × 3.2 m and ACP100 is 300 t at 10.0 × 3.35 m. Ours is 11.16 × 3.05 m and lands at 270 t — between the two, as it should. That agreement is what makes the estimate defensible.

### 10.2 Plant footprint — **≈ 31 600 m² (3.2 ha)**

The FER gives building footprints only, summing to **≈ 4 840 m²**. That is *not* comparable with the IAEA "plant footprint" column, which is a site plot area.

The site envelope is set by the **≈ 123 m hydrogen explosion stand-off (RG 1.91)**, not by the buildings:

| | |
|---|---|
| Site length | ≈ 263 m (nuclear island 80 + stand-off 123 + cogen island 60) |
| Site width | ≈ 120 m (islands + roads + security perimeter) |
| **Plant footprint** | **≈ 31 600 m² = 3.2 ha** |
| Without the hydrogen island | ≈ 20 400 m² (2.0 ha) |

**The hydrogen island roughly doubles the site.** That is a real and quotable design consequence — and it compares sensibly with CAREM-25 at 36 000 m² for 30 MW(e).

⚠️ **These are engineering estimates, not FER values.** Present them as such: *"we calculate approximately…"*, never *"the FER states…"*.

---

## 11. Design life — is 60 years right?

**Short answer: keep 60 years. The concern is real but it points at a different mechanism.**

### Why 60 years is defensible

The design life of a PWR is set by **reactor pressure vessel neutron embrittlement**, and ours passes with margin:

| | |
|---|---|
| 60-year fast fluence | **3.02 × 10¹⁸ n/cm²** |
| Limit | 1 × 10¹⁹ n/cm² |
| Margin | **3.3×** |

The vessel is not the constraint. That margin comes directly from the low power density and the wide downcomer — the same choices that bought the thermal margin.

### The six-year cycle *helps* rather than hurts

Thermal cycling — heat-up, cool-down, load change — is the dominant fatigue driver for a pressure boundary. Fewer outages means fewer cycles:

| | Major thermal cycles in 60 years |
|---|---|
| Aegis-40 (6-year cycles) | **≈ 10** |
| A plant on 18-month cycles | ≈ 40 |

**Four times fewer major transients over the plant life.** Running continuously is gentler on the pressure boundary than starting and stopping, not harsher.

### What the six-year cycle *does* put at risk

Not damage accumulation — **access**. For six years you cannot open the vessel, so:

1. **OTSG tube wear.** Flow-induced vibration wear normally caught by eddy-current inspection each outage; six years between examinations is long.
2. **In-vessel CRDM reliability.** Electromechanical devices inside the pressure boundary must function for six years with no access.
3. **Instrument drift** without recalibration opportunities.
4. **ASME Section XI in-service inspection intervals** are nominally ten years — compatible with a six-year cycle (inspect every second refuelling), but it needs stating rather than assuming.

### Where the field sits

CAREM-25 claims 40 y · ACP100, SMART, NuScale, NUWARD, BWRX-300, Rolls-Royce all claim 60 y · SMR-160 claims 80 y. **Our 60 is mainstream, not optimistic.**

### Recommendation

**Do not reduce the design life to 40 years.** It would be unjustified — the fluence substantiates 60, and CAREM's 40 reflects an older demonstration-prototype scope, not a physical limit.

**Do add in-service inspection and in-vessel maintainability as an explicit open item.** That is the genuine six-year vulnerability, and naming it is stronger than being asked about it. It has been added to §12 of the design datasheet.

**If asked:** *"Sixty years is set by vessel embrittlement, and our 60-year fluence is 3.0 × 10¹⁸ against a 1 × 10¹⁹ limit — a factor of three margin. The long cycle actually reduces fatigue, because we see about ten major thermal cycles in the plant life instead of forty. What the six-year cycle does require is a defined in-service inspection strategy and demonstrated in-vessel component reliability, and we list that as next-step work."*

---

## 12. ⚠️ Error found in the site layout figure

The FER states a seismic gap of **≥ 75 mm** between Category I and Category II structures (§8.10.3, and again in the building table). The site-layout figure used in the deck appears to read **"seismic gap ≥ 75 m"** — a factor of 1000.

Seventy-five metres between the reactor building and the turbine building would be an extraordinary separation and is clearly not what the layout shows. **Check the figure and correct it to 75 mm** before the finals.

---

## 13. How do long-cycle reactors handle the inspection problem? (RITM-200 and friends)

The question is exactly right, and the IAEA booklet answers it. **Three designs run longer than we do**, and all three are Russian marine-derived:

| Design | Cycle | Enrichment | Burnup | Fuel | How refuelling/inspection happens |
|---|---|---|---|---|---|
| **RITM-200M** | **120 months (10 y)** | **< 20 %** | — | cermet | *"Without on-site refuelling"* — the whole floating unit **sails back to the exporting country** with spent fuel still in the reactors |
| **SHELF-M** | **96 months (8 y)** | < 19.7 % | **162.4 GWd/t** | cermet | *"Refuelling and nuclear waste removal will be carried out at dedicated facilities"* — integral transportable containment; the power capsule is shipped |
| **VBER-300** | **72 months (6 y)** | 4.95 % | 50 GWd/t | UO₂ | land or floating; **CRDM + soluble boron** |
| **Aegis-40** | 73 months (6.09 y) | 4.95 % | 29.6 GWd/t | UO₂ | land, on-site refuelling |

### How RITM actually solves it — and why we can't copy it

**They don't inspect in place. They move the reactor.** That is the whole answer. RITM-200M is a floating power unit; at end of cycle the vessel returns to a dedicated facility where refuelling, inspection and waste removal all happen. SHELF-M does the same with a transportable power capsule. The in-service-inspection problem is solved by **logistics, not by engineering the components to be inspectable in situ**.

Three supporting factors:

1. **Enrichment up to 20 %** with **cermet fuel** (UO₂ in a metallic matrix). That is what buys a 10-year cycle — far more excess reactivity and much better fission-gas retention than our 4.95 % UO₂. It also puts them right at the LEU limit, with the non-proliferation scrutiny that brings.
2. **Cassette steam generators.** RITM's four SGs are built as *"3 rectangular cassettes"* each — an SG can be replaced as a unit rather than repaired tube-by-tube.
3. **400+ reactor-years** of operating experience in the OK-150 / OK-900 / KLT-40 lineage. Reliability is demonstrated by fleet statistics, not by analysis. We have none of that.

**We cannot sail Sinop back to a shipyard.** A land-based civil plant under ASME Section XI and NDK licensing has to be inspectable where it stands. So the RITM precedent proves long cycles are operationally viable — it does **not** give us their solution.

### What is genuinely transferable

- **Cassette / replaceable OTSG modules** rather than a permanently installed bundle.
- **Condition monitoring instead of periodic inspection**: online N-16 monitoring for primary-to-secondary leakage, acoustic leak detection, loose-parts monitoring. This is the modern answer to "we cannot open it."
- **Cross-calibration between redundant channels** handles instrument drift without physical access — we already have 21 channels of which 14 are Class 1E, so the redundancy exists.

### Two points that ease the concern

**ASME XI is less of a problem than it first appears.** The nominal in-service inspection interval is **10 years**. A 6-year fuel cycle means inspecting at *every* refuelling, which sits comfortably inside that interval. The pressure boundary is fine.

**Boron-free chemistry actually helps the steam generator.** No boric acid means less aggressive primary chemistry, less crud transport and less deposition on tube surfaces. Our OTSG environment is more benign than a conventional PWR's — which partly offsets inspecting it every 6 years instead of every 18 months.

**The residual concern is narrow:** OTSG tube flow-induced-vibration wear, examined every 6 years instead of every 1.5–2. That is worth naming as an open item and worth a monitoring strategy — it is not a reason to shorten the cycle.

### ⚠️ The sharper insight — and it changes how you explain the design

**VBER-300 achieves a 6-year cycle at the same 4.95 % enrichment as us, with 50 GWd/t burnup — nearly double ours.**

Working back from its parameters: 917 MWth over 72 months at 50 GWd/t implies a **34 tHM core running at ~26.9 MW/tHM — about twice our specific power.**

How? **It uses soluble boron.** Boron lets you hold far more beginning-of-cycle excess reactivity, so you can load a longer, hotter cycle.

**Therefore: our low burnup is the price of being boron-free, not the price of the long cycle.** Those are different claims, and the second one is the true one.

The design logic is really:

> A six-year cycle needs a large reactivity inventory. Holding it *without soluble boron* means holding it on burnable absorbers and rods alone — and that only works if the total swing is small enough, which means low specific power, which means low burnup.

**Use this if asked "why is your burnup so low?"**
> "Because we are boron-free. VBER-300 runs the same six-year cycle at the same enrichment and reaches 50 gigawatt-days per tonne — but it uses soluble boron to hold the excess reactivity. Without boron we have to hold the whole cycle on burnable absorbers and rods, and that is only feasible at low specific power. The low burnup is the price of eliminating the dilution accident and getting a strongly negative moderator coefficient — not a limitation of the six-year cycle itself."

That is a much stronger answer than "we chose margin over burnup," because it names the actual physical coupling and cites a design that proves the alternative.
