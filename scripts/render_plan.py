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
deck_boards = round(deck['stock_lm'] - 9 * 7.2, 1)
step_boards = round(9 * 7.2, 1)
rows = [
    ('Deck', '140×45 SG8 H3.2, 12×6.0 m and 1×3.0 m', '75', 'm', round(471.24 * 75 / 72 * 1.15, 2), 'NZ Timber', '', 'posted', ''),
    ('Deck', '190×45 SG8 H3.2, 6×4.8 m', '28.8', 'm', round(216.00 * 1.15, 2), 'NZ Timber', '', 'posted', ''),
    ('Deck', '125×125 H5, 4×3.0 m', '4', 'ea', round(4 * 47.00 * 1.15, 2), 'NZ Timber', '', 'posted', ''),
    ('Deck', '88×32 decking', f'{deck_boards}', 'm', round(deck_boards * 4.55, 2), 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
    ('Deck', 'Decking screws 10g×65 304, 2×1000', '2000', 'ea', 2 * 149.00, 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/titan-10g-x-65mm-304-stainless-steel-wide-head-decking-screw-1000-pack_p0658845'),
    ('Deck', 'Nails 100×4 galv, 5 kg', '5', 'kg', 51.77, 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-5kg-galvanised-flat-head-nail_p0318604'),
    ('Deck', 'Nails 100×4 316, 2 kg', '2', 'kg', 119.00, 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-2kg-316-stainless-steel-flat-head-nail_p0325482'),
    ('Deck', 'M12×120 316 bolts, 5', '5', 'ea', 5 * (4.90 + 1.25 + 2 * 3.54), 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
    ('Deck', 'Cemix Multicrete 20 kg, 59 bags', '59', 'ea', round(59 * 11.24, 2), 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/cemix-20kg-multicrete_p0232228'),
    ('Deck', 'Cement 20 kg, 12 bags', '12', 'ea', round(12 * 11.59, 2), 'Bunnings', '', 'alt', 'https://www.bunnings.co.nz/cemix-20kg-low-carbon-cement_p0581734'),
    ('Deck', 'Builders mix, 1 m³', '1.0', 'm³', 126.50, 'Auckland Aggregates', '', 'alt', 'https://www.aucklandaggregates.co.nz/shop/product/577984/bm-20--builders-mix-virgin-aggregate/'),
    ('Deck', 'DPC 150 mm×30 m', '1', 'ea', 27.42, 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
    ('Deck', 'Metalex, 1 L', '1', 'ea', 66.00, 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
    ('Deck', 'NZ Timber tipper', '1', 'ea', round(110.00 * 1.15, 2), 'NZ Timber', '', 'posted', ''),
    ('Steps', '150×50 H4 SG8, 6×6.0 m', '6', 'ea', round(6 * 6 * 8.25 * 1.15, 2), 'Auckland Aggregates', '', 'posted', 'https://www.aucklandaggregates.co.nz/product/retaining-wall-rails-150x50-rs-h4-sg8/'),
    ('Steps', 'Cemix Multicrete 20 kg, 2 bags', '2', 'ea', round(2 * 11.24, 2), 'Bunnings', '', 'later', 'https://www.bunnings.co.nz/cemix-20kg-multicrete_p0232228'),
    ('Steps', '88×32 decking', f'{step_boards}', 'm', round(step_boards * 4.55, 2), 'Bunnings', '', 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
]
priced = []
for cat, item, qty, unit, price, store, comment, kind, url in rows:
    shown = 0.0 if price is None else round(float(price), 2)
    priced.append((cat, item, qty, unit, shown, store, shown if kind in ('posted', 'estimate') else 0.0, comment, kind, url))
posted = round(sum(r[6] for r in priced if r[8] == 'posted'), 2)
est = round(sum(r[6] for r in priced if r[8] == 'estimate'), 2)
total = round(posted + est, 2)
steps = [
    'Before you buy. Match the old deck: the new boards sit at that same 500 mm, not 500 mm above the low grass. Measure from the old boards down to the concrete path. Joists need about 330 mm of air over the path and the bearers about 190 mm. The steps are measured off the path as well, because that is where you walk. Tape that height and divide by three. If it is 500, each rise is 167. The lawn is lower and is not the step. Check the sill and the cladding. Formby Avenue is about 1.1 km from the harbour, outside the 500 m sea-spray zone. Decking screws are 304. Nails into the piles are 316, because those connections are within 600 mm of the ground. The other nails stay hot-dip galvanised. The bolts stay 316. A services reply that says no power within 10 m is not to be trusted: there is power. Mark the stormwater and the waste before any digging.',
    'Set out. String the 6900×2600 outline. The rebuilt strip is 900 wide and runs 1970 back to the house wall. It has no holes. The steps are 6600 long from the eastern end and stick out 560 mm past the front, two goings of 280. Leave the path. End joist flush, then 437 mm centres, doubled joist centred at 3956. Four pile lines, measured from the eastern end: 300, 2400, 4500, 6600, on both bearers. That is 300 mm past each end pile, then bays of 2100, 2100 and 2100. Eight holes. Paint the marks and shift a line if it lands on the path or within 500 mm of a pipe. The two step holes go at 300 and 6300, 560 mm out, when the steps are built. Do not mark holes in the gap by the house.',
    'Dig, with a spade. Every deck hole is 400×400 and 600 deep, down to firm ground, not topsoil. No 900 mm anchor holes. At 600 a shovel is enough. An auger only earns its keep past 600, and these holes do not go there. About ten minutes a hole. No hole in the concrete, no hole between the blue pipe and the sewage, and no hole edge within 500 mm of either. No spare hole on the pipe side of the path.',
    f'Concrete. Eight holes, about {cv["main_pour_m3"]:.2f} m³. Fill to 100 mm below the ground. The pile sits on 100 mm of concrete. 59 bags of Multicrete, or 12 bags of cement and 1 m³ of builders mix. Not a truck. The step is two holes, 200×200×200, 2 bags, later.',
    'Cut the piles. Four 3.0 m lengths. Cut each in half and stand the 1.5 m piece, so there is room to brace it. After the concrete, cut the top to about +138. Keep the offcuts. Four of them are the step piles. String off the path, not the lawn. The grass is lower, so cut those piles first. Cut square, preservative on the cut, DPC on the top. Do not notch the bearer.',
    'Bearers. Doubled 190×45 on both rows of the deck, the whole 6900 (F1). The pair is 90 mm wide and sits on the 125 pile. The two plies do not stop on the same pile. On each bearer, one ply is 4.50 m then 2.40 m and butts at 4500. The other is 2.40 m then 4.50 m and butts at 2400. One board is continuous across the other cut and the nails share the load into it. Seat them and skew-nail (F2). No anchor brackets. Leave the existing bearer at the back edge. The rebuilt strip bolts to it at one end and to the house framing at the other.',
    'Joists and rims. 18 joists of 2510: flush at each end, 437 centres, the doubled joist at 3956. The last two spaces are 368, so the end stays inside 450. Screws into a bearer go in from the side of the joist, not down through the top. The rebuilt strip is three joists of 2270, 45 mm beside the deck joists, from the house ledger to the first new bearer so the lap can be nailed (F4, F6). No blocks and no holes. Rims at Y0 and Y2555, each 3519 then 3381, joint on the joist at 3518. Get the deck frame up before the steps. The step height is in mid-air until the deck is there. Offcuts can be a temporary step.',
    'Step piles. Later. Two H5 offcuts. Two holes, 200×200×200, at X300 and X6300, 560 mm out. 2 bags of Multicrete. Not in the 59.',
    'Bottom step. One frame. Double H4 ribbon on the front piles, 12 joists of 500 out from it, double front beam on the two small piles. Nail the upper-tread packers on the inner half of those joists. Do not build a second frame. Do not rip the beam. Chase the path where the beam meets it.',
    'Boards. 28 rows on the deck, 21 on the rebuilt strip, three on each step, all along X. Butts on the doubled joist at 3956. The western piece is 2944, cut from a 3.0 m board. Tape the three rises off the path and make them equal. No handrail.',
]
fixings = [
    ('F1', 'Double bearers and the step beams', '100×4 hot-dip galvanised nails, two rows at 250 mm centres, staggered. Same nail as the joists. Same on each double step beam and ribbon.'),
    ('F2', 'Pile to bearer, and the small step piles', 'Four 100×4 316 stainless skew nails. Same four nails from the front beam down into each small pile. The box is 2 kg. About 32 nails go into the eight deck piles.'),
    ('F3', 'Joists, rims, blocks', 'Two 100×4 hot-dip galvanised nails per joist end, through the rim or into the ribbon.'),
    ('F4', 'Rebuilt joists', 'Set 45 mm beside the deck joists. Four 100×4 nails through the lap, and four skew nails into the bearer.'),
    ('F5', 'Bottom-step ribbon to the front piles', 'Four 100×4 316 nails through the inner ply into each pile, the same nails as F2. Nail the outer ply to the inner one with the F1 nails. A fastener through both plies has about 10 mm left in the pile, which is not a fixing.'),
    ('F6', 'Rebuilt strip', 'Two M12×120 bolts through the new bearer into the existing bearer, at X200 and X700. Three more through the house ledger into the framing, not into the weatherboards. Flash the penetration. 50 mm square washers both sides.'),
    ('F7', 'Top-step ribbon to the front bearer', 'Same as F5: four 100×4 316 nails through the inner ply into the bearer face at each pile, then nail the outer ply on. The front of this step sits on the bottom step, packed so the rises match.'),
    ('F8', 'Face board and the two risers', 'A decking board on the boundary joist, and one on each riser. The top board laps over the face board.'),
]

def money(n):
    return f'${n:,.2f}'

md = f'''# Deck and step build guide

{DATE} · How I am going to build the 6.9 m deck and the two steps in front of it. One plan, three sheets, a bill of materials and the build order. Written for me, doing the work. It is not an engineer's design. Consent is not required: Building Act Schedule 1, exemption 24, because a fall is about 500 mm. The sheets are still drawn to AS/NZS 1100.501 and the Auckland Council AC1011 document list. They are not lodged.

## What we are building

| Part | What |
|---|---|
| Main deck | 6900×2600 mm, boards level with the old deck, about 500 mm. Two double 190×45 H3.2 bearers on 8 timber piles at Y300 and Y2510. The pair is 90 mm wide. Joists 140×45 across them, span 2.21 m. NZS 3604 Table 7.1(b), wet, allows 2.35 m at 450 centres. |
| Main joists | 18 members. Flush at the end, then 437 mm centres, one doubled joist centred at 3956 for the board butts. The last two spaces are 368 mm. Rims at Y0 and Y2555. No blocking. |
| Rebuilt strip | 900×1970 mm, from the house wall to the existing bearer, then 300 mm on to the first new bearer. No piles. Three 140×45 joists of 2270, each 45 mm beside a deck joist so the lap can be nailed. The long span is 1970 mm. Table 7.1(b) allows 2350 mm. The main deck is not carried by the house. |
| Steps | Two steps, three rises, 6600 long from the eastern end, 560 mm out. One H4 frame: double ribbon, 12 joists, double front beam. The upper tread is packed on those joists. The western 300 mm of the deck has no step. |
| Boards | 88×32 merch griptread, along X. 28 rows on the deck, 21 on the rebuilt strip, three on each step. A board on the face of the boundary joist, and one on each riser. |
| Finish | Natural, no handrail. Three rises is the limit. One more rise and it would need a rail. Lawn and path stay as they are. |

Set-out, X from the eastern end. Piles: 300, 2400, 4500, 6600 on Y300 and Y2510. Eight holes. The bearer overhangs 300 mm past each end pile. The bays are 2100, 2100 and 2100 mm. The bearers are two 190×45 plies, 90 mm wide, nailed as clause 2.4.4.7, and the pair sits on the 125 pile. Table 6.4(b) does not list a 190×45. It lists a 190×70 spanning 2.7 m at a loaded dimension of 1.65 m, wet, 2 kPa, continuous over two spans. The double 190×45 is the size chosen on 15 November 2026. The two plies do not butt on the same pile. One ply is 4.50 m then 2.40 m and stops at 4500. The other is 2.40 m then 4.50 m and stops at 2400, so one board runs through at each cut. The same standard caps a bearer overhang at 200 mm when the bearers are more than 2 m apart, and these are 2.21 m apart. The 300 mm is the set-out from the builder. Mark the holes and move one if it lands on the path or within 500 mm of a pipe. The western piles are on the drain side. The two step piles are at X300 and X6300, Y3115. The holes are 200×200×200, dug with the steps. 2 bags, later. The rebuilt strip has no piles. The steps stop 300 mm short of the west end.

Heights. The path is where you walk and the grass is lower, so the steps are taped off the path. Deck boards +500 if that is what the old deck measures, joist top +468, bearer top +328, pile top +138. Bottom step board about +167, framing top +135. Top step board about +333, framing top +301. If the tape from the path to the deck boards is not 500, divide whatever it is by three.

## The sheets

[Sheet 1 · Foundation and framing](docs/drawings/sheet.svg) · [Sheet 2 · Section and details](docs/drawings/sheet2.svg) · [Sheet 3 · Site, levels and schedules](docs/drawings/sheet3.svg). A2, to AS/NZS 1100.501 and the Auckland Council AC1011 list. Consent is not required. These sheets are not lodged.

## Foundations

8 timber piles under the deck: 400×400 holes, 600 deep. No holes for the rebuilt strip. No 900 mm anchors and no brackets. The step has two holes, 200×200×200, dug later. 2 bags. Not in the 59. No spare hole on the pipe side of the path.

The eight holes are 400×400×600. Fill to 100 mm below the ground. The pile sits on 100 mm of concrete, so the pour is about {cv["main_pour_m3"]:.2f} m³. That is 59 bags of Multicrete, or 12 bags of cement and 1 m³ of builders mix. Not a truck. The step is two holes, 200×200×200, about {cv["step_holes_m3"]:.3f} m³. That is 2 bags of Multicrete, later. The deck order stays 59 bags.

The path stays. The deck is built over it. A 190 bearer with its top at +328 has its underside at +138, which is 12 mm under the 150 mm NZS 3604 wants for H3.2 above a surface. The grass is lower, so the piles there still clear 150 mm. No hole through the concrete. Do not open a bay past 2.7 m. The longest bay is 2.1 m.

The waste and the stormwater run together on the right of the path, the west side. The blue pipe is 400 mm past the concrete. The sewage is 130 mm past the blue one: the plan has one pipe 740 mm off the deck and the other 870 mm off the deck. Beside the deck they are about 440 to 470 mm deep, and only 240 to 270 mm deep beside the pad. The hole is 600 deep, so it goes below them. No hole edge within 500 mm of either pipe, and no hole between them. Stormwater goes out through the gate. The left of the path, the meter-box side, is clear. Orange is power, white is fibre, water is its own pipe. Dig with a spade.

### The two steps

A single 250 mm rise is too big. About 190 is the limit and 200 is a push. Two steps make three rises of about 167, and 2×167+280 comes out at 613, inside 550 to 700. No handrail at three rises.

Build the deck first. Then the bottom step, then the top step on it, set back 280 mm. Tape the rises off the path until they match. Do not cut a stringer.

The step is one H4 frame, not two. Double ribbon on the front piles, 12 joists of 500 mm, double front beam on the two small piles. The upper tread is packed on the inner half of those joists. That is 36 m. The old 72 m was a second doubled frame. The beam stays full depth. Two holes, 200×200×200, at the ends. 2 bags of Multicrete, later. The deck order stays 59 bags. Chase the path where the beam meets it.

## Shopping list

Prepared for Max Hogervorst, 18B Formby Avenue, Point Chevalier. {DATE}. The 190 and the 140 are NZ Timber quote 00067524, shown including GST. The four pile lengths are at that quote's rate. The H4 is Auckland Aggregates.

[Download the CSV](docs/shopping-list.csv).

'''
parts_sum = {}
for cat, item, qty, unit, price, store, use, comment, kind, url in priced:
    if kind != 'alt':
        parts_sum[cat] = round(parts_sum.get(cat, 0) + use, 2)
last = None
for cat, item, qty, unit, price, store, use, comment, kind, url in priced:
    if cat != last:
        if last:
            md += f'\n**{last} ${parts_sum[last]:,.0f}.**\n\n'
        md += f'### {cat}\n\n| Description | Qty | Unit | Price | Store |\n|---|---|---|---|---|\n'
        last = cat
    if not url and kind == 'alt':
        cell = 'Ask the yard'
    else:
        cell = f'[{money(price)}]({url})' if url else money(price)
    note = ' · other option' if kind == 'alt' else (' · later, not in the total' if kind == 'later' else '')
    md += f'| {item}{note} | {qty} | {unit} | {cell} | {store} |\n'
md += f'''
**{last} ${parts_sum[last]:,.0f}.**

**${total:,.0f} including GST.** The concrete in that number is the 59 bags. The step is 2 bags, later, and is not in it. The cement and the builders mix are the other way to make the same eight holes. Do not add them as well.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Main and rebuilt: {d["main_stock_lm"]} m in the cut list, {d["main_installed_lm"]} m used. 3519 and 3381 are the two rims, joint on the joist at 3518. 2510 is the 18 joists. 2270 is the three rebuilt joists, 45 mm beside the deck joists and lapped to the first new bearer. 900 is the bearer on the existing one, and the house ledger. Twelve of the sticks are 6.0 m. The eighteenth joist is the 3.0 m stick. The main bearers are not in this list. They are six 4.8 m lengths of 190×45. On each bearer one ply is 4.50 m then 2.40 m, joint on the pile at 4500. The other ply is 2.40 m then 4.50 m, joint on the pile at 2400. Four sticks are cut to 4.50 m. The other two sticks are each cut into two 2.40 m pieces.

| 150×50 H4 stock | Cuts, mm |
|---|---|
'''
for a in d['H4_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Steps: six 6.0 m lengths. Four are cut 4500 + 500 + 500 + 500. The 4500 runs to the pile at 4500, and the three 500s are joists. The other two lengths are cut 2100 + 2100, which finish the four plies, and the remainder is the twelve packers of 240.

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
- **The ground.** Firm clay at about 100 kPa under the topsoil. That is the usual Auckland assumption, not a test. A step pile is at about {sc["step_pile_bearing_kPa"]:.0f} kPa on a 200×200. If a hole is soft or wet at 600, that hole gets deeper or wider and it is no longer a spade job.
- **The steps.** One H4 frame. Double ribbon, 12 joists, double front beam. The upper tread is packed on the same joists. The two step holes are 200×200×200, dug after the deck. 2 bags, later. The deck order stays 59 bags. The beam is not ripped.
- **The services reply.** It said no gas and no power within 10 m. The power is there. Drain depths are approximate. Paint, spade, and move a hole rather than dig through a pipe.
- **Fixings.** Formby Avenue is about 1.1 km from the harbour, past the 500 m sea-spray line, so this is zone C. Decking screws are 304. Nails into the piles are 316, because those connections are within 600 mm of the ground. Bearer and joist nails stay hot-dip galvanised. The bolts stay 316. The decking is CCA. Do not swap in ACQ timber and keep these screws.
- **The path.** It stays. The piles are on a regular grid, 300 mm in from each end, then 2.1 m, 2.1 m and 2.1 m. Paint them and move a hole if it lands on the concrete or within 500 mm of a pipe. The western pair is on the drain side. Both bearers are doubled 190×45, 90 mm wide, on the 125 piles. Table 6.4(b) does not list a 190×45. The listed 190×70 spans 2.7 m, and the longest bay is 2.1 m. The double 190×45 is the size chosen on 15 November 2026. The steps are taped off the path, not off the lawn.
- **Prices.** The 190×45 and the 140×45 are NZ Timber quote 00067524, shown including GST. The piles are four lengths at that quote's rate. The H4 is Auckland Aggregates, $8.25 a metre plus GST. The concrete in the total is 59 bags of Multicrete. The step is 2 bags, later, and is not in the total. Cement plus builders mix is the other option and is not added.
- **The rebuilt strip.** No holes. The joists run from the house ledger to the first new bearer, 45 mm beside the deck joists, and the lap is nailed. The long span is 1970 mm and Table 7.1(b) allows 2350 mm. Bolt the ledger into the framing and flash it. Do not fix it to the weatherboards. The main deck is on its own eight piles.

## Sources

Northpine wet-service joist table, which reproduces NZS 3604 Table 7.1(b): 140×45 SG8 at 450 centres spans 2.35 m. Bearer spans are NZS 3604:2011 Table 6.4(b), 2 kPa, wet in service: a 190×70 continuous over two or more spans spans 2.7 m at a loaded dimension of 1.65 m, and a 140×90 spans 3.0 m at 1.30 m. The table does not list a 190×45. The bearers on this job are two 190×45 plies. NZS 3604 wants H3.2 150 mm clear of a surface. The 190 bearer over the path is at 138 mm, and the bottom step is closer than that. The stair proportion used here is a rise under 190 and 2R+G between 550 and 700. [Northpine tables](https://www.northpine.co.nz/span-tables) · [BRANZ Bulletin 611](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf).

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
sheets = '''<section id="bearer" aria-label="One line of piles">
<h2>One line of piles</h2>
<p class="note">Four piles, one bearer. East on the left. The other line of piles is the same bearer again. The gap is drawn in. The boards butt tight.</p>
<div class="one-bearer">
<div class="ob-track">
<div class="ob-ply"><b style="left:0;width:64%">4.50 m</b><b style="left:66%;width:34%">2.40 m</b></div>
<div class="ob-ply"><b style="left:0;width:33.5%">2.40 m</b><b style="left:35.5%;width:64.5%">4.50 m</b></div>
<div class="ob-posts"><span style="left:4.3%">300</span><span style="left:34.8%">2400</span><span style="left:65.2%">4500</span><span style="left:95.7%">6600</span></div>
</div>
<p class="ob-bays">300 mm past the end pile, then 2100, 2100 and 2100, then 300 mm.</p>
</div>
<p>Top board stops on 4500. Bottom board stops on 2400. Where one is cut, the other runs through.</p>
</section>
<section id="sheets" aria-label="Drawing set">
<figure class="sheet"><div id="view-sheet"></div><figcaption>01 · Foundation, framing and long section</figcaption></figure>
<figure class="sheet"><div id="view-sheet2"></div><figcaption>02 · Section, pile and steps</figcaption></figure>
<figure class="sheet"><div id="view-sheet3"></div><figcaption>03 · Site, levels and schedules</figcaption></figure>
<p class="note"><a href="drawings/sheet.svg">Sheet 1</a> · <a href="drawings/sheet2.svg">Sheet 2</a> · <a href="drawings/sheet3.svg">Sheet 3</a></p>
</section>'''
body = sheets + schedules
html = '''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="ISL38807. Proposed deck for 18B Formby Avenue. Three sheets, not lodged."><title>ISL38807 · 18B Formby Avenue</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">ISL38807 <span>18B FORMBY AVENUE · NOT LODGED</span></a><nav aria-label="Sections"><a href="#bearer">Bearer</a><a href="#sheets">Sheets</a><a href="#shopping-list">Schedule</a></nav><button id="print">Print</button></header><main id="main">''' + body + '''</main><footer><span>AS/NZS 1100.501 · Exemption 24 · Do not scale</span></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
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

L = 6900
STEP = 6600

s1 = []
_title(s1, 1, '1:25', '01  FOUNDATION, FRAMING AND LONG SECTION')
# Rebuilt strip at the house, then the deck, then the two steps.
s1.append(_box(PX(0), PY(-1970), 900 * K, 1970 * K))
s1.append(_box(PX(0), PY(0), L * K, 2600 * K))
s1.append(_box(PX(0), PY(2600), STEP * K, 560 * K))
s1.append(_ln(PX(0), PY(2880), PX(STEP), PY(2880), INK, 0.45))
for x in d['main_joist_centres_mm']:
    heavy = x in (3933, 3978)
    s1.append(_ln(PX(x), PY(45), PX(x), PY(2555), INK, 1.05 if heavy else 0.4))
for x in d['rebuilt_joist_X_mm']:
    s1.append(_ln(PX(x), PY(-1970), PX(x), PY(300), RED, 0.7))
for y in (300, 2510):
    s1.append(_ln(PX(0), PY(y - 45), PX(4485), PY(y - 45), INK, 0.9))
    s1.append(_ln(PX(4515), PY(y - 45), PX(L), PY(y - 45), INK, 0.9))
    s1.append(_ln(PX(0), PY(y), PX(L), PY(y), INK, 0.35))
    s1.append(_ln(PX(0), PY(y + 45), PX(2385), PY(y + 45), INK, 0.9))
    s1.append(_ln(PX(2415), PY(y + 45), PX(L), PY(y + 45), INK, 0.9))
s1.append(_ln(PX(0), PY(2555), PX(L), PY(2555), INK, 0.7))
s1.append(_ln(PX(0), PY(3070), PX(STEP), PY(3070), INK, 0.7))
s1.append(_ln(PX(0), PY(3160), PX(STEP), PY(3160), INK, 0.7))
for y in (300, 2510):
    for x in pile_x:
        s1.append(_box(PX(x - 200), PY(y - 200), 400 * K, 400 * K, '#8a8a8a', 0.4, '2 1.4'))
        s1.append(_box(PX(x - 62.5), PY(y - 62.5), 125 * K, 125 * K, INK, 0.8))
for x in t['small_pile_X_mm']:
    s1.append(_box(PX(x - 100), PY(3115 - 100), 200 * K, 200 * K, '#8a8a8a', 0.4, '2 1.4'))
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
s1.append(_hdim(PX(0), PX(L), chain + 16, '6900'))
s1.append(_tx(PX(0) - 2, chain - 10, '300', 7, 'end', RED))
s1.append(_tx(PX(L) + 2, chain - 10, '300', 7, 'start', RED))
cx = PX(L / 2)
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
s1.append(_note(360, 46, ['DOUBLE BEARER 190×45', 'JOINTS STAGGERED', 'ONE PLY AT 2400', 'OTHER PLY AT 4500'], (PX(2400), PY(300))))
s1.append(_note(500, 46, ['NOTE', 'DECKING IS FIXED WITH', 'DECKING SCREWS'], (PX(4200), PY(80))))
s1.append(_note(188, 108, ['140×45 SG8 H3.2 JOIST', 'AT 437 CENTRES', 'DOUBLED AT 3956'], (PX(1770.5), PY(400))))
s1.append(_note(400, 108, ['125×125 H5 PILE', 'HOLE 400×400×600', 'NO ANCHOR BRACKET'], (PX(4500), PY(300))))
s1.append(_note(560, 118, ['TWO STEPS', 'GOING 280', 'SEE SHEET 2'], (PX(5000), PY(2880))))
s1.append(_tx(PX(450), 34, 'STRIP TO HOUSE  NO PILES', 7.5, 'middle', GREEN, '600'))

# Long elevation, aligned with the plan. True 1:25, so it is the thin strip.
def EZ(z):
    return 648 - z * K

s1.append(_ln(PX(0), EZ(0), PX(L), EZ(0), INK, 0.9))
for x in pile_x:
    s1.append(_box(PX(x - 62.5), EZ(138), 125 * K, (138 + 40) * K))
s1.append(_box(PX(0), EZ(328), L * K, 190 * K))
s1.append(_tx(PX(L / 2), EZ(110), '190×45 DOUBLE', 7, 'middle', RED))
s1.append(_box(PX(0), EZ(468), L * K, 140 * K))
s1.append(_box(PX(0), EZ(500), L * K, 32 * K))
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
    'BEARERS: 190×45 SG8 H3.2,',
    'DOUBLED, 90 WIDE.',
    'JOISTS AND REBUILT STRIP:',
    '140×45 SG8 H3.2.',
    'STEPS: 150×50 SG8 H4.',
    'PILES: 125×125 H5.',
    'BOARDS: 88×32 H3.2.',
    '6. 8 DECK PILES. HOLE',
    '400×400, 600 DEEP.',
    'NO REBUILT PILES.',
    'TWO STEP PILES, LATER.',
    'HOLE 200×200, 200 DEEP.',
    '2 BAGS. NOT IN THE 59.',
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
    s2.append(_box(EY(y - 45), EZ2(328), 90 * K, 190 * K))
    s2.append(_ln(EY(y), EZ2(328), EY(y), EZ2(138), INK, 0.4))
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
s2.append(_box(SY(2510 - 45), SZ(328), 90 * k10, 190 * k10))
s2.append(_ln(SY(2510), SZ(328), SY(2510), SZ(138), INK, 0.4))
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
s3.append(_box(SX(0), SY3(0), 6900 * ks, 2600 * ks))
s3.append(_tx(SX(3450), SY3(1200), 'DECK 6900×2600', 8, 'middle', INK, '700'))
s3.append(_tx(SX(3450), SY3(1200) + 12, 'FFL +500', 7.5, 'middle', GREEN, '600'))
s3.append(_box(SX(0), SY3(2600), 6600 * ks, 560 * ks))
s3.append(_tx(SX(7000), SY3(2880), 'STEPS 6600', 7, 'start', INK, '600'))
s3.append(_hdim(SX(0), SX(6900), SY3(3600), '6900'))
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
    ('P2', '2', '125×125 H5', '200×200×200', '2 BAGS, LATER'),
]
for i, row in enumerate(rows_p):
    y = 272 + i * 16
    xs = [566, 660, 720, 900, 1040]
    for val, x in zip(row, xs):
        s3.append(_tx(x, y, val, 7.5, 'start', INK, '500'))
s3.append(_tx(560, 330, 'FRAMING SCHEDULE — FINISHED SIZES', 9, 'start', GREEN, '700'))
s3.append(_ln(560, 338, 1120, 338, INK, 0.6))
framing = [
    'BEARERS  190×45 SG8 H3.2 DOUBLE, 90 WIDE. JOINTS STAGGERED, 2400 AND 4500',
    'JOISTS  140×45 SG8 H3.2, 18 OF, 437 CENTRES, DOUBLED AT 3956',
    'REBUILT  3 JOISTS, 45 mm BESIDE THE DECK JOISTS, LAP NAILED',
    'STEPS  150×50 SG8 H4. ONE FRAME, DOUBLE RIBBON, 12 JOISTS, DOUBLE FRONT BEAM',
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
s3.append(_tx(560, 570, 'WEST PILES AT 6600. STEPS STOP AT 6600.', 8, 'start', GREEN, '700'))
s3.append(_tx(560, 586, 'CONSENT NOT REQUIRED. NOT LODGED. NOT ENGINEER CHECKED.', 7.2, 'start', GREEN, '500'))
s3.append(_tx(560, 610, 'BRACING IS A DEPARTURE FROM NZS 3604 cl 7.4.2.2.', 7.2, 'start', GREEN, '500'))
s3.append(_tx(560, 626, 'SEE NOTE 7 ON SHEET 2.', 7.2, 'start', GREEN, '500'))
(root / 'site/drawings' / 'sheet3.svg').write_text(_sheet(s3, 'Sheet 3. Site of the works, levels and schedules. Ref ISL38807. Consent exempt, not lodged. Boundaries not surveyed.'))

# Top-down of the individual boards. East on the left, the house at the top.
# The bearer butt is on the pile at 4500. Each rim is cut on the joist at 3518
# so both halves come out of a 6.0 m board.
k = 0.132
ox, oy, y0 = 78, 86, -2140
GAP = 90

def SX(mm):
    return ox + mm * k

def SY(mm):
    return oy + (mm - y0) * k

def board(x, y, w, h, fill):
    return f'<rect x="{SX(x):.2f}" y="{SY(y):.2f}" width="{w * k:.2f}" height="{h * k:.2f}" fill="{fill}" stroke="{INK}" stroke-width="0.8"/>'

BEAR, JOIST_F, RIM_F, REB = '#c4a15a', '#f3e6c4', '#8d6b3e', '#7d9a78'
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 860" role="img" aria-label="Top-down piece plan. Each bar is one board.">',
    '<title>Piece plan. Each bar is one board, seen from above.</title>',
    '<style>text{font-family:Arial,Helvetica,sans-serif}</style>',
    '<rect width="1180" height="860" fill="#faf9f5"/>',
    _tx(24, 36, 'EACH BAR IS ONE BOARD', 16, 'start', INK, '700'),
    _tx(24, 56, 'EAST ON THE LEFT  ·  HOUSE AT THE TOP  ·  LOOKING DOWN', 11, 'start', GREEN, '600'),
]
# Piles first, under the timber.
for yb in (300, 2510):
    for x in pile_x:
        parts.append(f'<rect x="{SX(x - 62.5):.2f}" y="{SY(yb - 62.5):.2f}" width="{125 * k:.2f}" height="{125 * k:.2f}" fill="#d5ddd4" stroke="{INK}" stroke-width="0.7"/>')
# Rims, each one two pieces, joint on the joist at 3518.
rim_joint = 3518.5
for y in (0, 2555):
    parts.append(board(0, y, rim_joint - GAP, 45, RIM_F))
    parts.append(board(rim_joint + GAP, y, 6900 - rim_joint - GAP, 45, RIM_F))
# Bearers. House-side ply butts at 4500. Front-side ply butts at 2400.
for yb in (300, 2510):
    parts.append(board(0, yb - 45, 4500 - GAP, 45, BEAR))
    parts.append(board(4500 + GAP, yb - 45, 6900 - 4500 - GAP, 45, BEAR))
    parts.append(board(0, yb, 2400 - GAP, 45, BEAR))
    parts.append(board(2400 + GAP, yb, 6900 - 2400 - GAP, 45, BEAR))
# Deck joists sit on the bearers, so they are drawn over them.
for x in d['main_joist_centres_mm']:
    parts.append(board(x - 22.5, 45, 45, 2510, JOIST_F))
# Rebuilt strip. Ledger at the house, three joists, and the piece on the existing bearer.
parts.append(board(0, -1970, 900, 45, REB))
for x in d['rebuilt_joist_X_mm']:
    parts.append(board(x - 22.5, -1970, 45, 2270, REB))
parts.append(board(0, -45, 900, 45, REB))
# Labels
parts.append(_tx(SX(1200), SY(230), '2.40 m', 12, 'middle', INK, '700'))
parts.append(_tx(SX(4650), SY(230), '4.50 m', 12, 'middle', INK, '700'))
parts.append(_tx(SX(2250), SY(400), '4.50 m', 12, 'middle', INK, '700'))
parts.append(_tx(SX(5700), SY(400), '2.40 m', 12, 'middle', INK, '700'))
parts.append(_tx(SX(2400), SY(560), 'JOINT', 11, 'middle', RED, '700'))
parts.append(_tx(SX(4500), SY(560), 'JOINT', 11, 'middle', RED, '700'))
parts.append(_tx(SX(rim_joint), SY(-28), 'RIM JOINT', 11, 'middle', RED, '700'))
parts.append(_tx(24, SY(-2080), 'HOUSE', 13, 'start', GREEN, '700'))
parts.append(_tx(SX(20), SY(2680), 'FRONT', 13, 'start', GREEN, '700'))
parts.append(_tx(16, SY(1300), 'EAST', 13, 'start', GREEN, '700'))
parts.append(_tx(SX(980), SY(-1900), 'LEDGER 900', 11, 'start', INK, '600'))
parts.append(_tx(SX(980), SY(-1100), '3 REBUILT JOISTS, 2.27 m', 12, 'start', INK, '600'))
parts.append(_tx(SX(3450), SY(1400), '18 JOISTS, 2.51 m', 13, 'middle', INK, '700'))
parts.append(_tx(SX(3450), SY(1560), 'FULL WIDTH, BETWEEN THE TWO RIMS', 11, 'middle', INK, '600'))
parts.append(_vdim(SX(7200), SY(0), SY(2600), '2600'))
parts.append(_tx(SX(7350), SY(1300), 'JOIST 2510', 11, 'start', RED, '700'))
parts.append(_tx(SX(7350), SY(1480), 'RIM 45 EACH EDGE', 11, 'start', RED, '600'))
parts.append(_tx(SX(3956), SY(1700), 'DOUBLE', 11, 'middle', RED, '700'))
# Zoom, so the two side-by-side plies and the butt are readable.
zx, zy = 860, 90
parts.append(_tx(zx, zy, 'AT A JOINT', 13, 'start', INK, '700'))
parts.append(f'<rect x="{zx}" y="{zy + 16}" width="270" height="168" fill="white" stroke="{INK}" stroke-width="0.8"/>')
parts.append(f'<rect x="{zx + 106}" y="{zy + 36}" width="58" height="70" fill="#d5ddd4" stroke="{INK}" stroke-width="0.8"/>')
parts.append(f'<rect x="{zx + 16}" y="{zy + 46}" width="238" height="20" fill="{BEAR}" stroke="{INK}" stroke-width="0.8"/>')
parts.append(f'<rect x="{zx + 16}" y="{zy + 70}" width="108" height="20" fill="{BEAR}" stroke="{INK}" stroke-width="0.8"/>')
parts.append(f'<rect x="{zx + 140}" y="{zy + 70}" width="114" height="20" fill="{BEAR}" stroke="{INK}" stroke-width="0.8"/>')
parts.append(_tx(zx + 135, zy + 112, 'ONE BOARD RUNS THROUGH', 10, 'middle', INK, '600'))
parts.append(_tx(zx + 135, zy + 128, 'THE OTHER STOPS ON THE PILE', 10, 'middle', RED, '700'))
parts.append(_tx(zx + 135, zy + 146, 'THE OTHER JOINT IS SWAPPED', 10, 'middle', INK, '500'))
parts.append(_tx(zx + 135, zy + 168, 'BOTH BEARERS ARE THE SAME', 10, 'middle', INK, '500'))
# Legend
lx, ly = 900, 748
parts.append(_tx(lx, ly, '190×45 BEARER', 12, 'start', INK, '600'))
parts.append(f'<rect x="{lx - 28}" y="{ly - 12}" width="18" height="12" fill="{BEAR}" stroke="{INK}" stroke-width="0.6"/>')
parts.append(_tx(lx, ly + 22, '140×45 JOIST', 12, 'start', INK, '600'))
parts.append(f'<rect x="{lx - 28}" y="{ly + 10}" width="18" height="12" fill="{JOIST_F}" stroke="{INK}" stroke-width="0.6"/>')
parts.append(_tx(lx, ly + 44, '140×45 RIM', 12, 'start', INK, '600'))
parts.append(f'<rect x="{lx - 28}" y="{ly + 32}" width="18" height="12" fill="{RIM_F}" stroke="{INK}" stroke-width="0.6"/>')
parts.append(_tx(lx, ly + 66, 'REBUILT STRIP', 12, 'start', INK, '600'))
parts.append(f'<rect x="{lx - 28}" y="{ly + 54}" width="18" height="12" fill="{REB}" stroke="{INK}" stroke-width="0.6"/>')
parts.append(_tx(24, 830, 'The gap is drawn wide so the cut shows. The boards actually butt tight. House-side ply joints at 4500. Front-side ply joints at 2400. Joists are 2510 because each rim takes 45. The deck is 6900 by 2600.', 11, 'start', INK, '500'))
parts.append('</svg>')
(root / 'site/drawings' / 'pieces.svg').write_text(''.join(parts))
print('sheets', len(s1), len(s2), len(s3), 'pieces')


