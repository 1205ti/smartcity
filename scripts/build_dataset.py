"""KOSIS MCP 응답(마크다운 표)을 대시보드용 JSON으로 변환."""
import json, re
from collections import OrderedDict

raw = json.load(open("gwanak_data.json"))

def rows(text):
    """응답에서 마크다운 표의 데이터 행만 (셀 리스트, 헤더) 형태로 뽑는다."""
    header, out = None, []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set("".join(cells)) <= set("- "):      # |---|---| 구분선
            continue
        if header is None:
            header = cells
            continue
        out.append(cells)
    return header, out

def series_from(text, key_col, want, period_col, value_col, unit_col=None):
    """특정 분류값(want)에 해당하는 (시점, 값) 시계열을 만든다. 첫 등장만 취한다."""
    header, data = rows(text)
    pts = OrderedDict()
    unit = ""
    for cells in data:
        if len(cells) <= max(key_col, period_col, value_col):
            continue
        if cells[key_col] != want:
            continue
        period, value = cells[period_col], cells[value_col]
        if not value:                              # 결측치는 버린다
            continue
        if unit_col is not None and len(cells) > unit_col and cells[unit_col] and not unit:
            unit = cells[unit_col]
        if period not in pts:
            pts[period] = float(value)
    return [{"period": p, "value": v} for p, v in sorted(pts.items())], unit

KOSIS = "https://kosis.kr/statHtml/statHtml.do?orgId=201&tblId="

metrics = []

# ── 1) 강수량 · 강수일수 (서울 관측, 지역 분류 없음) ──────────────────────
rain = raw["rain"]
for item, unit in [("강수량", "mm"), ("강수일수", "일")]:
    pts, _ = series_from(rain, 0, item, 1, 3, 2)
    metrics.append({
        "id": f"rain_{item}", "name": f"연 {item}", "unit": unit,
        "region": "서울특별시(관측소 기준)", "group": "강우",
        "survey": "서울특별시기본통계", "table": "강수량 및 강수일수",
        "url": KOSIS + "DT_201004_O010005",
        "note": "이 통계표는 지역 분류가 없어 관악구 단위로 분리되지 않습니다. 서울 관측값입니다.",
        "points": pts,
    })

# ── 2) 토지현황(지목별) — 지목별 면적을 원자료 그대로 ────────────────────
land = raw["land"]
for jimok, label in [("대지", "대지 면적"), ("도로", "도로 면적"),
                     ("임야", "임야 면적"), ("하천", "하천 면적")]:
    pts, _ = series_from(land, 0, jimok, 1, 2)
    if not pts:
        continue
    metrics.append({
        "id": f"land_{jimok}", "name": f"{label} (관악구)", "unit": "㎡",
        "region": "관악구", "group": "토지피복",
        "survey": "서울특별시기본통계", "table": "토지현황(지목별)",
        "url": KOSIS + "DT_201004_O010002",
        "note": "지목 면적 원자료입니다. 불투수면 비율은 원표에 없어 계산하지 않았습니다.",
        "points": pts,
    })

# ── 3) 하수관거 ─────────────────────────────────────────────────────────
sewer = raw["sewer"]
for item, unit, label in [("시설연장", "m", "하수관거 시설연장"),
                          ("보급률", "%", "하수도 보급률"),
                          ("계획면적", "㎢", "하수도 계획면적")]:
    pts, _ = series_from(sewer, 0, item, 1, 3, 2)
    if not pts:
        continue
    metrics.append({
        "id": f"sewer_{item}", "name": f"{label} (관악구)", "unit": unit,
        "region": "관악구", "group": "하수 인프라",
        "survey": "서울특별시기본통계", "table": "하수관거",
        "url": KOSIS + "DT_201004_O070015",
        "note": "",
        "points": pts,
    })

# ── 4) 자연재해 피해 ────────────────────────────────────────────────────
flood = raw["flood"]
for item, unit, label in [("주택침수세대", "세대", "주택 침수 세대"),
                          ("이재민", "명", "이재민"),
                          ("피해액", "천원", "피해액")]:
    pts, _ = series_from(flood, 0, item, 1, 3, 2)
    if not pts:
        continue
    metrics.append({
        "id": f"flood_{item}", "name": f"{label} (관악구)", "unit": unit,
        "region": "관악구", "group": "침수 피해",
        "survey": "서울특별시기본통계", "table": "자연재해 발생 및 피해 현황",
        "url": KOSIS + "DT_201004_O160036",
        "note": "원표에 값이 있는 연도만 실었습니다. 수록 연도가 띄엄띄엄해 꺾은선으로 잇지 않고 막대로 표시합니다.",
        "chart": "bar", "polarity": "harm",
        "points": pts,
    })

doc = {
    "title": "관악캠퍼스 주변 수문 기반시설 통계",
    "updated": "2026-09-14 수집",
    "source": "국가통계포털(KOSIS) — 서울특별시기본통계",
    "metrics": [m for m in metrics if m["points"]],
}
json.dump(doc, open("/Users/taecinkim/Documents/Lab/smartcity/public/data/dashboard.json", "w"),
          ensure_ascii=False, indent=1)

for m in doc["metrics"]:
    p = m["points"]
    print(f"{m['group']:10s} {m['name']:28s} {len(p):2d}개 "
          f"{p[0]['period']}~{p[-1]['period']}  최근={p[-1]['value']:,.1f}{m['unit']}")
