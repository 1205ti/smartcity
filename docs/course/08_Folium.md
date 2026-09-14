
# 08 : Folium
> GeoJSON·GeoPandas로 공간데이터를 다루고, Folium으로 세계 지도를 시각화하기
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - GeoJSON의 FeatureCollection·Feature·properties·geometry 구조를 이해한다.
  - GeoPandas의 GeoDataFrame과 geometry 열을 읽고 지도에 그린다.
  - 좌표계(CRS)와 Polygon·MultiPolygon의 차이를 확인한다.
  - ISO-3 국가 코드를 이용해 공간데이터와 Gapminder 통계를 조인한다.
  - 조인 키 중복으로 행 수가 늘어나는 문제를 진단하고 수정한다.
  - Plotly choropleth로 국가별 1인당 GDP 단계구분도를 만든다.
  - Folium으로 웹 타일 지도 위에 단계구분도·툴팁·포인트 레이어를 결합한다.

## 0. 실습 준비
```Python
import matplotlib.pyplot as plt
import koreanize_matplotlib

import numpy as np
import pandas as pd

from urllib.request import urlopen
import json

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import folium
```
실행 결과
💡 
  지도 실습에서는 일반 데이터 처리용 Pandas·NumPy와 함께 GeoPandas, Plotly, Folium을 사용합니다. 라이브러리 import만 수행하므로 화면 출력은 없습니다.

## 1. Gapminder 데이터 준비

### 전체 데이터 불러오기
```Python
# Gap Minder Data 불러오기
# 대륙, 나라, 연도, 수명, 인구수, GDP ...
gapminder = px.data.gapminder()
gapminder
```
노트북에 저장된 실행 결과
```Plain Text
          country continent  year  lifeExp       pop   gdpPercap iso_alpha  iso_num
0     Afghanistan      Asia  1952   28.801   8425333  779.445314       AFG        4
1     Afghanistan      Asia  1957   30.332   9240934  820.853030       AFG        4
2     Afghanistan      Asia  1962   31.997  10267083  853.100710       AFG        4
...
1703     Zimbabwe    Africa  2007   43.487  12311143  469.709298       ZWE      716

[1704 rows x 8 columns]
```
💡 
  Gapminder에는 국가·대륙·연도·기대수명·인구·1인당 GDP와 ISO 국가 코드가 들어 있습니다. 공간데이터와 결합할 때 iso_alpha가 핵심 연결 키가 됩니다.

### 2007년만 추출
```Python
gapminder_2007 = gapminder.query("year == 2007")
```
💡 
  여러 시점이 반복되는 원본에서 2007년 한 시점만 남기면 국가별 공간 통계와 1:1로 연결하기 쉬워집니다.

## 2. GeoJSON과 GeoPandas

### GeoJSON 구조
- GeoJSON은 좌표와 도형을 JSON 형식으로 표현하는 공개 공간데이터 표준입니다.
- FeatureCollection 안에 여러 Feature가 있고, 각 Feature는 properties와 geometry로 구성됩니다.
- geometry에는 Point, LineString, Polygon, MultiPolygon 등이 들어갈 수 있습니다.
- 공식 사이트: geojson.org

### GeoPandas
- Pandas의 DataFrame에 공간 정보인 geometry 열을 더한 GeoDataFrame을 사용합니다.
- gpd.read_file()로 GeoJSON·Shapefile 등을 읽을 수 있습니다.
- Shapely geometry를 이용해 면적·거리·중첩 등 공간 연산을 수행할 수 있습니다.
- 공식 사이트: GeoPandas

