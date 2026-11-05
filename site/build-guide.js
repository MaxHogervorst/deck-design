import { renderAssemblyDiagram } from './assembly-diagrams.js';

const assemblySteps = [
  {
    "id": "levels",
    "title": "Settle levels before any foundations",
    "picture": "finish",
    "parts": "Agreed GP01 levels + FP01/AP01/DF01",
    "tools": "Laser or level · tape",
    "action": "Set one deck datum, the final garden landing level and the one-tread level. Agree these with the complete foundation and connection plan before construction.",
    "check": "Current 500 mm drop ÷ 2 rises = 250 mm each. BRANZ gives 190 mm maximum for common/main private stairs; this combination is on hold.",
    "status": "Levels unresolved",
    "detail": "One tread and 400 mm projection stay in the brief. To use that 190 mm guidance, two rises total at most 380 mm. Any level solution must also recheck timber clearance and foundation heights; no landing change is selected."
  },
  {
    "id": "outline",
    "title": "Mark the whole footprint",
    "picture": "setout",
    "parts": "Main + rebuilt + tread outline marks",
    "tools": "Tape · string · square",
    "action": "Mark the 6600 × 2600 mm deck, 900 × 1970 mm rebuilt section and full-width 6600 × 400 mm tread from one baseline.",
    "check": "Main diagonals ≈7094 mm. X runs across the frontage; Y=0 is the extension front face, positive towards the garden.",
    "status": "Confirmed footprints",
    "detail": "The tread ends at Y=3000. The retained bearer is near Y=−1970; verify its actual bearing faces, condition and capacity before relying on it."
  },
  {
    "id": "supports",
    "title": "Mark all foundation positions",
    "picture": "pile-grid",
    "parts": "P01–P12 main pile marks + GP01 tread support marks",
    "tools": "Tape · strings · level",
    "action": "Transfer the agreed main and tread foundation layouts together. Label ordinary and bracing piles from FP01/AP01.",
    "check": "Main proposal: X=250/1470/2690/3910/5130/6350; Y=350/2250. Main bays 1220 mm; rows 1900 mm apart.",
    "status": "Needs FP01 + GP01",
    "detail": "Tread footing number and locations remain to design. The former twelve-concrete-bearing layout is withdrawn; it was not a verified requirement."
  },
  {
    "id": "foundations",
    "title": "Build all foundations in one operation",
    "picture": "tread-ground",
    "parts": "Main piles/concrete + specified tread foundations and restraint components",
    "tools": "Excavation · level · temporary braces · specified installation tools",
    "action": "Install the main piles and ground-supported tread foundations to their respective schedules. Set every bearing height from the same agreed levels; cure concrete as specified.",
    "check": "Main pile-top arithmetic at the old datum: 500−38−140−140=182 mm before DPC. Tread bearing heights depend on the resolved levels and frame.",
    "status": "Schedules required",
    "detail": "The picture shows a typical tread bearing, not hole dimensions or an anchor recipe. FP01/GP01 must give footing sizes/depths, ground basis, separation, restraint products and installation details."
  },
  {
    "id": "bearers",
    "title": "Seat and connect both bearer lines",
    "picture": "bearer",
    "parts": "BA-1/BA-2 rear · BB-1/BB-2 front · AP01 connections",
    "tools": "Level · strings · clamps · specified fixing tools",
    "action": "Place the doubled bearers on their scheduled bearing/separation. Install ply, splice and pile connections from AP01.",
    "check": "Each pair is nominally 90 wide ×140 deep. Rear/front centres Y=350/2250; both tops share one datum.",
    "status": "Needs AP01",
    "detail": "Review 1220 mm pile spans, 250 mm end offsets and bracing in both directions. MiTek 12KNH is only a candidate; doubled-bearer fit and complete rated connection remain unverified. Splices need approved ordinary-pile locations."
  },
  {
    "id": "joists",
    "title": "Fit J01–J16 and the edge rims",
    "picture": "joists",
    "parts": "J01–J16 · RM1 front · RM2 rear rim line",
    "tools": "Tape · square · level · clamps",
    "action": "Set J01/J02/J03 at X=22.5/450/877.5, then use the coordinate table. Fit rims without crossing the three continuous-joist candidates.",
    "check": "First two bays 427.5 mm; next thirteen ≈438.46 mm. Support separations ≈2320/1900 mm for J01–J03; main end projections 350 mm from bearer centres.",
    "status": "Cuts / bearing unresolved",
    "detail": "4570/2600 mm are finished envelopes, not joist cuts. Rim thickness changes actual member ends. Verify retained support, wet-service spans, cantilevers, bearing, lateral restraint and the anchor-pile/joist alignment."
  },
  {
    "id": "cross-blocks",
    "title": "Fit the rebuilt-board supports",
    "picture": "blocking",
    "parts": "B01–B12 + AP01 structural block-end fixings",
    "tools": "Tape · square · straightedge · clamps",
    "action": "Fit two flush cross-blocks between J01/J02/J03 at each of the six rows. Complete the rim junction and supported board-joint framing.",
    "check": "Y centres −1947.5/−1562.5/−1177.5/−792.5/−407.5/−22.5; 385 mm spacing. Nominal clear blocks 382.5 mm.",
    "status": "Needs AP01",
    "detail": "The rebuilt boards are illustrated running in Y, across these blocks. Block-end structural fixings differ from decking screws. Add final butt-joint support before covering the frame."
  },
  {
    "id": "tread-frame",
    "title": "Fit the tread frame on its foundations",
    "picture": "tread-box",
    "parts": "R1/R2 rails · T01–T16 crosspieces, geometry proposal only",
    "tools": "Tape · square · clamps · specified connection tools",
    "action": "Assemble the reviewed single-layer frame on its prepared ground supports. Install the specified restraint and separation. Keep it structurally independent of the main deck.",
    "check": "Proposed outside frame 6600 ×400; two 45 mm rails leave 310 mm nominal crosspieces. Frame diagonal ≈6612 mm.",
    "status": "Needs resolved GP01",
    "detail": "140 mm depth is a trial section. At the old 250 mm surface it leaves only 72 mm underside clearance. Final levels may require another section/support detail; do not release these cuts or assume twelve footings."
  },
  {
    "id": "frame-check",
    "title": "Check the complete uncovered structure",
    "picture": "joists",
    "parts": "Main + rebuilt + tread frames · agreed connection schedules",
    "tools": "Level · tape · straightedge",
    "action": "Check both frames, the retained support, cross-blocks and all concealed structural connections before laying any boards.",
    "check": "Confirm levels, bearing, specified bracing/anchors, rim joints, board-end supports and tread stability against the agreed plan.",
    "status": "Owner check before covering",
    "detail": "Main load path: boards → joists/blocks → bearers → piles → soil. Tread: boards → box frame → its foundations → soil. No support from fascia, cladding or deck boards; no builder inspection visit is assumed."
  },
  {
    "id": "boards",
    "title": "Lay boards on all three areas",
    "picture": "boards",
    "parts": "38 mm pine main/rebuilt boards + TD1–TD3 illustrated tread rows",
    "tools": "Driver · spacers · straightedge · saw",
    "action": "Lay main boards across X, rebuilt boards in the illustrated Y direction, then the tread boards across the short supports. Use DF01 throughout.",
    "check": "All butt ends supported; actual product gaps, edge rows, screws and edge distances followed. Keep the tread within the 400 mm envelope including the agreed edge/nosing detail.",
    "status": "Needs DF01",
    "detail": "19 main +7 rebuilt +3 tread rows give 158.99 lm before stock losses/waste with assumed 138 mm boards. This is one provisional stock scenario. The three tread rows need rips; two fixing dots per support are illustrative."
  },
  {
    "id": "final",
    "title": "Measure the complete finished route",
    "picture": "finish",
    "parts": "Deck → one tread → garden · agreed levels and fixing schedules",
    "tools": "Tape · level · straightedge",
    "action": "Check the finished assembly against the resolved plan, including actual rises, going, edges, board fixings and stable ground support.",
    "check": "One full-width 6600 ×400 tread. Use the agreed finished levels, not the unresolved halfway-height target.",
    "status": "Owner completion check",
    "detail": "The pictured 500/250 mm arrangement records the unresolved starting geometry. It is not the construction target. Resolve differences from the agreed plan before use."
  }
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
    <tr><th>R1/R2 · T01–T16</th><td>Tread rails / crosspieces</td><td>2 ×6600 +16 ×310 mm trial geometry; depth, treatment and cuts from resolved GP01</td></tr>
    <tr><th>GP01 · DPC · C1/C2/C3</th><td>Tread foundations / separation / restraint</td><td>Count and positions TBD; typical connection families only</td></tr>
    <tr><th>TD1–TD3</th><td>Tread-board rows</td><td>3 illustrated; actual board, gaps, edge rips and screws from DF01</td></tr>
  </tbody></table></div></details>
  <div class="assembly-inputs"><strong>Levels first, then one build:</strong> GP01 final access levels + tread foundations/frame · FP01 main footings · AP01 spans/bracing/connections · DF01 boards/fixings. All foundations and all framing precede decking.</div>
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
