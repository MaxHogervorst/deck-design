import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const read = (name) => readFile(path.join(root, name), 'utf8');
const files = ['PROJECT.md', 'DESIGN.md', 'MATERIALS.md', 'OPEN_ISSUES.md', 'SITE_MEASUREMENTS.md', 'BUILD_STEPS.md', 'REFERENCES.md', 'DECISIONS.md'];
const sources = Object.fromEntries(await Promise.all(files.map(async name => [name, await read(name)])));
const css = await read('site/styles.css');
const diagrams = (await read('site/diagrams.js')).replace(/^export\s+/gm, '');
const app = (await read('site/app.js')).replace(/^import\s+\{[^}]*\}\s+from\s+['"]\.\/diagrams\.js['"];?\s*$/m, '');
const safeJSON = JSON.stringify(sources).replace(/</g, '\\u003c');
const script = (diagrams + '\n' + app).replace(/<\/script/gi, '<\\/script');
const html = (await read('site/index.html'))
  .replace('<!-- INLINE_STYLES -->', `<style>\n${css}\n</style>`)
  .replace('<!-- SOURCE_DOCUMENTS -->', `<script type="application/json" id="source-documents">${safeJSON}</script>`)
  .replace('<!-- INLINE_SCRIPT -->', `<script type="module">\n${script}\n</script>`);
await mkdir(path.join(root, 'dist'), { recursive: true });
await writeFile(path.join(root, 'dist/index.html'), html);
await mkdir(path.join(root, 'docs'), { recursive: true });
const publicHTML = html
  .replace(/<script type="application\/json" id="source-documents">[\s\S]*?<\/script>/, '<script type="application/json" id="source-documents">{}</script>')
  .replace(/^[ \t]*<section class="sources-section page-width"[\s\S]*?<\/section>[ \t]*\n?/m, '');
await writeFile(path.join(root, 'docs/index.html'), publicHTML);
await writeFile(path.join(root, 'docs/.nojekyll'), '');
console.log(`Built dist/index.html and docs/index.html (${Math.round(Buffer.byteLength(html) / 1024)} KB). Pages output excludes private working documents.`);
