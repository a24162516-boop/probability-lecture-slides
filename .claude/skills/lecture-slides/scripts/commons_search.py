"""Wikimedia Commons 이미지 검색 (라이선스, 작성자 포함).

사용: python -I -X utf8 commons_search.py CA묶음.pem 결과.json "검색어1" "검색어2" ...
결과.json 이 이미 있으면 검색 결과를 추가함.
"""
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "LectureSlidesBuilder/1.0 (https://claude.com/claude-code; educational slides) python-urllib"}
FREE = re.compile(r"^(CC|Public domain|PD|No restrictions)", re.I)

cafile, out, queries = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
ctx = ssl.create_default_context(cafile=cafile)


def search(q, n=8):
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
         "gsrsearch": q + " filetype:bitmap", "gsrlimit": n, "prop": "imageinfo",
         "iiprop": "url|extmetadata|size", "iiurlwidth": 1280}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), context=ctx))
    items = []
    for pg in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = pg["imageinfo"][0]
        m = ii.get("extmetadata", {})
        g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
        items.append({"title": pg["title"], "thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"),
                      "license": g("LicenseShortName"), "artist": g("Artist")[:80],
                      "w": ii["width"], "h": ii["height"]})
    return items


res = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
for q in queries:
    res[q] = search(q)
    time.sleep(2)  # Commons 요청 제한(429) 방지
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

for q in queries:
    print("##", q)
    for i, it in enumerate(res[q]):
        mark = "" if FREE.match(it["license"]) else "  [사용 불가 라이선스]"
        print(f"  {i} {it['title'][5:75]} | {it['license']} | {it['w']}x{it['h']}{mark}")
