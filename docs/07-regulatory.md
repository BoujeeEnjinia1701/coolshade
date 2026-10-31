---
doc_id: CSH-REG-001
title: CoolShade regulatory and standards register
project: CoolShade
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-30'
    author: Amish Chadha
    change: "First issue in the kit 1.9.1 upgrade, for the current design (option A) and the first site, a market lane in a hot, dry city; every applicability is to assess with a qualified reviewer"
---

# CoolShade regulatory and standards register

No product certification is sought at TRL 3. The rules that matter most for a public misting shade are local and about people, not products: water hygiene for a mist that people breathe (G1), permission to stand a structure on public land (G2), wind loading of a canopy (G3) and the anchors in the slab (G6). The first site is a market lane in a hot, dry city, with the Phoenix area as the first candidate (CSH-DEC-001); nothing has been agreed with any authority, so the jurisdiction column names the likely rule and every applicability is "to assess". Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Local public health rules on water systems that make aerosols, and the WHO guidance on *Legionella* | City or county of the site; international guidance | Control of *Legionella* in water at 20 to 50 °C; temperature, water age, cleaning, sampling | The 7 bar mist is an aerosol from 34 °C tank water (CSH-CAL-001 I3); PR-009 is at risk | Market operator and health authority | To assess; a hygiene plan is a pre-condition of a public trial (CSH-DEC-001 to-confirm item 11) |
| G2 | Permission to install a structure on public land or in a market | City or market operator | Right to stand a fixed canopy; setback from vehicles and walkways; sight lines | Every site; the street-side posts stand 25 mm inside the roof's street edge (CSH-DDR-003 P1) | Market operator | To assess |
| G3 | Wind load rules for canopies and open structures (for example EN 1991-1-4 in Europe, ASCE 7 in the United States) | Country or state of the site | Design gust speed, pressure coefficients, importance factors | CSH-CAL-001 section G uses 30 m/s, a net pressure coefficient of 1.2 and a 1.5 factor; the site's design gust may differ | Design lead | To assess (number and title only; text not consulted) |
| G4 | EN 1090, execution of steel structures | European Union; reference elsewhere | Fabrication and assembly quality of steel structures | The bolted 80 x 80 x 3 mm frame; welding appears only in options B and C | Design lead | To assess |
| G5 | ISO 4017, ISO 4032 and ISO 7089, hexagon bolts, nuts and plain washers | International | Dimensions of the fasteners | Every bolt, nut and washer in the D3 model uses these dimensions (`.kit/cad_parts.py`) | Design lead | Met by design in the model |
| G6 | European Assessment Document EAD 330232, mechanical fasteners for use in concrete | European Union; reference elsewhere | Anchor performance in cracked and uncracked concrete | The four M16 anchor sets at the post bases (about 2.8 kN each with the cloth off, CSH-CAL-001 G13) | Site engineer | To assess (the slab and anchor type are unknown until a site is chosen) |
| G7 | IEC 60529, degrees of protection provided by enclosures (IP code) | International | Ingress of dust and water into the controller enclosure | The enclosure is specified IP65 (PR-012) | Design lead | To assess (the maker's rating to confirm) |
| G8 | IEC 62619, safety requirements for secondary lithium cells and batteries for industrial applications | International | Safety of the LiFePO4 battery | One 12.8 V 25 Ah battery with a BMS and a cold-charge cutoff | Design lead | To assess (maker's declaration to confirm) |
| G9 | United Nations Manual of Tests and Criteria, part III, section 38.3 | International (transport) | Transport tests for lithium batteries | Shipping the battery to a builder | Builder | To assess |
| G10 | IEC 61215 and IEC 61730, photovoltaic module qualification and safety | International | The 100 W solar panel | A bought panel; confirm the maker's certificates | Builder | To assess |
| G11 | Local electrical rules for extra-low-voltage DC installations | Country or state of the site | Fusing, cable sizes, isolation of a 12 V system | Battery fused at the terminal (15 A, margin 2.0, CSH-CAL-001 I2) | Builder | To assess |
| G12 | Backflow prevention rules for a mains water connection | City water utility | A mains connection to the tank, if used | The mains connection is optional (CSH-DDR-001 D4) and needs a backflow preventer | Market operator | To assess |
| G13 | Accessible design rules for clear space and routes (the common clear floor space is 30 by 48 in, or about 0.76 x 1.22 m) | Country of the site | A wheelchair space and a route to it | PR-001 requires a 0.8 x 1.2 m space; the posts stand on a 2,800 x 2,350 mm grid | Design lead | To assess |
| G14 | ISO 11228-1, manual handling: lifting and carrying | International | Mass limits for manual lifting | The heaviest piece is a front post, 21.0 kg; no part over 40 kg (PR-017) | Design lead | Met by design (two-person lift of each piece) |
| G15 | Rules on public misting, pressure equipment and water use in a drought | City, county or state of the site | Whether a 7 bar pump system and its water use need a permit | A 12 V, 60 W diaphragm pump at about 7 bar; 85 L per design day | Market operator | To assess |
| G16 | ISO 12100, general principles for risk assessment | International | Method of the hazard analysis | CSH-RSK-001 follows it | Design lead | Applies as a method |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- World Health Organization. "Legionellosis." https://www.who.int/news-room/fact-sheets/detail/legionellosis (checked 2026-10-30), as in CSH-PRB-001.
- World Health Organization. "Climate change and health: heat." https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health (checked 2026-10-30), as in CSH-PRB-001.
- Standards G3 to G5, G7 to G11, G13, G14 and G16 are cited by number and title or description only; their texts were not consulted for this register and each applicability is to be confirmed by the role named. No standard number is given where none was known.
