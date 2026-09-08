# Digital Appendix - Power-conversion cycle, hydrogen and district-heat cogeneration

The Chapter 8.9 energy-cycle state points: secondary Rankine cycle, SOE hydrogen co-production schedule, and TCES district-heat balance, plus LCOE and exergy.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`code/thermo_cycle.py` (Rankine, IAPWS-IF97), `soe_h2_schedule.py`, `tces_dh_balance.py`, `zeolite_tes_sizing.py`, `economics_lcoe.py`, `thermo_exergy.py`, `seawater_heat_sink.py`. Operating point in-script.

## Approach
IAPWS-IF97 steam properties; OTSG pinch constraint; single-turbine cogeneration with IHX-isolated TCES (zeolite-13X/water) store; SOE hydrogen at off-peak.

## Outputs obtained
`outputs/cycle_state_points.csv` - full T/p/h/s state points; ~40 MWe net at ~32% efficiency; hydrogen ~427 t/yr; district-heat balance closes. `outputs/fuel_cycle_cost.csv` - front-end fuel-cycle cost from the 4.43 wt% core-average enrichment (6.72 SWU/kg, front-end $5.47M/yr, matches Table 8.12-5). `outputs/lcoe_sensitivity.csv` - LCOE vs CAPEX band and discount rate (NOAK $3500/kWe -> $74.9/MWh at 7%). The report Section 8.12 detailed case is authoritative; this is the Tier-B cross-check (NOAK and fuel cost reproduce it; higher-CAPEX cells drift ~$1-3 on capital-financing assumptions).

## How to reproduce
```bash
`python code/thermo_cycle.py` (writes state points); other scripts run standalone.
```

## Verification & validation (reliable sources)
Steam properties verified against IAPWS-IF97 reference points; TCES store validated separately in folder 9 (Yan 2020).

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
