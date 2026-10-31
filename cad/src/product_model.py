"""CoolShade product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is: posts, braces, base plates and cleats,
roof frame, cleats, shade cloth, solar panel with rails and feet, enclosure with door, battery and board, sensor
head, pump, filter, tank with strap, mist line with nozzles, hoses and every bolt, nut, washer and rivet nut.
Only the site is added, as context parts: a market lane with a concrete slab, a kerb and an asphalt road on the
street side (-Y), an existing bench and a 1.75 m person standing in the shade for scale. The hero is rendered by
.kit/photoreal.py as an outdoor scene on concrete with the ground at model z = 0 (RENDER_VIEWS "args").
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the whole canopy), "plant" (the water plant only, for the detail view), "context" (site, bench, person).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "CoolShade: solar-powered shade canopy with fine misting"

# Sun from the camera side: camera azimuth -40, sun azimuth -70 (30 degrees apart), 58 degrees up.
_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=58,-70", "--lens=35"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "context"], "explode": False, "el": 16, "az": -40, "args": _SITE,
     "note": "Site render from the street side, front right and a little above (about 16 deg elevation): the canopy "
             "on a market-lane slab beside the kerb, shade cloth over the roof, solar panel at the rear edge, "
             "mist line and nozzles under the street-side beam, strapped tank and pump at the rear left post, "
             "controller enclosure on the rear right post; 1.75 m person in the shade for scale"},
    {"name": "studio", "groups": ["shell"], "explode": False, "el": 24, "az": -40,
     "note": "Studio render from the front right and above (about 24 deg elevation): posts with knee braces and "
             "base plates, roof frame, cloth, panel, nozzles, tank, pump box and enclosure on the bare canopy"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): panel and rails, shade cloth "
             "and roof frame lifted off the posts; mist line loop with nozzles below the frame; tank, pump, filter "
             "and drain valve pulled out at left; enclosure, battery and board at right; base plates below"},
    {"name": "detail", "groups": ["plant"], "explode": False, "el": 20, "az": -35,
     "note": "Detail from the front right and slightly above (about 20 deg elevation), water plant only: "
             "strapped 120 L tank, pump on its equipment plate, filter, drain valve and hoses at the rear left post"},
]


def _explode(p):
    """Explode vector (mm) by system and name, relative to the assembled position."""
    n, s = p["name"].lower(), p.get("sys", "")
    if s == "fabric":
        return (0, 0, 1400)
    if s == "panel":
        return (0, 900, 2100)
    if s == "enc":
        return (450, 0, 0) if "battery" not in n else (1100, -350, -500)
    if s == "sensor":
        return (600, -600, 350)
    if s == "plant":
        return (-1000, 600, 300)
    if s == "mist":
        return (0, -300, 350)
    if any(k in n for k in ("base plate", "base cleat", "m16", "anchor")):
        return (0, 0, -350)
    if any(k in n for k in ("beam", "purlin", "cleat", "bearer")):
        return (0, 0, 700)
    return (0, 0, 0)


def site():
    """Market lane: a concrete slab 120 mm thick (its top at z = 0, reaching below ground), a kerb and a strip of
    asphalt on the street side (-Y), an existing bench and a person standing in the shade. Every site part reaches
    below z = 0."""
    out = []
    ctx = lambda n, sh, mat, col=None: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context", color=col))
    ctx("Concrete slab", Pos(300, 0, -150) * Box(7000, 4200, 300), "concrete")
    ctx("Kerb", break_edges(Pos(300, -2230, -150) * Box(7000, 220, 320), 8), "concrete")
    ctx("Road", Pos(300, -3500, -150) * Box(7000, 2300, 290), "concrete", "#4B4F55")
    bench = (Pos(150, 560, 440) * Box(1500, 420, 50) + Pos(150, 750, 700) * Box(1500, 40, 380)
             + Pos(-500, 560, 210) * Box(50, 380, 420) + Pos(800, 560, 210) * Box(50, 380, 420))
    out.append(part("Existing bench (site)", bench, "mild_steel", kind="context", group="context", color="#9CA3AF"))
    try:
        import context_parts
        man = Pos(450, -150, 0) * Rot(0, 0, 160) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    parts = [p for p in M.components(M.CHOSEN) if p["kind"] != "context"]
    out = []
    for p in parts:
        q = dict(p)
        q["group"] = "shell"
        q["explode"] = _explode(p)
        out.append(q)
        if p.get("sys") == "plant":
            r = dict(p)
            r["group"] = "plant"
            r["name"] = p["name"] + " (plant)"
            r["explode"] = (0, 0, 0)
            out.append(r)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "plant" for p in ps), "plant,",
          sum(p["group"] == "context" for p in ps), "context")
