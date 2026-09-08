# Relaxing the rod-ejection constraint in soluble-boron-free PWR cores: attainable control-rod worth and residual boron dependency with in-vessel drives

**Authors:**
**S. Achilova**¹'\*, L. Ismailov¹, A. Abdikarimov¹

*(Samira Achilova, Laziz Ismailov, Adilbek Abdikarimov — confirm the spelling and initials of every name before submission.)*

¹ New Uzbekistan University, Tashkent, Uzbekistan

**\*Corresponding author:** S. Achilova, s.achilova@newuu.uz

**Target journal:** *Nuclear Engineering and Design* (Elsevier) — subscription route, no author charges.

> **Draft status.** All numerical results below are computed and archived (see *Data availability*). Items still requiring author action before submission are marked **[TODO]**. Reference volume/page details marked **[verify]** must be checked against the publisher record.

---

## Abstract

Soluble-boron-free (SBF) operation removes the boron-dilution accident, deletes the boron make-up and recovery plant, and makes the moderator temperature coefficient more negative, but it transfers the whole cycle excess reactivity onto the control-rod system. The resulting demand for total bank worth raises individual cluster worth until the rod-ejection accident (REA) becomes design-limiting, and a body of recent work is devoted to optimising SBF cores to survive it. That constraint is a property of the drive-line topology rather than of the core: in an integral PWR with in-vessel control-rod drive mechanisms there is no head penetration, and the pressure-boundary-mediated ejection mechanism assumed for externally mounted drives does not apply. Both features are established individually and coexist in several SMR concepts, but the neutron-physics consequence of *deliberately relaxing the individual-cluster-worth constraint* on that basis has not, to our knowledge, been quantified.

We address that question for a 125 MWth, 37-assembly, 17×17, 2.0 m active-height natural-circulation integral PWR with in-vessel drives, using continuous-energy Monte Carlo (OpenMC 0.15.3, ENDF/B-VIII.0) validated against four ICSBEP LEU-COMP-THERM-008 measured criticals (mean bias −50 pcm, worst case 0.86σ) and against a NuScale-like rod-worth sequence reproduced to within ±80 pcm across 19,400 pcm of total worth. A complete 2 × 2 matrix over two design levers — absorber B-10 enrichment and cluster count — spans 13,409 to 21,509 pcm of bank worth. The levers are approximately additive, with a small but statistically significant positive interaction of +392 pcm. The 12-cluster natural-B₄C base configuration cannot achieve hot shutdown at all (k = 1.00255 with all rods inserted), and either lever alone recovers it: enrichment gives +2.01 % Δk/k and the four added clusters alone give +5.20 %, while both together reach 7.85 %. Of the sixteen clusters, only the four centre-adjacent positions exceed one dollar in single-cluster worth. For context, a published SBF core of near-identical geometry — 37 assemblies, 17×17, 200 cm active height — requires 29 to 37 Ag–In–Cd clusters to reach 14,906 to 20,570 pcm of available worth.

At the top of the ladder the highest-worth cluster is worth 844 ± 82 pcm at hot zero power and 902 ± 34 pcm at full-power fuel temperature; against a directly computed effective delayed-neutron fraction of 704.5 ± 28.2 pcm these are **1.20 ± 0.13 $** and **1.28 ± 0.07 $**. Both exceed one dollar, by 1.5σ and 4.0σ of the combined uncertainty respectively. For an externally driven plant this configuration would require a dedicated rod-ejection transient analysis; it is reachable here because the ejection mechanism does not apply to the in-vessel architecture. The upgrade holds the core subcritical through a main-steam-line-break cooldown to ≈443 K but does not close cold shutdown: with the most reactive cluster stuck, the cold core remains supercritical at k = 1.031, and 771 ppm of emergency boron is still required to reach the k_adj ≤ 0.95 acceptance line, against 3,000 ppm credited in the design. For this core at 43 % rodded fraction, therefore, cold shutdown with a stuck rod rather than rod ejection is the constraint that remains unsatisfied; published results at full-core rodding indicate the cold condition is soluble by rodding more of the core, so the finding characterises partially rodded compact cores rather than boron-free operation in general. The design is boron-free in normal operation — no dilution accident, no boron plant, and the associated moderator-temperature-coefficient benefit — but it is not boron-free as a plant, and we suggest that SBF design reporting should make that distinction explicit. All results are steady-state eigenvalue calculations at beginning of cycle; no transient analysis is performed or claimed.

**Keywords:** soluble-boron-free; small modular reactor; integral PWR; control-rod worth; rod-ejection accident; shutdown margin; Monte Carlo

---

## 1. Introduction

Eliminating soluble boron from the primary coolant of a pressurised water reactor is attractive for several independent reasons. It removes the boron-dilution accident as an initiating event; it simplifies the plant by deleting the boron make-up, recovery and purification trains; it removes a corrosion and crud-deposition driver; and it makes the moderator temperature coefficient (MTC) more negative across the cycle, because the positive boron-density feedback term disappears. These advantages have made SBF operation a recurring feature of small modular reactor (SMR) design studies (Flexblue [1], boron-free SMART-type cores [2,14], ACP100 [3]). We refer throughout to *design studies* rather than to licensed designs: of these, only Flexblue adopts SBF operation as a design commitment, while the SMART-type boron-free cores are research variants of a plant whose licensed configuration uses soluble boron.

The cost is concentrated in one place. A boron-free core must hold its entire cycle excess reactivity with fixed burnable absorbers and movable control rods alone. Burnable absorbers can flatten the reactivity trace but cannot provide shutdown; the shutdown function therefore falls entirely on the rod system, and the required total bank worth rises accordingly. In a conventional PWR, soluble boron supplies several thousand pcm of cold shutdown depth that the SBF designer must find elsewhere.

Raising total bank worth by adding worth to each cluster has a well-known consequence. The rod-ejection accident (REA) — the mechanical failure of a control-rod drive-mechanism pressure housing, expelling one rod at full system pressure — is bounded by the worth of the single highest-worth rod. When that worth exceeds one dollar (the delayed-neutron fraction β_eff), the excursion becomes prompt-critical and the event drives fuel-enthalpy limits. The SBF literature is explicit about this coupling: reported designs need high total worth, which produces individual rod worths large enough that the REA becomes the design-limiting transient, and recent work is devoted to optimising SBF cores specifically to survive it [4,5].

That coupling is not, however, a property of the core. It is a property of where the drive mechanisms are mounted. Integral PWRs with in-vessel control-rod drive mechanisms (CRDMs) place the drive inside the pressure boundary; there is no head penetration to fail and therefore no ejection path. This is a long-standing and explicitly safety-motivated design choice — IRIS adopted internal CRDMs partly to eliminate the REA [6], and in-vessel drives have been developed for marine propulsion reactors for the same reason [7].

