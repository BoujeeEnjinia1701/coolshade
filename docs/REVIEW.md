# Review note: CoolShade

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CSH-PRB-001 v0.2): problem with cited figures, users, operating environment (design day 38 °C and 25 % RH, humid check 35 °C and 60 % RH), constraints including water hygiene and privacy, out of scope, prior work, open questions; co-design checklist kept.
- `docs/03-requirements.md` (CSH-REQ-001 v0.2): 17 measurable requirements (R1 to R17) with targets, verification method and concept status.
- `docs/02-concept.md` (CSH-PRC-001 v0.2): how it works, 15 numbered components, water, cooling, energy, wind and cost estimates with assumptions, key design choices, integration with HeatMap Node and FieldNode, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a four-post mono-pitch canopy (3.0 x 2.4 m) with shade cloth, panel, equipment enclosure, sensor head, pump, filter, mist line, tank and drain valve, in street context (sidewalk, curb, road, existing bench) with the 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 15, `flow.png` (daily water flow, estimates), `model.glb` and `viewer.html`. No cutaway: the canopy is open, and the enclosed parts (battery, MPPT, controller) are shown in the exploded view.
- `bom/bom.csv`: 16 lines with indicative USD prices, lines 1 to 15 numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 5 regions), What sparked the idea (origin text kept, trigger added), Problem, Concept, Key components and Safety expanded.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged: the pitch and problem still match the concept and the sources found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Shaded area | 7.2 m² | R1 met |
| Mean radiant temperature drop from shade | about 17 °C (published shade sail data, Tempe) | R3 expected met, unverified |
| Air temperature drop at 1 m/s wind | about 1.4 °C averaged, about 2.7 °C while spraying | **R4 not met** at 1 m/s |
| Water per design day | about 85 L (80 L sprayed, 5 L flush) | R7 met |
| Tank endurance | about 1.4 design days | R15 met |
| Energy per design day | about 205 Wh used, about 340 Wh harvested | R8 met |
| Battery usable | about 205 Wh, one design day without sun | R8 met |
| Wind force at 30 m/s | about 4.7 kN on the roof; about 144 MPa in each post as a cantilever | R10 unverified |
| Parts cost | about $735 | **R13 not met**, about 5 % over $700 |

Requirements not met or at risk:

- **R13 (cost) not met:** about $735 against $700.
- **R4 (air cooling of 2 °C) not met at 1 m/s wind**; met in calmer air. The shade, not the mist, gives most of the relief.
- **R5 (no wetting) at risk:** low-pressure nozzles make larger droplets than high-pressure systems.
- **R9 (water hygiene) at risk:** tank water on hot days will be in the 20 to 50 °C *Legionella* growth range; control relies on draining, turnover and disinfection.
- **R16 (maintenance) at risk** in hard-water areas from nozzle scaling.
- **R2 (headroom) marginal:** about 2.1 m under the rear knee braces, which sit at the edge of the waiting area.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` to $750; (b) cut cost to reach $700, for example by dropping to 60 mm posts with larger knee braces (needs the wind check) or a smaller 80 L tank; (c) keep $700 and treat the anchors and tank as site-supplied. Recommendation: (a), because the post section and tank size carry safety and service margins. `project.yaml` is unchanged.
2. **Misting pressure class.** Low pressure (about 7 bar, 12 V, off-grid) versus mid pressure (about 10 to 20 bar, finer droplets, more pump power) versus high pressure (about 70 bar, mains). Recommendation: low pressure for the first concept, with droplet size and wetting as the first thing to check.
3. **Activation thresholds.** Fixed 32 °C and 60 % RH with PIR presence, versus a heat index or WBGT threshold. Recommendation: fixed thresholds first, since they are easy to explain and audit.
4. **Fans.** None, versus two 12 V fans (about 20 to 40 W more). Recommendation: none at TRL 2; revisit if R4 remains unmet at TRL 3.
5. **Water supply.** Tank only, versus tank with an optional mains float valve and backflow preventer. Recommendation: tank as standard, mains optional where local rules allow.
6. **Canopy size and structure.** 3.0 x 2.4 m, four 80 x 80 x 3 mm posts with knee braces, bolted to an existing slab. Recommendation: keep for TRL 3 and check by calculation.
7. **Storm practice.** Fabric removed before forecast storms versus fabric designed to stay on. Recommendation: removable fabric.
8. **Status link.** None, versus a FieldNode-compatible LoRaWAN link reporting counts and levels only. Recommendation: none for the first prototype.
9. **First site type and partner** for co-design (bus stop, market or queue).

### Safety concerns

- *Legionella* and other waterborne pathogens in warm stored water sprayed as an aerosol near the public. This is the main hazard; a named person responsible for water hygiene and a written flush and disinfection routine are needed before any public trial.
- Wind loading of the canopy and anchors; failure could injure people waiting.
- LiFePO4 battery (about 256 Wh): fuse, BMS, cold-charge cutoff, locked ventilated enclosure.
- 7 bar water line; slippery wet ground; work at height and heavy steel during assembly.
- Public perception: people may believe the mist is drinking water or a medical service. Signage is needed.

### Problems and notes

- WebSearch was not available in this session; all sources were checked by fetching the pages directly. No figure was used that could not be verified. The Farnham et al. (2015) and SSRN (2023) prior work entries are cited by title and DOI only; their findings were not used.
- Small parts (MPPT, drain valve, PIR) are partly hidden behind their callout circles in `media/exploded.png`; the legend identifies them. Callouts for frame-like parts (posts, mist line, harness) sit at the part's center, which falls in open space.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 and 2. If approved, run `/advance-trl3` to check the cooling and wetting estimates against nozzle data, the wind and anchor loads, and the energy budget by calculation, and to produce the parametric model and drawing sheet.
