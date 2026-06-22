# Aegis-40 cogeneration — process-flow description (Fig 8.9-3)

Accompanies `aegis40_cogen_pfd.drawio` / `pfd_cogeneration_tces.png`. Numbers from
`thermo_cycle.py` and `tces_dh_balance.py`.

## Plant in one sentence
A 125 MWth integral PWR drives **one** tandem-compound turbine-generator for electricity,
while a **thermochemical store (TCES)** — kept outside the nuclear island behind an
intermediate heat exchanger — time-shifts heat to a district-heating network, and an
off-peak electrolyser makes hydrogen. Three products: **electricity + district heat + H₂**.

## 1. Power path (always on)
Natural-circulation primary coolant boils the secondary side in the in-vessel helical OTSG,
producing **superheated steam (4.5 MPa, 296 °C, 57.8 kg/s)**. The steam expands through the
**single tandem-compound turbine** (HP → moisture separator → LP, one shaft, one generator)
to the condenser (7 kPa, 39 °C), which rejects 82.6 MWth to a **once-through seawater** ultimate
heat sink (Black Sea, Sinop; ~2,065 kg/s / 2.0 m³/s intake, ΔT ≤ 10 K outfall — **no cooling tower,
no evaporative water use**; far-field sea rise ≤ 0.2 K after diffuser dilution, see
`scripts/seawater_heat_sink.py`). Condensate is pumped
back through the feedwater train (FWH/deaerator → feed pump) to the OTSG. Gross output
**40.0 MWe net** (η ≈ 32 %).

## 2. Charge path (off-peak / summer — low district-heat demand)
A branch of **HP-extraction steam (1.0 MPa, 180 °C)** is routed to the **intermediate heat
exchanger (IHX)**. Across the IHX it heats a **closed charge loop (~168 °C)** that drives the
endothermic regeneration of the store:
- **ammine:** NiCl₂·6NH₃ + heat → NiCl₂·2NH₃ + 4 NH₃↑ (desorption);
- **zeolite:** zeolite·(H₂O) + heat → dry zeolite + H₂O↑.

The IHX is the isolation boundary: the storage medium never contacts reactor steam, so the
store is a **non-safety auxiliary**. Charging costs **0.31 MWe per MWth** stored (the
extraction steam is no longer making power), so net output dips to ≈ **35.6 MWe** while
charging. The store then holds its charge **loss-free** — for hours, days, or a full season.

## 3. Discharge path (peak / winter — high district-heat demand)
On demand the reaction reverses exothermically and releases heat at **~150 °C** (ammine) /
~130 °C (zeolite). This heat passes through the **district-heat heat exchanger (DH HX)** into a
**separate district-heating water loop (90 °C supply / 45 °C return, 133 kg/s)** feeding the
town network at up to **25 MWth**. Because the heat comes from the store, the turbine keeps
the **full 40 MWe** flowing to the grid during the peak — the electricity penalty was already
paid at off-peak charge time. This is the core value: **decouple heat delivery from generation.**

## 4. Hydrogen path (off-peak)
Surplus off-peak electricity feeds an **8 MWe PEM electrolyser** (≈ 50 kWh/kg), producing
**~160 kg H₂/h (≈640 t/yr)**; TCES discharge heat can pre-heat the electrolyser feed.

## Operating modes at a glance
| Mode | Turbine | Store | DH network | H₂ |
|---|---|---|---|---|
| Baseload (day) | 40 MWe → grid | idle (holds charge) | direct extraction only | — |
| Charge (off-peak/summer) | ~35.6 MWe | charging from IHX | low | running |
| Discharge (peak/winter) | 40 MWe → grid | discharging | up to 25 MWth from store | reduced |