Neither observation is new on its own, and it is worth being precise about what is. Soluble-boron-free operation and in-vessel drives already coexist in several integral SMR concepts: mPower, SMR-160 and CAREM are described in exactly those terms [2], the SCOR concept placed its drive mechanisms inside the vessel as early as 2005 [19], and the Korean i-SMR is a boron-free integral PWR with in-vessel CRDMs whose control-rod arrangements are the subject of current work [20,21]. That in-vessel drives remove the conventional ejection mechanism is likewise well established [6,7]. We therefore make no claim to have identified an unexplored architecture.

The closest single antecedent is the Flexblue core study [1], which identifies cold shutdown and rod ejection as the two governing difficulties of boron-free operation, examines B-10 enrichment and the number of rodded assemblies as the available levers, and evaluates the most-reactive-rod-stuck cold condition. Two of its findings bear directly on the present work. First, Flexblue retains the ejection constraint and answers it mechanically, selecting a compact drive incorporating an anti-ejection device — the constraint is mitigated rather than sidestepped by architecture. Second, with **100 % of assemblies rodded**, Flexblue reports that cold shutdown with the most reactive rod stuck is readily achieved, even with natural B₄C or Ag–In–Cd absorber. **The cold-shutdown difficulty is therefore not a universal feature of SBF cores; it is a function of how much of the core is rodded.** A design that can afford a cluster in every assembly can buy its way out of it.

What has not been quantified, to our knowledge, is the intermediate case a compact integral core actually presents. Although SBF studies have extensively investigated the increased bank-worth requirement and the resulting rod-ejection constraint, and integral concepts have demonstrated that in-vessel drives remove the conventional pressure-boundary-mediated ejection mechanism, the neutron-physics consequence of *relaxing the individual-cluster-worth constraint* has not been systematically quantified. In particular, the trade-off between attainable total bank worth and the residual cold-shutdown requirement under a stuck rod, at a rodded fraction well below full-core rodding, has received little attention. Table 1 positions this work against the closest published studies.

**Table 1.** Positioning against the closest published soluble-boron-free control-rod studies. ● = addressed, ○ = not addressed.

| Study | SBF core | In-vessel drives | REA treated as | Worth levers quantified | Cold stuck-rod | Residual boron quantified |
|---|---|---|---|---|---|---|
| Ingremeau & Cordiez 2015 [1] | ● | ○ (anti-ejection device) | constraint, mitigated mechanically | ● B-10, rodded fraction | ● (solved at 100 % rodded) | ○ |
| van der Merwe & Hah 2018 [5] | ● | ○ | not treated | ● cluster count | ● | ○ |
| Alzaben et al. 2019 [2] | ● | noted for mPower/CAREM | transient analysis | ○ | ○ | ○ |
| Song & Sánchez-Espinoza 2026 [4] | ● | ○ | constraint, design optimised to satisfy | ● pattern, hybrid absorber | ○ | ○ |
| KSMR equilibrium core 2026 [20] | ● | ○ | ○ | ● enrichment, BA | ● BOC/MOC/EOC | ○ |
| i-SMR loading pattern 2026 [21] | ● | ● | ○ | ● BA types | ● | ○ |
| **This work** | **●** | **●** | **mechanism not applicable; worth allowed above 1 $** | **● full 2 × 2, B-10 × cluster count** | **● (unresolved at 43 % rodded)** | **● 771 ppm** |

The distinguishing row is the fourth column combined with the last two: no prior study deliberately admits individual cluster worth above one dollar on the grounds that the ejection mechanism does not apply, then asks what constraint replaces it.

This paper addresses that question for a specific reference core. We (i) construct a rod-worth ladder over two independent design levers and quantify the shutdown states each reaches; (ii) compute the ejected-rod worth at the top of the ladder and show that it exceeds one dollar, i.e. that the configuration is only admissible because the drives are in-vessel; and (iii) quantify what remains — the residual soluble-boron requirement for cold shutdown, which the rod upgrade reduces substantially but does not remove. The last result is the practically important one: it identifies cold shutdown with a stuck rod, not rod ejection, as the binding constraint for SBF cores of this class.

## 2. Reference core and computational method

### 2.1 Core description

The reference design is a 125 MWth integral PWR with natural-circulation primary flow and no reactor coolant pumps. The plant design point is 40 MWe net; that figure comes from the balance-of-plant design and is quoted here only to identify the reactor, as no thermal-to-electric conversion is analysed in this paper. The core comprises 37 Westinghouse-type 17 × 17 fuel assemblies on a 21.6038 cm pitch (the value used in the model, set by the assembly envelope and inter-assembly gap; the digits are the modelled geometry, not a claim of manufacturing tolerance) in a 7-wide octagonal arrangement (rows 3-5-7-7-7-5-3), with a 200 cm active height. Pin pitch is 1.2623 cm, pellet radius 0.40958 cm and Zircaloy-4 clad outer radius 0.4760 cm. Heavy-metal loading is 9.39 tHM, giving a specific power of 13.31 W/gHM — roughly one third of a large PWR, which is the origin of the design's thermal margin and of the long single-batch cycle.

Reactivity control uses three static mechanisms in combination. Enrichment is graded radially in three intra-assembly zones at 4.95 / 4.70 / 4.40 wt % U-235, dropping to 4.0 wt % at the core edge, all below the 5 % LEU limit. Burnable absorption is a Gd–Er hybrid. Gadolinia rods at 6 wt % Gd₂O₃ provide strong early hold-down and burn out quickly; their number is zoned radially by ring, at 33 / 29 / 19 / 14 rods per assembly from the centre ring outward, giving a core-average loading of 20 rods per assembly. Sixteen rods per assembly of 0.75 wt % Er₂O₃ deplete slowly, trimming residual reactivity late in life and hardening the resonance absorption that keeps the MTC negative at beginning of cycle. **[verify the ring populations used to form the 20-rod core average.]**

The core is surrounded by a 20 cm radial water reflector and 30 cm axial water plena, with vacuum boundary conditions on all outer surfaces. Nominal operating conditions are 12.8 MPa, a core-average moderator temperature of 556 K (water density 0.748 g/cm³ by IAPWS-IF97) and a fuel temperature of 900 K.

