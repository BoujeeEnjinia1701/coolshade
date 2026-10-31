"""CoolShade concept options B and C, modelled at D3 on the same bolted frame as option A (kit 1.9).

Option B, wet-pad fan cooler under shade: a welded 25 mm SHS cabinet at the rear of the canopy with a
cellulose wet pad in its rear opening, a 12 V axial fan in its front panel, a drip tube in a trough over the
pad and a drain tray under it; water is pumped once-through from the tank (no sump, no free aerosol).
Option C, passive double-skin roof: eight welded spacers on the end beams and purlins carry four rails
100 mm above the shade cloth, and three white aluminium composite strips on the rails reflect the sun; the
air gap vents by buoyancy. No water, no power.

Both keep option A's posts, base plates, braces, roof frame, cleats, fixings and (B) tank, equipment plate,
sensor, panel, battery and controller; parts that only option A needs are left out. Axes as model.py.
"""
from __future__ import annotations

import math

from build123d import Box, Cylinder, Plane, Pos, Rot, Sketch, Circle, RegularPolygon, Vector, extrude

import cad_parts as cp
import model as M
import csh_parts as cs
from csh_parts import sp, soft, weld_bead, box

SKIP_B = ("Misting pump", "Drain valve", "Vacuum breaker", "Mist line", "Slip-lok tee", "Mist line hanger")


def _weld_ring(c, a, size, leg=4.0, skip=()):
    """Fillet welds all round a square tube of side 'size' that butts a flat face: c is the centre of the
    seam, a the unit vector from the tube toward the face."""
    a = Vector(*a)
    ref = Vector(1, 0, 0) if abs(a.X) < 0.9 else Vector(0, 1, 0)
    u1 = a.cross(ref).normalized()
    u2 = a.cross(u1).normalized()
    c = Vector(*c)
    beads = []
    for u, v in ((u1, u2), (u2, u1)):
        for sg in (-1, 1):
            n1 = u * sg
            if any((n1 - Vector(*k)).length < 1e-6 for k in skip):
                continue
            p0 = c + n1 * (size / 2) - v * (size / 2 - 0.5)
            beads.append(weld_bead(p0, v, size - 1.0, n1, a * -1, leg))
    return M.fuse(beads)


def _pop_rivet(axis, u, v, s, sg, hole_r=1.2):
    """2.4 mm blind rivet: head on the surface at s, shank 8 mm toward sg. Returns (rivet, hole)."""
    sh = M.at_axis(axis, u, v, s, sg, Pos(0, 0, 3.0) * Cylinder(1.2, 6.0))
    hd = M.at_axis(axis, u, v, s, -sg, Pos(0, 0, 0.5) * Cylinder(3.2, 1.0))
    return sh + hd, M.acyl(axis, u, v, s - 1.5 * sg, s + 6.0 * sg, hole_r)


def _base_filtered(exclude, keep_sys):
    return [q for q in M.parts_A() if q["sys"] in keep_sys and not q["name"].startswith(exclude)]


# ================================================================================================ option B
def _on(origin, x_dir, z_dir, shape):
    return Plane(origin=origin, x_dir=x_dir, z_dir=z_dir) * shape


def _new_fasteners(n0, sysn="cabinet"):
    out = []
    for f in M.FAST[n0:]:
        out.append(sp(f["name"], f["shape"], "stainless" if "rivet" in f["name"] else "zinc_plated", "fastener", None, sysn))
    return out


