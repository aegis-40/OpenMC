# Reference reactors & method precedents (FER §3 lit review + §8.11/§8.2)

Sourced from `D:\projects\literature`. These anchor our design choices to published
work so we cite precedent instead of inventing — the cheapest way to de-risk the FER.

## Design comparison

| Parameter | **Aegis-40 (ours, rev_3)** | CAREM-25 | Jang SBF-SMPWR (2020) | IAEA iPWR sim (NuScale-like) |
|---|---|---|---|---|
| Thermal power | 125 MWth | 100 MWth | 180 MWth | 150 MWth |
| Electric | 40 MWe | 32 MWe | — | ~50 MWe |
| Lattice | square 17×17 | **hexagonal** | square 17×17 | square 17×17 |
| Assemblies | 21 | 61 (hex) | 37 | 24 |
| Active height | 200 cm | — | 200 cm | 135 cm |
| Enrichment | 4.95 / 4.70 / 4.40 wt% | 1.8 & 3.1 wt% | (multi) | 4.95 wt% |
| Soluble boron | **NONE (SBF)** | **NONE (boron-free)** | **NONE (SBF)** | uses boron |
| Burnable absorber | Gd 8 wt% + Er 0.5 wt% | **Gd 8 wt%** (Gd₂O₃, only) | Gd 2&8 wt% IBA + Gd R-BA + B WABA | — |
| Reactivity control | rods + integral BA | rods + Gd | **rods + 3 BA types** | rods + boron |
| Cycle length | ~500 EFPD (~16-18 mo) | 14 months | **1555 EFPD (~51 mo!)** | — |
| Discharge burnup | ~46 GWd/t (target) | lower (~24 GWd/t, lit.) | (ultra-long) | — |

**Read-out:** CAREM is the *named* SBF small-iPWR twin (use for the headline waste/efficiency
comparison), but it is hexagonal, low-enrichment, Gd-only, lower burnup. **Jang is the closer
*methodological* twin** — square 17×17, 200 cm, SBF, **8 wt% Gd (same as us)** — and is the right
citation for "SBF via integral BA + control rods." We sit *between* CAREM (simplest) and Jang
(most complex): two BA types (Gd+Er) and a moderate ~17-mo cycle, vs. CAREM's one BA / 14 mo
and Jang's three BA / 51 mo.

## Why NOT simplify the design down to CAREM
The competition scores **fuel efficiency = high burnup + minimized waste per unit energy**, and
waste intensity is locked to `1/(burnup×efficiency)`. Dropping to CAREM-like ~3.1% / ~24 GWd/t
would *roughly double* tHM/TWhe and directly **lose** the fuel-efficiency/waste score. The
high-burnup choice is what makes the waste story competitive. Keep it; simplify *methodology*,
not the design point. (Dropping Er, however, is the one real simplification lever — see below.)

## The Er question (our one genuine "simpler" option)
CAREM proves **Gd-only** works boron-free — but at low burnup where the reactivity hump is small.
We added Er precisely because pushing to 4.95% / long cycle reintroduced the mid-cycle Gd-burnout
hump. So: Gd-only is simpler and CAREM-backed, but only viable if we accept lower enrichment /
shorter cycle. Er is the price of high burnup in an SBF core. Decision stays with the burnup target.

## Peaking — reframed (good news)
Jang's SBF-SMPWR design limit is a **3D power peaking factor < 5.09** (their core is low
power-density with large DNBR margin). Our rev_2 F_q ≈ 3.6 sits comfortably inside that class.
**Peaking is a margin/optimization issue for us, not a failure** — the radial-zoning work lowers
it further, but we are not in violation of SBF-SMR precedent. (The binding limit is still our own
DNBR analysis — Adilbek's T-H — not a borrowed number.)

## Method precedent for §8.11 storage criticality — Cabrera (2023)
"Criticality calculation with burnup credit of a PWR spent fuel pool" gives us the recipe:
- Deplete fuel → build storage-rack model → compute k_eff. (They use SCALE POLARIS+KENO-VI +
  ORIGEN; **we replicate with OpenMC** — our `openmc_bridge.build_storage_rack_model`.)
- **Acceptance criterion: k_eff(95/95) ≤ 0.95** with racks flooded with *unborated* water at the
  maximum-reactivity assembly, at 95% probability / 95% confidence. (For SBF this is natural —
  we have no boron to credit anyway, so the unborated case IS our operating case.)
- Burnup credit = credit selected actinides + fission products; axial burnup distribution matters.

This is the authoritative template for our storage-criticality deliverable. Also relevant:
`gadolinia burnable absorbers.pdf` (Gd BA modeling), `NuScale-Like SMR Benchmark.pdf` and
`Depletion capabilities.pdf` / `OpenMC.pdf` (code V&V for the Digital Appendix).
