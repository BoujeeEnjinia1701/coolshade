"""CoolShade parametric model (build123d), TRL 3, constructable design (CSH-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL and prints the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Exports into cad/step and cad/stl:
    coolshade-assembly   the whole canopy with its water, power and control parts and fixings
    frame                posts, knee braces, cleats, roof frame, base plates and anchors
    water-system         tank with strap and stops, equipment plate, pump, filter, drain valve,
                         vacuum breaker, mist line loop with nozzles and clips, hoses

Axes (mm): X runs along the curb, Y across the sidewalk (street side is -Y), Z up with the
sidewalk surface at Z = 0. The roof is a mono-pitch plane, high at the street edge.

Every part is modelled as it is made or bought, and every joint as it is fixed: the long beams
sit square on the post tops and are held by angle cleats; the end beams, purlins and the panel
bearer butt against the beam faces on angle cleats; the knee braces have flattened, bent ends;
the posts stand on base plates between two anchored angle cleats; bolts into the closed beams go
into rivet nuts, so nothing stands proud where the shade cloth runs. Holes are cut where bolts
and cables pass. checks() tests every pair of parts for overlap and every joint for contact with
build123d booleans and distances.

The same PARAMS feed docs/04-calcs/sizing.py (CSH-CAL-001), cad/src/sheets.py (CSH-DWG-001),
cad/src/build_plan_media.py (CSH-BLD-001 pictures, CSH-DWG-101 onward) and
cad/src/concept_media.py. Main dimensions and interfaces only; drawings carry no tolerances
before TRL 4.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # roof plan and slope; roof plane (beam centre line) at the street and rear edges
    "roof_l": 3000.0, "roof_d": 2400.0,
    "z_front": 2940.0, "z_rear": 2640.0,
    # 1 posts: 80 x 80 x 3 mm SHS on a 2800 x 2350 mm grid (long beams sit on them, at the roof edges)
    "post_x": 1400.0, "post_y": 1175.0, "post": 80.0, "post_t": 3.0,
    # knee braces: 32 mm tube, ends flattened and bent; bends 350 mm down the post and 350 mm along the beam
    "brace_od": 32.0, "brace_t": 2.5, "brace_drop": 350.0, "brace_reach": 350.0, "brace_tab": 45.0,
    # 2 roof frame: 50 x 50 x 2 long beams (horizontal), end beams at the roof ends, 40 x 40 x 2
    #   purlins and a 50 x 50 x 2 panel bearer; cleats 50 x 50 x 5 angle
    "beam": 50.0, "beam_t": 2.0, "purlin": 40.0, "purlin_t": 2.0, "purlin_x": 530.0, "end_x": 1475.0,
    "bearer_y": 560.0, "cleat": 50.0, "cleat_t": 5.0, "head_cleat_l": 46.0,
    # 3 shade fabric, laced over the frame, with a notch at the rear for the panel
    "fabric_t": 4.0, "fabric_lift": 3.2,
    # 4 base plates, base cleats (75 x 75 x 6 angle, 220 long) and M16 anchors at 160 mm centres
    "plate": 220.0, "plate_t": 10.0, "anchor_d": 16.0, "anchor_pitch": 160.0, "anchor_embed": 125.0,
    "base_cleat": 75.0, "base_cleat_t": 6.0,
    # 5 solar panel on two rails, L-feet on the bearer and the rear beam; rear edge at the roof edge
    "panel": (1000.0, 670.0, 35.0), "panel_y": 867.6, "rail": 40.0, "rail_x": 300.0, "rail_gap": 15.0,
    # 8 enclosure (houses 6 battery and 7 MPPT) on two rails on the outer face of the rear right post
    "enc": (160.0, 320.0, 420.0), "enc_z": 1650.0, "enc_y": 1090.0, "enc_rail": (40.0, 6.0, 340.0),
    "battery": (100.0, 180.0, 170.0), "mppt": (40.0, 90.0, 140.0),
    # 9 sensor head: 40 x 40 x 4 angle arm on the street face of the front right post; PIR under the front beam
    "shield_r": 60.0, "shield_z": 2400.0, "arm_l": 300.0, "arm": 40.0, "arm_t": 4.0,
    # 10 pump, 11 filter, 14 drain valve: on an equipment plate on the front face of the rear left post
    "pump": (200.0, 130.0, 140.0), "pump_z": 1250.0,
    "filter_r": 45.0, "filter_h": 240.0,
    "eq_plate": (-1530.0, -1210.0, 750.0, 1380.0, 3.0),        # x0, x1, z0, z1, thickness
    "drain": (90.0, 60.0, 70.0),
    # 13 tank: on the slab inside the rear left corner, strapped to the rear left post
    "tank_d": 540.0, "tank_h": 700.0, "tank_xy": (-1050.0, 820.0), "tank_nominal_l": 120.0,
    # 12 mist line: closed loop under the long beams (70 mm inboard) and the end beams, 8 nozzles
    "line_od": 9.5, "line_id": 6.5, "line_inset": 70.0, "line_drop": 35.0,
    "nozzle_x": (-1050.0, -350.0, 350.0, 1050.0), "nozzle_orifice": 0.4, "nozzle_len": 33.0,
    # 15 harness: cables run inside the posts and beams; hoses at the rear left corner; tank level switch cable
    "cable_r": 3.5,
}

AF = {5: 8.0, 6: 10.0, 8: 13.0, 10: 17.0, 12: 19.0, 16: 24.0}   # hex across flats


@dataclass
class Comp:
    name: str
    shape: object
    bom: int          # bom/bom.csv line
    kind: str         # made, bought, fixing
    group: str        # concept media group (None for fixings)


def derived(p=PARAMS):
    """Dimensions the calc note, drawings and build plan quote, computed from PARAMS."""
    L, Dp = p["roof_l"], p["roof_d"]
    rise = p["z_front"] - p["z_rear"]
    slope = math.atan(rise / Dp)
    t, c = math.tan(slope), math.cos(slope)
    z_mid = (p["z_front"] + p["z_rear"]) / 2
    zr = lambda y: z_mid - y * t                                # roof plane height at plan Y
    half = p["beam"] / 2
    PY, PX = p["post_y"], p["post_x"]
    under_f, under_r = zr(-PY) - half, zr(PY) - half           # long beams are horizontal and square
    tab = p["brace_tab"]
    yl = PY - p["line_inset"]
    zline = lambda y: zr(y) - half / c - p["line_drop"]        # line centre under the sloping end beams
    run_x = 2 * p["end_x"]
    run_y = 2 * yl / c
    riser = zline(yl) - 1070.0
    loop = 2 * run_x + 2 * run_y
    line_len = loop + riser + 35.0
    ex = PX + p["post"] / 2 + p["enc_rail"][1] + p["enc"][0] / 2
    tx, ty = p["tank_xy"]
    b_len = math.hypot(p["brace_drop"] - 2.5, p["brace_reach"] - 2.5)
    return {
        "slope_deg": math.degrees(slope), "z_mid": z_mid, "zr": zr, "zline": zline,
        "roof_area_m2": L * Dp / 1e6, "roof_true_area_m2": L * Dp / c / 1e6,
        "beam_under_front": under_f, "beam_under_rear": under_r,
        "post_len_front": under_f - p["plate_t"], "post_len_rear": under_r - p["plate_t"],
        "brace_low_rear": under_r - p["brace_drop"] - tab, "brace_low_front": under_f - p["brace_drop"] - tab,
        "brace_len": b_len + 2 * tab, "brace_tube_len": b_len - 60.0,
        "clear_x": 2 * PX - p["post"], "clear_y": 2 * PY - p["post"],
        "y_line": yl, "line_z_front": zline(-yl), "line_z_rear": zline(yl),
        "nozzle_tip_rear": zline(yl) - p["nozzle_len"], "nozzle_tip_front": zline(-yl) - p["nozzle_len"],
        "line_len_mm": line_len, "loop_len_mm": loop, "riser_mm": riser,
        "line_vol_l": math.pi / 4 * p["line_id"] ** 2 * line_len / 1e6,
        "enc_x": ex, "enc_bot": p["enc_z"] - p["enc"][2] / 2, "enc_top": p["enc_z"] + p["enc"][2] / 2,
        "tank_xy": (tx, ty), "tank_gross_l": math.pi / 4 * p["tank_d"] ** 2 * p["tank_h"] / 1e6,
        "overall_h": zr(-Dp / 2) + half + p["fabric_lift"] + p["fabric_t"],
        "end_beam_len": 2 * (PY - half) / c, "purlin_len": 2 * (PY - half) / c,
        "bearer_len": 2 * (p["purlin_x"] - p["purlin"] / 2),
        "long_beam_len": L,
        "fabric_notch": (2 * (p["purlin_x"] - p["purlin"] / 2), Dp / 2 - (p["bearer_y"] - half)),
        "arm_z": p["shield_z"], "shield_low": p["shield_z"] + p["arm"] / 2 - p["arm_t"] - 46 - 104,
    }


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


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


def _pt(axis, u, v, s):
    return {"x": (s, u, v), "y": (u, s, v), "z": (u, v, s)}[axis]


def acyl(axis, u, v, s0, s1, r):
    return rod(_pt(axis, u, v, s0), _pt(axis, u, v, s1), r)


def ahex(axis, u, v, s0, s1, af):
    b = _b3d()
    a, c = b.Vector(*_pt(axis, u, v, s0)), b.Vector(*_pt(axis, u, v, s1))
    d = c - a
    return b.Plane(origin=a, z_dir=d.normalized()) * b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), d.length)


def bolt(axis, u, v, s0, s1, d, nut=True, head=True, tip=None):
    """A bolt along axis at (u, v) whose head bears on the plane s0 and whose clamped thickness
    ends at s1 (a nut there if nut, else the shank runs to tip, into a rivet nut or the slab).
    Returns (solid, hole): hole is the clearance hole from s0 to s1 to cut from the parts."""
    sg = 1 if s1 > s0 else -1
    parts = []
    if head:
        parts.append(ahex(axis, u, v, s0 - sg * 0.65 * d, s0, AF[d]))
    end = s1 + sg * (0.8 * d + 0.3 * d) if nut else (tip if tip is not None else s1 + sg * 6)
    parts.append(acyl(axis, u, v, s0, end, d / 2 - 0.3))
    if nut:
        parts.append(ahex(axis, u, v, s1, s1 + sg * 0.8 * d, AF[d]))
    return fuse(parts), acyl(axis, u, v, s0 - sg * 0.01, s1 + sg * 0.01, d / 2 + 0.5)


def roof_plane(p=PARAMS):
    """build123d Plane in the roof: local x along the curb, local y down the slope (toward +Y),
    local z normal to the roof, origin on the roof plane at plan Y = 0."""
    b = _b3d()
    th = math.atan((p["z_front"] - p["z_rear"]) / p["roof_d"])
    return b.Plane(origin=(0, 0, (p["z_front"] + p["z_rear"]) / 2), x_dir=(1, 0, 0),
                   z_dir=(0, math.sin(th), math.cos(th)))


def roof_s(y, n, p=PARAMS):
    """Slope coordinate s of the point at plan y and normal offset n in the roof plane."""
    th = math.atan((p["z_front"] - p["z_rear"]) / p["roof_d"])
    return (y - n * math.sin(th)) / math.cos(th)


def sloped_shs(x, n_c, size, t, y0, y1, p=PARAMS):
    """SHS along the roof slope at x, centre n_c above the roof plane, ends cut square to plan Y
    at y0 and y1 (so they butt flat against the vertical faces of the long beams)."""
    b = _b3d()
    RP = roof_plane(p)
    long_ = (y1 - y0) * 2
    tube = RP * (b.Pos(x, 0, n_c) * b.Box(size, long_, size) - b.Pos(x, 0, n_c) * b.Box(size - 2 * t, long_ + 2, size - 2 * t))
    return tube & bx(x - size, x + size, y0, y1, 0, 4000)


def hull_band(circ, rect, z0, h, t):
    """A strap band of thickness t round a circle (cx, cy, r) and a square (x0, x1, y0, y1)."""
    b = _b3d()
    cx, cy, r = circ

    def hull_pts(off):
        rr = (r + off) / math.cos(math.pi / 120)          # polygon edges just outside the true circle
        pts = [(cx + rr * math.cos(a), cy + rr * math.sin(a)) for a in [i * math.pi / 60 for i in range(120)]]
        x0, x1, y0, y1 = rect
        for (px, py) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            for a in range(0, 360, 15):
                pts.append((px + off * math.cos(math.radians(a)), py + off * math.sin(math.radians(a))))
        return _convex_hull(pts)

    def solid(off):
        w = b.Wire.make_polygon([b.Vector(x, y, z0) for x, y in hull_pts(off)], close=True)
        return b.extrude(b.Face(w), h)
    return solid(t) - solid(0.0)


def _convex_hull(pts):
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))

    def cross(o, a, c):
        return (a[0] - o[0]) * (c[1] - o[1]) - (a[1] - o[1]) * (c[0] - o[0])
    lower, upper = [], []
    for q in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    return lower[:-1] + upper[:-1]


def polyline_rod(points, r):
    """A cable or hose: rods between consecutive points with a ball at every bend."""
    b = _b3d()
    out = None
    for a, c in zip(points, points[1:]):
        seg = rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out = out + b.Pos(*q) * b.Sphere(r)
    return out


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name, with all bolt and cable holes cut."""
    b = _b3d()
    D = derived(p)
    zr = D["zr"]
    th = math.radians(D["slope_deg"])
    RP = roof_plane(p)
    PX, PY, S, T = p["post_x"], p["post_y"], p["post"], p["post_t"]
    half, bt = p["beam"] / 2, p["beam_t"]
    C, holes = {}, {}

    def add(key, name, shape, bom, kind, group):
        C[key] = Comp(name, shape, bom, kind, group)

    def hole_in(keys, h):
        for k in keys:
            holes.setdefault(k, []).append(h)

    posts = {(sx, sy): (sx * PX, sy * PY) for sx in (1, -1) for sy in (-1, 1)}
    pname = {(1, -1): "front right", (-1, -1): "front left", (1, 1): "rear right", (-1, 1): "rear left"}
    pkey = {k: f"post_{'f' if k[1] < 0 else 'r'}{'r' if k[0] > 0 else 'l'}" for k in posts}

    # ---- 4 base plates, base cleats, anchors; 1 posts
    pt_, bc, bct = p["plate_t"], p["base_cleat"], p["base_cleat_t"]
    ap = p["anchor_pitch"] / 2
    base_bolts, anchors = [], []
    for k, (cx, cy) in posts.items():
        pk = pkey[k]
        top = zr(cy) - half
        add(pk, f"Post, {pname[k]}", shs(cx, cy, pt_, S, T, top - pt_), 1, "made", "posts")
        add(f"plate_{pk[5:]}", f"Base plate, {pname[k]}", box(cx, cy, pt_ / 2, p["plate"], p["plate"], pt_), 4, "made", "plates")
        cl = []
        for sg in (-1, 1):
            f = cx + sg * S / 2
            cl.append(bx(f, f + sg * bct, cy - 110, cy + 110, pt_, pt_ + bc) + bx(f, f + sg * bc, cy - 110, cy + 110, pt_, pt_ + bct))
        add(f"bcleat_{pk[5:]}", f"Base cleats (2), {pname[k]}", fuse(cl), 4, "made", "plates")
        for z in (pt_ + 35, pt_ + 62):
            s_, h_ = bolt("x", cy, z, cx - S / 2 - bct, cx + S / 2 + bct, 12)
            base_bolts.append(s_)
            hole_in([pk, f"bcleat_{pk[5:]}"], h_)
        for dx in (-ap, ap):
            for dy in (-ap, ap):
                s_, h_ = bolt("z", cx + dx, cy + dy, pt_ + bct, 0.0, 16, nut=False, tip=-p["anchor_embed"])
                s_ = s_ + zcyl(cx + dx, cy + dy, pt_ + bct + 0.65 * 16 + 3, 7.7, 6)       # stud end above the nut
                anchors.append(s_)
                hole_in([f"plate_{pk[5:]}", f"bcleat_{pk[5:]}"], h_)
    add("base_bolts", "M12 bolts, base cleats (8)", fuse(base_bolts), 16, "fixing", None)
    add("anchors", "M16 anchors with nuts (16)", fuse(anchors), 4, "fixing", None)

    # ---- 2 long beams on the post tops, head cleats
    lb = {}
    for sy in (-1, 1):
        zc = zr(sy * PY)
        lb[sy] = box(0, sy * PY, zc, p["roof_l"], p["beam"], p["beam"]) - box(0, sy * PY, zc, p["roof_l"] + 2, p["beam"] - 2 * bt, p["beam"] - 2 * bt)
        add(f"beam_{'f' if sy < 0 else 'r'}", f"Long beam, {'front (street)' if sy < 0 else 'rear'}", lb[sy], 2, "made", "frame")
    cw, ctk, chl = p["cleat"], p["cleat_t"], p["head_cleat_l"]
    head_bolts = []
    for k, (cx, cy) in posts.items():
        pk = pkey[k]
        top = zr(cy) - half
        bk = f"beam_{'f' if cy < 0 else 'r'}"
        cl = []
        for sg in (-1, 1):
            f = cx + sg * S / 2
            cl.append(bx(f, f + sg * ctk, cy - chl / 2, cy + chl / 2, top - cw, top)
                      + bx(f, f + sg * cw, cy - chl / 2, cy + chl / 2, top - ctk, top))
            s_, h_ = bolt("z", cx + sg * (S / 2 + ctk + (cw - ctk) / 2), cy, top - ctk, top + bt, 8, nut=False, tip=top + bt + 6)
            head_bolts.append(s_)
            hole_in([f"hcleat_{pk[5:]}", bk], h_)
        add(f"hcleat_{pk[5:]}", f"Head cleats (2), {pname[k]}", fuse(cl), 2, "made", "frame")
        s_, h_ = bolt("x", cy, top - 28, cx - S / 2 - ctk, cx + S / 2 + ctk, 10)
        head_bolts.append(s_)
        hole_in([pk, f"hcleat_{pk[5:]}"], h_)
    add("head_bolts", "Head cleat bolts: M10 through, M8 into rivet nuts", fuse(head_bolts), 16, "fixing", None)

    # ---- knee braces with flattened, bent ends
    brace_bolts = []
    drop, reach, tab = p["brace_drop"], p["brace_reach"], p["brace_tab"]
    tw, tt = math.pi * p["brace_od"] / 2, 2 * p["brace_t"]          # flattened width and thickness
    for k, (cx, cy) in posts.items():
        pk = pkey[k]
        sx = 1 if cx > 0 else -1
        zb = zr(cy) - half
        face = cx - sx * S / 2
        B1 = (face - sx * tt / 2, cy, zb - drop)
        B2 = (face - sx * reach, cy, zb - tt / 2)
        u = b.Vector(B2[0] - B1[0], 0, B2[2] - B1[2]).normalized()
        n = b.Vector(-u.Z, 0, u.X) if sx > 0 else b.Vector(u.Z, 0, -u.X)
        tab1 = bx(face, face - sx * tt, cy - tw / 2, cy + tw / 2, B1[2] - tab, B1[2])
        tab2 = bx(B2[0], B2[0] - sx * tab, cy - tw / 2, cy + tw / 2, zb - tt, zb)
        fl1 = b.Plane(origin=b.Vector(*B1) + u * 15, x_dir=u, z_dir=n) * b.Box(30, tw, tt)
        fl2 = b.Plane(origin=b.Vector(*B2) - u * 15, x_dir=u, z_dir=n) * b.Box(30, tw, tt)
        a_, c_ = b.Vector(*B1) + u * 30, b.Vector(*B2) - u * 30
        tube = rod(tuple(a_), tuple(c_), p["brace_od"] / 2) - rod(tuple(a_ - u), tuple(c_ + u), p["brace_od"] / 2 - p["brace_t"])
        add(f"brace_{pk[5:]}", f"Knee brace, {pname[k]}", fuse([tab1, tab2, fl1, fl2, tube]), 1, "made", "posts")
        s_, h_ = bolt("x", cy, B1[2] - tab / 2, face - sx * tt, face + sx * S, 10)
        brace_bolts.append(s_)
        hole_in([f"brace_{pk[5:]}", pk], h_)
        s_, h_ = bolt("z", B2[0] - sx * tab / 2, cy, zb - tt, zb + bt, 8, nut=False, tip=zb + bt + 6)
        brace_bolts.append(s_)
        hole_in([f"brace_{pk[5:]}", f"beam_{'f' if cy < 0 else 'r'}"], h_)
    add("brace_bolts", "Knee brace bolts: M10 through, M8 into rivet nuts", fuse(brace_bolts), 16, "fixing", None)

    # ---- end beams, purlins, bearer and their cleats
    yin = PY - half
    ex, px_ = p["end_x"], p["purlin_x"]
    for sx in (-1, 1):
        add(f"endb_{'r' if sx > 0 else 'l'}", f"End beam, {'right' if sx > 0 else 'left'}",
            sloped_shs(sx * ex, 0.0, p["beam"], bt, -yin, yin, p), 2, "made", "frame")
        add(f"purlin_{'r' if sx > 0 else 'l'}", f"Purlin, {'right' if sx > 0 else 'left'}",
            sloped_shs(sx * px_, half - p["purlin"] / 2, p["purlin"], p["purlin_t"], -yin, yin, p), 2, "made", "frame")
    by = p["bearer_y"]
    bxl = px_ - p["purlin"] / 2
    add("bearer", "Panel bearer", box(0, by, zr(by), 2 * bxl, p["beam"], p["beam"]) - box(0, by, zr(by), 2 * bxl + 2, p["beam"] - 2 * bt, p["beam"] - 2 * bt),
        2, "made", "frame")

    def zrange_member(key_kind, x, y):
        """Lowest and highest Z of a member's section at plan y."""
        c = math.cos(th)
        if key_kind == "long":
            zc = zr(math.copysign(PY, y))
            return zc - half, zc + half
        if key_kind == "bearer":
            return zr(by) - half, zr(by) + half
        if key_kind == "end":
            return zr(y) - half / c, zr(y) + half / c
        if key_kind == "purlin":
            nc = half - p["purlin"] / 2
            return zr(y) + (nc - p["purlin"] / 2) / c, zr(y) + (nc + p["purlin"] / 2) / c

    frame_cleats, frame_bolts = [], []

    def corner(X0, Y0, tx, ty, kA, kB, kindA, kindB, hgt, keyA, keyB):
        """Angle cleat with leg A on the y-face (plane Y0) of member A and leg B on the x-face
        (plane X0) of member B; tx and ty point away from B and A."""
        ys = [Y0 + ty * v for v in (0, cw)]
        zA = zrange_member(kindA, X0, Y0)
        zB = [zrange_member(kindB, X0, yy) for yy in ys]
        lo = max(zA[0], min(z[0] for z in zB))
        hi = min(zA[1], max(z[1] for z in zB))
        zc = (lo + hi) / 2
        z0, z1 = zc - hgt / 2, zc + hgt / 2
        legA = bx(X0, X0 + tx * cw, Y0, Y0 + ty * ctk, z0, z1)
        legB = bx(X0, X0 + tx * ctk, Y0, Y0 + ty * cw, z0, z1)
        frame_cleats.append(legA + legB)
        wA = p["beam_t"] if kindA != "purlin" else p["purlin_t"]
        wB = p["beam_t"] if kindB != "purlin" else p["purlin_t"]
        s_, h_ = bolt("y", X0 + tx * (ctk + (cw - ctk) / 2 - 2.5), zc, Y0 + ty * ctk, Y0 - ty * wA, 8, nut=False, tip=Y0 - ty * (wA + 6))
        frame_bolts.append(s_)
        hole_in(["frame_cleats", keyA], h_)
        s_, h_ = bolt("x", Y0 + ty * (ctk + (cw - ctk) / 2 - 2.5), zc, X0 + tx * ctk, X0 - tx * wB, 8, nut=False, tip=X0 - tx * (wB + 6))
        frame_bolts.append(s_)
        hole_in(["frame_cleats", keyB], h_)

    for sx in (-1, 1):
        for sy in (-1, 1):
            corner(sx * (ex - half), sy * yin, -sx, -sy, "long", "end", "long", "end", 40.0,
                   f"beam_{'f' if sy < 0 else 'r'}", f"endb_{'r' if sx > 0 else 'l'}")
            corner(sx * (px_ - p["purlin"] / 2), sy * yin, -sx, -sy, "long", "purlin", "long", "purlin", 30.0,
                   f"beam_{'f' if sy < 0 else 'r'}", f"purlin_{'r' if sx > 0 else 'l'}")
        corner(sx * bxl, by - half, -sx, -1, "bearer", "purlin", "bearer", "purlin", 30.0, "bearer", f"purlin_{'r' if sx > 0 else 'l'}")
    add("frame_cleats", "Frame cleats (10)", fuse(frame_cleats), 2, "made", "frame")
    add("frame_bolts", "Frame cleat bolts, M8 into rivet nuts (20)", fuse(frame_bolts), 16, "fixing", None)

    # ---- 3 shade fabric: laced over the frame, notch at the rear for the panel
    c_ = math.cos(th)
    nf = half + p["fabric_lift"]
    Ls = p["roof_d"] / c_
    fab = RP * b.Pos(0, 0, nf + p["fabric_t"] / 2) * b.Box(p["roof_l"], Ls + 40, p["fabric_t"])
    fab = fab & bx(-p["roof_l"] / 2, p["roof_l"] / 2, -p["roof_d"] / 2, p["roof_d"] / 2, 0, 4000)
    fab = fab - bx(-bxl, bxl, by - half, p["roof_d"] / 2 + 10, 0, 4000)
    add("fabric", "Shade fabric", fab, 3, "bought", "fabric")

    # ---- 5 panel, rails, L-feet, end clamps
    pw, pd, ph = p["panel"]
    rail, rx, rg = p["rail"], p["rail_x"], p["rail_gap"]
    n_rail0 = half + rg                           # rail bottom above the roof plane at the foot centre
    n_pan = n_rail0 + rail
    sc = roof_s(p["panel_y"], n_pan, p)
    sa, sb = sc - pd / 2, sc + pd / 2
    add("panel", "Solar panel, 100 W", RP * b.Pos(0, sc, n_pan + ph / 2) * b.Box(pw, pd, ph), 5, "bought", "panel")
    rails = fuse(RP * b.Pos(sx * rx, sc, n_rail0 + rail / 2) * b.Box(rail, pd + 50, rail) for sx in (-1, 1))
    clamps = fuse(RP * b.Pos(sx * rx, s0 + sg * 10, n_pan + ph / 2) * b.Box(rail, 20, ph)
                  for sx in (-1, 1) for s0, sg in ((sa, -1), (sb, 1)))
    feet, foot_bolts = [], []
    for yc, ttop, keyb in ((by, zr(by) + half, "bearer"), (PY, zr(PY) + half, "beam_r")):
        for sx in (-1, 1):
            xo = sx * (rx + rail / 2)
            base = bx(sx * (rx - 10), xo + sx * 4, yc - 20, yc + 20, ttop, ttop + 4)
            leg = bx(xo, xo + sx * 4, yc - 20, yc + 20, ttop, ttop + 50)
            feet.append(base + leg)
            s_, h_ = bolt("z", sx * (rx + 5), yc, ttop + 4, ttop - bt, 8, nut=False, tip=ttop - bt - 6)
            foot_bolts.append(s_)
            hole_in(["feet", keyb], h_)
    add("rails", "Panel rails (2)", rails, 5, "bought", "panel")
    add("feet", "L-feet (4)", fuse(feet), 5, "bought", "panel")
    add("clamps", "Panel end clamps (4)", clamps, 5, "bought", "panel")
    add("foot_bolts", "L-foot bolts, M8 into rivet nuts (4)", fuse(foot_bolts), 16, "fixing", None)

    # ---- 8 enclosure on rails on the rear right post; 6 battery, 7 MPPT, controller board
    ew, ed, eh = p["enc"]
    rh, rt, rl = p["enc_rail"]
    cx, cy = PX, PY
    xr0 = cx + S / 2
    ey, ez = p["enc_y"], p["enc_z"]
    rz = (ez - 130, ez + 130)
    add("enc_rails", "Enclosure rails (2)", fuse(bx(xr0, xr0 + rt, ey - rl / 2, ey + rl / 2, z - rh / 2, z + rh / 2) for z in rz), 8, "made", "enclosure")
    rail_bolts = []
    for z in rz:
        for yb_ in (cy - 25, cy + 25):
            s_, h_ = bolt("x", yb_, z, xr0 + rt, xr0 - S, 10, head=False)
            rail_bolts.append(s_)
            hole_in(["enc_rails", "post_rr"], h_)
    add("rail_bolts", "Enclosure rail bolts, M10 countersunk (4)", fuse(rail_bolts), 16, "fixing", None)
    x0e = xr0 + rt
    w = 2.0
    shell = bx(x0e, x0e + ew, ey - ed / 2, ey + ed / 2, ez - eh / 2, ez + eh / 2) - bx(x0e + w, x0e + ew - w, ey - ed / 2 + w, ey + ed / 2 - w, ez - eh / 2 + w, ez + eh / 2 - w)
    glands = []
    gl_y = (ey - 90, ey - 9, cy - 13)
    for gy in gl_y:
        glands.append(zcyl(x0e + 134, gy, ez - eh / 2 - 7.5, 10.5, 15) + zcyl(x0e + 134, gy, ez - eh / 2 + w + 3, 11, 6))
        shell = shell - zcyl(x0e + 134, gy, ez - eh / 2 + w / 2, 8.25, w + 0.02)
    screws = []
    for z in rz:
        for yy in (ey - 130, ey + 130):
            screws.append(acyl("x", yy, z, x0e + w, x0e + w + 4, 5.0))
            shell = shell - acyl("x", yy, z, x0e - 0.01, x0e + w + 0.01, 3.3)
    bosses = fuse(acyl("x", yy, zz, x0e + w, x0e + w + 6, 5.0) for yy in (ey - 100, ey + 110) for zz in (ez + 0, ez + 180))
    gear = bx(x0e + w + 6, x0e + w + 8, ey - 110, ey + 120, ez - 10, ez + 190)
    add("enclosure", "Enclosure, IP65", fuse([shell] + glands + screws + [bosses, gear]), 8, "bought", "enclosure")
    bw, bd_, bh = p["battery"]
    add("battery", "LiFePO4 battery", bx(x0e + w, x0e + w + bw, ey - 100, ey - 100 + bd_, ez - eh / 2 + w, ez - eh / 2 + w + bh), 6, "bought", "battery")
    mw, md, mh = p["mppt"]
    xg = x0e + w + 8
    add("mppt", "MPPT charge controller", bx(xg, xg + mw, ey - 100, ey - 100 + md, ez + 30, ez + 30 + mh), 7, "bought", "mppt")
    add("board", "Controller board", bx(xg, xg + 20, ey + 10, ey + 110, ez + 40, ez + 150), 8, "bought", "mppt")

    # ---- 9 sensor arm, radiation shield, PIR
    fx, fy = PX, -PY
    ya = fy - S / 2
    az = p["shield_z"]
    aw, at = p["arm"], p["arm_t"]
    xa0, xa1 = fx - 35, fx + S / 2 + p["arm_l"]
    arm = bx(xa0, xa1, ya - at, ya, az - aw / 2, az + aw / 2) + bx(xa0, xa1, ya - aw, ya, az + aw / 2 - at, az + aw / 2)
    arm_bolts = []
    for xb_ in (fx - 15, fx + 15):
        s_, h_ = bolt("y", xb_, az - 2, ya - at, ya + S, 8)
        arm_bolts.append(s_)
        hole_in(["arm", "post_fr"], h_)
    shx, shy = xa1 - 50, ya - aw / 2 - 4
    s_, h_ = bolt("z", shx, shy, az + aw / 2, az + aw / 2 - at - 4, 8, nut=False, tip=az + aw / 2 - at - 4)
    arm_bolts.append(s_)
    hole_in(["arm", "shield"], h_)
    add("arm", "Sensor arm", arm, 9, "made", "sensors")
    add("arm_bolts", "Sensor arm bolts, M8 (3)", fuse(arm_bolts), 16, "fixing", None)
    ztop = az + aw / 2 - at
    sh = zcyl(shx, shy, ztop - 2, 18, 4) + zcyl(shx, shy, ztop - 4 - 21, 8, 42)
    d0 = ztop - 4 - 42
    for k in range(6):
        sh = sh + (zcyl(shx, shy, d0 - 20 * k - 2, p["shield_r"], 4) - zcyl(shx, shy, d0 - 20 * k - 2, 20, 5))
    for a in (90, 210, 330):
        sh = sh + zcyl(shx + 45 * math.cos(math.radians(a)), shy + 45 * math.sin(math.radians(a)), d0 - 50, 3, 100)
    sh = sh + zcyl(shx, shy, d0 - 45, 8, 90)
    add("shield", "Temperature and humidity sensor in radiation shield", sh, 9, "bought", "sensors")
    zbf = zr(-PY) - half
    pir = bx(-25, 25, -PY - 20, -PY + 20, zbf - 2, zbf) + bx(-30, 30, -PY - 30, -PY + 30, zbf - 52, zbf - 2) + zcyl(0, -PY, zbf - 52 - 8, 15, 16)
    add("pir", "PIR presence sensor with bracket", pir, 9, "bought", "sensors")

    # ---- 10 pump, 11 filter, 14 drain valve on the equipment plate (rear left post, front face)
    lx, ly = -PX, PY
    x0p, x1p, z0p, z1p, tpl = p["eq_plate"]
    yf = ly - S / 2                                 # post front face
    add("eq_plate", "Equipment plate", bx(x0p, x1p, yf - tpl, yf, z0p, z1p), 10, "made", "pump")
    eq_bolts = []
    for zz in (z0p + 40, z1p - 30):
        s_, h_ = bolt("y", lx, zz, yf - tpl, yf + S, 10)
        eq_bolts.append(s_)
        hole_in(["eq_plate", "post_rl"], h_)
    add("eq_bolts", "Equipment plate bolts, M10 (2)", fuse(eq_bolts), 16, "fixing", None)
    qw, qd, qh = p["pump"]
    yp = yf - tpl
    pz = p["pump_z"]
    add("pump", "Misting pump, 12 V", bx(lx - 40, lx - 40 + qw, yp - qd, yp, pz - qh / 2, pz + qh / 2), 10, "bought", "pump")
    fr, fh = p["filter_r"], p["filter_h"]
    fxc, fyc = lx + 110, yp - fr
    add("filter", "Filter, 5 um, with check valve", zcyl(fxc, fyc, 980, fr, fh) + bx(fxc - 20, fxc + 20, yp - 6, yp, 1060, 1100), 11, "bought", "filter")
    dw, dd, dh = p["drain"]
    xl0 = -p["end_x"]
    add("drain", "Drain valve, normally open", bx(xl0 - dw / 2, xl0 + dw / 2, yp - dd, yp, 1000, 1000 + dh)
        + zcyl(xl0, yp - dd / 2, 1000 - 30, 6, 60), 14, "bought", "drain")

    # ---- 12 mist line loop, tees and nozzles, vacuum breaker, clips
    yl = D["y_line"]
    r = p["line_od"] / 2
    zl = D["zline"]
    zf, zrr = zl(-yl), zl(yl)
    corners = {(sx, sy): (sx * ex, sy * yl, zl(sy * yl)) for sx in (-1, 1) for sy in (-1, 1)}
    segs = [((-1, -1), (1, -1)), ((-1, 1), (1, 1)), ((-1, -1), (-1, 1)), ((1, -1), (1, 1))]
    line = fuse(rod(corners[a], corners[c], r) for a, c in segs)
    line = line + fuse(_b3d().Pos(*q) * _b3d().Sphere(r) for q in corners.values())
    tees = []
    for x in p["nozzle_x"]:
        for sy, z in ((-1, zf), (1, zrr)):
            tees.append(box(x, sy * yl, z, 20, 20, 20) + zcyl(x, sy * yl, z - 10 - (p["nozzle_len"] - 10) / 2, 6, p["nozzle_len"] - 10))
    vb_x = 150.0
    tees.append(box(vb_x, -yl, zf, 20, 20, 20))
    riser = rod((xl0, yl, zrr), (xl0, yl, 1000 + dh), r) + rod((xl0, yl, pz), (lx - 40, yl, pz), r)
    add("mistline", "Mist line loop, tees and 8 nozzles", fuse([line, riser] + tees), 12, "bought", "mistline")
    add("vbreaker", "Vacuum breaker", zcyl(vb_x, -yl, zf + 10 + 22.5, 12, 45), 14, "bought", "drain")
    clips = []
    for x in (-1200.0, -700.0, -200.0, 200.0, 700.0, 1200.0):
        for sy in (-1, 1):
            z = zl(sy * yl)
            yface = sy * (PY - half)
            clips.append(bx(x - 7.5, x + 7.5, yface - sy * 2, yface, z - r - 2, zr(sy * PY) - half + 20)
                         + bx(x - 7.5, x + 7.5, sy * yl - sy * 6, yface, z - r - 2, z - r))
    for sx in (-1, 1):
        for yy in (-800.0, 0.0, 800.0):
            z = zl(yy + 7.5)
            top = zr(yy + 7.5) - half / math.cos(th)
            clips.append(bx(sx * (ex + r), sx * (ex + r + 2), yy - 7.5, yy + 7.5, z - r - 2, top)
                         + bx(sx * (ex - 6), sx * (ex + r + 2), yy - 7.5, yy + 7.5, z - r - 2, z - r))
    add("clips", "Mist line hanger clips (18)", fuse(clips), 12, "bought", "mistline")

    # ---- 13 tank, strap, stop cleats
    tx, ty = p["tank_xy"]
    tr, tht = p["tank_d"] / 2, p["tank_h"]
    tank = zcyl(tx, ty, tht / 2, tr, tht) + zcyl(tx, ty, tht + 15, 100, 30)
    oa = math.atan2(1087 - ty, -1290 - tx)
    ox, oy = tx + tr * math.cos(oa), ty + tr * math.sin(oa)
    tank = tank + rod((ox - 5 * math.cos(oa), oy - 5 * math.sin(oa), 40), (ox + 10 * math.cos(oa), oy + 10 * math.sin(oa), 40), 10)
    add("tank", "Water tank, 120 L", tank, 13, "bought", "tank")
    strap = hull_band((tx, ty, tr), (lx - S / 2, lx + S / 2, ly - S / 2, ly + S / 2), 400.0, 40.0, 2.0)
    add("strap", "Tank strap", strap, 13, "bought", "tank")
    stops, stop_bolts = [], []
    for adeg in (235.0, 305.0):
        a = math.radians(adeg)
        loc = (bx(0, 5, -30, 30, 0, 50) + bx(0, 50, -30, 30, 0, 5))
        loc = loc - acyl("z", 32, 0, -1, 6, 5.5)
        pl = b.Pos(tx + tr * math.cos(a), ty + tr * math.sin(a), 0) * b.Rot(0, 0, adeg)
        stops.append(pl * loc)
        stop_bolts.append(pl * bolt("z", 32, 0, 5, 0, 10, nut=False, tip=-60)[0])
    add("stops", "Tank stop cleats (2)", fuse(stops), 13, "made", "tank")
    add("stop_bolts", "Tank stop anchors, M10 (2)", fuse(stop_bolts), 13, "fixing", None)

    # ---- 15 harness: cables inside the posts and beams, hoses at the rear left corner
    cr = p["cable_r"]
    zcf, zcr = zr(-PY) + 5, zr(PY) + 5
    xi = PX - 25
    yi = PY - 13
    zbr = zr(PY) - half
    sensor = [(shx, ya - aw - 8, ztop - 8), (shx, ya - aw - 8, az + aw / 2 + cr + 0.5), (shx - 20, ya - aw / 2 + 5, az + aw / 2 + cr + 0.5),
              (fx + 30, ya - aw / 2 + 5, az + aw / 2 + cr + 0.5), (fx + 30, ya - aw / 2 + 5, az + 45), (fx + 30, fy - S / 2 + 10, az + 45),
              (xi, -yi, az + 45), (xi, -yi, zcf), (xi, -PY, zcf), (ex, -PY, zcf), (ex, -(PY - 35), zcf),
              (ex, PY - 35, zcr + (zr(PY - 35) - zr(PY))), (ex, PY, zcr), (xi, PY, zcr), (xi, yi, zcr), (xi, yi, 1400),
              (x0e + 134, yi, 1400), (x0e + 134, yi, ez - eh / 2 - 15)]
    pirc = [(35, -PY, zbf - 20), (35, -PY, zcf - 8), (40, -PY - 10, zcf), (ex - 10, -PY - 10, zcf), (ex, -PY, zcf)]
    panel_c = [(420, PY, zr(PY) + n_pan / math.cos(th) - 0.6), (420, PY, zcr), (xi, PY, zcr)]
    pump_c = [(xi, PY, zcr), (-xi, PY, zcr), (-xi, yi, zcr), (-xi, yi, z1p - 40), (-xi, yp - 8, z1p - 40), (-xi, yp - 8, pz + qh / 2)]
    hose1 = [(ox + 10 * math.cos(oa), oy + 10 * math.sin(oa), 40), (ox + 25 * math.cos(oa), oy + 25 * math.sin(oa), 40),
             (ox + 25 * math.cos(oa), oy + 25 * math.sin(oa), 1080.0),
             (fxc + (fr + 7) * math.cos(math.atan2(oy + 25 * math.sin(oa) - fyc, ox + 25 * math.cos(oa) - fxc)),
              fyc + (fr + 7) * math.sin(math.atan2(oy + 25 * math.sin(oa) - fyc, ox + 25 * math.cos(oa) - fxc)), 1080.0)]
    hose2 = [(fxc, fyc, 980 + fh / 2), (fxc, fyc, pz - qh / 2)]
    float_c = [(tx - 50, ty + 50, tht + 30), (tx - 50, ty + 50, z1p - 40), (-xi, yp - 8, z1p - 40)]   # tank level switch cable
    harness = fuse([polyline_rod(sensor, cr), polyline_rod(pirc, cr), polyline_rod(panel_c, cr), polyline_rod(pump_c, cr), polyline_rod(float_c, cr),
                    polyline_rod(hose1, 6.5), polyline_rod(hose2, 6.5)])
    add("harness", "Cables and hoses", harness, 15, "bought", "harness")
    # grommet holes where the cables pass through walls
    gh = 6.0
    hole_in(["beam_r"], acyl("z", 420, PY, zr(PY) + half - bt - 1, zr(PY) + half + 1, gh))
    hole_in(["beam_r"], acyl("z", xi, yi, zbr - 1, zbr + bt + 1, gh))
    hole_in(["beam_r"], acyl("z", -xi, yi, zbr - 1, zbr + bt + 1, gh))
    hole_in(["beam_f"], acyl("z", xi, -yi, zr(-PY) - half - 1, zr(-PY) - half + bt + 1, gh))
    hole_in(["beam_f"], acyl("z", 35, -PY, zr(-PY) - half - 1, zr(-PY) - half + bt + 1, gh))
    hole_in(["beam_f"], acyl("y", ex, zcf, -(PY - half) - bt - 1, -(PY - half) + 1, gh))
    hole_in(["beam_r"], acyl("y", ex, zcr + (zr(PY - 35) - zr(PY)), (PY - half) - 1, (PY - half) + bt + 1, gh))
    hole_in(["post_fr"], acyl("y", fx + 30, az + 45, fy - S / 2 - 1, fy - S / 2 + T + 1, gh))
    hole_in(["post_rr"], acyl("x", yi, 1400, cx + S / 2 - T - 1, cx + S / 2 + 1, gh))
    hole_in(["post_rl"], acyl("y", -xi, z1p - 40, yf - 1, yf + T + 1, gh))
    hole_in(["eq_plate"], acyl("y", -xi, z1p - 40, yf - tpl - 1, yf + 1, gh))

    # cut every hole from the parts it passes through
    for k, hs in holes.items():
        if k not in C:
            continue
        shp = C[k].shape
        bb = shp.bounding_box()
        for h in hs:
            hb = h.bounding_box()
            if hb.min.X > bb.max.X or hb.max.X < bb.min.X or hb.min.Y > bb.max.Y or hb.max.Y < bb.min.Y or hb.min.Z > bb.max.Z or hb.max.Z < bb.min.Z:
                continue
            shp = shp - h
        C[k].shape = shp
    return C


