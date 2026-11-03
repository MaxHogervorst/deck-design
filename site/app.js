import { renderPlan, renderElevation } from './diagrams.js';

const $ = (selector) => document.querySelector(selector);
const STORAGE_KEY = 'auckland-deck-review-v1';
const topicData = [
  { id: 'layout', title: 'Layout & house interface', summary: 'Footprint, thresholds, drainage and clearances', question: 'Does the 6600 × 2600 mm main deck and 900 × 1970 mm rebuilt section fit the site? What cladding, door, ventilation, drainage or foundation clearance details are needed?', placeholder: 'Note any site conflicts, clearance details or measurements to check…' },
  { id: 'junction', title: 'Rebuilt section & retained bearer', summary: 'Joist junction, existing condition and shared loading', question: 'The retained bearer is at the rebuilt section’s back edge, approximately 2320 mm from the proposed rear bearer. How should the rebuilt joists meet or continue into the main deck without conflicting with its joists/rim? Check support condition, bearing and combined reactions.', placeholder: 'Suggest a junction detail or record the evidence needed to reuse the bearer…' },
  { id: 'structure', title: 'Framing, bracing & connections', summary: 'Spans, member grades, pile layout and exact fixings', question: 'Check the provisional double 140 × 45 bearers, 140 × 45 joists, proposed support locations and 12-pile concept against the applicable design requirements. Which bracing and exact pile-to-bearer-to-joist connection details are needed?', placeholder: 'Include the applicable source, detail number and any assumptions…' },
  { id: 'ground', title: 'Footings & ground', summary: 'Bearing, excavation, services and neighbouring footings', question: 'What ground, footing and embedment evidence is needed? Confirm ordinary versus bracing-pile requirements, footing shape, buried services and clearance from the house foundations. No excavation schedule is fixed.', placeholder: 'Record ground observations and the proposed verification or footing detail…' },
  { id: 'access', title: 'Deck → tread → garden', summary: 'One full-width 400 mm tread, proposed halfway level', question: 'The owner wants one 6600 × 400 mm tread, with its surface 250 mm above the garden under a deck about 500 mm high. This creates two approximately 250 mm rises. Check the applicable access geometry, going/nosing, supports, slip resistance, landing/approach and any required level changes; the proposal is not verified.', placeholder: 'Comment on the proposed levels and the detail needed to make the access work…' },
  { id: 'materials', title: 'Decking & purchase plan', summary: '38 mm pine, actual width, finish and stock lengths', question: 'Pine decking at 38 mm thickness is selected. Board width is provisionally 138 mm. Confirm the exact product, treatment, actual sizes, wet/dry installation gap, fixing pattern, finish, available stock lengths and a supported butt-joint/cut plan before ordering.', placeholder: 'Recommend a specific product or identify quantities, cuts and pricing to confirm…' }
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
const emptyState = () => ({ name: '', topics: Object.fromEntries(topicData.map(t => [t.id, { status: '', note: '' }])) });
let state = emptyState();
let storageAvailable = true;
try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  if (saved && typeof saved === 'object') {
    if (typeof saved.name === 'string') state.name = saved.name.slice(0, 100);
    for (const topic of topicData) {
      const entry = saved.topics?.[topic.id];
      if (!entry || typeof entry !== 'object') continue;
      state.topics[topic.id] = { status: ['', 'reasonable', 'change', 'professional'].includes(entry.status) ? entry.status : '', note: typeof entry.note === 'string' ? entry.note.slice(0, 6000) : '' };
    }
  }
} catch { storageAvailable = false; }
let toastTimer;
function toast(message) {
  clearTimeout(toastTimer);
  $('#toast').textContent = message;
  $('#toast').classList.add('visible');
  toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 4200);
}
function save() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
  catch {
    if (storageAvailable) toast('Browser storage is unavailable. Download your review before closing this page.');
    storageAvailable = false;
    $('.privacy-note').textContent = 'Notes are available for this session. Browser storage is unavailable: download the review before closing this page. Nothing is submitted automatically.';
  }
  updateProgress();
}
function reviewed(entry) { return Boolean(entry.status || entry.note.trim()); }
function updateProgress() {
  let count = 0;
  for (const topic of topicData) {
    const done = reviewed(state.topics[topic.id]);
    if (done) count++;
    const label = $(`#topic-status-${topic.id}`);
    label.textContent = done ? 'Has feedback' : 'Not reviewed';
    label.classList.toggle('is-reviewed', done);
  }
  $('#review-count').textContent = `${count} of ${topicData.length}`;
  $('#progress-fill').style.width = `${count / topicData.length * 100}%`;
}
function renderTopics() {
  const container = $('#review-topics');
  container.replaceChildren();
  for (const [i, topic] of topicData.entries()) {
    const details = document.createElement('details');
    details.className = 'review-topic';
    details.id = `review-${topic.id}`;
    if (i === 0) details.open = true;
    details.innerHTML = `<summary><span class="topic-number">0${i + 1}</span><span class="topic-summary"><h3>${topic.title}</h3><p>${topic.summary}</p></span><span class="topic-status" id="topic-status-${topic.id}">Not reviewed</span><span class="topic-chevron" aria-hidden="true">+</span></summary><div class="topic-body"><p class="topic-question">${topic.question}</p><label for="status-${topic.id}">Your assessment</label><select id="status-${topic.id}"><option value="">Choose an assessment…</option><option value="reasonable">Looks reasonable as a concept</option><option value="change">Suggest a change</option><option value="professional">Needs specialist verification</option></select><label for="note-${topic.id}">Notes, questions or source details</label><textarea id="note-${topic.id}" maxlength="6000" placeholder="${topic.placeholder}"></textarea></div>`;
    container.append(details);
    const select = $(`#status-${topic.id}`);
    const note = $(`#note-${topic.id}`);
    select.value = state.topics[topic.id].status;
    note.value = state.topics[topic.id].note;
    select.addEventListener('change', () => { state.topics[topic.id].status = select.value; save(); });
    note.addEventListener('input', () => { state.topics[topic.id].note = note.value; save(); });
  }
}
let selected = 'main';
let currentView = 'layout';
function selectArea(id) {
  if (!selectionData[id]) return;
  selected = id;
  const data = selectionData[id];
  $('#selection-detail').innerHTML = `<div class="detail-kicker"><span>DESIGN DETAIL / ${data.number}</span><span class="detail-icon" aria-hidden="true">${data.icon}</span></div><h3 id="detail-title">${data.title}</h3><span class="badge badge-${data.type}">${data.badge}</span><dl class="detail-values">${data.values.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')}</dl><p class="detail-description">${data.description}</p><p class="detail-footnote">${data.note}</p><a class="detail-review-link" href="#review-${data.topic}">Review this detail <span aria-hidden="true">↗</span></a>`;
  for (const element of $('#design-drawing').querySelectorAll('[data-select]')) {
    const active = element.dataset.select === selected;
    element.classList.toggle('selected', active);
    element.setAttribute('aria-pressed', String(active));
  }
  $('.detail-review-link').addEventListener('click', () => openTopic(data.topic));
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
  const topic = $(`#review-${id}`);
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
const assessmentLabels = { reasonable: 'Looks reasonable as a concept', change: 'Suggest a change', professional: 'Needs specialist verification' };
function reviewText() {
  const lines = ['# Auckland deck — design review', '', 'Design revision: 01 · 03 November 2026', `Reviewer: ${state.name.trim() || 'Not specified'}`, `Feedback exported: ${new Intl.DateTimeFormat('en-NZ', { dateStyle: 'medium', timeZone: 'Pacific/Auckland' }).format(new Date())}`, '', 'This is reviewer feedback, not structural certification or construction approval.', '', '## Design being reviewed', '', '- Main deck: 6600 × 2600 mm; rebuilt section: 900 × 1970 mm.', '- Main + rebuilt: 18.933 m², excluding tread.', '- One full-width 6600 × 400 mm tread; proposed surface 250 mm above garden beneath deck about 500 mm high.', '- Pine decking: 38 mm thick; 138 mm board width remains provisional.', '- Structural, footing, connector, access and clearance verification remains open.', ''];
  for (const topic of topicData) {
    const entry = state.topics[topic.id];
    lines.push(`## ${topic.title}`, '', `Assessment: ${assessmentLabels[entry.status] || 'Not reviewed'}`, '', entry.note.trim() || '_No notes._', '');
  }
  return lines.join('\n');
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
renderTopics();
$('#reviewer-name').value = state.name;
$('#reviewer-name').addEventListener('input', event => { state.name = event.target.value; save(); });
$('#download-review').addEventListener('click', () => { download('auckland-deck-review.md', reviewText(), 'text/markdown;charset=utf-8'); toast('Review downloaded. Send the file to the project owner.'); });
$('#copy-review').addEventListener('click', () => copy(reviewText(), 'Review copied. Paste it into your message to the owner.'));
$('#clear-review').addEventListener('click', () => {
  if (!window.confirm('Clear your name and all review notes saved in this browser?')) return;
  state = emptyState();
  $('#reviewer-name').value = '';
  renderTopics();
  save();
  toast('Your review notes have been cleared.');
});
updateProgress();
if (!storageAvailable) $('.privacy-note').textContent = 'Notes are available for this session. Download your review before closing this page. Nothing is submitted automatically.';

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
  clone.querySelectorAll('input').forEach(input => input.removeAttribute('value'));
  clone.querySelectorAll('textarea').forEach(textarea => { textarea.textContent = ''; });
  clone.querySelectorAll('option').forEach(option => option.removeAttribute('selected'));
  clone.querySelector('#toast').textContent = '';
  clone.querySelector('#toast').classList.remove('visible');
  download('auckland-deck-design.html', '<!doctype html>\n' + clone.outerHTML, 'text/html;charset=utf-8');
  toast('Website downloaded. Send the HTML file to your reviewers.');
});
setView('layout');
if (location.hash.startsWith('#review-')) openTopic(location.hash.slice('#review-'.length));
