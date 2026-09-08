# Aegis-40 — Project Context & Design Rationale

**A plain-language orientation to what we're building and why.** Read this to understand the project;
use `01_FINAL-NUMBERS.md` for exact values and `02_FER-DOCX-EDITS.md` for the change list.

**Updated:** 2026-08-14

---

## 1. What this project is

**Aegis-40** is our entry to the **TEKNOFEST 2026 Nuclear Technologies (Detailed Design) competition**. The deliverable is a full **Final Engineering Report (FER, "FER Chapter 8")** describing a complete small modular reactor design — core physics, thermal-hydraulics, fuel, safety, control, auxiliaries, energy cycle, layout, waste, and economics — backed by a **digital appendix** of reproducible calculations. We passed the report stage and are now in the **finals: a ~30-minute presentation + ~15-minute jury Q&A**, due in about a week.

The name: *Aegis* (a shield) + *40* (40 MW electric).

## 2. The design in one paragraph

Aegis-40 is a **125 MWth / 40 MWe integral pressurized-water reactor (iPWR)** — a small modular reactor where the steam generator, pressurizer, and control-rod drives all sit **inside one reactor vessel**, so there are no large external pipes to break. It runs on **natural circulation** (heat drives the water loop by itself — **no reactor coolant pumps**), it is **soluble-boron-free** (no boric acid dissolved in the coolant for reactivity control), and it uses a **once-through fuel cycle** (fuel loaded once, burned ~6 years, discharged). Reactivity is held down over life by **burnable poisons** (gadolinium + erbium mixed into the fuel) and controlled by **16 solid control-rod assemblies**; a diverse **Emergency Boron Injection System (EBIS)** provides an independent backup shutdown. Beyond electricity, it does **cogeneration** — district heat via a thermochemical store and **hydrogen** via solid-oxide electrolysis.

## 3. Design philosophy — the "why" behind the choices

Every major choice traces to one of three goals: **inherent safety, simplicity, and proliferation resistance.**

| Choice | Why we made it |
|---|---|
| **Integral (iPWR) layout** | No large-diameter external primary piping → the big loss-of-coolant accident is *designed out*, not just mitigated. |
| **Natural circulation (no pumps)** | Removes the pumps as an accident initiator and a power draw; the core cools itself on physics alone during a station blackout. |
| **Soluble-boron-free (SBF)** | Boric acid causes a *positive* moderator reactivity contribution and needs a whole chemical control system. Removing it gives a strongly **negative moderator coefficient** (safer) and deletes a subsystem (simpler). The hard part it creates — holding down beginning-of-life reactivity without boron — we solve with burnable poisons + rods. |
| **Burnable poisons (Gd + Er)** | Gd gives strong early suppression that burns out; Er is a milder, longer-lasting absorber that flattens the curve and helps keep coefficients negative late in life. Together they replace soluble boron. |
| **16 control-rod assemblies, enriched-B-10** | Deliver a **7.85 % hot shutdown margin** — about 4× the acceptance criterion — so the reactor trips safely hot on rods alone. |
| **EBIS (boron injection) as 2nd shutdown** | Regulations (IAEA SSR-2/1 Req. 46) require **two diverse shutdown systems**. Rods handle hot shutdown; EBIS independently handles cold shutdown (where rods alone are insufficient because cold water is a better moderator). |
| **Once-through fuel cycle** | Simplicity and proliferation resistance — no reprocessing, spent fuel goes to dry storage. We accept lower uranium utilization as a deliberate trade. |
| **Lead-free shielding** | Borated polyethylene + magnetite concrete instead of lead — avoids a toxic heavy metal, easier to license and dispose of. |
| **Cogeneration (heat + H₂)** | A 40 MWe unit is more economic if it also sells district heat and hydrogen; it improves the LCOE story and fits a "energy hub" narrative. |

## 4. Walk-through of the plant

**The core.** 37 fuel assemblies, each a 17×17 array of fuel rods, 2.0 m tall. Fuel is standard UO₂ pellets in Zircaloy-4 cladding, enriched in three radial zones (4.95 / 4.70 / 4.40 wt%, edge 4.0) averaging **4.43 wt%** — below the 5 % commercial ceiling. Selected pins carry gadolinia (Gd₂O₃) and erbia (Er₂O₃) as burnable poison. The core produces **125 MW of heat** and runs a single ~6-year batch to **29.6 GWd/tHM** average burnup.

**The coolant loop.** Water heated in the core rises through a central **riser**, gives up its heat in the **once-through steam generator (OTSG)** near the top of the vessel, and sinks back down the outside — a natural-circulation loop with no pumps. The design riser height (4 m) sets the flow; our tightest thermal margin (**minimum departure-from-nucleate-boiling ratio, MDNBR ≈ 1.33** by the W-3 correlation) lives here — it's the number that says "the fuel never dries out."

**Reactivity & control.** With no soluble boron, reactivity is managed by (a) burnable poisons burning out as fuel depletes, and (b) 16 control-rod assemblies for operational control and fast shutdown. All temperature coefficients are **negative** (moderator −26.9, Doppler −1.9 pcm/°C, void −173 pcm/%) — if the core heats up or voids, reactivity falls automatically. That's *inherent* safety.

