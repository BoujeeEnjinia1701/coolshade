"""CoolShade STEM check calculations (CSH-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. First-order screens of each claim of option A (the solar misting shade
canopy). The sizing is in the calculation note (CSH-CAL-001, docs/04-calcs/sizing.py), which this script imports
(it prints a long report, hidden here, and builds the model) to close rows on the TRL 3 design. Design day:
38 degC, 25 % relative humidity, 5 h of misting demand, 4.5 peak sun hours.
"""
import contextlib, io, math, sys
sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX, FAILS, limits  # noqa: F401
sys.path.insert(0, "docs/04-calcs")
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  CSH-CAL-001, reads cad/src/model.py and bom/bom.csv

c = Check()
HFG = 2.43e6                                    # J/kg, latent heat of water at about 30 degC
Q_SPRAY = CAL.Q_NOZ * CAL.N_NOZ                 # L/h while spraying (32)
GAMMA, FY = CAL.GAMMA, CAL.FY

# ---- Physics: evaporative cooling
p_evap = Q_SPRAY / 3600 * CAL.EVAP * HFG        # W absorbed while spraying
c.cited("S1", "The mist absorbs about 18.8 kW from the air while spraying", "Physics", "Thermodynamics and heat transfer",
        f"Q = m_dot x 0.87 evaporated x latent heat (2.43 MJ/kg) for 8 nozzles x 4 L/h = {p_evap / 1e3:.1f} kW; the 0.87 evaporated share is an estimate that falls as the droplets get bigger (S4), and drops that drift out of the zone (CSH-CAL-001 D2) cool air outside it, so the share that cools the waiting zone is a range, not a point",
        "Arithmetic checks out (independent review); the evaporated share inside the zone needs the nozzle's droplet spectrum", PLAUSIBLE, closed_by="CSH-CAL-001 E1")
c.claim("S2", "The air in the waiting zone is at least 2 degC cooler while spraying (2.71 degC computed)", "Physics", "Thermodynamics and heat transfer",
        "Sensible heat removed from a 3 x 2 m control volume crossed by air at 1 m/s: dT = Q / (m_dot cp); assumes the mist mixes through the whole volume, which real spray plumes do not (CSH-PRS-001 assumptions); the control volume's 3 m is used both as the frontal width and as the transit length, so the drop moves by about 25 % with the wind direction",
        round(CAL.dt_on, 2), 2.0, "degC", rule="above", margin=0.4, closed_by="CSH-CAL-001 E2, E3")
c.claim("S3", "Misting cannot cool the air below the wet bulb (design day: 15 degC below ambient)", "Physics", "Thermodynamics and heat transfer",
        "Adiabatic saturation limit: dry-bulb depression is at most T_air - T_wetbulb (Stull wet bulb, 38 degC at 25 % RH)",
        round(CAL.dt_on, 2), round(CAL.T_DAY - CAL.tw_d, 1), "degC", closed_by="CSH-CAL-001 E4")
c.cited("S4", "Droplets from the nozzle evaporate before they reach a person at 1.5 m (no wetting)", "Physics", "Fluid mechanics",
        "Droplet evaporation after Maxwell/Fuchs diffusion: on the design day a droplet of up to about 100 um evaporates in the 0.76 m between the jet end and head height, at the humid edge (32 degC, 60 %) up to about 80 um (CSH-CAL-001 D3); nozzle makers state the spectrum as Dv0.9",
        "Needs Dv0.9 below about 80 um at 7 bar; no maker's data yet. At risk: fog that flash-evaporates is normally made at much higher pressure (50 bar and more), and a 7 bar spectrum is likely coarser; if it is, wetting (PR-005) and cooling (S1, S2) fail together and option B becomes the fallback", PLAUSIBLE, closed_by="")
