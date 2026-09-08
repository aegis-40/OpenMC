# Final week — what is left

**Written 24 Aug 2026.** Event: TENMAK İstanbul Çekmece, **1–4 September**.

> ⚠️ **First, settle the date.** My notes carry a **26 August** deadline for the deck/FER submission.
> If that is real, everything in Block 1 below is due in **two days**, not seven. If 26 Aug has moved
> and the only fixed date is the event, the plan below stands. **Confirm this before anything else** —
> it changes what is achievable.

**Honest status: the deck is roughly 90 % done.** What remains is mostly polish, and the single
highest-value use of the remaining time is **rehearsal**, not more editing.

---

# BLOCK 1 — Deck finishing (½ day, two people)

Full detail in `16_DECK-FIX-INSTRUCTIONS.md`. Outstanding after your 24 Aug pass:

| # | Slide | Fix |
|---|---|---|
| 1 | **29** | Σ CDF line appears **three times** — delete the two leftovers |
| 2 | **34** | Result line still says *"$57–193/MWh spread … $64.8/MWh"*; tile 1 now shows the range so it is redundant. BASIS / uncertainty blocks never added |
| 3 | **35** | SMART ↔ CAREM still swapped: SMART = **6.40**, CAREM = **1.64** |
| ~~4~~ | ~~21~~ | ~~"single turbine"~~ — **withdrawn, the slide is correct.** It is one tandem-compound turbine; DWSIM shows three blocks only because it has no multi-stage object |
| 5 | **25** | Fig. 10 caption truncated to *"Sinop coastal site"*; box 3 lost the salinity and winter-recovery lines |
| 6 | **26** | Figure caption gone (was Fig. 9) — was the figure removed on purpose? |
| 7 | *global* | Superscripts still flat: `3.02 × 1018`, `1.0 × 1019`, `10−7`, `10−5`, `Gd2O3`, `UO2` |
| 8 | **8** | `YERLILIK` → **YERLİLİK** · `HEDEF KITLE` → **HEDEF KİTLE** |
| 9 | **32** | `78 kg` → **78.1 kg** · `self protecting` → `self-protecting` |
| 10 | **30** | Run-on: *"A standby-liquid-control principle Rods carry…"* — needs a colon |
| 11 | **28** | Rod-withdrawal row: criterion says MDNBR ≥ 1.3, result gives an insertion rate |
| 12 | **39–45** | Appendix footers read 38, 39, 40, **41, 41, 41**; I&C at position 45 still shows footer **26** and **Fig. 11** (duplicating Passive Safety) |
| 13 | **appendix** | **Glossary was deleted, not moved.** The deck uses ~30 acronyms. Put it on a blank APPENDIX slide |

## Two things only you can check (I read text, not images)

- **Slide 5** — Samira appears to have no role label next to her name, and three role labels contain
  literal `&#11;` control characters that may render as boxes.
- **Site-layout figure** — reported as reading **"seismic gap ≥ 75 m"**. The FER says **≥ 75 mm**.
  A factor of 1000 on a drawing is the kind of thing a juror photographs.

---

# BLOCK 2 — The banner (do this on **day 1–2**, not later)

`14_STAND-BANNER-BRIEF.md` has the full spec. **This is the only item with external lead time** —
printing, delivery and mounting take days, and it has to travel to İstanbul with you.

- [ ] Choose and prepare the hero image (**strip the technical callouts**)
- [ ] Lay out at 400 × 500 mm, 300 dpi, matte
- [ ] Check the dark-on-dark trap — a navy vessel disappears on a navy field
- [ ] Test Turkish characters: *ısıl · yakıt değişimi · güvenli*
- [ ] **Send to print by 26 Aug at the latest**

---

# BLOCK 3 — The FER divergence 🔴 *highest remaining risk*

`02_FER-DOCX-EDITS.md` §A has been open since **14 Aug with every box unchecked**, and the 15 Jul
submitted FER confirms the edits were never applied. **The report still carries the 12-CRA values:**

| FER says | Deck says |
|---|---|
| 15,672 pcm bank worth | **21,509 pcm** |
| ~2.0 % hot SDM | **7.85 %** |
| k_ARI 0.980 | **0.927** |
| k_adj cold 0.845 | **0.790** |
| fluence 3.35 × 10¹⁸ | **3.02 × 10¹⁸** |

**Decide which case you are in:**

**(a) The FER can still be revised** → apply §A (six locations), §B (the 2.78 → 1.78 MDNBR typo) and
the remainder of §C (**Table 8.12-2 still reads $65.9** while §8.12.3 prose reads $64.8). Half a day
in Word, and it removes the problem entirely.

