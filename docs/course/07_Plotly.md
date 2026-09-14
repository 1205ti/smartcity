
# 07 : Plotly
> Plotly Express로 인터랙티브 그래프를 만들고, 서울 전월세 데이터를 탐색적으로 시각화하기
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - Plotly의 인터랙티브 시각화 특징을 이해한다.
  - plotly.express로 Scatter, Bar, Histogram, Box, Line, Area plot을 만든다.
  - size, color, hover_name, log_x, facet_col, animation_frame 등 Plotly의 주요 옵션을 활용한다.
  - Plotly 그래프를 HTML 파일로 저장해 웹에서 재사용한다.
  - 서울 전월세 데이터를 전처리하고 전세 환산 보증금과 ㎡당 전세가를 계산한다.
  - 분포·상관관계·월별 추세를 인터랙티브 그래프로 분석한다.

## 1. 실습 준비: Plotly
Plotly는 마우스 오버, 확대·축소, 범례 선택, 애니메이션 등을 지원하는 인터랙티브 시각화 라이브러리입니다. 그래프 정보를 JSON 형태로 표현할 수 있고, 완성된 그래프를 HTML로 저장하여 웹페이지에서도 사용할 수 있습니다.
```Python
# 설치가 필요한 경우
# pip install plotly

import matplotlib.pyplot as plt
import koreanize_matplotlib

import numpy as np
import pandas as pd

from urllib.request import urlopen
import json

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
```
실행 결과
💡 
  plotly.express는 한 줄의 함수 호출만으로 완성된 Figure를 만들 수 있는 고수준 인터페이스입니다. 관례적으로 px라는 별칭을 사용합니다. graph_objects는 그래프를 더 세밀하게 제어할 때 사용합니다.
💡 
  Plotly 그래프는 fig.show()로 표시하고, fig.write_html("파일명.html")로 인터랙티브 상태 그대로 저장할 수 있습니다.

## 2. Scatter Plot: 두 변수의 관계

### Gapminder 데이터 불러오기
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
...
1703     Zimbabwe    Africa  2007   43.487  12311143  469.709298       ZWE      716

[1704 rows x 8 columns]
```
💡 
  Gapminder는 국가·대륙·연도·기대수명·인구·1인당 GDP를 포함합니다. 한 국가가 여러 연도에 걸쳐 반복되므로 시계열과 애니메이션 실습에도 적합합니다.

### 2007년 데이터만 추출
```Python
gapminder_2007 = gapminder.query("year == 2007")
gapminder_2007
```
실행 결과
```Plain Text
[142 rows x 8 columns]
```
💡 
  전체 1,704행에서 2007년 자료만 남기면 142개 국가의 한 시점 데이터가 됩니다.

### 기본 산점도
```Python
fig = px.scatter(gapminder_2007, x="gdpPercap", y="lifeExp")
fig.show()
fig.write_html("html/1_1.html")
```
실행 결과: 1_1.html
1_1.html
💡 
  가로축은 1인당 GDP, 세로축은 기대수명입니다. Plotly에서는 점에 마우스를 올리면 좌표값을 즉시 확인할 수 있고, 드래그하여 특정 영역을 확대할 수도 있습니다.

### 크기·색상·Hover·로그축 적용
```Python
fig = px.scatter(
    gapminder_2007,
    x="gdpPercap", y="lifeExp",
    width=800, height=500,
    labels={'gdpPercap':'GDP per capita', 'lifeExp':'Life Expectancy'},
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
    color_discrete_sequence=px.colors.qualitative.G10[::-1],
)

fig.update_layout(plot_bgcolor='white')
fig.update_xaxes(ticks='outside', showline=True, linecolor='black',
                 showgrid=True, griddash='dot', gridwidth=0.05,
                 gridcolor='lightgrey')
fig.update_yaxes(ticks='outside', showline=True, linecolor='black',
                 showgrid=True, griddash='dot', gridwidth=0.05,
                 gridcolor='lightgrey')
