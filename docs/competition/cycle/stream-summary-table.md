# Aegis-40 iPWR — PFD Stream Summary Table

Companion to **Fig 8.9-3** (`aegis40_cogen_pfd.drawio` / `pfd_cogeneration_tces.png`). Stream
numbers (S1…) on the PFD key into the rows below. Secondary-cycle state points are the design-point
heat balance from `scripts/thermo_cycle.py` (regenerative superheated Rankine cycle, IAPWS-IF97),
scaled to **ṁ = 57.75 kg/s** boiler steam at 125 MWth → 39.7 MWe net (η = 31.8 %), 40 MWe nameplate.
TCES/DH and H₂ streams are from `scripts/tces_dh_balance.py`.

Basis tags: **C** = computed (`thermo_cycle.py` / `tces_dh_balance.py`) ·
**A** = assumed/Tier-B (confirm with §8.4 T-H) · **O** = off-design / mode-dependent
(not concurrent with the 40 MWe baseload design point).

---

## A. Secondary cycle — process streams (baseload design point, TCES idle)

| # | From → To | Fluid / service | ṁ (kg/s) | P (MPa) | T (°C) | Phase (x) | h (kJ/kg) | Basis |
|---|-----------|-----------------|---------:|--------:|-------:|-----------|----------:|:-----:|
| **S1** | OTSG → header → TCV → HP turbine | main steam | 57.75 | 4.50 | 296.0 | sup. vapour (1.000) | 2932.1 | C |
| **S2** | HP turbine → FWH-1 (and IHX tap) | HP extraction steam | 7.70 | 1.00 | 179.9 | wet (0.950) | 2676.8 | C |
| **S3** | crossover → deaerator (FWH-2) | LP extraction steam | 6.01 | 0.15 | 111.4 | wet (0.873) | 2409.8 | C |
| **S4** | LP turbine → condenser | LP exhaust | 38.44 | 0.007 | 39.0 | wet (0.892) | 2310.9 | C |
| **S5** | condenser → CP → deaerator | condensate | 38.44 | 0.007→0.15 | 39.0 | sat. liquid (0) | 163.4 | C |
| **S6** | deaerator → BP → FWH-1 | deaerated feed | 50.05 | 0.15→1.00 | 111.4 | sat. liquid (0) | 467.1 | C |
| **S7** | FWH-1 → FP → OTSG | feedwater | 57.75 | 4.50 | 180.6 | subcooled liquid | 767.5 | C |

> Mass check: S1 = 57.75 in; HP bleed S2 (7.70) + DA bleed S3 (6.01) + last-stage to condenser
> (38.44) + moisture-separator drain (≈5.60, drains to DA) = 57.75 out. ✔ Feedwater returns to
> 57.75 at S7 (FWH-1 adds the S2 extraction back into the (1−y₁) deaerated flow).
>
> **Single turbine-generator:** S1→S4 all expand through one tandem-compound machine (HP + moisture
> separator + LP on one shaft, one generator). No second turbine — the TCES charge uses an
> *extraction* bleed (§D), not a dedicated back-pressure unit. (§8.9, construction/economics.)

## B. Primary circuit (in-vessel, natural circulation)

| # | Path | Fluid | ṁ (kg/s) | P (MPa) | T (°C) | Phase | Basis |
|---|------|-------|---------:|--------:|-------:|-------|:-----:|
| **P1** | core → riser → OTSG (hot leg) | primary coolant | ~483 | 12.8 | 308 | subcooled liquid | C |
| **P2** | OTSG → downcomer → core (cold leg) | primary coolant | ~483 | 12.8 | 258 | subcooled liquid | C |

> No reactor coolant pumps — flow is buoyancy-driven. ṁ ≈ Q/(c_p·ΔT) = 125 MW /(5.18 kJ/kg·K · 50 K)
> ≈ 483 kg/s; driving head 2.62 kPa over H_th 2.85 m, hot-leg subcooling 21.7 °C (§8.4,
> `scripts/natcirc_primary.py`).

## C. Utility streams — **seawater once-through ultimate heat sink** (Black Sea, Sinop)

| # | Path | Fluid | ṁ (kg/s) | T (°C) | Notes | Basis |
|---|------|-------|---------:|-------:|-------|:-----:|
| **SW1** | sea intake → condenser (tube side) | seawater | ~2,065 | 25 → 35 | intake; ≈ 2.04 m³/s; coarse + fine screens | C |
| **SW2** | condenser → diffuser outfall → sea | seawater | ~2,065 | 35 → sea | rejects Q = 82.6 MWth; ΔT_cond ≤ 10 K; **no evaporative water use** | C |
| **Sel** | generator → grid | electricity | — | — | **40 MWe nameplate** (39.7 net: gross 42.2, −0.36 pumps, −2.11 BOP) | C |

> **No cooling tower** — once-through seawater (brackish, ~18 psu; c_p ≈ 4.00 kJ/kg·K, ρ ≈ 1012 kg/m³).
> Intake ṁ = Q/(c_p·ΔT_cond) = 82.6 MW/(4.00·10) ≈ **2,065 kg/s (2.04 m³/s)** for a 10 K condenser
> rise. Summer (intake ~25 °C) is the absolute-temperature-limiting case: outfall 25→35 °C at ΔT=10 K;
> a managed ΔT=7 K (ṁ ≈ 2,950 kg/s) caps the pipe at **32 °C**. Sea-temperature impact is in §D-note
> below and `scripts/seawater_heat_sink.py` / `seawater_plume_dilution.png`. Seasonal intake 8 °C
> (winter) → 25 °C (summer).

