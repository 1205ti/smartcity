
# 05 : API
> 웹 API로 서울시 열린데이터를 요청하고, JSON 응답을 Pandas DataFrame으로 바꾸어 분석하기
💡 
  강의 바로가기
  01 : 환경설정 · 02 : Python 기초 · 03 : NumPy · 04 : Pandas · 05 : API · 06 : Matplotlib · 07 : Plotly · 08 : Folium · 09-1 : 공간데이터와 좌표계 · 09-2 : 지오코딩
💡 
  학습 목표
  - API의 요청(Request)과 응답(Response) 구조를 설명한다.
  - requests로 웹 API를 호출하고 JSON 데이터를 확인한다.
  - API 인증키를 .env와 환경 변수로 안전하게 관리한다.
  - 1,000건 단위 Paging을 이용해 대용량 데이터를 반복 수집한다.
  - API 결과를 Pandas DataFrame과 CSV로 저장하고 다시 불러온다.
  - 서울시 전월세 데이터에서 전세만 선택해 동별·주택유형별 평균 전세가를 계산한다.
  - 웹앱 배포 시 API Key를 브라우저에 노출하지 않는 구조를 이해한다.
💡 
  보안 주의: 원본 실습 노트북에는 이해를 돕기 위해 인증키가 직접 입력된 셀이 있지만, 이 수업자료에서는 실제 키를 노출하지 않습니다. 공개 저장소·수업자료·웹 프론트엔드 코드에는 실제 API Key를 넣지 말고 .env, 환경 변수, Cloudflare Secret처럼 서버 측 비밀 저장소를 사용하세요.

## 0. API란 무엇인가?
API는 Application Programming Interface의 약자로, 서로 다른 프로그램이나 시스템이 정해진 규칙에 따라 데이터를 주고받을 수 있게 연결해 주는 창구입니다.
쉽게 생각하면 식당의 점원과 비슷합니다. 손님이 주방에 직접 들어가지 않고 점원에게 주문하듯, Python 프로그램도 데이터베이스에 직접 접속하지 않고 API에 요청을 보내 필요한 결과만 전달받을 수 있습니다.
  | 구분 | 식당 비유 | 웹 API 환경 |
  | Client | 손님 | 내 컴퓨터, Python, 브라우저 |
  | API | 점원 | 요청 규칙과 데이터 전달 창구 |
  | Server | 주방 | 원격 서버·데이터베이스 |

### 요청(Request)과 응답(Response)
API 통신은 크게 요청 → 처리 → 응답 순서로 이루어집니다.
- URL: 데이터를 요청할 위치
- API Key: 사용 권한을 확인하는 인증키
- Parameter: 연도, 자치구, 시작·종료 위치처럼 원하는 데이터의 조건
- Response: 서버가 돌려주는 처리 결과
대부분의 웹 API는 응답 형식으로 JSON을 사용합니다. JSON은 Python의 Dictionary와 매우 비슷합니다.
```JSON
{
  "name": "홍길동",
  "age": 25,
  "city": "서울"
}
```
💡 
  JSON의 { key: value } 구조는 Python의 Dictionary와 닮아 있기 때문에, response.json()으로 읽은 뒤 필요한 부분을 골라 Pandas DataFrame으로 변환하기 좋습니다.

## 1. 서울 열린데이터광장 API 인증키 준비
서울 열린데이터광장에 접속해 회원가입·로그인 후 사용할 데이터셋의 OpenAPI를 신청합니다. 실습 데이터는 서울시 부동산 전월세가 정보이며 서비스명은 tbLnOpendataRentV입니다.
1. 서울 열린데이터광장에 로그인합니다.
1. 데이터셋을 검색하고 OpenAPI 신청을 선택합니다.
1. 활용 용도는 교육·연구 또는 개인 데이터 분석으로 작성합니다.
1. 마이페이지의 인증키 관리에서 발급된 인증키를 확인합니다.
1. 실제 프로젝트에서는 인증키를 .env 또는 배포 플랫폼의 Secret에 저장합니다.