Control-rod cluster assemblies (CRAs) occupy guide-tube positions in a checkerboard pattern. The base configuration has 12 CRAs, with the central assembly reserved as an instrument position. The final configuration adds four clusters in the central cross, using existing guide tubes, for 16 CRAs total (Fig. 1). Absorber is solid B₄C; two absorber variants are considered, natural boron (19.9 at % B-10) and 90 at % enriched B-10. Enriching the *solid* absorber does not reintroduce soluble boron and leaves the SBF claim intact.

> **Figure 1.** Control-rod cluster layout: (a) base 12-CRA checkerboard; (b) final 16-CRA configuration with four clusters added in the central cross. The instrument position is retained. The highest-worth cluster used for the ejected-rod case is outlined.
> `figures/fig1_cra_layout.png`

### 2.2 Monte Carlo model and statistics

All results are continuous-energy Monte Carlo eigenvalue calculations with OpenMC 0.15.3 [8] and ENDF/B-VIII.0 cross sections [9]. The model is fully three-dimensional and explicit at pin level across all 37 assemblies; no assembly homogenisation or few-group condensation is used at any stage. Each case runs 180 batches of 20,000 particles with 50 inactive batches, giving a typical statistical uncertainty of 50–65 pcm on k_eff.

All states reported here are beginning-of-cycle with fresh fuel. BOC is expected to be the limiting condition for the shutdown questions addressed here, because unburned excess reactivity — and hence the demand on the rod system — is highest then. We note, however, that this expectation is not demonstrated by the present calculations: the gadolinia hold-down produces a mid-cycle reactivity maximum in this core, and establishing that the cold stuck-rod state is genuinely bounding at BOC would require the burnup-dependent repeat identified as future work in §6.3. The BOC results should therefore be read as the beginning-of-cycle condition rather than as a demonstrated envelope.

### 2.3 Acceptance metric

Monte Carlo results are graded before comparison with acceptance criteria, using

  k_adj = k + 2σ + 0.005

where σ is the reported statistical standard deviation. The two terms cover different things and are kept separate in intent: 2σ is the Monte Carlo statistical allowance, and the additive 0.005 in k — approximately 500 pcm — is a bias-and-modelling allowance.

The 0.005 value is an authors' conservative design convention, not a regulatory requirement, and we state its basis explicitly because subcriticality claims in §4 and §5 are made on k_adj rather than on the raw eigenvalue. It is intended to envelope two contributions: the nuclear-data and methods bias indicated by the criticality benchmarking of §2.4 (mean −50 pcm, worst case −143 pcm over four cases) and the geometric idealisations of the full-core model, principally the smeared structural material, the absence of grid spacers and the idealised reflector boundary. At 500 pcm it is roughly an order of magnitude larger than the statistical uncertainty and roughly 3.5 times the worst single-case benchmark deviation, so it is deliberately conservative rather than a best estimate. A criticality-safety application would derive such an allowance formally from a validation suite spanning the application's area of applicability; that is beyond the scope of this paper, and the value is used here only to avoid resting subcriticality conclusions on unadjusted eigenvalues. Where the choice affects a conclusion — the 771 ppm boron requirement of §5.2 — the sensitivity is reported.

Uncertainties on differences of eigenvalues (rod worths, and reactivity differences generally) are propagated in quadrature from the contributing statistical uncertainties, and dollar values combine the worth and β_eff uncertainties the same way.

Shutdown margin is reported *signed*, as SDM = −(k − 1)/k, so that a positive value denotes genuine subcritical margin and a supercritical state appears as a negative number. This matters here: several configurations in the ladder are supercritical in the cold stuck-rod state, and an unsigned convention would conceal it.

### 2.4 Code and methodology benchmarking

Two independent checks support the rod-worth results. Both are benchmarks of the computational chain — criticality behaviour and control-rod worth — rather than validation of the Aegis-40 core itself, which is a conceptual design with no experimental counterpart.

*Measured criticals.* Four low-enriched UO₂ light-water lattice benchmarks from the OECD/NEA ICSBEP Handbook, LEU-COMP-THERM-008 [10], were run with the production toolchain. The evaluated benchmark-model eigenvalue is 1.0007 ± 0.0016; computed values were 1.00047, 1.00042, 1.00062 and 0.99927, giving C − E of −23, −28, −8 and −143 pcm respectively. The mean bias is −50 pcm and every case falls within the handbook experimental uncertainty (worst case 0.86σ).

*Rod worth, code-to-code.* Because this paper's central quantity is control-rod worth, the most relevant check is against a published SMR core with documented rod states. The open NuScale-like benchmark deck of the Euratom McSAFER project [11], whose reference solution is Serpent 2 (v2.2) with ENDF/B-VII.1, was run in six control-rod configurations spanning approximately 19,400 pcm of total worth. Agreement with the reference Serpent solution is within ±80 pcm at every state (all-rods-out −6 pcm, all-rods-in −80 pcm, intermediate states +18 to +58 pcm), i.e. within about 2σ combined. Rod worths lie on the parity line over a range wider than the ladder examined here.

Depletion is not used anywhere in this paper — all states are beginning-of-cycle — so no depletion benchmarking is claimed in support of these results.

## 3. The rod-ejection constraint

### 3.1 Ejected-rod worth of the reference core

The ejected-rod case was evaluated at the final 16-CRA, 90 % B-10 configuration in two independently constructed OpenMC models, both taking the bounding cluster nearest the core centre and measuring the difference between the all-rods-out state and the state with that single cluster inserted.

SRP 15.4.8 requires the ejected-rod case at both hot zero power and hot full power, so both are reported.

| Case | absorber | evaluation state | worth | in dollars |
|---|---|---|---|---|
| **Reference design, HZP** | 90 % B-10 | isothermal, 556 K | **844 ± 82 pcm** | **1.20 ± 0.13 $** |
| **Reference design, hot fuel** | 90 % B-10 | fuel 900 K | **902 ± 34 pcm** | **1.28 ± 0.07 $** |
| Absorber sensitivity | natural B₄C | fuel 900 K | 794 ± 48 pcm | 1.13 ± 0.08 $ |

β_eff was computed for this core rather than assumed (§3.2), giving 704.5 ± 28.2 pcm. The two evaluation states differ by the Doppler reactivity between them; both place the ejected-rod worth above one dollar, so the conclusion does not depend on the choice.

### 3.1.1 The bounding cluster is identified, not assumed

The cluster used above is the one nearest the core centre. That it is the maximum-worth position was verified rather than presumed. Under the 8-fold dihedral symmetry of the core map the sixteen CRA positions collapse into three equivalence classes, and because enrichment and gadolinia are both zoned by ring, positions within a class are neutronically equivalent. One representative of each class was evaluated at full statistics, together with a second member of the largest class as an explicit symmetry check (Table 2).

