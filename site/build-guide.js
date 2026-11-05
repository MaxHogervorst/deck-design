import { renderAssemblyDiagram } from './assembly-diagrams.js';

const assemblySteps = [
  {
    "id": "levels",
    "title": "Mark the selected height datums",
    "picture": "finish",
    "parts": "Deck 500 · tread 250 mm above garden · 32 mm boards",
    "tools": "Laser or level · tape",
    "action": "Use the owner-selected levels: deck about 500 mm above garden, one tread at 250 mm, 400 mm total projection. Carry these datums through the foundation and framing plans.",
    "check": "Nominal main pile top188 mm; tread frame top218 /underside78 mm before separation and actual timber sizes. Board width is approximately80 mm, not yet measured.",
    "status": "Owner levels retained",
    "detail": "Access compliance is not verified. Main framing is based on a 2 kPa residential deck without a cantilevered barrier; ground is reported firm natural. Retained support and exact connection details still need verification."
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
    "parts": "P01–P12 main · M1/M2 intermediate rebuilt piles · six tread pads",
    "tools": "Tape · strings · level",
    "action": "Mark the two main rows and six shared tread pads at the same X stations. Mark M1/M2 at X=175/725, Y=−800 for the new 900 mm bearer.",
    "check": "Main X=250/1470/2690/3910/5130/6350; Y=350/2250. Proposed anchor piles P01/P03/P06/P07/P09/P12; remaining main and M piles ordinary.",
    "status": "Specific proposal for review",
    "detail": "Anchor lines at X=250/2690/6350 have gaps 2440/3660 mm. Six pads span both tread rails; they are six foundations, not twelve."
  },
  {
    "id": "foundations",
    "title": "Build all foundations in one operation",
    "picture": "tread-ground",
    "parts": "6 anchor +6 ordinary main piles ·2 ordinary M piles ·6 shared tread pads",
    "tools": "Excavation · level · temporary braces · specified installation tools",
    "action": "Use the footing schedule after its ground and connection assumptions are confirmed. Install all foundations before framing; set bearing tops from the selected datums.",
    "check": "Planning sizes: anchors Ø400×900 deep; ordinary main Ø400×450; M piles 350 square×450. Keep at least 100 mm concrete under timber piles.",
    "status": "Conditional foundation schedule",
    "detail": "Tread pad proposal:500 across the tread ×300 alongX,300 below cleared ground, raised to the bearing datum. With32 mm boards and2 mm separation, pad head is76 mm; calculated net concrete≈1.35 m³ before waste under the stated datum assumption. Ground bearing and exact pad/anchor details still require review."
  },
  {
    "id": "bearers",
    "title": "Seat and connect both bearer lines",
    "picture": "bearer",
    "parts": "BA/BB doubled main bearers · BC new 900 mm doubled bearer · complete connections",
    "tools": "Level · strings · clamps · specified fixing tools",
    "action": "Seat the two main bearer lines and BC at Y=−800. Keep the proposed double 140×45 sections; obtain the ply, splice and rated connection detail before fastening.",
    "check": "Main pile centres 1220 mm apart. Splice main bearers over ordinary piles at X=3910, not the six anchor locations.",
    "status": "Gravity benchmark found; joints pending",
    "detail": "BRANZ’s published wet-service example uses a solid 140×70 bearer at 1.3 m spans /2.3 m loaded dimension. The doubled 140×45 proposal has greater section width but is not validated as a built-up member merely by that comparison."
  },
  {
    "id": "joists",
    "title": "Fit J01–J19, butt sisters and rims",
    "picture": "joists",
    "parts": "4 long joists +15 main-only · BJ1/BJ2 · RM1/RM2",
    "tools": "Tape · square · level · clamps",
    "action": "Use centres 22.5/307.5/592.5/877.5, then fifteen 380 mm bays. Add BJ1/BJ2 beside J08/J12 for board seams. Keep J01–J04 continuous through the rebuilt strip.",
    "check": "Rebuilt support separations become 1170/1150 mm; main 1900 mm. Main end projection 350 mm from bearer centre. All joist centres ≤400 mm.",
    "status": "Revised source-bounded layout",
    "detail": "BRANZ’s worked example accepts 140×45 SG8 wet-service joists over 2.1 m at 400 centres. New layout stays below that example; full applicable standard/connection checks still apply. Finished-envelope allowance gives nominal 4525/2510 mm members with the illustrated rims; verify actual bearing faces before cutting."
  },
  {
    "id": "cross-blocks",
    "title": "Fit the rebuilt-board supports",
    "picture": "blocking",
    "parts": "B01–B18 · selected structural block-end connections",
    "tools": "Tape · square · straightedge · clamps",
    "action": "Fit three flush blocks between J01/J02/J03/J04 at each of the six rows. Add 36 main lateral blocks at Y600/2000, then complete rims and board-butt support pairs.",
    "check": "Rebuilt:18×240 mm. Main:36 lateral blocks:6×240,4×290,26×335 mm (11.31 lm). Their rows are250 mm from the nearest bearer.",
    "status": "Wet-service hanger detail required",
    "detail": "Specify structural fixings for lateral blocks and candidate stainless45 mm joist hangers for rebuilt block ends, with wet-service fastening schedules. Do not apply Pryda’s published dry-timber capacity table unchanged to this exposed structure."
  },
  {
    "id": "tread-frame",
    "title": "Fit the tread frame on its foundations",
    "picture": "tread-box",
    "parts": "R1/R2 ·19 crosspieces +2 butt sisters ·6 shared pads",
    "tools": "Tape · square · clamps · specified connection tools",
    "action": "Assemble the 140×45 single-layer tread frame on its six shared ground supports. Seek SG8 H5 framing for this low, damp exposure; install reviewed separation and restraint.",
    "check": "6600×400 outer frame;21 short pieces ×310 mm nominal; rail bearings at X=250/1470/2690/3910/5130/6350. The rails do not load the main deck rim.",
    "status": "Specific proposal; hardware review",
    "detail": "H5 structural framing is listed on request by Timberlink NZ, not confirmed shelf stock. Pad reinforcement/bearing, restraint bracket, concrete anchors, timber fasteners and rail joints need a matching reviewed detail; no post-shoe substitution is specified."
  },
  {
    "id": "frame-check",
    "title": "Check the complete uncovered structure",
    "picture": "joists",
    "parts": "Main + rebuilt + tread frames · agreed connection schedules",
    "tools": "Level · tape · straightedge",
    "action": "Check both frames, the retained support, cross-blocks and all concealed structural connections before laying any boards.",
    "check": "Check 19 main joist lines +2 butt sisters, 18 rebuilt blocks, the intermediate bearer, retained-support condition, six main anchor assemblies and all tread bearing/restraint connections.",
    "status": "Owner check before covering",
    "detail": "Main load path: boards → joists/blocks → bearers → piles → soil. Tread: boards → box frame → its foundations → soil. No support from fascia, cladding or deck boards; no builder inspection visit is assumed."
  },
  {
    "id": "boards",
    "title": "Lay boards on all three areas",
    "picture": "boards",
    "parts": "32 mm pine · approximately80 mm wide · matched decking screws",
    "tools": "Driver · spacers · straightedge · saw",
    "action": "Run main boards in X and rebuilt boards in Y. Alternate main/tread board seams at X≈2375 and 3895 on the doubled supports, using the selected product’s butt gap and screw edge distances.",
    "check": "At provisional80 mm width /5 mm gaps:31 main +11 rebuilt +5 tread rows. Stock scenario:19×2.4,17×3.0,23×4.2,19×4.8 m =284.4 lm, including one spare rebuilt piece.",
    "status": "Needs DF01",
    "detail": "Exact width and product gap determine the quantities:88/90 mm boards use fewer rows. Base fixing positions1644;2000 is a provisional allowance. Confirm actual product, available lengths, screw embedment and minimum edge-strip width before ordering or ripping."
  },
  {
    "id": "final",
    "title": "Measure the complete finished route",
    "picture": "finish",
    "parts": "Deck → one tread → garden · agreed levels and fixing schedules",
    "tools": "Tape · level · straightedge",
    "action": "Check the finished assembly against the resolved plan, including actual rises, going, edges, board fixings and stable ground support.",
    "check": "One 6600×400 tread at the selected 250 mm level; main about 500 mm. Compare actual framing, fixings and levels with the reviewed plan.",
    "status": "Owner completion check",
    "detail": "Owner completion check. The retained 250 mm rises are an owner choice, not a declaration of access compliance."
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
    <tr><th>J01–J04 / J05–J19</th><td>Main joist lines</td><td>4 continuation candidates +15 main +2 butt sisters; finished envelopes 4570 / 2600 mm, not cuts</td></tr>
    <tr><th>RM1 / RM2</th><td>Front / rear rim lines</td><td>2 × 6600 mm overall allowance; rear split around J01–J04 to AP01, not two approved cuts</td></tr>
    <tr><th>L01–L36</th><td>Main lateral blocks</td><td>6×240 +4×290 +26×335 mm;11.31 lm nominal</td></tr>
    <tr><th>B01–B18</th><td>Rebuilt cross-blocks</td><td>18 ×240 mm /4.32 lm nominal</td></tr>
    <tr><th>R1/R2 · T01–T19</th><td>Tread rails / crosspieces</td><td>2 ×6600 rails +21 ×310 short pieces, nominal; SG8 H5 request</td></tr>
    <tr><th>GP01 · DPC · C1/C2/C3</th><td>Tread foundations / separation / restraint</td><td>6 shared-pad proposals, each bearing both rails; exact hardware review required</td></tr>
    <tr><th>TD1–TD5</th><td>Tread-board rows</td><td>5 illustrated at80 mm width /5 mm gap; confirm actual width/product</td></tr>
  </tbody></table></div></details>
  <div class="assembly-inputs"><strong>One build:</strong> selected 500/250 mm levels → main/rebuilt/tread foundations → all framing/concealed connections → boards. Specific dimensions below remain a proposal for the builder’s pre-build review; retained support and exact connections are not remotely verified. Plan details: FP01 foundations · AP01 main connections · GP01 tread · DF01 boards.</div>
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
