# §8.3 — Reactor-Core Material Selection, Fuel Performance & Structural Materials

> **Scope.** Materials of the core (fuel, cladding, coolant/moderator, reflector, burnable
> and control absorbers, structural members), their selection criteria, and their demonstrated
> behaviour under neutron irradiation and over the steady-state / transient / accident temperature
> range. Quantitative inputs reuse the OpenMC neutronics (fluence) and conjugate-CFD thermal results
> already established in §8.2/§8.4 — no new simulation is introduced here; established irradiation and
> fuel-performance correlations are applied to those inputs. Owner: NEU.

## 8.3.1 Material inventory and role

| Material | Composition / grade | ρ (g/cm³) | Role | Code / qualification basis |
|---|---|---|---|---|
| Fuel | UO₂, 4.0–4.95 wt% ²³⁵U (ring-graded) | 10.40 | Fissile/fertile heat source | ASTM C776; LWR fleet-qualified |
| Burnable absorber | Gd₂O₃ (rings 1.65/1.45/0.95/0.68 wt%, core-avg ≈1.0) **+ Er₂O₃** | in-pellet | Hold-down reactivity, boron-free SDM | LWR IFBA/Gd practice |
| Cladding | M5® (Zr-1Nb) — Zircaloy-4 alternate | 6.55 | Fission-product barrier, structural | ASTM B811; NRC-approved |
| Gap | Helium | — | Gap conductance | — |
| Coolant / moderator | Light water (boron-free), 12.8 MPa | 0.72 (hot) | Heat transport + moderation | — |
| Radial reflector | Light water (200 mm) / heavy SS-304 option | 0.72 / 8.0 | Leakage reduction, barrel protection | NuScale concept |
| Control absorber | B₄C (Ag-In-Cd / Hf alternate) | 2.52 | Shutdown / control | ASTM C750 |
| Core barrel / internals | SS-304 | 8.00 | Structure, thermal shield | ASME III NG |
| Reactor pressure vessel | SA-508 Gr.3 low-alloy steel | 7.90 | Pressure boundary | ASME III NB |
| Guide tubes / grids | Zircaloy-4 | 6.55 | CRA channels, fuel-rod support | ASTM B353 |

Pin geometry (from the OpenMC core deck): pellet radius **0.40958 cm**, clad inner **0.41873 cm**,
clad OD ≈ 0.475 cm (17×17 standard), pin pitch **1.2623 cm**, 264 fuel rods + 24 guide + 1 instrument
tube per assembly, active height **2.0 m**.

## 8.3.2 Selection criteria

Each material is selected against six weighted criteria:

1. **Neutronic** — low parasitic absorption (cladding, structure), good moderation (H₂O), tailored
   absorber worth (Gd/Er for boron-free hold-down; B₄C for shutdown).
2. **Thermal** — high conductivity and melting margin (UO₂ T_melt ≈ 2840 °C; M5 stable to ≈1200 °C
   short-term), low gap resistance.
3. **Mechanical** — strength, creep and irradiation-growth resistance, fretting/grid integrity.
4. **Corrosion / compatibility** — clad–coolant (oxide growth, hydrogen pickup), clad–pellet (PCI),
   no boric-acid system (SBF removes boron-corrosion and dilution pathways).
5. **Irradiation tolerance** — limited swelling, embrittlement and dimensional change over life.
6. **Availability / domesticity / licensing** — all materials are LWR fleet-standard and
   commercially sourced; none require first-of-a-kind qualification.

**Why boron-free + Gd₂O₃/Er₂O₃.** Removing soluble boron (i) guarantees a negative moderator
temperature coefficient at all conditions (no dilution accident), and (ii) eliminates boric-acid
corrosion and CVCS chemistry. The reactivity that boron would hold is instead held by **integral
Gd₂O₃** (strong thermal absorber, burns out with cycle) plus **Er₂O₃** (resonance absorber at 0.5 eV)
to recover cold shutdown margin — the design distinction vs the NuScale anchor (which uses chemical
shim). Selection follows the boron-free SMR literature (Jang et al. 2020; SMART/CAREM practice).

## 8.3.3 Behaviour under neutron irradiation

The relevant fluence environment is taken from the OpenMC fixed-source/shielding model (§8.8):
**RPV fast fluence (E>1 MeV) ≈ 7.0×10¹⁷ n/cm² at 60 y**, set low by the thick (~57 cm) downcomer
water annulus. Core-region fast flux is higher (fuel/clad) but bounded by LWR fleet experience at the
target ≈35–50 GWd/tHM discharge burnup.

