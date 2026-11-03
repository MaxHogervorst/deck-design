import { renderAssemblyDiagram } from './assembly-diagrams.js';

const assemblySteps = [
  { id: 'outline', title: 'Mark the deck outline', picture: 'setout', parts: 'Corner marks and string', tools: 'Tape · string · square', action: 'Mark the 6600 × 2600 mm main rectangle. Add the 900 × 1970 mm rebuilt section behind its left end.', check: 'Both main-deck diagonals ≈ 7094 mm. Check the 6600 mm frontage is one straight line.', status: 'Layout dimensions', detail: 'Coordinates start at the left front face of the extension: X across, Y towards the garden.' },
  { id: 'pile-centres', title: 'Mark P01–P12', picture: 'pile-grid', parts: 'P01–P06 rear row · P07–P12 front row', tools: 'Tape · string · marker', action: 'Mark six X centres on each row: 250, 1470, 2690, 3910, 5130, 6350 mm. Rear row Y=350; front row Y=2250.', check: 'Five 1220 mm bays per row. Row centres are 1900 mm apart.', status: 'Proposed set-out', detail: 'Mark only. Pile classes, final positions and footing dimensions require FP01; these marks are not a digging schedule.' },
  { id: 'piles', title: 'Install P01–P12 to FP01', picture: 'pile-grid', parts: 'P01–P12 · concrete specified in FP01', tools: 'Level or laser · temporary braces', action: 'Use the reviewed footing schedule for each pile. Plumb and brace the piles, then place and cure the specified concrete.', check: 'Transfer pile-top marks from the deck datum: subtract actual decking + joist + bearer depths + DPC thickness.', status: 'Needs FP01', detail: 'Missing: ordinary/anchor allocation, hole dimensions, embedment, concrete and curing period. Nominal stack subtraction is 38+140+140=318 mm; pile top is about 182 mm above level garden before DPC.' },
  { id: 'bearers', title: 'Seat the doubled bearers', picture: 'bearer', parts: 'BA-1 + BA-2 rear · BB-1 + BB-2 front · separation pads', tools: 'Level · clamps · selected fixing tools', action: 'Place each pair side by side on its specified pile bearing/separation detail. Set the bearer centres on rows A and B.', check: 'Each double bearer is nominally 90 mm wide × 140 mm deep. Keep both rows straight and at the same top datum.', status: 'Needs AP01', detail: 'Use the reviewed ply, splice and pile-connection schedule. At anchor piles, install the complete specified connection. MiTek 12KNH is a candidate, not yet verified for these doubled bearers or the low pile height.' },
  { id: 'joists', title: 'Place J01–J16 and edge rims', picture: 'joists', parts: 'J01–J16 · RM1 front rim · RM2 rear rim line', tools: 'Tape · square · level · clamps', action: 'Set J01/J02/J03 at X=22.5/450/877.5 mm, then the remaining centres from the coordinate table. Fit RM1/RM2 to AP01, splitting or terminating RM2 around the continuous J01–J03 option.', check: 'First two bays: 427.5 mm. Next 13: ≈438.46 mm. Tops align; bearing, rim joints and lateral restraint match the plan.', status: 'Cuts / connections pending', detail: '4570 mm and 2600 mm are finished joist envelopes, not cut lengths. Each rim line has a 6600 mm overall envelope; RM2 cannot pass through the three continuous joists. AP01 must settle cuts, bearing, continuity, joist ties and rim/blocking connections.' },
  { id: 'cross-blocks', title: 'Insert B01–B12 flush', picture: 'blocking', parts: '12 cross-blocks · nominal clear length 382.5 mm', tools: 'Tape · square · clamps', action: 'Fit two blocks between J01/J02/J03 at each of the six marked rows. Set every block top flush with the joist tops.', check: 'Y centres: −1947.5, −1562.5, −1177.5, −792.5, −407.5, −22.5 mm. Row spacing: 385 mm.', status: 'Block joints need AP01', detail: 'Use the reviewed block-end structural fixings or hangers. Decking screws are not a structural block-connection specification.' },
  { id: 'deck-boards', title: 'Fix boards across their supports', picture: 'boards', parts: '38 mm pine boards · selected exterior board fixings', tools: 'Drill/driver · gap spacers · straightedge', action: 'Run main boards across the frontage. Run the illustrated rebuilt boards along the 1970 mm depth and fix down at the cross-support rows.', check: 'Two fixing positions per board/support are illustrated. Every butt end has support; gaps and edge strips match the selected board guidance.', status: 'Needs DF01', detail: 'DF01 must name the actual board, gap, screw type/length, corrosion rating and edge distances. The dot pattern is not a complete screw schedule.' },
  { id: 'tread-frame', title: 'Assemble R1/R2 with T01–T16', picture: 'tread-box', parts: '2 rails, nominal 6600 mm · 16 crosspieces, nominal 310 mm', tools: 'Tape · square · clamps · selected joint fixings', action: 'Keep the two rails parallel. Place T01–T16 between them, including the end pieces, with all 140 mm-deep members standing on edge.', check: 'Outside frame: 6600 × 400 mm. Clear distance between 45 mm rails: 310 mm. Diagonals ≈ 6612 mm.', status: 'Joint / timber spec needs GP01', detail: 'One layer only. Low-clearance treatment/grade, rail splices and crosspiece connections must be specified in GP01. Nominal dimensions are not a cut order.' },
  { id: 'ground', title: 'Bear on G01–G12; anchor the rails', picture: 'tread-ground', parts: 'G01–G12 concrete bearing heads · DPC · C1/C2/C3 connection set', tools: 'Level · anchor-installation tools specified by GP01', action: 'Seat both rails directly on the specified separation and concrete bearings. Fit the reviewed side-restraint connection: C1 bracket to rail with C3 fixings, and to concrete with C2 anchors.', check: 'Weight follows rail → separation → concrete → suitable ground. The connector restrains movement/uplift; it does not suspend the rail.', status: 'Needs GP01', detail: 'Six stations provide twelve rail bearings. Frame underside is nominally 72 mm above garden; allow for DPC. GP01 must give footing depth/size, bracket, anchor embedment/edge distances, timber fasteners and anchorage capacity. Do not use loose pavers or copy a post-shoe detail.' },
  { id: 'tread-boards', title: 'Fix TD1–TD3 to the tread frame', picture: 'tread-boards', parts: '3 tread-board rows illustrated · actual width / edge rips from DF01', tools: 'Driver · spacers · level', action: 'Lay the 38 mm boards across the tread crosspieces. Set the selected gaps and rip the two edge rows to keep the total projection at 400 mm.', check: 'Target surface: 250 mm above garden. Frame top: 212 mm; underside: 72 mm, before actual-size/separation adjustments.', status: 'Needs DF01 + GP01', detail: 'Three rows assume 138 mm boards. Edge widths depend on the actual board and gap. Complete the reviewed access/nosing detail; no second tread is proposed.' },
  { id: 'final', title: 'Measure the finished result', picture: 'finish', parts: 'Agreed plan and fixing schedules', tools: 'Tape · level · straightedge', action: 'Compare the finished deck, one tread and garden levels with the agreed plan. Check the specified structural and board fixings are complete.', check: 'Main deck about 500 mm; one tread selected at 250 mm; full-width tread projection 400 mm. Check the actual rise/going detail, edges and finish.', status: 'Owner completion check', detail: 'This is the owner’s check against the pre-build plan, not a scheduled builder visit. Resolve differences from that plan before using the deck.' }
];
let assemblyCurrent = 0;
let assemblyPrint = false;
function showAssemblyStep(index, moveFocus = false) {
  assemblyCurrent = Math.max(0, Math.min(assemblySteps.length - 1, index));
  document.querySelectorAll('.assembly-step').forEach((card, i) => { card.hidden = !assemblyPrint && i !== assemblyCurrent; });
  document.querySelectorAll('[data-assembly-index]').forEach((button, i) => {
    button.classList.toggle('is-current', i === assemblyCurrent);
    if (i === assemblyCurrent) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  });
  document.getElementById('assembly-count').textContent = `${assemblyCurrent + 1} / ${assemblySteps.length}`;
  document.getElementById('assembly-prev').disabled = assemblyCurrent === 0;
  document.getElementById('assembly-next').disabled = assemblyCurrent === assemblySteps.length - 1;
  if (moveFocus) document.querySelector(`.assembly-step[data-step-index="${assemblyCurrent}"] h3`).focus({ preventScroll: true });
}
export function setAssemblyPrintMode(enabled) {
  assemblyPrint = enabled;
  showAssemblyStep(assemblyCurrent);
}
export function renderBuildGuide(container) {
  container.innerHTML = `<details class="assembly-parts"><summary>Parts used in the assembly pictures</summary><div class="table-scroll"><table><thead><tr><th>IDs</th><th>Part</th><th>Quantity / nominal geometry</th></tr></thead><tbody>
    <tr><th>P01–P12</th><td>Main piles</td><td>12 proposed; types and lengths from FP01</td></tr>
    <tr><th>BA-1/BA-2 · BB-1/BB-2</th><td>Double-bearer plies</td><td>4 × 6600 mm nominal; joints from AP01</td></tr>
    <tr><th>J01–J03 / J04–J16</th><td>Main joist lines</td><td>3 continuation candidates + 13 main; finished envelopes 4570 / 2600 mm, not cuts</td></tr>
    <tr><th>RM1 / RM2</th><td>Front / rear rim lines</td><td>2 × 6600 mm overall allowance; rear split around J01–J03 to AP01, not two approved cuts</td></tr>
    <tr><th>B01–B12</th><td>Rebuilt cross-blocks</td><td>12 × 382.5 mm nominal clear length</td></tr>
    <tr><th>R1/R2 · T01–T16</th><td>Tread rails / crosspieces</td><td>2 × 6600 + 16 × 310 mm nominal; grade/treatment from GP01</td></tr>
    <tr><th>G01–G12 · DPC · C1/C2/C3</th><td>Tread bearings / separation / restraint</td><td>12 connection locations; footing and hardware schedule from GP01</td></tr>
    <tr><th>TD1–TD3</th><td>Tread-board rows</td><td>3 illustrated; actual board, gaps, edge rips and screws from DF01</td></tr>
  </tbody></table></div></details>
  <div class="assembly-inputs"><strong>Four plan inputs still needed:</strong> FP01 main footings/pile classes · AP01 pile/joist connections and blocking · GP01 tread foundations/restraint/timber · DF01 boards and screws. Pictures show proposed assembly; do not substitute the sketch for these details.</div>
  <nav class="assembly-nav" aria-label="Assembly steps">${assemblySteps.map((step, i) => `<button type="button" data-assembly-index="${i}" title="${step.title}">${String(i + 1).padStart(2, '0')}</button>`).join('')}</nav>
  <div class="assembly-controls"><button class="button button-small" id="assembly-prev">Previous</button><span id="assembly-count" role="status" aria-live="polite"></span><button class="button button-small" id="assembly-next">Next</button></div>
  <div class="assembly-cards">${assemblySteps.map((step, i) => `<article class="assembly-step" data-step-index="${i}" id="assembly-step-${i + 1}" ${i ? 'hidden' : ''}><div class="assembly-step-heading"><span class="assembly-number">${String(i + 1).padStart(2, '0')}</span><h3 tabindex="-1">${step.title}</h3><span class="badge badge-sand">${step.status}</span></div><div class="assembly-step-layout"><div class="assembly-picture"><svg xmlns="http://www.w3.org/2000/svg" data-assembly-picture="${step.picture}" aria-label="${step.title}"></svg></div><div class="assembly-instruction"><p class="assembly-parts-line"><strong>Parts</strong> ${step.parts}</p><p class="assembly-tools"><strong>Tools</strong> ${step.tools}</p><p class="assembly-action">${step.action}</p><p class="assembly-check"><strong>Check</strong> ${step.check}</p><p class="assembly-detail">${step.detail}</p></div></div></article>`).join('')}</div>`;
  for (const svg of container.querySelectorAll('[data-assembly-picture]')) {
    renderAssemblyDiagram(svg, svg.dataset.assemblyPicture);
    const controls = document.createElement('div');
    controls.className = 'assembly-picture-tools';
    const zoom = document.createElement('button');
    zoom.type = 'button';
    zoom.className = 'text-button';
    zoom.textContent = 'Enlarge picture';
    zoom.setAttribute('aria-pressed', 'false');
    zoom.addEventListener('click', () => {
      const enlarged = svg.parentElement.classList.toggle('is-zoomed');
      zoom.textContent = enlarged ? 'Fit picture' : 'Enlarge picture';
      zoom.setAttribute('aria-pressed', String(enlarged));
    });
    controls.append(zoom);
    svg.before(controls);
  }
  container.querySelectorAll('[data-assembly-index]').forEach(button => button.addEventListener('click', () => showAssemblyStep(Number(button.dataset.assemblyIndex), true)));
  document.getElementById('assembly-prev').addEventListener('click', () => showAssemblyStep(assemblyCurrent - 1, true));
  document.getElementById('assembly-next').addEventListener('click', () => showAssemblyStep(assemblyCurrent + 1, true));
  showAssemblyStep(0);
}