### 처음에는 구조를 이해하기 위한 변수 지정
원본 노트북에서는 API 호출 흐름을 이해하기 위해 인증키를 변수에 직접 넣었습니다. 수업자료에서는 실제 키를 마스킹합니다.
```Python
# 각자 발급받은 키를 사용하세요.
# 공개 자료에는 실제 키를 절대 기록하지 않습니다.
SEOUL_API_KEY = "YOUR_API_KEY"
```
💡 
  원본 노트북의 실제 인증키는 공개 자료에 재사용하지 않는 것이 안전합니다.

## 2. 첫 번째 API 호출: 5건 받아오기
requests는 웹 서버에 HTTP 요청을 보내는 라이브러리이고, pandas는 응답 데이터를 표로 바꾸는 데 사용합니다.
```Python
import requests
import pandas as pd

# 1. API 설정
API_KEY = SEOUL_API_KEY
TYPE = "json"
SERVICE = "tbLnOpendataRentV"
START_INDEX = 1
END_INDEX = 5

# 2. 요청 URL 생성
url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/"

# 3. API 호출
response = requests.get(url)
data = response.json()

# 4. DataFrame 변환
df = pd.DataFrame(data[SERVICE]["row"])

# 5. 결과 확인
df.head()
```
노트북에 저장된 실행 결과
```Plain Text
  RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ... GRFE RTFE BLDG_USG NEW_UPDT_YN
0    2026  11620    관악구   10200     신림동 ... 18000    0  연립다세대          신규
1    2026  11215    광진구   10700     화양동 ...  2000  100   오피스텔          신규
2    2026  11500    강서구   10200     등촌동 ... 14700    0   오피스텔          신규
3    2026  11710    송파구   10400     송파동 ...  5000   94  연립다세대          갱신
4    2026  11260    중랑구   10200     상봉동 ... 20000    0   오피스텔          신규

[5 rows x 23 columns]
```
💡 
  URL 안에는 인증키, 응답 형식, 서비스명, 시작 위치, 종료 위치가 순서대로 들어갑니다. response.json()은 JSON 응답을 Python 객체로 바꾸고, data[SERVICE]["row"]에서 실제 거래 행만 꺼내 DataFrame으로 변환합니다.
💡 
  실무에서는 requests.get(url, timeout=30)처럼 timeout을 지정하고, response.raise_for_status() 또는 API의 RESULT.CODE를 확인해 실패를 명시적으로 처리하는 습관이 좋습니다.

## 3. API Key를 .env로 안전하게 관리하기
API Key와 같은 보안 정보는 코드에 직접 하드코딩하지 않고 환경 변수로 관리하는 것이 안전합니다.

### python-dotenv 설치
```Python
! pip install python-dotenv
```
노트북에 저장된 실행 결과
```Plain Text
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: python-dotenv ... (1.2.2)
```
💡 
  이미 설치되어 있어 Requirement already satisfied가 출력되었습니다. 처음 설치하는 환경에서는 패키지를 내려받아 설치하는 메시지가 표시됩니다.

### .env 파일 만들기
노트북과 같은 프로젝트 폴더에 .env 파일을 만들고 다음처럼 작성합니다.
```
SEOUL_API_KEY=여기에_실제_발급받은_인증키_입력
```
💡 
  .env 파일은 GitHub에 올리지 않습니다. 프로젝트의 .gitignore에 .env를 추가하세요.

### Python에서 환경 변수 불러오기
```Python
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 읽기
API_KEY = os.getenv("SEOUL_API_KEY")

# API 호출
url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/tbLnOpendataRentV/1/5/"
response = requests.get(url)

df = pd.DataFrame(response.json()["tbLnOpendataRentV"]["row"])
df
```
노트북에 저장된 실행 결과
```Plain Text
  RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ... GRFE RTFE BLDG_USG NEW_UPDT_YN
0    2026  11620    관악구   10200     신림동 ... 18000    0  연립다세대          신규
1    2026  11215    광진구   10700     화양동 ...  2000  100   오피스텔          신규
2    2026  11500    강서구   10200     등촌동 ... 14700    0   오피스텔          신규
3    2026  11710    송파구   10400     송파동 ...  5000   94  연립다세대          갱신
4    2026  11260    중랑구   10200     상봉동 ... 20000    0   오피스텔          신규

[5 rows x 23 columns]
```
💡 
  첫 API 호출과 결과는 같지만 인증키를 코드 밖으로 분리했습니다. os.getenv()는 환경 변수의 값을 읽어 오며, 키가 없다면 None을 반환합니다.

