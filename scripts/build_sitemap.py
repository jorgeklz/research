#!/usr/bin/env python3
"""Generate sitemap.xml (pages in EN and ES, plus one URL per post). Run from the repo root."""
import json
from datetime import date
from pathlib import Path
from urllib.parse import quote

BASE = "https://jorgeklz.github.io/research/"
ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    ("index.html", "es/index.html"),
    ("publications.html", "es/publicaciones.html"),
    ("news.html", "es/noticias.html"),
    ("portfolio.html", "es/portafolio.html"),
]


def entry(loc, alts=None, lastmod=None):
    out = ["  <url>", f"    <loc>{loc}</loc>"]
    if lastmod:
        out.append(f"    <lastmod>{lastmod}</lastmod>")
    for lang, href in (alts or []):
        out.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>')
    out.append("  </url>")
    return "\n".join(out)


def main():
    posts = json.loads((ROOT / "data" / "posts.json").read_text(encoding="utf-8")).get("items", [])
    # stable lastmod (newest post date) so the file only changes when the content does
    today = max([(p.get("date") or "")[:10] for p in posts] or [date.today().isoformat()])
    items = []
    for en, es in PAGES:
        alts = [("en", BASE + en), ("es", BASE + es)]
        items.append(entry(BASE + en, alts, today))
        items.append(entry(BASE + es, alts, today))
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8")).get("items", [])
    for pr in projects:
        q = quote(str(pr["id"]), safe="")
        alts = [("en", f"{BASE}project.html?id={q}"), ("es", f"{BASE}es/proyecto.html?id={q}")]
        items.append(entry(alts[0][1], alts, today))
        items.append(entry(alts[1][1], alts, today))
    for p in posts:
        pid = p.get("id")
        if not pid:
            continue
        q = quote(str(pid), safe="")
        alts = [("en", f"{BASE}post.html?id={q}"), ("es", f"{BASE}es/entrada.html?id={q}")]
        items.append(entry(alts[0][1], alts, (p.get("date") or today)[:10]))
        items.append(entry(alts[1][1], alts, (p.get("date") or today)[:10]))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(items) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml: {len(items)} URLs")


if __name__ == "__main__":
    main()
