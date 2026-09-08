# Google Slides audit — "Final presentation-new"

**Checked:** 23 Aug 2026, against the live deck
(`docs.google.com/presentation/d/1xcrN-RckJEEIlQwVPQ6ELcGgcQqiD4N6rf0NnSdvDmU`),
43 slides, last modified 23 Aug 13:50 by s.achilova@newuu.uz.

> **The live Google deck is now the master.** The local `D:\projects\Final pptx\Final presentation.pptx`
> is 37 slides and **behind** — do not re-import it over the Google version, you would lose six slides.

---

## ✅ What landed from `13_SLIDES-MANUAL-EDIT-CHECKLIST`

| Item | Status |
|---|---|
| A1 · slide 14 bank worth 21,509 / SDM 7.85 % | ✅ |
| A2 · Safety Criteria 21,509 / k_adj 0.790 | ✅ |
| A3 · Event matrix CDF 1×10⁻⁸ / k_adj 0.790 | ✅ |
| A4 · Shutdown tiles 21,509 · 7.85 % · k 0.927 · ~13,100 · 0.790 | ✅ all four |
| A5 · fluence 3.02 × 10¹⁸ | ✅ |
| A6 · peak cladding temperature 353 °C | ✅ |
| A7 · GDC-28 / β_eff 704.5 block | ✅ |
| A8 · `FIGURE SLOT` placeholder removed | ✅ |
| B1 · NUWARD row on Literature Review | ✅ |
| B2 · burnup reframed as the boron price | ✅ **including the VBER softening** ("seven times larger, so it also leaks fewer neutrons") |
| B3 · power-density row | ⚠️ added but **values mis-ordered** — see C4 |
| ICSBEP bias −50 pcm | ✅ correct |

Also new and good: **Core-Damage Frequency Arithmetic** slide, **Security + Safeguards** panel on
Auxiliary Systems, MOC/EOC peaking closed on Core Design.

---

## 🔴 CRITICAL — fix before Tuesday

### ~~C1 · Slide order~~ — **withdrawn, the order is deliberate**

*Corrected 23 Aug after Samira explained the intent. Recorded so nobody "fixes" it back.*

Radiation Shielding and Waste Management were moved into the early block **on purpose**: they are
Samira's OpenMC results, so they belong in her run rather than making her interrupt Azamkhon's section
later. I&C Architecture was moved out of her way for the same reason.

**The result is a better structure than the original.** Samira now speaks **one continuous run,
slides 1–22**, hands over once, and returns for **34–38**. The old arrangement had three hand-offs.

**But two things follow from the move and still need doing:**

**C1a · Renumber the footers.** They still carry the *old* positions — Shielding reads 29 at position 16,
Waste reads 31 at position 17, I&C reads 26 at position 43. Right now the footer numbers contradict the
deck, which is what made this look accidental. Renumber 01–43 in the new order, or drop the footer
numbers entirely.

**C1b · Waste intensity is now stated twice, back to back.** Slide 17 (Waste) leads with
**4.40 tHM/TWhe, −32 %**, and slide 18 (Fuel Cycle) has a **WASTE INTENSITY 4.40 tHM/TWhe · 32 % below
CAREM-25** tile. They were 15 slides apart before and are now adjacent. Cut it from one — recommend
dropping the tile on 18 (Fuel Cycle already carries four tiles) and keeping it on 17, where it is the
headline.

**Open question — is I&C Architecture (43) meant to be presented?** It sits *after* the four BACKUP
slides and *after* the References / Teşekkürler closing slide, and it still carries a full figure
caption and footer 26. If it is now a backup slide, that is fine but it should move above the closing
slide or be labelled as backup. If it is still in Azamkhon's spoken run, it needs to move into 23–33.

### C2 · Slide 29 "Core-Damage Frequency Arithmetic" carries the **wrong body text**

Its paragraph is the radiation-shielding text, pasted verbatim:

> *"The build is deliberately lead-free: 20 cm borated polyethylene plus 180 cm magnetite heavy
> concrete. That closes the occupational-dose target…"*

The Turkish özet on the same slide is correct (Σ CDF ≈ 5.8 × 10⁻⁸ /ry) and the "Result:" label is
**empty**. Replace the body with the CDF roll-up, e.g.:

> Nine initiator groups are quantified sequence by sequence and summed: **Σ CDF ≈ 5.8 × 10⁻⁸ /ry**,
> against a < 1 × 10⁻⁷ /ry target. Every core-damage path requires at least two independent failures.

Its footer also reads **29**, duplicating Radiation Shielding. Give it 24a or renumber the block.

### C3 · Economics slide (34) is still the **old version**

`PART D` of the checklist was not applied. It still shows:

- `$74.8` as the headline — the most optimistic of four capital cases
- a **FUEL CYCLE $18.3** tile sitting beside it, though $18.3 is *inside* $74.8
- a result line quoting `$57–193/MWh`, a range not visible in the three-row table
- no external benchmark anywhere

The nine table cells (55.5 / 74.8 / 92.1 · 63.1 / 90.6 / 115.2 · 79.5 / 124.7 / 165.2) are **correct** —
they match FER Table 8.12-6 exactly. **Leave the table alone; change the tiles and the result line.**
Full instructions in `13_SLIDES-MANUAL-EDIT-CHECKLIST` Part D.

### C4 · Power-density row: SMART and CAREM values are swapped — **my error**

Checklist B3 listed the columns as Aegis / NuScale / **CAREM** / SMART; the deck's table is
Aegis / NuScale / **SMART** / CAREM. Pasted in order, the last two landed the wrong way round.

| Column | Now shows | Should be |
|---|---|---|
| SMART | 1.64 | **6.40** |
| CAREM-25 | 6.40 | **1.64** |

CAREM-25 is the low-power-density design (100 MWth over 61 assemblies); SMART is 365 MWth over 57.
As it stands the slide claims SMART is half our power density, which is backwards and checkable.

---

## 🟡 Worth fixing

### C5 · Figure numbers are broken again by the reordering

Sequence by position is now **1, 2, 3, 13, 15, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 11**.

- **Fig. 11 appears twice** — Core-Damage Frequency (29) and I&C Architecture (43).
- Shielding keeps Fig. 13 and Waste keeps Fig. 15 while sitting fifth and sixth.

Renumber **after** fixing the order in C1, not before.

### C6 · Four empty BACKUP slides (39–42)

All blank, all footer **35**. Either fill them (the obvious candidates: LCOE sensitivity chart,
CDF event tree, peaking maps, SMR comparison detail) or delete them. Empty slides in a submitted deck
read as unfinished.

### C7 · Typo — slide 6

`Flexible operaation` → **`Flexible operation`** (NUWARD row).

### C8 · B5 open item never added — slide 37

Add to "What remains detailed-design work":

> Definition of in-service inspection intervals and in-vessel component maintainability across the
> six-year cycle.

Naming it is stronger than being asked about it.

### C9 · B4 values never added

Plant footprint **≈ 31,600 m² (3.2 ha)** and RPV weight **≈ 270 t** are still absent (slide 11 or 33).
Say "we calculate approximately" — these are engineering estimates, not FER values.

---

## Speaker notes — already remapped

`speaker-notes-Samira-FINAL.md` has been renumbered to the live 43-slide deck (23 Aug):

| | Live deck |
|---|---|
| Samira, continuous run | **1–22** (shielding 16, waste 17) |
| Hand to Azamkhon | 23–33 |
| Samira returns | **34–38** (economics 34) |

Total unchanged at **20 min 55 s**; the shielding/waste block now sits between slide 15 and the fuel
cycle slide, where it is spoken.
