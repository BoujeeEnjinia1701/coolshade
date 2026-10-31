---
doc_id: CSH-PRS-001
title: CoolShade product requirements and specifications
project: CoolShade
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold, as CSH-REQ-001 (requirements R1 to R17)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CSH-CAL-001 for every requirement; R6 thresholds adopted under CSH-DDR-001; R13 stated against $700 and the proposed $750
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Status from CSH-CAL-001 v0.3 for the constructable design (CSH-DDR-003); R13 not met against $775, new budget proposed
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R14 tool list adds a hand rivet nut tool and a bench vice, decided by Amish on 2026-10-02"
- version: "0.8"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: requirements renumbered PR-001 to PR-017 (the Was column keeps R1 to R17), each traced to a user requirement in CSH-URS-001; document is now the PRS (was CSH-REQ-001); R8 status updated for the white enclosure (CSH-DEC-001 D9); no target changed"
---

# CoolShade product requirements and specifications

What the canopy must do, each requirement traced to a user need in CSH-URS-001 (links in CSH-RTM-001). The requirements describe option A, the solar misting shade canopy, which is the current design; the concept options and the proposed choice are in CSH-OPT-001. The document was CSH-REQ-001 (requirements R1 to R17) before the kit 1.9.1 upgrade of 2026-10-30; the numbers are the same (PR-001 is R1) and the Was column keeps the old number. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (CSH-PRB-001). Status comes from the TRL 3 calculations in CSH-CAL-001 v0.6 for the constructable design of CSH-DDR-003: **13 of the 17 are met on paper or by design; PR-013 (cost) is over its value-engineering target (USD 882 against USD 775), PR-009 (water hygiene) and PR-016 (maintenance) are at risk, and PR-005 (no wetting) cannot be judged at TRL 3 for lack of droplet data.** Four of the 13 are met by design only (PR-006, PR-011, PR-012, PR-014) and PR-010 is met on paper.

**Design day:** 38 °C air, 25 % relative humidity, clear sky, wind about 1 m/s, 5 h of misting demand, 4.5 peak sun hours. **Humid edge:** 32 °C and 60 % relative humidity, the wettest air in which the controller still mists.

*Table 1. Product requirements and specifications. Status after the TRL 3 calculations (CSH-CAL-001 v0.6, python docs/04-calcs/sizing.py; tags in brackets are lines of its output).*

