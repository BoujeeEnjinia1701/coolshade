---
doc_id: CSH-CAL-001
title: CoolShade sizing calculations
project: CoolShade
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (shade and space, headroom, misting and water, droplets and wetting, cooling, energy, wind and structure, handling, control and electrical, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: 'Constructable design (CSH-DDR-003): post grid, headroom, mist line, masses, panel support, rivet nuts, fixings and cost updated; R13 not met against $775'
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R14 row text updated for the tool list decided on 2026-10-02; no figures changed"
---

# CoolShade sizing calculations

On paper, CoolShade meets thirteen of its seventeen requirements (seven by calculation, four by design, one on published evidence and one, R10, on paper with the anchors to be confirmed per site), has two at risk (R9 water hygiene and R16 scaling), one that cannot be judged at TRL 3 (R5 wetting) and one over its value-engineering target: R13, cost, because the parts added to make the design buildable (CSH-DDR-003, version 0.3 of this note) bring the estimated parts cost to $882.00 against the $775 target (a hypothetical control target), $107 over; savings worth trying are in CSH-DEC-001. Version 0.3 also takes the constructable geometry: posts on a 2,800 x 2,350 mm grid, flattened-end knee braces with a lowest point of 2,223 mm, a longer mist line, the panel on a bearer and L-feet at the rear edge, and 167 kg of steel. Version 0.2 applies the recommendations Amish accepted on 2026-09-25 (CSH-DDR-002): R4 is restated as 2 °C while spraying (2.71 °C is met; it was 1.35 °C averaged against 2 °C, not met); R10 is restated as surviving 30 m/s with the fabric removed and keeping the fabric on only in forecast gusts below 15 m/s (met on paper; the original fabric-on 30 m/s case overloads the 50 mm roof beams about 3.5 times); the battery grows from 20 Ah to 25 Ah (1.26 design days without sun, was 1.005); and `budget_usd` rises from $700 to $775, against which the $773 parts cost is $2 under but at risk because the steel prices look low. The calculations changed four details of the TRL 2 concept: shorter knee braces for headroom, a vacuum breaker so that the mist line can drain past its anti-drip nozzles, a closed mist line loop, and a strap on the tank, which tips over in a 30 m/s gust when empty. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [G7], is the line of that script's output that carries it.

> **Safety:** These are first-principles screening estimates for a paper proof of concept. They are not a structural design to any code, they do not show that the mist is safe to breathe, and they do not replace an engineer's check of the frame, anchors and slab at a real site, or a water hygiene plan approved by the local health authority. See CSH-PRC-001, Safety.

## Scope and method

The note checks every requirement in CSH-REQ-001 v0.5 against the design in CSH-PRC-001 v0.5 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and derived dimensions, so the post grid, roof heights, brace geometry, nozzle heights and mist line length used here are the ones in the STEP files and in drawing CSH-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design day is unchanged from CSH-REQ-001: 38 °C air at 25 % relative humidity, clear sky, wind about 1 m/s, 5 h of misting demand and 4.5 peak sun hours. The humid edge is the wettest air in which the controller still mists: 32 °C at 60 % relative humidity.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Nozzles | Eight 0.4 mm swirl nozzles at 7 bar (100 psi), 4 L/h each; spray 20 s on, 20 s off (50 %) during 5 h of demand; 87 % of the sprayed water evaporates in the air | TRL 2 estimates; flow to confirm from the maker's data |
| Air | Density 1.15 kg/m³, specific heat 1,006 J/(kg K), latent heat 2.43 MJ/kg; control volume 3.0 m long and 2.0 m high crossed at the wind speed; vapor diffusivity 2.6 x 10⁻⁵ m²/s; viscosity 1.9 x 10⁻⁵ Pa s | Handbook values near 35 °C |
| Droplets | Surface at the wet-bulb temperature (Stull approximation); Stokes settling; nozzle jet carries droplets 300 mm below the tip before they move with the air; head height 1.5 m | Screening model; jet length assumed |
| Energy | Pump 60 W while spraying; controller and sensors 1.2 W continuous; normally open drain valve 5 W while held shut; 100 W panel, 4.5 peak sun hours, 0.75 system factor; 320 Wh battery (12.8 V 25 Ah, CSH-DDR-002), 80 % usable | TRL 2 estimates |
| Enclosure | 200 W/m² on its worst face under the cloth, absorptance 0.5, film coefficient 10 W/(m² K), 5 W internal loss; LiFePO4 charging stops above 45 °C | Screening values; typical cell data |
| Wind | 30 m/s gust, air 1.2 kg/m³; net normal force coefficient 1.2 on the whole roof with the fabric treated as solid; center of pressure a quarter of the depth off center; friction 0.04 on each face; drag 2.0 on square sections and 0.8 on the tank; roof edge band 100 mm | Conservative screening values, not a code check |
| Steel | S275 (275 MPa yield), density 7,850 kg/m³; partial factor 1.5 on wind, 0.9 on dead load | Common minimum grade for galvanized hollow sections |
| Fabric | Sags 5 % of its 2.4 m span under load | Assumed; knitted cloth stretch data needed |
| Tank | 8 kg empty | Assumed |
| Space | 0.5 m² per standing person; wheelchair space 0.8 x 1.2 m; existing bench 1.5 x 0.42 m | R1 and site context |

## A. Shade and space (R1)

- **Shade area.** The roof is 7.20 m² in plan and 7.26 m² on the slope [A1]. Its shadow is 7.20 m² with the sun overhead and at least 6.30 m² for any sun elevation of 45° or more [A2], so R1's 6 m² is met.
- **Where the shadow falls.** With the sun at 60° elevation from the street side, only 2.11 m² of the shadow falls inside the canopy's own footprint; from along the curb, 3.33 m² [A2]. The shaded waiting spot moves with the sun, so the sun path check at each site (R1's verification) matters more than the roof area.
- **Space.** The clear floor between the posts is 2.72 x 2.27 m (6.17 m²; it was 2.72 x 2.02 m before the posts moved out under CSH-DDR-003). After the tank and pump, the bench and one wheelchair space, 4.27 m² remains, room for eight people standing plus three seated [A3]. R1 (six people and one wheelchair space) is met.

