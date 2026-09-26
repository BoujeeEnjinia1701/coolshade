---
doc_id: CSH-PRB-001
title: CoolShade problem statement
project: CoolShade
doc_type: Problem statement
version: "0.4"
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; budget constraint stated against the proposed figure, humid edge of the misting window, open questions aligned with CSH-DDR-001 and CSH-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# CoolShade problem statement

People waiting outdoors in extreme heat have nowhere to cool down, and public cooling is rarely where they wait. Bus stops, market lanes, clinic and ration queues and school gates put people in full sun for 10 to 60 minutes at a time, often at midday, and the people who wait longest are often those with the fewest alternatives.

## The problem

Heat is a leading weather-related cause of death. WHO estimates about 489,000 heat-related deaths each year between 2000 and 2019, 45 % of them in Asia and 36 % in Europe, and notes that the urban and rural poor are often disproportionately exposed, with informal settlements often hotter than other urban areas ([WHO](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)). In one summer, 2022, an estimated 61,672 people died of heat across 35 European countries ([Ballester et al., *Nature Medicine*, 2023](https://www.nature.com/articles/s41591-023-02419-z)).

Cities make it worse where people stand. The US EPA reports urban daytime temperatures about 1 to 7 °F (about 0.5 to 4 °C) above outlying areas ([US EPA](https://www.epa.gov/heatislands/learn-about-heat-islands)). For a person in the sun, radiant heat from the sun and hot surfaces matters as much as air temperature. In Tempe, Arizona, measurements at 159 locations found that even lightweight shade such as umbrellas and shade sails cut the daytime mean radiant temperature by about 17.3 °C ([Middel et al., *BAMS*, 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)).

Cooling centers and air-conditioned shelters help people who can travel to them, but they are not where people must wait. Many stops and market spots have no shade at all, and where there is shade it does nothing about hot, still air. Commercial misting systems exist, but they are usually mains-powered, high-pressure installations for restaurants and theme parks, run on timers regardless of humidity or occupancy, and are not designed for unattended public sites without power.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Transit riders waiting at stops | Shade and some relief from hot air for 5 to 30 min, without getting wet | Curbside stops, often with no power or water connection |
| Market traders and shoppers | Cooler place to stand and sell during the midday peak | Open-air markets, informal vendors |
| People in queues | Relief during long waits at clinics, offices, food and water distribution | Temporary or semi-permanent sites |
| Outdoor workers | Shaded, cooled rest spot close to work | Street vendors, traffic staff, delivery riders |
| City, transit or market operator | Low-maintenance unit that is safe, uses little water and no grid power, and can be moved | Asset owner responsible for hygiene, permits and inspection |
| Community groups and schools | A shade they can build and maintain themselves | School gates, community spaces |

Heat-vulnerable people include older adults, young children, pregnant people, people with chronic illness and outdoor workers ([WHO](https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health)). The design must work for them, including wheelchair users.

## Operating environment

- Hot seasons with air temperatures of 32 to 45 °C and strong sun; the design case is 38 °C at 25 % relative humidity (hot and dry) with a check at 35 °C and 60 % (hot and humid). The wettest air in which the unit still mists is 32 °C at 60 %, the humid edge used for the wetting check in CSH-CAL-001.
- Misting only helps when the air can absorb water. In hot, humid air it adds little cooling and wets people, so the unit must not mist then.
- Dust, rain, hard water, vandalism and theft; public sites with no staff present most of the time.
- Wind storms. The shade fabric can act as a sail, and on the conservative TRL 3 calculation it must come off before gusts of about 16 m/s (58 km/h). The fabric is fitted only when forecast gusts are below 15 m/s (54 km/h) (CSH-CAL-001, CSH-DDR-002).

## Constraints

- Garage-buildable prototype, about $775 USD in parts (`budget_usd`, set by Amish on 2026-09-25, CSH-DDR-002; it was $700). The parts cost is $773 (CSH-CAL-001).
- Off-grid: solar powered, 12 V DC only, no mains connection needed.
- Water from a refillable tank; mains water connection optional where local rules permit, with backflow prevention.
- Bolted steel frame; no welding required.
- Water hygiene is a public health requirement. *Legionella* grows in water at 20 to 50 °C (optimal 35 °C) and spreads by inhaled aerosols ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)). A misting system in a hot climate is exactly such an aerosol source.
- Privacy: presence detection only (passive infrared). No camera or microphone; no images or audio are recorded or leave the device.
- Installation on public land needs the asset owner's permission.

## Out of scope

- Air conditioning or enclosed, cooled shelters.
- High-pressure (about 70 bar) mains-powered misting.
- Drinking water supply. The tank water is not for drinking.
- Heat warnings or health advice. CoolShade provides shade and local cooling only.

## Prior work

- Shade: the Tempe shade study above measured large radiant heat reductions from shade sails and structures ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)).
- Misting: a systematic review of water mist spray for outdoor cooling covers technologies, methods and impacts ([Ulpiani, *Applied Energy*, 2019](https://doi.org/10.1016/j.apenergy.2019.113647)). Field evaluations include an outdoor mist fan ([Farnham, Emura and Mizuno, *Building Research and Information* 43(3), 2015](https://doi.org/10.1080/09613218.2015.1004844)) and a shade sail and mist-spray hybrid in a school courtyard ([Zhao et al., SSRN preprint, 2023](https://doi.org/10.2139/ssrn.4627041)).
- Lab siblings: HeatMap Node measures street-level heat stress and can identify where shade is most needed. FieldNode is the lab's shared solar and LoRaWAN sensor core, which CoolShade could use for an optional status link.

No open, solar-powered, humidity- and occupancy-controlled misting shade for public waiting spots was found in this review; that is the gap CoolShade targets.

## Open questions

- Which sites to start with (bus stop, market, clinic queue) and through which partner? Proposed, awaiting Amish.
- Is misting acceptable to users at all, given concerns about wet clothes, hair and hygiene? To be asked in co-design.
- Who refills the tank and flushes the lines, and can they visit daily on hot days? CSH-CAL-001 assumes a daily drain-and-refill of about 95 L.
- What local rules apply to public misting (water hygiene, permits, mains backflow)?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
