"""CoolShade prototype build plan pictures (CSH-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|wiring ...]
A sheet, joint or step can be named on its own, for example "sheet:103" or "step:7" or "joint:2",
so that each picture can be drawn in its own process when memory is tight.
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CSH-DWG-101 to 116        making sketches for the made components and the cloth
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/slab-layout.png     anchor and post positions on the slab (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
    docs/05-build-plan/water.png           water circuit, tank to nozzles and drain (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
D = derived(P)
_C = None


def C():
    global _C
    if _C is None:
        _C = build_components(P)
    return _C


COL = {"plate": "#A16207", "bcleat": "#CA8A04", "post": "#64748B", "hcleat": "#1D4ED8", "beam": "#475569",
       "brace": "#0E7490", "fcleat": "#6D28D9", "endb": "#334155", "purlin": "#57534E", "bearer": "#B45309",
       "line": "#111827", "clip": "#9CA3AF", "vb": "#DC2626", "rails": "#94A3B8", "feet": "#0F766E",
       "panel": "#1E3A8A", "clamps": "#374151", "encr": "#B91C1C", "enc": "#E5E7EB", "battery": "#C2410C",
       "mppt": "#16A34A", "arm": "#7C3AED", "shield": "#F5F5F4", "pir": "#4B5563", "eqp": "#78716C",
       "pump": "#2563EB", "filter": "#0EA5E9", "drain": "#DC2626", "tank": "#D4A017", "strap": "#1F2937",
       "stops": "#A16207", "fabric": "#0F766E", "harness": "#EA580C", "bolt": "#111827", "slab": "#E5E7EB"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


ABOVE_SLAB = {"anchors", "stop_bolts"}      # anchors drawn only above the slab surface


def part(name, keys, color, explode=(0, 0, 0), alpha=1.0):
    keys = [keys] if isinstance(keys, str) else keys
    shapes = [C()[k].shape & bx(-5000, 5000, -5000, 5000, 0, 5000) if k in ABOVE_SLAB else C()[k].shape for k in keys]
    return Part(name, _fuse(shapes), color, None, tuple(explode), alpha)


POSTS = ("fr", "fl", "rr", "rl")


def slab(x0=-1750, x1=1950, y0=-1500, y1=1450):
    return Part("Slab (existing)", bx(x0, x1, y0, y1, -60, 0), COL["slab"])


def made():
    """Named parts in build order (the overview numbering)."""
    return {
        "plates": part("Base plates (4)", [f"plate_{p}" for p in POSTS], COL["plate"]),
        "bcleats": part("Base cleats (8) and anchors", [f"bcleat_{p}" for p in POSTS] + ["anchors", "base_bolts"], COL["bcleat"]),
        "posts": part("Posts (4)", [f"post_{p}" for p in POSTS], COL["post"]),
        "hcleats": part("Head cleats (8)", [f"hcleat_{p}" for p in POSTS] + ["head_bolts"], COL["hcleat"]),
        "beams": part("Long beams (2)", ["beam_f", "beam_r"], COL["beam"]),
        "braces": part("Knee braces (4)", [f"brace_{p}" for p in POSTS] + ["brace_bolts"], COL["brace"]),
        "fcleats": part("Frame cleats (10)", ["frame_cleats", "frame_bolts"], COL["fcleat"]),
        "endb": part("End beams (2)", ["endb_r", "endb_l"], COL["endb"]),
        "purlins": part("Purlins (2)", ["purlin_r", "purlin_l"], COL["purlin"]),
        "bearer": part("Panel bearer", "bearer", COL["bearer"]),
        "line": part("Mist line loop, nozzles, clips, vacuum breaker", ["mistline", "clips", "vbreaker"], COL["line"]),
        "rails": part("Panel rails and L-feet", ["rails", "feet", "foot_bolts"], COL["feet"]),
        "panel": part("Solar panel and clamps", ["panel", "clamps"], COL["panel"]),
        "encr": part("Enclosure rails (2)", ["enc_rails", "rail_bolts"], COL["encr"]),
        "enc": part("Enclosure, battery, MPPT, controller", ["enclosure", "battery", "mppt", "board"], COL["enc"]),
        "arm": part("Sensor arm and shield", ["arm", "arm_bolts", "shield"], COL["arm"]),
        "pir": part("PIR presence sensor", "pir", COL["pir"]),
        "eqp": part("Equipment plate", ["eq_plate", "eq_bolts"], COL["eqp"]),
        "pump": part("Pump, filter, drain valve", ["pump", "filter", "drain"], COL["pump"]),
        "tank": part("Tank, strap, stop cleats", ["tank", "strap", "stops", "stop_bolts"], COL["tank"]),
        "fabric": part("Shade fabric", "fabric", COL["fabric"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"plates": (0, 0, -500), "bcleats": (0, 0, -250), "posts": (0, 0, 0), "hcleats": (0, 0, 300),
           "beams": (0, 0, 600), "braces": (0, 0, 0), "fcleats": (0, 0, 900), "endb": (0, 0, 1200),
           "purlins": (0, 0, 1200), "bearer": (0, 0, 1200), "line": (0, 0, -900), "rails": (0, 0, 2400),
           "panel": (0, 0, 2900), "encr": (500, 0, 0), "enc": (1100, 0, 0), "arm": (600, -600, 0), "pir": (300, -1500, -700),
           "eqp": (-1200, 0, -400), "pump": (-1800, -400, -400), "tank": (-300, -1300, -500), "fabric": (0, 0, 1750)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CoolShade prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the street side, front right and above. Cables (run inside the posts and beams) are not shown",
                       elev=20, azim=-62, size=(12, 9.5), dpi=150, key=True)


# ----------------------------------------------------------------- steps
def steps(only=None):
    M = made()
    out = []
    sl = slab()

    def st(n, done, new, title, sub, **kw):
        if only is not None and n != only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    base = [M["plates"], M["bcleats"]]
    st(1, [], [mv(part("Base plates (4) with anchors", [f"plate_{p}" for p in POSTS] + ["anchors"], COL["plate"]), (0, 0, 400))],
       "base plates and anchors on the slab",
       "Mark the post centres (2,800 x 2,350 mm), drill the slab through each plate, set 16 M16 anchors; nuts loose for now",
       context=[sl], elev=28, azim=-60, size=(9, 6))
    st(2, [M["plates"]], [mv(M["posts"], (0, 0, 500)), mv(part("Base cleats (8) and M12 bolts", [f"bcleat_{p}" for p in POSTS] + ["base_bolts"], COL["bcleat"]), (0, 0, 250))],
       "posts and base cleats",
       "Stand each post on its plate between two cleats over the anchors; two M12 bolts through cleat, post and cleat; plumb, prop, then tighten",
       elev=22, azim=-60, size=(9, 6.5))
    done2 = base + [M["posts"]]
    st(3, done2, [mv(M["hcleats"], (0, 0, 300))], "head cleats onto the post tops",
       "Two cleats per post, one each side, top faces flush with the post top; one M10 bolt through both and the post",
       elev=22, azim=-60, size=(9, 6.5), label_done=False)
    done3 = done2 + [M["hcleats"]]
    st(4, done3, [mv(M["beams"], (0, 0, 450))], "long beams onto the posts",
       "Rivet nuts set in the beams first. Lower each beam onto its two posts and fit one M8 bolt up through each cleat",
       elev=22, azim=-60, size=(9, 6.5), label_done=False)
    done4 = done3 + [M["beams"]]
    st(5, done4, [mv(M["braces"], (0, 0, -350))], "knee braces",
       "Lower end flat on the post's inner face (M10 through the post); upper end flat under the beam (M8 into a rivet nut)",
       elev=18, azim=-60, size=(9, 6.5), label_done=False)
    done5 = done4 + [M["braces"]]
    st(6, done5, [mv(M["fcleats"], (0, 0, 350))], "frame cleats onto the long beams",
       "Ten cleats on the inner faces of the long beams and of the purlins; one M8 bolt each into a rivet nut, finger tight",
       elev=30, azim=-60, size=(9, 6.5), label_done=False)
    done6 = done5 + [M["fcleats"]]
    st(7, done6, [mv(M["endb"], (0, 0, 400)), mv(M["purlins"], (0, 0, 400))], "end beams and purlins",
       "Drop each between the long beams against its cleats; one M8 bolt into a rivet nut per cleat; tops flush; then tighten all",
       elev=30, azim=-60, size=(9, 6.5), label_done=False)
    done7 = done6 + [M["endb"], M["purlins"]]
    st(8, done7, [mv(M["bearer"], (0, 0, 350))], "panel bearer between the purlins",
       "On its two cleats at the purlins' inner faces, 560 mm behind the roof's centre line; one M8 bolt per cleat",
       elev=32, azim=-55, size=(9, 6.5), label_done=False)
    done8 = done7 + [M["bearer"]]
    st(9, done8, [mv(M["line"], (0, 0, -450))], "mist line loop, clips, nozzles and vacuum breaker",
       "Clips on the long beams' inner faces and under the end beams; loop pushed into the clips; down pipe at the rear left corner",
       elev=24, azim=-60, size=(9, 6.5), label_done=False)
    done9 = done8 + [M["line"]]
    st(10, done9, [mv(M["rails"], (0, 0, 350))], "L-feet and panel rails",
       "Two L-feet on the bearer and two on the rear beam (M8 into rivet nuts); rails bolted to the feet 15 mm clear of the tubes",
       elev=34, azim=-55, size=(9, 6.5), label_done=False)
    done10 = done9 + [M["rails"]]
    st(11, done10, [mv(M["panel"], (0, 0, 400))], "solar panel onto the rails",
       "Panel's rear edge at the roof's rear edge; four end clamps. Cover the panel or leave it unplugged until section 6 allows",
       elev=34, azim=-55, size=(9, 6.5), label_done=False)
    done11 = done10 + [M["panel"]]
    def near(name, keys, box):
        return Part(name, _fuse([C()[k].shape for k in keys]) & bx(*box), "#9CA3AF")
    PX, PY = P["post_x"], P["post_y"]
    rr = [near("Rear right post", ["post_rr", "plate_rr", "bcleat_rr", "beam_r", "hcleat_rr", "brace_rr", "endb_r"], (PX - 500, PX + 200, PY - 600, PY + 200, 900, 2300))]
    fr = [near("Front right post", ["post_fr", "plate_fr", "bcleat_fr", "beam_f", "hcleat_fr", "brace_fr", "endb_r"], (PX - 700, PX + 200, -PY - 200, -PY + 500, 1900, 3100))]
    rl = [near("Rear left post", ["post_rl", "plate_rl", "bcleat_rl", "beam_r", "hcleat_rl", "brace_rl", "endb_l", "mistline"], (-PX - 200, -PX + 700, PY - 900, PY + 200, -10, 1650))]
    st(12, rr, [mv(M["encr"], (200, 0, 0)), mv(M["enc"], (450, 0, 0))], "enclosure rails and enclosure on the rear right post",
       "Rails on the post's outer face (M10 countersunk); box on the rails with four M6 screws from inside; battery out until section 6",
       elev=18, azim=-30, size=(9, 6.5), label_done=False)
    done12 = done11 + [M["encr"], M["enc"]]
    st(13, fr + [near("Front beam", ["beam_f"], (-200, PX - 700, -PY - 200, -PY + 200, 2800, 3100))], [mv(M["arm"], (0, -350, 0)), mv(M["pir"], (0, 0, -300))], "sensor arm, shield and PIR",
       "Arm on the street face of the front right post (two M8 through bolts); shield under the arm's end; PIR under the front beam",
       elev=16, azim=-50, size=(9, 6.5), label_done=False)
    done13 = done12 + [M["arm"], M["pir"]]
    st(14, rl, [mv(M["eqp"], (0, -300, 0)), mv(M["pump"], (0, -600, 0))], "equipment plate, pump, filter and drain valve",
       "Plate on the rear left post's front face (two M10 bolts); pump, filter and valve on the plate; down pipe into the valve and pump",
       elev=18, azim=-105, size=(9, 6.5), label_done=False)
    done14 = done13 + [M["eqp"], M["pump"]]
    st(15, rl + [M["eqp"], M["pump"]], [mv(M["tank"], (0, -500, 0))], "tank, stop cleats and strap",
       "Tank on the slab against the two stop cleats (one M10 anchor each); strap round the tank and the post at 400 mm",
       elev=22, azim=-110, size=(9, 6.5), label_done=False)
    done15 = done14 + [M["tank"]]
    st(16, done15, [part("Cables (inside the posts and beams) and hoses", "harness", COL["harness"])], "cables and hoses",
       "Pull the cables through the posts and beams (grommet at every hole); hoses tank to filter to pump. No power yet",
       elev=24, azim=-60, size=(9, 6.5), label_done=False)
    done16 = done15 + [part("Cables and hoses", "harness", "#9CA3AF")]
    st(17, done16, [mv(M["fabric"], (0, 0, 500))], "shade fabric, last, in calm weather",
       "Lay the cloth over the frame from the front, notch round the panel; lace every eyelet round its beam; only below 15 m/s forecast gusts",
       elev=26, azim=-60, size=(9, 6.5), label_done=False)
    return out


# ----------------------------------------------------------------- joints
def _win(k, b0, color, name, at=None):
    sh = C()[k].shape & bx(*b0) if isinstance(k, str) else _fuse([C()[q].shape for q in k]) & bx(*b0)
    p = Part(name, sh, color)
    p.at = at
    return p


def _joint(parts, out, title, subtitle=None, elev=24, azim=-58, size=(8, 6), dpi=160):
    """bv.joint with the leader of each part ending at a chosen point on it (Part.at, world mm),
    so that no leader ends on a neighbouring part."""
    import numpy as np
    parts = [p for p in parts if bv._has_volume(p.shape)]
    W, H = int(size[0] * dpi), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, verts = bv._raster([(p, p.color, p.alpha, (0, 0, 0)) for p in parts], elev, azim, W, H)
    fig, ax = bv._frame(size, dpi, title, subtitle)
    ax.imshow(img, interpolation="bilinear")
    pts = [np.asarray(getattr(p, "at", None), float) if getattr(p, "at", None) is not None else bv._anchor(v) for p, v in zip(parts, verts)]
    bv._draw_labels(ax, proj, pts, [p.name for p in parts], W, H)
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return out


def joints(only=None):
    out = []
    PX, PY = P["post_x"], P["post_y"]
    zr = D["zr"]

    def jt(n, parts, title, sub, **kw):
        out.append(_joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    want = lambda n: only is None or only == n  # noqa: E731
    if want(1):
        b0 = (PX - 130, PX + 130, -PY - 125, -PY + 125, -20, 260)
        jt(1, [_win("plate_fr", b0, "#78350F", "Base plate, 10 mm", (PX + 95, -PY - 105, 10)),
               _win("bcleat_fr", b0, COL["bcleat"], "Base cleat, 75 x 75 x 6 angle (one each side)", (PX + 44, -PY - 70, 80)),
               _win("post_fr", b0, COL["post"], "Post, 80 x 80 x 3", (PX + 10, -PY - 40, 220)),
               _win("anchors", b0, COL["bolt"], "M16 anchor through cleat and plate (4)", (PX + 80, -PY - 80, 26)),
               _win("base_bolts", (PX, PX + 130, -PY - 125, -PY + 125, -20, 260), "#475569", "M12 bolts through cleat, post, cleat (2)", (PX + 54, -PY, 72))],
           "post base (front right)", "The post stands on the plate between two cleats; anchors hold cleats and plate to the slab",
           elev=28, azim=-55)
    if want(2):
        zt = zr(PY) - 25
        b0 = (PX - 140, PX + 140, PY - 80, PY + 70, zt - 260, zt + 60)
        jt(2, [_win("post_rr", b0, COL["post"], "Post (top cut square)", (PX + 40, PY - 20, zt - 180)),
               _win("hcleat_rr", b0, COL["hcleat"], "Head cleat, 50 x 50 x 5 angle (one each side)", (PX + 70, PY - 23, zt - 3)),
               _win("beam_r", b0, COL["beam"], "Long beam, sits on the post top", (PX - 90, PY - 25, zt + 35)),
               _win("head_bolts", b0, COL["bolt"], "M10 through bolt; M8 bolts up into rivet nuts", (PX + 51, PY, zt - 28))],
           "post head (rear right)", "The beam sits on the post; each cleat bolts through the post and up into a rivet nut in the beam",
           elev=8, azim=-35)
    if want(3):
        zb = zr(PY) - 25
        b0 = (PX - 230, PX + 60, PY - 60, PY + 60, zb - 470, zb - 230)
        jt(3, [_win("post_rr", b0, COL["post"], "Post (inner face)", (PX - 40, PY - 32, zb - 450)),
               _win("brace_rr", b0, COL["brace"], "Knee brace, end flattened and bent", (PX - 150, PY, zb - 255)),
               _win("brace_bolts", b0, COL["bolt"], "M10 bolt through the post", (PX - 48, PY, zb - 372))],
           "knee brace lower end (rear right)", "The flattened end lies flat on the post's inner face; its bottom is the lowest point overhead, 2,223 mm",
           elev=12, azim=-125)
    if want(4):
        zb = zr(PY) - 25
        b0 = (PX - 440, PX - 250, PY - 60, PY + 60, zb - 130, zb + 55)
        jt(4, [_win("beam_r", b0, COL["beam"], "Long beam", (PX - 270, PY - 25, zb + 40)),
               _win("brace_rr", b0, COL["brace"], "Knee brace upper end", (PX - 300, PY, zb - 60)),
               _win("brace_bolts", b0, COL["bolt"], "M8 bolt into a rivet nut in the beam", (PX - 412, PY, zb - 8))],
           "knee brace upper end, seen from below", "The flattened end lies flat under the beam, 350 mm in from the post face",
           elev=-25, azim=-120)
    if want(5):
        zc = 2644.6
        b0 = (1370, 1510, 1040, 1215, zr(1150) - 60, zr(1150) + 45)
        jt(5, [_win("beam_r", b0, COL["beam"], "Long beam (rear)", (1385, 1185, zr(PY) + 25)),
               _win("endb_r", b0, "#94A3B8", "End beam, end cut to butt the beam face", (1475, 1105, zr(1105) + 25.2)),
               _win("frame_cleats", b0, COL["fcleat"], "Frame cleat, 50 x 50 x 5 angle", (1405, 1145, zc + 15)),
               _win("frame_bolts", b0, COL["bolt"], "M8 bolts into rivet nuts (2)", (1425, 1140, zc))],
           "end beam to long beam (rear right corner)", "Seen from inside the canopy. The end beam butts the beam's inner face; the cleat holds both",
           elev=22, azim=-145)
    if want(6):
        zc = 2649.6
        b0 = (440, 580, 1040, 1215, zr(1150) - 50, zr(1150) + 40)
        jt(6, [_win("beam_r", b0, COL["beam"], "Long beam (rear)", (455, 1185, zr(PY) + 25)),
               _win("purlin_r", b0, "#A8A29E", "Purlin, 40 x 40, top level with the end beams", (530, 1060, zr(1060) + 25.2)),
               _win("frame_cleats", b0, COL["fcleat"], "Frame cleat", (465, 1145, zc + 10)),
               _win("frame_bolts", b0, COL["bolt"], "M8 bolts into rivet nuts", (485, 1140, zc))],
           "purlin to long beam (rear right)", "The same cleat as joint 5, on the purlin's inner side",
           elev=22, azim=-145)
    if want(7):
        by = P["bearer_y"]
        zc = 2726.5
        b0 = (250, 580, by - 80, by + 60, zr(by) - 40, zr(by) + 100)
        jt(7, [_win("purlin_r", b0, "#A8A29E", "Purlin (right)", (545, by - 70, zr(by - 70) + 25)),
               _win("bearer", b0, COL["bearer"], "Panel bearer, 50 x 50", (400, by - 25, zr(by) - 5)),
               _win("frame_cleats", b0, COL["fcleat"], "Frame cleat on the bearer's front face", (470, by - 30, zc + 12)),
               _win("feet", b0, COL["feet"], "L-foot on the bearer", (323, by - 20, zr(by) + 55)),
               _win("rails", b0, COL["rails"], "Panel rail, 15 mm clear of the bearer", (300, by + 50, zr(by + 50) + 80.5)),
               _win(["frame_bolts", "foot_bolts"], b0, COL["bolt"], "M8 bolts into rivet nuts", (485, by - 30, zc))],
           "panel bearer, purlin and L-foot (right)", "Seen from the front left. The bearer butts the purlin on a cleat; the rail stands on an L-foot on the bearer",
           elev=26, azim=-125)
    if want(8):
        b0 = (230, 380, PY - 80, PY + 60, zr(PY) - 30, zr(PY) + 130)
        pt = lambda y, n: zr(y) + n / math.cos(math.radians(D["slope_deg"]))  # noqa: E731
        jt(8, [_win("beam_r", b0, COL["beam"], "Long beam (rear)", (250, PY - 25, zr(PY))),
               _win("feet", b0, COL["feet"], "L-foot", (323, PY - 20, zr(PY) + 60)),
               _win("rails", b0, COL["rails"], "Panel rail", (300, PY - 70, pt(PY - 70, 80))),
               _win("panel", b0, COL["panel"], "Solar panel frame", (250, PY - 60, pt(PY - 60, 115))),
               _win("clamps", b0, COL["clamps"], "End clamp at the panel's rear edge", (300, PY + 30, pt(PY + 30, 115))),
               _win("foot_bolts", b0, COL["bolt"], "M8 bolt into a rivet nut", (305, PY, zr(PY) + 34))],
           "rail, L-foot and end clamp on the rear beam (right rail)", "The panel's rear edge is level with the roof's rear edge",
           elev=22, azim=-35)
    if want(9):
        yl = D["y_line"]
        zf = D["line_z_front"]
        b0 = (1000, 1250, -PY - 30, -yl + 40, zf - 50, zr(-PY) + 30)
        jt(9, [_win("beam_f", b0, COL["beam"], "Long beam (front), inner face", (1120, -PY + 25, zr(-PY) + 5)),
               _win("clips", b0, "#64748B", "Hanger clip on an M5 rivet nut", (1200, -PY + 26, zr(-PY) - 25 - 25)),
               _win("mistline", b0, COL["line"], "Mist line, tee and nozzle", (1050, -yl, zf - 28))],
           "mist line clip and nozzle (front run)", "Seen from inside. The line runs 70 mm inboard of the beam and 35 mm below it; nozzles point down",
           elev=12, azim=120)
    if want(10):
        ey = P["enc_y"]
        b0 = (PX - 50, PX + 240, ey - 180, PY + 60, 1380, 1880)
        jt(10, [_win("post_rr", b0, COL["post"], "Post (rear right)", (PX + 20, PY - 40, 1870)),
                _win("enc_rails", b0, COL["encr"], "Enclosure rail, 40 x 6 flat bar (2)", (PX + 43, ey - 168, 1540)),
                _win("enclosure", (PX + 46, PX + 203, ey - 160, ey + 160, 1380, 1880), COL["enc"], "Enclosure, door side cut away", (PX + 140, ey + 158, 1500)),
                _win("battery", b0, COL["battery"], "Battery on the floor", (PX + 120, ey - 40, 1612)),
                _win("mppt", b0, COL["mppt"], "MPPT charge controller", (PX + 96, ey - 60, 1750)),
                _win("board", b0, "#0F766E", "Controller board", (PX + 76, ey + 60, 1745)),
                _win("harness", b0, COL["harness"], "Cable bundle from inside the post to a gland", (PX + 120, PY - 13, 1400))],
            "enclosure on its rails (rear right post)", "Rails bolt through the post with flush countersunk heads; the box screws to the rails from inside",
            elev=14, azim=-40)
    if want(11):
        b0 = (PX - 60, PX + 360, -PY - 120, -PY + 50, 2240, 2470)
        jt(11, [_win("post_fr", b0, COL["post"], "Post (front right)", (PX + 20, -PY - 40, 2300)),
                _win("arm", b0, COL["arm"], "Sensor arm, 40 x 40 x 4 angle", (PX + 200, -PY - 44, 2400)),
                _win("arm_bolts", b0, COL["bolt"], "M8 bolts: two through the post, one into the shield", (PX - 15, -PY - 49, 2398)),
                _win("shield", b0, "#D6D3D1", "Radiation shield with the sensor", (PX + 290, -PY - 124, 2330)),
                _win("harness", b0, COL["harness"], "Sensor cable into the post", (PX + 100, -PY - 75, 2424))],
            "sensor arm and shield (front right post)", "Seen from the street. The shield hangs outside the roof, its lowest plate 2,266 mm up",
            elev=8, azim=-80)
    if want(12):
        b0 = (-1560, -1180, 900, 1230, 900, 1420)
        jt(12, [_win("post_rl", b0, COL["post"], "Post (rear left)", (-1425, 1135, 1400)),
                _win("eq_plate", b0, COL["eqp"], "Equipment plate, 3 mm", (-1515, 1132, 1360)),
                _win("pump", b0, COL["pump"], "Pump", (-1300, 1002, 1280)),
                _win("filter", b0, COL["filter"], "Filter", (-1270, 1045, 960)),
                _win("drain", b0, COL["drain"], "Drain valve, normally open", (-1500, 1072, 1040)),
                _win("mistline", b0, COL["line"], "Down pipe, with the tee to the pump", (-1475, 1105, 1160)),
                _win("harness", b0, COL["harness"], "Hoses and pump cable", (-1290, 1087, 1150))],
            "equipment plate (rear left post)", "Seen from inside the canopy. The down pipe ends in the valve; a tee takes the pump outlet into it",
            elev=12, azim=-100)
    if want(13):
        b0 = (-1500, -720, 480, 1240, -10, 760)
        jt(13, [_win("post_rl", b0, COL["post"], "Post (rear left)", (-1400, 1135, 650)),
                _win(["plate_rl", "bcleat_rl"], b0, COL["plate"], "Post base", (-1490, 1070, 12)),
                _win("tank", b0, COL["tank"], "Tank, 120 L", (-1050, 551, 620)),
                _win("strap", b0, COL["strap"], "Ratchet strap round tank and post", (-1000, 549, 430)),
                _win(["stops", "stop_bolts"], b0, COL["stops"], "Stop cleats with M10 anchors (2)", (-1215, 585, 45))],
            "tank strap and stop cleats", "The strap pulls the tank against the post; the two stop cleats stop it sliding away",
            elev=25, azim=-75)
    return out


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="CoolShade", date=DATE)
    out = []
    th = D["slope_deg"]
    PX, PY = P["post_x"], P["post_y"]
    zr = D["zr"]
    G = "#9CA3AF"

    def nb(*keys, win=None):
        sh = _fuse([C()[k].shape for k in keys])
        if win is not None:
            sh = sh & bx(*win)
        return [Part("n", sh, G)]

    def sheet(n, *a, **kw):
        if only is not None and n != only:
            return
        out.append(bv.component_sheet(*a, dwg_no=f"CSH-DWG-{n}", **kw, **base))

    def at0(k):
        bb = C()[k].shape.bounding_box()
        return b.Pos(-bb.center().X, -bb.center().Y, -bb.min.Z) * C()[k].shape

    # 101 base plate
    sheet(101, Part("Base plate", C()["plate_fr"].shape, COL["plate"]), nb("post_fr", "bcleat_fr", win=(0, 3000, -3000, 0, -10, 450)),
          title="CoolShade base plate (make 4): making sketch", material="Steel plate 10 mm, hot-dip galvanized after drilling",
          view_shape=at0("plate_fr"), inset_view=(30, -55),
          notes=["Make four. Cut 220 x 220 mm from 10 mm plate; square; deburr.",
                 "Four 18 mm holes on a 160 mm square: 30 mm in from each edge.",
                 "Galvanize after drilling, or touch up with zinc-rich paint.",
                 "Fit: lies on the slab; the post stands on its centre between two",
                 "  base cleats; the four M16 anchors pass through cleat and plate.",
                 "Use the drilled plate as the template for the slab holes.",
                 "Check: the plate sits flat on the slab without rocking; pack with",
                 "  steel shims or bedding grout if the slab is out of level."])
    # 102 base cleat
    sheet(102, Part("Base cleat", C()["bcleat_fr"].shape, COL["bcleat"]), nb("post_fr", "plate_fr", "anchors", win=(1200, 1600, -1400, -950, -10, 450)),
          title="CoolShade base cleat (make 8): making sketch", material="Galvanized equal angle 75 x 75 x 6 mm",
          view_shape=b.Pos(-(PX + 40 + 37.5), PY, -10) * (C()["bcleat_fr"].shape & bx(PX + 30, PX + 200, -PY - 200, -PY + 200, -10, 200)),
          inset_view=(28, -55),
          notes=["Make eight. Cut 220 mm lengths of 75 x 75 x 6 angle; deburr.",
                 "Upright leg: two 13 mm holes on the middle of the length (110 mm),",
                 "  35 and 62 mm above the underside of the flat leg.",
                 "Flat leg: two 18 mm holes 40 mm out from the back of the upright",
                 "  leg, 30 mm in from each end (160 mm apart).",
                 "Drill a pair together, clamped back to back, so the holes match.",
                 "Fit: one cleat each side of the post, upright legs flat on the",
                 "  post's left and right faces (as seen from the street),",
                 "  flat legs on the base plate. Two M12 bolts through cleat, post",
                 "  and cleat; the anchors go through the flat legs and the plate.",
                 "Check: with both cleats on, the four flat-leg holes line up with",
                 "  the plate's holes and the post's holes with the upright legs."])
    # 103 front post, 104 rear post
    for n, k, other, nm, Lp, extra in (
            (103, "post_fr", "fl", "front", D["post_len_front"],
             ["Front right only: two 9 mm holes through the street face and back",
              "  face, 15 mm each side of centre, 2,388 mm up (sensor arm); and a",
              "  12 mm cable hole in the street face, 30 mm toward the outer side,",
              "  2,435 mm up. Fit a grommet."]),
            (104, "post_rr", "rl", "rear", D["post_len_rear"],
             ["Rear right only: four 11 mm holes through both side faces, 25 mm",
              "  each side of centre, 1,510 and 1,770 mm up (enclosure rails),",
              "  countersunk on the outer face; a 12 mm cable hole in the outer",
              "  face, 13 mm toward the street, 1,390 mm up.",
              "Rear left only: two 11 mm holes through the street face and back",
              "  face on the centre line, 780 and 1,340 mm up (equipment plate);",
              "  a 12 mm cable hole in the street face, 25 mm toward the canopy,",
              "  1,330 mm up."])):
        sheet(n, Part("Post", C()[k].shape, COL["post"]), nb(f"plate_{k[5:]}", f"bcleat_{k[5:]}", f"beam_{k[5]}", f"brace_{k[5:]}"),
              title=f"CoolShade {nm} post (make 2, a left and a right): making sketch",
              material="Galvanized steel SHS 80 x 80 x 3 mm", view_shape=at0(k), inset_view=(20, -55),
              notes=[f"Make two {nm} posts, {Lp:,.0f} mm long; cut both ends square.",
                     "All holes go through both walls, on the face's centre line",
                     "  unless stated. Heights from the bottom end.",
                     "Left and right faces: 13 mm at 35 and 62 mm up (base",
                     "  cleats); 11 mm at 28 mm below the top (head cleats); 11 mm at",
                     "  372.5 mm below the top (knee brace).",
                     ] + extra + [
                     "Deburr every hole; zinc-rich paint on cut ends and holes.",
                     "Hole positions: figure post-holes in the build plan.",
                     "Check: holes in opposite faces line up (a rod passes square)."])
    # 105 head cleat
    hc = C()["hcleat_fr"].shape & bx(PX + 30, PX + 120, -PY - 60, -PY + 60, 0, 4000)
    zt = zr(-PY) - 25
    sheet(105, Part("Head cleat", C()["hcleat_fr"].shape, COL["hcleat"]), nb("post_fr", "beam_f", win=(1200, 1600, -1300, -1050, 2400, 3100)),
          title="CoolShade head cleat (make 8): making sketch", material="Galvanized equal angle 50 x 50 x 5 mm",
          view_shape=b.Pos(-(PX + 65), PY, -zt) * hc, inset_view=(-20, -60),
          notes=["Make eight. Cut 46 mm lengths of 50 x 50 x 5 angle; deburr.",
                 "Upright leg (goes on the post): one 11 mm hole on the middle of",
                 "  the length, 28 mm below the top face of the flat leg.",
                 "Flat leg (goes under the beam): one 9 mm hole on the middle of the",
                 "  length, 27.5 mm out from the back of the upright leg.",
                 "Fit: one cleat on each side face of the post top, the flat leg's",
                 "  top face flush with the post's square-cut top, pointing away",
                 "  from the post. One M10 bolt through both cleats and the post;",
                 "  one M8 bolt up through each flat leg into a rivet nut in the",
                 "  beam's underside.",
                 "Check: a straight edge across the post top touches both cleats."])
    # 106 knee brace
    br = C()["brace_fr"].shape
    sheet(106, Part("Knee brace", br, COL["brace"]), nb("post_fr", "beam_f"),
          title="CoolShade knee brace (make 4): making sketch", material="Galvanized steel tube 32 mm OD x 2.5 mm",
          view_shape=b.Pos(-(PX - 40), PY, -(zr(-PY) - 25)) * br, inset_view=(18, -120),
          notes=["Make four. Cut 581 mm lengths of 32 mm tube.",
                 "Squash the last 75 mm of each end flat in a vice (about 50 mm",
                 "  wide, 5 mm thick), both ends flat in the same plane.",
                 "Bend each flat end 45 degrees, 45 mm from the end, the two ends",
                 "  bent opposite ways so they end up square to each other.",
                 "  The bend points are 491 mm apart.",
                 "Lower end: one 11 mm hole, 22 mm from the end, on the centre line.",
                 "Upper end: one 9 mm hole, 22 mm from the end, on the centre line.",
                 "Zinc-rich paint where the galvanizing cracked in the vice.",
                 "Fit: lower end flat on the post's inner side face, its bend 350 mm",
                 "  below the beam (M10 through the post); upper end flat under the",
                 "  beam, its bend 350 mm in from the post (M8 into a rivet nut).",
                 "Check: lying on the post and beam, both flat ends sit flat."])
    # 107 long beam
    sheet(107, Part("Long beam", C()["beam_r"].shape, COL["beam"]), nb("post_rr", "post_rl", "endb_r", "endb_l", "purlin_r", "purlin_l"),
          title="CoolShade long beam (make 2: front and rear): making sketch", material="Galvanized steel SHS 50 x 50 x 2 mm",
          view_shape=b.Pos(0, -PY, -(zr(PY) - 25)) * C()["beam_r"].shape, inset_view=(30, -60),
          notes=["Make two, 3,000 mm long, ends square; plastic end caps.",
                 "Positions from the left end, as seen from the street. Rivet nut",
                 "  holes are 11 mm; set an M8 steel rivet nut in each.",
                 "Underside: 32.5, 167.5, 2,832.5 and 2,967.5 (head cleats);",
                 "  512.5 and 2,487.5 (knee braces); all on the centre line.",
                 "Inner face: 75 and 2,925 (end beam cleats), 1,015 and 1,985",
                 "  (purlin cleats); 26 mm below the top on the front beam, 23.5",
                 "  (end) and 18.5 (purlin) below the top on the rear beam.",
                 "Cable holes 12 mm with grommets: underside 125 and 2,875 (13 mm",
                 "  toward the canopy); inner face 2,975, 20 (front) or 16 (rear) below top.",
                 "Rear beam: top face 1,195 and 1,805 (L-feet), 1,920 (panel cable).",
                 "Front beam: underside 1,535 (PIR cable); two M5 rivet nuts at 1,485",
                 "  and 1,515 (PIR bracket). Both: six M5 rivet nuts on the inner",
                 "  face for the line clips, at 300, 800, 1,300, 1,700, 2,200, 2,700."])
    # 108 end beam, 109 purlin (laid flat)
    for n, k, nm, mat, extra in (
            (108, "endb_r", "end beam", "Galvanized steel SHS 50 x 50 x 2 mm",
             ["Inboard face: one 11 mm rivet nut hole 25 mm from each end, 20 mm",
              "  (front end) and 30 mm (rear end) below the top face.",
              "Underside: three M5 rivet nuts for the line clips, at 353, 1,159",
              "  and 1,965 mm from the front end, on the centre line."]),
            (109, "purlin_r", "purlin", "Galvanized steel SHS 40 x 40 x 2 mm",
             ["Inboard face: one 11 mm rivet nut hole 25 mm from each end, 20 mm",
              "  (front end) and 25 mm (rear end) below the top face; one more",
              "  1,673 mm from the front end, 25 mm below the top (bearer)."])):
        bb = C()[k].shape.bounding_box()
        flat = b.Rot(th, 0, 0) * b.Pos(-bb.center().X, 0, -D["zr"](0)) * C()[k].shape
        sheet(n, Part(nm.capitalize(), C()[k].shape, COL["endb" if n == 108 else "purlin"]), nb("beam_f", "beam_r", "frame_cleats"),
              title=f"CoolShade {nm} (make 2): making sketch, drawn laid flat", material=mat, view_shape=flat, inset_view=(30, -60),
              notes=[f"Make two, {D['end_beam_len']:,.0f} mm long on the centre line ({D['end_beam_len'] + 6:,.0f} overall).",
                     "Cut each end 7 degrees off square, the two cuts parallel (the",
                     "  tube is a long parallelogram seen from the side): fitted, both",
                     "  ends stand upright against the long beams' inner faces.",
                     ] + extra + [
                     "Fit: between the long beams, ends against their inner faces,",
                     "  tops of end beams and purlins level; one cleat at each end.",
                     "Check: laid between two straight edges 2,300 mm apart, both end",
                     "  faces touch them fully."])
    # 110 bearer
    sheet(110, Part("Panel bearer", C()["bearer"].shape, COL["bearer"]), nb("purlin_r", "purlin_l", "feet", "rails"),
          title="CoolShade panel bearer: making sketch", material="Galvanized steel SHS 50 x 50 x 2 mm",
          view_shape=b.Pos(0, -P["bearer_y"], -(zr(P["bearer_y"]) - 25)) * C()["bearer"].shape, inset_view=(30, -55),
          notes=[f"Make one, {D['bearer_len']:,.0f} mm long, ends square.",
                 "Front face: one 11 mm rivet nut hole 25 mm from each end, 18.5 mm",
                 "  below the top face (cleats).",
                 "Top face: two 11 mm rivet nut holes 205 and 815 mm from the left",
                 "  end, on the centre line (L-feet).",
                 "Fit: square across between the purlins' inner faces, its front",
                 "  face 1,685 mm behind the front beam's inner face (plan), level.",
                 "  The cloth's notch edge laces round it.",
                 "Check: it drops between the purlins with no more than 1 mm gap."])
    # 111 frame cleat
    fc = C()["frame_cleats"].shape & bx(1390, 1460, 1090, 1160, 0, 4000)
    bbf = fc.bounding_box()
    sheet(111, Part("Frame cleat", fc, COL["fcleat"]), nb("beam_r", "endb_r", win=(1100, 1600, 800, 1300, 2400, 2900)),
          title="CoolShade frame cleat (make 10): making sketch", material="Galvanized equal angle 50 x 50 x 5 mm",
          view_shape=b.Pos(-bbf.center().X, -bbf.center().Y, -bbf.min.Z) * fc, inset_view=(35, -60),
          notes=["Make ten from 50 x 50 x 5 angle: four 40 mm long (end beams) and",
                 "  six 30 mm long (four for the purlins, two for the bearer).",
                 "Each leg: one 9 mm hole on the middle of the length, 25 mm out",
                 "  from the back of the other leg.",
                 "Fit: one leg flat on the face of one tube, the other leg flat on",
                 "  the face of the tube it meets; one M8 bolt through each leg into",
                 "  a rivet nut in that tube. Drawn: rear right end beam corner.",
                 "Check: both legs sit flat on their faces with the bolts in."])
    # 112 sensor arm
    arm = C()["arm"].shape
    sheet(112, Part("Sensor arm", arm, COL["arm"]), nb("post_fr", "shield"),
          title="CoolShade sensor arm: making sketch", material="Galvanized equal angle 40 x 40 x 4 mm",
          view_shape=b.Pos(-(PX - 35), PY + 40, -(P["shield_z"] - 20)) * arm, inset_view=(15, -70),
          notes=["Make one. Cut 375 mm of 40 x 40 x 4 angle; deburr.",
                 "Upright leg: two 9 mm holes 20 and 50 mm from the post end,",
                 "  22 mm below the top face.",
                 "Flat leg: one 9 mm hole 325 mm from the post end, 24 mm out from",
                 "  the back of the upright leg (the shield's bolt).",
                 "Fit: upright leg flat on the street face of the front right post,",
                 "  flat leg on top pointing to the street, top 2,420 mm up, 75 mm",
                 "  of arm on the post face and 300 mm beyond its outer face. Two M8",
                 "  bolts through the post; the shield hangs under the arm's end.",
                 "Check: the arm is level and the shield's lowest plate is 2,266 mm",
                 "  or more above the pavement."])
    # 113 enclosure rail
    er = C()["enc_rails"].shape & bx(0, 4000, 0, 4000, 1400, 1600)
    sheet(113, Part("Enclosure rail", C()["enc_rails"].shape, COL["encr"]), nb("post_rr", "enclosure", win=(1300, 1700, 800, 1400, 1200, 2000)),
          title="CoolShade enclosure rail (make 2): making sketch", material="Galvanized steel flat bar 40 x 6 mm",
          view_shape=b.Pos(-(PX + 43), -P["enc_y"], -1500) * er, inset_view=(18, -35),
          notes=["Make two. Cut 340 mm of 40 x 6 flat bar; round the corners.",
                 "Positions from the street end, on the centre line of the 40 mm",
                 "  face:",
                 "  two 11 mm holes at 230 and 280 mm, countersunk on the outer",
                 "  face for M10 countersunk bolts (through the post);",
                 "  two 5 mm holes at 40 and 300 mm, tapped M6 (enclosure screws).",
                 "Fit: flat on the outer side face of the rear right post, level,",
                 "  centred 1,520 and 1,780 mm up; the bolts' heads must sit flush",
                 "  so the enclosure's back lies flat on both rails.",
                 "Check: a straight edge across both rails touches all along."])
    # 114 equipment plate
    sheet(114, Part("Equipment plate", C()["eq_plate"].shape, COL["eqp"]), nb("post_rl", "pump", "filter", "drain", win=(-1700, -1000, 800, 1400, 500, 1600)),
          title="CoolShade equipment plate: making sketch", material="Galvanized steel sheet 3 mm",
          view_shape=b.Pos(1370, -1133.5, -750) * C()["eq_plate"].shape, inset_view=(20, -60),
          notes=["Make one, 320 x 630 mm from 3 mm sheet; round the corners.",
                 "Positions from the left edge (seen from inside the canopy) and",
                 "  from the bottom edge:",
                 "  two 11 mm holes at 130, 40 up and 130, 600 up (bolts to post);",
                 "  one 12 mm cable hole at 155, 590 up, with a grommet.",
                 "Mark and drill the pump's, filter bracket's and drain valve's",
                 "  holes from the parts: pump 90 to 290 across, 430 to 570 up;",
                 "  filter centre 240 across, bracket 1,060 to 1,100 mm above the",
                 "  pavement; valve 10 to 100 across, 250 to 320 up.",
                 "Fit: flat on the street face of the rear left post, bottom edge",
                 "  750 mm up, 90 mm of plate beyond the post's outer face.",
                 "Check: plumb, and the drain valve is the lowest part of the line."])
    # 115 tank stop cleat
    st_ = C()["stops"].shape & bx(-2000, -1050, 0, 900, -1, 100)
    bbs = st_.bounding_box()
    sheet(115, Part("Tank stop cleat", C()["stops"].shape, COL["stops"]), nb("tank", "post_rl", "strap", win=(-1600, -600, 400, 1300, -10, 800)),
          title="CoolShade tank stop cleat (make 2): making sketch", material="Galvanized equal angle 50 x 50 x 5 mm",
          view_shape=b.Rot(0, 0, -235) * b.Pos(-bbs.center().X, -bbs.center().Y, 0) * st_, inset_view=(30, -70),
          notes=["Make two. Cut 60 mm lengths of 50 x 50 x 5 angle; deburr.",
                 "Flat leg: one 11 mm hole on the middle, 32 mm out from the back of",
                 "  the upright leg.",
                 "Fit: on the slab, upright leg touching the tank at its foot, on",
                 "  the canopy side of the tank, the two cleats 70 degrees apart",
                 "  round the tank. One M10 anchor each.",
                 "Check: the tank cannot slide toward the canopy centre."])
    # 116 shade fabric
    fab = C()["fabric"].shape
    flat = b.Rot(th, 0, 0) * b.Pos(0, 0, -D["zr"](0)) * fab
    sheet(116, Part("Shade fabric", fab, COL["fabric"]), nb("beam_f", "beam_r", "endb_r", "endb_l", "purlin_r", "purlin_l", "bearer", "panel"),
          title="CoolShade shade fabric: outline for the maker, drawn laid flat", material="Knitted HDPE shade cloth, about 90 % UV block",
          view_shape=flat, inset_view=(35, -60),
          notes=["Order made to size: 3,000 mm wide (along the curb) by 2,419 mm",
                 "  (down the slope), with a 1,020 x 670 mm notch at the middle of",
                 "  the rear edge for the solar panel.",
                 "Reinforced hem all round, including the notch; brass or stainless",
                 "  eyelets about every 300 mm and at every corner.",
                 "Fit: over the frame; lace each eyelet round the beam below it",
                 "  with cord. The notch's sides lace round the purlins, its front",
                 "  edge round the panel bearer; the panel covers the notch.",
                 "Fit only when forecast gusts are below 15 m/s; take it off before",
                 "  storms (15 minutes or less by unlacing).",
                 "Check: laid on the frame, the hem reaches every edge and the",
                 "  notch clears the L-feet and rails."])
    return out


# ----------------------------------------------------------------- slab layout, wiring, water
def _fig(w, h):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(w, h), dpi=150)
    return plt, fig


INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"


def _foot(fig):
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN)
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/coolshade", fontsize=7, color=AC, ha="right", family="monospace")


def layouts():
    from matplotlib.patches import Rectangle, Circle
    plt, fig = _fig(11, 8.6)
    ax = fig.add_axes([0.04, 0.07, 0.68, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    PX, PY = P["post_x"], P["post_y"]
    L, Dp = P["roof_l"], P["roof_d"]
    ax.add_patch(Rectangle((-L / 2, -Dp / 2), L, Dp, fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(L / 2 - 30, -Dp / 2 + 60, "roof outline above, 3,000 x 2,400", fontsize=7.5, color=MUT, va="bottom", ha="right")
    ax.plot([-L / 2 - 250, L / 2 + 250], [-Dp / 2 - 260, -Dp / 2 - 260], color=INK, lw=2.2)
    ax.text(0, -Dp / 2 - 300, "STREET SIDE (curb this way)", fontsize=8, color=INK, ha="center", va="top", fontweight="bold")
    ap = P["anchor_pitch"] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * PX, sy * PY
            ax.add_patch(Rectangle((cx - 110, cy - 110), 220, 220, fc="#FDE68A", ec=INK, lw=0.9))
            ax.add_patch(Rectangle((cx - 40, cy - 40), 80, 80, fc="#CBD5E1", ec=INK, lw=0.7))
            for dx in (-ap, ap):
                for dy in (-ap, ap):
                    ax.add_patch(Circle((cx + dx, cy + dy), 22, fc="white", ec=INK, lw=0.8))
            ax.plot([cx - 150, cx + 150], [cy, cy], color=MUT, lw=0.4); ax.plot([cx, cx], [cy - 150, cy + 150], color=MUT, lw=0.4)
    tx, ty = P["tank_xy"]
    ax.add_patch(Circle((tx, ty), P["tank_d"] / 2, fc="none", ec="#A16207", lw=1.0, ls="--"))
    ax.text(tx, ty, "tank\n540 dia.", fontsize=7.5, color="#A16207", ha="center", va="center")
    for adeg in (235, 305):
        a = math.radians(adeg)
        x, y = tx + (P["tank_d"] / 2 + 32) * math.cos(a), ty + (P["tank_d"] / 2 + 32) * math.sin(a)
        ax.add_patch(Circle((x, y), 22, fc="white", ec="#A16207", lw=0.9))
    ax.text(tx + 330, ty - 330, "M10 anchors for the\ntank stop cleats", fontsize=7.5, color="#A16207", va="top")

    def dim(x0, y0, x1, y1, text, off, vertical=False):
        if vertical:
            ax.annotate("", xy=(x0 + off, y0), xytext=(x0 + off, y1), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.8))
            ax.text(x0 + off - 40, (y0 + y1) / 2, text, rotation=90, ha="right", va="center", fontsize=8, color=AC)
        else:
            ax.annotate("", xy=(x0, y0 + off), xytext=(x1, y0 + off), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.8))
            ax.text((x0 + x1) / 2, y0 + off + 40, text, ha="center", va="bottom", fontsize=8, color=AC)
    dim(-PX, PY, PX, PY, f"{2 * PX:,.0f} between post centres", 330)
    dim(-PX, -PY, -PX, PY, f"{2 * PY:,.0f} between post centres", -380, vertical=True)
    ax.plot([-PX, PX], [-PY, PY], color=AC, lw=0.5, ls=":"); ax.plot([-PX, PX], [PY, -PY], color=AC, lw=0.5, ls=":")
    diag = math.hypot(2 * PX, 2 * PY)
    ax.text(250, 120, f"both diagonals {diag:,.0f}", fontsize=8, color=AC, rotation=math.degrees(math.atan2(2 * PY, 2 * PX)), ha="center")
    for (sx, sy, nm) in ((1, -1, "front right"), (-1, -1, "front left"), (1, 1, "rear right"), (-1, 1, "rear left")):
        ax.text(sx * PX, sy * PY + sy * 190, nm, fontsize=8, ha="center", va="center", color=INK)
    ax.set_xlim(-L / 2 - 650, L / 2 + 300); ax.set_ylim(-Dp / 2 - 450, Dp / 2 + 520)
    fig.text(0.03, 0.965, "Slab layout: post centres, base plates and anchors", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Plan view from above, street at the bottom. Sizes in mm.", fontsize=8.5, color=MUT, va="top")
    key = ["Base plate 220 x 220 (yellow),", "  post 80 x 80 (grey)",
           "Anchor holes: four per post on a 160 mm square,",
           "  M16, drilled through the plate into the slab;",
           "  depth and edge distance from the anchor maker",
           "Set out the four post centres, then check both",
           "  diagonals are equal within 5 mm before drilling",
           "Keep every anchor at least the anchor maker's",
           "  edge distance from the slab's edge and joints",
           "The slab and anchors must be checked for each",
           "  site (about 2.8 kN factored per anchor with",
           "  the fabric off at 30 m/s; CSH-CAL-001)"]
    fig.text(0.73, 0.86, "How to set out", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.73, 0.83 - i * 0.03, t, fontsize=8, color=INK, va="top")
    _foot(fig)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "slab-layout.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def _blocks(ax):
    from matplotlib.patches import FancyBboxPatch
    B = {}

    def blk(key, x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.4, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)
        B[key] = (x, y, w, h)
    return blk


def _wire(ax, pts, color, lw=2.0):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)


def _lab(ax, x, y, text, color, ha="left"):
    ax.text(x, y, text, fontsize=7.2, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


def wiring():
    from matplotlib.patches import FancyBboxPatch
    plt, fig = _fig(12, 7.4)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 74); ax.set_axis_off()
    ax.text(2, 72, "CoolShade prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 68.6, "12 V DC only. Bought modules wired at block level; no circuit board is laid out. Stranded copper; ferrules on every screw terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.add_patch(FancyBboxPatch((24, 13), 70, 48, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(25.5, 59.8, "Inside the enclosure on the rear right post", fontsize=8, color=MUT, va="top")
    blk = _blocks(ax)
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    blk("panel", 3, 46, 16, 12, "Solar panel", "100 W, about 18 V,\non the roof", "#1E3A8A")
    blk("mppt", 28, 46, 16, 12, "MPPT controller", "10 A, LiFePO4\nprofile", "#16A34A")
    blk("batt", 28, 20, 16, 13, "Battery", "12.8 V 25 Ah LiFePO4\nwith BMS and cold-\ncharge cutoff", "#C2410C")
    blk("fuse", 52, 20, 14, 13, "Fuse block", "blade fuses:\npump 7.5 A, valve\n2 A, controller 1 A", "#7C3AED")
    blk("ctrl", 52, 40, 22, 18, "Controller board", "microcontroller,\nMOSFET pump driver,\nvalve driver,\nI2C bus extender", "#0F766E")
    blk("sens", 101, 50, 17, 10, "T and RH sensor", "in the shield, front\nright post, about 7 m", BLU)
    blk("pir", 101, 37, 17, 10, "PIR sensor", "under the front\nbeam, about 6 m", BLU)
    blk("float", 101, 24, 17, 10, "Tank level switch", "float in the tank,\nabout 9 m", BLU)
    blk("pump", 101, 4, 17, 13, "Pump and valve", "pump 60 W, 4.7 A;\ndrain valve, normally\nopen, 5 W", RED)
    _wire(ax, [(19, 52), (28, 52)], RED); _lab(ax, 23.5, 49.5, "2.5 mm²", RED, "center")
    _wire(ax, [(36, 46), (36, 33)], RED); _lab(ax, 36.6, 40, "4 mm²,\n15 A fuse at\nthe battery", RED)
    _wire(ax, [(44, 26), (52, 26)], RED); _lab(ax, 48, 28.5, "4 mm²", RED, "center")
    _wire(ax, [(59, 33), (59, 40)], RED); _lab(ax, 58.4, 36.5, "0.75 mm²", RED, "right")
    _wire(ax, [(66, 22), (96, 22), (96, 12), (101, 12)], RED); _lab(ax, 67, 19.6, "pump 2.5 mm², valve 0.75 mm² (via the drivers)", RED)
    _wire(ax, [(74, 55), (101, 55)], BLU); _lab(ax, 76, 57.2, "4-core 0.5 mm² screened, I2C extended", BLU)
    _wire(ax, [(74, 45), (101, 42)], BLU); _lab(ax, 78, 46.4, "3-core 0.5 mm²", BLU)
    _wire(ax, [(70, 40), (70, 29), (101, 29)], BLU); _lab(ax, 76, 30.8, "2-core 0.5 mm²", BLU)
    _wire(ax, [(63, 40), (63, 33)], GRY, 1.2); _lab(ax, 63.6, 36.5, "gates", GRY)
    ax.text(25, 10.2, "Cables run inside the posts and beams (build plan section 4, step 16); a grommet at every hole; three glands under the box.",
            fontsize=7.6, color=MUT)
    ax.text(25, 7.0, "Safety: battery fuse out and battery disconnected until the stop points in section 6 of the plan are passed.",
            fontsize=7.6, color=WARN, fontweight="bold")
    ax.text(25, 4.0, "Red: power. Blue: sensors. Grey: driver control. All circuits 12.8 V nominal, under 22 V from the panel.", fontsize=7.2, color=MUT)
    _foot(fig)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def water():
    plt, fig = _fig(12, 6.4)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 64); ax.set_axis_off()
    ax.text(2, 62, "CoolShade prototype: water circuit", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 58.6, "Potable water only. Arrows show the flow while misting; after every session the drain valve opens and the line empties through it.",
            fontsize=8.5, color=MUT, va="top")
    blk = _blocks(ax)
    W, DR = "#0EA5E9", "#DC2626"
    blk("tank", 3, 18, 15, 14, "Tank, 120 L", "opaque, locked lid,\nbottom outlet, level\nswitch, strapped", "#D4A017")
    blk("filt", 25, 18, 15, 14, "Filter, 5 um", "clear housing,\nstrainer and check\nvalve", W)
    blk("pump", 47, 18, 15, 14, "Pump, 7 bar", "12 V diaphragm with\npressure switch, on\nthe equipment plate", "#2563EB")
    blk("loop", 73, 38, 30, 14, "Mist line loop under the roof", "about 12 m, 6.5 mm bore; 4 nozzles\nunder the front run, 4 under the rear", "#111827")
    blk("vb", 106, 38, 12, 14, "Vacuum\nbreaker", "\non the front\nrun, the loop's\nhigh point", DR)
    blk("valve", 73, 6, 18, 12, "Drain valve", "normally open; at the\nbottom of the down pipe", DR)
    _wire(ax, [(18, 25), (25, 25)], W); ax.annotate("", xy=(25, 25), xytext=(21, 25), arrowprops=dict(arrowstyle="-|>", color=W))
    _lab(ax, 21.5, 27.5, "hose", W, "center")
    _wire(ax, [(40, 25), (47, 25)], W); ax.annotate("", xy=(47, 25), xytext=(43, 25), arrowprops=dict(arrowstyle="-|>", color=W))
    _wire(ax, [(62, 25), (68, 25)], W); ax.annotate("", xy=(68, 25), xytext=(64, 25), arrowprops=dict(arrowstyle="-|>", color=W))
    _wire(ax, [(68, 18), (68, 45), (73, 45)], "#111827", 2.4)
    ax.annotate("", xy=(68, 40), xytext=(68, 33), arrowprops=dict(arrowstyle="-|>", color="#111827"))
    _lab(ax, 66, 40, "down pipe\n(tee at the\npump outlet)", "#111827", "right")
    _wire(ax, [(68, 18), (73, 12)], DR, 2.0)
    _wire(ax, [(103, 45), (106, 45)], "#111827", 2.0)
    _wire(ax, [(82, 6), (82, 2.5)], DR, 1.6); _lab(ax, 83, 3.4, "to the slab drain", DR)
    for i, x in enumerate((76, 82, 88, 94)):
        ax.plot([x, x], [38, 35], color="#111827", lw=1.2); ax.text(x, 34.5, "v", ha="center", va="top", fontsize=7, color=W)
    ax.text(74, 32, "8 nozzles, 0.4 mm, anti-drip", fontsize=7.2, color=MUT)
    ax.text(3, 13.5, "Daily: drain the tank's residual and refill about 95 L. Weekly: disinfect.\nWater no more than 24 h old; the line drains in about 30 s after every session.",
            fontsize=7.6, color=MUT, va="top")
    ax.text(3, 6.5, "Safety: the line runs at about 7 bar. Depressurize before opening any fitting.", fontsize=7.6, color=WARN, fontweight="bold")
    _foot(fig)
    out = OUT / "water.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def _stagger(vals, min_gap):
    """Assign each sorted value a label level so that labels on one level are min_gap apart."""
    last = []
    lev = {}
    for v in sorted(vals):
        for i, l in enumerate(last):
            if v - l >= min_gap:
                last[i] = v; lev[v] = i; break
        else:
            last.append(v); lev[v] = len(last) - 1
    return lev


def holes():
    """Hole position charts for the posts and the long beams (from the same numbers as the model)."""
    from matplotlib.patches import Rectangle
    res = []
    # ---- posts
    Lf, Lr = D["post_len_front"], D["post_len_rear"]
    common = lambda L_: [(35, "13, L+R"), (62, "13, L+R"), (L_ - 372.5, "11, L+R (brace)"), (L_ - 28, "11, L+R (head cleats)")]
    posts = [("Front right", Lf, common(Lf) + [(2388, "9 x 2, S+B, 15 each side (arm)"), (2435, "12 cable, S face, 30 to outer side")]),
             ("Front left", Lf, common(Lf)),
             ("Rear right", Lr, common(Lr) + [(1390, "12 cable, outer face, 13 to street"), (1510, "11 x 2, L+R, 25 each side, csk outer"),
                                             (1770, "11 x 2, L+R, 25 each side, csk outer")]),
             ("Rear left", Lr, common(Lr) + [(780, "11, S+B (equipment plate)"), (1330, "12 cable, S face, 25 to canopy"),
                                            (1340, "11, S+B (equipment plate)")])]
    plt, fig = _fig(13, 8.4)
    for i, (nm, L_, hs) in enumerate(posts):
        ax = fig.add_axes([0.03 + i * 0.245, 0.07, 0.23, 0.8]); ax.set_axis_off()
        ax.set_xlim(-60, 400); ax.set_ylim(-150, 3050)
        ax.add_patch(Rectangle((0, 0), 60, L_, fc="#E2E8F0", ec=INK, lw=0.9))
        ax.text(30, L_ + 60, f"{nm}\n{L_:,.0f} long", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=INK)
        lev = _stagger([h for h, _ in hs], 120)
        ys = {}
        last = -1e9
        for h, t in sorted(hs):
            y = max(h, last + 95); ys[h] = y; last = y
        for h, t in sorted(hs):
            ax.plot([0, 60], [h, h], color="#B91C1C", lw=1.2)
            ax.plot([60, 85, 100], [h, ys[h], ys[h]], color=MUT, lw=0.5)
            ax.text(104, ys[h], f"{h:,.1f}".rstrip("0").rstrip(".") + f": {t}", fontsize=6.6, color=INK, va="center")
        ax.text(30, -60, "bottom", ha="center", va="top", fontsize=7, color=MUT)
    fig.text(0.03, 0.965, "Post hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.935, "Heights in mm from the bottom end; hole size in mm. L+R: through the left and right faces (as seen from the street); S+B: through the street and back faces. "
             "On the centre line unless stated.", fontsize=8, color=MUT, va="top")
    _foot(fig)
    out = OUT / "post-holes.png"; fig.savefig(out, facecolor="white"); plt.close(fig); res.append(out)
    # ---- long beams
    plt, fig = _fig(13, 8.0)
    faces = {
        "Front beam": [("Underside", [(32.5, "11 rn"), (125, "12 cable"), (167.5, "11 rn"), (512.5, "11 rn"), (1485, "7, M5 rn"), (1515, "7, M5 rn"),
                                      (1535, "12 cable"), (2487.5, "11 rn"), (2832.5, "11 rn"), (2875, "12 cable"), (2967.5, "11 rn")]),
                       ("Inner face", [(75, "11 rn"), (300, "7, M5 rn"), (800, "7, M5 rn"), (1015, "11 rn"), (1300, "7, M5 rn"), (1700, "7, M5 rn"), (1985, "11 rn"),
                                       (2200, "7, M5 rn"), (2700, "7, M5 rn"), (2925, "11 rn"), (2975, "12 cable")])],
        "Rear beam": [("Underside", [(32.5, "11 rn"), (125, "12 cable"), (167.5, "11 rn"), (512.5, "11 rn"), (2487.5, "11 rn"), (2832.5, "11 rn"),
                                     (2875, "12 cable"), (2967.5, "11 rn")]),
                      ("Inner face", [(75, "11 rn"), (300, "7, M5 rn"), (800, "7, M5 rn"), (1015, "11 rn"), (1300, "7, M5 rn"), (1700, "7, M5 rn"), (1985, "11 rn"),
                                      (2200, "7, M5 rn"), (2700, "7, M5 rn"), (2925, "11 rn"), (2975, "12 cable")]),
                      ("Top face", [(1195, "11 rn"), (1805, "11 rn"), (1920, "12 cable")])]}
    row = 0
    for beam, fl in faces.items():
        for face, hs in fl:
            y0 = 0.74 - row * 0.145
            ax = fig.add_axes([0.03, y0, 0.94, 0.12]); ax.set_axis_off(); ax.set_xlim(-520, 3100); ax.set_ylim(-300, 80)
            ax.add_patch(Rectangle((0, 0), 3000, 50, fc="#E2E8F0", ec=INK, lw=0.8))
            ax.text(-500, 25, f"{beam}\n{face}", fontsize=7.5, color=INK, va="center", ha="left", fontweight="bold")
            lev = _stagger([h for h, _ in hs], 260)
            for h, t in hs:
                ax.plot([h, h], [0, 50], color="#B91C1C", lw=1.2)
                yl = -30 - 85 * lev[h]
                ax.plot([h, h], [0, yl + 15], color=MUT, lw=0.4)
                ax.text(h, yl, f"{h:,.1f}".rstrip("0").rstrip(".") + f"\n{t}", fontsize=6.3, color=INK, ha="center", va="top", linespacing=1.0)
            row += 1
    fig.text(0.03, 0.97, "Long beam hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.935, "From the left end as seen from the street, in mm. rn: hole for a steel rivet nut, 11 mm for M8 and 7 mm for M5 (check the rivet nut maker).\n"
             "Heights on the inner face, below the top: front beam 26; rear beam 23.5 (end beam cleats) and 18.5 (purlin cleats); cable holes 20 (front), 16 (rear).",
             fontsize=8, color=MUT, va="top")
    _foot(fig)
    out = OUT / "beam-holes.png"; fig.savefig(out, facecolor="white"); plt.close(fig); res.append(out)
    return res


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "holes", "joints", "steps", "wiring", "water"]
    for w in what:
        if ":" in w:
            kind, n = w.split(":")
            r = {"step": steps, "joint": joints, "sheet": lambda only: sheets(only)}[kind](int(n))
        else:
            r = globals()[w]()
        print(w, "->", r)
