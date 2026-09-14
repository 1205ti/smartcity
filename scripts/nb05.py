import sys; sys.path.insert(0, "scripts")
from build_notebooks import build

c = []
c.append(("md", """# 05 : API

강의자료: `docs/course/05_API.md`

서울 열린데이터광장 OpenAPI를 호출해 부동산 전월세가 정보를 수집하고,
JSON → DataFrame → CSV → 집계까지 한다.

## API 키

이 노트북은 **키가 없어도 끝까지 돈다.** 수집 결과 CSV(`data/raw/seoul_rent_2026.csv`)가
이미 있어서 6번 이후는 그 파일로 진행한다. 3~5번의 실제 API 호출만 키가 필요하다.

키를 발급받으려면:

1. https://data.seoul.go.kr 회원가입·로그인
2. "서울시 부동산 전월세가 정보" 검색 → OpenAPI 신청 (용도: 교육·연구)
3. 마이페이지 > 인증키 관리에서 확인
4. 프로젝트 루트에 `.env` 파일을 만들고 아래 한 줄 추가

```
SEOUL_API_KEY=발급받은_키
```

`.env`는 `.gitignore`에 있어서 커밋되지 않는다. 노트북 셀에 키를 직접 쓰지 않는다."""))

c.append(("code", '''import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()   # 프로젝트 루트의 .env를 읽는다
API_KEY = os.getenv("SEOUL_API_KEY")

HAS_KEY = bool(API_KEY)
print("API 키:", "있음" if HAS_KEY else "없음 — 저장된 CSV로 진행한다")'''))

c.append(("md", """## 1. 요청 URL 구조

```
http://openapi.seoul.go.kr:8088/{인증키}/json/{서비스명}/{시작}/{끝}/{연도}/
```

| 자리 | 값 |
| --- | --- |
| 서비스명 | `tbLnOpendataRentV` (서울시 부동산 전월세가 정보) |
| 시작/끝 | 한 번에 최대 1,000건 |
| 연도 | `RCPT_YR` — 접수연도 |"""))

c.append(("code", '''SERVICE = "tbLnOpendataRentV"
BASE = "http://openapi.seoul.go.kr:8088"


def build_url(start, end, year=None):
    """요청 URL을 만든다. 키가 없으면 None."""
    if not API_KEY:
        return None
    url = f"{BASE}/{API_KEY}/json/{SERVICE}/{start}/{end}/"
    if year:
        url += f"{year}/"
    return url


# 키가 노출되지 않도록 마스킹해서 확인만 한다
sample = build_url(1, 5, "2026")
print(sample.replace(API_KEY, "*" * 12) if sample else "키 없음 — 호출 생략")'''))

c.append(("md", "## 2. 5건만 호출해 구조 확인"))
c.append(("code", '''if HAS_KEY:
    r = requests.get(build_url(1, 5, "2026"), timeout=30)
    data = r.json()
    print("상태코드:", r.status_code)
    print("최상위 키:", list(data.keys()))
    head = data[SERVICE]
    print("전체 건수:", head["list_total_count"])
    print("결과 코드:", head["RESULT"]["CODE"], head["RESULT"]["MESSAGE"])
    df_sample = pd.DataFrame(head["row"])
    display(df_sample)
else:
    print("키가 없어 건너뛴다. 아래 6번부터 저장된 CSV로 이어진다.")'''))

c.append(("md", """## 3. Paging — 나눠서 가져오기

한 번에 1,000건까지만 오므로 시작·끝을 옮겨가며 반복한다.
첫 응답의 `list_total_count`로 전체 건수를 알 수 있어 몇 번 돌지 자동으로 정해진다."""))
c.append(("code", '''def fetch_all(year="2026", step=1000, max_data=None, verbose=True):
    """전월세 데이터를 페이지 단위로 모아 DataFrame으로 돌려준다.

    max_data를 주면 그만큼만 받는다(연습용). None이면 전량.
    """
    if not API_KEY:
        raise RuntimeError("SEOUL_API_KEY가 없다")

    rows, start, total = [], 1, None
    while True:
        end = start + step - 1
        r = requests.get(build_url(start, end, year), timeout=60)
        body = r.json().get(SERVICE, {})

        if total is None:
            total = body.get("list_total_count", 0)
            limit = total if max_data is None else min(total, max_data)
            if verbose:
                print(f"전체 {total:,}건 중 {limit:,}건 수집")

        chunk = body.get("row", [])
        if not chunk:
            break
        rows.extend(chunk)

        if verbose and start % 50000 == 1:
            print(f"  {len(rows):,} / {limit:,}")
        if len(rows) >= limit:
            break
        start = end + 1

    return pd.DataFrame(rows[:limit])'''))

c.append(("md", "## 4. 5,000건만 시험 수집"))
c.append(("code", '''if HAS_KEY:
    df_try = fetch_all(max_data=5000)
    print(df_try.shape)
    display(df_try.head())
else:
    print("건너뜀")'''))

c.append(("md", """## 5. 전량 수집 후 저장

362,731건(2026년 기준)이라 몇 분 걸린다. 이미 CSV가 있으면 건너뛴다."""))
c.append(("code", '''from pathlib import Path

CSV = Path("data/raw/seoul_rent_2026.csv")

if HAS_KEY and not CSV.exists():
    df_total = fetch_all()
    CSV.parent.mkdir(parents=True, exist_ok=True)
    df_total.to_csv(CSV, index=False, encoding="utf-8-sig")
    print(f"저장: {CSV} ({len(df_total):,}건)")
else:
    print(f"이미 있음: {CSV} — 수집 생략")'''))

