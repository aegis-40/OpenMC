<!-- Aegis-40 FER §8.10 (final). Auto-exported from FER_Aegis40_8.10.docx. Figures in ./FER_Aegis40_8.10_figures/. Delete this comment before use. -->

## 8.10. Plant Layout Design

### 8.10.1. Overall Layout Description

The Aegis-40 is a 125 MWth / ~40 MWe (net) integral Pressurized Water Reactor (iPWR) for coastal deployment at the Sinop site on the Turkish Black Sea coast, identified as the optimal Turkish NPP location by multi-criteria analysis [Kurt, 2014]. The general arrangement is developed to satisfy four governing objectives simultaneously: **inherent nuclear safety, construction efficiency and modularity, economic competitiveness, and reliable long-term operation and maintenance** over the 60-year design life.

The defining spatial characteristic is the complete integration of the primary pressure boundary. The Reactor Pressure Vessel (RPV) — dimensionally referenced to the NuScale VOYGR Design Certification Application (NRC Docket No. 52-048) — houses the core, two helical-coil once-through steam generators (OTSGs), and the integral pressurizer within a single pressure boundary. Primary circulation is driven entirely by natural convection, with no reactor coolant pumps. This integral, pump-free architecture removes all large-bore primary piping, eliminates the large-break loss-of-coolant accident (LB-LOCA) as a design-basis event, and substantially reduces the Reactor Building footprint.

Following IAEA plant-grouping practice, the site is organised into a **Nuclear Island (NI)** (Seismic Category I / Class 1E; Protected security area), a **Turbine (Conventional) Island** (Seismic Category II power conversion, switchyard and once-through seawater cooling; Vital security area) and a Cogen (Industrial) Island (Seismic Category III, non-safety: thermochemical district-heat store, SOE hydrogen unit and H₂ storage; NFPA 2; Additional security area, H₂ set back ≥100 m). The Turbine and Cogen islands together form the secondary-side Energy Island. Seismic category is a per-building property, not a property of the island — e.g. the Control Building sits in the Turbine Island for MCR–turbine adjacency but is Seismic Cat I. The overall site arrangement and security-area zoning are shown in **Figure 8.10-1**. Governing layout constraints are the ≈0.5 km Emergency Planning Zone, the 0.3 g SSE foundation basis, consolidated containment penetrations, and the NFPA-2 hydrogen explosion stand-off.

![Figure 8.10-1](FER_Aegis40_8.10_figures/fig-8.10-1.png)

*Figure 8.10-1. Aegis-40 site general arrangement and security-area zoning (Protected / Vital / Additional areas; single 40 MWe unit).*

### 8.10.2. Site Zoning and the Combined Energy Island

A key layout decision for the Aegis-40 is that the three secondary-side consumers — the **steam turbine, the Thermochemical Energy Storage (TES) district-heating module, and the Solid Oxide Electrolysis (SOE) hydrogen unit** — are all co-located within a single Energy Island and fed from **one main-steam corridor** leaving the Reactor Building. Because all three loads draw from the secondary side (the turbine from the main steam header, the TES from a pass-out / extraction branch at ~280 °C / 15 bar during peak hours, and the SOE from the deaerator-inlet steam during off-peak hours), a single below-grade steam corridor with short branch take-offs serves the entire island. This minimises high-energy piping length, the number of Reactor-Building penetrations, and the overall footprint, while simplifying isolation and in-service inspection. The steam-distribution arrangement is shown in **Figure 8.10-2**.

![Figure 8.10-2](FER_Aegis40_8.10_figures/fig-8.10-2.png)

*Figure 8.10-2. Secondary-side steam distribution: main steam to turbine, TES from turbine extraction, SOE from deaerator-inlet steam.*

