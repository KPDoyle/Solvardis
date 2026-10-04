#!/usr/bin/env python3
"""Reproducible WordPress-to-static capture. No PHP or WordPress at runtime."""
import argparse, concurrent.futures, hashlib, html, json, re, urllib.parse, urllib.request, zipfile
from pathlib import Path
from html.parser import HTMLParser

BASE = 'http://pi2.local:8082'
ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
UA = 'Mozilla/5.0 SolvardisStaticCapture/1.0'
URLS = re.compile(r'''(?:https?:)?//[^\s<>"'\\)]+''')
BAD = ('/wp-json', '/xmlrpc.php', '/wp-admin/', '/wp-login.php', '/feed/', '/comments/feed/')

def request(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=45) as response:
        return response.read(), response.headers.get_content_type()

def local(url):
    url = html.unescape(url).replace('\\/', '/')
    u = urllib.parse.urlsplit(url if not url.startswith('//') else 'https:' + url)
    if u.hostname == 'pi2.local':
        p = u.path.replace('/wp-content/', '/assets/content/').replace('/wp-includes/', '/assets/vendor/')
        if p.endswith('.php'): return '#'
        return p + (('?' + u.query) if u.query and not p.startswith('/assets/') else '') + (('#' + u.fragment) if u.fragment else '')
    if u.hostname in ['fonts.googleapis.com', 'fonts.gstatic.com']:
        normalized = urllib.parse.urlunsplit(('https',u.netloc,u.path,u.query,u.fragment))
        return '/assets/fonts/' + hashlib.sha256(normalized.encode()).hexdigest()[:20] + ('.css' if u.hostname == 'fonts.googleapis.com' else Path(u.path).suffix)
    if u.hostname in ['demo.qodeinteractive.com', 'bridge.qodeinteractive.com'] and '/wp-content/' in u.path:
        return '/assets/content/' + u.path.split('/wp-content/', 1)[1]
    return url

def rewrite(text):
    text = text.replace('http:\\/\\/pi2.local:8082', BASE)
    text = URLS.sub(lambda m: local(m.group()), text)
    return text

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.assets = set(); self.pages = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for key in ['src', 'poster', 'data-src']:
            if d.get(key): self.assets.add(d[key])
        if d.get('srcset'):
            self.assets.update(s.strip().split()[0] for s in d['srcset'].split(','))
        if tag == 'link' and d.get('rel') in ['stylesheet', 'icon', 'shortcut icon', 'apple-touch-icon']:
            self.assets.add(d.get('href',''))
        if tag == 'a' and d.get('href'):
            u = urllib.parse.urlsplit(d['href'])
            if u.hostname == 'pi2.local' or (not u.hostname and u.path.startswith('/')):
                if Path(u.path).suffix: self.assets.add(d['href'])
                elif not any(b in u.path for b in BAD): self.pages.add(u.path)

