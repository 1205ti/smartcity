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

- `data/raw/` — 내려받은 원본. 건드리지 않는다.
- `data/processed/` — 전처리 결과
- `outputs/figures/` — 저장한 그림·HTML

`data/raw/`는 용량 때문에 git에서 제외한다. 내려받는 방법은 각 노트북 첫 셀에 적는다.
