---
doc_id: CSH-PRC-001
title: CoolShade design precis
project: CoolShade
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, components, first-order numbers, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from CSH-CAL-001 and CSH-DDR-001 (numbers checked, shorter knee braces, vacuum breaker, closed mist line loop, tank strap, design choices adopted for TRL 3, GA drawing CSH-DWG-001)
---

# CoolShade design precis

## Summary

CoolShade is a bolted steel shade canopy, 3.0 x 2.4 m in plan, with a knitted shade cloth roof, a 100 W solar panel, a 12 V battery and a low-pressure misting line. It gives shade all day and mists only when the air is hot and dry enough for misting to help and a person is waiting. The TRL 3 calculations (CSH-CAL-001) give, for a hot, dry design day (38 °C, 25 % relative humidity), 85 L of water and 203.8 Wh of electricity per day, an average air temperature drop of 1.35 °C at 1 m/s wind (2.71 °C while spraying) and, from published shade sail data, a drop in mean radiant temperature of about 17 °C, which is where most of the relief comes from. Three requirements are not met: air cooling at 1 m/s (R4), wind resistance with the fabric fitted (R10, because of the fabric's edge pull on the roof beams) and cost (R13, $758 against the $700 budget and the proposed $750). The design choices below are adopted for TRL 3 work under Amish's 2026-09-25 instruction, open for his review (CSH-DDR-001).

![Hero render](../media/hero.png)

*Figure 1. CoolShade at a curbside stop next to an existing bench, with a 1.75 m person for scale. Kit parts are colored; the street and bench are grey.*

## How it works

1. **Shade.** Four 80 mm square steel posts on a 2.8 x 2.1 m grid carry a mono-pitch roof frame (7.1°, high edge at the street) with knitted HDPE shade cloth. The cloth blocks most direct sun while letting hot air escape.
2. **Harvest and store.** A 100 W panel on rails over the rear half of the roof charges a 12.8 V, 20 Ah LiFePO4 battery through an MPPT controller. Everything runs at 12 V DC.
3. **Sense.** A temperature and humidity sensor in a radiation shield on an arm off the front post measures the ambient air outside the mist zone. A passive infrared sensor under the front beam detects whether anyone is waiting. No camera or microphone is fitted.
4. **Decide.** The controller mists only when air temperature is 32 °C or more, relative humidity is 60 % or less, someone has been detected in the last 2 min, and the tank is above its low level (thresholds adopted for TRL 3, CSH-DDR-001 D2). A 10 s control loop with a 20 s debounce stops the spray within 30 s of a condition failing. In humid air it does not mist, because misting would add little cooling and wet people.
5. **Mist.** A 12 V diaphragm pump draws from a 120 L opaque tank through a 5 µm filter and pushes water at about 7 bar through a closed loop of mist line under all four roof beams to eight anti-drip nozzles under the front and rear beams, in cycles of 20 s on and 20 s off. Fine droplets evaporate and cool the air under the canopy.
6. **Drain.** When the pump stops at the end of a session, a normally open drain valve at the low point empties the line in about 30 s, while a vacuum breaker at the front, highest point of the loop lets air in past the anti-drip nozzles. On design days the tank is drained of its residual and refilled with about 95 L daily, so no water is more than 24 h old, and it is disinfected weekly.

![Water flow](../media/flow.png)

*Figure 2. Daily water flow on the design day, in liters. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

Table 1. Main components.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Posts with knee braces | 80 x 80 x 3 mm galvanized SHS, 2.62 to 2.89 m, one 32 mm tube brace each, 400 mm down and 400 mm along the beam | Utilization 0.29 in a 30 m/s gust (CSH-CAL-001) |
| 2 | Roof frame | 50 x 50 mm SHS perimeter, two 40 x 40 mm purlins, bolted brackets | About 7° mono-pitch |
| 3 | Shade fabric | Knitted HDPE, about 90 % UV block, 3.0 x 2.4 m, corded to the frame | Removable before storms (CSH-DDR-001, D6) |
| 4 | Base plates and anchors | 220 x 220 x 10 mm plates, four M16 anchors each, into an existing slab | Footing checked per site |
| 5 | Solar panel | 100 W monocrystalline on two rails | About 1,000 x 670 mm |
| 6 | Battery | 12.8 V, 20 Ah LiFePO4 with BMS and cold-charge cutoff | Inside item 8, fused |
| 7 | MPPT charge controller | 12 V, 10 A, LiFePO4 profile | Inside item 8 |
| 8 | Controller and enclosure | Lockable IP65 box on the rear right post, about 1.45 to 1.85 m high; microcontroller, pump and valve drivers, fuses | Firmware not started (TRL 4) |
| 9 | Sensor head | SHT4x-class temperature and humidity sensor in a multi-plate shield, plus a PIR presence sensor | No camera or microphone |
| 10 | Misting pump | 12 V diaphragm pump, about 7 bar, about 60 W, pressure switch | Bracketed to the rear left post |
| 11 | Filter and check valve | 5 µm cartridge, inlet strainer | Protects 0.4 mm nozzles |
| 12 | Mist line and nozzles | About 11 m of 9.5 mm (3/8 in) line as a closed loop, 8 brass anti-drip nozzles, about 0.4 mm | 32 L/h while spraying at 4 L/h per nozzle (to confirm) |
| 13 | Water tank | 120 L, opaque, food-grade, lockable, strapped to the rear left post | Optional mains float valve with backflow preventer; strap because an empty tank tips in a 30 m/s gust |
| 14 | Drain valve and vacuum breaker | 12 V normally open solenoid at the low point; air admittance valve at the loop's high point | Empties the line in about 30 s after every session |
| 15 | Hose and wiring harness | Suction and delivery hose, outdoor cable, glands | |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. Items 6 and 7 are shown out of the enclosure (item 8) that houses them.*

![Concept blueprint](../media/concept-blueprint.png)

*Figure 4. Concept sheet CSH-DWG-010 with orthographic and isometric views and key figures.*

The general arrangement drawing CSH-DWG-001 (Rev P1, `cad/drawings/CSH-DWG-001.pdf`) gives the main dimensions and interfaces from the parametric model `cad/src/model.py`. It is preliminary and not for fabrication.

No cutaway is provided: the canopy is open, and the only enclosed parts (items 6 to 8) are shown in the exploded view.

## Numbers checked at TRL 3

All values come from CSH-CAL-001 and its script `docs/04-calcs/sizing.py`; the tags in brackets are lines of its output. They are first-principles estimates, not measurements.

### Water and misting

Assumptions: eight nozzles at 4 L/h each at 7 bar (to be checked against nozzle datasheets; this implies a discharge coefficient of 0.24 for a 0.4 mm orifice), 20 s on and 20 s off while active (50 % duty), 5 h of active misting on the design day, 87 % of sprayed water evaporating in the air, and a daily flush of 5 L.

Table 2. Water use on the design day.

| Quantity | Value | Basis |
| --- | --- | --- |
| Flow while spraying | 32 L/h | 8 x 4 L/h [C2] |
| Average flow while active | 16 L/h | 50 % duty |
| Sprayed per day | 80 L | 16 L/h x 5 h |
| Used per day, with flush | 85 L | 80 + 5 L |
| Drawn per day with the drain-and-refill routine | 95 L | Daily fill; about 10 L residual drained [C5] |
| Evaporated in the air | 69.6 L | 87 % of 80 L |
| Tank endurance | 1.41 design days | 120 L / 85 L [C4] |
| Mist line volume and drain time | 0.36 L, about 27 s | 10.96 m of 6.5 mm bore; 3 mm valve orifice [C7] |

R7 holds up to 4.75 L/h per nozzle [C3]. Whether the nozzles keep people dry (R5) depends on droplet size: droplets up to about 100 µm evaporate before reaching head height on the design day, but only up to about 81 µm in the most humid air the controller allows [D3]. No droplet data are in hand.

### Cooling

Assumptions: latent heat of evaporation 2.43 MJ/kg; air density 1.15 kg/m³ and specific heat 1,006 J/(kg K) at 35 °C; air crossing a control volume 3.0 m long and 2.0 m high at the wind speed; all evaporation within that volume.

Table 3. Cooling on the design day.

| Quantity | Value | Basis |
| --- | --- | --- |
| Heat absorbed by evaporation, averaged | 9.40 kW | 13.9 L/h evaporated x 2.43 MJ/kg [E1] |
| Heat absorbed while spraying | 18.8 kW | 27.8 L/h evaporated |
| Air through the zone at 1 m/s | 6.90 kg/s | 6 m² x 1 m/s x 1.15 kg/m³ |
| Air temperature drop at 1 m/s | 1.35 °C averaged, 2.71 °C while spraying | Q / (m x cp) [E2] |
| Wind speed for a 2 °C averaged drop | 0.68 m/s or less | Same method [E3] |
| Air temperature drop at 0.3 m/s | 4.5 °C averaged | Wetting risk rises in still air [E3] |
| Wet-bulb temperature, 38 °C and 25 % RH | 23.0 °C | Stull approximation; far from the limit [E4] |
| Humidity added at 1 m/s | 0.56 g/kg | Small against about 10 g/kg ambient |
| Heat absorbed per day | 47 kWh | 69.6 L x 2.43 MJ/kg [E5] |
| Mean radiant temperature drop from shade | about 17 °C | Shade sails in Tempe ([Middel et al., 2021](https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml)) |

The shade does most of the work: a 17 °C drop in mean radiant temperature matters more to a person standing in the sun than a 1 to 3 °C drop in air temperature. Misting adds a noticeable but smaller benefit, and only in dry air. This is why the controller must never mist in humid air, and why R4 is not met at 1 m/s wind. Fans were left out for TRL 3 (CSH-DDR-001, D3); a revisit is listed for Amish in `docs/REVIEW.md`.

### Energy

Table 4. Daily energy budget on the design day.

| Load or source | Value | Basis |
| --- | --- | --- |
| Pump | 150 Wh | 60 W x 50 % x 5 h [F1] |
| Controller and sensors | 28.8 Wh | 1.2 W x 24 h |
| Drain valve held closed while active | 25 Wh | 5 W x 5 h |
| **Total use** | **203.8 Wh** | |
| Panel harvest | 337.5 Wh | 100 W x 4.5 h x 0.75 [F2] |
| Battery usable | 204.8 Wh | 256 Wh x 80 %; 1.005 design days |

The panel covers the design day 1.66 times, but the battery covers one design day without sun with only 1 Wh to spare, so R8 is at risk. A latching drain valve would save 24.5 Wh, but it would not open by itself if power failed [F3]. The enclosure runs about 3.6 K above the air, so the battery stops charging (at 45 °C) when the air is above about 41.4 °C [F5].

### Structure and wind

Assumptions: 30 m/s gust, air density 1.2 kg/m³, net normal force coefficient 1.2 on the roof with the fabric treated as solid, center of pressure a quarter of the depth off center, S275 steel with a partial factor of 1.5 on wind, fabric sag 5 % of its span.

Table 5. Wind check.

| Quantity | Value | Basis |
| --- | --- | --- |
| Dynamic pressure | 540 Pa | 0.5 x 1.2 x 30² [G2] |
| Normal force on the roof | 4.67 kN | 540 Pa x 1.2 x 7.2 m² |
| Post base moment | 1.24 kN m | Horizontal roof load 1.21 kN plus post drag, cantilevers [G3] |
| Post stress, 80 x 80 x 3 SHS | 54 MPa, utilization 0.29 factored | Z = 22,861 mm³ [G4] |
| Long beam, roof pressure as a simple span | Utilization 0.70 | 50 x 50 x 2 SHS over 2.8 m [G6] |
| Long beam, fabric edge pull at 5 % sag | 3.89 kN/m, utilization 3.52 | Membrane tension p L² / (8 f) [G7] |
| Fabric-on gust limit for the beams | about 16 m/s (58 km/h) | Edge pull the beams can take, 1.11 kN/m [G8] |
| Anchor tension, factored | about 6.4 kN per M16 anchor | Uplift plus base moment [G10] |
| Ballast needed if not anchored | 324 kg | Uplift less dead load [G11] |

The posts are adequate. The weak point is the fabric: a tensioned cloth pulls its edges inward far harder than the pressure alone suggests, and on the conservative solid-fabric case it overloads the 50 mm long beams in a 30 m/s gust, so R10 is not met. Porosity and stretch would reduce the pull, but no data are in hand. Taking the fabric off before storms (CSH-DDR-001, D6) is therefore structurally necessary. The anchors must be checked against the chosen anchor's data and the actual slab. The unit must be anchored; ballast alone is impractical. An empty tank would tip over in the same gust, so it is strapped to the rear left post [G12].

### Mass and cost

- Steel about 143 kg before brackets and bolts (a front post with its brace 22.0 kg, the heaviest part); panel about 7 kg; battery about 2.5 kg; full tank about 128 kg [G1, H1].
- Parts $758 (indicative, see `bom/bom.csv`), against the $700 `budget_usd` and the $750 proposed at TRL 2, which awaits Amish [J1]. The steel prices look low for small quantities, so cost is at risk of rising [J2].

## Key design choices

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review (CSH-DDR-001).

1. Low-pressure (about 7 bar) 12 V misting rather than high-pressure (about 70 bar) mains misting, so the unit runs off-grid and stays low-voltage. The trade-off is larger droplets and a higher wetting risk.
2. Humidity and presence gating with fixed thresholds, so water and energy are used only when misting helps someone.
3. Tank supply with an optional mains connection, so it can go anywhere.
4. Drain-after-use, a vacuum breaker and a daily drain-and-refill as the main defenses against *Legionella*.
5. Knitted shade cloth rather than a solid roof: cheaper, lighter and lets hot air escape, but it does not keep rain off, and it must come off before storms.
6. Bolted, movable frame on existing slabs, so a city can trial it at a site and move it.
7. No fans and no status link in the first prototype.

## Integration with other lab projects

- **HeatMap Node** measures street-level heat stress and can show where a CoolShade would help most, and whether it did.
- **FieldNode** could provide an optional LoRaWAN status link (counts and levels only). Its 6 W panel is far too small to run the pump, so CoolShade keeps its own power system. No link is fitted in the first prototype (CSH-DDR-001, D7), so CoolShade places no interface demands on FieldNode.

## Safety

> **Safety:** Misting is an aerosol, and *Legionella* grows in water at 20 to 50 °C and infects people who inhale contaminated mist ([WHO](https://www.who.int/news-room/fact-sheets/detail/legionellosis)). Use potable water only; keep the tank opaque, shaded and locked; drain the line after every session; drain the tank's residual and refill it daily; disinfect weekly; and stop misting if the water is not maintained. A site owner must name a responsible person for water hygiene.
>
> **Safety:** The 12.8 V LiFePO4 battery can overheat and burn if shorted, damaged or charged outside its limits. Fuse it at the terminal, use a BMS with cold-charge cutoff, keep it in the ventilated, locked enclosure, and never install a damaged or wet battery.
>
> **Safety:** The pump line runs at about 7 bar. Depressurize before opening fittings, and wear eye protection when working on it.
>
> **Safety:** The canopy is a wind-loaded structure. Anchor it to a checked slab or footing, strap the tank, remove the fabric before forecast storms (on the conservative calculation the roof beams are overloaded with the fabric on above gusts of about 16 m/s), and inspect bolts and anchors regularly. Building it is work at height with heavy steel; use two people, stable ladders and gloves, and deburr all cut edges.
>
> **Safety:** Wet surfaces can be slippery. Set nozzles and duty cycle so people and the ground stay dry; stop misting and adjust if puddles form.
>
> **Safety:** CoolShade is shade and local cooling, not a medical intervention or a cooling center. People with heat illness need medical help.

## Open questions

- [ ] Nozzle flow and droplet spectrum at 7 bar from the maker's data (R5, R7).
- [ ] Fabric porosity and stretch under wind, which decide the fabric's edge pull (R10); or a fabric-on wind limit.
- [ ] Whether to add small 12 V fans to mix cooled air down into the waiting zone, at about 20 to 40 W extra (R4).
- [ ] Water hygiene plan acceptable to the local health authority, including sampling (R9).
- [ ] Hard water scaling and a descaling method (R16).
- [ ] Site anchor details on different slabs; footing option where no slab exists.
- [ ] Budget: $758 against $700 and the proposed $750 (R13).
- [ ] First site type and co-design partner (proposed, awaiting Amish).
