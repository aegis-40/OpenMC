# Aegis-40 iPWR Detailed Design (Teknofest 2026)
This repository is the working space for the Teknofest 2026 Nuclear Energy Technologies (Detailed Design) submission focused on the **Aegis-40**, a 40 MWe integral Pressurized Water Reactor (iPWR).

## Project focus
- Soluble-boron-free (SBF) core design
- Open-source neutronics and thermal-hydraulics workflow (OpenMC + OpenFOAM)
- Integrated energy applications:
  - Thermochemical Energy Storage (TES) for district heating
  - Solid Oxide Electrolysis (SOE) for off-peak hydrogen production
- Digital Twin–based I&C architecture for predictive monitoring
- Weighted Figure of Merit (wFOM) framework for design optimization
- Integrated 3S (Safety, Security, Safeguards) design basis

> **This repository is the OpenMC / neutronics workstream** of the Aegis-40
> project (the `[NEU]` part): core design, depletion, and the depletion-driven
> back-end fuel-cycle / waste analysis. Thermal-hydraulics, systems, and the
> other disciplines live in their own organization repos.

## Repository layout
- `openmc_model/` — the full-core OpenMC notebook + curated results & sample input decks
- `src/aegis40/back_end/` — back-end fuel-cycle / waste analysis package (fuel cycle,
  source term, classification, and the OpenMC bridge)
- `scripts/` — WSL driver scripts (discharge-inventory extraction, decay-heat run)
- `docs/competition/` — FER preparation: locked design basis, §4.3.2 waste
  requirements, reference-reactor comparison, waste source-term reports
- `tests/` — automated tests for the back-end package

## Quick start
1. Create a Python virtual environment.
2. Install dev dependencies:
   `pip install -e .[dev]`
3. Run tests:
   `python -m pytest`

## Near-term milestones
1. Define baseline reactor constraints and assumptions.
2. Stand up first OpenMC reference model and input deck conventions.
3. Define OpenFOAM coupling assumptions and data exchange format.
4. Draft first-pass wFOM category set and weights.
