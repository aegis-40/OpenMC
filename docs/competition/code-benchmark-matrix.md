# Code & benchmark matrix — what needs V&V across §8.1–§8.12

**Purpose:** map every FER technical section to the code/method it uses and the
*citable* IAEA / OECD-NEA benchmark that validates it, so the Digital-Appendix
V&V package (a graded, mandatory gate) can lean on **published** validation of
our open-source tools instead of re-deriving it.

## Strategy — cite vs run

The Digital-Appendix gate asks for two distinct things:

1. **One sample input file per code** — this you must actually run (your real
   design deck is the sample input; it proves you can drive the tool). Not skippable.
2. **V&V evidence (repeatability + benchmarking + reproducibility) vs IAEA/OECD-NEA
   data** — for *popular open-source codes this is mostly citation*: reference the
   code developers' published validation against the standard benchmark suites,
   plus **one** cheap confirmatory case you run to show correct usage.

So per code: **cite the published V&V suite + include your design deck as the
sample input + (optionally) one lightweight confirmatory benchmark run.**

Legend — **Cite** = reference published V&V; **Run** = we execute a case; the
"Benchmark family" names are searchable (OECD-NEA / IAEA / code docs).

---

## Neutronics — OpenMC  (§8.2, §8.3 depletion, §8.11)

| Capability | Citable benchmark family (searchable) | Action |
|---|---|---|
| Code verification (transport) | Romano & Forget, *Ann. Nucl. Energy* 51 (2013) 274 — the OpenMC code paper | **Cite** |
| Criticality / k_eff accuracy | **ICSBEP** — *International Handbook of Evaluated Criticality Safety Benchmark Experiments* (OECD-NEA); OpenMC's `openmc-dev/benchmarks` runs it | **Cite** (+ optional 1 case) |
| Reactor-physics lattice/core | **C5G7** (OECD-NEA deterministic transport benchmark); **BEAVRS** (MIT-CRPG full-core PWR); **VERA** core-physics progression (CASL) | **Cite**; run our own assembly as the deck |
| Depletion / isotopics (code-to-code) | Romano et al., *Ann. Nucl. Energy* 152 (2021) 107989 — OpenMC vs Serpent, BEAVRS 2.4% pincell, <1% | **Cite + Run** (`benchmark_depletion_pincell.py`) |
| Spent-fuel isotopics (measured) | **SFCOMPO 2.0** (OECD-NEA assay DB); **OECD-NEA Burnup-Credit Benchmark Phase I-B** | Cite; run if time |
| Storage criticality (burnup credit) | **OECD-NEA Burnup-Credit Benchmark Phase II**; **ANS-8.1** arrays; method per Cabrera (2023) | **Run** (`run_storage_criticality.py`) + cite |

Sample inputs already in repo: `openmc_model/sample_inputs/*.xml` (core deck),
`scripts/run_storage_criticality.py`, `scripts/benchmark_depletion_pincell.py`.
Detailed plan: `digital-appendix-vv-plan.md`.

## Thermal-hydraulics — OpenFOAM *or* subchannel/correlation  (§8.4, §8.5, §8.6)

> NB: tooling decision still open (full CFD vs subchannel rescope — see team plan).
> Pick the row set that matches the final method.

**If OpenFOAM CFD:**

| Capability | Citable benchmark family | Action |
|---|---|---|
| Turbulent rod-bundle mixing | **OECD-NEA / KAERI MATiS-H** rod-bundle CFD benchmark | **Cite** (+ optional case) |
| Thermal mixing / striping | **OECD-NEA Vattenfall T-Junction** CFD benchmark | Cite |
| Natural / buoyant convection | **de Vahl Davis** differentially-heated cavity; Rayleigh-Bénard (classic CFD verification) | **Run** (cheap verification) |
| Solver verification | lid-driven cavity, backward-facing step (OpenFOAM tutorials) | Run |

**If subchannel / correlation (W-3 DNBR, 1D hot-channel):**

| Capability | Citable benchmark family | Action |
|---|---|---|
| Subchannel void / DNB | **OECD-NEA PSBT** (PWR Subchannel & Bundle Tests); **BFBT** (BWR) | **Cite** |
| CHF / DNBR correlation | **W-3** and **EPRI-1 / Columbia** CHF correlations (empirically validated) | Cite |
| Decay heat | **ANS-5.1** decay-heat standard (validation by definition) | **Cite + Run** (we already use it) |

## Fuel & material / fuel performance — §8.3

| Capability | Citable benchmark family | Action |
|---|---|---|
| Fuel-rod thermo-mechanics (FRAPCON-style) | **OECD-NEA IFPE** (Int'l Fuel Performance Experiments DB); **Halden Reactor Project**; **Risø** | **Cite** |
| Code validation | FRAPCON validation report **PNNL / NUREG-CR-7022** | Cite |
| Centreline temp / fission-gas | benchmark vs IFPE rod (e.g. a Halden instrumented rod) | Cite; run if FRAPCON used |

## Safety / accident analysis — §8.5, §8.6

| Capability | Citable benchmark family | Action |
|---|---|---|
| Decay-heat source (post-shutdown) | **ANS-5.1** standard | **Cite** (already in §8.11) |
| System transient / LOCA (if a system code used) | **OECD-NEA** integral-test benchmarks: **LOFT**, **ROSA/LSTF**, **PKL** | Cite |
| PRA / fault & event trees | method per **IAEA SSG-3/-4**, **NUREG-1150**; generic reliability data **IAEA-TECDOC / NUREG** | **Cite** (method, not a physics run) |

## Energy cycle & integrated systems — §8.9

| Capability | Citable benchmark family | Action |
|---|---|---|
| Steam/water properties | **IAPWS-IF97** industrial formulation (the reference standard) | **Cite** |
| Rankine/Brayton cycle, TES/SOE | published cycle data / textbook reference for the chosen config | Cite |

## I&C / digital twin — §8.7

| Capability | Citable reference | Action |
|---|---|---|
| Reactor kinetics / point-kinetics model | standard point-kinetics; IAEA NPP I&C guidance **SSG-39** | Cite (method) |
| Digital-twin / control models | no nuclear benchmark expected — descriptive + control-loop verification | — |

## Sections with no code benchmark (descriptive / design)

| Section | Note |
|---|---|
| §8.1 General plant description | parameters table (design-basis-locked.md); no benchmark |
| §8.8 Auxiliary systems | design/sizing; cite standards (ASME, IAEA) not benchmarks |
| §8.10 Plant layout | drawings/CAD; no benchmark |
| §8.12 Economics | method per **OECD-NEA/IEA "Projected Costs of Generating Electricity"**, **IAEA G4ECONS / NEST**; LCOE methodology cite, not a benchmark |

---

## Bottom line — minimum runs needed (everything else is cited)

The gate's "sample input per code" + a single confirmatory benchmark each means
the **only cases we must actually execute** are:

1. **OpenMC** — our core deck (have it) **+** the depletion pincell benchmark
   (`benchmark_depletion_pincell.py`, cheap) and the storage-criticality case.
2. **OpenFOAM / T-H code** — our design case **+** one cheap verification
   (cavity natural-convection, *or* PSBT subchannel point) — depends on the
   final T-H tooling decision. **Owner: [TH].**
3. **Fuel-performance code** (if used) — one IFPE/Halden rod. **Owner: [NEU/TH].**

Everything else (ICSBEP, C5G7, BEAVRS, MATiS-H, IFPE, ANS-5.1, IAPWS-IF97, PRA
methodology, economics methodology) is **cited published validation**, not work
we reproduce. That is standard and accepted practice for established open-source
codes.
