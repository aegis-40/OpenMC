# Aegis-40 — F3 (SBLOCA) & F6 (containment) bounding substantiation

*Substantiation of the SBLOCA and containment positions by bounding-by-reference (cite/bound strategy).*
*Created 2026-06-27.*

> **Method & honesty rule.** For a detailed-design competition entry (not a license application),
> F3 and F6 are substantiated by **demonstration-by-reference to the NRC-licensed envelope** rather than
> by de-novo system/containment-code runs the team does not operate. Aegis-40's primary system is, by
> construction, the **NuScale Power Module** (integral RPV, 37 FA / 9 768 pins / 2.0 m active, SBF,
> natural circulation, helical SG, internal CRDM, pool-immersed steel containment). Every claim below is
> explicitly **bounding / by-similarity**, not a plant-specific calculation, and must be labelled so in
> the FER. Key Aegis-vs-reference metric: **Aegis 125 MWth = 0.78 × the NuScale NPM-160 (160 MWth)
> module**, same core geometry → decay-heat source and accident energy are **bounded below** the licensed
> reference at equal-or-better passive-heat-sink margin.

---

## F3 — Small-break LOCA (SBLOCA)

**Acceptance criteria (10 CFR 50.46):** PCT ≤ 1204 °C (2200 °F); local cladding oxidation ≤ 17 %;
core-wide hydrogen ≤ 1 %; coolable geometry maintained; long-term cooling established.

**Bounding argument:**

1. **Large-break LOCA is practically eliminated (design feature, not analysis).** Aegis is an integral
   PWR — core, pressurizer and steam generator are all inside the RPV, with **no large-bore primary
   piping**. No pipe rupture can produce a large-break LOCA. Only **small lines** penetrating the vessel
   (CVCS, injection, instrument) and the ECCS valves remain → only SBLOCA is in the design basis.
   (Consistent with FER §8.6.1 / B1 practical-elimination argument.)

2. **Mitigation is the NRC-reviewed NuScale passive ECCS, adopted unchanged.** On a low-pressure ECCS
   actuation, **3 reactor vent valves (RVVs)** and **2 reactor recirculation valves (RRVs)** open: core
   steam vents through the RVVs into the containment, **condenses on the pool-cooled inner wall of the
   steel containment vessel (CNV)**, and returns through the RRVs to the downcomer — a closed
   natural-circulation recirculation loop **inside the vessel/containment that keeps the core covered**.
   No operator action, no AC power, no pumped injection required.

