# smartcity — KOSIS 통계 대시보드

> 국가통계포털(KOSIS) 데이터를 불러와 지표를 비교하는 학습용 대시보드입니다.

![대표 이미지](public/og-image.png)

스마트시티 수업(01: Python·GitHub·VS Code·Cloudflare 환경설정) 과제 저장소입니다.
Cloudflare Pages로 배포하는 정적 웹 앱과, 분석에 사용하는 Python 환경을 함께 관리합니다.

## 구성

```
public/
├── index.html        구조 및 레이아웃
├── styles.css        테마 및 스타일 (라이트/다크 자동 전환)
├── app.js            동작 로직 — 데이터 로드, SVG 차트, 표 렌더링
├── og-image.png      대표 이미지
└── data/
    └── dashboard.json  지표 시계열 데이터
```

## 개발 환경

- Python 가상환경: `.venv` (Python 3.12.13)
  ```bash
  source .venv/bin/activate
  ```
- Jupyter 커널: `Python 3.12 (smartcity)`
- 주요 패키지: numpy, pandas, geopandas, scikit-learn, matplotlib(+koreanize_matplotlib),
  plotly, folium, pydeck, mapclassify, nbformat, ipywidgets, openpyxl, python-dotenv

## 배포

Cloudflare Pages에 정적 파일을 그대로 올립니다. Node 22 이상이 필요합니다.

```bash
# 로컬 미리보기
npm run dev

# 배포
npm run deploy
```

## 데이터 출처

- 국가통계포털 KOSIS — https://kosis.kr
- KOSIS MCP 시범서비스 — `https://kosismcp2026.vercel.app/api/mcp`

> ⚠️ 본 페이지는 KOSIS 기반 시범서비스 자료를 활용합니다.
> 통계 분석·해석 결과는 국가데이터처의 공식 입장이 아닌 참고용입니다.
