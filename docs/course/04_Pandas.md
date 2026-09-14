
# 04 : Pandas
> Pandas로 표 형태의 데이터를 선택·정리·요약·변환·결합하기
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - Pandas의 Series와 DataFrame을 만들고 구조를 이해한다.
  - loc·iloc과 조건식을 이용해 필요한 행과 열을 선택한다.
  - CSV 데이터를 불러와 결측치 처리, 정렬, 파생변수 생성을 수행한다.
  - groupby()로 그룹별 통계를 계산하고 범주형 변수를 만든다.
  - wide_to_long·melt로 데이터 구조를 바꾸고 merge·concat으로 여러 표를 결합한다.

## 0. 실습 준비: Pandas
Pandas는 행과 열로 구성된 표 형태의 데이터를 다루는 Python 라이브러리입니다.
```Python
import numpy as np
import pandas as pd
```
실행 결과

## 1. Series와 DataFrame

### Series
Series는 값(value) 과 각 값을 구분하는 인덱스(index) 로 이루어진 1차원 자료구조입니다.
```Python
a = [1, 2, 3, 4, 5]
a_series = pd.Series(a)

print(a_series)
```
실행 결과
```Plain Text
0    1
1    2
2    3
3    4
4    5
dtype: int64
```
💡 
  왼쪽의 0~4는 index이고 오른쪽의 1~5는 실제 값입니다.

### DataFrame
DataFrame은 행을 index, 열을 column 이름으로 구분하는 2차원 표입니다.
```Python
raw_data = {
    "col0": [1, 2, 3, 4, 5],
    "col1": [10, 20, 30, 40, 50],
    "col2": [100, 200, 300, 400, 500]
}

df = pd.DataFrame(raw_data)
df
```
실행 결과
```Plain Text
   col0  col1  col2
0     1    10   100
1     2    20   200
2     3    30   300
3     4    40   400
4     5    50   500
```
💡 
  DataFrame에서는 행을 index로, 열을 column 이름으로 구분합니다.
DataFrame의 한 열을 선택하면 Series가 됩니다.
```Python
df["col0"]
df.col1
```
실행 결과
```Plain Text
0    10
1    20
2    30
3    40
4    50
Name: col1, dtype: int64
```
💡 
  Jupyter Notebook에서는 한 셀의 마지막 표현식만 자동 출력되므로 위 코드에서는 df.col1의 결과가 보입니다. df["col0"]도 같은 방식의 Series입니다.

### 열 추가와 삭제
```Python
new = ["딸기", "당근", "수박", "참외", "메론"]
df["new column"] = new

df
```
실행 결과
```Plain Text
   col0  col1  col2 new column
0     1    10   100         딸기
1     2    20   200         당근
2     3    30   300         수박
3     4    40   400         참외
4     5    50   500         메론
```
💡 
  새로운 리스트를 열 이름에 대입하면 DataFrame에 새 열이 추가됩니다.
```Python
del df["col2"]
df
```
실행 결과
```Plain Text
   col0  col1 new column
0     1    10         딸기
1     2    20         당근
2     3    30         수박
3     4    40         참외
4     5    50         메론
```
💡 
  del은 지정한 열을 원본 DataFrame에서 바로 삭제합니다.
```Python
df_without_new = df.drop("new column", axis=1)
df_without_new
```
실행 결과
```Plain Text
   col0  col1
0     1    10
1     2    20
2     3    30
3     4    40
4     5    50
```
💡 
  drop(..., axis=1)은 열을 제외한 새 DataFrame을 만들 수 있습니다. 별도로 저장하면 원본 df는 유지됩니다.

## 2. loc과 iloc으로 데이터 선택하기
  | 기준 | 명령어 | 예 |
  | 인덱스·열 이름(label) | loc | df.loc[1:4, ["col0"]] |
  | 실제 위치(integer position) | iloc | df.iloc[[1, 3], [0, 2]] |
