"""Render the single current build guide, CSV and three drawings from design.json."""
from pathlib import Path
from html import escape as E
import json,csv,io,re
root=Path(__file__).resolve().parents[1];d=json.loads((root/'design.json').read_text())
cv=d['concrete_geometry_only'];sc=d['screens'];t=d['tread'];pads=d['tread_pad_X_mm'];cleats=t['cleat_X_mm']
DATE='10 November 2026'
# (item, quantity, store, unit price basis, line total NZD incl GST, posted|estimate, url)
# posted = the price shown online for exactly that product on 10 November 2026.
# estimate = in-store or special-order item, or a stand-in product used as the price basis.
rows=[
 ('Framing 140×45 H3.2 SG8, wet (main deck and rebuilt strip)','100.8 m: 6×7.2 m, 8×6.0 m, 2×4.8 m','Bunnings','6.0 m $70.91 and 4.8 m $56.73 posted; 7.2 m not listed online, priced at the same $11.82/m',6*85.10+8*70.91+2*56.73,'estimate','https://www.bunnings.co.nz/140-x-45mm-sg8-h3-2-treated-green-radiata-timber-framing-6m_p0616262'),
 ('Step framing 140×45 H4 SG8 (rails, crosspieces, cleats)','31.8 m: 4 lengths of at least 6.7 m plus 3.0 m','Bunnings or Mitre 10, price in store','140×45 H4 has no online price at either store; basis Bunnings 150×50 SG8 H4 rough sawn $17.11/m (special order)',31.8*17.11,'estimate','https://www.bunnings.co.nz/150-x-50mm-sg8-h4-wet-sawn-treated-timber-per-linear-metre_p0276210'),
 ('Decking 88×32 H3.2 merch griptread, random lengths','270 m (263 m laid)','Bunnings, in store','$4.55/m posted; premium smooth is $6.65/m',270*4.55,'posted','https://www.bunnings.co.nz/88-x-32mm-merch-griptread-decking-random-lengths_p0307690'),
 ('Ordinary piles 125×125 H5, 750 mm','12','Bunnings','$21.04 each',12*21.04,'posted','https://www.bunnings.co.nz/125-x-125mm-0-75m-square-h5-anchor-pile_p0276396'),
 ('Corner anchor piles 125×125 H5, 1.2 m','4','Bunnings','$32.42 each',4*32.42,'posted','https://www.bunnings.co.nz/125-x-125mm-1-2m-square-h5-anchor-pile_p0276402'),
 ('Anchor pile fixing kits, LUMBERLOK 12KNH stainless','4','Bunnings','$84.93 each (galvanised 12KN is $37.89)',4*84.93,'posted','https://www.bunnings.co.nz/lumberlok-12kn-pile-fixing-high-corrosion-stainless-steel-12knh_p0827939'),
 ('Concrete for the 16 pile holes, about 0.99 m³','110 bags of 20 kg Cemix Multicrete (104 needed at 10 L a bag)','Bunnings','$11.24 a bag. A mini-mix truck for 1.2 m³ is usually cheaper and far less work; phone for a quote',110*11.24,'posted','https://www.bunnings.co.nz/cemix-20kg-multicrete_p0232228'),
 ('Concrete pavers 300×300, about 40 mm thick','12 (two per pad)','Mitre 10, price in store','Mitre 10 Urban Paving 300×300×40 has no online price; basis Bunnings WestStone 300×300×37 $10.83 (special order)',12*10.83,'estimate','https://www.mitre10.co.nz/shop/urban-paving-paver-300x300x40mm-natural/p/387387'),
 ('GAP7 basecourse for the six paver pits, about 0.32 m³','22 bags of 15 L','Bunnings','$9.79 a bag (Daltons 0-7 mm). A trailer scoop from a landscape yard is much cheaper',22*9.79,'posted','https://www.bunnings.co.nz/daltons-15l-0-7mm-sub-base-metal_p0237633'),
 ('Decking screws 10g×65 316 stainless','3×500 (1254 needed)','Bunnings','$116.00 per 500 (Building King)',3*116.00,'posted','https://www.bunnings.co.nz/decking-screw-65-x-10g-316-stainless-steel-500-pack_p0379643'),
 ('Framing nails 90×4 316 stainless jolt head','2×2 kg (bearer and rail plies, about 230 nails)','Mitre 10','$129.00 per 2 kg (Ecko)',2*129.00,'posted','https://www.mitre10.co.nz/shop/ecko-jolt-head-nails-90-x-4-0mm-2kg-316-stainless-steel/p/307864'),
 ('Framing nails 100×4 316 stainless jolt head','5×500 g (joists, rims, crosspieces, skew nails, about 210 nails)','Bunnings','$35.59 per 500 g (NZ Nails)',5*35.59,'posted','https://www.bunnings.co.nz/nz-nails-100-x-4mm-500g-316-stainless-steel-jolt-head-nail_p0383199'),
 ('Batten screws 14g×100 316 stainless','100 pack (12 for the step cleats, 12 for the hold-down cleats)','Bunnings','$77.05 per 100 (Bremick XTP)',77.05,'posted','https://www.bunnings.co.nz/bremick-xtp-14g-x-100mm-t40-stainless-steel-316-black-bugle-batten-100-pack_p0575899'),
 ('Hex screws 14g×35 stainless for the hold-down cleats','100 pack (12 needed)','Bunnings','$71.93 per 100 (LUMBERLOK)',71.93,'posted','https://www.bunnings.co.nz/lumberlok-17-14g-x-35mm-stainless-steel-hex-head-screws-100-pack_p0200542'),
 ('Hold-down cleats, LUMBERLOK SSCPC40 stainless','6 (three pairs)','Bunnings','$3.43 each',6*3.43,'posted','https://www.bunnings.co.nz/lumberlok-2-0-x-40mm-stainless-steel-concealed-purlin-cleat_p0277084'),
 ('Rim tie bolts M12×120 316 coach bolts, nuts and 50 mm square washers','2 bolts and nuts, 4 washers','Bunnings','$4.90 + $1.25 + 2×$3.54 per bolt',2*(4.90+1.25+2*3.54),'posted','https://www.bunnings.co.nz/zenith-m12-x-120mm-316-stainless-steel-coach-head-bolt-and-nut_p0236593'),
 ('DPC Supercourse 500, 150 mm×30 m','1 roll (pile tops and paver tops)','Bunnings','$27.42',27.42,'posted','https://www.bunnings.co.nz/thermakraft-supercourse-500-dpc-150mmx30m_p0207794'),
 ('Plastic packers, mixed 1 to 10 mm, 75 mm wide','1 pack of 600 (Titan)','Bunnings','$59.00',59.00,'posted','https://www.bunnings.co.nz/titan-75mm-600-piece-mixed-window-packers_p0647610'),
 ('Cut-end preservative, Metalex Green 1 L','1, brushed on every saw cut in treated timber','Bunnings','$66.00',66.00,'posted','https://www.bunnings.co.nz/metalex-1l-green-timber-preserve-44501_p0709374'),
]
rows=[(a,b,c,e,round(f,2),g,h) for a,b,c,e,f,g,h in rows]
posted=round(sum(r[4] for r in rows if r[5]=='posted'),2);est=round(sum(r[4] for r in rows if r[5]=='estimate'),2);total=round(posted+est,2)
padlist=', '.join(str(p) for p in pads);cleatlist=', '.join(str(c) for c in cleats)
steps=[
 'Before you start. Check where the deck top will sit against the house: it must stay below the door sill and clear of the bottom of the cladding by whatever the cladding maker asks for, so measure the real door and cladding, not a drawing. Call beforeUdig (0800 248 344) or check the property file for pipes and cables where the holes go. Agree the two datums with yourself: deck boards top at +500 and step boards top at +250 above the lawn.',
 'Set out. String the 6600×2600 outline, the 900×1970 rebuilt strip and the 400 mm step. Mark the 16 pile holes from Drawing 1. Do not mark the paver pits yet; they are dug after the deck frame is up. Leave the lawn and path at their present levels.',
 'Dig. Twelve ordinary pile holes 350×350 and 450 deep, four corner anchor holes 350×350 and 900 deep. Dig to firm natural ground, not topsoil; if a hole is still soft or wet at depth, stop and read the assumptions at the end.',
 f'Pour. Stand all 16 piles long and plumb, brace them with offcuts, and fill every hole to about 100 mm below ground in one go, about {cv["main_net_m3"]:.2f} m³. Order 1.2 m³ from a mini-mix truck, or mix {cv["bags_20kg_needed"]} bags of 20 kg (buy {cv["bags_20kg_buy"]}). Nothing in this pour needs to be level; the piles get cut later.',
 'Cut the piles. After the concrete has set, string a line at +187 mm (lawn = 0) along each pile row with a water level or laser, mark every pile and cut square. Brush preservative on the cuts. Lay a square of DPC on each pile top.',
 'Bearers. Nail up the two 6.6 m main double bearers and two 0.9 m rebuilt double bearers (F1). Seat them on the piles at Y300 and Y2510, and at Y−1925 and Y−800, and skew-nail (F2). Fit the four corner anchor kits to the sheet in the box. Take out the old rear bearer; do not reuse it.',
 'Joists and rims. 17 main joists of 2510 mm at the centres in the set-out list, with the pair at 3933/3978. Three rebuilt joists of 1880 mm, two blocks over the Y−800 bearer and the three SSCPC40 hold-down pairs at the rear (F4). Nail the 6.6 m rims at Y0 and Y2555 and the 900 mm rebuilt rims. Two M12 rim ties where the rebuilt strip meets the main deck (F6).',
 f'Step cleats. Screw three 250 mm H4 cleats to the outside face of the front bearer at X{cleatlist}, bottoms at +78 (that is 390 mm down from the rim top), with two 14g×100 screws each (F5).',
 f'Paver pits. Now that the deck frame is up and level, dig six pits 450×800 mm centred at X{padlist}, Y2800, about 150 mm deep or until you reach firm ground. Fill with GAP7 in two layers, tamping each hard with the end of a pile offcut. Bed two 300×300 pavers in each pit, one under each rail line (Y2645 and Y2955), and tap them down with a rubber mallet until the top is 400 to 420 mm below the deck rim top, measured with a straight edge and tape. Flat matters; exactly level does not.',
 'Step frame. Nail up the two 6.6 m double H4 rails (F1 pattern). Lay the inner-face ply of each rail on the lawn, nail the 17 crosspieces of 220 mm between them at the joist centres (F3), then nail the outer plies on. Lift the frame onto the pavers with the inner rail against the cleats. At each paver, slide DPC and plastic packers under the rail until the frame top is exactly 250 mm below the deck rim top and the frame does not rock. Screw each cleat to the inner rail (F5).',
 'Boards. Lay the 32 mm boards along X on the main deck, rebuilt strip and step. Put every butt joint on the paired members at 3955. Use the board supplier\'s gap and two screws per board per joist. Brush every cut. Finish with lawn, path and garden clear of all timber.',
]
fixings=[
 ('F1','Double bearers and double step rails','90×4 stainless nails, two rows at 250 mm centres, alternating faces. Same pattern for the four H4 rail plies.'),
 ('F2','Ordinary pile to bearer','Four 100×4 stainless skew nails at each pile.'),
 ('F3','Joists, rims, blocks, crosspieces','NZS 3604 Table 7.5 nailing: two 100×4 stainless per joist end through the rim, two per crosspiece end through the inner rail ply before the outer ply goes on.'),
 ('F4','Rebuilt rear hold-downs','Three SSCPC40 pairs, each cleat with two 14g×35 into the joist and two 14g×100 into the bearer. Screened uplift 1.92 kN against 2.69 kN per pair.'),
 ('F5','Step tie cleats (sideways only)',f'Three 250 mm 140×45 H4 cleats on the front bearer face at X{cleatlist}, bottom +78. Two 14g×100 stainless screws into the bearer and two into the inner rail. They stop the step sliding away from the deck; they carry no weight.'),
 ('F6','Rebuilt to main rim tie','Two M12×120 stainless coach bolts through the adjacent rims at X200/700, Z398, 50 mm square washers both sides.'),
 ('F7','Corner anchor piles','Four corner piles with complete LUMBERLOK 12 kN kits fitted to the maker\'s sheet. These brace the whole deck; see the assumptions.'),
 ('F8','Step rails on pavers','No fixing. Each rail sits on DPC and plastic packers on its paver. The three cleats (F5) hold the step to the deck.'),
]
jc=', '.join(str(int(x)) if float(x).is_integer() else str(x) for x in d['main_joist_centres_mm'])
md=f'''# Deck and step build guide

{DATE} · How I am going to build the 6.6 m deck and the low step in front of it. One plan, three drawings, a priced shopping list and the build order, written for an owner doing the work. It is not an engineer's design; the things I have assumed, and would ideally have checked, are listed at the end.

## What we are building

| Part | What |
|---|---|
| Main deck | 6600×2600 mm, boards about 500 mm above the lawn. Two double 140×45 H3.2 bearers on 16 timber piles in rows at Y300 and Y2510; 140×45 joists across them, 2.21 m span (the table limit at 450 centres is 2.35 m). |
| Main joists | 17 members: 16 lines at 437 mm centres, with the line at 3955 replaced by a pair at 3933/3978 to carry the board butt joints. Plain rims at Y0 and Y2555; no blocking, because the rims are within 300 mm of the bearers. |
| Rebuilt strip | 900×1970 mm beside the house. Old bearer replaced. Two 900 mm double bearers at Y−1925 and Y−800, three separate 1880 mm joists, two blocks, three hold-down pairs at the rear. Nothing runs through into the main deck. |
| Step | 6600×400 mm, boards 250 mm above the lawn. A ladder frame: two double 140×45 H4 rails (90 mm wide) at Y2600–2690 and Y2910–3000 with 17 crosspieces of 220 mm, sitting on six pairs of concrete pavers and tied to the deck by three short cleats. |
| Boards | 32 mm treated pine, all running along X, on the deck, the rebuilt strip and the step. |
| Finish | Natural treated pine, plain front edge, no handrails. Lawn and path stay at their present levels. |

Set-out, X from the left edge in mm. Joist and crosspiece centres: {jc}. Main piles: 62.5, 1357.5, 2652.5, 3947.5, 5242.5, 6537.5 on rows Y300 and Y2510. Rebuilt piles: X175 and X725 on Y−1925 and Y−800. Step pads: {padlist}, each a pair of 300×300 pavers centred on Y2645 and Y2955. Cleats: {cleatlist}.

Heights, lawn = 0: deck boards top +500, joist and rim top +468, bearer top +328, pile top +187 (DPC under the bearer). Step boards top +250, rail top +218, rail bottom +78; under that DPC, packers, and a paver top anywhere between +45 and +75.

## Three drawings

[1 · Piles, pads and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixings and step section](docs/drawings/fixings.svg)

## Foundations

16 timber piles: 12 ordinary (holes 350×350, 450 deep) and 4 corner anchors (holes 350×350, 900 deep) with 12 kN fixing kits. One pour of about {cv["main_net_m3"]:.2f} m³ fills every hole to 100 mm below ground; nothing in it needs to be level, because the piles are cut to a string afterwards. A mini-mix truck for 1.2 m³ is the easy way; {cv["bags_20kg_needed"]} bags of 20 kg and a hired mixer is the big-box way.

The step does not get concrete. Each of the six pads is a pit 450×800 mm dug to firm ground, filled with compacted GAP7, with two 300×300 concrete pavers bedded on top, one under each rail. The rails sit on the pavers on DPC and plastic packers. The pads are between the pile holes so the pavers sit on undisturbed ground.

### Why the step sits on pavers

A timber pile has to stand at least 150 mm clear of the ground, and under a 250 mm step there is only about 78 mm, so short piles are out. Pouring six little concrete pads to exactly the same level is the fiddliest job on the site for someone who has not done it before. Pavers on a tamped base, with the deck frame as the level reference and packers to take up the difference, is how most low steps beside a deck are actually built. The step is 89% of my bending screen with a 2.7 kN person standing on the very end, which is the hardest case.

### Setting the pavers without a level

1. Build the deck frame first. Its rim is straight and level, so every step measurement is a tape held down from the rim top.
2. Dig each pit to firm ground, fill with GAP7 in two layers and tamp each one hard. Bed the two pavers and tap them down until the top is 400 to 420 mm below the rim top (about +50 to +70 above the lawn). Lower is fine, higher is not.
3. Build the step frame on the lawn, lift it onto the pavers against the cleats, and pack under each rail at each paver until the frame top is 250 mm below the rim top everywhere and nothing rocks. Then screw the cleats on.

## Shopping list

[Download the CSV](docs/shopping-list.csv). NZD including GST, read from bunnings.co.nz and mitre10.co.nz on {DATE}. Posted means the price shown online for that exact product; estimate means the item is sold in store or by special order and a listed stand-in was used for the price. Timber and heavy items at both stores are click-and-collect or in-store only. Nothing has been bought and no supplier has been contacted.

| Item | Quantity | Store | Price basis | Line |
|---|---|---|---|---|
'''
for item,qty,sup,basis,line,kind,url in rows:
 md+=f"| {item} | {qty} | {('['+sup+']('+url+')') if url else sup} | {basis}{' (estimate)' if kind=='estimate' else ''} | ${line:,.2f} |\n"
