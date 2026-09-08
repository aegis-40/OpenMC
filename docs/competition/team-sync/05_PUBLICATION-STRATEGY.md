# Aegis-40 — Publication Strategy

**Prepared:** 2026-08-19 · **For:** team discussion 2026-08-20
**Context:** we have a validated OpenMC/OpenFOAM design package with a 12-folder reproducible appendix. Question on the table: what can we publish from it, where, and for free.

---

## The short version

- **Write topic ① (in-vessel CRDM / rod worth).** It is the only candidate that *reframes* an active literature instead of adding a data point to one, and it avoids the MIT group entirely.
- **Topic ② (CHF correlation governance) is the fast follow** — most of its data is already in our tables.
- **Do not write the peaking/margin paper.** It is published (MIT, *Nuclear Technology* 2024).
- **Do not write the proliferation paper yet** — see the data note below, and the physics objection in §2⑥.
- **Default publishing route is free:** Elsevier/T&F subscription track costs authors nothing. NET is cheap OA. EPJ-N is €800 with waivers.

**Decisions needed tomorrow:** target topic · author order · who runs the extra sweep · TEKNOFEST publication rules.

---

## 0. Before anything: data integrity

### Fixed on 2026-08-19

A stale file was shipping in the digital appendix and it materially changed the plutonium story.

| File | Date | U inventory | Pu total | Pu-240 |
|---|---|---|---|---|
| appendix `discharge_inventory.csv` *(stale)* | Jun 4 | **4.95 t** | 55.3 kg | 24.62 % |
| `docs/competition/waste/` | Jul 4 | 8.96 t | 76.2 kg | 21.16 % |
| `openmc_model/waste_sim/` | Jun 29 | 8.95 t | 78.5 kg | 21.01 % |
| **FER (authoritative)** | Jul 7 | 9.39 tHM | **78.1 kg** | **21.6 %** |

The June-4 file sat on a **~5 tHM basis — about half our 9.39 tHM core**. A pre-freeze smaller-core run that never got refreshed when the rest of the folder was updated on July 7.

Actions taken:

1. Archived to `docs/competition/waste/archive/discharge_inventory_STALE_2026-06-04_wrong-tHM-basis.csv`
2. Current July-4 inventory installed into the appendix
3. `CHECKSUMS.sha256` updated — **220/220 verify, 0 failures**
4. `safeguards_attractiveness.md` corrected: claimed *"whole 21-FA core… per-batch = /4 (4-batch reload)"* — both obsolete, now 37-FA once-through single batch
5. `0_icsbep_criticality/README.md` corrected: `-50 pcm` → `+20 pcm` (matches `results.csv` and the deck)

Also corrected a **backwards physics claim** repeated in three places: the doc said high burnup made our Pu *"more degraded than a typical 33 GWd/t LWR discharge."* At 29.6 GWd/tHM we are *below* that, so our Pu is **less** degraded. The doc now says so and puts the weight on the extrinsic barriers, which is where our real argument lives.

### ⚠️ Still open — someone needs to find this

**No file in the repo reproduces the FER's exact numbers.** FER = 78.1 kg / 61.6 / 21.6. The two valid-basis runs give 76.2 kg / 62.79 / 21.16 and 78.5 kg / 62.47 / 21.01. The FER *total* matches the June-29 run within 0.6 %, but the *percentages* match neither — so there is likely a final ~July-7 run whose CSV never got committed.

**Action: whoever ran the final waste depletion, please commit that CSV.** Right now the FER table is not backed by a shipped file. The deck is fine — slide 30 already carries the FER values.

---

## 1. What the literature check ruled out

Nine searches across the candidate space. Four ideas died:

**Peaking vs. margin / specific power — DEAD.** Halimi & Shirvan (MIT) built five core layouts explicitly including *"natural circulation with low burnup/low power density"* — our exact configuration — and already publish the finding: *"boron free operation exhibits the ability to achieve longer cycle lengths at the cost of higher peaking factors leading to high local power and fuel temperatures."* That is the paper. *Nuclear Technology*, 2024. They also have a companion specific-power sweep in *Annals* 2024. They would likely be our reviewers.

