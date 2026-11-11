#!/usr/bin/env python3
"""Atualiza posts.json com novos artigos HTML na raiz do Dreaminess.

Preserva os metadados existentes e ordena as publicações da mais recente
para a mais antiga, sem alterar os textos HTML.
"""
import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / 'posts.json'
EXCLUDED = {'index.html'}


def extract(pattern, html):
    match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
    return unescape(re.sub(r'\s+', ' ', match.group(1)).strip()) if match else ''


def meta(html, name):
    for tag in re.findall(r'<meta\b[^>]*>', html, flags=re.IGNORECASE | re.DOTALL):
        key = extract(r'\b(?:name|property)\s*=\s*["\']([^"\']+)["\']', tag)
        if key.lower() == name.lower():
            return extract(r'\bcontent\s*=\s*["\']([^"\']*)["\']', tag)
    return ''


def main():
    posts = json.loads(INDEX.read_text(encoding='utf-8')) if INDEX.exists() else []
    if not isinstance(posts, list):
        raise ValueError('posts.json precisa conter uma lista JSON')
    existing = {p.get('url') for p in posts if isinstance(p, dict)}
    new = []
    for file in ROOT.glob('*.html'):
        if file.name.lower() in EXCLUDED or file.name in existing:
            continue
        html = file.read_text(encoding='utf-8-sig')
        # Somente artigos explicitamente marcados, ou páginas com estrutura de artigo.
        if not (re.search(r'<article\b', html, flags=re.IGNORECASE) or meta(html, 'post-title')):
            continue
        title = meta(html, 'post-title') or extract(r'<h1\b[^>]*>(.*?)</h1>', html) or extract(r'<title\b[^>]*>(.*?)</title>', html)
        title = re.sub(r'<[^>]+>', '', title).strip()
        if not title:
            continue
        entry = {
            'title': title,
            'date': meta(html, 'post-date') or datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y'),
            'url': file.name,
        }
        description = meta(html, 'description') or meta(html, 'post-description')
        image = meta(html, 'post-image')
        if description:
            entry['description'] = description
        if image:
            entry['image'] = image
            alt = meta(html, 'post-image-alt')
            if alt:
                entry['imageAlt'] = alt
        new.append((file.stat().st_mtime, entry))
    # Datas explícitas prevalecem. Entradas antigas sem data mantêm sua
    # posição relativa e ficam após as publicações datadas.
    # A ordenação é estável: empates preservam a ordem atual.
    new.sort(key=lambda item: item[0], reverse=True)
    updated = [item[1] for item in new] + posts

    def post_date(post):
        raw = post.get('date', '') if isinstance(post, dict) else ''
        try:
            return datetime.strptime(raw, '%d/%m/%Y').date().toordinal()
        except (ValueError, TypeError):
            return 0

    updated.sort(key=post_date, reverse=True)
    serialized = json.dumps(updated, ensure_ascii=False, indent=2) + '\n'
    if not INDEX.exists() or INDEX.read_text(encoding='utf-8') != serialized:
        INDEX.write_text(serialized, encoding='utf-8')
        print(f'{len(new)} novo(s) artigo(s); publicações ordenadas da mais recente para a mais antiga.')
    else:
        print('Publicações já estão na ordem correta.')


if __name__ == '__main__':
    main()
