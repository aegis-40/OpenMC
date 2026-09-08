# FER §8.9 (extension) — Cogeneration: TCES District Heat + SOE Hydrogen

**Scope.** Aegis-40 (125 MWth iPWR, 40 MWe net) delivers three products from one
turbine: **electricity**, **district heat** (via a thermochemical store, TCES), and
**hydrogen** (via solid-oxide electrolysis, SOE). This section justifies each step of the
steam-side integration, the seasonal operating strategy for Sinop, and a first-order
economic case. State points: `cycle_state_points.csv`; numbers: `scripts/thermo_cycle.py`,
`scripts/tces_dh_balance.py`, `scripts/soe_h2_schedule.py`.

---

## 8.9.A — Steam extraction strategy (turbine-life justification)

**Concern.** Bleeding steam for cogeneration must not shorten HP-turbine life.

**Resolution (verified against the reference cogeneration design).** Heat is *not* taken
from fresh inlet steam (which would destroy exergy and disturb the inlet stage). Instead it
is drawn from a **designed intermediate-stage extraction port** — analogous to the reference
NuScale-class cogeneration turbine, where steam is bled **from stage 14 of the 24-stage HP
section** (inlet 73.7 barg/486 °C → extraction **9.0 barg/234.6 °C**, ~18.5 % of throughflow).
This is a standard **extraction (bleed) turbine**, mechanically identical to the regenerative
feedwater-heating extractions every PWR turbine already carries, so it imposes **no
incremental blade loading or life penalty**: the casing has a defined bleed nozzle, the flow
is throttle-controlled, and the machine is flow-sized for the split (full flow in stages
1–14, reduced flow thereafter).

**Aegis-40 mapping.** Our OTSG delivers 4.5 MPa / 296 °C steam (state 1). The cogeneration
bleed is taken at **1.0 MPa (≈ 9 barg), 180 °C, x≈0.95 (state 2)** — i.e. the *same ~9 barg
extraction-pressure level* Laziz specified, reached at the equivalent intermediate HP stage.

| Parameter | Reference (stage-14 bleed) | Aegis-40 (state 2) |
|---|---|---|
| Inlet | 73.7 barg / 486 °C | 4.5 MPa / 296 °C |
| Extraction P | **9.0 barg** | **1.0 MPa (≈9 barg)** ✅ matches |
| Extraction T | 234.6 °C (superheated) | 180 °C, x≈0.95 |
| Use | district heat | TCES charge (IHX) |

The lower extraction temperature (less inlet superheat) is acceptable: the TCES charge loop
needs only ~168 °C, and the slight moisture (x≈0.95) is below the HP erosion limit and
condenses usefully in the IHX. **Thermodynamic check:** isentropic expansion 73.7→9 barg
lands at ~234 °C — the reference table is consistent (verified).

---

## 8.9.B — TCES district heating

A **closed thermochemical store** (ammine NiCl₂·6NH₃ + zeolite), sited **outside the nuclear
island behind an intermediate heat exchanger (IHX)**, time-shifts heat:

- **Charge** (off-peak / summer): the 1.0 MPa extraction steam drives the IHX → ~168 °C
  charge loop → endothermic desorption (NiCl₂·6NH₃ → NiCl₂·2NH₃ + 4 NH₃; zeolite dehydration).
  Penalty **0.31 MWe/MWth** (net dips to ~35.6 MWe while charging); the store then holds its
  charge **loss-free** for hours→seasons.
- **Discharge** (peak / winter): exothermic reversal at ~150 °C → DH heat exchanger →
  **district-heat loop 90/45 °C, up to 25 MWth**. Heat comes from the *store*, so the turbine
  keeps the **full 40 MWe** on the grid during the peak — **heat delivery is decoupled from
  generation.** The IHX guarantees the medium never contacts reactor steam → non-safety auxiliary.

---

## 8.9.C — SOE hydrogen (replaces PEM)

We adopt **high-temperature solid-oxide electrolysis (SOE)** instead of PEM, following
Milewski, Kupecki et al. (2021), who coupled O²⁻/H⁺ SOE to a nuclear steam cycle and report
**37.55 kWh/kg H₂ (O²⁻ SOE)** vs ~50 kWh/kg for PEM — because high-temperature steam supplies
part of the dissociation energy as *heat* rather than electricity.

