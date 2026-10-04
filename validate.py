"""Verify every local page/asset reference and all technical data PDFs."""
import json, urllib.parse
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
DIST = ROOT/'dist'
class References(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for key in ['src','href','poster']:
            if d.get(key) and d[key].startswith('/'):self.refs.append(d[key])
        if d.get('srcset'):self.refs.extend(s.strip().split()[0] for s in d['srcset'].split(','))
missing=[];count=0
for page in DIST.rglob('*.html'):
    p=References();p.feed(page.read_text())
    for ref in p.refs:
        if not ref.startswith('/'):continue
        target=DIST/urllib.parse.unquote(urllib.parse.urlsplit(ref).path.lstrip('/'))
        if target.is_dir():target=target/'index.html'
        if not target.exists():missing.append({'page':str(page.relative_to(DIST)),'reference':ref})
        count+=1
p=References();p.feed((DIST/'techdata/index.html').read_text())
pdfs=[r for r in p.refs if r.endswith('.pdf')]
bad_pdf=[r for r in pdfs if not (DIST/r.lstrip('/')).read_bytes().startswith(b'%PDF-')]
result={'routes':len(list(DIST.rglob('index.html'))),'local_references_checked':count,'missing_references':missing,'technical_data_pdfs':len(pdfs),'invalid_pdfs':bad_pdf}
print(json.dumps(result,indent=2))
if missing or bad_pdf:raise SystemExit(1)
