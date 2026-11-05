import { renderPlan, renderElevation, renderTreadFrame, renderDeckingDetail, JOIST_CENTRES } from './diagrams.js';
import { renderBuildGuide, setAssemblyPrintMode } from './build-guide.js';
import { renderAssemblyDiagram } from './assembly-diagrams.js';

const $ = (selector) => document.querySelector(selector);
const topicData = [
  { id: 'structure', title: 'AP01 · Framing / connections', question: 'Review the 19-line ≤400 mm proposal, doubled 140×45 bearer ply/splice detail, six complete stainless 12 kN connections, ordinary-pile fixings and lateral blocking. BRANZ’s worked example bounds the short joist spans; full current standard and wet-service connection checks remain necessary.' },
  { id: 'junction', title: 'Retained beam / rebuilt strip', question: 'Measure the retained bearer section, pile spacing, grade/condition and connections. A new 900 mm bearer at Y−800 shortens the joist spans to1170/1150 mm but does not prove the retained beam. If unsuitable, replace its support line under a reviewed detail.' },
  { id: 'ground', title: 'FP01 · Conditional footing schedule', question: 'Ground is reported firm natural; establish applicable good-ground bearing. Review six main anchors, six main ordinary piles, two intermediate ordinary piles and six shared tread pads; verify cleared-ground datums and the computed concrete quantity.' },
  { id: 'access', title: 'GP01 · Tread hardware', question: 'Owner keeps one 250 mm-high tread. Review the SG8 H5 frame request, six shared pad sizes, reinforcement if required, separation, rail splices and exact stainless restraint/anchor/wood-fixing detail. Access compliance is not asserted.' },
  { id: 'materials', title: 'DF01 · Board choice', question: 'Keep true 38 mm unless owner changes it. Compare the listed 32 mm alternatives; confirm actual width/moisture, available lengths, gap, board-end screws and staggered seams at X≈2375/3895 on doubled supports.' }
];
const selectionData = {
 main: { title:'Main deck',badge:'Footprint confirmed',type:'green',values:[['Width ×depth','6600 ×2600 mm'],['Area','17.16 m²'],['Surface above garden','About500 mm']],description:'Boards run in X across the frontage. Owner retains 38 mm pine.',note:'Normal 2 kPa residential deck basis; no cantilevered barrier. Specific proposal requires the pre-build connection/ground checks.',topic:'structure'},
 rebuilt: { title:'Rebuilt decking',badge:'Direction illustrated',type:'sand',values:[['Footprint','900 ×1970 mm'],['Boards','Y along the depth'],['Cross-blocks','18 ×240 mm nominal'],['Added bearer','Y−800 ·900 mm long']],description:'Four long joists and three flush blocks per support row carry the rotated boards.',note:'The retained beam’s capacity remains unknown. The reported1970 spacing has ambiguous endpoints/axis; the beam section and condition remain unknown.',topic:'junction'},
 blocking: { title:'Rebuilt board supports',badge:'Revised proposal',type:'sand',values:[['Long joists','J01–J04'],['Rows','6 at 385 mm centres'],['Blocks','18 ×240 mm /4.32 lm'],['Levels','Flush with joists']],description:'Three blocks per row span between the four long joists; board fixings go into those rows.',note:'Select the complete stainless hanger/end-fixing detail for wet timber. Decking screws are not the structural block fasteners.',topic:'junction'},
 tread: { title:'Ground-supported tread',badge:'Six shared-pad proposal',type:'sand',values:[['Footprint','6600 ×400 mm'],['Surface','250 mm selected'],['Frame','140 ×45 SG8 H5 request'],['Members','2 rails +19 crosspieces +2 butt sisters'],['Supports','6 pads /12 rail bearings']],description:'Both rails bear on each shared concrete pad; their load goes directly to ground, independently of the main deck rim.',note:'Pad dimensions are a planning proposal; reinforcement, restraint product, anchor embedment/edges and wet timber connections require a matching reviewed detail.',topic:'access'},
 ground: { title:'Tread foundation proposal',badge:'GP01 review required',type:'sand',values:[['Pads','6 shared concrete strips'],['Plan size','500 across tread ×300 along X'],['Below cleared ground','300 mm proposed'],['Top datum','Rail underside minus separation']],description:'With garden equal to cleared-ground datum and2 mm separation, the pads total about 0.333 m³. Include them in the same groundworks.',note:'Soil bearing, pad/anchor design and exact separation remain to confirm. C1/C2/C3 are still product families, not an installation recipe.',topic:'ground'},
 extension: { title:'House extension',badge:'Frontage confirmed',type:'green',values:[['Frontage','5700 mm'],['Rebuilt alongside','900 mm']],description:'Freestanding deck; no structural connection to the house.',note:'',topic:'structure'},
 bearer: { title:'Bearers and piles',badge:'Specific review proposal',type:'sand',values:[['Main','2 doubled140 ×45 lines'],['Y centres','350 /2250 mm'],['Main piles','6 anchor +6 ordinary'],['Added rebuilt support','900 bearer +2 ordinary piles']],description:'Main spans1220 mm. Anchor X lines250/2690/6350 keep bracing-line gaps below5 m.',note:'BRANZ’s published 140×70 solid-bearer benchmark is not a built-up bearer fastening schedule. Main splices proposed over ordinary piles at X3910.',topic:'structure'},
 joists: { title:'J01–J04 continue through',badge:'19-line proposal',type:'sand',values:[['Main lines','19 +2 butt sisters'],['First 3 bays','285 mm'],['Other 15 bays','380 mm'],['Rebuilt spans','1170 /1150 mm'],['Main span','1900 mm']],description:'Four long joists pass over the added Y−800 bearer and continue into the main deck. Fifteen joists are main-only; BJ1/BJ2 support staggered board seams.',note:'This ≤400 mm layout follows the spacing in BRANZ’s published worked example. Retained support, member end/bearing details and connections still require confirmation.',topic:'junction'}
};
const sourceLabels = {
  'STRUCTURAL_REVIEW.md': ['Structural proposal and calculations', 'Published evidence, footing/stock arithmetic and remaining limits'],
  'PROJECT.md': ['Project brief', 'Confirmed requirements and latest owner decisions'],
  'DESIGN.md': ['Design & geometry', 'Coordinates, framing concepts and access detail'],
  'MATERIALS.md': ['Materials & quantities', 'Conditional quantities, assumptions and price history'],
  'OPEN_ISSUES.md': ['Open design checks', 'Evidence needed before construction'],
  'SITE_MEASUREMENTS.md': ['Site measurements', 'Known dimensions and remaining field checks'],
  'BUILD_STEPS.md': ['Assembly guide', 'Eleven numbered actions with parts and pending plan details'],
  'REFERENCES.md': ['Sources & provenance', 'Research leads and verification history'],
  'DECISIONS.md': ['Decision log', 'How the design has developed']
};
let toastTimer;
function toast(message) {
  clearTimeout(toastTimer);
  $('#toast').textContent = message;
  $('#toast').classList.add('visible');
  toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 4200);
}
function renderDiscussionTopics() {
  $('#discussion-topics').innerHTML = `<caption>One builder plan review before construction</caption><thead><tr><th scope="col">Plan detail</th><th scope="col">Agree before building</th></tr></thead><tbody>${topicData.map(topic => `<tr id="discussion-${topic.id}" class="discussion-row"><th scope="row">${topic.title}</th><td>${topic.question}</td></tr>`).join('')}</tbody>`;
}
function renderJoistCoordinates() {
  $('#joist-coordinates tbody').innerHTML = JOIST_CENTRES.map((x, i) => `<tr><th scope="row">J${String(i + 1).padStart(2, '0')}</th><td>${Number(x.toFixed(2))}</td><td>${i < 4 ? 'Continuous rebuilt + main; intermediate support Y−800' : 'Main deck'}</td></tr>`).join('');
}
let selected = 'joists';
function selectArea(id) {
  if (!selectionData[id]) return;
  selected = id;
  const data = selectionData[id];
  $('#selection-detail').innerHTML = `<h3 id="detail-title">${data.title}</h3><span class="badge badge-${data.type}">${data.badge}</span><dl class="detail-values">${data.values.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')}</dl><p class="detail-description">${data.description}</p><p class="detail-footnote">${data.note}</p><a class="detail-discussion-link" href="#discussion-${data.topic}">Builder check →</a>`;
  for (const element of $('#design-drawing').querySelectorAll('[data-select]')) {
    const active = element.dataset.select === selected;
    element.classList.toggle('selected', active);
    element.setAttribute('aria-pressed', String(active));
  }
  $('.detail-discussion-link').addEventListener('click', () => openTopic(data.topic));
}
function setView(view) {
  if (view === 'framing' && ['main', 'extension'].includes(selected)) selected = 'joists';
  $('#drawing-panel').classList.remove('is-zoomed');
  $('#zoom-drawing').setAttribute('aria-pressed', 'false');
  $('#zoom-drawing').textContent = 'Enlarge +';
  for (const tab of document.querySelectorAll('[data-view]')) {
    const active = tab.dataset.view === view;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  }
  $('#drawing-panel').setAttribute('aria-labelledby', `tab-${view}`);
  const svg = $('#design-drawing');
  if (view === 'elevation') {
    renderElevation(svg);
    $('#drawing-note').textContent = 'Owner retains deck500 /tread250 mm and one400 mm tread. Access compliance is not verified.';
    $('#drawing-scale').textContent = 'SIDE PROFILE';
    selectArea('tread');
  } else if (view === 'tread') {
    renderTreadFrame(svg);
    $('#drawing-note').textContent = 'Proposed140×45 SG8 H5 frame on six shared pads. Exact ground/connection checks remain; see the conditional schedule.';
    $('#drawing-scale').textContent = 'TREAD DETAIL';
    selectArea('tread');
  } else if (view === 'ground') {
    renderAssemblyDiagram(svg, 'tread-ground');
    $('#drawing-note').textContent = 'Typical bearing and restraint. Six500×300 shared pads are proposed; depth, reinforcement and exact hardware require the reviewed GP01 detail.';
    $('#drawing-scale').textContent = 'GROUND CONNECTION';
    selectArea('ground');
  } else if (view === 'decking') {
    renderDeckingDetail(svg);
    $('#drawing-note').textContent = 'Rebuilt boards turn 90°. Cross-blocks are flush with J01–J04; dots show example board fixing locations, not a final screw schedule.';
    $('#drawing-scale').textContent = 'REBUILT DETAIL';
    selectArea('blocking');
  } else {
    renderPlan(svg, { view, selected });
    $('#drawing-note').textContent = view === 'framing' ? 'J01–J04 are proposed to continue through. Blue cross-blocks support the rotated rebuilt boards. All new frame/support details remain provisional.' : 'Main boards run across the frontage; rebuilt boards run along the 1970 mm depth.';
    $('#drawing-scale').textContent = 'TOP VIEW';
    if (view === 'layout' && ['joists', 'bearer', 'blocking', 'ground'].includes(selected)) selected = 'rebuilt';
    selectArea(selected);
  }
  const legends = {
    framing: '<span><i class="legend-joist"></i>Joists</span><span><i class="legend-bearer"></i>Bearers</span><span><i class="legend-block"></i>Cross-blocks</span>',
    layout: '<span><i class="legend-main"></i>Deck boards</span><span>Rebuilt boards rotated 90°</span>',
    decking: '<span><i class="legend-block"></i>Cross-supports</span><span>Dots = example fixings</span>',
    tread: '<span>Single layer · section / supports follow resolved levels</span>',
    ground: '<span>Six shared pads · typical connection shown</span>',
    elevation: '<span>Owner-selected levels · access unverified</span>'
  };
  $('#drawing-legend').innerHTML = legends[view] || '';
}
function openTopic(id) {
  const target = id === 'layout' ? 'structure' : id;
  const topic = $(`#discussion-${target}`);
  document.querySelectorAll('.discussion-row.is-focused').forEach(row => row.classList.remove('is-focused'));
  if (topic) topic.classList.add('is-focused');
}
$('#design-drawing').addEventListener('plan-select', (event) => selectArea(event.detail.id));
for (const tab of document.querySelectorAll('[data-view]')) {
  tab.addEventListener('click', () => setView(tab.dataset.view));
  tab.addEventListener('keydown', event => {
    const tabs = Array.from(document.querySelectorAll('[data-view]'));
    let i = tabs.indexOf(tab);
    if (event.key === 'ArrowRight') i = (i + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') i = (i + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') i = 0;
    else if (event.key === 'End') i = tabs.length - 1;
    else return;
    event.preventDefault();
    setView(tabs[i].dataset.view);
    tabs[i].focus();
  });
}
$('#zoom-drawing').addEventListener('click', () => {
  const zoomed = $('#drawing-panel').classList.toggle('is-zoomed');
  $('#zoom-drawing').setAttribute('aria-pressed', String(zoomed));
  $('#zoom-drawing').textContent = zoomed ? 'Fit −' : 'Enlarge +';
});
$('#reset-view').addEventListener('click', () => { selected = 'joists'; setView('framing'); });
for (const link of document.querySelectorAll('[data-open-view]')) {
  link.addEventListener('click', () => { setView(link.dataset.openView); $('#plan').scrollIntoView(); });
}

