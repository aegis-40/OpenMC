# Aegis-40 — F3 (SBLOCA) & F6 (containment) substantiation

*Substantiation of the SBLOCA and containment positions: plant-specific screening + reference support.*
*Created 2026-06-27; revised 2026-07-06 — containment baseline changed to the low-pressure
pressure-suppression containment with internal IRWST (team FER decision); the immersed-CNV
option is retained in the FER only as a non-baseline future option (FER Appendix B-2).*

> **Method & honesty rule.** For a detailed-design competition entry (not a license application),
> F3 and F6 are substantiated by a **graded approach**: plant-specific screening calculations where
> the team's toolchain reaches (energy balances, DNBR/PCT, grace periods), and
> **demonstration-by-reference** to published integral-PWR precedents for phenomena that need
> containment-transient or system codes the team does not operate. Every by-reference claim below is
> explicitly labelled so, consistent with FER §8.5.4 and Appendix B.

**Containment baseline:** compact **low-pressure pressure-suppression containment**
(design pressure **0.414 MPa**, inner diameter 15 m) with an **internal IRWST pool (250 m³)**
serving as suppression pool, gravity-injection source and PRHR/passive-containment-cooling heat
sink — CAREM-25 / SMART100-CPRSS architectural class. The IRWST is the same 250 m³ design input
credited in F5 (`tools/f5_prhr.py`); F6 screening below uses `tools/f6_suppression.py`.

---

## F3 — Small-break LOCA (SBLOCA)

**Acceptance criteria (10 CFR 50.46):** PCT ≤ 1204 °C (2200 °F); local cladding oxidation ≤ 17 %;
core-wide hydrogen ≤ 1 %; coolable geometry maintained; long-term cooling established.

**Argument:**

1. **Large-break LOCA is practically eliminated (design feature, not analysis).** Aegis is an integral
   PWR — core, pressurizer and steam generator are all inside the RPV, with **no large-bore primary
   piping**. No pipe rupture can produce a large-break LOCA. Only **small lines** penetrating the vessel
   (CVCS, injection, instrument) remain → only SBLOCA is in the design basis.
   (Consistent with FER §8.6.1 practical-elimination argument.)

2. **No drain path below the core (design feature, per CAD).** All CRDM drives are internal
   (ICRDM, top-mounted) and all vessel nozzles are side-mounted above the core region; the bottom
   head has **no penetrations** (reactor-vessel general-arrangement CAD, 2026-07-06). A small-break
   cannot drain the vessel below the top of the core; the integral geometry keeps the core covered
   during depressurization.

3. **Mitigation = staged depressurization + IRWST gravity injection (AP1000/CAREM-class).** On
   low pressurizer pressure/level, the reactor trips and the automatic depressurization stages open,
   discharging through spargers into the IRWST suppression pool. Once the RCS approaches containment
   pressure, **gravity injection from the IRWST** maintains inventory; PRHR/DHRS rejects decay heat
   to the same pool. Head check (`f6_suppression.py`, Q4): with the IRWST level ≥ 8 m above the
   injection nozzle, injection starts at RCS ≤ **≈0.20 MPa abs** → the ADS must depressurize to
   near-containment pressure (staged, AP1000/CAREM-class). *The ≥ 8 m level is a reactor-building
   layout requirement to be confirmed in CAD.* No operator action, no AC power, no pumped injection.

4. **Decay-heat source is low and long-term cooling is demonstrated.** 125 MWth with peak linear
   power **12.8 kW/m ≪ ~43 kW/m** PWR practice → low stored energy and slow clad heat-up. With the
   core covered (items 2–3), the long-term sink is the IRWST: ≥ 240 h at ×1.15 decay-heat
   uncertainty for the 250 m³ pool (F5 result, plant-specific).

**Conclusion.** LBLOCA is practically eliminated by the integral geometry; the remaining SBLOCA is
mitigated passively (ADS + IRWST gravity injection + suppression condensation) with the core covered
by design (no sub-core drain path) and a demonstrated ≥ 240 h passive heat sink. With the core
covered and stored energy low, PCT, oxidation and hydrogen stay far below the 10 CFR 50.46 limits.

**Label:** plant-specific screening (head check, grace period, stored-energy argument) + by-reference
for blowdown phenomenology (integral-PWR SBLOCA precedents, FER Appendix B-1). **Refinement
(licensing stage):** plant-specific SBLOCA blowdown/reflood run in a qualified system code
(RELAP5-3D / TRACE) — out of the present T-H scope.

---

## F6 — Containment pressure / temperature response

**Acceptance criterion:** peak containment pressure ≤ design pressure **0.414 MPa**.

> **DESIGN DECISION (team FER, 2026-07-06): low-pressure pressure-suppression containment with
> internal IRWST**, replacing the earlier immersed-CNV working assumption. The governing limit is
> the 0.414 MPa design pressure; pressure control is by direct-contact condensation of the released
> steam in the IRWST suppression pool.