d_ideal = (math.pi / 4 * (CAL.P["nozzle_orifice"] / 1000) ** 2) * math.sqrt(2 * CAL.P_BAR * 1e5 / 1000) * 3.6e6
c.claim("S5", "Each 0.4 mm nozzle can pass 4 L/h at 7 bar (the physical bound is 16.9 L/h; the real flow is the maker's figure)", "Physics", "Fluid mechanics",
        f"A bound only, not a prediction: Bernoulli orifice flow Q = A sqrt(2 dp / rho): ideal {d_ideal:.1f} L/h, so 4 L/h implies a discharge coefficient of {CAL.Q_NOZ / d_ideal:.2f}, plausible for a swirl nozzle (maker's datasheet to confirm)",
        CAL.Q_NOZ, round(d_ideal, 1), "L/h", closed_by="CSH-CAL-001 C1")
c.balance("S6", "The 60 W pump draw covers the hydraulic power of 32 L/h at 7 bar", "Physics", "Fluid mechanics",
          {"pump electrical input": CAL.PUMP_W}, {"hydraulic power": Q_SPRAY / 3.6e6 * CAL.P_BAR * 1e5}, "W",
          law="Hydraulic power = Q x dp; the rest is motor and diaphragm loss (10 % wire to water)", closed_by="CSH-CAL-001 C6")
t_drain = CAL.vol / 1000 / CAL.q_d              # s
c.claim("S7", "The bulk of the mist line drains within 5 min after a session (about 30 s computed); water films and the anti-drip nozzle bodies stay wet", "Physics", "Fluid mechanics",
        "Torricelli flow through the 3 mm valve orifice at 0.5 m head (Cd 0.6), with air let in by the vacuum breaker; the 0.40 L line volume from the model",
        round(t_drain, 0), 300.0, "s", closed_by="CSH-CAL-001 C7")
# ---- Physics: energy
p_eff = 100.0 / (1000.0 * 1.0 * 0.67)           # panel efficiency at standard test conditions, 100 W on 1.0 x 0.67 m
c.claim("S8", "A 100 W panel of 1.0 x 0.67 m is a credible rating", "Physics", "Thermodynamics and heat transfer",
        "Efficiency = P / (1000 W/m2 x area) must stay below the Shockley-Queisser limit for a single junction (33.7 %); commercial monocrystalline panels reach about 20 %",
        round(p_eff * 100, 1), round(limits.SHOCKLEY_QUEISSER * 100, 1), "%", closed_by="CSH-CAL-001 F2")
c.balance("S9", "The panel harvests more energy per design day than the system uses", "Physics", "Thermodynamics and heat transfer",
          {"panel harvest (100 W x 4.5 h x 0.75)": CAL.e_harv}, {"pump, controller, sensors, valve": CAL.e_use}, "Wh",
          law="Conservation of energy, with 0.75 for MPPT, wiring and temperature losses; holds on the design day only: on days above 42.7 degC charging pauses at midday (S11)", closed_by="CSH-CAL-001 F1, F2")
c.claim("S10", "The battery runs the system for a full design day with no sun", "Physics", "Thermodynamics and heat transfer",
        "Usable energy = 12.8 V x 25 Ah x 0.80 depth of discharge divided by the daily use, at beginning of life (at 80 % state of health it is about 1.0 design days, and cells at 40 to 47 degC age faster)",
        round(CAL.e_batt / CAL.e_use, 2), 1.0, "design days", rule="above", margin=0.3, closed_by="CSH-CAL-001 F2")