**Table 2.** Single-cluster worth by symmetry class, measured from the all-rods-out state at fuel 900 K / moderator 556 K with 90 at % B-10 absorber. k(ARO) = 1.15042 ± 24 pcm. Dollars use β_eff = 704.5 ± 28.2 pcm (§3.2).

| Symmetry class | Positions in class | Representative | Worth (pcm) | In dollars |
|---|---|---|---|---|
| **(0,1) — centre-adjacent** | **4** | **(3,2)** | **902 ± 26** | **1.28 ± 0.06** |
| (0,2) — added central-cross clusters | 4 | (3,5) | 669 ± 26 | 0.95 ± 0.05 |
| (1,2) — outer checkerboard | 8 | (2,1) | 556 ± 25 | 0.79 ± 0.05 |
| (1,2) — symmetry check | — | (4,1) | 535 ± 26 | 0.76 ± 0.05 |

Three points follow. The symmetry check agrees to 21 pcm against a combined uncertainty of 36 pcm, i.e. **0.6σ**, confirming that positions within a class may be treated as equivalent. The centre-adjacent class is the maximum by 233 pcm over the next class, a separation of **6.3σ**, so the bounding position is unambiguous. And the value obtained for it, 902 ± 26 pcm, reproduces the independent determination of §3.1 to within 1 pcm.

The distribution also qualifies the headline result usefully. **Only the four centre-adjacent clusters exceed one dollar**; the four added central-cross positions sit at 0.95 $ and the eight outer positions between 0.76 and 0.79 $. Twelve of the sixteen clusters would therefore be admissible under a conventional ejection constraint. What the in-vessel architecture buys is not a uniformly high-worth bank but the freedom to place four clusters where the neutron importance is greatest.

### 3.1.2 The screening basis

The unshadowed single-cluster worth measured from an all-rods-out state is used as a conservative screening estimate of the worth available to an ejection from a partially inserted bank position. It is not proven here to be a strict upper bound: rod worth depends on neighbouring insertion, axial shape, temperature and burnup, and a formal bounding argument would require those dependencies to be swept.

Subject to those qualifications, the reference configuration exceeds one dollar on both evaluation bases, and the unenriched-absorber sensitivity does so as well. In dollars the two reference cases sit 1.5σ and 4.0σ above unity on the combined worth-and-β_eff uncertainty; the hot-fuel case is therefore the robust one, and the HZP case, at 1.20 ± 0.13 $, is above one dollar but not decisively so. For a plant with externally mounted CRDMs this would require a dedicated rod-ejection transient analysis against fuel-enthalpy limits (NUREG-0800 SRP 15.4.8; RG 1.77) rather than a static comparison of this kind, and would plausibly force a design retreat: fewer or weaker clusters, a more distributed pattern, or bank-insertion limits that reduce the worth available for ejection. Each of those retreats costs total bank worth — the very quantity the SBF core needs. We make no claim here about the outcome of such a transient analysis, only that it would be required.

### 3.2 Effective delayed-neutron fraction

Because the acceptance question is a comparison against one dollar, β_eff was computed for this core
rather than taken from the literature. Two eigenvalue calculations were run at the identical state
(BOC, HFP, all rods out) at higher statistics than the ladder cases — 400 batches of 50,000 particles
with 80 inactive batches, about 1.6 × 10⁷ active histories — one with delayed neutrons produced normally and one
with every fission neutron forced prompt, giving

  k = 1.150421 ± 0.000239,  k_p = 1.142316 ± 0.000222,  β_eff = 1 − k_p/k = **704.5 ± 28.2 pcm**

This is the prompt-k Monte-Carlo estimate rather than an adjoint-weighted iterated-fission-probability
value — OpenMC 0.15.3 exposes no IFP tally scores through its Python API — and the two methods
typically agree to within a few per cent for light-water lattices. The computed value is about 8 %
above the 650 pcm often quoted for low-enriched UO₂ PWRs. Because the dollar is ρ/β_eff, the larger
computed β_eff *reduces* the dollar figure of §3.1 rather than raising it: the hot-fuel ejected-rod
worth is 1.28 $ against the computed value where the 650 pcm figure would have given 1.39 $. Using
the core's own β_eff is therefore the less favourable choice for the argument made here, and the
conclusion that the worth exceeds one dollar survives it.

Because β_eff directly determines that conclusion, its robustness is worth stating explicitly rather
than leaving to the quoted uncertainty. For the hot-fuel case to fall to exactly one dollar, β_eff
would have to be 902 pcm — 197 pcm, or 7.0σ, above the computed value, and 39 % above the 650 pcm
literature figure. For the HZP case the corresponding threshold is 844 pcm, 4.9σ above the computed
value. Prompt-k and IFP estimates for light-water lattices differ by of order a few per cent, far
short of either threshold, so the conclusion is not sensitive to the choice of β_eff method within
its plausible range. An independent IFP or perturbation-theory calculation would nonetheless remove
the residual methodological objection, and is recommended before the dollar comparison is relied upon
for any licensing purpose.

### 3.3 Consequence of drive-line topology

In the reference design the CRDMs are located inside the reactor pressure vessel. There is no head penetration housing a drive rod, and therefore no drive-housing pressure-boundary rupture that can expel a cluster from the core at system pressure.

It is worth separating two claims that are easily conflated. The first is architectural: *the conventional pressure-boundary-mediated rod-ejection mechanism assumed for externally mounted PWR CRDMs is not applicable to an in-vessel configuration.* That claim follows from the absence of the penetration and is the one this paper makes. The second is a general safety claim — that rapid positive reactivity insertion is excluded as a class — and we do not make it. In-vessel drives introduce their own failure modes that a complete safety case would have to address: drive-to-rod decoupling and the resulting rod drop, internal mechanical failure producing rapid rod motion, and drive malfunction causing uncontrolled withdrawal. Uncontrolled bank withdrawal in particular remains a design-basis event, bounded by drive speed rather than by single-rod worth. Establishing the maximum credible reactivity insertion rate for a specific in-vessel mechanism is a mechanical-design question outside the scope of this paper.

Subject to that first, narrower claim, the consequence for core design is direct: the 1.20–1.28 $ result of §3.1 is not an acceptance failure but an observation about a configuration that an external-drive plant could not adopt without dedicated transient analysis. Individual cluster worth ceases to be a constrained design variable, and total bank worth can be pursued by whatever combination of cluster count, absorber enrichment and pattern is neutronically most effective. Sections 4 and 5 quantify what that freedom is worth, and what it does not solve.

In-vessel drives also carry an engineering burden of their own — in-service inspection, maintainability and qualification of an electromechanical component inside the pressure boundary — which is outside the scope of this paper but is a real trade against the neutronic freedom gained.

