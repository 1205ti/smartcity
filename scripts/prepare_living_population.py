"""서울 생활인구 원본(853MB)을 분석용 크기로 줄인다.

3,731,761행을 통째로 메모리에 올리면 8GB 가까이 먹는다.
청크로 읽으면서 집계만 누적해 processed/ 에 작은 파일 몇 개로 떨군다.

만드는 것
  living_pop_daily.csv        일자 x 행정동 — 하루 평균 생활인구
  living_pop_hourly.csv       시간대 x 행정동 — 연평균
  living_pop_age_gender.csv   행정동 x 성별 x 연령 — 연평균
"""
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "SPOP_2025_ADM.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

AGE_COLS = [f"{g}{a}" for g in ("M", "F")
            for a in ("00", "10", "20", "30", "40", "50", "60", "70")]
KEEP = ["YMD", "TT", "H_DNG_CD", "SPOP", "SIDO_NM", "SGG_NM", "ADMI_NM"] + AGE_COLS
CHUNK = 500_000


def main():
    t0 = time.time()
    daily, hourly, age, name_parts = [], [], [], []
    rows = 0

    # dtype을 미리 못박아 두면 청크마다 추론하느라 느려지는 것을 막는다.
    # 행정동 코드는 앞자리 0이 날아가지 않게 문자열로 읽는다.
    dtypes = {"H_DNG_CD": "string", "TT": "int16", "SPOP": "float32"}
    dtypes.update({c: "float32" for c in AGE_COLS})

    reader = pd.read_csv(SRC, usecols=KEEP, dtype=dtypes, chunksize=CHUNK,
                         encoding="utf-8-sig")

    for i, ch in enumerate(reader, 1):
        rows += len(ch)

        # 하루 평균 — 24개 시간대를 평균내야 '그날의 생활인구'가 된다
        daily.append(ch.groupby(["YMD", "H_DNG_CD"], observed=True)["SPOP"].mean())

        # 시간대별 — 나중에 다시 평균내려면 합과 개수를 같이 들고 있어야 한다
        hourly.append(ch.groupby(["TT", "H_DNG_CD"], observed=True)["SPOP"]
                      .agg(["sum", "count"]))

        # 성·연령 — 행정동별 합과 개수
        g = ch.groupby("H_DNG_CD", observed=True)[AGE_COLS]
        age.append(pd.concat({"sum": g.sum(), "count": g.count()}, axis=1))

        # 이름표는 청크마다 모은다. 앞부분만 보면 뒤에서 처음 나오는 동이 빠진다.
        name_parts.append(ch[["H_DNG_CD", "SIDO_NM", "SGG_NM", "ADMI_NM"]]
                          .drop_duplicates("H_DNG_CD"))

        if i % 2 == 0:
            print(f"  {rows:,}행  {time.time()-t0:.0f}초", flush=True)

    print(f"읽기 완료 {rows:,}행 {time.time()-t0:.0f}초", flush=True)

    names = pd.concat(name_parts).drop_duplicates("H_DNG_CD")
    print(f"행정동 이름표 {len(names)}개", flush=True)

    d = pd.concat(daily).groupby(level=[0, 1]).mean().round(2).reset_index()
    d.columns = ["YMD", "H_DNG_CD", "SPOP"]
    d = d.merge(names, on="H_DNG_CD", how="left")
    d.to_csv(OUT / "living_pop_daily.csv", index=False, encoding="utf-8-sig")
    print("daily", d.shape, flush=True)

    h = pd.concat(hourly).groupby(level=[0, 1]).sum()
    h["SPOP"] = (h["sum"] / h["count"]).round(2)
    h = h[["SPOP"]].reset_index().merge(names, on="H_DNG_CD", how="left")
    h.to_csv(OUT / "living_pop_hourly.csv", index=False, encoding="utf-8-sig")
    print("hourly", h.shape, flush=True)

    a = pd.concat(age).groupby(level=0).sum()
    res = (a["sum"] / a["count"]).round(2)
    res = res.reset_index().merge(names, on="H_DNG_CD", how="left")
    res.to_csv(OUT / "living_pop_age_gender.csv", index=False, encoding="utf-8-sig")
    print("age_gender", res.shape, flush=True)

    print(f"총 {(time.time()-t0)/60:.1f}분", flush=True)


if __name__ == "__main__":
    main()
