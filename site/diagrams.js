const NS = 'http://www.w3.org/2000/svg';
const C = {
  ink: '#243f36', muted: '#69796f', line: '#a2aea3', timber: '#dfc5a0',
  timberLine: '#c5a77f', green: '#547966', pale: '#e9eee7', amber: '#a86e36',
  amberFill: '#f2e5d2', paper: '#fafbf7', white: '#ffffff', outline: '#415f4b'
};
let sequence = 0;

export const JOIST_CENTRES = [22.5, 450, 877.5, ...Array.from({ length: 13 }, (_, i) => 877.5 + (5700 / 13) * (i + 1))];
export const BLOCK_CENTRES = [-1947.5, -1562.5, -1177.5, -792.5, -407.5, -22.5];
export const TREAD_SUPPORT_X = [250, 1470, 2690, 3910, 5130, 6350];

function el(name, attributes = {}, children = []) {
  const node = document.createElementNS(NS, name);
  for (const [key, value] of Object.entries(attributes)) {
    if (value !== undefined && value !== null) node.setAttribute(key, String(value));
  }
  for (const child of children) node.append(child);
  return node;
}
function text(parent, x, y, value, attributes = {}) {
  const node = el('text', {
    x, y, fill: C.ink, 'font-family': 'inherit', 'font-size': 16,
    ...attributes
  });
  node.textContent = value;
  parent.append(node);
  return node;
}
function line(parent, x1, y1, x2, y2, attributes = {}) {
  const node = el('line', { x1, y1, x2, y2, stroke: C.line, 'stroke-width': 1.2, ...attributes });
  parent.append(node);
  return node;
}
function dimH(parent, x1, x2, y, label) {
  line(parent, x1, y, x2, y);
  line(parent, x1, y - 5, x1, y + 5);
  line(parent, x2, y - 5, x2, y + 5);
  text(parent, (x1 + x2) / 2, y - 11, label, {
    'text-anchor': 'middle', 'font-size': 15, fill: C.muted,
    'paint-order': 'stroke', stroke: C.paper, 'stroke-width': 7, 'stroke-linejoin': 'round'
  });
}
function dimV(parent, x, y1, y2, label) {
  line(parent, x, y1, x, y2);
  line(parent, x - 5, y1, x + 5, y1);
  line(parent, x - 5, y2, x + 5, y2);
  text(parent, x + 20, (y1 + y2) / 2, label, {
    transform: `rotate(90 ${x + 20} ${(y1 + y2) / 2})`,
    'text-anchor': 'middle', 'font-size': 15, fill: C.muted,
    'paint-order': 'stroke', stroke: C.paper, 'stroke-width': 7, 'stroke-linejoin': 'round'
  });
}
function begin(svg, title, description, viewBox) {
  svg.replaceChildren();
  const uid = `deck-drawing-${++sequence}`;
  svg.setAttribute('viewBox', viewBox);
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-labelledby', `${uid}-title ${uid}-desc`);
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  const t = el('title', { id: `${uid}-title` }); t.textContent = title;
  const d = el('desc', { id: `${uid}-desc` }); d.textContent = description;
  svg.append(t, d);
  const style = el('style');
  style.textContent = '.deck-area{cursor:pointer;outline:none}.deck-area .area-outline{transition:stroke .15s,stroke-width .15s}.deck-area:hover .area-outline,.deck-area:focus-visible .area-outline,.deck-area.selected .area-outline{stroke:#2a6651;stroke-width:4}.deck-area.selected .main-joist{fill:#164c34;stroke:#164c34}.deck-area:focus-visible .main-joist,.deck-area.selected .main-joist{stroke:#133c27;stroke-width:1.8}.deck-label{pointer-events:none;user-select:none}';
  svg.append(style);
  return uid;
}
function interactive(svg, id, label, selected) {
  const group = el('g', {
    class: `deck-area${selected === id ? ' selected' : ''}`, role: 'button', tabindex: '0',
    'aria-label': label, 'aria-pressed': String(selected === id), 'data-plan-id': id, 'data-select': id
  });
  const choose = () => svg.dispatchEvent(new CustomEvent('plan-select', { detail: { id }, bubbles: true }));
  group.addEventListener('click', choose);
  group.addEventListener('keydown', event => {
    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); choose(); }
  });
  svg.append(group);
  return group;
}
function outline(selected, id, normal = C.outline) {
  return { class: 'area-outline', stroke: selected === id ? '#23694d' : normal, 'stroke-width': selected === id ? 4 : 1.8 };
}

