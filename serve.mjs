import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('./dist/', import.meta.url));
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.gif':'image/gif','.svg':'image/svg+xml','.ico':'image/x-icon','.pdf':'application/pdf','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.eot':'application/vnd.ms-fontobject','.mp4':'video/mp4','.webm':'video/webm'};
const port = Number(process.env.PORT || 4173);
createServer(async (req,res) => {
  try {
    if (!['GET','HEAD'].includes(req.method)) {res.writeHead(405,{'Allow':'GET, HEAD'});res.end();return;}
    const url = new URL(req.url,'http://localhost');
    let target = path.resolve(root,'.'+decodeURIComponent(url.pathname));
    if (target!==path.resolve(root) && !target.startsWith(root)) {res.writeHead(403);res.end();return;}
    if ((await stat(target)).isDirectory()) target=path.join(target,'index.html');
    const body = await readFile(target);
    res.writeHead(200,{'Content-Type':types[path.extname(target)]||'application/octet-stream','Content-Length':body.length});
    res.end(req.method==='HEAD'?undefined:body);
  } catch {
    res.writeHead(404,{'Content-Type':'text/html; charset=utf-8'});
    res.end('<!doctype html><title>Solvardis — Page not found</title><h1>Page not found</h1><a href="/">Return to Solvardis</a>');
  }
}).listen(port,'127.0.0.1',()=>console.log(`Solvardis: http://127.0.0.1:${port}`));