def clean_page(text):
    text = re.sub(r'<link\b[^>]*(?:dns-prefetch|pingback|EditURI|api\.w\.org|wp-json|application/(?:rss\+xml|json\+oembed|xml\+oembed)|title=["\']JSON)[^>]*>', '', text, flags=re.I)
    text = re.sub(r'<meta\s+name=["\']generator["\'][^>]*>', '', text, flags=re.I)
    text = re.sub(r'<script\b[^>]*(?:id=["\'](?:wp-emoji-settings|qode-like-js(?:-extra)?|comment-reply-js)|type=["\']speculationrules)[^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'<script\b[^>]*type=["\']module["\'][^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'<script\b[^>]*>\s*jQuery\(document\)\.ready\(function\(\$\)\{\s*\$j\(\'form#contact-form\'.*?</script>', '', text, flags=re.S)
    if 'id="map_canvas"' not in text and 'qode_google_map' not in text:
        text = re.sub(r'<script\b[^>]*id=["\']google_map_api-js["\'][^>]*>.*?</script>', '', text, flags=re.S)
    text = re.sub(r'(<a\b[^>]*?)href=["\']["\']([^>]*>Home</a>)',r'\1href="/"\2',text)
    # Public map configuration is retained for parity; it is an external service.
    text = rewrite(text)
    text = text.replace('</head>', '<link rel="stylesheet" href="/assets/content/themes/bridge/css/webkit_stylesheet.css"></head>')
    text = text.replace('</body>', '<script src="/assets/static-adapter.js"></script></body>')
    return text

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--export', required=True); parser.add_argument('--uploads', required=True)
    args = parser.parse_args(); records = json.load(open(args.export)); z = zipfile.ZipFile(args.uploads)
    DIST.mkdir(parents=True, exist_ok=True)
    routes = {'/'} | {urllib.parse.urlsplit(d['link']).path for d in records if d['type'] in ['page','portfolio_page'] and d['status']=='publish'}
    assets = set(); pages = {}; failures = []; seen = set()
    ids = {urllib.parse.urlsplit(d['link']).path:d['id'] for d in records if d['type'] in ['page','portfolio_page']}
    def page(path):
        try:
            try:
                data, kind = request(BASE + urllib.parse.quote(urllib.parse.unquote(path), safe='/'))
            except Exception:
                if path not in ids: raise
                record = next(d for d in records if d['id']==ids[path])
                query = ('portfolio_page='+record['slug']) if record['type']=='portfolio_page' else ('page_id='+ids[path])
                data, kind = request(BASE + '/?'+ query + '&preview=true')
            if kind != 'text/html': raise ValueError(kind)
            return path, data.decode('utf-8'), None
        except Exception as e: return path, None, str(e)
    while routes - seen:
        todo = sorted(routes - seen); seen.update(todo)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for path, text, error in pool.map(page, todo):
                if error: failures.append({'url': BASE+path, 'error':error}); continue
                p = Links(); p.feed(text); assets.update(p.assets)
                routes.update(s for s in p.pages if s and not s.startswith('/?'))
                assets.update(m.group() for m in URLS.finditer(text) if '/wp-content/' in m.group() or 'fonts.google' in m.group())
                pages[path] = text
        print('Captured pages:',len(pages),flush=True)
    recovered = []
    for record in records:
        path = urllib.parse.urlsplit(record['link']).path
        if record['type'] != 'page' or record['status'] != 'publish' or path in pages: continue
        try:
            data,_ = request(BASE+'/wp-json/wp/v2/pages/'+record['id'])
            content = json.loads(data)['content']['rendered']
            template = pages['/solutions/']
            match = re.search(r'<div class="full_width_inner"[^>]*>',template)
            start = match.end(); depth = 1
            for tag in re.finditer(r'</?div\b[^>]*>',template[start:]):
                depth += -1 if tag.group().startswith('</') else 1
                if depth==0: end=start+tag.start(); break
            page_text = template[:start]+content+template[end:]
            page_text = page_text.replace('Our Services',record['title']).replace('OUR SERVICES',record['title'].upper()).replace('page-id-15338','page-id-'+record['id']).replace('>15338<','>'+record['id']+'<')
            pages[path]=page_text; recovered.append(path)
            failures=[f for f in failures if f['url']!=BASE+path]
            p=Links();p.feed(page_text);assets.update(p.assets)
        except Exception as e: print('REST fallback failed:',path,str(e),flush=True)
    # Include every original exported attachment and its PDF, not only visible thumbnails.
    assets.update(d['attachment'] for d in records if d['type']=='attachment' and d.get('attachment'))
    assets.add(BASE+'/wp-content/themes/bridge/css/webkit_stylesheet.css')
    skins = BASE+'/wp-content/plugins/LayerSlider/static/layerslider/skins/'
    for name in ['noskin','fullwidth','v5','v6','borderlessdark','borderlesslight','glass','lightskin','darkskin']:
        assets.update([skins+name+'/skin.css',skins+name+'/skin.png'])
    captured = {}; asset_seen = set()
    def asset(url):
        url = html.unescape(url); url = urllib.parse.urljoin(BASE+'/',url)
        destination = local(url).split('?')[0].split('#')[0]
        if not destination.startswith('/assets/'): return url, None, None, None
        try:
            archive_name = 'uploads/'+urllib.parse.unquote(urllib.parse.urlsplit(url).path.split('/uploads/',1)[1]) if '/uploads/' in url else ''
            if archive_name in z.namelist(): data = z.read(archive_name); kind = 'text/css' if archive_name.endswith('.css') else 'binary'
            else: data, kind = request(url.replace('http://fonts.', 'https://fonts.'))
            return url, destination, data, kind
        except Exception as e: return url, destination, None, str(e)
    while assets - asset_seen:
        todo = sorted(assets - asset_seen); asset_seen.update(todo)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for url,destination,data,kind in pool.map(asset,todo):
                if not destination: continue
                if data is None: failures.append({'url':url,'error':kind}); continue
                target = DIST / urllib.parse.unquote(destination.lstrip('/')); target.parent.mkdir(parents=True,exist_ok=True)
                if destination.endswith(('.css','.js')):
                    text = data.decode('utf-8', errors='replace')
                    for ref in re.findall(r'''url\(\s*["']?([^\s)'";]+)''',text):
                        if not ref.startswith('data:'): assets.add(urllib.parse.urljoin(url,ref))
                    target.write_text(rewrite(text));
                else: target.write_bytes(data)
                captured[url]=destination
        print('Captured assets:',len(captured),flush=True)
    for path,text in pages.items():
        target = DIST / path.strip('/') / 'index.html'; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(clean_page(text))
    mapping = [{'id':d['id'],'title':d['title'],'source':d['attachment'],'local':local(d['attachment']),'in_zip':('uploads/'+urllib.parse.urlsplit(d['attachment']).path.split('/uploads/',1)[-1]) in z.namelist()} for d in records if d['type']=='attachment' and d.get('attachment')]
    (ROOT/'asset-map.json').write_text(json.dumps(mapping,indent=2))
    (ROOT/'capture-report.json').write_text(json.dumps({'pages':sorted(pages),'assets':len(captured),'zip_entries':len(z.namelist()),'zip_expanded_bytes':sum(i.file_size for i in z.infolist()),'failures':failures,'rest_recovered_pages':recovered,'limitations':['The exported legacy Shop page is empty and the original frontend returns HTTP 500. No commerce backend is included.','The contact map retains the original Google Maps configuration and requires the external Google Maps service.']},indent=2))
    (ROOT/'page-map.json').write_text(json.dumps([{'id':d['id'],'title':d['title'],'route':urllib.parse.urlsplit(d['link']).path,'shortcodes':sorted(set(re.findall(r'\[([a-z_]+)',d.get('content') or '')))} for d in records if d['type'] in ['page','portfolio_page']],indent=2))
    print('COMPLETE',len(pages),len(captured),'failures',len(failures),flush=True)

if __name__ == '__main__': main()
