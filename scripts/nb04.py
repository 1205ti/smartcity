import sys; sys.path.insert(0, "scripts")
from build_notebooks import build

c = []
c.append(("md", """# 04 : Pandas

강의자료: `docs/course/04_Pandas.md`

Series/DataFrame 구조를 익힌 뒤 뉴욕 항공편 33만 행으로 선택·결측치·정렬·파생변수·
groupby·구조변환·결합까지 전처리 전 과정을 한다.

## 데이터

`data/raw/nycflights13.csv` — 2013년 뉴욕 3개 공항(EWR/LGA/JFK) 출발 항공편 336,776건.
수업 실습 저장소(`https://github.com/jslee-gses/code`)에서 가져왔다.
강의자료에 원 출처 URL이 없어 강사 확인이 필요하다."""))

c.append(("code", "import numpy as np\nimport pandas as pd\n\npd.set_option('display.max_columns', 30)\npd.set_option('display.width', 160)"))

c.append(("md", "## 1. Series — 값 + 인덱스"))
c.append(("code", '''s = pd.Series([10, 20, 30, 40])
print(s)
print("\\n값:", s.values)
print("인덱스:", list(s.index))

# 인덱스를 직접 지정할 수도 있다
s2 = pd.Series([947, 335, 238], index=["서울", "부산", "대구"])
print("\\n", s2, sep="")
print("\\n서울:", s2["서울"])'''))

c.append(("md", "## 2. DataFrame 만들기와 열 선택"))
c.append(("code", '''data = {
    "도시": ["서울", "부산", "대구", "인천"],
    "인구": [947, 335, 238, 296],
    "면적": [605.2, 770.1, 883.5, 1063.3],
}
df = pd.DataFrame(data)
print(df)

print("\\n대괄호 방식:\\n", df["인구"], sep="")
print("\\n점 방식:", list(df.인구))   # 공백·특수문자 없는 열 이름에서만 쓸 수 있다'''))

c.append(("md", "## 3. 열 추가와 삭제"))
c.append(("code", '''df["인구밀도"] = (df["인구"] * 10000 / df["면적"]).round(1)
df["권역"] = ["수도권", "영남", "영남", "수도권"]
print(df)

df2 = df.drop("권역", axis=1)      # 원본을 두고 사본을 만든다
print("\\ndrop 후:\\n", df2, sep="")

del df["권역"]                      # 원본에서 바로 지운다
print("\\ndel 후 열:", list(df.columns))'''))

c.append(("md", """## 4. loc와 iloc

`loc`은 **라벨**로, `iloc`은 **정수 위치**로 고른다.
`loc`의 슬라이싱은 끝을 포함하고, `iloc`은 포함하지 않는다."""))
c.append(("code", '''print("loc[1] — 인덱스 라벨 1:\\n", df.loc[1], sep="")
print("\\niloc[0] — 첫 번째 행:\\n", df.iloc[0], sep="")

print("\\nloc[0:2] (끝 포함):\\n", df.loc[0:2, ["도시", "인구"]], sep="")
print("\\niloc[0:2] (끝 제외):\\n", df.iloc[0:2, 0:2], sep="")

print("\\n열 순서 바꾸기:\\n", df[["인구", "도시", "면적", "인구밀도"]], sep="")
print("\\n전치:\\n", df.T, sep="")'''))

c.append(("md", "## 5. 조건 필터링과 파생변수"))
c.append(("code", '''# 여러 조건은 & | 로 묶고 각 조건을 괄호로 감싼다
big = df[(df["인구"] > 300) & (df["면적"] < 800)]
print("인구 300만 초과 & 면적 800 미만:\\n", big, sep="")

# 조건 결과를 그대로 열로 저장할 수 있다
df["대도시"] = df["인구"] > 300
print("\\n", df, sep="")'''))

c.append(("md", "## 6. 실제 데이터 불러오기"))
c.append(("code", '''flights = pd.read_csv("data/raw/nycflights13.csv")
print("shape:", flights.shape)
print("\\n열 목록:", list(flights.columns))
flights.head()'''))

c.append(("code", '''core = flights[["year", "month", "day", "hour", "origin", "dest",
                "carrier", "air_time", "distance", "dep_delay"]]
core.head()'''))

c.append(("md", "## 7. loc 복합 선택과 다중 조건"))
c.append(("code", '''# 조건과 열을 한 번에 지정한다
sel = flights.loc[flights["month"] == 1, ["month", "day", "origin", "dest", "distance"]]
print("1월 항공편:", len(sel))
print(sel.head())

# AND
jfk_long = flights[(flights["origin"] == "JFK") & (flights["distance"] > 2000)]
print("\\nJFK 출발 & 2000마일 초과:", len(jfk_long))

# OR
ewr_or_lga = flights[(flights["origin"] == "EWR") | (flights["origin"] == "LGA")]
print("EWR 또는 LGA 출발:", len(ewr_or_lga))'''))

c.append(("md", "## 8. 결측치"))
c.append(("code", '''na_counts = flights.isna().sum()
print("결측치가 있는 열:\\n", na_counts[na_counts > 0], sep="")

print("\\nair_time이 빈 행:", flights["air_time"].isna().sum())
print("air_time이 있는 행:", flights["air_time"].notna().sum())

# 채우기 — 다만 air_time을 0으로 채우면 "비행시간 0분"이라는 잘못된 값이 된다.
# 여기서는 방법만 확인하고 실제 분석에는 notna()로 걸러 쓴다.
filled = flights["air_time"].fillna(0)
print("0으로 채운 뒤 결측:", filled.isna().sum())

clean = flights[flights["air_time"].notna()].copy()
print("결측 제거 후:", clean.shape)'''))