# ---- Chemistry: battery in the heat
d_t = CAL.d_t
enc_sun = (CAL.ALPHA_ENC * 900.0 * CAL.a_face + CAL.Q_INT) / (CAL.H_ENC * CAL.a_enc)      # enclosure in direct late sun (900 W/m2)
c.cited("S11", "The battery keeps charging on hot days: LiFePO4 charge limit 45 degC against an enclosure 2.3 K above the air (white enclosure, in the cloth's shade)", "Chemistry", "Electrochemistry and batteries",
        f"Enclosure heat balance dT = (alpha G A_face + Q_internal) / (h A), G = 200 W/m2 in the shade of the cloth; cells are charged only below about 45 degC (typical cell data; the BMS reads cell temperature, which runs above the air in the box). The original grey enclosure (alpha 0.5) rose 3.6 K and stopped charging above 41.4 degC air; the white one (CSH-DEC-001 D9) rises {CAL.d_t:.1f} K, charging holds to {CAL.T_CHG_MAX - CAL.d_t:.1f} degC air. In direct late sun (900 W/m2, the enclosure is on the outer face of the rear right post) the white enclosure rises {enc_sun:.1f} K and charging stops above {CAL.T_CHG_MAX - enc_sun:.1f} degC air, so the fix is partial",
        "Sun exposure of the enclosure across the day, long-wave exchange with the hot slab and the named cell's charge limit to assess at the site; a sunshield on the enclosure is a candidate", PLAUSIBLE, closed_by="CSH-CAL-001 F5; CSH-DEC-001 D9")
c.cited("S12", "Scale from hard water does not block the 0.4 mm nozzles within a month", "Chemistry", "Materials and polymer chemistry",
        "Calcium carbonate precipitates as the mist evaporates and when water warms; orifices of 0.4 mm clog from a few mg of deposit; a 5 um filter does not remove dissolved hardness",
        "Hardness of the site water and descaling interval to assess at the site (CSH-DEC-001 to-confirm item 12)", PLAUSIBLE, closed_by="")
# ---- Biology
c.cited("S13", "Shade cuts the mean radiant temperature by at least 15 degC at midday", "Physics", "Thermodynamics and heat transfer",
        "Measured in Tempe, Arizona at 159 locations: shade sails and umbrellas cut the daytime mean radiant temperature by about 17.3 degC (Middel et al., BAMS 2021)",
        "Evidence from analogous shade sails, not this design: 17.3 degC measured against the 15 degC target, a margin of 2.3 K on a site average; this cloth (about 90 % UV block, which is not 90 % of the shortwave) and the occupied spots, where the shadow falls partly outside the roof footprint at low sun (CSH-CAL-001 A2), are unmeasured; confirm with a globe thermometer", PLAUSIBLE, closed_by="CSH-CAL-001 E (PR-003)")
c.cited("S14", "The misting system does not become a Legionella source", "Biology", "Ecology and agronomy",
        "Legionella grows in water at 20 to 50 degC (optimum about 35 degC) and spreads by inhaled aerosol (WHO fact sheet). Tank water on a design day settles near 34 degC (CSH-CAL-001 I3), inside the growth range; the controls are a 5 um filter, water no older than 24 h (95 L drain-and-refill), the bulk of the line drained within 30 s (films and the anti-drip nozzle bodies stay wet), an opaque shaded tank and weekly disinfection",
        "Temperature cannot be avoided; water age and cleaning are the controls; sampling with a partner lab needs TRL 4", PLAUSIBLE, closed_by="")
c.cited("S15", "A passive infrared sensor detects people standing still in 38 to 45 degC air", "Biology", "Ecology and agronomy",
        "A PIR sensor responds to the contrast between a warm body (skin about 33 to 35 degC, clothing cooler) and its background; in air near body temperature the contrast and the detection range fall, and a person standing still gives little signal (sensor datasheets derate range with ambient temperature)",
        "Range and sensitivity above 35 degC to take from the sensor maker; a radar presence sensor is a privacy and radio-approval trade-off for Amish (CSH-DEC-001 D10)", PLAUSIBLE, closed_by="")
