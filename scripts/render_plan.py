"""Render the single current plan, CSV and three drawings from design.json."""
from pathlib import Path
from html import escape as E
import json,csv,io
root=Path(__file__).resolve().parents[1];d=json.loads((root/'design.json').read_text())
core=round(106.8*6.84+270*2.99,2);cv=d['concrete_geometry_only'];sc=d['screens']
rows=[
 ('Main/rebuilt H3.2 SG8','106.8 stock lm in140×45','NZ Timber','$6.84/m; $730.51 inclGST','https://www.nztimber.net.nz/shop/p/150x50-140x45-h32-sg8-wt-rad-framing-1-metre'),
 ('Tread H4 SG8','22.8 stock lm in140×45:2×7.2m,1×6m,1×2.4m','Waipapa Pine stockist','Quote exact grade,section and lengths','https://www.fwp.co.nz/wp-content/uploads/2023/11/Building-Products-Information-Waipapa-Pine-H4-H5-H6-MG-RS-SG8-Framing-Timber.pdf'),
 ('32mm pine boards','270lm price allowance;88mm suggested width','Warehouse Building Supplies','$2.99/m; $807.30 inclGST','https://www.warehousebuildingsupplies.co.nz/shop/timber-decking-merch-grade-30/106672-deck-merch-h32-100x4088x32-smthrandom-30605'),
 ('Main/rebuilt piles','16 total:4 candidate anchors +12 ordinary','Local timber merchant','H5 NZS3605; anchor size/stock pending;12ordinary750mm basis',''),
 ('Concrete','Planning net1.263268m³: main0.986875 +six outer pads0.276393','Ready-mix supplier','25MPa; conditional geometry,not an order; crowns/waste/actual anchor section additional',''),
 ('Board screws','1500 allowance;1254 base positions','Fastener merchant','75mm10gSS316 basis;confirm pine head/penetration',''),
 ('Ordinary structural nails','500×100×3.75 SS +200×90×4 SS allowances','Fastener merchant','Exact packs/profile; excludes proprietary connector fasteners',''),
 ('Rebuilt hold-downs','3 pairs genuineSSCPC40;12each14g×35 and14g×75 SS screws','MiTek stockist','Rear row only; complete manufacturer pattern; coordinate final joints',''),
 ('Cleat/tie bolts - provisional','30×M12×120 SS316 bolt/nut sets;60×50×50×3 washers','Fastener merchant','28for7cleats +2rim ties; full hanging joint remains unverified',''),
 ('Main anchor connections','4 complete standard/manufacturer assemblies','Connector merchant','Hardware/grade/fit and bracing must be confirmed; no untested substitute kit',''),
 ('Outer-rail pad restraint','6 bearing positions; final positive-restraint detail pending','Connector merchant','No old14-restraint order; verify uplift/shear path to deck or pad',''),
 ('DPC +cut treatment','150mm×30m DPC roll; compatible preservative','Building merchant','0.75mm nominal embossed Supercourse500; protect exposed DPC',''),
]
steps=[
 'Check the house cladding gap, door threshold/weatherproofing detail and actual500/250mm datums with the builder; complete the hanging and anchor details.',
 'Mark all footprints, sixteen timber-pile positions and six outer-rail pad positions from Drawing1. Keep surrounding ground levels.',
 'Dig the footing holes to the agreed bearing and depth schedule; set piles and individual pad forms.',
 'Set all six pad bearing tops level at nominal+77.25mm, place the specified concrete and observe cure/anchor installation requirements.',
 'Fit continuous main double bearers atY300/2510 and the two900mm rebuilt double bearers. Replace the old deck bearer safely; do not assume it supports only the deck without checking.',
 'Fit seventeen main joist members and three separate rebuilt joists. Fit the two lateral blocks over the intermediate rebuilt bearer and the rear hold-downs.',
 'Build the front rim: continuous inner ply plus the seven vertical cleat heads and eight outer infill pieces. Keep the cleats clear of joist ends and bolt access.',
 'Bolt the tread inner rail to the cleats to the completed fixing detail. Assemble seventeen310mm H4 crosspieces and the continuous outer rail.',
 'Seat the outer rail on DPC at the six pad tops. Complete the agreed positive restraint and main bracing/load path before boards.',
 'Lay32mm pine boards alongX in the main deck, rebuilt strip and tread. Support butt ends on paired members and use supplier-approved gaps/screws.',
 'Treat permitted cuts and finish the lawn/path/garden clear of timber. Check the owner-built work against the agreed plan; no builder inspection visits are assumed.'
]
fixings=[
 ('F1','Built-up main/rebuilt bearers','90×4SS structural nails,two rows≤250centres,alternate faces; connector exclusions apply.'),
 ('F2','Ordinary pile/bearer','Four100×3.75SS skew nails at each ordinary seated joint; no blanket soil lowering.'),
 ('F3','Ordinary joist/rim/block','NZS3604Table7.5 schedule; joist/rim basis2×100×3.75SS per joint; short curtailed tread pieces3per end,subject to the2.7kN stair-action check.'),
 ('F4','Rebuilt rear uplift','3genuineSSCPC40pairs,each cleat2specified14g×35intojoist +2specified14g×75intobearer. Rear zero-dead uplift demand1.812kN vs2.688kN/pair preliminary screen.'),
 ('F5','Tread cleats - draft','7×414mm140×45H4 cleats,top+468/bottom+54. TwoM12upper bolts atZ380 and two lower atZ152 per cleat,80mm across the140face. M12×120/50-square washers are provisional; not a drilling release.'),
 ('F6','Rebuilt/main lateral tie - draft','TwoM12×120bolts through adjacent140mm rims atX200/700,Z398; washers/nut access and whole bracing transfer to confirm.'),
 ('F7','Anchors and outer pads','Four corner anchor assemblies and six outer pad restraint points need complete applicable standard/manufacturer details. No connection approval is inferred from a component screen.')
]
foundation=f'''16timber piles: **4candidate anchors +12ordinary** (main12positions,rebuilt4). **6outer tread pads**; no inner ground supports. Main pile X:62.5/1357.5/2652.5/3947.5/5242.5/6537.5 onY300/2510; proposed anchors at the four end locations. Rebuilt pilesX175/725 onY−1925/−800. Outer pad X:175/1325/2640/3960/5275/6425,Y2955.

One conditional concrete basis:4anchor holes350×350×900;12ordinary holes350×350×450,100concrete below timber,125-square timber only as the volume assumption. Six outer bases350×350 from−450to−100,with200×90heads to+77.25 (headsY2910…3000,within the visible tread). Main net0.986875m³ +pads0.276393m³ = **1.263268m³ net**. Crowns,irregular holes,waste and any changed anchor section are additional. These are planning dimensions,not a placement order. Four anchors remain conditional on the builder confirming compliant bracing and connections.'''
md='''# Deck and deck-supported tread

8November2026 · One current plan and three drawings. Working proposal: the hanging tread/rim connection,outer-pad restraint and four-anchor arrangement still need complete verification before building. No paid-designer appointment or construction-phase builder inspections are assumed.

## Agreed layout

| Part | Current decision |
|---|---|
| Main deck |6600×2600mm,about500mm above the garden; double140×45H3.2SG8bearers and140×45joists|
| Rebuilt strip |900×1970mm; old bearer replaced; two900mm double bearers; three separate1880mm joists; all boards alongX|
| Main joists |16base lines at437mmcentres,with one line replaced by a supported butt pair:17members,not13. X22.5+437i,i0…15; replace3955.5by3933/3978.|
| Main bearing rows |Y300/2510:2.21m span,below2.35m wet-service table limit at450centres. End rims provide lateral support within300mm,so the36main blocks are omitted.|
| Rebuilt supports |Rear bearer rear faceY−1970,centre−1925; intermediate centre−800. Two lateral blocks remain over the intermediate row; three rear hold-down pairs. No joists continuous into the main deck.|
| Tread |6600×400mm,surface250mm;140×45H4SG8ladder,seven rim cleats supporting inner rail,six concrete pads under outer rail. No H5 tread special order.|
| Front rim |Continuous140×45inner plyY2510…2555,plus cleat heads/infill layerY2555…2600. Bearer directly below inner ply; complete eccentric hanging load path remains to check.|
| Tread rails |Continuous6600mm140×45H4inner/outer rails atY2600…2645/2955…3000; seventeen310mm crosspieces. Boards alongX,paired butt supports at3955.5.|
| Finish |Natural treated pine,plain front rail,selected500/250levels and surrounding lawn/path levels retained; no handrails proposed.|

## Three drawings

[1 · Piles and heights](docs/drawings/piles.svg) · [2 · Framing and sizes](docs/drawings/framing.svg) · [3 · Fixing schedule](docs/drawings/fixings.svg)

## Foundations

'''+foundation+'''

Only the **six individual outer-pad bearing tops** need to be level with each other. There is no continuous concrete slab. Nominal tread rail bottom+78,DPC0.75,concrete+77.25;frame top+218,pine top+250.

## Materials and costs

[Download shopping CSV](docs/shopping-list.csv). NZD,posted prices checked8November2026; exact graded stock,usable lengths and freight require confirmation. H4framing has a documented manufacturer supply route; long lengths are not a stock reservation. Never substitute non-structural reman/fence timber or150×50rough stock for140×45 without reworking sizes.

| Item | Quantity | Source / price |
|---|---|---|
'''
for item,qty,supplier,price,url in rows:md+='|'+item+'|'+qty+'|'+('['+supplier+']('+url+')' if url else supplier)+' · '+price+'|\n'
md+=f'\n**Priced main timber and boards: ${core:,.2f}inclGST.** H4timber,piles,concrete,hardware,freight and ground work are additional;this is not a project total. No supplier contacted or purchase made.\n\n### Stock cuts\n\n| Main/rebuilt140×45H3.2 | Cuts from each,mm |\n|---|---|\n'
for a in d['main_stock_allocations']:md+=f"|{a['count']}×{a['stock_mm']}|"+' +'.join(str(c) for c in a['cuts_mm'])+'|\n'
md+='\nMain/rebuilt106.8stock lm /98.93installed lm. The final6000length supplies the eight front-rim infills. H4tread22.8stock lm /21.368installed lm:\n\n| H4stock | Cuts from each,mm |\n|---|---|\n'
for a in d['H4_stock_allocations']:md+=f"|{a['count']}×{a['stock_mm']}|"+' +'.join(str(c) for c in a['cuts_mm'])+'|\n'
md+='\nAllow4mm kerf per cut and5mm end trim. Board example at88mm/~5mm gaps:28main,22rebuilt,five tread rows;39×4.2m +33×3.0m =262.8lm before extra defect allowance.270lm is the price allowance. Base board screws1254;buying allowance1500. Actual moisture,width and supplier gaps govern.\n\n## Fixing schedule\n\n| ID | Joint | Detail / status |\n|---|---|---|\n'
for f in fixings:md+='|'+'|'.join(f)+'|\n'
md+='\nCleat Xcentres175/1230/2300/3200/4200/5370/6425. Upper/lower bolt axes are±40across each cleat. The seven cleats are deck attachments,not seven independent foundations.\n\n## Before building\n\n- Confirm four corner anchors,actual anchor-pile grade/section,low connection clearance and full bracing/load path. No blanket ground lowering is selected.\n- Complete the front-rim/cleat/bolt and tread board/crosspiece/end-joint/outer-pad restraint checks. Inner-rail preliminary support reaction reaches5.299kN;rim eccentric moment0.477kNm. \n- Check house cladding clearance,door-threshold height and weatherproofing/drainage against the actual door/cladding detail. Do not apply one universal gap to all claddings or doors.\n- Confirm H4SG8lengths and compatible fasteners. Keep the builder review before work;later checks are by the owner.\n\n## Build sequence\n\n'
for i,t in enumerate(steps,1):md+=f'{i}. {t}\n'
md+='\n## Evidence and limits\n\nNorthpine wet-service140×45SG8at450centres permits2.35m;Table7.2permits1100mm domestic-balcony projection versus the rebuilt755mm beyond support face. NZS3604§7.1.2permits boundary-rim lateral support within300mm;the intermediate rebuilt row keeps two blocks. Sources: [Northpine tables](https://www.northpine.co.nz/span-tables),[MiTek characteristic-load sheet](https://mitek.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf),[H4SG8 product information](https://www.fwp.co.nz/wp-content/uploads/2023/11/Building-Products-Information-Waipapa-Pine-H4-H5-H6-MG-RS-SG8-Framing-Timber.pdf).\n\nReproduce `OPENBLAS_NUM_THREADS=1 python scripts/check_revision.py`;data in design.json. Continuous inner/outer rail moment screens0.949/1.040kNm against1.101kNm provisional wet-SG8bending screen are favourable;not full assembly verification. Outer rail must remain continuous6600mm. Soil100kPa and normal ground are planning assumptions. The selected250mm rises exceed D1/AS1Table6stair limits;access compliance remains unresolved. No structural or access approval is claimed. Historical material is in archive/.\n'
(root/'CURRENT_DESIGN.md').write_text(md)
b=io.StringIO(newline='');w=csv.writer(b,lineterminator='\n');w.writerow(['Item','Quantity/specification','Suggested supplier','Price/status','Source']);w.writerows(rows);(root/'SHOPPING_LIST.csv').write_text(b.getvalue())
# Minimal Markdown renderer for this controlled document: headings,tables,lists and paragraphs.
import re
inline=lambda x: re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',E(x)))
parts=[];lines=md.splitlines();i=0
while i<len(lines):
 l=lines[i]
 if not l.strip():i+=1;continue
 if l.startswith('#'):
  level=len(l)-len(l.lstrip('#'));t=l[level:].strip();slug=re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-');parts.append(f'<h{level} id="{slug}">{inline(t)}</h{level}>');i+=1
 elif l.startswith('|'):
  block=[]
  while i<len(lines) and lines[i].startswith('|'):block.append(lines[i]);i+=1
  parts.append('<div class="table-wrap"><table>')
  for j,row in enumerate(block):
   if j==1:continue
   tag='th' if j==0 else 'td';parts.append('<tr>'+''.join(f'<{tag}>'+inline(c.strip())+f'</{tag}>' for c in row.strip('|').split('|'))+'</tr>')
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
# Replace the drawing-link paragraph with the three-view component, preserving download links.
a=body.index('<h2 id="three-drawings">');b=body.index('<h2 id="foundations">',a)
body=body[:a]+'''<h2 id="three-drawings">Three drawings</h2><div class="tabs" role="tablist" aria-label="Drawings"><button id="tab-piles" role="tab" aria-controls="drawing-panel" aria-selected="true" data-view="piles">1 · Piles &amp; heights</button><button id="tab-framing" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="framing">2 · Framing</button><button id="tab-fixings" role="tab" aria-controls="drawing-panel" aria-selected="false" tabindex="-1" data-view="fixings">3 · Fixings</button></div><div id="drawing-panel" role="tabpanel" aria-labelledby="tab-piles"><div id="drawing"></div><p id="drawing-caption" class="caption"></p></div><p class="note">Download: <a href="drawings/piles.svg">piles</a> · <a href="drawings/framing.svg">framing</a> · <a href="drawings/fixings.svg">fixings</a></p>''' +body[b:]
body=body.replace('href="docs/','href="').replace('href="archive/"','href="https://github.com/MaxHogervorst/deck-design/tree/main/archive"')
html='''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#254c3e"><meta name="description" content="One current deck plan: deck-supported tread, framing, foundations,fixings and shopping list."><title>Deck and supported tread · current plan</title><!-- INLINE_STYLES --></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="#main">Auckland deck <span>08 /11 /2026 · ONE CURRENT PLAN</span></a><nav aria-label="Sections"><a href="#three-drawings">Drawings</a><a href="#materials-and-costs">Materials</a><a href="#before-building">Builder brief</a><a href="#build-sequence">Build</a></nav><button id="print">Print</button></header><main id="main">'''+body+'''</main><footer><span>Current working plan · not construction approval</span><button id="copy-link">Copy link</button></footer><p id="message" role="status"></p><!-- INLINE_SCRIPT --></body></html>'''
(root/'site/index.html').write_text(html)
print('Rendered one plan,CSV and page;priced subtotal',core)
# Three standalone technical drawings; no abandoned foundation variants.
T='#cba773';G='#456b54';C='#d6dad7';S='#ece5d6'
def r(x,y,w,h,fill,stroke='#52675b'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,x2,y2,stroke='#71847b',dash=''):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{stroke}" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'
def text(x,y,t,size=13):return f'<text x="{x}" y="{y}" font-size="{size}">{E(t)}</text>'
def svg(name,title,b,w=1100,h=800):
 out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(title)}"><title>{E(title)}</title><style>text{{font-family:system-ui,sans-serif;fill:#21382f}}line{{stroke-width:1.5}}</style>{b}</svg>'
 (root/'site/drawings'/f'{name}.svg').write_text(out)
