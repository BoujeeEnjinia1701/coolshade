"""CoolShade concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the canopy parts from cad/src/model.py (PARAMS), adds the street (sidewalk, curb, road)
and an existing bench (grey, no BOM number) as site context, and renders the media set with
.kit/concept.py. Parts are colored and numbered to match bom/bom.csv. Figures on the sheet and
in the flow diagram come from docs/04-calcs/sizing.py (CSH-CAL-001). Not for fabrication.

Coordinates in mm. X runs along the curb, Y across the sidewalk (street side is -Y), Z up,
sidewalk surface at Z = 0.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

m = build_parts()
posts, frame, fabric, plates, panel = m["posts"], m["frame"], m["fabric"], m["plates"], m["panel"]
battery, mppt, enclosure, sensors = m["battery"], m["mppt"], m["enclosure"], m["sensors"]
pump, filt, mistline, tank, drain, harness = m["pump"], m["filter"], m["mistline"], m["tank"], m["drain"], m["harness"]

GREY = "#9CA3AF"
parts = [
    Part("Posts, 80 x 80 mm steel, with knee braces", posts, "#64748B", 1, (0, 0, 0)),
    Part("Roof frame, 50 x 50 mm steel", frame, "#475569", 2, (0, 0, 700)),
    Part("Shade fabric, knitted HDPE", fabric, "#0F766E", 3, (0, 0, 1400)),
    Part("Base plates and anchors", plates, "#A16207", 4, (0, 0, -350)),
    Part("Solar panel, 100 W", panel, "#1E3A8A", 5, (0, 900, 2100)),
    Part("LiFePO4 battery, 12.8 V 20 Ah", battery, "#C2410C", 6, (1100, -350, -500)),
    Part("MPPT charge controller", mppt, "#16A34A", 7, (1100, 300, 450)),
    Part("Controller and enclosure", enclosure, "#E5E7EB", 8, (450, 0, 0)),
    Part("Sensor head (T, RH, PIR)", sensors, "#7C3AED", 9, (600, -600, 350)),
    Part("Misting pump, 12 V", pump, "#2563EB", 10, (-1100, -300, 900)),
    Part("Filter, 5 um", filt, "#0EA5E9", 11, (-1300, -700, 250)),
    Part("Mist line loop and 8 nozzles", mistline, "#111827", 12, (0, -300, 350)),
    Part("Water tank, 120 L, strapped", tank, "#D4A017", 13, (-900, 1100, 0)),
    Part("Drain valve and vacuum breaker", drain, "#DC2626", 14, (-100, -700, 0)),
    Part("Hose and wiring harness", harness, "#374151", 15, (0, 400, 150)),
]

# Street context for the hero only: sidewalk slab, curb, road strip and an existing bench (grey, no BOM)
sidewalk = Pos(300, 0, -60) * Box(6200, 3800, 120)
curb = Pos(300, -1960, -85) * Box(6200, 120, 170)
road = Pos(300, -2720, -230) * Box(6200, 1400, 60)
bench = (Pos(150, 520, 440) * Box(1500, 420, 50) + Pos(150, 710, 700) * Box(1500, 40, 380)
         + Pos(-500, 520, 210) * Box(50, 380, 420) + Pos(800, 520, 210) * Box(50, 380, 420))
context = [Part("Sidewalk", sidewalk, "#D1D5DB"), Part("Curb and road", curb + road, "#6B7280"),
           Part("Existing bench", bench, GREY)]

if __name__ == "__main__":
    render_all(
        parts, project="CoolShade", title="Solar misting shade canopy concept", dwg_no="CSH-DWG-010",
        key_figures=["Shade roof 3.0 x 2.4 m (7.2 m²); headroom 2,234 mm minimum (CSH-CAL-001)",
                     "8 low-pressure nozzles at 7 bar, 32 L/h while spraying (nozzle data to confirm)",
                     "85 L water and 204 Wh per hot, dry day; 1.35 °C air cooling at 1 m/s",
                     "100 W panel, 12.8 V 20 Ah LiFePO4; 12 V DC only, no mains",
                     "Mists only above 32 °C, below 60 % RH, with people present",
                     "Fabric off before storms; $758 in parts (indicative), $700 budget"],
        cut=False, context=context,
        flow={"title": "daily water flow on a hot, dry day, L per day (estimates, CSH-CAL-001; 70 L evaporated absorbs about 47 kWh)",
              "unit": "L",
              "stages": [("Daily fill, potable", 95), ("Tank, 120 L", 95), ("Filter and pump", 80),
                         ("Mist line, 8 nozzles", 80), ("Evaporated", 70)],
              "losses": [(1, "Residual drained, line flush", 15), (3, "Drift, drip and wetting", 10)]},
    )
