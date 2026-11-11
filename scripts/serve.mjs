import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const port = Number(process.env.PORT || 3000);
const server = http.createServer(async (req, res) => {
  const pathname = new URL(req.url, 'http://localhost').pathname;
  if (!['/', '/index.html', '/shopping-list.csv', '/drawings/sheet.svg', '/drawings/piles.svg', '/drawings/framing.svg', '/drawings/fixings.svg'].includes(pathname)) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Not found');
    return;
  }
  try {
    const csv = pathname === '/shopping-list.csv';
    const vector = pathname.startsWith('/drawings/');
    const file = fileURLToPath(new URL(csv ? '../dist/shopping-list.csv' : vector ? '../dist'+pathname : '../dist/index.html', import.meta.url));
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': csv ? 'text/csv; charset=utf-8' : vector ? 'image/svg+xml; charset=utf-8' : 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch {
    res.writeHead(503, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Build the website first with npm run build.');
  }
});
server.listen(port, '0.0.0.0', () => console.log(`Deck review server listening on port ${port}.`));
