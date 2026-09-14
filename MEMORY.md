# 프로젝트 상태

현재 진행 상황과 결정 사항. 규칙은 `CLAUDE.md`, 시간순 기록은 `logs/WORKLOG.md`.
최종 갱신: 2026-09-14 (서울 데이터 3종 확보, 폴더 구조 정리)

## 지금 하는 일

노션 강의자료 02~08의 실습을 노트북으로 미리 구현한다.

**02~08 노트북 7개 전부 구현·실행 완료** (2026-09-14). 오류 0.

| 강의 | 노트북 | 코드셀 | 비고 |
| --- | --- | --- | --- |
| 02 Python 기초 | `02_python_basics.ipynb` | 15 | 소수 판별·과일가게 과제 포함 |
| 03 NumPy | `03_numpy.ipynb` | 12 | 미세먼지 배열 과제 포함 |
| 04 Pandas | `04_pandas.ipynb` | 18 | 평균 속도 과제 포함 |
| 05 API | `05_api.ipynb` | 15 | 키 없이도 완주 |
| 06 Matplotlib | `06_matplotlib.ipynb` | 12 | PNG 11개 |
| 07 Plotly | `07_plotly.ipynb` | 11 | HTML 11개, 전세 환산 과제 포함 |
| 08 Folium | `08_folium.ipynb` | 10 | HTML 2개, 조인 진단 |
| 13 생활인구 | `13_living_population.ipynb` | 10 | 노션 자료 없이 선구현 |

검증은 `scripts/run_notebooks.py`로 nbclient 실행. 산출물은 `outputs/`(git 제외).

## 사용자가 해야 할 일

제가 대신 할 수 없는 것만 모았다.

### 1. ~~서울 열린데이터광장 API 키~~ — 완료 (2026-09-14)

발급받아 `.env`에 넣었고 두 데이터셋 모두 정상 응답(`INFO-000`) 확인.
**인증키는 계정당 하나**로 모든 데이터셋에 쓴다. 데이터셋별 신청이 아니다.

### 2. 강사에게 확인할 것

- `world-countries.geojson` / `world-centroids.geojson` 원본 출처. 08 강의자료에 URL이 없다.
  지금은 folium 공식 저장소 예제본(177개국, id=ISO-3)으로 대체했고 구조는 강의자료와 일치한다.
  중심점은 `representative_point()`로 직접 만들었다.
- `data/nycflights13.csv` 출처 URL. 실습 저장소에는 있으나 강의자료에 출처가 없다.

### 3. 나중에 다시 받을 강의자료

09-2, 12, 13-1~3, 13, 14는 본문이 비어 있고 09-1은 완결 여부가 불확실하다.
강의가 진행되면 알려달라. `scripts/fetch_notion.py`로 다시 받는다.
페이지 ID는 `docs/course/_나중에_다시_받을_자료.md`에 있다.

## 결정한 것

- **실습 범위는 02~08**. 09-1은 완결 자료가 아닐 수 있어 보류(2026-09-14 사용자 판단).
- **가상환경은 프로젝트마다**. `~/.venv`에 만들었다가 `smartcity/.venv`로 옮겼다.
- **배포는 GitHub Actions**. Direct Upload로 만든 Pages 프로젝트는 나중에 Git 연결로 바꿀 수 없어서,
  기존 주소를 지키려면 이 길뿐이었다. 교재 5.1(대시보드 Git 연결)로 갔으면 토큰이 필요 없었다.
- **Node는 프로젝트 한정으로 22를 쓴다**. 전역 PATH를 바꾸면 Claude Code가 쓰는 conda node가 밀린다.

## 확보한 데이터

### `data/raw/` — 원본 (git 제외, 1.1GB)

| 파일 | 크기 | 출처 | 쓰는 곳 |
| --- | --- | --- | --- |
| `SPOP_2025_ADM.csv` | 853MB | 서울 열린데이터광장 (2025년 전체) | 13 |
| `bnd_all_00_2025_2Q.zip` | 181MB | 통계청 행정구역 경계 | 13 |
| `seoul_rent_2026.csv` | 57MB | **API로 직접 수집** (416,037건, 8.7분) | 05, 07 |
| `nycflights13.csv` | 19MB | 실습 저장소 | 04 |
| `world-countries.geojson` | 247KB | folium 공식 저장소 예제 | 08 |
| `world-centroids.geojson` | 28KB | `representative_point()`로 생성 | 08 |

### `data/processed/` — 분석용 (커밋)

| 파일 | 내용 |
| --- | --- |
| `living_pop_daily.csv` | 일자 x 행정동 (155,490행) |
| `living_pop_hourly.csv` | 시간대 x 행정동 (10,224행) |
| `living_pop_age_gender.csv` | 행정동 x 성·연령 (426행) |
| `seoul_dong_simplified.geojson` | 행정동 경계 426개, 0.9MB |
| `dong_crosswalk.csv` | 통계청 ↔ 서울 행정동 코드 대응표 |
| `jeonse_mean.csv` | 자치구·법정동·용도별 평균 전세가 (1,194행) |

URL에서 직접 읽는 것: `drinks.csv`, `ufo.csv` (06), `px.data.gapminder()` (07·08)

### 행정동 코드 주의

통계청 경계와 서울 생활인구의 코드 체계가 다르다. 426개 중 32개만 우연히 일치한다.
`dong_crosswalk.csv`를 쓰거나, 이미 코드가 붙어 있는 `seoul_dong_simplified.geojson`을 쓴다.
새 데이터를 붙일 때 조인 전후 행 수를 반드시 확인할 것.

## 열려 있는 문제

- **07 강의자료 본문 누락** — 학습목표에 서울 전월세 전처리가 있으나 본문은 Gapminder만 다룬다.
  실제 코드는 실습 저장소 `03_2_plotly.ipynb`에만 있다. 과제 2를 하려면 노트북을 함께 봐야 한다.
- **08 학습목표 누락** — `px.choropleth` 언급이 있으나 본문에는 Folium Choropleth만 있다.
- **05 건수 불일치** — 본문은 362,731건인데 이후 절의 출력 index는 392,074까지 간다. 재실행 시점 차이로 보인다.

## 배포

- https://smartcity-apa.pages.dev — push하면 자동 배포
- 저장소 시크릿: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` (둘 다 등록됨)
- Cloudflare 계정: taecin.kim@snu.ac.kr
- `workers.dev` 서브도메인 미등록 — 정적 페이지만 쓰면 불필요
