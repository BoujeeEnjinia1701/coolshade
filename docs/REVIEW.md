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

### Proposed at TRL 2 (status updated 2026-09-25, see CSH-DDR-002)

1. **Budget.** Options: (a) raise `budget_usd` to $750; (b) cut cost to reach $700, for example by dropping to 60 mm posts with larger knee braces (needs the wind check) or a smaller 80 L tank; (c) keep $700 and treat the anchors and tank as site-supplied. Recommendation: (a), because the post section and tank size carry safety and service margins. **Decided by Amish, 2026-09-25: go with recommendation**, at the later TRL 3 recommendation of $775.
2. **Misting pressure class.** Low pressure (about 7 bar, 12 V, off-grid) versus mid pressure (about 10 to 20 bar, finer droplets, more pump power) versus high pressure (about 70 bar, mains). Recommendation: low pressure for the first concept, with droplet size and wetting as the first thing to check. **Decided by Amish, 2026-09-25: go with recommendation.**
3. **Activation thresholds.** Fixed 32 °C and 60 % RH with PIR presence, versus a heat index or WBGT threshold. Recommendation: fixed thresholds first, since they are easy to explain and audit. **Decided by Amish, 2026-09-25: go with recommendation.**
4. **Fans.** None, versus two 12 V fans (about 20 to 40 W more). Recommendation: none at TRL 2; revisit if R4 remains unmet at TRL 3. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **Water supply.** Tank only, versus tank with an optional mains float valve and backflow preventer. Recommendation: tank as standard, mains optional where local rules allow. **Decided by Amish, 2026-09-25: go with recommendation.**
6. **Canopy size and structure.** 3.0 x 2.4 m, four 80 x 80 x 3 mm posts with knee braces, bolted to an existing slab. Recommendation: keep for TRL 3 and check by calculation. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **Storm practice.** Fabric removed before forecast storms versus fabric designed to stay on. Recommendation: removable fabric. **Decided by Amish, 2026-09-25: go with recommendation.**
8. **Status link.** None, versus a FieldNode-compatible LoRaWAN link reporting counts and levels only. Recommendation: none for the first prototype. **Decided by Amish, 2026-09-25: go with recommendation.**
9. **First site type and partner** for co-design (bus stop, market or queue). No recommendation; still Proposed, awaiting Amish.

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

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, now **Decided by Amish, 2026-09-25: go with recommendation** (CSH-DDR-002): D1 low-pressure 7 bar misting; D2 fixed thresholds (32 °C, 60 % RH, presence in 2 min, tank level); D3 no fans at TRL 3; D4 tank standard, mains optional; D5 3.0 x 2.4 m bolted four-post canopy; D6 removable fabric before storms; D7 no status link. No pitch or problem rewording was recommended, so none was applied. CoolShade uses no shared component from this batch (FieldNode link not fitted), so there is no interface conflict.

### Still awaiting Amish at the end of TRL 3 (status updated 2026-09-25, see CSH-DDR-002)

