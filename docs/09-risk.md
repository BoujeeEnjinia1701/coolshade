---
doc_id: CSH-RSK-001
title: CoolShade risk register and hazard analysis
project: CoolShade
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade: project risks, preliminary hazard analysis and a first-pass design FMEA with RPN for option A, from CSH-CAL-001 v0.6 and CSH-STM-001"
---

# CoolShade risk register and hazard analysis

The top project risk is that no site or partner agrees to a public trial, because a misting system needs a hygiene plan that a health authority accepts (P1, P3). The top hazard is *Legionella* from the mist (H1), controlled by water that is never older than 24 h, a line that drains within 30 s of a session, a filter and weekly disinfection, with a residual that stays high until a partner lab samples the water at TRL 4. The highest design FMEA scores are a blocked vacuum breaker or wet runs that leave warm water in the line (RPN 48), a shade cloth left on in an unforecast gust (RPN 48), anchors that pull out of an unknown slab (RPN 40), and a drifting or misted humidity sensor (RPN 36 each). Method: STANDARDS section 23 and ISO 12100. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be caught) to 5 (unlikely to be caught).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | No site or partner agrees to a trial | Candidate named, nothing agreed (CSH-DEC-001); misting on public land raises hygiene and liability questions | Requirements and the reference site stay desk assumptions; no TRL 4 | 3 | 5 | Amish | Approach the market operator and a university heat group with the hygiene plan first |
| P2 | Parts cost stays over the target | USD 882 against USD 775; steel prices look low until quoted | Prototype not affordable for a community group | 4 | 3 | Design lead | Savings in CSH-DEC-001 (base plates, steel panel rails); steel quotes; budget raise only proposed, never made here |
| P3 | Health authority will not accept public misting | *Legionella* risk in 34 °C tank water (STEM S14) | No public trial; option B or C becomes the fallback | 3 | 5 | Market operator | Hygiene plan with named responsible person; sampling with a partner lab; option B has no free aerosol (CSH-OPT-001) |
| P4 | Nozzle maker has no droplet data or the droplets are too big | Dv0.9 not published for the 0.4 mm swirl nozzle at 7 bar | Wetting (PR-005); complaints | 3 | 4 | Design lead | Ask makers for Dv0.9 and flow before buying (CSH-DEC-001 to-confirm item 1); option B as fallback |
| P5 | People do not want to stand in a mist | Wet clothes, hair and hygiene concerns | Low use | 3 | 3 | Partner | Ask in co-design (CSH-PRB-001 open questions) before building |
| P6 | Theft or vandalism of the panel, battery, pump or fabric | Public site, no staff | Loss of function; cost | 3 | 3 | Market operator | Lockable enclosure and tamper-proof screws; bolted frame; fabric removable and stored off site between storms |
| P7 | Design gust at the site above 30 m/s | Storm climate not the hot, dry design case | Frame and anchors under-designed | 2 | 5 | Design lead | Site wind data per site (CSH-REG-001 G3); fabric off above 15 m/s |

## Preliminary hazard analysis

