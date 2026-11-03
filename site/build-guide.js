const buildPhases = [
  {
    title: 'Confirm the design',
    steps: [
      'Give the builder the finished dimensions, levels and retained-support measurements/photos for a pre-build plan review.',
      'Agree J01–J03 continuity, the rebuilt cross-blocking and both decking directions.',
      'Agree the span, bracing, footing, connector and tread-frame schedules before work starts.',
      'Verify the one-tread access detail, then agree the dimensioned plan, fixing schedule and cut list.'
    ],
    gate: 'Do not buy structural quantities, cut framing or dig until the affected details are verified.'
  },
  {
    title: 'Set out',
    steps: [
      'Mark the 6600 × 2600 mm main deck; check both diagonals are about 7094 mm.',
      'Mark the 900 × 1970 mm rebuilt section and 6600 × 400 mm garden tread.',
      'Set the finished-deck datum. Calculate each pile top using actual timber sizes, DPC and local ground level.',
      'Mark supports from the agreed plan and set board rows and supported butt joints.'
    ],
    gate: '500 − 38 − 140 − 140 = 182 mm is nominal pile exposure before DPC, not a pile-cut schedule.'
  },
  {
    title: 'Install piles and footings',
    steps: [
      'Excavate to the verified footing schedule for each ordinary or bracing pile.',
      'Check pile treatment and structural suitability; position, plumb and brace the piles.',
      'Check support coordinates and pile tops before placing the specified concrete.',
      'Protect and cure the concrete for the required period before loading.'
    ],
    gate: 'Resolve any difference between actual bearing ground and the agreed footing assumptions before proceeding.'
  },
  {
    title: 'Fit bearers and bracing',
    steps: [
      'Fit the specified DPC and double-bearer members; join and fasten plies only as detailed.',
      'Install the scheduled ordinary-pile and anchor/bracing connections, using the exact components and fixings.',
      'Check bearer alignment, levels and the completed lateral-load system.'
    ],
    gate: 'Confirm the doubled-bearer connection detail; a generic bracket or “12 kN kit” label is insufficient.'
  },
  {
    title: 'Fit joists and blocking',
    steps: [
      'Set edge joists, then fit the remaining joists at the verified centres with specified bearing and fixings.',
      'Fit the agreed J01–J03 continuations and 12 flush cross-blocks in the rebuilt section; six support rows are proposed at 385 mm centres.',
      'Fit rims, blocking, butt-joint supports and required ties; count side edge joists once.',
      'Check the framing plane with a string and straightedge; preserve required member sizes and treatment when correcting it.'
    ],
    gate: 'Use the reviewed continuity, block-end fixing and cut details; the illustration is not a cut order.'
  },
  {
    title: 'Fix the decking',
    steps: [
      'Check actual board size, treatment and moisture: 38 mm pine is selected; 138 mm width remains provisional.',
      'Lay main-deck boards across the joists. Lay rebuilt boards along the 1970 mm depth, fixing into the cross-block support rows.',
      'Support every butt joint; pre-drill and keep fixing edge distances as specified.',
      'Use the selected gap and fixing schedule; the two-fastener examples do not specify screw size. Trim edges and treat cuts.'
    ],
    gate: 'Confirm actual stock lengths, supported joints, kerf, defects and waste before ordering or cutting.'
  },
  {
    title: 'Build the tread and finish',
    steps: [
      'Install the tread’s agreed supports at six stations, bearing beneath both rails; set the frame underside about 72 mm above the garden before actual DPC/level adjustments.',
      'Build one 140 mm-deep ladder frame: two 6600 mm rails and 16 nominal 310 mm crosspieces. Use the specified low-clearance treatment, grade and anchorage.',
      'Fix the 38 mm tread boards to the crosspieces; target the selected 250 mm surface level. Check rises, going and nosing against the reviewed access detail.',
      'Treat cuts, apply the chosen finish and check the completed fixings, levels and edges against the agreed plan.'
    ],
    gate: 'Resolve any difference between the built levels and verified access or structural details before use.'
  }
];

export function renderBuildGuide(container) {
  container.replaceChildren();
  for (const [index, phase] of buildPhases.entries()) {
    const details = document.createElement('details');
    details.className = 'build-phase';
    details.id = `build-phase-${index}`;
    details.open = true;
    details.innerHTML = `<summary><span class="phase-number">0${index}</span><span class="phase-copy"><h3>${phase.title}</h3></span><span class="phase-toggle" aria-hidden="true">+</span></summary><div class="phase-body"><ol>${phase.steps.map(step => `<li>${step}</li>`).join('')}</ol><p class="phase-gate"><strong>${index === 0 ? 'Before starting:' : 'Check:'}</strong> ${phase.gate}</p></div>`;
    container.append(details);
  }
}
