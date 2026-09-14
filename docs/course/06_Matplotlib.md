
# 06 : Matplotlib
> Matplotlib과 Pandas 시각화 기능으로 분포·관계·비교·추세를 그래프로 표현하기
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - Matplotlib의 기본 선그래프와 산점도를 그린다.
  - Histogram과 Density plot으로 수치형 변수의 분포를 확인한다.
  - Scatter plot으로 두 수치형 변수의 관계를 표현하고 투명도·크기·색상을 활용한다.
  - Bar plot으로 범주별 개수와 평균을 비교한다.
  - Box plot으로 중앙값·사분위수·이상치를 읽는다.
  - Line plot으로 시간에 따른 변화 추세를 표현한다.
  - 그래프 스타일을 바꾸고 이미지 파일로 저장한다.

## 1. 실습 준비: Matplotlib
Matplotlib은 Python의 대표적인 데이터 시각화 라이브러리입니다. 선그래프, 산점도, 막대그래프, 히스토그램, Box plot 등 대부분의 기본 시각화를 만들 수 있습니다. Pandas의 plot()과 hist() 역시 내부적으로 Matplotlib을 이용합니다.
한국어가 그래프에서 깨지는 것을 줄이기 위해 koreanize-matplotlib을 사용합니다.
```Python
# 한글깨지는것 방지하기 위해 koreanize-matplotlib 사용
# %pip install koreanize-matplotlib
```
노트북에 저장된 실행 결과
```Plain Text
Requirement already satisfied: koreanize-matplotlib ... (0.1.1)
Requirement already satisfied: matplotlib ... (3.11.1)
...
```
💡 
  이미 패키지가 설치된 환경에서 실행되어 Requirement already satisfied가 기록되어 있습니다. 처음 설치한다면 주석의 #을 제거하고 %pip install koreanize-matplotlib을 실행합니다.
```Python
import matplotlib.pyplot as plt
import setuptools  # Python 3.12+ removed distutils; setuptools provides a shim that koreanize_matplotlib needs
import koreanize_matplotlib

import numpy as np
import pandas as pd

plt.style.use('default')
```
실행 결과
💡 
  matplotlib.pyplot은 그래프를 만들고 제목·축·범례 등을 설정하는 핵심 모듈입니다. 관례적으로 plt라는 별칭을 사용합니다.

## 2. Histogram: 수치형 변수의 분포
Histogram은 연속적인 수치 데이터를 여러 구간(bin) 으로 나누고, 각 구간에 포함되는 관측치의 개수를 막대 높이로 표현하는 그래프입니다. 숫자 목록만 볼 때보다 데이터가 어느 범위에 몰려 있는지, 한쪽으로 치우쳐 있는지, 넓게 퍼져 있는지를 빠르게 파악할 수 있습니다.
💡 
  이 절의 목표
  - DataFrame.hist()로 수치형 변수의 Histogram을 그린다.
  - bins에 따라 분포가 어떻게 다르게 보이는지 이해한다.
  - Matplotlib의 스타일을 확인하고 적용한다.
  - by, sharex, sharey, layout, figsize를 이용해 집단별 분포를 비교한다.

### 실습 데이터 불러오기
세계 여러 나라의 맥주·증류주·와인 소비량 데이터인 drinks를 사용합니다.
```Python
# Example data: Drinks data
drink_cols = ['country', 'beer', 'spirit', 'wine', 'pure', 'continent']
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
drinks = pd.read_csv(url, header=0, names=drink_cols, na_filter=False)
drinks
```
노트북에 저장된 실행 결과
```Plain Text
         country  beer  spirit  wine  pure continent
0    Afghanistan     0       0     0   0.0        AS
1        Albania    89     132    54   4.9        EU
2        Algeria    25       0    14   0.7        AF
3        Andorra   245     138   312  12.4        EU
4         Angola   217      57    45   5.9        AF
..           ...   ...     ...   ...   ...       ...
188    Venezuela   333     100     3   7.7        SA
189      Vietnam   111       2     1   2.0        AS
190        Yemen     6       0     0   0.1        AS
191       Zambia    32      19     4   2.5        AF
192     Zimbabwe    64      18     4   4.7        AF

[193 rows x 6 columns]
```
💡 
  193개 국가가 행으로 저장되어 있습니다. beer, spirit, wine은 주류별 소비량, pure는 순수 알코올 소비량, continent는 대륙 코드입니다. Histogram 실습에서는 먼저 beer 열을 사용합니다.

