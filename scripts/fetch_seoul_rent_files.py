"""서울 열린데이터광장의 전월세가 연도별 ZIP을 내려받아 하나로 합친다.

OpenAPI는 최근 3년치만 준다(공식 안내). 그 이전 자료는 파일 다운로드로만
받을 수 있고, 2011년부터 연도별 ZIP이 올라와 있다.

파일 쪽은 열 이름이 한글이라 API 응답(영문 코드)과 다르다. 두 자료를
같이 쓰려면 이름을 맞춰야 해서 여기서 API 쪽 이름으로 통일한다.
"""
import io
import sys
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "rent_zip"
OUT = ROOT / "data" / "interim"

DOWNLOAD = "https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false"
REFERER = "https://data.seoul.go.kr/dataList/OA-21276/S/1/datasetView.do"
INF_ID = "OA-21276"

# 데이터셋 페이지의 downloadFile(seq) 값. 연도별로 고정돼 있다.
SEQ = {2011: 24, 2012: 25, 2013: 26, 2014: 27, 2015: 28, 2016: 29, 2017: 30,
       2018: 31, 2019: 32, 2020: 33, 2021: 34, 2022: 36, 2023: 38, 2024: 39,
       2025: 40}

# 파일(한글) → API(영문) 열 이름 대응
RENAME = {
    "접수년도": "RCPT_YR", "자치구코드": "CGG_CD", "자치구명": "CGG_NM",
    "법정동코드": "STDG_CD", "법정동명": "STDG_NM", "지번구분코드": "LOTNO_SE",
    "지번구분": "LOTNO_SE_NM", "본번": "MNO", "부번": "SNO", "층": "FLR",
    "계약일": "CTRT_DAY", "전월세구분": "RENT_SE", "임대면적": "RENT_AREA",
    "보증금(만원)": "GRFE", "임대료(만원)": "RTFE", "건물명": "BLDG_NM",
    "건축년도": "ARCH_YR", "건물용도": "BLDG_USG", "계약기간": "CTRT_PRD",
    "신규계약구분": "NEW_UPDT_YN", "갱신청구권사용": "CTRT_UPDT_USE_YN",
    "종전보증금": "BFR_GRFE", "종전임대료": "BFR_RTFE",
}


def download(year):
    """연도별 ZIP을 내려받아 캐시한다. 이미 있으면 건너뛴다."""
    RAW.mkdir(parents=True, exist_ok=True)
    dst = RAW / f"seoul_rent_{year}.zip"
    if dst.exists() and dst.stat().st_size > 1000:
        return dst

    r = requests.post(
        DOWNLOAD,
        headers={"Referer": REFERER,
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 Chrome/140.0 Safari/537.36"},
        data={"infId": INF_ID, "seqNo": "", "seq": SEQ[year], "infSeq": 3},
        timeout=300,
    )
    r.raise_for_status()
    dst.write_bytes(r.content)
    return dst


def read_zip(path):
    """ZIP 안의 텍스트 파일을 DataFrame으로 읽는다.

    인코딩이 연도마다 다르다. 2022년까지는 CP949, 2023년부터 UTF-8(BOM)이다.
    BOM을 먼저 보고, 없으면 CP949 → UTF-8 순으로 시도한다.
    파일명도 CP949라 zipfile이 주는 이름을 그대로 쓰면 깨진다.
    """
    z = zipfile.ZipFile(path)
    frames = []
    for info in z.infolist():
        if info.is_dir():
            continue
        raw = z.read(info)
        encodings = (["utf-8-sig"] if raw[:3] == b"\xef\xbb\xbf"
                     else ["cp949", "utf-8-sig"])
        for enc in encodings:
            try:
                frames.append(pd.read_csv(io.BytesIO(raw), encoding=enc,
                                          low_memory=False))
                break
            except UnicodeDecodeError:
                continue
        else:
            raise RuntimeError(f"인코딩 판별 실패: {path.name}")
    return pd.concat(frames, ignore_index=True)


def main(years):
    OUT.mkdir(parents=True, exist_ok=True)
    frames, t0 = [], time.time()

    for y in years:
        p = download(y)
        df = read_zip(p)
        df = df.rename(columns=RENAME)
        # 건물명 앞뒤에 탭 문자가 섞여 있다. 그대로 두면 비교·조인이 어긋난다.
        if "BLDG_NM" in df:
            df["BLDG_NM"] = df["BLDG_NM"].astype("string").str.strip().str.strip("\t")
        frames.append(df)
        print(f"{y}  {len(df):>9,}건  {p.stat().st_size/1e6:5.1f}MB  "
              f"{time.time()-t0:5.0f}초", flush=True)

    all_df = pd.concat(frames, ignore_index=True)
    dst = OUT / f"seoul_rent_{min(years)}_{max(years)}.parquet"
    all_df.to_parquet(dst, index=False)
    print(f"\n합계 {len(all_df):,}건 → {dst.name} {dst.stat().st_size/1e6:.1f}MB", flush=True)
    print(f"계약일 {all_df.CTRT_DAY.min()} ~ {all_df.CTRT_DAY.max()}", flush=True)
    return all_df


if __name__ == "__main__":
    ys = [int(a) for a in sys.argv[1:]] or list(range(2021, 2026))
    main(sorted(ys))
