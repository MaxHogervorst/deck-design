# Current published design brief

8 November 2026 Auckland. This brief supersedes conflicting historical tread, splice and quantity schedules. The website reflects this pine-box development plan; the two structural connection details below remain unfinished. Publication is not a construction release.

## Decisions resolved

| Item | Current decision |
|---|---|
| Geometry | Main 6600 × 2600; rebuilt 900 × 1970; tread 6600 × 400 mm. Retain selected deck/tread surfaces about +500/+250 mm. |
| Main/rebuilt | Conventional timber piles, double 140 × 45 SG8 bearers, 140 × 45 SG8 joists. New rear support avoids depending on the unknown retained bearer. |
| Tread | One-layer pine box directly bearing on low concrete supports, with DPC and positive stainless restraint. No short timber piles, drop-cleats or fabricated heads. |
| Tread timber | 140 × 45 SG8, minimum H4 for this clear-but-close-to-ground exposure; doubled long rails, 21 crosspieces. H5 graded framing is an acceptable supply route. Product treatment instructions govern cuts. |
| Long member joints | Continuous 6600 mm plies cut from 7200 mm stock remove both main bearer splice locations and all four proposed tread rail-ply seams. |
| Boards | Confirmed 32 mm pine, approximately 80 mm wide. Main/tread rows along frontage; rebuilt boards along 1970 mm depth as working layout. Actual width/moisture governs gaps/rips. |
| Finish | Natural treated pine, exposed front rail, no added fascia or paint/stain in the base plan. Finished tread remains 400 mm deep. Nominal 78 mm opening below the rail; neatly formed concrete may be visible obliquely. |
| Landscaping | Buried foundations may extend beneath path/lawn/garden. Keep soil/turf/mulch away from timber and fixings; do not bank soil against the rail to hide the opening. |
| Process | One pre-build discussion, then one owner build sequence. No builder inspections during construction added. No owner preference questions needed now. |

Cypress Sawmill lists 140 × 45 SG8 H3.2 and H5 in 7.2 m lengths: a real procurement route, not a stock reservation. H4 SG8 is documented, but its 7.2 m availability is unconfirmed. Quote actual grade, treatment, lengths and delivery together. Longer stock removes splice design; it does not resolve the low anchor connection.

**Main pile procurement basis:** use the documented Pinepac route: six 1.5 m, A-marked H5 anchor piles and ten 750 mm ordinary H5 house piles, nominal 125 square, subject to final site/cut lengths. Its published anchor range starts at 1.5 m; do not invent a 1.2 m anchor SKU. The 750 mm ordinary product is made to request. At the present illustrative 800/350 mm embedments and +186 mm pile top, required cut lengths are 986/536 mm before any datum change. This is a supply/cutting basis, not an instruction to cut an untreated buried end or ignore grade marks. Keep the supplied treated bottom intact and follow the manufacturer's top-cut treatment instructions.

Pinepac documents a 150 mm finished-ground processing restriction. With pile top +186 and a connection's lowest surface processing d mm below that top, finished ground at that pile must be **no higher than +(36−d) mm**. For example d80 implies ground at or below −44, not a blanket 125 mm excavation everywhere. Determine d from the actual complete connector drawing and establish drainage before adopting a local ground change. The final main anchor detail must satisfy this geometry; the pile's top alone does not prove it.

## Geometry and assembly

Retain the main/rebuilt support and joist positions in DESIGN_RESOLUTION.md: 12 main plus four rebuilt piles, including six candidate anchors. Main bearers Y350/2250; rebuilt Y−800/−1795. **Delete the main bearer seams at X3910.** Member-table comparisons remain favourable; prior force/deflection calculations are preliminary rather than a complete structural pass.

Tread local coordinates: X along frontage; y0 rear, y400 front. Rails occupy y0–90 / y310–400; crosspieces are **220 mm long**. Seven candidate crosswise concrete supports each bear directly under both rails, at X300/1300/2300/3300/4300/5300/6300; maximum 1000 mm intervals.

Nominal tread section, mm above adjacent finished garden/path datum:

```text
 +250  walking surface  ────────────── 32 pine boards
 +218  frame top       ┌─────────────┐
                      │  140 frame  │  crosspieces flush with double rails
  +78  frame underside └─────────────┘
  +76  concrete top    ── 2 mm DPC ──
    0  garden/path datum; actual levels and drainage to establish
       concrete extends down to suitable bearing ground
```

Crosspiece centres: 22.5 + 380i for i0…17, plus 6577.5; add board-joint sisters at 3277.5/3322.5. Maximum support interval 380 mm. At the X3300 board seam, each board end has its own support; cuts allow the actual butt gap. No 6.6 m supplied decking length is assumed.

