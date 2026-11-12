"""Render the single current build guide, CSV and three drawings from design.json."""
from pathlib import Path
from html import escape as E
import json, csv, io, re
root = Path(__file__).resolve().parents[1]
d = json.loads((root / 'design.json').read_text())
cv = d['concrete_geometry_only']
sc = d['screens']
t = d['tread']
deck = d['decking']
pile_x = d['main_pile_X_mm']
DATE = '11 November 2026'
# category, item, qty, unit, line price, store, comment, kind, url
# Prices read 12 November 2026, GST included, Auckland stores only. Each line is the cheapest posted price. Delivery is extra.
rows = [
    ('Timber', '140×45 SG8 H3.2 framing, wet. Main deck and rebuilt strip', '102', 'm', 17 * 70.91, 'Bunnings', '17×6.0 m at $70.91. Green, not kiln dried. 7.2 m is not listed, so splice each bearer ply over a pile. The 4.8 m length is $58.42 and works out dearer per metre', 'posted', 'https://www.bunnings.co.nz/140-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-6m_p0616262'),
    ('Timber', '190×45 SG8 H3.2 for the one long bearer bay', '9.6', 'm', 2 * 86.50, 'Bunnings', '2×4.8 m at $86.50. Cut each one in half for the four 2.39 m plies. A 6.0 m length is $108.12 and leaves more waste. Kiln-dried 6.0 m is $131.34', 'posted', 'https://www.bunnings.co.nz/190-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-4-8m_p0616614'),
    ('Timber', '150×50 SG8 H4 for the two steps. 140×45 H4 is not listed', '72', 'm', 72 * 17.11, 'Bunnings', 'Special order at $17.11/m. Mitre 10 lists 150×50 H4 from $11.96/m, but that is N2 grade, not SG8', 'posted', 'https://www.bunnings.co.nz/150-x-50mm-sg8-h4-wet-sawn-treated-timber-per-linear-metre_p0276210'),
    ('Piles', '125×125 H5 pile, 1.2 m', '16', 'ea', 16 * 32.42, 'Bunnings', 'The 16 deck and rebuilt piles. $32.42. Mitre 10 is $36.50 for the same 1.2 m', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-1-2m-square-h5-anchor-pile_p0276402'),
    ('Piles', '125×125 H5 pile, 750 mm', '8', 'ea', 8 * 21.04, 'Bunnings', 'Six under the bottom step and two spare. $21.04. Most of the length gets cut off', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
    ('Decking', '88×32 H3.2 merch griptread', f'{deck["stock_lm"]}', 'm', deck['stock_lm'] * 4.55, 'Bunnings', f'{deck["stock_4200"]}×4.2 m and {deck["stock_3000"]}×3.0 m at $4.55/m. The listed price is the random-length bin. Named lengths, so the butts land on the doubled joist. Trade price is $4.33/m and needs a PowerPass', 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
    ('Fasteners', 'Decking screws 10g×65, coated for treated pine', '1500', 'ea', 3 * 75.92, 'Bunnings', f'3×500 Buildex Climacoat at $75.92. CCA decking, zone C, so stainless is not required. A 304 decking screw is about $234 for the same 1500 and is the one to take if the heads will show. {deck["base_screws"]} positions', 'posted', 'https://www.bunnings.co.nz/buildex-10g-x-65mm-climacoat-rapiddrive-treated-pine-screws-500-pack_p0417168'),
    ('Fasteners', 'Framing nails 90×3.55 galvanised jolt head', '7', 'kg', 51.98 + 26.65, 'Bunnings', '1×5 kg at $51.98 and 1×2 kg at $26.65. Hot-dip galvanised. Bearer plies and the step beams. The stainless nails only came in 4 mm', 'posted', 'https://www.bunnings.co.nz/nz-nails-90-x-3-55mm-5kg-galvanised-jolt-head-nail_p0318485'),
    ('Fasteners', 'Framing nails 100×4 galvanised flat head', '5', 'kg', 51.77, 'Bunnings', 'One 5 kg tub at $51.77. Joists, rims and the skew nails. The heads are buried, so a flat head is fine', 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-5kg-galvanised-flat-head-nail_p0318604'),
    ('Fasteners', 'Batten screws 14g×100 class 3 galvanised', '100', 'ea', 29.95, 'Bunnings', 'One box, $29.95. Step ribbons, and the rebuilt joists. Class 3, for outside', 'posted', 'https://www.bunnings.co.nz/titan-14g-x-100mm-cl3-gal-bugle-batten-screw-100-pack_p0579091'),
    ('Fasteners', 'M12×120 316 coach bolt, nut, two 50 mm washers', '2', 'ea', 2 * (4.90 + 1.25 + 2 * 3.54), 'Bunnings', 'The two rim ties. $4.90 + $1.25 + 2×$3.54 each', 'posted', 'https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
    ('Concrete', 'Ready-mix 20 MPa, small load', '2.0', 'm³', 650, 'Auckland plant', 'Not a published price. On site the figure was about $600 for the 1.1 m³ in the twelve holes. This load is still about $650 until Firth or Allied prices Point Chevalier. Firth adds $9.90/m³ fuel on top of the quote. Do not add the cement as well', 'estimate', 'https://www.firth.co.nz/temporary-fuel-surcharge'),
    ('Concrete', 'Portland cement, 20 kg. Only if mixing on site', '36', 'ea', 36 * 11.59, 'Bunnings', 'Cemix Ecostrong $11.59, used as GP cement. Four shovels of builders mix to one shovel of cement', 'alt', 'https://www.bunnings.co.nz/cemix-20kg-low-carbon-cement_p0581734'),
    ('Concrete', 'Builders mix BM20. Only if mixing on site', '2.5', 'm³', 2.5 * 126.50, 'Auckland Aggregates', '$126.50/m³ including GST. Cartage is priced by the kilometre and is not in this figure. This replaces the truck, so it is not in the total', 'alt', 'https://www.aucklandaggregates.co.nz/shop/product/577984/bm-20--builders-mix-virgin-aggregate/'),
    ('DPC', 'DPC Supercourse 500, 150 mm×30 m', '1', 'ea', 27.42, 'Bunnings', 'On every pile top. $27.42', 'posted', 'https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
    ('DPC', 'Metalex Green, 1 L', '1', 'ea', 66.00, 'Bunnings', 'On every saw cut. $66', 'posted', 'https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
]
priced = []
for cat, item, qty, unit, price, store, comment, kind, url in rows:
    priced.append((cat, item, qty, unit, round(float(price), 2), store, round(float(price), 2) if kind != 'alt' else 0.0, comment, kind, url))
posted = round(sum(r[6] for r in priced if r[8] == 'posted'), 2)
est = round(sum(r[6] for r in priced if r[8] == 'estimate'), 2)
total = round(posted + est, 2)
steps = [
    'Before you buy. Match the old deck: the new boards sit at that same 500 mm, not 500 mm above the low grass. Measure from the old boards down to the concrete path. Joists need about 330 mm of air over the path and the bearers about 190 mm. The steps are measured off the path as well, because that is where you walk. Tape that height and divide by three. If it is 500, each rise is 167. The lawn is lower and is not the step. Check the sill and the cladding. Formby Avenue is about 1.1 km from the harbour, outside the 500 m sea-spray zone, so the nails and the screws are galvanised. The two bolts stay stainless. A services reply that says no power within 10 m is not to be trusted: there is power. Mark the stormwater and the waste before any digging.',
    'Set out. String the 6600×2600 outline and the 900×1970 rebuilt strip. The steps stick out 560 mm past the front, two goings of 280. Leave the path. End joist flush, then 437 mm centres, doubled joist centred at 3956. Lines 1, 4, 5 and 6 stay. Line 2 moves 200 mm onto the grass, so the 400 hole stops at the concrete. Line 3 is 1,230 mm past the right edge of the concrete: 400 to the blue pipe, 130 to the sewage, 500 clear, 200 to the middle of the hole. Paint the marks. The six step holes go on those same lines, 560 mm out.',
    'Dig, with a spade. Every deck hole is 400×400 and 600 deep, down to firm ground, not topsoil. No 900 mm anchor holes. At 600 a shovel is enough. An auger only earns its keep past 600, and these holes do not go there. About ten minutes a hole. No hole in the concrete, no hole between the blue pipe and the sewage, and no hole edge within 500 mm of either. The 2.39 m bay is the doubled 190. Every other bearer bay stays under 1.4 m.',
    f'Concrete. One hole at a time, unless the weather is settled and every hole is open. The twelve main holes are {cv["main_12_holes_m3"]:.2f} m³, the 1.1 m³ counted on site, pile left in the hole. Rebuilt holes and the step holes bring it to about {cv["main_net_m3"]:.2f} m³. Order {cv["readymix_order_m3"]:.1f} m³ if a truck is coming, and barrow it. Otherwise builders mix dumped in front of the garage, plus cement: four shovels of mix to one of cement, a bit more cement if it looks lean, mixer hired. Fill to about 100 mm below the ground. Do not use the no-mix post-hole bags. Nothing in the hole has to be level.',
    'Cut the piles. String off the path, not the lawn. On the path the tops finish about 310 mm below the old boards, and at least 150 mm clear of the path. The grass piles stand taller. Cut square, preservative on the cut, DPC on the top.',
    'Bearers. Nail the doubled 140s and, between line 2 and line 3 only, a doubled 190 (F1). That bay is 2.39 m. Notch the underside of the 190 at each pile, no longer than the pile, so the top lines up with the 140s. Seat them and skew-nail (F2). No anchor brackets. Take out the old rear bearer and do not reuse it.',
    'Joists and rims. 17 joists of 2510: flush at each end, 437 centres, the doubled joist at 3956. Screws into a bearer go in from the side of the joist, not down through the top. Three rebuilt joists of 1880, two blocks cut at 380, and the skewed 14g screws (F4). Rims at Y0 and Y2555. Two M12 bolts where the rebuilt strip meets the deck (F6). Get the deck frame up before the steps. The step height is in mid-air until the deck is there. Offcuts can be a temporary step.',
    'Step piles. With the deck frame up, dig the six small holes, 300×300 and 400 deep, on the same X as the front piles and 560 mm out from the face. Not 600. Stand a 750 mm pile, plumb it, and concrete it. Cut it so the front beam will finish with its top about 135 mm above the path.',
    'Bottom step. Screw a double H4 ribbon to the front piles, four 14g×100 screws each (F5). Joists out from it, cut about 500, on the same lines as the deck joists. Double front beam on the small piles. Top of this framing about 135 mm above the path, so the 32 mm board finishes at about 167. A 140 does not fit over the path. Rip the bottom of the ribbon and the beam where they would touch it, leave 15 mm of air, and do not go under 120 mm deep. Do not run that ripped piece across the 2.39 m bay. In that gap the step joists are doubled and cantilever off the front bearer, and the front beam stops at the piles either side.',
    'Top step, on the bottom one. Set it back one going, 280 mm. Double ribbon screwed to the face of the front bearer (F7), short joists cut about 240, front beam packed off the bottom step so the framing top is about 301 mm above the path. The board then finishes at about 333. Tape the three rises off the path and make them equal. Do not cut a stringer. No handrail. Three rises is the limit. One more would need a rail.',
    'Boards. 28 rows on the deck, 21 on the rebuilt strip, three on each step, all along X. Butts on the doubled joist at 3956, so use the 4.2 m and 3.0 m lengths. A decking board on the face of the boundary joist, the top board over it, and a board on each riser. About 5 mm gaps on the deck and about 6 mm on the rebuilt strip. Two screws per board per joist. Preservative on every cut.',
]
fixings = [
    ('F1', 'Double bearers and the step beams', '90×3.55 galvanised jolt nails, two rows at 250 mm centres, staggered. Same on each double step beam and ribbon.'),
    ('F2', 'Pile to bearer, and the small step piles', 'Four 100×4 galvanised skew nails. Same four nails from the front beam down into each small pile.'),
    ('F3', 'Joists, rims, blocks', 'Two 100×4 galvanised nails per joist end, through the rim or into the ribbon.'),
    ('F4', 'Rebuilt joists', 'Four 100×4 skew nails and two 14g×100 screws, skewed in from the side of the joist. The point-load screen can put about 1.9 kN of uplift on one support. Ordinary carpentry, not a rated bracket.'),
    ('F5', 'Bottom-step ribbon to the front piles', 'Four 14g×100 screws into each pile, in from the side. A bolt through is fine if you would rather drill the pile. Ordinary screws, not a bracket.'),
    ('F6', 'Rebuilt strip to the main rim', 'Two M12×120 stainless coach bolts at X200 and X700, 50 mm square washers both sides.'),
    ('F7', 'Top-step ribbon to the front bearer', 'Four 14g×100 screws into the bearer face at each pile. The front of this step sits on the bottom step, packed so the rises match.'),
    ('F8', 'Face board and the two risers', 'A decking board on the boundary joist, and one on each riser. The top board laps over the face board.'),
]

def money(n):
    return f'${n:,.2f}'

md = f'''# Deck and step build guide

{DATE} · How I am going to build the 6.6 m deck and the two steps in front of it. One plan, a set-out sheet, three drawings, a bill of materials and the build order. Written for me, doing the work. It is not an engineer's design. Consent is not required: Building Act Schedule 1, exemption 24, because a fall is about 500 mm. The sheets are still drawn to AS/NZS 1100.501 and the Auckland Council AC1011 document list. They are not lodged.

## What we are building

| Part | What |
|---|---|
| Main deck | 6600×2600 mm, boards level with the old deck, about 500 mm. Two double 140×45 H3.2 bearers on 16 timber piles at Y300 and Y2510. Joists 140×45 across them, span 2.21 m. The wet-service table at 450 centres allows 2.35 m. |
| Main joists | 17 members. Flush at the end, then 437 mm centres, one doubled joist centred at 3956 for the board butts. Rims at Y0 and Y2555. No blocking. |
| Rebuilt strip | 900×1970 mm beside the house. Two 900 mm double bearers at Y−1925 and Y−800, three joists of 1880, two blocks cut at 380. Nothing runs through into the main deck. |
| Steps | Two steps, three rises, the full width of the deck, sticking out 560 mm. Going 280. Rise about 167 if the path-to-board tape is 500. Double 140×45 H4. Bottom step: a ribbon screwed to the front piles, joists out, a front beam on six small piles. Top step built on that and screwed to the bearer. Not a cut stringer. |
| Boards | 88×32 merch griptread, along X. 28 rows on the deck, 21 on the rebuilt strip, three on each step. A board on the face of the boundary joist, and one on each riser. |
| Finish | Natural, no handrail. Three rises is the limit. One more rise and it would need a rail. Lawn and path stay as they are. |

Set-out, X from the meter-box end. Piles: 62.5, 677.5, 3067.5, 3947.5, 5242.5, 6537.5 on Y300 and Y2510. Line 2 was on the path and line 3 was too close to the drains, so those two moved. The path is 960 wide, and these positions put the old line 2 in the middle of it. Tape still governs. Line 2 is 200 mm onto the grass, so the 400 hole stops at the concrete. Line 3 is 1,230 mm past the right edge of the concrete: 400 to the blue pipe, 130 on to the sewage, 500 clear, and 200 to the middle of the hole. The 130 is 870 minus 740, the two west measurements off the deck. The bay between them is 2.39 m, a doubled 190×45. The other bays stay under 1.4 m. The six step piles are on those same X, at Y3115. Rebuilt piles: X175 and X725 on Y−1925 and Y−800.

Heights. The path is where you walk and the grass is lower, so the steps are taped off the path. Deck boards +500 if that is what the old deck measures, joist top +468, bearer top +328, pile top +187. Bottom step board about +167, framing top +135. Top step board about +333, framing top +301. If the tape from the path to the deck boards is not 500, divide whatever it is by three.

## The sheets

[Sheet 1 · Foundation and framing](docs/drawings/sheet.svg) · [Sheet 2 · Section and details](docs/drawings/sheet2.svg) · [Sheet 3 · Site, levels and schedules](docs/drawings/sheet3.svg). A2, to AS/NZS 1100.501 and the Auckland Council AC1011 list. Consent is not required. These sheets are not lodged.

## Three drawings

[1 · Piles and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixings and the two steps](docs/drawings/fixings.svg)

## Foundations

16 timber piles, all the same: 400×400 holes, 600 deep. No 900 mm anchors and no brackets. 600 is deep enough that the deck is not sitting in the ground that swells. Four anchors would be more hole than this deck needs. The step has six smaller holes, 300×300 and 400 deep, plus two spare if the path is in the way.

Concrete volume leaves the pile in the hole. The twelve main holes are {cv["main_12_holes_m3"]:.2f} m³, the 1.1 m³ counted on site. With the four rebuilt holes and the step holes it is about {cv["main_net_m3"]:.2f} m³, so a truck order is {cv["readymix_order_m3"]:.1f} m³. The other way is builders mix dumped in front of the garage, plus cement, four shovels of mix to one of cement, and each hole concreted as it is dug so a shower does not fill twelve of them. Do not use the no-mix post-hole bags.

The path stays. The deck is built over it. Joists want about 330 mm of air over it and the bearers about 190 mm, so the piles clear 150 mm. No hole through the concrete. Line 2 is the one that landed on it. It moves 200 mm onto the grass. Anywhere else, slide a pile along the bearer and do not open a bay past 1.4 m.

The waste and the stormwater run together on the right of the path, the west side. The blue pipe is 400 mm past the concrete. The sewage is 130 mm past the blue one: the plan has one pipe 740 mm off the deck and the other 870 mm off the deck. Beside the deck they are about 440 to 470 mm deep, and only 240 to 270 mm deep beside the pad. The hole is 600 deep, so it goes below them. No hole edge within 500 mm of either pipe, and no hole between them. Stormwater goes out through the gate. The left of the path, the meter-box side, is clear. Orange is power, white is fibre, water is its own pipe. Dig with a spade.

### The two steps

A single 250 mm rise is too big. About 190 is the limit and 200 is a push. Two steps make three rises of about 167, and 2×167+280 comes out at 613, inside 550 to 700. No handrail at three rises.

Build the deck first. Then the bottom step, then the top step on it, set back 280 mm. Tape the rises off the path until they match. Do not cut a stringer.

The bottom framing only has about 135 mm above the path, and a 140 is deeper than that, so over the path the ribbon and the front beam get ripped. Leave 15 mm of air and at least 120 mm of timber. That ripped piece does not cross the 2.39 m bay. In that gap the step joists are doubled and cantilever off the front bearer, and the front beam stops at the piles either side. Everywhere else the grass is lower and the full 140 stays. On the full 140 the beam screen is about {sc["step_beam_util_140"]*100:.0f}%. The ripped half-bay is about {sc["step_beam_util_120"]*100:.0f}%. The small pile sees about {sc["step_pile_bearing_kPa"]:.0f} kPa on a 300×300.

The underside of that bottom step is not 150 mm clear of the path. There is no way to have that and still walk off onto the path in even rises. It is H4 because it will stay damp. The deck piles themselves do clear 150 mm.

## Shopping list

Prepared for Max Hogervorst, 18B Formby Avenue, Point Chevalier. {DATE}. Auckland prices only, read 12 November 2026, including GST. Each line is the cheapest posted price, so the store can change. Delivery is extra. The truck is not a quote. Nothing has been bought.

[Download the CSV](docs/shopping-list.csv).

'''
last = None
for cat, item, qty, unit, price, store, use, comment, kind, url in priced:
    if cat != last:
        if last:
            md += '\n'
        md += f'### {cat}\n\n| Description | Qty | Unit | Cheapest | Store | Comments |\n|---|---|---|---|---|---|\n'
        last = cat
    cell = f'[{money(price)}]({url})' if url else money(price)
    note = comment + (' Not in the total.' if kind == 'alt' else '')
    md += f'| {item} | {qty} | {unit} | {cell} | {store} | {note} |\n'
md += f'''
**Posted ${posted:,.2f} + estimates ${est:,.2f} = about ${total:,.0f} including GST.** The total uses the truck. If the holes are mixed on site, take the truck out and add the cement. The builders mix is a yard quote and is not in the number either way. Do not add the truck and the cement together.

Pack sizes are already rounded up for the nails and the screws. Pile lengths are long on purpose. No allowance for a wasted bolt, or for timber used as a temporary brace. Delivery, the mixer and carting the spoil are extra. The nails and the screws are galvanised. The two bolts stay stainless.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Main and rebuilt: {d["main_stock_lm"]} m bought, {d["main_installed_lm"]} m used. 6600 is the bearer plies and the rims. 2510 is the 17 joists. 900 is the rebuilt bearers and rims. 380 is the two blocks. 1880 is the three rebuilt joists. If 7.2 m is not in stock, splice each bearer ply over a pile and stagger the two plies.

| 140×45 H4 stock | Cuts, mm |
|---|---|
'''
for a in d['H4_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Steps: {d["H4_stock_lm"]:.0f} m bought, {d["H4_installed_lm"]} m used. 6600 is the eight long plies, two doubles on each step. 500 is the 17 bottom-step joists. 240 is the 17 top-step joists. If there is no 7.2 m H4, cut each long ply as 3950 and 2650 from 4.8 m so the joint lands on a pile. {deck["base_screws"]} screw positions, buy 1500.

## Fixings

| ID | Joint | Detail |
|---|---|---|
'''
for f in fixings:
    md += '| ' + ' | '.join(f) + ' |\n'
md += '''
## Build order

'''
for i, s in enumerate(steps, 1):
    md += f'{i}. {s}\n'
md += f'''
## Assumptions, and what I would get checked in an ideal world

We walked it on 11 November. The holes, the concrete and the two steps follow that conversation. It is still not an engineering sign-off, and there is no consent. Under 1.5 m the work is exempt. Exempt is not the same thing as the stair rules or the bracing rules being met on paper.

- **No anchor piles.** A freestanding deck needs something against racking. Four 900 mm anchors with brackets was the old default, and the ROBO preview counts bracing that way. On site, four anchors was more than this wants, and 600 mm on every pile was the call. I am following that. It is not a bracing calculation, and I am not buying the brackets.
- **The ground.** Firm clay at about 100 kPa under the topsoil. That is the usual Auckland assumption, not a test. A step pile is at about {sc["step_pile_bearing_kPa"]:.0f} kPa on a 300×300. If a hole is soft or wet at 600, that hole gets deeper or wider and it is no longer a spade job.
- **The steps.** The front beam, full 140 over a 1.30 m bay, is about {sc["step_beam_util_140"]*100:.0f}% of my bending screen under a factored point load. Ripped to 120 mm, that half-bay is about {sc["step_beam_util_120"]*100:.0f}%. The ripped piece does not cross the 2.39 m gap. The screws are ordinary screws. The bottom step does not have 150 mm clearance over the path. The rises are even. They are not a consented stair.
- **The services reply.** It said no gas and no power within 10 m. The power is there. Drain depths are approximate. Paint, spade, and move a hole rather than dig through a pipe.
- **Fixings.** Formby Avenue is about 1.1 km from the harbour, past the 500 m sea-spray line, so this is zone C. The nails and the screws are galvanised. The deck is open, so the two bolts stay 316. The decking is CCA. Do not swap in ACQ timber and keep these screws.
- **The path.** It stays. Line 2 moves off it. The bay beside it is 2.39 m because the sewage is 130 mm past the blue pipe, and that bay is a doubled 190. The steps are taped off the path, not off the lawn.
- **Prices.** Auckland only, read on 12 November 2026. Marton, Horotiu and Stratford are left out. Each line is the cheapest posted price, and the store is named. The H4 line is 150×50 SG8 because 140×45 H4 is not listed. N2 H4 is cheaper and is the wrong grade. The truck is the figure from site, not a Point Chevalier quote.
- **The rebuilt strip.** The old bearer comes out. If the ground there is worse than the main holes, those four piles get the same 600 mm and the same concrete.

## Sources

Northpine wet-service tables: 140×45 SG8 at 450 centres spans 2.35 m. NZS 3604 wants a pile 150 mm clear of the ground. The deck piles meet that. The bottom step does not. The stair proportion used here is a rise under 190 and 2R+G between 550 and 700. [Northpine tables](https://www.northpine.co.nz/span-tables) · [BRANZ Bulletin 611](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf).

Reproduce with `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`. Drawing ISL38807 is a preview and is not for construction.
'''
(root / 'CURRENT_DESIGN.md').write_text(md)
b = io.StringIO(newline='')
w = csv.writer(b, lineterminator='\n')
w.writerow(['Category', 'Description', 'Qty', 'Unit', 'Cheapest NZD', 'Store', 'In total NZD', 'Posted, estimate or alternative', 'Comments', 'Source'])
for cat, item, qty, unit, price, store, use, comment, kind, url in priced:
    w.writerow([cat, item, qty, unit, f'{price:.2f}', store, f'{use:.2f}', kind, comment, url])
w.writerow(['TOTAL', '', '', '', '', '', f'{total:.2f}', f'posted {posted:.2f} + estimates {est:.2f}', 'Truck is in the total. Cement and builders mix are not.', ''])
(root / 'SHOPPING_LIST.csv').write_text(b.getvalue())

inline = lambda x: re.sub(r'`([^`]+)`', r'<code>\1</code>', re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', E(x))))
parts = []
lines = md.splitlines()
i = 0
while i < len(lines):
    l = lines[i]
    if not l.strip():
        i += 1
        continue
    if l.startswith('#'):
        level = len(l) - len(l.lstrip('#'))
        tt = l[level:].strip()
        slug = re.sub(r'[^a-z0-9]+', '-', tt.lower()).strip('-')
        parts.append(f'<h{level} id="{slug}">{inline(tt)}</h{level}>')
        i += 1
    elif l.startswith('|'):
        block = []
        while i < len(lines) and lines[i].startswith('|'):
            block.append(lines[i])
            i += 1
        parts.append('<div class="table-wrap"><table>')
        for j, row in enumerate(block):
            if j == 1:
                continue
            tag = 'th' if j == 0 else 'td'
            parts.append('<tr>' + ''.join(f'<{tag}>' + inline(c.strip()) + f'</{tag}>' for c in row.strip().strip('|').split(' | ')) + '</tr>')
        parts.append('</table></div>')
    elif l.startswith('- ') or re.match(r'^\d+\. ', l):
        ordered = bool(re.match(r'^\d+\. ', l))
        tag = 'ol' if ordered else 'ul'
        parts.append('<' + tag + '>')
        while i < len(lines) and ((bool(re.match(r'^\d+\. ', lines[i])) if ordered else lines[i].startswith('- '))):
            parts.append('<li>' + inline(re.sub(r'^(?:\d+\. |- )', '', lines[i])) + '</li>')
            i += 1
        parts.append('</' + tag + '>')
    else:
        p = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '- ')) and not re.match(r'^\d+\. ', lines[i]):
            p.append(lines[i])
            i += 1
        parts.append('<p>' + inline(' '.join(p)) + '</p>')
body = '\n'.join(parts)
shop = body.index('<h2 id="shopping-list">')
build = body.index('<h2 id="build-order">')
schedules = body[shop:build].replace('href="docs/', 'href="', 1)
schedules = schedules.replace('<h2 id="shopping-list">Shopping list</h2>', '<h2 id="shopping-list">Bill of materials</h2>', 1)
sheets = '''<section id="sheets" aria-label="Drawing set">
<figure class="sheet"><div id="view-sheet"></div><figcaption>01 · Foundation, framing and long section</figcaption></figure>
<figure class="sheet"><div id="view-sheet2"></div><figcaption>02 · Section, pile and steps</figcaption></figure>
<figure class="sheet"><div id="view-sheet3"></div><figcaption>03 · Site, levels and schedules</figcaption></figure>
<p class="note"><a href="drawings/sheet.svg">Sheet 1</a> · <a href="drawings/sheet2.svg">Sheet 2</a> · <a href="drawings/sheet3.svg">Sheet 3</a></p>
<details class="sketches"><summary>Working sketches</summary>
<figure class="sheet"><div id="view-piles"></div><figcaption>Piles</figcaption></figure>
<figure class="sheet"><div id="view-framing"></div><figcaption>Framing</figcaption></figure>
<figure class="sheet"><div id="view-fixings"></div><figcaption>Steps</figcaption></figure>
</details>
</section>'''
body = sheets + schedules


def chip(label, inner):
    return f'<svg viewBox="0 0 320 200" role="img" aria-label="{E(label)}"><rect width="320" height="200" fill="#f7f4ee"/>{inner}</svg>'

def tx(x, y, s, size=15, anchor='start', fill='#21382f'):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="650" text-anchor="{anchor}" fill="{fill}">{E(s)}</text>'

figs = []
# 1 Measure.
figs.append(chip('Tape from the old boards down to the concrete path. Grass is lower. Three rises off the path.',
    '<rect x="0" y="168" width="320" height="32" fill="#e4ecdf"/>'
    '<rect x="78" y="146" width="150" height="22" fill="#cfc6b4" stroke="#52675b"/>'
    '<rect x="18" y="28" width="22" height="140" fill="#e7e2d6" stroke="#52675b"/>'
    '<rect x="40" y="46" width="200" height="12" fill="#c4a574" stroke="#52675b"/>'
    '<line x1="150" y1="58" x2="150" y2="146" stroke="#254c3e" stroke-width="2" stroke-dasharray="4 3"/>'
    '<polygon points="146,138 154,138 150,148" fill="#254c3e"/>'
    + tx(148, 24, 'old boards', 14)
    + tx(92, 116, 'tape', 14, 'end', '#254c3e')
    + tx(100, 162, 'path', 14, 'middle')
    + tx(270, 186, 'grass, lower', 13, 'middle', '#3d5c45')
    + tx(188, 78, '÷ 3 rises', 14)
    + tx(188, 98, 'about 167', 13)
    + tx(188, 122, '190 mm', 14)
    + tx(188, 142, 'bearers', 13)
    + tx(16, 22, 'sill', 13)))
# 2 Set out.
figs.append(chip('Plan of the deck over the path, drain to the west, two steps out the front.',
    '<rect x="0" y="0" width="320" height="200" fill="#e4ecdf"/>'
    '<rect x="78" y="28" width="210" height="100" fill="#f7f4ee" stroke="#254c3e" stroke-width="2"/>'
    '<rect x="78" y="128" width="210" height="22" fill="#f3e6c8" stroke="#254c3e"/>'
    '<rect x="78" y="62" width="210" height="22" fill="#cfc6b4"/>'
    '<line x1="48" y1="16" x2="48" y2="184" stroke="#a33b32" stroke-width="4"/>'
    '<circle cx="110" cy="46" r="5" fill="#456b54"/>'
    '<circle cx="250" cy="46" r="5" fill="#456b54"/>'
    '<circle cx="110" cy="112" r="5" fill="#456b54"/>'
    '<circle cx="250" cy="112" r="5" fill="#456b54"/>'
    '<circle cx="110" cy="150" r="4" fill="#456b54"/>'
    '<circle cx="250" cy="150" r="4" fill="#456b54"/>'
    + tx(183, 40, '6.6 × 2.6', 14)
    + tx(183, 100, 'path stays', 13)
    + tx(160, 186, 'two steps, 560', 14, 'middle')
    + tx(48, 14, 'drain', 12, 'middle', '#a33b32')))
# 3 Dig.
figs.append(chip('Every deck hole is 600 deep. The step hole is 400. Spade near the pipe.',
    '<rect x="0" y="78" width="320" height="122" fill="#efe6d4"/>'
    '<rect x="40" y="78" width="76" height="90" fill="#f7f4ee" stroke="#52675b"/>'
    '<rect x="64" y="34" width="28" height="82" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="160" y="108" width="56" height="48" fill="#f7f4ee" stroke="#52675b"/>'
    '<rect x="174" y="78" width="28" height="55" fill="#c4a574" stroke="#52675b"/>'
    '<line x1="276" y1="24" x2="276" y2="170" stroke="#a33b32" stroke-width="4"/>'
    '<line x1="264" y1="48" x2="288" y2="72" stroke="#a33b32" stroke-width="3"/>'
    '<line x1="288" y1="48" x2="264" y2="72" stroke="#a33b32" stroke-width="3"/>'
    + tx(78, 28, '600', 16, 'middle')
    + tx(78, 184, 'deck', 13, 'middle')
    + tx(188, 70, '400', 14, 'middle')
    + tx(188, 184, 'step', 13, 'middle')
    + tx(276, 16, 'pipe', 12, 'middle', '#a33b32')
    + tx(276, 104, 'spade', 13, 'middle')))
# 4 Concrete.
figs.append(chip('Concrete to just below the ground. One hole at a time, or one truck if they are all open.',
    '<rect x="0" y="108" width="320" height="60" fill="#efe6d4"/>'
    '<rect x="70" y="118" width="64" height="50" fill="#d5d8d4" stroke="#52675b"/>'
    '<rect x="88" y="40" width="28" height="100" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="190" y="126" width="64" height="42" fill="#d5d8d4" stroke="#52675b"/>'
    '<rect x="208" y="56" width="28" height="90" fill="#c4a574" stroke="#52675b"/>'
    '<line x1="16" y1="108" x2="304" y2="108" stroke="#52675b"/>'
    + tx(16, 100, 'ground', 13)
    + tx(160, 28, 'leave them long', 16, 'middle')
    + tx(160, 190, '4 mix to 1 cement', 14, 'middle')))
# 5 Cut.
figs.append(chip('String line set off the concrete path. The grass pile is left taller.',
    '<rect x="0" y="158" width="320" height="42" fill="#e4ecdf"/>'
    '<rect x="16" y="112" width="88" height="46" fill="#cfc6b4" stroke="#52675b"/>'
    '<rect x="140" y="52" width="26" height="136" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="240" y="52" width="26" height="148" fill="#c4a574" stroke="#52675b"/>'
    '<line x1="16" y1="52" x2="300" y2="52" stroke="#254c3e" stroke-width="2"/>'
    + tx(168, 32, 'one string', 16, 'middle', '#254c3e')
    + tx(60, 140, 'path', 14, 'middle')
    + tx(118, 88, '150', 14, 'middle')
    + tx(16, 184, 'grass side stands taller', 14)))
# 6 Bearers.
figs.append(chip('Two long double bearers on the piles, and the short rebuilt bearers by the house.',
    '<rect x="0" y="0" width="320" height="200" fill="#e4ecdf"/>'
    '<rect x="36" y="48" width="250" height="16" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="36" y="120" width="250" height="16" fill="#c4a574" stroke="#52675b"/>'
    + ''.join(f'<rect x="{x}" y="44" width="10" height="24" fill="#456b54"/>' for x in (48, 110, 172, 234))
    + ''.join(f'<rect x="{x}" y="116" width="10" height="24" fill="#456b54"/>' for x in (48, 110, 172, 234))
    + '<rect x="36" y="18" width="70" height="12" fill="#b08958" stroke="#52675b"/>'
    '<rect x="36" y="78" width="70" height="12" fill="#b08958" stroke="#52675b"/>'
    + tx(200, 42, 'main', 14)
    + tx(200, 114, 'main', 14)
    + tx(114, 16, 'rebuilt', 13)
    + tx(160, 178, 'nail the two plies first', 14, 'middle')))
# 7 Joists from the side.
figs.append(chip('Joists across the bearers. The screws go in from the side, not down through the top.',
    '<rect x="16" y="36" width="150" height="14" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="16" y="150" width="150" height="14" fill="#c4a574" stroke="#52675b"/>'
    + ''.join(f'<rect x="{x}" y="36" width="10" height="128" fill="#456b54" stroke="#52675b"/>' for x in (28, 58, 88))
    + '<rect x="118" y="36" width="10" height="128" fill="#254c3e"/>'
    '<rect x="130" y="36" width="10" height="128" fill="#254c3e"/>'
    + tx(24, 28, 'joists', 13)
    + tx(150, 28, 'double', 13)
    + '<rect x="196" y="70" width="100" height="28" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="214" y="98" width="64" height="22" fill="#b08958" stroke="#52675b"/>'
    '<line x1="196" y1="88" x2="230" y2="108" stroke="#21382f" stroke-width="3"/>'
    '<line x1="246" y1="78" x2="246" y2="108" stroke="#a33b32" stroke-width="3"/>'
    '<line x1="236" y1="70" x2="256" y2="90" stroke="#a33b32" stroke-width="3"/>'
    + tx(250, 64, 'from the side', 13, 'middle')
    + tx(250, 168, 'not down', 13, 'middle', '#a33b32')
    + tx(250, 186, 'through the top', 12, 'middle', '#a33b32')))
# 8 Step piles.
figs.append(chip('Six small holes, 300 by 300 and 400 deep, in line with the front piles.',
    '<rect x="24" y="36" width="270" height="16" fill="#c4a574" stroke="#52675b"/>'
    + ''.join(f'<rect x="{x}" y="44" width="8" height="14" fill="#456b54"/>' for x in (40, 92, 144, 196, 248))
    + ''.join(f'<rect x="{x}" y="100" width="28" height="22" fill="none" stroke="#52675b"/>' for x in (32, 84, 136, 188, 240))
    + tx(160, 28, 'front piles', 14, 'middle')
    + tx(160, 150, '400 deep', 15, 'middle')
    + tx(160, 174, 'then concrete them', 13, 'middle')))
# 9 Bottom step.
figs.append(chip('Bottom step: ribbon on the piles, joists out, front beam on the small piles.',
    '<rect x="36" y="40" width="18" height="70" fill="#456b54"/>'
    '<rect x="54" y="70" width="180" height="16" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="234" y="70" width="16" height="16" fill="#b08958" stroke="#52675b"/>'
    '<rect x="230" y="86" width="24" height="80" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="150" y="158" width="70" height="16" fill="#cfc6b4" stroke="#52675b"/>'
    + tx(20, 30, 'pile', 12)
    + tx(100, 64, 'ribbon', 13)
    + tx(262, 64, 'beam', 12)
    + tx(185, 152, 'path', 12, 'middle')
    + tx(16, 190, 'rip it clear of the path', 13)))
# 10 Top step.
figs.append(chip('Top step built on the bottom one, set back one going, screwed to the bearer.',
    '<rect x="30" y="90" width="200" height="14" fill="#c4a574" stroke="#52675b"/>'
    '<rect x="30" y="48" width="120" height="14" fill="#b08958" stroke="#52675b"/>'
    '<rect x="150" y="48" width="14" height="42" fill="#456b54"/>'
    '<rect x="40" y="24" width="100" height="10" fill="#c4a574"/>'
    + tx(248, 34, '167', 14)
    + tx(248, 62, '167', 14)
    + tx(248, 100, '167', 14)
    + tx(16, 170, 'tape the three rises', 15)
    + tx(16, 190, 'no handrail', 13, 'start', '#637069')))
# 11 Boards.
figs.append(chip('Boards along the deck, three on each step, and a board on the face.',
    ''.join(f'<rect x="16" y="{y}" width="150" height="8" fill="#c4a574" stroke="#52675b"/>' for y in range(20, 104, 12))
    + '<rect x="16" y="112" width="150" height="8" fill="#456b54" stroke="#52675b"/>'
    + '<rect x="16" y="126" width="150" height="8" fill="#456b54" stroke="#52675b"/>'
    + '<rect x="16" y="148" width="8" height="28" fill="#c4a574" stroke="#52675b"/>'
    + '<line x1="118" y1="16" x2="118" y2="104" stroke="#254c3e" stroke-width="2" stroke-dasharray="3 2"/>'
    + tx(178, 48, '28 deck', 14)
    + tx(178, 70, 'butts', 13, 'start', '#254c3e')
    + tx(178, 130, '3 + 3', 14)
    + tx(36, 184, 'face board', 14)))
titles = ['Measure first', 'String the deck', 'Dig to 600', 'Concrete as you go', 'Cut to the path', 'Bearers', 'Joists from the side', 'Step piles', 'Bottom step', 'Top step', 'Boards and the face']
assert len(figs) == len(steps) == len(titles) == 11
html = '''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="ISL38807. Proposed deck for 18B Formby Avenue. Three sheets, not lodged."><title>ISL38807 · 18B Formby Avenue</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">ISL38807 <span>18B FORMBY AVENUE · NOT LODGED</span></a><nav aria-label="Sections"><a href="#sheets">Sheets</a><a href="#shopping-list">Schedule</a></nav><button id="print">Print</button></header><main id="main">''' + body + '''</main><footer><span>AS/NZS 1100.501 · Exemption 24 · Do not scale</span></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
(root / 'site/index.html').write_text(html)
print('Rendered guide, CSV and page; posted', posted, 'estimates', est, 'total', total)


T = '#cba773'
G = '#456b54'
C = '#d6dad7'
S = '#ece5d6'
A = '#af6b3c'
P = '#b9b3a6'

def r(x, y, w, h, fill, stroke='#52675b', dash=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'

def line(x, y, x2, y2, stroke='#71847b', dash=''):
    return f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" ' + (f'stroke-dasharray="{dash}"' if dash else '') + '/>'

def text(x, y, tx, size=13, anchor='start'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{E(tx)}</text>'

def svg(name, title, bd, w=1100, h=800):
    out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}"><title>{E(title)}</title><style>text{{font-family:system-ui,sans-serif;fill:#21382f}}line{{stroke-width:1.5}}</style><rect width="{w}" height="{h}" fill="#fbfbf8"/>{bd}</svg>'
    (root / 'site/drawings' / f'{name}.svg').write_text(out)

X = lambda x: 55 + x * .105
Y = lambda y: 295 + y * .09

outline = r(X(0), Y(0), 6600 * .105, 2600 * .09, '#f5f7f2') + r(X(0), Y(-1970), 900 * .105, 1970 * .09, '#f5f7f2') + r(X(0), Y(2600), 6600 * .105, 560 * .09, '#faf3e4')
bd = text(40, 35, '1 · Piles and heights', 21) + text(40, 62, 'All holes 600 deep. No anchor kits. Step holes 400 deep. Lawn is lower than the path.', 13) + outline
for y in [300, 2510]:
    for x in pile_x:
        bd += r(X(x - 200), Y(y - 200), 400 * .105, 400 * .09, 'none', '#9aa89f', '3 3') + r(X(x - 62.5), Y(y - 62.5), 125 * .105, 125 * .09, G)
for y in [-1925, -800]:
    for x in [175, 725]:
        bd += r(X(x - 62.5), Y(y - 62.5), 125 * .105, 125 * .09, G)
for x in pile_x:
    bd += r(X(x - 150), Y(3115 - 150), 300 * .105, 300 * .09, 'none', '#9aa89f', '3 3') + r(X(x - 40), Y(3115 - 40), 80 * .105, 80 * .09, A)
bd += text(185, 133, 'Rebuilt strip: four piles, same 600 mm holes', 12)
bd += text(X(3300), Y(1400), '16 piles. Two rows. Every hole 400×400×600', 13, 'middle')
bd += text(X(3300), Y(3450), 'Six step piles on the same X, 300×300×400. Two spare if the path is in a bay', 12, 'middle')
bd += text(790, 100, 'Heights off the path', 14)
bd += text(790, 128, 'Deck boards +500', 13)
bd += text(790, 152, 'Bottom step about +167', 13)
bd += text(790, 176, 'Top step about +333', 13)
bd += text(790, 200, 'Three equal rises. No rail', 13)
bd += text(790, 236, '16 piles, one length', 14)
bd += text(790, 260, 'Buy 1.2 m and cut to the string', 12)
bd += text(790, 284, '750 mm does not reach', 12)
bd += text(790, 320, 'Concrete, pile left in', 14)
bd += text(790, 344, f'Twelve holes {cv["main_12_holes_m3"]:.2f} m³', 12)
bd += text(790, 368, f'All of it about {cv["main_net_m3"]:.2f} m³', 12)
bd += text(790, 392, 'Truck 2.0 m³, or mix as you go', 12)
bd += text(40, 700, 'Path stays. Line 2 is 200 mm onto the grass. Line 3 is 1,230 mm past the concrete, clear of both pipes.', 12)
bd += text(40, 732, 'That bay is 2.39 m, a doubled 190. Every other bay stays under 1.4 m.', 12)
bd += text(40, 764, 'Orange squares are the step piles. Green squares are the deck and rebuilt piles.', 12)
svg('piles', 'Sixteen piles in 600 mm holes and six step piles in 400 mm holes. No anchor piles. Deck over the path.', bd, h=820)

bd = text(40, 35, '2 · Framing', 21) + text(40, 62, '140×45 SG8. H3.2 deck and rebuilt strip. H4 on the two steps. Boards along X.', 13) + outline
for y in [300, 2510]:
    bd += r(X(0), Y(y - 45), 6600 * .105, 90 * .09, T)
for y in [-1925, -800]:
    bd += r(X(0), Y(y - 45), 900 * .105, 90 * .09, T)
for x in d['main_joist_centres_mm']:
    bd += r(X(x - 22.5), Y(45), 45 * .105, 2510 * .09, G)
for x in [22.5, 450, 877.5]:
    bd += r(X(x - 22.5), Y(-1925), 45 * .105, 1880 * .09, G)
for x in [45, 472.5]:
    bd += r(X(x), Y(-822.5), 380 * .105, 45 * .09, G)
for y, length in [(0, 6600), (2555, 6600), (-1970, 900), (-45, 900)]:
    bd += r(X(0), Y(y), length * .105, 45 * .09, T)
bd += r(X(0), Y(2600), 6600 * .105, 90 * .09, T)
bd += r(X(0), Y(3070), 6600 * .105, 90 * .09, T)
bd += r(X(0), Y(2860), 6600 * .105, 90 * .09, A)
for x in d['main_joist_centres_mm']:
    bd += r(X(x - 22.5), Y(2690), 45 * .105, 380 * .09, G)
bd += text(790, 250, 'Deck: 17 joists of 2510', 13)
bd += text(790, 276, 'Flush, then 437 centres', 13)
bd += text(790, 302, 'Doubled joist at 3956', 13)
bd += text(790, 328, 'Span 2.21 m', 13)
bd += text(790, 366, 'Steps stick out 560', 13)
bd += text(790, 392, 'Going 280, rise about 167', 13)
bd += text(790, 418, 'Bottom beam may be ripped', 13)
bd += text(790, 444, 'to 120 where it hits the path', 13)
bd += text(40, 700, 'Bearers nailed as two plies. Joists sit on them. Screws into a bearer go in from the side.', 13)
bd += text(40, 732, 'Do not cut a stringer. Ribbon to the piles, joists out, front beam on the small piles, then the top step.', 13)
bd += text(40, 764, 'Board butts land on the doubled joist at 3956. Face board on the boundary joist.', 13)
svg('framing', 'Framing plan: seventeen joists, the rebuilt strip, and two full-width steps. Boards run along the deck.', bd, h=820)

sx = lambda y: 80 + (y - 2300) * 0.55
sz = lambda z: 430 - z * 0.62
bd = text(40, 32, '3 · The two steps, side on', 21) + text(40, 58, 'Tape the rises off the path. 32 mm boards. Bottom framing is ripped where it would hit the path.', 13)
bd += r(sx(2400), sz(0), (3300 - 2400) * 0.55, 70, S)
bd += r(sx(2500), sz(40), 700 * 0.55, sz(-80) - sz(40), '#cfc6b4', '#52675b')
bd += line(sx(2350), sz(0), sx(3300), sz(0), '#52675b')
bd += r(sx(2447), sz(187), 125 * 0.55, (187 + 200) * 0.62, 'none', '#9aa89f', '4 3')
bd += r(sx(3055), sz(20), 80 * 0.55, 180 * 0.62, 'none', '#9aa89f', '4 3')
bd += r(sx(2465), sz(328), 90 * 0.55, 140 * 0.62, T)
bd += r(sx(2350), sz(468), 250 * 0.55, 140 * 0.62, G)
bd += r(sx(2555), sz(468), 45 * 0.55, 140 * 0.62, T)
bd += r(sx(2350), sz(500), 250 * 0.55, 32 * 0.62, T)
bd += r(sx(2555), sz(135), 90 * 0.55, 120 * 0.62, T)
bd += r(sx(2645), sz(135), 425 * 0.55, 45 * 0.62, G)
bd += r(sx(3070), sz(135), 90 * 0.55, 120 * 0.62, T)
bd += r(sx(2600), sz(301), 90 * 0.55, 140 * 0.62, A)
bd += r(sx(2690), sz(301), 190 * 0.55, 45 * 0.62, G)
bd += r(sx(2880), sz(301), 90 * 0.55, 140 * 0.62, A)
bd += r(sx(2600), sz(333), 280 * 0.55, 32 * 0.62, T)
bd += r(sx(2880), sz(167), 280 * 0.55, 32 * 0.62, T)
bd += text(sx(2360), sz(530), 'Deck +500', 12)
bd += text(sx(2680), sz(365), 'Top +333', 12)
bd += text(sx(2940), sz(200), 'Bottom +167', 12)
bd += text(sx(2620), sz(-20), 'path', 12)
bd += text(680, 120, 'F5 · ribbon into the piles', 15)
bd += text(680, 146, 'Four 14g×100 from the side', 13)
bd += text(680, 184, 'F7 · top ribbon into the bearer', 15)
bd += text(680, 210, 'Same screws. Pack the front.', 13)
bd += text(680, 248, 'Front beam', 15)
bd += text(680, 274, f'Full 140 is {sc["step_beam_util_140"]*100:.0f}% of the screen', 13)
bd += text(680, 300, f'Ripped half-bay is {sc["step_beam_util_120"]*100:.0f}%', 13)
bd += text(680, 338, 'No handrail', 15)
bd += text(680, 364, 'Three rises. One more needs a rail.', 13)
bd += text(40, 620, 'F1 nails on the doubles. F2 four skew nails at every pile, including the small ones.', 13)
bd += text(40, 648, 'F6 two M12 bolts where the rebuilt strip meets the deck. F8 a board on the face and on each riser.', 13)
bd += text(40, 676, 'Bottom step is H4. It does not clear the path by 150 mm. The deck piles do.', 13)
svg('fixings', 'Side of the two steps: three rises off the path, ribbon screwed to the piles, small piles under the front beam', bd, h=720)

# Two A2 sheets in the preview sheet format. Geometry is this build, not ISL38807.
BLUE, GREEN, RED, INK = '#0033cc', '#008f2d', '#d10000', '#111111'
K = 0.08  # 1:25 when the viewBox is 2 units per paper millimetre

def _ln(x, y, x2, y2, stroke=INK, sw=0.8, dash=''):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{sw}" fill="none"{extra}/>'

def _tx(x, y, s, size=8, anchor='start', fill=INK, weight='500'):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{E(s)}</text>'

def _box(x, y, w, h, stroke=INK, sw=0.8, dash=''):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="none" stroke="{stroke}" stroke-width="{sw}"{extra}/>'

def _dot(x, y):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.7" fill="{GREEN}"/>'

def _hdim(x1, x2, y, label):
    mid = (x1 + x2) / 2
    return (_ln(x1, y, x2, y, RED, 0.6)
            + _ln(x1 - 2.4, y + 2.4, x1 + 2.4, y - 2.4, RED, 0.6)
            + _ln(x2 - 2.4, y + 2.4, x2 + 2.4, y - 2.4, RED, 0.6)
            + _tx(mid, y - 2.6, label, 8, 'middle', RED))

def _vdim(x, y1, y2, label):
    mid = (y1 + y2) / 2
    return (_ln(x, y1, x, y2, RED, 0.6)
            + _ln(x - 2.4, y1 - 2.4, x + 2.4, y1 + 2.4, RED, 0.6)
            + _ln(x - 2.4, y2 - 2.4, x + 2.4, y2 + 2.4, RED, 0.6)
            + _tx(x - 4, mid + 2, label, 8, 'end', RED))

def _note(x, y, lines, to=None, size=7.6):
    out = [''.join(_tx(x, y + i * 10.5, line, size, 'start', GREEN, '600') for i, line in enumerate(lines))]
    if to:
        out.append(_ln(x, y + (len(lines) - 1) * 10.5 + 3, to[0], to[1], GREEN, 0.55))
        out.append(_dot(*to))
    return ''.join(out)

def _title(parts, sheet_no, scale, drawing_title):
    top, bot = 742, 818
    parts.append(_box(10, 10, 1168, 820, BLUE, 2.6))
    parts.append(_box(16, 16, 1156, 808, BLUE, 0.7))
    parts.append(_box(16, top, 1156, bot - top, INK, 0.9))
    parts.append(_ln(168, top, 168, bot, INK, 0.8))
    parts.append(_ln(860, top, 860, bot, INK, 0.8))
    parts.append(_tx(92, 776, 'MH', 26, 'middle', INK, '700'))
    parts.append(_tx(92, 796, 'DECK', 12, 'middle', INK, '700'))
    parts.append(_tx(92, 812, 'WORKING PLAN', 6.5, 'middle', INK, '500'))
    parts.append(_tx(180, 760, drawing_title, 8, 'start', INK, '700'))
    parts.append(_tx(180, 776, 'PROPOSED DECK FOR MAX HOGERVORST', 11, 'start', INK, '700'))
    parts.append(_tx(180, 792, '18B FORMBY AVENUE, POINT CHEVALIER, AUCKLAND 1022', 8, 'start', INK, '500'))
    parts.append(_tx(180, 810, 'FLAT 2 DP 122876 · DIMS IN mm · DO NOT SCALE · EXEMPTION 24 · NOT LODGED', 6.2, 'start', INK, '400'))
    rows = [
        ('DRAWN', 'MH', 'REVISION', 'A'),
        ('DATE', '11/11/26', 'SCALE', scale),
        ('APPROVED', '—', 'SIZE', 'A2'),
        ('SHEET', f'{sheet_no} OF 3', 'DWG NO.', '0001'),
    ]
    rh = (bot - top) / 4
    xs = [860, 936, 1024, 1110, 1172]
    for i, row in enumerate(rows):
        y = top + i * rh
        if i:
            parts.append(_ln(860, y, 1172, y, INK, 0.55))
        for x in xs[1:-1]:
            parts.append(_ln(x, y, x, y + rh, INK, 0.45))
        for j, cell in enumerate(row):
            parts.append(_tx(xs[j] + 5, y + rh * 0.68, cell, 7.4, 'start', INK, '650' if j % 2 == 0 else '500'))
    parts.append(_tx(848, 810, 'REF NO. ISL38807', 6.5, 'end', INK, '500'))

def _sheet(parts, label):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1188 840" role="img" '
        f'aria-label="{E(label)}"><title>{E(label)}</title>'
        '<style>text{font-family:Arial,Helvetica,sans-serif}</style>'
        + ''.join(parts) + '</svg>'
    )

def PX(x):
    return 100 + x * K

def PY(y):
    return 206 + y * K

s1 = []
_title(s1, 1, '1:25', '01  FOUNDATION, FRAMING AND LONG SECTION')
# Rebuilt strip at the house, then the deck, then the two steps.
s1.append(_box(PX(0), PY(-1970), 900 * K, 1970 * K))
s1.append(_box(PX(0), PY(0), 6600 * K, 2600 * K))
s1.append(_box(PX(0), PY(2600), 6600 * K, 560 * K))
s1.append(_ln(PX(0), PY(2880), PX(6600), PY(2880), INK, 0.45))
for x in d['main_joist_centres_mm']:
    heavy = x in (3933, 3978)
    s1.append(_ln(PX(x), PY(45), PX(x), PY(2555), INK, 1.05 if heavy else 0.4))
for x in (22.5, 450, 877.5):
    s1.append(_ln(PX(x), PY(-1925), PX(x), PY(-45), INK, 0.4))
for y, length in ((300, 6600), (2510, 6600), (-1925, 900), (-800, 900)):
    s1.append(_ln(PX(0), PY(y - 45), PX(length), PY(y - 45), INK, 0.9))
    s1.append(_ln(PX(0), PY(y + 45), PX(length), PY(y + 45), INK, 0.9))
s1.append(_ln(PX(0), PY(2555), PX(6600), PY(2555), INK, 0.7))
s1.append(_ln(PX(0), PY(3070), PX(6600), PY(3070), INK, 0.7))
s1.append(_ln(PX(0), PY(3160), PX(6600), PY(3160), INK, 0.7))
for y in (300, 2510):
    for x in pile_x:
        s1.append(_box(PX(x - 200), PY(y - 200), 400 * K, 400 * K, '#8a8a8a', 0.4, '2 1.4'))
        s1.append(_box(PX(x - 62.5), PY(y - 62.5), 125 * K, 125 * K, INK, 0.8))
for y in (-1925, -800):
    for x in (175, 725):
        s1.append(_box(PX(x - 62.5), PY(y - 62.5), 125 * K, 125 * K, INK, 0.8))
for x in pile_x:
    s1.append(_box(PX(x - 62.5), PY(3115 - 62.5), 125 * K, 125 * K, INK, 0.8))

s1.append(_vdim(PX(0) - 16, PY(-1970), PY(0), '1970'))
s1.append(_vdim(PX(0) - 34, PY(0), PY(2600), '2600'))
s1.append(_vdim(PX(0) - 16, PY(2600), PY(3160), '560'))
chain = PY(3160) + 18
for a, b in zip(pile_x, pile_x[1:]):
    s1.append(_ln(PX(a), PY(y=2510) if False else PY(3115), PX(a), chain, RED, 0.35))
    s1.append(_hdim(PX(a), PX(b), chain, str(int(round(b - a)))))
s1.append(_ln(PX(pile_x[-1]), PY(3115), PX(pile_x[-1]), chain, RED, 0.35))
s1.append(_tx(PX((pile_x[1] + pile_x[2]) / 2), PY(2200), '190×45 DOUBLE', 8, 'middle', RED, '700'))
s1.append(_hdim(PX(0), PX(6600), chain + 16, '6600'))
s1.append(_tx(PX(0) - 2, chain - 10, '62.5', 7, 'end', RED))
s1.append(_tx(PX(6600) + 2, chain - 10, '62.5', 7, 'start', RED))
cx = PX(3300)
s1.append(_tx(cx, chain + 40, 'FOUNDATION AND FRAMING PLAN', 10, 'middle', GREEN, '700'))
s1.append(_ln(cx - 70, chain + 43, cx + 70, chain + 43, GREEN, 0.8))
s1.append(_tx(cx, chain + 54, 'SCALE 1:25', 7.5, 'middle', GREEN, '600'))
s1.append(_tx(640, 250, 'LOCAL DATUM', 8, 'start', GREEN, '700'))
s1.append(_tx(640, 264, 'PATH = 0.000', 8, 'start', GREEN, '500'))
s1.append(_tx(640, 278, 'FFL +500 BOARDS', 8, 'start', GREEN, '500'))
s1.append(_tx(640, 292, 'NOT AKL 1946', 8, 'start', GREEN, '500'))
s1.append(_tx(640, 314, 'SECTION A-A BELOW', 8, 'start', GREEN, '600'))
s1.append(_tx(640, 328, 'SECTION B-B: SHEET 2', 8, 'start', GREEN, '600'))
s1.append(_tx(640, 350, 'NO BRACES. NOTE 7.', 8, 'start', GREEN, '600'))
s1.append(_ln(640, 372, 720, 372, RED, 0.7))
s1.append(_tx(680, 366, '1000', 7, 'middle', RED))
s1.append(_tx(680, 386, 'SCALE BAR 1:25', 6.5, 'middle', INK, '500'))

s1.append(_note(188, 46, ['88×32 H3.2 MERCH GRADE', 'GRIPTREAD DECKING.', 'ABOUT 5mm GAP. BOARDS', 'ALONG THE DECK.'], (PX(1800), PY(30))))
s1.append(_note(360, 46, ['DOUBLE BEARER', '140×45, AND 190×45', 'ON THE 2390 BAY'], (PX(2200), PY(300))))
s1.append(_note(500, 46, ['NOTE', 'DECKING IS FIXED WITH', 'DECKING SCREWS'], (PX(4200), PY(80))))
s1.append(_note(188, 108, ['140×45 SG8 H3.2 JOIST', 'AT 437 CENTRES', 'DOUBLED AT 3956'], (PX(1770.5), PY(400))))
s1.append(_note(400, 108, ['125×125 H5 PILE', 'HOLE 400×400×600', 'NO ANCHOR BRACKET'], (PX(2652.5), PY(300))))
s1.append(_note(560, 118, ['TWO STEPS', 'GOING 280', 'SEE SHEET 2'], (PX(5000), PY(2880))))
s1.append(_tx(PX(450), 34, 'REBUILT 900×1970', 7.5, 'middle', GREEN, '600'))

# Long elevation, aligned with the plan. True 1:25, so it is the thin strip.
def EZ(z):
    return 648 - z * K

s1.append(_ln(PX(0), EZ(0), PX(6600), EZ(0), INK, 0.9))
for x in pile_x:
    s1.append(_box(PX(x - 62.5), EZ(187), 125 * K, (187 + 40) * K))
belly_a = pile_x[1] + 62.5
belly_b = pile_x[2] - 62.5
s1.append(_box(PX(0), EZ(328), belly_a * K, 140 * K))
s1.append(_box(PX(belly_a), EZ(328), (belly_b - belly_a) * K, 190 * K))
s1.append(_box(PX(belly_b), EZ(328), (6600 - belly_b) * K, 140 * K))
s1.append(_tx(PX((belly_a + belly_b) / 2), EZ(110), '190', 7, 'middle', RED))
s1.append(_box(PX(0), EZ(468), 6600 * K, 140 * K))
s1.append(_box(PX(0), EZ(500), 6600 * K, 32 * K))
s1.append(_vdim(PX(0) - 16, EZ(500), EZ(0), '500'))
s1.append(_tx(PX(80), 600, 'APPROX 500 TO TOP OF BOARDS', 7.5, 'start', RED))
s1.append(_tx(cx, 708, 'LONG SECTION A-A', 10, 'middle', GREEN, '700'))
s1.append(_ln(cx - 48, 711, cx + 48, 711, GREEN, 0.8))
s1.append(_tx(cx, 724, 'SCALE 1:25  ·  LOOKING TOWARD THE HOUSE', 7.5, 'middle', GREEN, '600'))
(root / 'site/drawings' / 'sheet.svg').write_text(_sheet(s1, 'Sheet 1. Foundation and framing plan, long section. Ref ISL38807. Consent exempt, not lodged.'))

# Sheet 2. Notes, end elevation, pile hole, two steps.
s2 = []
_title(s2, 2, '1:25 / 1:10', '02  SECTION, PILE AND STEPS')
notes = [
    'GENERAL NOTES',
    '1. AS/NZS 1100.501:2002.',
    'DIMENSIONS ARE IN MILLIMETRES.',
    'THEY GOVERN. DO NOT SCALE.',
    'SCALES ARE FOR A2, 10 mm MARGIN.',
    '2. BUILDING ACT SCHEDULE 1,',
    'EXEMPTION 24. THE FALL IS',
    'ABOUT 500, UNDER 1.5 m.',
    'CONSENT IS NOT REQUIRED.',
    'THESE SHEETS ARE NOT LODGED.',
    'DRAWN TO AC1011 PRACTICE.',
    'NOT A PS1. NOT CHECKED.',
    '3. OWNER AND DESIGNER:',
    'MAX HOGERVORST.',
    'LEGAL, FROM THE RATING',
    'RECORD: FLAT 2 DP 122876',
    'AND CARPORT 2 DP 122876.',
    '4. DATUM IS THE PATH = 0.',
    'FFL +500, TOP OF BOARDS.',
    'NOT AN AUCKLAND 1946 LEVEL.',
    'GRASS IS LOWER. UNTAPED.',
    'BOUNDARIES NOT SURVEYED.',
    '5. FINISHED SIZES.',
    'DECK AND REBUILT STRIP:',
    '140×45 SG8 H3.2.',
    'STEPS: 140×45 SG8 H4.',
    'PILES: 125×125 H5.',
    'BOARDS: 88×32 H3.2.',
    '6. 16 PILES. HOLE 400×400,',
    '600 DEEP. SIX STEP PILES,',
    'HOLE 300×300, 400 DEEP.',
    'NO ROD. NO ANCHOR.',
    'NO BRACKET. CONCRETE IS',
    '4:1 BUILDERS MIX, OR A TRUCK.',
    '7. NZS 3604 cl 7.4.2.2 WOULD',
    'WANT SUBFLOOR BRACES. THIS',
    'DECK IS 2600 OUT, OVER 2 m.',
    'NONE ARE SHOWN. DEPARTURE,',
    'ON OWNER DIRECTION.',
    '8. THE PATH STAYS.',
    'NO HOLE IN IT. WEST DRAINS:',
    'SPADE, AND 500 CLEAR.',
    '9. STAIRS. THREE EQUAL RISES,',
    'TWO GOINGS OF 280. IF THE',
    'TAPE IS 500, RISE IS 167 AND',
    '2R+G IS 614. NO BARRIER:',
    'THE FALL IS UNDER 1 m.',
    '10. VERIFY EVERY SIZE ON SITE',
    'BEFORE ORDERING.',
]
for i, line in enumerate(notes):
    s3_note_y = 32 + i * 9.15
    s2.append(_tx(36, s3_note_y, line, 6.9, 'start', GREEN, '700' if i == 0 else '500'))

# End elevation, short direction, 1:25.
def EY(y):
    return 40 + (y + 200) * K

def EZ2(z):
    return 640 - z * K

s2.append(_ln(EY(-100), EZ2(0), EY(3400), EZ2(0), INK, 0.8))
for y in (300, 2510):
    s2.append(_box(EY(y - 62.5), EZ2(187), 125 * K, (187 + 80) * K))
    s2.append(_box(EY(y - 45), EZ2(328), 90 * K, 140 * K))
s2.append(_box(EY(0), EZ2(468), 2555 * K, 140 * K))
s2.append(_box(EY(0), EZ2(500), 2600 * K, 32 * K))
s2.append(_box(EY(2555), EZ2(135), 605 * K, 120 * K))
s2.append(_box(EY(2555), EZ2(161), 325 * K, 26 * K))
s2.append(_box(EY(2555), EZ2(301), 325 * K, 140 * K))
s2.append(_box(EY(2600), EZ2(333), 280 * K, 32 * K))
s2.append(_box(EY(2880), EZ2(167), 280 * K, 32 * K))
s2.append(_box(EY(3115 - 40), EZ2(15), 80 * K, (15 + 80) * K))
s2.append(_tx(EY(1400), 668, 'CROSS SECTION B-B', 10, 'middle', GREEN, '700'))
s2.append(_ln(EY(1400) - 48, 671, EY(1400) + 48, 671, GREEN, 0.8))
s2.append(_tx(EY(1400), 684, 'SCALE 1:25  ·  LOOKING ALONG THE DECK', 7, 'middle', GREEN, '600'))

# Detail A, pile hole, 1:10.
k10 = 0.2
ax, ay = 760, 210
s2.append(_box(ax, ay - 120, 80, 120))
s2.append(_box(ax + 27.5, ay - 168, 25, 150))
s2.append(_ln(ax - 16, ay, ax + 96, ay, INK, 0.7))
for i in range(-2, 8):
    s2.append(_ln(ax - 10 + i * 8, ay + 4, ax + 6 + i * 8, ay + 22, '#777', 0.4))
s2.append(_note(ax + 96, ay - 150, ['125×125 H5 PILE'], (ax + 40, ay - 150)))
s2.append(_note(ax + 96, ay - 70, ['400×400 HOLE', '600 DEEP', 'NO ROD'], (ax + 70, ay - 60)))
s2.append(_note(ax - 150, ay - 20, ['150 MIN CLEAR', 'OF THE PATH', 'ON THE DECK PILES'], (ax + 10, ay - 8)))
s2.append(_tx(ax + 40, ay + 42, 'DETAIL A - PILE', 10, 'middle', GREEN, '700'))
s2.append(_ln(ax - 10, ay + 45, ax + 90, ay + 45, GREEN, 0.8))
s2.append(_tx(ax + 40, ay + 58, 'SCALE 1:10', 7.5, 'middle', GREEN, '600'))

# Detail B, the two steps, 1:10.
bx, bz = 700, 640

def SY(y):
    return bx + (y - 2350) * k10

def SZ(z):
    return bz - z * k10

s2.append(_ln(SY(2280), SZ(0), SY(2448), SZ(0), INK, 0.8))
s2.append(_ln(SY(2572), SZ(0), SY(3053), SZ(0), INK, 0.8))
s2.append(_ln(SY(3178), SZ(0), SY(3380), SZ(0), INK, 0.8))
s2.append(_box(SY(2510 - 62.5), SZ(187), 125 * k10, (187 + 220) * k10))
s2.append(_box(SY(2510 - 45), SZ(328), 90 * k10, 140 * k10))
s2.append(_box(SY(2360), SZ(468), 195 * k10, 140 * k10))
s2.append(_box(SY(2360), SZ(500), 240 * k10, 32 * k10))
s2.append(_box(SY(2555), SZ(135), 605 * k10, 120 * k10))
s2.append(_box(SY(3115 - 62.5), SZ(15), 125 * k10, (15 + 280) * k10))
s2.append(_box(SY(2555), SZ(161), 325 * k10, 26 * k10))
s2.append(_box(SY(2555), SZ(301), 325 * k10, 140 * k10))
s2.append(_box(SY(2600), SZ(333), 280 * k10, 32 * k10))
s2.append(_box(SY(2880), SZ(167), 280 * k10, 32 * k10))
s2.append(_hdim(SY(2600), SY(2880), SZ(400), '280'))
s2.append(_hdim(SY(2880), SY(3160), SZ(230), '280'))
s2.append(_tx(SY(3360), SZ(8), '15 CLEAR', 8, 'start', RED))
s2.append(_tx(SY(2200), SZ(520), '+500', 8, 'end', RED))
s2.append(_tx(SY(2480), SZ(360), '+333', 8, 'end', RED))
s2.append(_tx(SY(3180), SZ(200), '+167', 8, 'start', RED))
s2.append(_note(SY(3520), SZ(150), ['RIP TO 120 MIN', 'OVER THE PATH'], (SY(2900), SZ(55))))
s2.append(_tx(SY(2750), 458, 'DETAIL B - TWO STEPS', 10, 'middle', GREEN, '700'))
s2.append(_ln(SY(2580), 461, SY(2920), 461, GREEN, 0.8))
s2.append(_tx(SY(2750), 474, 'SCALE 1:10', 7.5, 'middle', GREEN, '600'))
s2.append(_tx(SY(2700), SZ(-90), 'PATH = 0.000 LOCAL', 7.5, 'middle', GREEN, '500'))
(root / 'site/drawings' / 'sheet2.svg').write_text(_sheet(s2, 'Sheet 2. Notes, cross section, pile hole and the two steps. Ref ISL38807. Consent exempt, not lodged.'))

# Sheet 3. Site of the works only, levels, schedules. No invented boundaries.
s3 = []
_title(s3, 3, '1:100', '03  SITE, LEVELS AND SCHEDULES')
ks = 0.02

def SX(x):
    return 70 + x * ks

def SY3(y):
    return 150 + y * ks

s3.append(_tx(36, 40, 'SITE PLAN — WORKS AREA ONLY', 11, 'start', GREEN, '700'))
s3.append(_tx(36, 54, 'SCALE 1:100. HOUSE DEPTH, PATH WIDTH AND BOUNDARIES ARE NOT SURVEYED, SO THEY ARE NOT DIMENSIONED.', 7, 'start', GREEN, '500'))
s3.append(_ln(SX(0), SY3(-1970), SX(900), SY3(-1970), INK, 1.3))
s3.append(_tx(SX(0), SY3(-1970) - 8, 'EXISTING HOUSE WALL', 7.5, 'start', GREEN, '600'))
s3.append(_box(SX(0), SY3(-1970), 900 * ks, 1970 * ks))
s3.append(_tx(SX(1100), SY3(-1100), 'REBUILT 900×1970', 7, 'start', INK, '600'))
s3.append(_box(SX(0), SY3(0), 6600 * ks, 2600 * ks))
s3.append(_tx(SX(3300), SY3(1200), 'DECK 6600×2600', 8, 'middle', INK, '700'))
s3.append(_tx(SX(3300), SY3(1200) + 12, 'FFL +500', 7.5, 'middle', GREEN, '600'))
s3.append(_box(SX(0), SY3(2600), 6600 * ks, 560 * ks))
s3.append(_tx(SX(6800), SY3(3000), 'STEPS', 7, 'start', INK, '600'))
s3.append(_hdim(SX(0), SX(6600), SY3(3600), '6600'))
s3.append(_vdim(SX(9000), SY3(0), SY3(2600), '2600'))
s3.append(_vdim(SX(9800), SY3(2600), SY3(3160), '560'))
s3.append(_ln(SX(0), SY3(4800), SX(1000), SY3(4800), RED, 0.7))
s3.append(_tx(SX(500), SY3(4800) - 4, '1000', 7, 'middle', RED))
s3.append(_tx(SX(500), SY3(4800) + 12, 'SCALE BAR 1:100', 6.5, 'middle', INK))
s3.append(_tx(36, 300, 'NORTH IS NOT SURVEYED. NO ARROW.', 7.2, 'start', GREEN, '600'))
s3.append(_tx(36, 316, 'WEST END: DRAINS. SPADE. 500 CLEAR. PATH STAYS. NO HOLE IN IT.', 7.2, 'start', GREEN, '500'))
s3.append(_tx(36, 332, 'PATH = 0.000 LOCAL.', 7.2, 'start', GREEN, '500'))

# Schedules, right side.
s3.append(_tx(560, 40, 'LEVELS — LOCAL DATUM', 9, 'start', GREEN, '700'))
s3.append(_tx(560, 54, 'PATH SURFACE IS 0. NOT AUCKLAND 1946.', 7, 'start', INK, '500'))
levels = [
    ('PATH', '0'),
    ('GRASS', 'LOWER, NOT TAPED'),
    ('PILE TOP', '+187'),
    ('BEARER TOP', '+328'),
    ('JOIST TOP', '+468'),
    ('DECK BOARDS, FFL', '+500'),
    ('TOP STEP BOARD', '+333'),
    ('BOTTOM STEP BOARD', '+167'),
]
s3.append(_ln(560, 64, 1120, 64, INK, 0.6))
for i, (name, val) in enumerate(levels):
    y = 80 + i * 16
    s3.append(_tx(566, y, name, 7.5, 'start', INK, '500'))
    s3.append(_tx(1114, y, val, 7.5, 'end', INK, '600'))
    s3.append(_ln(560, y + 4, 1120, y + 4, INK, 0.3))
s3.append(_tx(560, 230, 'PILE SCHEDULE', 9, 'start', GREEN, '700'))
s3.append(_ln(560, 238, 1120, 238, INK, 0.6))
heads = [('MARK', 566), ('QTY', 660), ('MEMBER', 720), ('HOLE', 900), ('NOTE', 1040)]
for label, x in heads:
    s3.append(_tx(x, 254, label, 7, 'start', INK, '700'))
rows_p = [
    ('P1', '16', '125×125 H5', '400×400×600', 'NO ROD'),
    ('P2', '6', '125×125 H5', '300×300×400', 'STEPS'),
    ('R', '4', '125×125 H5', '400×400×600', 'REBUILT'),
]
for i, row in enumerate(rows_p):
    y = 272 + i * 16
    xs = [566, 660, 720, 900, 1040]
    for val, x in zip(row, xs):
        s3.append(_tx(x, y, val, 7.5, 'start', INK, '500'))
s3.append(_tx(560, 330, 'FRAMING SCHEDULE — FINISHED SIZES', 9, 'start', GREEN, '700'))
s3.append(_ln(560, 338, 1120, 338, INK, 0.6))
framing = [
    'BEARERS  140×45 SG8 H3.2 DOUBLE. 190×45 DOUBLE ON THE 2390 BAY. TOPS LINED UP',
    'JOISTS  140×45 SG8 H3.2, 437 CENTRES, DOUBLED AT 3956',
    'REBUILT  140×45 SG8 H3.2, 900×1970, NOT INTO THE DECK',
    'STEPS  140×45 SG8 H4, TWO GOINGS OF 280, FULL WIDTH',
    'BOARDS  88×32 H3.2 MERCH GRIPTREAD, ALONG THE DECK',
    'BOTTOM BEAM RIPPED TO 120 MIN WHERE IT MEETS THE PATH',
]
for i, line in enumerate(framing):
    s3.append(_tx(566, 356 + i * 16, line, 7.2, 'start', INK, '500'))
s3.append(_tx(560, 470, 'DRAWING INDEX', 9, 'start', GREEN, '700'))
s3.append(_ln(560, 478, 1120, 478, INK, 0.6))
index = [
    '01  FOUNDATION AND FRAMING PLAN, LONG SECTION A-A   1:25',
    '02  CROSS SECTION B-B, DETAIL A PILE, DETAIL B STEPS  1:25 / 1:10',
    '03  SITE, LEVELS AND SCHEDULES   1:100',
]
for i, line in enumerate(index):
    s3.append(_tx(566, 496 + i * 16, line, 7.2, 'start', INK, '500'))
s3.append(_tx(560, 570, 'REVISION A  ·  11/11/26  ·  WORKING SET', 8, 'start', GREEN, '700'))
s3.append(_tx(560, 586, 'CONSENT NOT REQUIRED. NOT LODGED. NOT ENGINEER CHECKED.', 7.2, 'start', GREEN, '500'))
s3.append(_tx(560, 610, 'BRACING IS A DEPARTURE FROM NZS 3604 cl 7.4.2.2.', 7.2, 'start', GREEN, '500'))
s3.append(_tx(560, 626, 'SEE NOTE 7 ON SHEET 2.', 7.2, 'start', GREEN, '500'))
(root / 'site/drawings' / 'sheet3.svg').write_text(_sheet(s3, 'Sheet 3. Site of the works, levels and schedules. Ref ISL38807. Consent exempt, not lodged. Boundaries not surveyed.'))
print('sheets', len(s1), len(s2), len(s3))


