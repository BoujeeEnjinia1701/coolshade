"""CoolShade product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the solar misting shade canopy: galvanized posts with
rounded corners, knee braces with bolted end sleeves, base plates with anchor nuts and washers, a
roof frame with black end caps, knitted shade cloth with a reinforced hem and eyelets, and a 100 W
panel with cells, busbars, glass, an aluminium frame, clamps and a junction box. The mist line
hangs from clips under the beams with eight slip-lok tees and brass nozzles, a vacuum breaker at
the front and a riser clipped to the rear left post. The water plant has a strapped, opaque 120 L
tank with rolling hoops, screw lid, label, outlet tap and anchor cleats; a vented pump box with a
window onto the pump; a clear-bowl filter with its cartridge; and the solenoid drain valve. The
IP65 enclosure has a door with a window onto the MPPT controller's lit display, a lock, hinges, a
rain hood, a lit status lamp and post clamps; the sensor head has a louvred radiation shield and a
PIR with a Fresnel dome. Context is a compact paved patch with a curb, an existing slatted bench
and the shared clay mannequin standing underneath.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS and derived() in model.py, and the
helpers box(), rod(), zcyl() and shs() are reused. Axes as model.py: X along the curb, Y across the
sidewalk (street side is -Y), Z up, sidewalk surface at Z = 0. Groups: "shell" holds the canopy,
power and sensing parts; "internal" holds the water plant at the rear left post (tank, pump box,
filter, drain valve and hoses) so the "detail" view can frame it; "context" the paving, bench and
person. Appearance-only differences from model.py are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Axis, Box, Compound, Cone, Cylinder, Pos, RegularPolygon, Rot,  # noqa: E402
                       Sphere, extrude, fillet)
from model import PARAMS, derived, box, rod, zcyl, shs  # noqa: E402

TITLE = "CoolShade: solar-powered shade canopy with fine misting"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation); canopy over a paved "
             "patch with the solar panel on the roof, the mist nozzles under the street-side beam, the "
             "strapped tank and pump at the rear left post and a person standing by the bench for scale"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): solar panel and rails, "
             "shade cloth and roof frame lifted off the posts; mist line loop with nozzles below the frame; "
             "tank, pump box, filter and drain valve pulled out at left; enclosure, door, battery and MPPT "
             "at right; base plates below"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 20, "az": -35,
     "note": "Detail from the front right and slightly above (about 20 deg elevation), water plant only: "
             "strapped 120 L tank, vented pump box with its window, clear-bowl filter, solenoid drain valve "
             "and hoses, as mounted on the rear left post"},
]

# ------------------------------------------------------------------------------------ appearance sizes
PATCH = (-1750.0, 1950.0, -1560.0, 1350.0, 120.0)    # paved patch x0, x1, y0, y1, depth (top at Z = 0)
SLAB = 500.0                                          # paving slab module
PERSON_AT = (950.0, -100.0)                           # mannequin pelvis over this point, in front of the bench
PERSON_ROT = 25.0                                     # turned toward the hero camera
BENCH = (150.0, 560.0)                                # bench centre (x, y), from concept_media.py

# Colours (restrained product palette; kit accent)
C_GALV = "#A9AFB6"
C_GALV_D = "#8E959D"
C_CAP = "#1F2328"
C_FABRIC = "#0F766E"
C_HEM = "#0B5D57"
C_ALU = "#C3C8CE"
C_CELL = "#1B2A4A"
C_BACKSHEET = "#E6E8EB"
C_BUS = "#D8DCE0"
C_GLASS = "#DCEBF5"
C_BLACK = "#1C1F24"
C_LINE = "#23262B"
C_BRASS = "#B8913A"
C_SHELL = "#E9EAEC"
C_SHELL2 = "#C9CDD3"
C_TANK = "#3B4A57"
C_STRAP = "#2B2F36"
C_LABEL = "#F4F4F2"
C_ACCENT = "#0F766E"
C_LED_G = "#22C55E"
C_LCD = "#5EEAD4"
C_BATT = "#2F3A4A"
C_PCB = "#166534"
C_RED = "#B91C1C"
C_CART = "#F1EFE8"
C_PAVE = "#D6D3CD"
C_JOINT = "#A8A49C"
C_CURB = "#BDB9B1"
C_TIMBER = "#B08D66"
C_BENCH = "#4B5563"
C_CLAY = "#9CA3AF"


# ------------------------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _rbox(cx, cy, cz, sx, sy, sz, r, axis=Axis.Z):
    """Box with the edges parallel to `axis` filleted (with fallbacks)."""
    b = box(cx, cy, cz, sx, sy, sz)
    return _fillet_try(b, b.edges().filter_by(axis), [r, r * 0.6, r * 0.3])


def _rbox_all(cx, cy, cz, sx, sy, sz, r):
    b = box(cx, cy, cz, sx, sy, sz)
    return _fillet_try(b, b.edges(), [r, r * 0.6, r * 0.3])


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _comp(shapes):
    return Compound(children=list(shapes))


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _hexnut(x, y, z0, af, h):
    """Hex nut (across flats af) standing on z0."""
    return Pos(x, y, z0) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _ring(x, y, z, ro, ri, h):
    return Pos(x, y, z) * (Cylinder(ro, h) - Cylinder(ri, h + 2))


def _pipe(points, r):
    """Round tube through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        seg = rod(a, c, r)
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _roof(D):
    """The model.py roof-plane transform: local X, Y in the roof plane, Z normal to it."""
    return Pos(0, 0, D["z_mid"]) * Rot(-D["slope_deg"], 0, 0)