## 4. Attainable bank worth

Table 3 and Fig. 2 give the ladder, evaluated as a complete 2 × 2 matrix over the two design levers — absorber enrichment {natural, 90 at % B-10} × cluster count {12, 16}. Total bank worth spans 13,409 to 21,509 pcm, a 60 % increase over the base configuration.

Measuring each lever at both settings of the other separates the effects and quantifies their interaction:

| | at 12 CRA | at 16 CRA |
|---|---|---|
| **Enrichment lever** (natural → 90 % B-10) | +2,264 pcm | +2,656 pcm |
| **Cluster-count lever** (12 → 16) | +5,444 pcm *(natural)* | +5,836 pcm *(90 % B-10)* |

The two levers are therefore **approximately but not exactly additive**. The interaction term, (16 B-10 − 12 B-10) − (16 natural − 12 natural), is **+392 pcm**: enriching the absorber is worth 17 % more when sixteen clusters are present than when twelve are, and adding four clusters is worth 7 % more when the absorber is enriched. Against a statistical uncertainty of about 32 pcm on each bank worth the interaction is roughly 9σ, so it is a real effect rather than noise, but it is small beside either main effect. Bank worth may be estimated by adding the two lever contributions with an accuracy of a few hundred pcm; it should not be assumed exactly separable. An independent full-power-fuel evaluation of the same configuration gives 21,479 pcm, the 30 pcm difference confirming that bank worth is insensitive to the evaluation state.

**Table 3.** Rod-worth ladder and shutdown states, evaluated at isothermal hot zero power (fuel = moderator) — the physically consistent state for a rods-in condition — so that the four configurations are directly comparable. All values BOC, fresh fuel; k(ARO) = 1.15826 at this state throughout. SDM signed, positive = subcritical.

| Configuration | Bank worth (pcm) | k (HZP, all in) | Hot SDM (%) | k (cold, all in) | k (cold, stuck rod) | Cold stuck SDM (%) |
|---|---|---|---|---|---|---|
| 12 CRA, natural B₄C | 13,409 | 1.00255 | −0.25 | 1.09798 | 1.11422 | −10.25 |
| 12 CRA, 90 % B-10 | 15,673 | 0.98031 | +2.01 | 1.08147 | 1.09796 | −8.92 |
| 16 CRA, natural B₄C | 18,853 ± 32 | 0.95053 | +5.20 | — | 1.05622 | −5.32 |
| **16 CRA, 90 % B-10** | **21,509** | **0.92725** | **+7.85** | — | **1.03115** | **−3.02** |

> **Figure 2.** (a) Attainable bank worth and the contribution of each lever; (b) hot and cold shutdown states across the ladder. The cold stuck-rod state remains supercritical at every point on the ladder.
> `figures/fig2_rod_worth_ladder.png`

Two features are worth drawing out.

The base configuration **fails hot shutdown outright**. With natural-boron absorber and 12 clusters, the all-rods-in hot state is k = 1.00255 — supercritical. A boron-free core of this excess reactivity cannot be tripped by that rod system at all; the reactor is not merely short of margin but unable to shut down by rods.

**Either lever alone recovers it.** Absorber enrichment at fixed cluster count gives k = 0.98031 (+2.01 %), and the four added clusters with unenriched absorber give k = 0.95053 (+5.20 %). Enrichment is therefore not a prerequisite for hot shutdown in this core — the cluster count is the more powerful of the two levers, and enrichment buys margin rather than capability. Applying both reaches k_adj = 0.93338 and a hot shutdown margin of 7.85 % Δk/k. We do not compare this against a generic numerical shutdown-margin criterion: the applicable margin depends on the regulator, the plant category, the initial condition and the single-failure assumption, and IAEA SSR-2/1 Requirement 46 states the shutdown function in terms of effectiveness, speed and margin under operational and accident conditions rather than as a single threshold.

The cold stuck-rod state improves monotonically but **remains supercritical across the entire ladder**. Increasing rod worth reduces k from 1.11422 to 1.03115 — a gain of 7.2 percentage points in signed SDM, from −10.25 % to −3.02 % — but does not achieve shutdown at any point. The 8,100 pcm of additional bank worth bought by both levers together is not enough to close a gap that the cold-to-hot moderator density swing opens.

### 4.1 Comparison with a published SBF core of the same geometry

The cluster-count requirement can be placed against published work on a nearly identical core. van der Merwe and Hah [5] report a reactivity balance for a soluble-boron-free SMR at 180 MWth with 37 fuel assemblies, Westinghouse 17×17 lattice, 200 cm active height and 4.95 w/o enrichment — the same core geometry as the present design at a different power rating. Using Ag–In–Cd control element assemblies (CEAs) they find that 37 CEAs give 20,570 pcm of available worth with the highest-worth rod stuck at cold zero power, and that a reduced 29-CEA arrangement gives 14,906 pcm against a net requirement of 12,354 pcm.

Figure 3(a) places both studies on the same axes. The present core reaches 21,509 pcm from **16** clusters. Two caveats bound the comparison: the reference worths are N−1 values evaluated at cold zero power whereas ours are full-bank worths at hot zero power, and the two cores differ in thermal power and therefore in cycle excess reactivity. Because of those differences we draw only the weaker conclusion the data support: the comparison suggests that substantially higher total bank worth can be obtained from fewer cluster positions with a 90 % B-10 enriched B₄C absorber than with Ag–In–Cd, while noting that the reported worth definitions and evaluation states are not directly equivalent. A like-for-like statement would require recomputing the reference core on a common basis, which we have not done.

That economy is not free, and its price is exactly the quantity the ejection event constrains. Concentrating comparable bank worth into fewer clusters raises the worth of each, and Fig. 3(b) shows where this places the design relative to the one-dollar line. SBF studies working under an REA constraint have reason to stay below that line; the present configuration sits above it, which is a position available to this architecture but not to an externally driven one.

> **Figure 3.** The soluble-boron-free control-rod design space.
> **(a)** Attainable total bank worth against cluster count: this work as a complete 2 × 2 matrix (circles; open = natural B₄C, filled = 90 at % B-10; vertical arrows give the enrichment lever measured at each cluster count) and van der Merwe and Hah [5] (squares). The near-parallel lever lines show the two effects to be approximately additive; the interaction term is +392 pcm (§4). Reference values are N−1 available worths at cold zero power; present values are full-bank worths at hot zero power, so the panel indicates the *cluster-count* requirement rather than a like-for-like worth comparison.
> **(b)** Maximum single-cluster worth on the dollar scale, using the computed β_eff = 704.5 ± 28.2 pcm of §3.2; error bars are the propagated 1σ Monte Carlo uncertainty. Configurations left of the 1 $ line are admissible with externally mounted drives, and the published SBF optimisation literature works to remain there [2,4]; the region to its right is reachable only where the drive-line topology eliminates the ejection path. All three configurations of the present core lie to the right of the line.
> `figures/fig3_design_space.png`

