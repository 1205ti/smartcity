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

    seoul["key"] = seoul["SGG_NM_SGIS"] + "|" + seoul["ADM_NM"].map(norm)
    names["key"] = names["SGG_NM"] + "|" + names["ADMI_NM"].map(norm)

    cw = seoul.merge(names, on="key", how="left")
    miss = cw["H_DNG_CD"].isna()
    print(f"\n매칭 {(~miss).sum()}/{len(cw)}  미매칭 {miss.sum()}", flush=True)
    if miss.any():
        print("경계에만 있는 동:", cw.loc[miss, ["SGG_NM_SGIS", "ADM_NM"]]
              .to_string(index=False), flush=True)

    only_pop = set(names["key"]) - set(seoul["key"])
    if only_pop:
        print("생활인구에만 있는 동:", sorted(only_pop), flush=True)

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
