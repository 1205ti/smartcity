"""서울 열린데이터광장에서 부동산 전월세가 전량을 수집한다.

한 번에 1,000건까지만 오므로 시작·끝을 옮겨가며 반복한다.
첫 응답의 list_total_count로 전체 건수를 알 수 있어 몇 번 돌지 자동으로 정해진다.
"""
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("SEOUL_API_KEY")
SERVICE = "tbLnOpendataRentV"
STEP = 1000


def fetch(year="2026", out=None):
    if not API_KEY:
        sys.exit("SEOUL_API_KEY가 없다. .env를 확인할 것")

    rows, start, total, t0 = [], 1, None, time.time()
    while True:
        url = (f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/{SERVICE}"
               f"/{start}/{start + STEP - 1}/{year}/")
        try:
            body = requests.get(url, timeout=90).json().get(SERVICE, {})
        except Exception as exc:
            # 일시적인 네트워크 오류로 수집 전체가 날아가지 않게 한 번 더 시도한다
            print(f"  재시도 ({type(exc).__name__}) start={start}", flush=True)
            time.sleep(3)
            continue

        if total is None:
            total = body.get("list_total_count", 0)
            print(f"{year}년 전체 {total:,}건", flush=True)

        chunk = body.get("row", [])
        if not chunk:
            break
        rows.extend(chunk)

        if start % 50_000 == 1:
            el = time.time() - t0
            eta = el / max(len(rows), 1) * (total - len(rows))
            print(f"  {len(rows):>7,} / {total:,}  경과 {el/60:.1f}분  남은 {eta/60:.1f}분",
                  flush=True)

        if len(rows) >= total:
            break
        start += STEP

    df = pd.DataFrame(rows)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"저장: {out}  {df.shape}  총 {(time.time()-t0)/60:.1f}분", flush=True)
    return df


if __name__ == "__main__":
    year = sys.argv[1] if len(sys.argv) > 1 else "2026"
    fetch(year, ROOT / "data" / "raw" / f"seoul_rent_{year}.csv")
