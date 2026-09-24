# Revision plan — rod-worth / in-vessel-CRDM paper

**Date:** 2026-09-24 · **Target:** *Annals of Nuclear Energy* · **Status:** not ready to submit

This plan responds to an external referee-style review of the current draft. Every
claim in it that could be checked has been checked against our own files; the
verification is recorded below so it does not have to be repeated.

---

## Bottom line

One finding is on the critical path. Everything else is parallel work.

The paper's thesis — *cold stuck-rod shutdown, not the rod-ejection accident, is
what binds at partial rodding* — **survives and gets stronger**. A larger boron
requirement makes the binding constraint more binding.

What is at risk is the secondary reassurance: *"771 ppm against 3,000 ppm
credited, a factor of 3.9."* That number will shrink, possibly a lot. We are
correcting a number and sharpening a claim, not rescuing the paper.

---

## Verified finding 1 — BOC does not bound the shutdown problem

**This is the item that can move a number already written into the abstract.**

Read directly from `openmc_model/depletion_results.h5`:

- **Xe-135 at step 0 is exactly zero atoms.** BOC is xenon-free, as OpenMC
  depletion always starts. Every later step carries about 7 × 10²¹ atoms.
- Measured from step 0 to 3 days — 0.040 GWd/tHM burnt, so essentially pure
  poison build-in — the **Xe/Sm saturating-fission-product defect is 4,416 pcm**.
- The record has **36 steps, not 3**. The shape is visible, and it is not what
  §2.2 describes:

| Burnup (GWd/tHM) | k_eff | |
|---|---|---|
| 0.00 | 1.15336 | xenon-free |
| 4.13 | **1.07963** | post-BOC minimum |
| 12.11 | **1.14475** | mid-cycle maximum, **+5,269 pcm** |
| 30.75 | 0.98522 | |

Two consequences:

1. **"The eigenvalue falls monotonically from BOC to MOC" is false.** It dips,
   then climbs 5,269 pcm as the gadolinia burns out.
2. Cold shutdown is a xenon-free condition. Removing 4,416 pcm from the
   mid-cycle peak gives **k ≈ 1.2057 against BOC's 1.15336 — mid-cycle is about
   3,760 pcm *more* reactive.**

So *"BOC is the most reactive state the core occupies"* is wrong for the
shutdown question, and **771 ppm is an underestimate.**

> **Caveat, stated honestly.** The 3,760 pcm is an estimate, not a result: the
> defect is measured at BOC composition, not at mid-cycle, where the spectrum
> and flux differ. The sign is not in doubt; the magnitude must be computed.

> **Also to reconcile.** This file gives BOC k = 1.15336, while Table 2 of the
> manuscript gives 1.1502. Table 2 came from a different (higher-statistics)
> depletion run. Confirm which record is authoritative before quoting either.
> The xenon-free-at-step-0 behaviour is structural and will be the same in both.

---

## Verified finding 2 — smaller, all confirmed

| Item | Verification |
|---|---|
| **16-CRA natural bank worth** | `1/0.95053 − 1/1.15826 = 18,868 pcm`, not the 18,853 stated. Real 15 pcm discrepancy. Give ± on all four bank worths, not just one. |
| **Two β_eff values in use** | Fig. 3(b)'s caption uses prompt-k 704.5 pcm; the abstract and conclusions use IFP. Pick one and use it everywhere. |
| **A numeric citation baked into a figure image** | `code/fig3_design_space.py:88` writes the literal text *"published SBF cores stay here [2,4]"* into the plot. The Harvard conversion fixed the manuscript text and could not touch the PNG, so the paper is author–date everywhere except inside a picture. The same figure reads "van der Merwe & Hah"; Harvard wants "and". |
| **The two 902s are not a typo** | `data/rea_tfuel900_results.json` gives 902.2 ± 34 pcm for the ejected rod at 900 K fuel. Table 3 gives 902 ± 26 pcm for symmetry class (0,1), whose representative position is **(3,2)** — the same cluster. Two determinations of one quantity. The reviewer read it as an inconsistency, which is the point: the paper must say so. Confirm the two runs used different random seeds; if they did, note that agreement to 0.2 pcm at a combined σ of 43 pcm is fortuitous and should not be presented as mutual confirmation. |

---

## Track A — the blocking runs

**We do not need to re-run depletion.** The review assumed a new finely stepped
burnup campaign; we do not need one. `depletion_results.h5` already holds 36
steps of depleted compositions. These are **branch calculations off material
states we already own** — cheap eigenvalue runs.

| | Run | Purpose |
|---|---|---|
| **A1** | Hot ARO k at ~6 burnup points spanning 4–17 GWd/tHM, **Xe-135 zeroed** | Locate the true xenon-free reactivity maximum |
| **A2** | Cold stuck-rod case at that maximum | The real shutdown margin; replaces the BOC-only §5 |
| **A3** | Boron sweep at that maximum | The real EBIS requirement; replaces 771 ppm |

### One technical point to get right

Cold shutdown is **not simply "xenon-free"**, which is how the review phrased it:

- **Xe-135** decays away (9.2 h half-life) — zero it.
- **Sm-149 is stable and *grows* after shutdown**, because Pm-149 decays into it.

Handle Pm-149 → Sm-149 explicitly rather than lumping both into one "xenon-free"
branch, or the result will be conservative in one direction and wrong in the
other.

---

## Track B — a reading task, not a calculation

The **EBIS sizing basis** swings the margin from 3.9× to roughly break-even, and
it is settled by reading **SSR-2/1 Requirement 46's supporting paragraphs**, not
by running anything.