# ---- Mathematics
a_post = CAL.P["post"] ** 2 - (CAL.P["post"] - 2 * CAL.P["post_t"]) ** 2          # mm2
c.order_of_magnitude("S16", "A front post (80 x 80 x 3 SHS, 2.90 m) weighs about 21 kg", "Mathematics", "Units and dimensional analysis",
                     claimed=21.0, estimate=a_post * 1e-6 * CAL.STEEL * CAL.D["post_len_front"] / 1000, unit="kg",
                     law="Mass = section area x length x 7850 kg/m3", closed_by="CSH-CAL-001 H1")
# ---- Engineering and technology: structure
q15 = 0.5 * CAL.RHO_W * 15.0 ** 2
u_fab15 = CAL.sig_edge * GAMMA / FY * (15.0 / CAL.V_GUST) ** 2
c.claim("S17", "With the fabric fitted the long beams carry forecast gusts up to 15 m/s (the original 30 m/s case gives utilization 3.5 and failed; fixed by removing the fabric above 15 m/s, CSH-DDR-002)", "Engineering and technology", "Strength of materials",
        "Fabric as a membrane with 5 % sag: edge pull T = p L^2 / (8 s) per metre, in-plane bending of the 50 x 50 x 2 SHS long beam over the 2.8 m post span, S275 with a 1.5 factor",
        round(u_fab15, 2), 1.0, "utilization", margin=0.15, closed_by="CSH-CAL-001 G7, G8, G14")
u_off = CAL.u0                                   # post utilization, fabric off, 30 m/s: CSH-CAL-001 G13 (panel as a flat plate plus frame drag)
c.claim("S18", "With the fabric removed the frame survives a 30 m/s gust", "Engineering and technology", "Strength of materials",
        "Post as a cantilever: panel as a flat plate (1.2 q A) with its tilt component plus drag on the frame and posts, S275 with a 1.5 factor (CSH-CAL-001 G13); roof members and anchors in G13 too; recomputed by the independent reviewer as 0.14",
        round(u_off, 2), 1.0, "utilization (post)", closed_by="CSH-CAL-001 G13")
m_over, m_rest = CAL.m_over, CAL.m_rest
strap = (m_over - m_rest) / (CAL.h_tank * 0.9)
c.cited("S19", "An empty tank tips in a 30 m/s gust unless strapped; the strap carries the difference (the unstrapped tank failed, strap added in CSH-DDR-003)", "Engineering and technology", "Mechanics and statics",
        f"Overturning {m_over:.0f} N m against restoring {m_rest:.0f} N m; strap tension = difference / (0.9 x tank height) = {strap:.0f} N, {1.5 * strap:.0f} N with the 1.5 factor; the strap works for some wind directions only, so the two stop cleats are the second restraint; sliding (163 N of drag against about 40 N of friction) is held by the strap and the cleats; the strap's rating is not yet named",
        f"{1.5 * strap:.0f} N factored against a strap of a few hundred newtons or more; rating and cleat anchors to confirm when parts are bought", PLAUSIBLE, closed_by="CSH-CAL-001 G12")
c.cited("S20", "The M16 anchors hold in the slab at the site", "Engineering and technology", "Standards practice",
        f"Factored anchor tension about {CAL.t_bolt / 1000:.1f} kN with the fabric on in a 30 m/s gust and about 2.8 kN with it removed (CSH-CAL-001 G10, G13); the resistance depends on the anchor type and the slab, which are unknown until a site is chosen",
        "Anchor design resistance and slab to assess at each site", PLAUSIBLE, closed_by="")
c.cited("S21", "A garage can build the frame: bolted, no welding, rivet nuts in 2 mm tube", "Engineering and technology", "Manufacturing tolerances",
        "Blind rivet nuts are standard in thin-wall tube; the largest pull on one M8 rivet nut is about 0.16 kN factored (CSH-CAL-001 G15); the maker's pull-out rating in a 2 mm wall is not yet checked",
        "Rating to confirm from the rivet nut maker's data when parts are bought", PLAUSIBLE, closed_by="")

