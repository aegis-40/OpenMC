# Submission checklist — rod-worth / in-vessel-CRDM paper

**Target:** *Nuclear Engineering and Design* (Elsevier). Subscription route = **no author charges**.
**Draft:** `PAPER-DRAFT.md` · **Figures:** `figures/` · **Data:** `data/`

---

## Blocking — must be done before submission

| # | Item | Who | Effort |
|---|---|---|---|
| 1 | ~~**Compute β_eff** instead of assuming 650 pcm.~~ **✅ DONE** — β_eff = **704.5 ± 28.2 pcm** computed (prompt-k method; OpenMC 0.15.3 has no IFP scores). Ejected-rod worth is now **1.20 ± 0.13 $** (HZP) and **1.28 ± 0.07 $** (hot fuel). In `data/beta_eff_results.json`, and the abstract already carries it. *Note for reviewers: state the prompt-k method explicitly — a referee may ask why IFP was not used.* | Neutronics | — |
| 2 | ~~**Agree author order**~~ **✅ DONE** — S. Achilova first author and corresponding author. **Still needed: institutional affiliation line and an institutional e-mail** (do not submit with a personal address). | Team | ~10 min |
| 3 | ~~**Confirm TEKNOFEST rules**~~ **✅ DONE** — confirmed no restriction on publishing competition material. | Team | — |
| 4 | ~~**Verify all `[verify]` references**~~ **✅ SUBSTANTIALLY DONE.** Verified: **[1]** Ingremeau & Cordiez, *EPJ Nucl. Sci. Technol.* **1**:11 (2015) · **[3]** *EPJ Web Conf.* **247**, 19002 (2021) · **[5]** van der Merwe & Hah, *NET* **50**(4) 648–653, doi:10.1016/j.net.2018.01.019 · **[7]** *J. Nucl. Sci. Technol.* **38**(7) (2001), doi:10.1080/18811248.2001.9715067 · **[11]** Fridman et al., RODARE 2457 (30 Aug 2023) · **[13]** Alzaben et al., *NED* **350**, 33–42 (2019) · **[14]** Alzaben et al., *Ann. Nucl. Energy* **132**, 70–81 (2019). **[2] was replaced** — see item 4a. Residual: author lists for [3][6][11], end page for [2], page range for [7], DOI for [1]. All are publisher-record lookups, ~30 min. | Refs | ~30 min |
| 4a | **⚠ A citation error was found and corrected.** The old ref [2] cited **SMART as a soluble-boron-free design**. It is not — the licensed SMART design uses soluble boron, and only research variants are boron-free. Ref [2] is now Alzaben et al. (2019), *Ann. Nucl. Energy* **134**, 114 — an REA analysis of a genuinely boron-free 330 MWth / 57-FA core, which also strengthens §1's claim that the REA constrains SBF design. §1 now says "design studies" and states which are licensed. **Re-read §1 to confirm the new wording reads the way you want.** | Lead author | ~10 min |
| 5 | **Deposit at Zenodo** — ✅ **package built and ready**: `zenodo-deposit/` and `Aegis40-SBF-rod-worth-zenodo-v1.0.0.zip` (18 files, 0.7 MB). Upload the zip, paste the metadata from `zenodo-deposit/zenodo-metadata.json`, publish, then **(a)** insert the DOI into *Data availability* and **(b)** update `related_identifiers` with the article DOI once accepted. | Lead author | ~20 min |

## Strongly recommended

| # | Item | Why |
|---|---|---|
| 6 | **Burnup-dependent cold stuck-rod case** | §5 currently BOC-only. BOC is the bounding state, so the conclusion holds — but a reviewer will ask. A 3-point burnup repeat (BOC/MOC/EOC) closes it. |
| 7 | **Obtain Halimi & Shirvan (2024) in full** | They cover SBF + natural circulation. Confirm they do not already report an ejected-rod-worth-versus-bank-worth result. If they do, §3 needs reframing. |
| 8 | **Vary the 16-cluster pattern** | §6.3 admits the ladder is not an optimisation. Even two alternative patterns would let us say "pattern-insensitive within X pcm". |

## Optional / strengthens

- Point-kinetics envelope for the ejected-rod case (turns a screening statement into a bounded transient result)
- A second core size to support the generality claim in §6.1

---

## What is already done and defensible

