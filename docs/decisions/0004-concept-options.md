---
doc_id: CSH-DDR-004
title: CoolShade concept options
project: CoolShade
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-30'
  author: Amish Chadha
  change: Concept options compared in the kit 1.9.1 upgrade (CSH-OPT-001); the choice is proposed, awaiting Amish
---

# 0004: Concept options

- **Date:** 2026-10-30
- **Status:** proposed, awaiting Amish. Nothing in this record is decided.

## Context

Kit 1.8 asks every design to compare at least two working principles before it commits (STANDARDS section 21). CoolShade was designed at kit 1.7 as a solar misting shade canopy; in this record that design is option A and it does not change. Two further options with different working principles were added and all three were modelled to detail level D3 ("Detail every option", Amish, 2026-10-24). The options, their numbers and the scoring are in CSH-OPT-001; their STEM screens are in CSH-STM-001 (S22 to S26).

## Options considered

1. **Option A, solar misting shade canopy.** Score 134 of 190. The current design: 7 bar mist from eight anti-drip nozzles, switched on heat, humidity and presence; 2.7 °C cooling while spraying for a group. Open: wetting (S4), *Legionella* (S14), cost USD 882 against USD 775.
2. **Option B, wet-pad fan cooler under shade.** Score 135. Direct evaporative cooling through a cellulose pad and a 12 V fan, once-through water, no free aerosol. It reaches one or two people (about 1.5 kW), has a welded cabinet and uses about 2.2 L/h.
3. **Option C, passive double-skin reflective roof.** Score 159. A white composite skin 100 mm above the cloth; no water, no power, no moving parts. It cools no air (UR-002 scores 1), so it is a better shade, not a cooling product, and the skin cannot come off before a gust.

## Decision

**Proposed, awaiting Amish.** Options A and B are within 10 % of each other, so both go to Amish. Option C scores highest, but it fails a High need, so the score does not make it the pick.

Recommendation: keep **option A** as the design, consider **option C's white skin as an add-on to A** (to assess; not modelled or priced), and keep **option B as the fallback** if the droplets are too big or the hygiene plan fails. `concept_chosen` is "A (proposed)" in `project.yaml`.

## Consequences

- If Amish confirms A: no design change; the precis, requirements, calculation note, drawing, BOM and build plan already describe A.
- If Amish chooses B or C: the PRS, CAL, BOM, drawing and build plan would be redone for that option; their D3 models exist (`cad/src/csh_options.py`) but have no priced BOM, drawing or build plan.
- If Amish asks for the hybrid: the roof would carry both the removable cloth and a fixed skin, and the wind case (cloth off above 15 m/s, S17) would be redone.