### 숫자를 정렬해서 확인하기
```Python
# sort the beer column 
drinks.beer.sort_values(ascending=True)
```
실행 결과
```Plain Text
0        0
13       0
40       0
46       0
111      0
      ... 
98     343
65     346
62     347
45     361
117    376
Name: beer, Length: 193, dtype: int64
```
💡 
  오름차순으로 정렬하면 최솟값이 0이고 최댓값이 376이라는 사실은 알 수 있지만, 어느 구간에 국가가 많이 몰려 있는지는 숫자 목록만으로 파악하기 어렵습니다. 이때 Histogram이 유용합니다.

### bins=10: 기본 Histogram
```Python
drinks.hist(column='beer',    # beer count 시각화
            bins=10)          # 10개 구간

plt.savefig('image/1_1.png')  # 그래프 출력과 저장
```
실행 결과
matplotlib_histogram_1_1.svg
💡 
  bins=10은 beer 소비량 전체 범위를 10개의 구간으로 나눕니다. 그래프를 보면 낮은 beer 소비량 구간에 많은 국가가 집중되어 있고, 값이 커질수록 빈도가 전반적으로 감소하는 오른쪽 꼬리가 긴 분포임을 확인할 수 있습니다.
💡 
  plt.savefig()는 현재 Figure를 이미지 파일로 저장합니다. 보고서나 웹페이지에서 그래프를 재사용하려면 그래프 생성 코드 뒤에 저장 코드를 두는 습관이 좋습니다.

### Matplotlib 스타일 확인과 적용
현재 사용할 수 있는 그래프 스타일은 plt.style.available로 확인할 수 있습니다.
```Python
# list available plot styles
plt.style.available
```
노트북에 저장된 실행 결과
```Plain Text
['Solarize_Light2',
 'bmh',
 'classic',
 'dark_background',
 'fast',
 'fivethirtyeight',
 'ggplot',
 'grayscale',
 'petroff10',
 'petroff6',
 'petroff8',
 'seaborn-v0_8',
 'seaborn-v0_8-bright',
 'seaborn-v0_8-colorblind',
 'seaborn-v0_8-dark',
 'seaborn-v0_8-dark-palette',
 'seaborn-v0_8-darkgrid',
 'seaborn-v0_8-deep',
 'seaborn-v0_8-muted',
 'seaborn-v0_8-notebook',
 'seaborn-v0_8-paper',
 'seaborn-v0_8-pastel',
 'seaborn-v0_8-poster',
 'seaborn-v0_8-talk',
 'seaborn-v0_8-ticks',
 'seaborn-v0_8-white',
 'seaborn-v0_8-whitegrid',
 'tableau-colorblind10']
```
```Python
plt.style.use('seaborn-v0_8-deep')        # 스타일 적용
```

### bins=20: 구간을 더 세밀하게 나누기
```Python
drinks.hist(column='beer',                # beer count 시각화
            bins=20)                      # 20개 구간

plt.xlabel('Beer Servings')               # x축 레이블
plt.ylabel('Frequency')                   # y축 레이블
plt.title('Histogram of Beer Servings')   # 타이틀 추가

plt.savefig('image/1_2.png') 
```
실행 결과
matplotlib_histogram_1_2.svg
💡 
  같은 데이터를 bins=20으로 나누면 bins=10보다 구간 폭이 좁아져 분포의 세부적인 굴곡을 더 자세히 볼 수 있습니다. xlabel, ylabel, title을 추가하면 그래프가 무엇을 의미하는지 독자가 바로 이해하기 쉬워집니다.
💡 
  bins가 너무 적으면 분포가 지나치게 단순해지고, 너무 많으면 작은 변동이 과도하게 강조될 수 있습니다. 하나의 정답이 있는 값이 아니라 분석 목적과 데이터 크기에 맞춰 선택합니다.