```Python
df.loc[3]
df.loc[1, ["col0"]]
df.loc[1:4, :]
df.loc[:, ["col0", "new column"]]
df.loc[[1, 2, 4], ["col1", "new column"]]
```
실행 결과 (마지막 표현식)
```Plain Text
   col1 new column
1    20         당근
2    30         수박
4    50         메론
```
💡 
  loc은 행의 index와 열 이름을 기준으로 선택합니다. 한 셀에 여러 표현식이 있으면 마지막 표현식의 결과만 자동으로 표시됩니다.
```Python
df.loc[:, ["new column", "col1", "col0"]]
```
실행 결과
```Plain Text
  new column  col1  col0
0         딸기    10     1
1         당근    20     2
2         수박    30     3
3         참외    40     4
4         메론    50     5
```
💡 
  열 이름의 순서를 바꾸면 결과 DataFrame의 열 순서도 그대로 바뀝니다.
```Python
df.iloc[[1, 3], [0, 2]]
```
실행 결과
```Plain Text
   col0 new column
1     2         당근
3     4         참외
```
💡 
  iloc은 이름이 아니라 0부터 시작하는 실제 행·열 위치를 사용합니다.
```Python
df.T
```
실행 결과
```Plain Text
             0   1   2   3   4
col0         1   2   3   4   5
col1        10  20  30  40  50
new column  딸기  당근  수박  참외  메론
```
💡 
  .T는 행과 열을 서로 바꾸는 전치(transpose) 연산입니다.

## 3. 조건 필터링과 파생변수
```Python
condition = (df["col1"] <= 30) & (df["new column"] == "딸기")
print(condition)
```
실행 결과
```Plain Text
0     True
1    False
2    False
3    False
4    False
dtype: bool
```
💡 
  각 행마다 조건을 만족하는지 검사하기 때문에 True/False가 행 수만큼 만들어집니다.
```Python
df["buy"] = (df["col1"] <= 30) & (df["new column"] == "딸기")
df
```
실행 결과
```Plain Text
   col0  col1 new column    buy
0     1    10         딸기   True
1     2    20         당근  False
2     3    30         수박  False
3     4    40         참외  False
4     5    50         메론  False
```
💡 
  조건식의 결과를 새 열에 저장하면 각 행의 조건 충족 여부를 파생변수로 만들 수 있습니다.
- AND 조건: &
- OR 조건: |
- 여러 조건을 결합할 때는 각각의 조건을 괄호로 감쌉니다.

## 4. CSV 불러오기와 실제 데이터 선택
```Python
flight_data = pd.read_csv("data/nycflights13.csv")
flight_data[["origin", "dest", "hour", "distance", "arr_delay"]].head()
```
실행 결과
```Plain Text
  origin dest  hour  distance  arr_delay
0    EWR  IAH     5      1400       11.0
1    LGA  IAH     5      1416       20.0
2    JFK  MIA     5      1089       33.0
3    JFK  BQN     5      1576      -18.0
4    LGA  ATL     6       762      -25.0
```
💡 
  전체 데이터는 336,776행 × 16열이므로 핵심 열의 앞부분만 확인합니다.
```Python
flight_data.loc[:, ["origin", "dest", "hour"]]
```
실행 결과
```Plain Text
       origin dest  hour
0         EWR  IAH     5
1         LGA  IAH     5
2         JFK  MIA     5
3         JFK  BQN     5
4         LGA  ATL     6
...       ...  ...   ...
336775    LGA  RDU     8

[336776 rows x 3 columns]
```
💡 
  행 수는 그대로 유지하면서 세 열만 선택했습니다.
```Python
new_df = flight_data.loc[
    flight_data["origin"] == "LGA",
    ["origin", "dest", "hour"]
]

new_df
```
실행 결과
```Plain Text
       origin dest  hour
1         LGA  IAH     5
4         LGA  ATL     6
7         LGA  IAD     6
9         LGA  ORD     6
14        LGA  DFW     6
...       ...  ...   ...
336775    LGA  RDU     8

[104662 rows x 3 columns]
```
💡 
  LGA 출발 행만 남기면서 필요한 세 열을 동시에 선택했습니다.
