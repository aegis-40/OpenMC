# Aegis-40 spent-fuel arisings & waste intensity vs CAREM-25 (FER §8.11) — generated

- Generated: `2026-06-05T16:32:48.264322+00:00`
- Source: `aegis40.back_end.fuel_cycle` (validated, 15/15 tests) on the LOCKED rev_3 design basis (`docs/competition/design-basis-locked.md`).
- Headline metric: **tonnes initial heavy metal discharged per TWh electric (tHM/TWhe)** — lower = less waste per unit energy.

## 1. Aegis-40 spent-fuel arisings (once-through)

| Quantity | Value |
|---|---|
| HM discharged per cycle | 1.325 tHM |
| Assemblies discharged per cycle | 5.25 FA |
| Calendar days per cycle (CF 0.90) | 532 d |
| Cycles per year | 0.686 |
| **HM discharged per year** | **0.909 tHM/yr** |
| **Assemblies discharged per year** | **3.60 FA/yr** |
| Electric energy per cycle | 0.460 TWhe |
| Thermal energy per cycle | 1.437 TWhth |
| **Waste intensity** | **2.88 tHM/TWhe** (0.92 tHM/TWhth) |

_The module value (2.88 tHM/TWhe) uses the as-modeled initial HM of 5.3 t; the burnup x efficiency identity gives 3.04. The ~5% spread is the known 5.3-vs-5.6 tHM / 42.8-vs-~45 GWd/t self-consistency band (confirm exact fresh iHM via `--step 0`). Both round to ~3 tHM/TWhe._

## 2. Waste intensity vs the reference reactor (CAREM-25)

Once-through identity `tHM/TWhe = 1e6 / (BU[MWd/tHM] x 24 x eta)`, `eta = P_e/P_th` — depends only on discharge burnup and thermal efficiency, so the comparison does not hinge on CAREM's exact HM loading or batch scheme.

| Reactor | P_th (MWth) | P_e (MWe) | eta | Discharge burnup (GWd/tHM) | tHM/TWhe | note |
|---|---|---|---|---|---|---|
| Aegis-40 (ours, rev_3) | 125 | 40 | 0.320 | 42.8 | **3.04** | SBF iPWR, Gd+Er, 4-batch, 479 EFPD |
| CAREM-25 (reference) | 100 | 27 | 0.270 | 24.0 | **6.43** | SBF iPWR, Gd-only, ~3.1 wt%, 27 MWe central (25-30 band) |

- CAREM-25 intensity band over 25-30 MWe: **5.79-6.94 tHM/TWhe** (central 6.43).
- **Aegis-40 is ~2.1x lower waste intensity than CAREM-25 (~53% reduction in tHM/TWhe)** — less than half the heavy-metal arisings per unit electricity.

## 3. Why — the high-burnup + SBF design choice

- **Discharge burnup 42.8 vs ~24 GWd/tHM** is the dominant lever: ~1.8x more energy extracted per tonne of fuel before discharge.
- **Thermal efficiency 0.32 vs ~0.27** (higher steam conditions) adds a further factor.
- Together they roughly halve tHM/TWhe. Dropping Aegis-40 to a CAREM-like ~3.1 wt% / ~24 GWd/t point would roughly double our arisings and forfeit the fuel-efficiency / waste score — this is the quantitative reason the high-burnup choice is kept (see `reference-reactors-comparison.md`).
- **SBF (soluble-boron-free)** additionally eliminates the borated-water secondary-waste stream (spent resins, evaporator concentrates, tritiated boron effluent) that a boron-controlled PWR generates — a separate 'reduce waste quantity' win not captured in the tHM/TWhe number (see deliverable #12).

## Method notes & caveats

- **Initial heavy metal (iHM)** basis throughout (tonnes charged), the standard fuel-cycle convention for waste intensity.
- CAREM-25 parameters are published figures (INVAP/CNEA, IAEA ARIS): 100 MWth, ~25-30 MWe, ~24 GWd/tU, boron-free + Gd. Electric output is quoted variously across sources; the 25-30 MWe band brackets it.
- The comparison is **per-unit-energy**, which is the fair basis for reactors of different size. Absolute arisings (Section 1) are tiny in any case: <1 tHM/yr and <4 FA/yr for Aegis-40.
- Jang SBF-SMPWR (ultra-long 1555 EFPD) would also score very low intensity but its published burnup is not tabulated here; CAREM-25 is the team's chosen named reference per spec p.17.
