# References slide — paste-ready

For slide 38 (`References · Glossary · Teşekkürler`). Built so that **[9], [10], [14] and [15] mean
exactly what slide 7 already assumes** — only one bracket in the whole deck needs changing.

Items marked **[verify]** need checking against the publisher record before submission.

---

## Block 1 — numbered references (paste as-is)

```
PRINCIPAL REFERENCES

[1]  IAEA. Advances in Small Modular Reactor Technology Developments,
     2022 Edition. IAEA, Vienna, 2022.
[2]  IAEA. SSR-2/1 Rev. 1 — Safety of Nuclear Power Plants: Design.
     IAEA Safety Standards Series, Vienna, 2016.
[3]  U.S. NRC. NuScale standard design approval and final safety
     evaluation report, 2023.
[4]  IAEA. SSG-52; SSG-53; GSR Part 4 Rev. 1.
[5]  Bowring, R.W. AEEW-R 789, UKAEA Winfrith, 1972; Groeneveld, D.C.
     et al. "The 2006 CHF look-up table," Nucl. Eng. Des. 237 (2007)
     1909–1922.
[6]  ANSI/ANS-5.1 — Decay Heat Power in Light Water Reactors;
     U.S. NRC NUREG-0800 Standard Review Plan §4.2, 4.3, 4.4, 6.5.5.
[7]  Kim et al., 2021 — soluble-boron-free small modular reactor core
     design. [verify full citation]
[8]  Republic of Türkiye, Ministry of Energy and Natural Resources.
     Türkiye National Energy Plan, 2022.
[9]  Romano, P.K. et al. "OpenMC: A state-of-the-art Monte Carlo code
     for research and development," Ann. Nucl. Energy 82 (2015) 90–97.
[10] Brown, D.A. et al. "ENDF/B-VIII.0: The 8th Major Release of the
     Nuclear Reaction Data Library," Nuclear Data Sheets 148 (2018) 1–142.
[11] Romano, P.K., Josey, C.J., Johnson, A.E., Liang, J. "Depletion
     capabilities in the OpenMC Monte Carlo particle transport code,"
     Ann. Nucl. Energy 152 (2021) 107989.
[12] ASME V&V 20-2009 (R2021) — Standard for Verification and Validation
     in Computational Fluid Dynamics and Heat Transfer.
[13] Weller, H.G. et al. "A tensorial approach to computational continuum
     mechanics using object-oriented techniques," Computers in Physics
     12(6) (1998) 620–631. (OpenFOAM)
[14] OECD/NEA. International Handbook of Evaluated Criticality Safety
     Benchmark Experiments, NEA/NSC/DOC(95)03 — case LEU-COMP-THERM-008.
[15] Horelik, N., Herman, B., Forget, B., Smith, K. "Benchmark for
     Evaluation And Validation of Reactor Simulations (BEAVRS) v1.0.1,"
     Proc. M&C 2013, Sun Valley, Idaho.
```

## Block 2 — codes and standards (unnumbered, cited by name in the text)

```
CODES & STANDARDS

ASME BPVC Section III Div. 1, Subsection NB — Class 1 nuclear components
ASME V&V 20 — verification and validation in CFD and heat transfer  [12]
IEEE Std 603 — safety-system criteria · IEEE Std 384 — Class 1E
   independence · IEEE Std 323 — equipment qualification
10 CFR 50.46 — ECCS acceptance criteria · 10 CFR 100 — reactor site
   criteria · 10 CFR 73.54 — digital-system security
ICRP Publication 116 — external-exposure conversion coefficients
IAPWS-IF97 — thermodynamic properties of water and steam
Tong, L.S. (1967) — W-3 critical-heat-flux correlation
```

This block solves the "cited by name but not listed" problem **without** giving every standard a
number you would then have to bracket in the text. Standards are conventionally cited by designation,
so this is normal practice, not a shortcut.

---

## The bracket changes in the deck

| Slide | Reads now | Change to | Why |
|---|---|---|---|
| **7** verification line | `[7,8,12]` | **`[5][12]`** | [7] is SBF cores and [8] is the Türkiye energy plan — neither is about verification. [5] is the CHF correlations named in the same sentence; [12] is ASME V&V 20. **This is the only wrong bracket in the deck.** |
| **6** gap statement | `[1][3]` | **`[1][3][7]`** | [7] is the SBF core literature — it is what establishes the gap you are claiming. It also keeps [7] cited after the slide-7 change. |
| 7 neutronics line | `[9,10]` | *(no change)* | now resolves to OpenMC + ENDF/B-VIII.0 |
| 7 validation line | `[14,15]` | *(no change)* | now resolves to ICSBEP + BEAVRS |
| 8 broader impact | `[8]` | *(no change)* | correct |
| 43 I&C | `[IEEE 603; IEEE 384; 10 CFR 73.54]` | *(no change)* | now covered by Block 2 |
| 15 fuel | `[SRP 4.2; 10 CFR 50.46]` | *(no change)* | now covered by [6] and Block 2 |

### Two references that would otherwise be listed but never cited

Add these so [11] and [13] are not orphans:

- **Slide 36**, neutronics row — after `OpenMC 0.15.3, ENDF/B-VIII.0, 400 batches` add **`[9,11]`**
- **Slide 36**, thermal-margins row — after `OpenFOAM conjugate hot channel` add **`[13]`**

---

## Layout: this will not fit alongside the glossary

Slide 38 currently holds 8 references **and** a 7-term glossary. Fifteen references plus a standards
block needs the whole slide.

**Recommended:** move the glossary to one of the four empty **BACKUP** slides (39–42) and let slide 38
be references only, in two columns — [1]–[8] left, [9]–[15] right, standards block across the bottom.

The glossary is reference material a juror reads *after* the talk, not during it, so it loses nothing
by moving.

### While you are there — the glossary is thin

Seven terms are defined; the deck uses roughly thirty acronyms. Highest-value additions:

```
CRA   — control-rod assembly · kontrol çubuğu demeti
COLR  — core operating limits report
AOO   — anticipated operational occurrence · beklenen işletme olayı
DBA   — design-basis accident · tasarım esaslı kaza
CDF   — core-damage frequency · çekirdek hasar sıklığı
SSE   — safe-shutdown earthquake · güvenli kapatma depremi
CRDM  — control-rod drive mechanism
TCES  — thermochemical energy storage · termokimyasal enerji depolama
pcm   — per cent mille, 10⁻⁵ Δk/k — the unit of reactivity
tHM   — tonnes of heavy metal · ton ağır metal
BOC / MOC / EOC — beginning / middle / end of cycle
```

Note that **DEC-A** is used on slide 28 but only **DEC** is defined.

---

## Accuracy notes

- **[7]** — I do not have the full citation for the Kim et al. SBF paper. Whoever added it originally
  should supply volume/pages, or replace it with a reference the team can verify.
- **IEEE and ASME edition years** were deliberately omitted from Block 2. Add them only if you know
  which edition was actually used; a wrong year is worse than none.
- **[3]** — NuScale's standard design approval was issued in 2023; if you relied on a specific NRC
  document number (e.g. the FSER), cite that instead of the general description.
- **[14]** — LEU-COMP-THERM-008 is the specific benchmark case behind the −50 pcm bias quoted on
  slide 7. Naming the case, not just the handbook, is what makes that number checkable.