1. **O1, budget.** The TRL 2 recommendation was to raise `budget_usd` to $750. It is not applied: `budget_usd` stays at $700. The parts cost is now $758, over both figures. Options: (a) $775, which covers the TRL 3 changes with a little room for quotes; (b) $750 and cut the tank to 100 L or accept site-supplied anchors; (c) keep $700 and treat the tank and anchors as site-supplied. Recommendation: (a), because the steel prices look low and quotes may raise them further. **Decided by Amish, 2026-09-25: go with recommendation** ($775).
2. **O2, first site type and co-design partner.** No recommendation; stays open (Proposed, awaiting Amish).
3. **New, R10 fabric-on wind case.** Options: (a) restate R10 as "frame and anchors survive 30 m/s with the fabric removed; fabric fitted only in forecast gusts below 15 m/s (54 km/h)", which the design meets on paper; (b) keep R10 and upsize the long beams (for example to 80 x 80 mm), which costs money and mass; (c) keep R10 and fit a cord lacing that releases the fabric at a set load. Recommendation: (a) now, with (c) studied at TRL 4 if allowed later, because the fabric's porosity and stretch are unknown and a release that fails safe is worth having. **Decided by Amish, 2026-09-25: go with recommendation**: (a) applied; (c) on hold with TRL 4.
4. **New, R4 and fans (revisit under D3).** R4 remains unmet at 1 m/s. Options: (a) relax R4 to "2 °C while spraying", which is met (2.71 °C); (b) add two 12 V fans (about 20 to 40 W, which would break the R8 energy balance without a larger battery); (c) keep R4 as a stretch target. Recommendation: (a), because the shade gives most of the relief and the battery has no margin for fans. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **New, R8 energy margin.** Options: (a) a 25 Ah battery instead of 20 Ah (about 1.26 design days); (b) a latching drain valve (1.14 days, but it does not open on power loss). Recommendation: (a), keeping the fail-safe normally open valve. **Decided by Amish, 2026-09-25: go with recommendation.**

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

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation" and recorded in `docs/decisions/0002-recommendations-accepted.md` (CSH-DDR-002 v0.1). CSH-DDR-001 is revised to v0.2 and the earlier lists in this note are annotated.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| D1 to D7 | Pressure class, thresholds, no fans, tank supply, canopy structure, removable fabric, no status link | Adopted for TRL 3, open for review | Decided; no design change |
| O1 Budget | $775 (TRL 3 recommendation, supersedes $750) | `budget_usd` 700 | `budget_usd` 775 |
| R10 wind | Restate: frame and anchors survive 30 m/s with fabric removed; fabric on only in forecast gusts below 15 m/s | Not met: long-beam utilization 3.52 with fabric on at 30 m/s; anchors about 6.4 kN | Met on paper: fabric off at 30 m/s posts 0.14, purlins 0.15; fabric on at 15 m/s beams 0.88; anchors about 2.8 kN, per site |
| R10 release lacing | Study at TRL 4 | Option | Decided, on hold (TRL 4) |
| R4 cooling | Restate as 2 °C while spraying; no fans | Not met: 1.35 °C averaged at 1 m/s | Met: 2.71 °C while spraying at 1 m/s (holds to 1.35 m/s) |
| R8 energy | 25 Ah battery, keep normally open drain valve | At risk: 20 Ah, 1.005 design days | Met: 25 Ah, 1.256 design days |
| Parts cost | Consequence of the battery | $758.00 | $773.00 ($2.00, 0.3 %, under $775) |

Files changed: `project.yaml` (`budget_usd`, evidence list); `README.md` (budget, concept and results text, battery, new "What sparked the idea"); `docs/01-problem.md` (CSH-PRB-001 v0.4); `docs/02-concept.md` (CSH-PRC-001 v0.4); `docs/03-requirements.md` (CSH-REQ-001 v0.4, R4, R10 and R13 targets); `docs/04-calcs/sizing.py` and `01-sizing.md` (CSH-CAL-001 v0.2, new lines G13 and G14); `docs/decisions/0001-trl2-review-decisions.md` (v0.2); `bom/bom.csv` (line 6 battery 25 Ah, $85 to $100; line 3 note) and `bom/bom-notes.md`; `cad/src/model.py` (battery envelope 80 to 100 mm wide), STEP and STL re-exported; `cad/src/sheets.py` and `cad/drawings/CSH-DWG-001.*` (Rev P1 to P2: battery and wind notes, anchor load 6.4 to 2.8 kN); `cad/src/concept_media.py` and all of `media/` re-rendered (key figures, battery label); `docs/pdf/` rebuilt. The site footer is now designmolecule.com in every regenerated file.

### Requirement status now (CSH-CAL-001 v0.2)

| Status | Requirements |
| --- | --- |
| Not met | None (was R4, R10, R13) |
| At risk | R13 cost ($773 against $775; steel prices look low), R9 water hygiene (tank water about 34 °C), R16 nozzle scaling |
| Not verifiable at TRL 3 | R5 wetting (needs Dv0.9 below about 81 µm at 7 bar) |
| Met | R1, R2, R3 (published evidence), R4, R6, R7, R8, R10 (on paper; anchors per site), R11, R12, R14, R15, R17 |

### Still awaiting Amish

- O2, first site type (bus stop, market or queue) and co-design partner: no recommendation was made, so it stays Proposed, awaiting Amish.

### Cross-repo actions

- None. No FieldNode status link is fitted (D7), so CoolShade asks nothing of another repo. HeatMap Node remains a related project only.

### Safety

The safety sections are unchanged in substance. The wind rule is now explicit: the fabric goes on only when forecast gusts are below 15 m/s (54 km/h) and comes off before storms. *Legionella* control (R9) remains the main hazard.

### TRL

`trl: 3` and `trl_target: 3` are unchanged. TRL 4 remains on hold by Amish's instruction: the load-release lacing study, nozzle and droplet measurement, wind tests, firmware and any build or purchase have not been started.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose CoolShade for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it changes no design figure, requirement, calculation, drawing or BOM line.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 102 named parts (64 shell, 32 internal, 6 context) with colour, material, BOM line, group and explode offset; `TITLE` and `RENDER_VIEWS` define three views: "hero" (canopy, water plant and context), "exploded" and "detail" (the water plant only, since the mannequin makes the hero scene tall). All dimensions, positions and interfaces come from `PARAMS` and `derived()` in `cad/src/model.py`, and its `box()`, `rod()`, `zcyl()` and `shs()` helpers are reused.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced separately by the orchestrator.