c.append(("md", """## 6. CSV 다시 읽기 — 코드형 열의 앞자리 0 문제

자치구 코드처럼 `01110` 같은 값은 그냥 읽으면 숫자 1110이 되어 앞자리 0이 사라진다.
`dtype`으로 문자열임을 지정해야 한다."""))
c.append(("code", '''# 문제 상황 — 코드 열이 숫자로 읽힌다
naive = pd.read_csv(CSV, encoding="utf-8-sig", nrows=5)
print("dtype 지정 없이:", naive["CGG_CD"].dtype, "→", naive["CGG_CD"].tolist()[:3])

# 해결 — 코드형 열을 문자열로 못박는다
CODE_COLS = {"CGG_CD": "string", "STDG_CD": "string", "LOTNO_SE": "string",
             "MNO": "string", "SNO": "string"}
df = pd.read_csv(CSV, encoding="utf-8-sig", dtype=CODE_COLS)
print("dtype 지정 후:", df["CGG_CD"].dtype, "→", df["CGG_CD"].tolist()[:3])

print("\\nshape:", df.shape)'''))

c.append(("md", "## 7. 변수 살펴보기"))
c.append(("code", '''print("열 목록:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

df.head()'''))

c.append(("code", '''print("전월세 구분:")
print(df["RENT_SE"].value_counts())

print("\\n건물용도:")
print(df["BLDG_USG"].value_counts().head())'''))

c.append(("md", "## 8. 전세만 걸러내기"))
c.append(("code", '''jeonse = df[df["RENT_SE"] == "전세"].copy()
print(f"전세 {len(jeonse):,}건 / 전체 {len(df):,}건 ({len(jeonse)/len(df)*100:.1f}%)")
jeonse[["CGG_NM", "STDG_NM", "BLDG_USG", "GRFE", "RENT_AREA"]].head()'''))

c.append(("md", "## 9. 자치구·법정동·용도별 평균 전세가"))
c.append(("code", '''jeonse_mean = (jeonse
    .groupby(["CGG_NM", "STDG_NM", "BLDG_USG"])["GRFE"]
    .agg(평균전세가_만원="mean", 거래건수="count")
    .round(1)
    .reset_index())

print("shape:", jeonse_mean.shape)
jeonse_mean.head()'''))

c.append(("md", """## 10. 상위 10개 — 거래건수가 함정

평균만 보고 정렬하면 **거래가 한 건뿐인 곳**이 맨 위로 올라온다.
한 건은 그 동네의 시세가 아니라 그냥 그 한 거래일 뿐이다."""))
c.append(("code", '''top = jeonse_mean.sort_values("평균전세가_만원", ascending=False).head(10)
print("거래건수를 따지지 않은 상위 10개:")
display(top)

print(f"이 중 거래건수 1건: {(top['거래건수'] == 1).sum()}개")'''))

c.append(("code", '''# 거래건수 10건 이상으로 걸러야 시세라고 부를 만하다
solid = jeonse_mean[jeonse_mean["거래건수"] >= 10]
print(f"10건 이상: {len(solid):,}개 조합")
display(solid.sort_values("평균전세가_만원", ascending=False).head(10))'''))

c.append(("md", "## 11. 집계 결과 저장"))
c.append(("code", '''OUT = "data/processed/jeonse_mean.csv"
import os
os.makedirs("data/processed", exist_ok=True)
jeonse_mean.to_csv(OUT, index=False, encoding="utf-8-sig")
print("저장:", OUT, jeonse_mean.shape)'''))

c.append(("md", """## 연습 문제

1. 마포구만 보기
2. 평균과 중앙값 비교 — 어느 쪽이 시세에 가까운가"""))
c.append(("code", '''mapo = jeonse[jeonse["CGG_NM"] == "마포구"]
print(f"마포구 전세 {len(mapo):,}건\\n")

summary = (mapo.groupby(["STDG_NM", "BLDG_USG"])["GRFE"]
           .agg(평균="mean", 중앙값="median", 건수="count")
           .round(1))
summary = summary[summary["건수"] >= 10].sort_values("평균", ascending=False)
display(summary.head(10))

# 평균이 중앙값보다 크면 위쪽에 비싼 거래가 몇 건 끼어 평균을 끌어올린 것이다.
summary["평균-중앙값"] = (summary["평균"] - summary["중앙값"]).round(1)
print("\\n평균이 중앙값보다 많이 큰 곳 — 고가 거래가 평균을 끌어올린 사례:")
display(summary.sort_values("평균-중앙값", ascending=False).head(5))'''))

c.append(("md", """## 과제 2 — 웹앱 배포

강의자료는 두 옵션을 준다.

| 옵션 | 방식 | 키 |
| --- | --- | --- |
| 1 | `jeonse_mean.csv`를 정적 파일로 올리고 브라우저에서 조회 | 불필요 |
| 2 | Cloudflare Worker가 서울 API를 중계, 키는 서버 Secret | 필요 |

이 저장소는 이미 Cloudflare Pages에 붙어 있다(`public/`, https://smartcity-apa.pages.dev).
옵션 1이라면 `data/processed/jeonse_mean.csv`를 `public/data/`로 옮기고 조회 화면을
만들면 된다. 키가 브라우저에 노출되지 않는다는 점이 옵션 1의 장점이다.

옵션 2는 Worker가 필요하고, 그러려면 `workers.dev` 서브도메인 등록이 선행돼야 한다
(`MEMORY.md` 참고)."""))

print(build("05_api.ipynb", c).name)
