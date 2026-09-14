"""통계청 행정구역 경계(181MB zip)에서 서울 행정동만 뽑아 GeoJSON으로 저장한다.

전국 shp가 135MB라 통째로 쓰면 지도가 무겁다. 서울만 잘라 내고
좌표계도 웹 지도용(EPSG:4326)으로 바꿔 둔다.
"""
import time
import zipfile
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent
ZIP = ROOT / "data" / "raw" / "bnd_all_00_2025_2Q.zip"
INTERIM = ROOT / "data" / "interim" / "bnd"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    t0 = time.time()

    if not INTERIM.exists():
        INTERIM.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(INTERIM)
        print(f"압축 해제 {time.time()-t0:.0f}초", flush=True)

    shp = next(INTERIM.rglob("bnd_dong_*.shp"))
    print("읽는 중:", shp.name, flush=True)

    gdf = gpd.read_file(shp)
    print(f"전국 {gdf.shape}  CRS={gdf.crs}  {time.time()-t0:.0f}초", flush=True)
    print("열:", list(gdf.columns), flush=True)

    # 행정동 코드 앞 2자리가 11이면 서울이다
    code_col = next(c for c in gdf.columns if c.upper().startswith("ADM"))
    seoul = gdf[gdf[code_col].astype(str).str.startswith("11")].copy()
    print(f"서울 {seoul.shape}", flush=True)

    # 통계청 경계는 EPSG:5179(UTM-K). 웹 지도는 4326을 쓴다.
    seoul = seoul.to_crs("EPSG:4326")

    # 원본 정점이 너무 촘촘해 파일이 커진다. 약 10m 수준으로 단순화한다.
    # 시각화용이라 이 정도 오차는 화면에서 보이지 않는다.
    simplified = seoul.copy()
    simplified["geometry"] = seoul.geometry.simplify(0.0001, preserve_topology=True)

    full = ROOT / "data" / "interim" / "seoul_dong.geojson"
    seoul.to_file(full, driver="GeoJSON")
    simp = OUT / "seoul_dong_simplified.geojson"
    simplified.to_file(simp, driver="GeoJSON")

    print(f"저장 {full.name} {full.stat().st_size/1e6:.1f}MB", flush=True)
    print(f"저장 {simp.name} {simp.stat().st_size/1e6:.1f}MB", flush=True)
    print(f"총 {(time.time()-t0)/60:.1f}분", flush=True)


if __name__ == "__main__":
    main()
