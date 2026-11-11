const drawings = {}; // INLINE_DRAWINGS
for (const id of ['sheet','sheet2','sheet3','piles','framing','fixings']) {
  const el = document.querySelector('#view-' + id);
  if (el) el.innerHTML = drawings[id];
}
document.querySelector('#print').onclick = () => window.print();
