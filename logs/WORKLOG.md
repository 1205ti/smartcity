# 작업 로그

스마트도시데이터분석 수업 환경 구축 및 과제 저장소 작업 기록.
새로 추가되는 기록은 맨 위에 쌓는다.

---

## 2026-09-14 — 강의자료 수집

노션 강의 홈(`2155235c90d080bda32fc6d654786ce2`) 아래 하위 페이지 16개를 수집해(이후 8개는 보류)
`docs/course/`에 마크다운으로 저장.

수집 방법은 `scripts/fetch_notion.py`. 노션 공개 페이지의 `api/v3/loadPageChunk`
엔드포인트를 직접 호출한다. 웹페이지를 그냥 긁으면 SPA 껍데기만 나와서 본문을 못 얻는다.
커서를 따라가며 청크를 이어 받아야 긴 페이지가 잘리지 않는다.

### 보관 중인 자료 (8개)

| 파일 | 분량 |
| --- | --- |
| `01_환경설정_매뉴얼.md` | 32KB |
| `02_Python_기초.md` | 14KB |
| `03_NumPy.md` | 9KB |
| `04_Pandas.md` | 25KB |
| `05_API.md` | 26KB |
| `06_Matplotlib.md` | 22KB |
| `07_Plotly.md` | 13KB |
| `08_Folium.md` | 14KB |

### 수집 대상에서 뺀 자료 (8개)

09-2 지오코딩, 12 도시계획 지표, 13-1~13-3 생활인구, 13 머신러닝 기초, 14 머신러닝 심화는
제목만 있고 본문 블록이 0개다. 09-1 공간데이터와 좌표계는 본문이 40KB 있지만 완결 자료가
아닐 수 있어 함께 보류했다. 페이지 ID는 `docs/course/_나중에_다시_받을_자료.md`에 적어 뒀다.

따라서 실습 구현 범위는 **02~08 일곱 개 강의**다.

### 실습 코드 저장소

`https://github.com/jslee-gses/code` → `~/Documents/Lab/gses_code`에 클론.
lecture01~lecture06 폴더에 `.ipynb` 실습 파일과 `data/` 포함.

---

## 2026-09-14 — 자동 배포 구축

`main`에 push하면 GitHub Actions가 Cloudflare Pages로 배포한다. 워크플로는
`.github/workflows/deploy.yml`.

### 막혔던 지점과 해결

**Node 버전** — 기본 `node`가 conda 환경의 v20이라 wrangler(Node 22+ 요구)가 거부했다.
전역 PATH를 바꾸면 Claude Code 자체가 conda node로 돌아가고 있어 위험하므로,
프로젝트에서만 `/opt/homebrew/opt/node@22/bin`을 앞에 붙여 쓴다.

**Pages 프로젝트 생성** — 계정에 `workers.dev` 서브도메인이 없어 신규 Workers 통합
경로가 막혔다. `--force`로 기존 Pages 방식으로 생성했다. 이 플래그는 최초 1회만 필요하다.

**저장소 이름 충돌** — `smartcity`가 선점돼 있어 배포 주소는 `smartcity-apa.pages.dev`가 됐다.

**`workflow` 스코프** — `.github/workflows/` 파일은 `workflow` 스코프 없이 push할 수 없다.
`gh auth refresh -s workflow`로 추가. 이때 `gh`는 TTY가 없으면 'Press Enter' 프롬프트에서
멈추므로 `pty`로 띄워야 한다(`scripts/` 참고). wrangler는 브라우저를 자동으로 열지만
`gh`는 Enter를 먼저 기다린다는 차이가 있다.

**빈 시크릿** — `CLOUDFLARE_API_TOKEN`이 값 없이 등록돼 배포가 두 번 실패했다.
워크플로에 값 대신 길이만 출력하는 단계를 임시로 넣어 원인을 특정했다(길이 0).
GitHub 웹에서 다시 넣어 해결. 진단 단계는 제거했다.

### 최종 상태

- 배포 주소: https://smartcity-apa.pages.dev
- 저장소 시크릿: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
- Cloudflare 계정: taecin.kim@snu.ac.kr (OAuth 토큰은 macOS 키체인)
- `workers.dev` 서브도메인: 미등록. 정적 페이지만 쓰면 불필요하다.

---

## 2026-09-14 — KOSIS 대시보드

관악구 수문 관련 통계 4개 표, 12개 시계열을 수집해 대시보드로 만들었다.

### 데이터 수집 경로

KOSIS MCP 서버(`https://kosismcp2026.vercel.app/api/mcp`)에 HTTP로 직접 붙었다.
`scripts/mcp_client.py`가 Streamable HTTP로 initialize → tools/call을 수행한다.
세션 재시작 없이 MCP 도구를 쓸 수 있다.

수집 스크립트는 `scripts/fetch_data.py`, 변환은 `scripts/build_dataset.py`,
원본 응답은 `scripts/gwanak_data.json`.

### 사용한 통계표

| 그룹 | 통계표 | ID | 구간 |
| --- | --- | --- | --- |
| 강우 | 강수량 및 강수일수 | `DT_201004_O010005` | 2010–2024 |
| 토지피복 | 토지현황(지목별) | `DT_201004_O010002` | 2010–2024 |
| 하수 인프라 | 하수관거 | `DT_201004_O070015` | 2009–2023 |
| 침수 피해 | 자연재해 발생 및 피해 현황 | `DT_201004_O160036` | 2005–2022 |

관악구 지역코드는 세 표 모두 `objL1=001021`. 강수량 표는 지역 분류가 없어 서울 관측값이다.

### 데이터를 다루며 지킨 원칙

- 불투수면 비율처럼 원표에 없는 합성 지표는 계산하지 않았다. 지목별 면적을 원자료 그대로 싣는다.
- 침수 피해는 수록 연도가 불연속(2005·2007·2008·2010·2011·2015·2022)이라 막대로 그린다.
  꺾은선으로 이으면 원자료에 없는 추세가 생긴다.
- 증감 색상은 피해 지표에만 적용한다. 강수량·면적은 좋고 나쁨이 없다.

### 걸렸던 것

`kosis_get_data`의 `newEstPrdCnt`는 문자열이 아니라 숫자여야 한다. 문자열로 넘기면
`invalid_type` 오류가 난다.

---

## 2026-09-14 — 개발 환경

- Python 3.12.13 (Homebrew `python@3.12`). 시스템 python은 3.9.6이라 최신 pandas·geopandas가 안 맞는다.
- 가상환경은 프로젝트 폴더마다 만든다. `~/.venv`에 만들었다가 `smartcity/.venv`로 옮겼다.
- Jupyter 커널 이름: `Python 3.12 (smartcity)`
- VS Code + Python·Jupyter·Claude Code 확장 설치
- git 2.50.1, gh 2.100.0, Node 22.17.0(Homebrew)