**MSLB / EBIS — TAKEN.** KIT ran TRACE/PARCS steam-line-break on a boron-free SMART core (*NED* 2019); *Annals* 2019 covers boron-free core safety characteristics. Worse for our framing: the literature states that in SBF reactors *"there is no criticality after automatic shutdown thanks to the increased control rod worth, making the main steam line break accident much less an issue."* **This is also a Q&A risk for the finals** — a judge may ask why EBIS is needed for MSLB. Answer: EBIS is for **cold shutdown and ATWS diversity**, not MSLB per se.

**POD/GP reduced-order model — CROWDED.** POD+RBF, gappy POD, POD+GP for core power distribution are all published. Our R² = 0.99 is standard practice, not a result.

**CHF correlation screening at low mass flux — MOSTLY DONE.** A PSU/CTF study already screened correlations by validity range for SMR-160 and selected Bowring + Groeneveld — our exact conclusion. A mechanistic CHF correlation exists for natural circulation at 540–890 kg/m²·s, which brackets our G ≈ 542. Survives only in the narrower framing of ②.

---

## 2. Ranked candidate topics

### ① In-vessel CRDM dissolves the rod-ejection constraint on SBF core design ⭐ RECOMMENDED

**The gap.** Two literatures exist and nobody has connected them:

- SBF cores need high *total* rod worth → forces high *individual* rod worth → severe rod-ejection accident. People actively design around this; there is a 2026 *J. Nucl. Eng.* paper titled *"Optimization Strategies to Improve the Safety Behaviour of a Soluble-Boron-Free SMR Core During a Rod Ejection Accident."*
- Integral PWRs with **in-vessel CRDM eliminate rod ejection by construction** (IRIS, marine reactors, multiple patents).

So an entire optimization literature is constrained by an accident our architecture removes.

**Thesis.** Once REA no longer binds, individual rod worth becomes a free design variable. How far does that get us toward eliminating the boron-injection dependency for cold shutdown?

**Why it is honest.** We are still supercritical cold with all rods in, so cold shutdown is credited to EBIS. We report a **quantified residual boron dependency** rather than overclaiming. Negative results are fine here and make the paper more credible, not less.

**Assets in hand:** 16 CRA @ 90 % B-10, 21,509 pcm bank worth, 7.85 % hot SDM, k_ARI 0.927, validated OpenMC STAT_FINAL model, ICSBEP + BEAVRS validation.
**Extra sims:** rod-worth sweep over CRA count × B-10 enrichment × pattern, hot and cold. Bounded — roughly 1–2 weeks on the existing model.
**Journal:** *Nuclear Engineering and Design* (free subscription route) or *Annals of Nuclear Energy*.
**Risk:** low. Different reviewer pool from MIT.

### ② CHF correlation governance at natural-circulation mass flux under an off-nominal neutronic state

**The gap.** Correlation screening at low G is done. What is *not* done: which correlation should govern **acceptance** when G ≈ 542 kg/m²·s sits below W-3's 1350 kg/m²·s validity floor **and** the neutronic state is simultaneously off-nominal from Gd burnout.

**Framing that survives review.** Lead with **Groeneveld-2006 LUT as the primary metric, W-3 as the conservative bound**. Same numbers, defensible framing. Written the other way round, the W-3 extrapolation becomes the reviewer's central objection.

**What modern reviewers will demand:** uncertainty quantification, not point values. Our four-method spread (W-3 1.33 / Bowring 2.13 / Groeneveld 6.18 — a factor of 4.6) is exactly the raw material for a polynomial-chaos + Sobol' treatment.

**Assets in hand:** Table 8.4-9 four-method closure, 8.4-8 mesh independence (0.05 % outlet ΔT), 8.4-3 riser sweep, OpenFOAM CHT.
**Extra sims:** UQ propagation over pressure, mass flux, power shape. Modest.
**Journal:** NED.
**Risk:** medium — narrower than it first looked, but **the data is largely already in hand**, so it is the fastest route to a submission.

