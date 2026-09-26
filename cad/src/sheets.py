"""CoolShade general arrangement sheet CSH-DWG-001, Rev P1 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CSH-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept blueprint in media/ is CSH-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", [] if name in ("iso", "top") else hidden)):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm, _ = assembly()
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CoolShade", title="General arrangement", dwg_no="CSH-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Galvanized S275 SHS frame; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    PX, PY = P["post_x"], P["post_y"]
    zr = D["zr"]

    # front view (from -Y, the street): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 8:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(x - 10, zg + 11, "SLAB (EXISTING)", 2.0, 600, MUTED, "start"))
    top_front = zr(-P["roof_d"] / 2)
    L += [ext(X(-P["roof_l"] / 2), Z(top_front) - 1, X(-P["roof_l"] / 2), Z(top_front) - 9),
          ext(X(P["roof_l"] / 2), Z(top_front) - 1, X(P["roof_l"] / 2), Z(top_front) - 9)]
    L += dim_h(X(-P["roof_l"] / 2), X(P["roof_l"] / 2), Z(top_front) - 8, f"{P['roof_l']:,.0f} roof")
    L += dim_h(X(-PX), X(PX), zg + 6, f"{2 * PX:,.0f} post centers")
    L += [ext(X(-PX), zg + 1, X(-PX), zg + 7), ext(X(PX), zg + 1, X(PX), zg + 7)]
    xl = X(bb.min.X) - 4
    L += [ext(X(-PX) - 2, Z(D["beam_under_front"]), xl - 1, Z(D["beam_under_front"]))]
    L += dim_v(xl, Z(D["beam_under_front"]), zg, f"{D['beam_under_front']:,.0f} beam underside")
    L += [ext(X(-PX + P['post'] / 2), Z(D["brace_low_front"]), xl - 7, Z(D["brace_low_front"]))]
    L += dim_v(xl - 6, Z(D["brace_low_front"]), zg, f"{D['brace_low_front']:,.0f} front brace")

    # top view (from +Z): X to the right, Y up the sheet (street at the bottom)
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L.append(_t(Xt(bb.max.X) + 4, Yt(bb.min.Y) + 1, "STREET SIDE (-Y), HIGH EDGE", 1.9, 600, MUTED, "start"))
    L += leader(Xt(D["enc_x"]), Yt(PY), Xt(bb.max.X) + 4, Yt(PY) - 6, "ENCLOSURE, ITEMS 6 TO 8")
    L += leader(Xt(0), Yt(P["panel_y"]), Xt(bb.max.X) + 4, Yt(P["panel_y"]) + 2, "PANEL 100 W")
    L += leader(Xt(D["tank_xy"][0]), Yt(D["tank_xy"][1]), Xt(bb.min.X) - 3, Yt(D["tank_xy"][1]) + 6, "TANK 120 L", "end")

    # right view (from +X): Y to the right, Z up
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Zr(0)
    L.append(f'<line x1="{x - 4:.2f}" y1="{zg:.2f}" x2="{x + w + 4:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L += dim_h(Yr(-P["roof_d"] / 2), Yr(P["roof_d"] / 2), Zr(P["z_front"]) - 8, f"{P['roof_d']:,.0f} roof")
    L += [ext(Yr(-P["roof_d"] / 2), Zr(P["z_front"]) - 1, Yr(-P["roof_d"] / 2), Zr(P["z_front"]) - 9),
          ext(Yr(P["roof_d"] / 2), Zr(P["z_rear"]) - 1, Yr(P["roof_d"] / 2), Zr(P["z_front"]) - 9)]
    L += dim_h(Yr(-PY), Yr(PY), zg + 6, f"{2 * PY:,.0f} post centers")
    L += [ext(Yr(-PY), zg + 1, Yr(-PY), zg + 7), ext(Yr(PY), zg + 1, Yr(PY), zg + 7)]
    xr = Yr(bb.max.Y) + 4
    for i, (zz, label) in enumerate(((D["brace_low_rear"], f"{D['brace_low_rear']:,.0f} rear brace, min. headroom"),
                                     (D["nozzle_tip_rear"], f"{D['nozzle_tip_rear']:,.0f} nozzle tip"),
                                     (P["z_rear"], f"{P['z_rear']:,.0f} rear beam axis"))):
        xd = xr + 6 * i
        L += [ext(Yr(PY), Zr(zz), xd + 1, Zr(zz))]
        L += dim_v(xd, Zr(zz), zg, label, side=1)
    L += [ext(Yr(-P["roof_d"] / 2), Zr(P["z_front"]), Yr(bb.min.Y) - 9, Zr(P["z_front"]))]
    L += dim_v(Yr(bb.min.Y) - 8, Zr(P["z_front"]), zg, f"{P['z_front']:,.0f} front beam axis")
    L.append(_t(Yr(0), Zr(P["z_front"]) - 14, f"ROOF SLOPE {D['slope_deg']:.1f} DEG", 2.0, 600, INK, "middle"))
    L.append(_t(Yr(-P["roof_d"] / 2), zg + 12, "STREET", 1.9, 600, MUTED, "start"))

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 88, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Roof {P['roof_l']:,.0f} x {P['roof_d']:,.0f} ({D['roof_area_m2']:.1f} m2), mono-pitch {D['slope_deg']:.1f} deg, high at the street",
        f"Posts {P['post']:.0f} x {P['post']:.0f} x {P['post_t']:.0f} SHS on {2 * PX:,.0f} x {2 * PY:,.0f}; beams {P['beam']:.0f} x {P['beam_t']:.0f} SHS",
        f"Knee braces {P['brace_od']:.0f} OD, {P['brace_drop']:.0f} down x {P['brace_reach']:.0f} along; headroom {D['brace_low_rear']:,.0f} min.",
        f"Base plates {P['plate']:.0f} x {P['plate']:.0f} x {P['plate_t']:.0f}, 4 x M{P['anchor_d']:.0f} at {P['anchor_pitch']:.0f}; anchors about 6.4 kN factored",
        f"Mist loop {D['line_len_mm'] / 1000:.1f} m, {P['line_id']:.1f} bore, 8 nozzles {P['nozzle_orifice']} mm; vacuum breaker at front",
        f"Tank {P['tank_nominal_l']:.0f} L, strapped to the rear left post; drain valve at the low point",
        f"Enclosure {P['enc'][0]:.0f} x {P['enc'][1]:.0f} x {P['enc'][2]:.0f} on the rear right post, {D['enc_bot']:,.0f} to {D['enc_top']:,.0f}",
        "Fabric off before storms: beams overloaded with fabric above about 16 m/s (CSH-CAL-001)",
        "Third-angle; front view from the street (-Y); slab by others, checked per site",
    ], x=276, y=146, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "CSH-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
