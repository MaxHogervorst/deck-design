const buildPhases = [
  {
    title: 'Settle the design before buying or digging',
    context: 'Bring the plan and its open details to the builder first.',
    steps: [
      'Record finished deck levels at the door and corners, garden levels, cladding and flashing clearances, drainage routes and nearby house footings.',
      'Inspect the retained bearer and its piles, connections, condition and support spacing. Record exact bearing faces and centre lines; the rebuilt section is 900 × 1970 mm.',
      'Locate buried services and establish suitable bearing ground. Resolve uncertain fill, wet ground or foundation conflicts before excavation.',
      'Have the applicable spans, cantilevers, bracing, pile classes, footings and exact pile-to-double-bearer-to-joist connections checked. Resolve the rebuilt-section junction and shared loading.',
      'Agree the one full-width 6600 × 400 mm tread and verify the selected 250 mm surface level, access geometry and supports. Freeze the dimensioned plan, fixing schedule and cut list.'
    ],
    gate: 'Do not order structural quantities, cut members or dig holes until the affected design details are verified. The current 12-pile layout and framing remain provisional.'
  },
  {
    title: 'Set out the footprint and finished levels',
    context: 'Make the reference lines accurate before locating individual supports.',
    steps: [
      'Set out the 6600 × 2600 mm main rectangle. Check both diagonals against approximately 7094 mm and confirm the rectangle is square.',
      'Mark the 900 × 1970 mm rebuilt section behind the extension’s front face and the full-width 400 mm tread projection along the garden edge.',
      'Transfer a consistent finished-deck datum with a laser or level. Use actual delivered decking, joist, bearer and DPC thicknesses to calculate pile tops at each ground level.',
      'Mark pile and framing locations from the verified plan and check them against services and foundations. The illustrated bearer positions are not a final excavation layout.',
      'Plan the actual board-width and gap module, supported butt joints and edge strips before fixing the framing layout.'
    ],
    gate: 'The nominal stack is 500 − 38 − 140 − 140 = 182 mm before DPC. It is an arithmetic starting point, not a universal pile-cut height.'
  },
  {
    title: 'Excavate and concrete the specified footings',
    context: 'Follow the verified footing schedule for each pile type.',
    steps: [
      'Excavate only the specified hole shape, width and depth, with the required bearing ground and clearances. Keep ordinary and bracing-pile details distinct.',
      'Check the supplied piles have the specified treatment and structural suitability, including any anchor-pile requirements.',
      'Position, plumb and temporarily brace the piles. Check support coordinates and tops against the datum before placing concrete.',
      'Place the specified concrete and protect and cure it as required. Recheck pile position and plumb, and allow the required curing before loading.'
    ],
    gate: 'Stop if the excavation exposes unsuitable ground, services or a house-footing conflict. No hole dimensions or concrete order are approved by this website.'
  },
  {
    title: 'Install bearers and the lateral-load system',
    context: 'Establish a straight, braced support platform.',
    steps: [
      'Fit the specified DPC or separation detail at pile tops, allowing for its thickness in the finished level.',
      'Install the specified double-bearer members. Locate ply joins only where the verified detail permits and fix the plies together as scheduled.',
      'Fit the exact ordinary-pile and bracing/anchor connections, including the specified components, fixings, corrosion class and edge distances.',
      'Check bearer straightness and top levels with a string or laser. Confirm the complete bracing system and all support connections before proceeding.'
    ],
    gate: 'A generic bracket or “12 kN kit” label does not settle the doubled-bearer connection. Use the actual verified assembly and installation detail.'
  },
  {
    title: 'Fit joists, rims, blocking and the rebuilt junction',
    context: 'Resolve the junction once, then keep every board support in the same plane.',
    steps: [
      'Set first and last joists from the verified framing envelope, then install the remaining joists at the specified centres and with the required bearing and fixings.',
      'Build the agreed junction between the rebuilt section and main deck. Joists reaching the proposed rear bearer cross into the main footprint; do not overlap separate members in the same space.',
      'Install rims, blocking, board-butt supports and any ties required for the lateral-load system. Do not count side edge joists twice.',
      'Check the framing plane with a long straightedge and string. Correct discrepancies only in a way that preserves the required member size, grade, treatment and connections.'
    ],
    gate: 'The 16 main-only joist lines and continuous-joist option are layout scenarios. Use the verified junction, support and cut details rather than cutting from those counts alone.'
  },
  {
    title: 'Lay and fix the pine decking',
    context: 'Use the actual product and moisture guidance, not a universal gap.',
    steps: [
      'Measure the supplied boards and check their condition, treatment and moisture. The selected thickness is 38 mm; 138 mm width remains provisional until the product is confirmed.',
      'Dry-plan the rows, gaps and edge strips using the supplier’s installation guidance. Align the main and rebuilt areas without obstructing cladding, vents or drainage.',
      'Arrange lengths so every butt joint has the specified support and fixing space. Pre-drill ends where required and keep the required fixing edge distances.',
      'Use the specified exterior fixings for the timber treatment and corrosion environment. Trim edges uniformly and treat cut ends as required by the product instructions.'
    ],
    gate: 'Board-row estimates are not a purchase or cutting schedule. Confirm stock lengths, supported joints, kerf, defects and waste before ordering or cutting.'
  },
  {
    title: 'Build the one tread and complete the deck',
    context: 'Keep the agreed route: deck → one full-width tread → garden.',
    steps: [
      'Build the verified tread structure and foundations for the 6600 × 400 mm full-width layout. The selected surface is 250 mm above garden beneath the deck at about 500 mm.',
      'Check final rises, going and nosing, landing/approach, slip resistance and any required handrail details against the agreed access design. The selected halfway level is not proof of compliance.',
      'Treat exposed cuts and apply the chosen finish in accordance with the timber and finish manufacturers’ instructions.',
      'Inspect connections and visible fixings, deck flatness, edges and trip hazards. Confirm clear drainage and ventilation and that the deck remains structurally independent of the house.'
    ],
    gate: 'Complete the access and structural checks before using the finished deck. Resolve any difference between the built levels and the verified details.'
  }
];

export function renderBuildGuide(container) {
  container.replaceChildren();
  for (const [index, phase] of buildPhases.entries()) {
    const details = document.createElement('details');
    details.className = 'build-phase';
    details.id = `build-phase-${index}`;
    details.open = index === 0;
    details.innerHTML = `<summary><span class="phase-number">0${index}</span><span class="phase-copy"><h3>${phase.title}</h3><span>${phase.context}</span></span><span class="phase-toggle" aria-hidden="true">+</span></summary><div class="phase-body"><ol>${phase.steps.map(step => `<li>${step}</li>`).join('')}</ol><p class="phase-gate"><strong>${index === 0 ? 'Before starting:' : 'Before continuing:'}</strong> ${phase.gate}</p></div>`;
    container.append(details);
  }
}
