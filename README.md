# 확률과 통계 강의자료 제작

대학교 1학년 공대생 대상 「확률과 통계」 강의 PPT를 만드는 스크립트 모음.
manim 애니메이션과 Wikimedia Commons 비유 사진을 넣은 .pptx를 회차별로 생성.

**강의 사이트**: https://a24162516-boop.github.io/probability-lecture-slides/ (슬라이드 · 퀴즈 · 플레이그라운드)

## 폴더
| 폴더 | 내용 |
|---|---|
| `CLAUDE.md` | 강의 정보, 스타일 규칙, 제작 방식 |
| `.claude/skills/lecture-slides/` | 회차별 제작 절차 스킬과 보조 스크립트 |
| `scripts/` | 회차별 애니메이션(`wNN_anim.py`), 렌더링(`render_wNN.py`), PPT 생성(`build_wNN_pptx.py`) |
| `docs/` | GitHub Pages 사이트 (회차별 슬라이드, 퀴즈, 플레이그라운드) |
| `04_이미지/` | 비유 사진 (자유 라이선스, 출처는 `출처.json`) |

교과서 PDF(`01_원본자료/`)와 생성 결과물(`05_결과물/`)은 저장소에 포함하지 않음.

## 1주차 다시 만들기
```bash
pip install manim pymupdf python-pptx
python scripts/render_w01.py        # 애니메이션 렌더링
python scripts/build_w01_pptx.py    # PPT 생성 → 05_결과물/01주차/
python scripts/build_web_w01.py     # 웹용 미디어 → docs/week01/media/
```
