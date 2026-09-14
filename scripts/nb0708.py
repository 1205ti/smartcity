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

c.append(("md", """## 과제 2 — 서울 전세 가격 분석

월세를 전세로 환산해 비교 가능한 지표를 만들고, 면적으로 나눠 단위 가격을 본다.

**전월세 전환율 5%** 가정: 환산보증금 = 보증금 + (월세 x 12 / 0.05)"""))
c.append(("code", '''CODE_COLS = {"CGG_CD": "string", "STDG_CD": "string"}
rent = pd.read_csv("data/raw/seoul_rent_2026.csv", encoding="utf-8-sig", dtype=CODE_COLS)
print(rent.shape)

df = rent[["CGG_NM", "STDG_NM", "BLDG_USG", "RENT_SE",
           "GRFE", "RTFE", "RENT_AREA", "CTRT_DAY", "FLR"]].copy()

# 전월세 전환율 5% — 월세를 전세 보증금으로 환산해 같은 잣대로 비교한다
CONVERSION_RATE = 0.05
df["JEONSE_CONVERTED"] = df["GRFE"] + (df["RTFE"] * 12 / CONVERSION_RATE)

# 면적으로 나눠 단위 가격을 만든다. 면적이 0이면 나눗셈이 깨지므로 먼저 거른다
df = df[df["RENT_AREA"] > 0]
df["JEONSE_PER_M2"] = (df["JEONSE_CONVERTED"] / df["RENT_AREA"]).round(2)

print(df[["RENT_SE", "GRFE", "RTFE", "JEONSE_CONVERTED", "RENT_AREA", "JEONSE_PER_M2"]].head())'''))

c.append(("code", '''# 극단값이 축을 다 잡아먹으므로 상하위 1%를 잘라낸다
lo, hi = df["JEONSE_PER_M2"].quantile([0.01, 0.99])
trimmed = df[(df["JEONSE_PER_M2"] >= lo) & (df["JEONSE_PER_M2"] <= hi)]
print(f"상하위 1% 제외: {len(df):,} → {len(trimmed):,}")

# 박스플롯은 원자료를 전부 브라우저로 보낸다. 39만 행이면 파일이 9MB를 넘어
# 열리지도 않으므로 그룹당 최대 1,500건을 무작위 추출한다(seed 고정).
# 사분위수 모양을 보는 목적이라 표본으로 충분하다.
box_src = trimmed[trimmed["BLDG_USG"].isin(["아파트", "연립다세대", "단독다가구"])]
# 전체를 섞은 뒤 그룹별로 앞에서 1,500건씩 — groupby.apply보다 열이 안 사라져 안전하다
box_src = box_src.sample(frac=1, random_state=0).groupby(["CGG_NM", "BLDG_USG"]).head(1500)
print(f"박스플롯용 표본: {len(box_src):,}건 (원본 {len(trimmed):,}건)")

fig = px.box(box_src,
             x="CGG_NM", y="JEONSE_PER_M2", color="BLDG_USG",
             labels={"CGG_NM": "자치구", "JEONSE_PER_M2": "㎡당 환산전세가 (만원)",
                     "BLDG_USG": "건물용도"})
fig.update_layout(title="자치구·건물용도별 ㎡당 환산전세가",
                  template="plotly_white", height=520, xaxis_tickangle=-45)
fig.write_html(HTML / "7_1.html", include_plotlyjs="cdn")
fig.show()'''))

c.append(("code", '''# 계약일을 월 단위로 묶어 추세를 본다
t = trimmed.copy()
t["CTRT_DAY"] = pd.to_datetime(t["CTRT_DAY"], format="%Y%m%d", errors="coerce")
t = t[t["CTRT_DAY"].notna()]
t["month"] = t["CTRT_DAY"].dt.to_period("M").astype(str)

monthly = (t[t["BLDG_USG"] == "아파트"]
           .groupby(["month", "CGG_NM"], as_index=False)["JEONSE_PER_M2"]
           .mean().round(2))

# 거래가 많은 6개 구만 본다. 전부 그리면 선이 뒤엉켜 못 읽는다
top_gu = t[t["BLDG_USG"] == "아파트"]["CGG_NM"].value_counts().head(6).index

fig = px.line(monthly[monthly["CGG_NM"].isin(top_gu)],
              x="month", y="JEONSE_PER_M2", color="CGG_NM", markers=True,
              labels={"month": "계약월", "JEONSE_PER_M2": "㎡당 환산전세가 (만원)",
                      "CGG_NM": "자치구"})
fig.update_layout(title="아파트 ㎡당 환산전세가 월별 추이 (거래 상위 6개구)",
                  template="plotly_white", height=460)
fig.write_html(HTML / "7_2.html", include_plotlyjs="cdn")
fig.show()

print("저장된 HTML:", sorted(p.name for p in HTML.glob("*.html")))'''))

c.append(("md", """### 읽어낸 것

- 자치구 간 ㎡당 환산전세가 격차가 건물용도보다 크다. 어디냐가 무엇이냐보다 세다.
- 아파트는 분포 폭이 좁고 연립다세대·단독다가구는 넓다. 같은 구 안에서도 편차가 크다는 뜻이다.
- 월별 추이는 구마다 방향이 갈린다. 서울 전체를 하나의 시장으로 묶어 보면 이 차이가 지워진다.

주의: 전환율 5%는 가정이다. 실제 전환율은 시기·지역·주택유형에 따라 다르므로
이 값은 비교를 위한 공통 잣대일 뿐 실거래 전세가가 아니다."""))

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
