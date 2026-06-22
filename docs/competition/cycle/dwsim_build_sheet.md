# DWSIM build sheet — Aegis-40 cogeneration cycle

Step-by-step to reproduce `thermo_cycle.py` + the TCES/DH integration in **DWSIM**
(free, open-source: https://dwsim.org). Build in three stages; validate each before
adding the next. Targets in **bold** come from `thermo_cycle.py` / `tces_dh_balance.py`.

## Setup
1. Install DWSIM (Windows/Linux/macOS). New **Steady-State** simulation.
2. **Property package:** *Steam Tables (IAPWS-IF97)*. Compound: **Water**.
3. Unit system: SI (°C, bar, kg/s, kW). Note **45 bar = 4.5 MPa**, **0.07 bar = 7 kPa**.

## Stage 1 — basic Rankine (validate the heat balance)
Build the simplest loop; confirm power and condenser duty before adding regeneration.

| Block | Type | Key spec |
|---|---|---|
| Main Steam | Material Stream | 45 bar, 296 °C, **57.8 kg/s** |
| TRB-1 | Expander (Turbine) | outlet 0.07 bar, isentropic η = **0.85** → energy stream `W_t` |
| COND | Cooler | outlet 0.07 bar, vapour fraction = 0 → duty `Q_cond` |
| CP | Pump | outlet 45 bar, η = 0.82 → energy stream `W_p` |
| BOILER | Heater | outlet 296 °C (closes loop) → duty `Q_in` |

**Validate:** `Q_in` ≈ **125 MWth**, `Q_cond` ≈ **82.6 MWth**, net shaft `W_t − W_p` ≈ **42.8 MW**.
(Single-stage expansion gives wet exhaust — Stage 2 fixes last-stage moisture.)

## Stage 2 — extractions, moisture separator, feedwater heating
Split the expansion so you can bleed steam; raises efficiency to the real design point.

- Replace TRB-1 with **TRB-1 (45→10 bar)** → **TEE-1** (bleed `y1` to FWH-1) → **TRB-2 (10→1.5 bar)**
  → **SEP-1** (moisture separator: vapour to TRB-3, liquid drain to deaerator) →
  **TRB-3 (1.5→0.07 bar)**.
- **FWH-1 / Deaerator:** model open FWHs as **Mixers** (bleed steam + feedwater → saturated liquid),
  with a pump between pressure levels (CP → DA → BP → FWH-1 → FP).
- Extraction pressures: **10 bar (1.0 MPa)** → FWH-1; **1.5 bar (0.15 MPa)** → deaerator.

**Validate (Table 8.9-3):** gross electric ≈ **42.2 MWe**, **net ≈ 39.7 MWe**, η_net ≈ **31.8 %**,
last-stage exhaust quality **x ≈ 0.892**.

## Stage 3 — TCES charge + district-heat loop (the new part)
The store is represented by **heat duties**, not chemistry.

- **Charge:** TEE off the 10 bar extraction → **IHX (Cooler)** cooling the steam to saturated liquid
  (180 °C); its duty is the **charge power**. Drain returns to the feedwater train.
- **Store:** a single **Energy Stream** link — discharge heat = charge heat × round-trip
  (**0.88 ammine / 0.78 zeolite**). (DWSIM holds no chemistry; that's correct here.)
- **DH loop (separate water circuit):** Material Stream **DH water** 90/45 °C; a **DH HX (Heater)**
  adds the discharge heat to it. Size for **25 MWth → 133 kg/s** DH water.
- **H₂ (optional):** off-peak `W_t` → note 8 MWe to a PEM block (160 kg/h); no DWSIM block needed.

**Validate:** charge-loop temperature ≥ **168 °C**; DH supply ≥ **90 °C**; charge penalty
≈ **0.31 MWe/MWth** (compare lost expander work of the bled steam vs. IHX duty).

## When to graduate to OpenModelica
Only once you need **time-domain dispatch** (store filling/emptying over a day or season) or
plant **transients** — then port this validated flowsheet to OpenModelica + ThermoSysPro. The
TCES reaction kinetics (salt–NH₃ / zeolite–water) go in **Cantera** or the `alishsan/tces` model,
coupled to the steam side.
