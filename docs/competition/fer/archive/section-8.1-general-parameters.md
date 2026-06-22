# FER §8.1 General Plant Design Parameters — Aegis-40 iPWR

> **Drafting status (2026-06-08).** This is the consolidated "front-page" parameter set for the
> Aegis-40 iPWR. Every neutronic / fuel value is the **LOCKED rev_3** number from
> `design-basis-locked.md`; thermal-hydraulic values are either locked assumptions or computed from
> them (formula shown). Rows that belong to another owner's section, or that still need an analysis,
> are collected in §8.1.9 "Parameters requiring confirmation." Design-process documentation,
> codes/standards, and the regulatory-requirements list are in §8.1.6–§8.1.8.
>
> **Source-of-truth note.** An earlier reference parameter sheet (240 FA, Zircaloy-2 clad, 7.17 MPa SG,
> 1.82 Mkg coolant, 1827 kg/s, ~50 GWd burnup) was a borrowed large-PWR template and is **superseded**
> by the locked Aegis-40 values below. Do not reintroduce those numbers.

---

## 8.1 General Design Parameters

The Aegis-40 is an integral, soluble-boron-free pressurised-water small modular reactor (iPWR-SMR)
rated **125 MWth / 40 MWe net** (32.0 % net efficiency). All primary equipment — core, steam
generator, pressuriser, and control-rod drives — is contained within a single reactor pressure
vessel. The plant is designed for a 60-year life, a small (~0.5 km) emergency-planning zone enabled
by passive safety, and modular factory construction. Tables 8.1-1 to 8.1-5 give the consolidated
design parameters; their derivation and basis documents are in §8.1.6, and pending items in §8.1.9.

### 8.1.1 Plant and power

**Table 8.1-1 — Plant configuration and power**

| Parameter | Value | Unit |
| --- | --- | --- |
| Plant type | Integral PWR (iPWR), soluble-boron-free | — |
| Thermal power | 125 | MWth |
| Net electrical output | 40 | MWe (net to grid) |
| Net thermal efficiency | 32.0 (nameplate) / 31.8 (computed) | % |
| Design lifetime | 60 | years |
| Capacity factor (design target) | 95 | % |
| Capacity factor (used in waste/fuel-cycle analysis) | 90 | % |
| Available process-heat temperature | Flexible: 100–260 | °C |
| Modular design | Yes | — |
| Construction duration (n-th unit) | < 30 | months (first concrete → criticality) |

‹REVIEW — capacity factor: advertise the 95 % design target (consistent with the outage schedule in
§8.1.5); note in §8.11 that the waste arisings used a conservative 0.90. Reconcile the two so the FER
never shows both as "the" CF without explanation.›

### 8.1.2 Primary system and thermal-hydraulics

**Table 8.1-2 — Primary coolant system**

| Parameter | Value | Unit |
| --- | --- | --- |
| Primary system operating pressure | 12.8 | MPa |
| Core inlet / outlet temperature | 258 / 308 | °C / °C |
| Core temperature rise (ΔT) | 50 | K |
| Average primary mass flow rate | ~483 | kg/s |
| Primary coolant inventory | ~25.6 (≈ 34.6 m³) | t |
| Steam-generator (secondary) operating pressure | 4.5 | MPa |
| Circulation mode | Natural circulation (no primary pumps) | — |

‹REVIEW — primary coolant inventory ~25.6 t is a geometric estimate (`scripts/primary_inventory.py`,
±~25 %): sum of the documented in-vessel primary water regions (core lattice + reflector, lower
plenum/head, riser, SG shell-side, downcomer, upper plenum/head) at ρ ≈ 740 kg/m³. It replaces the
erroneous 1.82 Mkg large-PWR figure; confirm the precise value against the §8.4 T-H model.›

‹RESOLVED — the 12.8 MPa / 258→308 °C (ΔT 50 K) primary boundary is now fixed by the §8.4
natural-circulation analysis (`scripts/natcirc_primary.py`). Saturation at 12.8 MPa is 329.7 °C, so the
308 °C outlet keeps 21.7 °C hot-leg subcooling — single-phase with margin. The §8.9 steam side is
re-coupled to these legs (4.5 MPa / 296 °C, 8.8 °C OTSG pinch).›

### 8.1.3 Fuel and core

**Table 8.1-3 — Fuel and core design**

