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
# category, item, qty, unit, bunnings unit text, bunnings line or None, mitre line or None, comment, kind, url
rows = [
    ('Timber', '140×45 SG8 H3.2 framing, wet. Main deck and rebuilt strip', '100.8', 'm', 6 * 85.10 + 8 * 70.91 + 2 * 56.73, None, '6×7.2 m, 8×6.0 m, 2×4.8 m. 7.2 m is not listed, priced at the 6.0 m rate of $11.82/m', 'estimate', 'https://www.bunnings.co.nz/140-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-6m_p0616262'),
    ('Timber', '140×45 SG8 H4 framing for the two steps', f'{d["H4_stock_lm"]:.0f}', 'm', d['H4_stock_lm'] * 17.11, None, '8×7.2 m and 3×4.8 m. No 140×45 H4 price online, so this is 150×50 H4 at $17.11/m. Splice over a pile if 7.2 m H4 is not in the rack', 'estimate', 'https://www.bunnings.co.nz/150-x-50mm-sg8-h4-wet-sawn-treated-timber-per-linear-metre_p0276210'),
    ('Piles', '125×125 H5 pile, 1.2 m', '16', 'ea', 16 * 32.42, None, 'The 16 deck and rebuilt piles. 600 in the ground plus about 190 above the path, and the grass is lower, so 750 mm is too short. $32.42. Cut to the string', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-1-2m-square-h5-anchor-pile_p0276402'),
    ('Piles', '125×125 H5 pile, 750 mm', '8', 'ea', 8 * 21.04, None, 'Six under the bottom step and two spare for the path. $21.04. Most of the length gets cut off', 'posted', 'https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
    ('Decking', '88×32 H3.2 merch griptread', f'{deck["stock_lm"]}', 'm', deck['stock_lm'] * 4.55, None, f'{deck["stock_4200"]}×4.2 m and {deck["stock_3000"]}×3.0 m at $4.55/m. Named lengths, so the butts land on the doubled joist', 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
    ('Fasteners', 'Decking screws 10g×65 316 stainless', '1500', 'ea', 3 * 116.00, None, f'3×500 at $116. {deck["base_screws"]} positions', 'posted', 'https://www.bunnings.co.nz/decking-screw-65-x-10g-316-stainless-steel-500-pack_p0379643'),
    ('Fasteners', 'Framing nails 90×4 316 stainless jolt head', '6', 'kg', None, 3 * 129.00, '3×2 kg at $129, Mitre 10. Bearer plies and the step beams', 'posted', 'https://www.mitre10.co.nz/shop/ecko-jolt-head-nails-90-x-4-0mm-2kg-316-stainless-steel/p/307864'),
    ('Fasteners', 'Framing nails 100×4 316 stainless jolt head', '4', 'kg', 8 * 35.59, None, '8×500 g at $35.59. Joists, rims, skew nails', 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-500g-316-stainless-steel-jolt-head-nail_p0383199'),
    ('Fasteners', 'Batten screws 14g×100 316 stainless', '100', 'ea', 77.05, None, 'One box, $77.05. Step ribbons, and the rebuilt joists', 'posted', 'https://www.bunnings.co.nz/bremick-xtp-14g-x-100mm-t40-stainless-steel-316-black-bugle-batten-100-pack_p0575899'),
    ('Fasteners', 'M12×120 316 coach bolt, nut, two 50 mm washers', '2', 'ea', 2 * (4.90 + 1.25 + 2 * 3.54), None, 'The two rim ties. $4.90 + $1.25 + 2×$3.54 each', 'posted', 'https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
    ('Concrete', 'Ready-mix, small load', '2.0', 'm³', 650, None, 'About $650, not a quote. On site the figure was about $600 for the 1.1 m³ in the twelve holes. This load covers the rebuilt holes and the step as well. Do not add the cement as well', 'estimate', ''),
    ('Concrete', 'Portland cement, 20 kg. Only if mixing on site', '36', 'ea', 36 * 11.59, None, 'Cemix Ecostrong $11.59, used as GP cement. Four shovels of builders mix to one shovel of cement, and a bit more cement if the mix looks lean', 'alt', 'https://www.bunnings.co.nz/cemix-20kg-low-carbon-cement_p0581734'),
    ('Concrete', 'Builders mix, dumped in front of the garage', '2.5', 'm³', None, None, 'Only with the cement. Phone a yard. Not priced', 'alt', ''),
    ('DPC', 'DPC Supercourse 500, 150 mm×30 m', '1', 'ea', 27.42, None, 'On every pile top. $27.42', 'posted', 'https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
    ('DPC', 'Metalex Green, 1 L', '1', 'ea', 66.00, None, 'On every saw cut. $66', 'posted', 'https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
]
priced = []
for cat, item, qty, unit, line, mitre, comment, kind, url in rows:
    use = mitre if line is None else line
    priced.append((cat, item, qty, unit, None if line is None else round(float(line), 2), None if mitre is None else round(float(mitre), 2), round(float(use), 2) if use and kind != 'alt' else 0.0, comment, kind, url))
posted = round(sum(r[6] for r in priced if r[8] == 'posted'), 2)
est = round(sum(r[6] for r in priced if r[8] == 'estimate'), 2)
total = round(posted + est, 2)
steps = [
    'Before you buy. Match the old deck: the new boards sit at that same 500 mm, not 500 mm above the low grass. Measure from the old boards down to the concrete path. Joists need about 330 mm of air over the path and the bearers about 190 mm. The steps are measured off the path as well, because that is where you walk. Tape that height and divide by three. If it is 500, each rise is 167. The lawn is lower and is not the step. Check the sill and the cladding. Stainless or galvanised still depends on the sea-spray zone. A services reply that says no power within 10 m is not to be trusted: there is power. Mark the stormwater and the waste before any digging.',
    'Set out. String the 6600×2600 outline and the 900×1970 rebuilt strip. The steps stick out 560 mm past the front, two goings of 280. Leave the path. End joist flush, then 437 mm centres, doubled joist centred at 3956. Mark the 16 pile holes, then the six step holes on the same X, 560 mm out. Shift any mark that lands on the path or within 500 mm of a pipe. Paint the marks.',
    'Dig, with a spade. Every deck hole is 400×400 and 600 deep, down to firm ground, not topsoil. No 900 mm anchor holes. At 600 a shovel is enough. An auger only earns its keep past 600, and these holes do not go there. About ten minutes a hole. The west end, the gully trap, the rebuilt piles and every hole beside the path are the careful ones. Stormwater goes out through the gate, and the waste is beside it. Power is the orange, fibre is the white, water is its own pipe. If the spade finds pipe, plastic or bedding sand, stop and move the hole. No hole edge within 500 mm of a pipe, and no bearer bay past 1.4 m.',
    f'Concrete. One hole at a time, unless the weather is settled and every hole is open. The twelve main holes are {cv["main_12_holes_m3"]:.2f} m³, the 1.1 m³ counted on site, pile left in the hole. Rebuilt holes and the step holes bring it to about {cv["main_net_m3"]:.2f} m³. Order {cv["readymix_order_m3"]:.1f} m³ if a truck is coming, and barrow it. Otherwise builders mix dumped in front of the garage, plus cement: four shovels of mix to one of cement, a bit more cement if it looks lean, mixer hired. Fill to about 100 mm below the ground. Do not use the no-mix post-hole bags. Nothing in the hole has to be level.',
    'Cut the piles. String off the path, not the lawn. On the path the tops finish about 310 mm below the old boards, and at least 150 mm clear of the path. The grass piles stand taller. Cut square, preservative on the cut, DPC on the top.',
    'Bearers. Nail the two 6.6 m double bearers and the two 0.9 m rebuilt bearers (F1). Seat them on the piles and skew-nail (F2). No anchor brackets. Take out the old rear bearer and do not reuse it.',
    'Joists and rims. 17 joists of 2510: flush at each end, 437 centres, the doubled joist at 3956. Screws into a bearer go in from the side of the joist, not down through the top. Three rebuilt joists of 1880, two blocks cut at 380, and the skewed 14g screws (F4). Rims at Y0 and Y2555. Two M12 bolts where the rebuilt strip meets the deck (F6). Get the deck frame up before the steps. The step height is in mid-air until the deck is there. Offcuts can be a temporary step.',
    'Step piles. With the deck frame up, dig the six small holes, 300×300 and 400 deep, on the same X as the front piles and 560 mm out from the face. Not 600. Stand a 750 mm pile, plumb it, and concrete it. Cut it so the front beam will finish with its top about 135 mm above the path.',
    'Bottom step. Screw a double H4 ribbon to the front piles, four 14g×100 screws each (F5). Joists out from it, cut about 500, on the same lines as the deck joists. Double front beam on the small piles. Top of this framing about 135 mm above the path, so the 32 mm board finishes at about 167. A 140 does not fit over the path. Rip the bottom of the ribbon and the beam where they would touch it, leave 15 mm of air, and do not go under 120 mm deep. If that rip is in a bay, put a spare pile each side of the path.',
    'Top step, on the bottom one. Set it back one going, 280 mm. Double ribbon screwed to the face of the front bearer (F7), short joists cut about 240, front beam packed off the bottom step so the framing top is about 301 mm above the path. The board then finishes at about 333. Tape the three rises off the path and make them equal. Do not cut a stringer. No handrail. Three rises is the limit. One more would need a rail.',
    'Boards. 28 rows on the deck, 21 on the rebuilt strip, three on each step, all along X. Butts on the doubled joist at 3956, so use the 4.2 m and 3.0 m lengths. A decking board on the face of the boundary joist, the top board over it, and a board on each riser. About 5 mm gaps on the deck and about 6 mm on the rebuilt strip. Two screws per board per joist. Preservative on every cut.',
]
fixings = [
    ('F1', 'Double bearers and the step beams', '90×4 stainless nails, two rows at 250 mm centres, staggered. Same on each double step beam and ribbon.'),
    ('F2', 'Pile to bearer, and the small step piles', 'Four 100×4 stainless skew nails. Same four nails from the front beam down into each small pile.'),
    ('F3', 'Joists, rims, blocks', 'Two 100×4 stainless per joist end, through the rim or into the ribbon.'),
    ('F4', 'Rebuilt joists', 'Four 100×4 skew nails and two 14g×100 screws, skewed in from the side of the joist. The point-load screen can put about 1.9 kN of uplift on one support. Ordinary carpentry, not a rated bracket.'),
    ('F5', 'Bottom-step ribbon to the front piles', 'Four 14g×100 screws into each pile, in from the side. A bolt through is fine if you would rather drill the pile. Ordinary screws, not a bracket.'),
    ('F6', 'Rebuilt strip to the main rim', 'Two M12×120 stainless coach bolts at X200 and X700, 50 mm square washers both sides.'),
    ('F7', 'Top-step ribbon to the front bearer', 'Four 14g×100 screws into the bearer face at each pile. The front of this step sits on the bottom step, packed so the rises match.'),
    ('F8', 'Face board and the two risers', 'A decking board on the boundary joist, and one on each riser. The top board laps over the face board.'),
]

def money(n):
    return 'POA' if not n else f'${n:,.2f}'

md = f'''# Deck and step build guide

{DATE} · How I am going to build the 6.6 m deck and the two steps in front of it. One plan, a set-out sheet, three drawings, a bill of materials and the build order. Written for me, doing the work. It is not an engineer's design. The ROBO preview ISL38807 is not this build. That sheet says preview only, and the quantities below are this deck, not that export.

## What we are building

| Part | What |
|---|---|
| Main deck | 6600×2600 mm, boards level with the old deck, about 500 mm. Two double 140×45 H3.2 bearers on 16 timber piles at Y300 and Y2510. Joists 140×45 across them, span 2.21 m. The wet-service table at 450 centres allows 2.35 m. |
| Main joists | 17 members. Flush at the end, then 437 mm centres, one doubled joist centred at 3956 for the board butts. Rims at Y0 and Y2555. No blocking. |
| Rebuilt strip | 900×1970 mm beside the house. Two 900 mm double bearers at Y−1925 and Y−800, three joists of 1880, two blocks cut at 380. Nothing runs through into the main deck. |
| Steps | Two steps, three rises, the full width of the deck, sticking out 560 mm. Going 280. Rise about 167 if the path-to-board tape is 500. Double 140×45 H4. Bottom step: a ribbon screwed to the front piles, joists out, a front beam on six small piles. Top step built on that and screwed to the bearer. Not a cut stringer. |
| Boards | 88×32 merch griptread, along X. 28 rows on the deck, 21 on the rebuilt strip, three on each step. A board on the face of the boundary joist, and one on each riser. |
| Finish | Natural, no handrail. Three rises is the limit. One more rise and it would need a rail. Lawn and path stay as they are. |

Set-out, X from the left edge. Piles: 62.5, 1357.5, 2652.5, 3947.5, 5242.5, 6537.5 on Y300 and Y2510. The six step piles are on those same X, at Y3115. Rebuilt piles: X175 and X725 on Y−1925 and Y−800.

Heights. The path is where you walk and the grass is lower, so the steps are taped off the path. Deck boards +500 if that is what the old deck measures, joist top +468, bearer top +328, pile top +187. Bottom step board about +167, framing top +135. Top step board about +333, framing top +301. If the tape from the path to the deck boards is not 500, divide whatever it is by three.

## The sheet

[Open the set-out sheet](docs/drawings/sheet.svg). Plan, long side and the two steps, with the sizes on this page. Same build as the notes below. Not the ROBO preview, and not for consent.

## Three drawings

[1 · Piles and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixings and the two steps](docs/drawings/fixings.svg)

## Foundations

16 timber piles, all the same: 400×400 holes, 600 deep. No 900 mm anchors and no brackets. 600 is deep enough that the deck is not sitting in the ground that swells. Four anchors would be more hole than this deck needs. The step has six smaller holes, 300×300 and 400 deep, plus two spare if the path is in the way.

Concrete volume leaves the pile in the hole. The twelve main holes are {cv["main_12_holes_m3"]:.2f} m³, the 1.1 m³ counted on site. With the four rebuilt holes and the step holes it is about {cv["main_net_m3"]:.2f} m³, so a truck order is {cv["readymix_order_m3"]:.1f} m³. The other way is builders mix dumped in front of the garage, plus cement, four shovels of mix to one of cement, and each hole concreted as it is dug so a shower does not fill twelve of them. Do not use the no-mix post-hole bags.

The path stays. The deck is built over it. Joists want about 330 mm of air over it and the bearers about 190 mm, so the piles clear 150 mm. No hole through the concrete. If a mark lands on it, slide that pile along the bearer onto soil and do not open a bay past 1.4 m. If the slide would be bigger than that, add a pile on the other side of the path.

The waste and the stormwater run together down the west side, about 700 to 900 mm off the deck, mostly 430 to 550 mm deep and only 240 to 270 mm deep beside the pad. Stormwater goes out through the gate. The waste is beside it. The services reply that put no power within 10 m is wrong. Orange is power, white is fibre, water is its own pipe. Tape what you can find, paint the holes, and dig them with a spade. No hole edge within 500 mm of a pipe. The careful ground is from the path outward, plus the west end, the gully trap and the rebuilt piles.

### The two steps

A single 250 mm rise is too big. About 190 is the limit and 200 is a push. Two steps make three rises of about 167, and 2×167+280 comes out at 613, inside 550 to 700. No handrail at three rises.

Build the deck first. Then the bottom step, then the top step on it, set back 280 mm. Tape the rises off the path until they match. Do not cut a stringer.

The bottom framing only has about 135 mm above the path, and a 140 is deeper than that, so over the path the ribbon and the front beam get ripped. Leave 15 mm of air and at least 120 mm of timber, and put a spare pile each side of the path so the thin piece is not spanning 1.3 m. Everywhere else the grass is lower and the full 140 stays. On the full 140 the beam screen is about {sc["step_beam_util_140"]*100:.0f}%. The ripped half-bay is about {sc["step_beam_util_120"]*100:.0f}%. The small pile sees about {sc["step_pile_bearing_kPa"]:.0f} kPa on a 300×300.

The underside of that bottom step is not 150 mm clear of the path. There is no way to have that and still walk off onto the path in even rises. It is H4 because it will stay damp. The deck piles themselves do clear 150 mm.

## Shopping list

Prepared for Max Hogervorst, 18B Formby Avenue, Point Chevalier. {DATE}. Laid out as a supplier comparison. The quantities are this build, not the ROBO bill. Measure first, then buy. Nothing has been bought. Prices include GST. Placemakers is a phone call. A blank cell means no price was found.

[Download the CSV](docs/shopping-list.csv).

'''
last = None
for cat, item, qty, unit, line, mitre, use, comment, kind, url in priced:
    if cat != last:
        if last:
            md += '\n'
        md += f'### {cat}\n\n| Description | Qty | Unit | Bunnings | Mitre 10 | Comments |\n|---|---|---|---|---|---|\n'
        last = cat
    b = money(line)
    m = money(mitre)
    if url and b != 'POA':
        b = f'[{b}]({url})'
    elif url and m != 'POA':
        m = f'[{m}]({url})'
    note = comment + (' Not in the total.' if kind == 'alt' else '')
    md += f'| {item} | {qty} | {unit} | {b} | {m} | {note} |\n'
md += f'''
**Posted ${posted:,.2f} + estimates ${est:,.2f} = about ${total:,.0f} including GST.** The total uses the truck. If the holes are mixed on site, take the truck out and add the cement. The builders mix is a yard quote and is not in the number either way. Do not add the truck and the cement together.

Pack sizes are already rounded up for the nails and the screws. Pile lengths are long on purpose. No allowance for a wasted bolt, or for timber used as a temporary brace. Delivery, the mixer and carting the spoil are extra. Galvanised fasteners, if the map says the site is outside the sea-spray zone, cut a lot of the fixing cost.

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
- **The steps.** The front beam, full 140 over a 1.30 m bay, is about {sc["step_beam_util_140"]*100:.0f}% of my bending screen under a factored point load. Ripped to 120 mm, with a pile each side of the path, that half-bay is about {sc["step_beam_util_120"]*100:.0f}%. The screws are ordinary screws. The bottom step does not have 150 mm clearance over the path. The rises are even. They are not a consented stair.
- **The services reply.** It said no gas and no power within 10 m. The power is there. Drain depths are approximate. Paint, spade, and move a hole rather than dig through a pipe.
- **Stainless until the map is checked.** 316 because I have not confirmed the sea-spray zone. Outside it, hot-dip galvanised is allowed and much cheaper.
- **The path.** It stays. The deck spans it. The steps are taped off it, not off the lawn.
- **Prices.** Read on {DATE} where a figure is shown. The H4 line is 150×50 because 140×45 H4 is not listed. The truck is a round figure, not a quote.
- **The rebuilt strip.** The old bearer comes out. If the ground there is worse than the main holes, those four piles get the same 600 mm and the same concrete.

## Sources

Northpine wet-service tables: 140×45 SG8 at 450 centres spans 2.35 m. NZS 3604 wants a pile 150 mm clear of the ground. The deck piles meet that. The bottom step does not. The stair proportion used here is a rise under 190 and 2R+G between 550 and 700. [Northpine tables](https://www.northpine.co.nz/span-tables) · [BRANZ Bulletin 611](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf).

Reproduce with `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`. Earlier plans, including the five short frames, are in archive/. Drawing ISL38807 is a preview and is not for construction.
'''
(root / 'CURRENT_DESIGN.md').write_text(md)
b = io.StringIO(newline='')
w = csv.writer(b, lineterminator='\n')
w.writerow(['Category', 'Description', 'Qty', 'Unit', 'Bunnings NZD', 'Mitre 10 NZD', 'In total NZD', 'Posted, estimate or alternative', 'Comments', 'Source'])
for cat, item, qty, unit, line, mitre, use, comment, kind, url in priced:
    w.writerow([cat, item, qty, unit, '' if line is None else f'{line:.2f}', '' if mitre is None else f'{mitre:.2f}', f'{use:.2f}', kind, comment, url])
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
a = body.index('<h2 id="three-drawings">')
bb = body.index('<h2 id="foundations">', a)
body = body[:a] + '''<h2 id="three-drawings">Drawings</h2><div class="tabs" role="tablist" aria-label="Drawings"><button id="tab-sheet" role="tab" aria-controls="drawing-panel" aria-selected="true" data-view="sheet">Sheet</button><button id="tab-piles" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="piles">1 · Piles</button><button id="tab-framing" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="framing">2 · Framing</button><button id="tab-fixings" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="fixings">3 · Steps</button></div><div id="drawing-panel" role="tabpanel" aria-labelledby="tab-sheet"><div id="drawing"></div><p id="drawing-caption" class="caption"></p></div><p class="note">Download: <a href="drawings/sheet.svg">set-out sheet</a> · <a href="drawings/piles.svg">piles</a> · <a href="drawings/framing.svg">framing</a> · <a href="drawings/fixings.svg">steps</a></p>''' + body[bb:]
body = body.replace('href="docs/', 'href="').replace('archive/', '<a href="https://github.com/MaxHogervorst/deck-design/tree/main/archive">archive/</a>')


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

ol_at = body.index('<ol>', body.index('<h2 id="build-order">'))
ol_end = body.index('</ol>', ol_at) + 5
cards = ''.join(
    f'<details class="step" open><summary><span class="step-number">{n}</span>{E(title)}</summary><div class="step-content">{fig}<div><p>{inline(text)}</p></div></div></details>'
    for n, (title, text, fig) in enumerate(zip(titles, steps, figs), 1))
body = body[:ol_at] + '<div class="steps">' + cards + '</div>' + body[ol_end:]
html = '''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="Owner-builder guide for a 6.6 m Auckland deck and a low step of two steps in front of a 6.6 m deck: layout, holes, fixings and a priced bill of materials."><title>Deck and step build guide</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">Auckland deck <span>11 / 11 / 2026 · BUILD GUIDE</span></a><nav aria-label="Sections"><a href="#three-drawings">Drawings</a><a href="#foundations">Foundations</a><a href="#shopping-list">Shopping list</a><a href="#build-order">Build order</a><a href="#assumptions-and-what-i-would-get-checked-in-an-ideal-world">Assumptions</a></nav><button id="print">Print</button></header><main id="main">''' + body + '''</main><footer><span>Owner-builder working plan · read the assumptions before building</span><button id="copy-link">Copy link</button></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
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
bd += text(40, 700, 'Concrete path stays. No hole in it. Stormwater through the gate, waste beside it. Spade, 500 mm clear.', 12)
bd += text(40, 732, 'Pile marks are the starting grid. Slide a pile off the path or a pipe. Do not open a bay past 1.4 m.', 12)
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

# Set-out sheet. Same geometry as the guide. Not a copy of the ROBO preview.
Sht = 0.098
OX, OY = 168, 34

def PX(x):
    return OX + x * Sht

def PY(y):
    return OY + (y + 1970) * Sht

def piece(x, y, w, h, fill, stroke='#1c1c1c', sw=1, dash=''):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'

def ln(x, y, x2, y2, stroke='#1c1c1c', sw=1.2, dash=''):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'

def tx(x, y, s, size=13, anchor='start', fill='#1c1c1c', weight='650'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{E(s)}</text>'

def hdim(x1, x2, y, label):
    mid = (x1 + x2) / 2
    return (ln(x1, y, x2, y, '#9a2b2b', 1) + ln(x1, y - 4, x1, y + 4, '#9a2b2b', 1)
            + ln(x2, y - 4, x2, y + 4, '#9a2b2b', 1)
            + tx(mid, y - 5, label, 12, 'middle', '#9a2b2b'))

def vdim(x, y1, y2, label):
    mid = (y1 + y2) / 2
    return (ln(x, y1, x, y2, '#9a2b2b', 1) + ln(x - 4, y1, x + 4, y1, '#9a2b2b', 1)
            + ln(x - 4, y2, x + 4, y2, '#9a2b2b', 1)
            + tx(x + 8, mid + 4, label, 12, 'start', '#9a2b2b'))

sh = []
sh.append('<rect width="1680" height="1188" fill="#ffffff"/>')
sh.append('<rect x="16" y="16" width="1648" height="1156" fill="none" stroke="#1d4e89" stroke-width="3"/>')
sh.append('<rect x="22" y="22" width="1636" height="1144" fill="none" stroke="#1d4e89" stroke-width="0.8"/>')
sh.append(tx(40, 78, 'PLAN', 16, 'start', '#1d6b3a'))
sh.append(tx(40, 98, 'house', 12, 'start', '#1d6b3a', '500'))
sh.append(tx(40, 114, 'at the', 12, 'start', '#1d6b3a', '500'))
sh.append(tx(40, 130, 'back', 12, 'start', '#1d6b3a', '500'))

# Outlines. House at the back (top), steps at the front (bottom).
sh.append(piece(PX(0), PY(-1970), 900 * Sht, 1970 * Sht, '#f4f7f2'))
sh.append(piece(PX(0), PY(0), 6600 * Sht, 2600 * Sht, '#f7f4ee'))
sh.append(piece(PX(0), PY(2600), 6600 * Sht, 280 * Sht, '#f3e6c8'))
sh.append(piece(PX(0), PY(2880), 6600 * Sht, 280 * Sht, '#f7ecd2'))
# Path reminder, not a survey. Runs out from the house, under the deck.
sh.append(piece(PX(2850), PY(-1970), 900 * Sht, 5130 * Sht, 'none', '#8a8172', 1, '5 4'))
sh.append(tx(PX(3300), PY(1400), 'path under here', 12, 'middle', '#6d6456', '500'))
sh.append(tx(PX(3300), PY(1400) + 16, 'tape it · no hole', 12, 'middle', '#6d6456', '500'))
# West drain, approximate.
sh.append(ln(PX(-780), PY(-1970), PX(-780), PY(3160), '#a33b32', 3))
sh.append(tx(46, 250, 'drain', 12, 'middle', '#a33b32'))
sh.append(tx(46, 266, 'tape', 11, 'middle', '#a33b32', '500'))
sh.append(tx(46, 280, '500 clear', 11, 'middle', '#a33b32', '500'))
# Joists
for x in d['main_joist_centres_mm']:
    sh.append(piece(PX(x - 22.5), PY(45), 45 * Sht, 2510 * Sht, '#c9d5c4', '#52675b', 0.6))
for x in (3933, 3978):
    sh.append(piece(PX(x - 22.5), PY(45), 45 * Sht, 2510 * Sht, '#254c3e', '#254c3e', 0.6))
for x in (22.5, 450, 877.5):
    sh.append(piece(PX(x - 22.5), PY(-1925), 45 * Sht, 1880 * Sht, '#c9d5c4', '#52675b', 0.6))
# Bearers and rims
for y in (300, 2510):
    sh.append(piece(PX(0), PY(y - 45), 6600 * Sht, 90 * Sht, '#c4a574', '#1c1c1c', 0.8))
for y in (-1925, -800):
    sh.append(piece(PX(0), PY(y - 45), 900 * Sht, 90 * Sht, '#c4a574', '#1c1c1c', 0.8))
for y, length in ((0, 6600), (2555, 6600), (-1970, 900), (-45, 900)):
    sh.append(piece(PX(0), PY(y), length * Sht, 45 * Sht, '#b08958', '#1c1c1c', 0.7))
# Step members
sh.append(piece(PX(0), PY(2555), 6600 * Sht, 90 * Sht, '#c4a574', '#1c1c1c', 0.8))
sh.append(piece(PX(0), PY(3070), 6600 * Sht, 90 * Sht, '#c4a574', '#1c1c1c', 0.8))
sh.append(piece(PX(0), PY(2600), 6600 * Sht, 90 * Sht, '#af6b3c', '#1c1c1c', 0.8))
sh.append(piece(PX(0), PY(2880), 6600 * Sht, 90 * Sht, '#af6b3c', '#1c1c1c', 0.8))
for x in d['main_joist_centres_mm']:
    sh.append(piece(PX(x - 22.5), PY(2645), 45 * Sht, 425 * Sht, '#d7e0d2', '#52675b', 0.5))
# Piles
for y in (300, 2510):
    for x in pile_x:
        sh.append(piece(PX(x - 200), PY(y - 200), 400 * Sht, 400 * Sht, 'none', '#7d8b82', 0.8, '3 2'))
        sh.append(piece(PX(x - 62.5), PY(y - 62.5), 125 * Sht, 125 * Sht, '#254c3e', '#1c1c1c', 0.8))
for y in (-1925, -800):
    for x in (175, 725):
        sh.append(piece(PX(x - 200), PY(y - 200), 400 * Sht, 400 * Sht, 'none', '#7d8b82', 0.8, '3 2'))
        sh.append(piece(PX(x - 62.5), PY(y - 62.5), 125 * Sht, 125 * Sht, '#254c3e', '#1c1c1c', 0.8))
for x in pile_x:
    sh.append(piece(PX(x - 150), PY(3115 - 150), 300 * Sht, 300 * Sht, 'none', '#af6b3c', 0.8, '3 2'))
    sh.append(piece(PX(x - 62.5), PY(3115 - 62.5), 125 * Sht, 125 * Sht, '#af6b3c', '#1c1c1c', 0.8))

sh.append(tx(PX(500), PY(-700), 'rebuilt', 13, 'middle', '#1d6b3a'))
sh.append(tx(PX(500), PY(-560), '900 wide', 12, 'middle', '#1d6b3a', '500'))
sh.append(tx(PX(1600), PY(900), 'deck  6600 × 2600', 15, 'start'))
sh.append(tx(PX(1800), PY(1700), 'joists 437 crs', 13, 'middle', '#254c3e'))
sh.append(tx(PX(4300), PY(1100), 'board butts', 12, 'start', '#254c3e'))
sh.append(tx(PX(6100), PY(2740), 'top step', 13, 'end'))
sh.append(tx(PX(6100), PY(3020), 'bottom step', 13, 'end'))
sh.append(tx(PX(62.5), PY(-400), '62.5', 11, 'middle', '#9a2b2b', '500'))

# Dimensions outside the plan
sh.append(hdim(PX(0), PX(6600), PY(3160) + 22, '6600'))
sh.append(vdim(PX(6600) + 16, PY(0), PY(2600), '2600'))
sh.append(vdim(PX(0) - 16, PY(-1970), PY(0), '1970'))
sh.append(vdim(PX(6600) + 58, PY(2600), PY(3160), '560'))
sh.append(tx(PX(80), PY(3160) + 42, 'piles at 1295 centres · two goings of 280 · step piles on the same X, at Y3115', 12, 'start', '#9a2b2b', '500'))

# Section
sec_s = 0.46

def SY(y):
    return 900 + (y - 2400) * sec_s

def SZ(z):
    return 390 - z * sec_s

sh.append(tx(900, 58, 'STEPS  ·  cut through the front', 16, 'start', '#1d6b3a'))
sh.append(tx(900, 76, 'tape the rises off the path', 12, 'start', '#1d6b3a', '500'))
sh.append(piece(SY(2480), SZ(0), (3300 - 2480) * sec_s, 36, '#efe6d4', '#52675b', 0.8))
sh.append(piece(SY(2520), SZ(46), 620 * sec_s, 28, '#cfc6b4', '#52675b', 0.8))
sh.append(ln(SY(2420), SZ(0), SY(3320), SZ(0), '#52675b', 1.2))
sh.append(piece(SY(2465), SZ(328), 90 * sec_s, 140 * sec_s, '#c4a574'))
sh.append(piece(SY(2380), SZ(468), 220 * sec_s, 140 * sec_s, '#456b54'))
sh.append(piece(SY(2555), SZ(468), 45 * sec_s, 140 * sec_s, '#c4a574'))
sh.append(piece(SY(2380), SZ(500), 220 * sec_s, 32 * sec_s, '#d7b98a'))
sh.append(piece(SY(2555), SZ(135), 90 * sec_s, 120 * sec_s, '#c4a574'))
sh.append(piece(SY(2645), SZ(135), 425 * sec_s, 45 * sec_s, '#456b54'))
sh.append(piece(SY(3070), SZ(135), 90 * sec_s, 120 * sec_s, '#c4a574'))
sh.append(piece(SY(2600), SZ(301), 90 * sec_s, 140 * sec_s, '#af6b3c'))
sh.append(piece(SY(2690), SZ(301), 190 * sec_s, 45 * sec_s, '#456b54'))
sh.append(piece(SY(2880), SZ(301), 90 * sec_s, 140 * sec_s, '#af6b3c'))
sh.append(piece(SY(2600), SZ(333), 280 * sec_s, 32 * sec_s, '#d7b98a'))
sh.append(piece(SY(2880), SZ(167), 280 * sec_s, 32 * sec_s, '#d7b98a'))
sh.append(piece(SY(3052), SZ(20), 26, 70, '#af6b3c'))
sh.append(tx(SY(2360), SZ(530), '+500', 12, 'start', '#9a2b2b'))
sh.append(tx(SY(2680), SZ(370), '+333', 12, 'start', '#9a2b2b'))
sh.append(tx(SY(3000), SZ(200), '+167', 12, 'start', '#9a2b2b'))
sh.append(tx(SY(2700), SZ(-30), 'path = 0', 12, 'start', '#6d6456', '500'))
sh.append(hdim(SY(2600), SY(2880), SZ(-8), '280'))
sh.append(hdim(SY(2880), SY(3160), SZ(70), '280'))
sh.append(tx(SY(3180), SZ(150), 'rip to', 11, 'start', '#1d6b3a'))
sh.append(tx(SY(3180), SZ(134), '120 min', 11, 'start', '#1d6b3a'))
sh.append(tx(SY(3180), SZ(100), 'over path', 11, 'start', '#1d6b3a', '500'))

# Notes
sh.append(tx(1360, 58, 'NOTES', 16, 'start', '#1d6b3a'))
notes = [
    '140×45 SG8. H3.2 on the deck.',
    'H4 on both steps.',
    '88×32 griptread, along the length.',
    '16 piles, 125×125 H5.',
    'Holes 400×400, 600 deep.',
    'No anchor brackets.',
    'Six step piles, holes',
    '300×300 and 400 deep.',
    'Joists at 437. Doubled',
    'at 3956 for the butts.',
    'Screws into a bearer',
    'go in from the side.',
    'Path stays. No hole in it.',
    'West drains: spade, and',
    '500 mm clear of a pipe.',
    'Rises off the path. If the',
    'tape is not 500, divide by 3.',
    'No handrail. Three rises',
    'is the limit.',
    'Not drawing ISL38807.',
    'Not for consent.',
]
ny = 82
for note in notes:
    sh.append(tx(1360, ny, note, 12, 'start', '#1c1c1c', '500'))
    ny += 16

# Long elevation, aligned with the plan
sh.append(tx(40, 690, 'LONG SIDE', 16, 'start', '#1d6b3a'))
sh.append(tx(160, 690, 'steps are towards you · pile tops cut to one string off the path', 12, 'start', '#1d6b3a', '500'))
GZ = 900

def EZ(z):
    return GZ - z * 0.34

sh.append(ln(PX(0), EZ(0), PX(6600), EZ(0), '#52675b', 1.4))
sh.append(piece(PX(0), EZ(0), 6600 * Sht, 28, '#efe6d4', 'none'))
for x in pile_x:
    sh.append(piece(PX(x - 62.5), EZ(187), 125 * Sht, (187 + 80) * 0.34, '#c4a574'))
    sh.append(ln(PX(x), EZ(187), PX(x), EZ(187) + 46, '#7d8b82', 1, '3 2'))
sh.append(piece(PX(0), EZ(468), 6600 * Sht, 140 * 0.34, '#456b54'))
sh.append(piece(PX(0), EZ(328), 6600 * Sht, 140 * 0.34, '#c4a574'))
sh.append(piece(PX(0), EZ(500), 6600 * Sht, 32 * 0.34, '#d7b98a'))
sh.append(tx(PX(6700), EZ(490), '+500', 12, 'start', '#9a2b2b'))
sh.append(tx(PX(200), EZ(300), 'bearer', 12, 'start', '#9a2b2b'))
sh.append(tx(PX(5200), EZ(160), 'pile top +187', 12, 'start', '#9a2b2b'))
sh.append(tx(PX(80), EZ(-36), '600 deep, all 16 the same', 12, 'start', '#1d6b3a'))
sh.append(tx(PX(2800), EZ(0) + 20, 'path / string  0', 12, 'start', '#6d6456', '500'))

# Title block
sh.append('<rect x="22" y="1048" width="1636" height="118" fill="#f7f4ee" stroke="#1d4e89"/>')
sh.append(ln(300, 1048, 300, 1166, '#1d4e89', 1))
sh.append(ln(1280, 1048, 1280, 1166, '#1d4e89', 1))
sh.append(ln(1280, 1107, 1658, 1107, '#1d4e89', 0.8))
sh.append(tx(48, 1095, 'WORKING', 22))
sh.append(tx(48, 1122, 'PLAN', 22))
sh.append(tx(48, 1148, 'owner-builder', 12, 'start', '#1d6b3a', '500'))
sh.append(tx(320, 1088, 'DECK AND TWO STEPS', 22))
sh.append(tx(320, 1116, '18B FORMBY AVENUE, POINT CHEVALIER', 15, 'start', '#1c1c1c', '500'))
sh.append(tx(320, 1142, 'Not the ROBO preview ISL38807. Dimensions in millimetres. Read the assumptions before building.', 13, 'start', '#1d6b3a', '500'))
sh.append(tx(1300, 1078, 'DATE   11 / 11 / 2026', 14))
sh.append(tx(1300, 1100, 'SHEET   1 of 1', 14))
sh.append(tx(1300, 1136, 'Holes 600. No anchors.', 13, 'start', '#1c1c1c', '500'))
sh.append(tx(1300, 1154, 'Two steps. Rise about 167.', 13, 'start', '#1c1c1c', '500'))

sheet = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1680 1188" role="img" '
    'aria-label="Set-out sheet for the 6.6 m deck and two steps. Owner-builder working plan, not the ROBO preview.">'
    '<title>Set-out sheet · deck and two steps</title>'
    '<style>text{font-family:system-ui,sans-serif}</style>'
    + ''.join(sh) + '</svg>'
)
(root / 'site/drawings' / 'sheet.svg').write_text(sheet)
print('sheet', len(sheet))