## B. Headroom (R2)

- The long beams are horizontal and sit on the posts at the roof's edges (CSH-DDR-003); their underside is 2,912 mm at the front and 2,618 mm at the rear [B1].
- At TRL 2 the rear knee braces dropped 520 mm below the beam, leaving about 2,110 mm at the post face, below R2's 2,200 mm; the TRL 3 concept shortened them to 400 mm (low end 2,234 mm). The constructable braces have flattened ends 45 mm long bolted flat to the post and beam, so their bends are 350 mm down the post and 350 mm along the beam, and the bottom of the lower flattened end, the lowest point overhead, is at 2,223 mm at the rear posts and 2,517 mm at the front posts [B2].
- The nozzle tips are at 2,559 mm (rear row) and 2,835 mm (front row); the sensor arm is at 2,400 mm, and the shield's lowest plate at 2,266 mm, outboard of the front right post [B3]. R2 is met, with 23 mm to spare at the rear braces.

## C. Misting and water (R7, R15, R9)

- **Nozzle flow.** A 0.4 mm orifice at 7 bar would pass 16.9 L/h as an ideal jet. The assumed 4 L/h implies a discharge coefficient of 0.24, which is plausible for a swirl nozzle that trades flow for fine atomization, but it must be confirmed from the maker's data [C1].
- **Daily water.** Eight nozzles spray 32 L/h, or 16 L/h averaged over the cycle, so the design day sprays 80 L and uses 85 L with the 5 L flush; about 69.6 L evaporates [C2]. R7 (100 L per day) holds up to 4.75 L/h per nozzle. At 5 L/h the day would use 105 L and R7 would not be met [C3].
- **Tank.** A full 120 L tank lasts 1.41 design days [C4]; R15 is met.
- **Drain-and-refill routine.** R9 limits tank water to 48 h old. Topping up a part-full tank never guarantees this, so the routine is to drain the residual and refill. Filling 95 L each design day leaves about 10 L to drain at the next visit, keeps every liter under 24 h old and draws 95 L per day; filling to 120 L and draining the rest would draw 120 L and miss R7 [C5].
- **Pump.** The hydraulic power is 6.2 W, so the assumed 60 W draw implies 10 % wire-to-water efficiency [C6], a conservative figure for a small diaphragm pump near its pressure limit.
- **Draining the mist line.** The line is a closed loop 70 mm inboard of the long beams and under the end beams, plus a down pipe to the drain valve: 11.91 m of 6.5 mm bore, holding 0.40 L. Through a 3 mm valve orifice at 0.5 m head it drains in about 30 s [C7], well inside R9's 5 min, but only if air can get in. Anti-drip nozzles close when the pressure drops, so the TRL 2 line would have held its water. A vacuum breaker at the front, highest point of the loop is added to BOM item 14.

