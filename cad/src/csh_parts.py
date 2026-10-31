"""CoolShade repo-specific part builders for the kit 1.9 model (D3), used by cad/src/model.py.

Everything here is built from PARAMS and the helpers of model.py; nothing changes a design dimension.
  sp()                  a cad_parts.part() dict with a "sys" tag (the sub-system it belongs to)
  soft()                break the edges of a bare box or cylinder, as a real part has
  weld_bead()           a triangular fillet weld bead along an edge, between two faces
  enclosure_parts()     IP65 enclosure: body, door, gasket, hinges, lock, glands, gear plate, battery,
                        MPPT controller, controller board with standoffs, connectors and fuse holders
  panel_parts()         100 W solar panel: aluminium frame, laminate, junction box; rails and T-bolts
  end_cap_parts()       black plastic end caps of the long beams
"""
from __future__ import annotations

import math

from build123d import Box, Cone, Cylinder, Plane, Polygon, Pos, Rot, Vector, extrude

import cad_parts as cp
from cad_parts import part
import model as M


def sp(name, shape, material, kind="made", bom=None, sys="frame", color=None, explode=(0, 0, 0)):
    q = part(name, shape, material, kind=kind, bom=bom, group=sys, explode=explode, color=color)
    q["sys"] = sys
    return q


def is_bare(shape):
    try:
        faces = shape.faces()
        return len(faces) == 3 or (len(faces) == 6 and all(str(f.geom_type).endswith("PLANE") for f in faces))
    except Exception:
        return False


def soft(shape, r=1.0):
    """Edge break on a bare box or cylinder (r limited to a fifth of the smallest side)."""
    if not is_bare(shape):
        return shape
    bb = shape.bounding_box()
    r = min(r, 0.2 * min(bb.size.X, bb.size.Y, bb.size.Z))
    return cp.break_edges(shape, max(r, 0.2)) if r > 0.05 else shape


def weld_bead(p, d, length, n1, n2, leg=5.0):
    """Fillet weld bead from point p along unit vector d for 'length' mm, in the corner between a face with
    outward normal n1 and one with outward normal n2 (both perpendicular to d); 'leg' mm legs."""
    d, n1, n2 = Vector(*d), Vector(*n1), Vector(*n2)
    s = 1.0 if d.cross(n1).dot(n2) > 0 else -1.0
    pts = [(0, 0), (leg, 0), (0, leg)] if s > 0 else [(0, 0), (0, -leg), (leg, 0)]       # counter-clockwise, so extrude goes along +d
    tri = Polygon(*pts, align=None)
    pl = Plane(origin=Vector(*p), x_dir=n1, z_dir=d)
    return pl * extrude(tri, length)


def box(x0, x1, y0, y1, z0, z1):
    return M.bx(x0, x1, y0, y1, z0, z1)


def _tube(r_out, r_in, x0, x1, y, z):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * (Cylinder(r_out, x1 - x0) - Cylinder(r_in, x1 - x0 + 1))


# ----------------------------------------------------------------------------------------------------------
def end_cap_parts(p):
    """Four black plastic end caps (50 x 50 mm) closing the long beams, with a spigot into the tube."""
    D = M.derived(p)
    out = []
    L, half, bt = p["roof_l"], p["beam"] / 2, p["beam_t"]
    for sy in (-1, 1):
        zc = D["zr"](sy * p["post_y"])
        for sx in (-1, 1):
            x_face = sx * L / 2
            plate = M.bx(x_face, x_face + sx * 3, sy * p["post_y"] - half, sy * p["post_y"] + half, zc - half, zc + half)
            spig = M.bx(x_face - sx * 14, x_face, sy * p["post_y"] - (half - bt - 0.6), sy * p["post_y"] + (half - bt - 0.6),
                        zc - (half - bt - 0.6), zc + (half - bt - 0.6))
            cap = cp.break_edges(plate + spig, 0.8)
            out.append(sp(f"End cap, {'right' if sx > 0 else 'left'} end of the {'front' if sy < 0 else 'rear'} long beam", cap,
                          "matte_black", "bought", 2, "frame"))
    return out