### 세계 국가 GeoJSON 불러오기
```Python
import geopandas as gpd

world = gpd.read_file("data/world-countries.geojson")

print(world.shape)
print(world.crs)
world.head()
```
실행 결과
```Plain Text
(177, 3)
EPSG:4326

    id                  name                                           geometry
0  AFG           Afghanistan  POLYGON ((61.21082 35.65007, 62.23065 35.27066...
1  AGO                Angola  MULTIPOLYGON (((16.32653 -5.87747, 16.57318 -6...
2  ALB               Albania  POLYGON ((20.59025 41.8554, 20.46318 41.51509,...
3  ARE  United Arab Emirates  POLYGON ((51.57952 24.2455, 51.75744 24.29407,...
4  ARG             Argentina  MULTIPOLYGON (((-65.5 -55.2, -66.45 -55.25, -6...
```
💡 
  EPSG:4326은 경도·위도를 사용하는 WGS84 좌표계입니다. geometry 열에 실제 국가 경계 도형이 저장됩니다.

### Polygon과 MultiPolygon 개수
```Python
world.geom_type.value_counts()
```
실행 결과
```Plain Text
Polygon         149
MultiPolygon     28
Name: count, dtype: int64
```
💡 
  한 덩어리의 육지로 표현되는 국가는 주로 Polygon, 섬이나 분리된 영토를 포함하면 MultiPolygon으로 저장될 수 있습니다.

### 세계지도 그리기
```Python
world.plot(figsize=(12, 8), color="white", edgecolor="black")
plt.savefig('image/6_1.png')
```
실행 결과
6_1.png
💡 
  GeoDataFrame의 .plot()은 geometry 열을 자동으로 해석하여 공간 도형을 그립니다. 속성값 없이 경계 자체를 확인할 때 유용합니다.

### 대한민국만 선택
```Python
world[world["id"] == "KOR"].plot()
plt.savefig('image/6_2.png')
```
실행 결과
6_2.svg
💡 
  ISO-3 코드 KOR을 조건으로 사용해 대한민국 도형 한 개만 선택할 수 있습니다. 공간데이터도 일반 DataFrame처럼 조건 필터링할 수 있다는 점이 핵심입니다.

## 3. 세계 경계와 Gapminder 조인

### 첫 번째 left join
```Python
world_gapminder = world.merge(
    gapminder_2007,
    left_on="id",
    right_on="iso_alpha",
    how="left",
)

print(type(world_gapminder))
print(len(world), "->", len(world_gapminder))
world_gapminder.head()
```
실행 결과
```Plain Text
<class 'geopandas.geodataframe.GeoDataFrame'>
177 -> 178
```
💡 
  177개였던 국가가 178개로 늘었습니다. left join이라고 해서 항상 행 수가 유지되는 것은 아닙니다. 오른쪽 데이터의 조인 키가 중복되어 있으면 한 행이 여러 행과 매칭되어 결과가 늘어날 수 있습니다.

### 매칭되지 않은 국가 수
```Python
world_gapminder["iso_alpha"].isna().sum()
```
실행 결과
```Plain Text
43
```
💡 
  GeoJSON에는 있지만 Gapminder에 없거나, 국가 코드 체계가 서로 다른 경우 통계값이 결측치로 남습니다.

### KOR 중복 확인
```Python
world_gapminder[world_gapminder["id"] == "KOR"][["id", "name", "country", "pop"]]
```
실행 결과
```Plain Text
     id         name           country         pop
87  KOR  South Korea  Korea, Dem. Rep.  23301725.0
88  KOR  South Korea       Korea, Rep.  49044790.0
```
💡 
  노트북의 Gapminder 데이터에서는 북한과 남한이 모두 KOR로 기록되어 있어 대한민국 경계가 두 통계 행과 매칭되었습니다.

### 북한 코드 수정
```Python
gapminder_2007.loc[
    gapminder_2007["country"] == "Korea, Dem. Rep.", "iso_alpha"
] = "PRK"

gapminder_2007[
    gapminder_2007["country"].str.contains("Korea")
][["country", "iso_alpha"]]
```
실행 결과
```Plain Text
              country iso_alpha
839  Korea, Dem. Rep.       PRK
851       Korea, Rep.       KOR
```

