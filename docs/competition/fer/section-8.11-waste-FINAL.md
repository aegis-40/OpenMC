# 8.11 Nuclear Waste Management

Aegis-40 addresses waste on the three fronts mandated by Technical-Specification Section 4.3.2: (i) an innovative fuel-cycle design minimising spent-fuel quantity and radioactivity per unit energy; (ii) a back-end plan with the three required analyses (source term, decay heat, storage criticality); (iii) minimisation of secondary radioactive waste. All numbers below are from the final STAT_FINAL depletion record (ENDF/B-VIII.0, corrected material volumes, 2026-07-03).

## 8.11.1 Waste-minimization by design (fuel cycle)

The once-through waste basis is 2224 EFPD (6.09 full-power years), 29.6 GWd/tHM core-average discharge burnup and 9.39 tHM initial heavy-metal loading. The calculated waste intensity is 4.40 tHM/TWhe, based on ~2.14 TWhe lifetime electrical generation. The lower-power-density long-cycle design eliminates refuelling entirely and supports a simple once-through baseline.

| Quantity | Aegis-40 (once-through) | CAREM-25 |
|---|---|---|
| Thermal / electric power | 125 MWth / 40 MWe | 100 MWth / 27 MWe |
| Net efficiency | 0.320 | 0.270 |
| Discharge burnup (core-avg) | 29.6 GWd/tHM | 24.0 GWd/tHM |
| Peak-assembly burnup | 42 GWd/tHM (<< 62 GWd/MTU qualified limit) | — |
| HM discharged | 9.39 tHM per ~6.09 FPY (whole core, once) | — |
| Equivalent discharge rate | ~6.1 FA per full-power year | — |
| Waste intensity | **4.40 tHM/TWhe** | 6.43 tHM/TWhe |

Even at the deliberately low once-through burnup, Aegis-40 produces ~32 % less heavy metal per unit electricity than CAREM-25, driven by the higher net efficiency. No assembly exceeds 42 GWd/tHM — a >30 % margin to the 62 GWd/MTU fuel-qualification ceiling even in the hottest position, so cladding-integrity margins are preserved into storage. The lower burnup (vs a multi-batch scheme) is the accepted price of the safety- and nonproliferation-led once-through cycle (Section 8.2.3); the LRM 3-batch equilibrium option (~44.4 GWd/tHM) would cut the intensity to ~2.9 tHM/TWhe if ever adopted.

## 8.11.2 Back-end fuel-cycle management plan

Aegis-40 uses a once-through baseline with no reprocessing. At EOC, the whole core is discharged to the spent-fuel pool, cooled and shielded on site, then transferred to dry storage or a national spent-fuel management pathway according to future regulatory requirements.

## 8.11.3 Spent-fuel source term and decay heat (Section 4.3.2)

All values are evaluated at the end-of-cycle record step (29.4 GWd/tHM, nearest the k = 1 crossing at 29.6 GWd/tHM). Two decay-heat bases are reported. The **rigorous whole-inventory value** (all ~3800 tracked nuclides) governs the immediate pool-cooling load: **7.95 MW at shutdown (about 6.4 % of rated thermal power), falling to 48.4 kW at 1 year and 9.0 kW at 10 years**. The **curated long-lived set** (transport/storage-relevant nuclides) governs the long-term planning basis in Table 8.11-2.

Table 8.11-2 — Long-lived source term vs cooling time (37-FA once-through, ~9.1 tHM at discharge; curated nuclide set):

| Cooling (yr) | Activity (Bq) | Decay heat (W) | Radiotoxicity (Sv) |
|---|---|---|---|
| 0 | 1.23e17 | 16 550 | 2.11e9 |
| 1 | 1.12e17 | 14 230 | 1.92e9 |
| 5 | 8.49e16 | 9 519 | 1.48e9 |
| 10 | 6.87e16 | 7 497 | 1.25e9 |
| 30 | 3.73e16 | 4 643 | 8.01e8 |
| 100 | 6.42e15 | 1 272 | 2.54e8 |
| 1000 | 2.52e14 | 209 | 6.08e7 |