# ------------------------------------------------------------------------------------ structure
def _posts(P, D):
    """Posts (rounded SHS), braces with end sleeves, plates, anchors, nuts and washers."""
    zr, PX, PY, S = D["zr"], P["post_x"], P["post_y"], P["post"]
    half = P["beam"] / 2
    cs = math.cos(math.radians(D["slope_deg"]))
    posts, braces, sleeves, bolts = [], [], [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            top = zr(sy * PY) - half / cs
            h = top - P["plate_t"]
            outer = _rbox(sx * PX, sy * PY, P["plate_t"] + h / 2, S, S, h, 6.0)
            inner = box(sx * PX, sy * PY, P["plate_t"] + h / 2, S - 2 * P["post_t"], S - 2 * P["post_t"], h + 2)
            posts.append(outer - inner)
            a = (sx * (PX - S / 2), sy * PY, top - P["brace_drop"])
            c = (sx * (PX - S / 2 - P["brace_reach"]), sy * PY, top)
            braces.append(rod(a, c, P["brace_od"] / 2))
            # bolted end sleeves at both ends of each brace
            va = (c[0] - a[0], 0, c[2] - a[2])
            ln = math.hypot(va[0], va[2])
            u = (va[0] / ln, 0, va[2] / ln)
            for t0, t1 in ((6, 56), (ln - 56, ln - 6)):
                p0 = (a[0] + u[0] * t0, a[1], a[2] + u[2] * t0)
                p1 = (a[0] + u[0] * t1, a[1], a[2] + u[2] * t1)
                sleeves.append(rod(p0, p1, P["brace_od"] / 2 + 3.0))
                pm = ((p0[0] + p1[0]) / 2, a[1], (p0[2] + p1[2]) / 2)
                bolts.append(rod((pm[0], pm[1] - 26, pm[2]), (pm[0], pm[1] + 26, pm[2]), 4.0))
                bolts.append(Pos(pm[0], pm[1] - 27, pm[2]) * Rot(90, 0, 0) *
                             extrude(RegularPolygon(6.5, 6), amount=5.0, both=True))
    pl, pt, ap = P["plate"], P["plate_t"], P["anchor_pitch"] / 2
    plates, anchors, nuts = [], [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            plates.append(_rbox(sx * PX, sy * PY, pt / 2, pl, pl, pt, 12.0))
            for dx in (-ap, ap):
                for dy in (-ap, ap):
                    x, y = sx * PX + dx, sy * PY + dy
                    anchors.append(zcyl(x, y, (pt + 40 - P["anchor_embed"]) / 2, P["anchor_d"] / 2,
                                        P["anchor_embed"] + pt + 40))
                    w = _ring(x, y, pt + 1.5, 15.0, 8.5, 3.0)
                    n = _hexnut(x, y, pt + 3.0, 24.0, 13.0) - zcyl(x, y, pt + 9, 8.2, 16)
                    nuts.append(w + n)
    return (_comp(posts), _comp(braces), _comp(sleeves), _comp(bolts),
            _comp(plates), _comp(anchors), _comp(nuts))


def _frame(P, D):
    """Roof frame in the roof plane: filleted beams and purlins, black end caps."""
    R = _roof(D)
    L, Dp, PX, PY, bm = P["roof_l"], P["roof_d"], P["post_x"], P["post_y"], P["beam"]
    pu = P["purlin"]
    members = [_rbox(0, sy * PY, 0, L - 8, bm, bm, 3.0, Axis.X) for sy in (-1, 1)]
    members += [_rbox(sx * PX, 0, 0, bm, Dp - 8, bm, 3.0, Axis.Y) for sx in (-1, 1)]
    members += [_rbox(sx * P["purlin_x"], 0, 0, pu, Dp - 100, pu, 2.5, Axis.Y) for sx in (-1, 1)]
    caps = []
    for sy in (-1, 1):
        for sx in (-1, 1):
            caps.append(_rbox(sx * (L / 2 - 2), sy * PY, 0, 4, bm + 2, bm + 2, 2.0, Axis.X))
            caps.append(_rbox(sx * PX, sy * (Dp / 2 - 2), 0, bm + 2, 4, bm + 2, 2.0, Axis.Y))
            caps.append(_rbox(sx * P["purlin_x"], sy * ((Dp - 100) / 2 + 2), 0, pu + 2, 4, pu + 2, 2.0, Axis.Y))
    return R * _fuse(members), R * _comp(caps)


def _fabric(P, D):
    """Shade cloth over the frame, a reinforced hem band and eyelets with cord ties."""
    R = _roof(D)
    L, Dp, half, ft = P["roof_l"], P["roof_d"], P["beam"] / 2, P["fabric_t"]
    cloth = box(0, 0, half + ft / 2, L - 20, Dp - 20, ft)
    cloth = _fillet_try(cloth, cloth.edges().filter_by(Axis.Z), [40.0, 20.0])
    hem = box(0, 0, half + ft / 2 + 0.5, L, Dp, ft + 1.0)
    hem = _fillet_try(hem, hem.edges().filter_by(Axis.Z), [40.0, 20.0])
    inner = box(0, 0, half + ft / 2, L - 120, Dp - 120, ft + 4)
    hem = hem - inner
    eyelets = []
    for x in [-L / 2 + 60 + k * (L - 120) / 8 for k in range(9)]:
        for sy in (-1, 1):
            eyelets.append(_ring(x, sy * (Dp / 2 - 30), half + ft + 1.5, 11.0, 6.0, 2.0))
    for y in [-Dp / 2 + 60 + k * (Dp - 120) / 6 for k in range(1, 6)]:
        for sx in (-1, 1):
            eyelets.append(_ring(sx * (L / 2 - 30), y, half + ft + 1.5, 11.0, 6.0, 2.0))
    return R * cloth, R * hem, R * _comp(eyelets)


def _panel(P, D):
    """100 W panel on two rails: frame, backsheet, cells, busbars, glass, clamps, junction box."""
    R = _roof(D)
    pw, pd, ph = P["panel"]
    half, py = P["beam"] / 2, P["panel_y"]
    zc = half + 70
    zt, zb = zc + ph / 2, zc - ph / 2
    rim = 28.0
    frame = box(0, py, zc, pw, pd, ph) - box(0, py, zc, pw - 2 * rim, pd - 2 * rim, ph + 2)
    frame += box(0, py, zb + 4, pw - 20, pd - 20, 8) - box(0, py, zb + 4, pw - 2 * rim - 4, pd - 2 * rim - 4, 10)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.Z), [3.0, 1.5])
    iw, idp = pw - 2 * rim, pd - 2 * rim
    back = box(0, py, zt - 9, iw + 4, idp + 4, 3)
    nx, ny, gap = 9, 4, 4.0
    cw, cd = (iw - 16 - (nx - 1) * gap) / nx, (idp - 16 - (ny - 1) * gap) / ny
    cells, bus = [], []
    for i in range(nx):
        for j in range(ny):
            x = -iw / 2 + 8 + cw / 2 + i * (cw + gap)
            y = py - idp / 2 + 8 + cd / 2 + j * (cd + gap)
            cells.append(box(x, y, zt - 7, cw, cd, 1.0))
    for j in range(ny):
        y0 = py - idp / 2 + 8 + cd / 2 + j * (cd + gap)
        for dy in (-cd / 4, cd / 4):
            bus.append(box(0, y0 + dy, zt - 6.3, iw - 16, 1.6, 0.4))
    glass = box(0, py, zt - 3.5, iw + 4, idp + 4, 3.2)
    rails, clamps = [], []
    for sx in (-1, 1):
        x = sx * P["purlin_x"]
        r_ = _rbox(x, py, half + 30, 40, pd + 30, 40, 2.0, Axis.Y)
        r_ -= box(x, py, half + 30 + 17, 12, pd + 40, 8)          # top T-slot
        rails.append(r_)
        for sy in (-1, 1):
            y = py + sy * (pd / 2 + 6)
            c = box(x, y, zt + 3, 44, 18, 8) + box(x, py + sy * (pd / 2 + 12), zc + 5, 44, 6, ph + 10)
            c = _fillet_try(c, c.edges().filter_by(Axis.X), [1.5, 0.8])
            clamps.append(c + zcyl(x, y, zt + 9, 6.0, 4.0))
            clamps.append(box(x, py + sy * (pd / 2 + 15), half + 30, 42, 3, 42))   # rail end cap
    jbox = _rbox(0, py + pd / 4, zb + 4 - 14, 110, 80, 20, 3.0)
    jbox += _ycyl(-30, py + pd / 4 - 55, zb - 10, 5.0, 40) + _ycyl(30, py + pd / 4 - 55, zb - 10, 5.0, 40)
    return (R * frame, R * back, R * _comp(cells), R * _comp(bus), R * glass,
            R * _fuse(rails), R * _comp(clamps), R * jbox)


