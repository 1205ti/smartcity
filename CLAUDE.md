# smartcity — 프로젝트 규칙

스마트도시데이터분석 수업 과제 저장소. 이 파일은 **변하지 않는 규칙**을 담는다.
진행 상황과 결정 사항은 `MEMORY.md`, 시간순 기록은 `logs/WORKLOG.md`에 있다.

## 문서 역할 분담

| 파일 | 담는 것 | 갱신 시점 |
| --- | --- | --- |
| `CLAUDE.md` | 규칙·관례·환경 (거의 안 변함) | 규칙이 바뀔 때만 |
| `MEMORY.md` | 현재 상태·결정·미해결 항목 | 작업 단위가 끝날 때마다 |
| `logs/WORKLOG.md` | 무엇을 왜 했고 뭐가 막혔는지 (시간순, append) | 하루 단위 또는 큰 작업 후 |
| `docs/course/` | 노션 강의자료 원본 (수정 금지) | `scripts/fetch_notion.py` 재실행 시 |

## 환경

- Python은 **반드시 `.venv`** 를 쓴다. 시스템 python(3.9.6)은 pandas 3.x·geopandas가 안 맞는다.
  ```bash
  source .venv/bin/activate        # 또는 .venv/bin/python 직접 호출
  ```
- Jupyter 커널: `Python 3.12 (smartcity)`
- Node가 필요한 작업(wrangler)은 앞에 PATH를 붙인다. 전역 PATH는 건드리지 않는다 —
  기본 `node`는 conda 환경(v20)이고 Claude Code가 그걸 쓰고 있다.
  ```bash
  PATH="/opt/homebrew/opt/node@22/bin:$PATH" ./node_modules/.bin/wrangler ...
  ```

## 배포

`main`에 push하면 GitHub Actions가 Cloudflare Pages로 올린다. 수동 배포는 필요 없다.

- 배포 주소: https://smartcity-apa.pages.dev
- 정적 파일은 `public/` 아래에만 둔다. 빌드 과정은 없다.
- 워크플로: `.github/workflows/deploy.yml`

## 커밋

- 공개 저장소이므로 커밋·푸시는 확인 없이 진행한다.
- 단, 커밋 전 `.env`·API 키·토큰이 diff에 섞였는지 반드시 확인한다.
- 커밋 메시지는 한국어. 무엇을 했는지보다 **왜 그렇게 했는지**를 적는다.

## 비밀값

- API 키는 `.env`에 넣고 `python-dotenv`로 읽는다. `.env`는 `.gitignore`에 있다.
- 노트북 셀에 키를 직접 쓰지 않는다. 출력에 키가 찍히지 않게 주의한다.
- GitHub Actions용 값은 저장소 시크릿에 둔다. 로컬 파일로 관리하지 않는다.

## 데이터 취급 원칙

수업 주제가 통계·공간데이터라 아래를 지킨다.

- **원자료를 바꾸지 않는다.** `data/raw/`는 내려받은 그대로 두고, 가공물은 `data/processed/`에 쓴다.
- **원표에 없는 값을 만들지 않는다.** 여러 구간을 합산·평균해 새 지표를 만들어 제시하지 않는다.
  필요하면 원자료를 그대로 싣고 해석을 따로 적는다.
- **결측을 추세로 만들지 않는다.** 수록 연도가 불연속인 계열은 꺾은선으로 잇지 말고 막대로 그린다.
- **좋고 나쁨이 없는 지표에 색으로 방향을 주지 않는다.** 강수량 감소를 초록으로 칠하면 오독된다.
- 출처와 통계표 ID를 항상 함께 표시한다.

## 노트북 규칙

- 강의별로 하나씩 `notebooks/NN_주제.ipynb`
- 첫 셀에 **데이터 출처와 내려받는 방법**을 적는다. 다른 컴퓨터에서 재현 가능해야 한다.
- 한글 그래프는 `import koreanize_matplotlib` 한 줄이면 된다.
- 큰 원본 데이터는 커밋하지 않는다. 내려받는 코드를 대신 남긴다.

## 코드 스타일

- 주석은 한국어. **무엇을 하는지가 아니라 왜 그렇게 했는지**를 적는다.
- 변수·함수명은 영어. 의미가 드러나게.
- 외부 라이브러리를 새로 쓸 때는 `requirements.txt`에 추가한다.