function arrow(parent, x1, y1, x2, y2, color = C.green) {
  line(parent, x1, y1, x2, y2, { stroke: color, 'stroke-width': 2 });
  const angle = Math.atan2(y2 - y1, x2 - x1);
  for (const turn of [-.55, .55]) line(parent, x2, y2, x2 - 10 * Math.cos(angle + turn), y2 - 10 * Math.sin(angle + turn), { stroke: color, 'stroke-width': 2 });
}

// Flush cross-supports for the assumed 90-degree rebuilt-board direction.
function drawRebuiltBlocks(parent, x0, y0, scale) {
  let index = 0;
  for (const y of BLOCK_CENTRES) {
    for (const left of [45, 472.5]) {
      parent.append(el('rect', {
        class: 'rebuilt-block area-outline', 'data-block-id': `B${String(++index).padStart(2, '0')}`,
        'data-y-mm': y, 'data-clear-mm': 382.5,
        x: x0 + left * scale, y: y0 + (y - 22.5) * scale,
        width: 382.5 * scale, height: 45 * scale,
        fill: '#a7c6d0', stroke: '#436b7a', 'stroke-width': 1.1
      }));
    }
  }
}

// Single-layer ladder: symbols indicate bearing POINTS, not footing dimensions.
function drawTreadFrame(parent, x0, y0, scale) {
  const marker = Math.max(9, 70 * scale);
  for (const x of TREAD_SUPPORT_X) {
    for (const [side, y] of [['rear', 22.5], ['front', 377.5]]) {
      parent.append(el('rect', {
        class: 'tread-bearing', 'data-x-mm': x, 'data-side': side, 'data-symbolic': 'true',
        x: x0 + x * scale - marker / 2, y: y0 + y * scale - marker / 2,
        width: marker, height: marker, fill: '#fff', stroke: '#8d6637',
        'stroke-width': 1.6, 'stroke-dasharray': '3 2'
      }));
    }
  }
  for (const [side, y] of [['rear', 0], ['front', 355]]) {
    parent.append(el('rect', {
      class: 'tread-rail area-outline', 'data-side': side,
      x: x0, y: y0 + y * scale, width: 6600 * scale, height: 45 * scale,
      fill: '#efd3a9', stroke: '#8d6637', 'stroke-width': 1.2
    }));
  }
  for (const [i, x] of JOIST_CENTRES.entries()) {
    parent.append(el('rect', {
      class: 'tread-crosspiece', 'data-member-id': `T${String(i + 1).padStart(2, '0')}`,
      'data-x-mm': x, 'data-clear-mm': 310,
      x: x0 + (x - 22.5) * scale, y: y0 + 45 * scale,
      width: 45 * scale, height: 310 * scale,
      fill: '#788f69', stroke: '#436044', 'stroke-width': .8
    }));
  }
}

