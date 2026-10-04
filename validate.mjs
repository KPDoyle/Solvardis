import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('./dist/',import.meta.url));
let pages=0,refs=0;const missing=[],empty=[],legacyHostReferences=[];
function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isDirectory())walk(file);else if(entry.name.endsWith('.html')){
  pages++;const text=fs.readFileSync(file,'utf8');
  if(/(?:pi2\.local(?::8082)?|localhost:8082)/i.test(text))legacyHostReferences.push(path.relative(root,file));
  const links=[...text.matchAll(/\b(?:src|href|poster)=["'](\/[^"']*)["']/g)].map(m=>m[1]);
  for(const m of text.matchAll(/\bsrcset=["']([^"']*)["']/g))links.push(...m[1].split(',').map(s=>s.trim().split(/\s+/)[0]).filter(s=>s.startsWith('/')));
  for(const link of links){refs++;let target=path.join(root,decodeURIComponent(link.split(/[?#]/)[0]));if(fs.existsSync(target)&&fs.statSync(target).isDirectory())target=path.join(target,'index.html');if(!fs.existsSync(target))missing.push({page:path.relative(root,file),reference:link});}
}else{
  if(/\.(?:css|js|json|xml|txt|svg)$/i.test(entry.name)||!entry.name.includes('.')){
    const text=fs.readFileSync(file,'utf8');
    if(/(?:pi2\.local(?::8082)?|localhost:8082)/i.test(text))legacyHostReferences.push(path.relative(root,file));
  }
  if(/\.(png|jpe?g|gif|pdf|woff2?|ttf|mp4|webm)$/i.test(entry.name)&&fs.statSync(file).size===0)empty.push(path.relative(root,file));
}}}
walk(root);
const sheet=fs.readFileSync(path.join(root,'techdata/index.html'),'utf8');
const pdfs=[...sheet.matchAll(/href=["']([^"']+\.pdf)["']/g)].map(m=>m[1]);
const invalid=pdfs.filter(p=>fs.readFileSync(path.join(root,p)).subarray(0,5).toString()!=='%PDF-');
const result={routes:pages,local_references_checked:refs,missing_references:missing,empty_media:empty,legacy_host_references:legacyHostReferences,technical_data_pdfs:pdfs.length,invalid_pdfs:invalid};
console.log(JSON.stringify(result,null,2));
if(missing.length||empty.length||legacyHostReferences.length||invalid.length)process.exitCode=1;
