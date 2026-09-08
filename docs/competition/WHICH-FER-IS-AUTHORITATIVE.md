# ⚠ WHICH FER IS AUTHORITATIVE

**Created 23 August 2026 after quoting the wrong FER twice in one day.** Read this before citing any
FER number anywhere — slides, papers, speaker notes, Q&A prep.

## The answer

> ## `docs/Aegis40_FER_submission_ready_compact_final.docx` — **15 Jul 2026 13:39**
> Companion PDF `docs/Aegis40_FER.pdf` (15 Jul 13:31) is the export of it.
> **This is the newest FER anywhere on disk and the only one to cite.**

## Every other FER file, and why not to use it

| File | Date | Status |
|---|---|---|
| **`docs/Aegis40_FER_submission_ready_compact_final.docx`** | **15 Jul 13:39** | ✅ **AUTHORITATIVE** |
| `docs/Aegis40_FER.pdf` | 15 Jul 13:31 | ✅ export of the above |
| `docs/Aegis40_FER_latest_submission_ready.md` / `.docx` | 7 Jul | ⚠ superseded — LCOE 75.9 / cogen 65.9, later corrected to 74.8 / 64.8 |
| `docs/Aegis40-FER.docx` | 7 Jul | ⚠ superseded, same vintage |
| `docs/competition/fer/Aegis40-FER-master.md` | §§8.11/8.12 written **30 Jun** | ❌ **STALE** — pre-dates the 4 Jul basis freeze |
| `D:\Downloads Edge\Aegis40_FER_*.docx` (7 files) | 2–7 Jul | ❌ working drafts, ignore entirely |

`docs/competition/fer/FROZEN-MASTER-VALUES.md` (4 Jul) remains the quick lookup for frozen quantities
and carries a **"❌ STALE VALUES — replace on sight"** table. Use it as the cross-check.

## What the stale files will tell you if you read them

`Aegis40-FER-master.md` §§8.11/8.12 pre-date the **4 July basis freeze**, when discharge burnup moved
27.6 → **29.6 GWd/tHM** and heavy metal 9.87 → **9.39 tHM**:

| Quantity | Stale master (30 Jun) | Authoritative (15 Jul) |
|---|---|---|
| Waste intensity | 4.72 tHM/TWhe, −27 % | **4.40 tHM/TWhe, −32 %** |
| Discharge burnup / HM | 27.6 GWd/tHM / 9.87 tHM | **29.6 GWd/tHM / 9.39 tHM** |
| Fuel-cycle cost | $7.5/MWh | **$18.3/MWh** ($17.3 front end + ~$1 back end) |
| LCOE (7 %) | 85.0 / 107.8 / 141.9 | **74.8 / 90.6 / 124.7** |
| Total Pu | 76.6 kg, Pu-239 63.6 % | **78.1 kg, Pu-239 61.6 %, Pu-240 21.6 %** |

`1000 / (29.608 × 24 × 0.320) = 4.40` — the whole waste-intensity change is the burnup move.

## The FER is BEHIND the deck on safety neutronics — open action

The 15 Jul FER still carries the **12-CRA** values. `team-sync/02_FER-DOCX-EDITS.md` §A has listed the
replacements since **14 Aug with every box still unchecked**, and the 15 Jul document confirms they
were never applied:

| In the FER (wrong) | Should be | On the slides |
|---|---|---|
| rod worth **15,672 pcm** | 21,509 pcm | ✅ corrected 22–23 Aug |
| hot SDM **~2.0 %** | 7.85 % | ✅ corrected |
| k_ARI **0.980** | 0.927 | ✅ corrected |
| k_adj cold **0.845** | 0.790 | ✅ corrected |
| vessel fluence **3.35 × 10¹⁸** | 3.02 × 10¹⁸ | ✅ corrected |

**This is a live finals exposure**, and it points the opposite way from a stale-slide problem: a juror
reading the FER sees 15,672 pcm and 2.0 % shutdown margin while the slide says 21,509 and 7.85 %.

**It is an upgrade, so lead with it:** *"The report carries the 12-rod configuration. We finalised at
16 control-rod assemblies, which raises bank worth to 21,509 pcm and hot shutdown margin to 7.85 % —
about four times the acceptance criterion. The digital appendix carries the final run."*

Also still open from §C: **Table 8.12-2 cogeneration-credited LCOE reads $65.9/MWh** while §8.12.3
prose reads **$64.8** — the edit was applied to the prose but not the table.

## Rule

1. Cite **`Aegis40_FER_submission_ready_compact_final.docx` (15 Jul)** — nothing else.
2. Cross-check against **`FROZEN-MASTER-VALUES.md`**.
3. Where the deck and the FER differ on **safety neutronics or shielding**, the **deck is newer** — see
   the open action above.
4. Where they differ on **anything else**, assume the FER is right and check before changing a slide.
