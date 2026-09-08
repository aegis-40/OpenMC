# Aegis-40 — Team Handbook

**Everything you need to understand and defend this design.**
Updated 22 August 2026. Numbers here are the frozen basis — if a slide disagrees, the slide is stale.

---

## PART 1 — The design in one page

**Aegis-40 is a 125 MWth / 40 MWe integral pressurised-water reactor for the Sinop coast.**

Four choices define it, and almost every number follows from them:

1. **Integral vessel.** The core, one helical-coil once-through steam generator and the pressuriser all sit inside one pressure boundary. *Consequence:* no large-bore primary piping → large-break LOCA eliminated; no head-mounted rod drives → rod ejection eliminated; no external surge line → surge-line break eliminated.
2. **Natural circulation.** No reactor coolant pumps; buoyancy drives the loop. *Consequence:* loss of offsite power is not a loss-of-flow event. But mass flux is low (~543 kg/m²·s), which squeezes thermal margin — hence choice 3.
3. **Low power density (13.31 MW/tHM, ~⅓ of a large PWR).** *Consequence:* large thermal margins (centreline 828 °C, cladding 353 °C), but low burnup and a physically large core for the power.
4. **Soluble-boron-free, single-batch, six-year cycle.** *Consequence:* no boron dilution accident, a more negative moderator coefficient, no boron plant — but the entire six-year reactivity inventory must be held by burnable absorbers and rods, which is the hardest problem in the design.

**The one-sentence version:** *A small integral PWR that cools itself without power, runs six years without refuelling, holds its reactivity without boron, and sells electricity, heat and hydrogen.*

---

## PART 2 — Terminology

### 2.1 Reactor physics

