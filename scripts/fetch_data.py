"""관악구 4개 통계표 실제 수치 조회."""
import json, mcp_client as m

JOBS = [
    ("sewer", {"orgId": "201", "tblId": "DT_201004_O070015", "objL1": "001021",
               "prdSe": "Y", "newEstPrdCnt": 15}),
    ("land",  {"orgId": "201", "tblId": "DT_201004_O010002", "objL1": "001021",
               "prdSe": "Y", "newEstPrdCnt": 15}),
    ("rain",  {"orgId": "201", "tblId": "DT_201004_O010005", "objL1": "ALL",
               "prdSe": "Y", "newEstPrdCnt": 15}),
    ("flood", {"orgId": "201", "tblId": "DT_201004_O160036", "objL1": "001021",
               "prdSe": "Y", "newEstPrdCnt": 20}),
]

m.init()
out = {}
for key, args in JOBS:
    txt = m.text_of(m.call("kosis_get_data", args))
    out[key] = txt
    body = txt.split("———")[1] if "———" in txt else txt
    print("=" * 70, key, flush=True)
    print(body[:2500], flush=True)
json.dump(out, open("gwanak_data.json", "w"), ensure_ascii=False, indent=1)
print("SAVED")