## 4. Paging: 1,000건씩 반복 수집하기
서울 열린데이터광장은 한 요청에서 받을 수 있는 행 수에 제한이 있으므로 시작·종료 index를 바꾸어 여러 번 호출해야 합니다. 이를 Paging이라고 합니다.
```Python
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SEOUL_API_KEY")

TYPE = "json"
SERVICE = "tbLnOpendataRentV"

all_rows = []
start_idx = 1
step = 1000
max_data = 5000  # 수집할 총 데이터 건수 예시

while start_idx <= max_data:
    end_idx = start_idx + step - 1
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{TYPE}/{SERVICE}/{start_idx}/{end_idx}/"

    res = requests.get(url)
    data = res.json()

    if SERVICE in data:
        rows = data[SERVICE]["row"]
        all_rows.extend(rows)
        start_idx += step
    else:
        print("결과 없음 또는 오류 발생:", data.get("RESULT", {}).get("MESSAGE"))
        break

df_total = pd.DataFrame(all_rows)
print(f"총 {len(df_total)}건 수집 완료")
df_total.head()
```
노트북에 저장된 실행 결과
```Plain Text
총 5000건 수집 완료

  RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ... GRFE RTFE BLDG_USG NEW_UPDT_YN
0    2026  11620    관악구   10200     신림동 ... 18000    0  연립다세대          신규
1    2026  11215    광진구   10700     화양동 ...  2000  100   오피스텔          신규
2    2026  11500    강서구   10200     등촌동 ... 14700    0   오피스텔          신규
3    2026  11710    송파구   10400     송파동 ...  5000   94  연립다세대          갱신
4    2026  11260    중랑구   10200     상봉동 ... 20000    0   오피스텔          신규

[5 rows x 23 columns]
```
💡 
  1~1000, 1001~2000, …처럼 범위를 이동하며 데이터를 누적합니다. all_rows.extend(rows)는 이번 요청에서 받은 여러 행을 기존 리스트 뒤에 이어 붙입니다.

## 5. 접수연도 2026년 전체 데이터 수집
이번에는 URL 마지막에 RCPT_YR = "2026" 조건을 추가하고, 첫 응답의 list_total_count를 읽어 전체 건수를 자동으로 판단합니다.
```Python
import os
import requests
import pandas as pd
from dotenv import load_dotenv

# 1. .env 파일 로드 및 API 키 읽기
load_dotenv()
API_KEY = os.getenv("SEOUL_API_KEY")

# 2. API 기본 정보 및 수집 조건 설정
TYPE = "json"
SERVICE = "tbLnOpendataRentV"
RCPT_YR = "2026"

all_rows = []
start_idx = 1
step = 1000
total_count = None

print(f"[{RCPT_YR}년 서울시 부동산 전월세가 데이터 수집 시작]")

# 3. 데이터 반복 수집 (Paging)
while True:
    end_idx = start_idx + step - 1
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{TYPE}/{SERVICE}/{start_idx}/{end_idx}/{RCPT_YR}/"

    res = requests.get(url)
    data = res.json()

    if SERVICE in data:
        # 첫 호출 시 전체 데이터 건수 자동 감지
        if total_count is None:
            total_count = data[SERVICE]["list_total_count"]
            print(f"총 수집 대상 데이터: {total_count:,}건")

        rows = data[SERVICE]["row"]
        all_rows.extend(rows)
        print(f"수집 진행 중: {len(all_rows):,} / {total_count:,} 건 완료")

        start_idx += step

        if len(all_rows) >= total_count:
            break
    else:
        msg = data.get("RESULT", {}).get("MESSAGE", "데이터 없음")
        print(f"수집 종료/중단: {msg}")
        break

# 4. DataFrame 변환 및 확인
df_total = pd.DataFrame(all_rows)
print(f"\n✅ 최종 {len(df_total):,}건 수집 완료!")
df_total.head()
```
노트북에 저장된 실행 결과
```Plain Text
[2026년 서울시 부동산 전월세가 데이터 수집 시작]
총 수집 대상 데이터: 362,731건
수집 진행 중: 1,000 / 362,731 건 완료
수집 진행 중: 2,000 / 362,731 건 완료
수집 진행 중: 3,000 / 362,731 건 완료
...
수집 진행 중: 361,000 / 362,731 건 완료
수집 진행 중: 362,000 / 362,731 건 완료
수집 진행 중: 362,731 / 362,731 건 완료

✅ 최종 362,731건 수집 완료!

  RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ... GRFE RTFE BLDG_USG
0    2026  11200    성동구   11400   성수동1가 ...  2000   85   오피스텔
1    2026  11470    양천구   10200      목동 ... 69000   70    아파트
2    2026  11680    강남구   10800     논현동 ...  1000   94  단독다가구
3    2026  11500    강서구   10200     등촌동 ... 44000    0    아파트
4    2026  11215    광진구   10500     자양동 ... 25000    0  연립다세대

[5 rows x 23 columns]
```
💡 
  첫 요청에서 list_total_count = 362,731을 확인한 뒤 1,000건씩 반복합니다. 마지막 요청에서는 남은 731건을 받아 총 362,731건이 되면 반복문이 종료됩니다.
