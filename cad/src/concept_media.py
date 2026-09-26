"""CoolShade concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X runs along the curb, Y across the sidewalk (street side is -Y), Z up,
sidewalk surface at Z = 0. The canopy is a four-post mono-pitch frame, 3.0 m x 2.4 m in plan,
high edge at the street side. Street context (sidewalk, curb, road, bench) is grey and has no
BOM number; kit parts are colored and numbered to match bom/bom.csv.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# ---------------- main dimensions (proposed, awaiting Amish) ----------------
L, D = 3000.0, 2400.0            # roof plan: along curb (X), across sidewalk (Y)
PX, PY = 1400.0, 1050.0          # post centers at (+/-PX, +/-PY)
POST = 80.0                      # 80 x 80 x 3 mm steel square hollow section
Z_MID = 2790.0                   # roof plane height at Y = 0
Z_FRONT, Z_REAR = 2940.0, 2640.0  # roof plane at the street edge and rear edge
SLOPE = math.degrees(math.atan((Z_FRONT - Z_REAR) / D))
BEAM = 50.0                      # 50 x 50 mm roof beams


def roof(shape):
    """Place a shape built flat around (0, 0, 0) into the sloped roof plane (high at -Y)."""
    return Pos(0, 0, Z_MID) * Rot(-SLOPE, 0, 0) * shape


def z_roof(y):
    return Z_MID - y * math.tan(math.radians(SLOPE))


def rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# 1 Posts, four, from base plate to roof beam underside
posts = union(Pos(sx * PX, sy * PY, 0) * Pos(0, 0, (z_roof(sy * PY) - BEAM / 2 - 10) / 2 + 10)
              * Box(POST, POST, z_roof(sy * PY) - BEAM / 2 - 10)
              for sx in (-1, 1) for sy in (-1, 1))
# knee braces from each post to the long beams
braces = union(rod((sx * PX - sx * 40, sy * PY, z_roof(sy * PY) - 520),
                   (sx * PX - sx * 460, sy * PY, z_roof(sy * PY) - 60), 16)
               for sx in (-1, 1) for sy in (-1, 1))
posts = posts + braces

# 2 Roof frame: two long beams, two end beams, two purlins (flat in the roof plane)
frame = roof(Pos(0, -PY, 0) * Box(L, BEAM, BEAM) + Pos(0, PY, 0) * Box(L, BEAM, BEAM)
             + Pos(-PX, 0, 0) * Box(BEAM, D, BEAM) + Pos(PX, 0, 0) * Box(BEAM, D, BEAM)
             + Pos(-450, 0, 0) * Box(40, D - 100, 40) + Pos(450, 0, 0) * Box(40, D - 100, 40))

# 3 Shade fabric, knitted HDPE, tensioned over the frame
fabric = roof(Pos(0, 0, BEAM / 2 + 2) * Box(L, D, 4))

# 4 Base plates with anchor bolts
plates = union(Pos(sx * PX, sy * PY, 5) * Box(220, 220, 10) for sx in (-1, 1) for sy in (-1, 1))
bolts = union(Pos(sx * PX + dx, sy * PY + dy, 30) * Cylinder(8, 50)
              for sx in (-1, 1) for sy in (-1, 1) for dx in (-80, 80) for dy in (-80, 80))
plates = plates + bolts

# 5 Solar panel, 100 W, about 1,000 x 670 x 35 mm, on rails over the purlins, rear half of the roof
panel = roof(Pos(0, 500, BEAM / 2 + 70) * Box(1000, 670, 35)
             + Pos(-450, 500, BEAM / 2 + 30) * Box(40, 700, 40) + Pos(450, 500, BEAM / 2 + 30) * Box(40, 700, 40))

# 8 Equipment enclosure on the outer face of the rear right post (houses 6 and 7)
EX, EY, EZ = PX + POST / 2 + 80, PY, 1650.0
enclosure = Pos(EX, EY, EZ) * Box(160, 320, 420)
# 6 LiFePO4 battery and 7 MPPT charge controller, inside the enclosure
battery = Pos(EX, EY - 60, EZ - 90) * Box(80, 180, 170)
mppt = Pos(EX, EY + 90, EZ + 90) * Box(40, 90, 140)

# 9 Sensor head: radiation shield on a short arm off the front right post, and a PIR under the front beam
shield = union(Pos(PX + 330, -PY, 2250 + k * 22) * Cylinder(60 - 2 * k, 10) for k in range(6))
arm = rod((PX + POST / 2, -PY, 2300), (PX + 300, -PY, 2300), 12)
pir = Pos(0, -PY + 40, z_roof(-PY) - BEAM / 2 - 40) * Box(60, 60, 50)
sensors = shield + arm + pir

# 13 Water tank, 120 L, opaque, at the rear left corner inside the footprint
TX, TY = -PX + 280, PY - 250
tank = Pos(TX, TY, 350) * Cylinder(270, 700)
# 10 Pump, 12 V diaphragm, about 7 bar, in a small box bracketed to the rear left post
pump = Pos(-PX + 150, PY - 100, 900) * Box(200, 130, 140)
# 11 Filter, 5 um cartridge, beside the pump
filt = Pos(-PX + 110, PY - 230, 880) * Cylinder(45, 240)
# 14 Normally open drain valve at the low point by the tank
drain = Pos(TX + 260, TY - 180, 90) * Box(90, 60, 70)

# 12 Mist line: nylon line under both long beams and one end beam, eight nozzles pointing down
LINE_Z = -BEAM / 2 - 25
line_flat = (rod((-PX + 60, -PY + 70, LINE_Z), (PX - 60, -PY + 70, LINE_Z), 7)
             + rod((-PX + 60, PY - 70, LINE_Z), (PX - 60, PY - 70, LINE_Z), 7)
             + rod((-PX + 60, -PY + 70, LINE_Z), (-PX + 60, PY - 70, LINE_Z), 7))
nozzles_flat = union(Pos(x, y, LINE_Z - 18) * Cylinder(11, 30)
                     for x in (-1050, -350, 350, 1050) for y in (-PY + 70, PY - 70))
mistline = roof(line_flat + nozzles_flat)

# 15 Supply hose and wiring: tank to pump, pump up the rear left post to the mist line,
#    panel and sensor cables to the enclosure (simplified runs)
zl = z_roof(PY) - BEAM / 2 - 60
harness = (rod((TX + 150, TY + 120, 650), (-PX + 150, PY - 100, 830), 8)
           + rod((-PX + 60, PY - 60, 970), (-PX + 60, PY - 60, zl), 8)
           + rod((PX + 60, PY, zl), (PX + 60, PY, EZ + 210), 6)
           + rod((PX + 60, -PY + 60, 2300), (PX + 60, -PY + 60, z_roof(-PY) - 60), 6)
           + rod((PX + 60, -PY + 60, z_roof(-PY) - 60), (PX + 60, PY - 60, z_roof(PY) - 60), 6))

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
    Part("Mist line and 8 nozzles", mistline, "#111827", 12, (0, -300, 350)),
    Part("Water tank, 120 L", tank, "#D4A017", 13, (-900, 1100, 0)),
    Part("Drain valve", drain, "#DC2626", 14, (-100, -700, 0)),
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
        key_figures=["Shade roof 3.0 x 2.4 m (7.2 m²), clear height about 2.5 m",
                     "8 low-pressure nozzles at about 7 bar, about 32 L/h while spraying (estimate)",
                     "About 85 L water and 205 Wh per hot day (estimate)",
                     "100 W panel, 12.8 V 20 Ah LiFePO4; 12 V DC only, no mains",
                     "Mists only above 32 °C, below 60 % RH, with people present",
                     "About $735 in parts (indicative), $700 budget"],
        cut=False, context=context,
        flow={"title": "daily water flow on a hot day, L per day (estimates; 70 L evaporated absorbs about 47 kWh of heat)",
              "unit": "L",
              "stages": [("Refill, potable", 85), ("Tank, 120 L", 85), ("Filter and pump", 80),
                         ("Mist line, 8 nozzles", 80), ("Evaporated", 70)],
              "losses": [(1, "Daily tank and line flush", 5), (3, "Drift, drip and wetting", 10)]},
    )
