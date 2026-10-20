"""commons_search.py 결과에서 고른 이미지를 내려받기.

미리보기: python -I -X utf8 commons_fetch.py CA.pem 후보.json 내려받을폴더 "이름:검색어:번호" ...
  → 내려받을폴더/이름.jpg 와 preview.png 생성
저장:     위 명령에 --save 04_이미지/N주차 추가
  → 04_이미지/N주차/이름.jpg 저장, 출처.json 에 제목·작성자·라이선스·주소 추가
"이름"은 슬라이드에서 쓸 한글 파일명 (예: 원탁_윈체스터).
"""
import argparse
import json
import ssl
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

UA = {"User-Agent": "LectureSlidesBuilder/1.0 (https://claude.com/claude-code; educational slides) python-urllib"}

ap = argparse.ArgumentParser()
ap.add_argument("cafile")
ap.add_argument("cands")
ap.add_argument("dl")
ap.add_argument("picks", nargs="+", help="이름:검색어:번호")
ap.add_argument("--save", help="최종 저장 폴더 (예: 04_이미지/02주차)")
a = ap.parse_args()

ctx = ssl.create_default_context(cafile=a.cafile)
cands = json.loads(Path(a.cands).read_text(encoding="utf-8"))
dl = Path(a.dl)
dl.mkdir(parents=True, exist_ok=True)

chosen = []
for spec in a.picks:
    name, q, idx = spec.rsplit(":", 2)
    it = cands[q][int(idx)]
    f = dl / f"{name}.jpg"
    if not f.exists():
        data = urllib.request.urlopen(urllib.request.Request(it["thumb"], headers=UA), context=ctx).read()
        f.write_bytes(data)
        time.sleep(1)
    chosen.append((name, f, it))

if a.save:
    dest = Path(a.save)
    dest.mkdir(parents=True, exist_ok=True)
    cred_path = dest / "출처.json"
    credits = json.loads(cred_path.read_text(encoding="utf-8")) if cred_path.exists() else []
    credits = [c for c in credits if c["file"] not in {f"{n}.jpg" for n, _, _ in chosen}]
    for name, f, it in chosen:
        Image.open(f).convert("RGB").save(dest / f"{name}.jpg", quality=90)
        credits.append({"file": f"{name}.jpg", "title": it["title"], "author": it["artist"],
                        "license": it["license"], "source": it["page"]})
        print("saved", dest / f"{name}.jpg", "|", it["license"], "|", it["artist"][:50])
    cred_path.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
else:
    cols = 4
    rows = (len(chosen) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 300, rows * 260), "white")
    d = ImageDraw.Draw(sheet)
    for k, (name, f, it) in enumerate(chosen):
        im = Image.open(f).convert("RGB")
        im.thumbnail((290, 230))
        x, y = (k % cols) * 300, (k // cols) * 260
        sheet.paste(im, (x + 5, y + 5))
        d.text((x + 5, y + 240), f"{k}  {it['license']}", fill="black")
    sheet.save(dl / "preview.png")
    for k, (name, _, it) in enumerate(chosen):
        print(k, name, "|", it["title"][5:70], "|", it["license"])
    print("preview:", dl / "preview.png")