## 5. Residual soluble-boron dependency

### 5.1 Cold shutdown

The physical reason the cold state resists is the moderator density change. Cooling from 556 K to 294 K raises water density from 0.748 to 1.003 g/cm³; in a core designed around a strongly negative MTC, that density increase inserts a large positive reactivity. In a conventional PWR this is absorbed by soluble boron, whose worth also rises with water density. A boron-free core has no such compensating term, and the rods must cover the entire swing with a stuck-rod allowance on top.

For the reference core the swing is of order 10,000 pcm. The 16-CRA bank covers most of it — enough to keep the *hot* state deeply subcritical — but leaves k = 1.03115 in the cold stuck-rod configuration.

### 5.2 Emergency boron requirement

The design provides an Emergency Boron Injection System (EBIS) as the second, diverse shutdown system required by IAEA SSR-2/1 Requirement 46. Its actual requirement was quantified by sweeping soluble boron concentration at the cold stuck-rod endpoint (Table 4).

**Table 4.** Emergency boron requirement at the cold (294 K) stuck-rod state, 16 CRA, 90 % B-10. The 700–900 ppm points bracket the acceptance crossing directly.

| Boron (ppm) | k_eff | k_adj | Acceptance (k_adj ≤ 0.95) |
|---|---|---|---|
| 0 | 1.03115 | 1.0374 | fail |
| 500 | 0.97205 | 0.9781 | fail |
| **700** | **0.95110** | **0.9566** | **fail** |
| **800** | **0.94183** | **0.9473** | **pass** |
| **900** | **0.93280** | **0.9383** | **pass** |
| 1000 | 0.92278 | 0.9288 | pass |
| 1500 | 0.88273 | 0.8889 | pass |
| 2000 | 0.84489 | 0.8510 | pass |

The acceptance crossing is bracketed directly by the 700 and 800 ppm points, placing the requirement at **771 ppm**. Linear interpolation across the wider 500–1000 ppm interval would have given 785 ppm, so the coarser estimate was conservative by 14 ppm, or 1.8 %. The k_adj(boron) relation is smooth but not strictly linear — successive 500 ppm increments give −0.0593, −0.0493, −0.0399 and −0.0379 in k_adj as self-shielding progresses — which is why the crossing was determined directly rather than interpolated across the gap. The requirement is also a function of the k_adj definition of §2.3: dropping the 0.005 allowance and interpolating on k + 2σ instead moves it to approximately 730 ppm. The design credits 3,000 ppm, which reaches k_adj = 0.790 — a factor of 3.9 margin on the concentration actually required. For comparison, an independent sweep at the cold all-rods-*out* state (no rod credit at all) requires 2,040 ppm to reach criticality, so the rod system is carrying the substantial majority of the cold shutdown duty even though it cannot complete it alone.

### 5.3 Reactivity response along an assumed MSLB cooldown path

Among design-basis events, main-steam-line break is the overcooling transient conventionally taken to drive a PWR core furthest toward the cold condition, and we adopt it here as the motivating scenario for the temperature range examined.

**What follows is not a transient calculation.** No coupled thermal-hydraulic model was run: there is no pressure or flow history, no break boundary condition, no heat-transfer or void modelling, and no kinetics feedback. What is computed is a sequence of independent steady-state eigenvalue calculations at successive moderator temperatures between 556 K and 294 K, with the most reactive cluster stuck out — that is, the *quasi-static reactivity response along an assumed cooldown temperature path*. The temperature path itself is prescribed, not derived, and a plant-specific MSLB analysis would be required to establish the actual path and its endpoint. The results below should be read accordingly: they characterise the core's reactivity as a function of moderator temperature, not the outcome of a steam-line break.

> **Figure 4.** (a) Quasi-static reactivity response along the assumed cooldown path with the most reactive cluster stuck out, base versus final configuration; (b) emergency boron requirement at the cold endpoint.
> `figures/fig4_mslb_and_ebis.png`

The difference is qualitative rather than incremental. In the base configuration the core is supercritical at *every* temperature examined, beginning at k = 1.0183 at 556 K — the rods cannot hold it even at hot conditions. In the final configuration the core is subcritical from 556 K down to approximately 443 K on the graded metric (≈431 K on the raw eigenvalue), and reaches only k = 1.03115 at 294 K rather than 1.11422. The 443 K crossing is a property of the reactivity-versus-temperature curve; whether a given transient actually reaches that temperature is a thermal-hydraulic question this paper does not answer.

This is worth stating plainly because it reconciles the present design with the SBF literature. Published analyses of boron-free cores report that high rod worth largely removes the steam-line break as a re-criticality concern [13,14], and that is consistent with what we find: the rods do handle the transient over most of its range. What they do not handle is the deep cold endpoint, and it is there — not in the return-to-power phase — that the diverse boron system is actually required.

## 6. Discussion

### 6.1 Which criterion binds

For the reference core the results reorder the constraint hierarchy. The rod-ejection mechanism that bounds individual cluster worth in the published SBF optimisation literature does not apply to this architecture, and the configuration reached — 1.20–1.28 $ single-cluster worth — is one an externally driven plant could not adopt without dedicated transient analysis. Cold shutdown with a stuck rod, by contrast, remains unsatisfied even after both rod-worth levers examined here are exhausted.

This last conclusion must be stated with its scope attached, because a third lever exists that we did not exercise. Sixteen clusters in thirty-seven assemblies is a rodded fraction of 43 %. Flexblue reports that at **100 %** rodding, cold shutdown with the most reactive rod stuck is readily achieved even with natural B₄C or Ag–In–Cd [1]. The cold-state problem is therefore not intrinsic to boron-free operation: it is a function of rodded fraction, and it is soluble by rodding more of the core. What the present results show is that at a rodded fraction typical of a compact integral core — where guide-tube positions, in-vessel drive count and instrument positions all compete — the two levers available *within* a fixed cluster layout do not close it. The design choice is then between rodding substantially more of the core and crediting a small diverse boron system.

The practical implication is that for integral designs with in-vessel drives, the relative importance of the REA constraint may change, while the cold-state reactivity swing — which receives comparatively little attention at partial rodding — can become the limiting problem. Design responses that act on *that* problem — a higher rodded fraction, heavier reflectors to reduce the density-swing sensitivity, spectral-shift devices, higher erbium loading, or simply accepting a small credited boron system — are the ones that move the constraint.

