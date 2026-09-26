---
doc_id: CSH-DDR-002
title: CoolShade recommendations accepted
project: CoolShade
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); record every newly decided item, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Amish wrote, in chat on 2026-09-25: "i accept all your recommendations, go with them across all repos."

## Context

After the TRL 3 session, `docs/REVIEW.md` and CSH-DDR-001 listed seven design choices adopted for TRL 3 and open for Amish's review (D1 to D7), the budget (O1), the first site and partner (O2), and three new items raised by the TRL 3 calculations (R10 wind with the fabric fitted, R4 air cooling and fans, R8 energy margin). Every item with a recommendation is now decided as recommended. Where several options were offered, the recommended option is the decision. Items without a recommendation stay open. TRL 4 stays on hold.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in CSH-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Misting pressure class | Low pressure, about 7 bar, 12 V, off-grid | Status only; design already used it |
| D2 | Activation thresholds | Fixed: 32 °C or more, 60 % RH or less, presence in the last 2 min, tank above low level | Status only (CSH-REQ-001 R6, CSH-PRC-001) |
| D3 | Fans | None; confirmed by the R4 decision below | Status only |
| D4 | Water supply | Tank as standard; mains with float valve and backflow preventer optional where rules allow | Status only |
| D5 | Canopy size and structure | 3.0 x 2.4 m, four 80 x 80 x 3 mm posts with knee braces, bolted to an existing slab | Status only |
| D6 | Storm practice | Removable fabric | Now tied to the restated R10 below |
| D7 | Status link | None for the first prototype | Status only |
| O1 | Budget | Option (a) of the TRL 3 review: `budget_usd` $775 (supersedes the TRL 2 recommendation of $750) | `project.yaml` `budget_usd` 700 to 775; README, CSH-PRB-001, CSH-REQ-001 R13, CSH-PRC-001, CSH-CAL-001 section J, BOM notes, concept sheet |
| N1 | R10 fabric-on wind case | Option (a): restate R10 as "frame and anchors survive 30 m/s with the fabric removed; fabric fitted only in forecast gusts below 15 m/s (54 km/h)" | CSH-REQ-001 R10 restated; CSH-CAL-001 new lines G13 (fabric off, 30 m/s: posts 0.14, purlins 0.15, anchors about 2.8 kN) and G14 (fabric on, 15 m/s: long beams 0.88); R10 moves from not met to met on paper; GA drawing notes; BOM line 3 note; safety text |
| N1c | Load-release cord lacing | Option (c), to be studied at TRL 4 | Decided but on hold: TRL 4 is on hold by Amish's instruction. Nothing built or tested |
| N2 | R4 and fans | Option (a): relax R4 to "2 °C while spraying"; no fans | CSH-REQ-001 R4 restated; CSH-CAL-001 E3 (2.71 °C while spraying at 1 m/s, held to 1.35 m/s); R4 moves from not met to met |
| N3 | R8 energy margin | Option (a): 25 Ah battery instead of 20 Ah; keep the fail-safe normally open drain valve | BOM line 6: 12.8 V 25 Ah, $85 to $100; `cad/src/model.py` battery 80 to 100 mm wide; STEP and STL re-exported; CSH-CAL-001 F2 (1.005 to 1.256 design days); R8 moves from at risk to met; GA drawing CSH-DWG-001 Rev P1 to P2; media re-rendered |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O2 | First site type (bus stop, market or queue) and co-design partner. No recommendation was made. | Proposed, awaiting Amish |

The suggestion in the TRL 3 review (a continuous spray at half the flow instead of 20 s pulses) was listed as a suggestion only, not a recommendation on a decision item, so it is not applied.

## Consequences

- Parts cost: $758.00 to $773.00, against the new $775 budget, $2.00 (0.3 %) under. R13 moves from not met to at risk, because the steel prices look low until quoted.
- Requirement status (CSH-CAL-001 v0.2): none not met (was 3: R4, R10, R13); 3 at risk (R9, R13, R16; was R8, R9, R16); 1 not verifiable at TRL 3 (R5); 13 met (was 10).
- Documents bumped: CSH-PRB-001 v0.4, CSH-PRC-001 v0.4, CSH-REQ-001 v0.4, CSH-CAL-001 v0.2, CSH-DDR-001 v0.2, drawing CSH-DWG-001 Rev P2. No pitch or problem rewording was recommended, so `project.yaml` pitch and problem are unchanged.
- Cross-repo actions: none. No FieldNode link is fitted (D7), so CoolShade places no demand on another repo.
- `trl: 3` and `trl_target: 3` are unchanged. TRL 4 is on hold by Amish's instruction; nothing in this record authorizes building, testing, purchasing, PCB or firmware work.