def option_b(p=None):
    p = p or M.PARAMS
    keep = ("frame", "fabric", "panel", "enc", "sensor", "plant", "cables")
    base = [q for q in M.parts_A(p) if q["sys"] in keep and not q["name"].startswith(SKIP_B)]
    n0 = len(M.FAST)
    out = list(base)
    lx, ly = -p["post_x"], p["post_y"]
    yf = ly - p["post"] / 2
    x0p, x1p, z0p, z1p, tpl = p["eq_plate"]
    yp = yf - tpl
    pz = p["pump_z"]
    out.append(sp("Circulation pump 12 V, 5 L/min", cp.break_edges(box(lx - 40, lx + 120, yp - 80, yp, pz - 50, pz + 50), 4.0),
                  "matte_black", "bought", 10, "plant", color="#2563EB"))
    cab = []                                    # (name, shape, material, kind, color)
    X0, W, Y0, D, Z0, H = 0.0, 800.0, 800.0, 300.0, 6.0, 894.0
    a = 25.0
    ux = (-W / 2 + a / 2, W / 2 - a / 2)
    uy = (Y0 + a / 2, Y0 + D - a / 2)
    members = {}
    for i, (xx, yy) in enumerate([(x, y) for x in ux for y in uy], 1):
        members[f"Cabinet upright {i}, SHS 25 x 25 x 2"] = Pos(xx, yy, Z0) * cp.shs(a, 2.0, H)
    rails = []
    ZB = Z0 + 10.0
    for (z0_, nm) in ((ZB, "bottom"), (Z0 + H - a, "top")):
        zc = z0_ + a / 2
        for yy, side in zip(uy, ("front", "rear")):
            members[f"Cabinet {nm} rail, {side}"] = Pos(-(W / 2 - a), yy, zc) * Rot(0, 90, 0) * cp.shs(a, 2.0, W - 2 * a)
            rails.append((zc, "x", yy))
        for xx, side in zip(ux, ("left", "right")):
            members[f"Cabinet {nm} rail, {side}"] = Pos(xx, Y0 + a, zc) * Rot(-90, 0, 0) * cp.shs(a, 2.0, D - 2 * a)
            rails.append((zc, "y", xx))
    welds = []
    for zc, d, k in rails:
        zin = (0, 0, 1) if zc < 100 else (0, 0, -1)         # one fillet on the face toward the middle of the cabinet
        skip_all = tuple(v for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)) if v != zin)
        if d == "x":
            for sx in (-1, 1):
                welds.append(("Weld, rail to upright (x rail)", _weld_ring((sx * (W / 2 - a), k, zc), (sx, 0, 0), a, skip=skip_all)))
        else:
            for sy_, ycen in ((-1, Y0 + a), (1, Y0 + D - a)):
                welds.append(("Weld, rail to upright (y rail)", _weld_ring((k, ycen, zc), (0, sy_, 0), a, skip=skip_all)))
    feet = {}
    for i, (xx, yy) in enumerate([(x, y) for x in ux for y in uy], 1):
        sxo = 1 if xx > 0 else -1
        syo = 1 if yy > Y0 + D / 2 else -1
        fk = f"Cabinet foot plate {i}, 70 x 70 x 6"
        feet[fk] = Pos(xx, yy, 0.0) * cp.sheet(70, 70, 6.0, holes=[(sxo * 27.5, syo * 27.5, 9.0), (0, syo * 27.5, 9.0)], r_corner=4.0)
        welds.append(("Weld, upright to foot plate", _weld_ring((xx, yy, Z0), (0, 0, -1), a)))
        M.setctx("cabinet")
        for ax_, ay_ in ((xx + sxo * 27.5, yy + syo * 27.5), (xx, yy + syo * 27.5)):
            s_, h_ = M.bolt("z", ax_, ay_, 6.0, 0.0, 8, nut=False, tip=-70.0)
            feet[fk] = feet[fk] - h_
    # skins
    th = 1.5
    fan_z = Z0 + H / 2
    bolt_pts = [(sx * 105, fan_z + sz * 105) for sx in (-1, 1) for sz in (-1, 1)]
    skins = {}
    zs, hs = (Z0 + 10.0 + Z0 + H) / 2, H - 10.0
    skins["Cabinet front panel, galvanised 1.5 mm"] = _on((0, Y0, zs), (1, 0, 0), (0, -1, 0),
        cp.sheet(W, hs, th, holes=[(0, fan_z - zs, 235.0)] + [(x, z - zs, 6.0) for x, z in bolt_pts], r_corner=6.0, edge=0.3))
    skins["Cabinet left side panel, galvanised 1.5 mm"] = _on((-W / 2, Y0 + D / 2, zs), (0, 1, 0), (-1, 0, 0), cp.sheet(D, hs, th, r_corner=6.0, edge=0.3))
    skins["Cabinet right side panel, galvanised 1.5 mm"] = _on((W / 2, Y0 + D / 2, zs), (0, 1, 0), (1, 0, 0), cp.sheet(D, hs, th, r_corner=6.0, edge=0.3))
    skins["Cabinet top panel, galvanised 1.5 mm"] = Pos(0, Y0 + D / 2, Z0 + H) * cp.sheet(W, D, th, holes=[(-360, 1053.5 - (Y0 + D / 2), 22.0)], r_corner=6.0, edge=0.3)
    # blind rivets through the skins into the tubes
    rivs = []
    for sx in (-1, 1):
        for z in (100, 300, 500, 700, 850):
            rivs.append(_pop_rivet("y", sx * (W / 2 - a / 2), z, Y0 - th, 1))
    for sx in (-1, 1):
        for yy in uy:
            for z in (100, 450, 850):
                rivs.append(_pop_rivet("x", yy, z, sx * (W / 2 + th), -sx))
    for sx in (-1, 1):
        for yy in (Y0 + D / 2 - 60, Y0 + D / 2 + 60):
            rivs.append(_pop_rivet("z", sx * (W / 2 - a / 2), yy, Z0 + H + th, -1))
    for r_, h_ in rivs:
        for k in list(members):
            members[k] = members[k] - h_ if _touch(members[k], h_) else members[k]
        for k in list(skins):
            skins[k] = skins[k] - h_ if _touch(skins[k], h_) else skins[k]
    # pad, tray, trough, tube
    px0, px1 = -(W / 2 - a - 5.0), (W / 2 - a - 5.0)
    py0, py1 = 1008.5, 1098.5
    zt = ZB + a
    tray = box(px0, px1, py0 - 1.5, py1 + 1.5, zt, zt + 1.5) + box(px0, px1, py0 - 1.5, py0, zt, zt + 30) + box(px0, px1, py1, py1 + 1.5, zt, zt + 30)
    tray = tray - M.acyl("z", -330, 1053.5, zt - 1, zt + 2.5, 9.6)
    pad = cp.break_edges(box(px0, px1, py0, py1, zt + 1.5, 840.0), 1.5)
    trough_z = Z0 + H - a - 1.5
    trough_hole = M.acyl('z', -360, 1053.5, trough_z - 1, trough_z + 2.5, 10.3)
    trough = box(px0, px1, py0 - 1.5, py1 + 1.5, trough_z, trough_z + 1.5) + box(px0, px1, py0 - 1.5, py0, 825.0, trough_z) + box(px0, px1, py1, py1 + 1.5, 825.0, trough_z)
    trough = trough - trough_hole
    tube_y, tube_z = 1053.5, 855.0
    tube = Pos(-360, tube_y, tube_z) * Rot(0, 90, 0) * Pos(0, 0, 360) * cp.round_tube(20.0, 2.0, 720.0)
    tube = Pos(-360 + 360, tube_y, tube_z) * Rot(0, 90, 0) * Pos(0, 0, 0) * (Cylinder(10, 720) - Cylinder(8, 722))
    for xh in range(-315, 316, 90):
        tube = tube - M.acyl("z", xh, tube_y, tube_z - 11, tube_z, 2.0)
    riser = M.acyl("z", -360, tube_y, tube_z, 935.0, 10.0) - M.acyl("z", -360, tube_y, tube_z - 1, 936.0, 8.0)
    tube = tube + riser
    cap_r = Pos(360, tube_y, tube_z) * Rot(0, 90, 0) * (Pos(0, 0, 5) * Cylinder(8.0, 10) + Pos(0, 0, 11.5) * Cylinder(10.5, 3))
    cap_l = Pos(-360, tube_y, tube_z) * Rot(0, 90, 0) * (Pos(0, 0, -5) * Cylinder(8.0, 10) + Pos(0, 0, -11.5) * Cylinder(10.5, 3))
    cap_r = Pos(0, 0, 0) * cap_r
    clamps, clamp_r = [], []
    for xc in (-200.0, 200.0):
        ring = Pos(xc, tube_y, tube_z) * Rot(0, 90, 0) * (Cylinder(12.5, 12) - Cylinder(10, 13))
        tab = box(xc - 5, xc + 5, tube_y - 2.0, tube_y + 2.0, tube_z + 12.4, trough_z)
        clamps.append(cp.break_edges(ring + tab, 0.4))
        r_, h_ = _pop_rivet("z", xc, tube_y, trough_z + 1.5, -1)
        clamp_r.append((r_, h_))
        trough = trough - h_
        clamps[-1] = clamps[-1] - h_
    # drain nipple and nut
    nip = M.acyl("z", -330, 1053.5, 22.0, zt + 1.5, 9.5) - M.acyl("z", -330, 1053.5, 21.0, zt + 2.5, 7.5)
    nut = Pos(-330, 1053.5, zt - 6.0) * extrude(RegularPolygon(24 / math.sqrt(3), 6), 6.0)
    nut = nut - M.acyl("z", -330, 1053.5, zt - 7.0, zt + 1.0, 9.5)
    # fan: frame and motor, rotor, guard
    y_panel = Y0 - th
    fan_frame = Pos(0, 0, 12.5) * Box(250, 250, 25) - Pos(0, 0, 12.5) * Cylinder(117, 26)
    for bx_, bz_ in ((105, 105), (-105, 105), (105, -105), (-105, -105)):
        fan_frame = fan_frame - Pos(bx_, bz_, 12.5) * Cylinder(3.0, 26)
    can = Pos(0, 0, 5) * Cylinder(30, 10)
    struts = [Rot(0, 0, ang) * Pos(73, 0, 3) * Box(88, 7, 6) for ang in (90, 210, 330)]
    fan_frame = cp.break_edges(fan_frame, 1.5) + can + M.fuse(struts)
    blades = [Rot(0, 0, i * 360 / 7) * Pos(72.5, 0, 0) * Rot(25, 0, 0) * Box(85, 28, 1.5) for i in range(7)]
    rotor = Pos(0, 0, 16) * Cylinder(30, 12) + Pos(0, 0, 16) * M.fuse(blades)
    gsheet = cp.sheet(250, 250, 2.0, holes=[(0, 0, 232.0)] + [(x, z, 6.0) for x, z in ((105, 105), (-105, 105), (105, -105), (-105, -105))], r_corner=6.0, edge=0.3)
    guard = Pos(0, 0, 25.0) * gsheet
    wires = [Pos(0, 0, 26) * (Cylinder(r + 1.5, 2) - Cylinder(r - 1.5, 2.2)) for r in (40.0, 80.0)]
    spokes = [Rot(0, 0, ang) * Pos(58, 0, 26) * Box(116.5, 3, 2) for ang in range(0, 180, 30)] + [Rot(0, 0, ang) * Pos(58, 0, 26) * Box(116.5, 3, 2) for ang in range(180, 360, 30)]
    guard = cp.break_edges(guard, 0.2) + M.fuse(wires) + M.fuse(spokes)
    fan_place = lambda sh: M.at_axis("y", 0.0, fan_z, y_panel, -1, sh)
    for x, z in bolt_pts:
        s_, h_ = M.bolt("y", x, z, y_panel - 27.0, Y0, 5)
    out.append(sp("Axial fan frame and motor, 250 mm 12 V", fan_place(fan_frame), "matte_black", "bought", None, "cabinet", color="#1C1F24"))
    out.append(sp("Axial fan rotor, 7 blades", fan_place(rotor), "matte_black", "bought", None, "cabinet", color="#2F3A4A"))
    out.append(sp("Fan guard, galvanised", fan_place(guard), "galvanised", "bought", None, "cabinet"))
    for nm, sh in members.items():
        out.append(sp(nm, sh, "galvanised", "made", None, "cabinet"))
    for nm, sh in feet.items():
        out.append(sp(nm, sh, "galvanised", "made", None, "cabinet"))
    for nm, sh in skins.items():
        out.append(sp(nm, sh, "galvanised", "made", None, "cabinet"))
    for i, (nm, sh) in enumerate(welds, 1):
        out.append(sp(f"{nm} {i}", sh, "mild_steel", "weld", None, "cabinet"))
    out.append(sp("Drip tray, galvanised 1.5 mm", cp.break_edges(tray, 0.4), "galvanised", "made", None, "cabinet"))
    out.append(sp("Pad trough, galvanised 1.5 mm", cp.break_edges(trough, 0.4), "galvanised", "made", None, "cabinet"))
    out.append(sp("Cellulose wet pad, 90 mm", pad, "plywood", "bought", None, "cabinet", color="#C9A46E"))
    out.append(sp("Drip tube with riser, PVC 20 mm", tube, "hdpe_natural", "bought", None, "cabinet"))
    out.append(sp("Drip tube end plug", cp.break_edges(cap_r, 0.4), "hdpe_natural", "bought", None, "cabinet"))
    for i, c_ in enumerate(clamps, 1):
        out.append(sp(f"Tube clamp {i}, polypropylene", c_, "hdpe_black", "bought", None, "cabinet"))
    for r_, h_ in clamp_r + rivs:
        out.append(sp("Pop rivet 2.4 mm (cabinet)", r_, "aluminium", "fastener", None, "cabinet"))
    out.append(sp("Drain nipple, PVC 20 mm", nip, "hdpe_natural", "bought", None, "cabinet"))
    out.append(sp("Drain nipple lock nut", cp.break_edges(nut, 0.4), "hdpe_natural", "bought", None, "cabinet"))
    # supply hose from the pump to the drip tube riser
    hose = M.polyline_rod([(lx + 20, yp - 40, pz + 50), (lx + 20, yp - 40, 1370.0), (-380.0, 1092.0, 1370.0), (-360.0, tube_y, 1370.0), (-360.0, tube_y, 930.0)], 5.0)
    out.append(sp("Supply hose, pump to drip tube", hose, "epdm", "bought", None, "plant"))
    out += _new_fasteners(n0)
    return out