💡 
  대량 API 수집에서는 요청 실패에 대비해 timeout, 재시도, 중간 저장, 요청 간 짧은 대기 시간을 추가하면 더 안정적입니다. 실습에서는 구조를 이해하기 위해 핵심 로직만 사용했습니다.

## 6. 전체 DataFrame 확인과 CSV 저장

### 전체 데이터 확인
```Python
df_total
```
노트북에 저장된 실행 결과
```Plain Text
       RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ... BLDG_USG NEW_UPDT_YN
0         2026  11200    성동구   11400   성수동1가 ...   오피스텔          신규
1         2026  11470    양천구   10200      목동 ...    아파트          갱신
2         2026  11680    강남구   10800     논현동 ...  단독다가구          갱신
3         2026  11500    강서구   10200     등촌동 ...    아파트          갱신
4         2026  11215    광진구   10500     자양동 ...  연립다세대          신규
...        ...    ...    ...     ...     ... ...      ...         ...
362730    2026  11740    강동구   10800     성내동 ...  단독다가구          갱신

[362731 rows x 23 columns]
```
💡 
  Jupyter가 너무 큰 DataFrame을 전부 표시하지 않고 앞·뒤 일부 행과 전체 크기만 요약해 보여 줍니다.

### CSV 저장
```Python
df_total.to_csv("data/seoul_rent_2026.csv", index=False, encoding="utf-8-sig")
```
💡 
  파일 저장이 정상적으로 끝나면 기본적으로 화면 출력은 없습니다. data 폴더가 먼저 존재해야 하며, utf-8-sig는 Excel에서 한글이 깨지는 문제를 줄이는 데 유용합니다.

### 저장한 CSV 다시 불러오기
```Python
# 만약 여기까지 따라오지 못했다면 아래 코드로
# 서울시 2026년 전월세 데이터를 불러오세요.
seoul_rent_2026 = pd.read_csv(
    "data/seoul_rent_2026.csv",
    encoding="utf-8-sig"
)
seoul_rent_2026
```
노트북에 저장된 실행 결과
```Plain Text
        RCPT_YR  CGG_CD CGG_NM  STDG_CD STDG_NM ... BLDG_USG
0          2026   11200    성동구    11400   성수동1가 ...   오피스텔
1          2026   11470    양천구    10200      목동 ...    아파트
2          2026   11680    강남구    10800     논현동 ...  단독다가구
...         ...     ...    ...      ...     ... ...      ...
362730     2026   11740    강동구    10800     성내동 ...  단독다가구

[362731 rows x 23 columns]
```
💡 
  CSV로 저장했다가 다시 읽으면 MNO, SNO처럼 앞에 0이 있던 코드형 값이 숫자로 추론되어 0102 → 102.0처럼 보일 수 있습니다. 행정·식별 코드는 계산 대상 숫자가 아니라 문자열로 읽는 것이 안전합니다.
💡 
  코드형 열의 앞자리 0을 보존하려면 pd.read_csv(..., dtype={"CGG_CD": "string", "STDG_CD": "string", "MNO": "string", "SNO": "string"})처럼 자료형을 지정할 수 있습니다.

