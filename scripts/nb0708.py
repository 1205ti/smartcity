import sys; sys.path.insert(0, "scripts")
from build_notebooks import build

# ── 07 Plotly ─────────────────────────────────────────────────────────────
c = []
c.append(("md", """# 07 : Plotly

강의자료: `docs/course/07_Plotly.md`

Plotly Express로 인터랙티브 그래프를 만들고 HTML로 저장한다.
Matplotlib과 달리 마우스를 올리면 값이 보이고, 확대·필터가 된다.

## 데이터

- `px.data.gapminder()` — Plotly 내장. 1952~2007년 142개국 기대수명·인구·1인당 GDP
- `data/raw/seoul_rent_2026.csv` — 과제 2용 (05에서 쓴 파일)

저장 위치는 `outputs/html/`.

> 강의자료 학습목표에 서울 전월세 전처리가 있으나 본문 코드는 Gapminder만 다룬다.
> 전처리 부분은 실습 저장소 `03_2_plotly.ipynb`를 참고해 과제 2에 구현했다."""))

c.append(("code", '''import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

HTML = Path("outputs/html")
HTML.mkdir(parents=True, exist_ok=True)

gap = px.data.gapminder()
print(gap.shape, list(gap.columns))
gap.head()'''))

c.append(("md", "## 1. 산점도 — 기본에서 디자인까지"))
c.append(("code", '''g07 = gap.query("year == 2007")
print("2007년 국가 수:", len(g07))

fig = px.scatter(g07, x="gdpPercap", y="lifeExp")
fig.write_html(HTML / "1_1.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("code", '''fig = px.scatter(
    g07, x="gdpPercap", y="lifeExp",
    size="pop", color="continent", hover_name="country",
    log_x=True,                 # GDP는 편차가 커서 로그 축이 읽기 쉽다
    size_max=55,
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={"gdpPercap": "1인당 GDP (달러, 로그)", "lifeExp": "기대수명 (년)",
            "continent": "대륙", "pop": "인구"},
)
fig.update_layout(title="1인당 GDP와 기대수명 (2007)",
                  template="plotly_white", height=520)
fig.update_xaxes(showgrid=True, gridcolor="#eee")
fig.update_yaxes(showgrid=True, gridcolor="#eee")
fig.write_html(HTML / "1_2.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", "## 2. Facet — 연도별로 쪼개 보기"))
c.append(("code", '''fig = px.scatter(
    gap.query("year >= 1982"), x="gdpPercap", y="lifeExp",
    size="pop", color="continent", hover_name="country",
    log_x=True, size_max=35,
    facet_col="year", facet_col_wrap=3,
    labels={"gdpPercap": "1인당 GDP", "lifeExp": "기대수명"},
)
fig.update_xaxes(matches="x")   # 패널 간 축을 맞춰야 비교가 된다
fig.update_yaxes(matches="y")
fig.update_layout(height=620, template="plotly_white")
fig.write_html(HTML / "1_3.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", "## 3. 애니메이션 — 시간 흐름"))
c.append(("code", '''fig = px.scatter(
    gap, x="gdpPercap", y="lifeExp",
    size="pop", color="continent", hover_name="country",
    animation_frame="year", animation_group="country",
    log_x=True, size_max=55,
    range_x=[200, 100000], range_y=[25, 90],   # 축을 고정해야 프레임이 튀지 않는다
    labels={"gdpPercap": "1인당 GDP", "lifeExp": "기대수명"},
)
fig.update_layout(title="1952-2007 변화", template="plotly_white", height=560)
fig.write_html(HTML / "1_4.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", "## 4. Bar"))
c.append(("code", '''asia07 = gap.query("year == 2007 and continent == 'Asia'").nlargest(15, "pop")

fig = px.bar(asia07.sort_values("pop"), x="pop", y="country",
             orientation="h", color="lifeExp",
             color_continuous_scale="Blues",
             labels={"pop": "인구", "country": "", "lifeExp": "기대수명"})
fig.update_layout(title="아시아 인구 상위 15개국 (2007)",
                  template="plotly_white", height=520)
fig.write_html(HTML / "2_3.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", "## 5. Histogram · Box"))
c.append(("code", '''fig = px.histogram(g07, x="lifeExp", nbins=30,
                   histnorm="probability density",
                   labels={"lifeExp": "기대수명"})
fig.update_layout(title="기대수명 분포 (2007)", template="plotly_white", height=380)
fig.write_html(HTML / "3_2.html", include_plotlyjs="cdn")
fig.show()

fig = px.box(g07, x="continent", y="lifeExp", color="continent",
             labels={"continent": "대륙", "lifeExp": "기대수명"})
fig.update_layout(title="대륙별 기대수명 (2007)", template="plotly_white",
                  height=420, showlegend=False)
fig.write_html(HTML / "4_2.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", "## 6. Line · Area — 추세"))
c.append(("code", '''asia = gap[gap["continent"] == "Asia"]
top6 = asia.query("year == 2007").nlargest(6, "pop")["country"]

fig = px.line(asia[asia["country"].isin(top6)],
              x="year", y="lifeExp", color="country", markers=True,
              labels={"year": "연도", "lifeExp": "기대수명", "country": "국가"})
fig.update_layout(title="아시아 주요국 기대수명 추이", template="plotly_white", height=440)
fig.write_html(HTML / "5_1.html", include_plotlyjs="cdn")
fig.show()

fig = px.area(asia.groupby(["year", "country"], as_index=False)["pop"].sum(),
              x="year", y="pop", color="country",
              labels={"year": "연도", "pop": "인구"})
fig.update_layout(title="아시아 인구 누적", template="plotly_white",
                  height=440, showlegend=False)
fig.write_html(HTML / "6_1.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", """## 과제 2 — 지난 5년간 서울 전세 가격 변화

### 데이터를 어디서 가져왔나

강의자료 05는 OpenAPI로 수집하지만, **API는 최근 3년치만 준다**(서울 열린데이터광장
공식 안내). 5년을 보려면 같은 데이터셋의 **연도별 ZIP 파일**을 받아야 한다.
2011년부터 올라와 있다.

`scripts/fetch_seoul_rent_files.py`가 2021~2025년 5개 연도를 받아 합친다.
323만 건을 34초에 받는다. API로 같은 양을 받으면 약 4시간 걸린다.

받으면서 걸린 것 둘:
- ZIP 내부 **파일명이 CP949**라 `unzip`이 `Illegal byte sequence`로 죽는다. Python `zipfile`로 읽는다.
- **인코딩이 연도마다 다르다.** 2022년까지 CP949, 2023년부터 UTF-8(BOM). BOM을 보고 판별한다.
- 열 이름이 한글(`자치구명`)이라 API(`CGG_NM`)와 다르다. API 쪽으로 통일했다."""))

c.append(("code", '''rent5 = pd.read_parquet("data/interim/seoul_rent_2021_2025.parquet")
print(f"{len(rent5):,}건  {rent5.RCPT_YR.min()}~{rent5.RCPT_YR.max()} 접수분")

# 접수연도 파일에는 과거 계약이 뒤늦게 신고된 건이 섞여 있다(2021년 이전 1.85%).
# 시계열을 보려면 접수연도가 아니라 계약일로 잘라야 한다.
rent5["ym"] = rent5["CTRT_DAY"].astype("string").str[:6]
rent5 = rent5[rent5["ym"].between("202101", "202512")].copy()
rent5["date"] = pd.to_datetime(rent5["ym"] + "01", format="%Y%m%d")
print(f"계약일 기준 2021-2025: {len(rent5):,}건")'''))

c.append(("md", """### 건수를 시계열로 읽으면 안 된다

먼저 확인할 것이 있다. 연도별 거래 건수가 이렇게 변한다."""))

c.append(("code", '''monthly_n = rent5.groupby("date").size().reset_index(name="건수")

fig = px.line(monthly_n, x="date", y="건수", markers=True,
              labels={"date": "계약월", "건수": "신고 건수"})
fig.add_vline(x="2025-06-01", line_dash="dash", line_color="#c0392b")
fig.add_annotation(x="2025-06-01", y=monthly_n["건수"].max(),
                   text="2025.6 계도기간 종료", showarrow=True, arrowhead=2,
                   ax=-70, ay=-20, font=dict(color="#c0392b"))
fig.update_layout(title="월별 전월세 신고 건수 — 시장 규모가 아니라 신고율의 변화",
                  template="plotly_white", height=420)
fig.write_html(HTML / "7_0.html", include_plotlyjs="cdn")
fig.show()

print(rent5.groupby(rent5["ym"].str[:4]).size().to_string())'''))

c.append(("md", """2021년 46만 건에서 2025년 102만 건으로 두 배가 넘게 늘었다.
**시장이 두 배가 된 것이 아니다.** 2021년 6월 시작된 전월세신고제의 계도기간이
2025년 5월 말 끝나면서 신고율이 올라간 것이다. 위 그래프에서 2025년 6월에
계단처럼 뛰는 지점이 그 경계다.

따라서 **건수는 연도 간 비교에 쓸 수 없다.** 가격만 본다. 가격도 신고 대상이
넓어지면서 표본 구성이 달라졌을 수 있으므로, 평균보다 극단값에 덜 흔들리는
중앙값을 쓴다."""))

c.append(("md", "### 가격 지표 정의"))

c.append(("code", '''# 전월세 전환율 5%로 월세를 보증금으로 환산해 같은 잣대로 놓는다.
# 실제 전환율은 시기·지역·주택유형마다 다르므로 이 값은 비교용 공통 잣대일 뿐
# 실거래 전세가가 아니다.
CONVERSION_RATE = 0.05
rent5["JEONSE_CONVERTED"] = rent5["GRFE"] + (rent5["RTFE"] * 12 / CONVERSION_RATE)

rent5 = rent5[rent5["RENT_AREA"] > 0]
rent5["JEONSE_PER_M2"] = rent5["JEONSE_CONVERTED"] / rent5["RENT_AREA"]

# 상하위 1%는 잘라 낸다. 극단값 몇 건이 중앙값까지 흔들지는 않지만
# 축이 늘어나 그래프가 읽히지 않는다.
lo, hi = rent5["JEONSE_PER_M2"].quantile([0.01, 0.99])
rent5 = rent5[rent5["JEONSE_PER_M2"].between(lo, hi)]
print(f"극단값 제외 후 {len(rent5):,}건")
print(rent5["JEONSE_PER_M2"].describe().round(1).to_string())'''))

c.append(("md", "### 1. 서울 전체 ㎡당 환산전세가 추이"))

c.append(("code", '''apt = rent5[rent5["BLDG_USG"] == "아파트"]

trend = (apt.groupby("date")["JEONSE_PER_M2"]
         .agg(중앙값="median", 평균="mean").round(1).reset_index())

fig = px.line(trend.melt(id_vars="date", var_name="지표", value_name="값"),
              x="date", y="값", color="지표", markers=True,
              labels={"date": "계약월", "값": "㎡당 환산전세가 (만원)"})
fig.update_layout(title="서울 아파트 ㎡당 환산전세가 (2021-2025)",
                  template="plotly_white", height=440)
fig.write_html(HTML / "7_1.html", include_plotlyjs="cdn")
fig.show()

first, last = trend.iloc[0], trend.iloc[-1]
print(f"{first['date']:%Y-%m} {first['중앙값']:.1f} → "
      f"{last['date']:%Y-%m} {last['중앙값']:.1f} 만원/㎡ "
      f"({(last['중앙값']/first['중앙값']-1)*100:+.1f}%)")
print(f"최고 {trend['중앙값'].max():.1f} ({trend.loc[trend['중앙값'].idxmax(),'date']:%Y-%m})")
print(f"최저 {trend['중앙값'].min():.1f} ({trend.loc[trend['중앙값'].idxmin(),'date']:%Y-%m})")'''))

c.append(("md", "### 2. 자치구별로 갈리는가"))

c.append(("code", '''gu_trend = (apt.groupby(["date", "CGG_NM"])["JEONSE_PER_M2"]
            .median().round(1).reset_index())

# 25개를 다 그리면 선이 엉켜 못 읽는다. 최근 수준 상위·하위 3개씩만 본다
recent = gu_trend[gu_trend["date"] >= "2025-07-01"].groupby("CGG_NM")["JEONSE_PER_M2"].median()
pick = list(recent.nlargest(3).index) + list(recent.nsmallest(3).index)

fig = px.line(gu_trend[gu_trend["CGG_NM"].isin(pick)],
              x="date", y="JEONSE_PER_M2", color="CGG_NM", markers=True,
              labels={"date": "계약월", "JEONSE_PER_M2": "㎡당 환산전세가 (만원)",
                      "CGG_NM": "자치구"})
fig.update_layout(title="자치구별 아파트 ㎡당 환산전세가 — 상위·하위 3개구",
                  template="plotly_white", height=460)
fig.write_html(HTML / "7_2.html", include_plotlyjs="cdn")
fig.show()

# 5년 사이 격차가 벌어졌는지 좁혀졌는지 확인한다
for label, period in [("2021 상반기", ("2021-01-01", "2021-06-30")),
                      ("2025 하반기", ("2025-07-01", "2025-12-31"))]:
    sub = gu_trend[(gu_trend["date"] >= period[0]) & (gu_trend["date"] <= period[1])]
    g = sub.groupby("CGG_NM")["JEONSE_PER_M2"].median()
    print(f"{label}  최고 {g.max():6.1f} ({g.idxmax()})  "
          f"최저 {g.min():5.1f} ({g.idxmin()})  배율 {g.max()/g.min():.2f}배")'''))

c.append(("md", "### 3. 건물용도별"))

c.append(("code", '''usg = (rent5[rent5["BLDG_USG"].isin(["아파트", "연립다세대", "단독다가구", "오피스텔"])]
       .groupby([rent5["ym"].str[:4].rename("연도"), "BLDG_USG"])["JEONSE_PER_M2"]
       .median().round(1).reset_index())

fig = px.bar(usg, x="연도", y="JEONSE_PER_M2", color="BLDG_USG", barmode="group",
             labels={"JEONSE_PER_M2": "㎡당 환산전세가 (만원)", "BLDG_USG": "건물용도"})
fig.update_layout(title="건물용도별 ㎡당 환산전세가 중앙값 (2021-2025)",
                  template="plotly_white", height=440)
fig.write_html(HTML / "7_3.html", include_plotlyjs="cdn")
fig.show()

pivot = usg.pivot(index="연도", columns="BLDG_USG", values="JEONSE_PER_M2")
print(pivot.to_string())
print()
print("2021 대비 2025 변화율(%):")
print(((pivot.loc["2025"] / pivot.loc["2021"] - 1) * 100).round(1).to_string())'''))

c.append(("md", """### 읽어낸 것

**건수는 신고제 이야기지 시장 이야기가 아니다.** 2021년 46만 건에서 2025년 102만 건으로
늘었지만, 2025년 6월 계도기간 종료에 맞춰 계단처럼 뛴다. 이 구간을 시장 확대로 읽으면
틀린다. 그래서 이 분석은 건수를 빼고 가격만 다뤘다.

**가격은 평균보다 중앙값이 낫다.** 두 선을 같이 그려 보면 평균이 늘 위에 있다.
비싼 거래 몇 건이 평균을 끌어올리기 때문이다. 신고 대상이 넓어지며 표본 구성이
바뀐 구간에서는 이 차이가 더 벌어진다.

**자치구 간 격차가 건물용도 간 격차보다 크다.** 어느 동네냐가 어떤 집이냐보다 세다.

### 이 분석의 한계

- 전환율 5%는 가정이다. 실제로는 시기·지역·유형마다 다르고, 금리에 따라 움직인다.
  여기 수치는 실거래 전세가가 아니라 비교용 환산값이다.
- 신고제 정착 과정에서 표본이 달라졌다. 초기에 신고된 거래와 나중에 신고된 거래의
  성격이 같다는 보장이 없다.
- 2025년 말 몇 달은 신고 지연으로 건수가 덜 잡혀 있을 수 있다."""))

p1 = build("07_plotly.ipynb", c)

# ── 08 Folium ─────────────────────────────────────────────────────────────
c = []
c.append(("md", """# 08 : Folium

강의자료: `docs/course/08_Folium.md`

GeoJSON으로 국가 경계를 읽고 ISO-3 코드로 통계를 붙인 뒤 단계구분도를 만든다.
**조인 키가 어긋나는 문제를 진단하는 과정**이 이 강의의 핵심이다.

## 데이터

- `data/raw/world-countries.geojson` — 177개국 경계. `id`가 ISO-3 코드
- `data/raw/world-centroids.geojson` — 중심점. `representative_point()`로 직접 생성
- `px.data.gapminder()` — 내장

> 강의자료에 두 GeoJSON의 출처 URL이 없다. folium 공식 저장소 예제본을 썼고
> 구조(177행, id/name/geometry)는 강의자료와 일치한다. 강사 확인이 필요하다."""))

c.append(("code", '''import json
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium
import branca.colormap as cm
from pathlib import Path

HTML = Path("outputs/html"); HTML.mkdir(parents=True, exist_ok=True)
FIG = Path("outputs/figures"); FIG.mkdir(parents=True, exist_ok=True)

gap07 = px.data.gapminder().query("year == 2007")
print("gapminder 2007:", gap07.shape)'''))

c.append(("md", "## 1. GeoDataFrame 읽기"))
c.append(("code", '''world = gpd.read_file("data/raw/world-countries.geojson")
print("shape:", world.shape)
print("CRS:", world.crs)
print("\\n도형 종류:\\n", world.geom_type.value_counts(), sep="")
world.head(3)'''))

c.append(("md", "## 2. 지도로 확인"))
c.append(("code", '''import matplotlib.pyplot as plt
import koreanize_matplotlib

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
world.plot(ax=axes[0], color="white", edgecolor="black", linewidth=0.3)
axes[0].set_title("세계 국가 경계")
axes[0].axis("off")

world[world["id"] == "KOR"].plot(ax=axes[1], color="#1f6feb", edgecolor="black")
axes[1].set_title("대한민국 (KOR)")
axes[1].axis("off")

fig.tight_layout()
fig.savefig(FIG / "6_1.png", dpi=120)
plt.show()'''))

c.append(("md", """## 3. 조인 — 행 수가 늘어나는 문제

경계 177행에 통계를 붙였는데 결과가 178행이 된다. 키가 중복됐다는 뜻이다."""))
c.append(("code", '''merged = world.merge(gap07, left_on="id", right_on="iso_alpha", how="left")
print(f"경계 {len(world)}행 + 통계 → 조인 결과 {len(merged)}행")

if len(merged) != len(world):
    print("행이 늘었다. 오른쪽 테이블에 키가 중복된 것이다.")
    dup = gap07[gap07["iso_alpha"].duplicated(keep=False)]
    print("\\n중복된 iso_alpha:")
    print(dup[["country", "iso_alpha", "lifeExp", "pop"]])'''))

c.append(("code", '''# 매칭되지 않은 국가 확인
print("통계가 안 붙은 국가 수:", merged["lifeExp"].isna().sum())
print("\\n예시:")
print(merged[merged["lifeExp"].isna()]["name"].head(10).tolist())'''))

c.append(("md", """## 4. 원인 수정

북한(Korea, Dem. Rep.)의 ISO 코드가 남한과 같은 `KOR`로 기록돼 있다.
북한의 정확한 코드는 `PRK`다."""))
c.append(("code", '''gap_fixed = gap07.copy()
gap_fixed.loc[gap_fixed["country"] == "Korea, Dem. Rep.", "iso_alpha"] = "PRK"

wg = world.merge(gap_fixed, left_on="id", right_on="iso_alpha", how="left")
print(f"수정 후: {len(world)}행 → {len(wg)}행")
print("중복 남았나:", gap_fixed["iso_alpha"].duplicated().any())

print("\\n한국:")
print(wg[wg["id"].isin(["KOR", "PRK"])][["id", "name", "country", "lifeExp", "gdpPercap"]])'''))

c.append(("md", """## 5. Plotly choropleth — 같은 자료를 다른 도구로

학습목표에 있는 항목이다. Folium과 비교하면 차이가 드러난다.
Plotly는 국가 코드만 주면 경계를 알아서 그리고, Folium은 GeoJSON을 직접 준다."""))
c.append(("code", '''fig = px.choropleth(
    gap_fixed, locations="iso_alpha", color="gdpPercap",
    hover_name="country", color_continuous_scale="Blues",
    projection="natural earth",
    labels={"gdpPercap": "1인당 GDP"},
)
fig.update_layout(title="국가별 1인당 GDP (2007) — Plotly",
                  height=520, margin=dict(l=0, r=0, t=50, b=0))
fig.write_html(HTML / "8_1.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("code", '''# 기대수명으로도 그려 비교한다. 색 방향이 GDP와 비슷하게 가는지 본다.
fig = px.choropleth(
    gap_fixed, locations="iso_alpha", color="lifeExp",
    hover_name="country", color_continuous_scale="RdYlGn",
    projection="natural earth",
    labels={"lifeExp": "기대수명"},
)
fig.update_layout(title="국가별 기대수명 (2007) — Plotly",
                  height=520, margin=dict(l=0, r=0, t=50, b=0))
fig.write_html(HTML / "8_2.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("md", """**Plotly와 Folium 중 무엇을 쓸까**

| | Plotly choropleth | Folium |
| --- | --- | --- |
| 경계 데이터 | 내장 (ISO 코드만 주면 됨) | 직접 준비해야 함 |
| 배경 지도 | 없음 (투영법만 선택) | 실제 타일 지도 위에 얹음 |
| 레이어 중첩 | 제한적 | 자유롭게 쌓음 |
| 적합한 경우 | 국가 단위 빠른 확인 | 행정동처럼 자체 경계가 필요한 경우 |

수업 후반 서울 행정동 분석에는 내장 경계가 없으므로 Folium 쪽이 맞다."""))

c.append(("md", "## 6. Folium 단계구분도"))
c.append(("code", '''geo = json.loads(wg.to_json())

m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

folium.Choropleth(
    geo_data=geo,
    data=wg,
    columns=["id", "gdpPercap"],
    key_on="feature.properties.id",
    fill_color="Blues",
    fill_opacity=0.75,
    line_opacity=0.3,
    nan_fill_color="lightgrey",     # 통계가 없는 국가는 회색으로 구분
    legend_name="1인당 GDP (달러, 2007)",
).add_to(m)

# 투명 레이어를 위에 얹어 마우스를 올리면 값이 보이게 한다
folium.GeoJson(
    geo,
    style_function=lambda _: {"fillColor": "transparent", "color": "transparent"},
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "gdpPercap", "lifeExp"],
        aliases=["국가", "1인당 GDP", "기대수명"],
        localize=True,
    ),
).add_to(m)

m.save(HTML / "9_1.html")
m'''))

c.append(("md", """## 7. 중심점 레이어 얹기

단계구분도 위에 원을 올려 두 변수를 한 지도에서 본다.
색은 기대수명, 크기도 기대수명으로 이중 부호화해 읽기 쉽게 했다."""))
c.append(("code", '''cent = gpd.read_file("data/raw/world-centroids.geojson")
print("중심점:", cent.shape)

# inner join — 양쪽 모두에 있는 것만 남는다. left와 달리 행이 줄어든다
cg = cent.merge(gap_fixed, left_on="id", right_on="iso_alpha", how="inner")
print(f"inner join: {len(cent)} → {len(cg)}행")'''))

c.append(("code", '''colormap = cm.LinearColormap(
    colors=["#c0392b", "#f0c419", "#1a7f45"],
    vmin=float(cg["lifeExp"].min()), vmax=float(cg["lifeExp"].max()),
    caption="기대수명 (년)",
)


def life_to_radius(life):
    """기대수명을 원 반지름으로 바꾼다. 40년을 기준으로 차이를 벌린다."""
    return max(3, (life - 40) * 0.45)


m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

folium.Choropleth(
    geo_data=geo, data=wg, columns=["id", "gdpPercap"],
    key_on="feature.properties.id", fill_color="Blues",
    fill_opacity=0.55, line_opacity=0.25, nan_fill_color="lightgrey",
    legend_name="1인당 GDP (달러)",
).add_to(m)

for _, row in cg.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=life_to_radius(row["lifeExp"]),
        color=colormap(row["lifeExp"]),
        fill=True, fill_color=colormap(row["lifeExp"]), fill_opacity=0.85,
        weight=1,
        tooltip=f"{row['country']}<br>기대수명 {row['lifeExp']:.1f}년"
                f"<br>1인당 GDP {row['gdpPercap']:,.0f}달러",
    ).add_to(m)

colormap.add_to(m)
m.save(HTML / "9_2.html")
m'''))

c.append(("code", '''print("저장된 파일:")
for p in sorted(HTML.glob("9_*.html")) + sorted(FIG.glob("6_*.png")):
    print(" ", p)'''))

c.append(("md", """### 이 강의에서 남길 것

조인은 붙였다고 끝이 아니다. **행 수가 변했는지 반드시 확인한다.**

- 행이 **늘면** 오른쪽 키에 중복이 있다 (여기서는 북한·남한이 둘 다 KOR)
- 행이 **줄면** inner join이라 한쪽에만 있는 것이 빠졌다
- 행 수는 같은데 값이 비면 키 표기가 다르다

수업 후반 팀 프로젝트에서 행정동 코드로 데이터를 붙일 때 똑같은 문제가 생긴다.
행정동 코드는 개편이 잦아서 연도가 다르면 코드가 안 맞는다."""))

p2 = build("08_folium.ipynb", c)
print(p1.name, p2.name)