| ID | Traces to | Category | Title | Requirement | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-004 | Performance | Shaded waiting area | 6 m² or more of shade at solar noon; room for at least 6 people standing or seated and one wheelchair space of 0.8 x 1.2 m | Plan layout; sun path check per site | Met: shadow 6.30 m² or more at any sun elevation of 45° or more; room for 8 standing, 3 seated and a wheelchair [A2, A3]. Where the shadow falls depends on the site | R1 |
| PR-002 | UR-004 | Physical architecture | Headroom | Clear height 2.2 m or more under any part of the frame, nozzle or brace in the waiting area | Model check | Met: 2,223 mm under the flattened ends of the rear knee braces; nozzle tips 2,559 mm or higher [B2, B3] | R2 |
| PR-003 | UR-001 | Performance | Radiant heat reduction | Mean radiant temperature under the canopy at least 15 °C below full sun at midday on the design day | Literature comparison; later field measurement with a globe thermometer (HeatMap Node method) | Met on published evidence: about 17.3 °C for shade sails in Tempe ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)); unverified for this fabric | R3 |
| PR-004 | UR-002 | Performance | Air cooling from misting | Air temperature in the waiting zone (0.5 to 2.0 m height) at least 2 °C below ambient while spraying on the design day (restated, CSH-DDR-002; was averaged over the spray cycle) | Energy balance at TRL 3; later field test | Met: 2.71 °C while spraying at 1 m/s, held to 1.35 m/s; 1.35 °C averaged over the cycle [E2, E3] | R4 |
| PR-005 | UR-003 | Performance | No wetting | No perceptible wetting of skin or clothing at 1.5 m height on the design day; no puddles on the waiting area | Droplet size data from nozzle maker; later field test | Not verifiable at TRL 3: met only if the nozzle's Dv0.9 is below about 80 µm at 7 bar; no droplet data yet [D3] | R5 |
| PR-006 | UR-005, UR-003 | Performance | Smart activation | Mists only when air temperature is 32 °C or more, relative humidity is 60 % or less, presence is detected in the last 2 min and the tank is above its low level; stops within 60 s when any condition fails | Control logic review; later bench test | Met by design: stops within 30 s [I1]; thresholds decided (CSH-DDR-001, D2) | R6 |
| PR-007 | UR-015 | Performance | Water use | 100 L or less per design day | Nozzle flow calculation | Met: 85 L used, 95 L drawn with the drain-and-refill routine [C2, C5]; holds up to 4.75 L/h per nozzle [C3] | R7 |
| PR-008 | UR-006 | Performance | Energy autonomy | Energy-neutral on the design day from the onboard panel; battery covers one full design day with no sun | Energy budget | Met: 203.8 Wh used against 337.5 Wh harvested; 25 Ah battery (CSH-DDR-002; was 20 Ah, 1.005 days) covers 1.256 design days; with the white enclosure (CSH-DEC-001 D9) no charging in air above about 42.7 °C [F2, F5] | R8 |
| PR-009 | UR-007 | Safety | Water hygiene | Potable-quality supply water; 5 µm filtration; mist line drained within 5 min after every session; water in the tank 48 h old or less; opaque, shaded, lockable tank; documented weekly disinfection | Design review; later microbiological sampling with a partner lab | **At risk:** line drains in about 30 s with the vacuum breaker and water stays under 24 h old with the routine [C5, C7], but tank water sits at about 34 °C, in the 20 to 50 °C *Legionella* growth range ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)) [I3] | R9 |
| PR-010 | UR-008 | Safety | Wind resistance | Frame and anchors survive a 3 s gust of 30 m/s (108 km/h) with the fabric removed; fabric fitted only when forecast gusts are below 15 m/s (54 km/h); fabric removable in 15 min or less (restated, CSH-DDR-002; was 30 m/s with the fabric fitted) | Structural calculation at TRL 3 | Met on paper: fabric off at 30 m/s, posts 0.14, panel bearer 0.02 and purlins 0.07 utilization [G13]; fabric on at 15 m/s, long beams 0.88 [G14]; anchors need about 2.8 kN each, to be confirmed per site. The original case gives 3.52 on the beams [G7] | R10 |
| PR-011 | UR-010 | Safety | Privacy | No camera or microphone; presence by passive infrared only; if a status link is fitted, only counts and levels (on-time, water used, temperature, humidity, faults) leave the device | Design review | Met by design; no status link fitted (CSH-DDR-001, D7) | R11 |
| PR-012 | UR-009, UR-006 | Electrical | Electrical safety | 12 V DC only, no mains; battery fused at the terminal; all electronics in a lockable IP65 enclosure; LiFePO4 chemistry with BMS and cold-charge cutoff | Design review | Met by design: 15 A terminal fuse, margin 2.0 on the largest current [I2] | R12 |
| PR-013 | UR-014 | Cost | Cost | Estimated parts cost for one prototype within the $775 value-engineering target (`budget_usd`, a hypothetical control target set under CSH-DDR-002; was $700) | BOM | **Over the value-engineering target by $107:** estimated $882, 13.8 % over, after the parts added to make the design buildable (CSH-DDR-003); savings worth trying are in CSH-DEC-001 [J1, J2] | R13 |
| PR-014 | UR-012 | Physical architecture | Buildability | Bolted assembly; no welding; built with a drill, angle grinder, spanners, a hand rivet nut tool, a bench vice and a ladder by two people in 2 days or less | Assembly review | Met by design: 79 bolts and anchors, 36 of them into rivet nuts, no welds [H2]; the hand rivet nut tool and bench vice were added to the tool list by Amish on 2026-10-02 (CSH-DEC-001); build time unverified | R14 |
| PR-015 | UR-011, UR-015 | Usability | Refill interval | 1 design day or more between tank refills | Water balance | Met: 1.41 design days per full tank [C4] | R15 |
| PR-016 | UR-011 | Usability | Maintenance | Nozzles cleanable or replaceable without tools in 15 min or less; filter changed in 10 min or less; descaling interval 1 month or longer | Design review; later field log | **At risk** in hard-water areas: scale can block 0.4 mm orifices; not verifiable at TRL 3 | R16 |
| PR-017 | UR-013 | Packaging and transport | Movability | Can be unbolted and moved to another site by two people in 1 day or less; no part heavier than 40 kg to lift (tank empty) | Mass estimate | Met: heaviest part a front post, 21.0 kg [H1] | R17 |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software, cost. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Nozzle flow 4 L/h each at 7 bar, eight nozzles, 50 % spray duty cycle while active; this implies a discharge coefficient of 0.24 for a 0.4 mm orifice, to be checked against nozzle datasheets.
- About 87 % of the sprayed water evaporates in the air; the rest drifts away, drips or wets surfaces (estimate).
- Cooling is estimated over a control volume 3.0 m long and 2.0 m high with air crossing it at the wind speed. Real mixing is less even than this.
- Panel output 100 W x 4.5 peak sun hours x 0.75 system factor; battery 12.8 V 25 Ah, 80 % usable; enclosure white or light grey (solar absorptance 0.25, CSH-DEC-001 D9).
- Wind: fabric treated as solid with 5 % sag, net normal force coefficient 1.2, S275 steel with a 1.5 factor on wind. All other assumptions are listed in CSH-CAL-001, Table 1.
