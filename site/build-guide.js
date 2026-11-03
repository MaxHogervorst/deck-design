const buildPhases = [
  {
    title: 'Confirm the design',
    steps: [
      'Measure door, deck and garden levels; mark cladding, drainage, vents, services and house footings.',
      'Inspect the retained bearer, piles and fixings. Record timber sizes, condition, bearing faces and support spacing.',
      'Resolve spans, bracing, footings, connectors and the rebuilt-section junction with the builder and any required specialist.',
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
      'Mark supports from the verified plan; check services, foundations, board rows and butt-joint positions.'
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
    gate: 'Stop if ground, services or nearby foundations differ from the verified footing assumptions.'
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
      'Build the agreed rebuilt-section junction; do not overlap separate joists in the same space.',
      'Fit rims, blocking, butt-joint supports and required ties; count side edge joists once.',
      'Check the framing plane with a string and straightedge; preserve required member sizes and treatment when correcting it.'
    ],
    gate: 'The illustrated 16-line grid and three rebuilt-section continuations are provisional, not approved cuts or connections.'
  },
  {
    title: 'Fix the decking',
    steps: [
      'Check actual board size, treatment and moisture: 38 mm pine is selected; 138 mm width remains provisional.',
      'Set board gaps and edge strips from the supplier’s instructions; keep cladding, vents and drainage clear.',
      'Support every butt joint; pre-drill and keep fixing edge distances as specified.',
      'Use the specified exterior fixings, trim edges and treat cut ends.'
    ],
    gate: 'Confirm actual stock lengths, supported joints, kerf, defects and waste before ordering or cutting.'
  },
  {
    title: 'Build the tread and finish',
    steps: [
      'Build the verified supports for one full-width 6600 × 400 mm tread, with the selected surface 250 mm above garden.',
      'Check final rises, going/nosing, approach, slip resistance and any required handrails against the verified access detail.',
      'Treat exposed cuts and apply the selected finish to the product instructions.',
      'Check fixings, flatness, edges, drainage and ventilation; confirm structural independence from the house.'
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
