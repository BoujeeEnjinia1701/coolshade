"""CoolShade concept media from the TRL 3 model (option A, constructable design, CSH-DDR-003).

Run from the repo root:  python cad/src/concept_media.py [hero|exploded|flow|web|blueprint|all ...]
With no argument it draws everything with .kit/concept.py render_all. On a small machine run one picture per
process; "web" alone rewrites only media/model.glb and viewer.html (the D3 model is large). Geometry comes from
components(CHOSEN) in cad/src/model.py, grouped by BOM line; figures come from CSH-CAL-001 (docs/04-calcs/sizing.py).

Axes as model.py: X along the curb, Y across the sidewalk (street side is -Y), Z up, slab at Z = 0.
Not for fabrication.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src"), str(ROOT / "docs" / "04-calcs")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
from build123d import Box, Compound, Pos  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "CoolShade", "Solar misting shade canopy concept", "CSH-DWG-010", "2026-10-30"
MD = ROOT / "media"
GREY = "#9CA3AF"
# colour and explode offset per BOM line (mm), as in the former massing model
LOOK = {1: ("#64748B", (0, 0, 0)), 2: ("#475569", (0, 0, 700)), 3: ("#0F766E", (0, 0, 1400)), 4: ("#A16207", (0, 0, -350)),
        5: ("#1E3A8A", (0, 900, 2100)), 6: ("#C2410C", (1100, -350, -500)), 7: ("#16A34A", (1100, 300, 450)),
        8: ("#E5E7EB", (450, 0, 0)), 9: ("#7C3AED", (600, -600, 350)), 10: ("#2563EB", (-1100, -300, 900)),
        11: ("#0EA5E9", (-1300, -700, 250)), 12: ("#111827", (0, -300, 350)), 13: ("#D4A017", (-900, 1100, 0)),
        14: ("#DC2626", (-100, -700, 0)), 15: ("#374151", (0, 400, 150)), 16: ("#94A3B8", (0, 0, 0))}


def _names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, name = r["item"].partition(" ")
        out[int(n)] = name
    return out


def parts():
    """One Part per BOM line (the whole detailed assembly grouped by line); fasteners without a line go to line 16."""
    names, groups = _names(), {}
    for p in M.components(M.CHOSEN):
        groups.setdefault(p["bom"] or 16, []).append(p["shape"])
    out = []
    for n in sorted(groups):
        col, ex = LOOK.get(n, (GREY, (0, 0, 0)))
        out.append(Part(names.get(n, "Fasteners"), Compound(children=groups[n]), col, n, ex))
    return out


def context():
    sidewalk = Pos(300, 0, -60) * Box(6200, 3800, 120)
    curb = Pos(300, -1960, -85) * Box(6200, 120, 170)
    road = Pos(300, -2720, -230) * Box(6200, 1400, 60)
    bench = (Pos(150, 520, 440) * Box(1500, 420, 50) + Pos(150, 710, 700) * Box(1500, 40, 380)
             + Pos(-500, 520, 210) * Box(50, 380, 420) + Pos(800, 520, 210) * Box(50, 380, 420))
    return [Part("Sidewalk", sidewalk, "#D1D5DB"), Part("Curb and road", curb + road, "#6B7280"), Part("Existing bench", bench, GREY)]


def key_figures():
    return ["Shade roof 3.0 x 2.4 m (7.2 m2); headroom 2,223 mm minimum (CSH-CAL-001)",
            "8 low-pressure nozzles at 7 bar, 32 L/h while spraying (nozzle data to confirm)",
            "85 L water and 204 Wh per hot, dry day; 2.7 °C air cooling while spraying at 1 m/s",
            "100 W panel, 12.8 V 25 Ah LiFePO4 (1.26 days); 12 V DC only, no mains",
            "Mists only above 32 °C, below 60 % RH, with people present",
            "Fabric on only in gusts below 15 m/s; USD 882 in parts (indicative), budget under review",
            "D3 model: 372 parts, 284 fasteners, 233 kg (cad/fidelity.json)"]


def flow_spec():
    return {"title": "daily water flow on a hot, dry day, L per day (estimates, CSH-CAL-001; 70 L evaporated absorbs about 47 kWh)",
            "unit": "L",
            "stages": [("Daily fill, potable", 95), ("Tank, 120 L", 95), ("Filter and pump", 80), ("Mist line, 8 nozzles", 80), ("Evaporated", 70)],
            "losses": [(1, "Residual drained, line flush", 15), (3, "Drift, drip and wetting", 10)]}


def _robust_views():
    """The kit's project_views stops on a degenerate ellipse edge from the hidden-line projection of the
    detailed model; fall back to the edge-by-edge projection of sheets.py for that view set."""
    import drawing
    from sheets import safe_project_views
    orig = drawing.project_views

    def views(part, workdir, line_weight=0.35, center_lines=True):
        try:
            return orig(part, workdir, line_weight=line_weight, center_lines=center_lines)
        except (AssertionError, ValueError, ZeroDivisionError):
            return safe_project_views(part, workdir, line_weight=line_weight)
    drawing.project_views = views


def everything():
    _robust_views()
    f = flow_spec()
    return K.render_all(parts(), PROJECT, TITLE, DWG, key_figures(), date=DATE, rev="P3", cut=False, context=context(), flow=f)


if __name__ == "__main__":
    fns = {"hero": lambda: K._render(K.with_scale_figure(parts()) + context(), MD / "hero.png", title=PROJECT,
                                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale"),
           "exploded": lambda: K._render(parts(), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                                         note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv"),
           "flow": lambda: K.flow_diagram(flow_spec()["stages"], MD / "flow.png", f"{PROJECT}: {flow_spec()['title']}", "L", flow_spec()["losses"]),
           "web": lambda: K.export_web_model(parts(), "media", title=f"{PROJECT}: {TITLE}"),
           "all": everything}
    for w in sys.argv[1:] or ["all"]:
        print(w, "->", fns[w]())
