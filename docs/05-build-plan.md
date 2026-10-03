---
doc_id: CSH-BLD-001
title: CoolShade prototype build plan
project: CoolShade
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: First build plan at TRL 3, with pictures by component and step; design made constructable (CSH-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Section 2: the changes recorded in CSH-DDR-003 accepted by Amish on 2026-10-02"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Safety stops S7 and S9 name the market operator's manager and the environmental health authority for a market lane"
---

# CoolShade prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The cables, which run inside the posts and beams, are not shown.*

The prototype is one CoolShade canopy on an existing concrete slab: four 80 mm square steel posts on a 2,800 x 2,350 mm grid carry two horizontal long beams, and between them two sloping end beams, two purlins and a panel bearer make a roof frame 3.0 x 2.4 m in plan that falls 300 mm from the street edge to the rear. Knitted shade cloth is laced over the frame; a 100 W solar panel sits in a notch at the rear of the cloth on two rails. A mist line loop with eight nozzles hangs under the roof; the pump, filter and drain valve are on a plate on the rear left post, the 120 L tank is strapped beside it, and the controller, battery and charge controller are in a locked box on the rear right post. Figure 1 shows the 21 components in the order you make or fit them. Fourteen kinds of part are made in a workshop from steel tube, angle, flat bar, plate and sheet by sawing, drilling, flattening and bending; everything else is bought and fitted. There is no welding: every joint is bolted, and bolts into the closed beams go into rivet nuts. The parts cost about $882 from the bill of materials.

> **Safety:** This is a wind-loaded steel structure built at height, with a 12.8 V lithium iron phosphate battery of about 320 Wh and a water line at about 7 bar that sprays an aerosol near the public. Lift posts and beams with two people, work from stable ladders or a platform, keep the battery fuse out and the line unpressurized until section 6 allows, use potable water only, and fit the cloth only when forecast gusts are below 15 m/s (54 km/h). Cut steel edges and flattened tube ends are sharp: deburr them and wear gloves.

## 2. What changed to make it buildable

The concept showed what CoolShade does; most of its parts met as overlapping blocks with no fixing. Each change below keeps what the canopy does, and all of them are recorded in decision record CSH-DDR-003, accepted by Amish on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Post grid and long beams | Posts 2,100 mm apart across the sidewalk; the cloth ran 125 mm past the beams with nothing under its edges | Posts 2,350 mm apart; the long beams sit on the post tops at the roof's street and rear edges (Figures 2 and 10) | Every edge of the cloth has a tube to lace to; the clear floor widens to 2.27 m |
| Roof corners | Beams overlapping each other and the post tops, tilted with the roof | Long beams horizontal on the posts; end beams, purlins and bearer cut to butt against the beam faces on angle cleats (Figures 17 and 18) | Face-to-face bolted joints a square tube can make |
| Post top and base | No fixing to the beam or the base plate | Head cleats (Figure 10) and base cleats (Figure 5), all bolted | No welding (R14) |
| Knee braces | Solid rods running into the post and beam | Tube with flattened, bent ends bolted flat to the post and beam (Figures 22 and 30) | The simplest bolted brace; its lowest point is 2,223 mm, above the 2,200 mm headroom (R2) |
| Solar panel | On rails floating above the purlins, on top of the cloth | At the rear edge on rails and L-feet on a new panel bearer and the rear beam; the cloth has a notch under it (Figures 22 and 30) | The cloth comes off before storms without touching the panel |
| Enclosure, sensor head, PIR | Floating beside the posts and beams | Enclosure rails, an angle sensor arm at 2.4 m, a PIR bracket (Figures 31 and 32) | Each is bolted, and the shield hangs 2,266 mm up |
| Pump, filter, drain valve | Floating beside the rear left post, no pipe to the drain valve | On an equipment plate; the down pipe ends in the drain valve (Figure 33) | One plate, and the valve stays at the low point |
| Tank | Overlapping the post base | Moved clear, strapped to the post, with two stop cleats (Figure 35) | It cannot tip or slide |
| Cables and missing parts | Cables through walls; no tank level switch | Cables inside the posts and beams; a tank level switch and an I2C extender added (step 16) | The control rules need the level switch; the sensor cable is about 7 m |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" are as seen standing on the street side looking at the canopy; "inner" faces face the middle of the canopy. Workshop tolerance is 1 mm unless a step says otherwise; drawings carry no tolerances before TRL 4. Galvanized steel is drilled after galvanizing here: paint every cut end, hole and flattened end with zinc-rich paint.

### 3.1 Base plates (make 4)

![Figure 2. Slab layout](05-build-plan/slab-layout.png)

*Figure 2. Slab layout: post centres, base plates and anchor holes.*

![Figure 3. Making sketch of the base plate](../cad/drawings/CSH-DWG-101.png)

*Figure 3. Base plate making sketch (CSH-DWG-101).*

**What it is and what it is made from.** The square plate each post stands on, anchored to the slab. Steel plate 10 mm thick.

**How to make it.**

1. Cut four plates 220 x 220 mm; deburr.
2. Drill four 18 mm holes on a 160 mm square, 30 mm in from each edge.
3. Zinc-rich paint, or galvanize the plates after drilling.

**How it fits the parts next to it.** It lies flat on the slab; the post stands on its centre between two base cleats, and four M16 anchors pass through the cleats and the plate into the slab (Figure 5). The drilled plate is the template for the slab holes.

**Check before moving on.** Each plate sits flat on the slab where Figure 2 puts it without rocking; if not, pack it with steel shims or bed it on grout.

### 3.2 Base cleats (make 8)

![Figure 4. Making sketch of the base cleat](../cad/drawings/CSH-DWG-102.png)

*Figure 4. Base cleat making sketch (CSH-DWG-102).*

**What it is and what it is made from.** A short angle each side of the post's foot that bolts the post to the plate and slab. Galvanized equal angle 75 x 75 x 6 mm.

**How to make it.**

1. Cut eight 220 mm lengths; deburr.
2. Upright leg: two 13 mm holes at mid-length, 35 and 62 mm above the underside of the flat leg.
3. Flat leg: two 18 mm holes 40 mm out from the back of the upright leg and 30 mm in from each end, 160 mm apart.
4. Drill the cleats in pairs, clamped back to back, so the holes match.

**How it fits the parts next to it.**

![Figure 5. Joint 1: post base](05-build-plan/joint-01.png)

*Figure 5. The post stands on the plate between two cleats; two M12 bolts go through cleat, post and cleat; the anchors pass through the cleats' flat legs and the plate.*

The cleats go on the post's left and right faces, upright legs flat on the post, flat legs flat on the plate, flat legs pointing away from the post. The two M12 bolts are tightened only after the post is plumb (step 2).

**Check before moving on.** On a trial fit with a post offcut, the four flat-leg holes line up with the plate's and the upright-leg holes with the post's.

### 3.3 Posts (make 4: two front, two rear)

![Figure 6. Making sketch of the front post](../cad/drawings/CSH-DWG-103.png)

*Figure 6. Front post making sketch (CSH-DWG-103).*

![Figure 7. Making sketch of the rear post](../cad/drawings/CSH-DWG-104.png)

*Figure 7. Rear post making sketch (CSH-DWG-104).*

![Figure 8. Post hole positions](05-build-plan/post-holes.png)

*Figure 8. Every post hole, measured up from the bottom end.*

**What it is and what it is made from.** The four legs. Galvanized steel square hollow section 80 x 80 x 3 mm: two front posts 2,902 mm long and two rear posts 2,608 mm long, the difference making the roof's fall.

**How to make it.**

1. Cut the four posts to length with both ends square; the top end must be square so the beam sits flat on it.
2. Drill the holes every post has, through both walls of its left and right faces, on the centre line: 13 mm at 35 and 62 mm from the bottom (base cleats), 11 mm at 372.5 mm below the top (knee brace) and 11 mm at 28 mm below the top (head cleats).
3. Drill the extra holes each post has, from Figure 8:
   - front right: two 9 mm holes through the street and back faces, 15 mm each side of centre, 2,388 mm up (sensor arm); a 12 mm cable hole in the street face, 30 mm toward the outer side, 2,435 mm up;
   - rear right: four 11 mm holes through the left and right faces, 25 mm each side of centre, 1,510 and 1,770 mm up, countersunk on the outer face (enclosure rails); a 12 mm cable hole in the outer face, 13 mm toward the street, 1,390 mm up;
   - rear left: two 11 mm holes through the street and back faces on the centre line, 780 and 1,340 mm up (equipment plate); a 12 mm cable hole in the street face, 25 mm toward the canopy, 1,330 mm up.
4. Deburr, paint the cut ends and holes, and fit a rubber grommet in each cable hole.

**How it fits the parts next to it.** The bottom stands on the base plate between the base cleats (Figure 5); the top carries the long beam and two head cleats (Figure 10); the knee brace bolts to the inner face (Figure 14).

**Check before moving on.** A straight rod passes square through each pair of opposite holes.

### 3.4 Head cleats (make 8)

![Figure 9. Making sketch of the head cleat](../cad/drawings/CSH-DWG-105.png)

*Figure 9. Head cleat making sketch (CSH-DWG-105).*

**What it is and what it is made from.** A short angle each side of the post top that holds the long beam down. Galvanized equal angle 50 x 50 x 5 mm.

**How to make it.**

1. Cut eight 46 mm lengths; deburr.
2. Upright leg: one 11 mm hole at mid-length, 28 mm below the top face of the flat leg.
3. Flat leg: one 9 mm hole at mid-length, 27.5 mm out from the back of the upright leg.

**How it fits the parts next to it.**

![Figure 10. Joint 2: post head](05-build-plan/joint-02.png)

*Figure 10. The long beam sits on the square-cut post top; a cleat each side, flat legs flush with the post top, pointing away from the post.*

One M10 bolt passes through both cleats and the post; one M8 bolt goes up through each flat leg into a rivet nut in the beam's underside.

**Check before moving on.** A straight edge across the post top touches both cleats' flat legs.

### 3.5 Long beams (make 2)

![Figure 11. Making sketch of the long beam](../cad/drawings/CSH-DWG-107.png)

*Figure 11. Long beam making sketch (CSH-DWG-107).*

![Figure 12. Long beam hole positions](05-build-plan/beam-holes.png)

*Figure 12. Every hole in the two long beams, from the left end.*

**What it is and what it is made from.** The two horizontal beams along the street and rear edges of the roof. Galvanized steel SHS 50 x 50 x 2 mm, 3,000 mm long.

**How to make it.**

1. Cut two beams 3,000 mm long, ends square. Mark the left end and which beam is the front.
2. Drill every hole in Figure 12, measured from the left end: in the underside for the head cleats and knee braces, in the inner face for the frame cleats and the line clips, in the rear beam's top face for the L-feet, and the 12 mm cable holes.
3. Set an M8 steel rivet nut in each 11 mm hole and an M5 rivet nut in each 7 mm hole with the hand rivet nut tool. Fit grommets in the cable holes and plastic caps in the ends.

**How it fits the parts next to it.** Each beam sits centred on two post tops, overhanging each post's centre by 100 mm (Figure 10). The end beams, purlins and cleats meet its inner face (Figures 17 and 18); the cloth laces round it.

**Check before moving on.** Lay the beam on two trestles with the head cleats bolted on in their places: the cleat bolts start by hand in every rivet nut.

### 3.6 Knee braces (make 4)

![Figure 13. Making sketch of the knee brace](../cad/drawings/CSH-DWG-106.png)

*Figure 13. Knee brace making sketch (CSH-DWG-106).*

**What it is and what it is made from.** A short diagonal from each post to its long beam that stiffens the corner. Galvanized steel tube 32 mm outside diameter, 2.5 mm wall.

**How to make it.**

1. Cut four 581 mm lengths.
2. Squash the last 75 mm of each end flat in a vice, to about 50 mm wide and 5 mm thick, both ends flat in the same plane.
3. Bend each flat end 45°, 45 mm from the end, the two ends bent opposite ways so they end square to each other; the bends are 491 mm apart.
4. Drill an 11 mm hole 22 mm from the lower end and a 9 mm hole 22 mm from the upper end, on the centre line.
5. Paint the flattened ends where the zinc has cracked.

**How it fits the parts next to it.**

![Figure 14. Joint 3: knee brace lower end](05-build-plan/joint-03.png)

*Figure 14. The lower end lies flat on the post's inner face, its bend 350 mm below the beam; one M10 bolt through the post.*

![Figure 15. Joint 4: knee brace upper end](05-build-plan/joint-04.png)

*Figure 15. The upper end lies flat under the beam, its bend 350 mm in from the post; one M8 bolt into a rivet nut.*

The bottom of the lower flat end is the lowest point overhead in the canopy: 2,223 mm above the slab at the rear posts.

**Check before moving on.** Held to a post and beam offcut set square, both flat ends sit flat without forcing.

### 3.7 Frame cleats (make 10)

![Figure 16. Making sketch of the frame cleat](../cad/drawings/CSH-DWG-111.png)

*Figure 16. Frame cleat making sketch (CSH-DWG-111).*

**What it is and what it is made from.** The angle that joins a tube to the face of the tube it butts against. Galvanized equal angle 50 x 50 x 5 mm: four 40 mm long (end beams) and six 30 mm long (four for the purlins, two for the bearer).

**How to make it.**

1. Cut the ten lengths; deburr.
2. Drill one 9 mm hole in each leg at mid-length, 25 mm out from the back of the other leg.

**How it fits the parts next to it.**

![Figure 17. Joint 5: end beam to long beam](05-build-plan/joint-05.png)

*Figure 17. The end beam's end butts flat against the long beam's inner face; the cleat sits in the inside corner with one M8 bolt into a rivet nut in each tube.*

![Figure 18. Joint 6: purlin to long beam](05-build-plan/joint-06.png)

*Figure 18. The purlin joins the long beam the same way, with a 30 mm cleat on its inner side.*

**Check before moving on.** Both legs sit flat on their faces with the bolts in.

### 3.8 End beams (make 2)

![Figure 19. Making sketch of the end beam](../cad/drawings/CSH-DWG-108.png)

*Figure 19. End beam making sketch (CSH-DWG-108), drawn laid flat.*

**What it is and what it is made from.** The two sloping beams at the left and right ends of the roof. Galvanized steel SHS 50 x 50 x 2 mm.

**How to make it.**

1. Cut two lengths 2,318 mm on the centre line, each end cut 7° off square with the two cuts parallel, so that fitted on the slope both ends stand upright.
2. Inboard face: one 11 mm rivet nut hole 25 mm from each end, 20 mm below the top face at the front end and 30 mm at the rear end. Underside: three 7 mm holes 353, 1,159 and 1,965 mm from the front end, on the centre line (line clips).
3. Set the rivet nuts.

**How it fits the parts next to it.** The end beams go between the long beams at the very ends of the roof, their outer faces level with the long beams' ends, ends flat against the long beams' inner faces (Figure 17). The mist line hangs under them (Figure 34).

**Check before moving on.** Laid between two straight edges 2,300 mm apart, both end faces touch them fully.

### 3.9 Purlins (make 2)

![Figure 20. Making sketch of the purlin](../cad/drawings/CSH-DWG-109.png)

*Figure 20. Purlin making sketch (CSH-DWG-109), drawn laid flat.*

**What it is and what it is made from.** Two lighter sloping tubes that carry the middle of the cloth and the panel bearer. Galvanized steel SHS 40 x 40 x 2 mm.

**How to make it.**

1. Cut two lengths 2,318 mm on the centre line, ends cut as for the end beams.
2. Inboard face: one 11 mm rivet nut hole 25 mm from each end (20 mm below the top at the front end, 25 mm at the rear end) and one 1,673 mm from the front end, 25 mm below the top (bearer cleat). Set the rivet nuts.

**How it fits the parts next to it.** The purlins stand 530 mm each side of the roof's centre line, tops level with the end beams (Figure 18). Their inner faces frame the notch in the cloth.

**Check before moving on.** As for the end beams.

### 3.10 Panel bearer (make 1)

![Figure 21. Making sketch of the panel bearer](../cad/drawings/CSH-DWG-110.png)

*Figure 21. Panel bearer making sketch (CSH-DWG-110).*

**What it is and what it is made from.** A short cross tube between the purlins that carries the front feet of the panel rails. Galvanized steel SHS 50 x 50 x 2 mm, 1,020 mm long.

**How to make it.**

1. Cut 1,020 mm, ends square.
2. Front face: one 11 mm rivet nut hole 25 mm from each end, 18.5 mm below the top. Top face: two 11 mm rivet nut holes 205 and 815 mm from the left end, on the centre line. Set the rivet nuts.

**How it fits the parts next to it.**

![Figure 22. Joint 7: panel bearer, purlin and L-foot](05-build-plan/joint-07.png)

*Figure 22. The bearer butts square against the purlins' inner faces on two 30 mm cleats; the rail's L-foot stands on its top.*

Its front face is 1,685 mm behind the front beam's inner face, measured level; the front edge of the cloth's notch laces round it.

**Check before moving on.** It drops between the purlins with no more than 1 mm to spare and sits level.

### 3.11 Enclosure rails (make 2)

![Figure 23. Making sketch of the enclosure rail](../cad/drawings/CSH-DWG-113.png)

*Figure 23. Enclosure rail making sketch (CSH-DWG-113).*

**What it is and what it is made from.** Two flat bars on the rear right post that the enclosure screws to. Galvanized steel flat bar 40 x 6 mm, 340 mm long.

**How to make it.**

1. Cut two lengths; round the corners.
2. On the centre line, from the street end: two 11 mm holes at 230 and 280 mm, countersunk on the outer face for M10 countersunk bolts; two 5 mm holes at 40 and 300 mm, tapped M6.

**How it fits the parts next to it.** The rails lie level on the rear right post's outer face, centred 1,520 and 1,780 mm above the slab, with the bolt heads flush; the enclosure's back lies flat on both (Figure 31).

**Check before moving on.** A straight edge across both rails touches all along.

### 3.12 Sensor arm (make 1)

![Figure 24. Making sketch of the sensor arm](../cad/drawings/CSH-DWG-112.png)

*Figure 24. Sensor arm making sketch (CSH-DWG-112).*

**What it is and what it is made from.** The bracket that holds the temperature and humidity sensor outside the mist zone. Galvanized equal angle 40 x 40 x 4 mm, 375 mm long.

**How to make it.**

1. Cut 375 mm; deburr.
2. Upright leg: two 9 mm holes 20 and 50 mm from the post end, 22 mm below the top.
3. Flat leg: one 9 mm hole 325 mm from the post end, 24 mm out from the back of the upright leg.

**How it fits the parts next to it.** The upright leg lies flat on the street face of the front right post, top 2,420 mm up, 75 mm on the post and 300 mm beyond it; two M8 bolts through the post. The shield hangs under the arm's end on one M8 bolt (Figure 32).

**Check before moving on.** The arm is level and the shield's lowest plate is at least 2,266 mm above the slab.

### 3.13 Equipment plate (make 1)

![Figure 25. Making sketch of the equipment plate](../cad/drawings/CSH-DWG-114.png)

*Figure 25. Equipment plate making sketch (CSH-DWG-114).*

**What it is and what it is made from.** The plate on the rear left post that carries the pump, filter and drain valve. Galvanized steel sheet 3 mm, 320 x 630 mm.

**How to make it.**

1. Cut the sheet; round the corners.
2. Measured from the left edge (seen from inside the canopy) and from the bottom edge: two 11 mm holes at 130 across, 40 and 600 up; one 12 mm cable hole at 155 across, 590 up, with a grommet.
3. Lay the pump (90 to 290 across, 430 to 570 up), the filter bracket (centre 240 across, bracket 310 to 350 up) and the drain valve (10 to 100 across, 250 to 320 up) on the plate, mark their holes through their feet and drill to suit.

**How it fits the parts next to it.** The plate lies flat on the street face of the rear left post, bottom edge 750 mm up, with 90 mm beyond the post's outer face; two M10 bolts through the post (Figure 33).

**Check before moving on.** With the parts laid on it, the drain valve is the lowest of the three and sits directly under where the down pipe comes down.

### 3.14 Tank stop cleats (make 2)

![Figure 26. Making sketch of the tank stop cleat](../cad/drawings/CSH-DWG-115.png)

*Figure 26. Tank stop cleat making sketch (CSH-DWG-115).*

**What it is and what it is made from.** Two short angles anchored to the slab against the tank's foot. Galvanized equal angle 50 x 50 x 5 mm, 60 mm long.

**How to make it.** Cut two 60 mm lengths; drill one 11 mm hole in the flat leg at mid-length, 32 mm out from the back of the upright leg.

**How it fits the parts next to it.** On the canopy side of the tank, 70° apart round it, upright legs touching the tank's foot, one M10 anchor each (Figure 35).

**Check before moving on.** The tank cannot slide toward the canopy's centre.

### 3.15 Shade fabric (bought, made to size)

![Figure 27. Outline of the shade fabric](../cad/drawings/CSH-DWG-116.png)

*Figure 27. Shade fabric outline for the maker (CSH-DWG-116), drawn laid flat.*

**What it is and what it is made from.** Knitted HDPE shade cloth, about 90 % UV block, made to order: 3,000 mm along the curb by 2,419 mm down the slope, with a 1,020 x 670 mm notch at the middle of the rear edge for the panel. Reinforced hem all round, including the notch, with brass or stainless eyelets about every 300 mm and at every corner, and lacing cord.

**How it fits the parts next to it.** It lies over the frame; each eyelet is laced round the tube below it. The notch's sides lace round the purlins and its front edge round the panel bearer, between the L-feet; the panel covers the notch. It is fitted last (step 17), only when forecast gusts are below 15 m/s, and taken off before storms by unlacing, in 15 minutes or less (R10).

**Check before moving on.** On delivery, lay it out and measure it against Figure 27.

### 3.16 Wiring and water circuit

![Figure 28. Block-level wiring](05-build-plan/wiring.png)

*Figure 28. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules are wired together.*

![Figure 29. Water circuit](05-build-plan/water.png)

*Figure 29. Water circuit from the tank to the nozzles and the drain.*

Wire it like this, with stranded copper and a ferrule on every screw terminal:

1. Solar panel to the charge controller's panel input: 2.5 mm², inside the rear beam and the rear right post.
2. Charge controller to the battery, through the 15 A fuse at the battery terminal: 4 mm².
3. Battery to the fuse block: 4 mm². Fuse block to the controller board: 0.75 mm², 1 A fuse.
4. Pump driver to the pump: 2.5 mm², 7.5 A fuse; valve driver to the drain valve: 0.75 mm², 2 A fuse. Both cables run inside the rear beam and the rear left post and come out through the equipment plate.
5. Temperature and humidity sensor: 4-core 0.5 mm² screened cable, about 7 m, with the I2C bus extender board at each end.
6. PIR sensor: 3-core 0.5 mm², about 6 m. Tank level switch: 2-core 0.5 mm², about 9 m.

Water: tank outlet to the filter inlet, filter outlet to the pump inlet, both with clamped potable-grade hose; the pump outlet joins the down pipe through a tee, the loop runs from the top of the down pipe, and the normally open drain valve sits at its bottom. The vacuum breaker sits on a tee in the front run, the loop's highest part.

**Check before moving on.** Every wire continues end to end and is labelled; with the battery disconnected, nothing reads short to the enclosure.

### 3.17 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Solar panel and mounting kit (line 5).** 100 W monocrystalline, about 1,000 x 670 x 35 mm, Vmp about 18 V; two aluminium rails about 770 mm, four L-feet and four end clamps for a 35 mm frame. The L-feet stand on the bearer and the rear beam on M8 bolts into rivet nuts; the rails bolt to the feet 15 mm clear of the tubes (Figure 30).
- **Battery (line 6).** 12.8 V 25 Ah LiFePO4 with built-in battery management and cold-charge cutoff; fused at the terminal.
- **Charge controller (line 7).** 12 V, 10 A MPPT with a LiFePO4 profile.
- **Enclosure and controller (line 8).** Lockable IP65 box about 420 x 320 x 160 mm with moulded mounting holes outside the gasket and bosses for a gear plate; microcontroller board, MOSFET pump driver, valve driver, blade fuse block, three M20 cable glands drilled in its floor 134 mm out from the back.
- **Sensor head (line 9).** SHT4x-class temperature and humidity sensor in a multi-plate radiation shield with a top mounting plate; I2C bus extender pair; PIR presence sensor with a small bracket (two M5 rivet nuts under the front beam). No camera or microphone.
- **Pump (line 10).** 12 V diaphragm pump, about 7 bar, about 60 W, with pressure switch.
- **Filter (line 11).** 5 µm cartridge in a clear housing, inlet strainer and check valve.
- **Mist line (line 12).** About 12 m of 9.5 mm (3/8 in) misting line, 6.5 mm bore, slip-lok tees and elbows, eight 0.4 mm brass anti-drip nozzles, 18 hanger clips.
- **Tank (line 13).** 120 L opaque food-grade tank with lockable lid and bottom outlet, low-level float switch, ratchet strap.
- **Drain valve and vacuum breaker (line 14).** 12 V normally open solenoid valve with about a 3 mm orifice; air admittance valve.
- **Hose and cable (line 15).** Potable-grade hose and clamps, UV-stable outdoor cable, grommets.
- **Fixings (line 16).** Galvanized or stainless: 8 M12 x 110 and 8 M10 x 100 through bolts with nyloc nuts; 16 M16 anchors (line 4) and 2 M10 anchors; 36 M8 x 16 bolts into rivet nuts; 4 M10 countersunk bolts; 3 M8 bolts with nuts for the arm and shield; 2 M10 bolts for the equipment plate; M6 and M5 screws; washers; lacing cord.

## 4. Putting it together

In each picture the parts already fitted are grey and the parts being fitted are in colour, with an arrow showing the way they go in. Bolts are tightened only where a step says so; until then they are snug.

### Step 1: base plates and anchors on the slab

![Step 1](05-build-plan/step-01.png)

Set out the four post centres from Figure 2 and check both diagonals are 3,655 mm, give or take 5 mm. Using each base plate as a template, drill the slab for the M16 anchors to the anchor maker's depth and set them. **Hold point:** safety stop S1.

### Step 2: posts and base cleats

![Step 2](05-build-plan/step-02.png)

Two people stand each post on its plate; fit the two base cleats over the anchors and the two M12 bolts through cleat, post and cleat. Plumb the post both ways, prop it, then tighten the M12 bolts and the anchor nuts to the anchor maker's torque. **Hold point:** safety stop S2.

### Step 3: head cleats onto the post tops

![Step 3](05-build-plan/step-03.png)

One cleat each side of each post top, flat legs flush with the top; one M10 bolt through both and the post, snug.

### Step 4: long beams onto the posts

![Step 4](05-build-plan/step-04.png)

With the rivet nuts already set, two people lift each beam onto its two post tops, 100 mm overhanging each post, and fit the M8 bolts up through the head cleats. Check the beams are parallel (2,350 mm between centres at both ends), then tighten the head cleat bolts. **Hold point:** safety stop S3 for all work at height from here.

### Step 5: knee braces

![Step 5](05-build-plan/step-05.png)

Lower end flat on the post's inner face with the M10 bolt through the post; upper end flat under the beam with the M8 bolt into its rivet nut. Tighten both.

### Step 6: frame cleats onto the long beams

![Step 6](05-build-plan/step-06.png)

Fit the eight cleats on the long beams' inner faces (four 40 mm for the end beams, four 30 mm for the purlins), one M8 bolt each, finger tight. Fit the bearer's two 30 mm cleats on the purlins' inner faces now, on the bench.

### Step 7: end beams and purlins

![Step 7](05-build-plan/step-07.png)

Drop each between the long beams against its cleats, ends flat on the beam faces, and fit one M8 bolt per cleat into the tube's rivet nut. Check the tops of the end beams and purlins are level with each other; then tighten all the frame cleat bolts.

### Step 8: panel bearer

![Step 8](05-build-plan/step-08.png)

Fit the bearer between the purlins on its two cleats, its front face 1,685 mm behind the front beam's inner face; one M8 bolt per cleat.

### Step 9: mist line loop, clips, nozzles and vacuum breaker

![Step 9](05-build-plan/step-09.png)

Screw the 18 hanger clips on with M5 screws: six on each long beam's inner face and three under each end beam. Push the line into the clips as one loop 70 mm inboard of the long beams and directly under the end beams; fit the eight nozzle tees (350 and 1,050 mm each side of centre on the front and rear runs), the vacuum breaker tee on the front run 150 mm right of centre, and the down pipe at the rear left corner. Set the clips on the rear run so the line falls slightly toward the down pipe. Leave the nozzle tips out until the first flush (safety stop S6).

### Step 10: L-feet and panel rails

![Step 10](05-build-plan/step-10.png)

Two L-feet on the bearer and two on the rear beam, 300 mm each side of centre, on M8 bolts into the rivet nuts. Bolt the rails to the feet, parallel to the slope, 15 mm clear of the tubes (Figure 30).

![Figure 30. Joint 8: rail, L-foot and end clamp on the rear beam](05-build-plan/joint-08.png)

*Figure 30. The rail stands on the L-foot 15 mm above the rear beam; the end clamp holds the panel's rear edge, level with the roof's rear edge.*

### Step 11: solar panel onto the rails

![Step 11](05-build-plan/step-11.png)

Two people lift the panel onto the rails, its rear edge level with the roof's rear edge, and fit the four end clamps. Cover the panel or leave its lead unplugged until section 6 allows.

### Step 12: enclosure rails and enclosure

![Step 12](05-build-plan/step-12.png)

Bolt the rails to the rear right post's outer face with the M10 countersunk bolts, nuts on the inner face. Screw the enclosure to the rails with four M6 screws from inside, through its moulded holes. Fit the charge controller and controller board on the gear plate; the battery goes in later (stop S4), strapped to the floor with two straps.

![Figure 31. Joint 10: enclosure on its rails](05-build-plan/joint-10.png)

*Figure 31. The rails bolt through the post with flush heads; the box lies flat on them; the cable bundle leaves the post below the box and enters a gland.*

### Step 13: sensor arm, shield and PIR

![Step 13](05-build-plan/step-13.png)

Bolt the arm to the street face of the front right post (two M8 through bolts, nuts inside); hang the shield under the arm's end on one M8 bolt. Fit the PIR's bracket under the middle of the front beam on two M5 screws into rivet nuts, the lens facing the waiting area.

![Figure 32. Joint 11: sensor arm and shield](05-build-plan/joint-11.png)

*Figure 32. The arm on the post's street face; the shield hangs 300 mm beyond the post, outside the roof.*

### Step 14: equipment plate, pump, filter and drain valve

![Step 14](05-build-plan/step-14.png)

Bolt the plate to the rear left post's street face with two M10 bolts, nuts on the back face. Fit the pump, filter and drain valve on it. Connect the bottom of the down pipe to the valve's inlet and the tee to the pump outlet.

![Figure 33. Joint 12: equipment plate](05-build-plan/joint-12.png)

*Figure 33. The down pipe comes down beside the post into the drain valve; a tee takes the pump's outlet into it.*

![Figure 34. Joint 9: mist line clip and nozzle](05-build-plan/joint-09.png)

*Figure 34. The line hangs in clips on the beam's inner face, 70 mm inboard and 35 mm below the beam; nozzles point down.*

### Step 15: tank, stop cleats and strap

![Step 15](05-build-plan/step-15.png)

Anchor the two stop cleats (one M10 anchor each) where Figure 2 shows, stand the tank against them, and pass the ratchet strap round the tank and the post at 400 mm. Tension it until the tank is pulled against the post.

![Figure 35. Joint 13: tank strap and stop cleats](05-build-plan/joint-13.png)

*Figure 35. The strap holds the tank to the post; the stop cleats stop it sliding away.*

### Step 16: cables and hoses

![Step 16](05-build-plan/step-16.png)

*Cables run inside the posts and beams: the sensor and PIR cables through the front beam and the right end beam, the panel cable through the rear beam, all down inside the rear right post to the enclosure; the pump, valve and level switch cables through the rear beam and down the rear left post.*

Pull each cable through with a draw wire before connecting anything, a grommet at every hole and a drip loop below every gland. Connect the hoses tank to filter to pump with clamps. Wire the enclosure as Figure 28 with the battery out and its fuse out. **Hold point:** safety stops S4 to S7 before power or water.

### Step 17: shade fabric, last, in calm weather

![Step 17](05-build-plan/step-17.png)

Only when forecast gusts are below 15 m/s. Lay the cloth over the frame from the street side, notch round the panel; lace every eyelet round the tube below it, working from the corners in, evenly tight. **Hold point:** safety stop S8.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of CSH-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Frame square, plumb and tight | R10, R14 | Diagonals, a level on every post, a spanner on every bolt | Diagonals within 5 mm; posts plumb within 5 mm over their height; nothing moves |
| Headroom | R2 | Tape from the slab to the brace ends, nozzles, clips and PIR | 2,200 mm or more everywhere inside the posts (2,223 mm expected at the rear braces) |
| Clear floor | R1 | Measure between the posts and mark the wheelchair space | 2.72 x 2.27 m clear; a 0.8 x 1.2 m space beside the bench |
| Cloth on and off | R10 | Time one person unlacing and relacing the cloth | 15 minutes or less each way |
| Line holds pressure | R7, R9 | Line flushed, nozzles fitted, pump run with the drain valve held closed | No leak at any fitting at 7 bar for 10 minutes |
| Nozzle flow | R7 | Collect one nozzle's spray in a bag for 60 s | 4 L/h, give or take 0.5, or record the value |
| Line drains | R9 | Stop the pump and time the flow at the valve outlet | The line empties within 5 minutes (about 30 s expected) |
| Activation logic | R6 | Bench test with the sensor warmed and dried, the PIR covered and uncovered, the float switch lifted | Mists only above 32 °C, below 60 % RH, with presence in the last 2 minutes and the tank above low level; stops within 60 s of any condition failing |
| Battery protection | R12 | With the battery in, check the 15 A fuse and the BMS cold-charge cutoff with the maker's method | Fuse rated 15 A; no charge current below 0 °C |
| Charging | R8 | Panel connected in sun; read the charge controller | It charges the battery at its LiFePO4 profile |
| Nozzle and filter service | R16 | Time removing and refitting one nozzle by hand and the filter cartridge | Nozzle 15 minutes or less without tools; filter 10 minutes or less |
| Heaviest lift | R17 | Weigh a front post before fitting | 40 kg or less (21 kg expected) |
| No camera or microphone | R11 | Inspect the parts fitted | None present |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before drilling the slab.** The site owner's written permission; the slab is checked for buried services with a scanner; the slab and anchor type are confirmed for about 2.8 kN factored per anchor by someone able to judge it; dust masks and eye and ear protection on.
- **S2. Before standing the posts.** Two people per post; props ready; nobody under a post being raised; anchors set and their nuts on.
- **S3. Before any work at height.** Stable ladders or a platform on level ground, a second person at the foot; beams lifted by two people; tools on lanyards; the area under the work coned off.
- **S4. Before the battery goes in.** Battery voltage about 12.8 to 13.4 V, no swelling or damage, the maker's datasheet in hand; 15 A fuse out; polarity of every power lead checked with a meter, not by colour.
- **S5. Before the battery fuse goes in.** No short from any rail to the enclosure; the pump and valve drivers off; panel unplugged. First charge attended, lid open, battery temperature checked; stop if it passes 45 °C.
- **S6. Before the line is pressurized.** Potable water only; every fitting pushed fully home and clipped; nozzles out for the first flush; eye protection on; the drain valve opens when the pump stops. Never open a fitting until the line is depressurized.
- **S7. Before misting with anyone nearby.** The tank cleaned, disinfected and filled with fresh potable water; the line drained after every run; a written hygiene routine (daily drain and refill, weekly disinfection) and a named responsible person (at a market lane, the market operator's manager); no misting if any of this has lapsed.
- **S8. Before the cloth goes on.** Forecast gusts below 15 m/s (54 km/h) for the time it will be on; every frame bolt tight; someone named to take it off before storms.
- **S9. Before any public use (outside this plan).** An engineer's check of the slab and anchors at the site; the asset owner's permission; a hygiene plan accepted by the environmental health authority of the city or county where the site stands (a market lane is the first site type); signs that the mist is not drinking water or a medical service.

## 7. Tools, skills and workspace

**Tools.** Metal cutting saw or angle grinder with cutting discs; bench or pillar drill and a hand drill, drills 5 to 18 mm, a step drill, countersink, M6 tap; hammer drill and masonry bits for the M16 and M10 anchors; hand rivet nut tool for M8 and M5 steel rivet nuts; heavy bench vice and a length of tube for bending the brace ends; files and a deburring tool; spanners and sockets 8 to 24 mm and a torque wrench; spirit level, plumb line, 5 m tape, chalk line and string; two stable stepladders or a mobile platform; ratchet strap; wire strippers, ferrule crimper, soldering iron and multimeter; a bucket and stopwatch for the nozzle check.

**Skills.** No certified trade is needed for the frame: marking out, cutting, drilling and bolting steel, setting rivet nuts and anchors, and safe work at height with a second person. Electrical work is all extra-low voltage (12.8 V nominal, under 22 V from the panel); the battery needs care. Anchoring to a public slab and the water hygiene plan need the site owner's and the health authority's agreement.

**Workspace.** A bench with a vice for the steel parts; a level working area at the site at least 5 x 4 m that can be coned off; shade and water for the team; a dry, non-combustible place to keep and first charge the battery.

**Personal protective equipment.** Safety glasses, hearing protection and gloves for cutting and drilling; a dust mask for drilling concrete; safety boots; hard hats while the frame is overhead; no gloves near a turning drill.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 117 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/CSH-DWG-101` to `CSH-DWG-116`.
- General arrangement: `cad/drawings/CSH-DWG-001.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (CSH-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; headroom [B2], [B3], mist line [C7], wind and anchors [G13], [G14], rivet nuts [G15], masses [G1], [H1], fixings [H2], cost [J1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (CSH-DDR-003), with CSH-DDR-001 and CSH-DDR-002; open items in `docs/06-design-decisions.md` (CSH-DEC-001).
- Requirements: `docs/03-requirements.md` (CSH-REQ-001 v0.5).
