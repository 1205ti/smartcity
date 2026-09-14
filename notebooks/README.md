# 실습 노트북

노션 강의자료(`docs/course/`)의 실습을 강의별로 따라 구현한다.

| 노트북 | 강의 |
| --- | --- |
| `02_python_basics.ipynb` | 02 : Python 기초 |
| `03_numpy.ipynb` | 03 : NumPy |
| `04_pandas.ipynb` | 04 : Pandas |
| `05_api.ipynb` | 05 : API |
| `06_matplotlib.ipynb` | 06 : Matplotlib |
| `07_plotly.ipynb` | 07 : Plotly |
| `08_folium.ipynb` | 08 : Folium |

## 실행 방법

커널은 `Python 3.12 (smartcity)`를 선택한다. 또는 터미널에서:

```bash
source .venv/bin/activate
jupyter lab
```

## 폴더 규칙

| 폴더 | 용도 | git |
| --- | --- | --- |
| `data/raw/` | 내려받은 원본. 읽기만 한다 | 제외 |
| `data/interim/` | 전처리 중간 산출물 | 제외 |
| `data/processed/` | 분석에 바로 쓰는 결과 | 커밋 |
| `outputs/figures/` | 그림 (PNG) | 커밋 |
| `outputs/html/` | 인터랙티브 결과 | 커밋 |
| `deploy/site/` | 웹에 공개되는 것만 | 커밋 |

원본을 덮어쓰면 되돌릴 수 없다. `raw`는 읽고, 쓰는 것은 `interim`·`processed`에 한다.
내려받는 방법은 각 노트북 첫 셀에 적는다.