### 대륙별 beer 소비량 Histogram
by='continent'를 사용하면 하나의 수치형 변수를 그룹별로 나누어 여러 Histogram을 한 번에 만들 수 있습니다.
```Python
# AF, AS, EU, NA, OC, SA 대륙별 beer Histogram 6개 출력
# 기본 배치: 3행 × 2열
drinks.hist(column='beer', 
            by='continent',   # 대률별 출력
            figsize=(12, 8),  # 가로 12, 세로 8 인치
)

plt.savefig('image/1_3.png')
```
실행 결과
matplotlib_histogram_1_3.svg
💡 
  by='continent'는 AF, AS, EU, NA, OC, SA의 6개 대륙으로 데이터를 나누어 각각의 beer 분포를 보여줍니다. 예를 들어 AF와 AS는 낮은 소비량 구간에 값이 많이 몰려 있는 반면, EU는 상대적으로 높은 범위까지 값이 넓게 분포합니다.
💡 
  각 패널의 축 범위가 서로 다르면 그래프 모양만 보고 집단 간 크기를 직접 비교하기 어렵습니다. 공정한 비교가 필요할 때는 다음처럼 축 범위를 공유합니다.

### sharex, sharey: 같은 축으로 대륙 비교하기
```Python
# x축과 y축 범위를 모두 동일하게 맞춤

drinks.hist(column='beer', 
            by='continent', 
            sharex=True,     # x 축 공유
            sharey=True,     # y 축 공유
            layout=(2, 3),   # 2 x 3으로 레이아웃 변경
            figsize=(12, 6)  # 가로 12, 세로 6 인치
            )

plt.savefig('image/1_4.png')
```
실행 결과
matplotlib_histogram_1_4.svg
💡 
  sharex=True는 모든 그래프의 x축 범위를 동일하게 하고, sharey=True는 y축 범위를 동일하게 합니다. 이렇게 하면 대륙별 beer 소비량의 위치와 빈도 차이를 같은 기준으로 직접 비교할 수 있습니다. layout=(2, 3)은 6개의 그래프를 2행 × 3열로 배치합니다.
💡 
  Histogram 핵심 정리
  1. hist(column='변수')로 수치형 변수의 분포를 그린다.
  1. bins는 데이터를 몇 개 구간으로 나눌지 결정한다.
  1. plt.style.use()로 전체 그래프 스타일을 변경할 수 있다.
  1. by='그룹변수'로 집단별 Histogram을 한 번에 비교한다.
  1. sharex=True, sharey=True를 사용하면 모든 패널을 같은 축 기준으로 비교할 수 있다.
  1. figsize와 layout으로 여러 그래프의 크기와 배치를 조절한다.

## 3. Scatter plot: 두 수치형 변수의 관계
Scatter plot은 두 수치형 변수 사이의 관계를 점으로 표시합니다.
```Python
# select the beer and wine columns and sort by beer
drinks[['beer', 'wine']].sort_values(by='beer')
```
실행 결과
```Plain Text
     beer  wine
0       0     0
13      0     0
40      0    74
46      0     0
111     0     0
..    ...   ...
98    343    56
65    346   175
62    347    59
45    361   134
117   376     1

[193 rows x 2 columns]
```
```Python
drinks.plot(kind='scatter', x='beer', y='wine')
```
실행 결과
2_1.png
```Python
drinks.plot(kind='scatter',
            x='beer',
            y='wine',
            s='spirit',         # spirit 값에 따라 점 크기 변화
            c='pure',           # pure 값에 따라 컬러 변화
            colormap='PiYG',    # 컬러팔레트 적용
            alpha=0.3,          # 투명도
            figsize=(10, 8),    # 이미지 크기
            )
```
실행 결과
2_2.png
💡 
  점이 많이 겹치는 데이터에서는 alpha를 낮추면 겹침이 많은 영역이 더 진하게 보이므로 데이터 밀도를 파악하기 쉽습니다.
💡 
  연속적으로 증가하는 값에는 Blues 같은 순차형 colormap, 기준값을 중심으로 양·음 방향을 비교할 때는 PiYG 같은 발산형 colormap이 적합합니다.
