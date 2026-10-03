#!/usr/bin/env python3
"""
update_publications.py
----------------------
Automatic pipeline for jorge-parraga researcher site.

1. Queries the ORCID public API for all works of the author.
2. Detects publications not yet present in data/publications.json.
3. Enriches each new one with Crossref metadata (authors, venue, abstract).
4. Generates a bilingual (EN/ES) plain-language post for each new publication:
   - If the ANTHROPIC_API_KEY environment variable is set, it asks Claude to
     write a proper divulgative post from the title + abstract.
   - Otherwise it creates a structured draft post (marked "auto": true) that
     you can polish by hand.
5. Updates data/publications.json and data/posts.json.

Run manually:   python3 scripts/update_publications.py
Run in CI:      see .github/workflows/update-publications.yml

Only Python standard library is required.
"""

import json
import os
import re
import sys
import html
import datetime
import urllib.request
import urllib.parse
import urllib.error

ORCID_ID = "0000-0001-8558-9122"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBS_PATH = os.path.join(ROOT, "data", "publications.json")
POSTS_PATH = os.path.join(ROOT, "data", "posts.json")

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

UA = {"User-Agent": "jorge-parraga-site-updater/1.0 (mailto:jorge.parraga@utm.edu.ec)"}


def get_json(url, headers=None, data=None, timeout=40):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def slugify(t, maxlen=40):
    s = re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")
    return s[:maxlen].rstrip("-") or "entry"


# ---------------------------------------------------------------- ORCID

def fetch_orcid_works():
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    data = get_json(url, headers={"Accept": "application/json"})
    works = []
    for group in data.get("group", []):
        s = group.get("work-summary", [{}])[0]
        title = (((s.get("title") or {}).get("title") or {}).get("value") or "").strip()
        year = None
        pd = s.get("publication-date") or {}
        if pd.get("year"):
            try:
                year = int(pd["year"]["value"])
            except (KeyError, ValueError, TypeError):
                year = None
        doi = None
        ids = (s.get("external-ids") or {}).get("external-id") or []
        for eid in ids:
            if eid.get("external-id-type") == "doi":
                doi = (eid.get("external-id-value") or "").strip()
                break
        wtype = s.get("type") or ""
        works.append({"title": title, "year": year, "doi": doi, "orcid_type": wtype})
    return works


# ------------------------------------------------------------- Crossref