```Python
flight_subset = new_df.drop(["hour"], axis=1).head()
flight_subset
```
실행 결과
```Plain Text
   origin dest
1     LGA  IAH
4     LGA  ATL
7     LGA  IAD
9     LGA  ORD
14    LGA  DFW
```
💡 
  hour 열을 제거한 뒤 앞의 5행만 확인했습니다.

### 여러 조건으로 행 필터링
```Python
flight_data[
    (flight_data["month"] == 1) &
    (flight_data["day"] == 1) &
    (flight_data["origin"] == "JFK") &
    (flight_data["hour"] > 10)
]
```
실행 결과 (요약)
```Plain Text
     year  month  day  dep_time  ...  distance  hour  minute
151  2013      1    1     848.0  ...       184    18      35
258  2013      1    1    1059.0  ...       213    11       0
265  2013      1    1    1111.0  ...       266    11      15
266  2013      1    1    1112.0  ...      2586    11       0
272  2013      1    1    1124.0  ...      2586    11       0
..    ...    ...  ...       ...  ...       ...   ...     ...
832  2013      1    1    2326.0  ...      2248    21      30
833  2013      1    1    2327.0  ...       209    22      50
835  2013      1    1    2353.0  ...      1617    23      59
836  2013      1    1    2353.0  ...      1598    23      59
837  2013      1    1    2356.0  ...      1576    23      59

[213 rows x 16 columns]
```
💡 
  &로 연결한 모든 조건을 만족하는 항공편만 남습니다.
```Python
flight_data[
    (flight_data["month"] == 1) |
    (flight_data["origin"] == "JFK") |
    (flight_data["origin"] == "LGA")
]
```
실행 결과 (요약)
```Plain Text
        year  month  day  dep_time  ...  distance  hour  minute
0       2013      1    1     517.0  ...      1400     5      15
1       2013      1    1     533.0  ...      1416     5      29
2       2013      1    1     542.0  ...      1089     5      40
3       2013      1    1     544.0  ...      1576     5      45
4       2013      1    1     554.0  ...       762     6       0
...      ...    ...  ...       ...  ...       ...   ...     ...
336771  2013      9   30       NaN  ...       213    14      55
336772  2013      9   30       NaN  ...       198    22       0
336773  2013      9   30       NaN  ...       764    12      10
336774  2013      9   30       NaN  ...       419    11      59
336775  2013      9   30       NaN  ...       431     8      40

[225834 rows x 16 columns]
```
💡 
  |는 조건 중 하나라도 참이면 행을 남기므로 AND보다 많은 행이 선택됩니다.

## 5. 결측치, 정렬, 새 열 만들기

### 결측치 확인과 처리
```Python
flight_data["arr_delay"].isna().sum()
```
실행 결과
```Plain Text
9430
```
💡 
  arr_delay 열에는 9,430개의 결측치가 있습니다.
```Python
flight_data.loc[flight_data["arr_delay"].isna(), :]
```
실행 결과 (요약)
```Plain Text
        year  month  day  dep_time  ...  distance  hour  minute
471     2013      1    1    1525.0  ...      1147    15      30
477     2013      1    1    1528.0  ...       872    14      59
615     2013      1    1    1740.0  ...      1147    17      45
643     2013      1    1    1807.0  ...      2425    17      38
725     2013      1    1    1939.0  ...      1391    18      40
...      ...    ...  ...       ...  ...       ...   ...     ...
336771  2013      9   30       NaN  ...       213    14      55
336772  2013      9   30       NaN  ...       198    22       0
336773  2013      9   30       NaN  ...       764    12      10
336774  2013      9   30       NaN  ...       419    11      59
336775  2013      9   30       NaN  ...       431     8      40

[9430 rows x 16 columns]
```
💡 
  결측치가 있는 행만 선택합니다.