X=lambda x:55+x*.105;Y=lambda y:295+y*.09
outline=r(X(0),Y(0),6600*.105,2600*.09,'#f5f7f2')+r(X(0),Y(-1970),900*.105,1970*.09,'#f5f7f2')+r(X(0),Y(2600),6600*.105,400*.09,'#faf3e4')
b=text(40,35,'1 · Piles, pad positions and heights',21)+text(40,62,'Planning layout · four anchors conditional on complete bracing/connection check',13)+outline
for y in [300,2510]:
 for x in d['main_pile_X_mm']:
  anchor=x in [62.5,6537.5]
  b+=r(X(x-62.5),Y(y-62.5),125*.105,125*.09,'#af6b3c' if anchor else G)
for y in [-1925,-800]:
 for x in [175,725]:b+=r(X(x-62.5),Y(y-62.5),125*.105,125*.09,G)
for x in d['outer_pad_X_mm']:b+=r(X(x-100),Y(2910),200*.105,90*.09,C)
b+=text(185,133,'Rebuilt: four ordinary piles',12)+text(180,169,'Rear bearer face −1970 / centre −1925',12)+text(180,205,'Intermediate bearer centre −800',12)
b+=text(790,105,'Height datum · garden = 0',14)
Z=lambda z:340-z*.38
b+=r(790,Z(0),280,100,S)+line(790,Z(0),1070,Z(0))
b+=r(800,Z(500),130,12,T)+r(810,Z(468),110,53.2,G)+r(820,Z(328),90,53.2,T)+r(850,Z(187.25),30,95,T)
b+=r(950,Z(250),100,12,T)+r(955,Z(218),85,53.2,T)+r(970,Z(77.25),55,45,C)
b+=text(800,134,'Deck +500',13)+text(950,225,'Tread +250',13)+text(800,370,'0 · lawn / path',12)
b+=text(790,490,'16 timber piles:',14)+text(790,518,'4 anchors +12 ordinary',13)+text(790,550,'6 outer-rail pads',14)+text(790,578,'No inner ground supports',12)
b+=text(40,635,'Main X:62.5 /1357.5 /2652.5 /3947.5 /5242.5 /6537.5 · rows Y300 /2510.',13)
b+=text(40,666,'Outer pad X:175 /1325 /2640 /3960 /5275 /6425 · centre Y2955.',13)
b+=text(40,697,'Set only the six individual pad tops level at +77.25; DPC0.75, rail bottom+78.',13)
b+=text(40,730,'Footing depths, conditional volumes and unfinished connection checks are in the single plan.',12)
b+=text(40,763,'Pile symbols show positions, not a released anchor-pile size or cutting pattern.',12)
svg('piles','Sixteen timber pile positions,four conditional corner anchors,six outer tread pads;deck500,tread250,individual concrete bearing tops77.25',b)
b=text(40,35,'2 · Framing sizes and board direction',21)+text(40,62,'140 ×45 SG8 · H3.2 main/rebuilt; H4 ladder and cleats',13)+outline
for y in [300,2510]:b+=r(X(0),Y(y-45),6600*.105,90*.09,T)
for y in [-1925,-800]:b+=r(X(0),Y(y-45),900*.105,90*.09,T)
for x in d['main_joist_centres_mm']:b+=r(X(x-22.5),Y(45),45*.105,2465*.09,G)
for x in [22.5,450,877.5]:b+=r(X(x-22.5),Y(-1925),45*.105,1880*.09,G)
for x in [45,472.5]:b+=r(X(x),Y(-822.5),382.5*.105,45*.09,G)
for y,length in [(0,6600),(2510,6600),(-1970,900),(-45,900)]:b+=r(X(0),Y(y),length*.105,45*.09,T)
for x in d['cleat_X_mm']:b+=r(X(x-70),Y(2555),140*.105,45*.09,'#af6b3c')
for y in [2600,2955]:b+=r(X(0),Y(y),6600*.105,45*.09,T)
for x in d['main_joist_centres_mm']:b+=r(X(x-22.5),Y(2645),45*.105,310*.09,G)
b+=text(215,125,'All boards run along X →',19)+text(215,158,'Main +rebuilt +tread',13)
for i,t in enumerate(['Main:17joist members','16base lines +butt pair','437maxcentres /2.21m span','','Rebuilt:3separate joists','2lateral blocks at Y−800','','Tread:2continuous rails','17×310crosspieces','7vertical cleats /6pads']):b+=text(790,270+i*27,t,13)
b+=text(40,635,'Main bearers:2×140×45; rebuilt bearers:2×900 double. End rims replace the main block rows.',13)
b+=text(40,666,'Front rim:continuous inner ply plus7cleat heads and8outer infills; bearer under inner ply.',13)
b+=text(40,697,'Board butt line X3955.5 has paired supports at3933/3978 in main and tread.',13)
b+=text(40,730,'Main cuts:17×2465; rebuilt3×1880. Tread rails6600, crosspieces310, cleats414.',13)
b+=text(40,763,'Rear lineY−1970 is the bearer rear face; its centre is−1925. No retained-bearer reliance.',12)
svg('framing','Framing plan:seventeen main joists,three separate rebuilt joists,two lateral blocks,seven vertical tread cleats,six outerpads,all boards alongX',b)
b=text(40,35,'3 · Fixing schedule and hanging-tread section',21)+text(40,65,'DRAFT CONNECTION · complete load-path check required before drilling or construction',14)
Z=lambda z:565-z*.72
b+=r(55,Z(328),90,140*.72,T)+r(100,Z(468),45,140*.72,T)+r(145,Z(468),45,414*.72,'#d8b786')
b+=r(65,Z(500),125,32*.72,T)+r(190,Z(250),400,32*.72,T)
b+=r(190,Z(218),45,140*.72,T)+r(545,Z(218),45,140*.72,T)+r(235,Z(218),310,140*.72,G)
b+=r(500,Z(77.25),90,125,C)+line(55,Z(0),675,Z(0))
b+=line(90,Z(380),200,Z(380),'#324c42')+line(135,Z(152),245,Z(152),'#324c42')
b+=text(50,165,'Deck +500',13)+text(240,370,'Tread +250',13)+text(245,520,'Rail bottom+78 /concrete+77.25',12)
b+=text(50,600,'Inner rim directly bears on front bearer; cleat head forms part of outer rim layer.',12)
b+=text(710,155,'F5 · Seven H4cleats',16)+text(710,186,'140×45, cut414',14)+text(710,217,'Upper bolts Z380',13)+text(710,246,'Lower bolts Z152',13)+text(710,275,'TwoM12 per row,80centres',13)+text(710,304,'M12×120 +50square washers',12)
b+=text(710,353,'Rim reaction up to5.30kN',13)+text(710,382,'Eccentric moment0.477kNm',13)+text(710,411,'Assembly capacity not verified',13)
b+=text(40,655,'F1:90×4SS ply nails, two rows≤250centres. F2:ordinary piles4×100×3.75SS skew nails.',12)
b+=text(40,685,'F3:standard joist/rim/block nails. F4:three genuineSSCPC40 hold-down pairs at rebuilt rear row.',12)
b+=text(40,715,'F6:twoM12rim ties at rebuilt/main junction. F7:complete4anchors and6outer pad restraint points.',12)
b+=text(40,748,'Front-rim reinforcement, bolt groups, stair-loaded crosspiece ends and pad restraint remain to check.',12)
b+=text(40,780,'Builder brief also checks cladding clearance, door threshold and weatherproofing.',12)
svg('fixings','Draft hanging tread fixing section and fixing schedule:seven414mmH4cleats,twoM12bolts perupper/lowerrow,mainrim directlyoverbearer;full connectioncapacityunfinished',b,h=815)
# Improve numeric text spacing without altering URLs or product classification strings.
links=[]
def protect(m):links.append(m.group(0));return '@LINK'+str(len(links)-1)+'@'
def readable(t):
 t=re.sub(r'https?://[^)\s]+',protect,t)
 t=re.sub(r'(?<=[a-z])(?=\d)',' ',t)
 t=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',t)
 t=re.sub(r'([,;:])(?=\S)',r'\1 ',t)
 t=re.sub(r'(?<=\d), (?=\d{3}(?:\.|[^\d]|$))',',',t)
 for a,b in [('inclGST','incl GST'),('gSS','g SS'),('mmcentres','mm centres'),('genuineSSCPC','genuine SSCPC'),('alongX','along X'),('faceY','face Y'),('plyY','ply Y'),('layerY','layer Y'),('atY','at Y'),('onY','on Y'),('pilesX','piles X'),('headsY','heads Y'),('centre−','centre −'),('from−','from −'),('bottom+','bottom +'),('top+','top +'),('DPC0','DPC 0'),('NZS360','NZS 360')]:t=t.replace(a,b)
 for j,url in enumerate(links):t=t.replace('@LINK'+str(j)+'@',url)
 return t
# Master text remains one source page; keep URLs intact.
text_md=(root/'CURRENT_DESIGN.md').read_text();(root/'CURRENT_DESIGN.md').write_text(readable(text_md))
# Apply the same readable numeric spacing to page text and drawing labels.
p=root/'site/index.html';chunks=re.split(r'(<[^>]+>)',p.read_text());p.write_text(''.join(c if c.startswith('<') else readable(c) for c in chunks))
for p in (root/'site/drawings').glob('*.svg'):
 p.write_text(re.sub(r'(<text[^>]*>)(.*?)(</text>)',lambda m:m.group(1)+readable(m.group(2))+m.group(3),p.read_text()))