# ----------------------------------------------------------------------------------------------------------
def panel_parts(p, Pc, th):
    """Solar panel in the roof plane (Pc = M.PIECES['panel']): frame, laminate, junction box; hollow aluminium
    rails with T-bolts to the L-feet."""
    RP = M.roof_plane(p)
    pw, pd, ph, sc, n_pan, rx, rail = Pc["pw"], Pc["pd"], Pc["ph"], Pc["sc"], Pc["n_pan"], Pc["rx"], Pc["rail"]
    fw = 30.0
    out = []
    frame = Box(pw, pd, ph) - Box(pw - 2 * fw, pd - 2 * fw, ph + 2)
    frame = cp.break_edges(frame, 1.0)
    fr = RP * Pos(0, sc, n_pan + ph / 2) * frame
    out.append(sp("Solar panel frame, anodised aluminium", fr, "aluminium", "bought", 5, "panel"))
    lam = Box(pw - 2 * fw, pd - 2 * fw, 6.8)
    lam = cp.break_edges(lam, 0.8)
    out.append(sp("Solar panel laminate, glass and cells", RP * Pos(0, sc, n_pan + ph - 3.0 - 3.4) * lam, "glass", "bought", 5, "panel", color="#1B2A4A"))
    jb = cp.break_edges(Box(100, 60, 15), 2.0)
    out.append(sp("Solar panel junction box", RP * Pos(0, sc + pd / 2 - 90, n_pan + ph - 3.0 - 6.8 - 7.5) * jb, "matte_black", "bought", 5, "panel"))
    # rails: hollow aluminium 40 x 40 x 2.5, one over each pair of feet (replaces the massing bars)
    n_rail0 = p["beam"] / 2 + p["rail_gap"]
    for i, sx in enumerate((-1, 1)):
        rl = RP * Pos(sx * rx, sc, n_rail0 + rail / 2) * Rot(-90, 0, 0) * Pos(0, 0, -(pd + 50) / 2) * cp.rhs(rail, rail, 2.5, pd + 50)
        for h in th["rail_l" if sx < 0 else "rail_r"]:
            rl = rl - h
        out.append(sp(f"Panel rail, {'right' if sx > 0 else 'left'}, aluminium 40 x 40 x 2.5", rl, "aluminium", "bought", 5, "panel"))
    return out


def rail_tbolts(p, Pc):
    """M6 bolts through each L-foot leg into its rail (nut and washer inside the hollow rail). Returns the
    fastener list and the holes to cut: {"feet": [...], "rail_l": [...], "rail_r": [...]}."""
    D = M.derived(p)
    th = math.atan((p["z_front"] - p["z_rear"]) / p["roof_d"])
    rx, rail, half = Pc["rx"], Pc["rail"], p["beam"] / 2
    n_c = half + p["rail_gap"] + rail / 2
    holes = {"feet": [], "rail_l": [], "rail_r": []}
    for yc in (p["bearer_y"], p["post_y"]):
        s = M.roof_s(yc, n_c, p)
        z = D["z_mid"] - s * math.sin(th) + n_c * math.cos(th)
        for sx in (-1, 1):
            xo = sx * (rx + rail / 2)
            M.setctx("panel")
            s_, h_ = M.bolt("x", yc, z, xo + sx * 4, xo - sx * 2.5, 6)
            holes["feet"].append(h_)
            holes["rail_l" if sx < 0 else "rail_r"].append(h_)
    return holes