- ✅ Rod-worth ladder, 3 configurations — `data/safety_neutronics_results.json` (N5, N5B, N5C)
- ✅ Ejected-rod worth 844 ± 82 pcm = 1.30 $ — `data/rea_n5c_results.json`
- ✅ MSLB cooldown, both bases, 7 points each — `data/mslb_n5c_results.json`
- ✅ EBIS requirement sweep → 785 ppm — `data/mslb_n5c_results.json` (N12E)
- ✅ Validation: ICSBEP LCT-008 (mean bias −50 pcm, worst 0.86σ); NuScale-like rod states within ±80 pcm over ~19,400 pcm of worth — the single most relevant validation for this paper
- ✅ **Four** figures, publication resolution (300 dpi) — Fig. 4 `figures/fig4_design_space.png` is the design-space comparison (rebuild: `scratchpad/fig4_design_space.py`)
- ✅ **Same-geometry literature comparator** — van der Merwe & Hah (2018), *NET* 50(4) 648–653: an SBF core at 180 MWth with **37 FA, 17×17, 200 cm, 4.95 w/o**, needing **29–37 Ag–In–Cd CEAs** for 14,906–20,570 pcm against our **16** clusters for 21,509 pcm. Written up as §4.1.
- ✅ Abstract rewritten — leads on the unconnected-literatures gap, carries method, validation, the ladder, the comparator and the binding-constraint conclusion

## Response to the external referee-style review

**Applied** (all in the current draft and DOCX): novelty claim narrowed to "we identified no published study that *quantitatively* examines…" with i-SMR acknowledged as an existing SBF + in-vessel-CRDM design · "admissible" removed throughout, replaced with "would require dedicated transient analysis" · Claim A/B split in §3.3 (architectural non-applicability vs. general safety exclusion), with rod drop, internal failure and uncontrolled withdrawal named · β_eff robustness quantified (reversal needs 4.9σ–7.0σ) · k_adj basis stated and its effect on the 785 ppm result reported · §2.4 renamed to benchmarking, depletion paragraph cut · §5.3 reframed as quasi-static reactivity response along a prescribed path · "does not cross criticality" → "remains supercritical" · van der Merwe comparison softened · unsourced "1 % criterion" removed · "bounds" → "conservative screening estimate" · design-space slice framing · figures renumbered (design space = Fig. 3, cooldown = Fig. 4) · uncertainty propagation stated · 40 MWe and the assembly pitch explained.

**⚠ One review point is wrong.** It calls the +0.005 in k_adj "a **5,000 pcm** penalty… enormous compared with your ~50–65 pcm," and builds its "biggest numerical-methodology issue" on that. **Δk = 0.005 is ≈ 500 pcm, not 5,000.** The underlying request to justify the value is fair and is now answered in §2.3; the "enormous" characterisation is not. Do not concede this point as stated if it comes back in a real review.

**Not applied — needs new OpenMC runs.** These are the three calculations that would most strengthen a resubmission:

| # | Run | Closes |
|---|---|---|
| R1 | **Individual worth of all 16 clusters** (or the top 3) | The bounding-cluster assumption — cheapest and highest value |
| R2 | **16 CRA + natural B₄C** — the missing fourth corner | Lets the two levers be shown separable rather than asserted |
| R3 | **Boron sweep at 700/800/900 ppm** | Replaces the 785 ppm interpolation with a direct determination |

Lower priority: burnup snapshots (BOC/MOC/EOC) for the cold stuck-rod state, and an independent β_eff by IFP or perturbation theory.

## Known weaknesses a reviewer will probe

1. **"Your ejected-rod worth is a static screen, not a transient."** — acknowledged in §6.3. Answer: the claim is conditional (would *require* analysis for an external-drive plant), not an enthalpy result.
2. **"β_eff is assumed."** — item 1 above. Fix it.
3. **"One core, one lattice."** — acknowledged in §6.3.
4. **"Is the REA constraint really binding in the literature, or are you overstating it?"** — cite [4] (a whole 2026 paper on optimising SBF cores to survive the REA) and [5]. This is the paper's hinge; make sure the introduction carries it clearly.
5. **"Isn't 785 ppm just a small boron system — so what?"** — the point is not the size but which criterion binds. Keep §6.1 sharp.

## Positioning note

Do **not** frame this as a peaking/thermal-margin or specific-power paper. Halimi & Shirvan (MIT) published that space in *Nuclear Technology* (2024) — see `../../team-sync/05_PUBLICATION-STRATEGY.md` §1. This paper deliberately occupies a different axis (reactivity control and drive-line topology) with a different reviewer pool.
