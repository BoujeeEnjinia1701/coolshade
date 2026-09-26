"""CoolShade sizing calculations, CSH-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[G4] that the note cites. Geometry comes from cad/src/model.py (PARAMS and derived), the
parts cost from bom/bom.csv and the budget from project.yaml. First-principles estimates
for a paper proof of concept; not a structural design and not a substitute for tests.
"""
import csv
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
G = 9.81


def tag(t, text):
    print(f"[{t}] {text}")


# ------------------------------------------------------------------ assumptions
# Design day (CSH-REQ-001): 38 degC, 25 % RH, wind 1 m/s, 5 h of misting demand, 4.5 peak sun hours.
T_DAY, RH_DAY, WIND = 38.0, 25.0, 1.0
T_EDGE, RH_EDGE = 32.0, 60.0          # the humid edge of the misting window (R6 thresholds)
T_HOT = 45.0                          # hottest air in the operating range (CSH-PRB-001)
ACTIVE_H = 5.0                        # h of misting demand on the design day
DUTY = 0.5                            # 20 s on, 20 s off
N_NOZ = len(P["nozzle_x"]) * 2
Q_NOZ = 4.0                           # L/h per nozzle at 7 bar (to confirm from the maker's data)
P_BAR = 7.0
EVAP = 0.87                           # fraction of sprayed water that evaporates in the air (estimate)
FLUSH_L = 5.0                         # daily line and filter flush
FILL_L = 95.0                         # daily fill on design days (drain-and-refill routine)
HFG = 2.43e6                          # J/kg latent heat at about 30 degC
RHO_A, CP_A = 1.15, 1006.0            # air at about 35 degC
CV_H, CV_L = 2000.0, 3000.0           # cooling control volume: height and length (mm)
DV, MU = 2.6e-5, 1.9e-5               # vapor diffusivity in air (m2/s), air viscosity (Pa s)
HEAD_Z = 1500.0                       # head height for the wetting check (mm), R5
JET = 300.0                           # downward jet penetration below the nozzle tip (mm), assumption
# Energy
PUMP_W, CTRL_W, VALVE_W = 60.0, 1.2, 5.0
PANEL_W, PSH, SYS = 100.0, 4.5, 0.75
BATT_WH, DOD = 12.8 * 20, 0.80
V_BATT, VMP = 12.8, 18.0
MPPT_EFF = 0.95
# Enclosure heat, under the shade cloth
G_ENC = 200.0                         # W/m2 on the worst face: 10 % of 900 W/m2 direct through the cloth plus 100 diffuse
ALPHA_ENC, H_ENC = 0.5, 10.0          # absorptance (light grey), combined film coefficient W/m2K
Q_INT = 5.0                           # W: MPPT and driver losses at peak charge
T_CHG_MAX = 45.0                      # LiFePO4 charge limit (typical cell data)
# Wind and structure
V_GUST, RHO_W = 30.0, 1.2
CF_N = 1.2                            # net normal force coefficient, free mono-pitch canopy (conservative)
ECC = 0.25                            # center of pressure offset as a fraction of the roof depth
CFR = 0.04                            # friction coefficient, each face of the fabric
CD_SQ, CD_CYL = 2.0, 0.8              # drag coefficients: square sections, cylinders
EDGE_H = 100.0                        # roof edge band height seen by the wind (mm)
FY, GAMMA = 275.0, 1.5                # S275 yield (MPa); partial factor on wind
SAG = 0.05                            # fabric sag as a fraction of its 2.4 m span under load (assumption)
STEEL = 7850.0
M_PANEL, M_FABRIC, M_ENC_ALL, M_TANK_EMPTY, M_PUMP = 7.0, 2.0, 10.0, 8.0, 3.0   # kg
# Space
A_PERSON = 0.5                        # m2 per standing person (assumption)
WHEEL = (0.8, 1.2)                    # m, R1 wheelchair space
BENCH = (1.5, 0.42)                   # m, existing bench footprint (context)