```Python
flight_data.loc[flight_data["arr_delay"].notna(), :]
```
실행 결과 (요약)
```Plain Text
        year  month  day  dep_time  ...  distance  hour  minute
0       2013      1    1     517.0  ...      1400     5      15
1       2013      1    1     533.0  ...      1416     5      29
2       2013      1    1     542.0  ...      1089     5      40
3       2013      1    1     544.0  ...      1576     5      45
4       2013      1    1     554.0  ...       762     6       0
...      ...    ...  ...       ...  ...       ...   ...     ...
336765  2013      9   30    2240.0  ...       209    22      45
336766  2013      9   30    2240.0  ...       301    22      50
336767  2013      9   30    2241.0  ...       264    22      46
336768  2013      9   30    2307.0  ...       187    22      55
336769  2013      9   30    2349.0  ...      1617    23      59

[327346 rows x 16 columns]
```
💡 
  notna()는 결측치가 아닌 행만 선택합니다.
```Python
flight_data["arr_delay"] = flight_data["arr_delay"].fillna(0)
print(flight_data["arr_delay"].isna().sum())
```
실행 결과
```Plain Text
0
```
💡 
  결측치를 무조건 0으로 바꾸면 분석 결과가 달라질 수 있습니다. 0이 실제 의미를 갖는 값인지 확인한 뒤 처리 방법을 결정하세요.

### 행 정렬하기
```Python
flight_data.sort_values(
    by=["distance", "hour"],
    ascending=True
).head()
```
실행 결과 (핵심 열)
```Plain Text
       origin dest  distance  hour
275945    EWR  LGA        17     1
3083      EWR  PHL        80    12
3901      EWR  PHL        80    12
3426      EWR  PHL        80    16
10235     EWR  PHL        80    16
```
💡 
  먼저 distance, 그다음 hour 순서로 오름차순 정렬합니다.

### 파생변수 만들기
```Python
df = flight_data.copy()

df["new_distance"] = df["distance"] / 1000
df["carrier_origin"] = df["carrier"] + df["origin"]

df
```
실행 결과 (관련 열 앞 5행)
```Plain Text
  carrier origin  distance  new_distance carrier_origin
0      UA    EWR      1400         1.400          UAEWR
1      UA    LGA      1416         1.416          UALGA
2      AA    JFK      1089         1.089          AAJFK
3      B6    JFK      1576         1.576          B6JFK
4      DL    LGA       762         0.762          DLLGA
```
💡 
  기존 열을 계산하거나 결합해 만든 새 열을 파생변수라고 합니다.

## 6. groupby로 그룹별 요약하기
```Python
flight_data.groupby("origin")["distance"].agg(["mean"])
```
실행 결과
```Plain Text
               mean
origin
EWR     1056.742790
JFK     1266.249077
LGA      779.835671
```
💡 
  출발 공항별로 행을 묶고 평균 비행거리를 계산했습니다.
```Python
flight_data.groupby("origin")["distance"].agg(
    mean_dist="mean"
).reset_index()
```
실행 결과
```Plain Text
  origin    mean_dist
0    EWR  1056.742790
1    JFK  1266.249077
2    LGA   779.835671
```
💡 
  reset_index()를 사용하면 그룹 기준인 origin을 일반 열로 되돌릴 수 있습니다.
```Python
flight_data.groupby("origin")["distance"].agg(
    dist_mean="mean",
    dist_first="first"
).reset_index()
```
실행 결과
```Plain Text
  origin    dist_mean  dist_first
0    EWR  1056.742790        1400
1    JFK  1266.249077        1089
2    LGA   779.835671        1416
```
💡 
  한 열에 여러 통계량을 동시에 적용할 수 있습니다.