The reviewer's reading is that at least one of the two shutdown means must hold
the core subcritical **on its own**, by an adequate margin, in the most reactive
state. Our rods cannot do that cold — so the boron must, which points at **cold
all-rods-out**, not the cold stuck-rod basis we currently use. We report that
cold ARO needs 2,040 ppm merely to reach k = 1; reaching k_adj ≤ 0.95 would need
substantially more.

**Resolve this before A3**, because it decides whether A3 sweeps the stuck-rod or
the ARO configuration.

We already have `N10_EBIS`, a cold ARO sweep at BOC. If the ARO basis wins, that
run needs repeating at the limiting burnup and carrying to k_adj ≤ 0.95.

This also affects §5.2, which currently sets a k = 1 criterion (ARO) against
k_adj = 0.95 (stuck rod) — two different criteria in one comparison.

---

## Track C — editorial, no dependency on A or B

Can start immediately and in parallel.

**Figures**
- Regenerate Fig. 3: remove the baked-in `[2,4]`, switch to author–date, "&" → "and"
- Remove the Fig. 3(a) annotation asserting what the text carefully declines to claim
- Fig. 2(a): fix the cluster-count annotation overlapping the bars; add error bars to the bar charts

**Numbers and criteria**
- Unify β_eff on IFP throughout. Adopt the g10/g20 value — they agree to 1.1 pcm — and state plainly that g5 was chosen as the **conservative** value, since it *lowers* the dollar figures. That is the opposite of cherry-picking and should be said, not left to look like it
- Criteria consistency: define SDM with the stuck rod (Table 4's hot "SDM" is all-rods-in, which is not shutdown margin in the conventional sense), use k_adj throughout, report the hot N-1 value from the existing Fig. 4(a) data, reconcile the §5.2 / §5.3 crossing criteria, and justify the 0.95 criterion
- Fix the 18,868 pcm arithmetic; add ± to all four bank worths
- Disambiguate the two 902 pcm values
- Note that shared-ARO uncertainties are correlated, so the quoted 6.3σ and 2.9σ are **conservative** — the lever interaction is probably more significant than stated

**Completeness**
- Add the control-rod geometry: absorber radius, clad, B₄C density, absorber length, and the axial definition of "all in". Currently absent, and the paper is not reproducible without it
- State explicitly whether xenon is included in each reported state
- Add the operating rod position. k(ARO, HFP, BOC) = 1.150 means roughly 13,000 pcm sits on the rods at power with no boron — over half the bank inserted in normal operation. This bears on the ejected-rod initial state, on Table 2's peaking factors, and on B-10 depletion in the rods over a long cycle. Report the critical rod configuration at BOC HFP and list rod burnout as a limitation
- Soften the claim that cluster worth "ceases to be a constrained design variable" to *the REA-derived constraint no longer applies*, and name dropped and misaligned rod events (SRP 15.4.3), which still depend on single-cluster worth
- Fill the Table 4 gaps (cold all-rods-in k is blank for both 16-CRA rows); state that Table 5's σ varies by point, and add the 3,000 ppm point
- Shannon entropy convergence for the tilted configurations (single cluster in, stuck rod)

**Wording**
- §5.2: the decreasing boron increment is spectral hardening and a lower k, not "self-shielding"
- §3.1: "the two evaluation states differ by the Doppler reactivity between them" reads as though the worths differ by ~590 pcm; they differ by 58 pcm
- Symmetry-class notation as (min(|Δi|,|Δj|), max(|Δi|,|Δj|)), and state the grid origin in Fig. 1
- Remove bold emphasis from running text; journals do not use it
- Trim the defensive prose ("it is worth being precise", "worth stating plainly", repeated re-quoting of uncertainties) — worth perhaps 10–15 % of the length and it will read more confidently
- Highlights: use ± and σ rather than "+/-" and "sigma"

**Literature**
- Add the i-SMR core-design work, including the gadolinia-burnable-absorber paper in *NET* and Cho, Lee & Hong (2025), *Ann. Nucl. Energy* **214**, 111203 — same group as our Lee et al. (2026), directly adjacent to §1, and currently uncited
- The i-SMR rodded-fraction data point (49 of 69 positions, ≈71 %) sits usefully between our 43 % and Flexblue's 100 %
- Verify each new reference against the publisher record before adding it

---

## Sequence

1. **Now, in parallel** — Track C starts; A1 starts; Track B gets resolved.
2. **A1 lands** → the limiting state is known → A2 and A3 follow.
3. **Only then** rewrite the abstract, §5 and the conclusions. Not before: the
   numbers will move and the work would be done twice.
4. Final consistency read, rebuild the DOCX, submit.

Realistically two to three weeks. There is no deadline pressure: TEKNOFEST is
finished, *Annals* has no page charges and no page limit, and no competing
submission is waiting on this.

---

## What not to do

**Do not submit on 771 ppm hoping it holds.** The reviewers most likely to be
assigned this paper are precisely the people who would spot the xenon asymmetry.
Found by a reviewer, it is a rejection rather than a revision, and the correction
becomes part of the record.

---

## Review points that are already closed

Recorded so they are not re-litigated:

- **"Check the reference style — I believe NET's is numbered."** Moot. We
  retargeted to *Annals*, which is author–date, and the manuscript was converted
  on 2026-09-22. Several other points in the review are NET-specific and no
  longer apply.
- **"I couldn't confirm Lee et al. (2026)."** Verified against Crossref:
  *Nucl. Eng. Technol.* **58**, 104029, doi:10.1016/j.net.2025.104029.
- **"Make sure the Zenodo DOI resolves publicly."** Verified — both records are
  published and open access.
- **"Confirm the author list is final."** Settled; A. Abdikarimov is not an
  author.
- **"20,000 particles with 50 inactive batches is thin."** That is STAT_MEDIUM.
  The reported results use 400 × 50,000 with 80 inactive. The entropy-convergence
  request stands on its own merits, but the premise was a misreading.
