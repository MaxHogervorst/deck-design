const assemblyNS = 'http://www.w3.org/2000/svg';
const assemblyInk = '#244c3b';
const assemblyArrow = '#a15e19';
let assemblySequence = 0;
function assemblyEl(tag, attrs = {}, children = []) {
  const node = document.createElementNS(assemblyNS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
  for (const child of children) node.append(child);
  return node;
}
function assemblyAdd(svg, tag, attrs = {}) { const node = assemblyEl(tag, attrs); svg.append(node); return node; }
function assemblyText(svg, x, y, value, attrs = {}) {
  const node = assemblyAdd(svg, 'text', { x, y, 'font-family': 'inherit', 'font-size': 13, fill: assemblyInk, ...attrs });
  node.textContent = value; return node;
}
function assemblyLine(svg, x1, y1, x2, y2, attrs = {}) { return assemblyAdd(svg, 'line', { x1, y1, x2, y2, stroke: assemblyInk, 'stroke-width': 1.5, ...attrs }); }
function assemblyRect(svg, x, y, width, height, attrs = {}) { return assemblyAdd(svg, 'rect', { x, y, width, height, fill: '#edf2ed', stroke: assemblyInk, 'stroke-width': 1.5, ...attrs }); }
function assemblyArrowLine(svg, x1, y1, x2, y2, color = assemblyArrow) {
  assemblyLine(svg, x1, y1, x2, y2, { stroke: color, 'stroke-width': 2.3 });
  const angle = Math.atan2(y2 - y1, x2 - x1);
  for (const offset of [-.52, .52]) assemblyLine(svg, x2, y2, x2 - 9 * Math.cos(angle + offset), y2 - 9 * Math.sin(angle + offset), { stroke: color, 'stroke-width': 2.3 });
}
function assemblyDim(svg, x1, x2, y, label) {
  assemblyLine(svg, x1, y, x2, y, { stroke: '#89968e' });
  for (const x of [x1, x2]) assemblyLine(svg, x, y - 4, x, y + 4, { stroke: '#89968e' });
  assemblyText(svg, (x1 + x2) / 2, y - 7, label, { 'text-anchor': 'middle', fill: '#53645a', 'font-size': 12 });
}
function assemblyPart(svg, x, y, label) {
  assemblyAdd(svg, 'circle', { cx: x, cy: y, r: 13, fill: '#fff', stroke: assemblyInk, 'stroke-width': 1.4 });
  assemblyText(svg, x, y + 4, label, { 'text-anchor': 'middle', 'font-size': 10, 'font-weight': 700 });
}
function assemblyNote(svg, value) { assemblyText(svg, 24, 283, value, { 'font-size': 11, fill: '#6a736c' }); }
const assemblyJoistCentres = [22.5, 450, 877.5, ...Array.from({ length: 13 }, (_, i) => 877.5 + 5700 / 13 * (i + 1))];
const assemblyBlockRows = [-1947.5, -1562.5, -1177.5, -792.5, -407.5, -22.5];
const assemblyPileX = [250, 1470, 2690, 3910, 5130, 6350];
const assemblyDescriptions = {
  setout: ['Mark all three finished outlines', 'One set-out for the main deck 6600 by 2600, rebuilt section 900 by 1970 and single tread 6600 by 400 millimetres. Main-deck diagonals approximately 7094 millimetres. Rebuilt and tread outlines are schematic.'],
  'pile-grid': ['Mark proposed support centres', 'Twelve proposed main pile positions at six X stations on bearer centre lines Y350 and Y2250. Pile classes and footing sizes remain unassigned.'],
  bearer: ['Lower bearer plies onto the specified pile connection', 'Exploded arrangement of two side-by-side bearer plies, separation and pile top. Connection symbol is a placeholder, not a bolt or nail pattern.'],
  joists: ['Position J01 to J16 and RM1/RM2 rims', 'Sixteen proposed joist lines. J01 to J03 continue as candidates through the rebuilt area. RM1 is the front rim line; RM2 is the rear rim, interrupted around the three continuation joists. Rim joints require AP01. This is a layout illustration, not verified cut lengths or bearing detail.'],
  blocking: ['Fit B01 to B12 flush', 'Twelve nominal 382.5 millimetre cross-blocks between three long joists, in six rows at 385 millimetre centres. Block-end connections require the reviewed fixing detail.'],
  boards: ['Fix boards across their supports', 'Main boards run across joists. Rebuilt boards turn ninety degrees and fix at the flush cross-block rows. Two fixing dots per crossing are illustrative.'],
  'tread-box': ['Assemble one tread ladder', 'Two nominal 6600 millimetre rails and sixteen nominal 310 millimetre crosspieces make a 6600 by 400 single-layer tread frame. Exact cuts and joints remain to specify.'],
  'tread-ground': ['Typical tread bearing and restraint', 'Provisional load path: timber rail bears through specified separation onto a concrete plinth or footing; a side connector and concrete anchor provide restraint. F is a typical concrete foundation, DPC the separation, C1 the side connector, C2 the concrete anchor and C3 timber-to-connector fixings. Timber bears directly through separation onto concrete, not suspended from the unverified side connector. Connector, fixings, anchor and foundation sizes are not specified. No loose paver or shallow footing is implied.'],
  'tread-boards': ['Lower the tread boards onto the frame', 'Three illustrative board rows sit on a single 140 millimetre frame layer. Board thickness 38 and selected surface 250 give a nominal frame underside 72 millimetres above garden. Product gaps and fixings remain to specify.'],
  finish: ['Check the finished levels', 'Side profile of main deck surface about 500 millimetres and one tread surface 250 above garden, with 400 millimetres total tread projection. These selected levels are not an access-compliance finding.']
};
function assemblySetout(svg) {
  const x=125,y=125,s=.044,w=6600*s,h=2600*s;
  assemblyRect(svg,x,y,w,h,{fill:'#fff','data-part':'main-outline'});
  assemblyRect(svg,x,y-1970*s,900*s,1970*s,{fill:'#edf4ec','stroke-dasharray':'4 3','data-part':'rebuilt-outline'});
  assemblyRect(svg,x,y+h,w,400*s,{fill:'#f8efe1','stroke-dasharray':'4 3','data-part':'tread-outline'});
  assemblyLine(svg,x,y,x+w,y+h,{'stroke-dasharray':'5 4',stroke:'#8b968d'});
  assemblyLine(svg,x,y+h,x+w,y,{'stroke-dasharray':'5 4',stroke:'#8b968d'});
  assemblyDim(svg,x,x+w,109,'6600');
  assemblyText(svg,105,190,'2600',{'transform':'rotate(-90 105 190)','text-anchor':'middle'});
  assemblyText(svg,285,185,'7094 ↔ 7094',{'text-anchor':'middle','font-size':17,'font-weight':650,'paint-order':'stroke',stroke:'#fff','stroke-width':6});
  assemblyText(svg,180,63,'900 × 1970 rebuilt',{'font-size':11});
  assemblyText(svg,270,252,'ONE TREAD · 6600 × 400',{'font-size':10,'text-anchor':'middle'});
  assemblyNote(svg,'One baseline for all areas. Keep both main-deck diagonals equal.');
}
function assemblyPileGrid(svg) {
  const x0=65,y0=63,s=.065;
  assemblyRect(svg,x0,y0,6600*s,2600*s,{fill:'#fff'});
  let n=0;
  for(const y of [350,2250]) {
    assemblyLine(svg,x0,y0+y*s,x0+6600*s,y0+y*s,{stroke:'#be925d','stroke-width':5});
    for(const x of assemblyPileX){
      assemblyRect(svg,x0+x*s-5,y0+y*s-5,10,10,{fill:'#fff','data-part':'proposed-pile'});
      assemblyText(svg,x0+x*s,y0+y*s-13,`P${String(++n).padStart(2,'0')}`,{'text-anchor':'middle','font-size':10});
    }
  }
  assemblyDim(svg,x0+250*s,x0+1470*s,47,'1220 typical');
  assemblyText(svg,505,y0+350*s+4,'A',{'font-weight':700});assemblyText(svg,505,y0+2250*s+4,'B',{'font-weight':700});
  assemblyRect(svg,x0,y0+2600*s,6600*s,400*s,{fill:'none','stroke-dasharray':'4 3','data-part':'tread-foundation-zone'});
  assemblyText(svg,279,252,'Tread foundations: GP01 positions / count TBD',{'font-size':10,'text-anchor':'middle'});
  assemblyNote(svg,'P01–P12: proposed main piles only. Include tread foundations in the same work.');
}
function assemblyBearer(svg) {
  assemblyRect(svg,210,163,125,92,{fill:'#eef0eb','data-part':'pile'});assemblyText(svg,272,229,'H5 pile',{'text-anchor':'middle'});
  assemblyRect(svg,207,153,131,5,{fill:'#758077','data-part':'separation'});
  assemblyRect(svg,183,48,44,71,{fill:'#e8d1af','data-part':'bearer-ply','data-part-id':'BA-1'});assemblyRect(svg,244,48,44,71,{fill:'#e8d1af','data-part':'bearer-ply','data-part-id':'BA-2'});
  assemblyText(svg,195,34,'2 × 140 × 45',{'font-weight':650});
  assemblyArrowLine(svg,205,124,232,145);assemblyArrowLine(svg,266,124,278,145);
  assemblyPart(svg,158,82,'BA-1');assemblyPart(svg,315,82,'BA-2');
  assemblyLine(svg,340,155,388,137);assemblyText(svg,393,141,'DPC / separation',{'font-size':12});
  assemblyRect(svg,338,181,52,40,{fill:'none','stroke-dasharray':'5 4'});assemblyText(svg,400,194,'Specified',{'font-size':12});assemblyText(svg,400,211,'connector',{'font-size':12});
  assemblyNote(svg,'Repeat for BB-1 / BB-2. Connector shown is a placeholder, not a fixing pattern.');
}
function assemblyJoists(svg) {
  const x0=100,y0=129,s=.054;
  assemblyRect(svg,x0,y0,6600*s,2600*s,{fill:'#fff'});
  for(const y of[350,2250])assemblyRect(svg,x0,y0+(y-45)*s,6600*s,90*s,{fill:'#edd1a8',stroke:'#9a703b'});
  for(const [i,x] of assemblyJoistCentres.entries()){
    if(i<3)assemblyRect(svg,x0+(x-22.5)*s,y0-1970*s,45*s,1970*s,{fill:'#edf5e9','stroke-dasharray':'4 3','data-part':'candidate-continuation'});
    assemblyRect(svg,x0+(x-22.5)*s,y0+(i<3?0:45*s),45*s,(i<3?2555:2510)*s,{fill:'#456b4c',stroke:'#244c3b','data-part':'main-joist'});
    assemblyText(svg,x0+x*s,y0+17,`${i+1}`,{'text-anchor':'middle','font-size':9,'paint-order':'stroke',stroke:'#fff','stroke-width':3});
  }
  assemblyRect(svg,x0,y0+2555*s,6600*s,45*s,{fill:'#d6b788',stroke:'#87683d','data-part':'rim','data-part-id':'RM1'});
  for(const [start,end] of [[45,427.5],[472.5,855],[900,6600]]) assemblyRect(svg,x0+start*s,y0,(end-start)*s,45*s,{fill:'#d6b788',stroke:'#87683d','data-part':'rim','data-part-id':'RM2'});
  assemblyText(svg,464,274,'RM1',{'font-size':11});
  assemblyText(svg,62,127,'RM2',{'font-size':11});
  assemblyText(svg,120,35,'J01–J03: rebuilt + main candidate',{'font-size':12});
  assemblyText(svg,330,109,'J04–J16: main',{'font-size':12});
  assemblyArrowLine(svg,320,70,320,120);
  assemblyNote(svg,'16 joist lines. RM1/RM2 joints: AP01. Envelopes are not cut lengths.');
}
function assemblyBlocking(svg) {
  const x0=135,y0=36,s=.1;
  for(const [i,x] of assemblyJoistCentres.slice(0,3).entries()){
    assemblyRect(svg,x0+(x-22.5)*s,y0,45*s,1970*s,{fill:'#e3ece0','data-part':'long-joist'});
    assemblyText(svg,x0+x*s,y0-10,`J0${i+1}`,{'text-anchor':'middle','font-size':11});
  }
  let n=0;
  for(const row of assemblyBlockRows)for(const left of[45,472.5]){
    const y=y0+(row+1970-22.5)*s;
    assemblyRect(svg,x0+left*s,y,382.5*s,45*s,{fill:'#b2ced9',stroke:'#416b7c','data-part':'cross-block'});
    if(n<2)assemblyText(svg,x0+(left+191.25)*s,y+19,`B${String(n+1).padStart(2,'0')}`,{'text-anchor':'middle','font-size':10});
    n++;
  }
  assemblyArrowLine(svg,270,65,224,65);assemblyText(svg,285,67,'B01–B12',{'font-weight':650});
  assemblyText(svg,285,99,'2 pieces per row');assemblyText(svg,285,126,'6 rows × 385 centres');assemblyText(svg,285,153,'382.5 clear per block');assemblyText(svg,285,187,'TOPS FLUSH',{'font-weight':700});
  assemblyNote(svg,'No extra batten layer. Block-end fixings follow the reviewed detail.');
}
function assemblyBoardsPanel(svg,x0,y0,rotated) {
  assemblyRect(svg,x0,y0,190,155,{fill:'#fff'});
  if(!rotated){
    for(const x of[22,78,134])assemblyRect(svg,x0+x,y0,8,155,{fill:'#acc5aa'});
    for(const y of[25,68,111]){
      assemblyRect(svg,x0,y0+y,190,30,{fill:'#e5cbA5','fill-opacity':.75,'data-part':'main-board'});
      for(const x of[26,82,138])for(const dy of[7,23])assemblyAdd(svg,'circle',{cx:x0+x,cy:y0+y+dy,r:2,fill:'#934b31'});
    }
    assemblyArrowLine(svg,x0+35,y0+174,x0+155,y0+174);
  }else{
    for(const y of[15,65,115])assemblyRect(svg,x0,y0+y,190,8,{fill:'#a6c6d2'});
    for(const x of[25,77,129]){
      assemblyRect(svg,x0+x,y0,36,155,{fill:'#e5cba5','fill-opacity':.75,'data-part':'rebuilt-board'});
      for(const y of[19,69,119])for(const dx of[9,27])assemblyAdd(svg,'circle',{cx:x0+x+dx,cy:y0+y,r:2,fill:'#934b31'});
    }
    assemblyArrowLine(svg,x0+207,y0+25,x0+207,y0+132);
  }
}
function assemblyBoards(svg) {
  assemblyText(svg,45,34,'MAIN DECK',{'font-weight':650});assemblyText(svg,305,34,'REBUILT SECTION',{'font-weight':650});
  assemblyBoardsPanel(svg,40,55,false);assemblyBoardsPanel(svg,300,55,true);
  assemblyText(svg,40,252,'Boards cross joists',{'font-size':12});assemblyText(svg,300,252,'Boards cross added blocks',{'font-size':12});
  assemblyText(svg,40,274,'Then fix the tread boards using the same DF01 schedule.',{'font-size':11});
  assemblyNote(svg,'All framing / concealed fixings complete before boards. Dots are examples.');
}
function assemblyTreadBox(svg) {
  const x0=55,y0=110,s=.067;
  assemblyRect(svg,x0,65,6600*s,7,{fill:'#e8caa0','data-part':'tread-rail'});assemblyPart(svg,31,68,'R1');
  assemblyRect(svg,x0,205,6600*s,7,{fill:'#e8caa0','data-part':'tread-rail'});assemblyPart(svg,31,209,'R2');
  for(const [i,x] of assemblyJoistCentres.entries()){
    const px=x0+(x-22.5)*s;
    assemblyRect(svg,px,y0,45*s,65,{fill:'#a9c09e','data-part':'tread-crosspiece'});
    if([0,7,15].includes(i))assemblyText(svg,px+2,y0-10,`T${String(i+1).padStart(2,'0')}`,{'text-anchor':'middle','font-size':10});
  }
  for(const x of[155,360]){assemblyArrowLine(svg,x,82,x,103);assemblyArrowLine(svg,x,195,x,180);}
  assemblyDim(svg,x0,x0+6600*s,45,'6600 outer');assemblyText(svg,444,245,'400 outer',{'font-size':12});
  assemblyText(svg,180,246,'R1 + R2 · 16 × T pieces · one layer',{'text-anchor':'middle','font-size':12});
  assemblyNote(svg,'Exploded view. T clear length 310 nominal; exact cuts / joints follow the plan.');
}
function assemblyTreadGround(svg) {
  assemblyRect(svg,225,91.6,31.5,98,{fill:'#e6cca5','data-part':'rail'});
  assemblyRect(svg,218,190,45,4,{fill:'#68736b','data-part':'separation','data-part-id':'DPC'});
  assemblyRect(svg,150,194,180,69,{fill:'#edf0ed',stroke:'none','data-part':'concrete-footing','data-part-id':'F'});
  assemblyAdd(svg,'path',{d:'M150 263 V194 H330 V263',fill:'none',stroke:assemblyInk,'stroke-width':1.5});
  // The footing deliberately extends below the soil and ends with a break, not a sized shallow pad.
  assemblyLine(svg,30,240,150,240,{stroke:'#8c8d77'});assemblyLine(svg,330,240,530,240,{stroke:'#8c8d77'});
  for(let x=35;x<530;x+=14)if(x<150||x>337)assemblyLine(svg,x,241,x-7,248,{stroke:'#b2b3a5','stroke-width':.8});
  assemblyAdd(svg,'path',{d:'M255 132 V194 H300',fill:'none',stroke:'#627e88','stroke-width':5,'data-part':'restraint-angle','data-part-id':'C1'});
  assemblyAdd(svg,'circle',{cx:252,cy:151,r:4,fill:'#fff',stroke:'#627e88','stroke-width':2,'data-part':'timber-fixing-symbol','data-part-id':'C3'});
  assemblyLine(svg,285,181,285,258,{stroke:'#627e88','stroke-width':3,'stroke-dasharray':'0'});
  assemblyRect(svg,279,185,12,5,{fill:'#627e88',stroke:'#627e88','data-part':'concrete-anchor-symbol','data-part-id':'C2'});
  assemblyAdd(svg,'path',{d:'M150 263 l15 -5 15 10 15 -10 15 10 15 -10 15 10 15 -10 15 10 15 -10 15 10 15 -10 15 5',fill:'none',stroke:assemblyInk,'stroke-width':1.5,'data-part':'foundation-depth-break'});
  assemblyArrowLine(svg,240,36,240,78,assemblyInk);assemblyText(svg,180,27,'BEARING',{'font-weight':700,'font-size':12});
  assemblyLine(svg,257,136,342,91);assemblyText(svg,348,85,'C1 · Side connector',{'font-size':12});assemblyText(svg,348,102,'resists movement',{'font-size':11});
  assemblyLine(svg,290,213,357,165);assemblyText(svg,364,160,'C2 · Concrete anchor',{'font-size':12});assemblyText(svg,364,177,'type / embedment TBD',{'font-size':11});
  assemblyLine(svg,220,192,107,169);assemblyText(svg,29,153,'DPC · Separation',{'font-size':11});assemblyText(svg,29,169,'rail bears on concrete',{'font-size':11});
  assemblyText(svg,32,218,'SOIL',{'font-size':11});assemblyText(svg,348,228,'F · Typical foundation',{'font-size':11});
  assemblyLine(svg,158,114,249,151,{stroke:'#627e88'});assemblyText(svg,30,116,'C3 · Timber fixings',{'font-size':11});
  assemblyText(svg,348,249,'Size / depth to specify',{'font-size':11});
  assemblyNote(svg,'Typical bearing only. Foundation count / sizes and C1–C3 fixings: GP01.');
}
function assemblyTreadBoards(svg) {
  assemblyRect(svg,80,155,400,98,{fill:'#e2eadc','data-part':'tread-frame'});
  for(const [i,[x,width]] of[[80,126],[211,138],[354,126]].entries()){
    assemblyRect(svg,x,53,width,26.6,{fill:'#e7cba3','data-part':'tread-board','data-part-id':`TD${i+1}`});
    assemblyText(svg,x+width/2,43,`TD${i+1}`,{'text-anchor':'middle','font-size':11});assemblyArrowLine(svg,x+width/2,95,x+width/2,143);
  }
  assemblyText(svg,104,183,'140 frame',{'font-weight':600});assemblyText(svg,277,211,'ONE LAYER',{'font-weight':700});
  assemblyText(svg,80,262,'38 boards → 250 surface / 72 underside',{'font-size':12});
  assemblyNote(svg,'TD1–TD3 illustrated only. Actual widths, gaps, edge rips and fixings follow the product.');
}
function assemblyFinish(svg) {
  assemblyAdd(svg,'path',{d:'M50 71 H244 V166 H396 V261 H520',fill:'none',stroke:assemblyInk,'stroke-width':4,'data-part':'one-tread-profile'});
  assemblyText(svg,106,54,'DECK',{'font-weight':700});assemblyText(svg,282,147,'ONE TREAD',{'font-weight':700});assemblyText(svg,426,244,'GARDEN',{'font-weight':700});
  assemblyText(svg,259,116,'250 rise',{'font-size':12});assemblyText(svg,408,205,'250 rise',{'font-size':12});
  assemblyDim(svg,244,396,193,'400 projection');
  assemblyLine(svg,27,71,27,261,{stroke:'#89968e'});assemblyText(svg,19,166,'500',{'transform':'rotate(-90 19 166)','text-anchor':'middle','font-size':12});
  assemblyText(svg,280,23,'CURRENT LEVELS · HOLD',{'text-anchor':'middle','font-size':13,'font-weight':700,fill:assemblyArrow});
  assemblyNote(svg,'250 + 250 rises exceed BRANZ common/main private 190 mm guidance.');
}

export function renderAssemblyDiagram(svg, type) {
  const entry=assemblyDescriptions[type]||assemblyDescriptions.setout;
  const id=`assembly-${++assemblySequence}`;
  svg.replaceChildren();svg.setAttribute('viewBox','0 0 560 300');svg.setAttribute('role','img');svg.setAttribute('aria-labelledby',`${id}-title ${id}-desc`);svg.setAttribute('data-assembly-type',type);
  const title=assemblyEl('title',{id:`${id}-title`});title.textContent=entry[0];
  const description=assemblyEl('desc',{id:`${id}-desc`});description.textContent=entry[1];
  svg.append(title,description,assemblyEl('rect',{width:560,height:300,fill:'#fff'}));
  const draw={setout:assemblySetout,'pile-grid':assemblyPileGrid,bearer:assemblyBearer,joists:assemblyJoists,blocking:assemblyBlocking,boards:assemblyBoards,'tread-box':assemblyTreadBox,'tread-ground':assemblyTreadGround,'tread-boards':assemblyTreadBoards,finish:assemblyFinish};
  (draw[type]||assemblySetout)(svg);
}