def strip_jats(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def fetch_crossref(doi):
    try:
        msg = get_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")["message"]
    except Exception as e:
        print(f"  crossref failed for {doi}: {e}")
        return {}
    authors = []
    for a in msg.get("author", []):
        name = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if name:
            authors.append(name)
    venue = ""
    ct = msg.get("container-title") or []
    if ct:
        venue = ct[0]
    year = None
    for k in ("published-print", "published-online", "issued"):
        parts = (msg.get(k) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    cr_type = msg.get("type", "")
    ptype = "journal" if cr_type == "journal-article" else "conference" if "proceedings" in cr_type or "conference" in cr_type else "other"
    return {
        "title": strip_jats((msg.get("title") or [""])[0]),
        "authors": authors,
        "venue": venue,
        "year": year,
        "pages": msg.get("page"),
        "type": ptype,
        "abstract": strip_jats(msg.get("abstract", "")),
        "openAccess": any("creativecommons" in (l.get("URL") or "") for l in msg.get("license", [])),
    }


# ------------------------------------------------- Post generation

PROMPT = """You are helping a researcher explain their work to the general public.
Write a clear, simple plain-language post (120-200 words per language) that explains what the paper
actually does and why it matters, so ANY person can understand it. Both language versions must be
fully self-contained and natural in that language (the Spanish version in Spanish even if the paper
is in English, and vice versa) — never a literal translation and never a copy of the abstract.

Hard rules:
- NEVER write phrases like "In the authors' words", "En palabras de los autores", or quote the abstract verbatim.
- Explain jargon in one short clause the first time it appears.
- Do not overstate. If the abstract is missing, explain cautiously from the title.
- Open with the everyday problem, then what was done, then why it matters.

Paper title: {title}
Venue: {venue}
Year: {year}
Authors: {authors}
Abstract: {abstract}

Return ONLY valid JSON with this exact shape (markdown allowed inside body: **bold**, paragraphs separated by blank lines):
{{
  "title": {{"en": "...", "es": "..."}},
  "summary": {{"en": "one sentence", "es": "una oración"}},
  "body": {{"en": "...", "es": "..."}}
}}"""


def generate_post_with_claude(pub):
    prompt = PROMPT.format(
        title=pub["title"],
        venue=pub.get("venue", ""),
        year=pub.get("year", ""),
        authors=", ".join(pub.get("authors", [])),
        abstract=pub.get("abstract") or "(not available)",
    )
    body = json.dumps({
        "model": ANTHROPIC_MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    try:
        resp = get_json(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
            },
            data=body,
            timeout=120,
        )
        text = "".join(b.get("text", "") for b in resp.get("content", []))
        m = re.search(r"\{.*\}", text, re.S)
        return json.loads(m.group(0)) if m else None
    except Exception as e:
        print(f"  claude generation failed: {e}")
        return None


def generate_post_fallback(pub):
    abstract = pub.get("abstract") or ""
    excerpt = (abstract[:600] + "…") if len(abstract) > 600 else abstract
    venue = pub.get("venue", "")
    year = pub.get("year", "")
    kind_en = "journal article" if pub.get("type") == "journal" else "conference paper" if pub.get("type") == "conference" else "publication"
    kind_es = "artículo de revista" if pub.get("type") == "journal" else "ponencia de congreso" if pub.get("type") == "conference" else "publicación"
    en = (
        f"This is a new {kind_en}"
        + (f", published in *{venue}*" if venue else "")
        + (f" in {year}" if year else "") + ".\n\n"
        + (f"**What it is about.** {excerpt}\n\n" if excerpt else
           "A clear plain-language summary is being prepared.\n\n")
        + "**Why it matters.** It adds to the research on artificial intelligence, machine learning and data science featured across this site. The full paper is available through the DOI below."
    )
    es = (
        f"Esta es una nueva {kind_es}"
        + (f", publicada en *{venue}*" if venue else "")
        + (f" en {year}" if year else "") + ".\n\n"
        + (f"**De qué trata.** {excerpt}\n\n" if excerpt else
           "Se está preparando un resumen claro en lenguaje llano.\n\n")
        + "**Por qué importa.** Se suma a la investigación en inteligencia artificial, machine learning y ciencia de datos presente en este sitio. El artículo completo está disponible a través del DOI de abajo."
    )
    return {
        "title": {"en": f"New paper: {pub['title']}", "es": f"Nuevo artículo: {pub['title']}"},
        "summary": {
            "en": f"New publication in {pub.get('venue') or 'a peer-reviewed venue'} ({pub.get('year', '')}).",
            "es": f"Nueva publicación en {pub.get('venue') or 'un medio arbitrado'} ({pub.get('year', '')}).",
        },
        "body": {"en": en, "es": es},
    }


def build_post(pub):
    generated = generate_post_with_claude(pub) if ANTHROPIC_KEY else None
    if generated is None:
        generated = generate_post_fallback(pub)
    post_id = "post-" + slugify(pub["title"])
    links = []
    if pub.get("doi"):
        links.append({"label": "DOI", "url": f"https://doi.org/{pub['doi']}"})
    return {
        "id": post_id,
        "date": datetime.date.today().isoformat(),
        "type": "paper",
        "doi": pub.get("doi"),
        "auto": True,
        "title": generated["title"],
        "summary": generated["summary"],
        "body": generated["body"],
        "links": links,
    }


# ---------------------------------------------------------------- main

def main():
    pubs = load(PUBS_PATH)
    posts = load(POSTS_PATH)

    known_dois = {(p.get("doi") or "").lower() for p in pubs["items"] if p.get("doi")}
    known_titles = {norm_title(p.get("title")) for p in pubs["items"]}
    post_ids = {p["id"] for p in posts["items"]}

    print(f"Fetching ORCID works for {ORCID_ID}…")
    works = fetch_orcid_works()
    print(f"  {len(works)} works found on ORCID")

    new_count = 0
    for w in works:
        doi = (w.get("doi") or "").lower()
        if doi and doi in known_dois:
            continue
        if not doi and norm_title(w.get("title")) in known_titles:
            continue
        if not w.get("title"):
            continue

        print(f"NEW: {w['title'][:80]}")
        meta = fetch_crossref(w["doi"]) if w.get("doi") else {}
        pub = {
            "id": slugify(w["title"]) + "-" + str(meta.get("year") or w.get("year") or ""),
            "doi": w.get("doi"),
            "title": meta.get("title") or w["title"],
            "authors": meta.get("authors") or ["Jorge Parraga-Alava"],
            "venue": meta.get("venue") or "",
            "type": meta.get("type") if meta.get("type") in ("journal", "conference") else (
                "journal" if w.get("orcid_type") == "journal-article" else "conference"
            ),
            "year": meta.get("year") or w.get("year") or datetime.date.today().year,
            "pages": meta.get("pages"),
            "openAccess": bool(meta.get("openAccess")),
            "abstract": meta.get("abstract") or "",
            "postId": None,
        }

        post = build_post(pub)
        if post["id"] in post_ids:
            post["id"] += "-" + str(pub["year"])
        pub["postId"] = post["id"]
        pub.pop("abstract", None)

        pubs["items"].append(pub)
        posts["items"].append(post)
        known_dois.add(doi)
        known_titles.add(norm_title(pub["title"]))
        post_ids.add(post["id"])
        new_count += 1

    if new_count:
        pubs["items"].sort(key=lambda p: (-int(p.get("year") or 0), p.get("title", "")))
        pubs["updated"] = datetime.date.today().isoformat()
        save(PUBS_PATH, pubs)
        save(POSTS_PATH, posts)
        print(f"Done: {new_count} new publication(s) added, with posts.")
    else:
        print("Done: nothing new.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