💡 
  2차원 좌표에 점의 크기까지 사용하면 하나의 그래프에서 세 개의 수치형 변수를 동시에 표현할 수 있습니다.
Matplotlib은 값을 색상에 대응시키는 다양한 Color map을 제공합니다. https://matplotlib.org/stable/tutorials/colors/colormaps.html
```Python
# scatter matrix of three numerical columns
pd.plotting.scatter_matrix(drinks[['beer', 'spirit', 'wine']])
```
실행 결과
2_3.png
💡 
  Scatter matrix는 여러 수치형 변수를 한꺼번에 탐색할 때 유용합니다. 어떤 변수 조합에 관계가 강한지 빠르게 찾을 수 있습니다.

## 4. Bar plot: 범주별 값 비교
Bar plot은 서로 다른 범주의 개수나 대표값을 비교할 때 사용합니다.

### 대륙별 국가 수
```Python
# count the number of countries in each continent
drinks.continent.value_counts()
```
실행 결과
```Plain Text
continent
AF    53
EU    45
AS    44
NA    23
OC    16
SA    12
Name: count, dtype: int64
```
```Python
# AF, EU, AS, NA, OC, SA의 국가 수를 막대 높이로 비교하는 Bar plot 출력
drinks.continent.value_counts().plot(kind='bar')
```
실행 결과
3_1.png
💡 
  이 그래프에서는 아프리카(AF)가 53개로 가장 많고 남아메리카(SA)가 12개로 가장 적다는 사실을 막대 길이로 빠르게 비교할 수 있습니다.

### 대륙별 평균 소비량
```Python
# 대륙별 평균 소비량 계산
drink_continent=drinks.groupby(['continent'])[['beer',
                                               'spirit',
                                               'wine',
                                               'pure']].agg(['mean']).droplevel(axis=1,level=1).reset_index()
drink_continent
```
실행 결과
```Plain Text
  continent        beer      spirit        wine      pure
0        AF   61.471698   16.339623   16.264151  3.007547
1        AS   37.045455   60.840909    9.068182  2.170455
2        EU  193.777778  132.555556  142.222222  8.617778
3        NA  145.434783  165.739130   24.521739  5.995652
4        OC   89.687500   58.437500   35.625000  3.381250
5        SA  175.083333  114.750000   62.416667  6.308333
```
💡 
  groupby('continent')로 대륙별로 묶은 뒤 네 수치형 열의 평균을 계산했습니다. droplevel()은 집계 과정에서 생긴 다중 열 이름 중 mean 레벨을 제거합니다.
```Python
# side-by-side bar plots
drink_continent.plot(kind='bar', x='continent')
```
실행 결과
3_2.png
```Python
# stacked bar plots
drink_continent.plot(kind='bar', x='continent', stacked=True)

```
실행 결과
3_3.png
💡 
  나란한 막대는 각 항목의 값을 직접 비교하기 좋고, 누적 막대는 항목의 합과 구성 비율을 함께 보여주는 데 유리합니다.

## 5. Box plot: 사분위수와 이상치
Box plot은 데이터의 중앙값, 사분위수, 범위와 이상치를 압축해서 보여줍니다.
  | 통계량 | 의미 |
  | Min | 최솟값 |
  | Q1 · 25% | 하위 25% 지점 |
  | Q2 · 50% | 중앙값(Median) |
  | Q3 · 75% | 하위 75% 지점 |
  | Max | 최댓값 |
IQR(Interquartile Range) = Q3 − Q1
일반적으로 Q1 − 1.5 × IQR보다 작거나 Q3 + 1.5 × IQR보다 큰 값은 Box plot에서 이상치 후보로 별도 표시됩니다.