/** Proportional concept plan. Member positions and continuity are provisional. */
export function renderPlan(svg, { view = 'layout', selected = null } = {}) {
  const framing = view === 'framing';
  const uid = begin(svg, framing ? 'Joist and bearer layout — provisional' : 'Deck layout and dimensions',
    'Main deck 6600 by 2600 millimetres. Rebuilt section 900 by 1970 millimetres behind the left end. One full-width tread projects 400 millimetres. Framing view shows sixteen 45 millimetre-wide joists J01 to J16, three dashed continuation candidates in the rebuilt section, twelve flush cross-blocks for the assumed rotated decking, two double bearer lines and twelve proposed piles. The independent single-layer tread ladder and its twelve bearing-point symbols are a proposal, not an approved footing or fixing detail.',
    '0 0 1180 870');
  svg.setAttribute('role', 'group');
  const defs = el('defs');
  const boards = el('pattern', { id: `${uid}-boards`, width: 20, height: 18.8, patternUnits: 'userSpaceOnUse' });
  boards.append(el('rect', { width: 20, height: 18.8, fill: C.timber }));
  boards.append(el('line', { x1: 0, y1: 18.1, x2: 20, y2: 18.1, stroke: C.timberLine, 'stroke-width': .65, opacity: .7 }));
  defs.append(boards);
  const rotatedBoards = el('pattern', { id: `${uid}-boards-rotated`, width: 18.8, height: 20, patternUnits: 'userSpaceOnUse' });
  rotatedBoards.append(el('rect', { width: 18.8, height: 20, fill: C.timber }));
  rotatedBoards.append(el('line', { x1: 18.1, y1: 0, x2: 18.1, y2: 20, stroke: C.timberLine, 'stroke-width': .65, opacity: .7 }));
  defs.append(rotatedBoards);
  svg.append(defs, el('rect', { width: 1180, height: 870, fill: C.paper }));

  const S = .13, X = 130, Y = 346.1, W = 6600 * S, H = 2600 * S, RW = 900 * S, RH = 1970 * S;
  const TX = X, TY = Y + H, TW = W, TH = 400 * S;
  const main = interactive(svg, 'main', 'Main deck: 6600 by 2600 millimetres, 17.16 square metres', selected);
  main.append(el('rect', { x: X, y: Y, width: W, height: H, fill: framing ? '#ffffff' : `url(#${uid}-boards)`, ...outline(selected, 'main') }));
  const rebuilt = interactive(svg, 'rebuilt', 'Rebuilt section: 900 by 1970 millimetres; retained bearer at back edge', selected);
  rebuilt.append(el('rect', { x: X, y: Y - RH, width: RW, height: RH, fill: framing ? '#f3f7f0' : `url(#${uid}-boards-rotated)`, ...outline(selected, 'rebuilt') }));
  const extension = interactive(svg, 'extension', 'House extension: 5700 millimetre frontage; rear extent not surveyed', selected);
  extension.append(el('rect', { x: X + RW, y: Y - RH, width: W - RW, height: RH, fill: '#e6ece4', ...outline(selected, 'extension', '#99a99a') }));
  line(extension, X + RW + 2, Y - RH, X + W - 2, Y - RH, { stroke: C.paper, 'stroke-width': 5 });
  line(extension, X + RW, Y - RH, X + W, Y - RH, { stroke: '#99a99a', 'stroke-dasharray': '8 6', 'stroke-width': 1.7 });
  const tread = interactive(svg, 'tread', 'One full-width tread: 6600 by 400 millimetres, selected surface 250 millimetres above garden; independent single-layer ladder frame proposed', selected);
  tread.append(el('rect', { x: TX, y: TY, width: TW, height: TH, rx: 1, fill: framing ? '#f1eee5' : `url(#${uid}-boards)`, ...outline(selected, 'tread', C.outline) }));

  if (framing) {
    // Bearers and piles sit beneath the joists; all are visible independently.
    const bearer = interactive(svg, 'bearer', 'Two provisional double 140 by 45 bearer lines at Y350 and Y2250, with twelve proposed piles', selected);
    for (const position of [350, 2250]) {
      const py = Y + position * S;
      bearer.append(el('rect', { class: 'new-bearer area-outline', 'data-y-mm': position, x: X, y: py - 45 * S, width: W, height: 90 * S, fill: '#f4d6a6', stroke: C.amber, 'stroke-width': 1.8 }));
      // Split the double bearer into its two 45 mm plies in the plan.
      line(bearer, X, py, X + W, py, { stroke: '#b17c3d', 'stroke-width': .8 });
      for (const pile of [250, 1470, 2690, 3910, 5130, 6350]) {
        bearer.append(el('rect', { class: 'pile', 'data-x-mm': pile, 'data-y-mm': position, x: X + pile * S - 8.125, y: py - 8.125, width: 16.25, height: 16.25, fill: '#fffefa', stroke: C.amber, 'stroke-width': 2 }));
      }
    }
    // Align J01–J03 with the 900 mm-wide rebuilt strip. This is a layout option,
    // not a verified span, bearing, continuity or cutting detail.
    const centres = JOIST_CENTRES;
    const joists = interactive(svg, 'joists', 'Sixteen provisional 140 by 45 joists J01 to J16; centres 427.5 millimetres twice then approximately 438.46 millimetres thirteen times. J01 to J03 have dashed rebuilt-section continuation candidates.', selected);
    for (const [i, centre] of centres.entries()) {
      const px = X + (centre - 22.5) * S;
      const id = `J${String(i + 1).padStart(2, '0')}`;
      if (i < 3) {
        joists.append(el('rect', { class: 'rebuilt-joist-extension', 'data-member-id': id, 'data-x-mm': centre, x: px, y: Y - RH, width: 45 * S, height: RH, fill: '#edf5e7', stroke: '#426b49', 'stroke-width': 1.4, 'stroke-dasharray': '6 4' }));
      }
      joists.append(el('rect', { class: 'main-joist', 'data-member-id': id, 'data-x-mm': centre, x: px, y: Y, width: 45 * S, height: H, fill: selected === 'joists' ? '#164c34' : '#456b4c', stroke: '#234c32', 'stroke-width': .7 }));
      text(svg, X + centre * S, Y + 23, id, {
        class: 'deck-label joist-id', 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 650,
        fill: '#203d2b', 'paint-order': 'stroke', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linejoin': 'round'
      });
    }
    const blocking = interactive(svg, 'blocking', 'Twelve flush cross-blocks between J01 to J03, at six support rows 385 millimetres apart, for the assumed rotated rebuilt decking; block-end fixing detail is provisional', selected);
    drawRebuiltBlocks(blocking, X, Y, S);
    drawTreadFrame(tread, TX, TY, S);
    text(svg, X + W + 11, Y + 350 * S + 5, 'A', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X + W + 11, Y + 2250 * S + 5, 'B', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X, 818, 'J01–J16: 45 mm wide · first 2 bays 427.5 mm · remaining 13 bays ≈438.46 mm', { 'font-size': 16, fill: C.ink });
    text(svg, X, 845, 'Dashed J01–J03: continuation option. Blue: flush blocks. Tread: independent ladder proposal.', { 'font-size': 15, fill: C.muted });
  } else {
    text(svg, X + W / 2, Y + H / 2 - 5, 'MAIN DECK', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 31, 'font-weight': 550, 'letter-spacing': 2.5 });
    text(svg, X + W / 2, Y + H / 2 + 29, '6.60 × 2.60 m  /  17.16 m²', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 19, fill: '#5f664e' });
    text(svg, X, 825, 'Confirmed footprint. Structural details remain provisional.', { 'font-size': 16, fill: C.muted });
  }

  const labels = el('g', { class: 'deck-label', 'pointer-events': 'none' }); svg.append(labels);
  if (!framing) {
    text(labels, X + RW / 2, Y - RH / 2 - 18, 'REBUILT', { 'text-anchor': 'middle', 'font-size': 16, 'font-weight': 650 });
    text(labels, X + RW / 2, Y - RH / 2 + 7, '0.90 × 1.97 m', { 'text-anchor': 'middle', 'font-size': 13 });
    text(labels, X + RW / 2, Y - RH / 2 + 30, 'BOARDS IN Y', { 'text-anchor': 'middle', 'font-size': 12, fill: '#5f664e' });
    arrow(labels, X + RW / 2, Y - RH / 2 + 44, X + RW / 2, Y - RH / 2 + 83);
  } else {
    text(labels, X + RW / 2, Y - RH + 32, 'REBUILT', { 'text-anchor': 'middle', 'font-size': 13, 'font-weight': 650, 'paint-order': 'stroke', stroke: '#f3f7f0', 'stroke-width': 4 });
  }
  text(labels, X + RW + (W - RW) / 2, Y - RH / 2 - 12, 'HOUSE EXTENSION', { 'text-anchor': 'middle', 'font-size': 25, 'font-weight': 450, 'letter-spacing': 2 });
  text(labels, X + RW + (W - RW) / 2, Y - RH / 2 + 20, '5700 mm frontage · rear extent not surveyed', { 'text-anchor': 'middle', 'font-size': 17, fill: C.muted });
  text(labels, TX + TW / 2, TY + TH / 2 + 6, framing ? 'TREAD LADDER · PROPOSED' : 'ONE TREAD · 6600 × 400 mm', { 'text-anchor': 'middle', 'font-size': 17, 'font-weight': 600, 'letter-spacing': .6 });
  text(labels, X + W / 2, 781, 'GARDEN', { 'text-anchor': 'middle', 'font-size': 17, 'letter-spacing': 3, fill: C.green });
  const retained = interactive(svg, 'rebuilt', 'Retained bearer at rebuilt-section back edge, approximately Y minus 1970 millimetres; exact offset and capacity unverified', selected);
  retained.append(el('rect', { x: X + 2, y: Y - RH - 4, width: RW - 4, height: 8, fill: C.green, stroke: C.green, 'stroke-width': 1.5 }));
  text(svg, X + RW + 17, Y - RH - 11, 'Retained bearer · exact offset to verify', { 'font-size': 13, fill: C.green });
  dimH(svg, X, X + W, 43, '6600 mm main frontage');
  dimH(svg, X, X + RW, Y - 20, '900');
  dimH(svg, X + RW + 8, X + W, Y - 20, '5700 mm extension frontage');
  dimV(svg, 83, Y - RH, Y, '1970 mm');
  dimV(svg, X + W + 54, Y, Y + H, '2600 mm');
  dimV(svg, TX + TW + 30, TY, TY + TH, '400 mm');
}