### ③ Lead-free biological shield for an integral PWR

**The gap.** Existing work is either *materials-level* (borated-poly attenuation coefficients, borated concrete with polyethylene aggregate) or *generic PWR*. A **system-level lead-free radial build for integral geometry**, with weight-window MC **cross-verified against an independent point-kernel calculation**, is not covered. Lead-free is well motivated: toxicity, decommissioning, RoHS pressure.

**Assets in hand:** 20 cm borated poly + 180 cm magnetite build; converged MC dose map; MC ↔ point-kernel agreement (downcomer 9.2e9 → RPV 1.6e9 vs 1.59e9 point-kernel anchor); RPV fluence 3.0×10¹⁸ vs 1×10¹⁹ limit; outer dose 0.23 µSv/h; 4 dose-rate zones.
**Extra sims:** essentially none — perhaps a material-variant sweep.
**Journal:** *Annals of Nuclear Energy*, *Nuclear Engineering and Technology*, or *Radiation Physics and Chemistry*.
**Risk:** low-medium. Modest novelty but genuinely self-contained and nearly write-ready.

### ④ Waste intensity of an SBF once-through iPWR

**The gap.** This is a live, contested space — there are published claims that SMR waste per MWh runs **2–30× higher** than large PWRs, plus an INL waste-attributes report finding heavy-metal mass factors of 0.2–1.2 versus a large-PWR reference. Our 4.40 tHM/TWhe vs CAREM-25's 6.43 is a real data point in an active argument.

**Weakness:** two designs is not a paper. Needs 4–6 comparators (NuScale, SMART, CAREM, ACP100, large-PWR reference).
**Journal:** **NET** — its scope explicitly covers fuel cycle and policy. *Annals* rejects policy papers outright.
**Risk:** medium.

### ⑤ ROM as a safety-screening tool

Crowded as a method (§1). Only viable if reframed away from "here is a ROM" toward honest capability grading — k_eff and power-map excellent (R² 0.9925 / 0.9961 / 0.9768), reactivity coefficients only indicative. **Conference, not journal.**

### ⑥ Proliferation / Pu vector

**Data now correct** (§0): Pu-240 is 21.0–21.6 %, genuinely below a 3-batch PWR's 24–26 %.

**But the objection stands.** The causal variable is **discharge burnup**, not batching strategy, and "lower burnup → less degraded Pu" has been textbook since the 1970s. A reviewer says that in one line. The honest framing is that our cycle is *slightly worse* on the intrinsic barrier — defensible as *"the long single-batch cycle SMR vendors adopt for economics carries a small unpriced safeguards cost,"* but modest.

**If we do it:** needs a burnup sweep (3-batch ~44.4 GWd/tHM plus 3–4 intermediate points) pushed through the Bathke FOM pipeline we already built. **Journal:** NET.

### ⑦ MSLB / EBIS — taken (§1). Do not pursue.

### ⑧ TCES + hydrogen cogeneration

Different field entirely. Our own FER classes it as non-safety balance-of-plant screening, and it will not carry a nuclear journal. If pursued: *Applied Thermal Engineering* or *Journal of Energy Storage*, and it needs substantially more development.

---

## 3. Journals and cost

| Journal | Fit | Cost to us |
|---|---|---|
| **Nuclear Engineering and Design** | Best for ① and ② — coupled neutronics/TH design analysis is core scope | **Free** on subscription route; gold OA $3,080 optional |
| **Annals of Nuclear Energy** | ① or ③. Reactor physics + thermal hydraulics | **Free** on subscription route |
| **Nuclear Engineering and Technology** | ③, ④, ⑥ — scope covers fuel cycle, waste, policy | **No APC to 8 pages**, then ~$200/page |
| **EPJ Nuclear Sciences & Technologies** | Where the SBF-SMR conversation actually lives (Flexblue, the 2026 SBF equilibrium paper) | Gold OA, **up to €800**, waivers for Research4Life countries |
| *Progress in Nuclear Energy* | Risky — reserves the right to reject papers that are routine application of codes to produce reactor designs | — |
| *Nuclear Technology* | Q2, and it is where the MIT blocker sits | — |