## 7. 서울시 부동산 전월세가 정보의 23개 변수
  | 예시·비고 | 한글 설명 | No | 변수명 |
  | 2026 | 접수연도 | 1 | RCPT_YR |
  | 5자리 코드 | 자치구코드 | 2 | CGG_CD |
  | 관악구 | 자치구명 | 3 | CGG_NM |
  | 5자리 코드 | 법정동코드 | 4 | STDG_CD |
  | 신림동 | 법정동명 | 5 | STDG_NM |
  | 1: 대지, 2: 산, 3: 블럭 | 지번구분 코드 | 6 | LOTNO_SE |
  | 대지 | 지번구분명 | 7 | LOTNO_SE_NM |
  | 코드형 문자열 권장 | 본번 | 8 | MNO |
  | 코드형 문자열 권장 | 부번 | 9 | SNO |
  | 1.0, 5.0 | 층수 | 10 | FLR |
  | YYYYMMDD | 계약일 | 11 | CTRT_DAY |
  | 전세, 월세 | 전월세 구분 | 12 | RENT_SE |
  | ㎡ | 임대면적 | 13 | RENT_AREA |
  | 만원 | 보증금 | 14 | GRFE |
  | 만원, 전세는 보통 0 | 임대료 | 15 | RTFE |
  | 단지·건물 명칭 | 건물명 | 16 | BLDG_NM |
  | YYYY | 건축년도 | 17 | ARCH_YR |
  | 아파트·오피스텔·연립다세대·단독다가구 | 건물용도 | 18 | BLDG_USG |
  | 26.09~28.09 | 계약기간 | 19 | CTRT_PRD |
  | 신규, 갱신 | 신규갱신여부 | 20 | NEW_UPDT_YN |
  | ○ 등 | 계약갱신권사용여부 | 21 | CTRT_UPDT_USE_YN |
  | 만원 | 종전 보증금 | 22 | BFR_GRFE |
  | 만원 | 종전 임대료 | 23 | BFR_RTFE |

### 변수 그룹으로 이해하기
- 행정·위치: CGG_NM, STDG_NM, MNO, SNO
- 거래·가격: RENT_SE, GRFE, RTFE, CTRT_DAY
- 건물·물건: BLDG_USG, BLDG_NM, RENT_AREA, FLR, ARCH_YR
- 갱신 계약: NEW_UPDT_YN, CTRT_UPDT_USE_YN, BFR_GRFE, BFR_RTFE

## 8. 전세 데이터만 골라 분석하기

### 전세만 필터링
```Python
# 전세만 골라내기
seoul_rent_2026_jeonse = seoul_rent_2026[
    seoul_rent_2026["RENT_SE"] == "전세"
]
seoul_rent_2026_jeonse
```
노트북에 저장된 실행 결과
```Plain Text
        RCPT_YR CGG_CD CGG_NM STDG_CD STDG_NM ...    GRFE RTFE BLDG_USG
1          2026  11620    관악구   10100     봉천동 ...   26700    0  연립다세대
3          2026  11440    마포구   12300     망원동 ...   56700    0    아파트
5          2026  11560   영등포구   10500  영등포동4가 ...   21700    0  연립다세대
12         2026  11380    은평구   10600     대조동 ...   15500    0  연립다세대
14         2026  11500    강서구   10900     방화동 ...   39900    0    아파트
...         ...    ...    ...     ...     ... ...     ...  ...     ...
392066     2026  11230   동대문구   10400     전농동 ...   68000    0    아파트
392070     2026  11680    강남구   10600     대치동 ...  108000    0    아파트
392071     2026  11320    도봉구   10500     쌍문동 ...   10000    0  단독다가구
392072     2026  11290    성북구   13300     정릉동 ...   14900    0  연립다세대
392074     2026  11440    마포구   12600      중동 ...   22000    0  연립다세대

[130748 rows x 23 columns]
```
💡 
  RENT_SE == "전세" 조건이 True인 행만 선택되어 130,748건의 전세 거래가 남았습니다. 필터링은 기존 DataFrame의 index를 그대로 유지하므로 결과의 index가 0부터 연속적으로 다시 시작하지 않습니다.