**Crosspiece assembly:** attach crosspieces to the inner 45 mm rail plies before adding outer plies. NZS 3604 Table 7.5 curtailed-joist end-fixing basis: **three 100 × 3.75 mm stainless hand-driven end nails per end**, 126 base nails. Through one 45 mm ply, nominal penetration is 55 mm; through both it would be only 10 mm. Nail placement must meet splitting/end/edge requirements and avoid ply-stitching nails.

Built-up rails/bearers retain the reviewed basis: two nail rows, maximum 250 mm centres along each row, 90 × 4 mm stainless nails, alternating driving faces, with final connection exclusions and actual nail geometry checked. The standard permits maximum 270 mm spacing for 45 mm plies and requires at least 33.75 mm penetration into the final ply; 90 mm length gives nominal 45 mm. Ordinary pile, joist, rim and blocking schedules are in DECK_FIXINGS_CHECK.md. Ordinary nails do not replace rated anchor/uplift connections.

## Fresh checked stock plan

Includes **4 mm kerf per cut plus 5 mm end trim per stock piece**. Sound usable stock assumed; defects and final connection changes additional. Keep treatment classes separate.

| Main/rebuilt H3.2 SG8 140 × 45 stock | Cuts per stock piece, mm |
|---|---|
| 4 × 4800 | 4525 + 240 |
| 9 × 3600 | 2510 + 240 + 240 |
| 8 × 3000 | 2510 + 335 |
| 4 × 7200 | 6600 + 240 + 290 — continuous bearer plies |
| 1 × 4200 | 900 + 900 + 900 + 900 + 335 |
| 1 × 7200 | 6600 + 335 — front rim |
| 1 × 6000 | 5700 + 240 |
| 1 × 6000 | 16 × 335 |
| **Total** | **29 stock lengths / 127.8 lm; installed 119.42 lm** |

Four 7.2 m bearer lengths replace four 4.2 m plus four 3.0 m pieces while supplying the same eight blocks. **The total stock length is unchanged**, with both splice locations removed.

| Tread minimum-H4 SG8 140 × 45 stock | Cuts per stock piece, mm |
|---|---|
| 4 × 7200 | 6600 — continuous rail plies |
| 1 × 4800 | 21 × 220 crosspieces |
| **Total** | **5 stock lengths / 33.6 lm; installed 31.02 lm** |

At actual board width 80 / gap 5 mm, the exact-width example is: main 31 rows with two 65 mm edge rips; rebuilt 11 rows with two 65 mm edge rips; tread five rows with two 70 mm edge rips. Measure supplied boards before ripping; **5 mm is an example, not an installation gap for unidentified wet/dry boards**. Installed row lengths total 259.27 lm before joint gaps, cuts and defects. Tread-only buying example: ten 3.6 m boards give ten approximately 3.3 m pieces, if that product/length exists: 36 lm bought for about 33 lm installed.

Recounted base screw positions: 1302 main + 132 rebuilt + 210 tread = **1644**. A 2000-screw planning allowance excludes structural fixings. Working screw basis: 75 mm 316 stainless; gross penetration through 32 mm decking is 43 mm before tip allowance. Gauge, effective thread penetration, pilots and end/edge rules follow actual board/screw instructions.

**Cost:** quote 127.8 lm main H3.2 framing and 33.6 lm minimum-H4 tread framing separately, plus 16 correctly classified piles, boards, concrete, structural hardware and delivery. Framing subtotal is `127.8 × main rate + 33.6 × tread rate`. No current all-in quote is available. Do not reuse old budgets or apply an H3.2 rate to H4/H5. NZ Timber's H4 listing mixes rough-sawn and 140 × 45 descriptions, so its dimensions/price are not accepted for this cut plan.

## Specific tread restraint candidate — geometry checked, capacity open

Pryda **PBB8515/SS**: 5 mm 304 stainless, 100 mm upright, 50 mm foot, 50 mm wide. The upper timber hole is 75 mm above the concrete-side base. With 2 mm DPC under the rail and the angle foot directly on concrete, the bolt centre is **73 mm above timber bottom / 67 mm below top**. It fits without a projecting bracket or a bolt close to the lower timber edge. The lower upright hole is **not included** in this proposed fixing. Use the actual drawing's Ø14 holes; the website's generic table differs.

Development arrangement: one angle on each inner rail face at each support station; a stainless M12 through-bolt through both rail plies with 50 × 50 × 3 washers, plus a separate matched stainless concrete anchor. A 130 mm bolt has geometric room for 90 mm timber, 5 mm bracket, washers, nut and exposed threads; actual grade/thread/grip is part of the capacity selection. Vertical walking load travels directly into concrete bearing.