def _mistline(P, D):
    """Closed loop under the beams with hanger clips, slip-lok tees, brass nozzles and the vacuum breaker;
    the riser down the rear left post with its clips."""
    R = _roof(D)
    PX, PY = P["post_x"], P["post_y"]
    half = P["beam"] / 2
    yl = D["y_line"]
    lz = -half - P["line_drop"] + 25
    x0, x1 = -PX + 60, PX - 60
    r = P["line_od"] / 2
    loop = _pipe([(x0, -yl, lz), (x1, -yl, lz), (x1, yl, lz), (x0, yl, lz), (x0, -yl, lz)], r)
    loop = loop + Pos(x0, -yl, lz) * Sphere(r)
    tees, brass = [], []
    for x in P["nozzle_x"]:
        for y in (-yl, yl):
            t = _xcyl(x, y, lz, 9.0, 30.0)
            t = _fillet_try(t, t.edges(), [2.0, 1.0])
            t += zcyl(x, y, lz - 13, 6.5, 10.0)
            tees.append(t)
            b = Pos(x, y, lz - 26) * extrude(RegularPolygon(7.5, 6), amount=8.0)
            b += Pos(x, y, lz - 29.5) * Cone(2.6, 5.5, 7.0)
            brass.append(b)
    clips = []
    # hanger clips: flat strap under the beam, drop to the line (long runs and end runs)
    for x in (-1200.0, -700.0, -180.0, 180.0, 700.0, 1200.0):   # clear of the tees and vacuum breaker
        for sy in (-1, 1):
            yb = sy * PY
            clips.append(box(x, (yb + sy * yl) / 2 + sy * 5, -half - 1.5, 20, abs(yb - sy * yl) + 30, 3))
            clips.append(box(x, sy * yl, (lz - half) / 2 + 2, 20, 3, -half - lz + 4 - r))
            clips.append(_ring(0, 0, 0, r + 2.5, r - 0.2, 20).rotate(Axis.Y, 90).translate((x, sy * yl, lz)))
    for y in (-600.0, 0.0, 600.0):
        for sx in (-1, 1):
            xb = sx * PX
            clips.append(box((xb + sx * (PX - 60)) / 2 + sx * 5, y, -half - 1.5, abs(60) + 30, 20, 3))
            clips.append(box(sx * (PX - 60), y, (lz - half) / 2 + 2, 3, 20, -half - lz + 4 - r))
            clips.append(_ring(0, 0, 0, r + 2.5, r - 0.2, 20).rotate(Axis.X, 90).translate((sx * (PX - 60), y, lz)))
    # vacuum breaker at the front, highest point of the loop (model.py envelope: r 12, 45 high)
    vz = -half - P["line_drop"] + 40
    vb = zcyl(0, -yl, vz - 12, 10.0, 21.0)
    vb = _fillet_try(vb, vb.edges(), [1.5, 0.8])
    vb_hex = Pos(0, -yl, vz - 22.5) * extrude(RegularPolygon(12.0, 6), amount=8.0)
    vb_cap = zcyl(0, -yl, vz + 12, 12.0, 21.0)
    vb_cap = _fillet_try(vb_cap, vb_cap.edges().group_by(Axis.Z)[-1], [5.0, 3.0, 1.5])
    # riser up the rear left post
    qh = P["pump"][2]
    riser_top = D["zr"](yl) + lz / math.cos(math.radians(D["slope_deg"]))
    z0 = P["pump_z"] + qh / 2
    riser = rod((x0, yl, z0), (x0, yl, riser_top), r)
    rclips = []
    for z in (1300.0, 1700.0, 2100.0):
        rc = box(x0 - 12, yl + 18, z, 30, 50, 22) - box(x0, yl, z, 2 * r + 1, 2 * r + 1, 30)
        rclips.append(rc)
    return (R * loop, R * _comp(tees), R * _comp(brass), R * _comp(clips),
            R * (vb + vb_hex), R * vb_cap, riser, _comp(rclips))