```Python
flight_data.groupby(["origin", "dest"])["distance"].agg(
    mean_distance="mean",
    sum_distance="sum"
).reset_index()
```
실행 결과 (앞 5행)
```Plain Text
  origin dest  mean_distance  sum_distance
0    EWR  ALB          143.0         62777
1    EWR  ANC         3370.0         26960
2    EWR  ATL          746.0       3746412
3    EWR  AUS         1504.0       1455872
4    EWR  AVL          583.0        154495
```
💡 
  origin과 dest의 조합을 하나의 그룹으로 보고 통계를 계산합니다.
```Python
new_df = flight_data.groupby(["origin", "dest"]).agg(
    dist_mean=("distance", "mean"),
    dist_sum=("distance", "sum"),
    delay_mean=("arr_delay", "mean")
).reset_index()

new_df
```
실행 결과 (앞 5행)
```Plain Text
  origin dest  dist_mean  dist_sum  delay_mean
0    EWR  ALB      143.0     62777   13.708428
1    EWR  ANC     3370.0     26960   -2.500000
2    EWR  ATL      746.0   3746412   12.848467
3    EWR  AUS     1504.0   1455872   -0.469008
4    EWR  AVL      583.0    154495    8.339623
```
💡 
  Named aggregation을 사용하면 서로 다른 열에 서로 다른 집계 함수를 적용하면서 결과 열 이름도 지정할 수 있습니다.

## 7. 범주형 변수 만들기

### 조건에 따라 범주 매핑하기
```Python
class_A = ["UA", "AA", "B6", "DL", "EV", "MQ", "US"]
class_B = ["WN", "VX", "FL", "AS", "9E", "F9", "HA", "YV", "OO"]

conditions = [
    flight_data["carrier"].isin(class_A),
    flight_data["carrier"].isin(class_B)
]
choices = ["A", "B"]

flight_data["carrier_class"] = np.select(
    conditions,
    choices,
    default="Other"
)

flight_data[["carrier", "carrier_class"]].sample(10)
```
실행 결과 예시 (sample()이므로 행은 달라질 수 있음)
```Plain Text
carrier carrier_class
DL      A
US      A
9E      B
UA      A
AA      A
```
💡 
  isin()과 np.select()를 이용하면 여러 코드를 원하는 범주로 묶을 수 있습니다.
```Python
flight_data.loc[
    flight_data["carrier"] == "UA",
    "carrier_class"
] = "B"
```
실행 결과
```Plain Text
(화면 출력 없음)
```
💡 
  대입문이므로 자동 출력은 없지만 UA 행의 carrier_class가 B로 수정됩니다.

### 연속형 값을 구간으로 나누기
```Python
bins = [0, 502, 872, 1389, np.inf]
labels = ["very_short", "short", "long", "very_long"]

flight_data["distance_class"] = pd.cut(
    flight_data["distance"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

flight_data[["distance", "distance_class"]].sample(10)
```
실행 결과 예시
```Plain Text
distance distance_class
1047     long
2133     very_long
169      very_short
738      short
```
💡 
  연속형 숫자인 거리를 네 개의 범주로 나눴습니다.

## 8. 데이터 구조 바꾸기: Wide → Long

### wide_to_long
```Python
data = {
    "id": [1, 2],
    "A2020": [100, 200],
    "A2021": [120, 220],
    "B2020": [15, 25],
    "B2021": [18, 28]
}

df = pd.DataFrame(data)

df
```
실행 결과
```Plain Text
   id  A2020  A2021  B2020  B2021
0   1    100    120     15     18
1   2    200    220     25     28
```
💡 
  현재 데이터는 한 행이 하나의 id를 나타내고, 변수명과 연도(A2020, A2021 등)가 각각의 열 이름에 함께 들어 있는 wide 형식입니다.
```Python
long = pd.wide_to_long(
    df,
    stubnames=["A", "B"],
    i="id",
    j="year"
).reset_index()

long
```
실행 결과
```Plain Text
   id  year    A   B
0   1  2020  100  15
1   2  2020  200  25
2   1  2021  120  18
3   2  2021  220  28
```
💡 
  열 이름에 들어 있던 연도가 year 열로 내려오면서 long 형식이 되었습니다.
