---
doc_id: CSH-DEC-001
title: CoolShade design decisions register
project: CoolShade
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the decision records, the review note and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for both open decisions; moved to decisions made; To confirm item 10 updated for the market lane"
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Design for construction (CSH-DDR-003, P1 to P16) accepted by Amish on 2026-10-02; moved from open for review to decisions made"
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "To confirm item 11 carries the market lane: health authority and responsible person named by role"
---

# CoolShade design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, CSH-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 1. Items to check against the real parts and site before or while buying.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Nozzle flow (4 L/h each assumed) and droplet spectrum (Dv0.9 below about 80 µm) at 7 bar, from the nozzle maker | Water use (R7) and wetting (R5) depend on them | CSH-CAL-001 [C1], [D3] |
| 2 | The anchor type, its design resistance and the slab at the site: about 2.8 kN factored per anchor with the fabric off at 30 m/s | The anchors and slab hold the canopy down | CSH-CAL-001 [G13] |
| 3 | Steel quotes for lines 1, 2 and 4 (about 167 kg, priced at about $1.61/kg) | The cost (R13) may rise | CSH-CAL-001 [J2] |
| 4 | The M8 steel rivet nut's pull-out rating in a 2 mm wall is well above 0.16 kN, and its hole size (11 mm assumed; 7 mm for M5) | Rivet nuts hold the beams to the posts, braces, cleats and L-feet | CSH-DDR-003, P16; CSH-CAL-001 [G15] |
| 5 | The enclosure has moulded mounting holes outside its gasket and internal bosses for a gear plate | The enclosure screws to its rails from inside and stays sealed | CSH-DDR-003, P8 |
| 6 | The pump may be mounted on a vertical plate, and its foot pattern and port positions | The pump, the tee from the down pipe and the hoses are placed on the equipment plate from it | CSH-DDR-003, P11 |
| 7 | The solar mounting kit's L-feet reach the rails 15 mm above the tubes on the 7° slope, and the end clamps suit a 35 mm panel frame | The panel rails stand on L-feet on the bearer and the rear beam | CSH-DDR-003, P7 |
| 8 | The shade cloth maker can make the 1,020 x 670 mm notch with a reinforced hem and eyelets | The cloth comes off without touching the panel | CSH-DDR-003, P7 |
| 9 | The radiation shield has a top plate that takes one M8 bolt (or an adapter plate is made) | The shield hangs under the sensor arm | CSH-DDR-003, P9 |
| 10 | The street-side posts stand 25 mm inside the roof's street edge; check the setback from vehicles, stalls and walkways and the sight lines at the first site (a market lane, decided 2026-10-02) | The posts moved out 125 mm each side to carry the cloth's edges | CSH-DDR-003, P1 |
| 11 | A water hygiene plan for a market lane, acceptable to the environmental health authority of the city or county where the first site stands (named once the site is chosen; the Phoenix area is the first candidate), with the market operator's manager named as the person responsible for the daily drain and refill, the weekly disinfection and the sampling | *Legionella* control (R9) is at risk; no public trial without it | CSH-CAL-001 [I3]; CSH-PRC-001 |
| 12 | Water hardness at the site and a descaling method and interval for the 0.4 mm nozzles | Scaling (R16) is at risk | CSH-REQ-001 R16 |
| 13 | Fabric porosity and stretch, which set the fabric's edge pull | The 15 m/s fabric-on limit is set on the conservative solid-fabric case | CSH-CAL-001 [G7], [G8] |

## Value engineering

Value-engineering target: USD 775 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 882 (USD 107, or 13.8 %, over the target). The concept came to USD 773, USD 2 under the target; the parts added to make it buildable add USD 109.

- **Main cost drivers:** the steel lines (1, 2 and 4), USD 269 for about 167 kg (about USD 1.61 per kg including cutting, drilling and galvanizing); the parts added for construction (cleats, rivet nuts, panel bearer and mounting kit, base cleats, equipment plate, enclosure rails, sensor arm, line clips, tank level switch, I2C extender, cloth notch and more fixings)(see `bom/bom.csv`).
- **Savings worth trying:** leave out the base plates (the cleats anchor straight to the slab) and make the panel rails from steel angle, which saves about USD 40; and get steel quotes, since the steel prices look low for small quantities and the real cost may be higher.

## Decisions made

*Table 2. Decisions made, newest last.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D7: low-pressure 7 bar misting; fixed thresholds (32 °C or more, 60 % RH or less, presence in the last 2 min, tank above its low level); no fans; tank as standard with mains optional; 3.0 x 2.4 m bolted four-post canopy on an existing slab; removable fabric before storms; no status link | Amish: "i accept all your recommendations, go with them across all repos." | CSH-DDR-001, CSH-DDR-002 |
| 2026-09-25 | Budget $775 (was $700) | Amish, same instruction | CSH-DDR-002, O1 |
| 2026-09-25 | R10 restated: frame and anchors survive 30 m/s with the fabric removed; fabric fitted only in forecast gusts below 15 m/s (54 km/h) | Amish, same instruction | CSH-DDR-002, N1 |
| 2026-09-25 | Load-release cord lacing to be studied at TRL 4 (on hold with TRL 4) | Amish, same instruction | CSH-DDR-002, N1c |
| 2026-09-25 | R4 restated as 2 °C while spraying; no fans | Amish, same instruction | CSH-DDR-002, N2 |
| 2026-09-25 | 25 Ah battery in place of 20 Ah; keep the fail-safe normally open drain valve | Amish, same instruction | CSH-DDR-002, N3 |
| 2026-09-30 | Design for construction: posts on a 2,800 x 2,350 mm grid with the long beams on their tops, angle cleats and rivet nuts at every roof joint, bolted post bases, flattened-end knee braces, panel at the rear edge on a bearer and L-feet with a notch in the cloth, equipment plate, enclosure rails, angle sensor arm, tank stop cleats, tank level switch and other changes (P1 to P16) | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."); the changes themselves were accepted on 2026-10-02 (below) | CSH-DDR-003 |
| 2026-10-02 | R14's tool list gains a hand rivet nut tool and a bench vice (option a); the rivet nuts are kept (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | CSH-DDR-003, A2 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P16 and their knock-on changes, as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [CSH-DDR-003](decisions/0003-design-for-construction.md), Tables 1 and 2 |
| 2026-10-02 | First site type a market lane, with the market operator as co-design partner, in a hot, dry city; first candidate to approach a farmers' market operator in the Phoenix area, with Arizona State University's urban heat researchers as the candidate measurement partner (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | CSH-DDR-001, O2; CSH-DDR-002 |
