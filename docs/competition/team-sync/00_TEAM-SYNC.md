# Aegis-40 — Team Sync (READ THIS FIRST)

**Updated:** 2026-08-14 · **Status:** FER submitted (finals stage) · **Finals presentation due:** ~8 days

This folder is the single source of truth so we're all on the same version. Four files:
1. **`00_TEAM-SYNC.md`** (this) — decisions, current state, what's done / pending, who owns what.
2. **`01_FINAL-NUMBERS.md`** — the authoritative numbers. If a value differs from here, **here wins**.
3. **`02_FER-DOCX-EDITS.md`** — the exact edits still pending in the report `.docx`.
4. **`03_PROJECT-CONTEXT.md`** — plain-language "what is Aegis-40 and why" — read this first if you're new or want the narrative + Q&A-defense rationale.
5. **`04_FINALS-IMPROVEMENT-TASKS.md`** — task board for the days before finals: 3D cutaway, event trees, I&C diagrams, dashboard, etc. — owners, tools, effort, priority.

---

## 1. Where we are

- **FER report:** submitted. A short list of consistency edits is still pending (see `02_...`).
- **Digital appendix:** rebuilt and current — `docs/competition/Aegis40-Digital-Appendix.zip` (~8 MB, ~203 files). Re-upload this latest ZIP; it changed a lot since the first submission.
- **Final presentation:** first draft exists — `Aegis40_Final_Presentation_v1.pptx` (24 slides). Needs restyling, team-name placeholders filled, and the 16-CRDM numbers updated.
- **CAD:** 2-D drawings in the appendix (DA-11); 3-D STEP/SolidWorks on the shared Google Drive.

💡 *Improvement: put a version tag + date in the ZIP filename (e.g., `Aegis40-Digital-Appendix_v2_2026-08-14.zip`) so we never re-upload a stale bundle by accident. Keep exactly one "latest" link pinned in the team chat.*

## 2. Decisions locked this round (IMPORTANT — new)

### 🔴 Control rods: **16 CRAs**, not 12
We found the FER said "16 CRA" but was quoting the **12-CRA** rod numbers. **Decision: commit to 16 CRAs** (12 base + 4 extra CRDMs in the central-cross fuel assemblies `(3,5),(1,3),(5,3),(3,1)` — existing guide tubes). This is the **N5C** case and it is *stronger*:

| | Old (12 CRA, wrong) | **New (16 CRA, correct)** |
|---|---|---|
| Rod bank worth | 15,672 pcm | **21,509 pcm** |
| Hot shutdown margin | ~2.0 % | **7.85 %** |
| k_ARI hot | 0.980 | **0.927** |

- **Unchanged:** cold shutdown is still credited to **EBIS** (k_stuck_cold = 1.031, still supercritical cold) — the SBF + diverse-shutdown story is intact. Only the *hot* margin gets much stronger.
- **Bonus:** this kills a Q&A weak spot — "only 2 % hot SDM?" is now 7.85 %.
- **Mechanical/CAD:** upper vessel now houses **16 in-vessel CRDMs**; +4 vs 12, in existing guide tubes. Any drawing showing 12 rod positions → 16.

### Other locked design values (recap)
Soluble-boron-free 37-FA iPWR · 125 MWth/40 MWe · natural circulation · once-through 29.6 GWd/tHM, 2224 EFPD · Gd 6 wt%×20 + Er 0.75 wt%×16 · lead-free shield (20 cm PE + 180 cm magnetite) · TCES district heat + SOE H₂ · full numbers in `01_FINAL-NUMBERS.md`.

💡 *Improvement: our headline originality points are SBF + natural circulation + lead-free shield + TCES cogen. For finals, pick the ONE we defend hardest (my vote: soluble-boron-free with 7.85 % rod margin — it's the cleanest "we solved a hard problem" story) and make it the spine of the pitch rather than listing all four equally.*

## 3. What's DONE vs PENDING

**Done (already in the appendix ZIP):**
- Economics recomputed at 4.43 wt% core-average enrichment → LCOE $74.8/MWh (NOAK); DA-7 model matches FER §8.12.
- Decay heat synced (7.95 MW shutdown / 48.4 kW 1 yr / 9.0 kW 10 yr).
- Hydrogen 427 t/yr; MDNBR 1.33/2.13 corrected everywhere; shielding adopted build (0.23 µSv/h, RPV fluence 3.0×10¹⁸).
- Reproducibility manifest (REPRODUCE.md + requirements + SHA-256 checksums); CAD folder (DA-11); TH package updated to Adilbek's latest.
- **16-CRDM propagation into the appendix + deck (DONE 2026-08-14):** all READMEs, DT files (`twin_sweep.py` map now 16 CRAs, `fit_surrogates.py`, `run_twin_sweep.sh`, `validation.txt`, `neutronics-STATFINAL-results.md`), master README, REPRODUCE.md, and slide 9 of the deck now read **21,509 pcm / 7.85 % / k=0.927**. Checksums regenerated (202/202 verify). The 12-CRA N5B result stays in `safety_neutronics_results.json` as a documented sensitivity.

**Pending (needs doing):**
- **FER docx edits** — the small consistency list in `02_...` (economics cascade, Fig 8.2-4 caption, Table 8.4-3 typo, **16-CRDM numbers 21,509/7.85 %**). *(Manual, in Word.)*
- **CAD** — show 16 rod positions in the upper-vessel drawings (currently may show 12).
- **Digital-twin fresh sweep** — script is ready (`run_twin_sweep.sh`, 16-CRA enriched-B10, ~168 pts); needs an OpenMC run (~3–6 h) on a free machine, then a 1-min retrain. Optional but recommended for precise coefficients + rod worth.
- **Presentation** — restyle, fill team placeholders, add speaker notes, update 16-CRDM numbers.

## 4. Suggested ownership (adjust as you like)
- **Neutronics lead** — confirm 16-CRDM edits in FER §8.2/§8.5/§8.6; run the fresh twin sweep when a machine is free.
- **TH** — confirm Table 8.4-3 typo fix (2.78 → 1.78) and MDNBR basis wording.
- **Mechanical/CAD** — 16 CRDMs in the upper-vessel drawings; sanity-check shield OD 7.6 m in layout.
- **Economics/BOP** — apply the §8.12 cascade edits (`02_...`).
- **Presentation owner** — deck restyle + speaker notes; live digital-twin demo.

## 5. Finals focus (this week)
1. **Q&A prep** — anticipated hard questions + crisp answers (biggest score lever).
2. **Deck + 30-min rehearsed script.**
3. **Live digital-twin demo** (memorable differentiator).
4. Optional credibility boosters: SFCOMPO measured-depletion benchmark, converged shielding MC (both need the OpenMC machine).

💡 *Improvement, ranked by score-per-effort for the week: (1) rehearse Q&A on our 3 weakest points — once-through fuel use, 4 m riser / MDNBR 1.37 margin, W-3 conservatism; (2) live digital-twin demo; (3) one converged shielding MC run to upgrade "estimate"→"calculated"; (4) SFCOMPO benchmark if a machine is free. Do 1 and 2 no matter what.*
