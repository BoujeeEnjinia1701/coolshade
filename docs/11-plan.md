---
doc_id: CSH-PLN-001
title: CoolShade project plan
project: CoolShade
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade: CoolShade is at stage P3 (design outputs), TRL 3; P4 to P6 on hold under the stage cap"
---

# CoolShade project plan

CoolShade is at stage P3 (design outputs), TRL 3. The calculation note, the D3 model of all three concept options, the drawings, the priced BOM and the build plan are done; the concept choice is proposed and waits for Amish (CSH-DDR-004). The next gate, P4 (verification, TRL 4), is on hold while the portfolio stage cap is P3, and needs a site and a hygiene plan first. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept choice | Amish Chadha | CSH-OPT-001, CSH-DDR-004, CSH-DEC-001 D8 | Proposed, awaiting Amish |
| Partner and site | Amish Chadha | Market operator and a heat-research partner in a hot, dry city (CSH-DEC-001) | Candidates named; nothing agreed |
| Requirements | Design lead | CSH-URS-001, CSH-PRS-001, CSH-RTM-001 | Done on paper; partner review pending |
| STEM check | Design lead | CSH-STM-001, `stem_check.py` | Done 2026-10-30; 13 rows plausible, need field data |
| Calculations and model | Design lead | CSH-CAL-001 v0.6; D3 model of options A, B and C; STEP and STL | Done 2026-10-30 |
| Drawings, BOM, build plan | Design lead | CSH-DWG-001, DWG-101 to 116, `bom/bom.csv`, CSH-BLD-001 | Done 2026-09-30, redrawn 2026-10-30 |
| Risk, market, regulatory | Design lead | CSH-RSK-001 with design FMEA, CSH-MKT-001, CSH-REG-001 | Done 2026-10-30 |
| Renders | Coordinator | Options picture and product renders (Blender, Amish's Mac) | Queued after the kit 1.9.1 upgrade |
| Verification (P4) | Partner | Hygiene sampling, nozzle spectrum, build and bench tests | On hold (stage cap P3) |

## Resources needed

Table 2. Resources.

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead (Claude with Amish's review) | P0 to P3 documents | Done | 0 |
| Prototype parts | One canopy (P4, on hold) | | 882 (`bom/bom.csv`, 107 over the 775 target) |
| Nozzle maker's data | Flow and Dv0.9 at 7 bar | A request | To assess |
| Water hygiene plan | Plan accepted by the health authority | Weeks, with the market operator | To assess |
| Site survey | Slab, wind, setbacks, water hardness | 1 to 2 days | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Done 2026-10-30 (kit 1.9.1 upgrade of a repo made at kit 1.7) |
| P1 Definition | URS, PRS draft, RSK, MKT, REG complete | Done 2026-10-30 |
| P2 Design inputs | PRS targets, CAL, RTM, DDR, STEM check closed by calculation | Done 2026-10-30; 13 STEM rows need field data |
| P3 Design outputs | Model, STEP, DWG, BOM, BLD, DEC, FMEA | Done 2026-10-30 |
| P4 Verification | Hygiene sampling, nozzle test, bench and wind-load checks | On hold |
| P5 to P6 | Field trials with a partner, launch | On hold |

## Next steps and decision requested

Decision requested from Amish: the concept choice (option A, B or C, or a hybrid of A with option C's white skin), the presence sensor trade-off (PIR or radar) and whether to disinfect the tank water (CSH-DEC-001 D8, D10, D11). The recommended next step is a partner and a hygiene plan and, when the cap allows, TRL 4: the nozzle's droplet spectrum, one canopy built from the plan, and a bench test of the controller.

## References

Advanced Misting Systems. "Mist N Go 2 - 14 inch Cabana Series Misting Fan Package." Accessed October 30, 2026. https://www.advancedmistingsystems.com/mist-n-go-2-14-cabana-series-misting-fan-package/.

Home Depot. "Hessaire Reconditioned 3100 CFM 3-Speed Portable Evaporative Cooler." Accessed October 30, 2026. https://homedepot.com/p/Hessaire-Reconditioned-3100-CFM-3-Speed-Portable-Evaporative-Cooler-Swamp-Cooler-for-950-sq-ft-MC37V-RFB/316951448.

Limerick Leader. "Building a Bus Shelter Can Cost up to 25,000, Says NTA." Accessed October 30, 2026. https://www.limerickleader.ie/news/building-a-bus-shelter-can-cost-up-to-eu25000-says-nta-7588831.

Middel, Ariane, et al. "Tempe, Arizona Shade Study." *Bulletin of the American Meteorological Society* 102 (2021). Accessed October 30, 2026. https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml.

Ulpiani, Giulia. "Water Mist Spray for Outdoor Cooling: A Systematic Review." *Applied Energy*, 2019. https://doi.org/10.1016/j.apenergy.2019.113647.

World Health Organization. "Legionellosis." Accessed October 30, 2026. https://www.who.int/news-room/fact-sheets/detail/legionellosis.