**(b) Submission is closed** → then this is purely a **Q&A preparation** item, and Azamkhon must be able
to deliver the upgrade line without hesitating. It is in his notes. **Rehearse it out loud.**

Either way, do not let a juror discover it first.

---

# BLOCK 4 — Rehearsal 🔴 *the highest-value hours you have left*

Speaker notes are done for both presenters:
`speaker-notes-Samira-FINAL.md` (slides 1–22, 34–38, ≈ 20:55) ·
`speaker-notes-Azamkhon.md` (slides 23–33, ≈ 8:30). Combined ≈ **29 min 25 s**.

- [ ] **Confirm the time limit.** If it is 25 minutes you must cut ~4:30 — the trim orders are in both
      notes. Find this out before rehearsing to a wrong target.
- [ ] **Two full run-throughs with a stopwatch**, hand-offs included. The hand-off at slide 22→23 and
      back at 33→34 is where teams lose time.
- [ ] **Q&A drill**, at least 20 questions. The five to rehearse verbatim:
      1. *"Why does a boron-free reactor have a boron system?"*
      2. *"Your report says 15,672 pcm."*
      3. *"Where is seismic in your core-damage frequency?"*
      4. *"Is 1.33 MDNBR enough?"*
      5. *"Is it economic?"* — never claim it is cheap; name the condition
- [ ] Everyone on the stand can answer *"how does it cool itself?"* in one sentence
- [ ] `11_AEGIS40-HANDBOOK.md` — everyone reads it once

---

# BLOCK 5 — Fill the six blank APPENDIX slides (half a day)

You have six and they are all empty. Best candidates, in order of Q&A value:

1. **Glossary** (see Block 1 #13 — it has to live somewhere)
2. **LCOE sensitivity chart** — the tornado; answers every economics follow-up
3. **OTSG temperature profile** — pinch is **8.4 K**, surface **≈ 1,850 m²**, comparable to NuScale per
   MW. First thing a thermal engineer computes; much stronger prepared than derived live
4. **CDF event tree** — backs slide 29
5. **BOC/MOC/EOC peaking maps** — backs slide 14
6. **Seawater plume dilution figure** — already generated
   (`docs/competition/cycle/seawater_plume_dilution.png`). ⚠️ It says **83 MWth**; slide 11 says
   **82.6** — make them match before using it

---

# BLOCK 6 — DWSIM (optional, only if someone has spare capacity)

From the flowsheet review. **None of this changes a slide.**

1. **Condenser pressure** — displayed as `0.01 MPa`, but 39.00 °C saturates at **0.00699 MPa**. Almost
   certainly display rounding; switch the flowsheet units to **kPa** and confirm. *10 minutes.*
2. **Move the moisture separator before the split** so no splitter divides a two-phase stream.
   *20 minutes, and it removes an obvious question.*
3. **HP/IP separator** — raises IP exhaust quality from 0.872 to ~0.912, clearing the erosion
   guideline. *Needs a re-run and a check that you still close on 40 MWe.*
4. **OTSG pinch** — nothing to model; write the 8.4 K / 1,850 m² result into §8.4 and Block 5 #3.

---

# What NOT to do this week

- **The paper.** `05_PUBLICATION-STRATEGY.md` and the rod-worth draft are post-competition work.
- **New OpenMC runs.** The basis is frozen and everything traces to it. A new number now creates
  inconsistency, not confidence.
- **The live digital-twin demo**, unless it is rehearsed on the actual venue laptop with a screenshot
  fallback. Slide 31 carries a "Demo" marker — a demo that fails on stage costs more than it gains.
- **Restructuring the deck.** It is coherent. Stop editing and start rehearsing.

---

# Suggested schedule

| Day | Focus |
|---|---|
| **Mon 25** | Block 1 deck fixes (½ day) · banner artwork finalised |
| **Tue 26** | **Banner to print** · Block 3 decision on the FER · start Block 5 appendix slides |
| **Wed 27** | Finish Block 5 · Block 6 if capacity · first full run-through |
| **Thu 28** | Full run-through #2 with stopwatch · fix whatever the timing exposes |
| **Fri 29** | Q&A drill, 20+ questions · handbook read-through |
| **Sat 30** | Q&A drill #2 · dry-run on the presentation laptop |
| **Sun 31** | Buffer · travel prep · banner collected and packed |

**If you only get three of these done: Block 1, the banner, and two rehearsals.** Everything else is
improvement on something that already works.
