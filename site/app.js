const green='#456b54', timber='#cba773', concrete='#d6dad7', soil='#ece5d6';
const line=(x1,y1,x2,y2,color='#71847b',width=1,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const rect=(x,y,w,h,fill,stroke='#52675b')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}"/>`;
const label=(x,y,t,size=13,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}">${t}</text>`;
const svg=(body,w=900,h=650,title='Design drawing')=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" role="img" aria-label="${title}"><title>${title}</title>${body}</svg>`;
const joists=[22.5,307.5,592.5,877.5,...Array.from({length:15},(_,i)=>1257.5+i*380)];
const supports=[300,1300,2300,3100,4300,5300,6300];
const pileXs=[250,1067.5,1660,2967.5,3910,5130,6007.5,6525];
const anchors=[1067.5,2967.5,6007.5];
const crosspieces=[...Array.from({length:18},(_,i)=>22.5+380*i),6577.5];
function overall(){
 const s=.103,X=x=>95+x*s,Y=y=>280+y*s;
 let b=label(95,24,'PLAN · timber deck + pine box tread',17)+label(95,46,'Proposed geometry; concrete tread supports shown as trial heads only',12);
 b+=rect(X(0),Y(0),6600*s,2600*s,'#f5f7f2')+rect(X(0),Y(-1970),900*s,1970*s,'#f5f7f2');
 for(const y of[350,2250])b+=rect(X(0),Y(y-45),6600*s,90*s,timber);
 for(const y of[-800,-1795])b+=rect(X(0),Y(y-45),900*s,90*s,timber);
 joists.forEach((x,i)=>{b+=rect(X(x-22.5),Y(i<4?-1970:0),45*s,(i<4?4570:2600)*s,green);if(i>=4)b+=label(X(x),Y(0)-12,`J${String(i+1).padStart(2,'0')}`,9,'middle');});
 [350,2250].forEach(y=>pileXs.forEach(x=>b+=rect(X(x-62.5),Y(y-62.5),125*s,125*s,anchors.includes(x)?'#af6b3c':'#314b3c')));
 [-800,-1795].forEach(y=>[175,725].forEach(x=>b+=rect(X(x-62.5),Y(y-62.5),125*s,125*s,'#314b3c')));
 [2352.5,3872.5].forEach(x=>b+=rect(X(x-22.5),Y(45),45*s,2510*s,green));
 b+=label(210,113,'Rebuilt 900 × 1970',13)+label(210,137,'Four continuous joists',11)+label(210,163,'New rear bearer; no retained-beam reliance',11);
 b+=label(210,Y(-800)+4,'BC · 900 double bearer / two piles',11);
 b+=label(782,Y(350)+4,'BA',12)+label(782,Y(2250)+4,'BB',12);
 b+=rect(X(0),Y(2600),6600*s,400*s,'#faf3e4');
 supports.forEach(x=>b+=rect(X(x-250),Y(2600),500*s,400*s,concrete));
 [2600,2910].forEach(y=>b+=rect(X(0),Y(y),6600*s,90*s,timber));
 crosspieces.forEach(x=>b+=rect(X(x-22.5),Y(2690),45*s,220*s,green));
 b+=line(X(0),Y(3090),X(6600),Y(3090))+label(X(3300),Y(3290),'6600',14,'middle');
 b+=label(95,670,'20 deck/rebuilt piles · six brown anchor heads · seven trial concrete tread pads',12);
 b+=label(30,Y(1300),'2600',12)+label(28,Y(2850),'400',12);
 return svg(b,900,700,'Overall plan: nineteen base joists, two sisters, twenty deck piles and seven concrete supports under a timber box tread');
}
function mainSection(){
 const Z=z=>465-z*.6;
 let b=label(45,35,'MAIN DECK · what the 100 mm proposal means',19)+label(45,62,'Surface and lawn heights stay; only the soil under the deck is proposed lower',12);
 b+=rect(55,Z(0),75,165,soil,'none')+rect(130,Z(-100),575,105,soil,'none')+rect(705,Z(0),190,165,soil,'none');
 b+=line(55,Z(0),130,Z(0))+line(130,Z(0),130,Z(-100))+line(130,Z(-100),705,Z(-100))+line(705,Z(-100),705,Z(0))+line(705,Z(0),895,Z(0));
 b+=line(130,Z(0),705,Z(0),'#8a968e',1,'5 4');
 b+=rect(185,Z(-100),150,100,concrete)+rect(225,Z(187.25),75,Z(-210)-Z(187.25),timber);
 b+=rect(145,Z(328),500,84,timber)+rect(130,Z(468),530,84,green)+rect(120,Z(500),550,19.2,'#e0bf8e');
 b+=line(145,Z(188),645,Z(188),'#313d36',2);
 b+=line(220,Z(67.25),310,Z(67.25),'#a35c39',3);
 b+=line(350,Z(67.25),350,Z(-100),'#a35c39',2)+line(343,Z(67.25),357,Z(67.25),'#a35c39',2)+line(343,Z(-100),357,Z(-100),'#a35c39',2);
 b+=label(365,490,'167.25 mm',14)+label(365,510,'cut clearance',11);
 [[500,'+500 pine surface'],[468,'+468 board underside'],[328,'+328 joist underside'],[188,'+188 bearer underside']].forEach(([z,t])=>b+=label(695,Z(z)+5,t,12));
 b+=label(160,360,'Pile top +187.25 / 0.75 DPC',12)+label(45,415,'Lowest example cut +67.25',12)+line(205,419,220,Z(67.25),'#a35c39');
 b+=label(715,Z(0)-12,'0 · surrounding lawn',12)+label(715,Z(-100)+5,'−100 · soil under deck',12);
 b+=label(45,650,'CLEARANCE: selected processed pile surfaces require 150 mm above soil.',13);
 b+=label(45,679,'DRAINAGE: measure a real lower outlet before accepting the soil lowering.',13);
 b+=label(45,708,'If there is no outlet, revise the anchor/ground detail before digging a basin.',12);
 b+=label(45,747,'The 100 mm comes from six anchor heads; it is not a rule for every low deck.',12);
 b+=label(45,776,'Main footing depths are measured below the actual proposed ground; shown broken/schematic.',11);
 return svg(b,960,810,'Main deck clearance proposal: surface stays500, surrounding lawn0, soil under deck minus100, lowest example anchor cut67.25 gives167.25 clearance; drainage outlet must be measured');
}
function treadSection(){
 let b=label(45,32,'TREAD · ordinary box, short boards, concrete pads',19)+label(45,57,'Proposed geometry; full foundation/restraint assembly still needs verification',12);
 const X=x=>80+x*.112,Y=y=>115+y*.34;
 b+=label(45,91,'PLAN · 6600 × 400; seven pads, maximum 1200 centre interval',14);
 b+=rect(X(0),Y(0),6600*.112,400*.34,'#f5f7f2');
 supports.forEach(x=>{b+=rect(X(x-250),Y(0),500*.112,400*.34,concrete);b+=label(X(x),Y(400)+23,String(x),10,'middle');});
 [0,310].forEach(y=>b+=rect(X(0),Y(y),6600*.112,90*.34,timber));
 crosspieces.forEach(x=>b+=rect(X(x-22.5),Y(90),45*.112,220*.34,green));
 b+=label(45,307,'400 mm boards run front-to-back and bear directly on both doubled rails.',12);
 b+=label(45,342,'SECTION · lower crosspieces brace the box; they do not carry walking load',13);
 const C=y=>230+y*1.1,Z=z=>650-z;
 b+=rect(150,Z(0),620,150,soil,'none')+line(150,Z(0),770,Z(0));
 b+=rect(C(-50),Z(-100),500*1.1,45,concrete)+rect(C(0),Z(77.25),400*1.1,177.25,concrete);
 b+=line(C(-50),Z(-100)+45,C(450),Z(-100)+45,'#71847b',2,'5 4');
 b+=rect(C(0),Z(250),440,32,'#e0bf8e');
 [0,310].forEach(y=>{b+=rect(C(y),Z(218),99,140,timber);b+=line(C(y+45),Z(218),C(y+45),Z(78));b+=line(C(y),Z(77.6),C(y+90),Z(77.6),'#313d36',2);});
 b+=rect(C(90),Z(168),220*1.1,90,green);
 b+=label(470,Z(190),'50 mm clear over blocks',11,'middle');
 b+=label(755,Z(250)+5,'+250 pine',12)+label(755,Z(218)+5,'+218 rail top',12)+label(755,Z(78)+2,'+78 rail bottom',12)+label(755,Z(77.25)+25,'+77.25 concrete',12)+label(755,Z(0)+5,'0 garden/path',12);
 b+=label(45,693,'PROPOSED PADS: 500-square buried base, bottom −450 / top −100.',12);
 b+=label(45,719,'Head 500 along X × 400 across tread, top +77.25; 25 MPa concrete.',12);
 b+=label(45,830,'Plain pine rail; concrete may show below it. Keep landscaping clear of timber.',12);
 return svg(b,960,855,'Pine box tread with short400mm boards on doubled140deep rails; nineteen lower90deep blocks; seven proposed500square bases and500by400heads, concrete top77.25');
}
function fixingDetail(){
 let b=label(45,35,'TREAD RESTRAINT · selected candidate, design hold',19)+label(45,62,'Pryda PBB0140/SS · 140 long × 75 upright × 50 foot · actual PDS thickness 4 mm',12);
 b+=label(45,100,'SIDE SECTION · two bolts/anchors along the rail project onto this same view',12);
 b+=rect(220,268.5,180,280,timber)+line(310,268.5,310,548.5);
 b+=rect(220,548.5,180,1.5,'#313d36')+rect(190,550,390,135,concrete);
 b+=rect(400,400,8,150,'#8f9f9b')+rect(400,542,100,8,'#8f9f9b');
 b+=line(205,450,425,450,'#324c42',7)+rect(208,425,6,50,'#8f9f9b')+rect(410,425,6,50,'#8f9f9b');
 b+=line(450,538,450,660,'#71847b',4,'6 4');
 b+=label(220,240,'90 mm doubled rail',14);
 b+=label(45,380,'2 × M12 timber bolts',12)+label(45,404,'100 mm along rail',12)+label(45,476,'49.25 mm lower edge',12)+label(45,500,'48 mm minimum criterion',12);
 b+=label(540,345,'14 angles total',14)+label(540,374,'28 M12 × 130 SS316 timber bolts',12)+label(540,402,'50 × 50 × 3 washers; fit to confirm',12);
 b+=label(540,445,'Two outer holes; centre unused',12)+line(430,450,525,445);
 b+=label(540,574,'28 Ramset T12110SSX anchors',12)+label(540,600,'81 mm effective depth at 4 mm fixture',12)+line(455,604,525,590);
 b+=label(45,724,'Footing/bolt/anchor capacity must be checked as a complete assembly before purchase.',12);
 b+=label(45,754,'Check bend/prying, timber splitting/group action, concrete edges and load combinations.',12);
 b+=label(45,790,'This is a proposal diagram, not a drilling template or a pre-rated kit.',13);
 return svg(b,960,820,'Held tread restraint proposal PBB0140 stainless4mm angle with two outerM12 timber bolts and two concrete anchors per angle; lower timber edge49.25mm; full assembly capacity unfinished');
}
const views={
 plan:[overall,'Continuous 6.6 m bearer/rail plies remove planned splices. Fresh main/rebuilt proposal: 20 piles, including six anchors positioned between ordinary joists. Tread uses seven concrete-pad candidates.'],
 main:[mainSection,'The 100 mm proposal concerns soil beneath the main deck, not the walking heights. Confirm complete anchor fit/bracing and a drainage outlet before excavation.'],
 tread:[treadSection,'Concrete supports replace short timber piles. Short boards bear directly on rails; lower crosspieces brace the box. Dimensioned pads are proposed; the complete foundation/restraint assembly is not released.'],
 fixings:[fixingDetail,'The wider PBB0140/SS replaces the small-angle candidate. Published geometry and favourable component screens do not establish the full assembly capacity; keep these items on design hold.']
};
function show(view){const[draw,caption]=views[view];document.querySelector('#drawing').innerHTML=draw();document.querySelector('#drawing-caption').textContent=caption;document.querySelector('#drawing-panel').setAttribute('aria-labelledby',`tab-${view}`);document.querySelectorAll('[data-view]').forEach(b=>{const selected=b.dataset.view===view;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;});}
document.querySelectorAll('[data-view]').forEach(button=>{button.onclick=()=>show(button.dataset.view);button.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const keys=Object.keys(views),i=keys.indexOf(button.dataset.view),next=e.key==='Home'?0:e.key==='End'?keys.length-1:(i+(e.key==='ArrowRight'?1:keys.length-1))%keys.length;show(keys[next]);document.querySelector(`#tab-${keys[next]}`).focus();};});
const steps=[
 ['Set datums and mark all footprints','Tape, strings, level','Mark main 6600 × 2600, rebuilt 900 × 1970 and tread 6600 × 400. Check main diagonal 7093.7 and tread diagonal 6612.1 mm; establish actual finished ground and a drainage outlet before adopting the proposed 100 mm lowering under the main deck.'],
 ['Mark piles and concrete tread supports','Tape, paint, complete foundation plan','Locate services before digging. Mark 20 deck/rebuilt pile locations and the agreed tread supports. Buried foundations may extend outside the tread; coordinate with the path and garden.'],
 ['Excavate all foundations','Spade or auger, depth rod','Use the agreed hole/pad dimensions and bearing levels. Check actual soil against the complete plan; resolve variations before concrete.'],
 ['Set piles and tread support forms','Level, clamps, braces, formwork','Keep treated pile bottoms intact; check grade marks, embedment and allowed top processing. Set tread bearing forms to the agreed level, nominally +77.25 with 0.75 mm DPC.'],
 ['Place concrete and allow it to cure','Specified concrete, placement tools','Maintain pile alignment and accurate tread bearing levels. Follow the agreed concrete, cure, loading and anchor installation requirements.'],
 ['Assemble continuous doubled bearers','Clamps, saw, specified nails/connectors','Cut 6600 mm main plies from 7200 stock; no main bearer seams. Fit the two rebuilt bearers, ply fixings, direct bearings and complete low anchor assemblies.'],
 ['Fit main joists, rims and restraint','Square, saw, specified fixings','Fit four continuous and 17 short joist members including sisters. Complete rebuilt crosspieces, lateral blocks, bracing transfer and rated uplift fixings before boards.'],
 ['Assemble the single-layer tread box','Tape, square, clamps, stainless framing nails','Use continuous 6600 rail plies and 19 × 220 crosspieces in 90 × 45, bottom-flush and 50 mm below the boards. Nail crosspieces to inner 45 mm plies first, then fit outer plies; preserve bracket access and check nail clashes.'],
 ['Seat and restrain the tread','DPC, level, drill, complete anchor schedule','Seat both rails directly on the agreed concrete supports with DPC. Install the designed stainless restraints; the illustrated bracket is a candidate until rated. Keep the opening and drainage clear.'],
 ['Lay the 32 mm pine boards','Spacers, saw, drill/driver, matching screws','Measure actual width/moisture and use supplier gaps. Support both ends at each seam; check edge rips, screw penetration and end distances. Main rows run along the frontage; tread boards are short 400 mm front-to-back cuts supported directly by both rails.'],
 ['Finish and check against the agreed plan','Tape, level, agreed drawings','Leave treated pine natural with required cut-end treatment. Finish path/grass/garden clear of timber; check fixings, stability, drainage and the agreed access solution. Owner checks; no builder inspection visit assumed.']
];
function stepDrawing(i){
 let b='';const ground=()=>rect(20,155,280,60,soil,'none')+line(20,155,300,155);
 if(i<2){b=rect(45,35,230,110,'#f2f5ef')+rect(45,145,230,25,'#efe2ca')+label(160,28,'6600',12,'middle')+label(160,196,i===0?'One set-out · all footprints':'Piles + concrete tread supports',12,'middle');if(i===1){[65,94,123,152,181,210,239,268].forEach(x=>b+=rect(x-6,75,12,12,timber)+rect(x-6,119,12,12,timber));[65,95,125,155,185,215,245].forEach(x=>b+=rect(x,147,12,21,concrete));}else b+=line(45,35,275,145,'#84958a',1,'4 3');}
 else if(i<5){b=ground()+rect(75,155,60,60,'white')+rect(210,155,65,60,'white');if(i>2)b+=rect(92,68,26,127,timber)+line(92,90,45,155,green,3)+rect(205,131,6,64,timber)+rect(275,131,6,64,timber);if(i===4)b+=rect(75,160,17,50,concrete)+rect(118,160,17,50,concrete)+rect(75,195,60,15,concrete)+rect(211,136,64,74,concrete);b+=label(160,35,['','','Bearing ground + agreed depths','Piles + low concrete forms','Pour both support types'][i],12,'middle');}
 else if(i===5){b=rect(70,115,30,75,timber)+rect(220,115,30,75,timber)+rect(40,77,240,19,timber)+rect(40,99,240,19,timber)+label(160,40,'Continuous double bearer plies',12,'middle');[70,110,150,190,230,270].forEach(x=>b+=rect(x,87,3,3,green));}
 else if(i===6){b=rect(40,40,240,140,'#f5f7f2');[70,120,170,220,270].forEach(x=>b+=rect(x,40,7,140,green));[70,150].forEach(y=>b+=rect(40,y,240,8,timber));b+=label(160,205,'Joists + rims + restraint',12,'middle');}
 else if(i===7){b=rect(40,65,240,16,timber)+rect(40,145,240,16,timber);[40,85,130,175,220,265].forEach(x=>b+=rect(x,81,10,64,green));b+=label(160,35,'Inner rails + crosspieces first',12,'middle')+label(160,205,'Add outer plies after end nailing',12,'middle');}
 else if(i===8){b=rect(65,148,65,65,concrete)+rect(195,148,65,65,concrete)+line(65,146,130,146,'#313d36',3)+line(195,146,260,146,'#313d36',3)+rect(45,86,230,58,timber)+label(160,35,'Direct bearing on concrete + DPC',12,'middle')+label(160,232,'Complete designed stainless restraints',11,'middle');}
 else {for(let y=45;y<180;y+=22)b+=rect(40,y,240,18,timber);if(i===9){[70,140,210,260].forEach(x=>[54,98,142].forEach(y=>b+=rect(x,y,3,3,green)));b+=label(160,208,'Supplier gaps + matching screws',12,'middle');}else b+=label(160,208,'Natural pine · clear drainage',12,'middle');}
 return svg(b,320,240,`Step ${i+1}: ${steps[i][0]}`);
}
document.querySelector('#build-steps').innerHTML=steps.map(([title,tools,check],i)=>`<details class="step" ${i===0?'open':''}><summary><span class="step-number">${String(i+1).padStart(2,'0')}</span>${title}</summary><div class="step-content">${stepDrawing(i)}<div><p><strong>Tools:</strong> ${tools}.</p><p><strong>Owner check:</strong> ${check}</p></div></div></details>`).join('');
let previousOpen=[];
window.addEventListener('beforeprint',()=>{previousOpen=[...document.querySelectorAll('details')].map(d=>d.open);document.querySelectorAll('details').forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>document.querySelectorAll('details').forEach((d,i)=>d.open=previousOpen[i]??false));
document.querySelector('#print').onclick=()=>window.print();
document.querySelector('#copy-link').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);document.querySelector('#message').textContent='Link copied.';}catch{document.querySelector('#message').textContent=`Page link: ${location.href}`;}};
show('plan');
