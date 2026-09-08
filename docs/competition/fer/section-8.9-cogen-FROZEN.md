# 8.9 Energy Cycle and Integrated Systems — FROZEN design point

*(Aegis-40, 2026-07-04. TCES material = **zeolite-13X (ammonia-free)** frozen as the reference store;
NiCl₂–SrCl₂/NH₃ ammine retained as the evaluated higher-density alternative, quantified by the
validated `tces` model — github.com/alishsan/tces, reproducing Yan et al. 2020. H₂ operating hours
frozen at 120 t/yr. Digital appendix: `7_energy_cycle/`, `9_tces_model/`.)*

## 8.9.1 Energy-conversion architecture

A single tandem-compound turbine-generator converts the 125 MWth core output to **40.0 MWe net**
(net efficiency 32.0 %) through a saturated-steam Rankine cycle: helical once-through steam
generator → main steam **4.5 MPa / 296 °C / 57.8 kg/s** → HP+LP turbine on one shaft → seawater-cooled
condenser (7 kPa, 39 °C; Black Sea once-through). Two co-products are taken from the secondary side
on a **non-safety, balance-of-plant (BOP)** branch, IHX-isolated from the nuclear island:
thermochemical district heat (TCES) and off-peak hydrogen (SOE). State points: Fig. 8.9-1 (labeled
PFD) and Table 8.9-2; T-s diagram Fig. 8.9-3.

## 8.9.2 Thermochemical energy storage (TCES) for district heat — FROZEN

**Material (frozen): Zeolite-13X / water adsorption store.** Zeolite-13X is adopted as the reference
storage medium because it is **ammonia-free** (no toxic/flammable NH₃ inventory → no ammonia hazard
QRA, simpler nuclear-site licensing), uses a **benign water working fluid**, is a **mature,
commercially deployed adsorbent**, and is thermally stable over many cycles. The accepted trade-off
is lower energy density than an ammoniate salt (larger footprint) and a lower discharge temperature —
both acceptable for a 90/45 °C district-heat network.

**Charge/discharge integration.** The store is charged from a **stage-14 HP turbine extraction
(1.0 MPa, ~180 °C)** stepped through an **intermediate heat exchanger (IHX)** to a **~168 °C charge
loop** (12 °C IHX pinch) that regenerates (desorbs) the zeolite bed; main steam (280–320 °C) is not
coupled to the bed. On discharge, water re-adsorption releases heat at ~130 °C into a **separate
90/45 °C district-heat water loop**. The IHX and the ammonia-free medium keep the store a non-safety
auxiliary with no chemical/water-quality path into the reactor steam cycle.

**Frozen sizing (from `tces_dh_balance.py`, 25 MWth DH peak / 200 MWh_th daily block):**

| Frozen TCES parameter | Zeolite-13X (reference) |
|---|---|
| Storage medium | zeolite-13X / H₂O adsorption |
| Energy density | 0.20 kWh/kg (uptake ~0.22, ΔH ~3500 kJ/kg-H₂O) |
| Store mass / volume | **~1000 t / ~1538 m³** |
| Delivered block | **200 MWh_th** per discharge (≈ 8 h at 25 MWth peak) |
| District-heat delivery | **25 MWth peak / 12.5 MWth seasonal-avg**, 90/45 °C |
| Discharge (adsorption) temperature | ~130 °C (≥ DH supply with margin) |
| Charge loop | HP extraction 1.0 MPa/180 °C → IHX → ~168 °C bed regeneration |
| Round-trip efficiency | ~0.78 (charge penalty ~4.9 MWe while charging) |
| Standby loss | **none** — adsorbed state holds indefinitely (loss-free); enables flexible day-to-season time-shifting of the daily block, unlike sensible molten-salt tanks |
| Store classification | non-safety BOP; IHX-isolated |