# ------------------------------------------------------------------------------------ power and sensing
def _enclosure(P, D):
    """IP65 enclosure on the rear right post: body, door with window, lock, hinges, hood, lamp, clamps,
    and its contents (battery, MPPT with lit display, controller board, back plate)."""
    ew, ed, eh = P["enc"]
    ex, ez, PY, PX, S = D["enc_x"], P["enc_z"], P["post_y"], P["post_x"], P["post"]
    x0, x1 = ex - ew / 2, ex + ew / 2
    dt = 18.0                                             # door thickness at the +X face
    body = _rbox(ex - dt / 2, PY, ez, ew - dt, ed, eh, 8.0, Axis.X)
    body -= box(ex - dt / 2 + 2.5, PY, ez, ew - dt, ed - 5, eh - 5)
    door = _rbox(x1 - dt / 2, PY, ez, dt - 1.0, ed - 3, eh - 3, 8.0, Axis.X)
    door = _fillet_try(door, door.faces().sort_by(Axis.X)[-1].edges(), [2.5, 1.2])
    wy, wz = PY + 90, ez + 90                             # window over the MPPT
    door -= box(x1, wy, wz, 60, 110, 150)
    window = box(x1 - 4, wy, wz, 4, 118, 158)
    door -= box(x1 - 4, wy, wz, 4.5, 118, 158)
    bezel = box(x1 + 0.5, wy, wz, 3, 124, 164) - box(x1 + 0.5, wy, wz, 5, 108, 148)
    lock = _xcyl(x1 + 3, PY - 125, ez - 10, 11.0, 8.0) + box(x1 + 8, PY - 125, ez - 10, 3, 4, 14)
    hinges = _comp([Pos(x1 - 2, PY + ed / 2 + 4, z) * Cylinder(5.5, 50) for z in (ez - 150, ez + 150)])
    hood = box(ex + 12, PY, ez + eh / 2 + 3, ew + 24, ed + 24, 6)
    hood = _fillet_try(hood, hood.edges().filter_by(Axis.Z), [6.0, 3.0])
    lamp = _xcyl(x1 + 1, PY - 125, ez + 150, 9.0, 3.0) + Pos(x1 + 2.5, PY - 125, ez + 150) * Sphere(6.0)
    lamp_led = Pos(x1 + 3.5, PY - 125, ez + 150) * Sphere(5.5) & box(x1 + 6, PY - 125, ez + 150, 10, 14, 14)
    lamp_ring = _xcyl(x1 + 1.5, PY - 125, ez + 150, 9.0, 3.0) - _xcyl(x1 + 1.5, PY - 125, ez + 150, 6.0, 5.0)
    label = box(x1 + 0.4, PY - 60, ez - 120, 1.0, 110, 50)
    stripe = box(x1 + 0.4, PY, ez - eh / 2 + 22, 1.0, ed - 40, 8)
    glands = _comp([_rbox(x, PY + dy, D["enc_bot"] - 9, 18, 18, 18, 2.0) + zcyl(x, PY + dy, D["enc_bot"] - 22, 6.0, 10)
                    for x, dy in ((ex - 30, -60), (ex - 30, 60))] +
                   [zcyl(PX + 60, PY, D["enc_top"] + 12, 10.0, 18.0)])
    clamps = []
    for z in (ez - 140, ez + 140):
        c = box(PX, PY, z, S + 16, S + 16, 40) - box(PX, PY, z, S + 1, S + 1, 44)
        c = _fillet_try(c, c.edges().filter_by(Axis.Z), [3.0, 1.5])
        clamps.append(c)
    # contents
    bw, bd, bh = P["battery"]
    bx, by, bz = ex, PY - 60, ez - 90
    batt = _rbox(bx, by, bz, bw, bd, bh - 12, 6.0)
    batt_top = _rbox(bx, by, bz + bh / 2 - 6, bw, bd, 12, 4.0)
    terms = zcyl(bx, by - 55, bz + bh / 2 + 5, 9.0, 10.0)
    terms_n = zcyl(bx, by + 55, bz + bh / 2 + 5, 9.0, 10.0)
    batt_label = box(bx + bw / 2 + 0.4, by, bz - 10, 1.0, bd - 40, 70)
    mw, md, mh = P["mppt"]
    mx, my, mz = ex, PY + 90, ez + 90
    mppt = _rbox(mx, my, mz, mw, md, mh, 3.0, Axis.X)
    fins = _comp([box(mx - mw / 2 - 1, my - md / 2 + 8 + k * 12.5, mz, 4, 3, mh - 20) for k in range(7)])
    lcd = box(mx + mw / 2 + 0.3, my, mz + 25, 1.2, 60, 32)
    leds = _comp([_xcyl(mx + mw / 2 + 0.6, my + dy, mz - 20, 3.0, 1.6) for dy in (-18, 0, 18)])
    keys = _comp([_xcyl(mx + mw / 2 + 1, my + dy, mz - 45, 5.0, 3.0) for dy in (-20, 0, 20)])
    plate = box(x0 + 4.5, PY, ez, 2, ed - 20, eh - 20)
    pcb = box(x0 + 7, PY + 90, ez - 110, 1.6, 90, 70)
    chips = _comp([box(x0 + 9, PY + 90 + dy, ez - 110 + dz, 3, 12, 10) for dy, dz in ((-25, 15), (5, 15), (25, -15))])
    return dict(body=body, door=door, window=window, bezel=bezel, lock=lock, hinges=hinges, hood=hood,
                lamp=lamp_ring, lamp_led=lamp_led, label=label, stripe=stripe, glands=glands,
                clamps=_comp(clamps), batt=batt, batt_top=batt_top, term_pos=terms, term_neg=terms_n,
                batt_label=batt_label, mppt=mppt, fins=fins, lcd=lcd, leds=leds, keys=keys, plate=plate,
                pcb=pcb, chips=chips)


def _sensors(P, D):
    """Radiation shield with louvred plates, spacer rods and cap on its arm; PIR with a Fresnel dome."""
    PX, PY, S = P["post_x"], P["post_y"], P["post"]
    sz, rr = P["shield_z"], P["shield_r"]
    cx = PX + S / 2 + P["arm_l"] - 10
    plates = []
    for k in range(6):
        ro = rr - 2 * k
        z = sz + k * 22 - 5
        if k < 5:
            pl = Pos(cx, -PY, z + 5) * (Cone(ro, ro - 14, 10) - Cone(ro - 4, ro - 16, 10.02)) - zcyl(cx, -PY, z + 5, 24, 12)
        else:
            pl = Pos(cx, -PY, z + 6) * Cone(ro, ro - 16, 12)
            pl = _fillet_try(pl, pl.edges().group_by(Axis.Z)[-1], [4.0, 2.0])
        plates.append(pl)
    spacers = _comp([zcyl(cx + 42 * math.cos(a), -PY + 42 * math.sin(a), sz + 55, 3.0, 125)
                     for a in (math.radians(d) for d in (30, 150, 270))])
    arm = rod((PX + S / 2, -PY, sz + 50), (cx - 2, -PY, sz + 50), 12)
    arm_clamp = _rbox(PX + S / 2 + 10, -PY, sz + 50, 20, 110, 90, 3.0, Axis.X)
    arm_end = _rbox(cx - 20, -PY, sz + 50, 24, 36, 36, 3.0, Axis.X)
    probe = zcyl(cx, -PY, sz + 50, 6.0, 60)
    pir = _rbox(0, -PY + 40, D["beam_under_front"] - 20, 60, 60, 40, 8.0)
    pir = _fillet_try(pir, pir.faces().sort_by(Axis.Z)[0].edges(), [3.0, 1.5])
    dome = Pos(0, -PY + 40, D["beam_under_front"] - 40) * Sphere(20.0) & box(0, -PY + 40, D["beam_under_front"] - 55, 50, 50, 30)
    pir_led = Pos(18, -PY + 40 - 30, D["beam_under_front"] - 15) * Sphere(2.5)
    return dict(plates=_comp(plates), spacers=spacers, arm=arm + arm_end, clamp=arm_clamp, probe=probe,
                pir=pir, dome=dome, pir_led=pir_led)


