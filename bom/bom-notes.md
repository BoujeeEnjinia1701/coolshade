# BOM notes

Costs are indicative USD prices for a single prototype, estimated in September 2026 without supplier quotes. Every line is priced and has a supplier type. Line numbers match the exploded view (`media/exploded.png`) and the component table in the design precis (CSH-PRC-001). Line 16 has no callout.

- Parts total: an estimated $882.00, against the $775 value-engineering target (`budget_usd` in `project.yaml`, a hypothetical control target; $107.00, 13.8 %, over). The target was set at $775 on 2026-09-25 (CSH-DDR-002; it was $700). `budget_usd` is not changed; savings worth trying are in CSH-DEC-001. See CSH-CAL-001, section J.
- Design for construction (CSH-DDR-003, 2026-09-30), +$109: cleats, rivet nuts, end caps and panel bearer (line 2, +$15); cloth notch (line 3, +$3); base cleats (line 4, +$24); panel mounting kit (line 5, +$20); enclosure rails and battery straps (line 8, +$3); sensor arm and I2C extender (line 9, +$8); equipment plate (line 10, +$6); line clips and longer line (line 12, +$5); tank level switch and stop cleats (line 13, +$7); fixings (line 16, +$18).
- TRL 3 changes: the mist line is now a closed loop of about 11 m (line 12, +$5); the tank has a strap and two small anchors (line 13, +$10); a vacuum breaker lets the line drain past its anti-drip nozzles (line 14, +$8).
- Recommendations accepted (CSH-DDR-002): the battery is 25 Ah instead of 20 Ah for energy margin (line 6, +$15).
- The steel lines (1, 2 and 4) come to about $1.61/kg for about 167 kg including cutting, drilling and galvanizing, which looks low for small quantities. Cost is at risk of rising until quoted.
- Not included: site survey, permits, an engineer's check of the slab and anchors, concrete footings where no slab exists, the existing bench, water, and labor.
- Items 6 and 7 sit inside the equipment enclosure (item 8).