| Term | What it means |
|---|---|
| **k_eff** | Multiplication factor. k = 1 exactly critical; k > 1 power rising; k < 1 shutting down. Ours is 1.1504 at beginning of life with rods out. |
| **Reactivity (ρ)** | How far from critical: ρ = (k−1)/k. Measured in **pcm** = 10⁻⁵. Our BOL excess is ~13,100 pcm. |
| **pcm** | "per cent mille" = 1/100,000. 21,509 pcm = 21.5 % Δk/k. |
| **β_eff** | Effective delayed-neutron fraction — the fraction of neutrons that arrive late. It's what makes a reactor controllable. **Ours = 704.5 ± 28 pcm** (we computed it, didn't assume it). |
| **Dollar ($)** | Reactivity measured in units of β_eff. **1 $ = 704.5 pcm for us.** Above 1 $ the reactor is *prompt critical* — it runs on prompt neutrons alone and the excursion is no longer controllable by rods. |
| **Prompt critical** | The dangerous threshold. Insert more than 1 $ suddenly and power rises on a millisecond timescale. |
| **MTC** — moderator temperature coefficient | How reactivity changes when the coolant heats up. **Ours: −26.87 pcm/K.** Negative = self-stabilising: hotter → less reactive. |
| **DTC / Doppler** — fuel temperature coefficient | Same, for fuel temperature. **Ours: −1.91 pcm/K.** Acts instantly (the fuel heats before the coolant), so it's the first line of defence in any power excursion. Caused by *Doppler broadening* — hot U-238 absorbs more neutrons. |
| **Void coefficient** | Reactivity change if coolant boils into steam. **Ours: −173.2 pcm/%void.** Negative — boiling shuts the reactor down. (Chernobyl's was strongly *positive*.) |
| **Burnup** | Energy extracted per mass of fuel, **GWd/tHM** (gigawatt-days per tonne of heavy metal). Ours: **29.6** core average. Large PWRs reach 45–55. |
| **EFPD** | Effective full-power days. **2224 EFPD** = 6.09 full-power years. |
| **Burnable absorber** | Neutron poison mixed into the fuel that "burns away" as the fuel depletes, holding down early-life reactivity. We use **Gd₂O₃ (gadolinia)** — very strong, burns out fast — and **Er₂O₃ (erbia)** — weaker, burns slowly, lasts the whole cycle. |
| **CRA** — control rod assembly | A cluster of absorber rods that drops into the core. We have **16**, B₄C enriched to **90 % B-10**. |
| **CRDM** — control rod drive mechanism | The motor that moves the rods. Ours are **in-vessel** — inside the pressure boundary — which is why rod ejection cannot happen. |
| **Bank worth** | Total reactivity all rods can insert. **Ours: 21,509 pcm.** |
| **SDM** — shutdown margin | How far below critical the core sits with rods in and the *most reactive rod stuck out*. **Ours: 7.85 % Δk/k hot**, against a ≥1 % criterion. |
| **ARO / ARI** | All Rods Out / All Rods In. |
| **HZP / HFP** | Hot Zero Power / Hot Full Power. At HZP the fuel and coolant are at the same temperature (no power). At HFP the fuel is much hotter (900 K vs 556 K). **This distinction matters** — see §5.2. |
| **Stuck rod** | The regulatory assumption that the single most reactive rod fails to insert. All shutdown claims must hold with one rod stuck. |
| **F_ΔH** | Enthalpy-rise hot channel factor — how much hotter the worst channel gets. Ours: 1.513 / 1.729 / 1.497 at BOC/MOC/EOC. |
| **F_q** | Total peaking factor — the hottest *point* in the core vs average. Ours: 1.937 / 2.435 / 2.121. |
| **COLR** | Core Operating Limits Report — the envelope the plant is licensed to operate inside. Ours: F_ΔH ≤ 1.75, F_q ≤ 2.4675. |
| **Xenon** | Xe-135, a strong neutron poison that builds up after shutdown and decays over ~2 days. Causes the "xenon dead time" when a reactor can't restart immediately. |

### 2.2 Thermal-hydraulics

| Term | What it means |
|---|---|
| **DNB** — departure from nucleate boiling | The failure mode. Normally bubbles form and detach, cooling efficiently. If heat flux gets too high, a *vapour film* blankets the cladding, heat transfer collapses, and the cladding overheats within seconds. |
| **CHF** — critical heat flux | The heat flux at which DNB occurs. |
| **DNBR / MDNBR** | Ratio of critical heat flux to actual heat flux. Minimum DNBR is the limiting value in the core. **Ours: 1.33** at the limiting state. **Below 1.0 means burnout.** |
| **The 1.30 limit** | Not a physical boundary — a **95/95 statistically protected** limit: 95 % confidence that 95 % of the time DNB will not occur. Physical margin is a further ~30 % beyond it. |
| **W-3 / Bowring / Groeneveld** | Three independent CHF correlations. We report all three: **1.33 / 2.13 / 6.18**. W-3 is the most conservative and we quote it as limiting. |
| **PCT** — peak cladding temperature | **353 °C** normal operation, against the **1204 °C** LOCA acceptance limit. |
| **Centreline temperature** | Hottest point in the fuel pellet: **828 °C**, far below UO₂ melting (~2800 °C). |
| **Subcooling** | How far below boiling the water is. Ours: ~23 K at the hot leg. |
| **Mass flux** | Coolant flow per unit area, kg/m²·s. Ours ~543 — low, because natural circulation. A large PWR is ~3500. |
| **OTSG** | Once-Through Steam Generator — makes superheated steam in a single pass, no steam drum. Ours is helical-coil, inside the vessel. |
| **Natural circulation** | Hot water rises, cold water sinks, flow is self-sustaining. Requires a tall "thermal centre height" (ours ~4 m) between the core and the heat sink. |

### 2.3 Safety systems and events

| Term | What it means |
|---|---|
| **LOCA** | Loss-of-Coolant Accident. **LB-LOCA** (large break) is the classic design-basis worst case — *eliminated by construction* in our design. **SB-LOCA** (small break) remains, bounded by nozzle size. |
| **MSLB** | Main Steam Line Break — an *overcooling* accident. The secondary side depressurises, over-cools the primary, and with a negative MTC that **inserts positive reactivity**. Our limiting reactivity transient. |
| **SBO** | Station Blackout — total loss of AC power. In our design this is nearly benign: loss of power *actuates* the passive systems. CDF ~1×10⁻¹¹/ry. |
| **LOHS** | Loss of Heat Sink. CDF ~1×10⁻⁸/ry. |
| **ATWS** | Anticipated Transient Without Scram — a transient where the rods fail to insert. This is what the diverse boron system covers. |
| **REA** | Rod Ejection Accident — a drive housing fails and blows one rod out at full pressure. *Eliminated by construction* (in-vessel CRDM). |
| **AOO** | Anticipated Operational Occurrence — things expected to happen occasionally (a trip, a load rejection). Must cause no fuel damage. |
| **DBA** | Design-Basis Accident — unlikely but designed against. |
| **DEC** | Design Extension Conditions — beyond design basis, managed with reasonable practicability. |
| **IRWST** | In-containment Refuelling Water Storage Tank — our **250 m³** pool. It is *the* safety heat sink: PRHR rejects heat into it, safety injection draws from it, containment condensate returns to it. **≥ 240 h of cooling with no power and no operator.** |
| **PRHR** | Passive Residual Heat Removal — natural-circulation loop from the vessel to a heat exchanger submerged in the IRWST. Two 100 % trains. |
| **ADS** | Automatic Depressurisation System — vents the primary so gravity injection can work. |
| **EBIS** | Emergency Boron Injection System — our **second, diverse** shutdown system. Dormant, passive, ~3000 ppm boron on gravity head and a nitrogen accumulator. |
| **Ultimate heat sink** | Where decay heat ultimately goes. **Ours is the IRWST + passive containment cooling — NOT the sea.** The Black Sea is only the normal condenser sink (82.6 MWth). This is the key to being seawater-independent. |
| **Defence in depth** | Five layers: prevent abnormal operation → control it → control design-basis accidents → control severe conditions → off-site emergency response. |
| **CDF / LRF** | Core Damage Frequency / Large Release Frequency, per reactor-year. Targets: < 1×10⁻⁶ and < 1×10⁻⁷. |
| **De-energize-to-trip** | Rods are held up by electromagnets. Lose power → they drop. Failure defaults to safe. |
| **Class 1E** | The safety-qualified electrical/I&C classification. |
| **RPS / ESFAS / DAS** | Reactor Protection System (trips the reactor, 4 divisions, 2-of-4 voting, ≤500 ms) / Engineered Safety Features Actuation System (starts the passive systems) / Diverse Actuation System (platform-diverse backstop against common-cause software failure). |
| **Practically eliminated** | A regulatory term: the scenario is made so unlikely by design that it need not be analysed as a design basis. |

### 2.4 Fuel cycle, waste, plant

| Term | What it means |
|---|---|
| **Once-through** | Fuel goes in once, comes out, no reprocessing. One core load for the whole six-year cycle. |
| **tHM** | Tonnes of heavy metal (uranium). Our core: **9.39 tHM**. |
| **Waste intensity** | Spent fuel per unit electricity: **4.40 tHM/TWhe**, ~32 % below CAREM-25. |
| **Reactor-grade Pu** | Plutonium with high Pu-240 content — unattractive for weapons. Ours is firmly reactor-grade. |
| **SQ** | Significant Quantity — IAEA's safeguards accounting unit; 8 kg for Pu. |
| **SFP** | Spent Fuel Pool. Ours uses ~2000 ppm boron + fixed absorber racks + burnup credit; k(95/95) = 0.892 < 0.95. |
| **TCES** | Thermochemical Energy Storage — zeolite-13X/water, 200 MWh thermal. Stores heat by adsorption. |
| **SOE** | Solid Oxide Electrolyser — makes hydrogen at high temperature, 8 MWe, run off-peak. |
| **LCOE** | Levelised Cost of Electricity. Ours: **$74.8/MWh** NOAK, $90.6 FOAK. |
| **NOAK / FOAK** | Nth-of-a-kind (mature) / First-of-a-kind (expensive first build). |
| **SSE** | Safe Shutdown Earthquake. Ours: **0.3 g**. |

### 2.5 Codes, standards, tools

| Term | What it means |
|---|---|
| **OpenMC** | Open-source Monte Carlo neutron transport code. Simulates individual neutrons statistically — no approximations in geometry or energy. Version 0.15.3. |
| **ENDF/B-VIII.0** | The nuclear data library — measured cross-sections for every isotope. |
| **Monte Carlo statistics** | We run **400 batches × 50,000 particles ≈ 16 M histories**, giving k uncertainty of 22–26 pcm. More particles = less noise. |
| **ICSBEP** | International Criticality Safety Benchmark Evaluation Project — a handbook of **measured** critical experiments. We validate against LEU-COMP-THERM-008: mean bias **−50 pcm**, every case within uncertainty. |
| **BEAVRS** | A benchmark based on a real operating PWR. |
| **OpenFOAM** | Open-source CFD. We use conjugate heat transfer (solid + fluid together) on the hot channel. |
| **DWSIM** | Open-source process simulator — our Rankine cycle balance. |
| **IAPWS-IF97** | The international standard for water/steam properties. |
| **SSR-2/1** | IAEA's core safety requirements document. **Requirement 46** = two diverse shutdown systems (why EBIS exists). |
| **NUREG-0800 / SRP** | US NRC Standard Review Plan. SRP 4.2 fuel, 4.3 nuclear design, 4.4 thermal-hydraulics, 15.4.8 rod ejection. |
| **GDC** | General Design Criteria (10 CFR 50 Appendix A). GDC-28 = reactivity limits. |
| **ASME III** | The pressure-vessel code. Our RPV is Division 1, Class 1. |

---

## PART 3 — Strengths

Ranked by how much they'll impress a technical jury.

### 3.1 Four accident classes eliminated by construction ⭐⭐⭐
Not mitigated — **removed**. Large-break LOCA (no large pipes), rod ejection (in-vessel drives), boron dilution (no boron), surge-line break (integral pressuriser). This is the strongest single argument in the deck because elimination beats any amount of mitigation equipment.

### 3.2 Every reactivity coefficient negative, with margin ⭐⭐⭐
MTC −26.87, Doppler −1.91, void −173.2 pcm/%void. The reactor is self-stabilising against every temperature and voiding perturbation. Boron-free operation *helps* here — soluble boron makes MTC less negative.

### 3.3 Enormous thermal margin ⭐⭐⭐
Centreline 828 °C against ~2800 melt. Cladding 353 °C against 1204. Three independent CHF correlations all pass. This is what the low power density bought.

### 3.4 Genuinely passive, genuinely seawater-independent ⭐⭐⭐
≥240 h (nominal ~286 h) with **no AC power, no seawater, no operator**. The credited ultimate heat sink is a 250 m³ pool inside containment, not the Black Sea. Station blackout is nearly a non-event: CDF ~10⁻¹¹/ry.

### 3.5 Shutdown margin ~8× the criterion ⭐⭐
7.85 % Δk/k hot against ≥1 %. Achieved without soluble boron, using 16 CRAs at 90 % B-10.

### 3.6 Reproducible, measured-data validation ⭐⭐
Validated against **measured** criticals (ICSBEP, −50 pcm bias) and an operating-PWR benchmark, not only code-to-code. Twelve-folder digital appendix with input decks, run settings, outputs, SHA-256 checksums. Most student teams cannot say this.

### 3.7 Three products, three barriers ⭐⭐
Electricity + district heat + hydrogen, with three physical barriers and a pressure gradient that drives any leak *inward*. Revenue stacking that peers don't have, without a safety compromise.

### 3.8 Honest open items ⭐⭐
Appendix C lists what isn't closed. Stating limits precisely buys more credibility with a technical jury than claiming completeness.

### 3.9 Working digital twin
GP + POD surrogates, R² = 0.9925 (k_eff) and 0.9961 (peaking) on held-out data, behind a one-way data diode, advisory only, not credited for safety.

### 3.10 Lead-free biological shield
20 cm borated polyethylene + 180 cm magnetite. RPV fluence 3.02×10¹⁸ vs 1×10¹⁹ limit; outer dose 0.23 µSv/h vs 10 target. Monte Carlo cross-checked against an independent point-kernel calculation.

---

## PART 4 — Weaknesses

**Know these better than the jury does.** Every one has a defence; none should surprise you.

### 4.1 Cold shutdown is NOT achievable by rods alone ⚠️⚠️⚠️
**The single biggest honest weakness.** With the most reactive rod stuck, the cold core is **supercritical at k = 1.031**. Even 21,509 pcm of bank worth doesn't close it.

**Why:** cooling from 556 K to 294 K raises water density from 0.748 to 1.003 g/cm³. In a core with a strongly negative MTC, that density increase inserts a large positive reactivity — roughly 10,000 pcm. A conventional PWR absorbs this with soluble boron. We have none.

**Defence:**
> "Rods handle the hot trip and most of the cooldown — subcritical from full power down to about 443 K. EBIS covers only the deep cold state, and it needs **785 ppm against the 3,000 ppm we credit** — a 3.8× margin. SSR-2/1 Requirement 46 wants two diverse shutdown systems anyway; this is our second one."

**Do not** claim the plant is boron-free. Claim the **coolant** is boron-free in **normal operation**.

### 4.2 Ejected-rod worth exceeds one dollar ⚠️⚠️
844–902 pcm = **1.20–1.28 $** against β_eff 704.5 pcm. That is prompt critical.

**Defence:** the ejection *cannot happen* — the drives are inside the vessel, there is no pressure housing to fail. This configuration is reachable only because of that. An external-drive plant would have to reduce rod worth, which a boron-free core cannot afford. **This is a strength disguised as a weakness** — but only if you frame it correctly.

### 4.3 MDNBR 1.33 is close to the 1.30 limit ⚠️⚠️
**Defence:** 1.30 is not physical — it is a 95/95 statistically protected correlation limit that already embeds DNB uncertainty. Physical margin is ~30 % beyond. Bowring gives 2.13 and Groeneveld 6.18 on the same state. And it's evaluated at the **mid-cycle limiting state**, not the easier BOC.

### 4.4 No time-dependent transient analysis ⚠️⚠️
The containment pressure/temperature transient is closed by **reference-supported screening** (SMART100, CAREM-25 precedent), not a plant-specific calculation. No integrated system-code (RELAP/TRACE-class) package across the limiting transients.

**Defence:** listed in Appendix C as controlled next-step work. Say so plainly; don't imply it's done.

### 4.5 Low fuel utilisation ⚠️
29.6 GWd/tHM vs 45–55 for a large PWR. We use more uranium per unit electricity than a multi-batch plant.

**Defence:** deliberate trade — availability (no outage in six years), simplicity (no shuffling equipment, no boron plant), and preserving the boron-free strategy. Higher burnup would need M5 cladding and would eat the margins we're banking.

### 4.6 FRAPCON fuel performance not run ⚠️
Fission-gas release, rod pressure and clad oxidation were screened **analytically**, not with a qualified fuel-performance code.

**Defence:** the fuel sits inside the approved LWR envelope at low linear heat rate, so the screening is bounding. FRAPCON is named as future work.

### 4.7 High beginning-of-life excess reactivity ⚠️
k = 1.1504, about 13,100 pcm of excess held on burnable absorbers.

**Defence:** unavoidable for a sealed six-year core — you load the whole cycle up front. The proof it's controlled is that every coefficient stays negative and SDM is 7.85 %.

### 4.8 Mid-cycle peaking hump ⚠️
F_ΔH rises to 1.729 and F_q to 2.435 at mid-cycle as the gadolinia burns out.

**Defence:** transient, bounded, inside the COLR envelope (1.75 / 2.4675), and it is the state the thermal case is run against.

### 4.9 Digital twin coefficients are only indicative
k_eff and power map are excellent (R² 0.99). The reactivity *coefficients* derived from the surrogate are weak — the sweep is wide and good for global behaviour, coarse for local derivatives. **The authoritative coefficients are the direct OpenMC runs.** The twin is advisory and not credited for anything.

### 4.10 β_eff is a prompt-k estimate, not adjoint-weighted
OpenMC 0.15.3 exposes no iterated-fission-probability scores. We used the prompt-k method (k with delayed neutrons suppressed). The two typically agree within a few per cent.

### 4.11 Economics is conditional on capital cost
$74.8/MWh at $3,500/kWe, but $124.7/MWh at $8,250/kWe. **Defence:** we report the unfavourable case rather than hiding it — that's honest engineering communication, and the sensitivity is explicit.

### 4.12 Open data item
The FER quotes 78.1 kg discharge plutonium (61.6 % Pu-239, 21.6 % Pu-240), but the exact source CSV was never committed; the two archived runs give 76.2 and 78.5 kg. Values are consistent to ~3 % and the *conclusion* (firmly reactor-grade) is unaffected. **If asked for provenance, say the depletion record is in the appendix and the vector is reactor-grade — don't improvise a number.**

---

## PART 5 — Things that will trip you up

### 5.1 "Boron-free" means the coolant, in normal operation
The plant has **two** boron systems: EBIS (~3000 ppm, emergency) and the spent-fuel pool (~2000 ppm, criticality DiD). Neither contradicts the claim. Say **"soluble-boron-free reactor coolant during normal operation."**

### 5.2 HZP vs full power — which basis a number is on
Shutdown quantities (bank worth, SDM) are evaluated at **isothermal hot zero power**: fuel at moderator temperature, because with rods in the reactor is shut down. Full-power quantities (k at BOL, the coefficients, burnup, cycle length) come from the **full-power** run. The two differ by ~590 pcm of Doppler. **This is a convention, not a discrepancy** — but if someone quotes 7.68 % instead of 7.85 %, that's why.

### 5.3 The MSLB story changed
Do **not** say EBIS exists because rods can't stop an MSLB return-to-power. The literature says high rod worth handles MSLB, and it does for us too — subcritical from full power down to ~443 K. EBIS exists for the **deep cold stuck-rod state**.

### 5.4 The ICSBEP bias is −50 pcm
The benchmark eigenvalue is **1.0007**, not 1.0000. C−E must be taken against 1.0007. If anyone says +20 pcm, they computed against unity.

### 5.5 Our ultimate heat sink is not the sea
Seawater is the **normal condenser** sink only (82.6 MWth). The **credited safety** sink is the IRWST. Marine intake blockage therefore cannot threaten core cooling.

---

## PART 6 — Expected questions

### Reactivity and core

**Q: How do you shut down without boron?**
> Sixteen control-rod assemblies with 90 %-enriched B-10 absorber, 21,509 pcm of bank worth, giving 7.85 % hot shutdown margin against a 1 % criterion. For the cold state we have a second, diverse system — emergency boron injection — as SSR-2/1 Requirement 46 requires anyway.

**Q: So you're not really boron-free.**
> The **reactor coolant** is boron-free during normal operation — that's what eliminates the dilution accident and improves the moderator coefficient. EBIS is a dormant emergency system, and the spent-fuel pool is a separate system entirely.

**Q: Why 16 rods rather than 12?**
> Twelve gave about 2 % hot shutdown margin. Sixteen at 90 % B-10 gives 7.85 %. We chose the margin.

**Q: Your BOL excess reactivity is very high.**
> It is, and it's inherent to a sealed six-year core — the whole cycle's reactivity is loaded up front. It's held by ring-graded gadolinia for early life and erbia across the cycle. Every coefficient stays negative throughout.

**Q: Why both gadolinium and erbium?**
> Gadolinium has a very large cross-section, so it suppresses the early peak and burns out fast. Erbium is weaker, depletes slowly, carries residual hold-down late, and its resonance absorption helps keep the moderator coefficient negative at BOC.

**Q: What's your rod ejection worth?**
> 844 to 902 pcm depending on evaluation state, which is 1.20 to 1.28 dollars against a computed β_eff of 704.5 pcm. Above prompt critical — which is exactly why the drives are inside the vessel. There is no ejection path.

### Thermal

**Q: MDNBR 1.33 is very close to the limit.**
> 1.30 isn't a physical limit — it's a 95/95 statistically protected correlation limit that already embeds the DNB uncertainty. Physical margin is a further 30 %. And two independent methods on the same state give 2.13 and 6.18.

**Q: How can natural circulation give enough flow?**
> A four-metre thermal centre height gives about 3.7 kPa of driving head at 543 kg/m²·s. The low power density means we don't need large flow. The benefit is that loss of offsite power is not a loss-of-flow event.

**Q: Which state are your thermal margins evaluated at?**
> The mid-cycle limiting state with F_ΔH 1.75 and F_q 2.47 on the record axial shape — not the easier beginning-of-cycle state.

### Safety

**Q: What's your worst accident?**
> By elimination, large-break LOCA doesn't exist. The limiting reactivity transient is a main-steam-line break — an overcooling event. The rods hold the core subcritical from full power to about 443 K; below that the emergency boron system covers the cold state.

**Q: What happens in a station blackout?**
> Almost nothing. Loss of power *actuates* the passive systems: rods drop on de-energisation, PRHR runs on natural circulation into the IRWST. Over 240 hours with no operator. CDF is about 10⁻¹¹ per reactor-year.

**Q: Could the district heat or hydrogen be contaminated?**
> No. Three physical barriers, and the intermediate loop is held above reactor-side pressure so any leak flows inward. Continuous radiation monitoring with fail-closed isolation.

**Q: What about the sea — jellyfish, storms, tsunami?**
> Screened per SSR-1/SSG-9. Safety structures sit on dry-site grade above the design-basis flood level. Intake blockage affects only the *normal* condenser sink — the safety heat sink is the IRWST and is seawater-independent.

### Method

**Q: How do you know your neutronics is right?**
> Validated against measured critical experiments — ICSBEP LEU-COMP-THERM-008, mean bias −50 pcm, every case inside the handbook uncertainty — plus the BEAVRS operating-PWR benchmark and a code-to-code check against Serpent on an SMR core with rod worths agreeing within ±80 pcm.

**Q: Is this a licensed design?**
> No, and we don't claim it is. It's a coherent detailed design with quantified margins, and Appendix C lists exactly what remains: a qualified containment transient, an integrated system-code package, FRAPCON fuel performance, a site-specific dose case.

### Economics

**Q: Is it economic?**
> Conditionally. $74.8/MWh at NOAK capital, $90.6 first-of-a-kind, and $124.7 if capital runs to $8,250/kWe. We report the unfavourable case. Cogeneration adds two revenue streams both priced below market.

---

## PART 7 — The numbers, one table

| | |
|---|---|
| Power | 125 MWth / 40 MWe / 32.0 % net |
| Core | 37 FA · 17×17 · 200 cm active · 9.39 tHM · 13.31 MW/tHM |
| Enrichment | 4.95 / 4.70 / 4.40 wt% (4.0 edge) |
| Absorbers | Gd₂O₃ 6 wt% × 20 rods · Er₂O₃ 0.75 wt% × 16 rods |
| Control | 16 CRA · B₄C 90 % B-10 · in-vessel drives |
| k_eff BOL | 1.1504 |
| MTC / DTC / void | −26.87 pcm/K · −1.91 pcm/K · −173.2 pcm/%void |
| Bank worth / hot SDM | **21,509 pcm** / **7.85 % Δk/k** (HZP) |
| β_eff | **704.5 ± 28 pcm** |
| Ejected-rod worth | 844–902 pcm = **1.20–1.28 $** |
| Cold stuck-rod | k = 1.031 → EBIS **785 ppm** required, 3,000 credited |
| Cycle | 2224 EFPD = 6.09 y · 29.6 GWd/tHM |
| Peaking (BOC/MOC/EOC) | F_ΔH 1.513 / 1.729 / 1.497 · F_q 1.937 / 2.435 / 2.121 |
| COLR envelope | F_ΔH ≤ 1.75 · F_q ≤ 2.4675 |
| Primary | 12.8 MPa (14.1 design) · 258/308 °C · 467 kg/s · ~543 kg/m²·s |
| MDNBR | **1.33** W-3 · 2.13 Bowring · 6.18 Groeneveld · 1.57 AOO · limit 1.30 |
| Temperatures | centreline **828 °C** · cladding **353 °C** (limit 1204) |
| Passive grace | **≥ 240 h** (nominal ~286 h) · IRWST 250 m³ |
| CDF / LRF targets | < 1×10⁻⁶ / < 1×10⁻⁷ per ry · LOHS ~10⁻⁸ · SBO ~10⁻¹¹ |
| Shielding | RPV fluence **3.02×10¹⁸** (limit 1×10¹⁹) · outer dose **0.23 µSv/h** (target 10) |
| Waste | 4.40 tHM/TWhe · SFP k(95/95) 0.892 |
| Economics | $74.8/MWh NOAK · $90.6 FOAK · $26/MWh-th heat · $2.49/kg H₂ |
| Site | Sinop · 0.3 g SSE · 60 y life · 95 % CF target |

---

## PART 8 — How to think about a question you don't know

1. **Don't invent a number.** "That's in the digital appendix — I don't want to quote it from memory" is a perfectly good answer and costs you nothing.
2. **Name the mechanism even if you don't have the value.** Showing you understand *why* is worth more than a remembered digit.
3. **If it's a weakness, own it and give the trade.** "Yes — we accept lower burnup, deliberately, because…"
4. **If it's outside your area, hand it over cleanly.** "Azamkhon owns the safety systems — Azamkhon?"
5. **Never contradict a teammate in front of the jury.** Note it, resolve it afterwards.