💡 
  필터링 후 index를 0부터 다시 정리하고 싶다면 seoul_rent_2026_jeonse = seoul_rent_2026_jeonse.reset_index(drop=True)를 사용할 수 있습니다.

### 동별·주택유형별 평균 전세가
```Python
jeonse_mean_df = seoul_rent_2026_jeonse.groupby(
    ["CGG_NM", "STDG_NM", "BLDG_USG"]
)["GRFE"].agg(
    평균전세가_만원="mean",
    거래건수="count"
).round(1).reset_index()

jeonse_mean_df
```
노트북에 저장된 실행 결과
```Plain Text
     CGG_NM STDG_NM BLDG_USG  평균전세가_만원  거래건수
0       강남구     개포동    단독다가구     21951.2      40
1       강남구     개포동      아파트     90199.0     830
2       강남구     개포동    연립다세대     33702.8     273
3       강남구     개포동     오피스텔     24917.2      34
4       강남구     논현동    단독다가구     21461.8     105
...      ...      ...      ...         ...     ...
1184    중랑구     신내동     오피스텔     21522.4      45
1185    중랑구     중화동    단독다가구     13304.7     118
1186    중랑구     중화동      아파트     45039.5      85
1187    중랑구     중화동    연립다세대     22254.8     247
1188    중랑구     중화동     오피스텔     13083.3       6

[1189 rows x 5 columns]
```
💡 
  groupby()로 자치구·법정동·건물용도 조합별로 묶고, GRFE의 평균과 거래 건수를 동시에 계산했습니다. round(1)은 평균 전세가를 소수 첫째 자리까지 정리합니다.

### 평균 전세가 상위 10개 확인
```Python
jeonse_mean_df = jeonse_mean_df.sort_values(
    by="평균전세가_만원",
    ascending=False
)
jeonse_mean_df.head(10)
```
노트북에 저장된 실행 결과
```Plain Text
     CGG_NM STDG_NM BLDG_USG  평균전세가_만원  거래건수
1130     중구   장충동1가      아파트    450000.0       1
1035    종로구   신문로2가      아파트    280000.0       1
1159     중구   회현동2가      아파트    181500.0       4
925     용산구     한남동      아파트    166131.1     111
921     용산구   한강로3가      아파트    157213.1      92
479     서초구     반포동      아파트    154899.9     757
876     용산구   용산동5가      아파트    153959.7      31
405     마포구     하중동      아파트    140170.0      20
991     종로구     내수동      아파트    132300.0      15
1156     중구   회현동1가      아파트    131500.0      12
```
💡 
  평균만 보면 거래 1건인 지역이 가장 높은 순위에 올라올 수 있습니다. 따라서 실제 비교에서는 거래건수를 함께 확인하고, 예를 들어 거래 10건 이상만 남기는 식으로 신뢰도를 보완할 수 있습니다.

### 집계 결과 CSV 저장
```Python
jeonse_mean_df.to_csv(
    "data/jeonse_mean.csv",
    index=False,
    encoding="utf-8-sig"
)
```
💡 
  평균 전세가와 거래 건수를 앱에서 빠르게 사용할 수 있도록 전처리된 CSV로 저장합니다.

## 9. 과제 2: 동별·주택유형별 평균 전세가 확인 앱

### 옵션 1. 전처리된 jeonse_mean.csv 활용
사용자가 동과 주택유형을 선택하면 해당 조건의 평균 전세가를 알려주는 앱을 만듭니다.
- GitHub에 seoul_rent 저장소 생성
- jeonse_mean.csv와 앱 코드를 저장소에 업로드
- 밝은 배경 + 오렌지 포인트의 심플한 UI
- 동과 주택유형 선택 → 평균 전세가와 거래 건수 표시
- Cloudflare로 배포
💡 
  옵션 1은 이미 전처리된 작은 CSV를 사용하므로 구현이 쉽고 빠릅니다. API Key도 필요하지 않습니다.