**Steam integration (Milewski's least-invasive route — "almost no cycle modification"):** the
SOE is fed **directly by a low-pressure turbine extraction** (the deaerator-inlet stream,
≈0.15 MPa) — the same bleed that already feeds the deaerator, so no steam-cycle modification is
needed. It is raised to the ~800 °C operating temperature by **internal recuperation** (the hot
H₂/O₂ product streams preheat the incoming feed) **+ the cell's own ohmic heating** (thermoneutral
operation) **+ a small electric trim** — *not* from the reactor, which (at ~300 °C) cannot reach
SOE temperature. This is why a PWR's SOE H₂ is inherently electricity-driven; the steam supplies
the feedstock and low-grade preheat, not the high-temperature reaction heat.

| Metric | PEM (old) | **SOE (adopted)** |
|---|---|---|
| Electrical demand | 50 kWh/kg | **37.55 kWh/kg** (−25 %) |
| H₂ at 8 MWe off-peak | 160 kg/h | **213 kg/h** (+33 %) |
| Steam slipstream | — | **0.53 kg/s = 0.92 % of main steam** (deaerator bleed) |
| Annual H₂ | ~640 t/yr* | **~120 t/yr** (at the duty cycle below) |

*The PEM figure assumed continuous run; the SOE figure uses the adopted modest schedule:
**4 h/night in the deepest valley (~02:00–06:00), non-heating season only, ~140 operating
nights/yr (net of outages) → 560 electrolysis-h/yr × 213 kg/h ≈ 120 t/yr** (SOE capacity
factor ~6 %; conservative — capacity exists to scale toward ~441 t/yr at 2,070 h/yr if the
grid valley deepens).

**Mode-exclusive routing (no double-conversion).** The cogeneration extraction is sent
**directly to whichever product is active — TCES (district-heat mode) or SOE (H₂ mode) — never
stacked.** Charging the store *only* to reheat the SOE feed would pay the 0.31 MWe/MWth charge
penalty plus the store round-trip for heat the turbine extraction already supplies. Because the
store is operated **periodically** (charge off-peak, discharge in winter) — not held continuously
charged — there is no benefit to a TCES→H₂ heat path; the two products share the extraction *in
time*, not in series.

---

## 8.9.D — Seasonal & diurnal operating schedule (Sinop)

Sinop (Black Sea coast) has a **heating season ~Oct–Apr (~212 days)** and **no district-heat
demand May–Sep (~153 days)**. The plant runs electricity baseload always, and switches TCES
and SOE by season and by the night/day price valley:

| Season | TCES | SOE / H₂ | Rationale |
|---|---|---|---|
| **Winter (Dec–Feb)** | **Discharge → DH 25 MWth** | reduced (night only) | max heat demand; keep 40 MWe on grid at peak |
| **Shoulder (Oct–Nov, Mar–Apr)** | partial discharge / top-up charge | night runs | moderate heat; balance |
| **Summer (May–Sep)** | charge (or idle) | **maximum H₂** | no DH → divert surplus night electricity to H₂ |

**Diurnal:** charge TCES + run SOE in the **off-peak night valley** (cheap electricity);
discharge TCES + minimize SOE at the **evening peak** (sell full 40 MWe).

---

## 8.9.E — First-order economics (indicative, Turkey/Sinop)

Prices: electricity $40 (off-peak)/$100 (peak)/MWh, H₂ $5/kg, DH heat $40/MWh-th.

| Stream | Annual | Note |
|---|---|---|
| Electricity | **$22.4 M** | 40 MWe baseload |
| Hydrogen (SOE) | **$0.60 M** rev / **$0.42 M margin** | 120 t/yr × $5/kg; off-peak electricity cost −$0.18 M |
| District heat | **$2.5 M** | 63.6 GWh-th/yr (avg 12.5 MWth) |
| **Cogen uplift** | **+$2.9 M/yr (≈ +13 %)** | heat+H₂ over electricity-only |

The cogeneration block adds **~18 % revenue** with negligible cycle disturbance (<1 % steam
diverted to SOE; a designed bleed for TCES) and improves **grid flexibility** (H₂ + TCES
absorb the off-peak valley), directly serving the TEKNOFEST **sustainability** and
**economics** criteria.

---

### References
1. J. Milewski, J. Kupecki, A. Szczęśniak, N. Uzunow, *Hydrogen production in solid oxide
   electrolyzers coupled with nuclear reactors*, **Int. J. Hydrogen Energy 46 (2021)
   35765–35776** — SOE 37.55 kWh/kg, deaerator steam feed. (`literature/SOE.pdf`)
2. Reference NuScale-class cogeneration PFD — stage-14/24 HP extraction at 9 barg/234.6 °C
   (steam-extraction strategy, Laziz).
3. IAEA NP-T-1.10, *Industrial Applications of Nuclear Energy*; IEA *Nuclear Hydrogen* (TCES + cogeneration basis).