Table 2. Hazards. Residual is the severity x likelihood score (1 to 25) after the control.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | *Legionella* from inhaled mist | Warm tank water (about 34 °C) and a line that stands wet | Legionnaires' disease or Pontiac fever | 5 | 2 | 5 um filter; water never older than 24 h; line drains within 30 s (vacuum breaker); opaque shaded lockable tank; weekly disinfection; a named responsible person | 10 |
| H2 | Frame or roof lifted or blown over in a gust | Wind uplift, anchors short, cloth left fitted | Crush injury; damage | 5 | 2 | Cloth off above 15 m/s forecast; M16 anchors; frame checks 0.14 utilization at 30 m/s with the cloth off (PR-010) | 10 |
| H3 | Shade cloth torn loose in a storm | Cloth fitted in a gust above 15 m/s | Flying cloth; eyelet and cord strike | 3 | 3 | Fit only when forecast gusts are below 15 m/s; reinforced hem and eyelets; removable in 15 min | 6 |
| H4 | Electric shock or fire | 12 V DC battery and wiring; short circuit | Burn; fire | 4 | 1 | 12 V only; 15 A terminal fuse; LiFePO4 with BMS; IP65 lockable enclosure | 4 |
| H5 | Slip on wet ground | Mist or drips wet the pavement | Fall and injury | 3 | 3 | Droplets sized to evaporate (PR-005, not yet verified); misting only in hot, dry air; no puddles as a requirement | 6 |
| H6 | Head strike | Knee brace ends and nozzles at 2.22 m | Cut or bump | 2 | 2 | Clear height 2,223 mm or more (PR-002); flattened brace ends; edges broken | 3 |
| H7 | Cuts and pinches in assembly | Sharp section ends, rivet nut tool, cloth lacing | Cuts, pinched fingers | 2 | 3 | End caps on tubes; edges broken in the model; gloves in the build plan | 4 |
| H8 | Tank tips or empties onto people | 128 kg full; an empty tank tips in 30 m/s | Crush; spill | 4 | 2 | Ratchet strap and two stop cleats anchored to the slab (CSH-CAL-001 G12) | 6 |
| H9 | Manual handling | Posts of 21.0 kg; panel 7 kg | Back injury | 3 | 3 | Two-person lifts; no part over 40 kg (PR-017) | 4 |
| H10 | Mist reduces visibility or wets the road | Street-side posts at the kerb | Traffic incident | 3 | 2 | Nozzles inboard of the long beams; setback check at the site (CSH-DEC-001 to-confirm item 10) | 4 |
| H11 | Hot surfaces and sun on metal | Pump at 60 W; steel in full sun | Burn on contact | 2 | 2 | Pump in a vented box on the plate; cloth shades the frame | 2 |
| H12 | Falling solar panel | 7 kg panel on rails and L-feet on a 7 degree roof | Strike injury | 4 | 1 | Four L-feet with M8 bolts into rivet nuts, four end clamps (pull per rivet nut about 0.16 kN, CSH-CAL-001 G15) | 4 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Vacuum breaker (air admittance valve) | Let air in so the mist line drains | Valve blocked or stuck shut | Line stays full of warm water between sessions | Dust, insects, scale; the horizontal runs and the nozzle bodies stay wet even when it works | 4 | 3 | 4 | 48 | Cap with a mesh; inspect weekly; check the drain time and a dry line at every visit; fall the long runs toward the riser (to assess); high priority for the hygiene plan |
| F2 | M16 anchors | Hold the posts to the slab | Pull out or crack the slab | Frame uplift in a gust | Unknown slab, short embedment | 5 | 2 | 4 | 40 | Pull test each anchor at installation; site engineer check (CSH-REG-001 G6, STEM S20) |
| F3 | Humidity and temperature sensor in the shield | Decide when to mist | Reading drifts or wets | Mists in humid air or not at all | Condensate, dust, ageing | 3 | 3 | 4 | 36 | Plate shield; replace on a schedule; sanity check against a second reading in firmware (TRL 4) |
| F4 | Rivet nuts in 2 mm tube | Fix the roof joints | Pull out | A loose roof joint | Thin wall, vibration, over-torque | 4 | 2 | 4 | 32 | Maker's pull-out rating check (STEM S21); torque limit in the build plan |
| F5 | Normally open drain valve | Open when the pump stops | Stuck closed | Line stays full | Debris, coil failure | 4 | 2 | 4 | 32 | Fail-safe normally open type; clean strainer; test at every visit |
| F6 | Shade cloth and eyelets | Cover the roof | Eyelet tears, hem frays | Cloth flaps loose | UV, wind | 3 | 3 | 3 | 27 | Reinforced hem; replace yearly; fit only below 15 m/s |
| F7 | PIR presence sensor | Detect people | Misses a person standing still in 38 to 45 °C air | No mist when someone waits | Low contrast near body temperature (STEM S15) | 2 | 4 | 3 | 24 | Sensor datasheet derating; test at TRL 4; radar alternative to Amish (CSH-DEC-001 D10) |
| F8 | Enclosure gasket and glands | Keep the electronics dry | Water or dust gets in | Short circuit or corrosion | Gasket set, gland not tightened | 4 | 2 | 3 | 24 | IP65 enclosure; moulded mounting holes outside the gasket (CSH-DDR-003); check glands at build |
| F9 | Aluminium rails on galvanised feet | Carry the panel | Galvanic corrosion at the contact | Loosening | Zinc and aluminium in a wet, salty air | 2 | 3 | 4 | 24 | Isolating washers to assess; inspect yearly |
| F10 | Tank strap | Stop the tank tipping | Strap fails or slackens | Tank tips in a gust | UV, ratchet creep | 3 | 2 | 3 | 18 | Two stop cleats as a second restraint; check the strap at each refill |
| F11 | Nozzles, 0.4 mm | Make the mist | Scale blocks the orifice | Less cooling, uneven spray | Hard water (STEM S12) | 2 | 4 | 2 | 16 | Tool-free removal; descale; 5 um filter; water hardness check |
| F12 | Pump | Pressurise the line | Runs dry, or the diaphragm wears from about 450 starts a day (20 s on, 20 s off) | No mist | Low tank, cycling, inrush | 2 | 3 | 2 | 12 | Low-level float switch cuts the pump; spare diaphragm; fewer, longer cycles to assess at TRL 4 |
| F13 | Battery charge cutoff | Protect the cells | Charging pauses in air above about 42.7 °C in the cloth's shade, about 38 °C with the enclosure in direct late sun | Less charge on the hottest days; cells age faster at 40 to 47 °C | Cell charge limit of about 45 °C (STEM S11) | 2 | 4 | 3 | 24 | White enclosure (CSH-DEC-001 D9); enclosure sun exposure and a sunshield to assess; 1.26 design days of reserve at beginning of life |
| F14 | Shade cloth, fitted | Shade | Cloth left on in an unforecast gust | Beams loaded to their limit near 16 m/s (19.6 m/s unfactored); at 30 m/s utilization 3.5 | Dust storms and microbursts in hot, dry climates come with little warning | 4 | 3 | 4 | 48 | Fit only when forecast gusts are below 15 m/s (CSH-DDR-002); cord lacing that releases under load is studied at TRL 4 (CSH-DDR-002 N1c); site wind data |
| F15 | Sensor shield and PIR window | Read the air and the people | Mist reaches the humidity sensor or the PIR window | False humid reading, mist off in dry air, or false presence | Drift of droplets in a breeze | 3 | 3 | 4 | 36 | Plate shield; sensor head 375 mm outboard of the front right post (CSH-DDR-003); check against nozzle drift at TRL 4 |
| F16 | Drain valve coil | Open the line when the pump stops | Valve opens in mid-session if its 5 W hold is lost | Session stops early; water drains to the slab | Power dip, loose connector | 2 | 3 | 2 | 12 | Fail-safe normally open type is kept (CSH-DDR-002); locking connector |

## Sources

- World Health Organization. "Legionellosis." https://www.who.int/news-room/fact-sheets/detail/legionellosis (checked 2026-10-30).
- CSH-CAL-001 and CSH-STM-001 for the loads, times and energy quoted.
- ISO 12100, general principles for risk assessment (method only; text not consulted).