## D. Droplets and wetting (R5)

A droplet stops being a wetting risk once it has evaporated. On the design day the air can take up 8.9 g/m³ more water vapor at the droplet surface, and on the humid edge only 3.8 g/m³ [D1]. The lifetime of a droplet grows with the square of its diameter and its fall distance with the fourth power, so size is everything:

*Table 2. Droplet lifetime and still-air fall [D2].*

| Diameter | Design day: life, fall | Humid edge: life, fall |
| --- | --- | --- |
| 30 µm | 0.48 s, 6 mm | 1.14 s, 15 mm |
| 50 µm | 1.34 s, 48 mm | 3.17 s, 114 mm |
| 80 µm | 3.44 s, 316 mm | 8.12 s, 745 mm |
| 100 µm | 5.38 s, 771 mm | 12.68 s, 1,819 mm |

Between the end of the jet under the rear nozzles and head height there are 759 mm. Droplets up to about 100 µm evaporate before reaching a head on the design day, and up to about 80 µm on the humid edge [D3]. R5 is therefore met only if the nozzle's droplet spectrum has nearly all its volume (Dv0.9) below about 80 µm at 7 bar. No maker's droplet data are in hand, so R5 cannot be judged at TRL 3. At 1 m/s wind, a 50 µm droplet drifts about 1.3 m before it is gone, and larger ones leave the canopy [D2]; this is the drift loss in the water balance.

## E. Cooling (R4, R3)

- **Heat absorbed.** Evaporation absorbs 9.40 kW averaged over the cycle and 18.8 kW while spraying; 6.90 kg/s of air crosses the zone at 1 m/s [E1].
- **Air temperature drop.** The drop is 1.35 °C averaged and 2.71 °C while spraying. The air takes 3 s to cross the canopy, less than one 20 s pulse, so people feel the pulses rather than the average [E2].
- **R4.** R4 is restated under CSH-DDR-002 as a drop of 2 °C or more while spraying. At the design day's 1 m/s the drop while spraying is 2.71 °C, and it stays at 2 °C or more in wind up to 1.35 m/s, so R4 is met. The former averaged target would have needed wind below 0.68 m/s; at 0.3 m/s the averaged drop would be 4.5 °C, but wetting risk rises in still air [E3].
- **Limits.** The design-day wet bulb is 23.0 °C, 15.0 °C below the air, so misting is far from saturating the air; it adds 0.56 g/kg of humidity [E4]. The design day absorbs about 47 kWh of heat [E5].
- **Radiant heat (R3).** CoolShade's main benefit remains the shade. The published figure for shade sails in Tempe is a 17.3 °C drop in mean radiant temperature ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)). R3 is taken as met on that evidence, but it is unverified for this fabric, and a globe thermometer measurement is needed later.

## F. Energy (R8)