### 다시 조인
```Python
world_gapminder = world.merge(
    gapminder_2007,
    left_on="id",
    right_on="iso_alpha",
    how="left",
)

print(type(world_gapminder))
print(len(world), "->", len(world_gapminder))
world_gapminder.head()
```
실행 결과
```Plain Text
<class 'geopandas.geodataframe.GeoDataFrame'>
177 -> 177
```
💡 
  공간데이터 조인 전에는 조인 키의 유일성(unique) 을 먼저 확인하는 습관이 중요합니다. value_counts()나 duplicated()를 이용해 중복 키를 점검하면 예상치 못한 행 증가를 예방할 수 있습니다.

## 4. Folium: 웹 타일 지도 위에 단계구분도

### Folium이란?
Folium은 JavaScript 지도 라이브러리 Leaflet.js를 Python에서 사용할 수 있게 감싼 라이브러리입니다.
- 확대·축소·이동이 가능한 웹 지도를 생성합니다.
- folium.Choropleth()로 GeoJSON과 통계 데이터를 결합합니다.
- Marker, CircleMarker, GeoJson, popup·tooltip 등을 추가할 수 있습니다.
- 공식 사이트: Folium

### GDP Choropleth + Tooltip
```Python
geojson_data = json.loads(world_gapminder.to_json())

m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

folium.Choropleth(
    geo_data=geojson_data,
    data=world_gapminder,
    columns=["id", "gdpPercap"],
    key_on="feature.properties.id",
    fill_color="Blues",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="lightgrey",
    legend_name="1인당 GDP (2007)",
).add_to(m)

folium.GeoJson(
    geojson_data,
    style_function=lambda x: {"fillOpacity": 0, "weight": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "gdpPercap"],
        aliases=["국가", "1인당 GDP"],
        localize=True,
    ),
).add_to(m)

m.save("html/9_1.html")
m
```
실행 결과
OpenStreetMap 배경 위에 국가별 1인당 GDP 단계구분도가 표시되고, 국가에 마우스를 올리면 국가명과 GDP를 확인할 수 있습니다.
9_1.html
💡 
  Plotly 지도는 데이터 시각화 중심이고, Folium은 실제 웹 지도 탐색과 레이어 결합에 강합니다. nan_fill_color='lightgrey'로 통계가 매칭되지 않은 국가도 구분합니다.

## 5. 국가 중심점과 기대수명 포인트 레이어

### 중심점 GeoJSON 불러오기
```Python
world_centroids = gpd.read_file("data/world-centroids.geojson")

print(world_centroids.shape)
world_centroids.head()
```
노트북에 저장된 실행 결과
```Plain Text
(177, 3)

    id                  name                     geometry
0  AFG           Afghanistan   POINT (66.12826 33.93667)
1  AGO                Angola  POINT (17.4732 -12.30289)
2  ALB               Albania   POINT (20.03154 41.1538)
3  ARE  United Arab Emirates  POINT (54.21085 23.87571)
4  ARG             Argentina   POINT (-65.4182 -36.7045)
```
💡 
  world_centroids는 177개 국가의 대표 좌표를 Point geometry로 저장한 GeoDataFrame입니다. id는 ISO-3 국가 코드이며, 이후 gapminder_2007.iso_alpha와 조인하는 키로 사용합니다.

### Gapminder와 inner join
```Python
centroids_gapminder = world_centroids.merge(
    gapminder_2007,
    left_on="id",
    right_on="iso_alpha",
    how="inner",
)

print(len(world_centroids), "->", len(centroids_gapminder))
centroids_gapminder.head()
```
노트북에 저장된 실행 결과
```Plain Text
177 -> 135

    id         name                     geometry      country continent  year  lifeExp       pop    gdpPercap iso_alpha  iso_num
0  AFG  Afghanistan   POINT (66.12826 33.93667)  Afghanistan      Asia  2007   43.828  31889923   974.580338       AFG        4
1  AGO       Angola  POINT (17.4732 -12.30289)         Angola    Africa  2007   42.731  12420476  4797.231267       AGO       24
2  ALB      Albania   POINT (20.03154 41.1538)        Albania    Europe  2007   76.423   3600523  5937.029526       ALB        8
3  ARG    Argentina   POINT (-65.4182 -36.7045)     Argentina  Americas  2007   75.320  40301927 12779.379640       ARG       32
4  AUS    Australia  POINT (134.61655 -26.2296)     Australia   Oceania  2007   81.235  20434176 34435.367440       AUS       36
```
💡 
  inner 조인은 양쪽 데이터에 공통으로 존재하는 ISO-3 코드만 남깁니다. 따라서 177개 중심점 중 Gapminder 2007 자료와 매칭되는 135개 국가만 결과에 남습니다.
