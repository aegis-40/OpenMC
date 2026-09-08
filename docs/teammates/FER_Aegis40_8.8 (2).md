<!-- Aegis-40 FER §8.8 (rev3). Auto-exported from FER_Aegis40_8.8_rev3.docx. Figures in ./FER_Aegis40_8.8_figures/. Delete this comment before use. -->

## 8.8. Auxiliary Systems Design

### Scope and design-driven simplification

Auxiliary and supporting systems sustain normal operation, provide defence-in-depth (DiD) backup and limit dose (ALARA), without themselves being required to prevent core damage — the fundamental safety functions are discharged passively (§8.4, §8.6) [IAEA SSG-62; SSR-2/1 Rev. 1]. Three Aegis-40 design choices directly **shrink the auxiliary-system burden**, and this is treated as a design advantage rather than generic PWR practice:

- **Soluble-Boron-Free (SBF) core** — eliminates the boric-acid make-up, boron-recovery and chemistry-control plant of a conventional CVCS, reducing the auxiliary-building footprint, liquid radioactive-waste volume and radiological source term.

- **In-vessel control rod drive mechanisms (CRDM)** — no external rod-drive housings, seals or dedicated CRDM cooling system to support.

- **Natural-circulation primary loop** — no reactor coolant pumps, hence no pump seal-injection, lube-oil, component-cooling or large motor electrical loads to serve.

Quantitative performance values quoted in this section are preliminary reference values, drawn from comparable iPWR practice (NuScale VOYGR, CAREM-25), and will be confirmed in the detailed-design phase.

The auxiliary-systems overview is shown in **Figure 8.8-1**.

![Figure 8.8-1](FER_Aegis40_8.8_figures/fig-8.8-1.png)

*Figure 8.8-1. Auxiliary and supporting systems - overview (per IAEA SSG-62).*

### 8.8.1. Fission-Product Release Control

**Purpose.** Confine radioactive fission products through successive barriers and, for any release path, filter and monitor effluent so that public dose stays within limits and the small (≈0.5 km) Emergency Planning Zone is preserved (§8.1, §8.5) [SSR-2/1 Rev. 1; NS-G-1.13].

**Operating principle.** Three DiD barriers act in series — the fuel matrix and Zircaloy-4 cladding, the integral RPV / primary pressure boundary, and the compact containment. Any leakage is captured by the controlled-area HVAC held at negative pressure, routed through a HEPA → charcoal-iodine → HEPA filter train, and released only via the monitored stack. On a high-radiation or containment-isolation signal, containment isolation valves close (fail-safe) and the Standby Gas Treatment System (SGTS) maintains the secondary-confinement underpressure.

**Layout.** Sources are nested within the below-grade containment; isolation valves sit at the containment boundary; filter trains and SGTS are in dedicated HVAC rooms; the release path terminates at the monitored stack. **Figure 8.8-2** gives the release-control flow/P&ID.

**Safety function.** Limit fission-product release in normal operation and design-basis accidents; classified per SSG-30. The **SBF core lowers the gaseous/liquid source term** (no boron-laden effluent), and the integral pump-free primary loop minimises containment penetrations and leak paths.

**Performance.** HEPA ≥99.97 % at 0.3 µm; charcoal ≥99 % elemental iodine; SGTS 2×100 % trains; negative-pressure cascade maintained on a single active failure; stack effluent continuously monitored for noble gas, iodine and particulate activity.

**Maintenance.** Bag-in/bag-out filter change-out, ΔP trending, in-place DOP/halide efficiency testing [RG 1.52]; periodic isolation-valve stroke tests and stack-monitor calibration.

![Figure 8.8-2](FER_Aegis40_8.8_figures/fig-8.8-2.png)

*Figure 8.8-2. Fission-product release control - confinement and filtered-release path (P&ID-level).*

### 8.8.2. Ventilation and Air Conditioning (HVAC)

**Purpose.** Control temperature, humidity, cleanliness and the directional pressure gradient of plant areas so air always flows toward higher potential contamination [SSG-62 §4.108–4.170; SSR-2/1 Req. 73].

**Operating principle.** Once-through (non-recirculating) controlled-area supply/exhaust establishes a pressure cascade (reactor building −250 Pa, fuel-handling/radwaste most negative); the MCR envelope is held slightly positive and filtered for habitability. Exhaust is filtered before stack release; SGTS provides the accident-mode train (§8.8.1).

