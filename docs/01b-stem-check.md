---
doc_id: CSH-STM-001
title: CoolShade STEM check
project: CoolShade
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade, on the TRL 3 design (CSH-CAL-001 v0.6); one detail failed and was fixed under the standing instruction (CSH-DEC-001 D9); earlier fixes recorded; independent review recorded"
---

# CoolShade STEM check

Verdict: the working principle (shade, then a 7 bar water mist that evaporates in hot, dry air and cools it, switched on only when it is hot, dry and someone is waiting) sits within known science, but most of the detail still has to be shown. Of the 21 claims of option A, **8 are within known science and 13 remain plausible, to confirm with maker's data, a site or field measurements at TRL 4**: S1 (how much of the 18.8 kW cools the zone), S2 (mixing), S4 (droplet size and wetting, the one most likely to fail), S10 (battery reserve at end of life), S11 (the battery in the heat), S12 (scale in hard water), S13 (radiant benefit of this cloth), S14 (*Legionella* control), S15 (a PIR sensor in air near body temperature), S17 (the fabric at 15 m/s, 0.88 of the limit), S19 (the tank strap), S20 (anchors in the site slab) and S21 (the rivet nut rating). None fails. One detail failed in this check and was fixed under Amish's standing instruction of 2026-10-23: the grey enclosure ran 3.6 K above the air and stopped charging the battery above 41.4 °C air; a white enclosure (CSH-DEC-001 D9) gives 2.3 K and 42.7 °C in the cloth's shade, a partial fix, because in direct late sun the rise is larger (S11). Two more details failed in earlier sessions and are in the design (the fabric at 30 m/s and the unstrapped tank, Table 2). The independent review (below) downgraded S1, S11 and S13 from within to plausible. The rows for options B and C (S22 to S26) are screens of their principles: 2 within, 3 plausible. `stem_check` stays **open** because the plausible rows need field data. Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which imports `docs/04-calcs/sizing.py`.

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv`).

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | The mist absorbs about 18.8 kW from the air while spraying | Physics | Thermodynamics and heat transfer | Q = m_dot x 0.87 evaporated x latent heat (2.43 MJ/kg) for 8 nozzles x 4 L/h = 18.8 kW; the 0.87 evaporated share is an estimate that falls as the droplets get bigger (S4), and drops that drift out of the zone (CSH-CAL-001 D2) cool air outside it, so the share that cools the waiting zone is a range, not a point | Arithmetic checks out (independent review); the evaporated share inside the zone needs the nozzle's droplet spectrum | Plausible, to confirm at TRL 3 | CSH-CAL-001 E1 |
| S2 | The air in the waiting zone is at least 2 °C cooler while spraying (2.71 °C computed) | Physics | Thermodynamics and heat transfer | Sensible heat removed from a 3 x 2 m control volume crossed by air at 1 m/s: dT = Q / (m_dot cp); assumes the mist mixes through the whole volume, which real spray plumes do not (CSH-PRS-001 assumptions); the control volume's 3 m is used both as the frontal width and as the transit length, so the drop moves by about 25 % with the wind direction | 2.71 °C >= 2 °C | Plausible, to confirm at TRL 3 | CSH-CAL-001 E2, E3 |
| S3 | Misting cannot cool the air below the wet bulb (design day: 15 °C below ambient) | Physics | Thermodynamics and heat transfer | Adiabatic saturation limit: dry-bulb depression is at most T_air - T_wetbulb (Stull wet bulb, 38 °C at 25 % RH) | 2.71 °C <= 15 °C | Within known science | CSH-CAL-001 E4 |
| S4 | Droplets from the nozzle evaporate before they reach a person at 1.5 m (no wetting) | Physics | Fluid mechanics | Droplet evaporation after Maxwell/Fuchs diffusion: on the design day a droplet of up to about 100 µm evaporates in the 0.76 m between the jet end and head height, at the humid edge (32 °C, 60 %) up to about 80 µm (CSH-CAL-001 D3); nozzle makers state the spectrum as Dv0.9 | Needs Dv0.9 below about 80 µm at 7 bar; no maker's data yet. At risk: fog that flash-evaporates is normally made at much higher pressure (50 bar and more), and a 7 bar spectrum is likely coarser; if it is, wetting (PR-005) and cooling (S1, S2) fail together and option B becomes the fallback | Plausible, to confirm at TRL 3 | Open |
| S5 | Each 0.4 mm nozzle can pass 4 L/h at 7 bar (the physical bound is 16.9 L/h; the real flow is the maker's figure) | Physics | Fluid mechanics | A bound only, not a prediction: Bernoulli orifice flow Q = A sqrt(2 dp / rho): ideal 16.9 L/h, so 4 L/h implies a discharge coefficient of 0.24, plausible for a swirl nozzle (maker's datasheet to confirm) | 4 L/h <= 16.9 L/h | Within known science | CSH-CAL-001 C1 |
| S6 | The 60 W pump draw covers the hydraulic power of 32 L/h at 7 bar | Physics | Fluid mechanics | Hydraulic power = Q x dp; the rest is motor and diaphragm loss (10 % wire to water) | in 60 W, out 6.222 W | Within known science | CSH-CAL-001 C6 |
| S7 | The bulk of the mist line drains within 5 min after a session (about 30 s computed); water films and the anti-drip nozzle bodies stay wet | Physics | Fluid mechanics | Torricelli flow through the 3 mm valve orifice at 0.5 m head (Cd 0.6), with air let in by the vacuum breaker; the 0.40 L line volume from the model | 30 s <= 300 s | Within known science | CSH-CAL-001 C7 |
| S8 | A 100 W panel of 1.0 x 0.67 m is a credible rating | Physics | Thermodynamics and heat transfer | Efficiency = P / (1000 W/m2 x area) must stay below the Shockley-Queisser limit for a single junction (33.7 %); commercial monocrystalline panels reach about 20 % | 14.9 % <= 33.7 % | Within known science | CSH-CAL-001 F2 |
| S9 | The panel harvests more energy per design day than the system uses | Physics | Thermodynamics and heat transfer | Conservation of energy, with 0.75 for MPPT, wiring and temperature losses; holds on the design day only: on days above 42.7 °C charging pauses at midday (S11) | in 337.5 Wh, out 203.8 Wh | Within known science | CSH-CAL-001 F1, F2 |
| S10 | The battery runs the system for a full design day with no sun | Physics | Thermodynamics and heat transfer | Usable energy = 12.8 V x 25 Ah x 0.80 depth of discharge divided by the daily use, at beginning of life (at 80 % state of health it is about 1.0 design days, and cells at 40 to 47 °C age faster) | 1.26 design days >= 1 design days | Plausible, to confirm at TRL 3 | CSH-CAL-001 F2 |
| S11 | The battery keeps charging on hot days: LiFePO4 charge limit 45 °C against an enclosure 2.3 K above the air (white enclosure, in the cloth's shade) | Chemistry | Electrochemistry and batteries | Enclosure heat balance dT = (alpha G A_face + Q_internal) / (h A), G = 200 W/m2 in the shade of the cloth; cells are charged only below about 45 °C (typical cell data; the BMS reads cell temperature, which runs above the air in the box). The original grey enclosure (alpha 0.5) rose 3.6 K and stopped charging above 41.4 °C air; the white one (CSH-DEC-001 D9) rises 2.3 K, charging holds to 42.7 °C air. In direct late sun (900 W/m2, the enclosure is on the outer face of the rear right post) the white enclosure rises 7.0 K and charging stops above 38.0 °C air, so the fix is partial | Sun exposure of the enclosure across the day, long-wave exchange with the hot slab and the named cell's charge limit to assess at the site; a sunshield on the enclosure is a candidate | Plausible, to confirm at TRL 3 | CSH-CAL-001 F5; CSH-DEC-001 D9 |
| S12 | Scale from hard water does not block the 0.4 mm nozzles within a month | Chemistry | Materials and polymer chemistry | Calcium carbonate precipitates as the mist evaporates and when water warms; orifices of 0.4 mm clog from a few mg of deposit; a 5 µm filter does not remove dissolved hardness | Hardness of the site water and descaling interval to assess at the site (CSH-DEC-001 to-confirm item 12) | Plausible, to confirm at TRL 3 | Open |
| S13 | Shade cuts the mean radiant temperature by at least 15 °C at midday | Physics | Thermodynamics and heat transfer | Measured in Tempe, Arizona at 159 locations: shade sails and umbrellas cut the daytime mean radiant temperature by about 17.3 °C (Middel et al., BAMS 2021) | Evidence from analogous shade sails, not this design: 17.3 °C measured against the 15 °C target, a margin of 2.3 K on a site average; this cloth (about 90 % UV block, which is not 90 % of the shortwave) and the occupied spots, where the shadow falls partly outside the roof footprint at low sun (CSH-CAL-001 A2), are unmeasured; confirm with a globe thermometer | Plausible, to confirm at TRL 3 | CSH-CAL-001 E (PR-003) |
| S14 | The misting system does not become a Legionella source | Biology | Ecology and agronomy | Legionella grows in water at 20 to 50 °C (optimum about 35 °C) and spreads by inhaled aerosol (WHO fact sheet). Tank water on a design day settles near 34 °C (CSH-CAL-001 I3), inside the growth range; the controls are a 5 µm filter, water no older than 24 h (95 L drain-and-refill), the bulk of the line drained within 30 s (films and the anti-drip nozzle bodies stay wet), an opaque shaded tank and weekly disinfection | Temperature cannot be avoided; water age and cleaning are the controls; sampling with a partner lab needs TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S15 | A passive infrared sensor detects people standing still in 38 to 45 °C air | Biology | Ecology and agronomy | A PIR sensor responds to the contrast between a warm body (skin about 33 to 35 °C, clothing cooler) and its background; in air near body temperature the contrast and the detection range fall, and a person standing still gives little signal (sensor datasheets derate range with ambient temperature) | Range and sensitivity above 35 °C to take from the sensor maker; a radar presence sensor is a privacy and radio-approval trade-off for Amish (CSH-DEC-001 D10) | Plausible, to confirm at TRL 3 | Open |
| S16 | A front post (80 x 80 x 3 SHS, 2.90 m) weighs about 21 kg | Mathematics | Units and dimensional analysis | Mass = section area x length x 7850 kg/m3 | claimed 21 kg, estimate 21 kg (ratio 1.00) | Within known science | CSH-CAL-001 H1 |
| S17 | With the fabric fitted the long beams carry forecast gusts up to 15 m/s (the original 30 m/s case gives utilization 3.5 and failed; fixed by removing the fabric above 15 m/s, CSH-DDR-002) | Engineering and technology | Strength of materials | Fabric as a membrane with 5 % sag: edge pull T = p L^2 / (8 s) per metre, in-plane bending of the 50 x 50 x 2 SHS long beam over the 2.8 m post span, S275 with a 1.5 factor | 0.88 utilization <= 1 utilization | Plausible, to confirm at TRL 3 | CSH-CAL-001 G7, G8, G14 |
| S18 | With the fabric removed the frame survives a 30 m/s gust | Engineering and technology | Strength of materials | Post as a cantilever: panel as a flat plate (1.2 q A) with its tilt component plus drag on the frame and posts, S275 with a 1.5 factor (CSH-CAL-001 G13); roof members and anchors in G13 too; recomputed by the independent reviewer as 0.14 | 0.14 utilization (post) <= 1 utilization (post) | Within known science | CSH-CAL-001 G13 |
| S19 | An empty tank tips in a 30 m/s gust unless strapped; the strap carries the difference (the unstrapped tank failed, strap added in CSH-DDR-003) | Engineering and technology | Mechanics and statics | Overturning 57 N m against restoring 21 N m; strap tension = difference / (0.9 x tank height) = 57 N, 86 N with the 1.5 factor; the strap works for some wind directions only, so the two stop cleats are the second restraint; sliding (163 N of drag against about 40 N of friction) is held by the strap and the cleats; the strap's rating is not yet named | 86 N factored against a strap of a few hundred newtons or more; rating and cleat anchors to confirm when parts are bought | Plausible, to confirm at TRL 3 | CSH-CAL-001 G12 |
| S20 | The M16 anchors hold in the slab at the site | Engineering and technology | Standards practice | Factored anchor tension about 6.4 kN with the fabric on in a 30 m/s gust and about 2.8 kN with it removed (CSH-CAL-001 G10, G13); the resistance depends on the anchor type and the slab, which are unknown until a site is chosen | Anchor design resistance and slab to assess at each site | Plausible, to confirm at TRL 3 | Open |
| S21 | A garage can build the frame: bolted, no welding, rivet nuts in 2 mm tube | Engineering and technology | Manufacturing tolerances | Blind rivet nuts are standard in thin-wall tube; the largest pull on one M8 rivet nut is about 0.16 kN factored (CSH-CAL-001 G15); the maker's pull-out rating in a 2 mm wall is not yet checked | Rating to confirm from the rivet nut maker's data when parts are bought | Plausible, to confirm at TRL 3 | Open |
| S22 | Option B: the wet pad delivers air at about 26 °C from 38 °C, 25 % RH air | Physics | Thermodynamics and heat transfer | Direct evaporative cooling, T_out = T_db - eps (T_db - T_wb), eps 0.8 for a 90 mm cellulose pad (typical, to confirm from the maker); the outlet cannot be below the wet bulb 23.0 °C | 26 °C >= 23 °C | Within known science | Open |
| S23 | Option B: the fan and pad remove about 1.5 kW and evaporate about 2.2 L/h | Physics | Thermodynamics and heat transfer | Q = m_dot cp dT = 1.53 kW at 0.11 m3/s; water = Q / latent heat (a pad also needs bleed-off water against scale, which adds 20 to 50 %) | claimed 2.2 L/h, estimate 2.27 L/h (ratio 0.97) | Within known science | Open |
| S24 | Option B: one 250 mm fan cools a group of 6 to 8 people | Physics | Fluid mechanics | The cooled stream carries 1.5 kW, 8 % of the 18.8 kW that option A's mist absorbs; an axial jet of 0.11 m3/s mixes with room air within about 1 to 2 m, so it cools one or two people, not a group | Throw and mixing to confirm with a jet model or a field test; several fans would change the cost and power | Plausible, to confirm at TRL 3 | Open |
| S25 | Option C: a white skin 100 mm above the shade cloth lowers the heat load and the gap vents by buoyancy | Physics | Thermodynamics and heat transfer | Stack effect in a gap 2.4 m long at 7.1 deg, 10 K warmer than the air: v = sqrt(2 g H dT / T) = 0.43 m/s, an upper bound before friction; white coatings reflect most of the sun (reflectance of the maker's panel to confirm) | Added radiant benefit over the shade cloth alone to measure; no air cooling at all (no evaporation) | Plausible, to confirm at TRL 3 | Open |
| S26 | Option C: the skin cannot be taken off before a gust, so the frame must carry 30 m/s with the roof solid | Engineering and technology | Strength of materials | Rigid sheets pass the load to the long beams as pressure, not as fabric edge pull: normal force 4.67 kN, long beams 0.70 utilization (CSH-CAL-001 G6); anchors about 6.4 kN each (G10), the slab to assess | Beams within; anchors and slab depend on the site | Plausible, to confirm at TRL 3 | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. The verdict label is the kit's; the design is at TRL 3 and the plausible rows are confirmed at TRL 4.

## Fixes made under the standing instruction

Table 2. Details that failed, the fix and the result.

| Item | What failed | Fix | Result |
| --- | --- | --- | --- |
| Enclosure heat (this session) | A grey enclosure (solar absorptance 0.5) under the shade cloth runs 3.6 K above the air, so the battery stops charging above 41.4 °C air; the season goes to 45 °C | CSH-DEC-001 D9: a white or light grey enclosure (absorptance 0.25 or less), BOM line 8 and CAL F5 updated; the model already shows a light enclosure | 2.3 K rise in the cloth's shade; charging holds to 42.7 °C air (S11); in direct late sun the rise is 6.9 K and charging would stop above 38 °C, so the enclosure's sun exposure and a sunshield are open (D9, FMEA F13); the battery carries the afternoon (1.256 design days of reserve) |
| Fabric at 30 m/s (CSH-DDR-002, before kit 1.8) | With the cloth fitted, a 30 m/s gust loads the long beams at 3.52 of their limit (S17) | Decided by Amish on 2026-09-25: the cloth comes off before gusts above 15 m/s and is fitted only in forecast gusts below 15 m/s | Fabric on at 15 m/s 0.88; fabric off at 30 m/s posts 0.16 (S17, S18) |
| Empty tank (CSH-DDR-003, before kit 1.8) | An empty 120 L tank tips in a 30 m/s gust: 57 N m overturning against 21 N m restoring | A ratchet strap round the tank and the rear left post and two stop cleats anchored to the slab (BOM line 13) | Strap tension 57 N, 86 N with the 1.5 factor, rating still to name (S19) |

None of the fixes changes the working principle, the pitch or the scope, and Amish can reverse the one made in this session (D9). Two rows are not fixes but raise a trade-off for Amish: S15 (a PIR sensor loses range and sensitivity as the air nears body temperature; a radar presence sensor would answer it but changes the privacy and radio-approval picture, D10) and S14 (*Legionella*: the temperature cannot be avoided; dosing the tank with a disinfectant would change the safety case, D11).

## Fields not relevant

None. Every field is touched: physics (evaporation, heat and fluid flow, wind loads), chemistry (battery charge limit, scale), biology (*Legionella*, heat stress), mathematics (units and masses) and engineering (fasteners, anchors, tank stability).

## Concept options

- Option A, solar misting shade canopy: the rows S1 to S21 above.
- Option B, wet-pad fan cooler under shade: direct evaporative cooling is within known science (S22, S23: air at 26 °C from 38 °C, 2.2 L/h, plus bleed-off water). Its weakness is reach: one 250 mm fan delivers about 1.5 kW, 8 % of option A's mist, so it cools one or two people rather than a group (S24, plausible).
- Option C, passive double-skin reflective roof: reflecting the sun and venting the gap by buoyancy is within known science in principle (S25, S26, plausible); it cools no air at all. With the roof solid at all times, the frame and anchors must carry 30 m/s (S26).

## Independent review

A second reviewer (a separate headless Claude session, `claude -p --model claude-opus-5-5`, given only this document, CSH-CAL-001, CSH-PRS-001 and `sizing.py`, and none of the author's reasoning) was asked on 2026-10-30 to refute the headline results and every "Within known science" verdict. It recomputed the figures by hand. What it found and what changed:

Table 3. Review findings.

| Row | Finding | Change |
| --- | --- | --- |
| S1 | Weakened: the arithmetic is right (18.8 kW) but the check is circular, and the evaporated share and the share that cools the zone depend on the droplet size (S4) | Downgraded to plausible; tied to S4 |
| S2 | Raised: the control volume's 3 m is used as the frontal width and as the transit length | Noted in the row; plausible stays |
| S3, S8, S16, S22 | Upheld | None |
| S5 | Upheld as a bound only: 4 L/h below 16.9 L/h says nothing about the real flow, and PR-007 fails at 4.75 L/h, 19 % above | Reworded as a bound; the maker's flow gates PR-007 |
| S6 | Upheld; pump starts about 450 times a day (20 s on, 20 s off) | Added to the FMEA (F12) |
| S7 | Weakened: the horizontal runs and the nozzle bodies stay wet, so "drains" is the bulk; CAL I3 said 27 s, C7 30 s | Restated as the bulk; 30 s everywhere; residual water added to S14 and FMEA F1 |
| S9, S10 | Upheld with caveats: holds at 38 °C only; at 80 % battery health the reserve is 1.0 day | Caveats in the rows; S10 downgraded to plausible |
| S11 | Weakened: the 200 W/m2 case assumes the cloth's shade; in direct sun the rise is 6.9 K; hot slab radiation and cell temperature ignored; claim wording | Downgraded to plausible; direct-sun case computed; the fix is partial; sunshield proposed (FMEA F13) |
| S13 | Weakened: evidence from analogous sails with a 2.3 K margin, the field label was wrong | Downgraded to plausible; field changed to physics |
| S18 | Upheld; the STEM check said 0.16 and CAL G13 0.14 | Now takes G13's 0.14 from the script |
| S19 | Upheld but inconsistent: 57 N unfactored, 106 N factored by the reviewer's factors; strap rating assumed; sliding ignored | Factored 86 N reported, row downgraded to plausible, sliding and cleat anchors noted |
| S23 | Upheld; pad bleed-off adds 20 to 50 % water | Noted in the row |
| Counts and labels | The headline said TRL 4 while the rows say TRL 3; `sizing.py` still printed v0.3 and "a new budget is proposed" | Label explained under Table 1; `sizing.py` header and R13 note corrected |
| S4 (not a within verdict) | Missing: 7 bar nozzles typically give coarser droplets than the 80 µm needed; fog that flash-evaporates is normally a 50 bar technique | S4 now says "at risk"; option B named as the fallback |
| Missing failure modes | Unforecast gusts (the fabric reaches its limit at about 16 m/s, 19.6 m/s unfactored); wet slab; mist on the PIR and the humidity sensor; pump and valve cycling; battery ageing; the drain valve fails open if its 5 W hold is lost | FMEA F12, F14, F15 and F16 added; hazard H5 stays; ageing in S10 |

The reviewer's figures that could not be confirmed here are kept as its figures. Nothing it found changed the working principle, the pitch or the scope, so no item goes to Amish beyond D10 and D11.

## Sources

- Ulpiani, G. Systematic review of water mist spray for outdoor cooling, *Applied Energy*, 2019, as cited in CSH-PRB-001. https://doi.org/10.1016/j.apenergy.2019.113647 (evaporation limit by wet bulb).
- Middel, A., et al. Tempe, Arizona shade study, *Bulletin of the American Meteorological Society* 102 (2021), as cited in CSH-PRB-001. https://journals.ametsoc.org/view/journals/bams/102/9/BAMS-D-20-0193.1.xml (S13).
- World Health Organization. "Legionellosis." https://www.who.int/news-room/fact-sheets/detail/legionellosis (S14).
- Shockley and Queisser limit for a single junction (33.7 %), as coded in `.kit/stem_check.py` (S8).
- Stull wet bulb approximation, as coded in `docs/04-calcs/sizing.py` (S3, S22).
- Typical PIR sensor behaviour near body temperature, from sensor datasheets in general; no particular datasheet was consulted (S15, to assess).
- Cell data for lithium iron phosphate charging below about 45 °C is typical, not from a named datasheet (S11, to confirm with the cell maker).