## D. Thermochemical energy storage (TCES) — IHX-isolated, **non-safety auxiliary**

The store sits **outside the nuclear island**. It is charged by an HP-extraction *bleed* routed
through an **intermediate heat exchanger (IHX)** — the IHX is the isolation boundary, so the storage
medium (salt–NH₃ or zeolite–water) never contacts reactor steam. The reactor stays at 125 MWth
baseload throughout; charge happens **off-peak / low-DH-demand** and discharge at **peak / winter**.
Charge and discharge streams are **not concurrent**. Primary medium = **ammine** (NiCl₂·6NH₃ / NH₃);
**zeolite-13X / H₂O** is the ammonia-free alternative (values in brackets).

| # | From → To | Fluid / service | ṁ (kg/s) | P (MPa) | T (°C) | Mode | Basis |
|---|-----------|-----------------|---------:|--------:|-------:|------|:-----:|
| **C1** | S2 tap → IHX (steam side) | HP-extraction bleed | ≤ 7.4 | 1.00 | 179.9 | charge | C |
| **C2** | IHX → closed charge loop → store | charge-loop water | (sized) | ~1.0 | 90 → 168 | charge | C |
| **C3** | IHX steam side → feedwater drain | condensate drain | ≈ C1 | 1.00→0.15 | 180 → 111 | charge | C |
| **C4** | reactant store ⇄ sorbate store | NH₃ vapour [H₂O vapour] | (sized) | ~1.5 [~0.01] | desorb 168 / sorb ~150 [~130] | both | A |
| **D1** | store → DH HX (storage side) | discharge heat carrier | (sized) | low | ~150 [~130] → return | discharge | C |
| **D2** | DH HX → district network (supply) | DH water | 133 | ~1.6 | 45 → 90 | discharge | C |
| **D3** | district network → DH HX (return) | DH water | 133 | ~1.6 | 90 → 45 | discharge | C |

> **Sizing (`tces_dh_balance.py`, 25 MWth × 8 h discharge):** ammine store ≈ 735 t / ≈735 m³
> (0.272 kWh/kg bulk); zeolite ≈ 1000 t / ≈1540 m³ (0.20 kWh/kg). Round-trip 0.88 ammine /
> 0.78 zeolite. **Charge penalty z = 0.31 MWe per MWth** stored (lost expander work of the bled
> S2 steam) → baseload dips to ≈ 35.6 MWe while charging; the store then holds **loss-free**
> (chemical bond), enabling day-shift or full-season storage. DH water 90/45 °C, 133 kg/s ≙ 25 MWth.

## E. Co-generation off-takes

| # | From → To | Fluid | ṁ / rating | Notes | Basis |
|---|-----------|-------|-----------:|-------|:-----:|
| **H1** | generator (off-peak) → PEM electrolyser | electricity | 8 MWe | surplus off-peak power | O |
| **H2** | PEM electrolyser → H₂ storage | hydrogen | ~160 kg/h | ≈ 50 kWh/kg → ≈ 640 t/yr | C |
| **H3** | TCES discharge → electrolyser feed pre-heat | hot water | (optional) | discharge heat pre-heats PEM feed water | A |
| **Tdh** | DH HX → district heating network | hot water | 25 MWth | the §D D2/D3 loop, listed here as the heat product | C |

> Electrolyser is **PEM** (low-temperature, modular, off-peak-dispatchable) — supersedes the earlier
> SOE option. H₂ and DH heat add to annual energy utilization (capacity factor); they do not subtract
> from the 40 MWe nameplate, which is the TCES-idle baseload point.

---

### Notes
1. **40 MWe is the TCES-idle baseload point.** TCES/DH/H₂ off-takes shift *when/where* the product is
   delivered; the reactor is constant at 125 MWth. The 0.31 MWe/MWth charge penalty is paid only
   during off-peak charging (≈ 35.6 MWe), and is recovered as district heat at peak. See §8.9.
2. State points S1–S7 regenerate from `scripts/thermo_cycle.py` → `cycle_state_points.csv`;
   TCES/DH/H₂ figures from `scripts/tces_dh_balance.py` → `tces_dh_balance.csv`.
3. **Heat source for TCES = HP-extraction bleed (S2, 1.0 MPa/180 °C) through the IHX — taken
   off-peak.** Source (turbine extraction) and timing (off-peak hours/summer) are independent and
   both apply; main steam is deliberately *not* tapped (grade mismatch — the store needs only ~168 °C).
4. Tier-B / assumed values (primary P1/P2, NH₃/H₂O sorbate streams C4, pre-heat H3) are flagged
   for confirmation against the §8.4 thermal-hydraulics analysis and detailed TCES design.
5. **Sea-temperature impact (`scripts/seawater_heat_sink.py`).** The 82.6 MWth condenser load
   leaves the outfall at +10 K (design). The regulated metric is the *far-field* excess after
   near-field dilution: a multiport diffuser reaches **10–50× dilution within tens of metres**,
   giving an edge-of-mixing-zone rise of **0.9 K (10×) down to 0.2 K (50×)** — comfortably inside
   the typical **≤ 3 K** mixing-zone cap (met at only ~3× dilution). With a modest Black Sea
   longshore current (0.05–0.20 m/s over a 10 m × 200 m section), the far-field rise is **0.05–0.20 K**,
   i.e. negligible against natural seasonal swing (8→25 °C). Once-through also has **zero consumptive
   (evaporative) water use**, unlike a wet tower. See `seawater_plume_dilution.png` and §8.4/§8.9.