Trial head geometry **400 mm along X × 360 mm across y20–380** gives each rail 70 mm transverse bearing. Feet project inward; concrete anchor axes approximately y115/285 give 95 mm to the nearest head edge. Bracket X candidates 300/1300/2400/3200/4300/5200/6300 clear the crosspieces; three are offset 100 mm from support centres. Minimum longitudinal anchor edge distance in that trial head is nominally 100 mm. These are useful dimensions to assess, **not an approved footing size, anchor edge distance, foundation depth, reinforcement detail or concrete volume**.

Candidate counts: 14 angles, 14 timber through-bolts, 14 concrete anchors **if this exact arrangement is justified**. Pryda's PDS publishes geometry and leaves assembly capacity to design; it gives no pre-rated pine-tread connection. Check bracket bending/prying, single-upper-hole use, wet SG8 bolt resistance, both lateral directions, uplift/overturning, concrete-anchor breakout and foundation/soil together. No arbitrary Ramset SKU or Euro C24 rating is adopted. This remains one bounded technical task, not an order.

## Genuinely remaining work

| Item | Exact scope / route to closure |
|---|---|
| **Main low anchor + joist hold-down detail** | Complete six actual 125-square pile / doubled bearer / adjacent joist assemblies and overall bracing transfer. MiTek 12KNH is the stainless candidate: check both-ply transfer, scarf/plate fit and lowest processing elevation against the selected pile instructions. Rebuilt continuous joists have calculated uplift demand requiring a rated wet-service hold-down. Continuous bearers eliminate the former splice task. |
| **Tread support + restraint capacity** | Check the explicit candidate above; issue footing, concrete, any reinforcement and matched anchor schedule. Include the 2.7 kN stair point action, lateral/overturning actions and the independent-tread line-action interpretation. The recognised support method and preliminary member-demand screen do not establish capacity. |
| **Physical site facts** | Establish bearing ground, actual finished path/garden levels and a drainage route during the pre-build site discussion; check existing-foundation conflicts. Keep the nominal 78 mm opening real after landscaping. Conditional main footing quantities are not soil verification. |
| **Procurement facts** | Confirm graded/treatment-marked long stock, pile processing instructions, actual pine board width/moisture/profile, compatible fixings and delivered prices with the merchant. Owner already answered that these were unknown; no repeat questionnaire. |

Selected levels and no-handrail preference remain. This progress does not establish access compliance; the existing finding in DESIGN_RESOLUTION.md remains recorded without reopening the owner's height decision here.

## One owner sequence after the complete details are settled

1. Settle support/fixing drawings in the single pre-build discussion; order actual products/lengths.
2. Mark all datums/supports together and establish agreed drainage/landscaping levels.
3. Excavate all foundations; set piles, tread forms and levels; place concrete to the agreed detail.
4. Observe concrete/anchor curing and installation requirements before loading/drilling.
5. Build main/rebuilt framing. Assemble tread inner rails/crosspieces, add outer plies, seat on DPC and complete designed restraints.
6. Complete concealed fixings and owner checks against agreed drawings, then lay boards and finish landscaping clear of timber.

## Evidence and reproducibility

- `python calculations/current_takeoff.py`; results in calculations/current_takeoff.json. Checks all cuts, kerfs, counts, support intervals and bracket/crosspiece conflicts. **Not a structural resistance calculation.** Earlier structural_check.py/results.json retain their stated historical scope.
- NZS 3604:2011 §§2.4.4.7, 6.5.2, 6.9.3, 6.12.7 and Table 7.5: https://moodle.unitec.ac.nz/pluginfile.php/358840/mod_resource/content/1/NZS-3604.2011%20.pdf .
- BRANZ Bulletin 611 §§5.1.3–5.1.4, low concrete support/treatment method: https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf .
- Graded long stock ranges: https://www.cypress-sawmill.co.nz/square-posts-beams . Stock/price still require a quote.
- Product-specific pile processing and available lengths: https://pinepac.co.nz/anchor-piles/ and https://pinepac.co.nz/house-piles/ . Do not transfer these processing instructions to another brand.
- Pryda Builders Brackets PDS, October 2024, pp2–3, geometry and capacity responsibility: https://www.pryda.co.nz/wp-content/uploads/NZ-Builders-Brackets-Range-PDS.pdf .
- Existing member-table/fixing/demand records: DECK_FIXINGS_CHECK.md and STRUCTURAL_CALCULATION_REVIEW.md. Old tread-cleat results do not design this tread's connection.

The published page contains the current plan, materials, drawings and build sequence. No historical working documents or research PDFs are embedded. No supplier or designer has been contacted.
