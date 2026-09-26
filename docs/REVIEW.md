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

## Session 2026-09-25: TRL 3

On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CoolShade TRL 2 items one by one. This session ran `/advance-trl3` on that instruction and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CSH-DDR-001 v0.1, status proposed): seven items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (D1 to D7), and two items left open (O1 budget, O2 first site and partner).
- `docs/04-calcs/01-sizing.md` (CSH-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: shade and space, headroom, nozzle flow and water balance, line draining, droplet evaporation and wetting, cooling, energy and enclosure heat, wind on posts, beams, fabric, anchors and tank, handling, control and electrical, and cost, with a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`; every number in the note is printed by it.
- `cad/src/model.py`: parametric build123d model (posts and braces, roof frame, fabric, base plates and anchors, panel, enclosure with battery and MPPT, sensor head, tank with strap, pump, filter, drain valve and vacuum breaker, mist line loop with nozzles, harness). Exports `cad/step/` and `cad/stl/` for `coolshade-assembly`, `frame` and `water-system`.
- `cad/src/sheets.py` and `cad/drawings/CSH-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:50, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". CSH-DWG-001 was free because the concept blueprint is CSH-DWG-010.
- `bom/bom.csv` (16 lines, all priced with a supplier type, $758.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The temporary `media/_views*` folders were deleted. No cutaway (the canopy is open), so the kit's origin-centered cut did not matter here.
- CSH-PRB-001, CSH-PRC-001 and CSH-REQ-001 revised to v0.3; `README.md` and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. `budget_usd`, pitch and problem unchanged. PDFs rebuilt in `docs/pdf/`.

Detail changes found necessary by the calculations, all within the adopted choices: knee braces shortened to 400 mm down and 400 mm along (the TRL 2 braces left about 2.11 m of headroom, below R2); a vacuum breaker at the loop's high point (anti-drip nozzles would stop the line from draining); the mist line made a closed loop with a fall toward the down pipe; and a strap on the tank (an empty tank tips in a 30 m/s gust). They add $23.

### Requirement status (CSH-CAL-001, Table 3)

3 not met, 3 at risk, 1 not verifiable at TRL 3, 10 met (5 by calculation, 4 by design, 1 on published evidence).

| ID | Status | Key number |
| --- | --- | --- |
| R4 Air cooling | **Not met** | 1.35 °C averaged (2.71 °C while spraying) at 1 m/s; met only below 0.68 m/s |
| R10 Wind | **Not met** (conservative case) | Fabric edge pull loads the 50 mm long beams to 3.52 times capacity at 30 m/s; fabric must come off above about 16 m/s. Posts 0.29; anchors need about 6.4 kN each, not verifiable |
| R13 Cost | **Not met** | $758: +8.3 % on $700 and +1.1 % on the proposed $750; steel prices look low |
| R8 Energy | At risk | Battery covers 1.005 design days, no margin; no charging above about 41 °C air |
| R9 Hygiene | At risk | Line drains in about 27 s, water under 24 h old with a 95 L daily drain-and-refill, but tank water about 34 °C |
| R16 Maintenance | At risk | Scaling of 0.4 mm orifices; not verifiable on paper |
| R5 Wetting | Not verifiable at TRL 3 | Needs Dv0.9 below about 81 µm at 7 bar (humid edge); no droplet data |
| R1, R2, R7, R15, R17 | Met | 6.30 m² shadow or more; 2,234 mm headroom; 85 L used, 95 L drawn; 1.41 days per tank; heaviest part 22.0 kg |
| R6, R11, R12, R14 | Met by design | Stop within 30 s; PIR only; 15 A fuse; bolted, no welds |
| R3 | Met on published evidence | About 17.3 °C for shade sails; unverified for this fabric |

Key numbers: 32 L/h while spraying; 203.8 Wh used and 337.5 Wh harvested per design day; about 143 kg of steel; post stress 54 MPa unfactored in a 30 m/s gust (the TRL 2 figure of about 144 MPa was an upper bound).

### Decisions recorded (CSH-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: D1 low-pressure 7 bar misting; D2 fixed thresholds (32 °C, 60 % RH, presence in 2 min, tank level); D3 no fans at TRL 3; D4 tank standard, mains optional; D5 3.0 x 2.4 m bolted four-post canopy; D6 removable fabric before storms; D7 no status link. No pitch or problem rewording was recommended, so none was applied. CoolShade uses no shared component from this batch (FieldNode link not fitted), so there is no interface conflict.

### Still awaiting Amish

1. **O1, budget.** The TRL 2 recommendation was to raise `budget_usd` to $750. It is not applied: `budget_usd` stays at $700. The parts cost is now $758, over both figures. Options: (a) $775, which covers the TRL 3 changes with a little room for quotes; (b) $750 and cut the tank to 100 L or accept site-supplied anchors; (c) keep $700 and treat the tank and anchors as site-supplied. Recommendation: (a), because the steel prices look low and quotes may raise them further.
2. **O2, first site type and co-design partner.** No recommendation; stays open.
3. **New, R10 fabric-on wind case.** Options: (a) restate R10 as "frame and anchors survive 30 m/s with the fabric removed; fabric fitted only in forecast gusts below 15 m/s (54 km/h)", which the design meets on paper; (b) keep R10 and upsize the long beams (for example to 80 x 80 mm), which costs money and mass; (c) keep R10 and fit a cord lacing that releases the fabric at a set load. Recommendation: (a) now, with (c) studied at TRL 4 if allowed later, because the fabric's porosity and stretch are unknown and a release that fails safe is worth having. Not applied.
4. **New, R4 and fans (revisit under D3).** R4 remains unmet at 1 m/s. Options: (a) relax R4 to "2 °C while spraying", which is met (2.71 °C); (b) add two 12 V fans (about 20 to 40 W, which would break the R8 energy balance without a larger battery); (c) keep R4 as a stretch target. Recommendation: (a), because the shade gives most of the relief and the battery has no margin for fans. Not applied.
5. **New, R8 energy margin.** Options: (a) a 25 Ah battery instead of 20 Ah (about 1.26 design days); (b) a latching drain valve (1.14 days, but it does not open on power loss). Recommendation: (a), keeping the fail-safe normally open valve. Not applied.

Suggestion only, not in the repo: a continuous spray at half the flow (smaller nozzles) instead of 20 s pulses would give a steadier temperature drop at the same water use.

### Safety concerns

- *Legionella* stays the main hazard: tank water sits at about 34 °C on design days. The daily drain-and-refill, line draining and weekly disinfection need a named responsible person, and no public trial should run without a hygiene plan accepted by the local health authority.
- Wind: on the conservative case the roof beams are overloaded with the fabric on above gusts of about 16 m/s. Removing the fabric before storms is structurally necessary, and the anchors and slab must be checked by an engineer at each site. The tank must be strapped.
- Battery heat: in 45 °C air the enclosure reaches about 48.6 °C, so charging stops; the BMS must enforce the 45 °C charge limit.
- 7 bar water line, slippery wet ground, work at height with heavy steel during assembly.
- Public perception: signage that the mist is not drinking water or a medical service.

### Gaps and notes

- Citations: WebFetch of Crossref on 2026-09-25 confirmed the metadata of the two prior-work entries: Farnham, Emura and Mizuno, "Evaluation of cooling effects: outdoor water mist fan", *Building Research and Information* 43(3), 2015; and Zhao et al., "Assessment of Sun Sail Shading, Mist-Spray Cooling, and Their Hybrid System in Improving Outdoor Thermal Comfort in a School Courtyard", SSRN, 2023. CSH-PRB-001 now names the authors. Their findings were not read and are not used.
- Assumptions that only data or tests can settle: nozzle flow and droplet spectrum, fabric porosity and stretch, the 87 % evaporation fraction, pump draw, enclosure heat and tank temperature.
- The exploded view is dense: the MPPT (7), drain valve (14) and PIR are small and partly hidden; callouts for the mist line (12) and harness (15) sit in open space near their thin runs. The legend identifies them.
- The model's roof beams and braces are solid massing bodies, so the STEP volume overstates steel mass; CSH-CAL-001 computes mass from the section properties instead.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. `electronics/` and `firmware/` are empty. No test, build or firmware material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on the budget (O1), the first site (O2) and the new R10, R4 and R8 items above. For the record only, TRL 4 would need: nozzle flow and droplet size measured at 7 bar at both the design day and the humid edge; a bench spray and drain rig showing the line empties past the anti-drip nozzles; wind data or a test for the chosen fabric; a lab test report (TST, `environment: lab`); and build log entries. None of this has been started.
