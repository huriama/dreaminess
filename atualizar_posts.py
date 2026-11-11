import json, re
from pathlib import Path
from datetime import datetime
from html import unescape

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'posts.json'
EXCLUDED = {'index.html', '404.html'}

def clean(s):
    return unescape(re.sub(r'<[^>]+>', '', s)).strip()

def metadata(html, name):
    title = re.search(r'<h1\b[^>]*>(.*?)</h1>', html, re.I | re.S)
    if not title:
        title = re.search(r'<title\b[^>]*>(.*?)</title>', html, re.I | re.S)
    title = clean(title.group(1)) if title else name.replace('-', ' ').removesuffix('.html').title()
    title = re.sub(r'\s*[—|]\s*Dreaminess\s*$', '', title, flags=re.I)
    desc = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)', html, re.I)
    if not desc:
        desc = re.search(r'<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description', html, re.I)
    image = re.search(r'<(?:img|meta)\b[^>]*(?:src|content)=["\'](imagens/[^"\']+)["\']', html, re.I)
    return title, unescape(desc.group(1)) if desc else '', image.group(1) if image else None

def main():
    posts = json.loads(INDEX.read_text(encoding='utf-8')) if INDEX.exists() else []
    existing = {p.get('url') for p in posts}
    new = []
    for path in ROOT.glob('*.html'):
        if path.name in EXCLUDED or path.name in existing:
            continue
        html = path.read_text(encoding='utf-8')
        # Only include actual articles, not utility pages.
        if not re.search(r'<article\b', html, re.I):
            continue
        title, description, image = metadata(html, path.name)
        post = {'title': title, 'date': datetime.now().strftime('%d/%m/%Y'), 'url': path.name}
        if image:
            post['image'] = image
        if description:
            post['description'] = description
        new.append((path.stat().st_mtime, post))
    if not new:
        print('Nenhum artigo novo encontrado.')
        return
    new.sort(reverse=True)
    INDEX.write_text(json.dumps([p for _, p in new] + posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(new)} artigo(s) adicionado(s) ao índice.')

if __name__ == '__main__':
    main()
