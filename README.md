# CoolShade

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $700 USD · **Difficulty:** 3 of 5

A solar-powered shade canopy with fine misting for bus stops, markets and queues, switching on only when heat stress is high.

## Concept rationale

Shade and targeted misting can cut felt temperature where people must wait.

## Burning platform

Heat waves are more frequent and people at transit stops and markets are among the most exposed.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It pairs with HeatMap Node.

## Problem

People waiting outdoors in extreme heat have nowhere to cool down, and public cooling is rarely where they wait.

## Concept

A solar-powered shade canopy with fine misting for bus stops, markets and queues, switching on only when heat stress is high.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Canopy frame and shade fabric
- Solar panel and battery
- Low-pressure misting pump and nozzles
- Heat and humidity sensor
- Water tank and filter

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Water must be clean and lines drained or disinfected to prevent Legionella. Misting is ineffective in high humidity; the controller must switch off then. Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CSH-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CSH-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