def build_parts(p=PARAMS):
    """Return {concept media group: solid} (fixings are left out)."""
    C = build_components(p)
    out = {}
    for c in C.values():
        if c.group:
            out[c.group] = c.shape if c.group not in out else out[c.group] + c.shape
    return out


GROUPS = {
    "frame": lambda c: c.bom in (1, 2, 4) or c.name.startswith(("M12", "M16", "Head cleat bolts", "Knee brace bolts", "Frame cleat bolts")),
    "water-system": lambda c: c.bom in (10, 11, 12, 13, 14) or c.name.startswith(("Equipment plate bolts", "Tank stop")),
}


def assembly(p=PARAMS):
    b = _b3d()
    C = build_components(p)
    parts = {}
    for c in C.values():
        if c.group:
            parts[c.group] = c.shape if c.group not in parts else parts[c.group] + c.shape
    return b.Compound(children=[c.shape for c in C.values()]), parts


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def _bb_touch(a, b_, tol=1.0):
    A, B = a.bounding_box(), b_.bounding_box()
    return not (A.min.X > B.max.X + tol or A.max.X < B.min.X - tol or A.min.Y > B.max.Y + tol or A.max.Y < B.min.Y - tol
                or A.min.Z > B.max.Z + tol or A.max.Z < B.min.Z - tol)


