import { renderPlan, renderElevation } from './diagrams.js';
import { renderBuildGuide } from './build-guide.js';

const $ = (selector) => document.querySelector(selector);
const topicData = [
  { id: 'layout', title: 'Layout & house interface', summary: 'Footprint, thresholds, drainage and clearances', question: 'Does the 6600 × 2600 mm main deck and 900 × 1970 mm rebuilt section fit the site? What cladding, door, ventilation, drainage or foundation clearance details are needed?' },
  { id: 'junction', title: 'Rebuilt section & retained bearer', summary: 'Joist junction, existing condition and shared loading', question: 'The retained bearer is at the rebuilt section’s back edge, approximately 2320 mm from the proposed rear bearer. How should the rebuilt joists meet or continue into the main deck without conflicting with its joists/rim? Check support condition, bearing and combined reactions.' },
  { id: 'structure', title: 'Framing, bracing & connections', summary: 'Spans, member grades, pile layout and exact fixings', question: 'Check the provisional double 140 × 45 bearers, 140 × 45 joists, proposed support locations and 12-pile concept against the applicable design requirements. Which bracing and exact pile-to-bearer-to-joist connection details are needed?' },
  { id: 'ground', title: 'Footings & ground', summary: 'Bearing, excavation, services and neighbouring footings', question: 'What ground, footing and embedment evidence is needed? Confirm ordinary versus bracing-pile requirements, footing shape, buried services and clearance from the house foundations. No excavation schedule is fixed.' },
  { id: 'access', title: 'Deck → tread → garden', summary: 'One full-width 400 mm tread, proposed halfway level', question: 'The owner wants one 6600 × 400 mm tread, with its surface 250 mm above the garden under a deck about 500 mm high. This creates two approximately 250 mm rises. Check the applicable access geometry, going/nosing, supports, slip resistance, landing/approach and any required level changes; the proposal is not verified.' },
  { id: 'materials', title: 'Decking & purchase plan', summary: '38 mm pine, actual width, finish and stock lengths', question: 'Pine decking at 38 mm thickness is selected. Board width is provisionally 138 mm. Confirm the exact product, treatment, actual sizes, wet/dry installation gap, fixing pattern, finish, available stock lengths and a supported butt-joint/cut plan before ordering.' }
];
const selectionData = {
  main: { number: '01', icon: '▤', title: 'The main deck', badge: 'Confirmed dimensions', type: 'green', values: [['Frontage', '6600 mm'], ['Depth', '2600 mm'], ['Area', '17.16 m²'], ['Garden drop', 'About 500 mm']], description: 'A full rectangle across the entire frontage, sitting independently of the house. Decking runs parallel to the frontage.', note: 'The shape is confirmed. Member spans, bracing, connections, footings and clearances are still provisional.', topic: 'layout' },
  rebuilt: { number: '02', icon: '↰', title: 'The rebuilt section', badge: 'Confirmed dimensions', type: 'green', values: [['Frontage', '900 mm'], ['Depth', '1970 mm'], ['Area', '1.773 m²'], ['Retained bearer', 'At back edge']], description: 'The demolished section is to be rebuilt beside the extension, behind its front face. It does not reduce the new deck’s 6600 mm frontage.', note: 'Approx. 2320 mm to the proposed rear bearer. Exact bearing faces, retained support condition and the joist junction need checking.', topic: 'junction' },
  tread: { number: '03', icon: '↳', title: 'One garden tread', badge: 'Owner’s selected layout', type: 'green', values: [['Width', '6600 mm · full-width'], ['Projection', '400 mm total'], ['Horizontal area', '2.64 m²'], ['Proposed surface', '250 mm above garden']], description: 'Deck → one tread → garden. A single full-width tread runs along the new deck’s garden edge, halfway down the approximately 500 mm drop.', note: 'The two approximately 250 mm rises are proposed geometry, not a verified access detail. Rises, going/nosing, landing and tread structure need checking.', topic: 'access' },
  extension: { number: '04', icon: '⌂', title: 'The house extension', badge: 'Frontage confirmed', type: 'green', values: [['Frontage', '5700 mm'], ['Rebuilt alongside', '900 mm'], ['House attachment', 'None proposed'], ['Back extent', 'Not surveyed here']], description: 'The extension and rebuilt section meet the front face at the same line. The new main deck sits in front of both.', note: 'Keep cladding, door flashings, vents and drainage clear. The extension’s drawn back extent is context, not a measured building plan.', topic: 'layout' },
  bearer: { number: '05', icon: '⫶', title: 'The framing concept', badge: 'Provisional · check required', type: 'sand', values: [['New bearers', '2 double 140 × 45 lines'], ['Centre separation', '1900 mm'], ['New piles', '12 proposed'], ['Joist layout', '16 main-only lines']], description: 'Two new bearer lines sit 350 mm and 2250 mm out from the house front face. Six proposed pile centres support each line.', note: 'Pile count, anchor/bracing allocation, spans, footing sizes and connector details are not verified. Main-only spacing does not settle the rebuilt junction.', topic: 'structure' }
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
const discussionOutcomes = {
  layout: 'Confirm the site fit, finished datum and house clearances.',
  junction: 'Agree retained-support reuse and a dimensioned joist/rim junction.',
  structure: 'Settle the member layout and exact bracing and connection schedule.',
  ground: 'Confirm ground suitability and a footing schedule for each support type.',
  access: 'Agree a verified access detail for the selected one-tread arrangement.',
  materials: 'Choose the actual product, fixing/gap guidance and a cut-by-stock list.'
};
function renderDiscussionTopics() {
  const container = $('#discussion-topics');
  container.replaceChildren();
  for (const [i, topic] of topicData.entries()) {
    const details = document.createElement('details');
    details.className = 'discussion-topic';
    details.id = `discussion-${topic.id}`;
    if (i === 0) details.open = true;
    details.innerHTML = `<summary><span class="topic-number">0${i + 1}</span><span class="topic-summary"><h3>${topic.title}</h3><p>${topic.summary}</p></span><span class="topic-chevron" aria-hidden="true">+</span></summary><div class="topic-body"><p class="topic-question">${topic.question}</p><p class="discussion-outcome"><strong>To settle together:</strong> ${discussionOutcomes[topic.id]}</p></div>`;
    container.append(details);
  }
}
let selected = 'main';
let currentView = 'layout';
function selectArea(id) {
  if (!selectionData[id]) return;
  selected = id;
  const data = selectionData[id];
  $('#selection-detail').innerHTML = `<div class="detail-kicker"><span>DESIGN DETAIL / ${data.number}</span><span class="detail-icon" aria-hidden="true">${data.icon}</span></div><h3 id="detail-title">${data.title}</h3><span class="badge badge-${data.type}">${data.badge}</span><dl class="detail-values">${data.values.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')}</dl><p class="detail-description">${data.description}</p><p class="detail-footnote">${data.note}</p><a class="detail-discussion-link" href="#discussion-${data.topic}">Discuss this with the builder <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg></a>`;
  for (const element of $('#design-drawing').querySelectorAll('[data-select]')) {
    const active = element.dataset.select === selected;
    element.classList.toggle('selected', active);
    element.setAttribute('aria-pressed', String(active));
  }
  $('.detail-discussion-link').addEventListener('click', () => openTopic(data.topic));
}
function setView(view) {
  currentView = view;
  $('#drawing-panel').classList.remove('is-zoomed');
  $('#zoom-drawing').setAttribute('aria-pressed', 'false');
  $('#zoom-drawing').textContent = 'Enlarge drawing +';
  for (const tab of document.querySelectorAll('[data-view]')) {
    const active = tab.dataset.view === view;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  }
  $('#drawing-panel').setAttribute('aria-labelledby', `tab-${view}`);
  const svg = $('#design-drawing');
  if (view === 'elevation') {
    renderElevation(svg);
    $('#drawing-note').textContent = 'Selected layout: deck → one full-width 400 mm tread → garden. Halfway tread surface at 250 mm is proposed; access geometry and structure need verification.';
    $('#drawing-scale').textContent = 'SCHEMATIC SIDE PROFILE';
    selectArea('tread');
  } else {
    renderPlan(svg, { view, selected });
    $('#drawing-note').textContent = view === 'framing' ? 'Dashed framing and pile locations are provisional. Retained support condition, spans, bracing, junctions and connections are not verified.' : 'Finished deck and full-width tread outlines shown to proportion. Extension back extent is contextual. Select an area for details.';
    $('#drawing-scale').textContent = 'DIMENSIONS IN MM';
    selectArea(selected);
  }
}
function openTopic(id) {
  const topic = $(`#discussion-${id}`);
  if (topic) topic.open = true;
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
  $('#zoom-drawing').textContent = zoomed ? 'Fit to screen −' : 'Enlarge drawing +';
});
$('#reset-view').addEventListener('click', () => { selected = 'main'; setView('layout'); });

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
renderBuildGuide($('#build-phases'));
let printDetails = [];
window.addEventListener('beforeprint', () => {
  printDetails = Array.from(document.querySelectorAll('.build-phase, .discussion-topic')).map(element => [element, element.open]);
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
  toast('Guide downloaded. Open the HTML file on site or share it with your builder.');
});
setView('layout');
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