💡 
  inner join은 두 데이터에 모두 존재하는 국가만 남깁니다. left join과 달리 매칭되지 않은 국가를 결측으로 보존하지 않습니다.

### GDP 면 + 기대수명 점을 한 지도에 결합
```Python
geojson_data = json.loads(world_gapminder.to_json())

m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

folium.Choropleth(
    geo_data=geojson_data,
    data=world_gapminder,
    columns=["id", "gdpPercap"],
    key_on="feature.properties.id",
    fill_color="Blues",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="lightgrey",
    legend_name="1인당 GDP (2007)",
).add_to(m)

folium.GeoJson(
    geojson_data,
    style_function=lambda x: {"fillOpacity": 0, "weight": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=["name", "gdpPercap"],
        aliases=["국가", "1인당 GDP"],
        localize=True,
    ),
).add_to(m)

import branca.colormap as cm

lifeExp_min = centroids_gapminder["lifeExp"].min()
lifeExp_max = centroids_gapminder["lifeExp"].max()
lifeExp_colormap = cm.linear.YlOrRd_09.scale(lifeExp_min, lifeExp_max)
lifeExp_colormap.caption = "기대수명 (lifeExp)"

MIN_RADIUS, MAX_RADIUS = 2, 10

def lifeExp_to_radius(value):
    ratio = (value - lifeExp_min) / (lifeExp_max - lifeExp_min)
    return MIN_RADIUS + ratio * (MAX_RADIUS - MIN_RADIUS)

for _, row in centroids_gapminder.iterrows():
    lon, lat = row.geometry.x, row.geometry.y
    folium.CircleMarker(
        location=[lat, lon],
        radius=lifeExp_to_radius(row["lifeExp"]),
        color=lifeExp_colormap(row["lifeExp"]),
        weight=1,
        fill=True,
        fill_color=lifeExp_colormap(row["lifeExp"]),
        fill_opacity=0.70,
        tooltip=f"{row['name']}<br>기대수명: {row['lifeExp']:.1f}세",
    ).add_to(m)

lifeExp_colormap.add_to(m)

m.save("html/9_2.html")
m
```
실행 결과
국가 면의 파란색 농도는 1인당 GDP, 국가 중심점의 점 크기와 노랑→빨강 계열 색은 기대수명을 나타내는 복합 지도가 생성됩니다.
9_2.html
💡 
  한 지도에서 서로 다른 변수의 시각 채널을 분리했습니다. GDP는 면의 색, 기대수명은 점의 크기와 색으로 표현하므로 두 변수를 동시에 탐색할 수 있습니다.

## 6. 핵심 정리
  | 역할 | 도구·개념 | 이번 실습의 핵심 |
  | 공간도형 교환 포맷 | GeoJSON | properties + geometry 구조 |
  | 공간 DataFrame | GeoPandas | 읽기·필터링·조인·정적 지도 |
  | 좌표의 기준 | CRS | EPSG:4326 = 경도·위도 |
  | 국가 연결 키 | ISO-3 | id ↔ iso_alpha |
  | Leaflet 웹 지도 | Folium | 타일 지도 + 면·점·툴팁 레이어 |
💡 
  공간분석의 기본 흐름: 공간 경계 읽기 → CRS·geometry 확인 → 연결 키 정리 → 속성 데이터 조인 → 결측·중복 점검 → 정적/인터랙티브 지도 제작
---
💡 
  이전 강의: 07 : Plotly
💡 
  다음 강의: 09-1 : 공간데이터와 좌표계