def _touch(a, b):
    A, B = a.bounding_box(), b.bounding_box()
    return not (A.min.X > B.max.X or A.max.X < B.min.X or A.min.Y > B.max.Y or A.max.Y < B.min.Y or A.min.Z > B.max.Z or A.max.Z < B.min.Z)


def parts(option):
    return {"B": option_b, "C": option_c}[option]()


def _plane_hole(RP, x, s, n0, r, z0, z1):
    """Cylinder normal to the roof plane at (x, s) with its axis from n0 + z0 to n0 + z1 (mm along the normal)."""
    return RP * Pos(x, s, n0 + (z0 + z1) / 2) * Cylinder(r, abs(z1 - z0))


def option_c(p=None):
    p = p or M.PARAMS
    D = M.derived(p)
    RP = M.roof_plane(p)
    th = math.atan((p["z_front"] - p["z_rear"]) / p["roof_d"])
    half = p["beam"] / 2
    base = [q for q in M.parts_A(p) if q["sys"] == "frame"]
    out = list(base)
    M.setctx("roof")
    n0 = len(M.FAST)
    # shade cloth without the panel notch, with a cut-out round each spacer
    Ls = p["roof_d"] / math.cos(th)
    nf = half + p["fabric_lift"]
    fab = RP * Pos(0, 0, nf + p["fabric_t"] / 2) * Box(p["roof_l"], Ls + 40, p["fabric_t"])
    fab = fab & M.bx(-p["roof_l"] / 2, p["roof_l"] / 2, -p["roof_d"] / 2, p["roof_d"] / 2, 0, 4000)
    sites = [(sx * xm, sg * 800.0) for xm in (530.0, 1475.0) for sx in (-1, 1) for sg in (-1, 1)]
    for xm, sm in sites:
        fab = fab - RP * Pos(xm, sm, nf + p["fabric_t"] / 2) * Box(46, 110, 20)
    out.append(sp("Shade cloth, knitted HDPE", fab, "canvas", "bought", 3, "fabric", color="#0F766E"))
    # spacers: base plate, 30 x 30 x 2 SHS stub, top plate, two fillet-weld rings, M8 bolts into rivet nuts, M6 bolts to the rail
    rail_holes = []                       # world cutters for the rails
    member_holes = {}                     # world cutters for beams and purlins
    for k, (xm, sm) in enumerate(sites, 1):
        loc = RP * Pos(xm, sm, half)
        wt = p["purlin_t"] if abs(xm) < 1000 else p["beam_t"]
        n1 = len(M.FAST)
        base_pl = cp.sheet(36, 100, 4.0, holes=[(0, -36.0, 9.0), (0, 36.0, 9.0)], r_corner=3.0, edge=0.4)
        hole_m = []
        for sg in (-1, 1):
            s_, hc, ht = M.bolt("z", 0.0, sg * 36.0, 5.2, -wt, 8, nut=False, tip=-wt - 6.0, rivet=wt)
            hole_m.append(ht)
        stub = Pos(0, 0, 5.2) * cp.shs(30, 2.0, 90.8)
        top_pl = Pos(0, 0, 96.0) * cp.sheet(36, 100, 4.0, holes=[(0, -36.0, 7.0), (0, 36.0, 7.0)], r_corner=3.0, edge=0.4)
        hole_r = []
        for sg in (-1, 1):
            s_, h_ = M.bolt("z", 0.0, sg * 36.0, 96.0, 102.0, 6)
            top_pl = top_pl - h_
            hole_r.append(h_)
        w1 = _weld_ring((0, 0, 5.2), (0, 0, -1), 30.0, leg=4.0)
        w2 = _weld_ring((0, 0, 96.0), (0, 0, 1), 30.0, leg=4.0)
        out.append(sp(f"Spacer base plate {k}, 36 x 100 x 4", loc * soft(Pos(0, 0, 1.2) * base_pl), "galvanised", "made", None, "roof"))
        out.append(sp(f"Spacer stub {k}, SHS 30 x 30 x 2", loc * stub, "galvanised", "made", None, "roof"))
        out.append(sp(f"Spacer top plate {k}, 36 x 100 x 4", loc * soft(top_pl), "galvanised", "made", None, "roof"))
        out.append(sp(f"Weld, spacer {k} to base plate", loc * w1, "mild_steel", "weld", None, "roof"))
        out.append(sp(f"Weld, spacer {k} to top plate", loc * w2, "mild_steel", "weld", None, "roof"))
        for f in M.FAST[n1:]:
            f["shape"] = loc * f["shape"]
        base_pl_holes = hole_m
        for h in hole_m:
            member_holes.setdefault("m", []).append((xm, sm, loc * h))
        for h in hole_r:
            rail_holes.append(loc * h)
    # rails
    rail_len = Ls - 40.0
    rails = []
    for xm in sorted(set(x for x, _ in sites)):
        r_ = RP * Pos(xm, 0, half + 115.0) * Rot(-90, 0, 0) * Pos(0, 0, -rail_len / 2) * cp.shs(30, 2.0, rail_len)
        rails.append((xm, r_))
    # skin: three 3 mm white aluminium sheets, 3000 x 804, on the rails, fixed with self-drilling screws
    strips = []
    sw = (Ls - 4.0) / 3
    for i, sc in enumerate((-sw - 2.0, 0.0, sw + 2.0), 1):
        pl = cp.sheet(3000, sw, 3.0, r_corner=6.0, edge=0.4)
        strips.append((i, sc, pl))
    screws, skin_holes = [], []
    for i, sc, pl in strips:
        for xm, r_ in rails:
            for ds in (-250.0, 250.0):
                s_pos = sc + ds
                top = half + 133.0                                           # top face of the sheet
                washer = RP * Pos(xm, s_pos, top) * cp.washer(6)
                scr = RP * Pos(xm, s_pos, top + 1.6) * cp.hex_bolt(6, 15.0)
                screws.append((washer, scr))
                skin_holes.append((i, RP * Pos(xm, s_pos, top - 1.5) * Cylinder(3.5, 3.2)))
                rail_holes.append(RP * Pos(xm, s_pos, top - 4.0) * Cylinder(3.0, 2.0))
    for i, sc, pl in strips:
        shp = RP * Pos(0, sc, half + 130.0) * pl
        for j, h in skin_holes:
            if j == i:
                shp = shp - h
        out.append(sp(f"Roof sheet {i}, aluminium 3 mm, white powder coat", shp, "aluminium", "bought", None, "roof", color="#F2F2EE"))
    for xm, r_ in rails:
        for h in rail_holes:
            if _touch(r_, h):
                r_ = r_ - h
        out.append(sp(f"Roof rail {'right' if xm > 0 else 'left'} {abs(xm):.0f}, SHS 30 x 30 x 2", r_, "galvanised", "made", None, "roof"))
    for k, (w_, s_) in enumerate(screws, 1):
        out.append(sp("Washer, sealing, M6", w_, "epdm", "fastener", None, "roof"))
        out.append(sp("M6 x 15 self-drilling screw", s_, "zinc_plated", "fastener", None, "roof"))
    # member holes (rivet nuts) cut in the beams and purlins that carry spacers
    for q in out:
        if q["name"].startswith(("End beam", "Purlin")):
            for xm, sm, h in member_holes.get("m", []):
                if _touch(q["shape"], h):
                    q["shape"] = q["shape"] - h
    for f in M.FAST[n0:]:
        if f["sys"] == "roof":
            out.append(sp(f["name"], f["shape"], "stainless" if "rivet" in f["name"] else "zinc_plated", "fastener", None, "roof"))
    return out