| Parameter | Value | Unit |
| --- | --- | --- |
| Number of fuel assemblies | 21 | — (17×17 square lattice) |
| Active core height | 200 | cm (+ 30 cm H₂O axial reflector each end) |
| Heavy-metal loading (fresh) | ~5.3 | tHM |
| Specific power | 23.6 | MW/tHM |
| Fuel material | UO₂ | — |
| Fuel enrichment (zoned inner/mid/outer) | 4.95 / 4.70 / 4.40 | wt% ²³⁵U |
| Fuel enrichment (core average / maximum) | 4.54 / 4.95 | wt% |
| Fuel cladding material | Zircaloy-4 (Zr-4) | — |
| Primary burnable absorber | Gd₂O₃, 8 wt% (radially zoned) | — |
| Secondary burnable absorber | Er₂O₃, 0.5 wt% | — |
| Reload scheme | 4-batch | — |
| Cycle length | 479 EFPD (~16) | EFPD (months) |
| Fuel reload interval | ~16 (12–24 capable) | months |
| Discharge burnup | 42.8 | GWd/MTU |
| Primary reactivity control | Control rods + integral burnable absorbers | — |
| Control-rod absorber material | B₄C / Hf (REVIEW) | — |
| Fuel reprocessing | None (once-through) | — |

‹RESOLVED — core-average enrichment = 4.54 wt%, assembly-weighted from the rev_3 loading map
(`cad/core_map.csv`): r0/r1/r2 = 1/8/12 assemblies at 4.95/4.70/4.40 wt% → (1·4.95 + 8·4.70 +
12·4.40)/21 = 4.54. The old "3.81 %" was impossible (below the 4.40 minimum zone) and is dropped.›

‹REVIEW — control-rod absorber material: confirm with §8.5/§8.6 (Azamkhon). B₄C and/or Hf are typical
SBF-core choices; Gd₂O₃ is a *burnable absorber*, not a control-rod material, so the old "B₄C, Hf,
Gd₂O₃" lumping is split here.›

‹REVIEW — fresh heavy-metal loading: ~5.3 tHM is the as-modeled value; the depletion run gives 5.04
tHM at discharge. Confirm the exact fresh value with an OpenMC `--step 0` mass edit.›

### 8.1.4 Safety systems and probabilistic targets

> These rows are owned by §8.5/§8.6/§8.7/§8.10 (Azamkhon). Values reproduced here for the front-page
> summary; **confirm counts and descriptions against those sections before submission.**

**Table 8.1-4 — Engineered safety features and PSA targets**

| System / metric | Value | Note |
| --- | --- | --- |
| Reactor shutdown systems | 3 | Hydraulic scram, electrically-driven control rods, redundant trains |
| Core water injection | 2 | Redundant |
| Residual heat removal | 2 | Two redundant 100 % units |
| Emergency core cooling | 3 | Three redundant **passive** 100 % units |
| Containment isolation | 3 | Three redundant trains |
| Containment cooling | 2 | Two 100 % units |
| Passive containment | 3 | Three passive trains, continuously in service |
| Emergency power supplies | 2 | Facility protection only; not required for reactor safety |
| Containment type | Dry | — |
| Containment design pressure | 4.14 / 60 (REVIEW) | bar / psi |
| Core Damage Frequency (CDF) | < 1×10⁻⁷ (projected) | per reactor-year |
| Large Release Frequency (LRF) | < 1×10⁻⁸ (projected) | per reactor-year |

‹REVIEW — containment design pressure: 4.14 bar (60 psi) is a *large-dry-PWR* value. A compact iPWR
steel containment typically peaks higher; set this from the containment peak-pressure accident
analysis (LOCA / steam-line break × margin). Owner: §8.5/§8.6.›

‹REVIEW — CDF/LRF are projected targets benchmarked to the passive-iPWR class (a full PSA is out of
FER scope). State them as "projected, consistent with passive SMR class," not as PSA results.›

### 8.1.5 Site, construction, and outage schedule

**Table 8.1-5 — Site and operational design**

| Parameter | Value | Unit |
| --- | --- | --- |
| Emergency planning zone (radius) | 0.5 | km |
| Seismic design (SSE) | 0.3 | g (Safe-Shutdown Earthquake) |
| Major outage — refuelling | 15 days every 12 months | — |
| Major outage — turbine / vessel ISI | 30 days every 120 months | — |

**Derived relations (basis "C").** Net efficiency = 40 MWe / 125 MWth = **32.0 %** (nameplate); the
detailed re-coupled heat balance gives 39.7 MWe / **31.8 %** (§8.9), the 0.3 MWe difference being within
the turbine-efficiency assumption. The primary flow follows from the heat-balance identity Q = ṁ·c_p·ΔT
with Q = 125 MWth, ΔT = 308 − 258 = 50 K, and c_p ≈ 5.18 kJ/kg·K at 283 °C / 12.8 MPa → **ṁ ≈ 483 kg/s**
(flow and ΔT are coupled — they cannot be set independently; the natural-circulation loop settles at this
ΔT, `scripts/natcirc_primary.py`). Specific power = 125 MWth / 5.3 tHM = **23.6 MW/tHM**. The 95 % capacity-factor
target is consistent with the outage schedule: 15 d/12 mo (4.1 %) + 30 d/120 mo (0.8 %) ⇒ planned
availability ≈ 95 %.

