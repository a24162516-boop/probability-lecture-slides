---
name: lecture-slides
description: 확률과 통계 강의자료(PPT)를 회차 단위로 제작. 교과서 PDF를 읽고, manim 애니메이션과 Wikimedia Commons 비유 사진을 넣은 .pptx를 만들어 05_결과물/N주차/ 에 저장. "N주차 강의자료 만들어줘", "강의 PPT 만들어줘", "다음 회차 슬라이드" 같은 요청에 사용.
---

# 강의자료 제작 스킬

인자로 회차와 주제를 받음 (예: `/lecture-slides 2주차 중복조합`). 없으면 02_강의계획/ 과 교과서 순서에서 다음 회차를 추정하고, 추정한 범위를 사용자에게 한 줄로 알린 뒤 진행.

먼저 프로젝트 루트의 `CLAUDE.md`를 읽고 그 규칙(명사형 종결, 그림 위주, 공학 예시, 요약+연습문제 3문항, 색상)을 그대로 따름.

아래에서 `NN`은 두 자리 회차 번호(예: 02), `SKILL`은 이 파일이 있는 폴더(`.claude/skills/lecture-slides`).

## 0. 환경 준비 (세션마다 한 번)

이 PC는 HTTPS 검사 때문에 pip/urllib의 인증서 검증이 실패함. 검증을 끄지 말고 Windows 인증서 묶음을 사용:

```bash
python -I SKILL/scripts/make_ca_bundle.py scripts/_cache/winca.pem
pip install --cert scripts/_cache/winca.pem manim pymupdf python-pptx   # 이미 있으면 생략
```

네트워크가 필요한 명령은 샌드박스를 끄고 실행. Chrome 헤드리스는 막혀 있으므로 확인용 렌더링은 PowerPoint COM(아래 5단계)을 사용.

## 1. 교과서 읽기

PDF에서 글자 추출이 깨지므로 페이지를 이미지로 렌더링해서 직접 읽음:

```bash
python -I -X utf8 SKILL/scripts/render_pdf_pages.py "01_원본자료/<파일>.pdf" scripts/_cache/pages/<태그> --dpi 80
```

`sheet_*.png`(8쪽씩 모은 이미지)를 Read로 확인하고, 필요한 쪽은 개별 PNG를 더 높은 dpi로 다시 렌더링. 다룰 쪽 범위, 정의, 예제 번호, 「생각 열기」 소재를 메모. 슬라이드에 쓰는 예제마다 근거 쪽수를 기록 (예: "미래엔 p.14 예제 2").

## 2. 슬라이드 구성 설계

1주차 구성(`scripts/build_w01_pptx.py`)을 기본 틀로 사용:

표지 → 학습 흐름(비유 사진 카드 3장) → 개념별로 [비유 사진 + 애니메이션 + 글머리표 2개] 슬라이드와 [공식 상자 + 기호 설명] 슬라이드 → 교과서 예제 → 요약 → 연습문제(공학 소재) → 정답 → 이미지 출처

- 개념의 흐름, 그래프, 도표는 manim 애니메이션으로 만듦
- 정적인 도식(자리 상자, 표 등)은 PPT 도형으로 그려 사용자가 고칠 수 있게 함
- 모든 문장은 명사로 끝냄. 글머리표는 3개 이내

## 3. manim 애니메이션

`scripts/w01_anim.py`를 복사해 `scripts/wNN_anim.py`를 만들고, 맨 위의 공통 도구(색상, `T`, `person`, `label_box`, `tile` 등)는 그대로 두고 장면 클래스만 새로 작성. 장면은 10~25초.

- 흰 배경, 글꼴 `Malgun Gothic`, LaTeX를 쓰지 않음 (`Text`로 수식 표현, ², ³, ⁸ 같은 유니코드 첨자는 사용 가능)
- 화면은 16:9이고, 슬라이드에서는 폭 7.4~7.6인치로 보이므로 글자 크기 26 이상
- 먼저 마지막 장면만 빠르게 확인:
  `python -m manim -ql -s --media_dir scripts/_cache/mprev scripts/wNN_anim.py 장면1 장면2 ...`
  PNG를 Read로 보고 겹침과 잘림을 고친 뒤 본 렌더링
- `scripts/render_w01.py`를 복사해 `SCENES`와 파일명만 바꾼 `render_wNN.py`로 1080p 렌더링 → `05_결과물/N주차/애니메이션/장면.mp4`, `장면_마지막장면.png`
- 영상 중간 프레임도 한 번 확인 (PyAV로 45% 지점 프레임 추출)

## 4. 비유 사진 (Wikimedia Commons)

```bash
python -I -X utf8 SKILL/scripts/commons_search.py scripts/_cache/winca.pem scripts/_cache/cands_NN.json "검색어1" "검색어2" ...
python -I -X utf8 SKILL/scripts/commons_fetch.py scripts/_cache/winca.pem scripts/_cache/cands_NN.json scripts/_cache/dl_NN "이름:검색어:번호" ...
```

`commons_fetch.py`가 만든 `preview.png`를 Read로 보고 고름. 기준:
- CC, CC0, Public domain 라이선스만 사용
- 상표나 로고가 크게 보이는 제품 사진, 내부 분해 사진처럼 비유가 바로 읽히지 않는 사진은 제외
- 고른 사진은 `--save 04_이미지/N주차` 옵션으로 다시 실행해 한글 파일명과 `출처.json`을 저장 (기존 출처.json에 추가됨)

## 5. PPT 생성과 확인

`scripts/build_w01_pptx.py`를 복사해 `build_wNN_pptx.py`를 만들고, `# ---------- 슬라이드` 아래 부분만 새로 작성. 경로 상수(`IMG`, `ANIM`, `OUT`)는 회차에 맞게 수정.

- 영상: `movie(s, "장면", x, y, w)` (클릭하면 재생, 마지막 장면이 미리보기)
- 사진: `photo(s, 경로, x, y, w, h, caption)` (상자 비율에 맞춰 가운데를 잘라 넣음)
- 첨자: `SUB("n")`, `SUP("r")`, 강조: `K("파랑")`, `R("빨강")`
- 줄바꿈이 필요한 곳은 문자열에 `\n`을 넣음 (Python 소스 안에서 이스케이프로 작성. 실제 줄바꿈 문자가 들어가지 않게 Edit 도구로 수정)
- 슬라이드마다 `notes=`에 발표 포인트 작성

생성 후 반드시 PowerPoint로 내보내서 확인:

```bash
python -X utf8 scripts/build_wNN_pptx.py
powershell -ExecutionPolicy Bypass -File SKILL/scripts/export_pptx_png.ps1 "05_결과물/N주차/<파일>.pptx" scripts/_cache/pptshots_NN
python -I SKILL/scripts/contact_sheet.py scripts/_cache/pptshots_NN 4
```

시트 이미지를 Read로 보고 글자 겹침, 단어 중간 줄바꿈, 잘린 그림을 고친 뒤 다시 생성.

## 6. 마무리

- `CLAUDE.md`의 「원본자료 현황」에 새로 읽은 교과서 범위를 추가
- 사용자에게 보고: 결과 파일 경로, 슬라이드 수, 애니메이션 목록(슬라이드 번호와 내용), 사용한 사진과 라이선스, 교과서 근거 범위, 확인이 필요한 점
- `scripts/_cache/`는 임시 폴더라 지워도 됨
