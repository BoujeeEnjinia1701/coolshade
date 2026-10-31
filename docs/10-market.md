---
doc_id: CSH-MKT-001
title: CoolShade market and viability
project: CoolShade
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade; benchmark prices checked 2026-10-30; items whose prices could not be found are marked to assess"
---

# CoolShade market and viability

CoolShade is for market operators, transit agencies and community groups that want shade and cooling where people wait and have no mains power, competing with portable mains-powered coolers and misting fans on one side and fixed bus shelters on the other. An open design matters because the unit has to be built from common parts, repaired where it stands and adapted to each site's wind, slab and water. Prices and benchmarks were checked 2026-10-30; where a price could not be found it says so. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Market operators and vendors | Open-air markets in hot, dry cities (first site: a market lane, CSH-DEC-001) | Hessaire 3,100 CFM portable evaporative cooler, reconditioned, USD 288.53 with a 10 gallon tank (Home Depot listing, checked 2026-10-30); needs mains power and cools a small zone indoors or on a patio | 882 in parts (`bom/bom.csv`, indicative, no labour) | Shade plus cooling for a group, no mains power; the benchmark cools one zone and gives no shade |
| Cities and transit agencies | Bus stops and queues without power | A new bus shelter costs up to EUR 25,000 according to Ireland's National Transport Authority, quoted by the Limerick Leader (page undated; checked 2026-10-30); not converted; a shelter gives shade and cover but no cooling | 882 in parts | A fraction of a shelter's cost, movable by two people, with cooling; no seating or rain cover |
| Misting installations | Restaurants, patios and venues | Mist N Go 2 cabana misting fan package, 850 psi pump, 120 V AC input, 150 W (Advanced Misting Systems, checked 2026-10-30); price not listed on the page, to assess | 882 in parts | Off-grid, 7 bar, switched by heat, humidity and presence; the benchmark runs on mains and a timer or switch |
| Community groups and schools | School gates, community spaces | No priced benchmark found; shade sails are sold by many suppliers (price to assess) | 882 in parts | Open drawings and a build plan; bolted steel, no welding |

Two things the benchmarks do not show: the costs of water hygiene (a plan, sampling and a responsible person) and of daily refilling, which a mains misting system does not need and CoolShade does (CSH-CAL-001 C5). For options B and C: wet-pad fan coolers are sold as portable units (the Hessaire above); the price of composite sheet for option C was not found, to assess.

## Open route

A community workshop or a school builds the canopy from the drawings and the build plan with a drill, an angle grinder, spanners, a rivet nut tool and a vice (PR-014). The market operator installs it, refills the tank and flushes the line. Heat-research groups, NGOs and city programmes carry the design between sites. CERN-OHL-S keeps changes open. The steel, cloth and fixings are everyday parts; the pump, the nozzles and the controller are the parts a builder must buy from specialists.

## Sources

- Home Depot. "Hessaire Reconditioned 3100 CFM 3-Speed Portable Evaporative Cooler (Swamp Cooler) for 950 sq. ft. MC37V-RFB." https://homedepot.com/p/Hessaire-Reconditioned-3100-CFM-3-Speed-Portable-Evaporative-Cooler-Swamp-Cooler-for-950-sq-ft-MC37V-RFB/316951448 (checked 2026-10-30): USD 288.53.
- Limerick Leader. "Building a bus shelter can cost up to 25,000, says NTA." https://www.limerickleader.ie/news/building-a-bus-shelter-can-cost-up-to-eu25000-says-nta-7588831 (checked 2026-10-30): up to EUR 25,000 for a single new shelter; the page shows no date.
- Advanced Misting Systems. "Mist N Go 2 - 14 inch Cabana Series Misting Fan Package." https://www.advancedmistingsystems.com/mist-n-go-2-14-cabana-series-misting-fan-package/ (checked 2026-10-30): pump up to 850 psi, 120 V AC input, 12 V DC 150 W pump motor; no price on the page.
- Unit cost for CoolShade: the indicative prices in `bom/bom.csv`; the steel lines look low until quoted (CSH-CAL-001 J2).