The total whole-inventory activity at discharge is 2.76e19 Bq, dominated by short-lived fission/activation products (Np-239, Xe-133, Mo-99, Zr/Nb-95, Ce-144) that decay away within the first year (activity /59, rigorous heat /164); the long-term source is set by Cs-137, Sr-90 and the transuranics. Bulk specific activity and heat density exceed the heat-generating-waste threshold (>= 2000 W/m3), so the spent fuel is classified **HLW / SNF** (IAEA GSG-1/SSG-40 scheme). The rigorous decay-heat curve is the design input to the pool-cooling load and the dry-cask passive-cooling design. FIGURE 8.11-1 — decay heat + ingestion radiotoxicity vs cooling time (docs/competition/waste/decay_heat_vs_cooling.png).

**Discharge plutonium vector (FIGURE 8.11-2).** The once-through core discharges **76.2 kg of plutonium** with the isotopic vector Pu-238 / 239 / 240 / 241 / 242 = 2.0 / **62.8** / 21.2 / 10.1 / 3.9 wt% — firmly **reactor-grade** (Pu-239 far below the 93 % weapons-grade threshold, high Pu-238/240 content: 12.2 W/kg-Pu decay heat and 3.1e5 n/s/kg spontaneous-fission neutrons act as intrinsic technical barriers). The residual uranium is 1.77 wt% U-235. Because the whole core is discharged once with no reprocessing route, the material stays in intact, highly radioactive assemblies throughout the back end — the fuel-cycle design itself (once-through, moderate burnup, self-protecting assemblies) is the first waste-and-safeguards barrier; the engineered and institutional measures of Section 7 build on it.

## 8.11.4 Spent-fuel storage criticality (Section 4.3.2)

Spent-fuel storage criticality is evaluated separately from the soluble-boron-free reactor-coolant concept. The credited SFP storage basis uses flux-trap absorber racks, burnup credit and approximately 2000 ppm soluble boron in the spent-fuel pool as a defence-in-depth measure. This does not contradict Aegis-40's SBF operating concept because soluble boron is not used for normal reactor-coolant reactivity control. Unborated cases are retained as conservative sensitivity/bounding cases.

Criterion k(95/95) <= 0.95 (NUREG-0800 / 10 CFR 50.68). Burnup-credited fuel (29.6 GWd/tHM once-through composition) in a Region-II absorber rack (17x17 cell, 23.5 cm pitch), modelled as a bounding infinite array:

Table 8.11-3 — Storage-rack criticality (burnup-credited, record basis)

| Configuration | k_calc ± σ | k(95/95) | Verdict |
|---|---|---|---|
| Spent fuel + Boral box (0.40 g/cm² B₄C) | 0.83537 ± 0.00065 | **0.837** | PASS |
| Spent fuel + Metamic box (0.31 g/cm² B₄C) | 0.84521 ± 0.00064 | **0.847** | PASS |

Both sit >= 0.10 below the 0.95 limit, confirmed by two absorber materials. Reactivity ladder (bounding diagnostics, retained deliberately): fresh bare finite 3x3 array 1.363 -> burnup-credited bare infinite array 1.148 -> fresh fuel in Boral rack 1.107 -> **credited configuration 0.837**. A minimum-burnup loading curve administratively excludes fresh/low-burnup assemblies (held in a Region-I flux-trap rack). The credited margin is smaller than in earlier drafts because the once-through discharge burnup (29.6 GWd/tHM) carries less burnup credit than the previously assumed 42.8 GWd/tHM — the present values are the honest record basis. V&V: the reported margins use Delta_bias = Delta_unc = 0; a licensing-grade result adds the OpenMC + ENDF/B-VIII.0 bias from the OECD/NEA Burnup-Credit Benchmark (Phase II) (Section 8.13); even Delta ~ 0.02–0.05 leaves <= 0.90, comfortably under 0.95. The transport+library combination is itself validated against OECD/NEA ICSBEP measured critical experiments (mean bias ~ -50 pcm, Section 8.13). Consistent with the published SBF small-PWR envelope (Kim, Jung & Yoon, 2024).

## 8.11.5 Secondary radioactive-waste minimisation

The soluble-boron-free design eliminates the borated-water secondary-waste streams a boron-controlled PWR generates — spent ion-exchange resins, evaporator concentrates, tritiated boron effluent from the CVCS — a "reduce-quantity" benefit not captured in the tHM/TWhe metric. Remaining operational wastes (filters, dry active waste, clean-up resins) are managed by best-available-technique segregation, volume reduction and conditioning per IAEA GSR Part 5; wastes are collected and segregated by nature for their subsequent processing/destination (not mixed with streams of different characteristics). The integral-vessel layout with no large primary penetrations further limits contaminated-component arisings.
