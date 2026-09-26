---
doc_id: CSH-DDR-001
title: CoolShade TRL 2 review decisions
project: CoolShade
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted. On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Items D1 to D7 are "Decided by Amish, 2026-09-25: go with recommendation". O1 (budget) is decided at the latest recommendation, $775 (see CSH-DDR-002). O2 has no recommendation and remains "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", eight of them with a recommendation, and the design precis CSH-PRC-001 v0.2 listed six key design choices, all proposed. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CoolShade items one by one. Under that instruction, every item with a recommendation is adopted as recommended so that TRL 3 work can proceed, and each stays open for his review. Items without a recommendation stay open. A recommended budget change is not applied to `project.yaml`; it is recorded here as awaiting Amish.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CSH-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items decided.*

| # | Item | Recommendation | Status |
| --- | --- | --- | --- |
| D1 | Misting pressure class | Low pressure, about 7 bar, 12 V, off-grid; droplet size and wetting are the first things to check | Decided by Amish, 2026-09-25: go with recommendation |
| D2 | Activation thresholds | Fixed thresholds: 32 °C or more, 60 % relative humidity or less, presence in the last 2 min, tank above its low level | Decided by Amish, 2026-09-25: go with recommendation |
| D3 | Fans | None at TRL 3; revisit because R4 remains unmet (see `docs/REVIEW.md`) | Decided by Amish, 2026-09-25: go with recommendation |
| D4 | Water supply | Tank as standard; mains connection with a float valve and backflow preventer optional where local rules allow | Decided by Amish, 2026-09-25: go with recommendation |
| D5 | Canopy size and structure | 3.0 x 2.4 m, four 80 x 80 x 3 mm posts with knee braces, bolted to an existing slab; checked by calculation in CSH-CAL-001 | Decided by Amish, 2026-09-25: go with recommendation |
| D6 | Storm practice | Removable fabric, taken off before forecast storms. CSH-CAL-001 shows this is structurally necessary, not only a convenience | Decided by Amish, 2026-09-25: go with recommendation |
| D7 | Status link | None for the first prototype; no FieldNode link fitted | Decided by Amish, 2026-09-25: go with recommendation |

*Table 2. Items that were open after TRL 3.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Budget. The TRL 2 recommendation was option (a), raise `budget_usd` to $750. Under the batch instruction, budget figures are not changed: `budget_usd` stays at $700 and the $750 figure is recorded here as a recommendation. CSH-CAL-001 v0.1 found a parts cost of $758, over both figures, and the TRL 3 review recommended $775. | Decided by Amish, 2026-09-25: go with recommendation ($775; see CSH-DDR-002) |
| O2 | First site type and co-design partner (bus stop, market or queue). No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields change. `budget_usd` stays at $700. No pitch or problem rewording was recommended, so none is applied.
- CSH-PRB-001, CSH-PRC-001 and CSH-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed"; they are adopted for TRL 3 pending Amish's review. No requirement target changes; the R6 thresholds are now adopted rather than proposed, and R13 is stated against both $700 and the proposed $750.
- The TRL 3 calculations led to four detail changes within these decisions: shorter knee braces (headroom), a vacuum breaker on the mist line (draining past anti-drip nozzles), a closed mist line loop, and a tank strap (an empty tank tips in a 30 m/s gust). They add $23 to the parts cost.
- CSH-CAL-001 finds R4, R10 and R13 not met. New options for R10 (fabric-on wind limit or heavier roof beams) and a revisit of fans for R4 are listed in `docs/REVIEW.md` as proposed, awaiting Amish; this record does not decide them.
- Update, 2026-09-25: Amish accepted all recommendations. D1 to D7 and O1 are decided; the R10, R4 and R8 items and their effects are recorded in CSH-DDR-002. O2 stays open.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building or testing.
