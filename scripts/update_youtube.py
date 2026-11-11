#!/usr/bin/env python3
"""Download the YouTube channel feed and save it as data/youtube.json.

The site reads this file first, so visitors do not depend on public CORS proxies.
If the download fails, the existing file is left untouched. Run from the repo root.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NS = {"a": "http://www.w3.org/2005/Atom", "m": "http://search.yahoo.com/mrss/", "yt": "http://www.youtube.com/xml/schemas/2015"}


def parse(xml_text, limit=15):
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", NS)[:limit]:
        title = (e.findtext("a:title", default="", namespaces=NS) or "").strip()
        link_el = e.find("a:link[@rel='alternate']", NS)
        link = link_el.get("href") if link_el is not None else ""
        vid = (e.findtext("yt:videoId", default="", namespaces=NS) or "").strip()
        thumb_el = e.find("m:group/m:thumbnail", NS)
        thumb = thumb_el.get("url") if thumb_el is not None else (f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg" if vid else "")
        if title and link:
            out.append({"title": title, "link": link, "thumb": thumb})
    return out


def main():
    profile = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
    channel = (profile.get("youtube") or {}).get("channelId")
    if not channel:
        print("No YouTube channelId in profile.json; nothing to do.")
        return 0
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            items = parse(r.read().decode("utf-8"))
    except Exception as exc:  # network or parse error: keep the previous file
        print(f"Could not update YouTube feed: {exc}", file=sys.stderr)
        return 0
    if not items:
        print("Feed returned no videos; keeping the previous file.", file=sys.stderr)
        return 0
    out = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "items": items}
    (ROOT / "data" / "youtube.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"data/youtube.json: {len(items)} videos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