‹REVIEW — EPZ 0.5 km and SSE 0.3 g: the 0.5 km EPZ is a design goal that must be *closed* by the
source-term/dose case (§8.11 + safety); 0.3 g is a generic site-bounding SSE — given Türkiye's
seismicity, check whether the candidate site(s) warrant 0.5 g. Owner: site/safety.›

### 8.1.6 Design phase, methodology, and basis documents

The parameters above are the consolidated output of the **preliminary (conceptual/basic) design
phase** that precedes detailed engineering. Aegis-40 was developed through an integrated,
reproducible analysis chain; each element produced a controlled record that becomes a verified
input to detailed design. This subsection documents that preparatory work so the parameter set can
be traced to its origin, in line with a graded, standards-based design process (IAEA SSG-52 §2;
IAEA GSR Part 4 design-input control).

**Table 8.1-6 — Preliminary-design analyses and basis documents**

| Design domain | Method / tool | Controlled output (basis document) |
|---|---|---|
| Neutronics, depletion, reactivity coefficients | OpenMC Monte-Carlo (ENDF/B-VIII.0), 21-FA 3-D core + depletion | `design-basis-locked.md` (rev_3); OpenMC model + tally outputs (§8.2) |
| Fuel performance (T_centerline, FGR, rod pressure) | Steady-state fuel-rod analysis vs SSG-52 limits | §8.3 fuel-performance tables |
| Primary thermal-hydraulics | Natural-circulation loop balance, IAPWS-IF97 (`scripts/natcirc_primary.py`); DNBR/hot-channel | §8.4 cooling-circuit analysis |
| Secondary power conversion | Regenerative Rankine + exergy model, IAPWS-IF97 (`scripts/thermo_cycle.py`, `thermo_exergy.py`) | §8.9 state points, heat balance, PFD |
| Shielding / dose | Attenuation + flux-to-dose (ICRP-116) | shielding spec + dose profiles |
| Waste / source term | Depletion inventory + ANSI/ANS-5.1 decay heat | §8.11 |
| Geometry / layout | Parametric CAD (RPV, assembly, pin STEP models) | `cad/` STEP files, GA drawings |

Parameters that are not yet design-frozen — because they depend on another owner's detailed
analysis or a confirmatory run — are tracked transparently in §8.1.9.

### 8.1.7 Design codes and standards

All systems, components, and materials are designed to recognised nuclear and conventional
engineering codes. The pressure boundary and safety-related components follow the **ASME Boiler &
Pressure Vessel Code Section III** (nuclear), with balance-of-plant items to **ASME Section VIII /
B31.1** (non-nuclear); materials are PWR-proven grades qualified for the operating envelope (§8.4).

**Table 8.1-7 — Codes and standards applied in the design**

| Design domain | Code / standard | Application in Aegis-40 |
|---|---|---|
| Class-1 nuclear pressure boundary | **ASME BPVC Section III**, Div. 1 (NB / NG) | RPV, OTSG, self-pressurizer, in-vessel CRDM, core support (§8.4) |
| Non-nuclear pressure parts / BOP | **ASME BPVC Section VIII**; **ASME B31.1** | Condenser, feedwater heaters, secondary piping (§8.9) |
| Pressure-boundary & internals materials | SA-508 Gr.3 Cl.1, SA-533B (RPV); **ASTM A240** 304/316L; Inconel-690 TT; Incoloy-800 | Forgings, plate, OTSG tubes, heater sheaths (§8.4) |
| Fuel cladding | Zircaloy-4 (**ASTM B811**) | Fuel-rod cladding (§8.3) |
| Reactor-core nuclear design limits | **IAEA SSG-52**; **NUREG-1431** Rev. 5 | Peaking (F_Q, F_ΔH), reactivity coefficients, SDM (§8.2) |
| Neutronics method & nuclear data | OpenMC (Romano & Forget 2013); ENDF/B-VIII.0; benchmarked to ICSBEP / BEAVRS | Core physics (§8.2) |
| Decay heat | **ANSI/ANS-5.1** | DHRS sizing, post-shutdown source term (§8.4, §8.11) |
| Water/steam thermodynamic properties | **IAPWS-IF97** | Primary & secondary T-H (§8.4, §8.9) |
| Radiation shielding / dose conversion | **ANSI/ANS-6.4**; **ICRP-116** flux-to-dose | Shield design, dose profiles (§8.2.6) |
| Spent-fuel storage criticality | **NUREG-0800** §9.1.1; **10 CFR 50.68** (k_eff(95/95) ≤ 0.95) | Wet/dry storage (§8.11) |
| Instrumentation & safety systems | **IEEE Std 603-2018**; **IAEA SSG-39** | Protection system, I&C (§8.7) |
| Predisposal waste management | **IAEA GSR Part 5** | Secondary-waste handling (§8.11) |