The Turbine Generator Building (TGB) is oriented with its condenser end toward the sea to shorten the circulating-water route to the Black Sea, which is the seawater normal heat sink (the safety-grade ultimate heat sink is the below-grade RPV pool / IRWST, §8.5, §8.8.8 — independent of seawater). The TES Building (TESB) is placed on the landward side of the TGB, closest to the Sinop district-heating tie-in, and the SOE hydrogen unit (SOEU) is located at the downwind end of the island as a detached, NFPA-2-compliant hydrogen hazard zone, kept clear of the control room and the public boundary. A seismic gap of not less than **75 mm** separates all Category I structures from the Category II Energy Island to prevent structural interaction during the Safe Shutdown Earthquake (SSE = 0.3 g).

### 8.10.3. Principal Buildings and Structures

Table 8.10-1 summarises the main buildings, their functions, safety classifications, footprints and key construction parameters. Footprints are preliminary first-cut estimates (reference iPWR practice), to be confirmed in detailed design. The Nuclear Island grade-level arrangement is shown in **Figure 8.10-3**.

**Table 8.10-1. Aegis-40 principal buildings, safety classification and construction notes.**

- **Reactor Building (RB)** — houses RPV, natural-circulation primary loop, containment vessel, passive DHRS HX and IRWST. Seismic Cat. I / Class 1E. Reinforced concrete; 1.2 m shielding walls; post-tensioned dome; below-grade RPV pool. Footprint ≈625 m²; security Vital/Protected.

- **Spent Fuel Pool Building (SFPB)** — interim spent-fuel storage, transfer canal, fuel-handling machine. Seismic Cat. I. RC; shared shielding wall with RB; borated-water pool (pool boron is credited for spent-fuel-pool criticality per 10 CFR 50.68; the reactor itself is soluble-boron-free — see §8.8.4). Footprint ≈450 m²; Protected.

- **Auxiliary / Radwaste Building (ARB)** — reduced CVCS (SBF core), liquid radwaste, decontamination, chemistry. Seismic Cat. I/II. RC (Cat. I zones) + steel (Cat. II). Footprint ≈500 m²; Protected.

- **Control Building (CB)** — main control room, supplementary control point, Digital-Twin process computer, Class 1E switchgear. Seismic Cat. I / Class 1E; sited in the Turbine Island for MCR–turbine adjacency. Hardened RC; tornado-missile protected; air-gapped from external networks. Footprint ≈375 m² (2-storey, ≈700 m² GFA); Vital/Protected.

- **Turbine Generator Building (TGB)** — steam turbine, condenser, feedwater heaters, deaerator, generator. Seismic Cat. II. Structural steel; seismic gap ≥75 mm from NI; ≥20 m turbine-missile separation. Footprint ≈600 m²; owner-controlled.

- **TES / District-Heating Building (TESB)** — zeolite 13X sorption modules (~390 t), heat exchangers, district-heating interface. Seismic Cat. III (non-safety, Cogen Island). Steel; charged from turbine extraction. Footprint ≈900 m²; owner-controlled.

- **SOE Hydrogen Unit (SOEU)** — solid-oxide cells (8 MWe), H₂ condenser-chiller, compression to 30 bar. Seismic Cat. III (non-safety, Cogen Island). Detached pad; H₂ hazard separation per NFPA 2. Footprint ≈625 m²; owner-controlled.

- **Diesel Generator Building (DGB)** — 2× emergency diesel generators (≥100 % each), day tanks, control panels. Seismic Cat. I / Class 1E. Footprint ≈150 m²; Protected.

- **Waste Management Building (WMB)** — liquid-radwaste tanks, solid-waste compactor, gaseous-radwaste hold-up, HEPA + charcoal; off-gas stack. Seismic Cat. I. Footprint ≈375 m²; Protected.

- **Switchyard & Main Transformers (EHB)** — main + unit-auxiliary transformers (≈50 MVA), station-service transformer, 154 kV grid interface with 34.5 kV reserve (§8.8.7). Seismic Cat. II (non-safety). Footprint ≈2 650 m² (incl. ≈2 500 m² yard); owner-controlled.

- **Circulating-Water Pump House (CWP) + seawater intake/outfall** — once-through Black Sea circulating water for the condenser; breakwater-protected intake (trash racks, redundant travelling screens, chlorination) and discharge/outfall structure. Seismic Cat. III (non-safety); normal heat sink only. CWP ≈240 m² on-island; intake/outfall are shoreline structures.