3. **Aegis is bounded by NuScale on the decay-heat source.** 125 MWth = **0.78 ×** the NPM-160 module;
   identical 37-FA core. Lower per-module power → lower decay heat for the **same** ultimate heat sink
   (the reactor pool). Long-term core cooling is the same passive pool credited in **F5** (≥ 286 h to pool
   boil-off, and unlimited with make-up / by NuScale's "indefinite" pool result).

4. **Low linear power → inherently low LOCA PCT.** Aegis peak linear power **12.8 kW/m ≪ ~43 kW/m** PWR
   limit → low stored energy and low clad heat-up rate. With the core kept covered (item 2), the cladding
   excursion is small.

**Conclusion.** Aegis-40 SBLOCA peak cladding temperature, oxidation and hydrogen generation are
**bounded well below the 10 CFR 50.46 limits** by the NuScale NPM design-basis LOCA, by similarity (same
integral configuration and ECCS, 0.78 × module power). Large-break LOCA is practically eliminated by the
integral geometry. NuScale's licensed result is that ECCS heat removal "maintains containment and core at
acceptably low levels **for an unlimited period**" with **no core uncovery**.

**Label:** bounding / demonstration-by-reference. **Refinement (licensing stage):** a plant-specific
SBLOCA blowdown/reflood run in a qualified system code (RELAP5-3D / TRACE) — out of the present T-H scope.

---

## F6 — Containment pressure / temperature response

**Acceptance criterion:** peak containment pressure ≤ containment design pressure.

> **DESIGN DECISION: immersed high-pressure steel CNV** (NuScale-style), **not** a
> conventional dry containment. Consequence: the plan's ≤ 0.414 MPa (≈ 60 psia) large-dry figure **does
> not apply**; the governing limit is the **CNV design pressure** (a high-pressure vessel), and peak
> pressure is condensation-limited (below). All F6 conditional "provided C5…" language is now firm.

**Bounding argument:**

1. **Selected configuration (C5) = NuScale-style immersed CNV.** A compact **high-pressure steel
   containment vessel immersed in the reactor pool**, operated near vacuum at power. This is the natural fit
   for Aegis: the integral RPV and the pool are already in the design (the pool is the F5 heat sink). The
   vacuum/low-conductivity gap at power also cuts normal-operation heat loss and suppresses combustible-gas
   accumulation (RG 1.7), and the immersion makes the pool the single passive sink for F5 and F6 alike.

2. **Peak pressure is condensation-limited.** A LOCA/MSLB mass-energy release into the CNV raises P and T;
   steam then **condenses on the pool-cooled inner CNV wall**, so pressure peaks and **declines** as heat
   is conducted/convected to the pool. NuScale's licensed result: CNV heat removal "**rapidly reduces
   containment pressure and temperature and maintains them at acceptably low levels for an unlimited
   period**."

3. **Bounded by NuScale on the source term.** Aegis primary inventory and stored/decay energy ≤ the
   NPM-160 module (0.78 × power, comparable inventory) → peak CNV P/T are **bounded by the NuScale licensed
   CNV response**, which stays within the CNV design pressure with margin.

4. **The pool is the ultimate heat sink** (same one credited in F5) → passive, unlimited containment heat
   removal; no containment spray, fan coolers or AC power credited.

**Conclusion.** With the immersed-CNV configuration selected (C5), Aegis-40 peak containment pressure and
temperature are **bounded by the NuScale NPM CNV response** — condensation-limited, within CNV design
pressure, unlimited-duration passive heat removal.

**Label:** bounding / by-reference. **Refinement:** a plant-specific mass-energy release + containment
response calculation (GOTHIC / CONTAIN-class) — out of scope.

**Containment type: immersed high-pressure steel CNV** (inherits the NuScale
bounding directly). The dry/passive-containment alternative (which would have re-anchored F6 on the AP1000
PCS envelope and the ≤ 0.414 MPa-class limit) is **not** adopted.

### CNV design parameters (mechanical-design inputs to confirm)
| Parameter | Basis / value | Status |
|---|---|---|
| Configuration | High-pressure steel CNV, fully pool-immersed, near-vacuum at power | fixed (C5) |
| Design pressure | Set by the bounding peak-LOCA CNV pressure (condensation-limited); anchor to NuScale CNV class (high-pressure steel vessel, ≫ 0.414 MPa) | ⏳ mechanical design to set the number; T-H gives the source-term bound only |
| Ultimate heat sink | Reactor pool (the F5 sink: ≥ 286 h to boil-off, vented/boiling, ~100–250 m³) | fixed (= F5) |
| Heat-removal mode | Steam condensation on the pool-cooled inner CNV wall; no spray / fan / AC | fixed |
| Heat-transfer area | CNV wetted shell; size to the bounding condensation duty (≤ NuScale per 0.78× power) | ⏳ mechanical/thermal sizing |

The two ⏳ items are **mechanical/structural design** (vessel wall, design pressure, shell area), not T-H
solver work; the T-H scope supplies only the bounding source term (0.78 × NuScale module, F5 pool sink).

---

## Citations

- **10 CFR 50.46** — ECCS acceptance criteria (PCT 1204 °C, oxidation 17 %, H₂ 1 %, coolable geometry,
  long-term cooling); **RG 1.157** — best-estimate ECCS evaluation.
- **10 CFR 50 App. A GDC 16, 38, 50** — containment & containment heat removal; **RG 1.7** — combustible-gas control.
- **NuScale FSAR/DCA Ch. 6** (containment functional design), **Ch. 15** (transient & accident analysis),
  including the RVV/RRV ECCS; NRC ADAMS **ML111010170** (NuScale preliminary LOCA), **ML103470495** (technology overview).
- Ingersoll / NuScale, "Unique safety features and licensing requirements of the NuScale SMR," *Front. Energy Res.* (2023):
  https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1160150/full
- **IAEA SSG-2** (deterministic safety analysis), **SSG-53** (design of the reactor containment).

*All F3/F6 claims are bounding / by-similarity to the NuScale NPM, not Aegis-specific code calculations,
and are to be presented as such in the FER.*