**Layout.** Air-handling units, fans and filter banks in dedicated HVAC rooms; below-grade placement shortens ducting and adds shielding. **Figure 8.8-3** shows the HVAC flow and pressure-zone cascade.

**Safety function.** Confinement of airborne activity and MCR habitability [GDC 19]; confinement dampers fail closed on loss of power/air.

**Performance.** Pressure-zone cascade and filter efficiencies as in §8.8.1; controlled-area ventilation 2–4 air changes per hour (once-through); MCR envelope +120 Pa with ≈2 000 m³/h filtered make-up air; MCR operator dose within DBA limits [GDC 19].

**Maintenance.** Filter change-out and in-place efficiency testing [RG 1.52]; fan/damper functional tests.

![Figure 8.8-3](FER_Aegis40_8.8_figures/fig-8.8-3.png)

*Figure 8.8-3. HVAC flow and pressure-zone cascade.*

### 8.8.3. Compressed-Air Systems

**Purpose.** Supply clean, dry, oil-free air to pneumatic instruments and valve actuators, plus service and breathing air [SSG-62 §4.94–4.107; SSR-2/1 Req. 72].

**Operating principle.** Oil-free compressors → after-cooler → twin desiccant dryers → receiver → instrument-air header; service air and breathing air are isolated branches so their demand cannot degrade instrument-air quality.

**Layout.** Compressor/dryer skids in the auxiliary building; instrument-air header distributed to actuators across the nuclear island. **Figure 8.8-4** gives the compressed-air P&ID.

**Safety function.** All air-operated valves with a protective function **fail to the safe position on loss of air or power** (containment-isolation fail closed; passive-DHR valves fail open), so loss of air initiates rather than defeats the safe state.

**Performance.** Pressure dewpoint ≤ −40 °C, ISO 8573-1 Class 2; 2×100 % oil-free compressors, ≈10 Nm³/min each at 8 bar(g); receivers sized for ≥30 min instrument-air autonomy, covering compressor swap without actuator movement.

**Maintenance.** Lead/lag/standby compressor rotation, automatic dryer regeneration, dewpoint and oil-carryover monitoring.

![Figure 8.8-4](FER_Aegis40_8.8_figures/fig-8.8-4.png)

*Figure 8.8-4. Compressed-air system (P&ID).*

### 8.8.4. Fuel Handling and Storage Systems

**Purpose.** Receive, store, load and unload fuel while maintaining sub-criticality, cooling, shielding and confinement [SSR-2/1 Req. 80; SSG-63].

**Operating principle.** The complex has three sub-systems — fresh-fuel storage and handling, spent-fuel storage and handling, and the transport-and-technological system. Fresh assemblies are received in transport casks, inventoried and stored dry on criticality-safe cantilever racks in a dedicated Class-1 fresh-fuel store (air medium), sized for one full core plus an operational reserve. Refuelling is carried out under the below-grade cavity with the integral head and upper internals removed; the refuelling machine transfers assemblies underwater to the spent-fuel pool (biological shielding and decay-heat removal), under remote control with height, load and anti-tip interlocks. Pool cooling and cleanup are by redundant trains with passive gravity makeup from the IRWST, and fuel-rod cladding leak-tightness is monitored. After pool residence the assemblies are loaded into dual-purpose transport/storage casks and moved to an on-site dry cask store (ISFSI) with passive air cooling.

**Layout.** New-fuel vault → refuelling cavity → transfer canal → spent-fuel pool → cask-loading station → on-site dry cask store (ISFSI). **Figure 8.8-5** shows the fuel route and storage.

**Safety function.** Maintain **k_eff ≤ 0.95** in the spent-fuel pool. With the flux-trap Boral / Metamic B₄C rack, burnup credit and 2000 ppm pool soluble boron credited, the analysed reactivity is **k_adj = 0.892 ≤ 0.95** (95/95, including bias and uncertainty); the unborated racked configuration remains below 1.0, so both sub-limits of 10 CFR 50.68(b) are satisfied (full criticality basis in §8.11) [ANSI/ANS-8.1; 10 CFR 50.68b; SSG-27]. The pool soluble boron does not conflict with the soluble-boron-free reactor concept — it is credited only for spent-fuel-pool reactivity, never for reactor reactivity control. The once-through, single-batch core (37 assemblies; 2224 EFPD ≈ 6.1 EFPY; discharge burnup 29.6 GWd/tHM; §8.1.5) eliminates periodic refuelling: fuel handling is limited to the initial core load and the whole-core discharge at end of cycle, minimising handling frequency and occupational dose.

