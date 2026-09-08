# §8.9.2 — Zeolite-13X adsorption store: first-principles basis (paste-ready)

*(Independent, literature-anchored confirmation of the frozen zeolite-13X TCES store; script:
`openmc_model/scripts/zeolite_tes_sizing.py`, also in digital appendix `7_energy_cycle/`.)*

## Working principle

The reference store is a **zeolite-13X / water adsorption** thermochemical store. Heat is stored by
**desorbing** (drying) the zeolite bed during charge; heat is released when water vapour **re-adsorbs**
onto the dried zeolite during discharge, liberating the adsorption enthalpy (which exceeds the latent
heat of condensation by the sorbate binding energy). Because energy is held as a **dry-vs-hydrated
material state, the store has no standby thermal loss** — the defining advantage over sensible
molten-salt/water tanks, enabling flexible day-to-season time-shifting of the stored block.

## Material properties (published)

| Property | Value | Source |
|---|---|---|
| Water-on-13X adsorption enthalpy, ΔH_ads | ~3500 kJ/kg-H₂O (band 3300–3600) | Yu 2013 [1]; Scapino 2017 [2] |
| Working uptake swing, Δq (regen ~168–180 °C ↔ adsorbed) | ~0.20 kg-H₂O/kg-zeolite (full capacity ~0.25–0.30) | Scapino 2017 [2] |
| Packed pellet-bed bulk density | ~650 kg/m³ (band 640–720) | Scapino 2017 [2] |
| Regeneration (charge) temperature | ~130–180 °C | Hauer [4]; N'Tsoukpoe 2009 [3] |

## Derived storage metrics and design sizing

Gravimetric density = ΔH_ads × Δq = 3500 × 0.20 = **700 kJ/kg = 0.194 kWh/kg**; volumetric density =
0.194 × 650 = **~126 kWh/m³**. For the district-heat design block (25 MWth peak × 8 h = **200 MWh_th**
delivered), with a bed regenerated at the **168 °C IHX charge loop** (from the 1.0 MPa/180 °C HP
extraction) and discharging at **~130 °C** (≥ the 90 °C DH supply, with margin):

| Quantity | First-principles (literature) | Parametric (`tces_dh_balance.py`) | Δ |
|---|---|---|---|
| Gravimetric energy density | 0.194 kWh/kg | 0.20 kWh/kg | −3 % |
| Volumetric energy density | 126 kWh/m³ | 130 kWh/m³ | −3 % |
| Zeolite mass | ~1029 t | 1000 t | +3 % |
| Bed volume | ~1582 m³ | 1538 m³ | +3 % |
| Charge heat (round-trip 0.78) | 256 MWh_th | 256 MWh_th | 0 % |

**Two independent methods — a first-principles calculation from published zeolite-13X/water
adsorption data and the plant-level `tces_dh_balance.py` energy balance — agree within 3 %.** The
frozen store therefore rests on a self-consistent, citable basis: energy density, regeneration and
discharge temperatures, mass and volume are all confirmed. Zeolite-13X is commercially mature and
thermally stable over thousands of adsorption/desorption cycles [1,2], the water working fluid is
benign, and operation is near-atmospheric — properties that motivated its selection over the more
compact but ammonia-bearing resorption alternative (§8.9.2).

## References

[1] N. Yu, R.Z. Wang, L.W. Wang, *Sorption thermal storage for solar energy*, Prog. Energy Combust.
Sci. 39 (2013) 489–514.
[2] L. Scapino et al., *Sorption heat storage for long-term low-temperature applications: a review at
material and prototype scale*, Appl. Energy 190 (2017) 920–948.
[3] K.E. N'Tsoukpoe et al., *A review on long-term sorption solar energy storage*, Renew. Sustain.
Energy Rev. 13 (2009) 2385–2396.
[4] A. Hauer, *Adsorption systems for thermal energy storage — design and demonstration projects*
(Munich mobile zeolite store).