### spirit 분포 확인
```Python
# sort the spirit column
drinks.spirit.sort_values(ascending=True)
```
실행 결과
```Plain Text
0        0
2        0
13       0
19       0
27       0
      ... 
144    315
141    326
73     326
15     373
68     438
Name: spirit, Length: 193, dtype: int64
```
```Python
# show "five-number summary" for spirit
drinks.spirit.describe()
```
실행 결과
```Plain Text
count    193.000000
mean      80.994819
std       88.284312
min        0.000000
25%        4.000000
50%       56.000000
75%      128.000000
max      438.000000
Name: spirit, dtype: float64
```
💡 
  spirit의 중앙값은 56, Q1은 4, Q3는 128입니다. 따라서 IQR은 124입니다. Box plot은 평균 80.99보다 중앙값이 낮고 큰 값 쪽 꼬리가 긴 분포 특성을 시각적으로 확인하는 데 적합합니다.
```Python
# compare with box plot
drinks.boxplot(column='spirit', figsize=(5, 5))

plt.savefig('image/4_1.png')
```
실행 결과
matplotlib_box_spirit.svg
💡 
  상자는 Q1~Q3, 상자 안의 선은 중앙값(56), 수염 밖의 점은 이상치 후보입니다. figsize=(5, 5)로 정사각형 그래프를 만들었습니다.
```Python
# include multiple variables
drinks.drop('pure', axis=1).plot(kind='box')
```
실행 결과
```Plain Text
beer, spirit, wine 수치형 열의 Box plot을 한 그래프에서 비교
```
```Python
# box plot of spirit servings grouped by continent
drinks.boxplot(column='spirit', by='continent', figsize=(10, 10))

plt.savefig('image/4_2.png')
```
실행 결과
matplotlib_box_spirit_continent.svg
💡 
  대륙별 spirit 소비량의 중앙값·IQR·이상치를 같은 축에서 비교합니다. 북아메리카(NA)와 유럽(EU)은 중앙값이 상대적으로 높고, 여러 대륙에서 큰 값의 이상치가 확인됩니다.
```Python
# box plot of all numeric columns grouped by continent
drinks.boxplot(by='continent', figsize=(10, 10))

plt.savefig('image/4_3.png')
```
실행 결과
4_3.png
💡 
  beer, pure, spirit, wine 네 수치형 변수를 대륙별 Box plot으로 한 번에 비교합니다. 변수마다 값의 규모가 다르므로 각 패널의 분포 형태와 중앙값을 중심으로 읽는 것이 좋습니다.
💡 
  평균만 비교하면 극단값의 영향을 많이 받을 수 있습니다. 분포가 비대칭이거나 이상치가 있는 데이터에서는 Box plot과 중앙값을 함께 확인하는 것이 좋습니다.

## 6. Line plot: 시간에 따른 추세
시간 데이터에서는 x축에 시간, y축에 관측값을 두는 Line plot이 변화 추세를 보여주기 좋습니다.

### UFO 데이터 불러오기
```Python
# read in the ufo data
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/ufo.csv'
ufo = pd.read_csv(url)
ufo['Time'] = pd.to_datetime(ufo.Time)
ufo['YearMonth'] = ufo.Time.dt.to_period('M')
ufo
```
노트북에 저장된 실행 결과
```Plain Text
                       City Colors Reported Shape Reported State                Time  Year
0                    Ithaca             NaN       TRIANGLE    NY 1930-06-01 22:00:00  1930
1               Willingboro             NaN          OTHER    NJ 1930-06-30 20:00:00  1930
2                   Holyoke             NaN           OVAL    CO 1931-02-15 14:00:00  1931
3                   Abilene             NaN           DISK    KS 1931-06-01 13:00:00  1931
4      New York Worlds Fair             NaN          LIGHT    NY 1933-04-18 19:00:00  1933
...                     ...             ...            ...   ...                 ...   ...
80542              Loughman             NaN          LIGHT    FL 2014-09-05 05:30:00  2014

[80543 rows x 6 columns]
```
💡 
  문자열이었던 Time을 pd.to_datetime()으로 날짜·시간 자료형으로 변환한 뒤 .dt.year로 연도만 추출해 새 열 Year를 만들었습니다.