**Performance.** Pool bulk ≤ 50 °C; whole-core decay heat ≈7.75 MW at shutdown, falling to ≈48 kW at 1 year and ≈9 kW at 10 years (§8.11), giving a long passive boil-off grace period; the pool is sized for one full-core offload (37 assemblies) plus reserve, and the on-site dry store for at least two discharged cores (≈12 years of operation) [SSG-15].

**Maintenance.** Pool level/temperature instrumentation, liner leak-chase, periodic crane/refuelling-machine load testing.

![Figure 8.8-5](FER_Aegis40_8.8_figures/fig-8.8-5.png)

*Figure 8.8-5. Fuel route and storage.*

### 8.8.5. Fire Protection System

**Purpose.** Protect against fire by prevent–detect–suppress–confine while ensuring a safe-shutdown path survives any single fire [SSR-2/1 Req. 74; NS-G-1.7 / SSG-64; NFPA 805].

**Operating principle.** Redundant safety divisions in separate fire areas bounded by 3-hour-rated barriers; addressable detection to the fire panel/MCR; suppression by wet-pipe sprinklers (general), deluge/pre-action (oil, transformers) and clean-agent total flooding (electrical/I&C and the Digital-Twin computer room).

**Layout.** Division A / Division B fire areas separated by rated barriers; fire-water from redundant pumps. **Figure 8.8-6** is the fire-zone map.

**Safety function.** The division-independent passive safety functions strongly limit a fire's ability to defeat safe shutdown; fire-water pumps (one diesel, one electric) work on loss of off-site power.

**Performance.** 3-h barrier rating; clean-agent design concentration for electrical rooms; fire-water supply 2×100 % pumps (one diesel, one electric), ≈250 m³/h at 8 bar(g) each, with a dedicated reserve ≥500 m³ (≥2 h); safe-shutdown achievable assuming loss of one fire area.

**Maintenance.** Detector/pump testing, sprinkler inspection, barrier-penetration surveillance.

![Figure 8.8-6](FER_Aegis40_8.8_figures/fig-8.8-6.png)

*Figure 8.8-6. Fire-zone map.*

### 8.8.6. Radiation Protection (Shielding, Zoning, Access Control, Dose)

**Purpose.** Keep occupational and public exposure ALARA through shielding, radiation zoning, access control and monitoring [NS-G-1.13; ICRP 103; IAEA GSR Part 3].

**Operating principle.** The plant is divided into dose-rate zones (unrestricted → supervised → controlled → high-radiation); shielding (reinforced concrete plus the inherent self-shielding of the below-grade RPV pool) keeps each occupied area within its zone band; access to higher zones is through a Health-Physics control point with dosimetry and contamination monitoring; area monitors (ARMS) and continuous air monitors (CAM) alarm to the MCR.

**Layout.** **Figure 8.8-7** is the radiation **dose-zone map** with shielding boundaries and access-control points; **Figure 8.8-8** shows the area radiation-monitoring (ARMS/CAM) layout. (This replaces the earlier first-order radial dose profile with explicit dose-zone mapping.)

**Safety function.** Radiation signals interlock to HVAC realignment, SGTS actuation (§8.8.1) and MCR habitability isolation. The **SBF core and reduced CVCS lower the liquid source term**, shrinking the controlled-zone radwaste area and occupational dose.

**Performance.** Zone bands — Zone I <0.5, Zone II 0.5–7.5, Zone III 7.5–25, Zone IV >25 µSv/h; individual occupational dose target < 20 mSv/yr (ALARA).

**Maintenance.** Periodic monitor source-check/calibration; CAM filter change-out and shielding-integrity checks under HP control. (Effluent and radioactive-waste handling: FER §8.11.)

![Figure 8.8-7](FER_Aegis40_8.8_figures/fig-8.8-7.png)

