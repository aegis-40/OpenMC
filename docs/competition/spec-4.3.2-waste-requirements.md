# §4.3.2 Nuclear Fuel & Waste Management — requirements → §8.11 deliverables

Source: *2026 Nuclear Energy Technologies Design Competition Specification* (pp. 21-24, 43-44).
This is the authoritative extract for the FER **§8.11 Waste Management** section.
Owners: **Elbek [LAY]** (engineered systems, facility, regulatory prose) + **Samira [NEU]** (source term, criticality, the physics calcs).

---

## What the spec literally requires

**Scope (p.22 §4.3.2):** innovative, applicable solutions that minimize waste and
environmental impact across the *whole* fuel cycle — front-end (fuel + burnup
optimization) through back-end (spent-fuel management + disposal). Back-end
methods/systems are to be **designed from the reactor burnup analysis results**
(i.e. driven by our OpenMC depletion output).

**Design criteria called out (p.23-24):**
- **Fuel Efficiency** — more energy per unit fuel, longer interval between refuelings,
  minimize fissile material *and* waste in spent fuel, optimize fuel thermal conductivity.
- **Sustainability** — longer-cycle and *reprocessable* fuels; efficient use of resources.
- **Cost-effectiveness, Flexibility/Adaptability** (note applicability to other reactor types).
- **Waste Management** — reduce **quantity AND radioactivity** of waste; **explain
  disposal processes in detail**; **regulatory-compliance assessment**.

**Three safety analyses EXPLICITLY mandated for waste (p.24, the key new items):**
1. **Criticality-accident prevention during spent-fuel storage** → subcriticality (k_eff)
   of the storage racks / cask, with burnup credit. *(OpenMC — Samira)*
2. **Safe dissipation of radioactive decay heat** → decay-heat removal in pool/cask. *(thermal)*
3. **Geological & environmental impacts** → e.g. temperature rise at the disposal site;
   plus compliance of results with regulations.

**Award-ranking minimum criteria for Waste Management (p.43):**
- Comply with SMR/MMR limits + fuel-cycle requirements + international standards.
- Fuel efficiency vs. **a reference reactor of the team's choice** (tables/figures/drawings;
  spec p.~17 line 626: the team specifies the reference reactor).
- Fuel safety: integrity/durability, fission-product retention, deformation limits.
- **List the fission products**; minimize waste quantity & radioactivity; **fully describe
  the disposal method/system** and present its **environmental impacts**.
- **Digital Appendix (hard gate):** one sample input file per code + explanation of the
  case/approach/outputs + **repeatability, benchmarking, reproducibility** results.

---

## Deliverables map (each row = one figure/table/calc in §8.11)

| # | Deliverable | Source / tool | Owner |
|---|---|---|---|
| 1 | Innovative-fuel-cycle waste-reduction narrative (high burnup, SBF, Gd+Er, long cycle) | design rationale | NEU |
| 2 | Spent-fuel arisings: tHM & assemblies per cycle and per year; **tHM (or m³ HLW) per TWh** vs. reference | LRM + depletion | NEU |
| 3 | **Fission-product list** + discharge actinide/FP inventory (kg, Bq) | OpenMC depletion `Results` | NEU |
| 4 | **Decay-heat vs. cooling time** (1 d → 10⁶ yr) | decay-only depletion (power=0) | NEU |
| 5 | **Activity & radiotoxicity vs. cooling time** (Bq, Sv) — the "reduced radioactivity" proof | inventory × ICRP-72 | NEU |
| 6 | **Spent-fuel storage criticality** (k_eff of rack/cask, burnup credit, < limit) | OpenMC | NEU |
| 7 | Gamma/neutron source spectra for shielding | OpenMC from depleted mat. | NEU→LAY |
| 8 | Back-end strategy: pool → dry-cask ISFSI → geological disposal (once-through + optionality) | design | LAY |
| 9 | Pool/cask **decay-heat-removal** sizing & passive cooling | thermal (uses #4) | LAY |
| 10 | Disposal-site thermal/geological-environmental impact (temp rise) | analysis (uses #4) | LAY |
| 11 | **Waste classification** LLW/ILW/HLW vs. IAEA GSG-1 thresholds | uses #3-#5 | NEU+LAY |
| 12 | **Secondary-waste** plan: source-minimization (SBF eliminates boron streams) + segregation matrix | design | LAY |
| 13 | **Regulatory-compliance** assessment (IAEA SSR-5/GSG-1; Turkish NDK regs) | review | LAY |
| 14 | Digital-Appendix V&V: sample input + benchmark per code | see below | NEU |

---

## V&V / benchmarking plan (Digital Appendix gate)

Benchmarking proves the **code is used correctly** — it does NOT require a reactor
identical to ours. Plan:
- **Depletion / spent-fuel isotopics:** benchmark an OpenMC pin/assembly depletion
  against a published reference where the answer is known —
  **OECD/NEA Burnup-Credit Criticality Benchmark Phase I-B** (PWR pin cell, depleted
  ~30-40 GWd/t, tabulated nuclide concentrations from many codes) and/or a
  **SFCOMPO 2.0** measured PWR assay sample at similar enrichment/burnup. Compare
  U/Pu + key FP concentrations → table in appendix. Cheap (pin-cell), recognized source.
- **Storage criticality:** OpenMC k_eff against a standard fresh/spent-fuel storage-rack
  criticality benchmark (e.g. an OECD/NEA or ANS-8 array benchmark).

## Reference reactor (team's choice) — recommend **CAREM-25**
Closest real analog to Aegis-40: integral PWR, ~27-29 MWe / ~100 MWth (we are 40/125),
and **boron-free during normal operation** (control rods + Gd burnable poison) — i.e. a
real SBF small iPWR. Excellent for the fuel-efficiency / waste comparison tables.
Secondary references: NuScale (iPWR, public data, but uses soluble boron), ACP100/Linglong One.