print("CoolShade sizing, CSH-CAL-001 v0.1")
print(f"Geometry from cad/src/model.py: roof {P['roof_l']:.0f} x {P['roof_d']:.0f} mm, posts {P['post']:.0f} x {P['post_t']:.0f} SHS "
      f"on {2 * P['post_x']:.0f} x {2 * P['post_y']:.0f} mm, slope {D['slope_deg']:.2f} deg")
results = {}

# ------------------------------------------------------------------ A. Shade and space (R1)
print("\nA. Shade and space")
L, Dp = P["roof_l"] / 1000, P["roof_d"] / 1000
tag("A1", f"Roof plan {L * Dp:.2f} m2; fabric area on the slope {D['roof_true_area_m2']:.2f} m2")


def shadow(elev, azim_axis):
    """Shadow polygon of the roof on the ground for sun elevation elev (deg) arriving from -Y ('y') or -X ('x')."""
    k = 1 / math.tan(math.radians(elev))
    pts = []
    for x, y in ((-L / 2, -Dp / 2), (L / 2, -Dp / 2), (L / 2, Dp / 2), (-L / 2, Dp / 2)):
        z = D["zr"](y * 1000) / 1000
        pts.append((x, y + z * k) if azim_axis == "y" else (x + z * k, y))
    return pts


def area(poly):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]))) / 2