# ---- Concept options B and C (CSH-OPT-001): their working principles, first-order screens
cp_air, rho_air = 1006.0, 1.15
eps, q_fan = 0.8, 0.11                         # pad effectiveness (cellulose pad, 90 mm, typical), 250 mm 12 V axial fan at the pad (m3/s, estimate)
t_wb = CAL.tw_d
t_out = CAL.T_DAY - eps * (CAL.T_DAY - t_wb)
c.claim("S22", "Option B: the wet pad delivers air at about 26 degC from 38 degC, 25 % RH air", "Physics", "Thermodynamics and heat transfer",
        f"Direct evaporative cooling, T_out = T_db - eps (T_db - T_wb), eps 0.8 for a 90 mm cellulose pad (typical, to confirm from the maker); the outlet cannot be below the wet bulb {t_wb:.1f} degC",
        round(t_out, 1), round(t_wb, 1), "degC", rule="above", closed_by="")
q_b = q_fan * rho_air * cp_air * (CAL.T_DAY - t_out)
c.order_of_magnitude("S23", "Option B: the fan and pad remove about 1.5 kW and evaporate about 2.2 L/h", "Physics", "Thermodynamics and heat transfer",
                     claimed=2.2, estimate=q_b / HFG * 3600, unit="L/h",
                     law=f"Q = m_dot cp dT = {q_b / 1e3:.2f} kW at {q_fan} m3/s; water = Q / latent heat (a pad also needs bleed-off water against scale, which adds 20 to 50 %)", closed_by="")
c.cited("S24", "Option B: one 250 mm fan cools a group of 6 to 8 people", "Physics", "Fluid mechanics",
        f"The cooled stream carries {q_b / 1e3:.1f} kW, {q_b / p_evap * 100:.0f} % of the {p_evap / 1e3:.1f} kW that option A's mist absorbs; an axial jet of 0.11 m3/s mixes with room air within about 1 to 2 m, so it cools one or two people, not a group",
        "Throw and mixing to confirm with a jet model or a field test; several fans would change the cost and power", PLAUSIBLE, closed_by="")
dh = CAL.D["slope_deg"]
v_stack = math.sqrt(2 * G * (2.4 * math.sin(math.radians(dh))) * 10.0 / 310.0)
c.cited("S25", "Option C: a white skin 100 mm above the shade cloth lowers the heat load and the gap vents by buoyancy", "Physics", "Thermodynamics and heat transfer",
        f"Stack effect in a gap 2.4 m long at {dh:.1f} deg, 10 K warmer than the air: v = sqrt(2 g H dT / T) = {v_stack:.2f} m/s, an upper bound before friction; white coatings reflect most of the sun (reflectance of the maker's panel to confirm)",
        "Added radiant benefit over the shade cloth alone to measure; no air cooling at all (no evaporation)", PLAUSIBLE, closed_by="")
n_c = CAL.CF_N * CAL.q * CAL.P["roof_l"] / 1000 * CAL.P["roof_d"] / 1000
c.cited("S26", "Option C: the skin cannot be taken off before a gust, so the frame must carry 30 m/s with the roof solid", "Engineering and technology", "Strength of materials",
        f"Rigid sheets pass the load to the long beams as pressure, not as fabric edge pull: normal force {n_c / 1e3:.2f} kN, long beams 0.70 utilization (CSH-CAL-001 G6); anchors about {CAL.t_bolt / 1000:.1f} kN each (G10), the slab to assess",
        "Beams within; anchors and slab depend on the site", PLAUSIBLE, closed_by="")

if __name__ == "__main__":
    print(f"Record of the fixes: enclosure rise {d_t:.2f} K (white, alpha 0.25); grey (alpha 0.5) gave 3.65 K and charging stopped above 41.4 degC; "
          f"fabric on at 30 m/s utilization {CAL.sig_edge * GAMMA / FY:.2f}; empty tank overturning {m_over:.0f} N m against {m_rest:.0f} N m restoring")
    c.write()