# ----------------------------------------------------------------------------------------------------------
def enclosure_parts(p):
    """The lockable IP65 enclosure on its rails on the outer face of the rear right post, with everything in it."""
    S = p["post"]
    ew, ed, eh = p["enc"]
    rt = p["enc_rail"][1]
    xr0 = p["post_x"] + S / 2
    x0 = xr0 + rt
    ey, ez = p["enc_y"], p["enc_z"]
    w = 2.0
    out = []
    M.setctx("enc")
    # body, open on its outer face, with rail screw holes, gland holes and four internal bosses
    body = box(x0, x0 + ew, ey - ed / 2, ey + ed / 2, ez - eh / 2, ez + eh / 2) - box(x0 + w, x0 + ew + 1, ey - ed / 2 + w, ey + ed / 2 - w, ez - eh / 2 + w, ez + eh / 2 - w)
    body = cp.break_edges(body, 3.0)
    gl_y = (ey - 90, ey - 9, p["post_y"] - 13)
    glands = []
    for gy in gl_y:
        body = body - M.zcyl(x0 + 134, gy, ez - eh / 2 + w / 2, 8.25, w + 0.02)
        g = M.zcyl(x0 + 134, gy, ez - eh / 2 - 7.5, 10.5, 15) + M.zcyl(x0 + 134, gy, ez - eh / 2 + w + 3, 11, 6)
        g = g - M.zcyl(x0 + 134, gy, ez - eh / 2, 3.5, 40)
        glands.append(cp.break_edges(g, 0.6))
    rail_z = (ez - 130, ez + 130)
    screws_at = [(yy, z) for z in rail_z for yy in (ey - 130, ey + 130)]
    for yy, z in screws_at:
        body = body - M.acyl("x", yy, z, x0 - 0.01, x0 + w + 0.01, 3.5)
    boss_at = [(yy, zz) for yy in (ey - 100, ey + 110) for zz in (ez + 0, ez + 180)]
    for yy, zz in boss_at:
        body = body + (M.acyl("x", yy, zz, x0 + w, x0 + w + 6, 5.0) - M.acyl("x", yy, zz, x0 + w - 0.1, x0 + w + 6.1, 2.0))
    out.append(sp("Enclosure body, IP65, painted steel", body, "insulated_white", "bought", 8, "enc", color="#E5E7EB"))
    for i, g in enumerate(glands, 1):
        out.append(sp(f"Cable gland M20 ({i})", g, "matte_black", "bought", 8, "enc"))
    # rail screws (M6) from inside the body into the rails
    holes_rail = []
    for yy, z in screws_at:
        s_, h_ = M.bolt("x", yy, z, x0 + w, x0 - 14, 6, nut=False, tip=x0 - 14)
        holes_rail.append((yy, z, h_))
    # gear plate
    gp = M.bx(x0 + w + 6, x0 + w + 8, ey - 110, ey + 120, ez - 10, ez + 190)
    for yy, zz in boss_at:
        gp = gp - M.acyl("x", yy, zz, x0 + w + 5.9, x0 + w + 8.1, 2.2)
    gp = cp.break_edges(gp, 0.8)
    out.append(sp("Gear plate, galvanised steel 2 mm", gp, "galvanised", "made", 8, "enc"))
    for yy, zz in boss_at:                                 # M4 pan-head screws from the front into the bosses
        scr = M.at_axis("x", yy, zz, x0 + w + 8, 1, Pos(0, 0, 1.2) * Cylinder(4.0, 2.4) + Pos(0, 0, -4.0) * Cylinder(2.0, 8.0))
        out.append(sp("M4 pan-head screw (gear plate)", scr, "zinc_plated", "fastener", None, "enc"))
    # door, gasket, hinges, lock
    xd = x0 + ew
    gk = Box(ed, eh, 2.0) - Box(ed - 24, eh - 24, 2.2)
    gk = Pos(xd + 1.0, ey, ez) * Rot(0, 90, 0) * gk
    out.append(sp("Door gasket, EPDM", gk, "epdm", "bought", 8, "enc"))
    door = Pos(xd + 2.0 + 1.5, ey, ez) * Rot(0, 90, 0) * Box(ed, eh, 3.0)
    door = cp.break_edges(door, 2.5)
    lock_y, lock_z = ey + 110, ez
    door = door - M.acyl("x", lock_y, lock_z, xd + 1.9, xd + 5.1, 9.2)
    yw = ey - ed / 2
    xdo = xd + 5.0
    hz = (ez - 120, ez + 120)
    rivets = []
    for z in hz:
        for (kind, y_, xx_, z_) in (("door", yw + 14, xdo, z - 15), ("door", yw + 14, xdo, z + 15), ("body", yw, xd - 10, z - 15), ("body", yw, xd - 10, z + 15)):
            rivets.append((kind, y_, xx_, z_))
    for kind, y_, xx_, z_ in rivets:
        if kind == "door":
            door = door - M.acyl("x", y_, z_, xdo - 3.1, xdo + 0.1, 1.2)
    out.append(sp("Enclosure door, painted steel 3 mm", door, "insulated_white", "bought", 8, "enc", color="#E5E7EB"))
    for i, z in enumerate(hz, 1):
        leafA = box(xdo, xdo + 2, yw - 4, yw + 28, z - 25, z + 25)
        leafB = box(xdo + 2 - 28, xdo + 6.5, yw - 2, yw, z - 25, z + 25)
        knuckle = M.acyl("z", xdo + 4.5, yw - 4.5, z - 25, z + 25, 3.2) - M.acyl("z", xdo + 4.5, yw - 4.5, z - 26, z + 26, 1.5)
        hinge = cp.break_edges(leafA + leafB + knuckle, 0.4)
        for kind, y_, xx_, z_ in rivets:
            if abs(z_ - z) < 20 and kind == "door":
                hinge = hinge - M.acyl("x", y_, z_, xdo - 0.1, xdo + 2.1, 1.2)
            if abs(z_ - z) < 20 and kind == "body":
                hinge = hinge - M.acyl("y", xx_, z_, yw - 2.1, yw + 0.1, 1.2)
        out.append(sp(f"Door hinge ({i}), galvanised steel", hinge, "galvanised", "bought", 8, "enc"))
        out.append(sp(f"Hinge pin ({i}), 3 mm", M.acyl("z", xdo + 4.5, yw - 4.5, z - 25.5, z + 25.5, 1.5), "stainless", "fastener", None, "enc"))
    for kind, y_, xx_, z_ in rivets:                      # 2.4 mm pop rivets: door leaves into the door, body leaves into the side wall
        if kind == "door":
            sh = M.at_axis("x", y_, z_, xdo + 2.0, -1, Pos(0, 0, 1.5) * Cylinder(1.2, 3.0))
            hd = M.at_axis("x", y_, z_, xdo + 2.0, 1, Pos(0, 0, 0.5) * Cylinder(3.2, 1.0))
        else:
            sh = M.at_axis("y", xx_, z_, yw, 1, Pos(0, 0, 1.0) * Cylinder(1.2, 2.0))
            hd = M.at_axis("y", xx_, z_, yw, -1, Pos(0, 0, 2.5) * Cylinder(3.2, 1.0))
        out.append(sp("Pop rivet 2.4 mm (hinge leaf)", sh + hd, "aluminium", "fastener", None, "enc"))
    lk = M.at_axis("x", lock_y, lock_z, xd + 5, -1, Pos(0, 0, 8) * Cylinder(9.0, 16.0)) + M.at_axis("x", lock_y, lock_z, xd + 5, 1, Pos(0, 0, 1.0) * Cylinder(13.0, 2.0))
    lk = lk + M.at_axis("x", lock_y, lock_z, xd + 5 - 15, -1, Pos(0, 0, 1.0) * Box(40, 10, 2))
    lk = lk - M.at_axis("x", lock_y, lock_z, xd + 7.1, -1, Pos(0, 0, 1.0) * Box(1.2, 6, 2.0))
    out.append(sp("Cam lock with two keys", cp.break_edges(lk, 0.5), "zinc_plated", "bought", 8, "enc"))
    # battery 12.8 V 25 Ah, MPPT, board
    bw, bd_, bh = p["battery"]
    xb0 = x0 + w
    zb0 = ez - eh / 2 + w
    bat = cp.break_edges(box(xb0, xb0 + bw, ey - 100, ey - 100 + bd_, zb0, zb0 + bh), 4.0)
    out.append(sp("LiFePO4 battery 12.8 V 25 Ah", bat, "matte_black", "bought", 6, "enc", color="#2F3A4A"))
    for k, (sg, col) in enumerate(((1, "#B91C1C"), (-1, "#1C1F24"))):
        ty = ey - 100 + bd_ / 2 + sg * 45
        t = M.acyl("z", xb0 + bw / 2, ty, zb0 + bh, zb0 + bh + 12, 3.0) + M.acyl("z", xb0 + bw / 2, ty, zb0 + bh, zb0 + bh + 3, 6.0)
        out.append(sp(f"Battery terminal {'positive' if sg > 0 else 'negative'}, M6 stud", cp.break_edges(t, 0.4), "brass", "bought", 6, "enc"))
    # hold-down strap: a U band round three sides of the battery, resting on the back wall
    st = box(xb0, xb0 + bw + 2.0, ey - 100 - 1.5, ey - 100 + bd_ + 1.5, zb0 + 60, zb0 + 80) - box(xb0 - 1, xb0 + bw, ey - 100, ey - 100 + bd_, zb0 + 59, zb0 + 81)
    out.append(sp("Battery hold-down strap, galvanised 20 x 1.5", cp.break_edges(st, 0.4), "galvanised", "bought", 8, "enc"))
    mw, md, mh = p["mppt"]
    xg = x0 + w + 8
    mppt = cp.break_edges(box(xg, xg + mw, ey - 100, ey - 100 + md, ez + 30, ez + 30 + mh), 3.0)
    fins = M.fuse(box(xg + mw, xg + mw + 14, ey - 100 + 8 + 14 * k, ey - 100 + 8 + 14 * k + 3, ez + 30 + 6, ez + 30 + mh - 6) for k in range(6))
    out.append(sp("MPPT charge controller 12 V 10 A", mppt, "matte_black", "bought", 7, "enc", color="#2F3A4A"))
    # controller board on standoffs
    pcb_y0, pcb_y1, pcb_z0, pcb_z1 = ey + 10, ey + 110, ez + 40, ez + 150
    xp = xg + 6.0
    pcb = box(xp, xp + 1.6, pcb_y0, pcb_y1, pcb_z0, pcb_z1)
    mount = [(pcb_y0 + 5, pcb_z0 + 5), (pcb_y1 - 5, pcb_z0 + 5), (pcb_y0 + 5, pcb_z1 - 5), (pcb_y1 - 5, pcb_z1 - 5)]
    for yy, zz in mount:
        pcb = pcb - M.acyl("x", yy, zz, xp - 0.1, xp + 1.7, 1.7)
    out.append(sp("Controller board PCB, 1.6 mm", cp.break_edges(pcb, 0.3), "matte_black", "bought", 8, "enc", color="#166534"))
    for yy, zz in mount:
        so = M.acyl("x", yy, zz, xg, xp, 3.0) - M.acyl("x", yy, zz, xg - 1, xp + 1, 1.6)
        out.append(sp("Standoff M3 x 6, brass", so, "brass", "fastener", None, "enc"))
        scr = M.at_axis("x", yy, zz, xp + 1.6, 1, Pos(0, 0, 0.75) * Cylinder(2.8, 1.5)) + M.acyl("x", yy, zz, xg + 0.5, xp + 1.6, 1.5)
        out.append(sp("M3 pan-head screw (board)", scr, "zinc_plated", "fastener", None, "enc"))
    xt = xp + 1.6
    comps = [("Terminal block, 6-way", (pcb_y0 + 12, pcb_y0 + 88, pcb_z0 + 10, pcb_z0 + 25, 12), "#2563EB"),
             ("Blade fuse holder, 15 A", (pcb_y0 + 10, pcb_y0 + 35, pcb_z0 + 30, pcb_z0 + 50, 18), "#1C1F24"),
             ("Blade fuse holder, 5 A", (pcb_y0 + 45, pcb_y0 + 70, pcb_z0 + 30, pcb_z0 + 50, 18), "#1C1F24"),
             ("Microcontroller module", (pcb_y0 + 10, pcb_y0 + 60, pcb_z0 + 60, pcb_z0 + 85, 8), "#1D4ED8"),
             ("MOSFET driver module", (pcb_y0 + 65, pcb_y0 + 95, pcb_z0 + 55, pcb_z0 + 85, 10), "#B91C1C"),
             ("Sensor bus connector, 4-way", (pcb_y0 + 70, pcb_y0 + 90, pcb_z0 + 92, pcb_z0 + 102, 8), "#E5E7EB")]
    for nm, (y0_, y1_, z0_, z1_, h_), col in comps:
        out.append(sp(nm, cp.break_edges(box(xt, xt + h_, y0_, y1_, z0_, z1_), 0.8), "matte_black", "bought", 8, "enc", color=col))
    out.append(sp("MPPT heat sink fins", cp.break_edges(fins, 0.4), "aluminium", "bought", 7, "enc"))
    return out, holes_rail, (x0, ey, ez)