```Python
df = pd.DataFrame({
    "famid": [1, 1, 2, 2],
    "birth": [1, 2, 1, 2],
    "ht1": [50, 48, 52, 51],
    "ht2": [80, 76, 82, 81]
})

result = pd.wide_to_long(
    df,
    stubnames="ht",
    i=["famid", "birth"],
    j="age"
).reset_index()

result
```
실행 결과
```Plain Text
   famid  birth  age  ht
0      1      1    1  50
1      1      1    2  80
2      1      2    1  48
3      1      2    2  76
4      2      1    1  52
5      2      1    2  82
6      2      2    1  51
7      2      2    2  81
```
💡 
  식별자가 여러 개라면 i=[...]처럼 리스트로 지정할 수 있습니다.

### melt
```Python
df = pd.DataFrame({
    "date": ["05/03", "06/03", "07/03", "08/03"],
    "AA": [1, 4, 7, 5],
    "BB": [2, 5, 8, 7],
    "CC": [3, 6, 9, 1]
})

df
```
실행 결과
```Plain Text
    date  AA  BB  CC
0  05/03   1   2   3
1  06/03   4   5   6
2  07/03   7   8   9
3  08/03   5   7   1
```
💡 
  date는 각 행을 식별하는 기준 열이고, AA, BB, CC는 날짜별 관측값이 담긴 열입니다. melt()를 사용하면 세 관측값 열을 변수명과 값으로 나눠 long 형식으로 바꿀 수 있습니다.
```Python
long_df = pd.melt(
    df,
    id_vars="date",
    value_vars=["AA", "BB", "CC"]
)

long_df
```
실행 결과
```Plain Text
      date variable  value
0    05/03       AA      1
1    06/03       AA      4
2    07/03       AA      7
3    08/03       AA      5
4    05/03       BB      2
...
```
💡 
  AA·BB·CC라는 여러 열이 variable과 value 두 열로 정리되었습니다.

## 9. 데이터 결합: merge와 concat

### merge: 공통 키로 열을 결합하기
```Python
flight_data_reset = flight_data.copy()
flight_data_reset["id"] = range(1, len(flight_data_reset) + 1)

flight_distance = flight_data_reset.loc[
    flight_data_reset["carrier"].isin(["DL", "AA"]),
    ["id", "carrier", "distance"]
]

flight_time = flight_data_reset.loc[
    flight_data_reset["carrier"].isin(["AA"]),
    ["id", "carrier", "air_time"]
]

print(flight_distance.head())
print(flight_time.head())
```
실행 결과
```Plain Text
# flight_distance의 앞 5행
    id carrier  distance
2    3      AA      1089
4    5      DL       762
9   10      AA       733
14  15      AA      1389
20  21      DL      1020

# flight_time의 앞 5행
    id carrier  air_time
2    3      AA     160.0
9   10      AA     138.0
14  15      AA     257.0
22  23      AA     152.0
31  32      AA     153.0
```
💡 
  전체 항공편에 고유한 공통 키 id를 만든 뒤 두 DataFrame을 준비했습니다. flight_distance에는 AA와 DL 항공편의 거리, flight_time에는 AA 항공편의 비행시간이 들어 있습니다. 왼쪽 숫자는 원본 DataFrame의 index이고, 실제 병합에는 id 열을 사용합니다.
  | 병합 방식 | 남기는 행 |
  | inner | 양쪽 모두에 키가 존재하는 행 |
  | left | 왼쪽 표의 모든 행 |
  | right | 오른쪽 표의 모든 행 |
  | outer | 양쪽 표에 있는 모든 키 |
```Python
flight_inner = pd.merge(
    flight_distance,
    flight_time,
    left_on="id",
    right_on="id",
    how="inner"
)

flight_inner.head()
```
실행 결과
```Plain Text
   id carrier_x  distance carrier_y  air_time
0   3        AA      1089        AA     160.0
1  10        AA       733        AA     138.0
2  15        AA      1389        AA     257.0
3  23        AA      1085        AA     152.0
4  32        AA      1096        AA     153.0
```
💡 
  inner join은 양쪽에 id가 모두 존재하는 행만 남깁니다.