- **Workshop / Service Building (WSB)** — maintenance shops, warehouse, hot-tool storage. Seismic Cat. III (non-safety). Footprint ≈300 m²; owner-controlled.

- **H₂ Storage Yard (H2S)** — compressed-gas tanks (≈350 bar) and distribution manifold. Seismic Cat. III; NFPA 2; set back ≥100 m from the nearest NI building, clear of the switchyard and MCR. Footprint ≈600 m²; owner-controlled.

The Reactor Building is the dominant NI structure: a cylindrical RC shell with a post-tensioned hemispherical dome enclosing the containment vessel and the below-grade RPV pool. The pump-free integral primary loop requires no primary-pump penetrations through containment, reducing the number of penetrations and simplifying in-service inspection.

![Figure 8.10-3](FER_Aegis40_8.10_figures/fig-8.10-3.png)

*Figure 8.10-3. Nuclear Island plan, grade level (El. plus/minus 0.00).*

### 8.10.4. Below-Grade Arrangement and Passive-Safety Layout

The entire RPV is positioned below grade within a steel-lined borated-water pool, consistent with the NuScale and CAREM-25 reference configurations. The below-grade plan at the RPV-pool level (El. −12.0 m) is shown in **Figure 8.10-4** and the north–south cross-section in **Figure 8.10-5**. This placement simultaneously: lowers the centre of gravity of the heaviest components, improving seismic performance under the 0.3 g SSE; enables fully gravity-driven passive safety functions (DHRS and ECCS) with no pumps or active valves; provides the pool as the safety-grade ultimate heat sink for a 286 h passive-cooling grace period (§8.5) and as biological shielding; reduces the exposed security perimeter; and gives inherent protection against external hazards including aircraft impact — supporting the plant-boundary Emergency Planning Zone.

![Figure 8.10-4](FER_Aegis40_8.10_figures/fig-8.10-4.png)

*Figure 8.10-4. Nuclear Island below-grade plan (RPV pool, El. -12.0).*

![Figure 8.10-5](FER_Aegis40_8.10_figures/fig-8.10-5.png)

*Figure 8.10-5. Reactor Building cross-section A-A.*

### 8.10.5. Two- and Three-Dimensional Layout Plans

The general arrangement is documented in the following reference drawings, submitted as Digital Appendices:

- **AE-40-GA-001** — Site General Arrangement Plan (1:500): boundary, road access, Sinop seawater intake/discharge, building spacing, EPZ boundary.

- **AE-40-GA-002** — Nuclear Island Plan, Grade Level (El. ±0.00), 1:200.

- **AE-40-GA-003** — Nuclear Island Plan, Below-Grade (El. −12.0 / RPV pool), 1:200.

- **AE-40-GA-004** — Reactor Building Cross-Section A–A, 1:200.

- **AE-40-GA-005** — Main-Steam Distribution to Turbine + TES + SOE.

- **AE-40-GA-006** — Full-Site 3D Isometric, generated from the CAD model.

The 3D CAD model is the **Single Source of Truth (SSOT)** for spatial coordination and contains all structures, equipment and piping of nominal diameter ≥50 mm, maintained under version control (Git/GitHub). Structural information feeding the specification basis includes RC wall/slab thicknesses and rebar schedules (from seismic demand per ASCE 4-16 / 43-19), structural-steel member and connection details for Category II buildings, inter-building connection structures (below-grade pipe tunnel, cable tunnel, personnel corridors), and system weight distributions used as structural-analysis inputs. The site 3D massing is shown in **Figure 8.10-6**.

![Figure 8.10-6](FER_Aegis40_8.10_figures/fig-8.10-6.png)

*Figure 8.10-6. Site 3D isometric (schematic).*

### 8.10.6. Critical Piping Arrangement

Critical piping comprises large-diameter / high-energy lines whose dimensions, thermal expansion or seismic response govern building penetrations, equipment placement and structure sizing. Table 8.10-2 lists the Aegis-40 critical piping, including the TES and SOE steam branches unique to this multi-application configuration.

