import { renderPlan, renderElevation, renderTreadFrame, renderDeckingDetail, JOIST_CENTRES } from './diagrams.js';
import { renderBuildGuide, setAssemblyPrintMode } from './build-guide.js';
import { renderAssemblyDiagram } from './assembly-diagrams.js';

const $ = (selector) => document.querySelector(selector);
const topicData = [
  { id: 'junction', title: 'J01–J03 / rebuilt decking', question: 'Review the continuous-joist option, retained support data, 12 cross-blocks, block-end joints and board fixing rows.' },
  { id: 'structure', title: 'AP01 · main connections', question: 'Set anchor/ordinary-pile locations and the complete doubled-bearer/joist connection and lateral-restraint schedule. For the low MiTek option, check 12KNH stainless, available pile height and required geometry.' },
  { id: 'ground', title: 'FP01 · main footings', question: 'Agree hole dimensions, pile classes/lengths, embedment, concrete and curing instructions from the ground information.' },
  { id: 'access', title: 'GP01 · tread / ground', question: 'Specify G01–G12 concrete bearings, separation and the C1/C2/C3 rail-to-concrete restraint detail. Confirm timber grade/treatment, footing and anchor dimensions, levels and access geometry.' },
  { id: 'materials', title: 'DF01 · boards / screws', question: 'Choose the actual 38 mm pine board, width, gap, screw type/size, block-end connectors and stock/cut plan.' }
];
const selectionData = {
  main: { title: 'Main deck', badge: 'Dimensions confirmed', type: 'green', values: [['Width × depth', '6600 × 2600 mm'], ['Area', '17.16 m²'], ['Garden drop', 'About 500 mm']], description: 'Boards run across the joists, parallel to the frontage.', note: 'Frame schedule to be reviewed before construction.', topic: 'structure' },
  rebuilt: { title: 'Rebuilt decking', badge: 'Direction illustrated', type: 'sand', values: [['Width × depth', '900 × 1970 mm'], ['Board direction', 'Along 1970 mm depth'], ['Cross-support rows', '6 · 385 mm centres'], ['Flush blocks', '12 · between J01–J03']], description: 'Rotated boards fix into added cross-blocking, not just parallel joists.', note: 'Direction follows the description of boards turning 90°. Review block-end fixings and the final board/fastener schedule before building.', topic: 'junction' },
  blocking: { title: 'Rebuilt board supports', badge: 'Proposal', type: 'sand', values: [['Joist lines', 'J01 / J02 / J03'], ['Block rows', '6 at 385 mm centres'], ['Blocks', '12 × 382.5 mm nominal'], ['Top level', 'Flush with joists']], description: 'Two short blocks per row span between the three long joists. Board fasteners go into these cross-support rows.', note: 'Use reviewed block-end connectors/structural fixings. Two board fasteners per row are illustrated; actual screw size and edge distances remain to specify.', topic: 'junction' },
  tread: { title: 'Tread ladder frame', badge: 'Proposal', type: 'sand', values: [['Outer frame', '6600 × 400 mm'], ['Long rails', '2 × 6600 mm'], ['Crosspieces', '16 × 310 mm nominal'], ['Support stations', '6 / 12 rail bearings'], ['Frame top / bottom', '212 / 72 mm nominal']], description: 'Single 140 mm-deep layer under 38 mm boards. Separate supports; no stacked bearer layer.', note: 'Proposed G01–G12 concrete bearings carry both rails. C1/C2/C3 connectors restrain the frame. GP01 must specify the actual support and fixing details.', topic: 'access' },
  ground: { title: 'Tread ground connection', badge: 'Proposed · GP01 needed', type: 'sand', values: [['Bearings', 'G01–G12 · concrete'], ['Separation', 'DPC / specified layer'], ['C1', 'Structural side connector'], ['C2', 'Concrete anchorage'], ['C3', 'Rail-to-connector fixings']], description: 'Gravity: rail → separation → concrete → suitable soil. The bracket restrains movement and uplift; it does not suspend the rail.', note: 'Specify the actual bracket, timber fixings, concrete anchors, footing size/depth and low-clearance exposure detail before installation. Twelve locations do not establish fastener quantities.', topic: 'access' },
  extension: { title: 'House extension', badge: 'Frontage confirmed', type: 'green', values: [['Frontage', '5700 mm'], ['Rebuilt alongside', '900 mm'], ['Rear extent', 'Not surveyed']], description: 'Shown for context; no structural house attachment.', note: '', topic: 'structure' },
  bearer: { title: 'Bearers & piles', badge: 'Provisional', type: 'sand', values: [['New bearers', '2 double 140 × 45 lines'], ['Y centre lines', '350 / 2250 mm'], ['Separation', '1900 mm centres'], ['New piles', '12 proposed']], description: 'Six proposed pile positions on each new bearer line.', note: 'Review spans, footing/bracing, ply joints and connectors before building.', topic: 'structure' },
  joists: { title: 'J01–J03 continue through', badge: 'Proposed continuity', type: 'sand', values: [['Main lines', '16 · J01–J16'], ['J01–J03 extent', 'Rebuilt + main deck'], ['Finished envelope', '4570 mm'], ['Other joist envelope', '2600 mm'], ['Centres', '427.5 / 438.46 mm']], description: 'Yes: the three left joists are proposed to continue from the retained back bearer through to the main deck’s garden edge.', note: 'Envelope dimensions are not cut lengths. The rim junction, support reactions, bearing and connections remain to confirm in the pre-build plan review.', topic: 'junction' }
};
const sourceLabels = {
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
  $('#joist-coordinates tbody').innerHTML = JOIST_CENTRES.map((x, i) => `<tr><th scope="row">J${String(i + 1).padStart(2, '0')}</th><td>${Number(x.toFixed(2))}</td><td>${i < 3 ? 'Continuous rebuilt + main candidate; 4570 mm envelope' : 'Main deck'}</td></tr>`).join('');
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
    $('#drawing-note').textContent = 'One full-width 400 mm tread at the proposed 250 mm level. No handrails proposed.';
    $('#drawing-scale').textContent = 'SIDE PROFILE';
    selectArea('tread');
  } else if (view === 'tread') {
    renderTreadFrame(svg);
    $('#drawing-note').textContent = 'Independent single-layer proposal: 2 rails, 16 crosspieces and 12 rail bearing points. Grade/treatment and support/anchor details are not final.';
    $('#drawing-scale').textContent = 'TREAD DETAIL';
    selectArea('tread');
  } else if (view === 'ground') {
    renderAssemblyDiagram(svg, 'tread-ground');
    $('#drawing-note').textContent = 'Proposed direct concrete bearing plus positive restraint. Footing and connector geometry is schematic; GP01 must specify sizes, product and installation.';
    $('#drawing-scale').textContent = 'GROUND CONNECTION';
    selectArea('ground');
  } else if (view === 'decking') {
    renderDeckingDetail(svg);
    $('#drawing-note').textContent = 'Rebuilt boards turn 90°. Cross-blocks are flush with J01–J03; dots show example board fixing locations, not a final screw schedule.';
    $('#drawing-scale').textContent = 'REBUILT DETAIL';
    selectArea('blocking');
  } else {
    renderPlan(svg, { view, selected });
    $('#drawing-note').textContent = view === 'framing' ? 'J01–J03 are proposed to continue through. Blue cross-blocks support the rotated rebuilt boards. All new frame/support details remain provisional.' : 'Main boards run across the frontage; rebuilt boards run along the 1970 mm depth.';
    $('#drawing-scale').textContent = 'TOP VIEW';
    if (view === 'layout' && ['joists', 'bearer', 'blocking', 'ground'].includes(selected)) selected = 'rebuilt';
    selectArea(selected);
  }
  const legends = {
    framing: '<span><i class="legend-joist"></i>Joists</span><span><i class="legend-bearer"></i>Bearers</span><span><i class="legend-block"></i>Cross-blocks</span>',
    layout: '<span><i class="legend-main"></i>Deck boards</span><span>Rebuilt boards rotated 90°</span>',
    decking: '<span><i class="legend-block"></i>Cross-supports</span><span>Dots = example fixings</span>',
    tread: '<span>One layer · 140 mm frame + 38 mm boards</span>',
    ground: '<span>Bearing carries weight · connector restrains movement</span>',
    elevation: '<span>Surface levels proposed</span>'
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