fig.show()
fig.write_html("html/1_2.html")
```
실행 결과: 1_2.html
1_2.html
💡 
  점의 크기는 인구, 색상은 대륙을 나타냅니다. hover_name='country'로 국가명을 확인할 수 있고, log_x=True는 GDP처럼 범위가 큰 변수를 로그축으로 바꾸어 국가 간 차이를 더 읽기 쉽게 합니다.
💡 
  색상은 직접 Hex code를 지정할 수도 있고 px.colors.qualitative, px.colors.sequential, px.colors.diverging의 내장 팔레트를 사용할 수도 있습니다.

### Facet: 연도별 그래프를 한 화면에 비교
```Python
fig = px.scatter(
    gapminder, x="gdpPercap", y="lifeExp",
    size="pop", color="continent",
    labels={'gdpPercap':'GDP per capita', 'lifeExp':'Life Expectancy'},
    color_discrete_sequence=px.colors.qualitative.G10[::-1],
    log_x=True,
    facet_col="year",
    facet_col_wrap=4,
    facet_col_spacing=0.03,
    facet_row_spacing=0.1,
)
fig.update_xaxes(matches="x")
fig.update_yaxes(matches="y")
fig.show()
fig.write_html("html/1_3.html")
```
실행 결과: 1_3.html
1_3_no_webgl_selfcontained.html
💡 
  facet_col='year'는 연도별 그래프를 작은 패널로 분리합니다. matches='x', matches='y'를 이용하면 모든 패널의 축 범위를 공유하므로 시점 간 비교가 공정해집니다.

### Animation: 시간에 따른 변화
```Python
fig = px.scatter(
    gapminder,
    x="gdpPercap", y="lifeExp",
    animation_frame="year",
    animation_group="country",
    size="pop", color="continent",
    hover_name="country",
    log_x=True,
    size_max=55,
    range_x=[200, 100000],
    range_y=[25, 90],
)
fig.show()
fig.write_html("html/1_4.html")
```
실행 결과: 1_4.html
1_4.html
💡 
  재생 버튼을 누르면 1952년부터 2007년까지 국가별 GDP와 기대수명의 변화가 애니메이션으로 나타납니다. animation_group='country'는 프레임 사이에서 같은 국가를 같은 객체로 연결합니다.

### Scatter Matrix
```Python
fig = px.scatter_matrix(
    gapminder_2007[["gdpPercap", 'lifeExp', 'pop']],
    template="presentation"
)
fig.show()
fig.write_html("html/1_5.html")
```
실행 결과: 1_5.html
1_5_notion_no_webgl.html
💡 
  Scatter Matrix는 여러 수치형 변수의 조합을 한 화면에 나타냅니다. GDP·기대수명·인구 사이의 관계를 동시에 탐색할 수 있습니다.

### Plotly 기본 템플릿
- plotly — 기본 테마
- plotly_white — 흰 배경
- plotly_dark — 다크 테마
- simple_white — 미니멀한 흰 배경
- ggplot2 — ggplot 스타일
- seaborn — Seaborn 스타일
- presentation — 발표용 큰 글자·선
- xgridoff, ygridoff, gridon, none

## 3. Bar Graph: 범주별 크기 비교

### 아시아 국가 추출
```Python
gapminder_asia = gapminder.query("continent == 'Asia'")
gapminder_asia
```
실행 결과
```Plain Text
[396 rows x 8 columns]
```

### 2007년 국가별 인구
```Python
fig = px.bar(
    gapminder_asia.query("year == 2007"),
    x="country", y="pop",
    template="presentation"
)
fig.show()
fig.write_html("html/2_1.html")
```
실행 결과: 2_1.html
2_1.html
💡 
  Bar graph는 국가처럼 범주형 값마다 하나의 수치를 비교할 때 유용합니다. 여기서는 2007년 아시아 각 국가의 인구를 비교합니다.

### 여러 연도를 누적해 표현
```Python
fig = px.bar(
    gapminder_asia,
    x="country", y="pop",
    color='year',
    template="presentation",
    color_continuous_scale=px.colors.sequential.matter
)
fig.show()
fig.write_html("html/2_2.html")
```
실행 결과: 2_2.html
2_2.html
💡 
  color='year'를 적용하면 여러 연도의 값이 색상으로 구분됩니다. 범례를 클릭하면 특정 연도의 데이터만 켜고 끌 수 있습니다.

### 국가가 많을 때는 가로 막대그래프
```Python
data_2007 = gapminder_asia.query("year == 2007").sort_values("pop", ascending=False)