*Figure 8.8-7. Radiation dose-zone map and access control.*

![Figure 8.8-8](FER_Aegis40_8.8_figures/fig-8.8-8.png)

*Figure 8.8-8. Area radiation-monitoring (ARMS/CAM) layout.*

### 8.8.7. Electrical Power Systems — On-Site, Off-Site, Emergency and UPS

**Purpose.** Supply reliable power to plant loads and the supporting power needed by systems important to safety [SSG-34; SSG-62 §4.233–4.267 (Req. 68); GDC 17].

**Operating principle.** Two physically independent **off-site** supplies connect to the Sinop grid (preferred 154 kV line and independent 34.5 kV reserve line); **on-site** distribution segregates Class 1E and non-1E trains with fast transfer; **emergency AC** (2×100 % standby diesel generators, ≈1 MWe each) serves plant-protection and investment-protection loads; **Class 1E DC batteries** (125 V DC, two independent divisions, ≥72 h autonomy) and **uninterruptible power supplies (UPS)** feed protection, safety I&C and the Digital-Twin computer. Owing to passive safety, **AC power is not required for reactor safety** (SSG-62 §3.6) — the natural-circulation, pump-free design removes the large pump electrical loads that dominate conventional emergency-power sizing.

**Layout.** Off-site lines → switchyard → main/unit/reserve transformers → 1E and non-1E buses; battery/UPS rooms ventilated and H₂-monitored; redundant divisions in separate fire areas. **Figure 8.8-9** is the electrical single-line diagram.

**Safety function.** DC/UPS ride-through supports the 286 h passive-cooling grace (§8.5) through extended station blackout; safety side isolated from non-safety by a one-way data diode/air-gap.

**Performance.** Two independent off-site sources, each capable of supplying all plant auxiliaries (total station load ≈2.5 MWe); unit generator 13.8 kV; on-site distribution 6.3 kV MV / 400/230 V AC LV; Class 1E DC 125 V with ≥72 h autonomy (≈2×1 500 Ah per division); UPS 2×100 % static inverters per division, 230 V AC; independence and separation per IEEE Std 308/384.

**Maintenance.** Battery capacity-discharge tests, relay-protection testing, transfer-scheme functional checks.

![Figure 8.8-9](FER_Aegis40_8.8_figures/fig-8.8-9.png)

*Figure 8.8-9. Electrical single-line - emergency and UPS supplies.*

### 8.8.8. Other Auxiliary and Supporting Systems (SSG-62 completeness)

For completeness against IAEA SSG-62, the remaining supporting systems are summarised below; each carries the same purpose/principle/layout/safety/performance/maintenance basis as above and is documented in the digital appendix.

- **Process and post-accident sampling** (Req. 71) — representative sampling of coolant, containment atmosphere/sump and effluents under normal and accident conditions, with shielded handling. **Figure 8.8-10**.

- **Process radiation monitoring** (Req. 82) — activity monitoring of process and effluent streams; high readings drive ESF actuation. **Figure 8.8-11**.

- **Communication systems** (Req. 37) — diverse, independent media; accident-management links on emergency/UPS power. **Figure 8.8-12**.

- **Normal and emergency lighting** (Req. 75) — emergency lighting from emergency AC and self-contained battery units (≥90 min) for credited actions and egress. **Figure 8.8-13**.

- **Overhead lifting / handling** (Req. 76) — single-failure-proof reactor-hall (polar/bridge) crane, refuelling machine and cask-handling equipment; loads over the core and spent-fuel pool follow restricted safe-load paths with a postulated dropped-load analysis; the crane set also supports RPV-head, upper-internals, in-vessel-shaft and steam-generator-cassette handling for maintenance [ASME NOG-1; NUREG-0554; NUREG-0612; SSG-63]. **Figure 8.8-14**.

- **Component cooling, demineralised water and reduced make-up/purification** (Req. 70, §2.6(k)) — closed CCWS as a monitored barrier to the seawater normal heat sink (the safety-grade ultimate heat sink is the IRWST / passive containment cooling, §8.5, not seawater); the SBF core eliminates the boron-recovery functions of a conventional CVCS. **Figure 8.8-15**.

![Figure 8.8-10](FER_Aegis40_8.8_figures/fig-8.8-10.png)

*Figure 8.8-10. Process and post-accident sampling system.*