| Material | Irradiation effect | Assessment |
|---|---|---|
| UO₂ fuel | Densification (BOL), then solid+gaseous swelling, FGR, rim/HBS at pellet edge | Bounded by §8.3.4 fuel-performance stack-up; FGR within Halden threshold at our LHR |
| M5 cladding | Irradiation growth, creep, waterside oxidation, hydrogen pickup | M5 selected specifically for **low oxidation/H-pickup** vs Zr-4; corrosion/growth within fleet limits to ≥50 GWd/tHM |
| Gd₂O₃ / Er₂O₃ | Absorber depletion (designed burn-out), local power suppression | Burn-out captured in depletion (§8.2); residual Er gives cold SDM |
| SA-508 RPV | Fast-fluence embrittlement (RT_NDT shift, PTS) | **7.0×10¹⁷ ≪ 1×10¹⁹ n/cm² PTS screening** → ≈14× margin; embrittlement a non-issue |
| SS-304 internals | Void swelling, IASCC (fluence-dependent) | Below swelling threshold at internals fluence; SS-304 fleet-qualified |
| B₄C absorber | ¹⁰B depletion, He generation/swelling | Standard rodlet venting / clad accommodation; fleet practice |

The **RPV embrittlement result is a design strength** — the integral large-downcomer layout protects the
vessel far better than a loop PWR, so the 60-year RPV remains well within the unirradiated-toughness
screening envelope.

## 8.3.4 Behaviour over the temperature range (steady-state → accident)

**Steady-state (from conjugate CFD, §8.4):**

| Quantity | Value | Limit | Margin |
|---|---|---|---|
| Fuel centreline temperature | **734 °C** | UO₂ melt 2840 °C | large |
| Peak clad temperature (PCT, normal) | ≈349 °C | M5 design ≈400 °C | adequate |
| Core-average coolant temperature | ≈302 °C (575 K) | sat. at 12.8 MPa ≈330 °C | subcooled |
| MDNBR | 1.56 (CFD) | 1.30 design | PASS |

The 734 °C centreline at nominal LHR keeps the fuel far from melt and below the FGR-acceleration knee,
so steady-state fission-gas release stays in the low (≈1–2 %) athermal regime.

**Transient / accident temperatures.** AOO and DBA temperatures (LOCA PCT, clad oxidation/ECR,
RIA enthalpy) are governed by the transient T-H / DBA analysis (§8.5/§8.6) and are **carried as an
open item there** (TH/3S-owned). The materials selected are the LWR-standard set whose accident
behaviour is bounded by the 10 CFR 50.46 / 1200 °C PCT and 17 % ECR criteria; the design intent is to
demonstrate those margins once the DBA spectrum is closed. *(Cross-reference: could-not-close list.)*

## 8.3.5 Fuel performance and fuel safety (analyses)

Demonstrated by the thermal-mechanical stack-up and established correlations (no fuel-performance code
is required for this tier; a FRAPCON confirmation is identified as an optional strengthener):

- **Centreline-temperature stack-up** — pellet conductivity (k(T,Bu)), gap conductance (He, open/closed
  gap), clad; result **734 °C** at nominal LHR with margin to melt across the burnup range.
- **Fission-gas release** — low athermal release at the operating centreline temperature; rod internal
  pressure stays below system pressure (no clad lift-off).
- **Cladding integrity** — stress/strain within M5 allowables; waterside oxide and hydrogen pickup within
  fleet limits to the discharge burnup; PCI managed by ramp-rate practice.
- **Burnable-absorber compatibility** — Gd₂O₃ lowers local pellet conductivity (accounted in the
  centreline calc for Gd pins); Er₂O₃ loading is dilute (resonance absorber), negligible thermal penalty.

## 8.3.6 Front-end fuel-cycle structural materials

Materials of the fabrication/handling chain are LWR-standard: **Zircaloy-4** guide tubes/spacer grids
and **M5** cladding (tube-and-pellet fabrication, helium backfill, end-plug welding), **SS-304**
bottom/top nozzles and hold-down springs, and Inconel grid springs where fretting margin governs. All
are commercially available, code-qualified (ASTM/ASME), and require no novel fabrication route — keeping
the front-end fuel cycle within proven supply and licensing experience.

---
*Property values (melting points, allowables, oxidation/embrittlement thresholds) are established
fleet/handbook data (ASTM, ASME III, NUREG-0800 §4.2/§4.3, EPRI/Halden) to be cited inline at merge;
design-specific numbers (enrichment, fluence 7.0×10¹⁷, centreline 734 °C, MDNBR 1.56) trace to the
Aegis-40 OpenMC and CFD models.*
