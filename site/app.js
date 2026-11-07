const green='#456b54', timber='#cba773', concrete='#d6dad7', soil='#ece5d6';
const line=(x1,y1,x2,y2,color='#71847b',width=1,dash='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${dash?`stroke-dasharray="${dash}"`:''}/>`;
const rect=(x,y,w,h,fill,stroke='#52675b')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}"/>`;
const label=(x,y,t,size=13,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}">${t}</text>`;
const svg=(body,w=900,h=650,title='Design drawing')=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" role="img" aria-label="${title}"><title>${title}</title>${body}</svg>`;
const joists=[22.5,307.5,592.5,877.5,...Array.from({length:15},(_,i)=>1257.5+i*380)];
function overall(){
 const s=.103,X=x=>95+x*s,Y=y=>280+y*s;
 let b=label(95,24,'PLAN · H5 posts in concrete',17)+label(95,46,'Candidate framing and support geometry — dimensions in mm',12);
 b+=rect(X(0),Y(0),6600*s,2600*s,'#f5f7f2')+rect(X(0),Y(-1970),900*s,1970*s,'#f5f7f2');
 for(const y of[350,2250])b+=rect(X(0),Y(y-45),6600*s,90*s,timber);
 b+=rect(X(0),Y(-845),900*s,90*s,timber);
 joists.forEach((x,i)=>{b+=rect(X(x-22.5),Y(i<4?-1970:0),45*s,(i<4?4570:2600)*s,green);if(i>=4)b+=label(X(x),Y(0)-12,`J${String(i+1).padStart(2,'0')}`,9,'middle');});
 [350,2250].forEach(y=>[250,1470,2690,3910,5130,6350].forEach(x=>{b+=rect(X(x-62.5),Y(y-62.5),125*s,125*s,'#314b3c');}));
 [175,725].forEach(x=>{b+=rect(X(x-62.5),Y(-862.5),125*s,125*s,'#314b3c');});
 b+=label(210,113,'Rebuilt 900 × 1970',13)+label(210,137,'J01–J04 continue: candidate',11)+label(210,163,'Retained rear support unverified',11);
 b+=line(X(0),Y(-1970),X(900),Y(-1970),'#a66d40',4,'6 4');
 b+=label(210,Y(-800)+4,'BC · 900 double bearer / 2 posts',11);
 b+=label(782,Y(350)+4,'BA',12)+label(782,Y(2250)+4,'BB',12);
 b+=rect(X(0),Y(2600),6600*s,400*s,'#faf3e4');
 [2600,2955].forEach(y=>{b+=rect(X(0),Y(y),6600*s,45*s,timber);});
 Array.from({length:7},(_,i)=>250+i*6100/6).forEach(x=>{b+=rect(X(x-175),Y(2625),350*s,350*s,'none','#a66d40');b+=rect(X(x-62.5),Y(2737.5),125*s,125*s,green);});
 b+=line(X(0),Y(3090),X(6600),Y(3090))+label(X(3300),Y(3290),'6600',14,'middle');
 b+=label(95,670,'Tread: 7 centred posts · Y2800 · squares show excavation envelope only',12);
 b+=label(30,Y(1300),'2600',12)+label(28,Y(2850),'400',12);
 return svg(b,900,700,'Overall plan with nineteen joists, fourteen deck posts and seven candidate centred tread posts');
}
function mainSection(){
 let b=label(60,40,'DECK SECTION · main framing stack',19)+label(60,68,'Schematic, not to scale; levels relative to garden, before separation layers',12);
 b+=rect(80,410,740,170,soil,'none')+line(60,410,840,410);
 b+=rect(150,390,190,170,concrete)+rect(570,390,190,170,concrete);
 [195,615].forEach(x=>{b+=rect(x,285,100,245,timber);b+=line(x,530,x+100,530,'#a66d40',2);});
 b+=rect(110,173,690,112,timber)+rect(95,61+112,720,0,'none');
 b+=rect(90,89,730,84,green)+rect(80,70,750,19,'#e0bf8e');
 b+=label(335,123,'140 mm joists',15)+label(370,233,'140 mm doubled bearer',15);
 b+=label(45,400,'Garden',12)+label(340,335,'H5 structural post',14)+label(360,475,'Concrete footing',14);
 b+=label(60,610,'Footing depth, embedment, post length and bracing connection: design required',13);
 b+=label(835,78,'+500',12)+label(835,102,'+468',12)+label(835,183,'+328',12)+label(835,294,'+188',12)+label(835,414,'0',12);
 return svg(b,930,650,'Main deck section showing board surface 500, joist underside 328 and bearer underside 188 millimetres');
}
function treadSection(){
 let b=label(60,40,'TREAD SECTION · 400 mm footprint',19)+label(60,68,'Schematic, not to scale — transverse head requires specific structural design',12);
 b+=rect(170,335,560,215,soil,'none')+line(130,335,770,335);
 // 400 mm across = 520 drawing units; 350 mm envelope =455 units
 b+=rect(222.5,340,455,190,concrete)+rect(368.75,300,162.5,200,timber);
 b+=rect(190,170,520,42,'#e0bf8e');
 b+=rect(190,212,58.5,115,green)+rect(651.5,212,58.5,115,green);
 b+=rect(248.5,212,403,115,'#eff4ec');
 b+=line(200,327,700,327,'#9a633a',5,'8 5');
 b+=line(450,337,450,326,'#9a633a',3,'4 3');
 b+=label(450,247,'Single-layer 140 × 45 frame',14,'middle')+label(450,270,'310 clear between rails',12,'middle');
 b+=line(190,110,710,110)+label(450,100,'400 overall',15,'middle');
 b+=line(222.5,575,677.5,575)+label(450,600,'350 excavation envelope · not a footing specification',12,'middle');
 b+=label(60,378,'Garden 0',12)+label(740,183,'+250 surface',12)+label(740,221,'+218 frame top',12)+label(740,325,'+78 underside',12);
 b+=label(450,432,'H5 post',14,'middle')+label(450,459,'Depth / embedment TBD',12,'middle');
 b+=label(60,637,'Dashed head is symbolic: no head depth, plate, bolt or post-top level is specified.',12);
 return svg(b,960,670,'Tread section, both rails supported by a designed transverse head above a centred H5 timber post in concrete');
}
const views={plan:[overall,'Two bearer rows and the rebuilt intermediate support give 14 candidate deck posts. Seven centred tread posts make 21 new posts in this concept. Rim, blocking and board-joint details are still to specify.'],main:[mainSection,'Main framing preference retained: double 140 × 45 SG8 bearers and 140 × 45 SG8 joists. Post tops and footing bottoms must be set from measured cleared-ground levels.'],tread:[treadSection,'The 350 square is a footprint test only. Soil bearing, depth, cover, construction tolerance and the designed head must all fit inside the 400 mm tread. The low-clearance connection remains unresolved.']};
function show(view){const[draw,caption]=views[view];document.querySelector('#drawing').innerHTML=draw();document.querySelector('#drawing-caption').textContent=caption;document.querySelector('#drawing-panel').setAttribute('aria-labelledby',`tab-${view}`);document.querySelectorAll('[data-view]').forEach(b=>{const selected=b.dataset.view===view;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;});}
document.querySelectorAll('[data-view]').forEach(button=>{button.onclick=()=>show(button.dataset.view);button.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const keys=Object.keys(views),i=keys.indexOf(button.dataset.view),next=e.key==='Home'?0:e.key==='End'?2:(i+(e.key==='ArrowRight'?1:2))%3;show(keys[next]);document.querySelector(`#tab-${keys[next]}`).focus();};});
const steps=[
 ['Set datums and mark the footprints','Tape, strings, level','Mark 6600 × 2600 main, 900 × 1970 rebuilt and 6600 × 400 tread. Check main diagonal 7093.7 mm and tread diagonal 6612.1 mm. Survey the ground at every support.'],
 ['Mark all approved post holes','Tape, paint, approved post plan','Locate services before digging. Check every tread excavation, including tolerance, stays within the 400 mm footprint. Use the approved schedule rather than the spatial envelope.'],
 ['Dig to the agreed bearing level','Spade or auger, depth rod','Check actual soil, hole size and base levels against FP01 and GP01. Resolve any variation before proceeding.'],
 ['Place and temporarily brace the H5 posts','Level, clamps, temporary braces','Confirm treatment and structural marks, protected ends, embedment and designed head levels. Do not cut posts low without the approved treatment detail.'],
 ['Place concrete and allow it to cure','Specified concrete, placement tools','Provide the specified concrete below and around each post. Maintain alignment and temporary restraint; follow the agreed cure and loading times.'],
 ['Assemble and fix the doubled bearers','Clamps, drill, specified connectors','Fit main and rebuilt bearers. Check direct bearing, ply fastening, supported splices and every connection against AP01.'],
 ['Fit main joists, rims and restraint','Square, saw, drill','Check centres, continuous-member junctions, retained support and complete bracing in both directions. Install structural block-end fixings.'],
 ['Install tread heads and both rails','Tools from the designed GP01 detail','Check head fixings, both rail bearings, levels, corrosion separation and resistance to sideways movement, uplift and edge-load rotation.'],
 ['Fit crosspieces and board-joint supports','Square, saw, drill','Check support spacing for the actual decking and support all rail and board joints. Complete concealed connections before covering.'],
 ['Lay the 32 mm pine decking','Spacers, drill/driver, specified screws','Dry-lay the actual width and supplier gap. Check edge rips, supported seams, screw embedment and end distances.'],
 ['Finish and check against the agreed plan','Tape, level, agreed plan','Check fixings, stability, dimensions, drainage and safe usable access. These are owner checks; no builder visit is assumed.']
];
function stepDrawing(i){
 let b='';const ground=()=>rect(20,155,280,60,soil,'none')+line(20,155,300,155);
 if(i<2){b=rect(45,35,230,110,'#f2f5ef')+rect(45,145,230,25,'#efe2ca')+label(160,28,'6600',12,'middle')+label(160,196,i===0?'One set-out · all footprints':'Approved post / hole plan',12,'middle');if(i===1)[70,108,146,184,222,260].forEach(x=>b+=rect(x-6,75,12,12,timber)+rect(x-6,119,12,12,timber));else b+=line(45,35,275,145,'#84958a',1,'4 3');}
 else if(i<5){b=ground()+rect(115,155,90,60,'white');if(i>2)b+=rect(145,68,30,127,timber)+line(145,90,85,155,green,3)+line(175,90,235,155,green,3);if(i===4)b+=rect(115,160,30,50,concrete)+rect(175,160,30,50,concrete)+rect(115,195,90,15,concrete);b+=label(160,35,['','','Approved footing depth','Brace posts plumb','Concrete below and around'][i],12,'middle');}
 else if(i===5){b=rect(70,115,30,75,timber)+rect(220,115,30,75,timber)+rect(40,77,240,19,timber)+rect(40,99,240,19,timber)+label(160,40,'Double bearer · specified ply fixings',12,'middle');[70,110,150,190,230,270].forEach(x=>b+=rect(x,87,3,3,green));}
 else if(i===6||i===8){b=rect(40,40,240,140,'#f5f7f2');[70,120,170,220,270].forEach(x=>b+=rect(x,40,7,140,green));[70,150].forEach(y=>b+=rect(40,y,240,8,timber));if(i===8)[75,120,170,220].forEach(x=>b+=rect(x,106,42,7,timber));b+=label(160,205,i===6?'Joists + rims + structural restraint':'Crosspieces + supported joints',12,'middle');}
 else if(i===7){b=ground()+rect(145,145,30,55,timber)+line(65,137,255,137,'#9a633a',5,'6 4')+rect(65,85,25,50,green)+rect(230,85,25,50,green)+label(160,35,'GP01 · designed head supports rails',12,'middle')+label(160,220,'Head shown symbolically',11,'middle');}
 else {for(let y=45;y<180;y+=22)b+=rect(40,y,240,18,timber);if(i===9){[70,140,210,260].forEach(x=>[54,98,142].forEach(y=>b+=rect(x,y,3,3,green)));b+=label(160,208,'Supplier gaps + specified screws',12,'middle');}else b+=label(160,208,'Owner completion check',12,'middle');}
 return svg(b,320,240,`Step ${i+1}: ${steps[i][0]}`);
}
document.querySelector('#build-steps').innerHTML=steps.map(([title,tools,check],i)=>`<details class="step" ${i===0?'open':''}><summary><span class="step-number">${String(i+1).padStart(2,'0')}</span>${title}</summary><div class="step-content">${stepDrawing(i)}<div><p><strong>Tools:</strong> ${tools}.</p><p><strong>Owner check:</strong> ${check}</p></div></div></details>`).join('');
let previousOpen=[];
window.addEventListener('beforeprint',()=>{previousOpen=[...document.querySelectorAll('details')].map(d=>d.open);document.querySelectorAll('details').forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>document.querySelectorAll('details').forEach((d,i)=>d.open=previousOpen[i]??false));
document.querySelector('#print').onclick=()=>window.print();
document.querySelector('#copy-link').onclick=async()=>{try{await navigator.clipboard.writeText(location.href);document.querySelector('#message').textContent='Link copied.';}catch{document.querySelector('#message').textContent=`Page link: ${location.href}`;}};
show('plan');
