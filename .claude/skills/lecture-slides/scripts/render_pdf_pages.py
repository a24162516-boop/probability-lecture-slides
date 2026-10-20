"""PDF 페이지를 PNG로 렌더링하고 8쪽씩 모은 시트 이미지 생성.

사용: python -I -X utf8 render_pdf_pages.py 입력.pdf 출력폴더 [--dpi 80] [--pages 3-10]
"""
import argparse
from pathlib import Path

import fitz
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("out")
ap.add_argument("--dpi", type=int, default=80)
ap.add_argument("--pages", help="1부터 시작하는 범위, 예: 3-10")
a = ap.parse_args()

out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(a.pdf)
lo, hi = 1, doc.page_count
if a.pages:
    lo, hi = (int(x) for x in a.pages.split("-"))
files = []
for i in range(lo - 1, hi):
    f = out / f"p{i + 1:03d}.png"
    doc[i].get_pixmap(dpi=a.dpi).save(f)
    files.append(f)
print(f"{doc.page_count} pages in PDF, rendered {lo}-{hi} -> {out}")

for k in range(0, len(files), 8):
    ims = [Image.open(f).convert("RGB") for f in files[k:k + 8]]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * 4, h * 2), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % 4) * w, (i // 4) * h))
    name = out / f"sheet_{k // 8 + 1:02d}.png"
    sheet.save(name)
    print("sheet", name, f"(pages {lo + k}-{lo + k + len(ims) - 1})")
