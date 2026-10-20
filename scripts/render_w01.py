"""1주차 애니메이션을 1080p로 렌더링해 05_결과물/01주차/애니메이션 에 저장."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "05_결과물" / "01주차" / "애니메이션"
SCENES = ["CircleRotate", "CircleCount", "Adjacent", "Repeated", "SameThings", "ShortestPath"]


def main(media_dir):
    OUT.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).with_name("w01_anim.py")
    for flags, ext in [(["-r", "1920,1080", "--fps", "30"], "mp4"), (["-r", "1920,1080", "-s"], "png")]:
        subprocess.run([sys.executable, "-m", "manim", *flags, "--media_dir", media_dir, str(src), *SCENES], check=True)
    for sc in SCENES:
        mp4 = next(Path(media_dir, "videos", "w01_anim").rglob(f"{sc}.mp4"))
        png = next(Path(media_dir, "images", "w01_anim").glob(f"{sc}*.png"))
        shutil.copy(mp4, OUT / f"{sc}.mp4")
        shutil.copy(png, OUT / f"{sc}_마지막장면.png")
    print("saved to", OUT)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "scripts" / "_media"))