def _harness(P, D):
    """Cable runs from model.py (enclosure to roof, sensor arm up the front right post and across)."""
    PX, PY, zr, sz = P["post_x"], P["post_y"], D["zr"], P["shield_z"]
    runs = (rod((PX + 60, PY, zr(PY) - 80), (PX + 60, PY, D["enc_top"] + 20), 6)
            + rod((PX + 60, -PY + 60, sz + 50), (PX + 60, -PY + 60, zr(-PY) - 80), 6)
            + rod((PX + 60, -PY + 60, zr(-PY) - 80), (PX + 60, PY - 60, zr(PY) - 80), 6)
            + Pos(PX + 60, -PY + 60, zr(-PY) - 80) * Sphere(6))
    ties = []
    for z in (1950.0, 2150.0, 2400.0):
        ties.append(box(PX + 50, PY, z, 22, 16, 12))
    for z in (2450.0, 2650.0):
        ties.append(box(PX + 50, -PY + 50, z, 22, 16, 12))
    return runs, _comp(ties)


# ------------------------------------------------------------------------------------ water plant
def _water(P, D):
    PX, PY, S = P["post_x"], P["post_y"], P["post"]
    tx, ty = D["tank_xy"]
    tr, th = P["tank_d"] / 2, P["tank_h"]
    tank = Pos(tx, ty, th / 2) * Cylinder(tr, th)
    tank = _fillet_try(tank, tank.edges(), [30.0, 18.0, 10.0])
    for zh in (170.0, 560.0):
        hoop = Pos(tx, ty, zh) * Cylinder(tr + 7, 22)
        hoop = _fillet_try(hoop, hoop.edges(), [6.0, 3.0])
        tank += hoop
    neck = Pos(tx, ty, th + 8) * Cylinder(190, 16)
    lid = Pos(tx, ty, th + 28) * Cylinder(205, 24)
    lid = _fillet_try(lid, lid.edges().group_by(Axis.Z)[-1], [5.0, 3.0])
    ribs = []
    for k in range(36):
        a = 2 * math.pi * k / 36
        ribs.append(Pos(tx + 205 * math.cos(a), ty + 205 * math.sin(a), th + 26) *
                    Rot(0, 0, math.degrees(a)) * Box(6, 8, 18))
    lid = lid + _comp(ribs)
    hasp = Pos(tx + 150, ty - 150, th + 44) * Rot(0, 0, 45) * (Box(40, 10, 10) - Box(24, 12, 5))
    tank = tank + neck
    # strap as model.py: band at 0.6 h and a tether to the rear left post; ratchet buckle
    zs = th * 0.6
    strap = (Pos(tx, ty, zs) * Cylinder(tr + 6, 40) - Pos(tx, ty, zs) * Cylinder(tr + 0.5, 42))
    tether = rod((tx - tr * 0.7, ty + tr * 0.7, zs), (-PX + S / 2, PY - 10, zs), 6)
    a = math.radians(-95)
    buckle = Pos(tx + (tr + 14) * math.cos(a), ty + (tr + 14) * math.sin(a), zs) * Rot(0, 0, -95 + 90) * \
        (Box(70, 12, 46) + Pos(0, 7, 0) * Rot(0, 90, 0) * Cylinder(8, 60))
    post_eye = box(-PX + S / 2 + 6, PY - 10, zs, 12, 40, 50)
    # label band, facing the hero camera
    lab = (Pos(tx, ty, 320) * Cylinder(tr + 1.2, 140) - Pos(tx, ty, 320) * Cylinder(tr - 2, 142))
    lab &= Pos(tx, ty, 320) * Rot(0, 0, -40) * Pos(tr, 0, 0) * Box(200, 330, 150)
    lab_band = (Pos(tx, ty, 265) * Cylinder(tr + 1.6, 24) - Pos(tx, ty, 265) * Cylinder(tr - 2, 26))
    lab_band &= Pos(tx, ty, 265) * Rot(0, 0, -40) * Pos(tr, 0, 0) * Box(200, 330, 30)
    # bottom outlet tap toward the post and two anchor cleats
    ta = math.radians(215)
    tap = rod((tx + (tr - 20) * math.cos(ta), ty + (tr - 20) * math.sin(ta), 70),
              (tx + (tr + 45) * math.cos(ta), ty + (tr + 45) * math.sin(ta), 70), 14)
    tap += Pos(tx + (tr + 45) * math.cos(ta), ty + (tr + 45) * math.sin(ta), 95) * Cylinder(7, 40)
    tap += Pos(tx + (tr + 45) * math.cos(ta), ty + (tr + 45) * math.sin(ta), 118) * Rot(0, 0, 215) * Box(60, 10, 8)
    cleats = []
    for d in (150.0, 300.0):
        c = math.radians(d)
        px, py = tx + (tr + 18) * math.cos(c), ty + (tr + 18) * math.sin(c)
        cl = Pos(px, py, 0) * Rot(0, 0, d) * (Pos(0, 0, 3) * Box(50, 60, 6) + Pos(-22, 0, 35) * Box(6, 60, 70))
        cl += _hexnut(px + 6 * math.cos(c), py + 6 * math.sin(c), 6, 17, 8)
        cleats.append(cl)
    fitting = Pos(tx + 150, ty + 120, th + 4) * Cylinder(20, 24)

    # pump shelf on the rear left post, vented pump box with a window, pump inside
    qw, qd, qh = P["pump"]
    qx, qy, qz = -PX + 150, PY - 100, P["pump_z"]
    shelf = box((-PX + S / 2 + qx + qw / 2) / 2, qy, qz - qh / 2 - 3, (qx + qw / 2) - (-PX + S / 2) + 10, qd + 10, 6)
    shelf += box(-PX + S / 2 + 3, PY, qz - qh / 2 - 60, 6, S, 120)
    shelf += _comp([Pos(-PX + S / 2 + 7, PY + dy, qz - qh / 2 - 60) * Rot(0, 90, 0) *
                    extrude(RegularPolygon(7, 6), amount=4) for dy in (-22, 22)])
    pbox = _rbox(qx, qy, qz, qw, qd, qh, 8.0)
    pbox = _fillet_try(pbox, pbox.faces().sort_by(Axis.Z)[-1].edges(), [4.0, 2.0])
    pbox -= box(qx, qy, qz - 2, qw - 6, qd - 6, qh - 2)
    pbox -= box(qx - 20, qy - qd / 2, qz, 120, 12, 84)            # window opening
    win = box(qx - 20, qy - qd / 2 + 1.5, qz, 128, 2.5, 92)
    pbox -= box(qx - 20, qy - qd / 2 + 1.5, qz, 128.5, 3, 92.5)
    for k in range(6):                                            # louvres on the +X end
        pbox -= box(qx + qw / 2, qy, qz - 45 + k * 17, 8, qd - 40, 6)
    pbox_label = box(qx + 72, qy - qd / 2 - 0.4, qz + 30, 40, 1.0, 26)
    motor = _xcyl(qx + 15, qy, qz - 12, 36.0, 100)
    motor = _fillet_try(motor, motor.edges(), [5.0, 2.5])
    head = _rbox(qx - 60, qy, qz - 12, 50, 90, 90, 10.0, Axis.X)
    sw = zcyl(qx - 60, qy + 10, qz + 45, 12.0, 24)
    feet = box(qx + 10, qy, qz - qh / 2 + 7, 150, 70, 8)
    # filter: clear bowl, white cartridge, dark head with ports; bracket to the pump box
    fx, fy, fz, fr, fh = -PX + 110, PY - 230, P["pump_z"] - 20, P["filter_r"], P["filter_h"]
    fhead = _rbox(fx, fy, fz + fh / 2 - 22, 2 * fr + 4, 2 * fr + 4, 44, 8.0)
    bowl = Pos(fx, fy, fz - 22) * Cylinder(fr, fh - 44)
    bowl = _fillet_try(bowl, bowl.edges().group_by(Axis.Z)[0], [15.0, 8.0])
    bowl -= Pos(fx, fy, fz - 20) * Cylinder(fr - 3, fh - 44)
    cart = Pos(fx, fy, fz - 22) * Cylinder(fr - 14, fh - 60)
    cart_core = Pos(fx, fy, fz - 22) * Cylinder(9, fh - 58)
    fring = Pos(fx, fy, fz + fh / 2 - 50) * Cylinder(fr + 3, 12)
    fbr = box(fx, fy + fr + 12, fz + fh / 2 - 22, 40, 26, 30)
    fports = _xcyl(fx - fr - 10, fy, fz + fh / 2 - 22, 9.0, 20) + _ycyl(fx, fy + fr + 8, qz + 40, 7.0, 20)
    # drain valve (normally open solenoid) within the model.py envelope; tee from the riser
    dw, dd, dh = P["drain"]
    dx, dy = -PX + 60, PY - 60 - 130
    dz = qz + qh / 2 + 60
    vbody = _rbox(dx, dy, dz - dh / 2 + 16, dw, 40, 28, 4.0, Axis.Y)
    coil = _rbox(dx, dy, dz + dh / 2 - 17.5, 50, 50, 35, 5.0)
    coil_cap = zcyl(dx, dy, dz + dh / 2 + 3, 8.0, 6)
    spout = _pipe([(dx - 35, dy, dz - dh / 2 + 16), (dx - 35, dy, dz - dh / 2 - 40)], 7)
    tee = _pipe([(dx, 976, dz - dh / 2 + 16), (dx, dy + 20, dz - dh / 2 + 16)], 6)
    riser_fit = Pos(dx, PY - 70, qz + qh / 2 + 10) * Cylinder(10, 22)
    # hoses: model.py suction hose (tank top to pump), filter to pump
    suction = rod((tx + 150, ty + 120, th - 50), (qx, qy, qz - qh / 2), 8)
    fhose = _pipe([(fx - fr - 18, fy, fz + fh / 2 - 22), (fx - fr - 18, fy, fz + fh / 2 + 18),
                   (qx - qw / 2 + 25, fy, fz + fh / 2 + 18), (qx - qw / 2 + 25, qy - 20, fz + fh / 2 + 18)], 7)
    return dict(tank=tank, lid=lid, hasp=hasp, strap=strap + tether, buckle=buckle, post_eye=post_eye,
                label=lab, label_band=lab_band, tap=tap, cleats=_comp(cleats), fitting=fitting,
                shelf=shelf, pbox=pbox, win=win, pbox_label=pbox_label, motor=motor, head=head, sw=sw,
                feet=feet, fhead=fhead + fbr, bowl=bowl, cart=cart, cart_core=cart_core, fring=fring,
                fports=fports, vbody=vbody, coil=coil + coil_cap, spout=spout, tee=tee,
                riser_fit=riser_fit, suction=suction, fhose=fhose)


