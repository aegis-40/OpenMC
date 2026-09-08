# Slide build spec — "Sourcing & Construction"

Condenses `33_SOURCING-AND-CONSTRUCTION.md` onto one slide.

> **✅ Built and ready: `Aegis40-Sourcing-Construction-slide.pptx`** (same folder) — one slide, sized
> 10 × 5.625 in to match Google Slides. Open it, select all, copy, paste into the deck. Rebuild script:
> `scratchpad/build_sourcing_slide.py`. The spec below documents what is on it and how to adjust it.

**This is a second slide, not a replacement for `31`.** They do different jobs:

| Slide | Job |
|---|---|
| **31 — Realization Strategy** | *Why and how* — the three points, the argument |
| **34 — Sourcing & Construction** *(this one)* | *What and from where* — the evidence behind it |

If you only have room for one, keep 31 (its bottom strip carries the headline) and hold this as the
backup that survives a detailed question. If you have room for both, this one follows immediately.

**Layout: two zones + a bottom band.** Left = sourcing table. Right = construction management. Band =
the punchline. On-slide word count ≈ 210 — dense, but it is a reference slide and that is allowed.

---

# PART 1 — PURE TEXT, COPY FROM HERE

## Title

```
Sourcing & Construction — What We Order, and From Where
```

## LEFT ZONE — table header

```
SYSTEM                          ROUTE     SOURCE
```

## LEFT ZONE — ten rows

```
Turbine-generator, 40 MWe        ◐   Fuji / Toshiba / MHI class — all three have delivered
                                     this size to Turkish geothermal. TR kit ~55 % local
Condenser, feed heaters, BOP pumps ●  Domestic — conventional equipment
RPV + internals, 3.414 m OD      ○→◐  Partner licence-build; domestic target by unit ~5
Integral OTSG, 16 CRAs + CRDMs   ○   Nuclear-island partner
Fuel — 37 FA, UO₂ + Gd/Er        ○   Global fabricators; enrichment is a service contract
B₄C absorber, 90 % B-10          ○●  Separation imported — ore is Turkish, Eti Maden ~70 %
                                     of world reserves
Safety valves, Class 1E I&C      ○   Buy units 1–3; qualify domestic FPGA in parallel
Transformers, gensets, batteries ●   Domestic manufacture
Civil, buildings, tanks, containment ● 48 Turkish firms in ENR Top 250 — 2nd worldwide
TCES store, H₂ balance-of-plant  ●   Chemical-process, not nuclear (SOE stack imported)
```

## LEFT ZONE — route key

```
● domestic now      ◐ domestic within 5 yr      ○ imported
```

## RIGHT ZONE — block 1

```
DELIVERY MODEL

Owner — Turkish SPV under the state nuclear entity
Civil + conventional island — domestic EPC
Nuclear island — technology transfer, units 1–4
Commissioning — joint, domestic by unit 3

Not Akkuyu's build-own-operate.
```

## RIGHT ZONE — block 2

```
WHY THE SCHEDULE HOLDS

Integral primary system — no external loop, no
surge line, no large-bore primary piping. Removes
the site field-welding scope where nuclear projects
historically lose schedule.

Parallel, not serial — licensing runs alongside
procurement; modules are built while civil proceeds.
```

## RIGHT ZONE — block 3 (boxed, outlined)

```
CRITICAL PATH
RPV forging, 2–3 yr  ·  construction licence
Both must start in Y1–Y2 or the schedule does not hold.
```

## BOTTOM BAND (full width)

```
NEVER ORDERED AT ALL —  no reactor coolant pumps  ·  no seals or seal injection  ·  no boron plant  ·  no surge line  ·  no external CRDM housings
```

---

# PART 2 — LAYOUT

Google Slides 16:9 = **10.0 in × 5.63 in**.

| Element | x | y | w | h | Size |
|---|---|---|---|---|---|
| Title | 0.40 | 0.20 | 9.2 | 0.45 | **24 pt bold** |
| Left table | 0.40 | 0.82 | 5.50 | 3.55 | 8 pt |
| Route key | 0.40 | 4.42 | 5.50 | 0.20 | 7.5 pt italic |
| Right block 1 | 6.10 | 0.82 | 3.50 | 1.25 | see below |
| Right block 2 | 6.10 | 2.17 | 3.50 | 1.45 | see below |
| Right block 3 (boxed) | 6.10 | 3.72 | 3.50 | 0.65 | 8 pt, 1 pt outline |
| Bottom band | 0.40 | 4.72 | 9.20 | 0.45 | 9 pt |
| Source line | 0.40 | 5.26 | 9.20 | 0.22 | 7 pt italic, grey |

**Left table columns:** System `1.85 in` · Route `0.40 in` (centred) · Source `3.25 in`.
Header row 8 pt bold caps; body 8 pt; row height ~0.33 in; alternate row fill very light.