### 6.2 What "soluble-boron-free" means

The reference design is boron-free in normal operation: there is no boron in the coolant at power, no dilution accident, no boron recovery plant, and the MTC benefits accordingly. It is not boron-free as a plant. A diverse boron injection system is required, is credited, and is sized at 3,000 ppm against a computed requirement of 771 ppm.

We suggest this distinction should be made explicitly in SBF design reporting. The advantages claimed for SBF operation — dilution-accident elimination, MTC improvement, plant simplification — all follow from the absence of boron *during operation* and survive intact. Claims of complete boron elimination do not, at least for cores with the excess reactivity implied by a long single-batch cycle.

### 6.3 Limitations

Six limitations bound the strength of these conclusions.

*No transient analysis anywhere in this work.* Every result is a steady-state eigenvalue calculation. The ejected-rod worth of §3.1 is a static screening quantity compared against β_eff; no point-kinetics or coupled calculation was performed and no fuel-enthalpy result is claimed. The cooldown results of §5.3 are likewise a sequence of independent temperature-state eigenvalues along a prescribed path, not a steam-line-break transient. The statements made are conditional ones — that an external-drive plant would require such analysis for this configuration — and not findings about transient outcomes.

*Cluster worths are resolved by symmetry class, not individually.* §3.1.1 computes one representative of each of the three symmetry classes rather than all sixteen positions, relying on the ring-zoned enrichment and gadolinia to make positions within a class equivalent. The explicit symmetry check agrees to 0.6σ, and the 6.3σ separation between the leading class and the next makes the identification of the bounding cluster robust, but a full sixteen-position sweep has not been performed.

*Evaluation state.* The ladder and the HZP ejected-rod case are evaluated at isothermal hot zero power, i.e. fuel at moderator temperature. This is the physically consistent state for a rods-in condition — the reactor is shut down, so the fuel is not at full-power temperature — and it is the conventional basis for shutdown-margin reporting. Quantities that *are* full-power properties (k at BOL, the reactivity coefficients, burnup and cycle length) are taken from a separate full-power calculation. Where the two states are compared in §3.1 and §4, the difference is the Doppler reactivity between them (~590 pcm) and is reported explicitly rather than reconciled away.

*β_eff is a prompt-k estimate.* §3.2 uses the prompt-k method (k_p with delayed neutrons suppressed) rather than adjoint-weighted iterated fission probability, which this code version does not expose. The two typically agree within a few per cent for light-water lattices, but an IFP or perturbation-theory cross-check would further strengthen the dollar comparison.

*Single core, BOC only.* One core size, one lattice type and one absorber strategy are examined, at beginning of cycle. The BOC cold state is the bounding one for the shutdown questions asked, but the ladder's generality to other core sizes is asserted rather than demonstrated.

*Ladder is a full factorial over two levers, but is not an optimisation.* The 2 × 2 matrix is complete and the interaction term is resolved (§4), but four configurations are compared, not optimised. Cluster pattern was not varied: a redistributed 16-cluster pattern might reach a different worth, and the four added positions were chosen for guide-tube availability rather than by search. The results therefore describe a design-space *slice* for one representative 125 MWth integral PWR, holding absorber radius and density, B₄C composition, cluster geometry, burnable-absorber loading, enrichment distribution, reflector thickness and core dimensions all fixed. No claim is made about a global optimum or about the SBF design space in general.

## 7. Conclusions

1. For a 125 MWth soluble-boron-free integral PWR, total control-rod bank worth can be raised from 13,409 to 21,509 pcm by two levers — absorber B-10 enrichment and cluster count — without introducing soluble boron. Measured as a complete 2 × 2 matrix, the levers are approximately additive: enrichment is worth +2,264 pcm at 12 clusters and +2,656 pcm at 16, cluster count is worth +5,444 pcm with natural absorber and +5,836 pcm with enriched, and the interaction between them is +392 pcm, about 9σ and small beside either main effect.

2. The base 12-cluster natural-boron configuration cannot achieve hot shutdown at all (k = 1.00255 with all rods inserted). Either lever alone recovers it — enrichment to +2.01 % Δk/k, the four added clusters to +5.20 % — so cluster count is the more powerful lever and enrichment buys margin rather than capability. Both together reach 7.85 % Δk/k.

3. The bounding cluster is identified rather than assumed: single-cluster worths resolve into three symmetry classes at 902 ± 26, 669 ± 26 and 556 ± 25 pcm, the leading class separated from the next by 6.3σ, and only those four centre-adjacent positions exceed one dollar. At the final configuration that cluster has an ejected-rod worth of 844 ± 82 pcm at hot zero power and 902 ± 34 pcm at full-power fuel temperature. Against a computed β_eff of 704.5 ± 28.2 pcm these are 1.20 ± 0.13 $ and 1.28 ± 0.07 $, exceeding one dollar by 1.5σ and 4.0σ respectively. Reversing that conclusion would require β_eff to be 4.9σ to 7.0σ above the computed value. The configuration is reachable here because the pressure-boundary-mediated ejection mechanism does not apply to in-vessel drives; for an externally driven plant it would require a dedicated rod-ejection transient analysis, whose outcome this work does not predict.

4. The rod upgrade does not close cold shutdown. With the most reactive cluster stuck, the cold core remains supercritical at k = 1.03115 (signed SDM −3.02 %), improved from −10.25 % but not resolved.

5. A residual emergency boron requirement of 771 ppm therefore persists, against 3,000 ppm credited — a factor of 3.9. At this rodded fraction — 16 clusters in 37 assemblies, or 43 % — cold shutdown with a stuck rod, not rod ejection, is the constraint that remains unsatisfied. Published work reports that full-core rodding resolves the cold condition even with unenriched absorber [1], so the finding is a statement about partially rodded compact cores rather than about boron-free operation as such.

## Acknowledgements

The reference core was developed for the TEKNOFEST 2026 Detailed Design Competition (Nuclear — 40 MWe Modular PWR). The authors thank the Aegis-40 team at New Uzbekistan University for the plant-level design context within which this core analysis was carried out.

## Data availability

The core model, the run scripts and the complete result files for every eigenvalue reported here are archived at Zenodo, together with SHA-256 checksums for each file: **[Zenodo DOI to be inserted on deposit]**. The archive contains the locked OpenMC model and its case suite, the scripts for the single-cluster worth, lever-matrix and boron-sweep cases, the four manuscript figures at publication resolution, and the generating script for Fig. 3. Code is released under the MIT licence and result files and figures under CC BY 4.0.

