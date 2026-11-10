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
frames = t['frame_X_mm']
DATE = '10 November 2026'
frame_list = ', '.join(str(x) for x in frames)
# (item, quantity, store, unit price basis, line total NZD incl GST, posted|estimate, url)
rows = [
    ('Framing 140×45 H3.2 SG8, wet (main deck and rebuilt strip)', '100.8 m: 6×7.2 m, 8×6.0 m, 2×4.8 m', 'Bunnings', '6.0 m $70.91 and 4.8 m $56.73 posted; 7.2 m not listed online, priced at the same $11.82/m', 6 * 85.10 + 8 * 70.91 + 2 * 56.73, 'estimate', 'https://www.bunnings.co.nz/140-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-6m_p0616262'),
    ('Step framing 140×45 H4 SG8 (short frame rails, crosspieces, ties)', f'{d["H4_stock_lm"]:g} m: 5×4.8 m', 'Bunnings or Mitre 10, price in store', '140×45 H4 has no online price; basis Bunnings 150×50 SG8 H4 rough sawn $17.11/m. Ordinary 4.8 m lengths, not a 6.7 m rail', d['H4_stock_lm'] * 17.11, 'estimate', 'https://www.bunnings.co.nz/150-x-50mm-sg8-h4-wet-sawn-treated-timber-per-linear-metre_p0276210'),
    ('Decking 88×32 H3.2 merch griptread, 4.2 m and 3.0 m', f'{deck["stock_4200"]}×4.2 m and {deck["stock_3000"]}×3.0 m ({deck["stock_lm"]} m)', 'Bunnings, in store', '$4.55/m posted. Ask for these lengths. A random-length mix will not land the butts on the doubled joist', deck['stock_lm'] * 4.55, 'posted', 'https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
    ('Ordinary piles 125×125 H5, 750 mm', '12', 'Bunnings', '$21.04 each', 12 * 21.04, 'posted', 'https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
    ('Corner anchor piles 125×125 H5, 1.2 m', '4', 'Bunnings', '$32.42 each', 4 * 32.42, 'posted', 'https://www.bunnings.co.nz/125-x-125mm-1-2m-square-h5-anchor-pile_p0276402'),
    ('Anchor pile fixing kits, LUMBERLOK 12KNH stainless', '4', 'Bunnings', '$84.93 each (galvanised 12KN is $37.89). Confirm the bracket fits a 90 mm double bearer and a 125 mm pile before buying four', 4 * 84.93, 'posted', 'https://www.bunnings.co.nz/lumberlok-12kn-pile-fixing-high-corrosion-stainless-steel-12knh_p0827939'),
    ('Concrete for the 16 pile holes, about 0.99 m³', f'Mini-mix 1.2 m³. Fallback: {cv["bags_20kg_buy"]} bags of 20 kg ({cv["bags_20kg_needed"]} needed)', 'Bunnings for bags; phone a mini-mix yard', f'$11.24 a bag, which is the figure in the total. Order the truck first. Bags only if it cannot reach the lawn', cv['bags_20kg_buy'] * 11.24, 'posted', 'https://www.bunnings.co.nz/cemix-20kg-multicrete_p0232228'),
    ('Concrete pavers 300×300, about 40 mm thick', f'{d["paver_count"]} (four per frame)', 'Mitre 10, price in store', 'Mitre 10 Urban Paving 300×300×40 has no online price; basis Bunnings WestStone 300×300×37 $10.83. A thicker block is better if the store has one', d['paver_count'] * 10.83, 'estimate', 'https://www.mitre10.co.nz/shop/urban-paving-paver-300x300x40mm-natural/p/387387'),
    ('GAP7 basecourse for the five step pits', f'{cv["gap7_bags_15l"]} bags of 15 L (about {cv["gap7_m3"]:.2f} m³), or one trailer scoop', 'Bunnings, or a landscape yard', f'$9.79 a bag (Daltons 0-7 mm). A scoop is much cheaper than {cv["gap7_bags_15l"]} bags', cv['gap7_bags_15l'] * 9.79, 'posted', 'https://www.bunnings.co.nz/daltons-15l-0-7mm-sub-base-metal_p0237633'),
    ('Decking screws 10g×65 316 stainless', f'3×500 ({deck["base_screws"]} needed)', 'Bunnings', '$116.00 per 500 (Building King)', 3 * 116.00, 'posted', 'https://www.bunnings.co.nz/decking-screw-65-x-10g-316-stainless-steel-500-pack_p0379643'),
    ('Framing nails 90×4 316 stainless jolt head', '2×2 kg (bearer plies and the short step rails)', 'Mitre 10', '$129.00 per 2 kg (Ecko)', 2 * 129.00, 'posted', 'https://www.mitre10.co.nz/shop/ecko-jolt-head-nails-90-x-4-0mm-2kg-316-stainless-steel/p/307864'),
    ('Framing nails 100×4 316 stainless jolt head', '5×500 g (joists, rims, crosspieces, skew nails)', 'Bunnings', '$35.59 per 500 g (NZ Nails)', 5 * 35.59, 'posted', 'https://www.bunnings.co.nz/nz-nails-100-x-4mm-500g-316-stainless-steel-jolt-head-nail_p0383199'),
    ('Batten screws 14g×100 316 stainless', '100 pack (30 for the five step ties, 6 skewed into the rebuilt joists)', 'Bunnings', '$77.05 per 100 (Bremick XTP)', 77.05, 'posted', 'https://www.bunnings.co.nz/bremick-xtp-14g-x-100mm-t40-stainless-steel-316-black-bugle-batten-100-pack_p0575899'),
    ('Rim tie bolts M12×120 316 coach bolts, nuts and 50 mm square washers', '2 bolts and nuts, 4 washers', 'Bunnings', '$4.90 + $1.25 + 2×$3.54 per bolt', 2 * (4.90 + 1.25 + 2 * 3.54), 'posted', 'https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
    ('DPC Supercourse 500, 150 mm×30 m', '1 roll (pile tops and paver tops)', 'Bunnings', '$27.42', 27.42, 'posted', 'https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
    ('Cut-end preservative, Metalex Green 1 L', '1, brushed on every saw cut in treated timber', 'Bunnings', '$66.00', 66.00, 'posted', 'https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
]
rows = [(a, b, c, e, round(float(f), 2), g, h) for a, b, c, e, f, g, h in rows]
posted = round(sum(r[4] for r in rows if r[5] == 'posted'), 2)
est = round(sum(r[4] for r in rows if r[5] == 'estimate'), 2)
total = round(posted + est, 2)
steps = [
    'Before you buy. Measure the door sill and the bottom of the cladding, and measure the fall of the lawn along the 6.6 m. The deck top has to stay below the sill and clear of the cladding; if that forces it off +500, drop the step by the same amount and do not force this drawing. If the lawn falls more than about 30 mm, set the pile string off the high side so every pile stays at least 150 mm clear of the ground. Check the sea-spray zone on the Auckland Council GIS viewer and buy one fastener metal only: stainless if you are inside it, hot-dip galvanised if you are not. The shopping list is priced in stainless until that check is done. Call beforeUdig (0800 248 344) or check the property file for pipes and cables where the holes go.',
    'Set out. String the 6600×2600 outline, the 900×1970 rebuilt strip and the 400 mm step. End joist flush with the deck edge, then joists at 437 mm centres, with one doubled joist centred at 3956 (the two plies touching). Mark the 16 pile holes from Drawing 1. Do not mark the step pits yet. Leave the lawn and path at their present levels.',
    'Dig. Twelve ordinary holes and four corner anchor holes. Ordinary holes 450 deep, anchor holes 900 deep, down to firm natural ground, not topsoil. A 400 mm auger hole is fine; the 350×350 square is the same job if you are digging by hand. If a hole is still soft or wet at depth, stop and read the assumptions.',
    f'Pour. You want a second person for this. Stand all 16 piles long and plumb, brace them, and fill every hole to about 100 mm below ground in one go, about {cv["main_net_m3"]:.2f} m³. Order 1.2 m³ of mini-mix. Buy {cv["bags_20kg_buy"]} bags of 20 kg only if the truck cannot reach the lawn ({cv["bags_20kg_needed"]} are the calculated fill). Nothing in this pour needs to be level; the piles get cut later.',
    'Cut the piles. After the concrete has set, string a line along each pile row with a water level or laser. On a flat lawn the line is +187 mm. If the lawn rises, keep the line high enough that the shortest pile is still 150 mm clear, and let the low side stand taller. Mark every pile, cut square, brush preservative on the cuts, and lay a square of DPC on each pile top.',
    'Bearers. Nail up the two 6.6 m main double bearers and two 0.9 m rebuilt double bearers (F1). Seat them on the piles at Y300 and Y2510, and at Y−1925 and Y−800, and skew-nail (F2). Fit the four corner anchor kits the way the sheet in the box shows. Take out the old rear bearer; do not reuse it.',
    'Joists and rims. 17 main joists of 2510 mm: flush at each end, 437 mm centres, the doubled joist centred at 3956. Three rebuilt joists of 1880 mm, two blocks cut at 380 mm over the Y−800 bearer, and two 14g×100 screws skewed from each rebuilt joist down into that bearer (F4). Nail the 6.6 m rims at Y0 and Y2555 and the 900 mm rebuilt rims. Two M12 rim ties where the rebuilt strip meets the main deck (F6).',
    f'Step ties. Screw five 250 mm H4 ties to the outside face of the front bearer at X{frame_list}, bottoms at +78 (390 mm down from the rim top). Four 14g×100 screws into the bearer on each tie (F5). The frames get screwed to these once they are packed.',
    f'Step pits. With the deck frame up, dig five pits 760×800 mm centred at X{frame_list}, Y2800, about 150 mm deep or down to firm ground. Stay out of the pile concrete: the pit edge wants about 90 mm of soil between it and the hole, and the pavers want 100 mm. Fill with GAP7 in two layers and tamp each hard. In each pit bed four 300×300 pavers, two along each rail, centred 220 mm each side of the pit centre (Y2645 and Y2955). Tap them down until a straight edge and a tape put the top about 400 to 420 mm below the deck rim. Lower is fine. Higher is not.',
    'Step frames, in place. Do not build one 6.6 m ladder and try to lift it. For each bay, nail a double 900 mm H4 rail (F1), set it on the inner pavers against the tie, and screw an H4 offcut packer to the side of the rail so the rail top is 250 mm below the deck rim and the rail does not rock. Nail the three 220 mm crosspieces (ends and middle) to that rail, set the outer double rail, nail the crosspieces through into it, and pack that rail the same way. Then put two 14g×100 screws from the tie into the inner rail. Five frames, one at a time.',
    'Boards. Lay 28 rows on the main deck, 21 on the rebuilt strip and 4 on the step, all along X. Deck butts go on the doubled joist at 3956, so use the 4.2 m and 3.0 m lengths and trim them to meet there. Cut the step boards to 6400 mm, centre them (they stop about 100 mm short of each deck end), and put the step butt on the middle crosspiece of the centre frame. About 5 mm gaps on the deck and about 6 mm on the rebuilt strip. The four step boards sit on the 400 mm frame with a small overhang on the front. Two screws per board per joist or crosspiece. Brush every cut. Keep lawn, path and garden clear of the timber.',
]
fixings = [
    ('F1', 'Double bearers and double step rails', '90×4 stainless nails, two rows at 250 mm centres, alternating faces. Same pattern on each 900 mm step rail.'),
    ('F2', 'Ordinary pile to bearer', 'Four 100×4 stainless skew nails at each pile.'),
    ('F3', 'Joists, rims, blocks, crosspieces', 'NZS 3604 Table 7.5 nailing: two 100×4 stainless per joist end through the rim, two per crosspiece end.'),
    ('F4', 'Rebuilt joists to the bearer', 'Four 100×4 skew nails and two 14g×100 screws skewed down from the joist into the bearer, at each rebuilt joist. The point-load screen can put about 1.9 kN of uplift on one support. This is ordinary carpentry, not a rated bracket.'),
    ('F5', 'Step ties (hold-down and sideways)', f'Five 250 mm 140×45 H4 ties on the front bearer face, at X{frame_list}, bottom +78. Four 14g×100 screws into the bearer and two into the inner rail. A paver cannot pull the rail down. If the far paver lifts when someone stands on the end of a frame, the tie has to hold about {abs(sc["liftoff_tie_ULS_kN"]):.1f} kN and the near paver takes about {sc["liftoff_paver_ULS_kN"]:.1f} kN. Those two screws into the inner rail are ordinary carpentry, not a rated hold-down. The outer rail is only nailed on through the crosspieces.'),
    ('F6', 'Rebuilt to main rim tie', 'Two M12×120 stainless coach bolts through the adjacent rims at X200/700, Z398, 50 mm square washers both sides.'),
    ('F7', 'Corner anchor piles', 'Four corner piles with complete LUMBERLOK 12 kN kits fitted to the maker\'s sheet. Check the sheet fits a 90 mm double bearer. These brace the whole deck; see the assumptions.'),
    ('F8', 'Step rails on pavers', 'No fixing into the paver. DPC on the paver, then one H4 offcut packer screwed to the side of the rail if the paver is low. The five ties (F5) hold the frames to the deck.'),
]
md = f'''# Deck and step build guide

{DATE} · How I am going to build the 6.6 m deck and the low step in front of it. One plan, three drawings, a priced shopping list and the build order, written for an owner doing the work. It is not an engineer's design; the things I have assumed, and would ideally have checked, are listed at the end.

## What we are building

| Part | What |
|---|---|
| Main deck | 6600×2600 mm, boards about 500 mm above the lawn. Two double 140×45 H3.2 bearers on 16 timber piles in rows at Y300 and Y2510; 140×45 joists across them, 2.21 m span (the table limit at 450 centres is 2.35 m). |
| Main joists | 17 members. End joist flush with the deck edge, then 437 mm centres, and one doubled joist centred at 3956 so the board butts have something to land on. Plain rims at Y0 and Y2555; no blocking, because the rims are within 300 mm of the bearers. |
| Rebuilt strip | 900×1970 mm beside the house. Old bearer replaced. Two 900 mm double bearers at Y−1925 and Y−800, three separate 1880 mm joists, two blocks cut at 380 mm, screws and skew nails down into the bearer. Nothing runs through into the main deck. |
| Step | 400 mm deep, boards 250 mm above the lawn, stopping about 100 mm short of each end of the deck. Five separate 900 mm frames of double 140×45 H4, one in each gap between the front piles, centred at X{frame_list}. Each frame sits on four pavers and is screwed to the front bearer. The boards run along X across the frames. The gap between frames is {t["board_gap_mm"]:.0f} mm, under the 450 mm the deck joists already use. |
| Boards | 32 mm treated pine, all running along X. 28 rows on the deck, 21 on the rebuilt strip, 4 on the step. |
| Finish | Natural treated pine, plain front edge, no handrails. Lawn and path stay at their present levels. |

Set-out, X from the left edge. Joists: flush, then every 437 mm, double at 3956. Main piles: 62.5, 1357.5, 2652.5, 3947.5, 5242.5, 6537.5 on rows Y300 and Y2510. Rebuilt piles: X175 and X725 on Y−1925 and Y−800. Step frames: {frame_list}. Pavers sit 220 mm each side of those centres, on Y2645 and Y2955.

Heights, lawn = 0: deck boards top +500, joist and rim top +468, bearer top +328, pile top +187 (DPC under the bearer). Step boards top +250, rail top +218, rail bottom +78. Under the rail: an H4 packer if needed, DPC, and a paver top anywhere between +45 and +75.

## Three drawings

[1 · Piles, pads and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixings and step section](docs/drawings/fixings.svg)

## Foundations

16 timber piles: 12 ordinary (450 deep) and 4 corner anchors (900 deep) with 12 kN fixing kits. Holes can be 350×350 square or about 400 mm round from an auger. One pour of about {cv["main_net_m3"]:.2f} m³ fills every hole to 100 mm below ground; nothing in it needs to be level, because the piles are cut to a string afterwards. A mini-mix truck for 1.2 m³ is the way to do this. {cv["bags_20kg_buy"]} bags of 20 kg is the fallback if the truck cannot get in.

The step does not get concrete. Each of the five frames has one pit, 760×800 mm, dug to firm ground in the middle of the bay so it stays off the pile holes. Compacted GAP7, then four 300×300 pavers. The frames are screwed to the deck, so a paver does not have to be a perfect level and it does not have to hold the step from sliding away.

### Why the step is five short frames

A timber pile has to stand at least 150 mm clear of the ground, and under a 250 mm step there is only about 78 mm, so short piles are out. A single 6.6 m ladder rail is a special-order length, it is too heavy to lift in one piece, and the pads it needs clash with the corner pile holes. Five 900 mm frames use ordinary 4.8 m H4, each one is light enough to assemble where it sits, and the pavers land in the open ground between the holes. With someone standing on the end of a frame the rail is about {sc["double_rail_utilisation"]*100:.0f}% of my bending screen, and it stays there if the far paver lifts, because the moment is the short overhang. A paver cannot hold the rail down. If it lifts, the tie has to hold about {abs(sc["liftoff_tie_ULS_kN"]):.1f} kN, which is why each frame is screwed to the bearer instead of sitting loose.

### Setting the pavers without a level

1. Build the deck frame first. Its rim is straight and level, so every step measurement is a tape held down from the rim top.
2. Dig each pit to firm ground, keep it off the pile concrete, fill with GAP7 in two layers and tamp each one hard. Bed the four pavers and tap them down until the top is 400 to 420 mm below the rim top. Lower is fine, higher is not.
3. Build that frame on the pavers, pack each rail with an H4 offcut screwed to the rail until the frame top is 250 mm below the rim top, and screw the tie on. Then do the next frame.

## Shopping list

Do the measurements in build step 1 before you buy fasteners or lock the timber lengths.

[Download the CSV](docs/shopping-list.csv). NZD including GST, read from bunnings.co.nz and mitre10.co.nz on {DATE}. Posted means the price shown online for that exact product; estimate means the item is sold in store or by special order and a listed stand-in was used for the price. Timber and heavy items at both stores are click-and-collect or in-store only. Nothing has been bought and no supplier has been contacted.

| Item | Quantity | Store | Price basis | Line |
|---|---|---|---|---|
'''
for item, qty, sup, basis, line, kind, url in rows:
    md += f'| {item} | {qty} | {("[" + sup + "](" + url + ")") if url else sup} | {basis}{" (estimate)" if kind == "estimate" else ""} | ${line:,.2f} |\n'
md += f'''
**Posted prices ${posted:,.2f} + estimates ${est:,.2f} = about ${total:,.0f} including GST.** The concrete line is the bag price, so the total still covers the holes if the truck cannot get in; a mini-mix quote should be lower. Delivery, tool hire (auger, drop saw, tamper) and soil disposal are extra. Galvanised fasteners instead of stainless, if the GIS check says you are outside the sea-spray zone, cuts a lot of the fixing cost. Trade merchants will beat most of these prices.

If 140×45 H4 cannot be had, rough-sawn 150×50 H4 SG8 works for the step frames. The rails are then 10 mm deeper and 10 mm wider, so cut the crosspieces at 200 mm and aim the paver tops 10 mm lower. Still cut them at 900 mm. Do not go back to a 6.6 m rail.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Main and rebuilt: {d["main_stock_lm"]} m bought, {d["main_installed_lm"]} m used. 6600 = 4 bearer plies + 2 rims; 2510 = 17 joists; 900 = 4 rebuilt bearer plies + 2 rebuilt rims; 380 = 2 blocks; 1880 = 3 rebuilt joists. If 7.2 m lengths are not in stock, splice each bearer ply over a pile (stagger the two plies) and each rim at a joist.

| 140×45 H4 stock | Cuts, mm |
|---|---|
'''
for a in d['H4_stock_allocations']:
    md += '| {n}×{s} | {cuts} |\n'.format(n=a['count'], s=a['stock_mm'], cuts=' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm']))
md += f'''
Step: {d["H4_stock_lm"]:g} m bought, {d["H4_installed_lm"]} m used. 900 = the 20 rail plies (four per frame); 220 = 15 crosspieces (three per frame, at the ends and the middle); 250 = 5 ties. Ask for five 4.8 m lengths. Allow 4 mm per saw cut and 5 mm end trim. Boards: 28 rows on the deck from the 4.2 m and 3.0 m lengths, 21 rows of 900 mm on the rebuilt strip, 4 step boards cut to 6400 mm. {deck["base_screws"]} screw positions, buy 1500.

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

This is what I would do. None of it has been checked by an engineer or a builder, and no council consent is involved: the deck is under 1.5 m, so it is exempt building work, but it still has to be built properly.

- **The four corner piles as anchors.** A freestanding deck needs something to stop it racking. My default is four corner anchor piles with 12 kN kits in 900 mm holes. An engineer would size this properly from the deck weight and the site wind and earthquake loads. I also need the bracket in the box to fit a 90 mm double bearer and a 125 mm pile. If the sheet shows a single bearer, I will not pack it out to suit.
- **The ground.** Every footing assumes firm natural clay at about 100 kPa under the topsoil, which is normal for Auckland but not guaranteed. One step paver is asked for about {sc["paver_bearing_kPa_max"]:.0f} kPa while both pavers stay down, and about {sc["liftoff_paver_bearing_kPa"]:.0f} kPa if the far one lifts. That second figure is just over the 100 kPa assumption, and either figure is a lot for a 40 mm patio paver. A thicker paver or a concrete block from the same yard is better if they have it. If a hole hits soft, wet or filled ground, that hole needs a deeper or wider footing, and someone who knows soils should look at it.
- **The step frames.** Each double rail is checked as a short beam only, at {sc["double_rail_utilisation"]*100:.0f}% of my screen with a 2.7 kN point load on the end of a frame. Pretending both pavers can pull down shows about {abs(sc["min_paver_reaction_ULS_kN"]):.1f} kN trying to lift the far paver. They cannot. With that paver out of the sum, the centre tie holds about {abs(sc["liftoff_tie_ULS_kN"]):.1f} kN and the bending does not get worse. The two screws into the inner rail are ordinary carpentry, not a rated connection, and the outer rail only reaches them through the nailed crosspieces. I would rather have the screws than pretend the frame only sits on the pavers.
- **Stainless everywhere, until I check.** The list is priced in 316 stainless because I do not yet know if the site is in the sea-spray zone (within 500 m of the sea or a harbour, or 100 m of a tidal estuary or sheltered inlet). Outside it, NZS 3604 allows hot-dip galvanised, which is about a quarter of the price. I will check the GIS viewer before I buy a single nail.
- **The house junction and the fall of the lawn.** I have not drawn the gap to the cladding or the drop from the door sill, and I am assuming the lawn is flat to within about 30 mm. Step 1 is to measure all three. Keep the deck below the door sill, keep timber off the cladding, and do not bury a pile to save the low end.
- **The 250 mm step.** A single 250 mm rise is above what the stair rules allow for a compliant step. It is our choice for this garden, and nothing here claims access compliance. The step boards stop about 100 mm short of the deck ends so they are not cantilevering past the end frames.
- **Timber and prices.** 140×45 H4 is not listed online; 4.8 m lengths cut into 900 mm frames are the ask, and rough-sawn 150×50 is the fallback in the shopping list. Decking is named 4.2 m and 3.0 m lengths, not a random mix. Prices were read on {DATE} and will drift.
- **The old rebuilt strip.** I am replacing the old bearer and not relying on any retained timber. The rebuilt joists are screwed and skew-nailed to the new bearer. If what comes out of the ground is worse than expected, the rebuilt piles get the same treatment as the main ones.

## Sources

Northpine wet-service tables: 140×45 SG8 at 450 centres spans 2.35 m; NZS 3604 Table 7.2 allows an 1100 mm cantilever against the rebuilt 755 mm; §7.1.2 allows rims within 300 mm of a support to replace blocking; §6.4 requires piles to stand 150 mm clear of the ground. [Northpine tables](https://www.northpine.co.nz/span-tables) · [MiTek LUMBERLOK data](https://mitek.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf) · [BRANZ Bulletin 611, low bearers on concrete](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf) · [H4 SG8 product information](https://www.fwp.co.nz/wp-content/uploads/2023/11/Building-Products-Information-Waipapa-Pine-H4-H5-H6-MG-RS-SG8-Framing-Timber.pdf).

Reproduce with `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`; data in design.json. The step frames are 900 mm. They do not need to be one continuous rail. Earlier plans are in archive/.
'''
(root / 'CURRENT_DESIGN.md').write_text(md)
b = io.StringIO(newline='')
w = csv.writer(b, lineterminator='\n')
w.writerow(['Item', 'Quantity', 'Store', 'Price basis', 'Line NZD incl GST', 'Posted or estimate', 'Source'])
w.writerows(rows)
w.writerow(['TOTAL', '', '', '', total, f'posted {posted} + estimates {est}', ''])
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
body = body[:a] + '''<h2 id="three-drawings">Three drawings</h2><div class="tabs" role="tablist" aria-label="Drawings"><button id="tab-piles" role="tab" aria-controls="drawing-panel" aria-selected="true" data-view="piles">1 · Piles, pads & heights</button><button id="tab-framing" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="framing">2 · Framing</button><button id="tab-fixings" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="fixings">3 · Fixings & step section</button></div><div id="drawing-panel" role="tabpanel" aria-labelledby="tab-piles"><div id="drawing"></div><p id="drawing-caption" class="caption"></p></div><p class="note">Download: <a href="drawings/piles.svg">piles</a> · <a href="drawings/framing.svg">framing</a> · <a href="drawings/fixings.svg">fixings</a></p>''' + body[bb:]
body = body.replace('href="docs/', 'href="').replace('archive/', '<a href="https://github.com/MaxHogervorst/deck-design/tree/main/archive">archive/</a>')
html = '''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="Owner-builder guide for a 6.6 m Auckland deck and a low step of five short frames: layout, foundations, fixings, build order and a priced shopping list."><title>Deck and step build guide</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">Auckland deck <span>10 / 11 / 2026 · BUILD GUIDE</span></a><nav aria-label="Sections"><a href="#three-drawings">Drawings</a><a href="#foundations">Foundations</a><a href="#shopping-list">Shopping list</a><a href="#build-order">Build order</a><a href="#assumptions-and-what-i-would-get-checked-in-an-ideal-world">Assumptions</a></nav><button id="print">Print</button></header><main id="main">''' + body + '''</main><footer><span>Owner-builder working plan · read the assumptions before building</span><button id="copy-link">Copy link</button></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
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
outline = r(X(0), Y(0), 6600 * .105, 2600 * .09, '#f5f7f2') + r(X(0), Y(-1970), 900 * .105, 1970 * .09, '#f5f7f2') + r(X(100), Y(2600), 6400 * .105, 400 * .09, '#faf3e4')

def frame_pavers(cx, fill=P, stroke='#7f8f86'):
    s = ''
    for dx in (-220, 220):
        for top in (2495, 2805):
            s += r(X(cx + dx - 150), Y(top), 300 * .105, 300 * .09, fill, stroke)
    return s

bd = text(40, 35, '1 · Piles, pads and heights', 21) + text(40, 62, 'Set-out plan · lawn = 0 · 16 timber piles in concrete, 5 step pits with no concrete', 13) + outline
for y in [300, 2510]:
    for x in d['main_pile_X_mm']:
        anchor = x in [62.5, 6537.5]
        bd += r(X(x - 175), Y(y - 175), 350 * .105, 350 * .09, 'none', '#9aa89f', '3 3') + r(X(x - 62.5), Y(y - 62.5), 125 * .105, 125 * .09, A if anchor else G)
for y in [-1925, -800]:
    for x in [175, 725]:
        bd += r(X(x - 62.5), Y(y - 62.5), 125 * .105, 125 * .09, G)
for cx in frames:
    bd += r(X(cx - 380), Y(2400), 760 * .105, 800 * .09, 'none', '#9aa89f', '3 3') + frame_pavers(cx)
bd += text(185, 133, 'Rebuilt strip: four ordinary piles', 12) + text(180, 169, 'Rear bearer back face Y−1970, centre −1925', 12) + text(180, 205, 'Middle bearer centre Y−800', 12)
bd += text(X(3300), Y(1400), 'Main deck: 12 piles on rows Y300 and Y2510 (orange = corner anchors)', 13, 'middle')
bd += text(X(3300), Y(3450), 'Five step pits in the bays, four pavers each, clear of the pile holes', 12, 'middle')
bd += text(790, 105, 'Heights · lawn = 0', 14)
Z = lambda z: 340 - z * .38
bd += r(790, Z(0), 280, 100, S) + line(790, Z(0), 1070, Z(0))
bd += r(800, Z(500), 130, 12, T) + r(810, Z(468), 110, 53.2, G) + r(820, Z(328), 90, 53.2, T) + r(850, Z(187), 30, 71, T)
bd += r(950, Z(250), 100, 12, T) + r(955, Z(218), 85, 53.2, T) + r(960, Z(78), 75, 6, '#fff') + r(960, Z(60), 75, 15, P) + r(955, Z(20), 85, Z(-130) - Z(20), C, '#9aa89f', '3 3')
bd += text(800, 134, 'Deck +500', 13) + text(950, 225, 'Step +250', 13) + text(800, 370, '0 · lawn / path', 12) + text(1000, Z(95), 'H4 packer + DPC', 10) + text(1000, Z(40), 'paver top +45…+75', 10) + text(1000, Z(-60), 'GAP7, tamped', 10)
bd += text(790, 490, '16 timber piles, one pour', 14) + text(790, 516, '12 ordinary · 450 deep, square or 400 auger', 12) + text(790, 538, '4 corner anchors · 900 deep', 12)
bd += text(790, 572, '5 step pits, no concrete', 14) + text(790, 598, 'pit 760×800, GAP7, off the pile holes', 12) + text(790, 620, '4 pavers 300×300 per frame', 12)
bd += text(40, 635, 'Main pile X: 62.5 / 1357.5 / 2652.5 / 3947.5 / 5242.5 / 6537.5 · rows Y300 / Y2510. Pile tops cut to a string.', 13)
bd += text(40, 666, 'Step frames centred ' + ' / '.join(str(x) for x in frames) + ' · pavers 220 mm each side of those · pits after the deck frame is up.', 12)
bd += text(40, 697, 'Nothing is poured level. Piles are cut to a string. Pavers are tapped to a tape off the deck rim. An H4 offcut takes up a low paver.', 12)
bd += text(40, 730, f'One pour: about {cv["main_net_m3"]:.2f} m³. Mini-mix 1.2 m³, or {cv["bags_20kg_buy"]} bags of 20 kg if the truck cannot get in.', 12)
bd += text(40, 763, 'Pile symbols show position only. The corner anchor detail is an assumption listed at the end of the guide.', 12)
svg('piles', 'Sixteen timber piles with four corner anchors, and five step pits between the pile holes; deck 500, step 250', bd)

bd = text(40, 35, '2 · Framing sizes and board direction', 21) + text(40, 62, '140×45 SG8 · H3.2 main and rebuilt · H4 step in five 900 mm frames', 13) + outline
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
for cx in frames:
    x0 = cx - 450
    for y in (2600, 2910):
        bd += r(X(x0), Y(y), 900 * .105, 90 * .09, T)
    for dx in (-450, 0, 450):
        bd += r(X(cx + dx - 22.5), Y(2690), 45 * .105, 220 * .09, G)
    bd += r(X(cx - 70), Y(2555), 140 * .105, 45 * .09, A)
    bd += frame_pavers(cx, 'none', '#7f8f86')
bd += text(215, 125, 'All boards run along X →', 19) + text(215, 158, 'Deck + rebuilt strip + step', 13)
for i, tx in enumerate(['Deck: 17 joists of 2510', 'Flush, then 437 centres', 'Doubled joist centred at 3956', '2.21 m span, bearers Y300/Y2510', 'Plain rims Y0 and Y2555', '', 'Rebuilt: 3 joists of 1880', '2 blocks, cut at 380', '', 'Step: 5 frames of 900', '3 crosspieces each, 4 pavers', 'Orange tie on the bearer face']):
    bd += text(790, 250 + i * 26, tx, 13)
bd += text(40, 635, 'Bearers: 2×140×45 nailed (F1). Joists sit on the bearers and are nailed through the rims. No blocking in the deck.', 13)
bd += text(40, 666, 'Step frames are separate. Do not cut a 6.6 m rail. Assemble each 900 mm frame on its pavers.', 13)
bd += text(40, 697, 'Boards cross a 395 mm gap between frames. Deck butts land on the doubled joist at 3956.', 13)
bd += text(40, 730, 'Cuts: deck 17×2510, rebuilt 3×1880 and 2×380; step 20×900, crosspieces 15×220, ties 5×250.', 13)
bd += text(40, 763, 'Rear line Y−1970 is the rebuilt bearer back face; its centre is −1925. The old bearer is not reused.', 12)
svg('framing', 'Framing plan: seventeen main joists, three rebuilt joists, two blocks, and five short H4 step frames on pavers, all boards along X', bd)

bd = text(40, 35, '3 · Fixings and step section at a paver', 21) + text(40, 65, 'Each frame bears on four pavers and is screwed to the bearer. The tie is a hold-down, not just a sideways cleat.', 13)
Zs = lambda z: 560 - z * .5
Ys = lambda y: 60 + (y - 2250) * .6
bd += r(Ys(2250), Zs(0), (3250 - 2250) * .6, Zs(-500) - Zs(0), S) + line(Ys(2250), Zs(0), Ys(3250), Zs(0), '#52675b')
bd += r(Ys(2400), Zs(20), 800 * .6, Zs(-150) - Zs(20), C, '#9aa89f')
for yc in [2645, 2955]:
    bd += r(Ys(yc - 150), Zs(60), 300 * .6, 40 * .5, P) + r(Ys(yc - 45), Zs(78), 90 * .6, 18 * .5, '#c4a574', '#9aa89f')
bd += r(Ys(2335), Zs(-100), 350 * .6, 350 * .5, 'none', '#9aa89f', '4 3') + r(Ys(2447.5), Zs(187), 125 * .6, (187 + 350) * .5, 'none', '#9aa89f', '4 3')
bd += r(Ys(2465), Zs(328), 90 * .6, 140 * .5, T) + r(Ys(2250), Zs(468), 305 * .6, 140 * .5, G) + r(Ys(2555), Zs(468), 45 * .6, 140 * .5, T) + r(Ys(2250), Zs(500), 350 * .6, 32 * .5, T)
bd += r(Ys(2555), Zs(328), 45 * .6, 250 * .5, A)
bd += r(Ys(2600), Zs(218), 90 * .6, 140 * .5, T) + r(Ys(2690), Zs(218), 220 * .6, 140 * .5, G) + r(Ys(2910), Zs(218), 90 * .6, 140 * .5, T) + r(Ys(2600), Zs(250), 400 * .6, 32 * .5, T)
bd += line(Ys(2555), Zs(258), Ys(2555) - 18, Zs(258), '#324c42') + line(Ys(2555), Zs(148), Ys(2555) - 18, Zs(148), '#324c42')
bd += line(Ys(2600), Zs(148), Ys(2600) + 18, Zs(148), '#324c42') + line(Ys(2600), Zs(178), Ys(2600) + 18, Zs(178), '#324c42')
bd += text(Ys(2300), Zs(530), 'Deck +500', 12) + text(Ys(2700), Zs(280), 'Step +250', 12) + text(Ys(3010), Zs(85), 'H4 packer + DPC', 10) + text(Ys(3010), Zs(45), 'paver 300×300, top +45…+75', 10) + text(Ys(3010), Zs(-60), 'GAP7 pit, tamped', 10) + text(Ys(2300), Zs(-20), '0 · lawn', 11)
bd += text(Ys(2300), Zs(-300), 'pile footing at another X', 10) + text(Ys(2560), Zs(-280), 'firm ground', 11)
bd += text(Ys(2395), Zs(260), 'bearer', 11) + text(Ys(2460), Zs(560), 'joist / rim', 11) + text(Ys(2520), Zs(70), 'tie', 11)
bd += text(680, 150, 'F8 · Rail on its paver', 16) + text(680, 178, 'No fixing into the paver', 13) + text(680, 204, 'H4 offcut packer, screwed to the rail', 13) + text(680, 228, 'Frame top 250 mm below the rim', 13)
bd += text(680, 268, 'F5 · Tie, one per frame', 16) + text(680, 296, '250 mm H4 on the bearer face', 13) + text(680, 320, '4×14g×100 into the bearer, 2 into the rail', 13) + text(680, 344, f'About {abs(sc["liftoff_tie_ULS_kN"]):.1f} kN if the far paver lifts', 13)
bd += text(680, 384, 'Frame rail screen', 16) + text(680, 412, f'{sc["double_rail_max_M_ULS_kNm"]:.2f} of {sc["double_rail_bending_screen_capacity_kNm"]:.2f} kNm ({sc["double_rail_utilisation"]*100:.0f}%)', 13) + text(680, 436, f'near paver then {sc["liftoff_paver_ULS_kN"]:.1f} kN, {sc["liftoff_paver_bearing_kPa"]:.0f} kPa', 13)
bd += text(40, 860, 'F1: 90×4 SS nails for bearers and the short step rails. F2: 4×100×4 SS skew nails per pile.', 12)
bd += text(40, 888, 'F3: two 100×4 per joist end and per crosspiece end. F4: skew nails plus two 14g×100 screws on each rebuilt joist.', 12)
bd += text(40, 916, 'F6: two M12×120 SS coach bolts at X200/700. F7: four corner anchor kits, checked against a double bearer.', 12)
bd += text(40, 944, 'Before buying: measure the sill, the cladding, the lawn fall and the sea-spray zone, and call beforeUdig.', 12)
bd += text(40, 972, 'Drawn at a paver. The pile footing is at another X and does not share ground with the step pit.', 12)
svg('fixings', 'Section at a step paver: short H4 frame on pavers, tie screwed to the bearer as a hold-down, fixing schedule F1 to F8', bd, h=1000)
