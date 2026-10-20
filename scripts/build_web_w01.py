"""1주차 웹(GitHub Pages)용 미디어를 docs/week01/media 로 복사.

먼저 render_w01.py 로 애니메이션을 렌더링한 뒤 실행.
"""
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "04_이미지" / "01주차"
ANIM = ROOT / "05_결과물" / "01주차" / "애니메이션"
OUT = ROOT / "docs" / "week01" / "media"

SCENES = ["CircleRotate", "CircleCount", "Adjacent", "Repeated", "SameThings", "ShortestPath"]
# 웹에서는 한글 파일명 대신 영문 이름 사용
PHOTOS = {
    "원탁_윈체스터": "roundtable", "번호자물쇠": "lock", "모스전신기": "morsekey", "격자도시_바르셀로나": "gridcity",
    "서버랙": "serverrack", "RGB_LED": "rgbled", "생성_표지토큰": "cover", "생성_원탁회의": "meeting",
    "생성_LED회로": "ledboard", "생성_도어락": "keypad", "생성_전신기사": "telegrapher", "생성_화이트보드": "whiteboard",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for sc in SCENES:
        shutil.copy(ANIM / f"{sc}.mp4", OUT / f"{sc}.mp4")
        im = Image.open(ANIM / f"{sc}_마지막장면.png").convert("RGB")
        im.thumbnail((1280, 720))
        im.save(OUT / f"{sc}.jpg", quality=85)
    shutil.copy(IMG / "생성_인트로영상.mp4", OUT / "intro.mp4")
    shutil.copy(IMG / "생성_인트로영상_포스터.jpg", OUT / "intro.jpg")
    for src, dst in PHOTOS.items():
        im = Image.open(IMG / f"{src}.jpg").convert("RGB")
        im.thumbnail((1600, 1600))
        im.save(OUT / f"{dst}.jpg", quality=85)
    total = sum(p.stat().st_size for p in OUT.iterdir())
    print(f"{len(list(OUT.iterdir()))} files, {total // 1024} KB -> {OUT}")


if __name__ == "__main__":
    main()
