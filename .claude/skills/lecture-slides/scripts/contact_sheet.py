"""폴더 안 PNG를 N장씩 2열 시트로 모으기 (Read로 한 번에 확인하기 위함).

사용: python -I contact_sheet.py 폴더 [장수=4] [패턴=slide*.png]
"""
import sys
from pathlib import Path

from PIL import Image

folder = Path(sys.argv[1])
per = int(sys.argv[2]) if len(sys.argv) > 2 else 4
pattern = sys.argv[3] if len(sys.argv) > 3 else "slide*.png"
files = sorted(folder.glob(pattern))
for k in range(0, len(files), per):
    ims = [Image.open(f).convert("RGB") for f in files[k:k + per]]
    w, h = ims[0].size
    rows = (per + 1) // 2
    sheet = Image.new("RGB", (w * 2 + 10, h * rows + 10 * (rows - 1)), "gray")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % 2) * (w + 10), (i // 2) * (h + 10)))
    out = folder / f"_sheet{k // per + 1:02d}.png"
    sheet.save(out)
    print(out, f"({files[k].name} ~ {files[min(k + per, len(files)) - 1].name})")