c.append(("md", "## 9. 정렬"))
c.append(("code", '''print("거리 긴 순:")
print(flights.sort_values(by="distance", ascending=False)
      [["origin", "dest", "distance"]].head())

print("\\n월·일 순:")
print(flights.sort_values(by=["month", "day"])[["month", "day", "origin"]].head())'''))

c.append(("md", "## 10. 파생변수"))
c.append(("code", '''f = flights.copy()

f["distance_km"] = (f["distance"] * 1.609344).round(1)   # 마일 → km
f["route"] = f["origin"] + "-" + f["dest"]               # 문자열 결합

print(f[["origin", "dest", "route", "distance", "distance_km"]].head())'''))

c.append(("md", "## 11. groupby"))
c.append(("code", '''print("출발공항별 거리 통계:")
print(flights.groupby("origin")["distance"].agg(["count", "mean", "min", "max"]).round(1))

print("\\n이름을 붙인 집계:")
print(flights.groupby("origin").agg(
    편수=("distance", "count"),
    평균거리=("distance", "mean"),
    최대거리=("distance", "max"),
).round(1))

print("\\n다중 키 (출발공항 x 월) 상위 6개:")
print(flights.groupby(["origin", "month"])["distance"].mean().round(1).head(6))

print("\\n열마다 다른 집계:")
print(flights.groupby("origin").agg({"distance": "mean", "air_time": "median",
                                     "carrier": "nunique"}).round(1))'''))

c.append(("md", "## 12. 범주형 변수 만들기"))
c.append(("code", '''f = flights.copy()

# np.select — 조건 목록과 값 목록을 짝지어 분류한다
conditions = [f["carrier"].isin(["UA", "AA", "DL"]),
              f["carrier"].isin(["B6", "EV", "MQ"])]
choices = ["A그룹", "B그룹"]
f["carrier_group"] = np.select(conditions, choices, default="기타")

print(f["carrier_group"].value_counts())

# loc로 특정 조건의 행만 수정
f.loc[f["carrier"] == "UA", "carrier_group"] = "A그룹(대형)"
print("\\n수정 후:\\n", f["carrier_group"].value_counts(), sep="")'''))

c.append(("md", "## 13. 구간화 — pd.cut"))
c.append(("code", '''f = flights.copy()
f["distance_bin"] = pd.cut(f["distance"],
                           bins=[0, 502, 872, 1389, np.inf],
                           labels=["단거리", "중거리", "장거리", "초장거리"])

print(f["distance_bin"].value_counts().sort_index())
print("\\n구간별 평균 비행시간(분):")
print(f.groupby("distance_bin", observed=True)["air_time"].mean().round(1))'''))

c.append(("md", """## 14. Wide ↔ Long 변환

같은 성격의 값이 여러 열에 흩어져 있으면(wide) 그래프를 그리기 어렵다.
한 열에 값, 다른 열에 구분을 두는 long 형태로 바꾼다."""))
c.append(("code", '''wide = pd.DataFrame({
    "city": ["서울", "부산", "대구"],
    "pop_2020": [966, 339, 241],
    "pop_2021": [950, 336, 239],
    "area_2020": [605.2, 770.1, 883.5],
    "area_2021": [605.2, 770.1, 883.5],
})
print("wide:\\n", wide, sep="")

long = pd.wide_to_long(wide, stubnames=["pop", "area"], i="city", j="year", sep="_")
print("\\nwide_to_long:\\n", long, sep="")

melted = wide.melt(id_vars="city", var_name="변수", value_name="값")
print("\\nmelt:\\n", melted.head(6), sep="")'''))

c.append(("md", "## 15. 결합 — merge와 concat"))
c.append(("code", '''airports = pd.DataFrame({
    "origin": ["EWR", "LGA", "JFK"],
    "airport_name": ["Newark Liberty", "LaGuardia", "John F. Kennedy"],
})

sample = flights[["origin", "dest", "distance"]].head(1000)

inner = pd.merge(sample, airports, on="origin", how="inner")
left = pd.merge(sample, airports, on="origin", how="left")
print(f"inner {inner.shape}   left {left.shape}")
print(inner.head())

stacked = pd.concat([sample.head(3), sample.tail(3)], ignore_index=True)
print("\\nconcat:\\n", stacked, sep="")'''))

c.append(("md", """## 과제 1 — 출발공항별 평균 속도

1. `hour > 10` 인 항공편만 고른다
2. `speed = distance / air_time * 60` 열을 만든다 (마일/시)
3. 출발공항별 평균 속도를 구한다
4. 내림차순 정렬"""))
c.append(("code", '''# .copy()를 붙이는 이유 — 원본의 일부를 잘라낸 뒤 열을 추가하면
# pandas가 SettingWithCopyWarning을 낸다. 사본임을 명시하면 경고가 사라진다.
late = flights[flights["hour"] > 10].copy()
print("hour > 10:", len(late))

# air_time이 비었거나 0이면 나눗셈이 깨지므로 먼저 거른다
late = late[late["air_time"].notna() & (late["air_time"] > 0)]
late["speed"] = late["distance"] / late["air_time"] * 60

result = (late.groupby("origin")["speed"]
          .agg(평균속도="mean", 편수="count")
          .round(1)
          .sort_values("평균속도", ascending=False))
print("\\n출발공항별 평균 속도 (마일/시):\\n", result, sep="")'''))

print(build("04_pandas.ipynb", c).name)