What the appearance model adds:

- Structure: posts with rounded SHS corners; knee braces with bolted end sleeves; base plates with anchor washers and nuts; roof frame with black end caps.
- Roof: shade cloth with a reinforced hem band and 28 eyelets; 100 W panel with an aluminium frame, 36 cells, busbars, glass, clamps, rail caps and a junction box on slotted rails.
- Mist system: loop on hanger clips, eight slip-lok tees with brass nozzles, a vacuum breaker at the front, and a riser clipped up the rear left post.
- Power and sensing: enclosure with a door, a window onto the MPPT controller's lit display, a lock, hinges, a rain hood, a lit green status lamp, a label, glands and post clamps, with the battery, MPPT and controller board inside; louvred radiation shield with its probe, arm and clamp; PIR with a Fresnel dome.
- Water plant: opaque tank with rolling hoops, screw lid, lock hasp, "potable water only" label, outlet tap, anchor cleats, strap, ratchet and post eye; vented pump box with a window onto the pump; clear-bowl filter with its cartridge; solenoid drain valve; hoses.
- Context: compact paved patch with a curb, an existing slatted bench and the shared clay mannequin (1.75 m, standing) under the canopy.

### Differences from model.py (appearance only)

Each item is Proposed, awaiting Amish.

1. **Filter in the suction path.** `model.py` routes the supply hose from the tank straight to the pump, while the precis says the pump draws through the filter. The appearance model keeps the model.py hose and adds a short hose from the filter to the pump box. Recommendation: at the next model update, reroute the model.py hose from the tank to the filter and then to the pump, and leave the render as is until then.
2. **Pump shelf bracket.** `model.py` shows the pump box about 10 mm clear of the rear left post with no support. The appearance model adds a steel shelf bracket bolted to the post. Recommendation: add the bracket to `model.py` and to BOM line 16 hardware (no new line or cost).
3. **Drain valve connection.** `model.py` has no pipe between the riser and the drain valve. The appearance model adds a short tee from the riser and a 40 mm downturned spout below the valve envelope. Recommendation: adopt, since the valve must connect to the line to drain it.
4. **Enclosure details outside the model.py box.** The rain hood adds 12 mm at the sides and 6 mm on top; post clamps wrap the post; hinges, lock and lamp stand a few millimeters proud of the door. Recommendation: adopt as appearance detail; the 420 x 320 x 160 mm envelope is unchanged.
5. **Tank lid and hoops.** The screw lid and neck add about 50 mm to the 700 mm tank height, and the rolling hoops add 7 mm to the radius. Recommendation: adopt; this is typical of a 120 L drum and does not affect the post, strap or pump positions.
6. **Sensor head and PIR shapes.** The shield plates are louvred cones on spacer rods instead of flat discs; the PIR housing is 40 mm tall with a dome below it, ending 5 mm lower than the model.py block. Recommendation: adopt.
7. **Scene context.** The paved patch (3.7 x 2.9 m with a curb) replaces the larger sidewalk, curb and road of `concept_media.py`, and the bench moves 40 mm toward the rear and is shown as a slatted timber bench. Recommendation: keep for product renders only; the concept media are unchanged.

The shade cloth, beams, posts, panel, mist line, nozzle positions and enclosure envelope keep the model.py dimensions (the cloth has 40 mm rounded corners inside the full-size hem).

### Checks

All parts are valid solids and tessellate at `tessellate(0.05, 0.1)`; `.kit/product_export.py` exports them; `python .kit/render.py --check` passes. Matplotlib previews (clear parts omitted) were used to check the three views.

### TRL

