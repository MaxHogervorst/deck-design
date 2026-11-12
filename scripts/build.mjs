import {readFile,writeFile,mkdir,copyFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';import path from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));const read=n=>readFile(path.join(root,n),'utf8');
const names=['sheet','sheet2','sheet3'];const drawings=Object.fromEntries(await Promise.all(names.map(async n=>[n,await read(`site/drawings/${n}.svg`)])));
const [template,css,source]=await Promise.all(['site/index.html','site/styles.css','site/app.js'].map(read));const app=source.replace('const drawings = {}; // INLINE_DRAWINGS',`const drawings = ${JSON.stringify(drawings)};`);
const html=template.replace('<!-- INLINE_STYLES -->',`<style>\n${css}\n</style>`).replace('<!-- INLINE_SCRIPT -->',`<script type="module">\n${app.replace(/<\/script/gi,'<\\/script')}\n</script>`);
for(const dir of ['dist','docs']){await mkdir(path.join(root,dir,'drawings'),{recursive:true});await writeFile(path.join(root,dir,'index.html'),html);await copyFile(path.join(root,'SHOPPING_LIST.csv'),path.join(root,dir,'shopping-list.csv'));for(const name of names)await copyFile(path.join(root,'site/drawings',name+'.svg'),path.join(root,dir,'drawings',name+'.svg'));}
await writeFile(path.join(root,'docs/.nojekyll'),'');console.log('Built one current page, shopping CSV and three sheets.');
