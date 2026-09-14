"""KOSIS MCP 서버에 Streamable HTTP로 직접 붙는 최소 클라이언트."""
import json, sys, urllib.request, urllib.error

URL = "https://kosismcp2026.vercel.app/api/mcp"
_session = {"id": None}

def _post(payload, notify=False, _tries=4):
    import time
    last = None
    for attempt in range(_tries):
        try:
            return _post_once(payload, notify)
        except Exception as exc:          # 네트워크 끊김 · 타임아웃 재시도
            last = exc
            time.sleep(2 * (attempt + 1))
    return {"error": {"message": f"{type(last).__name__}: {last}"}}


def _post_once(payload, notify=False):
    body = json.dumps(payload).encode()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-03-26",
    }
    if _session["id"]:
        headers["Mcp-Session-Id"] = _session["id"]
    req = urllib.request.Request(URL, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            sid = r.headers.get("Mcp-Session-Id")
            if sid:
                _session["id"] = sid
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        return {"error": {"code": e.code, "message": e.read().decode()[:500]}}
    if notify:
        return None
    # SSE 프레임에서 data: 줄만 뽑아낸다
    for line in raw.splitlines():
        if line.startswith("data:"):
            return json.loads(line[5:].strip())
    return json.loads(raw) if raw.strip() else None

def init():
    r = _post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
               "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                          "clientInfo": {"name": "kosis-dash", "version": "1.0"}}})
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, notify=True)
    return r

def tools():
    return _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})

def call(name, args, rid=3):
    return _post({"jsonrpc": "2.0", "id": rid, "method": "tools/call",
                  "params": {"name": name, "arguments": args}})

def text_of(resp):
    """tools/call 응답에서 텍스트 본문만 이어붙인다."""
    if not resp or "result" not in resp:
        return json.dumps(resp, ensure_ascii=False)[:2000]
    return "\n".join(c.get("text", "") for c in resp["result"].get("content", []))

if __name__ == "__main__":
    init()
    t = tools()
    for tool in t["result"]["tools"]:
        schema = tool.get("inputSchema", {})
        props = list((schema.get("properties") or {}).keys())
        req = schema.get("required", [])
        print(f"- {tool['name']}({', '.join(props)})  required={req}")
        print(f"    {tool.get('description','')[:220]}")