**Safety systems.** Fully passive: an in-containment refueling water storage tank (IRWST, 250 m³) and passive heat removal give a **grace period ≥ 240 h** with no operator action and no AC power. The integral layout bounds loss-of-coolant events; core-damage frequency is below 10⁻⁷ per reactor-year. Two diverse shutdown systems (rods + EBIS) satisfy the defense-in-depth requirement.

**Shielding.** A lead-free stack — 20 cm borated polyethylene (moderates/absorbs neutrons) then 180 cm magnetite concrete (stops gammas) — keeps the reactor-vessel fast fluence to **3.0×10¹⁸ n/cm²** over life and contact dose to sub-µSv/h levels.

**Balance of plant.** The OTSG makes **4.5 MPa / 296 °C** steam driving a Rankine turbine for **40 MWe (≈32 % efficiency)**. Waste heat and off-peak electricity feed cogeneration: a **thermochemical energy store (TCES, zeolite-13X)** for district heating and **solid-oxide electrolysis** producing **427 t/yr of hydrogen**.

**Back end.** Spent fuel (once-through) discharges at **4.40 tHM/TWhe** with decay heat manageable for dry-cask storage; discharge plutonium is reactor-grade and the cycle is designed to be proliferation-unattractive.

## 5. The digital toolchain (our technical differentiator)

- **OpenMC 0.15.3** (Monte-Carlo neutron transport + depletion, ENDF/B-VIII.0 data) is the physics engine behind every neutronics number. Our converged "STAT_FINAL" runs are the authoritative source.
- A **digital twin** — a Gaussian-Process + POD (reduced-order) surrogate trained on a Latin-hypercube sweep of OpenMC runs — predicts k-effective, assembly power maps, and reactivity coefficients **instantly**, with a **Streamlit dashboard** for live "what-if" demonstration. (k-eff and power-map surrogates are excellent, R² ≈ 0.99; the sweep-based coefficients are indicative — a fresh 16-CRA sweep will tighten them.)
- The **digital appendix** packages everything reproducibly: 12 folders (0–11), each with code + inputs + outputs + figures + a README, plus a `REPRODUCE.md`, pinned `requirements.txt`, and SHA-256 checksums so a juror can re-run it.

## 6. How our documents fit together

| Document | What it is | Where |
|---|---|---|
| **FER Chapter 8** (`.docx`) | The formal report (sections 8.1–8.12) — the graded deliverable | `docs/competition/fer/` + Word |
| **Digital appendix** (ZIP) | Reproducible calc package, folders 0–11 (DA-0…DA-11) | `docs/competition/digital-appendix/` |
| **Final presentation** (`.pptx`) | The finals deck (30 min) | `Aegis40_Final_Presentation_v1.pptx` |
| **This `team-sync/` folder** | The master reference we all sync to | `docs/competition/team-sync/` |

Appendix folder map: 0 overview · 1 core transport · 2 depletion · 3 kinetics/coefficients · **4 safety neutronics (rods/SDM)** · **5 digital twin** · 6 fuel performance · **7 energy cycle/economics** · **8 thermal-hydraulics** · 9 waste/back-end · **10 shielding** · **11 CAD drawings**.

## 7. Acronym cheat-sheet
**iPWR** integral pressurized-water reactor · **SBF** soluble-boron-free · **SMR** small modular reactor · **FER** Final Engineering Report · **CRA/CRDM** control-rod assembly / drive mechanism · **EBIS** emergency boron injection system · **SDM** shutdown margin · **MTC/DTC** moderator/Doppler temperature coefficient · **pcm** per-cent-mille (10⁻⁵ Δk/k, a reactivity unit) · **MDNBR** minimum departure-from-nucleate-boiling ratio · **OTSG** once-through steam generator · **IRWST** in-containment refueling water storage tank · **LHR** linear heat rate · **F_ΔH / F_q** enthalpy-rise / heat-flux peaking factors · **COLR** core operating limits report · **BOC/MOC/EOC** beginning/middle/end of cycle · **GWd/tHM** gigawatt-days per tonne heavy metal (burnup) · **EFPD/FPY** effective full-power days/years · **LCOE** levelized cost of electricity · **NOAK/FOAK** n-th / first of a kind · **TCES** thermochemical energy storage · **SOE** solid-oxide electrolysis · **CDF/LRF** core-damage / large-release frequency.

## 8. Design-decision log (for Q&A defense)
The choices most likely to be probed, and our one-line answers:

- **Why once-through, not a breeder/recycle?** Simplicity + proliferation resistance; we accept lower U utilization deliberately. (💡 a paper multi-batch estimate would strengthen this.)
- **Why soluble-boron-free?** Strong negative moderator coefficient and one fewer chemical system; the reactivity-hold challenge is solved with Gd+Er + 16 rods.
- **Why only 4 m riser (tight MDNBR 1.37)?** Vessel-height economy; still above the 1.30 acceptance limit with the AOO transient at 1.57.
- **Is 7.85 % hot shutdown margin real?** Yes — 16 enriched-B-10 CRAs, N5C case; ~4× the criterion. Cold shutdown is separately covered by EBIS.
- **W-3 is an old DNB correlation — why trust it?** It's conservative; a modern-correlation cross-check is planned. (💡 do it if time.)
- **Lead-free shielding — does it really work?** Point-kernel dose passes; a converged Monte-Carlo confirmation is the next credibility step.
