const green='#456b54', timber='#cba773', concrete='#d6dad7', soil='#ece5d6';
const line=(x1,y1,x2,y2,color='#71847b',width=1,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const rect=(x,y,w,h,fill,stroke='#52675b')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}"/>`;
const label=(x,y,t,size=13,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}">${t}</text>`;
const svg=(body,w=900,h=650,title='Design drawing')=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" role="img" aria-label="${title}"><title>${title}</title>${body}</svg>`;
const joists=[22.5,307.5,592.5,877.5,...Array.from({length:15},(_,i)=>1257.5+i*380)];
const supports=[300,1300,2300,3300,4300,5300,6300];
const crosspieces=[...Array.from({length:18},(_,i)=>22.5+380*i),6577.5,3277.5,3322.5];
function overall(){
 const s=.103,X=x=>95+x*s,Y=y=>280+y*s;
 let b=label(95,24,'PLAN · timber deck + pine box tread',17)+label(95,46,'Proposed geometry; concrete tread supports shown as trial heads only',12);
 b+=rect(X(0),Y(0),6600*s,2600*s,'#f5f7f2')+rect(X(0),Y(-1970),900*s,1970*s,'#f5f7f2');
 for(const y of[350,2250])b+=rect(X(0),Y(y-45),6600*s,90*s,timber);
 for(const y of[-800,-1795])b+=rect(X(0),Y(y-45),900*s,90*s,timber);
 joists.forEach((x,i)=>{b+=rect(X(x-22.5),Y(i<4?-1970:0),45*s,(i<4?4570:2600)*s,green);if(i>=4)b+=label(X(x),Y(0)-12,`J${String(i+1).padStart(2,'0')}`,9,'middle');});
 [350,2250].forEach(y=>[250,1470,2690,3910,5130,6350].forEach(x=>b+=rect(X(x-62.5),Y(y-62.5),125*s,125*s,'#314b3c')));
 [-800,-1795].forEach(y=>[175,725].forEach(x=>b+=rect(X(x-62.5),Y(y-62.5),125*s,125*s,'#314b3c')));
 [2352.5,3872.5].forEach(x=>b+=rect(X(x-22.5),Y(45),45*s,2510*s,green));
 b+=label(210,113,'Rebuilt 900 × 1970',13)+label(210,137,'Four continuous joists',11)+label(210,163,'New rear bearer; no retained-beam reliance',11);
 b+=label(210,Y(-800)+4,'BC · 900 double bearer / two piles',11);
 b+=label(782,Y(350)+4,'BA',12)+label(782,Y(2250)+4,'BB',12);
 b+=rect(X(0),Y(2600),6600*s,400*s,'#faf3e4');
 supports.forEach(x=>b+=rect(X(x-200),Y(2620),400*s,360*s,concrete));
 [2600,2910].forEach(y=>b+=rect(X(0),Y(y),6600*s,90*s,timber));
 crosspieces.forEach(x=>b+=rect(X(x-22.5),Y(2690),45*s,220*s,green));
 b+=line(X(0),Y(3090),X(6600),Y(3090))+label(X(3300),Y(3290),'6600',14,'middle');
 b+=label(95,670,'16 deck/rebuilt pile candidates · seven concrete tread support candidates',12);
 b+=label(30,Y(1300),'2600',12)+label(28,Y(2850),'400',12);
 return svg(b,900,700,'Overall plan: nineteen base joists, two sisters, sixteen deck piles and seven concrete supports under a timber box tread');
}
function mainSection(){
 const Z=z=>620-z*.9;
 let b=label(55,38,'DECK SECTION · conventional framing stack',19)+label(55,66,'Nominal levels with 2 mm DPC; concrete footings shown schematically',12);
 b+=rect(60,Z(0),760,140,soil,'none')+line(55,Z(0),830,Z(0));
 [180,590].forEach(x=>{b+=rect(x-45,Z(10),180,115,concrete);b+=rect(x,Z(186),90,Z(-80)-Z(186),timber);});
 b+=rect(110,Z(328),680,140*.9,timber);
 b+=rect(95,Z(468),710,140*.9,green)+rect(85,Z(500),730,32*.9,'#e0bf8e');
 b+=line(110,Z(187),790,Z(187),'#313d36',2);
 b+=label(320,Z(400),'140 mm SG8 joists',15)+label(330,Z(260),'Double 140 × 45 bearers',15);
 b+=label(350,Z(100),'125-square H5 piles',14)+label(390,Z(-65),'Concrete',13);
 [[500,'+500 surface'],[468,'+468'],[328,'+328'],[186,'+186 pile top'],[0,'0 garden']].forEach(([z,t])=>b+=label(835,Z(z)+5,t,12));
 b+=label(55,795,'Six complete low anchor assemblies + rebuilt-joist hold-downs remain to specify.',13);
 return svg(b,970,825,'Deck section: surface 500, joist underside 328, bearer underside 188 and pile top 186 with two millimetre DPC');
}
function treadSection(){
 let b=label(45,32,'TREAD · single-layer pine box on concrete',20)+label(45,57,'Frame geometry developed; foundation depths and rated restraint remain open',12);
 const X=x=>80+x*.112,Y=y=>115+y*.34;
 b+=label(45,91,'PLAN · 6600 × 400; seven support stations, maximum 1000 centres',14);
 b+=rect(X(0),Y(0),6600*.112,400*.34,'#f5f7f2');
 supports.forEach(x=>{b+=rect(X(x-200),Y(20),400*.112,360*.34,concrete);b+=label(X(x),Y(400)+23,String(x),10,'middle');});
 [0,310].forEach(y=>b+=rect(X(0),Y(y),6600*.112,90*.34,timber));
 crosspieces.forEach(x=>b+=rect(X(x-22.5),Y(90),45*.112,220*.34,green));
 b+=label(45,307,'Double 140 × 45 rails · 21 × 220 crosspieces · board seam supported at X3300',12);
 b+=label(45,342,'CROSS-SECTION · trial recessed head only; actual foundation to design',14);
 const C=y=>230+y*1.1,Z=z=>650-z;
 b+=rect(170,Z(0),570,130,soil,'none')+line(170,Z(0),740,Z(0));
 b+=rect(C(20),Z(76),360*1.1,170,concrete);
 b+=line(C(20),Z(76)+170,C(380),Z(76)+170,'#71847b',2,'5 4');
 b+=rect(C(0),Z(250),440,32,'#e0bf8e');
 [0,310].forEach(y=>{b+=rect(C(y),Z(218),99,140,timber);b+=line(C(y+45),Z(218),C(y+45),Z(78));b+=line(C(y+20),Z(77),C(y+90),Z(77),'#313d36',2);});
 b+=rect(C(90),Z(218),220*1.1,140,green);
 b+=label(755,Z(250)+5,'+250 surface',12)+label(755,Z(218)+5,'+218 frame top',12)+label(755,Z(78)+2,'+78 timber bottom',12)+label(755,Z(76)+25,'+76 concrete / 2 DPC',12)+label(755,Z(0)+5,'0 garden/path',12);
 b+=label(450,710,'Below-ground size / depth / reinforcement: to design',12,'middle');
 b+=label(45,786,'Plain exposed pine rail. Keep the opening below it; no added fascia or soil bank.',12);
 return svg(b,960,820,'Box tread plan and section: 32 millimetre pine over 140 deep framing, timber underside 78, concrete top 76; seven support candidates');
}
function fixingDetail(){
 let b=label(45,35,'TREAD RESTRAINT · geometry candidate only',20)+label(45,62,'Pryda PBB8515/SS · 304 stainless, 5 mm thick · assembly capacity not established',13);
 b+=label(45,100,'SIDE SECTION THROUGH ONE RAIL · enlarged; bolt axis horizontal',13);
 b+=rect(200,220,180,280,timber)+line(290,220,290,500);
 b+=rect(200,500,180,4,'#313d36');
 b+=rect(170,504,390,130,concrete);
 b+=rect(380,304,10,200,'#8f9f9b')+rect(380,494,100,10,'#8f9f9b');
 b+=line(185,354,410,354,'#324c42',7)+rect(188,329,6,50,'#8f9f9b')+rect(392,329,6,50,'#8f9f9b');
 b+=line(430,488,430,591,'#71847b',3,'6 4');
 b+=`<circle cx="385" cy="454" r="8" fill="white" stroke="#52675b"/>`;
 b+=label(205,190,'90 mm doubled rail',14)+label(75,340,'Upper hole',12)+line(145,342,188,354);
 b+=label(75,374,'73 above bottom',12)+label(75,397,'67 below top',12);
 b+=label(505,350,'M12 × 130 bolt fit candidate',13)+label(505,375,'50 × 50 × 3 washers',13)+line(405,354,495,354);
 b+=label(505,447,'Lower hole unused in proposal',12)+line(395,454,495,447);
 b+=label(585,529,'Matched stainless concrete anchor',12)+label(585,552,'Product, embedment and edge distances: TBD',12)+line(435,541,570,537);
 b+=label(45,679,'Vertical weight: timber → DPC → concrete → soil. Angle provides restraint.',13);
 b+=label(45,712,'Check angle bending/prying, upper-hole-only use, wet timber bolts and concrete breakout.',12);
 b+=label(45,738,'Check the whole foundation for lateral load, uplift and overturning before specifying it.',12);
 b+=label(45,775,'This fit study is not a drilling template, rated assembly or hardware order.',13);
 return svg(b,960,805,'Unrated tread fixing candidate: PBB8515 stainless angle, upper M12 bolt through doubled rail, and concrete anchor still to specify');
}
const views={
 plan:[overall,'Continuous 6.6 m bearer/rail plies remove planned splices. Main/rebuilt pile layout retained; tread uses seven concrete support candidates.'],
 main:[mainSection,'Main member-table comparisons are favourable. The complete low anchor connections, bracing transfer and rebuilt-joist hold-downs remain unfinished.'],
 tread:[treadSection,'Concrete supports replace short timber piles. Trial bearing heads are shown; buried footprints may extend beyond the visible tread. Foundation/anchor design is not released.'],
 fixings:[fixingDetail,'This standard stainless angle physically fits the proposed box. Its manufacturer supplies geometry, not a pre-rated tread assembly; matched anchors and full capacity still need design.']
};
function show(view){const[draw,caption]=views[view];document.querySelector('#drawing').innerHTML=draw();document.querySelector('#drawing-caption').textContent=caption;document.querySelector('#drawing-panel').setAttribute('aria-labelledby',`tab-${view}`);document.querySelectorAll('[data-view]').forEach(b=>{const selected=b.dataset.view===view;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;});}
document.querySelectorAll('[data-view]').forEach(button=>{button.onclick=()=>show(button.dataset.view);button.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const keys=Object.keys(views),i=keys.indexOf(button.dataset.view),next=e.key==='Home'?0:e.key==='End'?keys.length-1:(i+(e.key==='ArrowRight'?1:keys.length-1))%keys.length;show(keys[next]);document.querySelector(`#tab-${keys[next]}`).focus();};});
const steps=[
 ['Set datums and mark all footprints','Tape, strings, level','Mark main 6600 × 2600, rebuilt 900 × 1970 and tread 6600 × 400. Check main diagonal 7093.7 and tread diagonal 6612.1 mm; establish actual finished ground and drainage levels.'],
 ['Mark piles and concrete tread supports','Tape, paint, complete foundation plan','Locate services before digging. Mark 16 deck/rebuilt pile locations and the agreed tread supports. Buried foundations may extend outside the tread; coordinate with the path and garden.'],
 ['Excavate all foundations','Spade or auger, depth rod','Use the agreed hole/pad dimensions and bearing levels. Check actual soil against the complete plan; resolve variations before concrete.'],
 ['Set piles and tread support forms','Level, clamps, braces, formwork','Keep treated pile bottoms intact; check grade marks, embedment and allowed top processing. Set tread bearing forms to the agreed level, nominally +76 with 2 mm DPC.'],
 ['Place concrete and allow it to cure','Specified concrete, placement tools','Maintain pile alignment and accurate tread bearing levels. Follow the agreed concrete, cure, loading and anchor installation requirements.'],
 ['Assemble continuous doubled bearers','Clamps, saw, specified nails/connectors','Cut 6600 mm main plies from 7200 stock; no main bearer seams. Fit the two rebuilt bearers, ply fixings, direct bearings and complete low anchor assemblies.'],
 ['Fit main joists, rims and restraint','Square, saw, specified fixings','Fit four continuous and 17 short joist members including sisters. Complete rebuilt crosspieces, lateral blocks, bracing transfer and rated uplift fixings before boards.'],
 ['Assemble the single-layer tread box','Tape, square, clamps, stainless framing nails','Use continuous 6600 rail plies and 21 × 220 crosspieces. Nail crosspieces to inner 45 mm plies first, then fit outer plies; preserve bracket access and check nail clashes.'],
 ['Seat and restrain the tread','DPC, level, drill, complete anchor schedule','Seat both rails directly on the agreed concrete supports with DPC. Install the designed stainless restraints; the illustrated bracket is a candidate until rated. Keep the opening and drainage clear.'],
 ['Lay the 32 mm pine boards','Spacers, saw, drill/driver, matching screws','Measure actual width/moisture and use supplier gaps. Support both ends at each seam; check edge rips, screw penetration and end distances. Main/tread rows run along the frontage.'],
 ['Finish and check against the agreed plan','Tape, level, agreed drawings','Leave treated pine natural with required cut-end treatment. Finish path/grass/garden clear of timber; check fixings, stability, drainage and the agreed access solution. Owner checks; no builder inspection visit assumed.']
];
function stepDrawing(i){
 let b='';const ground=()=>rect(20,155,280,60,soil,'none')+line(20,155,300,155);
 if(i<2){b=rect(45,35,230,110,'#f2f5ef')+rect(45,145,230,25,'#efe2ca')+label(160,28,'6600',12,'middle')+label(160,196,i===0?'One set-out · all footprints':'Piles + concrete tread supports',12,'middle');if(i===1){[70,108,146,184,222,260].forEach(x=>b+=rect(x-6,75,12,12,timber)+rect(x-6,119,12,12,timber));[65,95,125,155,185,215,245].forEach(x=>b+=rect(x,147,12,21,concrete));}else b+=line(45,35,275,145,'#84958a',1,'4 3');}
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
