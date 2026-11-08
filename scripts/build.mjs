import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));
const read=name=>readFile(path.join(root,name),'utf8');
const [template,css,app]=await Promise.all(['site/index.html','site/styles.css','site/app.js'].map(read));
const html=template.replace('<!-- INLINE_STYLES -->',`<style>\n${css}\n</style>`).replace('<!-- INLINE_SCRIPT -->',`<script type="module">\n${app.replace(/<\/script/gi,'<\\/script')}\n</script>`);
for(const dir of ['dist','docs']){await mkdir(path.join(root,dir),{recursive:true});await writeFile(path.join(root,dir,'index.html'),html);await writeFile(path.join(root,dir,'shopping-list.csv'),await read('SHOPPING_LIST.csv'));}
await writeFile(path.join(root,'docs/.nojekyll'),'');
console.log('Built standalone guide in dist/index.html and docs/index.html; no historical working documents embedded.');