fig = px.bar(
    data_2007,
    x="pop", y="country",
    orientation="h",
    template="presentation",
    width=1200, height=1000,
    category_orders={"country": data_2007["country"].tolist()},
)
fig.update_layout(margin=dict(l=180, r=50, t=60, b=70))
fig.update_yaxes(title_text="", automargin=True, tickfont=dict(size=14))
fig.show()
fig.write_html("html/2_3.html")
```
실행 결과: 2_3.html
2_3.html
💡 
  국가명이 많거나 이름이 길다면 orientation='h'가 읽기 쉽습니다. 시각화 전에 데이터를 내림차순 정렬하면 순위 비교도 쉬워집니다.

## 4. Histogram: 분포 확인
```Python
gapminder_2007[["gdpPercap", 'lifeExp', 'pop']]
```
실행 결과
```Plain Text
[142 rows x 3 columns]
```

### 기본 Histogram
```Python
fig = px.histogram(gapminder_2007, x="lifeExp")
fig.show()
fig.write_html("html/3_1.html")
```
실행 결과: 3_1.html
3_1.html
💡 
  기본 Histogram의 y축은 각 구간에 들어가는 국가 수(count) 입니다. 기대수명이 어느 구간에 많이 몰려 있는지 확인할 수 있습니다.

### 구간 수와 확률밀도 변경
```Python
fig = px.histogram(
    gapminder_2007,
    x="lifeExp",
    template="presentation",
    nbins=30,
    histnorm="probability density",
    labels={"lifeExp":"Life Expectancy"},
)
fig.show()
fig.write_html("html/3_2.html")
```
실행 결과: 3_2.html
3_2.html
💡 
  nbins=30은 구간을 더 촘촘하게 나누고, histnorm='probability density'는 y축을 단순 건수가 아닌 확률밀도로 바꿉니다.

## 5. Box Plot: 중앙값·사분위수·이상치
```Python
fig = px.box(gapminder_2007, y="lifeExp")
fig.show()
fig.write_html("html/4_1.html")
```
💡 
  하나의 Box plot으로 2007년 국가들의 기대수명 중앙값, 사분위범위와 이상치를 확인할 수 있습니다.
```Python
fig = px.box(
    gapminder_2007,
    y="lifeExp",
    x='continent',
    template="presentation",
)
fig.show()
fig.write_html("html/4_2.html")
```
실행 결과: 4_2.html
4_2.html
💡 
  x='continent'를 추가하면 대륙별 기대수명 분포를 나란히 비교할 수 있습니다. 평균값만 비교하는 것보다 분산과 이상치까지 함께 볼 수 있다는 장점이 있습니다.

## 6. Line Plot: 시간에 따른 변화
```Python
gapminder_asia.head(5)
```
실행 결과
```Plain Text
       country continent  year  lifeExp       pop   gdpPercap
0  Afghanistan      Asia  1952   28.801   8425333  779.445314
1  Afghanistan      Asia  1957   30.332   9240934  820.853030
2  Afghanistan      Asia  1962   31.997  10267083  853.100710
3  Afghanistan      Asia  1967   34.020  11537966  836.197138
4  Afghanistan      Asia  1972   36.088  13079460  739.981106
```
```Python
fig = px.line(
    gapminder_asia,
    x="year", y="lifeExp",
    color="country",
    template="presentation",
)
fig.show()
fig.write_html("html/5_1.html")
```
실행 결과: 5_1.html
5_1.html
💡 
  Line plot은 시간 순서가 있는 데이터의 변화를 표현합니다. color='country'로 각 국가를 서로 다른 선으로 나타냅니다.

## 7. Area Plot: 누적 변화
```Python
fig = px.area(
    gapminder_asia,
    x="year", y="pop",
    color="country",
    template="plotly_white",
)
fig.show()
fig.write_html("html/6_1.html")
```
실행 결과: 6_1.html
6_1.html
💡 
  Area plot은 선그래프 아래 영역을 채웁니다. 여러 범주를 쌓아 표현하면 전체 규모와 각 범주의 기여도 변화를 함께 볼 수 있습니다.

## 8. Matplotlib과 Plotly 비교
  | 항목 | Matplotlib | Plotly |
  | 기본 목적 | 정적 그래프·출판용 시각화 | 인터랙티브 탐색·웹 시각화 |
  | 마우스 Hover | 기본적으로 없음 | 기본 지원 |
  | 확대·축소 | 환경에 따라 제한적 | 기본 지원 |
  | 애니메이션 | 별도 구현 필요 | animation_frame으로 간단히 구현 |
  | 저장 | PNG·SVG 등 이미지 | HTML·이미지 |

## 9. 핵심 정리
💡 
  Plotly Express 기본 패턴
  1. DataFrame을 준비한다.
  1. px.scatter(), px.bar(), px.histogram(), px.box(), px.line() 등으로 Figure를 만든다.
  1. color, size, facet, hover, animation 옵션으로 정보를 추가한다.
  1. fig.update_layout(), fig.update_xaxes(), fig.update_yaxes()로 세부 디자인을 조정한다.
  1. fig.show()로 확인하고 fig.write_html()로 인터랙티브 그래프를 저장한다.

## 10. 과제 2

#### 지난 5년간 서울시 전세 가격 변화를 분석하시오.
- 분석 목적에 맞는 가격 지표를 정의하세요.
- 시간 변수와 자치구·건물용도 등 비교 기준을 정하세요.
- 최소 2개 이상의 Plotly 그래프를 사용하세요.
- 단순히 그래프를 그리는 데서 끝내지 말고 그래프에서 확인한 특징과 해석을 함께 작성하세요.
- 필요하면 fig.write_html()로 결과를 저장하여 제출물에 포함하세요.
---
💡 
  이전 강의: 06 : Matplotlib
💡 
  다음 강의: 08 : Folium