# ------------------------------------------------------------------------------------ context
def _context():
    x0, x1, y0, y1, dep = PATCH
    base = box((x0 + x1) / 2, (y0 + y1) / 2, -dep / 2 - 6, x1 - x0, y1 - y0, dep - 12)
    slabs = []
    g = 6.0
    xs = [x0 + k * SLAB for k in range(int((x1 - x0) // SLAB) + 1)]
    ys = [y0 + k * SLAB for k in range(int((y1 - y0) // SLAB) + 1)]
    for xa in xs:
        for ya in ys:
            xb, yb = min(xa + SLAB, x1), min(ya + SLAB, y1)
            if xb - xa < 50 or yb - ya < 50:
                continue
            slabs.append(box((xa + xb) / 2, (ya + yb) / 2, -6, xb - xa - g, yb - ya - g, 12))
    curb = _rbox((x0 + x1) / 2, y0 - 90, -60, x1 - x0, 180, 150, 12.0, Axis.X)
    cx, cy = BENCH
    slats = [_rbox_all(cx, cy - 170 + k * 85, 440, 1500, 70, 36, 5.0) for k in range(5)]
    back = [_rbox_all(cx, cy + 205, 560 + k * 110, 1500, 30, 80, 5.0) for k in range(3)]
    frame = []
    for dxl in (-620.0, 620.0):
        fr_ = box(cx + dxl, cy, 210, 50, 60, 420) + box(cx + dxl, cy, 405, 50, 440, 30)
        fr_ += box(cx + dxl, cy + 200, 620, 50, 30, 460) + box(cx + dxl, cy - 150, 210, 50, 60, 420)
        fr_ = fr_.clean()
        frame.append(fr_)
    return base, _comp(slabs), curb, _comp(slats + back), _comp(frame)


# ------------------------------------------------------------------------------------ assembly
def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- 1 posts and braces, 4 plates and anchors
    posts, braces, sleeves, bolts, plates, anchors, nuts = _posts(P, D)
    add("Posts, 80 x 80 mm galvanized SHS", posts, C_GALV, "metal", 1, "shell", (0, 0, 0))
    add("Knee braces, 32 mm tube", braces, C_GALV, "metal", 1, "shell", (0, 0, 0))
    add("Brace end sleeves", sleeves, C_GALV_D, "metal", 1, "shell", (0, 0, 0))
    add("Brace bolts", bolts, C_GALV_D, "metal", 16, "shell", (0, 0, 0))
    add("Base plates", plates, C_GALV_D, "metal", 4, "shell", (0, 0, -350))
    add("M16 anchors", anchors, C_GALV_D, "metal", 4, "shell", (0, 0, -350))
    add("Anchor nuts and washers", nuts, C_ALU, "metal", 4, "shell", (0, 0, -350))

    # ---- 2 roof frame, 3 fabric
    frame, caps = _frame(P, D)
    add("Roof frame, 50 x 50 mm SHS", frame, C_GALV, "metal", 2, "shell", (0, 0, 700))
    add("Frame end caps", caps, C_CAP, "plastic", 2, "shell", (0, 0, 700))
    cloth, hem, eyelets = _fabric(P, D)
    add("Shade cloth, knitted HDPE", cloth, C_FABRIC, "fabric", 3, "shell", (0, 0, 1400))
    add("Shade cloth reinforced hem", hem, C_HEM, "fabric", 3, "shell", (0, 0, 1400))
    add("Shade cloth eyelets", eyelets, C_ALU, "metal", 3, "shell", (0, 0, 1400))

    # ---- 5 solar panel
    pf, back, cells, bus, glass, rails, clamps, jbox = _panel(P, D)
    ep = (0, 700, 2100)
    add("Solar panel frame, aluminium", pf, C_ALU, "metal", 5, "shell", ep)
    add("Solar panel backsheet", back, C_BACKSHEET, "plastic", 5, "shell", ep)
    add("Solar cells, monocrystalline", cells, C_CELL, "painted", 5, "shell", ep)
    add("Cell busbars", bus, C_BUS, "metal", 5, "shell", ep)
    add("Solar panel glass", glass, C_GLASS, "clear", 5, "shell", ep)
    add("Solar panel junction box", jbox, C_BLACK, "plastic", 5, "shell", ep)
    add("Panel rails", rails, C_ALU, "metal", 5, "shell", (0, 700, 1750))
    add("Panel clamps and rail caps", clamps, C_BLACK, "plastic", 5, "shell", ep)

    # ---- 12 mist line and nozzles, 14 vacuum breaker
    loop, tees, brass, clips, vb, vb_cap, riser, rclips = _mistline(P, D)
    em = (0, -250, 350)
    add("Mist line loop, 9.5 mm", loop, C_LINE, "plastic", 12, "shell", em)
    add("Slip-lok nozzle tees", tees, C_BLACK, "plastic", 12, "shell", em)
    add("Brass anti-drip nozzles", brass, C_BRASS, "metal", 12, "shell", em)
    add("Mist line hanger clips", clips, C_GALV_D, "metal", 12, "shell", em)
    add("Vacuum breaker body", vb, C_BRASS, "metal", 14, "shell", em)
    add("Vacuum breaker cap", vb_cap, C_BLACK, "plastic", 14, "shell", em)
    add("Mist line riser", riser, C_LINE, "plastic", 12, "shell", em)
    add("Riser clips", rclips, C_BLACK, "plastic", 12, "shell", em)

    # ---- 8 enclosure with 6 battery and 7 MPPT
    E = _enclosure(P, D)
    ee, ed_, ei = (650, 0, 0), (1050, 0, 0), (650, -480, 0)
    add("Enclosure body, IP65", E["body"], C_SHELL, "painted", 8, "shell", ee)
    add("Enclosure door", E["door"], C_SHELL, "painted", 8, "shell", ed_)
    add("Enclosure door window", E["window"], C_GLASS, "clear", 8, "shell", ed_)
    add("Door window bezel", E["bezel"], C_SHELL2, "plastic", 8, "shell", ed_)
    add("Door lock", E["lock"], C_ALU, "metal", 8, "shell", ed_)
    add("Door hinges", E["hinges"], C_SHELL2, "metal", 8, "shell", ee)
    add("Enclosure rain hood", E["hood"], C_SHELL2, "painted", 8, "shell", (650, 0, 300))
    add("Status lamp bezel", E["lamp"], C_BLACK, "plastic", 8, "shell", ed_)
    add("Status lamp (lit green)", E["lamp_led"], C_LED_G, "emissive", 8, "shell", ed_)
    add("Enclosure rating label", E["label"], C_LABEL, "paper", 8, "shell", ed_)
    add("Enclosure accent stripe", E["stripe"], C_ACCENT, "plastic", 8, "shell", ed_)
    add("Cable glands", E["glands"], C_BLACK, "plastic", 15, "shell", ee)
    add("Post clamps", E["clamps"], C_GALV_D, "metal", 8, "shell", (250, 0, 0))
    add("Mounting back plate", E["plate"], C_ALU, "metal", 8, "shell", ee)
    add("Controller board", E["pcb"], C_PCB, "plastic", 8, "shell", ei)
    add("Controller board chips", E["chips"], C_BLACK, "plastic", 8, "shell", ei)
    add("LiFePO4 battery, 12.8 V 25 Ah", E["batt"], C_BATT, "plastic", 6, "shell", ei)
    add("Battery lid", E["batt_top"], C_BLACK, "plastic", 6, "shell", ei)
    add("Battery terminal cover, positive", E["term_pos"], C_RED, "plastic", 6, "shell", ei)
    add("Battery terminal cover, negative", E["term_neg"], C_BLACK, "plastic", 6, "shell", ei)
    add("Battery label", E["batt_label"], C_LABEL, "paper", 6, "shell", ei)
    add("MPPT charge controller", E["mppt"], C_BATT, "painted", 7, "shell", ei)
    add("MPPT heat sink fins", E["fins"], C_ALU, "metal", 7, "shell", ei)
    add("MPPT display (lit)", E["lcd"], C_LCD, "emissive", 7, "shell", ei)
    add("MPPT status LEDs (lit)", E["leds"], C_LED_G, "emissive", 7, "shell", ei)
    add("MPPT keys", E["keys"], C_BLACK, "plastic", 7, "shell", ei)

    # ---- 9 sensor head
    Sn = _sensors(P, D)
    es = (550, -450, 300)
    add("Radiation shield plates", Sn["plates"], C_SHELL, "plastic", 9, "shell", es)
    add("Radiation shield spacers", Sn["spacers"], C_ALU, "metal", 9, "shell", es)
    add("Temperature and humidity probe", Sn["probe"], C_SHELL2, "plastic", 9, "shell", es)
    add("Sensor arm", Sn["arm"], C_GALV, "metal", 9, "shell", es)
    add("Sensor arm post clamp", Sn["clamp"], C_GALV_D, "metal", 9, "shell", (300, -450, 300))
    add("PIR presence sensor housing", Sn["pir"], C_SHELL, "plastic", 9, "shell", (0, -450, -450))
    add("PIR Fresnel dome", Sn["dome"], C_CART, "plastic", 9, "shell", (0, -450, -450))
    add("PIR indicator (lit)", Sn["pir_led"], C_LED_G, "emissive", 9, "shell", (0, -450, -450))

    # ---- 15 harness
    runs, ties = _harness(P, D)
    add("Cable runs, outdoor cable", runs, C_LINE, "rubber", 15, "shell", (250, 0, 350))
    add("Cable clips", ties, C_BLACK, "plastic", 15, "shell", (250, 0, 350))

    # ---- water plant (internal): 13 tank, 10 pump, 11 filter, 14 drain valve, 15 hoses
    W = _water(P, D)
    et, epump, ef, ev = (-700, -600, 0), (-750, -650, 350), (-950, -900, 200), (-850, -1000, 600)
    add("Water tank, 120 L opaque", W["tank"], C_TANK, "plastic", 13, "internal", et)
    add("Tank screw lid", W["lid"], C_BLACK, "plastic", 13, "internal", (-700, -600, 250))
    add("Lid lock hasp", W["hasp"], C_ALU, "metal", 13, "internal", (-700, -600, 250))
    add("Tank strap and tether", W["strap"], C_STRAP, "fabric", 13, "internal", et)
    add("Strap ratchet", W["buckle"], C_ALU, "metal", 13, "internal", et)
    add("Strap post eye", W["post_eye"], C_GALV_D, "metal", 13, "internal", (0, 0, 0))
    add("Tank label, potable water only", W["label"], C_LABEL, "paper", 13, "internal", et)
    add("Tank label band", W["label_band"], C_ACCENT, "plastic", 13, "internal", et)
    add("Tank outlet tap", W["tap"], C_BLACK, "plastic", 13, "internal", et)
    add("Tank anchor cleats", W["cleats"], C_GALV_D, "metal", 13, "internal", et)
    add("Tank suction fitting", W["fitting"], C_BLACK, "plastic", 15, "internal", et)
    add("Pump shelf bracket", W["shelf"], C_GALV_D, "metal", 10, "internal", (0, 0, 0))
    add("Pump box, vented", W["pbox"], C_SHELL, "plastic", 10, "internal", epump)
    add("Pump box window", W["win"], C_GLASS, "clear", 10, "internal", epump)
    add("Pump box label", W["pbox_label"], C_ACCENT, "plastic", 10, "internal", epump)
    add("Pump motor", W["motor"], C_BLACK, "metal", 10, "internal", epump)
    add("Pump head", W["head"], C_SHELL2, "plastic", 10, "internal", epump)
    add("Pressure switch", W["sw"], C_BLACK, "plastic", 10, "internal", epump)
    add("Pump mounting feet", W["feet"], C_BLACK, "rubber", 10, "internal", epump)
    add("Filter head and bracket", W["fhead"], C_SHELL2, "plastic", 11, "internal", ef)
    add("Filter bowl, clear", W["bowl"], C_GLASS, "clear", 11, "internal", ef)
    add("Filter cartridge, 5 um", W["cart"], C_CART, "paper", 11, "internal", ef)
    add("Filter cartridge core", W["cart_core"], C_SHELL2, "plastic", 11, "internal", ef)
    add("Filter bowl ring", W["fring"], C_ACCENT, "plastic", 11, "internal", ef)
    add("Filter ports", W["fports"], C_BLACK, "plastic", 11, "internal", ef)
    add("Drain valve body", W["vbody"], C_BRASS, "metal", 14, "internal", ev)
    add("Drain valve coil", W["coil"], C_BLACK, "plastic", 14, "internal", ev)
    add("Drain valve spout", W["spout"], C_LINE, "plastic", 14, "internal", ev)
    add("Drain tee from riser", W["tee"], C_LINE, "plastic", 12, "internal", ev)
    add("Riser outlet fitting", W["riser_fit"], C_BLACK, "plastic", 12, "internal", epump)
    add("Suction hose", W["suction"], C_LINE, "rubber", 15, "internal", (-700, -600, 150))
    add("Filter to pump hose", W["fhose"], C_LINE, "rubber", 15, "internal", ef)

    # ---- context: paved patch, curb, existing bench, person
    base, slabs, curb, slats, bframe = _context()
    add("Paving bed", base, C_JOINT, "painted", None, "context", (0, 0, 0))
    add("Paving slabs", slabs, C_PAVE, "painted", None, "context", (0, 0, 0))
    add("Curb", curb, C_CURB, "painted", None, "context", (0, 0, 0))
    add("Existing bench, timber slats", slats, C_TIMBER, "wood", None, "context", (0, 0, 0))
    add("Existing bench frame", bframe, C_BENCH, "painted", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(PERSON_AT[0], PERSON_AT[1], 0) * Rot(0, 0, PERSON_ROT) * mannequin(1750, "stand")
    add("Person, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:38s} {p['group']:9s} {p['material']:8s} valid={s.is_valid}")