**Screening result (`tools/f6_suppression.py`, conservative inputs: entire 26 t primary inventory
released at hot-leg enthalpy 1390 kJ/kg; no structure/PRHR credit during pool heat-up; decay heat
ANS-5.1 ×1.15):**

| Check | Result | Verdict |
|---|---|---|
| Blowdown energy into the 250 m³ IRWST | 31.8 GJ → pool 40 → 67.5 °C | pool absorbs full inventory, ΔT +27.5 K |
| Quasi-static containment P after blowdown (heated air + steam at pool T) | **0.139 MPa** | **PASS ≤ 0.414 MPa, margin ×3.0** |
| Pool heat-up by decay heat, zero heat-removal credit | design P reached only at pool 131 °C ⇒ **t ≈ 16.5 h** | ample time; PRHR + passive containment cooling then carry decay heat per F5 (≥ 240 h) |
| Counterfactual without the suppression pool (flash of inventory into 2 000 m³ free volume) | ≈ 0.98 MPa (×2.4 over) | suppression pool is **required** — the architecture is load-bearing, not decorative |
| IRWST gravity-injection head | 8 m → 78.5 kPa ⇒ ADS end-state ≤ ≈0.20 MPa abs | sets the staged-ADS design requirement |

**By-reference support for the phenomena the screening does not resolve** (short-term vent-clearing
dynamics, direct-contact condensation efficiency, fission-product scrubbing): SMART100 CPRSS concept
and SISTA1/SISTA2 test programme; CAREM-25 pressure-suppression containment (closest architectural
analogue: integral natural-circulation PWR + compact suppression containment); NEA/CSNI
pressure-suppression state-of-the-art report; NUREG-0800 SRP 6.5.5 (suppression-pool review
criteria); AP1000 DCD (accepted IRWST safety functions). See FER Appendix B-1.

**Conclusion.** At FER screening level the suppression/IRWST architecture holds containment pressure
≤ 0.414 MPa through the bounding full-inventory blowdown (margin ×3) and through ≥ 16 h of decay
heat with zero heat-removal credit; long-term heat removal is the demonstrated F5 path. The pressure
peak during vent clearing is a dynamic phenomenon covered by reference precedent and carried as a
detailed-design analysis item.

**Label:** plant-specific screening (mass-energy balance) + bounding-by-reference (suppression
phenomenology). **Refinement:** plant-specific containment mass-energy transient
(GOTHIC / CONTAIN-class) including non-condensables, pool stratification, vent/submergence geometry
and DF/scrubbing — carried in FER Appendix B as detailed-design scope.

### Suppression-containment design parameters (inputs to confirm)
| Parameter | Basis / value | Status |
|---|---|---|
| Configuration | Low-pressure suppression containment, internal IRWST 250 m³ | fixed (team FER) |
| Design pressure | 0.414 MPa | fixed (FER §8.5.2); screening peak 0.139 MPa quasi-static |
| Free (gas) volume | ~2 000 m³ assumed (D = 15 m layout) | ⏳ confirm from reactor-building layout; sensitivity 1 500–2 500 m³ → no-pool flash 1.22–0.82 MPa, pooled case insensitive |
| IRWST level above injection nozzle | ≥ 8 m (head for gravity injection) | ⏳ CAD/layout requirement |
| ADS | staged, end-state ≤ ≈0.20 MPa abs | ⏳ valve count/stages = mechanical/I&C design |
| Vent/sparger submergence, DF | by reference (SRP 6.5.5, NEA SOAR) | ⏳ detailed design |
| Hydrogen management | passive autocatalytic recombiners (PARs) in the containment atmosphere | ⏳ detailed design — required for a low-pressure air-filled containment (RG 1.7 / SSG-53) |

---

## Citations

- **10 CFR 50.46** — ECCS acceptance criteria (PCT 1204 °C, oxidation 17 %, H₂ 1 %, coolable geometry,
  long-term cooling); **RG 1.157** — best-estimate ECCS evaluation.
- **10 CFR 50 App. A GDC 16, 38, 50** — containment & containment heat removal; **RG 1.7** — combustible-gas control.
- **NUREG-0800 SRP 6.5.5** — pressure-suppression pool as a fission-product cleanup system;
  **NEA/CSNI** pressure-suppression state-of-the-art report.
- **SMART100** CPRSS passive containment studies and **SISTA1/SISTA2** separate-effect/integral test
  programme (direct-contact condensation in IRWST-class inventories).
- **CAREM-25** (IAEA / Delmastro et al.) — integral natural-circulation PWR with pressure-suppression
  containment; closest architectural analogue.
- **AP1000 DCD** (NRC) — accepted IRWST functions: gravity injection, recirculation, long-duration
  heat absorption.
- **IAEA SSR-2/1** (Req. 56), **SSG-2** (deterministic safety analysis), **SSG-53** (design of the
  reactor containment).

*Screening numbers are from `tools/f6_suppression.py` (this repo); phenomenological claims are
bounding / by-reference as labelled, to be presented as such in the FER.*