**Table 8.10-2. Aegis-40 critical piping — routing, design parameters and layout drivers.**

- **Main Steam Line (MSL)** — 2 × DN250, ~296 °C / 4.5 MPa, RB → Energy Island (below-grade tunnel). ASME III Cl. 2; MSIVs inside RB within 1.5 m of penetration; whip restraints ≤3 m; redundant trains ≥3 m apart; common corridor serves turbine + TES + SOE branch take-offs.

- **Main Feedwater Line (FWL)** — 2 × DN200, ~180.6 °C / 4.5 MPa, Energy Island → RB (co-routed with MSL). ASME III Cl. 2; MFIVs at RB boundary; thermal sleeve at RPV nozzle; RC dividing wall from MSL in the tunnel.

- **TES charging branch** — pass-out / extraction steam ~280 °C / 1.5 MPa, header → TESB. Isolation valves at TESB inlet; short run within the Energy Island.

- **SOE steam branch** — ~DN150 [EST], deaerator-inlet steam, RB/turbine header → SOEU (off-peak). Sized larger than the H₂ product line to pass the electrolyser steam demand; isolation + flow control; H₂-side separated per NFPA 2.

- **Decay Heat Removal (DHRS)** — 2 × DN100, 308 °C / 14.1 MPa, intra-RB (RPV ↔ DHRS HX in pool). ASME III Cl. 1; fully passive; no active valves; no containment penetration required.

- **Passive ECCS injection** — 2 × DN80, 14.1 MPa design, intra-RB (IRWST → RPV). ASME III Cl. 1; gravity-driven; no pump penetrations.

- **Pressurizer surge line** — eliminated by the integral design (internal to RPV upper head).

- **Non-radioactive intermediate loop** — ~DN200 [EST], ~200–280 °C, held above reactor-side pressure so any leak flows inward; interface HX at the reactor–secondary boundary → TES / SOE / district-heat HXs. Req 35 isolation barrier — reactor steam never contacts customer circuits. ASME B31.1.

- **District-heat supply / return** — 2 × DN300–400 [EST], supply ~120–150 °C / cooler return, low P, district-heat HX → site boundary → town network. Non-radioactive (downstream of the intermediate loop); defines the district-heat pipeline corridor. ASME B31.1.

- **H₂ product line** — DN50–80 [EST], ambient / ~30–350 bar, SOE → compressor → H₂ storage yard within the Cogen Island. ASME B31.12; flammable-gas hazard drives the H₂ stand-off and NFPA-2 zoning.

- **Emergency feedwater (EFW)** — 2 × DN80 [EST], ~150 °C / SG pressure, elevated EFW tank (NI) → SG, gravity-driven; safety-related and passive (no pumps); diverse from the passive DHRS. ASME III Cl. 2/3.

- **Condenser circulating water (once-through seawater)** — large-bore, ~2–2.5 m³/s (≈82 MWth at ΔT ≈8–10 K), seawater intake → CWP → condenser → outfall. ASME B31.1; normal heat sink only (safety UHS independent).

- **Component cooling water (CCWS) final rejection** — to seawater (once-through), normal sink; non-safety final rejection — SFP/aux loads retain passive long-term grace independent of CCWS. ASME B31.1.

Main steam and feedwater lines exit the RB through dedicated, missile-protected, double-walled penetrations with annular leak-off monitoring and are routed in a below-grade tunnel to the Energy Island; postulated pipe-whip zones have been confirmed not to impact safety-related SSCs.

### 8.10.7. Scalability and Multi-Unit Roadmap

While the reference design is a single 40 MWe unit, the arrangement is laid out to support the staged multi-unit deployment envisaged in the PER (5–10 units toward Turkey's SMR targets). Additional units replicate the NI module and share common infrastructure (intake/discharge, switchyard, access, and the Energy Island services), enabling phased construction and economies of scale on the same site, consistent with the NuScale multi-module precedent.