# joints that must touch (contact, no overlap), with the fixing that holds them
CONTACTS = [
    ("post_{p}", "plate_{p}", "Post stands on its base plate"),
    ("bcleat_{p}", "plate_{p}", "Base cleats on the base plate"),
    ("bcleat_{p}", "post_{p}", "Base cleats against the post"),
    ("hcleat_{p}", "post_{p}", "Head cleats against the post"),
    ("beam_{b}", "post_{p}", "Long beam sits on the post top"),
    ("hcleat_{p}", "beam_{b}", "Head cleats under the long beam"),
    ("brace_{p}", "post_{p}", "Knee brace lower tab on the post"),
    ("brace_{p}", "beam_{b}", "Knee brace upper tab under the beam"),
    ("anchors", "bcleat_{p}", "Anchor nuts on the base cleats"),
    ("base_bolts", "bcleat_{p}", "Base bolts bear on the cleats"),
    ("head_bolts", "hcleat_{p}", "Head cleat bolts bear on the cleats"),
    ("brace_bolts", "brace_{p}", "Brace bolts bear on the tabs"),
]
CONTACTS_ONE = [
    ("endb_r", "beam_f"), ("endb_r", "beam_r"), ("endb_l", "beam_f"), ("endb_l", "beam_r"),
    ("purlin_r", "beam_f"), ("purlin_r", "beam_r"), ("purlin_l", "beam_f"), ("purlin_l", "beam_r"),
    ("bearer", "purlin_r"), ("bearer", "purlin_l"),
    ("frame_cleats", "beam_f"), ("frame_cleats", "beam_r"), ("frame_cleats", "endb_r"), ("frame_cleats", "endb_l"),
    ("frame_cleats", "purlin_r"), ("frame_cleats", "purlin_l"), ("frame_cleats", "bearer"), ("frame_bolts", "frame_cleats"),
    ("feet", "bearer"), ("feet", "beam_r"), ("rails", "feet"), ("panel", "rails"), ("clamps", "panel"), ("clamps", "rails"),
    ("foot_bolts", "feet"),
    ("enc_rails", "post_rr"), ("enclosure", "enc_rails"), ("battery", "enclosure"), ("mppt", "enclosure"), ("board", "enclosure"),
    ("arm", "post_fr"), ("shield", "arm"), ("arm_bolts", "arm"), ("pir", "beam_f"),
    ("eq_plate", "post_rl"), ("eq_bolts", "eq_plate"), ("pump", "eq_plate"), ("filter", "eq_plate"), ("drain", "eq_plate"),
    ("mistline", "drain"), ("mistline", "pump"), ("vbreaker", "mistline"), ("clips", "mistline"), ("clips", "beam_f"),
    ("clips", "beam_r"), ("clips", "endb_r"), ("clips", "endb_l"),
    ("strap", "post_rl"), ("stops", "tank"),
]
NEAR = [("strap", "tank", 0.2), ("fabric", "beam_f", 0.6), ("fabric", "beam_r", 0.6), ("fabric", "endb_r", 4.0), ("fabric", "endb_l", 4.0),
        ("fabric", "purlin_r", 4.0), ("fabric", "purlin_l", 4.0)]
