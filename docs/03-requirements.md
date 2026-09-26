---
doc_id: CSH-REQ-001
title: CoolShade requirements
project: CoolShade
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
---

# CoolShade requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see CSH-PRB-001). Two requirements are not met by the current concept (R13 cost and, in some conditions, R4 cooling), and three are at risk (R5 wetting, R9 water hygiene, R16 scaling).

**Design day:** 38 °C air, 25 % relative humidity, clear sky, wind about 1 m/s, 5 h of misting demand, 4.5 peak sun hours. **Humid check:** 35 °C and 60 % relative humidity.

Table 1. Requirements, targets and status of the TRL 2 concept (status values are estimates).

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Shaded waiting area | 6 m² or more of shade at solar noon; room for at least 6 people standing or seated and one wheelchair space of 0.8 x 1.2 m | Plan layout; sun path check per site | Met by design: 7.2 m² roof |
| R2 | Headroom | Clear height 2.2 m or more under any part of the frame, nozzle or brace in the waiting area | Model check | Met by design: about 2.1 m under knee braces at the rear posts, which sit outside the main waiting area; about 2.5 m or more elsewhere. Brace position to confirm |
| R3 | Radiant heat reduction | Mean radiant temperature under the canopy at least 15 °C below full sun at midday on the design day | Literature comparison; later field measurement with a globe thermometer (HeatMap Node method) | Expected met: about 17.3 °C measured for shade sails in Tempe ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)); unverified for this design |
| R4 | Air cooling from misting | Air temperature in the waiting zone (0.5 to 2.0 m height) at least 2 °C below ambient during misting on the design day | Energy balance at TRL 3; later field test | **Not met at 1 m/s wind:** about 1.4 °C averaged over the duty cycle, about 2.7 °C while spraying (estimate). Met in calmer air |
| R5 | No wetting | No perceptible wetting of skin or clothing at 1.5 m height on the design day; no puddles on the waiting area | Droplet size data from nozzle maker; later field test | **At risk:** low-pressure nozzles make larger droplets than high-pressure systems |
| R6 | Smart activation | Mists only when air temperature is 32 °C or more, relative humidity is 60 % or less, presence is detected in the last 2 min and the tank is above its low level; stops within 60 s when any condition fails | Control logic review; later bench test | Met by design (thresholds proposed, awaiting Amish) |
| R7 | Water use | 100 L or less per design day | Nozzle flow calculation | Met: about 85 L per design day (estimate) |
| R8 | Energy autonomy | Energy-neutral on the design day from the onboard panel; battery covers one full design day with no sun | Energy budget | Met: about 205 Wh per day used against about 340 Wh harvested; about 205 Wh usable storage (estimates) |
| R9 | Water hygiene | Potable-quality supply water; 5 µm filtration; mist line drained within 5 min after every session; water in the tank 48 h old or less; opaque, shaded, lockable tank; documented weekly disinfection | Design review; later microbiological sampling with a partner lab | **At risk:** stored water on hot days will sit in the 20 to 50 °C range in which *Legionella* grows ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)); relies on turnover, draining and disinfection |
| R10 | Wind resistance | Frame and anchors survive a 3 s gust of 30 m/s (108 km/h) with the fabric fitted; fabric removable in 15 min or less before forecast storms | Structural calculation at TRL 3 | Unverified: first estimate about 144 MPa bending stress in each post as a cantilever, before the benefit of knee braces |
| R11 | Privacy | No camera or microphone; presence by passive infrared only; if a status link is fitted, only counts and levels (on-time, water used, temperature, humidity, faults) leave the device | Design review | Met by design |
| R12 | Electrical safety | 12 V DC only, no mains; battery fused at the terminal; all electronics in a lockable IP65 enclosure; LiFePO4 chemistry with BMS and cold-charge cutoff | Design review | Met by design |
| R13 | Cost | Parts for one prototype $700 or less | BOM | **Not met:** about $735 (indicative), about 5 % over |
| R14 | Buildability | Bolted assembly; no welding; built with a drill, angle grinder, spanners and a ladder by two people in 2 days or less | Assembly review | Met by design; build time unverified |
| R15 | Refill interval | 1 design day or more between tank refills | Water balance | Met: 120 L tank covers about 1.4 design days (estimate) |
| R16 | Maintenance | Nozzles cleanable or replaceable without tools in 15 min or less; filter changed in 10 min or less; descaling interval 1 month or longer | Design review; later field log | **At risk** in hard-water areas: scale can block 0.4 mm orifices |
| R17 | Movability | Can be unbolted and moved to another site by two people in 1 day or less; no part heavier than 40 kg to lift (tank empty) | Mass estimate | Met: heaviest part a post of about 20 kg (estimate) |

## Assumptions

- Nozzle flow about 4 L/h each at about 7 bar, eight nozzles, 50 % spray duty cycle while active. To be checked against nozzle datasheets.
- About 87 % of the sprayed water evaporates in the air; the rest drifts away, drips or wets surfaces (estimate).
- Cooling is estimated over a control volume 3.0 m long and 2.0 m high with air crossing it at the wind speed. Real mixing is less even than this.
- Panel output 100 W x 4.5 peak sun hours x 0.75 system factor.
