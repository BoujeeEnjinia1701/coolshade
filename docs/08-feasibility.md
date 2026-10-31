---
doc_id: CSH-FEA-001
title: CoolShade feasibility assessment
project: CoolShade
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade, from CSH-STM-001, CSH-CAL-001 v0.6 and the D3 model of option A"
---

# CoolShade feasibility assessment

**Feasible on paper, with three open questions that only a site and maker's data can close:** the bolted frame, the energy budget and the cooling pass their checks with margin (CSH-CAL-001, CSH-STM-001), but the droplets must evaporate before they wet anyone (STEM S4), the water must stay safe (S14) and the cost, USD 882, is 13.8 % over the USD 775 target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | A 3.0 x 2.4 m shade at about 7 degrees on four 80 x 80 x 3 mm posts; the mist absorbs about 18.8 kW and cools the zone 2.7 °C while spraying; 85 L and 204 Wh per design day; the D3 model builds with 372 parts and no interference | High | Real mixing is less even than the control volume assumes (S2); wetting needs Dv0.9 below about 80 µm at 7 bar (S4) | CSH-STM-001 S1 to S10; CSH-CAL-001 sections A to F; `cad/fidelity.json` |
| Materials | Galvanised steel sections, HDPE shade cloth, an aluminium panel frame, polyethylene tank; brass nozzles | High | Scale in hard water blocks the 0.4 mm nozzles (S12); 90 % UV-block cloth is untested for the radiant benefit | CSH-STM-001 S12, S13 |
| Manufacturing and assembly | Cut, drill, bolt; M8 rivet nuts in 2 mm tube; no welding; two people in two days on paper | Medium | Needs a hand rivet nut tool and a vice (CSH-DEC-001); the rivet nut pull-out rating in a 2 mm wall is unchecked (S21); build time unverified | CSH-BLD-001; CSH-CAL-001 G15, H2 |
| Power and controls | 100 W panel, 25 Ah LiFePO4, MPPT, microcontroller, 12 V pump; 1.66 times the daily use harvested; 1.26 design days of reserve | High | Charging pauses in air above about 42.7 °C with the white enclosure (S11); a PIR sensor loses range in air near body temperature (S15); firmware is TRL 4 scope | CSH-CAL-001 F1 to F5; CSH-STM-001 S9, S10, S11, S15 |
| Supply of parts | Steel sections, cloth, panel, battery, pump, tank and nozzles from regional distributors; BOM of 16 priced lines | Medium | Steel prices look low until quoted (CSH-CAL-001 J2); nozzle flow and droplet data not yet from a maker; USD 882 against USD 775 | `bom/bom.csv`; CSH-DEC-001 to-confirm items 1 to 3 |
| Site | An existing concrete slab for M16 anchors; permission from the asset owner; a hygiene plan accepted by the health authority; someone to refill and drain daily | Low | No partner or site agreed (CSH-DEC-001); the hygiene plan is a pre-condition of a public trial (CSH-REG-001 G1) | CSH-REG-001 G1, G2; CSH-RSK-001 P1, P3 |

Ratings: High, Medium, Low.