```Python
ufo.dtypes
```
실행 결과
```Plain Text
City                          str
Colors Reported               str
Shape Reported                str
State                         str
Time               datetime64[us]
YearMonth               period[M]
dtype: object
```
```Python
# 월별 UFO 목격 횟수
ufo_count = ufo.YearMonth.value_counts().sort_index()

# 1970년 1월 이후만 추출
ufo_count_after_1970 = ufo_count[
    ufo_count.index >= pd.Period('1970-01', freq='M')
]

ufo_count_after_1970
```
실행 결과
```Plain Text
Year
1930       2
1931       2
1933       1
1934       1
1935       1
        ...
2010    4154
2011    5089
2012    7263
2013    7003
2014    5382
Name: count, Length: 82, dtype: int64
```
💡 
  value_counts()는 빈도순으로 정렬하므로 시간 추세 그래프를 그릴 때는 sort_index()로 월 순서를 다시 맞추는 것이 중요합니다. 여기서는 pd.Period('1970-01', freq='M') 조건으로 1970년 1월 이후 데이터만 선택했습니다.
```Python
# compare with line plot
# 선그래프로 시각화
ufo_count_after_1970.plot.line(
    xlabel='Year',
    ylabel='Count',
    title='UFO Sightings by Year',
    figsize=(20, 10)
)

plt.savefig('image/5_1.png')
```
실행 결과
matplotlib_ufo_line.svg
💡 
  1970년 1월 이후의 월별 UFO 신고 건수를 시간 순서대로 연결한 Line plot입니다. YearMonth를 사용해 월 단위 변화를 유지했기 때문에 연도별 집계보다 더 세밀한 추세와 급증 구간을 확인할 수 있습니다.
💡 
  그래프의 목적은 장식이 아니라 정보를 정확하게 전달하는 것입니다. Marker·Line·Color는 데이터 그룹을 구분하거나 중요한 값을 강조할 때 사용하고, 지나치게 많은 스타일을 한 그래프에 섞지 않는 것이 좋습니다.

### 자주 쓰는 스타일 옵션
  | 옵션 | 역할 | 예 |
  | marker | 점의 모양 | 'o', '^', 's' |
  | linestyle | 선 모양 | '-', '--', ':' |
  | linewidth | 선 굵기 | 2 |
  | alpha | 투명도 | 0.3 |
  | s | Scatter 점 크기 | 50 또는 열 이름 |
  | c / color | 색상 | 'blue' 또는 수치형 열 |
  | figsize | Figure 크기 | (10, 8) |
  | colormap | 수치값을 색상에 대응 | 'Blues', 'PiYG' |

## 7. 어떤 그래프를 선택할까?
  | 질문 | 대표 코드 | 추천 그래프 |
  | 하나의 숫자 변수가 어떻게 분포되어 있는가? | plot(kind='hist') | Histogram / Density |
  | 두 숫자 변수 사이에 관계가 있는가? | plot(kind='scatter') | Scatter plot |
  | 범주별 값이 얼마나 다른가? | plot(kind='bar') | Bar plot |
  | 중앙값·사분위수·이상치를 비교하고 싶은가? | plot(kind='box') | Box plot |
  | 시간에 따라 값이 어떻게 변하는가? | plot() | Line plot |
💡 
  핵심 정리
  1. 먼저 분석 질문이 분포·관계·비교·추세 중 무엇인지 정한다.
  1. 목적에 맞는 그래프 종류를 선택한다.
  1. 제목과 축 이름을 명확히 적는다.
  1. 여러 집단을 비교할 때는 축 범위를 통일한다.
  1. 투명도·크기·색상은 데이터를 더 잘 설명할 때만 사용한다.
  1. 필요한 그래프는 plt.savefig()로 저장해 보고서나 웹앱에서 재사용한다.
💡 
  연습 문제
  - drinks.wine의 Histogram을 bins=10, 20, 40으로 각각 그려 분포가 어떻게 달라 보이는지 비교하세요.
  - beer와 spirit의 Scatter plot을 만들고 wine을 점 크기 또는 색상으로 표현하세요.
  - 대륙별 wine 평균을 Bar plot으로 표현하세요.
  - 대륙별 spirit Box plot을 그리고 중앙값과 이상치를 비교하세요.
  - UFO 연도별 신고 건수 그래프에 제목, x축 이름, y축 이름을 추가한 뒤 PNG로 저장하세요.
---
💡 
  이전 강의: 05 : API
💡 
  다음 강의: 07 : Plotly