# Aegis-40 secondary cycle — exergy (2nd-law) balance

Dead state T0 = 25 C, P0 = 0.1013 MPa. Heat-source exergy from the primary log-mean temperature (283 C). Computed by `scripts/thermo_exergy.py`.

| Component | Exergy destruction / loss (kW) | Share of supplied exergy |
|---|---:|---:|
| OTSG / steam generator (finite-dT) | 3945 | 6.8 % |
| Turbine + generator stages | 6017 | 10.4 % |
| Condenser (internal dT) | -0 | -0.0 % |
| Condenser heat rejected to sea (loss) | 3702 | 6.4 % |
| Feed / condensate / booster pumps | 42 | 0.1 % |
| FWH-1 (closed-loop open heater) | 810 | 1.4 % |
| Deaerator (FWH-2) | 973 | 1.7 % |
| Moisture separator | 0 | 0.0 % |
| Generator + BOP house load (loss) | 2767 | 4.8 % |
| **Total destroyed + lost** | **18256** | **31.5 %** |
| **Useful electric output** | **39686** | **68.5 %** |

- Supplied heat-exergy (primary @ T_lm = 283 C): **57943 kW**
- Net electric output: **39.7 MWe**
- **Exergetic (2nd-law) efficiency: 68.5 %**  (1st-law net: 31.7 %)