### 8.1.8 Reference regulatory and nuclear-safety requirements

Nuclear safety is integrated into the design from the outset through a standard, defence-in-depth
approach: the four fundamental safety functions (control of reactivity, fuel cooling, confinement
of radioactivity, and radiation protection) are each met by inherent characteristics and
independent, redundant provisions. The candidate site being in Türkiye, the licensing basis is the
**Nuclear Regulation Authority (NDK)** framework, whose design regulations adopt the **IAEA Safety
Standards**; the table below lists the reference safety-requirement documents and where each is
addressed in this FER.

**Table 8.1-8 — Reference regulatory documents (nuclear-safety requirements)**

| Document | Scope | How addressed in the Aegis-40 design |
|---|---|---|
| **IAEA SSR-2/1 (Rev. 1)** — *Safety of NPPs: Design* | Top-level design safety requirements; defence-in-depth | Req. 24–25 redundant/independent reactivity control (rods + EBIS diverse shutdown); Req. 35 reactivity-feedback design; Req. 45 inherent stability (all coefficients < 0); Req. 46 ≥ 2 diverse shutdown systems (§8.2) |
| **IAEA SSG-52** — *Design of the Reactor Core for NPPs* | Core design limits and methods | Peaking, DNBR, reactivity coefficients, LHGR margins (§8.2) |
| **IAEA GSR Part 4 (Rev. 1)** — *Safety Assessment for Facilities and Activities* | Safety-assessment methodology | Deterministic analysis + projected-PSA framing (§8.5/§8.6) |
| **IAEA SSG-3 / SSG-4** — Level-1 / Level-2 PSA | PSA methodology | CDF / LRF class targets (§8.6) |
| **IAEA GSR Part 5** — *Predisposal Management of Radioactive Waste* | Waste-safety requirements | On-site storage & conditioning (§8.11) |
| **US NRC 10 CFR 50 App. A** — General Design Criteria | Generic design criteria | GDC 11 (reactivity feedback), 26/27 (reactivity control), 35 (ECCS) (§8.2, §8.5) |
| **US NRC NUREG-1431 Rev. 5** — Standard Technical Specifications | Requirement forms / LCOs | SDM, MTC, F_Q, F_ΔH limits (§8.2) |
| **US NRC NUREG-0800 / 10 CFR 50.68** | Standard Review Plan; SFP criticality | k_eff(95/95) ≤ 0.95 (§8.11) |
| **Türkiye NDK — Nuclear Regulation Law No. 7381 (2022)** + NDK design regulation | National licensing basis | Primary regulatory framework; adopts the IAEA Safety Standards above |

### 8.1.9 Parameters requiring confirmation or pending analysis

The following are not yet design-frozen and are tracked for the review buffer:

1. ~~Primary coolant inventory~~ — **CLOSED:** ~25.6 t estimated (`scripts/primary_inventory.py`);
   confirm precise value against the §8.4 T-H model. *(Samira → Adilbek)*
2. ~~Core-average enrichment~~ — **CLOSED:** 4.54 wt% (assembly-weighted, `cad/core_map.csv`).
   *(Samira)*
3. **Fresh heavy-metal loading** — confirm exact value via OpenMC `--step 0` (§8.1.3). *(Samira)*
4. **Primary pressure & core ΔT** — lock against the §8.4 steady-state T-H model. *(Adilbek)*
5. **Control-rod absorber material** — confirm B₄C / Hf selection. *(Azamkhon, §8.5/§8.6)*
6. **Containment design pressure** — set from containment accident analysis. *(Azamkhon, §8.5/§8.6)*
7. **Safety-system counts / descriptions** — confirm Table 8.1-4 against §8.5–§8.7, §8.10.
   *(Azamkhon)*
8. **CDF / LRF** — confirm framing as projected class targets, not computed PSA. *(safety)*
9. **EPZ / SSE** — close EPZ with the dose case; confirm SSE against candidate-site seismicity.
   *(site / safety)*
10. **Capacity factor** — reconcile the 95 % design target with the 0.90 used in §8.11. *(Samira)*