A model-reproduction check is included in the archive: six published states were recomputed independently, of which four reproduce to 0 pcm and the worst deviates by 1.3σ.

## References

1. Ingremeau, J.-J., & Cordiez, M. (2015). Flexblue® core design: optimisation of fuel poisoning for a soluble boron free core with full or half core refuelling. *EPJ Nuclear Sciences & Technologies*, **1**, 11. https://doi.org/10.1051/epjn/e2015-50025-3 ✅ *verified* — Flexblue is 550 MWth / 160 MWe.
2. Alzaben, Y., Sánchez-Espinoza, V. H., & Stieglitz, R. (2019). Analysis of a control rod ejection accident in a boron-free small modular reactor with coupled neutronics/thermal-hydraulics code. *Annals of Nuclear Energy*, **134**, 114–**[verify end page]**. ✅ *verified* — 330 MWth, 57-assembly boron-free core, PARCS/SUBCHANFLOW. **Replaces the previous SMART citation, which was inaccurate: the licensed SMART design uses soluble boron; only research variants are boron-free.**
3. Wang, L., Ju, H., Li, Q., Qin, D., Wang, L., Yu, Y., Ning, Z., Wang, C., Guo, R., Wang, S., Zhang, B., Xiang, H., Lou, L., & Sun, W. (2021). Multiple choices of reactor core nuclear design for ACP100's application in different scenarios. *EPJ Web of Conferences*, **247**, 19002 (PHYSOR 2020). ✅ *verified* — Nuclear Power Institute of China; ACP100 is 125 MWe, and the paper presents a boron-free option alongside a boron-and-rod co-controlled option.
4. Optimization Strategies to Improve the Safety Behaviour of a Soluble-Boron-Free SMR Core During a Rod Ejection Accident. *J. Nucl. Eng.* 7(3) (2026) 43. https://doi.org/10.3390/jne7030043
5. van der Merwe, L., & Hah, C. J. (2018). Reactivity balance for a soluble boron-free small modular reactor. *Nuclear Engineering and Technology*, **50**(4), 648–653. https://doi.org/10.1016/j.net.2018.01.019 ✅ *verified*
6. Internal control rod drive mechanisms, design options for IRIS (2004). Conference paper; OSTI 21160774. ✅ *record and year confirmed* — IRIS is a 335 MWe integral PWR; the paper states that RCCA ejection is eliminated by locating the drives inside the vessel. **⚠ [author list still required — take it from the OSTI record before submission]**
7. Development of in-vessel type control rod drive mechanism for marine reactor. *Journal of Nuclear Science and Technology*, **38**(7) (2001), 557–570 **[verify page range]**. https://doi.org/10.1080/18811248.2001.9715067 ✅ *verified*
8. Romano, P.K., et al. OpenMC: A state-of-the-art Monte Carlo code for research and development. *Ann. Nucl. Energy* 82 (2015) 90–97.
9. Brown, D.A., et al. ENDF/B-VIII.0. *Nucl. Data Sheets* 148 (2018) 1–142.
10. International Handbook of Evaluated Criticality Safety Benchmark Experiments, LEU-COMP-THERM-008. NEA/NSC/DOC(95)03.
11. Fridman, E. (2023). *Dataset for neutronics benchmark of a NuScale-like core.* RODARE (Rossendorf Data Repository), Helmholtz-Zentrum Dresden-Rossendorf, record 2457, 30 August 2023. https://rodare.hzdr.de/record/2457 ✅ *verified* — the Euratom McSAFER benchmark; reference solution is Serpent 2 (v2.2) with ENDF/B-VII.1. *(An independent OpenMC study of this same benchmark exists — Simulation of NuScale-like SMR benchmark with OpenMC, J. Nucl. Eng. 6(4) 44 — and is worth citing alongside §2.4 as prior OpenMC work on the reference case.)*
12. Romano, P.K., et al. *Ann. Nucl. Energy* 152 (2021) 107989.
13. Alzaben, Y., Sánchez-Espinoza, V. H., & Stieglitz, R. (2019). Analysis of a steam line break accident of a generic SMART-plant with a boron-free core using the coupled code TRACE/PARCS. *Nuclear Engineering and Design*, **350**, 33–42. ✅ *verified*
14. Alzaben, Y., Sánchez-Espinoza, V. H., & Stieglitz, R. (2019). Core neutronics and safety characteristics of a boron-free core for small modular reactors. *Annals of Nuclear Energy*, **132**, 70–81. ✅ *verified*
15. U.S. NRC, NUREG-0800 Standard Review Plan, SRP 15.4.8 (rod ejection).
16. U.S. NRC, Regulatory Guide 1.77.
17. IAEA, SSR-2/1 (Rev. 1), Safety of Nuclear Power Plants: Design, Requirement 46.
18. Halimi, A., Shirvan, K. Fuel Behavior Implications of Reactor Design Choices in Pressurized Water SMRs. *Nucl. Technol.* (2024). https://doi.org/10.1080/00295450.2024.2426416
19. IAEA (2005). *Innovative Small and Medium Sized Reactors: Design Features, Safety Approaches and R&D Trends.* IAEA-TECDOC-1451 — SCOR concept, soluble-boron-free with in-vessel CRDMs. ✅ *record confirmed* — **[verify the page range for the SCOR section]**
20. Song, Y., & Sánchez-Espinoza, V. H. (2026). Safety-related investigations designing a soluble-boron-free small modular reactor core at equilibrium. *EPJ Nuclear Sciences & Technologies*, **12**, 6. ✅ *verified* — Karlsruhe Institute of Technology; the academic KSMR core, two-batch equilibrium, CASMO5/SIMULATE5; evaluates cold shutdown with the highest-worth rod stuck at BOC/MOC/EOC.
21. Latoch, M., & Yoon, J. (2026). Loading pattern design of the soluble boron-free SMR using LEU+ fuel and multitype burnable absorbers. *EPJ Nuclear Sciences & Technologies*, **12**, 18. https://doi.org/10.1051/epjn/2026004 ✅ *verified* — KEPCO International Nuclear Graduate School; fully soluble-boron-free i-SMR operation using gadolinia in HIGA and IGD rods together with erbia in LEU+ fuel.
22. Lee, W. J., et al. (2025). Application and analysis of Cr-coated GdN-CBA to i-SMR core with two control rod patterns for load-following operations. *Nuclear Engineering and Technology*, published online 1 November 2025. ✅ *record confirmed* — i-SMR control-rod pattern study; a 24-finger cluster of 20 Inconel-625 and 4 Ag–In–Cd fingers, ~37-month cycle. **[complete the author list, volume and pages from the publisher record]**
