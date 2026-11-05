const NS = 'http://www.w3.org/2000/svg';
const C = {
  ink: '#243f36', muted: '#69796f', line: '#a2aea3', timber: '#dfc5a0',
  timberLine: '#c5a77f', green: '#547966', pale: '#e9eee7', amber: '#a86e36',
  amberFill: '#f2e5d2', paper: '#fafbf7', white: '#ffffff', outline: '#415f4b'
};
let sequence = 0;

export const JOIST_CENTRES = [22.5, 307.5, 592.5, 877.5, ...Array.from({ length: 15 }, (_, i) => 877.5 + 380 * (i + 1))];
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
    for (const left of [45, 330, 615]) {
      parent.append(el('rect', {
        class: 'rebuilt-block area-outline', 'data-block-id': `B${String(++index).padStart(2, '0')}`,
        'data-y-mm': y, 'data-clear-mm': 240,
        x: x0 + left * scale, y: y0 + (y - 22.5) * scale,
        width: 240 * scale, height: 45 * scale,
        fill: '#a7c6d0', stroke: '#436b7a', 'stroke-width': 1.1
      }));
    }
  }
}

// Single-layer ladder: symbols indicate bearing POINTS, not footing dimensions.
function drawTreadFrame(parent, x0, y0, scale) {
  // Six shared pad proposals support both rails. Symbols are not excavation drawings.
  for (const x of TREAD_SUPPORT_X) parent.append(el('rect', { class: 'tread-pad', 'data-x-mm': x,
    x: x0 + (x - 150) * scale, y: y0 - 50 * scale, width: 300 * scale, height: 500 * scale,
    fill: '#e6e8e1', stroke: '#8d6637', 'stroke-width': 1, 'stroke-dasharray': '4 3' }));
  for (const y of [22.5, 377.5]) {
    parent.append(el('rect', { class: 'tread-bearing-zone', 'data-symbolic': 'true',
      x: x0, y: y0 + y * scale - 5, width: 6600 * scale, height: 10,
      fill: 'none', stroke: '#8d6637', 'stroke-width': 1.4, 'stroke-dasharray': '5 4' }));
  }
  for (const [side, y] of [['rear', 0], ['front', 355]]) {
    parent.append(el('rect', {
      class: 'tread-rail area-outline', 'data-side': side,
      x: x0, y: y0 + y * scale, width: 6600 * scale, height: 45 * scale,
      fill: '#efd3a9', stroke: '#8d6637', 'stroke-width': 1.2
    }));
  }
  for (const [i, x] of [...JOIST_CENTRES, 2352.5, 3872.5].entries()) {
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
    'Main deck 6600 by 2600 millimetres. Rebuilt section 900 by 1970 millimetres behind the left end. One full-width tread projects 400 millimetres. Framing view shows nineteen 45 millimetre-wide joists J01 to J19, four dashed continuation candidates in the rebuilt section, eighteen flush cross-blocks for the assumed rotated decking, two double bearer lines and twelve proposed piles. The ground-supported tread frame is part of the same construction sequence. Six shared-pad symbols are a proposal for the independent tread; two new intermediate piles are also shown.',
    '0 0 1180 870');
  svg.setAttribute('role', 'group');
  const defs = el('defs');
  const boards = el('pattern', { id: `${uid}-boards`, width: 20, height: 11.05, patternUnits: 'userSpaceOnUse' });
  boards.append(el('rect', { width: 20, height: 11.05, fill: C.timber }));
  boards.append(el('line', { x1: 0, y1: 10.4, x2: 20, y2: 10.4, stroke: C.timberLine, 'stroke-width': .65, opacity: .7 }));
  defs.append(boards);
  const rotatedBoards = el('pattern', { id: `${uid}-boards-rotated`, width: 11.05, height: 20, patternUnits: 'userSpaceOnUse' });
  rotatedBoards.append(el('rect', { width: 11.05, height: 20, fill: C.timber }));
  rotatedBoards.append(el('line', { x1: 10.4, y1: 0, x2: 10.4, y2: 20, stroke: C.timberLine, 'stroke-width': .65, opacity: .7 }));
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
  const tread = interactive(svg, 'tread', 'One full-width tread: 6600 by 400 millimetres, selected surface 250 millimetres above garden; ground-supported box-frame proposal; six shared-pad proposal', selected);
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
        bearer.append(el('rect', { class: 'pile', 'data-x-mm': pile, 'data-y-mm': position, 'data-pile-class': [250,2690,6350].includes(pile) ? 'anchor' : 'ordinary', x: X + pile * S - 8.125, y: py - 8.125, width: 16.25, height: 16.25, fill: [250,2690,6350].includes(pile) ? '#c08d45' : '#fffefa', stroke: C.amber, 'stroke-width': 2 }));
      }
    }
    // Align J01–J04 with the 900 mm-wide rebuilt strip. This is a layout option,
    // not a verified span, bearing, continuity or cutting detail.
    const centres = JOIST_CENTRES;
    const joists = interactive(svg, 'joists', 'Nineteen provisional 140 by 45 joists J01 to J19; centres 285 millimetres three times, then 380 millimetres fifteen times. J01 to J04 have dashed rebuilt-section continuation candidates.', selected);
    for (const [i, centre] of centres.entries()) {
      const px = X + (centre - 22.5) * S;
      const id = `J${String(i + 1).padStart(2, '0')}`;
      if (i < 4) {
        joists.append(el('rect', { class: 'rebuilt-joist-extension', 'data-member-id': id, 'data-x-mm': centre, x: px, y: Y - RH, width: 45 * S, height: RH, fill: '#edf5e7', stroke: '#426b49', 'stroke-width': 1.4, 'stroke-dasharray': '6 4' }));
      }
      joists.append(el('rect', { class: 'main-joist', 'data-member-id': id, 'data-x-mm': centre, x: px, y: Y + (i < 4 ? 0 : 45 * S), width: 45 * S, height: H - (i < 4 ? 45 : 90) * S, fill: selected === 'joists' ? '#164c34' : '#456b4c', stroke: '#234c32', 'stroke-width': .7 }));
      text(svg, X + centre * S, Y + 23, id, {
        class: 'deck-label joist-id', 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 650,
        fill: '#203d2b', 'paint-order': 'stroke', stroke: '#ffffff', 'stroke-width': 4, 'stroke-linejoin': 'round'
      });
    }
    for (const [i, cx] of [2352.5, 3872.5].entries()) joists.append(el('rect', { class: 'butt-joist', 'data-member-id': `BJ${i+1}`, x: X + (cx - 22.5)*S, y: Y + 45*S, width: 45*S, height: (2600-90)*S, fill: '#78926e', stroke: '#375b35', 'stroke-width': .8 }));
    // Added intermediate support shortens the rebuilt spans without claiming old-beam capacity.
    const midY = Y - 800*S;
    bearer.append(el('rect', { class: 'rebuilt-new-bearer', x: X, y: midY - 45*S, width: RW, height: 90*S, fill: '#f4d6a6', stroke: C.amber, 'stroke-width': 1.5 }));
    for (const px of [175,725]) bearer.append(el('rect', { class:'rebuilt-new-pile', x:X+px*S-8.125, y:midY-8.125, width:16.25, height:16.25, fill:'#fffefa', stroke:C.amber, 'stroke-width':1.5 }));
    text(svg, X + RW + 14, midY + 5, 'New 900 bearer · Y−800 · 2 piles', {'font-size':12,fill:C.amber});
    const supportCentres = [...JOIST_CENTRES,2352.5,3872.5].sort((a,b)=>a-b);
    let lateralIndex=0;
    for(const cy of [600,2000]) for(let k=0;k<supportCentres.length-1;k++) {
      const clear=supportCentres[k+1]-supportCentres[k]-45;
      if(clear<=0) continue;
      joists.append(el('rect',{class:'main-lateral-block','data-member-id':`L${String(++lateralIndex).padStart(2,'0')}`,'data-clear-mm':clear,'data-y-mm':cy,x:X+(supportCentres[k]+22.5)*S,y:Y+(cy-22.5)*S,width:clear*S,height:45*S,fill:'#b8d7e4',stroke:'#436b7a','stroke-width':.7}));
    }
    // Rims occupy the finished envelope. Joists terminate at their inside faces.
    joists.append(el('rect', { class: 'main-rim', 'data-member-id': 'RM1', x: X, y: Y + (2600 - 45) * S, width: W, height: 45 * S, fill: '#b48d59', stroke: '#7c603c', 'stroke-width': .9 }));
    for (const [start, end] of [[45, 285], [330, 570], [615, 855], [900, 6600]]) joists.append(el('rect', { class: 'main-rim', 'data-member-id': 'RM2', x: X + start * S, y: Y, width: (end - start) * S, height: 45 * S, fill: '#b48d59', stroke: '#7c603c', 'stroke-width': .9 }));
    const blocking = interactive(svg, 'blocking', 'Eighteen flush cross-blocks between J01 to J04, at six support rows 385 millimetres apart, for the assumed rotated rebuilt decking; block-end fixing detail is provisional', selected);
    drawRebuiltBlocks(blocking, X, Y, S);
    drawTreadFrame(tread, TX, TY, S);
    text(svg, X + W + 11, Y + 350 * S + 5, 'A', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X + W + 11, Y + 2250 * S + 5, 'B', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X, 818, '19 lines +2 butt sisters. L01–L36: lateral blocks at Y600 /2000, within 300 of bearers.', { 'font-size': 16, fill: C.ink });
    text(svg, X, 845, '4 long joists +15 short +2 butt sisters. Filled piles: 6 proposed anchors. Tread: 6 shared pads.', { 'font-size': 15, fill: C.muted });
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
  text(labels, TX + TW / 2, TY + TH / 2 + 6, framing ? 'TREAD FRAME · 6 SHARED PADS' : 'ONE TREAD · 6600 × 400 mm', { 'text-anchor': 'middle', 'font-size': 17, 'font-weight': 600, 'letter-spacing': .6 });
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
    'Side section showing deck, one full-width 6600 by 400 millimetre tread, then garden. Measured total drop is about 500 millimetres. The user selects the tread surface halfway down, about 250 millimetres above the garden. That creates two approximately 250 millimetre rises. Pine decking thickness is 32 millimetres; board width remains provisional. The selected levels and allowable rises require verification; this is not an approved stair detail.',
    '0 0 1080 430');
  svg.append(el('rect', { width: 1080, height: 430, fill: C.paper }));
  const deckEnd = 470, deckTop = 131, groundY = 331, treadEnd = 630, treadTop = 231;
  // The horizontal and vertical section geometry uses the same 0.4px/mm scale.
  svg.append(el('path', {
    d: `M 100 ${deckTop} H ${deckEnd} V ${treadTop} H ${treadEnd} V ${groundY} H 932 V 361 H 100 Z`,
    fill: '#e8eee4', stroke: 'none'
  }));
  svg.append(el('rect', { x: 100, y: deckTop, width: deckEnd - 100, height: 12.8, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
  svg.append(el('rect', { x: deckEnd, y: treadTop, width: treadEnd - deckEnd, height: 12.8, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
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
  text(svg, 100, 399, 'Owner-selected 500/250 mm levels retained. Access compliance is not verified.', { 'font-size': 15, fill: C.muted });
}


/** Independent 6600 x 400 tread ladder, including the constrained height stack. */
export function renderTreadFrame(svg) {
  begin(svg, 'Proposed independent tread ladder frame',
    'One full-width 6600 by 400 millimetre tread. Two long 140 by 45 rails and nineteen 310 millimetre nominal crosspieces form one layer beneath 32 millimetre decking. Surface is selected at 250 millimetres above garden, frame top is 218 and underside 78. Six shared-pad proposals support both rails; exact foundation/anchor design still needs confirmation. SG8 H5 supply, low-clearance details, pad/anchor design and wet-service joints need the pre-build review.',
    '0 0 1180 800');
  svg.append(el('rect', { width: 1180, height: 800, fill: C.paper }));
  text(svg, 90, 35, 'TREAD FRAME — PROPOSAL', { 'font-size': 21, 'font-weight': 650 });
  const X = 100, Y = 100, S = .14;
  drawTreadFrame(svg, X, Y, S);
  dimH(svg, X, X + 6600 * S, 72, '6600 mm outer frame');
  dimV(svg, X + 6600 * S + 38, Y, Y + 400 * S, '400 mm');
  text(svg, 100, 195, '2 rails +19 crosspieces +2 butt sisters. 310 mm clear; six shared-pad proposal.', { 'font-size': 16 });
  text(svg, 100, 222, '6 shared pads carry both rails (12 bearings). Foundation/anchor design still requires review.', { 'font-size': 15, fill: C.muted });
  text(svg, 100, 276, 'SIDE SECTION THROUGH THE 400 mm DEPTH', { 'font-size': 16, 'font-weight': 650 });

  const left = 130, ground = 620, top = ground - 250, frameTop = ground - 218, frameBottom = ground - 78;
  // Five provisional 80 mm-board rows with illustrative 5 mm gaps and 70 mm edges.
  for (const [x, width] of [[0,70],[75,80],[160,80],[245,80],[330,70]]) {
    svg.append(el('rect', { class: 'tread-section-decking', x: left + x, y: top, width, height: 32, fill: C.timber, stroke: C.timberLine, 'stroke-width': 1 }));
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
  text(svg, 690, top + 10, '32 mm decking', { 'font-size': 18, 'font-weight': 600 });
  text(svg, 690, frameTop + 25, 'Frame top: 218 mm', { 'font-size': 17 });
  text(svg, 690, frameTop + 55, '140 mm-deep members, one layer', { 'font-size': 16 });
  text(svg, 690, frameBottom + 7, 'Frame underside: 78 mm', { 'font-size': 17 });
  text(svg, 690, frameBottom + 38, 'Low-clearance timber / ground fixing', { 'font-size': 15, fill: C.amber });
  text(svg, 690, frameBottom + 61, 'and support details: to confirm.', { 'font-size': 15, fill: C.amber });
  text(svg, 100, 700, 'Separate ground support is recommended; build its foundations with the main deck’s.', { 'font-size': 16 });
  text(svg, 100, 727, 'Frame section unchanged; recheck actual timber sizes, separation and low-clearance treatment.', { 'font-size': 15, fill: C.muted });
  text(svg, 100, 754, 'Selected surface 250; trial frame top / underside 218 /78 mm. Confirm actual sizes and separation.', { 'font-size': 15, fill: C.muted });
}

/** Rotated rebuilt boards fixed to flush cross-supports, not parallel joists. */
export function renderDeckingDetail(svg) {
  begin(svg, 'Rebuilt-section decking support and fixing proposal',
    'Assumed rebuilt decking runs along the 1970 millimetre depth, at ninety degrees to the main boards. J01, J02, J03 and J04 are proposed continuations. Eighteen flush cross-blocks between these joists make six support rows at 385 millimetre centres. Eleven board strips illustrate a provisional80 millimetre width and five millimetre gaps, not an actual product selection. Two fixing-location examples are shown per board at each support row. Exact screws, block-end fixings and edge distances require a pre-build specification.',
    '0 0 1180 800');
  svg.append(el('rect', { width: 1180, height: 800, fill: C.paper }));
  text(svg, 80, 36, 'REBUILT DECKING — ROTATED DIRECTION ASSUMED', { 'font-size': 21, 'font-weight': 650 });
  const X = 110, top = 125, S = .25, Y = top + 1970 * S;
  // Underlying members remain visible through the illustrative decking strips.
  for (const [i, x] of JOIST_CENTRES.slice(0, 4).entries()) {
    svg.append(el('rect', { class: 'detail-long-joist', 'data-member-id': `J0${i + 1}`, x: X + (x - 22.5) * S, y: top, width: 45 * S, height: 1970 * S, fill: '#426b49', stroke: '#21472c', 'stroke-width': 1 }));
    text(svg, X + x * S, Y + 30, `J0${i + 1}`, { 'text-anchor': 'middle', 'font-size': 14, 'font-weight': 650 });
  }
  drawRebuiltBlocks(svg, X, Y, S);
  // Provisional80 mm boards: nine full strips, two65 mm edges and ten5 mm gaps.
  const boardWidths = [65,...Array(9).fill(80),65];
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
  text(svg, textX, 140, 'J01–J04: proposed full-length continuations', { 'font-size': 19, 'font-weight': 600 });
  text(svg, textX, 171, 'They run parallel to these boards.', { 'font-size': 16, fill: C.muted });
  svg.append(el('rect', { x: textX, y: 210, width: 28, height: 12, fill: '#a7c6d0', stroke: '#436b7a' }));
  text(svg, textX + 42, 222, '18 flush cross-blocks in 6 rows', { 'font-size': 18, 'font-weight': 600 });
  text(svg, textX, 253, 'Three blocks per row, 240 mm nominal clear length.', { 'font-size': 16 });
  text(svg, textX, 283, 'Rows: 385 mm centres. Tops flush with joists.', { 'font-size': 16 });
  text(svg, textX, 313, 'No extra batten layer or extra finished height.', { 'font-size': 16, fill: C.muted });
  svg.append(el('circle', { cx: textX + 7, cy: 364, r: 4, fill: '#85432e' }));
  text(svg, textX + 27, 370, 'Fix boards down into cross-support rows.', { 'font-size': 18, 'font-weight': 600 });
  text(svg, textX, 403, 'Two fixing locations per board at each row are shown.', { 'font-size': 16 });
  text(svg, textX, 433, 'Exact 32 mm-board screws and edge/end distances: TBD.', { 'font-size': 16, fill: C.muted });
  text(svg, textX, 487, 'Before building: agree block-end connections,', { 'font-size': 16, fill: C.amber });
  text(svg, textX, 513, 'joist continuity, bearing and supported board joints.', { 'font-size': 16, fill: C.amber });
  text(svg, 110, 712, 'Board strips and dots are fixing examples, not a final board order or screw schedule.', { 'font-size': 16, fill: C.muted });
  text(svg, 110, 741, 'Direction is illustrated from the latest description; 80 mm width and5 mm gaps are assumptions; exact supplied width remains to measure.', { 'font-size': 15, fill: C.muted });
}