md+=f'''
**Posted prices ${posted:,.2f} + estimates ${est:,.2f} = about ${total:,.0f} including GST.** Delivery, tool hire (mixer, drop saw, nail punch, rubber mallet, tamper) and soil disposal are extra. Two things would cut this a lot: a mini-mix truck instead of 110 bags, and galvanised instead of stainless fasteners and kits if the site is outside the sea-spray zone (see the assumptions). Trade merchants will beat most of these prices; get two quotes once the list is final.

If 140×45 H4 cannot be had, rough-sawn 150×50 H4 SG8 works for the step. The rails are then 10 mm deeper and 10 mm wider, so cut the crosspieces at 200 mm and aim the paver tops 10 mm lower.

### Cut list

| 140×45 H3.2 stock | Cuts, mm |
|---|---|
'''
for a in d['main_stock_allocations']:md+=f"| {a['count']}×{a['stock_mm']} | "+' + '.join(str(int(c)) if float(c).is_integer() else str(c) for c in a['cuts_mm'])+' |\n'
md+=f"\nMain and rebuilt: {d['main_stock_lm']} m bought, {d['main_installed_lm']} m used. 6600 = 4 bearer plies + 2 rims; 2510 = 17 joists; 900 = 4 rebuilt bearer plies + 2 rebuilt rims; 382.5 = 2 blocks; 1880 = 3 rebuilt joists. If 7.2 m lengths are not in stock, splice each bearer ply over a pile (stagger the two plies) and each rim at a joist.\n\n| 140×45 H4 stock | Cuts, mm |\n|---|---|\n"
for a in d['H4_stock_allocations']:md+=f"| {a['count']}×{a['stock_mm']} | "+' + '.join(str(c) for c in a['cuts_mm'])+' |\n'
md+=f'''
Step: {d['H4_stock_lm']} m bought, {d['H4_installed_lm']} m used. 6600 = 4 rail plies; 220 = 17 crosspieces; 250 = 3 cleats. H4 is sold per metre, so ask for four lengths of at least 6.7 m and one of 3.0 m. Allow 4 mm per saw cut and 5 mm end trim. Boards at 88 mm with about 5 mm gaps: 28 rows on the deck, 22 on the rebuilt strip, 5 on the step; 1254 screw positions, buy 1500.

## Fixings

| ID | Joint | Detail |
|---|---|---|
'''
for f in fixings:md+='| '+' | '.join(f)+' |\n'
md+='''
## Build order

'''
for i,s in enumerate(steps,1):md+=f'{i}. {s}\n'
md+=f'''
## Assumptions, and what I would get checked in an ideal world

This is what I would do. None of it has been checked by an engineer or a builder, and no council consent is involved: the deck is under 1.5 m, so it is exempt building work, but it still has to be built properly.

- **The four corner piles as anchors.** A freestanding deck needs something to stop it racking. My default is four corner anchor piles with 12 kN kits in 900 mm holes. An engineer would size this properly from the deck weight and the site wind and earthquake loads; I am relying on it being a common detail for a low deck this size.
- **The ground.** Every footing assumes firm natural clay at about 100 kPa under the topsoil, which is normal for Auckland but not guaranteed. The pads put at most {sc['pad_bearing_kPa_max']:.0f} kPa on the pavers. If a hole hits soft, wet or filled ground, that hole needs a deeper or wider footing, and someone who knows soils should look at it.
- **The step rails.** The double H4 rails are checked as a beam only, at {sc['double_rail_utilisation']*100:.0f}% of my screen with a 2.7 kN point load on the very end, using the grade stresses for wet timber. The pavers, packers and cleats are ordinary carpentry, not rated connections. When someone stands on the very end of the step the rail may lift a millimetre or two off the next paver along; that is expected and harmless, but it is a reason not to leave big gaps under the rails.
- **No hold-down on the step.** The step is held to the deck by three cleats and otherwise sits by gravity. I think that is fine for a 250 mm high step with boards on it; a builder might add a bracket at each paver anyway.
- **Stainless everywhere.** I have priced 316 stainless nails, screws and kits because I do not know if the site is in the sea-spray zone (within 500 m of the sea or a harbour, or 100 m of a tidal estuary or sheltered inlet). Outside it, NZS 3604 allows hot-dip galvanised, which is about a quarter of the price. Worth checking on the Auckland Council GIS viewer before buying fasteners.
- **The house junction.** I have not drawn the gap to the cladding or the drop from the door sill. Both depend on the actual cladding and door, so step 1 of the build order is to measure them. Keep the deck below the door sill and keep timber off the cladding so water can get out.
- **The 250 mm step.** A single 250 mm rise is above what the stair rules allow for a compliant step. It is our choice for this garden, and nothing here claims access compliance.
- **Timber and prices.** 140×45 H4 is not listed online at either store; if the store only has rough-sawn 150×50 H4, use the note in the shopping list. Prices were read on {DATE} and will drift; the two estimates (7.2 m framing and the pavers) are what the store will tell me in person.
- **The old rebuilt strip.** I am replacing the old bearer and not relying on any retained timber. If what comes out of the ground is worse than expected, the rebuilt piles get the same treatment as the main ones.

## Sources

Northpine wet-service tables: 140×45 SG8 at 450 centres spans 2.35 m; NZS 3604 Table 7.2 allows an 1100 mm cantilever against the rebuilt 755 mm; §7.1.2 allows rims within 300 mm of a support to replace blocking; §6.4 requires piles to stand 150 mm clear of the ground. [Northpine tables](https://www.northpine.co.nz/span-tables) · [MiTek LUMBERLOK data](https://mitek.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf) · [BRANZ Bulletin 611, low bearers on concrete](https://d39d3mj7qio96p.cloudfront.net/media/documents/BU611-Timber-Slat-Deck.pdf) · [H4 SG8 product information](https://www.fwp.co.nz/wp-content/uploads/2023/11/Building-Products-Information-Waipapa-Pine-H4-H5-H6-MG-RS-SG8-Framing-Timber.pdf).

Reproduce with `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`; data in design.json. Both rails must be continuous 6600 mm. Earlier plans are in archive/.
'''
(root/'CURRENT_DESIGN.md').write_text(md)
b=io.StringIO(newline='');w=csv.writer(b,lineterminator='\n');w.writerow(['Item','Quantity','Store','Price basis','Line NZD incl GST','Posted or estimate','Source']);w.writerows(rows);w.writerow(['TOTAL','','','',total,f'posted {posted} + estimates {est}','']);(root/'SHOPPING_LIST.csv').write_text(b.getvalue())
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
body=body[:a]+'''<h2 id="three-drawings">Three drawings</h2><div class="tabs" role="tablist" aria-label="Drawings"><button id="tab-piles" role="tab" aria-controls="drawing-panel" aria-selected="true" data-view="piles">1 · Piles, pads &amp; heights</button><button id="tab-framing" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="framing">2 · Framing</button><button id="tab-fixings" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="fixings">3 · Fixings &amp; step section</button></div><div id="drawing-panel" role="tabpanel" aria-labelledby="tab-piles"><div id="drawing"></div><p id="drawing-caption" class="caption"></p></div><p class="note">Download: <a href="drawings/piles.svg">piles</a> · <a href="drawings/framing.svg">framing</a> · <a href="drawings/fixings.svg">fixings</a></p>'''+body[bb:]
body=body.replace('href="docs/','href="').replace('archive/','<a href="https://github.com/MaxHogervorst/deck-design/tree/main/archive">archive/</a>')
html='''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="Owner-builder guide for a 6.6 m Auckland deck and paver-supported step: layout, foundations, fixings, build order and a Bunnings and Mitre 10 priced shopping list."><title>Deck and step build guide</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">Auckland deck <span>10 / 11 / 2026 · BUILD GUIDE</span></a><nav aria-label="Sections"><a href="#three-drawings">Drawings</a><a href="#foundations">Foundations</a><a href="#shopping-list">Shopping list</a><a href="#build-order">Build order</a><a href="#assumptions-and-what-i-would-get-checked-in-an-ideal-world">Assumptions</a></nav><button id="print">Print</button></header><main id="main">'''+body+'''</main><footer><span>Owner-builder working plan · read the assumptions before building</span><button id="copy-link">Copy link</button></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
(root/'site/index.html').write_text(html)
print('Rendered guide, CSV and page; posted',posted,'estimates',est,'total',total)
# Three standalone drawings.
T='#cba773';G='#456b54';C='#d6dad7';S='#ece5d6';A='#af6b3c';P='#b9b3a6'
def r(x,y,w,h,fill,stroke='#52675b',dash=''):return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def line(x,y,x2,y2,stroke='#71847b',dash=''):return f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def text(x,y,tx,size=13,anchor='start'):return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{E(tx)}</text>'
def svg(name,title,bd,w=1100,h=800):
 out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}"><title>{E(title)}</title><style>text{{font-family:system-ui,sans-serif;fill:#21382f}}line{{stroke-width:1.5}}</style><rect width="{w}" height="{h}" fill="#fbfbf8"/>{bd}</svg>'
 (root/'site/drawings'/f'{name}.svg').write_text(out)
X=lambda x:55+x*.105;Y=lambda y:295+y*.09
outline=r(X(0),Y(0),6600*.105,2600*.09,'#f5f7f2')+r(X(0),Y(-1970),900*.105,1970*.09,'#f5f7f2')+r(X(0),Y(2600),6600*.105,400*.09,'#faf3e4')
def pavers(x,fill=P,stroke='#7f8f86'):
 return r(X(x-150),Y(2495),300*.105,300*.09,fill,stroke)+r(X(x-150),Y(2805),300*.105,300*.09,fill,stroke)
# Drawing 1
bd=text(40,35,'1 · Piles, pads and heights',21)+text(40,62,'Set-out plan · lawn = 0 · 16 timber piles in concrete, 6 paver pads with no concrete',13)+outline
for y in [300,2510]:
 for x in d['main_pile_X_mm']:
  anchor=x in [62.5,6537.5]
  bd+=r(X(x-175),Y(y-175),350*.105,350*.09,'none','#9aa89f','3 3')+r(X(x-62.5),Y(y-62.5),125*.105,125*.09,A if anchor else G)
for y in [-1925,-800]:
 for x in [175,725]:bd+=r(X(x-62.5),Y(y-62.5),125*.105,125*.09,G)
for x in pads:bd+=r(X(x-225),Y(2400),450*.105,800*.09,'none','#9aa89f','3 3')+pavers(x)
bd+=text(185,133,'Rebuilt strip: four ordinary piles',12)+text(180,169,'Rear bearer back face Y−1970, centre −1925',12)+text(180,205,'Middle bearer centre Y−800',12)
bd+=text(X(3300),Y(1400),'Main deck: 12 piles on rows Y300 and Y2510 (orange = corner anchors)',13,'middle')
bd+=text(X(3300),Y(3350),'Six step pads: two 300×300 pavers each (grey) in a 450×800 GAP7 pit (dashed), clear of every pile hole',12,'middle')
bd+=text(790,105,'Heights · lawn = 0',14)
Z=lambda z:340-z*.38
bd+=r(790,Z(0),280,100,S)+line(790,Z(0),1070,Z(0))
bd+=r(800,Z(500),130,12,T)+r(810,Z(468),110,53.2,G)+r(820,Z(328),90,53.2,T)+r(850,Z(187),30,71,T)
bd+=r(950,Z(250),100,12,T)+r(955,Z(218),85,53.2,T)+r(960,Z(78),75,6,'#fff')+r(960,Z(60),75,15,P)+r(955,Z(20),85,Z(-130)-Z(20),C,'#9aa89f','3 3')
bd+=text(800,134,'Deck +500',13)+text(950,225,'Step +250',13)+text(800,370,'0 · lawn / path',12)+text(1000,Z(95),'packers + DPC',10)+text(1000,Z(40),'paver top +45…+75',10)+text(1000,Z(-60),'GAP7, tamped',10)
bd+=text(790,490,'16 timber piles, one pour',14)+text(790,516,'12 ordinary · holes 350×350×450',12)+text(790,538,'4 corner anchors · holes 350×350×900',12)
bd+=text(790,572,'6 step pads, no concrete',14)+text(790,598,'pit 450×800 to firm ground, GAP7',12)+text(790,620,'2 pavers 300×300, tops 400–420 below rim top',12)
bd+=text(40,635,'Main pile X: 62.5 / 1357.5 / 2652.5 / 3947.5 / 5242.5 / 6537.5 · rows Y300 / Y2510. Pile tops cut to a string at +187.',13)
bd+=text(40,666,'Pad X: '+' / '.join(str(p) for p in pads)+' · pavers centred Y2645 and Y2955 · pits dug after the deck frame is up.',13)
bd+=text(40,697,'Nothing is poured level. Piles are cut to a string; pavers are tapped down to a tape off the deck rim; packers do the rest.',13)
bd+=text(40,730,f'One pour: about {cv["main_net_m3"]:.2f} m³ into all 16 holes. Mini-mix 1.2 m³, or {cv["bags_20kg_needed"]} bags of 20 kg.',12)
bd+=text(40,763,'Pile symbols show position only. The corner anchor detail is an assumption listed at the end of the guide.',12)
svg('piles','Sixteen timber pile positions with four corner anchors, six paver pads between the pile holes; deck 500, step 250, paver tops 45 to 75',bd)
# Drawing 2
bd=text(40,35,'2 · Framing sizes and board direction',21)+text(40,62,'140×45 SG8 · H3.2 main and rebuilt · H4 step (double rails)',13)+outline
for y in [300,2510]:bd+=r(X(0),Y(y-45),6600*.105,90*.09,T)
for y in [-1925,-800]:bd+=r(X(0),Y(y-45),900*.105,90*.09,T)
for x in d['main_joist_centres_mm']:bd+=r(X(x-22.5),Y(45),45*.105,2510*.09,G)
for x in [22.5,450,877.5]:bd+=r(X(x-22.5),Y(-1925),45*.105,1880*.09,G)
for x in [45,472.5]:bd+=r(X(x),Y(-822.5),382.5*.105,45*.09,G)
for y,length in [(0,6600),(2555,6600),(-1970,900),(-45,900)]:bd+=r(X(0),Y(y),length*.105,45*.09,T)
for x in cleats:bd+=r(X(x-70),Y(2555),140*.105,45*.09,A)
for x in pads:bd+=pavers(x,'none','#7f8f86')
for y in [2600,2910]:bd+=r(X(0),Y(y),6600*.105,90*.09,T)
for x in d['main_joist_centres_mm']:bd+=r(X(x-22.5),Y(2690),45*.105,220*.09,G)
bd+=text(215,125,'All boards run along X →',19)+text(215,158,'Deck + rebuilt strip + step',13)
for i,tx in enumerate(['Deck: 17 joists of 2510','16 lines at 437 + butt pair 3933/3978','2.21 m span on bearers Y300/Y2510','Plain rims Y0 and Y2555','','Rebuilt: 3 joists of 1880','2 blocks over Y−800 bearer','','Step: 2 double rails 6600','17 crosspieces of 220','3 cleats (orange) on bearer face','6 paver pairs (outlined)']):bd+=text(790,250+i*26,tx,13)
bd+=text(40,635,'Bearers: 2×140×45 nailed (F1). Joists sit on the bearers and are nailed through the rims; no blocking in the deck.',13)
bd+=text(40,666,'Step rails: 2×140×45 H4 nailed like a bearer, inner Y2600–2690, outer Y2910–3000, continuous 6600.',13)
bd+=text(40,697,'Crosspieces at the joist centres so board screw lines run straight through. Butt line X3955 has pairs in deck and step.',13)
bd+=text(40,730,'Cuts: deck 17×2510, rebuilt 3×1880; step rails 4×6600, crosspieces 17×220, cleats 3×250.',13)
bd+=text(40,763,'Rear line Y−1970 is the rebuilt bearer back face; its centre is −1925. The old bearer is not reused.',12)
svg('framing','Framing plan: seventeen main joists, three rebuilt joists, two blocks, two double H4 step rails on six paver pairs with seventeen crosspieces and three cleats, all boards along X',bd)
# Drawing 3: section through the front edge at a pad, looking along X.
bd=text(40,35,'3 · Fixings and step section at a pad',21)+text(40,65,'The step bears on two pavers per pad; the cleat only ties it sideways to the deck. Nothing is poured level.',13)
Zs=lambda z:560-z*.5;Ys=lambda y:60+(y-2250)*.6
bd+=r(Ys(2250),Zs(0),(3250-2250)*.6,Zs(-500)-Zs(0),S)+line(Ys(2250),Zs(0),Ys(3250),Zs(0),'#52675b')
bd+=r(Ys(2400),Zs(20),800*.6,Zs(-150)-Zs(20),C,'#9aa89f')
for yc in [2645,2955]:bd+=r(Ys(yc-150),Zs(60),300*.6,40*.5,P)+r(Ys(yc-45),Zs(78),90*.6,18*.5,'#fff','#9aa89f')
bd+=r(Ys(2335),Zs(-100),350*.6,350*.5,'none','#9aa89f','4 3')+r(Ys(2447.5),Zs(187),125*.6,(187+350)*.5,'none','#9aa89f','4 3')
bd+=r(Ys(2465),Zs(328),90*.6,140*.5,T)+r(Ys(2250),Zs(468),305*.6,140*.5,G)+r(Ys(2555),Zs(468),45*.6,140*.5,T)+r(Ys(2250),Zs(500),350*.6,32*.5,T)
bd+=r(Ys(2555),Zs(328),45*.6,250*.5,A)
bd+=r(Ys(2600),Zs(218),90*.6,140*.5,T)+r(Ys(2690),Zs(218),220*.6,140*.5,G)+r(Ys(2910),Zs(218),90*.6,140*.5,T)+r(Ys(2600),Zs(250),400*.6,32*.5,T)
bd+=line(Ys(2555),Zs(258),Ys(2555)-18,Zs(258),'#324c42')+line(Ys(2555),Zs(118),Ys(2555)-18,Zs(118),'#324c42')+line(Ys(2600),Zs(148),Ys(2600)+18,Zs(148),'#324c42')+line(Ys(2600),Zs(178),Ys(2600)+18,Zs(178),'#324c42')
bd+=text(Ys(2300),Zs(530),'Deck +500',12)+text(Ys(2700),Zs(280),'Step +250',12)+text(Ys(3010),Zs(85),'DPC + packers',10)+text(Ys(3010),Zs(45),'paver 300×300, top +45…+75',10)+text(Ys(3010),Zs(-60),'GAP7 pit 450×800, tamped',10)+text(Ys(2300),Zs(-20),'0 · lawn',11)
bd+=text(Ys(2300),Zs(-300),'pile footing (dashed, other X)',10)+text(Ys(2560),Zs(-280),'firm ground',11)
bd+=text(Ys(2395),Zs(260),'bearer',11)+text(Ys(2460),Zs(560),'joist / rim',11)+text(Ys(2520),Zs(70),'cleat',11)
bd+=text(680,150,'F8 · Rails on pavers',16)+text(680,178,'No fixing into the pavers',13)+text(680,204,'Pack under each rail until the frame top',13)+text(680,228,'is 250 below the rim top and nothing rocks',13)
bd+=text(680,268,'F5 · Cleats',16)+text(680,296,'3×250 mm H4 on bearer face',13)+text(680,320,'2×14g×100 into bearer, 2 into rail',13)+text(680,344,'Sideways tie only; no step weight',13)
bd+=text(680,384,'Rail screen',16)+text(680,412,f"{sc['double_rail_max_M_ULS_kNm']:.2f} of {sc['double_rail_bending_screen_capacity_kNm']:.2f} kNm ({sc['double_rail_utilisation']*100:.0f}%)",13)+text(680,436,f"max pad load {sc['max_pad_reaction_ULS_kN']:.1f} kN, {sc['pad_bearing_kPa_max']:.0f} kPa",13)
bd+=text(40,860,'F1: 90×4 SS nails, two rows at 250, alternating faces, for bearers and step rails. F2: 4×100×4 SS skew nails per pile.',12)
bd+=text(40,888,'F3: two 100×4 per joist end through the rim, two per crosspiece end through the inner rail ply. F4: three SSCPC40 pairs at the rear.',12)
bd+=text(40,916,'F6: two M12×120 SS coach bolts at X200/700, Z398. F7: four corner anchor kits (12 kN SS). F8: step rails free on pavers.',12)
bd+=text(40,944,'Before building: measure the door sill and cladding gap, call beforeUdig, and read the assumptions at the end of the guide.',12)
bd+=text(40,972,'Drawn at a pad; the pile and its footing (dashed) are at a different X and never share ground with a paver pit.',12)
svg('fixings','Section through the deck front edge at a step pad: deck on bearer and pile, step double rails on two pavers over a GAP7 pit, cleat on the bearer face; fixing schedule F1 to F8',bd,h=1000)
