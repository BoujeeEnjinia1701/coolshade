---
doc_id: CSH-DDR-003
title: CoolShade design for construction
project: CoolShade
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target, with cost question A1 replaced by the register's Value engineering section
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are proposed, awaiting Amish, and are listed in the design decisions register (CSH-DEC-001).

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of CSH-DDR-002 was a massing model: it showed what CoolShade does, but most of its parts met as overlapping solids with no fixing, and some could not be made or fitted at all. Checking it part by part found the problems P1 to P16 below.

The changes keep what CoolShade does and its pitch: a bolted four-post canopy, 3.0 x 2.4 m in plan with the same roof heights and slope, the same shade cloth, 100 W panel, 25 Ah battery, controller, sensors, 7 bar pump, 120 L tank, eight nozzles, drain valve and vacuum breaker, the same activation rules and the same safety case (fabric off above 15 m/s, drain after every session, 12 V only). Every change is in `cad/src/model.py`, which now runs 117 constructability checks with build123d (`python cad/src/model.py --check`): every pair of the 61 modelled parts that come near each other is tested for overlap, every joint for contact, and the headroom and the sensor shield's height are measured. All 117 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The shade cloth (3.0 x 2.4 m) ran 125 mm past the long beams at the street and rear edges and 75 mm past the end beams, with nothing under its edges to lace or tension it to. | Posts moved out across the sidewalk from 2,100 to 2,350 mm between centres, so the long beams sit on the post tops at the roof's street and rear edges; end beams moved from the posts to the roof ends, 1,475 mm each side of centre. The cloth is laced over the frame, every eyelet round the tube below it. | Keeps the 3.0 x 2.4 m roof and its 7.2 m² of shade (R1). Moving the posts out is simpler than adding outriggers, and widens the clear floor from 2.02 to 2.27 m. |
| P2 | The long beams, end beams and post tops met as overlapping solids at the corners, with no brackets. | The long beams sit on the posts; the end beams, purlins and panel bearer are cut to butt against the beams' inner faces and are held by 50 x 50 x 5 mm angle cleats, one M8 bolt into each tube. | Every joint is face to face and bolted; one cleat size for the whole roof. |
| P3 | The long beams were tilted with the 7.1° roof plane, which a square tube cannot do on a square-cut post top. | The long beams are horizontal and square; only the end beams and purlins slope. Their ends are cut 7° off square so they stand upright against the beam faces. | The cloth still lies on a 7.1° plane: the long beams' top edges and the sloping tubes' tops meet it within 4 mm. |
| P4 | The post tops had no fixing to the beams. | Two head cleats per post (50 x 50 x 5 mm angle, 46 mm long), one on each side face, flat leg flush with the square-cut post top: one M10 bolt through both cleats and the post, one M8 bolt up into a rivet nut in the beam's underside per cleat. | No welding (R14), nothing on the beam tops under the cloth. |
| P5 | Each post stood on its base plate with no fixing. | Two base cleats per post (75 x 75 x 6 mm angle, 220 mm long), one each side: two M12 bolts through cleat, post and cleat; the four M16 anchors pass through the cleats' flat legs and the plate. | Bolted post base without welding, using the anchors the concept already had on the same 160 mm square. |
| P6 | The knee braces were solid rods whose ends ran into the post and beam, with no fixing. | 32 mm tube, 581 mm long, both ends flattened in a vice and bent 45°: the lower end bolted flat on the post's inner face (M10 through the post), the upper end flat under the beam (M8 into a rivet nut). The bends are 350 mm down the post and along the beam (was 400 mm). | Flattened ends are the simplest bolted brace end. The shorter brace keeps the bottom of its flattened end at 2,223 mm, above R2's 2,200 mm. |
| P7 | The panel rails floated 15 mm above the purlins and passed through the cloth, the panel overlapped its rails, and with the panel on top of the cloth the cloth could not be taken off before storms (R10). | The panel moves to the rear edge of the roof on two rails standing on four L-feet: two on a new 50 x 50 x 2 mm panel bearer between the purlins and two on the rear long beam. The cloth has a 1,020 x 670 mm notch under the panel, laced round the bearer and the purlins; the panel shades the notch. The purlins move from 450 to 530 mm each side of centre to frame the notch. | The cloth comes off without touching the panel; the panel stays up in a storm. The panel's shade replaces the cloth's under the notch, so the shaded area is unchanged. |
| P8 | The enclosure floated against the rear right post with no fixing, and the battery and MPPT were solids inside a solid box. | Two 40 x 6 mm rails through-bolted to the post's outer face with M10 countersunk bolts; the enclosure screws to the rails from inside through its moulded mounting holes. Battery on the enclosure floor, MPPT and controller board on the maker's gear plate, three cable glands underneath. | The enclosure stays sealed and lies flat on the rails clear of the post. |
| P9 | The sensor shield's plates floated with gaps between them; the arm was a rod with no fixing whose tip ran through the shield; with the arm at 2.30 m the lowest plate hung at 2.25 m beside a footway. | A bought multi-plate shield with its own top plate and spacers, hung by one M8 bolt under the end of a 40 x 40 x 4 mm angle arm; the arm is bolted to the street face of the front right post with two M8 through bolts, its top 2,420 mm up. | The shield's lowest plate is at 2,266 mm, still outside the roof and the mist zone. |
| P10 | The PIR sensor touched the front beam with no fixing. | A small bracket on two M5 rivet nuts under the front beam. | |
| P11 | The pump floated 10 mm off the rear left post, the filter and drain valve floated, and nothing joined the down pipe to the drain valve (REVIEW 2026-09-26, items 2 and 3). | A 320 x 630 x 3 mm equipment plate bolted to the street face of the rear left post carries the pump, filter and drain valve. The down pipe ends in the drain valve, the system's low point, with a tee to the pump outlet. | One plate, two bolts through the post; the valve stays at the low point so the line drains. |
| P12 | The tank overlapped the rear left post and its base by about 30 mm; the "two small anchors" had nothing to hold. | The tank moves to 350 mm in from the post along the curb and 355 mm toward the street, clear of the post base. A ratchet strap goes round the tank and the post at 400 mm, and two stop cleats with one M10 anchor each stop the tank sliding away from the post. | The strap still holds an empty tank against the 30 m/s gust [G12]. |
| P13 | The mist line had no supports, and the supply hose bypassed the filter (REVIEW 2026-09-26, item 1). | The loop runs 70 mm inboard of the long beams and directly under the end beams, held by 18 hanger clips on M5 rivet nuts; hoses run tank to filter to pump. | Clear of the posts, braces and cleats by at least 26 mm. |
| P14 | The cables ran as rods through the post and beam walls and through the enclosure. | Cables run inside the posts and beams, through 12 mm grommeted holes, into the enclosure through three glands underneath. | Tidy, out of reach and protected from the sun. |
| P15 | Parts needed but missing: a tank level sensor for R6's "tank above its low level" rule (CSH-DDR-001, D2), and a way to carry the sensor's I2C signal about 7 m. | BOM line 13 adds a low-level float switch with its cable; line 9 adds an I2C bus extender pair. | Needed for the decided control rule; I2C alone is not reliable over 7 m. |
| P16 | Through bolts into the closed beams would put nuts under the cloth and crush the tubes. | Every bolt into a beam goes into a steel rivet nut (36 M8, 20 M5). | Nothing stands proud where the cloth runs. The largest pull on one M8 rivet nut is about 0.16 kN factored [G15]. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Posts | Front 2,902 mm and rear 2,608 mm (were about 2.89 and 2.62 m) on a 2,800 x 2,350 mm grid. Heaviest part a front post, 21.0 kg (was 22.0 kg with its brace) [H1]. | P1, P4 |
| Space and headroom | Clear floor 2.72 x 2.27 m: room for 8 standing and 3 seated with the wheelchair space (was 7) [A3]. Lowest point overhead 2,223 mm (was 2,234 mm) [B2]. Nozzle tips 2,559 mm rear, 2,835 mm front (were 2,584 and 2,829 mm) [B3]. Droplet size that stays clear of heads on the humid edge about 80 µm (was 81 µm) [D3]. | P1, P6, P13 |
| Mist line | 11.91 m, 0.40 L, drains in about 30 s (was 10.96 m, 0.36 L, 27 s) [C7]. | P1, P13 |
| Structure | Steel 167 kg (was 143 kg before brackets and bolts) [G1]. Fabric off at 30 m/s: posts 0.14, panel bearer 0.02, purlins 0.07 (were 0.15), rear beam from the panel feet 0.11; anchors about 2.8 kN factored, unchanged [G13]. Fabric on at 15 m/s: long beams 0.88, unchanged [G14]. | P1, P5, P7 |
| Fixings | 79 bolts and anchors, 36 of them M8 into rivet nuts (was about 48) [H2]. Two added hand tools: a rivet nut tool and a bench vice. | P2 to P16 |
| Cost | BOM lines 1 to 5, 8 to 10, 12, 13 and 16 updated: $882.00 (was $773.00), $107 (13.8 %) over the $775 value-engineering target (`budget_usd`). R13 moves from at risk to over the value-engineering target. `budget_usd` is not changed; savings worth trying are in the register's Value engineering section. | Parts added for construction |
| Drawings | General arrangement CSH-DWG-001 Rev P4; making sketches CSH-DWG-101 to 116 added. | Follows the model |
| Documents | CSH-CAL-001 v0.3, CSH-PRC-001 v0.5, CSH-REQ-001 v0.5, BOM and BOM notes. | Follows the model |
| Concept media | Hero, exploded view, blueprint and 3D viewer regenerated from the new model. | Follows the model |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A2 | R14 lists the tools as a drill, angle grinder, spanners and a ladder; the constructable design adds a hand rivet nut tool and a bench vice (for the brace ends). | (a) add both to R14's tool list; (b) use through bolts instead of rivet nuts, which puts nuts under the cloth and can crush the tubes. | (a). |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CSH-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register CSH-DEC-001.
- Requirement status (CSH-CAL-001 v0.3): 1 over its value-engineering target (R13 cost), 2 at risk (R9 water hygiene, R16 nozzle scaling), 1 not verifiable at TRL 3 (R5 wetting), 13 met. Before this record it was none not met, 3 at risk (R9, R13, R16), 1 not verifiable and 13 met.
- The photoreal renders (`media/render-hero.png`, `render-exploded.png`, `render-detail.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept: posts on the 2.1 m grid, the panel in the middle of the rear half on top of the cloth, the tank against the post and the hose bypassing the filter. They need updating on Amish's Mac, where Blender is.
- Nothing here authorizes building, buying or testing; TRL 4 stays on hold by Amish's instruction.
