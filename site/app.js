import { renderPlan, renderElevation, JOIST_CENTRES } from './diagrams.js';
import { renderBuildGuide } from './build-guide.js';

const $ = (selector) => document.querySelector(selector);
const topicData = [
  { id: 'layout', title: 'House / site', question: 'Confirm threshold, cladding, drainage and ventilation clearances; locate services and foundation conflicts.', stage: 'Before set-out' },
  { id: 'junction', title: 'Retained bearer / junction', question: 'Inspect retained supports. Verify the three joist continuation candidates, bearing, rim junction and combined loads.', stage: 'Before cutting framing' },
  { id: 'structure', title: 'Spans / bracing / fixings', question: 'Confirm spans, cantilevers, pile count, bracing and the exact doubled-bearer connection schedule.', stage: 'Before ordering fixings' },
  { id: 'ground', title: 'Footings', question: 'Specify hole shapes, dimensions, embedment and concrete from the actual ground and pile types.', stage: 'Before digging' },
  { id: 'access', title: 'One tread', question: 'Check the two proposed 250 mm rises, going/nosing, landing, supports and any required handrails.', stage: 'Before tread construction' },
  { id: 'materials', title: 'Decking product', question: 'Choose the actual 38 mm pine board, width, gap, finish, screws and stock/cut plan.', stage: 'Before ordering boards' }
];
const selectionData = {
  main: { title: 'Main deck', badge: 'Dimensions confirmed', type: 'green', values: [['Width × depth', '6600 × 2600 mm'], ['Area', '17.16 m²'], ['Garden drop', 'About 500 mm']], description: 'Freestanding. Boards run parallel to the frontage.', note: 'Member spans, supports and fixings remain provisional.', topic: 'layout' },
  rebuilt: { title: 'Rebuilt section', badge: 'Dimensions confirmed', type: 'green', values: [['Width × depth', '900 × 1970 mm'], ['Area', '1.773 m²'], ['Retained bearer', 'At back edge']], description: 'Three dashed joist continuations are shown as a layout option.', note: 'Check retained supports, combined loads, junction and bearing. Support separation to new rear bearer is about 2320 mm.', topic: 'junction' },
  tread: { title: 'One full-width tread', badge: 'Layout selected', type: 'green', values: [['Width × projection', '6600 × 400 mm'], ['Surface above garden', '250 mm proposed'], ['Area', '2.64 m²']], description: 'Deck → one tread → garden.', note: 'Two approximately 250 mm rises. Access geometry, supports and fixings need checking.', topic: 'access' },
  extension: { title: 'House extension', badge: 'Frontage confirmed', type: 'green', values: [['Frontage', '5700 mm'], ['Rebuilt alongside', '900 mm'], ['Rear extent', 'Not surveyed']], description: 'Deck remains independent of the house.', note: 'Verify cladding, door, vent and drainage clearances.', topic: 'layout' },
  bearer: { title: 'Bearers & piles', badge: 'Provisional', type: 'sand', values: [['New bearers', '2 double 140 × 45 lines'], ['Y centre lines', '350 / 2250 mm'], ['Separation', '1900 mm centres'], ['New piles', '12 proposed']], description: 'Six proposed pile positions on each new bearer line.', note: 'Check spans, footing/bracing requirements, ply joints and exact connectors.', topic: 'structure' },
  joists: { title: 'Joist layout', badge: 'Provisional', type: 'sand', values: [['Main lines', '16 · J01–J16'], ['Member', '140 × 45 H3.2 SG8'], ['First 2 bays', '427.5 mm centres'], ['Next 13 bays', '438.46 mm centres'], ['Rebuilt continuations', 'J01–J03 · candidates']], description: 'Joists run towards the garden. J01–J03 align within the 900 mm rebuilt strip.', note: 'Dashed continuity is not verified. The 4570 mm finished envelope is not a cut length. Extra butt supports and final rims/blocking remain to detail.', topic: 'junction' }
};
const sourceLabels = {
  'PROJECT.md': ['Project brief', 'Confirmed requirements and latest owner decisions'],
  'DESIGN.md': ['Design & geometry', 'Coordinates, framing concepts and access detail'],
  'MATERIALS.md': ['Materials & quantities', 'Conditional quantities, assumptions and price history'],
  'OPEN_ISSUES.md': ['Open design checks', 'Evidence needed before construction'],
  'SITE_MEASUREMENTS.md': ['Site measurements', 'Known dimensions and remaining field checks'],
  'BUILD_STEPS.md': ['Construction sequence', 'Draft phases, subject to the structural hold points'],
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
  $('#discussion-topics').innerHTML = `<caption>Items to confirm with the builder in person</caption><thead><tr><th scope="col">Check</th><th scope="col">Decision needed</th><th scope="col">When</th></tr></thead><tbody>${topicData.map(topic => `<tr id="discussion-${topic.id}" class="discussion-row"><th scope="row">${topic.title}</th><td>${topic.question}</td><td>${topic.stage}</td></tr>`).join('')}</tbody>`;
}
function renderJoistCoordinates() {
  $('#joist-coordinates tbody').innerHTML = JOIST_CENTRES.map((x, i) => `<tr><th scope="row">J${String(i + 1).padStart(2, '0')}</th><td>${Number(x.toFixed(2))}</td><td>${i < 3 ? 'Main + dashed rebuilt continuation candidate' : 'Main deck'}</td></tr>`).join('');
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
    $('#drawing-note').textContent = 'One full-width 400 mm tread, surface at 250 mm. Rises, supports and access geometry remain unverified.';
    $('#drawing-scale').textContent = 'SIDE PROFILE';
    selectArea('tread');
  } else {
    renderPlan(svg, { view, selected });
    $('#drawing-note').textContent = view === 'framing' ? '16 joist lines. Dashed J01–J03 are rebuilt-section continuation candidates. Check continuity, bearing, spans and fixings.' : 'Finished footprint. Extension rear extent is illustrative.';
    $('#drawing-scale').textContent = 'TOP VIEW';
    if (view === 'layout' && ['joists', 'bearer'].includes(selected)) selected = 'main';
    selectArea(selected);
  }
  $('#drawing-legend').innerHTML = view === 'framing' ? '<span><i class="legend-joist"></i>Joists</span><span><i class="legend-bearer"></i>Bearers</span><span><i class="legend-pile"></i>Piles</span>' : view === 'layout' ? '<span><i class="legend-main"></i>Deck</span><span><i class="legend-rebuilt"></i>Rebuilt</span><span><i class="legend-tread"></i>One tread</span>' : '<span>Surface levels proposed</span>';
}
function openTopic(id) {
  const topic = $(`#discussion-${id}`);
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
  printDetails = Array.from(document.querySelectorAll('.build-phase, .coordinate-details')).map(element => [element, element.open]);
  for (const [element] of printDetails) element.open = true;
});
window.addEventListener('afterprint', () => {
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