**Right blocks:** heading **9 pt bold caps** in accent colour; body 8.5 pt, line spacing 1.2.

---

# PART 3 — THE ROUTE SYMBOLS

Do **not** use emoji or flags — they render inconsistently in Google Slides and print badly.

Use three small filled circles, same size, differing only in fill:

| Symbol | Meaning | Fill |
|---|---|---|
| ● | domestic now | your deck accent, solid |
| ◐ | domestic within 5 yr | accent at ~40 % opacity, or half-filled |
| ○ | imported | outline only, no fill |

Insert as a shape (Insert → Shape → Oval, 0.10 in) rather than as a text character, so they stay aligned.
The `○→◐` on the RPV row means *imported now, domestic later* — draw it as two circles with a small arrow.

**Count the dots when you are done.** Five ● rows, one ◐, three ○, one mixed. If the slide looks
mostly-imported at a glance, the dots are wrong — half this table is domestic today, and that is the
message.

---

# PART 4 — EMPHASIS

Four things loud, nothing else:

1. **`Fuji / Toshiba / MHI`** — bold. The literal answer to the question that was asked.
2. **`2nd worldwide`** on the civil row — bold.
3. **`Not Akkuyu's build-own-operate.`** — bold, and give it its own line with space above.
4. **The whole bottom band** — reverse it out: accent or dark fill, light text. It is the punchline and
   it should read as a single stripe, not as a list.

**The critical-path box is outlined, not filled.** It should look like a caveat you volunteered, because
that is exactly what it is — and volunteering it is what makes the rest credible.

---

# PART 5 — BUILD ORDER

1. Title
2. Left table — build the header row and one body row, get the column widths right, then duplicate
3. Fill all ten rows of text before inserting any dots
4. Insert one ● as a shape, size it, then copy-paste it down the column and change fills
5. Route key under the table
6. Right zone: three blocks, top to bottom; outline the third
7. Bottom band last, full width, reversed out
8. Read at 50 % zoom — the bottom band and the bolded vendor names should be the two things you see

---

# PART 6 — IF IT IS TOO DENSE

Cut in this order. **Never cut the bottom band or the turbine row.**

1. Drop the route key and put the legend in your notes (the dots are still self-evident in context)
2. Merge rows: `Condenser, feed heaters, BOP pumps` + `Transformers, gensets, batteries` → one
   `Conventional BOP + electrical ● Domestic manufacture` row
3. Merge `Integral OTSG, CRAs + CRDMs` into the RPV row as `RPV, internals, OTSG, CRAs`
4. Drop right-zone block 2's second paragraph (`Parallel, not serial`) — say it out loud
5. Drop the source line

That takes ten rows to seven and buys real breathing room.

**If it still will not fit:** split into 34a (sourcing table, full width, all 22 rows from `33` Part 2)
and 34b (construction management). But try the cuts first — one slide is stronger here.

---

# PART 7 — SOURCE LINE FOR THE SLIDE FOOT

```
Sources: NucNet (Akkuyu local content, 2025) · ENR Top 250 International Contractors 2026 · Balkan Green Energy News (TR geothermal equipment localisation) · vendor releases (Fuji, Toshiba, MHI) · Aegis-40 FER §8.10, §8.12
```

---

# PART 8 — THE 40-SECOND WALK-THROUGH

> "This is the equipment question answered directly.
>
> **Left side, what we order and from where.** The dots are domestic today, domestic within five years,
> and imported. **Roughly half this list is domestic today** — civil, buildings, tanks, containment,
> transformers, generators, balance-of-plant pumps, the thermal store.
>
> **The turbine, since that was the question:** ours is a forty-megawatt saturated-steam machine, which
> is the geothermal class, not the nuclear class. **Fuji Electric, Toshiba and Mitsubishi have each
> delivered a turbine of this size to a Turkish site**, and Turkish geothermal equipment is already about
> fifty-five percent localised. That is a real supply base, not a hypothetical one.
>
> **Imported: fuel, the vessel forging, safety-class valves and the Class 1E instrumentation platform.**
> The boron absorber is interesting — the ore is Turkish, Eti Maden holds around seventy percent of world
> reserves, so only the isotope separation is bought in.
>
> **Right side, how it gets built.** Domestic EPC for civil and the conventional island, nuclear island
> under technology transfer for the first units — deliberately not the build-own-operate model used at
> Akkuyu. And the design protects the schedule: because the primary system is integral, there is no
> external loop and no large-bore primary piping to weld in the field, which is where nuclear
> construction normally loses time.
>
> **Our critical path is the vessel forging at two to three years, and the construction licence.** If
> either slips, the schedule slips.
>
> And along the bottom — **the things we never order at all.** No reactor coolant pumps, no seals, no
> boron plant, no surge line. The cheapest component to localise is the one you do not have to buy."