function download(filename, content, type = 'text/plain;charset=utf-8') {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}
async function copy(text, success) {
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(text);
    toast(success);
    return true;
  } catch {
    const input = document.createElement('textarea');
    input.value = text;
    input.style.cssText = 'position:fixed;left:-9999px;top:0;';
    document.body.append(input);
    input.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch {}
    input.remove();
    toast(ok ? success : 'Copy is unavailable in this browser. Use the download option instead.');
    return ok;
  }
}
renderDiscussionTopics();
renderJoistCoordinates();
renderBuildGuide($('#build-phases'));
let printDetails = [];
window.addEventListener('beforeprint', () => {
  setAssemblyPrintMode(true);
  printDetails = Array.from(document.querySelectorAll('.assembly-parts, .coordinate-details')).map(element => [element, element.open]);
  for (const [element] of printDetails) element.open = true;
});
window.addEventListener('afterprint', () => {
  setAssemblyPrintMode(false);
  for (const [element, wasOpen] of printDetails) element.open = wasOpen;
  printDetails = [];
});
$('#print-guide').addEventListener('click', () => window.print());

const sources = JSON.parse($('#source-documents').textContent);
for (const [filename, [title, description]] of Object.entries(sourceLabels)) {
  if (typeof sources[filename] !== 'string') continue;
  const button = document.createElement('button');
  button.className = 'source-button';
  button.innerHTML = `<span aria-hidden="true">▧</span><span>${title}<small>${description}</small></span><span aria-hidden="true">↓</span>`;
  button.setAttribute('aria-label', `Download ${title}, ${filename}`);
  button.addEventListener('click', () => download(filename, sources[filename], 'text/markdown;charset=utf-8'));
  $('#source-list').append(button);
}
const shareDialog = $('#share-dialog');
$('#share-open').addEventListener('click', () => shareDialog.showModal());
$('#share-close').addEventListener('click', () => shareDialog.close());
shareDialog.addEventListener('click', event => { if (event.target === shareDialog && (event.clientX < shareDialog.getBoundingClientRect().left || event.clientX > shareDialog.getBoundingClientRect().right || event.clientY < shareDialog.getBoundingClientRect().top || event.clientY > shareDialog.getBoundingClientRect().bottom)) shareDialog.close(); });
const localHosts = ['localhost', '127.0.0.1', '0.0.0.0', '::1', '[::1]'];
const hosted = ['https:', 'http:'].includes(location.protocol) && !localHosts.includes(location.hostname) && !location.hostname.endsWith('.localhost');
if (!hosted) {
  $('#copy-link').disabled = true;
  $('#hosted-note').textContent = 'This is a local copy. Share the downloaded HTML file, or put it on static hosting to get a public link.';
}
$('#copy-link').addEventListener('click', () => { if (hosted) copy(location.href.split('#')[0], 'Page link copied.'); });
$('#download-website').addEventListener('click', () => {
  const clone = document.documentElement.cloneNode(true);
  clone.querySelector('#share-dialog').removeAttribute('open');
  clone.querySelector('#toast').textContent = '';
  clone.querySelector('#toast').classList.remove('visible');
  download('auckland-deck-design.html', '<!doctype html>\n' + clone.outerHTML, 'text/html;charset=utf-8');
  toast('Guide downloaded.');
});
setView('framing');
function openLinkedDiscussion() {
  if (location.hash.startsWith('#discussion-')) openTopic(location.hash.slice('#discussion-'.length));
  else if (location.hash.startsWith('#review-')) {
    const id = location.hash.slice('#review-'.length);
    openTopic(id);
    document.getElementById(`discussion-${id}`)?.scrollIntoView();
  } else if (location.hash === '#review') $('#builder-brief').scrollIntoView();
}
openLinkedDiscussion();
window.addEventListener('hashchange', openLinkedDiscussion);