![Figure 8.8-11](FER_Aegis40_8.8_figures/fig-8.8-11.png)

*Figure 8.8-11. Process radiation monitoring system.*

![Figure 8.8-12](FER_Aegis40_8.8_figures/fig-8.8-12.png)

*Figure 8.8-12. Communication systems architecture.*

![Figure 8.8-13](FER_Aegis40_8.8_figures/fig-8.8-13.png)

*Figure 8.8-13. Normal and emergency lighting.*

![Figure 8.8-14](FER_Aegis40_8.8_figures/fig-8.8-14.png)

*Figure 8.8-14. Overhead lifting and safe-load-path.*

![Figure 8.8-15](FER_Aegis40_8.8_figures/fig-8.8-15.png)

*Figure 8.8-15. Auxiliary cooling, demineralised water and reduced CVCS.*

### 8.8.9. Cogeneration Interface Isolation (Radionuclide Confinement to the Heat / Hydrogen User)

**Purpose.** Ensure that no process transports radionuclides to the district-heat or hydrogen user in operational or accident states [SSR-2/1 Rev. 1 Req. 35].

**Operating principle.** A **non-radioactive intermediate loop** is interposed between the reactor secondary steam and both customer circuits (the thermochemical district-heat network and the solid-oxide electrolyser), so reactor steam never contacts district-heat water or electrolyser feed. The intermediate loop is held at **higher pressure than the reactor-side stream at each interface heat exchanger**, so any tube leak flows **inward** (clean → reactor), never outward to the user. This gives **≥ 3 independent barriers** between the primary coolant and the product: (1) steam-generator tube wall, (2) intermediate-loop boundary, (3) customer-side heat-exchanger wall.

**Layout.** Interface heat exchangers at the reactor-secondary boundary; the intermediate loop feeds the thermochemical-storage and electrolyser heat exchangers; the thermochemical store and electrolyser sit downstream of the barrier set. **Figure 8.8-16**.

**Safety function.** Confine radioactivity to the nuclear island under all conditions. Accident-condition isolation is by **fail-closed ESFAS valves** actuated on high intermediate-loop or product activity, on a steam-generator-tube-rupture signal, or on containment isolation (§8.7.3). Tritium is the governing nuclide at the high-temperature (~800 °C) electrolyser interface, addressed by permeation-barrier coatings, a hydrogen-product tritium monitor and an intermediate-loop getter.

**Performance.** Inward pressure bias maintained at every interface; ≥ 3 barriers on any radionuclide transport path; fail-closed isolation on the credited signals; product-stream activity continuously monitored.

**Maintenance.** Interface-heat-exchanger leak testing; intermediate-loop activity and tritium monitoring; isolation-valve stroke testing.

![Figure 8.8-16](FER_Aegis40_8.8_figures/fig-8.8-16.png)

*Figure 8.8-16. Cogeneration-interface isolation - non-radioactive intermediate loop and three-barrier confinement.*

### References cited in §8.8

- IAEA, Design of Auxiliary and Supporting Systems for NPPs, **SSG-62**.

- IAEA, Safety of NPPs: Design, **SSR-2/1 (Rev. 1)** — Req. 37, 68, 70–82.

- IAEA, Design of Electrical Power Systems for NPPs, **SSG-34**.

- IAEA, Design of Fuel Handling and Storage Systems, **SSG-63**; Storage of Spent Fuel, **SSG-15**.

- IAEA, Protection against Internal Fires and Explosions, **NS-G-1.7** (current **SSG-64**).

- IAEA, Radiation Protection Aspects of Design for NPPs, **NS-G-1.13**; **GSR Part 3**; ICRP **Publication 103**.

- IAEA, Safety Classification of SSCs, **SSG-30**.

- U.S. NRC **10 CFR 50 App. A** (GDC 17, 19); **RG 1.52**.

- IEEE **Std 308**, **Std 384**; **ANSI/ANS-8.1**; **NFPA 805**; **ISO 8573-1**.

- IAEA, Criticality Safety in the Handling of Fissile Material, **SSG-27**; U.S. NRC **10 CFR 50.68**; **NUREG-0800 §9.1**. Heavy-load handling / cranes: **ASME NOG-1**; **NUREG-0554**; **NUREG-0612**.

