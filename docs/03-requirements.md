---
doc_id: CSH-REQ-001
title: CoolShade requirements
project: CoolShade
doc_type: Requirements
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CSH-CAL-001 for every requirement; R6 thresholds adopted under CSH-DDR-001; R13 stated against $700 and the proposed $750
---

# CoolShade requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (see CSH-PRB-001). The status column now comes from the TRL 3 calculations in CSH-CAL-001: three requirements are not met (R4 air cooling at 1 m/s, R10 wind with the fabric fitted, R13 cost), three are at risk (R8 energy margin, R9 water hygiene, R16 scaling), one cannot be judged at TRL 3 (R5 wetting, for lack of droplet data) and ten are met, four of them by design. No target was changed at TRL 3. The R6 thresholds are adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review (CSH-DDR-001).

**Design day:** 38 °C air, 25 % relative humidity, clear sky, wind about 1 m/s, 5 h of misting demand, 4.5 peak sun hours. **Humid edge:** 32 °C and 60 % relative humidity, the wettest air in which the controller still mists.

Table 1. Requirements, targets and status after the TRL 3 calculations (CSH-CAL-001; tags in brackets are lines of its script output).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CSH-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Shaded waiting area | 6 m² or more of shade at solar noon; room for at least 6 people standing or seated and one wheelchair space of 0.8 x 1.2 m | Plan layout; sun path check per site | Met: shadow 6.30 m² or more at any sun elevation of 45° or more; room for 7 standing, 3 seated and a wheelchair [A2, A3]. Where the shadow falls depends on the site |
| R2 | Headroom | Clear height 2.2 m or more under any part of the frame, nozzle or brace in the waiting area | Model check | Met: 2,234 mm under the shortened rear knee braces; nozzle tips 2,584 mm or higher [B2, B3] |
| R3 | Radiant heat reduction | Mean radiant temperature under the canopy at least 15 °C below full sun at midday on the design day | Literature comparison; later field measurement with a globe thermometer (HeatMap Node method) | Met on published evidence: about 17.3 °C for shade sails in Tempe ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)); unverified for this fabric |
| R4 | Air cooling from misting | Air temperature in the waiting zone (0.5 to 2.0 m height) at least 2 °C below ambient during misting on the design day | Energy balance at TRL 3; later field test | **Not met at 1 m/s wind:** 1.35 °C averaged over the spray cycle, 2.71 °C while spraying; met below 0.68 m/s [E2, E3] |
| R5 | No wetting | No perceptible wetting of skin or clothing at 1.5 m height on the design day; no puddles on the waiting area | Droplet size data from nozzle maker; later field test | Not verifiable at TRL 3: met only if the nozzle's Dv0.9 is below about 81 µm at 7 bar; no droplet data yet [D3] |
| R6 | Smart activation | Mists only when air temperature is 32 °C or more, relative humidity is 60 % or less, presence is detected in the last 2 min and the tank is above its low level; stops within 60 s when any condition fails | Control logic review; later bench test | Met by design: stops within 30 s [I1]; thresholds adopted under CSH-DDR-001 |
| R7 | Water use | 100 L or less per design day | Nozzle flow calculation | Met: 85 L used, 95 L drawn with the drain-and-refill routine [C2, C5]; holds up to 4.75 L/h per nozzle [C3] |
| R8 | Energy autonomy | Energy-neutral on the design day from the onboard panel; battery covers one full design day with no sun | Energy budget | At risk: 203.8 Wh used against 337.5 Wh harvested; battery 1.005 design days, no margin; no charging in air above about 41 °C [F2, F5] |
| R9 | Water hygiene | Potable-quality supply water; 5 µm filtration; mist line drained within 5 min after every session; water in the tank 48 h old or less; opaque, shaded, lockable tank; documented weekly disinfection | Design review; later microbiological sampling with a partner lab | **At risk:** line drains in about 27 s with the vacuum breaker and water stays under 24 h old with the routine [C5, C7], but tank water sits at about 34 °C, in the 20 to 50 °C *Legionella* growth range ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)) [I3] |
| R10 | Wind resistance | Frame and anchors survive a 3 s gust of 30 m/s (108 km/h) with the fabric fitted; fabric removable in 15 min or less before forecast storms | Structural calculation at TRL 3 | **Not met** on the conservative case: fabric edge pull loads the 50 mm long beams to 3.52 times their capacity; fabric must come off above about 16 m/s. Posts at 0.29 utilization; anchors need about 6.4 kN each, not verifiable [G4, G7, G8, G10] |
| R11 | Privacy | No camera or microphone; presence by passive infrared only; if a status link is fitted, only counts and levels (on-time, water used, temperature, humidity, faults) leave the device | Design review | Met by design; no status link fitted (CSH-DDR-001, D7) |
| R12 | Electrical safety | 12 V DC only, no mains; battery fused at the terminal; all electronics in a lockable IP65 enclosure; LiFePO4 chemistry with BMS and cold-charge cutoff | Design review | Met by design: 15 A terminal fuse, margin 2.0 on the largest current [I2] |
| R13 | Cost | Parts for one prototype $700 or less (`budget_usd`; $750 proposed, awaiting Amish) | BOM | **Not met:** $758, 8.3 % over $700 and 1.1 % over $750 [J1] |
| R14 | Buildability | Bolted assembly; no welding; built with a drill, angle grinder, spanners and a ladder by two people in 2 days or less | Assembly review | Met by design: about 48 bolts and anchors, no welds [H2]; build time unverified |
| R15 | Refill interval | 1 design day or more between tank refills | Water balance | Met: 1.41 design days per full tank [C4] |
| R16 | Maintenance | Nozzles cleanable or replaceable without tools in 15 min or less; filter changed in 10 min or less; descaling interval 1 month or longer | Design review; later field log | **At risk** in hard-water areas: scale can block 0.4 mm orifices; not verifiable at TRL 3 |
| R17 | Movability | Can be unbolted and moved to another site by two people in 1 day or less; no part heavier than 40 kg to lift (tank empty) | Mass estimate | Met: heaviest part a front post with brace, 22.0 kg [H1] |

## Assumptions

- Nozzle flow 4 L/h each at 7 bar, eight nozzles, 50 % spray duty cycle while active; this implies a discharge coefficient of 0.24 for a 0.4 mm orifice, to be checked against nozzle datasheets.
- About 87 % of the sprayed water evaporates in the air; the rest drifts away, drips or wets surfaces (estimate).
- Cooling is estimated over a control volume 3.0 m long and 2.0 m high with air crossing it at the wind speed. Real mixing is less even than this.
- Panel output 100 W x 4.5 peak sun hours x 0.75 system factor.
- Wind: fabric treated as solid with 5 % sag, net normal force coefficient 1.2, S275 steel with a 1.5 factor on wind. All other assumptions are listed in CSH-CAL-001, Table 1.
