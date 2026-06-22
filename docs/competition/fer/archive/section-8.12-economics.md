# §8.12 Economics

> **Status:** first draft (NEU/[3S]). Inputs are first-of-a-kind (FOAK) SMR Tier-B
> values from the open literature, scaled to the 40 MWe unit — **⚠CONFIRM** before
> the final FER. All figures computed by `scripts/economics_lcoe.py`
> (→ `economics/lcoe_breakdown.csv`) and the fuel-cycle module
> `src/aegis40/back_end/fuel_cycle.py`. Methodology follows OECD-NEA (1994) and the
> levelised-cost treatment of Ashley et al. (2014, *Ann. Nucl. Energy* 69, 314).

This section levelises the lifetime cost of the Aegis-40 plant into a single
**levelised cost of electricity (LCOE)** and shows the **levelised fuel-cycle cost
(LFCC)** that feeds it. The intent is a transparent, reproducible cost model — not a
bankable estimate — that locates the dominant cost drivers for a 40 MWe iPWR.

## 8.12.1 Methodology

The LCOE is the constant electricity price that, discounted over the plant life, just
recovers all discounted costs (OECD-NEA 1994). With a real discount rate *r* and an
economic life *N*, costs are annualised through the **capital recovery factor**:

```
CRF = r(1+r)^N / [(1+r)^N − 1]
LCOE = [ OCC·IDC·CRF + FixedO&M ] / (8760·CF) + VarO&M + Fuel + Decommissioning   [$/MWh]
```

where *OCC* is the overnight capital cost ($/kWe), *IDC* the interest-during-construction
multiplier, *CF* the capacity factor, and the fuel term is the LFCC of §8.12.3. The
**LFCC** itself follows the same discounted-cash-flow form (Ashley et al. 2014, Eq. 3):

```
LFCC = Σ_i Σ_t [ F_i(t) / (1+r)^(t−t0) ]  /  Σ_t [ E(t) / (1+r)^(t−t0) ]
F_i = x_i · c_i · l_i · (1 + s_i)^(t−t0)
```

summed over front-end and back-end fuel-cycle stages *i* (mining/conversion, enrichment,
fabrication; interim storage, encapsulation, disposal), where *x* is the mass or SWU at
each stage, *c* its unit cost, *l* the process loss factor, and *s* an escalation rate.

## 8.12.2 Inputs (Tier-B, ⚠CONFIRM)

| Parameter | Value |
| --- | --- |
| Net electric capacity | 40 MWe |
| Capacity factor (CF) | 0.90 |
| Economic life (N) | 60 yr |
| Real discount rate (r) | 7 % |
| Construction duration | 4 yr |
| Overnight capital (OCC) | 5 000 / **7 200** / 10 500 $/kWe |
| Fixed O&M | 130 $/kWe·yr |
| Variable O&M | 3 $/MWh |
| Fuel (LFCC) | 7.5 $/MWh |
| Decommissioning fund | 700 $/kWe |

The **small-unit premium** is deliberate: a 40 MWe unit has a higher $/kWe than a
GW-class PWR because fixed engineering, licensing and staffing are spread over less
capacity. The offsetting SMR advantages — factory fabrication, shorter build, lower
absolute capital-at-risk, and the natural-circulation / soluble-boron-free simplification
(fewer pumps, no CVCS boron plant) — are reflected in the shorter construction period and
are discussed qualitatively in §8.12.4.

## 8.12.3 Levelised fuel-cycle cost (LFCC)

The Aegis-40 cycle is **once-through (open)**: no reprocessing, consistent with the
non-proliferation posture of §8.7. The LFCC therefore comprises front-end stages
(natural-U purchase, conversion, enrichment to the §8.2 average, fabrication including the
Gd₂O₃/Er₂O₃ integral burnable absorber) and back-end stages (on-site wet/dry interim
storage per §8.11, encapsulation, geological disposal levy). With the discharge burnup of
**42.8 GWd/tHM** (§8.11) spreading the front-end mass cost over more energy than a
33 GWd/t LWR, the levelised fuel contribution is **≈ 7.5 $/MWh** — a small share of LCOE,
typical of LWR-class once-through cycles. (A stage-by-stage table is produced by
`fuel_cycle.py`; populate once the enrichment/SWU per cycle is locked with §8.2.)

## 8.12.4 LCOE result and sensitivity

**Table 8.12-1 — LCOE breakdown** (`scripts/economics_lcoe.py`):

| CAPEX scenario | OCC ($/kWe) | Capital | Fixed O&M | Var O&M | Fuel | Decom. | **LCOE ($/MWh)** |
|---|---:|---:|---:|---:|---:|---:|---:|
| low | 5 000 | 51.7 | 16.5 | 3.0 | 7.5 | 6.3 | **85.0** |
| **mid** | **7 200** | **74.5** | **16.5** | **3.0** | **7.5** | **6.3** | **107.8** |
| high | 10 500 | 108.6 | 16.5 | 3.0 | 7.5 | 6.3 | **141.9** |

The **mid-case LCOE is ≈ 108 $/MWh**, of which **capital is ~69 %**. Two conclusions
follow directly:

1. **LCOE is capital-dominated.** Fuel (7 %) and O&M (18 %) are secondary; the result is
   driven almost entirely by OCC and the discount rate. The honest uncertainty band
   (85 → 142 $/MWh) is set by the ±FOAK CAPEX spread, not by operating cost.
2. **The design levers that matter are the capital ones** — capacity factor, construction
   schedule and OCC. The SBF / natural-circulation simplification helps here (fewer
   safety-grade pumps and no boron-recovery plant lower both OCC and O&M), and a high CF
   from the long SBF cycle directly dilutes the fixed charges.

This places Aegis-40 in the expected FOAK-SMR range (typically 90–150 $/MWh in the open
literature) — uncompetitive with GW-class nuclear on $/MWh alone, but that is the wrong
comparison: the SMR value proposition (§7 broader impacts) is **dispatchable cogeneration**
(electricity + the §8.9 district-heat / H₂ revenue streams), **grid-independent siting**,
and **low absolute capital-at-risk**, none of which a single-product LCOE captures.

## 8.12.5 Open items (⚠CONFIRM)

1. **OCC anchor** — replace the literature triangular with a bottom-up account once the
   §8.10 layout and major-equipment list are fixed.
2. **LFCC stage table** — populate `fuel_cycle.py` with the per-cycle enrichment/SWU,
   fabrication and disposal-levy unit costs from §8.2/§8.11.
3. **Cogeneration credit** — add the district-heat and H₂ revenue offset (§8.9) as an
   effective-LCOE reduction once those duty factors are set.
4. **Discount-rate sensitivity** — add r = 5 % / 10 % rows for the final FER.

## References (§8.12)

- OECD-NEA, *The Economics of the Nuclear Fuel Cycle*, OECD, Paris (1994).
- S.F. Ashley et al., "Fuel cycle modelling of open cycle thorium-fuelled nuclear energy
  systems," *Ann. Nucl. Energy* **69** (2014) 314–330 — levelised-cost methodology adopted here.
- IAEA, *Approaches to Assess Competitiveness of Small Modular Reactors*, IAEA-TECDOC (2018).
- IEA/NEA, *Projected Costs of Generating Electricity* (2020) — discount-rate and CF conventions.
