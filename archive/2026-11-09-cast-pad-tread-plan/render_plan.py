"""Render the single current plan, CSV and three drawings from design.json."""
from pathlib import Path
from html import escape as E
import json,csv,io,re
root=Path(__file__).resolve().parents[1];d=json.loads((root/'design.json').read_text())
cv=d['concrete_geometry_only'];sc=d['screens'];t=d['tread'];pads=d['tread_pad_X_mm'];cleats=t['cleat_X_mm']
# (item, quantity, supplier, unit price basis, line total NZD incl GST, posted|allowance, url)
rows=[
 ('Main and rebuilt framing 140×45 H3.2 SG8','100.8 m: 6×7.2 m, 8×6.0 m, 1×4.2 m, 1×3.0 m, 1×2.4 m','NZ Timber (wet SG8)','$6.84/m',689.47,'posted','https://www.nztimber.net.nz/shop/p/150x50-140x45-h32-sg8-wt-rad-framing-1-metre'),
 ('Tread framing 140×45 H4 SG8','31.8 m: 4×7.2 m, 1×3.0 m','Mitre 10 / ITM / PlaceMakers, price in store','allowance $19/m; quote',604.20,'allowance','https://www.mitre10.co.nz/shop/building-hardware/timber/structural-framing/structural-framing/c/RF7340'),
 ('Decking 88×32 H3.2 pine','270 m allowance (263 m laid): 39×4.2 m + 33×3.0 m','Warehouse Building Supplies','$2.99/m',807.30,'posted','https://www.warehousebuildingsupplies.co.nz/shop/timber-decking-merch-grade-30/106672-deck-merch-h32-100x4088x32-smthrandom-30605'),
 ('Ordinary piles 125×125 H5, 750 mm','12','Mitre 10','$24.35 each',292.20,'posted','https://www.mitre10.co.nz/shop/pine-products-125x125-house-pile-h5-treated-750mm/p/2053020'),
 ('Anchor piles 125×125 H5, 1.2 m','4 (section and length to confirm with builder)','Mitre 10','$39.00 each',156.00,'posted','https://www.mitre10.co.nz/shop/pine-products-125x125-house-pile-h5-treated-1200mm/p/2053022'),
 ('Anchor pile fixing kits, LUMBERLOK 12 kN stainless (12KNH)','4','Bunnings','$84.93 each',339.72,'posted','https://www.bunnings.co.nz/lumberlok-12kn-pile-fixing-high-corrosion-stainless-steel-12knh_p0827939'),
 ('Ready-mix concrete 25 MPa, small load','1.6 m³ ordered for a 1.35 m³ pour: 16 pile holes + 6 pad bases','Firth / Allied mini-mix, quote','guide $280–450/m³ + small-load fee',900.00,'allowance','https://auckland-concrete-driveways.pages.dev/concrete-costs-per-cubic-metre/'),
 ('Bagged high-strength concrete 20 kg','18 bags for the six pad tops (16 needed)','Bunnings (Cemix)','$11.24/bag basis',202.32,'posted','https://www.bunnings.co.nz/cemix-20kg-multicrete_p0232228'),
 ('D12 reinforcing bar 6 m','1 bar, cut into 12×300 mm dowels','Bunnings','$16.54',16.54,'posted','https://www.bunnings.co.nz/summit-steel-wire-d12-x-6m-grade-300e-reinforcing-bar_p0252359'),
 ('Boxing for six pad tops','10 m of 200×25 rough-sawn H3.2, or ply offcuts; reusable','Any merchant','allowance',50.00,'allowance',''),
 ('Decking screws 10g×75 316 stainless','3×500 (1254 needed, 1500 bought)','Mitre 10 (Building King)','$219/500',657.00,'posted','https://www.mitre10.co.nz/shop/building-king-decking-screw-316-stainless-steel-bronze-etch-10g-x75mm-pack-of-500/p/2011345'),
 ('Framing nails 316 stainless jolt head','4×2 kg: three of 90×4 (bearer and rail plies), one of 100×4 (joists, rims, skew nails)','Bunnings (NZ Nails)','$119/2 kg basis',476.00,'posted','https://www.bunnings.co.nz/nz-nails-100-x-4mm-5kg-316-stainless-steel-jolt-head-nail_p0383292'),
 ('Rebuilt hold-downs, LUMBERLOK SSCPC40 stainless + screws','6 cleats (3 pairs); 12×14g×35 and 12×14g×75 SS screws','MiTek stockist / Anzor','allowance',60.00,'allowance','https://anzor.co.nz/building-brackets-timber-connectors/lumberlok-timber-connectors/purlin-cleats/cpc40-ss-concealed-purlin-cleat-lumberlok'),
 ('Rim tie bolts M12×120 316 + 50 mm washers','2 bolts, 4 washers','Fastener merchant','allowance',20.00,'allowance',''),
 ('Tread tie-cleat screws 14g×100 316 Type 17','25-pack (12 needed)','Mitre 10 (Ecko T-REX17)','$34.98/25',34.98,'posted','https://www.mitre10.co.nz/shop/ecko-t-rex17-batten-screws-14g-x-100mm-pack-of-25-316-stainless-steel/p/384103'),
 ('Pad brackets 316 stainless angle, about 90×90×65×3','12 (one per rail per pad)','Fastener merchant / Anzor','allowance $8 each',96.00,'allowance',''),
 ('Sleeve anchors M10×75 316 stainless','12 needed; 50-pack listed, or singles from a fastener merchant','Mitre 10 (Bremick)','$198/50',198.00,'posted','https://www.mitre10.co.nz/shop/bremick-sleeve-anchors-hex-10-x-75mm-stainless-steel-316/p/361625'),
 ('Bracket screws 14g×35 316','24','Fastener merchant','allowance',15.00,'allowance',''),
 ('DPC Supercourse 500, 150 mm×30 m','1 roll (pile tops and pad tops)','Bunnings','$27.42',27.42,'posted','https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
 ('Plastic packers 75 mm','1.5 mm×200 pack, plus a 100 pack of 6 mm','Bunnings (Titan)','$26.45 + allowance $25',51.45,'posted','https://www.bunnings.co.nz/titan-1-5-x-75mm-200-piece-blue-window-packers_p0647619'),
 ('Cut-end preservative','1 L, for every saw cut in treated timber','Any merchant','allowance',40.00,'allowance',''),
]
posted=round(sum(r[4] for r in rows if r[5]=='posted'),2);allow=round(sum(r[4] for r in rows if r[5]=='allowance'),2);total=round(posted+allow,2)
steps=[
 'Builder brief (one visit). Check the house cladding gap, door threshold and weatherproofing against the actual door and cladding; confirm the 500/250 mm datums, the four corner anchors and the pad bracket hardware. Ask the council whether the deck is consent-exempt under Schedule 1 (a fall of less than 1.5 m usually is).',
 'Set out. String the 6600×2600 outline, the 900×1970 rebuilt strip and the 400 mm tread. Mark 16 pile holes and 6 pad holes from Drawing 1. Keep the lawn and path at their present levels.',
 'Dig. Ordinary pile holes 350×350×450 deep, four corner anchor holes 350×350×900, six pad holes 350×500×450. The two end pad holes may run into the corner pile holes; that is fine. Dig to firm natural ground, not topsoil.',
 'Pour 1. Stand all 16 piles long and plumb, brace them, and pour the ready-mix into every pile hole and pad base at once (about 1.35 m³). Pile holes to about 100 mm below ground; pad bases also to about 100 mm below ground. Push two 300 mm D12 dowels into each pad base, sticking up 150 mm. Nothing in this pour needs to be level.',
 'Cut the piles. After the concrete has set, string a line at +187 mm (garden = 0) along each pile row, mark every pile and cut square. Treat the cuts. Lay DPC on each pile top.',
 'Pour 2, the six pad tops. Follow "Levelling the six pads" in the Foundations section. Target +77 mm, never higher. Strip the boxes after two days.',
 'Bearers. Nail up the two 6.6 m main double bearers and two 0.9 m rebuilt double bearers (F1). Seat them on the piles at Y300 and Y2510, and at Y−1925 and Y−800, and skew-nail (F2). Fit the four anchor kits to the maker\'s sheet. Replace the old rear bearer; do not reuse it.',
 'Joists and rims. 17 main joists of 2510 mm at the centres in the set-out table, with the pair at 3933/3978. Three rebuilt joists of 1880 mm, two blocks over the Y−800 bearer and the three SSCPC40 hold-down pairs at the rear (F4). Nail the plain 6.6 m rims at Y0 and Y2555 and the 900 mm rebuilt rims. Two M12 rim ties at the rebuilt/main junction (F6).',
 'Tread tie cleats. Screw three 250 mm H4 cleats to the outside face of the front bearer at X1000, 3300 and 5600, bottoms at +78, with two 14g×100 screws each (F5).',
 'Tread frame. Nail up the two 6.6 m double rails (F1 pattern). Stand the inner rail against the cleats, fit the 17 crosspieces of 220 mm at the joist centres, then the outer rail. Sit the frame on DPC and packers on the six pads, check it against the string, then fix one bracket and anchor per rail per pad (F7) and screw the cleats to the inner rail from under the deck.',
 'Boards. Lay the 32 mm boards along X on the main deck, rebuilt strip and tread. Butt ends on the paired members at 3955. Use the board supplier\'s gaps and two screws per board per joist. Treat every cut. Finish lawn, path and garden clear of all timber.',
]
fixings=[
 ('F1','Double bearers and double tread rails','90×4 stainless nails, two rows at 250 mm centres, alternating faces. Same pattern for the four H4 tread rail plies.'),
 ('F2','Ordinary pile to bearer','Four 100×4 stainless skew nails at each pile.'),
 ('F3','Joists, rims, blocks, crosspieces','NZS 3604 Table 7.5 nailing; two 100×4 stainless per joist end into the rim, three per crosspiece end into the 90 mm rail.'),
 ('F4','Rebuilt rear hold-downs','Three genuine SSCPC40 pairs, each cleat with two 14g×35 into the joist and two 14g×75 into the bearer. Screened uplift 1.92 kN against 2.69 kN per pair.'),
 ('F5','Tread tie cleats (lateral only)','Three 250 mm 140×45 H4 cleats on the front bearer face at X1000/3300/5600, bottom +78. Two 14g×100 stainless screws into the bearer and two into the inner rail. They stop the tread sliding; they carry no weight.'),
 ('F6','Rebuilt to main rim tie','Two M12×120 stainless bolts through the adjacent rims at X200/700, Z398, 50 mm washers both sides.'),
 ('F7','Tread rails to pads, and corner anchors','One 316 angle bracket per rail per pad on the crosspiece side: one M10×75 sleeve anchor into the pad top at least 100 mm from any edge, two 14g×35 into the rail. Four corner anchor piles with complete 12 kN kits. Builder to confirm both details; the bracket is a sensible ordinary detail, not a rated connection.'),
]
jc=', '.join(str(int(x)) if float(x).is_integer() else str(x) for x in d['main_joist_centres_mm'])
md=f'''# Deck and pad-supported tread

9 November 2026 · One current plan and three drawings. Working proposal for the builder brief: the tread now sits on six concrete pads and is only tied sideways to the deck. Still to confirm with the builder: the four corner anchor piles and the pad bracket hardware. No paid designer and no builder inspections during construction are assumed. This is not construction approval.

## What changed on 9 November

The old plan hung the tread's inner rail from seven cleats and 28 M12 bolts on the deck rim. That was the hardest, least verified part of the job. Both tread rails now bear on six concrete pads, the rails are doubled so they span the pad spacing with margin, and three short cleats on the front bearer stop the tread sliding. The front rim is a plain 140×45. The old plan is kept in archive/.

## Agreed layout

| Part | Decision |
|---|---|
| Main deck | 6600×2600 mm, surface about 500 mm above the garden. Double 140×45 H3.2 SG8 bearers on timber piles at Y300 and Y2510; 140×45 joists seated on the bearers, 2.21 m span (table limit 2.35 m at 450 centres). |
| Main joists | 17 members: 16 lines at 437 mm centres with the line at 3955 replaced by a pair at 3933/3978 to carry board butt joints. Plain rims at Y0 and Y2555; no mid-span blocking needed (rims within 300 mm of the bearers). |
| Rebuilt strip | 900×1970 mm. Old bearer replaced. Two 900 mm double bearers at Y−1925 and Y−800, three separate 1880 mm joists, two blocks, three hold-down pairs at the rear. No joists run through into the main deck. |
| Tread | 6600×400 mm, surface 250 mm. Two double 140×45 H4 SG8 rails (90 mm wide) at Y2600–2690 and Y2910–3000, 17 crosspieces of 220 mm, all on six concrete pads. Three tie cleats to the deck bearer. |
| Boards | 32 mm pine, all along X, on the main deck, rebuilt strip and tread. |
| Finish | Natural treated pine, plain front rail, no handrails, lawn and path kept at their present levels. |

Set-out, X from the left edge in mm. Joist and crosspiece centres: {jc}. Main piles: 62.5, 1357.5, 2652.5, 3947.5, 5242.5, 6537.5 on rows Y300 and Y2510. Rebuilt piles: X175 and X725 on Y−1925 and Y−800. Tread pads: {', '.join(str(p) for p in pads)}, each pad top 300×450 covering Y2575–3025. Tie cleats: {', '.join(str(c) for c in cleats)}.

Heights, garden = 0: deck boards top +500, joist and rim top +468, bearer top +328, pile top +187 (DPC under the bearer). Tread boards top +250, rail top +218, rail bottom +78, DPC, pad top +77.

## Three drawings

[1 · Piles, pads and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixings and tread section](docs/drawings/fixings.svg)

## Foundations

16 timber piles: 12 ordinary (holes 350×350, 450 deep) and 4 corner anchors (holes 350×350, 900 deep, conditional on the builder confirming the bracing and the 12 kN kits). Six tread pads, each under both rails: base 350×500 from 450 to 100 below ground, then a 300×450 top up to +77. The pads sit between the front pile holes; the two end pad holes may join the corner pile holes.

Concrete, planning figures: pour 1 is about 1.35 m³ of ready-mix (piles and pad bases), order 1.6 m³. Pour 2 is the six pad tops, about 0.14 m³, 16 bags of 20 kg; buy 18. Nothing in pour 1 needs to be level. Only the six pad tops need to be level with each other, and the pile tops are cut to a string after the pour.

### Levelling the six pads

This is the one fiddly task, so it is set up to be forgiving.

1. Pour the pad bases rough, about 100 mm below ground, with two D12 dowels sticking up out of each. Let them set overnight.
2. Make six open boxes with an inside size of 300×450 mm and about 200 mm tall, screwed together so they come apart later.
3. Set the level once. Drive a peg beyond each end of the tread and mark +77 on both from the garden datum with a water level (a clear hose) or a laser. Pull a tight string between the marks along the pad line.
4. Sit each box over its dowels and pack under the corners until the box top is level both ways and sits 2–3 mm below the string. Peg or screw it so it cannot move. Low is fine, high is not: packers fix low.
5. Fill with the bagged mix, rod it, and screed off flush with the box top using a straight offcut. The box top is the level, so no finishing skill is needed.
6. Strip the boxes after two days. When the tread frame goes on, take up the last few millimetres with plastic packers under the DPC, then fix the brackets.

## Materials and costs

[Download shopping CSV](docs/shopping-list.csv). NZD incl GST. Posted prices were read from retailer pages on 9 November 2026 and may change; items marked allowance have no posted price and need a quote. No supplier has been contacted and nothing has been bought.

| Item | Quantity | Source | Price basis | Line |
|---|---|---|---|---|
'''
for item,qty,sup,basis,line,kind,url in rows:
 md+=f"| {item} | {qty} | {('['+sup+']('+url+')') if url else sup} | {basis if basis.startswith('allowance') else basis+(' (allowance)' if kind=='allowance' else '')} | ${line:,.2f} |\n"
md+=f'''
**Posted-price items ${posted:,.2f} + allowances ${allow:,.2f} = about ${total:,.0f} incl GST.** Delivery, tool hire and skip or soil disposal are extra. If 140×45 H4 is hard to get, 150×50 H4 SG8 works for the tread with the pad tops set 10 mm lower (+67). If the builder confirms the site is outside the sea-spray zone, hot-dip galvanised nails and kits are allowed by NZS 3604 and cost about a quarter of stainless.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:md+=f"| {a['count']}×{a['stock_mm']} | "+' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm'])+' |\n'
md+=f"\nMain and rebuilt: {d['main_stock_lm']} m bought, {d['main_installed_lm']} m used. 6600 = 4 bearer plies + 2 rims; 2510 = 17 joists; 900 = 4 rebuilt bearer plies + 2 rebuilt rims; 382.5 = 2 blocks; 1880 = 3 rebuilt joists.\n\n| 140×45 H4 stock | Cuts, mm |\n|---|---|\n"
for a in d['H4_stock_allocations']:md+=f"| {a['count']}×{a['stock_mm']} | "+' + '.join(str(c) for c in a['cuts_mm'])+' |\n'
md+=f'''
Tread: {d['H4_stock_lm']} m bought, {d['H4_installed_lm']} m used. 6600 = 4 rail plies; 220 = 17 crosspieces; 250 = 3 tie cleats. Allow 4 mm per saw cut and 5 mm end trim. Boards at 88 mm with about 5 mm gaps: 28 rows main, 22 rebuilt, 5 tread; 1254 screw positions, buy 1500.

## Fixing schedule

| ID | Joint | Detail |
|---|---|---|
'''
for f in fixings:md+='| '+' | '.join(f)+' |\n'
md+=f'''
## Before building

- Builder to confirm the four corner anchor piles (section, depth, 12 kN kits) and the whole bracing path. No ground lowering is planned.
- Builder to confirm the pad bracket and anchor detail (F7). Screens: double rail bending {sc['double_rail_max_M_ULS_kNm']:.2f} kNm against {sc['double_rail_bending_screen_capacity_kNm']:.2f} kNm, {sc['double_rail_utilisation']*100:.0f}% used; largest pad reaction {sc['max_pad_reaction_ULS_kN']:.1f} kN, about {sc['pad_bearing_kPa_on_base']:.0f} kPa on the pad base against 100 kPa assumed ground.
- Check house cladding clearance, door threshold height and weatherproofing against the actual door and cladding. Do not apply one universal gap.
- Confirm H4 140×45 lengths and stainless fasteners are in stock before ordering boards. Keep the one builder review before work; later checks are by the owner.
- The 250 mm step rise is the owner's choice and is above the D1/AS1 stair limit; no access compliance is claimed.

## Build sequence

'''
for i,s in enumerate(steps,1):md+=f'{i}. {s}\n'
md+=f'''
## Evidence and limits

Northpine wet-service tables: 140×45 SG8 at 450 centres spans 2.35 m; NZS 3604 Table 7.2 allows an 1100 mm cantilever against the rebuilt 755 mm; §7.1.2 allows rims within 300 mm of a support to replace blocking. Sources: [Northpine tables](https://www.northpine.co.nz/span-tables), [MiTek LUMBERLOK data](https://mitek.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf), [BRANZ Bulletin 611 low bearers on concrete](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf), [H4 SG8 product information](https://www.fwp.co.nz/wp-content/uploads/2023/11/Building-Products-Information-Waipapa-Pine-H4-H5-H6-MG-RS-SG8-Framing-Timber.pdf).

Reproduce with `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`; data in design.json. The rail screen uses a factored 2.7 kN stair point load at any position with board-edge eccentricity on a continuous double rail over the six pads; it is a member demand screen, not a full connection or foundation verification. Both rails must be continuous 6600 mm. Firm natural ground at 100 kPa is a planning assumption. Historical material is in archive/.
'''
(root/'CURRENT_DESIGN.md').write_text(md)
b=io.StringIO(newline='');w=csv.writer(b,lineterminator='\n');w.writerow(['Item','Quantity','Supplier','Price basis','Line NZD incl GST','Posted or allowance','Source']);w.writerows(rows);w.writerow(['TOTAL','','','',total,f'posted {posted} + allowances {allow}','']);(root/'SHOPPING_LIST.csv').write_text(b.getvalue())
inline=lambda x: re.sub(r'`([^`]+)`',r'<code>\1</code>',re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',E(x))))
parts=[];lines=md.splitlines();i=0
while i<len(lines):
 l=lines[i]
 if not l.strip():i+=1;continue
 if l.startswith('#'):
  level=len(l)-len(l.lstrip('#'));tt=l[level:].strip();slug=re.sub(r'[^a-z0-9]+','-',tt.lower()).strip('-');parts.append(f'<h{level} id="{slug}">{inline(tt)}</h{level}>');i+=1
 elif l.startswith('|'):
  block=[]
  while i<len(lines) and lines[i].startswith('|'):block.append(lines[i]);i+=1
  parts.append('<div class="table-wrap"><table>')
  for j,row in enumerate(block):
   if j==1:continue
   tag='th' if j==0 else 'td';parts.append('<tr>'+''.join(f'<{tag}>'+inline(c.strip())+f'</{tag}>' for c in row.strip().strip('|').split(' | '))+'</tr>')
  parts.append('</table></div>')
 elif l.startswith('- ') or re.match(r'^\d+\. ',l):
  ordered=bool(re.match(r'^\d+\. ',l));tag='ol' if ordered else 'ul';parts.append('<'+tag+'>')
  while i<len(lines) and ((bool(re.match(r'^\d+\. ',lines[i])) if ordered else lines[i].startswith('- '))):parts.append('<li>'+inline(re.sub(r'^(?:\d+\. |- )','',lines[i]))+'</li>');i+=1
  parts.append('</'+tag+'>')
 else:
  p=[]
  while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ')) and not re.match(r'^\d+\. ',lines[i]):p.append(lines[i]);i+=1
  parts.append('<p>'+inline(' '.join(p))+'</p>')
body='\n'.join(parts)
a=body.index('<h2 id="three-drawings">');bb=body.index('<h2 id="foundations">',a)
body=body[:a]+'''<h2 id="three-drawings">Three drawings</h2><div class="tabs" role="tablist" aria-label="Drawings"><button id="tab-piles" role="tab" aria-controls="drawing-panel" aria-selected="true" data-view="piles">1 · Piles, pads &amp; heights</button><button id="tab-framing" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="framing">2 · Framing</button><button id="tab-fixings" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="fixings">3 · Fixings &amp; section</button></div><div id="drawing-panel" role="tabpanel" aria-labelledby="tab-piles"><div id="drawing"></div><p id="drawing-caption" class="caption"></p></div><p class="note">Download: <a href="drawings/piles.svg">piles</a> · <a href="drawings/framing.svg">framing</a> · <a href="drawings/fixings.svg">fixings</a></p>'''+body[bb:]
body=body.replace('href="docs/','href="').replace('archive/','<a href="https://github.com/MaxHogervorst/deck-design/tree/main/archive">archive/</a>')
html='''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="One current deck plan: pad-supported tread, framing, foundations, fixings, pad levelling and a priced shopping list."><title>Deck and pad-supported tread · current plan</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">Auckland deck <span>09 / 11 / 2026 · ONE CURRENT PLAN</span></a><nav aria-label="Sections"><a href="#three-drawings">Drawings</a><a href="#levelling-the-six-pads">Pads</a><a href="#materials-and-costs">Materials</a><a href="#before-building">Builder brief</a><a href="#build-sequence">Build</a></nav><button id="print">Print</button></header><main id="main">'''+body+'''</main><footer><span>Current working plan · not construction approval</span><button id="copy-link">Copy link</button></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
(root/'site/index.html').write_text(html)
print('Rendered plan, CSV and page; posted',posted,'allowances',allow,'total',total)
# Three standalone drawings.
T='#cba773';G='#456b54';C='#d6dad7';S='#ece5d6';A='#af6b3c'
def r(x,y,w,h,fill,stroke='#52675b',dash=''):return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def line(x,y,x2,y2,stroke='#71847b',dash=''):return f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def text(x,y,tx,size=13,anchor='start'):return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{E(tx)}</text>'
def svg(name,title,bd,w=1100,h=800):
 out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}"><title>{E(title)}</title><style>text{{font-family:system-ui,sans-serif;fill:#21382f}}line{{stroke-width:1.5}}</style><rect width="{w}" height="{h}" fill="#fbfbf8"/>{bd}</svg>'
 (root/'site/drawings'/f'{name}.svg').write_text(out)
X=lambda x:55+x*.105;Y=lambda y:295+y*.09
outline=r(X(0),Y(0),6600*.105,2600*.09,'#f5f7f2')+r(X(0),Y(-1970),900*.105,1970*.09,'#f5f7f2')+r(X(0),Y(2600),6600*.105,400*.09,'#faf3e4')
# Drawing 1
bd=text(40,35,'1 · Piles, pads and heights',21)+text(40,62,'Set-out plan · garden = 0 · four corner anchors conditional on the builder brief',13)+outline
for y in [300,2510]:
 for x in d['main_pile_X_mm']:
  anchor=x in [62.5,6537.5]
  bd+=r(X(x-175),Y(y-175),350*.105,350*.09,'none','#9aa89f','3 3')+r(X(x-62.5),Y(y-62.5),125*.105,125*.09,A if anchor else G)
for y in [-1925,-800]:
 for x in [175,725]:bd+=r(X(x-62.5),Y(y-62.5),125*.105,125*.09,G)
for x in pads:bd+=r(X(x-175),Y(2550),350*.105,500*.09,'none','#9aa89f','3 3')+r(X(x-150),Y(2575),300*.105,450*.09,C)
bd+=text(185,133,'Rebuilt strip: four ordinary piles',12)+text(180,169,'Rear bearer back face Y−1970, centre −1925',12)+text(180,205,'Middle bearer centre Y−800',12)
bd+=text(X(3300),Y(1400),'Main deck: 12 piles on rows Y300 and Y2510',13,'middle')
bd+=text(X(3300),Y(3250),'Six tread pads 300×450 (dashed = hole 350×500), between the front pile holes',12,'middle')
bd+=text(790,105,'Heights · garden = 0',14)
Z=lambda z:340-z*.38
bd+=r(790,Z(0),280,100,S)+line(790,Z(0),1070,Z(0))
bd+=r(800,Z(500),130,12,T)+r(810,Z(468),110,53.2,G)+r(820,Z(328),90,53.2,T)+r(850,Z(187),30,71,T)
bd+=r(950,Z(250),100,12,T)+r(955,Z(218),85,53.2,T)+r(960,Z(77),75,67,C)
bd+=text(800,134,'Deck +500',13)+text(950,225,'Tread +250',13)+text(800,370,'0 · lawn / path',12)+text(1000,Z(140),'pad top +77',11)
bd+=text(790,490,'16 timber piles',14)+text(790,516,'12 ordinary · holes 350×350×450',12)+text(790,538,'4 corner anchors · holes 350×350×900',12)
bd+=text(790,572,'6 tread pads',14)+text(790,598,'base 350×500, −450 to −100',12)+text(790,620,'top 300×450, −100 to +77',12)
bd+=text(40,635,'Main pile X: 62.5 / 1357.5 / 2652.5 / 3947.5 / 5242.5 / 6537.5 · rows Y300 / Y2510.',13)
bd+=text(40,666,'Pad X: '+' / '.join(str(p) for p in pads)+' · pad top Y2575…3025. End pad holes may join the corner pile holes.',13)
bd+=text(40,697,'Only the six pad tops need levelling (+77, never higher). Pile tops are cut to a string at +187 after the pour.',13)
bd+=text(40,730,'Pour 1: ready-mix into all piles and pad bases, about 1.35 m³, order 1.6. Pour 2: 16–18 bags for the pad tops.',12)
bd+=text(40,763,'Pile symbols show position only; the anchor pile size and kit are confirmed in the builder brief.',12)
svg('piles','Sixteen timber pile positions, four conditional corner anchors, six tread pads between the front pile holes; deck 500, tread 250, pad tops 77',bd)
# Drawing 2
bd=text(40,35,'2 · Framing sizes and board direction',21)+text(40,62,'140×45 SG8 · H3.2 main and rebuilt · H4 tread (double rails)',13)+outline
for y in [300,2510]:bd+=r(X(0),Y(y-45),6600*.105,90*.09,T)
for y in [-1925,-800]:bd+=r(X(0),Y(y-45),900*.105,90*.09,T)
for x in d['main_joist_centres_mm']:bd+=r(X(x-22.5),Y(45),45*.105,2510*.09,G)
for x in [22.5,450,877.5]:bd+=r(X(x-22.5),Y(-1925),45*.105,1880*.09,G)
for x in [45,472.5]:bd+=r(X(x),Y(-822.5),382.5*.105,45*.09,G)
for y,length in [(0,6600),(2555,6600),(-1970,900),(-45,900)]:bd+=r(X(0),Y(y),length*.105,45*.09,T)
for x in cleats:bd+=r(X(x-70),Y(2555),140*.105,45*.09,A)
for y in [2600,2910]:bd+=r(X(0),Y(y),6600*.105,90*.09,T)
for x in d['main_joist_centres_mm']:bd+=r(X(x-22.5),Y(2690),45*.105,220*.09,G)
for x in pads:bd+=r(X(x-150),Y(2575),300*.105,450*.09,'none','#7f8f86','4 3')
bd+=text(215,125,'All boards run along X →',19)+text(215,158,'Main + rebuilt + tread',13)
for i,tx in enumerate(['Main: 17 joists of 2510','16 lines at 437 + butt pair 3933/3978','2.21 m span on bearers Y300/Y2510','Plain rims Y0 and Y2555','','Rebuilt: 3 joists of 1880','2 blocks over Y−800 bearer','','Tread: 2 double rails 6600','17 crosspieces of 220','3 tie cleats (orange) on bearer face','6 pads (dashed)']):bd+=text(790,250+i*26,tx,13)
bd+=text(40,635,'Bearers: 2×140×45 nailed (F1). Joists sit on the bearers and are nailed to the rims; no blocking in the main deck.',13)
bd+=text(40,666,'Tread rails: 2×140×45 H4 nailed like a bearer, inner Y2600–2690, outer Y2910–3000, continuous 6600.',13)
bd+=text(40,697,'Crosspieces at the joist centres so board screw lines run straight through. Butt line X3955 has pairs in deck and tread.',13)
bd+=text(40,730,'Cuts: main 17×2510, rebuilt 3×1880; tread rails 4×6600, crosspieces 17×220, cleats 3×250.',13)
bd+=text(40,763,'Rear line Y−1970 is the rebuilt bearer back face; its centre is −1925. The old bearer is not reused.',12)
svg('framing','Framing plan: seventeen main joists, three rebuilt joists, two blocks, two double H4 tread rails on six pads with seventeen crosspieces and three tie cleats, all boards along X',bd)
# Drawing 3: section through the front edge at a pad, looking along X.
bd=text(40,35,'3 · Fixing schedule and tread section at a pad',21)+text(40,65,'Tread bears on the pads; the cleats only tie it sideways. Builder confirms F7 hardware before anchors are drilled.',13)
Zs=lambda z:560-z*.5;Ys=lambda y:60+(y-2250)*.6
bd+=r(Ys(2250),Zs(0),(3150-2250)*.6,Zs(-500)-Zs(0),S)+line(Ys(2250),Zs(0),Ys(3150),Zs(0),'#52675b')
bd+=r(Ys(2550),Zs(-100),500*.6,350*.5,C)+r(Ys(2575),Zs(77),450*.6,177*.5,C)
bd+=line(Ys(2700),Zs(-250),Ys(2700),Zs(50),'#6b6b6b')+line(Ys(2900),Zs(-250),Ys(2900),Zs(50),'#6b6b6b')
bd+=r(Ys(2335),Zs(-100),350*.6,350*.5,'none','#9aa89f','4 3')+r(Ys(2447.5),Zs(187),125*.6,(187+350)*.5,'none','#9aa89f','4 3')
bd+=r(Ys(2465),Zs(328),90*.6,140*.5,T)+r(Ys(2250),Zs(468),305*.6,140*.5,G)+r(Ys(2555),Zs(468),45*.6,140*.5,T)+r(Ys(2250),Zs(500),350*.6,32*.5,T)
bd+=r(Ys(2555),Zs(328),45*.6,250*.5,A)
bd+=r(Ys(2600),Zs(218),90*.6,140*.5,T)+r(Ys(2690),Zs(218),220*.6,140*.5,G)+r(Ys(2910),Zs(218),90*.6,140*.5,T)+r(Ys(2600),Zs(250),400*.6,32*.5,T)
bd+=line(Ys(2690),Zs(100),Ys(2740),Zs(100),'#324c42')+line(Ys(2740),Zs(100),Ys(2740),Zs(77),'#324c42')+line(Ys(2910),Zs(100),Ys(2860),Zs(100),'#324c42')+line(Ys(2860),Zs(100),Ys(2860),Zs(77),'#324c42')
bd+=line(Ys(2555),Zs(258),Ys(2555)-18,Zs(258),'#324c42')+line(Ys(2555),Zs(118),Ys(2555)-18,Zs(118),'#324c42')+line(Ys(2600),Zs(148),Ys(2600)+18,Zs(148),'#324c42')+line(Ys(2600),Zs(178),Ys(2600)+18,Zs(178),'#324c42')
bd+=text(Ys(2300),Zs(530),'Deck +500',12)+text(Ys(2700),Zs(280),'Tread +250',12)+text(Ys(2700),Zs(55),'pad top +77 · DPC + packers',11)+text(Ys(2300),Zs(-20),'0 · garden',11)
bd+=text(Ys(2300),Zs(-300),'pile footing (dashed, other X)',10)+text(Ys(2560),Zs(-300),'pad base 350×500',11)+text(Ys(2560),Zs(-440),'to −450 on firm ground',11)
bd+=text(Ys(2395),Zs(260),'bearer',11)+text(Ys(2460),Zs(560),'joist / rim',11)+text(Ys(2520),Zs(70),'cleat',11)
bd+=text(680,150,'F7 · Pad brackets',16)+text(680,178,'316 angle, one per rail per pad',13)+text(680,204,'M10×75 SS sleeve anchor into pad top,',13)+text(680,228,'≥100 mm from edges; 2×14g×35 into rail',13)
bd+=text(680,268,'F5 · Tie cleats',16)+text(680,296,'3×250 mm H4 on bearer face',13)+text(680,320,'2×14g×100 into bearer, 2 into rail',13)+text(680,344,'Lateral only; no tread weight',13)
bd+=text(680,384,'Rail screen',16)+text(680,412,f"{sc['double_rail_max_M_ULS_kNm']:.2f} of {sc['double_rail_bending_screen_capacity_kNm']:.2f} kNm ({sc['double_rail_utilisation']*100:.0f}%)",13)+text(680,436,f"max pad reaction {sc['max_pad_reaction_ULS_kN']:.1f} kN",13)
bd+=text(40,860,'F1: 90×4 SS nails, two rows at 250, alternating faces, for bearers and tread rails. F2: 4×100×4 SS skew nails per pile.',12)
bd+=text(40,888,'F3: Table 7.5 nailing, 2 per joist end into rim, 3 per crosspiece end. F4: three SSCPC40 pairs at the rebuilt rear row.',12)
bd+=text(40,916,'F6: two M12×120 SS rim ties at X200/700, Z398. F7: four corner anchor kits (12 kN SS) and twelve pad brackets.',12)
bd+=text(40,944,'Builder brief also checks cladding clearance, door threshold, weatherproofing and the consent exemption.',12)
bd+=text(40,972,'Drawn at a pad; the pile and its footing (dashed) are at a different X and never share a hole except at the two ends.',12)
svg('fixings','Section through the deck front edge at a tread pad: deck on bearer and pile, tread double rails on the pad with brackets, tie cleat on the bearer face; fixing schedule F1 to F7',bd,h=1000)