/** One full-width tread between the deck and garden, at the selected halfway level. */
export function renderElevation(svg) {
  begin(svg, 'Deck to one tread to garden',
    'Side section showing deck, one full-width 6600 by 400 millimetre tread, then garden. Measured total drop is about 500 millimetres. The user selects the tread surface halfway down, about 250 millimetres above the garden. That creates two approximately 250 millimetre rises. Pine decking thickness is 38 millimetres; board width remains provisional. The selected levels and allowable rises require verification; this is not an approved stair detail.',
    '0 0 1080 430');
  svg.append(el('rect', { width: 1080, height: 430, fill: C.paper }));
  const deckEnd = 470, deckTop = 131, groundY = 331, treadEnd = 630, treadTop = 231;
  // The horizontal and vertical section geometry uses the same 0.4px/mm scale.
  svg.append(el('path', {
    d: `M 100 ${deckTop} H ${deckEnd} V ${treadTop} H ${treadEnd} V ${groundY} H 932 V 361 H 100 Z`,
    fill: '#e8eee4', stroke: 'none'
  }));
  svg.append(el('rect', { x: 100, y: deckTop, width: deckEnd - 100, height: 15.2, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
  svg.append(el('rect', { x: deckEnd, y: treadTop, width: treadEnd - deckEnd, height: 15.2, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
  line(svg, 100, deckTop, deckEnd, deckTop, { stroke: C.ink, 'stroke-width': 3 });
  line(svg, deckEnd, deckTop, deckEnd, treadTop, { stroke: C.amber, 'stroke-width': 2, 'stroke-dasharray': '5 4' });
  line(svg, deckEnd, treadTop, treadEnd, treadTop, { stroke: C.ink, 'stroke-width': 3 });
  line(svg, treadEnd, treadTop, treadEnd, groundY, { stroke: C.amber, 'stroke-width': 2, 'stroke-dasharray': '5 4' });
  line(svg, treadEnd, groundY, 932, groundY, { stroke: C.green, 'stroke-width': 3 });
  text(svg, 278, 103, 'DECK', { 'text-anchor': 'middle', 'font-size': 22, 'letter-spacing': 2, 'font-weight': 500 });
  text(svg, 551, 279, 'ONE TREAD', { 'text-anchor': 'middle', 'font-size': 18, 'letter-spacing': 1, 'font-weight': 600 });
  text(svg, 792, 306, 'GARDEN', { 'text-anchor': 'middle', 'font-size': 20, 'letter-spacing': 2, fill: C.green });
  dimH(svg, deckEnd, treadEnd, 194, '400 mm total');
  dimV(svg, 970, deckTop, groundY, '≈500 mm measured drop');
  text(svg, 437, 183, '≈250 mm', { 'text-anchor': 'end', 'font-size': 14, fill: C.amber });
  text(svg, 662, 286, '≈250 mm', { 'font-size': 14, fill: C.amber });
  text(svg, 100, 399, 'Selected levels · independent single-layer tread frame proposed. See Tread frame view.', { 'font-size': 15, fill: C.muted });
}


/** Independent 6600 x 400 tread ladder, including the constrained height stack. */
export function renderTreadFrame(svg) {
  begin(svg, 'Proposed independent tread ladder frame',
    'One full-width 6600 by 400 millimetre tread. Two long 140 by 45 rails and sixteen 310 millimetre nominal crosspieces form one layer beneath 38 millimetre decking. Surface is selected at 250 millimetres above garden, frame top is 212 and underside 72. Twelve rail bearing points at six stations are symbols, not specified footings. Grade and treatment for low clearance, supports, anchorage, joints, spans and access geometry need the pre-build plan check.',
    '0 0 1180 800');
  svg.append(el('rect', { width: 1180, height: 800, fill: C.paper }));
  text(svg, 90, 35, 'TREAD FRAME — PROPOSAL', { 'font-size': 21, 'font-weight': 650 });
  const X = 100, Y = 100, S = .14;
  drawTreadFrame(svg, X, Y, S);
  dimH(svg, X, X + 6600 * S, 72, '6600 mm outer frame');
  dimV(svg, X + 6600 * S + 38, Y, Y + 400 * S, '400 mm');
  text(svg, 100, 195, '2 long rails + 16 crosspieces (including end pieces). Crosspiece clear space: 310 mm.', { 'font-size': 16 });
  text(svg, 100, 222, 'Dashed bearing symbols: 6 stations × 2 rail bearings. Footing and anchorage design not specified.', { 'font-size': 15, fill: C.muted });
  text(svg, 100, 276, 'SIDE SECTION THROUGH THE 400 mm DEPTH', { 'font-size': 16, 'font-weight': 650 });

  const left = 130, ground = 620, top = ground - 250, frameTop = ground - 212, frameBottom = ground - 72;
  // Three decking rows shown in section; 5 mm gaps are illustrative, not selected.
  for (const [x, width] of [[0, 126], [131, 138], [274, 126]]) {
    svg.append(el('rect', { class: 'tread-section-decking', x: left + x, y: top, width, height: 38, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
  }
  svg.append(el('rect', { class: 'tread-section-crosspiece', x: left + 45, y: frameTop, width: 310, height: 140, fill: '#dfe8d8', stroke: '#4e6947', 'stroke-width': 1.5 }));
  for (const x of [left, left + 355]) {
    svg.append(el('rect', { class: 'tread-section-rail', x, y: frameTop, width: 45, height: 140, fill: '#efd3a9', stroke: '#8d6637', 'stroke-width': 1.5 }));
    svg.append(el('rect', { class: 'tread-support-symbol', x: x - 4, y: frameBottom, width: 53, height: ground - frameBottom, fill: '#eef0ec', stroke: '#7d877b', 'stroke-width': 1.3, 'stroke-dasharray': '5 3' }));
  }
  line(svg, 90, ground, 654, ground, { stroke: C.green, 'stroke-width': 2 });
  text(svg, 90, ground + 25, 'GARDEN DATUM', { 'font-size': 13, fill: C.muted });
  dimH(svg, left, left + 400, 340, '400 mm total projection');
  dimH(svg, left + 45, left + 355, frameBottom - 18, '310 clear');
  dimV(svg, left + 445, top, ground, '250 surface height');
  text(svg, 690, top + 10, '38 mm decking', { 'font-size': 18, 'font-weight': 600 });
  text(svg, 690, frameTop + 25, 'Frame top: 212 mm', { 'font-size': 17 });
  text(svg, 690, frameTop + 55, '140 mm-deep members, one layer', { 'font-size': 16 });
  text(svg, 690, frameBottom + 7, 'Frame underside: 72 mm', { 'font-size': 17 });
  text(svg, 690, frameBottom + 38, 'Low-clearance timber grade/treatment', { 'font-size': 15, fill: C.amber });
  text(svg, 690, frameBottom + 61, 'and support details: to confirm.', { 'font-size': 15, fill: C.amber });
  text(svg, 100, 700, 'No stacked bearer layer. Frame uses independent ground supports.', { 'font-size': 16 });
  text(svg, 100, 727, 'Rail support stations X: 250 / 1470 / 2690 / 3910 / 5130 / 6350 mm — provisional.', { 'font-size': 15, fill: C.muted });
  text(svg, 100, 754, 'Nominal geometry only; rail joints, bearing, foundations and fixings need a pre-build plan detail.', { 'font-size': 15, fill: C.muted });
}

/** Rotated rebuilt boards fixed to flush cross-supports, not parallel joists. */
export function renderDeckingDetail(svg) {
  begin(svg, 'Rebuilt-section decking support and fixing proposal',
    'Assumed rebuilt decking runs along the 1970 millimetre depth, at ninety degrees to the main boards. J01, J02 and J03 are proposed continuations. Twelve flush cross-blocks between these joists make six support rows at 385 millimetre centres. Seven board strips illustrate a 138 millimetre width and five millimetre gaps, not an actual product selection. Two fixing-location examples are shown per board at each support row. Exact screws, block-end fixings and edge distances require a pre-build specification.',
    '0 0 1180 800');
  svg.append(el('rect', { width: 1180, height: 800, fill: C.paper }));
  text(svg, 80, 36, 'REBUILT DECKING — ROTATED DIRECTION ASSUMED', { 'font-size': 21, 'font-weight': 650 });
  const X = 110, top = 125, S = .25, Y = top + 1970 * S;
  // Underlying members remain visible through the illustrative decking strips.
  for (const [i, x] of JOIST_CENTRES.slice(0, 3).entries()) {
    svg.append(el('rect', { class: 'detail-long-joist', 'data-member-id': `J0${i + 1}`, x: X + (x - 22.5) * S, y: top, width: 45 * S, height: 1970 * S, fill: '#426b49', stroke: '#21472c', 'stroke-width': 1 }));
    text(svg, X + x * S, Y + 30, `J0${i + 1}`, { 'text-anchor': 'middle', 'font-size': 14, 'font-weight': 650 });
  }
  drawRebuiltBlocks(svg, X, Y, S);
  // A 5 mm example gap gives two 90 mm edges and five 138 mm interior boards.
  const boardWidths = [90, 138, 138, 138, 138, 138, 90];
  let cursor = 0;
  for (const [i, width] of boardWidths.entries()) {
    svg.append(el('rect', { class: 'rebuilt-deck-board', 'data-board-id': i + 1, 'data-direction': 'Y', x: X + cursor * S, y: top, width: width * S, height: 1970 * S, fill: '#dfc5a0', 'fill-opacity': .58, stroke: '#b59060', 'stroke-width': .6 }));
    for (const row of BLOCK_CENTRES) {
      for (const fraction of [.25, .75]) {
        svg.append(el('circle', { class: 'decking-fixing-example', 'data-board-id': i + 1, 'data-support-y-mm': row, cx: X + (cursor + width * fraction) * S, cy: Y + row * S, r: 2.2, fill: '#85432e', stroke: '#fff', 'stroke-width': .5 }));
      }
    }
    cursor += width + 5;
  }
  dimH(svg, X, X + 900 * S, 95, '900 mm');
  dimV(svg, 72, top, Y, '1970 mm');
  arrow(svg, X + 900 * S + 39, top + 85, X + 900 * S + 39, Y - 85);
  text(svg, X + 900 * S + 75, Y + 27, 'Boards run Y', { 'text-anchor': 'start', 'font-size': 13, fill: C.green });

  const textX = 460;
  text(svg, textX, 140, 'J01–J03: proposed full-length continuations', { 'font-size': 19, 'font-weight': 600 });
  text(svg, textX, 171, 'They run parallel to these boards.', { 'font-size': 16, fill: C.muted });
  svg.append(el('rect', { x: textX, y: 210, width: 28, height: 12, fill: '#a7c6d0', stroke: '#436b7a' }));
  text(svg, textX + 42, 222, '12 flush cross-blocks in 6 rows', { 'font-size': 18, 'font-weight': 600 });
  text(svg, textX, 253, 'Two blocks per row, 382.5 mm nominal clear length.', { 'font-size': 16 });
  text(svg, textX, 283, 'Rows: 385 mm centres. Tops flush with joists.', { 'font-size': 16 });
  text(svg, textX, 313, 'No extra batten layer or extra finished height.', { 'font-size': 16, fill: C.muted });
  svg.append(el('circle', { cx: textX + 7, cy: 364, r: 4, fill: '#85432e' }));
  text(svg, textX + 27, 370, 'Fix boards down into cross-support rows.', { 'font-size': 18, 'font-weight': 600 });
  text(svg, textX, 403, 'Two fixing locations per board at each row are shown.', { 'font-size': 16 });
  text(svg, textX, 433, 'Exact 38 mm-board screws and edge/end distances: TBD.', { 'font-size': 16, fill: C.muted });
  text(svg, textX, 487, 'Before building: agree block-end connections,', { 'font-size': 16, fill: C.amber });
  text(svg, textX, 513, 'joist continuity, bearing and supported board joints.', { 'font-size': 16, fill: C.amber });
  text(svg, 110, 712, 'Board strips and dots are fixing examples, not a final board order or screw schedule.', { 'font-size': 16, fill: C.muted });
  text(svg, 110, 741, 'Direction is illustrated from the latest description; 138 mm width and 5 mm gaps are assumptions.', { 'font-size': 15, fill: C.muted });
}
