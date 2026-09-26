"""CoolShade parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    coolshade-assembly.step / .stl   the whole canopy with its water, power and control parts
    frame.step / .stl                posts, knee braces, roof frame, base plates and anchors
    water-system.step / .stl         tank with strap, pump, filter, drain valve, vacuum breaker,
                                     mist line loop with nozzles, supply hose

Axes (mm): X runs along the curb, Y across the sidewalk (street side is -Y), Z up with the
sidewalk surface at Z = 0. The roof is a mono-pitch plane, high at the street edge. The same
PARAMS feed docs/04-calcs/sizing.py (CSH-CAL-001), cad/src/sheets.py (drawing CSH-DWG-001)
and cad/src/concept_media.py. Main dimensions and interfaces only; not for fabrication.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # roof plan and slope
    "roof_l": 3000.0, "roof_d": 2400.0,          # along the curb (X), across the sidewalk (Y)
    "z_front": 2940.0, "z_rear": 2640.0,         # roof plane (beam centerline) at the street and rear edges
    # 1 posts: 80 x 80 x 3 mm SHS on a 2800 x 2100 mm grid, with a 32 mm tube knee brace each
    "post_x": 1400.0, "post_y": 1050.0, "post": 80.0, "post_t": 3.0,
    "brace_od": 32.0, "brace_t": 2.5,
    "brace_drop": 400.0, "brace_reach": 400.0,   # below the beam underside, and along the long beam (45 deg)
    # 2 roof frame: 50 x 50 x 2 mm long and end beams, 40 x 40 x 2 mm purlins at +/-450 mm
    "beam": 50.0, "beam_t": 2.0, "purlin": 40.0, "purlin_t": 2.0, "purlin_x": 450.0,
    # 3 shade fabric
    "fabric_t": 4.0,
    # 4 base plates and anchors: M16 at 160 mm centers
    "plate": 220.0, "plate_t": 10.0, "anchor_d": 16.0, "anchor_pitch": 160.0, "anchor_embed": 125.0,
    # 5 solar panel on two rails over the purlins, rear half of the roof
    "panel": (1000.0, 670.0, 35.0), "panel_y": 500.0,
    # 8 enclosure (houses 6 battery and 7 MPPT) on the outer face of the rear right post
    "enc": (160.0, 320.0, 420.0), "enc_z": 1650.0,
    "battery": (80.0, 180.0, 170.0), "mppt": (40.0, 90.0, 140.0),
    # 9 sensor head: multi-plate shield on an arm off the front right post; PIR under the front beam
    "shield_r": 60.0, "shield_z": 2250.0, "arm_l": 300.0,
    # 10 pump, 11 filter, 13 tank (rear left corner), 14 drain valve
    "pump": (200.0, 130.0, 140.0), "pump_z": 900.0,
    "filter_r": 45.0, "filter_h": 240.0,
    "tank_d": 540.0, "tank_h": 700.0, "tank_inset": (280.0, 250.0),
    "tank_nominal_l": 120.0,
    "drain": (90.0, 60.0, 70.0),
    # 12 mist line: closed loop under both long beams and both end beams, 8 nozzles
    "line_od": 9.5, "line_id": 6.5, "line_inset": 70.0, "line_drop": 50.0,
    "nozzle_x": (-1050.0, -350.0, 350.0, 1050.0), "nozzle_orifice": 0.4, "nozzle_len": 33.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and drawing quote, computed from PARAMS."""
    L, Dp = p["roof_l"], p["roof_d"]
    rise = p["z_front"] - p["z_rear"]
    slope = math.atan(rise / Dp)
    z_mid = (p["z_front"] + p["z_rear"]) / 2
    zr = lambda y: z_mid - y * math.tan(slope)                 # roof plane height at Y
    half = p["beam"] / 2
    py = p["post_y"]
    beam_under_rear = zr(py) - half / math.cos(slope)
    beam_under_front = zr(-py) - half / math.cos(slope)
    brace_low_rear = beam_under_rear - p["brace_drop"]
    li = p["line_inset"]
    y_line = py - li                                           # nozzle rows at +/-(post_y - inset)
    nozzle_tip = lambda y: zr(y) - (half + p["line_drop"] - 25 + p["nozzle_len"]) / math.cos(slope)
    run_x = 2 * p["post_x"] - 2 * 60
    run_y = (2 * y_line) / math.cos(slope)
    riser = (zr(y_line) - p["line_drop"]) - (p["pump_z"] + p["pump"][2] / 2)
    loop = 2 * run_x + 2 * run_y
    line_len = loop + riser
    ex = p["post_x"] + p["post"] / 2 + p["enc"][0] / 2      # bolted to the post's outer face
    tx, ty = -p["post_x"] + p["tank_inset"][0], py - p["tank_inset"][1]
    return {
        "slope_deg": math.degrees(slope), "z_mid": z_mid, "zr": zr,
        "roof_area_m2": L * Dp / 1e6,
        "roof_true_area_m2": L * Dp / math.cos(slope) / 1e6,
        "post_len_front": beam_under_front - p["plate_t"], "post_len_rear": beam_under_rear - p["plate_t"],
        "beam_under_front": beam_under_front, "beam_under_rear": beam_under_rear,
        "brace_low_rear": brace_low_rear, "brace_low_front": beam_under_front - p["brace_drop"],
        "brace_len": math.hypot(p["brace_drop"], p["brace_reach"]),
        "clear_x": 2 * p["post_x"] - p["post"], "clear_y": 2 * py - p["post"],
        "y_line": y_line,
        "nozzle_tip_rear": nozzle_tip(y_line), "nozzle_tip_front": nozzle_tip(-y_line),
        "line_len_mm": line_len, "loop_len_mm": loop, "riser_mm": riser,
        "line_vol_l": math.pi / 4 * p["line_id"] ** 2 * line_len / 1e6,
        "enc_x": ex, "enc_bot": p["enc_z"] - p["enc"][2] / 2, "enc_top": p["enc_z"] + p["enc"][2] / 2,
        "tank_xy": (tx, ty),
        "tank_gross_l": math.pi / 4 * p["tank_d"] ** 2 * p["tank_h"] / 1e6,
        "overall_h": zr(-Dp / 2) + half + p["fabric_t"],
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def rod(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def shs(cx, cy, z0, size, t, h):
    """Square hollow section standing on z0."""
    return box(cx, cy, z0 + h / 2, size, size, h) - box(cx, cy, z0 + h / 2, size - 2 * t, size - 2 * t, h + 2)


def build_parts(p=PARAMS):
    """Return {key: solid} for BOM items 1 to 15 (the strap and vent are part of items 13 and 14)."""
    b = _b3d()
    D = derived(p)
    zr = D["zr"]
    slope = D["slope_deg"]
    L, Dp = p["roof_l"], p["roof_d"]
    PX, PY, S = p["post_x"], p["post_y"], p["post"]
    half = p["beam"] / 2
    roof = lambda shape: b.Pos(0, 0, D["z_mid"]) * b.Rot(-slope, 0, 0) * shape
    parts = {}

    # 1 posts and knee braces (brace from the post face to the long beam underside)
    posts, braces = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            top = zr(sy * PY) - half / math.cos(math.radians(slope))
            posts.append(shs(sx * PX, sy * PY, p["plate_t"], S, p["post_t"], top - p["plate_t"]))
            a = (sx * (PX - S / 2), sy * PY, top - p["brace_drop"])
            c = (sx * (PX - S / 2 - p["brace_reach"]), sy * PY, top)
            braces.append(rod(a, c, p["brace_od"] / 2))
    parts["posts"] = fuse(posts) + fuse(braces)

    # 2 roof frame, flat in the roof plane
    bm = p["beam"]
    frame = (box(0, -PY, 0, L, bm, bm) + box(0, PY, 0, L, bm, bm)
             + box(-PX, 0, 0, bm, Dp, bm) + box(PX, 0, 0, bm, Dp, bm)
             + box(-p["purlin_x"], 0, 0, p["purlin"], Dp - 100, p["purlin"])
             + box(p["purlin_x"], 0, 0, p["purlin"], Dp - 100, p["purlin"]))
    parts["frame"] = roof(frame)

    # 3 shade fabric over the frame
    parts["fabric"] = roof(box(0, 0, half + p["fabric_t"] / 2, L, Dp, p["fabric_t"]))

    # 4 base plates and anchors
    pl, pt, ap = p["plate"], p["plate_t"], p["anchor_pitch"] / 2
    plates = fuse(box(sx * PX, sy * PY, pt / 2, pl, pl, pt) for sx in (-1, 1) for sy in (-1, 1))
    anchors = fuse(zcyl(sx * PX + dx, sy * PY + dy, (pt + 40 - p["anchor_embed"]) / 2,
                        p["anchor_d"] / 2, p["anchor_embed"] + pt + 40)
                   for sx in (-1, 1) for sy in (-1, 1) for dx in (-ap, ap) for dy in (-ap, ap))
    parts["plates"] = plates + anchors

    # 5 solar panel on two rails
    pw, pd, ph = p["panel"]
    parts["panel"] = roof(box(0, p["panel_y"], half + 70, pw, pd, ph)
                          + box(-p["purlin_x"], p["panel_y"], half + 30, 40, pd + 30, 40)
                          + box(p["purlin_x"], p["panel_y"], half + 30, 40, pd + 30, 40))

    # 8 enclosure bolted to the post's outer face; 6 battery and 7 MPPT inside
    ew, ed, eh = p["enc"]
    ex, ez = D["enc_x"], p["enc_z"]
    parts["enclosure"] = box(ex, PY, ez, ew, ed, eh)
    bw, bd, bh = p["battery"]
    parts["battery"] = box(ex, PY - 60, ez - 90, bw, bd, bh)
    mw, md, mh = p["mppt"]
    parts["mppt"] = box(ex, PY + 90, ez + 90, mw, md, mh)

    # 9 sensor head: shield plates, arm, PIR
    sz = p["shield_z"]
    shield = fuse(zcyl(PX + S / 2 + p["arm_l"] - 10, -PY, sz + k * 22, p["shield_r"] - 2 * k, 10) for k in range(6))
    arm = rod((PX + S / 2, -PY, sz + 50), (PX + S / 2 + p["arm_l"], -PY, sz + 50), 12)
    pir = box(0, -PY + 40, D["beam_under_front"] - 25, 60, 60, 50)
    parts["sensors"] = shield + arm + pir

    # 13 tank with strap; 10 pump; 11 filter; 14 drain valve and vacuum breaker
    tx, ty = D["tank_xy"]
    tr, th = p["tank_d"] / 2, p["tank_h"]
    tank = zcyl(tx, ty, th / 2, tr, th)
    strap = zcyl(tx, ty, th * 0.6, tr + 6, 40) - zcyl(tx, ty, th * 0.6, tr + 1, 42)
    strap = strap + rod((tx - tr * 0.7, ty + tr * 0.7, th * 0.6), (-PX + S / 2, PY - 10, th * 0.6), 6)
    parts["tank"] = tank + strap
    qw, qd, qh = p["pump"]
    parts["pump"] = box(-PX + 150, PY - 100, p["pump_z"], qw, qd, qh)
    parts["filter"] = zcyl(-PX + 110, PY - 230, p["pump_z"] - 20, p["filter_r"], p["filter_h"])
    dw, dd, dh = p["drain"]
    y_line = D["y_line"]
    vent = roof(zcyl(0, -y_line, -half - p["line_drop"] + 40, 12, 45))
    parts["drain"] = box(-PX + 60, PY - 60 - 130, p["pump_z"] + qh / 2 + 60, dw, dd, dh) + vent

    # 12 mist line loop and nozzles, in the roof plane; riser down the rear left post
    lz = -half - p["line_drop"] + 25
    x0, x1 = -PX + 60, PX - 60
    r = p["line_od"] / 2
    loop = (rod((x0, -y_line, lz), (x1, -y_line, lz), r) + rod((x0, y_line, lz), (x1, y_line, lz), r)
            + rod((x0, -y_line, lz), (x0, y_line, lz), r) + rod((x1, -y_line, lz), (x1, y_line, lz), r))
    noz = fuse(box(x, y, lz - p["nozzle_len"] / 2, 20, 20, p["nozzle_len"])
               for x in p["nozzle_x"] for y in (-y_line, y_line))
    riser_top = zr(y_line) + (lz) / math.cos(math.radians(slope))
    riser = rod((x0, y_line, p["pump_z"] + qh / 2), (x0, y_line, riser_top), r)
    parts["mistline"] = roof(loop + noz) + riser

    # 15 supply hose and cable runs (simplified)
    parts["harness"] = (rod((tx + 150, ty + 120, th - 50), (-PX + 150, PY - 100, p["pump_z"] - qh / 2), 8)
                        + rod((PX + 60, PY, zr(PY) - 80), (PX + 60, PY, D["enc_top"]), 6)
                        + rod((PX + 60, -PY + 60, sz + 50), (PX + 60, -PY + 60, zr(-PY) - 80), 6)
                        + rod((PX + 60, -PY + 60, zr(-PY) - 80), (PX + 60, PY - 60, zr(PY) - 80), 6))
    return parts


GROUPS = {
    "frame": ["posts", "frame", "plates"],
    "water-system": ["tank", "pump", "filter", "drain", "mistline", "harness"],
}


def assembly(p=PARAMS):
    b = _b3d()
    parts = build_parts(p)
    return b.Compound(children=list(parts.values())), parts


if __name__ == "__main__":
    b = _b3d()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    asm, parts = assembly()
    exports = {"coolshade-assembly": asm}
    for name, keys in GROUPS.items():
        fresh = build_parts()          # new solids: a shape can only be the child of one compound
        exports[name] = b.Compound(children=[fresh[k] for k in keys])
    for name, shape in exports.items():
        b.export_step(shape, str(out / "step" / f"{name}.step"))
        b.export_stl(shape, str(out / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm, volume {shape.volume / 1e6:.2f} L")
    D = derived()
    print(f"slope {D['slope_deg']:.2f} deg; rear brace low point {D['brace_low_rear']:.0f} mm; "
          f"nozzle tips {D['nozzle_tip_rear']:.0f} (rear) and {D['nozzle_tip_front']:.0f} (front) mm; "
          f"mist line {D['line_len_mm'] / 1000:.2f} m, {D['line_vol_l']:.2f} L")
