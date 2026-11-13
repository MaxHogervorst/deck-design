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
    ('Timber', '140×45 SG8 H3.2 framing, wet. Joists, rims and the rebuilt strip', '72', 'm', 12 * 70.91, 'Bunnings', '12×6.0 m at $70.91. The two rims are 6.6 m, so splice each one. 7.2 m is not listed. The main bearers are the 190 line, not this one', 'posted', 'https://www.bunnings.co.nz/140-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-6m_p0616262'),
    ('Timber', '190×70 SG8 H3.2 doubled bearers, both rows, full length', '28.8', 'm', None, 'Merchant', 'Six 4.8 m lengths. Four plies. Each long piece butts on the pile at 4500 and runs over the two 2.1 m bays. The end piece is the 1.8 m bay. Not on the Bunnings rack. Ask the yard', 'alt', ''),
    ('Timber', '150×50 SG8 H4 for the two steps. 140×45 H4 is not listed', '72', 'm', 72 * 17.11, 'Bunnings', 'Special order at $17.11/m. Mitre 10 lists 150×50 H4 from $11.96/m, but that is N2 grade, not SG8', 'posted', 'https://www.bunnings.co.nz/150-x-50mm-sg8-h4-wet-sawn-treated-timber-per-linear-metre_p0276210'),
    ('Piles', '125×125 H5 house pile, 6.0 m', '1', 'ea', 8 * 21.04, 'Bunnings', 'One 6.0 m length, cut into the eight deck piles. Bunnings does not sell 6.0 m. Eight 0.75 m piles are the same 6.0 m at $21.04. Two 3.6 m lengths are $103.82 each. None for the rebuilt strip', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
    ('Piles', '125×125 H5 pile, 750 mm', '4', 'ea', 4 * 21.04, 'Bunnings', 'Four under the bottom step, on the same lines as the deck piles. Later, with the steps. $21.04. Most of the length gets cut off', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
    ('Decking', '88×32 H3.2 merch griptread', f'{deck["stock_lm"]}', 'm', deck['stock_lm'] * 4.55, 'Bunnings', f'{deck["stock_4200"]}×4.2 m and {deck["stock_3000"]}×3.0 m at $4.55/m. The listed price is the random-length bin. Named lengths, so the butts land on the doubled joist. Trade price is $4.33/m and needs a PowerPass', 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
    ('Fasteners', 'Decking screws 10g×65, coated for treated pine', '1500', 'ea', 3 * 75.92, 'Bunnings', f'3×500 Buildex Climacoat at $75.92. CCA decking, zone C, so stainless is not required. A 304 decking screw is about $234 for the same 1500 and is the one to take if the heads will show. {deck["base_screws"]} positions', 'posted', 'https://www.bunnings.co.nz/buildex-10g-x-65mm-climacoat-rapiddrive-treated-pine-screws-500-pack_p0417168'),
    ('Fasteners', 'Framing nails 90×3.55 galvanised jolt head', '7', 'kg', 51.98 + 26.65, 'Bunnings', '1×5 kg at $51.98 and 1×2 kg at $26.65. Hot-dip galvanised. Bearer plies and the step beams. The stainless nails only came in 4 mm', 'posted', 'https://www.bunnings.co.nz/nz-nails-90-x-3-55mm-5kg-galvanised-jolt-head-nail_p0318485'),
    ('Fasteners', 'Framing nails 100×4 galvanised flat head', '5', 'kg', 51.77, 'Bunnings', 'One 5 kg tub at $51.77. Joists, rims and the skew nails. The heads are buried, so a flat head is fine', 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-5kg-galvanised-flat-head-nail_p0318604'),
    ('Fasteners', 'Batten screws 14g×100 class 3 galvanised', '100', 'ea', 29.95, 'Bunnings', 'One box, $29.95. Step ribbons, and the rebuilt joists. Class 3, for outside', 'posted', 'https://www.bunnings.co.nz/titan-14g-x-100mm-cl3-gal-bugle-batten-screw-100-pack_p0579091'),
    ('Fasteners', 'M12×120 316 coach bolt, nut, two 50 mm washers', '5', 'ea', 5 * (4.90 + 1.25 + 2 * 3.54), 'Bunnings', 'Two into the existing bearer and three through the house ledger into the framing. $4.90 + $1.25 + 2×$3.54 each. Not into the weatherboards', 'posted', 'https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
    ('Concrete', 'Ready-mix 20 MPa, small load', '2.0', 'm³', 650, 'Auckland plant', 'Not a published price. On site the figure was about $600 for the 1.1 m³ in the twelve holes. This load is still about $650 until Firth or Allied prices Point Chevalier. Firth adds $9.90/m³ fuel on top of the quote. Do not add the cement as well', 'estimate', 'https://www.firth.co.nz/temporary-fuel-surcharge'),
    ('Concrete', 'Portland cement, 20 kg. Only if mixing on site', '12', 'ea', 12 * 11.59, 'Bunnings', 'Cemix Ecostrong $11.59. Twelve bags for the 0.59 m³ in the eight holes. Four shovels of builders mix to one shovel of cement. Not premixed concrete bags. Steps are later', 'alt', 'https://www.bunnings.co.nz/cemix-20kg-low-carbon-cement_p0581734'),
    ('Concrete', 'Builders mix BM20. Only if mixing on site', '1.0', 'm³', 1.0 * 126.50, 'Auckland Aggregates', '$126.50/m³ including GST. Cartage is priced by the kilometre and is not in this figure. This replaces the truck, so it is not in the total', 'alt', 'https://www.aucklandaggregates.co.nz/shop/product/577984/bm-20--builders-mix-virgin-aggregate/'),
    ('DPC', 'DPC Supercourse 500, 150 mm×30 m', '1', 'ea', 27.42, 'Bunnings', 'On every pile top. $27.42', 'posted', 'https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
    ('DPC', 'Metalex Green, 1 L', '1', 'ea', 66.00, 'Bunnings', 'On every saw cut. $66', 'posted', 'https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
]
priced = []
for cat, item, qty, unit, price, store, comment, kind, url in rows:
    shown = 0.0 if price is None else round(float(price), 2)
    priced.append((cat, item, qty, unit, shown, store, shown if kind != 'alt' else 0.0, comment, kind, url))
posted = round(sum(r[6] for r in priced if r[8] == 'posted'), 2)
est = round(sum(r[6] for r in priced if r[8] == 'estimate'), 2)
total = round(posted + est, 2)
steps = [
    'Before you buy. Match the old deck: the new boards sit at that same 500 mm, not 500 mm above the low grass. Measure from the old boards down to the concrete path. Joists need about 330 mm of air over the path and the bearers about 190 mm. The steps are measured off the path as well, because that is where you walk. Tape that height and divide by three. If it is 500, each rise is 167. The lawn is lower and is not the step. Check the sill and the cladding. Formby Avenue is about 1.1 km from the harbour, outside the 500 m sea-spray zone, so the nails and the screws are galvanised. The two bolts stay stainless. A services reply that says no power within 10 m is not to be trusted: there is power. Mark the stormwater and the waste before any digging.',
    'Set out. String the 6600×2600 outline. The rebuilt strip is 900 wide and runs 1970 back to the house wall. It has no holes. The steps stick out 560 mm past the front, two goings of 280. Leave the path. End joist flush, then 437 mm centres, doubled joist centred at 3956. Four pile lines, measured from the eastern end: 300, 2400, 4500, 6300, on both bearers. That is 300 mm past each end pile, then bays of 2100, 2100 and 1800. Eight holes. Paint the marks and shift a line if it lands on the path or within 500 mm of a pipe. The four step holes go on those same lines, 560 mm out, when the steps are built. Do not mark holes in the gap by the house.',
    'Dig, with a spade. Every deck hole is 400×400 and 600 deep, down to firm ground, not topsoil. No 900 mm anchor holes. At 600 a shovel is enough. An auger only earns its keep past 600, and these holes do not go there. About ten minutes a hole. No hole in the concrete, no hole between the blue pipe and the sewage, and no hole edge within 500 mm of either. No spare hole on the pipe side of the path.',
    f'Concrete. The eight deck holes are this pour. Fill to 100 mm below the ground. The pile sits on 100 mm of concrete at the bottom, so the concrete is about {cv["main_pour_m3"]:.2f} m³. Twelve 20 kg bags of cement and 1 m³ of builders mix, four shovels of mix to one of cement. The four step holes are later. Order {cv["readymix_order_m3"]:.1f} m³ only if the yard will not sell less, and ask what they charge to take the rest back. A hired mixer. Do not use premixed concrete bags. Nothing in the hole has to be level.',
    'Cut the piles. One 6.0 m length makes the eight piles. String off the path, not the lawn. The bearer is 190 deep, so the pile tops finish at about +138, which is 190 mm below the bearer top at +328. That is 12 mm under the 150 mm NZS 3604 wants between H3.2 and the path. The grass is lower, so cut those piles first. Cut square, preservative on the cut, DPC on the top. Do not notch the bearer.',
    'Bearers. Doubled 190×70 on both rows of the deck, the whole length (F1). Each ply is a 4.8 m length from the eastern end, butted on the pile at 4500, so that piece runs over the two 2.1 m bays. The remaining piece is the 1.8 m bay. Seat them and skew-nail (F2). No anchor brackets. Leave the existing bearer at the back edge. The rebuilt strip bolts to it at one end and to the house framing at the other.',
    'Joists and rims. 17 joists of 2510: flush at each end, 437 centres, the doubled joist at 3956. Screws into a bearer go in from the side of the joist, not down through the top. The rebuilt strip is three joists of 2270, 45 mm beside the deck joists, from the house ledger to the first new bearer so the lap can be nailed (F4, F6). No blocks and no holes. Rims at Y0 and Y2555. Get the deck frame up before the steps. The step height is in mid-air until the deck is there. Offcuts can be a temporary step.',
    'Step piles. Later, with the deck frame up. Dig the four small holes, 300×300 and 400 deep, on the same X as the front piles and 560 mm out from the face. Not 600. No extra hole beside the path. Stand a 750 mm pile, plumb it, and concrete it. Cut it so the front beam will finish with its top about 135 mm above the path.',
    'Bottom step. Screw the inner ply of the H4 ribbon to the front piles, four 14g×100 screws each, then nail the outer ply to the inner one (F5). Joists out from it, cut about 500, on the same lines as the deck joists. Double front beam on the small piles, full depth, one piece so it runs over the piles. Top of this framing about 135 mm above the path, so the 32 mm board finishes at about 167. Do not rip it. Where the full depth meets the concrete, chase the path under the timber. A ripped beam is not a size in Table 6.4.',
    'Top step, on the bottom one. Set it back one going, 280 mm. Double ribbon screwed to the face of the front bearer (F7), short joists cut about 240, front beam packed off the bottom step so the framing top is about 301 mm above the path. The board then finishes at about 333. Tape the three rises off the path and make them equal. Do not cut a stringer. No handrail. Three rises is the limit. One more would need a rail.',
    'Boards. 28 rows on the deck, 21 on the rebuilt strip, three on each step, all along X. Butts on the doubled joist at 3956, so use the 4.2 m and 3.0 m lengths. A decking board on the face of the boundary joist, the top board over it, and a board on each riser. About 5 mm gaps on the deck and about 6 mm on the rebuilt strip. Two screws per board per joist. Preservative on every cut.',
]
fixings = [
    ('F1', 'Double bearers and the step beams', '90×3.55 galvanised jolt nails, two rows at 250 mm centres, staggered. Same on each double step beam and ribbon.'),
    ('F2', 'Pile to bearer, and the small step piles', 'Four 100×4 galvanised skew nails. Same four nails from the front beam down into each small pile.'),
    ('F3', 'Joists, rims, blocks', 'Two 100×4 galvanised nails per joist end, through the rim or into the ribbon.'),
    ('F4', 'Rebuilt joists', 'Set 45 mm beside the deck joists. Four 100×4 nails through the lap, and four skew nails into the bearer.'),
    ('F5', 'Bottom-step ribbon to the front piles', 'Screw the inner ply only: four 14g×100 screws into each pile, in from the side, about 55 mm of thread in the pile. Nail the outer ply to the inner one with the F1 nails. A screw through both plies has about 10 mm left in the pile, which is not a fixing.'),
    ('F6', 'Rebuilt strip', 'Two M12×120 bolts through the new bearer into the existing bearer, at X200 and X700. Three more through the house ledger into the framing, not into the weatherboards. Flash the penetration. 50 mm square washers both sides.'),
    ('F7', 'Top-step ribbon to the front bearer', 'Same as F5: screw the inner ply into the bearer face at each pile, then nail the outer ply on. The front of this step sits on the bottom step, packed so the rises match.'),
    ('F8', 'Face board and the two risers', 'A decking board on the boundary joist, and one on each riser. The top board laps over the face board.'),
]

def money(n):
    return f'${n:,.2f}'

md = f'''# Deck and step build guide

{DATE} · How I am going to build the 6.6 m deck and the two steps in front of it. One plan, three sheets, a bill of materials and the build order. Written for me, doing the work. It is not an engineer's design. Consent is not required: Building Act Schedule 1, exemption 24, because a fall is about 500 mm. The sheets are still drawn to AS/NZS 1100.501 and the Auckland Council AC1011 document list. They are not lodged.

## What we are building

| Part | What |
|---|---|
| Main deck | 6600×2600 mm, boards level with the old deck, about 500 mm. Two double 190×70 H3.2 bearers on 8 timber piles at Y300 and Y2510. Joists 140×45 across them, span 2.21 m. NZS 3604 Table 7.1(b), wet, allows 2.35 m at 450 centres. |
| Main joists | 17 members. Flush at the end, then 437 mm centres, one doubled joist centred at 3956 for the board butts. Rims at Y0 and Y2555. No blocking. |
| Rebuilt strip | 900×1970 mm, from the house wall to the existing bearer, then 300 mm on to the first new bearer. No piles. Three 140×45 joists of 2270, each 45 mm beside a deck joist so the lap can be nailed. The long span is 1970 mm. Table 7.1(b) allows 2350 mm. The main deck is not carried by the house. |
| Steps | Two steps, three rises, the full width of the deck, sticking out 560 mm. Going 280. Rise about 167 if the path-to-board tape is 500. Double H4, the listed 150×50 SG8. Bottom step: a ribbon on the front piles, joists out, a front beam on four small piles. Top step built on that and screwed to the bearer. Not a cut stringer. The beam is not ripped. Built after the deck. |
| Boards | 88×32 merch griptread, along X. 28 rows on the deck, 21 on the rebuilt strip, three on each step. A board on the face of the boundary joist, and one on each riser. |
| Finish | Natural, no handrail. Three rises is the limit. One more rise and it would need a rail. Lawn and path stay as they are. |

Set-out, X from the eastern end. Piles: 300, 2400, 4500, 6300 on Y300 and Y2510. Eight holes. The bearer overhangs 300 mm past each end pile. The bays are 2100, 2100 and 1800 mm. NZS 3604 Table 6.4(b), wet, 2 kPa, allows a 190×70 bearer to span 2.7 m when it is continuous over two or more spans and the loaded dimension is 1.65 m. These bearers are two 190×70 plies. The long piece butts on the pile at 4500 and covers the two 2.1 m bays. The end piece is the single 1.8 m bay. The same standard caps a bearer overhang at 200 mm when the bearers are more than 2 m apart, and these are 2.21 m apart. The 300 mm is the set-out from the builder. Mark the holes and move one if it lands on the path or within 500 mm of a pipe. The four step piles are on those same X, at Y3115, and they are dug with the steps. The rebuilt strip has no piles.

Heights. The path is where you walk and the grass is lower, so the steps are taped off the path. Deck boards +500 if that is what the old deck measures, joist top +468, bearer top +328, pile top +138. Bottom step board about +167, framing top +135. Top step board about +333, framing top +301. If the tape from the path to the deck boards is not 500, divide whatever it is by three.

## The sheets

[Sheet 1 · Foundation and framing](docs/drawings/sheet.svg) · [Sheet 2 · Section and details](docs/drawings/sheet2.svg) · [Sheet 3 · Site, levels and schedules](docs/drawings/sheet3.svg). A2, to AS/NZS 1100.501 and the Auckland Council AC1011 list. Consent is not required. These sheets are not lodged.

## Foundations

8 timber piles under the deck: 400×400 holes, 600 deep. No holes for the rebuilt strip. No 900 mm anchors and no brackets. The step has four smaller holes, 300×300 and 400 deep, dug later. No spare hole on the pipe side of the path.

The eight holes are dug 400×400×600. Fill to 100 mm below the ground. The pile sits on 100 mm of concrete at the bottom, so this pour is about {cv["main_pour_m3"]:.2f} m³. Twelve 20 kg bags of cement and 1 m³ of builders mix. Not premixed concrete bags. A truck minimum is still often {cv["readymix_order_m3"]:.1f} m³, which is more than the holes. Ask the yard the smallest load and the fee to take the rest back. The steps are a later pour.

The path stays. The deck is built over it. A 190 bearer with its top at +328 has its underside at +138, which is 12 mm under the 150 mm NZS 3604 wants for H3.2 above a surface. The grass is lower, so the piles there still clear 150 mm. No hole through the concrete. Do not open a bay past 2.7 m. The longest bay is 2.1 m.

The waste and the stormwater run together on the right of the path, the west side. The blue pipe is 400 mm past the concrete. The sewage is 130 mm past the blue one: the plan has one pipe 740 mm off the deck and the other 870 mm off the deck. Beside the deck they are about 440 to 470 mm deep, and only 240 to 270 mm deep beside the pad. The hole is 600 deep, so it goes below them. No hole edge within 500 mm of either pipe, and no hole between them. Stormwater goes out through the gate. The left of the path, the meter-box side, is clear. Orange is power, white is fibre, water is its own pipe. Dig with a spade.

### The two steps

A single 250 mm rise is too big. About 190 is the limit and 200 is a push. Two steps make three rises of about 167, and 2×167+280 comes out at 613, inside 550 to 700. No handrail at three rises.

Build the deck first. Then the bottom step, then the top step on it, set back 280 mm. Tape the rises off the path until they match. Do not cut a stringer.

The bottom framing only has about 135 mm above the path. The beam stays full depth, because Table 6.4 has no ripped size. At a loaded dimension under 1.30 m the same table allows a doubled 140 to span 3.0 m, continuous, and the longest step bay is 2.1 m. Where the timber meets the concrete, chase the path under it. Do not cantilever the joists off the bearer: they sit below it and they are only 500 mm long. The small pile sees about {sc["step_pile_bearing_kPa"]:.0f} kPa on a 300×300.

The underside of that bottom step is not 150 mm clear of the path. There is no way to have that and still walk off onto the path in even rises. It is H4 because it will stay damp. The deck bearer is H3.2 and sits 138 mm above the path, 12 mm short of the same 150 mm.

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
    if not url and kind == 'alt':
        cell = 'Ask the yard'
    else:
        cell = f'[{money(price)}]({url})' if url else money(price)
    note = comment + (' Not in the total.' if kind == 'alt' else '')
    md += f'| {item} | {qty} | {unit} | {cell} | {store} | {note} |\n'
md += f'''
**Posted ${posted:,.2f} + estimates ${est:,.2f} = about ${total:,.0f} including GST.** The total uses the truck and does not include the 190×70 bearers, which are not a posted price. If the holes are mixed on site, take the truck out and add the cement. The builders mix is a yard quote and is not in the number either way. Do not add the truck and the cement together.

Pack sizes are already rounded up for the nails and the screws. Pile lengths are long on purpose. No allowance for a wasted bolt, or for timber used as a temporary brace. Delivery, the mixer and carting the spoil are extra. The nails and the screws are galvanised. The bolts stay stainless.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Main and rebuilt: {d["main_stock_lm"]} m in the cut list, {d["main_installed_lm"]} m used. 6600 is the two rims. 2510 is the 17 joists. 2270 is the three rebuilt joists, 45 mm beside the deck joists and lapped to the first new bearer. 900 is the bearer on the existing one, and the house ledger. Buy 12×6.0 m and splice the rims. 7.2 m is not listed. The main bearers are not in this list. They are six 4.8 m lengths of 190×70. Four run from the eastern end to the pile at 4500. The other two lengths are cut into the four end pieces.

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
- **The steps.** The front beam is a doubled 140, full depth, continuous, and the longest bay is 2.1 m. Table 6.4(b) allows 3.0 m at a loaded dimension of 1.30 m. It is not ripped. Where it meets the path, the concrete is chased. The screws go through the inner ply only. The bottom step does not have 150 mm clearance over the path. The rises are even. They are not a consented stair. The four step holes are dug after the deck.
- **The services reply.** It said no gas and no power within 10 m. The power is there. Drain depths are approximate. Paint, spade, and move a hole rather than dig through a pipe.
- **Fixings.** Formby Avenue is about 1.1 km from the harbour, past the 500 m sea-spray line, so this is zone C. The nails and the screws are galvanised. The deck is open, so the two bolts stay 316. The decking is CCA. Do not swap in ACQ timber and keep these screws.
- **The path.** It stays. The piles are on a regular grid, 300 mm in from each end, then 2.1 m, 2.1 m and 1.8 m. Paint them and move a hole if it lands on the concrete or within 500 mm of a pipe. Both bearers are doubled 190×70. Table 6.4(b) allows one 190×70 to span 2.7 m, and the longest bay is 2.1 m. The steps are taped off the path, not off the lawn.
- **Prices.** Auckland only, read on 12 November 2026. Marton, Horotiu and Stratford are left out. Each line is the cheapest posted price, and the store is named. The H4 line is 150×50 SG8 because 140×45 H4 is not listed. N2 H4 is cheaper and is the wrong grade. The truck is the figure from site, not a Point Chevalier quote.
- **The rebuilt strip.** No holes. The joists run from the house ledger to the first new bearer, 45 mm beside the deck joists, and the lap is nailed. The long span is 1970 mm and Table 7.1(b) allows 2350 mm. Bolt the ledger into the framing and flash it. Do not fix it to the weatherboards. The main deck is on its own eight piles.

## Sources

Northpine wet-service joist table, which reproduces NZS 3604 Table 7.1(b): 140×45 SG8 at 450 centres spans 2.35 m. Bearer spans are NZS 3604:2011 Table 6.4(b), 2 kPa, wet in service: a 190×70 continuous over two or more spans spans 2.7 m at a loaded dimension of 1.65 m, and a 140×90 spans 3.0 m at 1.30 m. NZS 3604 wants H3.2 150 mm clear of a surface. The 190 bearer over the path is at 138 mm, and the bottom step is closer than that. The stair proportion used here is a rise under 190 and 2R+G between 550 and 700. [Northpine tables](https://www.northpine.co.nz/span-tables) · [BRANZ Bulletin 611](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf).

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
</section>'''
body = sheets + schedules
html = '''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="ISL38807. Proposed deck for 18B Formby Avenue. Three sheets, not lodged."><title>ISL38807 · 18B Formby Avenue</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">ISL38807 <span>18B FORMBY AVENUE · NOT LODGED</span></a><nav aria-label="Sections"><a href="#sheets">Sheets</a><a href="#shopping-list">Schedule</a></nav><button id="print">Print</button></header><main id="main">''' + body + '''</main><footer><span>AS/NZS 1100.501 · Exemption 24 · Do not scale</span></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
(root / 'site/index.html').write_text(html)
print('Rendered guide, CSV and page; posted', posted, 'estimates', est, 'total', total)


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
for x in d['rebuilt_joist_X_mm']:
    s1.append(_ln(PX(x), PY(-1970), PX(x), PY(300), RED, 0.7))
for y, length in ((300, 6600), (2510, 6600)):
    s1.append(_ln(PX(0), PY(y - 70), PX(length), PY(y - 70), INK, 0.9))
    s1.append(_ln(PX(0), PY(y + 70), PX(length), PY(y + 70), INK, 0.9))
s1.append(_ln(PX(0), PY(2555), PX(6600), PY(2555), INK, 0.7))
s1.append(_ln(PX(0), PY(3070), PX(6600), PY(3070), INK, 0.7))
s1.append(_ln(PX(0), PY(3160), PX(6600), PY(3160), INK, 0.7))
for y in (300, 2510):
    for x in pile_x:
        s1.append(_box(PX(x - 200), PY(y - 200), 400 * K, 400 * K, '#8a8a8a', 0.4, '2 1.4'))
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
s1.append(_tx(PX((pile_x[1] + pile_x[2]) / 2), PY(2200), '190×70 DOUBLE', 8, 'middle', RED, '700'))
s1.append(_hdim(PX(0), PX(6600), chain + 16, '6600'))
s1.append(_tx(PX(0) - 2, chain - 10, '300', 7, 'end', RED))
s1.append(_tx(PX(6600) + 2, chain - 10, '300', 7, 'start', RED))
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
s1.append(_note(360, 46, ['DOUBLE BEARER', '190×70 BOTH ROWS', 'SPLICED AT 4500'], (PX(2400), PY(300))))
s1.append(_note(500, 46, ['NOTE', 'DECKING IS FIXED WITH', 'DECKING SCREWS'], (PX(4200), PY(80))))
s1.append(_note(188, 108, ['140×45 SG8 H3.2 JOIST', 'AT 437 CENTRES', 'DOUBLED AT 3956'], (PX(1770.5), PY(400))))
s1.append(_note(400, 108, ['125×125 H5 PILE', 'HOLE 400×400×600', 'NO ANCHOR BRACKET'], (PX(4500), PY(300))))
s1.append(_note(560, 118, ['TWO STEPS', 'GOING 280', 'SEE SHEET 2'], (PX(5000), PY(2880))))
s1.append(_tx(PX(450), 34, 'STRIP TO HOUSE  NO PILES', 7.5, 'middle', GREEN, '600'))

# Long elevation, aligned with the plan. True 1:25, so it is the thin strip.
def EZ(z):
    return 648 - z * K

s1.append(_ln(PX(0), EZ(0), PX(6600), EZ(0), INK, 0.9))
for x in pile_x:
    s1.append(_box(PX(x - 62.5), EZ(138), 125 * K, (138 + 40) * K))
s1.append(_box(PX(0), EZ(328), 6600 * K, 190 * K))
s1.append(_tx(PX(3300), EZ(110), '190×70 DOUBLE', 7, 'middle', RED))
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
    'BEARERS: 190×70 SG8 H3.2,',
    'DOUBLED, FULL LENGTH.',
    'JOISTS AND REBUILT STRIP:',
    '140×45 SG8 H3.2.',
    'STEPS: 150×50 SG8 H4.',
    'PILES: 125×125 H5.',
    'BOARDS: 88×32 H3.2.',
    '6. 8 DECK PILES. HOLE',
    '400×400, 600 DEEP.',
    'NO REBUILT PILES.',
    'FOUR STEP PILES, LATER.',
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
    s2.append(_box(EY(y - 62.5), EZ2(138), 125 * K, (138 + 80) * K))
    s2.append(_box(EY(y - 70), EZ2(328), 140 * K, 190 * K))
s2.append(_box(EY(0), EZ2(468), 2555 * K, 140 * K))
s2.append(_box(EY(0), EZ2(500), 2600 * K, 32 * K))
s2.append(_box(EY(2555), EZ2(135), 605 * K, 150 * K))
s2.append(_box(EY(2555), EZ2(161), 325 * K, 26 * K))
s2.append(_box(EY(2555), EZ2(301), 325 * K, 140 * K))
s2.append(_box(EY(2600), EZ2(333), 280 * K, 32 * K))
s2.append(_box(EY(2880), EZ2(167), 280 * K, 32 * K))
s2.append(_box(EY(3115 - 40), EZ2(15), 80 * K, (15 + 80) * K))
s2.append(_tx(EY(1400), 668, 'CROSS SECTION B-B', 10, 'middle', GREEN, '700'))
s2.append(_ln(EY(1400) - 48, 671, EY(1400) + 48, 671, GREEN, 0.8))
s2.append(_tx(EY(1400), 684, 'SCALE 1:25  ·  LOOKING ALONG THE DECK', 7, 'middle', GREEN, '600'))

# Detail A, pile hole. 0.2 units per mm. The hole is below the ground line.
ax, ay = 760, 168
s2.append(_box(ax, ay, 80, 120))
s2.append(_box(ax + 27.5, ay - 30, 25, 130))
s2.append(_ln(ax - 24, ay, ax + 104, ay, INK, 0.7))
for i in range(-3, 0):
    s2.append(_ln(ax - 8 + i * 8, ay + 6, ax + 8 + i * 8, ay + 22, '#777', 0.4))
for i in range(11, 14):
    s2.append(_ln(ax - 8 + i * 8, ay + 6, ax + 8 + i * 8, ay + 22, '#777', 0.4))
s2.append(_note(ax + 110, ay - 16, ['125×125 H5 PILE'], (ax + 40, ay - 16)))
s2.append(_note(ax + 110, ay + 48, ['400×400 HOLE', '600 DEEP', 'NO ROD'], (ax + 70, ay + 48)))
s2.append(_note(ax - 168, ay - 24, ['150 MIN CLEAR', 'OF THE PATH'], (ax + 12, ay - 8)))
s2.append(_note(ax - 168, ay + 88, ['100 CONCRETE', 'UNDER THE PILE'], (ax + 24, ay + 108)))
s2.append(_tx(ax + 40, ay + 148, 'DETAIL A - PILE', 10, 'middle', GREEN, '700'))
s2.append(_ln(ax - 10, ay + 151, ax + 90, ay + 151, GREEN, 0.8))
s2.append(_tx(ax + 40, ay + 164, 'SCALE 1:10', 7.5, 'middle', GREEN, '600'))

# Detail B, the two steps, 1:10.
k10 = 0.2
bx, bz = 700, 640

def SY(y):
    return bx + (y - 2350) * k10

def SZ(z):
    return bz - z * k10

s2.append(_ln(SY(2280), SZ(0), SY(2448), SZ(0), INK, 0.8))
s2.append(_ln(SY(2572), SZ(0), SY(3053), SZ(0), INK, 0.8))
s2.append(_ln(SY(3178), SZ(0), SY(3380), SZ(0), INK, 0.8))
s2.append(_box(SY(2510 - 62.5), SZ(138), 125 * k10, (138 + 220) * k10))
s2.append(_box(SY(2510 - 70), SZ(328), 140 * k10, 190 * k10))
s2.append(_box(SY(2360), SZ(468), 195 * k10, 140 * k10))
s2.append(_box(SY(2360), SZ(500), 240 * k10, 32 * k10))
s2.append(_box(SY(2555), SZ(135), 605 * k10, 150 * k10))
s2.append(_box(SY(3115 - 62.5), SZ(15), 125 * k10, (15 + 280) * k10))
s2.append(_box(SY(2555), SZ(161), 325 * k10, 26 * k10))
s2.append(_box(SY(2555), SZ(301), 325 * k10, 140 * k10))
s2.append(_box(SY(2600), SZ(333), 280 * k10, 32 * k10))
s2.append(_box(SY(2880), SZ(167), 280 * k10, 32 * k10))
s2.append(_hdim(SY(2600), SY(2880), SZ(400), '280'))
s2.append(_hdim(SY(2880), SY(3160), SZ(230), '280'))
s2.append(_tx(SY(3360), SZ(-20), 'CHASE PATH', 8, 'start', RED))
s2.append(_tx(SY(2200), SZ(520), '+500', 8, 'end', RED))
s2.append(_tx(SY(2480), SZ(360), '+333', 8, 'end', RED))
s2.append(_tx(SY(3180), SZ(200), '+167', 8, 'start', RED))
s2.append(_note(SY(3520), SZ(150), ['FULL DEPTH', 'DO NOT RIP'], (SY(2900), SZ(40))))
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
s3.append(_tx(SX(0), SY3(-1970) - 8, 'HOUSE WALL  LEDGER BOLTED TO FRAMING', 7, 'start', GREEN, '600'))
s3.append(_box(SX(0), SY3(-1970), 900 * ks, 1970 * ks))
s3.append(_tx(SX(1100), SY3(-1100), 'STRIP 900×1970', 7, 'start', INK, '600'))
s3.append(_tx(SX(1100), SY3(-1100) + 12, 'NO PILES. EXISTING BEARER TO HOUSE.', 7, 'start', GREEN, '600'))
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
    ('PILE TOP', '+138'),
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
    ('P1', '8', '125×125 H5', '400×400×600', 'DECK'),
    ('P2', '4', '125×125 H5', '300×300×400', 'STEPS, LATER'),
]
for i, row in enumerate(rows_p):
    y = 272 + i * 16
    xs = [566, 660, 720, 900, 1040]
    for val, x in zip(row, xs):
        s3.append(_tx(x, y, val, 7.5, 'start', INK, '500'))
s3.append(_tx(560, 330, 'FRAMING SCHEDULE — FINISHED SIZES', 9, 'start', GREEN, '700'))
s3.append(_ln(560, 338, 1120, 338, INK, 0.6))
framing = [
    'BEARERS  190×70 SG8 H3.2 DOUBLE, BOTH ROWS. SPLICE ON THE PILE AT 4500',
    'JOISTS  140×45 SG8 H3.2, 437 CENTRES, DOUBLED AT 3956',
    'REBUILT  3 JOISTS, 45 mm BESIDE THE DECK JOISTS, LAP NAILED',
    'STEPS  150×50 SG8 H4 DOUBLE, FULL DEPTH, TWO GOINGS OF 280',
    'BOARDS  88×32 H3.2 MERCH GRIPTREAD, ALONG THE DECK',
    'WHERE THE STEP MEETS THE PATH, CHASE THE CONCRETE. DO NOT RIP',
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