**Note on "free":** the Elsevier/T&F subscription route costs authors nothing — the article simply is not open access. That is our default. **Someone should check whether our institutional country qualifies for Research4Life**, which would make EPJ-N free *and* open.

---

## 4. Recommended sequence

1. **Now:** commit the missing July-7 waste CSV (§0). Confirm TEKNOFEST rules on publishing competition material. Agree author order.
2. **Weeks 1–2:** run the ① rod-worth sweep while the OpenMC model is still hot.
3. **Weeks 2–5:** draft ① against NED structure.
4. **In parallel:** ② needs mostly writing, not computing — a second person can start it independently.
5. **Later / optional:** ③ is nearly write-ready and is a good first paper for whoever wants one. ⑤ goes to a conference (PHYSOR / ICAPP / NURETH / ANS Winter) — much faster acceptance and a reasonable first publication for a student author.

**Strategy note:** conferences are a legitimate home for the weaker topics. Do not burn the strong topic on one.

---

## 5. Open questions for the team

1. **TEKNOFEST rules** — are we permitted to publish competition material, and does anything need to wait until after the finals?
2. **Author order** — decide now, not at submission. Suggest deciding per-paper, mapped to who owns the work package.
3. **Who runs the ① sweep?** (Neutronics — Samira / Laziz)
4. **Does anyone want ③ as a first-author paper?** It needs the least new work.
5. **Do we spread across journals** or concentrate? Note we are already queuing an LMFR paper at NET — two NET submissions is fine if topics are distinct, but self-cite clearly so reviewers see method reuse, not salami-slicing.
6. **Is anyone able to pull the two Halimi & Shirvan papers in full?** If their five layouts already include an SBF natural-circulation case with a Gd hump, that closes off more than we think — worth knowing this week.

---

## Sources

- Halimi & Shirvan, *Fuel Behavior Implications of Reactor Design Choices in Pressurized Water SMRs*, Nuclear Technology (2024) — [T&F](https://www.tandfonline.com/doi/full/10.1080/00295450.2024.2426416)
- *Impact of core power density on economics of a small integral PWR*, NED (2021) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0029549321004404)
- *Optimization Strategies to Improve the Safety Behaviour of a Soluble-Boron-Free SMR Core During a Rod Ejection Accident*, J. Nucl. Eng. (2026) — [DOI](https://doi.org/10.3390/jne7030043)
- *Reactivity balance for a soluble boron-free small modular reactor*, NET (2018) — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1738573317308161)
- *Analysis of a steam line break accident of a generic SMART-plant with a boron-free core using TRACE/PARCS*, NED (2019) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0029549319301128)
- *Core neutronics and safety characteristics of a boron-free core for Small Modular Reactors*, Annals (2019) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0306454919301951)
- *Mechanistic CHF modeling for natural circulation applications in SMR*, NED (2016) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0029549316304162)
- *Critical Heat Flux Model Improvement in CTF for Natural Circulation Type Reactors* (PSU thesis) — [PSU](https://etda.libraries.psu.edu/catalog/28952)
- *Internal Control Rod Drive Mechanisms, Design Options for IRIS* — [OSTI](https://www.osti.gov/biblio/21160774)
- *Internal shield design in the IRIS reactor* — [NRC](https://www.nrc.gov/docs/ML0336/ML033600080.pdf)
- *Multi-objective optimization of a compact PWR computational model for biological shielding design using innovative materials*, NED (2016) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0029549316304423)
- *Analyzing the sources of radioactive waste from Small Modular Reactors*, (2026) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0149197026000041)
- INL, *SMR waste attributes report* — [INL](https://sai.inl.gov/content/uploads/29/2024/12/smr_waste_attributes_report_final.pdf)
- Bathke et al., *The application of a figure of merit for nuclear explosive utility* — [OSTI](https://www.osti.gov/servlets/purl/1057239)
- EPJ-N instructions for authors (APC) — [EPJ-N](https://www.epj-n.org/author-information/instructions-for-authors)
