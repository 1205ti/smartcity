"""통계청 경계와 서울 생활인구의 행정동을 잇는 대응표를 만든다.

두 기관의 행정동 코드 체계가 다르다.
  통계청(SGIS)  11010530  = 시도2 + 시군구2 + 동4
  서울/행자부     11110530  = 행정동코드 앞 8자리
426개 중 32개만 우연히 일치해 코드로는 붙일 수 없다.

그래서 (시군구명, 행정동명)으로 잇는다. 이름 표기도 구분자가 달라서
(종로1·2·3·4가동 vs 종로1.2.3.4가동) 정규화가 필요하다.
"""
import re
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BND = ROOT / "data" / "interim" / "bnd"
OUT = ROOT / "data" / "processed"


def norm(name):
    """동 이름을 비교 가능한 형태로 만든다.

    구분자(· . , 공백)를 없애고 붙여 쓴다. '종로1·2·3·4가동' → '종로1234가동'
    """
    if pd.isna(name):
        return ""
    return re.sub(r"[·.,\s‧・]", "", str(name)).strip()


def validate(cw, seoul, names):
    """조인 결과를 검사하고 문제가 있으면 크게 알린다.

    이름으로 잇는 방식은 두 자료가 같은 시점일 때만 안전하다.
    행정동은 수시로 통폐합된다 — 동대문구 용신동은 용두동과 신설동이 합쳐진 것이고,
    노원구 상계3·4동처럼 여러 동이 묶인 이름도 있다. 자료 연도가 어긋나면
    한쪽에만 있는 동이 생겨 조용히 빠진다. 그걸 막으려고 양방향으로 검사한다.
    """
    problems = []

    # 행 수가 변하면 키가 중복됐다는 뜻이다
    if len(cw) != len(seoul):
        problems.append(f"행 수 변화: 경계 {len(seoul)} → 조인 {len(cw)}. 키 중복 의심")

    miss = cw["H_DNG_CD"].isna()
    if miss.any():
        rows = cw.loc[miss, ["SGG_NM_SGIS", "ADM_NM"]].to_string(index=False)
        problems.append(f"경계에만 있는 동 {miss.sum()}개 (통계 미매칭):\n{rows}")

    only_pop = set(names["key"]) - set(seoul["key"])
    if only_pop:
        problems.append(f"통계에만 있는 동 {len(only_pop)}개 (경계 미매칭): "
                        f"{sorted(only_pop)}")

    for col in ("SGIS_CD", "H_DNG_CD"):
        src = cw["ADM_CD"] if col == "SGIS_CD" else cw["H_DNG_CD"]
        d = src.dropna().duplicated().sum()
        if d:
            problems.append(f"{col} 중복 {d}건 — 1:1 대응이 깨졌다")

    print(f"\n매칭 {(~miss).sum()}/{len(cw)}", flush=True)
    if problems:
        print("\n" + "!" * 60, flush=True)
        print("조인에 문제가 있다. 두 자료의 기준 시점이 다를 수 있다.", flush=True)
        for x in problems:
            print(f"  - {x}", flush=True)
        print("!" * 60, flush=True)
        raise SystemExit(1)
    print("검증 통과 — 1:1 대응, 양방향 누락 없음", flush=True)


def main():
    t0 = time.time()

    dong = gpd.read_file(next(BND.rglob("bnd_dong_*.shp")))
    sgg = gpd.read_file(next(BND.rglob("bnd_sigungu_*.shp")))[["SIGUNGU_CD", "SIGUNGU_NM"]]
    sgg.columns = ["SGG_CD", "SGG_NM_SGIS"]

    seoul = dong[dong["ADM_CD"].astype(str).str.startswith("11")].copy()
    # 시군구코드는 5자리(11010). 동코드 8자리의 앞 5자리와 맞물린다.
    seoul["SGG_CD"] = seoul["ADM_CD"].astype(str).str[:5]
    seoul = seoul.merge(sgg, on="SGG_CD", how="left")
    print(f"통계청 서울 행정동 {len(seoul)}개, 시군구 {seoul.SGG_NM_SGIS.nunique()}개",
          flush=True)

    pop = pd.read_csv(OUT / "living_pop_daily.csv", dtype={"H_DNG_CD": "string"})
    names = pop[["H_DNG_CD", "SGG_NM", "ADMI_NM"]].drop_duplicates()
    print(f"생활인구 행정동 {len(names)}개", flush=True)

    # 시군구는 두 체계가 1:1로 고정돼 있어(11010 ↔ 11110 종로구) 코드로 이어도 되지만,
    # 동은 뒤 3자리가 33%만 일치해 규칙이 없다. 그래서 동은 이름으로 잇는다.
    #
    # 동명만으로 이으면 안 된다. 신사동이 강남구와 관악구 양쪽에 있다.
    # 반드시 시군구를 함께 묶어야 한다.
    seoul["key"] = seoul["SGG_NM_SGIS"] + "|" + seoul["ADM_NM"].map(norm)
    names["key"] = names["SGG_NM"] + "|" + names["ADMI_NM"].map(norm)

    cw = seoul.merge(names, on="key", how="left")
    validate(cw, seoul, names)

    table = cw[["ADM_CD", "ADM_NM", "SGG_NM_SGIS", "H_DNG_CD"]].copy()
    table.columns = ["SGIS_CD", "DONG_NM", "SGG_NM", "H_DNG_CD"]
    table.to_csv(OUT / "dong_crosswalk.csv", index=False, encoding="utf-8-sig")

    # 경계 파일에도 생활인구 코드를 붙여 둔다. 이후 조인이 한 번에 끝난다.
    geo = cw[["ADM_CD", "ADM_NM", "SGG_NM_SGIS", "H_DNG_CD", "geometry"]].copy()
    geo.columns = ["SGIS_CD", "DONG_NM", "SGG_NM", "H_DNG_CD", "geometry"]
    geo = gpd.GeoDataFrame(geo, geometry="geometry", crs=seoul.crs).to_crs("EPSG:4326")
    geo["geometry"] = geo.geometry.simplify(0.0001, preserve_topology=True)
    dst = OUT / "seoul_dong_simplified.geojson"
    geo.to_file(dst, driver="GeoJSON")

    print(f"\n저장 dong_crosswalk.csv {table.shape}", flush=True)
    print(f"저장 {dst.name} {dst.stat().st_size/1e6:.1f}MB  {time.time()-t0:.0f}초", flush=True)


if __name__ == "__main__":
    main()