### 옵션 2. 서울 열린데이터 API를 실시간으로 활용
사용자가 자치구와 동을 선택하면 필요한 2026년 데이터를 API에서 가져와 평균 전세가를 계산합니다.
- GitHub에 seoul_rent_api 저장소 생성
- 자치구·동·주택유형 선택 UI 제공
- 선택 조건에 필요한 데이터를 API로 가져오기
- API Key는 코드에 포함하지 않기
- Cloudflare에 배포
💡 
  중요: 정적 프론트엔드 JavaScript에서 환경 변수를 읽어 API를 호출하면, 빌드 과정에서 값이 코드에 포함되어 브라우저 사용자에게 노출될 수 있습니다. 옵션 2는 브라우저 → Cloudflare Worker 또는 Pages Function → 서울 API 구조로 만들고, SEOUL_API_KEY는 서버 측 Secret/환경 변수로 저장하는 방식이 안전합니다.
```Plain Text
브라우저
   ↓ 동·주택유형 요청
Cloudflare Worker / Pages Function
   ↓ 서버 측에서 SEOUL_API_KEY 사용
서울 열린데이터광장 API
   ↓ JSON 응답
Worker / Pages Function
   ↓ 필요한 데이터만 반환
브라우저
```

## 10. Cloudflare 배포 시 확인할 점
원본 노트북의 배포 목표는 Cloudflare를 이용해 결과 앱을 공개하는 것입니다.
1. GitHub 저장소와 Cloudflare 프로젝트를 연결합니다.
1. 정적 파일만 사용하는 옵션 1은 Pages로 바로 배포할 수 있습니다.
1. API Key가 필요한 옵션 2는 Worker 또는 Pages Function에서 API 호출을 처리합니다.
1. Cloudflare 프로젝트의 환경 변수·Secret에 SEOUL_API_KEY를 등록합니다.
1. 배포 후 브라우저 개발자 도구의 Network·Sources에서 API Key가 노출되지 않는지 확인합니다.
💡 
  .env는 로컬 개발 환경용입니다. GitHub에 .env를 올리지 말고, Cloudflare 배포 환경에서는 플랫폼의 Secret/Environment Variables 기능을 사용합니다. 또한 프론트엔드 번들에 삽입되는 변수는 비밀이 될 수 없다는 점을 기억하세요.

## 11. 실행 결과를 읽는 법과 자주 만나는 오류
  | 해결 방향 | 상황 | 확인할 내용 |
  | 위 셀부터 순서대로 실행, Run All | NameError | 변수가 아직 만들어지지 않음 |
  | RESULT.MESSAGE 확인 | API 응답에 서비스명이 없음 | 키·URL·파라미터·호출 한도 |
  | status code와 response.text 먼저 확인 | JSONDecodeError | 서버가 JSON이 아닌 응답을 반환 |
  | 폴더를 만들거나 정확한 경로 사용 | CSV 경로 오류 | data 폴더 존재 여부 |
  | dtype="string" 또는 열별 dtype 지정 | 코드 앞자리 0 소실 | Pandas의 숫자형 자동 추론 |
  | 키 폐기·재발급 후 서버 측 Secret 사용 | API Key 노출 | GitHub·브라우저 Sources·Network |

## 12. 핵심 정리
💡 
  API 데이터 분석의 기본 흐름
  1. API 문서에서 URL·인증·파라미터 구조를 확인한다.
  1. 작은 범위의 데이터를 먼저 요청해 응답 구조를 확인한다.
  1. JSON에서 실제 행을 꺼내 DataFrame으로 변환한다.
  1. Paging으로 필요한 전체 데이터를 수집한다.
  1. CSV로 저장해 반복 호출을 줄인다.
  1. Pandas로 필터링·그룹화·정렬해 분석 결과를 만든다.
  1. 배포할 때는 API Key를 반드시 서버 측에서 보호한다.
💡 
  연습 문제
  - CGG_NM == "마포구" 조건을 API 또는 DataFrame 단계에서 적용해 보세요.
  - 전세 중 거래건수 10건 이상인 동·주택유형만 남긴 뒤 평균 전세가 상위 10개를 다시 구해 보세요.
  - GRFE의 평균뿐 아니라 중앙값도 함께 계산해 평균이 극단값에 얼마나 영향을 받는지 비교해 보세요.
---
💡 
  이전 강의: 04 : Pandas
💡 
  다음 강의: 06 : Matplotlib