const NS = 'http://www.w3.org/2000/svg';
const C = {
  ink: '#243f36', muted: '#69796f', line: '#a2aea3', timber: '#dfc5a0',
  timberLine: '#c5a77f', green: '#547966', pale: '#e9eee7', amber: '#a86e36',
  amberFill: '#f2e5d2', paper: '#fafbf7', white: '#ffffff', outline: '#415f4b'
};
let sequence = 0;

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
  style.textContent = '.deck-area{cursor:pointer;outline:none}.deck-area .area-outline{transition:stroke .15s,stroke-width .15s}.deck-area:hover .area-outline,.deck-area:focus-visible .area-outline,.deck-area.selected .area-outline{stroke:#2a6651;stroke-width:4}.deck-label{pointer-events:none;user-select:none}';
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

/** Proportional, dimensioned concept plan. All member positions are provisional. */
export function renderPlan(svg, { view = 'layout', selected = null } = {}) {
  const framing = view === 'framing';
  const uid = begin(svg, framing ? 'Provisional deck framing plan' : 'Deck layout and dimensions',
    'Main deck 6600 by 2600 millimetres. A 900 by 1970 millimetre rebuilt section sits behind the left end beside the extension. One full-width tread spans 6600 millimetres and projects 400 millimetres towards the garden, as selected by the user. Activate an area for its details. Framing positions are provisional, not approved construction details.',
    '0 0 1180 870');
  svg.setAttribute('role', 'group');
  const defs = el('defs');
  const boards = el('pattern', { id: `${uid}-boards`, width: 20, height: 18.8, patternUnits: 'userSpaceOnUse' });
  boards.append(el('rect', { width: 20, height: 18.8, fill: framing ? '#efe3d0' : C.timber }));
  boards.append(el('line', { x1: 0, y1: 18.1, x2: 20, y2: 18.1, stroke: C.timberLine, 'stroke-width': .65, opacity: framing ? .3 : .7 }));
  defs.append(boards);
  const grid = el('pattern', { id: `${uid}-grid`, width: 24, height: 24, patternUnits: 'userSpaceOnUse' });
  grid.append(el('circle', { cx: 1, cy: 1, r: .65, fill: '#cfd7ca' }));
  defs.append(grid);
  svg.append(defs, el('rect', { width: 1180, height: 870, fill: C.paper }), el('rect', { x: 45, y: 20, width: 1090, height: 785, fill: `url(#${uid}-grid)`, opacity: .55 }));
  const S = .13, X = 130, Y = 346.1, W = 6600 * S, H = 2600 * S, RW = 900 * S, RH = 1970 * S;
  const main = interactive(svg, 'main', 'Main deck: 6600 by 2600 millimetres, 17.16 square metres, confirmed dimensions', selected);
  main.append(el('rect', { x: X, y: Y, width: W, height: H, fill: `url(#${uid}-boards)`, ...outline(selected, 'main') }));
  const rebuilt = interactive(svg, 'rebuilt', 'Rebuilt section: 900 by 1970 millimetres, 1.773 square metres; retained bearer at back edge', selected);
  rebuilt.append(el('rect', { x: X, y: Y - RH, width: RW, height: RH, fill: `url(#${uid}-boards)`, ...outline(selected, 'rebuilt') }));
  const extension = interactive(svg, 'extension', 'House extension: 5700 millimetre frontage; back extent unknown; deck is freestanding', selected);
  extension.append(el('rect', { x: X + RW, y: Y - RH, width: W - RW, height: RH, fill: '#e6ece4', ...outline(selected, 'extension', '#99a99a') }));
  // Dashed back edge indicates that the extension's true rear extent is not surveyed.
  line(extension, X + RW + 2, Y - RH, X + W - 2, Y - RH, { stroke: C.paper, 'stroke-width': 5 });
  line(extension, X + RW, Y - RH, X + W, Y - RH, { stroke: '#99a99a', 'stroke-dasharray': '8 6', 'stroke-width': 1.7 });
  const tread = interactive(svg, 'tread', 'One full-width garden tread: 6600 millimetres wide by 400 millimetres total projection; selected surface level about 250 millimetres above the garden', selected);
  const TX = X, TY = Y + H, TW = W, TH = 400 * S;
  tread.append(el('rect', { x: TX, y: TY, width: TW, height: TH, rx: 1, fill: `url(#${uid}-boards)`, ...outline(selected, 'tread', C.outline) }));

  if (framing) {
    const bearer = interactive(svg, 'bearer', 'Provisional framing: two double 140 by 45 bearer lines, twelve suggested piles; structural verification outstanding', selected);
    // Joist alignment in the rebuilt strip requires a junction detail; do not draw a resolved grid there.
    for (let i = 0; i < 16; i++) {
      const px = X + (22.5 + 437 * i) * S;
      if (px <= X + RW) continue;
      line(bearer, px, Y + 5, px, Y + H - 5, { stroke: '#7c8874', 'stroke-width': 1.6, opacity: .65 });
    }
    bearer.append(el('rect', { x: X + 3, y: Y + 3, width: RW - 6, height: 350 * S, fill: '#e6c492', opacity: .48, stroke: C.amber, 'stroke-dasharray': '3 4' }));
    for (const position of [350, 2250]) {
      const py = Y + position * S;
      bearer.append(el('rect', { x: X, y: py - 5.85, width: W, height: 11.7, fill: C.amberFill, ...outline(selected, 'bearer', C.amber), 'stroke-dasharray': '7 4' }));
      for (const pile of [250, 1470, 2690, 3910, 5130, 6350]) {
        bearer.append(el('rect', { x: X + pile * S - 8.125, y: py - 8.125, width: 16.25, height: 16.25, rx: 1.5, fill: C.paper, stroke: C.amber, 'stroke-width': 2 }));
      }
    }
    text(svg, X + W + 11, Y + 350 * S + 5, 'A', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X + W + 11, Y + 2250 * S + 5, 'B', { fill: C.amber, 'font-size': 17, 'font-weight': 700 });
    text(svg, X + W / 2, Y + H / 2 - 12, 'PROVISIONAL FRAMING', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 24, 'font-weight': 650, 'letter-spacing': 1.4, fill: C.ink, 'paint-order': 'stroke', stroke: '#efe3d0', 'stroke-width': 9 });
    text(svg, X + W / 2, Y + H / 2 + 18, '2 double bearer lines · 12 suggested piles', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 17, fill: C.muted, 'paint-order': 'stroke', stroke: '#efe3d0', 'stroke-width': 8 });
    text(svg, X, 825, 'Dashed amber = proposed members. Junction, spans, bracing and connections need verification.', { 'font-size': 16, fill: C.amber });
  } else {
    text(svg, X + W / 2, Y + H / 2 - 5, 'MAIN DECK', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 31, 'font-weight': 550, 'letter-spacing': 2.5 });
    text(svg, X + W / 2, Y + H / 2 + 29, '6.60 × 2.60 m  /  17.16 m²', { class: 'deck-label', 'text-anchor': 'middle', 'font-size': 19, fill: '#5f664e' });
    text(svg, X, 825, 'Confirmed layout: main deck, rebuilt section and full-width tread. Structural details need review.', { 'font-size': 16, fill: C.muted });
  }
  const labels = el('g', { class: 'deck-label', 'pointer-events': 'none' }); svg.append(labels);
  text(labels, X + RW / 2, Y - RH / 2 - 18, 'REBUILT', { 'text-anchor': 'middle', 'font-size': 16, 'font-weight': 650, 'letter-spacing': .5 });
  text(labels, X + RW / 2, Y - RH / 2 + 7, '0.90 × 1.97 m', { 'text-anchor': 'middle', 'font-size': 13 });
  text(labels, X + RW / 2, Y - RH / 2 + 30, '1.773 m²', { 'text-anchor': 'middle', 'font-size': 14, fill: '#5f664e' });
  text(labels, X + RW + (W - RW) / 2, Y - RH / 2 - 12, 'HOUSE EXTENSION', { 'text-anchor': 'middle', 'font-size': 25, 'font-weight': 450, 'letter-spacing': 2 });
  text(labels, X + RW + (W - RW) / 2, Y - RH / 2 + 20, '5.70 m frontage · rear extent not surveyed', { 'text-anchor': 'middle', 'font-size': 17, fill: C.muted });
  text(labels, TX + TW / 2, TY + TH / 2 + 6, 'ONE TREAD · 6600 × 400 mm', { 'text-anchor': 'middle', 'font-size': 17, 'font-weight': 600, 'letter-spacing': 1 });
  text(labels, X + W / 2, 781, 'GARDEN', { 'text-anchor': 'middle', 'font-size': 17, 'letter-spacing': 3, fill: C.green });
  const retained = interactive(svg, 'rebuilt', 'Retained bearer at rebuilt section back edge, approximately Y minus 1970 millimetres; capacity and exact offset unverified', selected);
  retained.append(el('rect', { x: X + 2, y: Y - RH - 4, width: RW - 4, height: 8, rx: 1, fill: C.green, stroke: selected === 'rebuilt' ? '#23694d' : C.green, 'stroke-width': 1.5 }));
  text(svg, X + RW + 17, Y - RH - 11, 'Retained bearer · exact offset to verify', { 'font-size': 13, fill: C.green });
  dimH(svg, X, X + W, 43, '6600 mm main frontage');
  dimH(svg, X, X + RW, Y - 20, '900');
  dimH(svg, X + RW + 8, X + W, Y - 20, '5700 mm extension frontage');
  dimV(svg, 83, Y - RH, Y, '1970 mm');
  dimV(svg, X + W + 54, Y, Y + H, '2600 mm');
  dimV(svg, TX + TW + 30, TY, TY + TH, '400 mm');
  line(svg, X + W + 78, 111, X + W + 78, 161, { stroke: C.green, 'stroke-width': 1.5 });
  line(svg, X + W + 78, 111, X + W + 73, 120, { stroke: C.green });
  line(svg, X + W + 78, 111, X + W + 83, 120, { stroke: C.green });
  text(svg, X + W + 78, 184, 'HOUSE', { 'text-anchor': 'middle', 'font-size': 11, fill: C.muted, 'letter-spacing': 1 });
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
  text(svg, 100, 399, 'Selected halfway tread level · 38 mm pine decking. Rises and landing detail need verification.', { 'font-size': 15, fill: C.muted });
}