```Python
flight_left = pd.merge(
    flight_distance,
    flight_time,
    left_on="id",
    right_on="id",
    how="left"
)

flight_left.head()
```
실행 결과
```Plain Text
   id carrier_x  distance carrier_y  air_time
0   3        AA      1089        AA     160.0
1   5        DL       762       NaN       NaN
2  10        AA       733        AA     138.0
3  15        AA      1389        AA     257.0
4  21        DL      1020       NaN       NaN
```
💡 
  left join은 왼쪽 DataFrame의 행을 모두 유지하고, 오른쪽에 대응되는 값이 없으면 NaN이 들어갑니다.

### concat: 같은 구조의 표를 위아래로 이어 붙이기
```Python
df1 = pd.DataFrame([
    ["A0", "A1", "A2", "A3"],
    ["B0", "B1", "B2", "B3"]
], columns=list("ABCD"))

df2 = pd.DataFrame([
    ["A4", "A5", "A6", "A7"],
    ["B4", "B5", "B6", "B7"]
], columns=list("ABCD"))

print(df1)
print(df2)
```
실행 결과
```Plain Text
# df1
    A   B   C   D
0  A0  A1  A2  A3
1  B0  B1  B2  B3

# df2
    A   B   C   D
0  A4  A5  A6  A7
1  B4  B5  B6  B7
```
💡 
  df1과 df2는 모두 A·B·C·D라는 같은 열 구조를 가지며 각각 두 행으로 구성됩니다. 따라서 concat()으로 두 표를 위아래 방향으로 자연스럽게 이어 붙일 수 있습니다.
```Python
result = pd.concat(
    [df1, df2],
    ignore_index=True
)

result
```
실행 결과
```Plain Text
    A   B   C   D
0  A0  A1  A2  A3
1  B0  B1  B2  B3
2  A4  A5  A6  A7
3  B4  B5  B6  B7
```
💡 
  ignore_index=True를 사용하면 이어 붙인 뒤 index를 0부터 다시 정리합니다.
💡 
  merge는 키를 기준으로 옆으로 결합, concat은 같은 구조의 데이터를 위아래로 이어 붙이기라고 기억하면 이해하기 쉽습니다.

## 실습 과제

### 과제 1. 항공편 데이터 분석 파이프라인
nycflights13.csv를 이용해 다음 분석을 순서대로 수행해 보세요.
1. hour가 10보다 큰 항공편만 필터링하고 .copy()로 별도 DataFrame을 만드세요.
1. speed = distance / air_time * 60 공식으로 속도 열을 추가하세요.
1. 출발 공항(origin)별 평균 속도를 계산하세요.
1. 평균 속도를 내림차순으로 정렬하세요.
```Python
filtered_data = flight_data[flight_data["hour"] > 10].copy()

# 여기에 speed 계산, groupby, 정렬 코드를 작성하세요
```
💡 
  hour > 10인 항공편을 복사해 실습용 DataFrame을 만드는 시작 코드입니다. 이후 코드는 직접 완성합니다.

## 핵심 정리
- Pandas의 Series는 1차원, DataFrame은 2차원 표 형태의 자료구조입니다.
- loc·iloc과 조건식을 사용하면 필요한 행과 열을 정교하게 선택할 수 있습니다.
- 결측치 처리, 정렬, 파생변수, groupby는 실제 데이터 전처리와 요약의 핵심 과정입니다.
- wide_to_long·melt는 데이터 구조를 바꾸고, merge·concat은 여러 데이터를 결합합니다.
- 정리된 데이터는 다음 단계의 시각화와 공간·시간 패턴 분석에 활용할 수 있습니다.
---
💡 
  이전 강의: 03 : NumPy
💡 
  다음 강의: 05 : API