- **Use.** The pump takes 150 Wh, the controller and sensors 28.8 Wh and the normally open drain valve 25 Wh while held shut: 203.8 Wh per design day [F1].
- **Harvest and storage.** The panel yields 337.5 Wh, 1.66 times the use. The battery is now 12.8 V 25 Ah (CSH-DDR-002); its 256.0 Wh usable covers 1.256 design days without sun [F2]. With the former 20 Ah battery it was 204.8 Wh and 1.005 days, a margin of 1 Wh.
- **Latching valve option.** A latching drain valve would cut the use to 179.3 Wh and give 1.43 days with the 25 Ah battery, but a latching valve does not open by itself when power fails, so the line could sit full of warm water [F3]. The normally open valve is kept (CSH-DDR-002).
- **Currents.** Peak charge current is 7.4 A (the MPPT is rated 10 A) and the pump draws 4.7 A; the battery recharges from empty in 0.76 design days of sun [F4].
- **Heat.** The enclosure runs about 3.6 K above the air: 41.6 °C on the design day but 48.6 °C in 45 °C air. The battery stops charging above 45 °C, so charging stops whenever the air is above about 41.4 °C [F5]. On the hottest days the battery can only discharge; the design day (38 °C) is below that limit. R8 is met, with the hot-day charge limit noted.

## G. Structure and wind (R10)

- **Mass.** The steel weighs about 167 kg before bolts: four posts 79.9 kg (a front post 21.0 kg), braces 4.2 kg, long beams, end beams and panel bearer 35.1 kg, purlins 11.1 kg, base plates 15.2 kg, base cleats 11.9 kg, head and frame cleats 2.6 kg, and the equipment plate, enclosure rails and sensor arm 6.9 kg. The dead load on the anchors, with panel, rails, fabric, equipment and pump, is 167 kg (1.64 kN) [G1].
- **Wind.** A 30 m/s (108 km/h) gust gives 540 Pa, and with the fabric treated as solid, a normal force of 4.67 kN on the roof [G2].
- **Posts.** The horizontal load at roof level is 1.21 kN (the tilted roof, fabric friction and the roof edge) plus 86 N/m of drag on each post. As cantilevers with no help from the braces, the posts see 1.24 kN m each [G3], or 82 MPa with the 1.5 factor, a utilization of 0.30 of S275 [G4] (the posts are 13 mm longer at the front than in v0.2). The TRL 2 figure of about 144 MPa came from applying the whole normal force sideways; that is not a physical load case, but even that bound gives a utilization of 0.81 [G5].
- **Roof beams in bending.** If the long beams simply carry half the roof pressure over the 2.8 m post spacing, they reach a utilization of 0.70 [G6].
- **Fabric edge pull.** A tensioned fabric does not load the beams like a floor. It pulls inward on its edges with a force that grows as its sag shrinks. At 5 % sag the edge pull is 3.89 kN/m on each long beam, which bends the 50 x 50 x 2 mm beam sideways at a utilization of 3.52 [G7]. The beams can take 1.11 kN/m. To stay within that, the fabric would need 422 mm of sag (18 % of its span), or its porosity would need to relieve 72 % of the pressure, or it would have to come off above gusts of about 16 m/s (58 km/h) [G8].
- **Original R10 not met** on the conservative, solid-fabric case. Real knitted cloth is porous and stretches, both of which reduce the edge pull, but no data are in hand to show by how much. Amish accepted the recommendation to restate R10 (CSH-DDR-002): the frame and anchors must survive 30 m/s with the fabric removed, and the fabric is fitted only when forecast gusts are below 15 m/s (54 km/h). Removing the fabric before storms (decision D6) is therefore load-bearing, not a convenience.
- **Restated R10, fabric removed, 30 m/s.** The panel, as a flat plate of 0.67 m², takes 0.43 kN, 109 N at each of its four L-feet; the horizontal load at roof level is 0.33 kN; the post base moment is 0.60 kN m, a utilization of 0.14. The panel now stands at the rear edge on two feet on the panel bearer and two on the rear beam (CSH-DDR-003): the bearer reaches 0.02, the purlins carrying it 0.07 and the rear beam 0.11. The worst post lifts with 0.19 kN against 0.41 kN of dead load per post. Each anchor needs about 2.8 kN factored, mostly from the base moment [G13].
- **Rivet nuts.** Bolts into the closed beams go into M8 steel rivet nuts. The largest pull on one is about 0.16 kN factored, from the worst post's uplift shared by its two head cleat nuts or from one L-foot [G15]; the chosen rivet nut's pull-out rating in a 2 mm wall must be well above this, which is typical of steel rivet nuts but is to be confirmed from the maker's data.
- **Restated R10, fabric fitted, 15 m/s.** The pressure is 135 Pa, a quarter of the 30 m/s value. The fabric's edge pull brings the long beams to a utilization of 0.88 on the same solid-fabric, 5 % sag case; the posts are at 0.07 and each anchor needs about 1.5 kN factored [G14]. The restated R10 is met on paper; the anchors still depend on the slab at each site. A cord lacing that releases the fabric at a set load was recommended for study at TRL 4, which is on hold.
- **Anchors, original fabric-on 30 m/s case.** With the center of pressure 0.6 m off center, the worst post lifts with 1.76 kN, or 1.35 kN net of dead load and 2.27 kN factored [G9]. Adding the base moment over the 160 mm bolt pitch, each M16 anchor needs a factored tension of about 6.4 kN [G10]. Whether a given anchor in a given slab can provide it depends on the slab's thickness, concrete and edge distances, so the anchors cannot be verified at TRL 3. Under the restated R10 the governing anchor load falls to about 2.8 kN [G13]. Without anchors, 309 kg of ballast would be needed [G11], so anchoring stays mandatory.
- **Tank.** An empty 8 kg tank sees 163 N of drag; its overturning moment of 57 N m is well above the 21 N m that holds it down, so it would tip [G12]. A strap to the rear left post and two small anchors are added to BOM item 13.