def clip(poly, xmin, xmax, ymin, ymax):
    def cut(pts, inside, inter):
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(inter(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(inter(prev, cur))
        return out
    def ix(a, b, x):
        t = (x - a[0]) / (b[0] - a[0]); return (x, a[1] + t * (b[1] - a[1]))
    def iy(a, b, y):
        t = (y - a[1]) / (b[1] - a[1]); return (a[0] + t * (b[0] - a[0]), y)
    for inside, inter in ((lambda p: p[0] >= xmin, lambda a, b: ix(a, b, xmin)), (lambda p: p[0] <= xmax, lambda a, b: ix(a, b, xmax)),
                          (lambda p: p[1] >= ymin, lambda a, b: iy(a, b, ymin)), (lambda p: p[1] <= ymax, lambda a, b: iy(a, b, ymax))):
        poly = cut(poly, inside, inter)
        if not poly:
            return []
    return poly


rows = []
for elev in (90, 75, 60, 45):
    for ax in ("y", "x"):
        s = shadow(elev, ax)
        rows.append((elev, ax, area(s), area(clip(s, -L / 2, L / 2, -Dp / 2, Dp / 2) or [(0, 0)] * 3)))
for elev, ax, a, ov in rows:
    tag("A2", f"Sun at {elev} deg from {'the street (-Y)' if ax == 'y' else 'along the curb (-X)'}: shadow {a:.2f} m2, of which {ov:.2f} m2 falls within the roof footprint")
shade_min = min(r[2] for r in rows)
cx, cy = D["clear_x"] / 1000, D["clear_y"] / 1000
a_clear = cx * cy
a_tank = math.pi / 4 * (P["tank_d"] / 1000) ** 2 + 0.25 * 0.35   # tank plus pump and filter nook
a_free = a_clear - a_tank - BENCH[0] * BENCH[1] - WHEEL[0] * WHEEL[1]
n_stand = int(a_free / A_PERSON)
tag("A3", f"Clear floor between posts {cx:.2f} x {cy:.2f} m = {a_clear:.2f} m2; less tank and pump {a_tank:.2f}, bench {BENCH[0] * BENCH[1]:.2f} "
    f"and wheelchair space {WHEEL[0] * WHEEL[1]:.2f} leaves {a_free:.2f} m2, room for {n_stand} standing plus 3 seated")
results["R1"] = ("Met", f"{shade_min:.1f} m2 shadow at any sun elevation of 45 deg or more; {n_stand} standing + 3 seated + wheelchair space; where the shadow falls is site-specific")

# ------------------------------------------------------------------ B. Headroom (R2)
print("\nB. Headroom")
tag("B1", f"Beam underside {D['beam_under_front']:.0f} mm (front) and {D['beam_under_rear']:.0f} mm (rear)")
tag("B2", f"Knee brace low end, at the post face: {D['brace_low_rear']:.0f} mm (rear posts), {D['brace_low_front']:.0f} mm (front posts); "
    f"brace {P['brace_drop']:.0f} mm down, {P['brace_reach']:.0f} mm along, {D['brace_len']:.0f} mm long (was 520 mm down at TRL 2, low end about 2,110 mm)")
tag("B3", f"Nozzle tips {D['nozzle_tip_rear']:.0f} mm (rear row) and {D['nozzle_tip_front']:.0f} mm (front row); sensor arm 2,300 mm, outboard of the front right post")
hmin = min(D["brace_low_rear"], D["nozzle_tip_rear"])
results["R2"] = ("Met", f"lowest point {hmin:.0f} mm (rear knee braces) against 2,200 mm")

# ------------------------------------------------------------------ C. Misting and water (R7, R15, R9)
print("\nC. Misting and water")
a_or = math.pi / 4 * (P["nozzle_orifice"] / 1000) ** 2
v_jet = math.sqrt(2 * P_BAR * 1e5 / 1000)
q_ideal = a_or * v_jet * 3.6e6                      # L/h
cd_impl = Q_NOZ / q_ideal
tag("C1", f"Ideal orifice flow, {P['nozzle_orifice']} mm at {P_BAR:.0f} bar: {q_ideal:.1f} L/h (jet {v_jet:.1f} m/s); "
    f"the assumed {Q_NOZ:.1f} L/h implies a discharge coefficient of {cd_impl:.2f}, plausible for a swirl nozzle; to confirm from the maker's data")
q_spray = Q_NOZ * N_NOZ
sprayed = q_spray * DUTY * ACTIVE_H
used = sprayed + FLUSH_L
evap = EVAP * sprayed
tag("C2", f"{N_NOZ} nozzles: {q_spray:.0f} L/h while spraying, {q_spray * DUTY:.0f} L/h averaged; sprayed {sprayed:.0f} L, used {used:.0f} L with the flush, "
    f"evaporated {evap:.1f} L per design day")
q_lim = (100 - FLUSH_L) / (N_NOZ * DUTY * ACTIVE_H)
for qn in (3.0, 4.0, 5.0):
    u = qn * N_NOZ * DUTY * ACTIVE_H + FLUSH_L
    tag("C3", f"Sensitivity: at {qn:.1f} L/h per nozzle the day uses {u:.0f} L and a full tank lasts {P['tank_nominal_l'] / u:.2f} days")
tag("C3", f"R7 (100 L per day) holds up to {q_lim:.2f} L/h per nozzle")
endur = P["tank_nominal_l"] / used
tag("C4", f"Tank {P['tank_nominal_l']:.0f} L nominal (model envelope {D['tank_gross_l']:.0f} L gross): {endur:.2f} design days per full tank")
resid = FILL_L - used
tag("C5", f"Drain-and-refill routine: fill {FILL_L:.0f} L each design day, {resid:.0f} L drained at the next visit; water drawn {FILL_L:.0f} L per day, "
    f"no water older than 24 h. Filling 120 L and draining the rest would draw 120 L per day (R7 not met)")
hyd = q_spray / 3.6e6 * P_BAR * 1e5
tag("C6", f"Pump hydraulic power {hyd:.1f} W at {q_spray:.0f} L/h and {P_BAR:.0f} bar, so the assumed {PUMP_W:.0f} W draw implies {hyd / PUMP_W * 100:.0f} % wire-to-water efficiency")
vol = D["line_vol_l"]
a_d = math.pi / 4 * 0.003 ** 2
q_d = 0.6 * a_d * math.sqrt(2 * G * 0.5)
tag("C7", f"Mist line {D['line_len_mm'] / 1000:.2f} m ({D['loop_len_mm'] / 1000:.2f} m loop + {D['riser_mm'] / 1000:.2f} m down pipe), bore {P['line_id']:.1f} mm: {vol:.2f} L; "
    f"through a 3 mm valve orifice at 0.5 m head it drains in about {vol / 1000 / q_d:.0f} s, provided air can enter (vacuum breaker)")
results["R7"] = ("Met", f"{used:.0f} L used, {FILL_L:.0f} L drawn per design day; holds to {q_lim:.2f} L/h per nozzle")
results["R15"] = ("Met", f"{endur:.2f} design days per full tank")

# ------------------------------------------------------------------ D. Droplets and wetting (R5)
print("\nD. Droplets and wetting")


def es(t):
    return 0.61094 * math.exp(17.625 * t / (t + 243.04)) * 1000      # Pa


def wet_bulb(t, rh):
    return (t * math.atan(0.151977 * (rh + 8.313659) ** 0.5) + math.atan(t + rh) - math.atan(rh - 1.676331)
            + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh) - 4.686035)


def evap_k(t, rh):
    tw = wet_bulb(t, rh)
    rv_s = es(tw) / (461.5 * (tw + 273.15))
    rv_a = rh / 100 * es(t) / (461.5 * (t + 273.15))
    return tw, rv_s - rv_a, 8 * DV * (rv_s - rv_a) / 1000.0         # m2/s, d(d^2)/dt


c_st = 1000 * G / (18 * MU)
fall_avail = (D["nozzle_tip_rear"] - JET - HEAD_Z) / 1000
for name, t, rh in (("design day", T_DAY, RH_DAY), ("humid edge", T_EDGE, RH_EDGE)):
    tw, drho, K = evap_k(t, rh)
    dmax = (2 * K * fall_avail / c_st) ** 0.25 * 1e6
    tag("D1", f"{name}, {t:.0f} degC and {rh:.0f} % RH: wet bulb {tw:.1f} degC, vapor density deficit {drho * 1000:.1f} g/m3, evaporation constant {K:.2e} m2/s")
    for d_um in (30, 50, 80, 100):
        d = d_um * 1e-6
        life = d ** 2 / K
        fall = c_st * d ** 4 / (2 * K)
        tag("D2", f"  {name}: {d_um} um droplet lives {life:.2f} s, falls {fall * 1000:.0f} mm in still air, drifts {life * WIND:.1f} m at {WIND:.0f} m/s")
    tag("D3", f"  {name}: largest droplet that evaporates within the {fall_avail * 1000:.0f} mm between the jet end and head height: about {dmax:.0f} um")
    if name == "humid edge":
        d_edge = dmax
results["R5"] = ("Not verifiable at TRL 3", f"needs a droplet spectrum with Dv0.9 below about {d_edge:.0f} um at 7 bar; no maker's data yet")

# ------------------------------------------------------------------ E. Cooling (R4, R3)
print("\nE. Cooling")
m_air = CV_H / 1000 * CV_L / 1000 * WIND * RHO_A
q_avg = evap * (1 / (ACTIVE_H * 3600)) * HFG
q_on = q_avg / DUTY
dt_avg = q_avg / (m_air * CP_A)
dt_on = q_on / (m_air * CP_A)
v_need = q_avg / (CV_H / 1000 * CV_L / 1000 * RHO_A * CP_A * 2.0)
tag("E1", f"Evaporative heat absorbed {q_avg / 1000:.2f} kW averaged, {q_on / 1000:.1f} kW while spraying; air through the zone {m_air:.2f} kg/s at {WIND:.0f} m/s")
tag("E2", f"Air temperature drop {dt_avg:.2f} degC averaged over the duty cycle, {dt_on:.2f} degC while spraying; transit time {CV_L / 1000 / WIND:.0f} s is shorter than the 20 s pulse, so the drop follows the pulses")
tag("E3", f"R4 (2 degC averaged) is met at wind speeds below {v_need:.2f} m/s; at 0.3 m/s the averaged drop is {q_avg / (CV_H / 1000 * CV_L / 1000 * 0.3 * RHO_A * CP_A):.1f} degC (wetting risk rises)")
tw_d = wet_bulb(T_DAY, RH_DAY)
tag("E4", f"Wet-bulb limit on the design day {tw_d:.1f} degC, {T_DAY - tw_d:.1f} degC below ambient; humidity added {evap / (ACTIVE_H * 3600) / m_air * 1000:.2f} g/kg")
tag("E5", f"Heat absorbed per design day {evap * HFG / 3.6e6:.0f} kWh")
results["R4"] = ("Not met", f"{dt_avg:.2f} degC averaged ({dt_on:.2f} while spraying) at 1 m/s; met below {v_need:.2f} m/s")
results["R3"] = ("Met (literature)", "about 17.3 degC for shade sails (Middel et al., 2021); not verifiable for this fabric at TRL 3")

# ------------------------------------------------------------------ F. Energy (R8)
print("\nF. Energy")
e_pump = PUMP_W * DUTY * ACTIVE_H
e_ctrl = CTRL_W * 24
e_valve = VALVE_W * ACTIVE_H
e_use = e_pump + e_ctrl + e_valve
e_harv = PANEL_W * PSH * SYS
e_batt = BATT_WH * DOD
tag("F1", f"Use: pump {e_pump:.0f} Wh, controller and sensors {e_ctrl:.1f} Wh, drain valve held shut {e_valve:.0f} Wh; total {e_use:.1f} Wh per design day")
tag("F2", f"Harvest {e_harv:.1f} Wh ({e_harv / e_use:.2f} times the use); battery usable {e_batt:.1f} Wh = {e_batt / e_use:.3f} design days without sun")
tag("F3", f"With a latching drain valve the use would be {e_use - e_valve + 0.5:.1f} Wh and the battery would last {e_batt / (e_use - e_valve + 0.5):.2f} days, but the valve would no longer open by itself on power loss")
i_chg = PANEL_W * MPPT_EFF / V_BATT
i_pump = PUMP_W / V_BATT
tag("F4", f"Peak charge current {i_chg:.1f} A (MPPT rated 10 A); pump {i_pump:.1f} A; empty to full in {e_batt / e_harv:.2f} design days of sun")
a_enc = 2 * (P["enc"][0] * P["enc"][1] + P["enc"][0] * P["enc"][2] + P["enc"][1] * P["enc"][2]) / 1e6
a_face = P["enc"][1] * P["enc"][2] / 1e6
d_t = (ALPHA_ENC * G_ENC * a_face + Q_INT) / (H_ENC * a_enc)
tag("F5", f"Enclosure {a_enc:.3f} m2, rise above ambient about {d_t:.1f} K: {T_DAY + d_t:.1f} degC on the design day, {T_HOT + d_t:.1f} degC at {T_HOT:.0f} degC air; "
    f"charging stops above {T_CHG_MAX:.0f} degC, i.e. at air above about {T_CHG_MAX - d_t:.1f} degC")
results["R8"] = ("At risk", f"{e_use:.0f} Wh used vs {e_harv:.0f} Wh harvested; battery {e_batt / e_use:.2f} days (no margin); charging stops above about {T_CHG_MAX - d_t:.0f} degC air")

# ------------------------------------------------------------------ G. Structure and wind (R10)
print("\nG. Structure and wind")


def shs_props(b, t):
    a = b ** 2 - (b - 2 * t) ** 2
    i = (b ** 4 - (b - 2 * t) ** 4) / 12
    return a, i, i / (b / 2)


A_post, I_post, Z_post = shs_props(P["post"], P["post_t"])
A_beam, _, Z_beam = shs_props(P["beam"], P["beam_t"])
A_purl, _, _ = shs_props(P["purlin"], P["purlin_t"])
A_brace = math.pi / 4 * (P["brace_od"] ** 2 - (P["brace_od"] - 2 * P["brace_t"]) ** 2)
kgm = lambda a: a * 1e-6 * STEEL
m_posts = 2 * kgm(A_post) * D["post_len_front"] / 1000 + 2 * kgm(A_post) * D["post_len_rear"] / 1000
m_braces = 4 * kgm(A_brace) * D["brace_len"] / 1000
m_beams = kgm(A_beam) * (2 * P["roof_l"] + 2 * P["roof_d"]) / 1000
m_purl = kgm(A_purl) * 2 * (P["roof_d"] - 100) / 1000
m_plates = 4 * P["plate"] ** 2 * P["plate_t"] * 1e-9 * STEEL
m_steel = m_posts + m_braces + m_beams + m_purl + m_plates
m_dead = m_steel - m_plates + M_PANEL + M_FABRIC + M_ENC_ALL + M_PUMP + 2.0
tag("G1", f"Steel: posts {m_posts:.1f} kg (front {kgm(A_post) * D['post_len_front'] / 1000:.1f} kg each), braces {m_braces:.1f}, beams {m_beams:.1f}, purlins {m_purl:.1f}, "
    f"plates {m_plates:.1f}; total {m_steel:.0f} kg before brackets and bolts. Dead load on the anchors {m_dead:.0f} kg ({m_dead * G / 1000:.2f} kN)")
q = 0.5 * RHO_W * V_GUST ** 2
A_roof = L * Dp
N = CF_N * q * A_roof
tag("G2", f"Gust {V_GUST:.0f} m/s ({V_GUST * 3.6:.0f} km/h): dynamic pressure {q:.0f} Pa; normal force on the roof {N / 1000:.2f} kN (fabric treated as solid)")
slope = math.radians(D["slope_deg"])
h_tilt = N * math.sin(slope)
h_fric = 2 * CFR * q * A_roof
h_edge = CD_SQ * q * P["roof_l"] / 1000 * EDGE_H / 1000
h_roof = h_tilt + h_fric + h_edge
hp = D["post_len_front"] / 1000
w_post = CD_SQ * q * P["post"] / 1000
m_base = h_roof / 4 * hp + w_post * hp ** 2 / 2
sig = m_base * 1e3 / Z_post                   # N m -> N mm, over mm3: MPa
tag("G3", f"Horizontal load at roof level {h_roof / 1000:.2f} kN (tilt {h_tilt / 1000:.2f}, friction {h_fric / 1000:.2f}, edge {h_edge / 1000:.2f}); "
    f"post drag {w_post:.0f} N/m; base moment per post {m_base / 1000:.2f} kN m, posts as cantilevers without help from the braces")
tag("G4", f"Post {P['post']:.0f} x {P['post_t']:.0f} SHS, Z = {Z_post:,.0f} mm3: {sig:.0f} MPa unfactored, {sig * GAMMA:.0f} MPa with the 1.5 factor, "
    f"utilization {sig * GAMMA / FY:.2f} of S275")
m_ub = N / 4 * hp
sig_ub = m_ub * 1e3 / Z_post
tag("G5", f"Upper bound used at TRL 2 (whole normal force applied horizontally): {m_ub / 1000:.2f} kN m, {sig_ub:.0f} MPa, {sig_ub * GAMMA:.0f} MPa factored, "
    f"utilization {sig_ub * GAMMA / FY:.2f}; not a physical load case, kept as a bound")
w_beam = CF_N * q * Dp / 2
m_beam = w_beam * (2 * P["post_x"] / 1000) ** 2 / 8
sig_beam = m_beam * 1e3 / Z_beam
tag("G6", f"Long beam {P['beam']:.0f} x {P['beam_t']:.0f} SHS, Z = {Z_beam:,.0f} mm3, as a 2.8 m simple span carrying half the roof pressure: "
    f"{m_beam / 1000:.2f} kN m, {sig_beam:.0f} MPa, utilization {sig_beam * GAMMA / FY:.2f}")
p_n = CF_N * q
T_edge = p_n * Dp ** 2 / (8 * SAG * Dp)
m_edge = T_edge * (2 * P["post_x"] / 1000) ** 2 / 8
sig_edge = m_edge * 1e3 / Z_beam
tag("G7", f"Fabric as a membrane over its {Dp:.1f} m span with {SAG * 100:.0f} % sag: edge pull {T_edge / 1000:.2f} kN/m on each long beam; "
    f"in-plane bending {m_edge / 1000:.2f} kN m, {sig_edge:.0f} MPa, utilization {sig_edge * GAMMA / FY:.2f}")
m_allow = FY / GAMMA * Z_beam / 1e3          # N m
T_allow = 8 * m_allow / (2 * P["post_x"] / 1000) ** 2
sag_need = p_n * Dp ** 2 / (8 * T_allow)
v_fabric = V_GUST * math.sqrt(T_allow / T_edge)
tag("G8", f"The long beams can take an edge pull of {T_allow / 1000:.2f} kN/m: the fabric would need {sag_need * 1000:.0f} mm of sag ({sag_need / Dp * 100:.0f} % of span), "
    f"or to pass {100 * (1 - T_allow / T_edge):.0f} % of the pressure, or to come off above gusts of about {v_fabric:.0f} m/s ({v_fabric * 3.6:.0f} km/h)")
t_post = N / 4 + N * ECC * Dp / (2 * 2 * P["post_y"] / 1000)
t_net = t_post - m_dead * G / 4
f_tf = GAMMA * t_post - 0.9 * m_dead * G / 4
lever = P["anchor_pitch"] / 1000
t_bolt = GAMMA * m_base / (2 * lever) + max(f_tf, 0) / 4
tag("G9", f"Uplift with the center of pressure {ECC * Dp:.1f} m off center: worst post {t_post / 1000:.2f} kN, {t_net / 1000:.2f} kN net of dead load; "
    f"factored {f_tf / 1000:.2f} kN")
tag("G10", f"Anchor tension, factored, uplift plus base moment over a {P['anchor_pitch']:.0f} mm bolt pitch: about {t_bolt / 1000:.1f} kN per M16 anchor; "
    f"the chosen anchor's design resistance in the actual slab must exceed this (not verifiable at TRL 3)")
ballast = (N - m_dead * G) / G
tag("G11", f"Ballast to resist uplift without anchors {ballast:.0f} kg (unfactored); anchoring stays mandatory")
d_tank, h_tank = P["tank_d"] / 1000, P["tank_h"] / 1000
f_tank = CD_CYL * q * d_tank * h_tank
m_over = f_tank * h_tank / 2
m_rest = M_TANK_EMPTY * G * d_tank / 2
tag("G12", f"Empty tank ({M_TANK_EMPTY:.0f} kg assumed): drag {f_tank:.0f} N, overturning {m_over:.0f} N m against {m_rest:.0f} N m restoring; it tips unless strapped (strap added to item 13)")
results["R10"] = ("Not met", f"fabric edge pull gives long-beam utilization {sig_edge * GAMMA / FY:.1f} at 30 m/s (fabric solid, 5 % sag); fabric must come off above about {v_fabric:.0f} m/s; "
                  f"posts {sig * GAMMA / FY:.2f}; anchors not verifiable")

# ------------------------------------------------------------------ H. Movability and buildability (R17, R14, R16)
print("\nH. Movability and handling")
heaviest = kgm(A_post) * D["post_len_front"] / 1000 + kgm(A_brace) * D["brace_len"] / 1000
tag("H1", f"Heaviest part: front post with brace {heaviest:.1f} kg; long beam {kgm(A_beam) * P['roof_l'] / 1000:.1f} kg; panel {M_PANEL:.0f} kg; empty tank {M_TANK_EMPTY:.0f} kg (assumed); "
    f"full tank about {P['tank_nominal_l'] + M_TANK_EMPTY:.0f} kg (drain before moving)")
n_bolts = 16 + 4 * 4 + 8 + 8
tag("H2", f"Bolted joints: about {n_bolts} bolts and anchors (16 anchors, 4 per post-to-beam bracket, 8 brace bolts, 8 purlin bolts); no welding")
results["R17"] = ("Met", f"heaviest part {heaviest:.0f} kg against 40 kg")
results["R14"] = ("Met by design", "bolted, no welding; build time not verifiable at TRL 3")
results["R16"] = ("At risk", "scaling of 0.4 mm orifices in hard water; interval not verifiable at TRL 3")

# ------------------------------------------------------------------ I. Control, privacy, electrical, hygiene (R6, R9, R11, R12)
print("\nI. Control and electrical")
LOOP_S, DEBOUNCE_S = 10.0, 20.0
tag("I1", f"Control loop {LOOP_S:.0f} s with a {DEBOUNCE_S:.0f} s debounce on the humidity and temperature conditions: stop within {LOOP_S + DEBOUNCE_S:.0f} s of a condition failing (target 60 s); pump stops at once")
i_max = i_pump + VALVE_W / V_BATT + CTRL_W / V_BATT
tag("I2", f"Largest continuous battery current {max(i_max, i_chg):.1f} A (charge) or {i_max:.1f} A (discharge); a 15 A terminal fuse gives {15 / max(i_max, i_chg):.1f} times margin")
t_tank = (T_DAY + 26.0) / 2 + 2.0
tag("I3", f"Tank water on design days settles near the daily mean air temperature plus a little solar gain: about {t_tank:.0f} degC (assumed 26 degC night), inside the 20 to 50 degC Legionella growth range")
results["R6"] = ("Met by design", f"stop within {LOOP_S + DEBOUNCE_S:.0f} s (logic); sensor lag in the shield not verifiable at TRL 3")
results["R9"] = ("At risk", f"tank water about {t_tank:.0f} degC; age 24 h or less with the {FILL_L:.0f} L drain-and-refill routine; line drains in about {vol / 1000 / q_d:.0f} s with the vacuum breaker")
results["R11"] = ("Met by design", "PIR only; no camera or microphone; no status link fitted")
results["R12"] = ("Met by design", f"12 V DC only; 15 A terminal fuse; BMS with cold-charge cutoff")

# ------------------------------------------------------------------ J. Cost (R13)
print("\nJ. Cost")
with open(ROOT / "bom" / "bom.csv", newline="") as f:
    bom = list(csv.DictReader(f))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
budget = float(re.search(r"^budget_usd:\s*([\d.]+)", (ROOT / "project.yaml").read_text(), re.M).group(1))
PROPOSED = 750.0
steel_usd = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r["item"].split()[0] in ("1", "2", "4"))
tag("J1", f"BOM {len(bom)} lines, total ${total:,.2f}: ${total - budget:+,.2f} ({(total / budget - 1) * 100:+.1f} %) against budget_usd ${budget:,.0f}; "
    f"${total - PROPOSED:+,.2f} ({(total / PROPOSED - 1) * 100:+.1f} %) against the proposed ${PROPOSED:,.0f}")
tag("J2", f"Steel lines 1, 2 and 4 cost ${steel_usd:,.0f} for about {m_steel:.0f} kg, ${steel_usd / m_steel:.2f}/kg including cutting, drilling and galvanizing: low, so cost is at risk upward until quoted")
results["R13"] = ("Not met", f"${total:,.0f} against ${budget:,.0f} ({(total / budget - 1) * 100:+.1f} %) and against the proposed ${PROPOSED:,.0f} ({(total / PROPOSED - 1) * 100:+.1f} %)")

# ------------------------------------------------------------------ Summary
print("\nRequirement status")
order = [f"R{i}" for i in range(1, 18)]
for k in order:
    s, note = results[k]
    print(f"{k}: {s}; {note}")
groups = {"Not met": [], "At risk": [], "Not verifiable at TRL 3": [], "Met": []}
for k in order:
    s = results[k][0]
    groups["Met" if s.startswith("Met") else s].append(k)
print("Counts: " + "; ".join(f"{g} {len(v)} ({', '.join(v)})" for g, v in groups.items()))
