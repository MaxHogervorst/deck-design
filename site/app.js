const drawings = {}; // INLINE_DRAWINGS
for (const id of ['sheet','sheet2','sheet3']) {
  const el = document.querySelector('#view-' + id);
  if (el) el.innerHTML = drawings[id];
}
document.querySelector('#print').onclick = () => window.print();