## H. Handling (R17, R14)

The heaviest part is a front post at 21.0 kg (its brace now bolts on separately), against R17's 40 kg; a long beam weighs 9.0 kg and the panel 7 kg. A full tank weighs about 128 kg and must be drained before it is moved [H1]. The constructable design has 79 bolts and anchors, 36 of them M8 bolts into rivet nuts, and no welds [H2], so R14 is met by design; it needs two hand tools beyond R14's list (a rivet nut tool and a vice for the brace ends; open decision in CSH-DEC-001), and the 2-day build time cannot be checked on paper.

## I. Control, electrical and hygiene (R6, R12, R9)

- **Control.** A 10 s control loop with a 20 s debounce on the temperature and humidity conditions stops the spray within 30 s of a condition failing, inside R6's 60 s [I1]. The lag of the sensor in its radiation shield is not known.
- **Electrical.** The largest continuous battery current is 7.4 A while charging and 5.2 A while misting, so a 15 A terminal fuse has a margin of 2.0 [I2]. R12 is met by design.
- **Tank temperature.** On design days the tank water settles near the daily mean air temperature plus some solar gain, about 34 °C (with an assumed 26 °C night), inside the 20 to 50 °C range in which *Legionella* grows ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)) [I3]. R9 stays at risk: the design controls water age (under 24 h with the routine) and line draining (about 27 s), but not temperature.

## J. Cost (R13)

The BOM has 16 lines, all priced, totaling an estimated $882.00 against the $775 value-engineering target (`budget_usd`, set on 2026-09-25 under CSH-DDR-002; a hypothetical control target, not a limit): $107.00 (13.8 %) over [J1]. The concept came to $773.00; the parts added to make it buildable (CSH-DDR-003: cleats, rivet nuts, panel bearer and mounting kit, base cleats, equipment plate, enclosure rails, sensor arm, line clips, tank level switch, I2C extender, cloth notch and more fixings) add $109. The steel lines (1, 2 and 4) come to $269 for about 167 kg, about $1.61/kg including cutting, drilling and galvanizing, which still looks low for small quantities [J2]. R13 is over the value-engineering target by $107; savings worth trying are in CSH-DEC-001. `budget_usd` is not changed.

## K. Results against every requirement

