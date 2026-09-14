"""노션 공개 페이지를 loadPageChunk로 받아 마크다운으로 저장한다."""
import json, re, time, urllib.request, sys
from pathlib import Path

BASE = "https://gelatinous-cardinal-e24.notion.site/api/v3/loadPageChunk"
OUT = Path("notion_pages"); OUT.mkdir(exist_ok=True)

def post(payload):
    req = urllib.request.Request(
        BASE, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 Chrome/140.0 Safari/537.36"},
        method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode())
        except Exception:
            time.sleep(2 * (attempt + 1))
    return {}

def fetch_all(page_id):
    """커서를 따라가며 페이지의 모든 청크를 모은다."""
    blocks, cursor, n = {}, {"stack": []}, 0
    while n < 12:
        d = post({"pageId": page_id, "limit": 200, "chunkNumber": n,
                  "cursor": cursor, "verticalColumns": False})
        rm = d.get("recordMap", {})
        for bid, wrap in rm.get("block", {}).items():
            v = wrap.get("value")
            if isinstance(v, dict) and "value" in v:
                v = v["value"]
            if v:
                blocks.setdefault(bid, v)
        cursor = d.get("cursor", {})
        if not cursor.get("stack"):
            break
        n += 1
    return blocks

def txt(prop):
    return "".join(s[0] for s in (prop or []) if s and s[0] != "‣")

PREFIX = {"header": "\n## ", "sub_header": "\n### ", "sub_sub_header": "\n#### ",
          "bulleted_list": "- ", "numbered_list": "1. ", "to_do": "- [ ] ",
          "quote": "> ", "callout": "💡 ", "toggle": "▸ ", "page": "\n# "}

def render(blocks, root):
    seen, out = set(), []
    def walk(bid, depth=0):
        if bid in seen:
            return
        seen.add(bid)
        b = blocks.get(bid)
        if not b:
            return
        t = b.get("type")
        props = b.get("properties") or {}
        title = txt(props.get("title"))
        ind = "  " * max(0, depth - 1)
        if t == "code":
            out.append(f"{ind}```{txt(props.get('language'))}\n{title}\n{ind}```")
        elif t == "divider":
            out.append(f"{ind}---")
        elif t == "table_row":
            out.append(f"{ind}| " + " | ".join(txt(v) for _, v in sorted(props.items())) + " |")
        elif title or t in PREFIX:
            out.append(f"{ind}{PREFIX.get(t, '')}{title}")
        for c in (b.get("content") or []):
            walk(c, depth + 1)
    walk(root)
    return "\n".join(out)

PAGES = json.load(open("page_list.json"))
for num, (pid, name) in enumerate(PAGES, 1):
    safe = re.sub(r"[^\w가-힣]+", "_", name).strip("_")[:60]
    blocks = fetch_all(pid)
    md = render(blocks, pid)
    (OUT / f"{safe}.md").write_text(md)
    print(f"{num:2d}/{len(PAGES)}  {len(md):7,d}자  {name}", flush=True)