This is an appearance model only: no tolerances, fabrication detail, PCB layout or build work. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: constructable design and prototype build plan (kit 1.7.0)

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, with outstanding decisions kept out of the build plan in a separate design decisions register, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session installed kit 1.7.0 and ran `/build-plan` on that instruction. It stopped at TRL 3: nothing was built, bought or tested.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- `cad/src/model.py` rewritten as a constructable model: 61 parts, each modelled as it is made or bought, with every bolt and cable hole cut, and 117 build123d constructability checks (`python cad/src/model.py --check`): overlap of every neighbouring pair, contact at every joint, headroom and the sensor shield's height. All pass. STEP and STL re-exported (`coolshade-assembly`, `frame`, `water-system`).
- `docs/decisions/0003-design-for-construction.md` (CSH-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (CSH-BLD-001 v0.1): the illustrated build plan, with 16 making sketches (`cad/drawings/CSH-DWG-101` to `116`), 13 joint close-ups, 17 assembly step pictures, an overview, a slab layout, post and beam hole charts, block wiring and the water circuit, all drawn from the model by `cad/src/build_plan_media.py`.
- `docs/06-design-decisions.md` (CSH-DEC-001 v0.1): 3 open decisions, 13 items to confirm when parts are bought or the site is chosen, and every decision made.
- `docs/04-calcs/sizing.py` and `01-sizing.md` (CSH-CAL-001 v0.3), `docs/02-concept.md` (CSH-PRC-001 v0.5), `docs/03-requirements.md` (CSH-REQ-001 v0.5), `bom/bom.csv`, `bom/bom-notes.md`, `README.md` (links line and "Building the prototype"), `project.yaml` (`design_state: constructable`, evidence list).
- General arrangement `cad/drawings/CSH-DWG-001` Rev P4 and the concept media (`media/hero.png`, `exploded.png`, `concept-blueprint.*`, `flow.png`, `model.glb`, `viewer.html`) regenerated from the new model. PDFs rebuilt in `docs/pdf/`.

### Design changes made for construction (CSH-DDR-003)

1. Posts moved out across the sidewalk from 2,100 to 2,350 mm between centres so the long beams sit on the post tops at the roof's edges and the cloth has a tube under every edge; end beams moved to the roof ends.
2. Long beams horizontal and square on the post tops; end beams, purlins and a new panel bearer cut 7° off square to butt against the beam faces.
3. Head cleats at every post top and base cleats at every post foot (angle, bolted); no welding.
4. Roof joints made with 50 x 50 x 5 mm angle frame cleats; every bolt into a closed beam goes into an M8 or M5 steel rivet nut, so nothing stands proud under the cloth.
5. Knee braces with flattened, bent, bolted ends; bends 350 mm down and along (was 400 mm), lowest point 2,223 mm.
6. Solar panel moved to the rear edge on two rails and four L-feet on the panel bearer and the rear beam; a 1,020 x 670 mm notch in the cloth under it; purlins moved from 450 to 530 mm off centre to frame the notch.
7. Enclosure on two through-bolted rails; battery, MPPT and controller board placed inside; three cable glands.
8. Sensor arm made from 40 x 40 x 4 mm angle on the street face of the front right post, raised to 2.4 m (shield's lowest plate 2,266 mm); bought shield unit hung on one bolt; PIR on a bracket.
9. Pump, filter and drain valve on an equipment plate on the rear left post; the down pipe ends in the drain valve with a tee to the pump outlet; hoses tank to filter to pump (REVIEW 2026-09-26, items 1 to 3).
10. Tank moved clear of the post base; strap round tank and post; two stop cleats with M10 anchors.
11. Mist line loop moved 70 mm inboard of the long beams and under the end beams, on 18 hanger clips.
12. Cables routed inside the posts and beams through grommeted holes.
13. Added parts needed for the decided function: a tank low-level switch (R6) and an I2C bus extender for the 7 m sensor cable.

### Key results (CSH-CAL-001 v0.3)

- Requirement status: **1 over its value-engineering target (R13 cost: estimated $882.00 against the $775 target, +13.8 %)**, 2 at risk (R9, R16), 1 not verifiable at TRL 3 (R5), 13 met. Before this session: none not met, 3 at risk.
- Headroom 2,223 mm (R2 met, was 2,234); clear floor 2.72 x 2.27 m (8 standing, 3 seated and a wheelchair); nozzle tips 2,559 and 2,835 mm.
- Steel 167 kg; heaviest part a front post, 21.0 kg; 79 bolts and anchors.
- Fabric off at 30 m/s: posts 0.14, panel bearer 0.02, purlins 0.07, rear beam 0.11; anchors about 2.8 kN factored. Largest rivet nut pull about 0.16 kN factored.
- Mist line 11.91 m, 0.40 L, drains in about 30 s.

### Proposed, awaiting Amish (see CSH-DEC-001)

1. R14 tool list: add a hand rivet nut tool and a bench vice (recommended).
2. First site type and co-design partner (no recommendation; carried over).

### Stale media (made on Amish's Mac; not regenerated here)

The design changed visibly, so `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` are stale: they show posts on the 2.1 m grid, the panel in the middle of the rear half on top of the cloth, the tank against the post and the concept braces. `cad/src/product_model.py` still builds the concept appearance (it reads `model.py`'s parameters, so the posts move, but its panel, rails, tank and equipment details follow the concept); it needs updating before the renders are redone.

### Safety

Unchanged in substance. The build plan adds safety stops S1 to S9 (slab drilling, lifting posts, work at height, battery, pressurizing the line, misting near people, fitting the cloth, public use). *Legionella* control (R9) remains the main hazard.

### Recommended next step

Amish reviews CSH-DDR-003 and the open decisions in CSH-DEC-001; the Value engineering section there holds the $775 target, the $882 estimate and the savings worth trying. TRL 4 (building to this plan) stays on hold by his instruction.

## Session 2026-10-02: open decisions decided

Amish approved every recommendation for the open decisions on 2026-10-02: "i approve your recommendations for all 555 open decisions."

### Decisions recorded

Two, both moved to "Decisions made" in CSH-DEC-001: R14's tool list gains a hand rivet nut tool and a bench vice, and the rivet nuts are kept (CSH-DDR-003, A2); the first site type is a market lane with the market operator as co-design partner in a hot, dry city, with a farmers' market operator in the Phoenix area as the first candidate to approach and Arizona State University's urban heat researchers as the candidate measurement partner.

### Documents changed

- `docs/06-design-decisions.md` CSH-DEC-001 v0.3: decisions made; open decisions section now reads "None"; To confirm item 10 updated for a market lane site.
- `docs/decisions/0003-design-for-construction.md` CSH-DDR-003 v0.3: A2 decided as recommended (status Draft kept).
- `docs/03-requirements.md` CSH-REQ-001 v0.7: R14 restated with the hand rivet nut tool and bench vice.
- `docs/04-calcs/01-sizing.md` CSH-CAL-001 v0.5: R14 row text only; no figures changed.
- `docs/01-problem.md` CSH-PRB-001 v0.5 and `docs/02-concept.md` CSH-PRC-001 v0.7: first site type and candidate partners.

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (model, drawings, pictures): set the slab, anchors, setback and orientation of the first build for a market lane once a site is offered; the model and build plan pictures now show a curbside stop layout.
2. Decision 2 (docs): carry the market lane into the water hygiene plan (To confirm item 11), naming the local health authority and responsible person once a site is offered.

### Points found in the review

- The design for construction (DDR-003, P1 to P16) was still "open for his review" but had no row in the open decisions table; the recommendation was to accept it, with steel quotes taken before buying. Amish accepted it later on 2026-10-02 (see the next session).
- The *Legionella* water hygiene plan ("To confirm" item 11) is a safety stop for any public trial, not a purchase check; it belongs with the open decisions or the safety stops.
- The constructable design is $882 against the $775 target, $107 (13.8 percent) over, and the steel at about $1.61 per kg including cutting, drilling and galvanizing looks low for small quantities, so the gap may widen.

## Session 2026-10-02: design-for-construction changes accepted

Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This accepts the design-for-construction changes P1 to P16 in Table 1 of CSH-DDR-003, with their knock-on changes in Table 2, which were left open for his review when the open decisions were decided earlier the same day. No other item is decided by it. trl stays 3; no build or test work was done, and the model, BOM, calculations and pictures are unchanged.

### Documents changed

- `docs/decisions/0003-design-for-construction.md` (CSH-DDR-003 v0.4, status Draft): status line now "accepted" with Amish's words.
- `docs/06-design-decisions.md` (CSH-DEC-001 v0.4): Decisions made row added, dated 2026-10-02; the 2026-09-30 row no longer calls the changes open for review.
- `docs/05-build-plan.md` (CSH-BLD-001 v0.2): section 2 says CSH-DDR-003 is accepted.
- PDFs regenerated.

### Recommended next step

Take steel quotes before buying, as noted in the previous session. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out. trl stays 3; nothing was built, bought or tested.

### Follow-ups (2)

| # | Follow-up | Result |
| --- | --- | --- |
| 1 | Set the slab, anchors, setback and orientation of the first build for a market lane | Not done: needs a site to be offered; the model and pictures keep the curbside stop until then (see To confirm item 10) |
| 2 | Carry the market lane into the water hygiene plan (To confirm item 11) | Done. Item 11 and safety stops S7 and S9 now name the market operator's manager and the environmental health authority by role; the authority itself is named once a site is chosen |

No model, BOM, calculation or picture change was called for: requirement statuses, cost and mass are unchanged. The appearance model (`cad/src/product_model.py`) already follows `cad/src/model.py`; render scenes were exported again to /home/claude/renders/coolshade.

### Documents changed

- `docs/06-design-decisions.md` (CSH-DEC-001 v0.5), `docs/05-build-plan.md` (CSH-BLD-001 v0.3); PDFs regenerated.

### Cross-repo actions

None.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