*Table 3. Requirement status from this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R13 | Cost | $882 [J1] | $775 or less (value-engineering target) | **Over the value-engineering target by $107** (13.8 %) after the parts added for construction |
| R9 | Water hygiene | Water under 24 h old with the routine [C5]; line drains in about 30 s [C7]; tank about 34 °C [I3] | Age 48 h or less; drained within 5 min | At risk: water sits in the *Legionella* growth range |
| R16 | Maintenance | Scaling of 0.4 mm orifices | Descaling interval 1 month or more | At risk; not verifiable at TRL 3 |
| R5 | No wetting | Needs Dv0.9 below about 80 µm at 7 bar [D3] | No wetting at 1.5 m | Not verifiable at TRL 3 (no droplet data) |
| R4 | Air cooling from misting | 2.71 °C while spraying (1.35 °C averaged) at 1 m/s [E2] | 2 °C or more while spraying (restated) | Met; holds to 1.35 m/s [E3] |
| R8 | Energy autonomy | 203.8 Wh used, 337.5 Wh harvested; 25 Ah battery 1.256 days [F2] | Energy-neutral; 1 day without sun | Met; no charging above about 41 °C air [F5] |
| R10 | Wind resistance | Fabric off at 30 m/s: posts 0.14, bearer 0.02, purlins 0.07 [G13]; fabric on at 15 m/s: long beams 0.88 [G14]; anchors about 2.8 kN each | Restated: survive 30 m/s with fabric removed; fabric on only below 15 m/s | Met on paper; anchors to be confirmed per site. Original fabric-on case: beams 3.52 [G7] |
| R1 | Shaded waiting area | 6.30 m² or more shadow above 45° sun [A2]; 8 standing + 3 seated + wheelchair [A3] | 6 m²; 6 people and a wheelchair | Met |
| R2 | Headroom | 2,223 mm at the rear braces' flattened ends [B2] | 2,200 mm or more | Met |
| R3 | Radiant heat reduction | About 17.3 °C for shade sails (literature) | 15 °C or more | Met on published evidence; unverified for this fabric |
| R6 | Smart activation | Stop within 30 s [I1] | Within 60 s | Met by design |
| R7 | Water use | 85 L used, 95 L drawn [C2], [C5] | 100 L or less | Met at 4 L/h per nozzle; at risk above 4.75 L/h [C3] |
| R11 | Privacy | PIR only, no link fitted | No camera or microphone | Met by design |
| R12 | Electrical safety | 12 V DC, 15 A fuse, margin 2.0 [I2] | 12 V, fused, IP65, BMS | Met by design |
| R14 | Buildability | Bolted, 79 fasteners [H2] | No welding; 2 days | Met by design; rivet nut tool and bench vice in R14 since 2026-10-02; time unverified |
| R15 | Refill interval | 1.41 design days [C4] | 1 day or more | Met |
| R17 | Movability | Heaviest part 21.0 kg [H1] | 40 kg or less | Met |

In summary: 1 over its value-engineering target (R13), 2 at risk (R9, R16), 1 not verifiable at TRL 3 (R5) and 13 met (R1, R2, R3, R4, R6, R7, R8, R10, R11, R12, R14, R15, R17). In v0.2, before CSH-DDR-003, R13 was at risk ($773 against $775). In v0.1, before CSH-DDR-002, the count was 3 not met (R4, R10, R13), 3 at risk (R8, R9, R16), 1 not verifiable and 10 met.

## Checks against the TRL 2 figures

- Water (85 L), tank endurance (1.4 days), energy use (about 205 Wh), harvest (about 340 Wh), battery (about 205 Wh) and cooling (1.4 °C averaged and 2.7 °C while spraying) all stand.
- Parts cost rises from about $735 to $758 at TRL 3, and to $773 with the 25 Ah battery (v0.2).
- The post stress of about 144 MPa at TRL 2 was an upper bound; the physical case gives 54 MPa unfactored. R10 moves from "unverified" to "not met" because of the fabric edge pull, which the TRL 2 estimate did not consider.
- Headroom under the rear braces rises from about 2.1 m to 2,234 mm, so R2 is now met with margin.
- The TRL 2 structure mass of about 130 kg becomes about 143 kg of steel before brackets and bolts.
- v0.3 (constructable design, CSH-DDR-003): steel 167 kg with cleats and plates, headroom 2,223 mm, mist line 11.91 m, parts $882.