CLEAR = [("panel", "fabric", 5.0), ("rails", "fabric", 3.0), ("feet", "fabric", 3.0), ("mistline", "beam_f", 20.0),
         ("mistline", "beam_r", 20.0), ("mistline", "endb_r", 20.0), ("mistline", "endb_l", 20.0),
         ("mistline", "post_rl", 15.0), ("mistline", "frame_cleats", 15.0), ("harness", "pump", 0.0)]
# parts allowed to touch or meet inside (bought assemblies, cables inside tubes)
SKIP = {frozenset(("mistline", "clips")), frozenset(("mistline", "vbreaker"))}


def checks(p=PARAMS):
    """Returns rows (description, overlap mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect, vmax=0.5):
        v = _vol(S(a), S(b_))
        gp = S(a).distance_to(S(b_))
        if expect == "touch":
            ok = v < vmax and gp < 0.05
        elif isinstance(expect, tuple):
            ok = v < vmax and gp <= expect[1] + 1e-6
        else:
            ok = v < vmax and gp >= expect - 1e-6
        rows.append((desc, v, gp, expect, ok))

    pk = {"fr": "f", "fl": "f", "rr": "r", "rl": "r"}
    for post_, bm in pk.items():
        for a, b_, d in CONTACTS:
            chk(f"{d} ({post_})", a.format(p=post_, b=bm), b_.format(p=post_, b=bm), "touch")
    for a, b_ in CONTACTS_ONE:
        chk(f"{C[a].name} meets {C[b_].name}", a, b_, "touch")
    for a, b_, m in NEAR:
        chk(f"{C[a].name} rests on {C[b_].name} (gap at most {m:g} mm)", a, b_, ("near", m))
    for a, b_, m in CLEAR:
        chk(f"{C[a].name} clear of {C[b_].name}", a, b_, m)
    # every pair of parts: no overlap
    keys = list(C)
    n_pairs, bad = 0, []
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            if frozenset((a, b_)) in SKIP or not _bb_touch(S(a), S(b_)):
                continue
            n_pairs += 1
            v = _vol(S(a), S(b_))
            if not v < 0.5:
                bad.append((a, b_, v))
    for a, b_, v in bad:
        rows.append((f"Overlap: {C[a].name} and {C[b_].name}", v, 0.0, "touch", False))
    rows.append((f"No overlap in any of {n_pairs} neighbouring pairs", sum(v for *_, v in bad), 0.0, "touch", not bad))
    # headroom inside the post grid: lowest point of anything overhead
    D = derived(p)
    lows = []
    for k in ("brace_fr", "brace_fl", "brace_rr", "brace_rl", "mistline", "clips", "pir", "vbreaker", "frame_cleats", "head_bolts", "brace_bolts"):
        sh = S(k) & bx(-p["post_x"] + p["post"] / 2, p["post_x"] - p["post"] / 2, -p["post_y"] - p["post"] / 2, p["post_y"] + p["post"] / 2, 1800, 4000)
        if sh is not None and sh.volume > 0:
            lows.append((sh.bounding_box().min.Z, C[k].name))
    zmin, what = min(lows)
    rows.append((f"Headroom: lowest overhead part ({what}) at {zmin:.0f} mm", 0.0, zmin - 2200.0, 0.0, zmin >= 2200.0))
    sl = S("shield").bounding_box().min.Z
    rows.append((f"Sensor shield lowest point {sl:.0f} mm (outside the canopy)", 0.0, sl - 2200.0, 0.0, sl >= 2200.0))
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else (f"<= {exp[1]:g} mm" if isinstance(exp, tuple) else f">= {exp:g} mm")
        print(f"  {'ok ' if ok else 'BAD'}  {desc[:78]:78s} overlap {v:9.3f} mm3  gap {gp:8.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    b = _b3d()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    exports = {"coolshade-assembly": [c.shape for c in C.values()]}
    for name, f in GROUPS.items():
        exports[name] = [c.shape for c in C.values() if f(c)]
    for name, shapes in exports.items():
        shape = b.Compound(children=shapes)
        b.export_step(shape, str(out / "step" / f"{name}.step"))
        b.export_stl(shape, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"slope {D['slope_deg']:.2f} deg; brace low point {D['brace_low_rear']:.0f} (rear) and {D['brace_low_front']:.0f} (front) mm; "
          f"nozzle tips {D['nozzle_tip_rear']:.0f} (rear) and {D['nozzle_tip_front']:.0f} (front) mm; "
          f"mist line {D['line_len_mm'] / 1000:.2f} m, {D['line_vol_l']:.2f} L")
    print_checks()