**Evaluated higher-density alternative — NiCl₂–SrCl₂/NH₃ ammine (validated, not adopted).** A
higher-density ammoniate resorption store was quantitatively evaluated with the open `tces`
thermodynamic model, which **reproduces the Yan et al. (2020) published performance exactly**
(validation table below). At the same 200 MWh_th / 25 MWth design point it is **~2× more compact
(~735 t / ~735 m³)** with a higher round-trip efficiency (~0.88) and 150 °C discharge. It was **not
adopted** because the ammonia inventory adds a hazard-analysis and licensing burden that the
compactness gain does not justify for a nuclear BOP. Its inclusion demonstrates the material choice
is the result of a quantitative, validated trade study rather than an assumption.

**`tces` model validation (ammine alternative, vs Yan et al. 2020, X = 0.85, μ = 8):**

| Mode | COPh (model) | COPh (Yan 2020) | γ_h (kJ/kg) |
|---|---|---|---|
| direct | 0.973 | 0.973 | 1692.8 |
| upgrade | 0.550 | 0.550 | 1427.8 |
| combined | 0.902 | 0.902 | 2099.8 |

## 8.9.3 Hydrogen (SOE electrolyser) — FROZEN

**The 120 t/yr vs 441 t/yr conflict is resolved in favour of 120 t/yr** (a modest, defensible duty).
The 441 t/yr figure (2,070 h/yr, ~24 % capacity factor) is **withdrawn**; the frozen basis is the
deep-night-valley schedule:

| Frozen SOE parameter | Value |
|---|---|
| Electrolyser | solid-oxide (O²⁻ route), ~800 °C, **8 MWe** off-peak |
| Specific energy | 37.55 kWh/kg (Milewski 2021; vs 50 for PEM) |
| Instantaneous rate | 213 kg/h |
| **Operating schedule** | **4 h/night in the deepest valley (~02:00–06:00), non-heating season only, ~140 nights/yr** |
| Electrolysis hours | 560 h/yr (SOE capacity factor ~6 %) |
| **Annual H₂ production** | **≈ 120 t/yr** |
| Steam slipstream | 0.53 kg/s (0.9 % of main steam, deaerator bleed ~0.15 MPa) |

Capacity headroom exists to scale toward ~441 t/yr if the grid off-peak valley deepens, but the
reported design and all economics use **120 t/yr**.

## 8.9.4 Mode-exclusive dispatch & grid balance

The cogeneration extraction (stage-14 HP bleed, 1.0 MPa / 180 °C) is routed **by mode — to TCES
(winter / district-heat) OR to the SOE feed (summer / H₂) — never stacked.** Grid export: full
**40 MWe** at peak; **≈ 35.6 MWe** while TCES is charging (~4.9 MWe charge penalty at the zeolite
store); **≈ 27.6 MWe** in the night valley if the SOE (8 MWe) also runs — a demand-valley condition
only.

| Season | TCES | SOE / H₂ |
|---|---|---|
| Winter (Dec–Feb) | discharge → DH 25 MWth | reduced (night only) |
| Shoulder (Oct–Nov, Mar–Apr) | partial discharge / top-up charge | night runs |
| Summer (May–Sep) | charge (or idle) | maximum H₂ (up to ~120 t/yr) |

## 8.9.5 Consistency with §8.12 (economics)

Frozen inputs propagate to §8.12: H₂ **120 t/yr × $5/kg = $0.60 M rev** (≈ $0.42 M margin); district
heat 63.6 GWh-th/yr ≈ **$2.5 M**; electricity 40 MWe baseload ≈ $22.4 M; **cogeneration uplift ≈
+$2.9 M/yr (≈ +13 %)** over electricity-only. Update any §8.12 table still showing 441 t/yr H₂ or a
+$4.1 M / +18 % uplift.

## Digital appendix

- `7_energy_cycle/` — `thermo_cycle.py`, `soe_h2_schedule.py`, `tces_dh_balance.py` (the zeolite/ammine
  store sizing) + `cycle_state_points.csv`.
- `9_tces_model/` — the validated `tces` ammine-alternative model (sample input `smr-40mwe-pwr.edn`,
  SMR-concept explanation, source snapshot, Yan-2020 validation). *(Note: this model covers the
  ammine alternative; the frozen zeolite reference is sized by `tces_dh_balance.py`.)*
