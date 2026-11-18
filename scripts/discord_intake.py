#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
discord_intake — NHẬN VÀO: đọc tin nhắn mới trong 1 kênh Discord → tạo việc trong hàng đợi intake.
Để mọi người trong cty (PO/dev/QA) nạp yêu cầu + ĐÍNH KÈM TÀI LIỆU ngay trong Discord; cả team theo dõi.

Khác với post_to_discord.py (ĐẨY RA, dùng webhook). ĐỌC VÀO cần BOT TOKEN (webhook không đọc được).
Chỉ dùng thư viện chuẩn (urllib) — KHÔNG thêm thư viện (tránh nhóm cấm-tự-quyết).

CẦN (bạn tự cấp, 1 lần) trong scripts/discord_config.json:
  "bot_token": "<token bot Discord>",          # Developer Portal → Bot → Reset Token; BẬT "Message Content Intent"
  "intake_channel_id": "<id kênh #agent-requests>"   # chuột phải kênh → Copy Channel ID (bật Developer Mode)
  Mời bot vào server + cho quyền đọc kênh đó.

Chạy:  python3 scripts/discord_intake.py          # kéo tin mới → tạo việc intake
       python3 scripts/discord_intake.py --loop   # lặp mỗi 30s (hoặc dùng cron / Claude /loop)
"""
import os, sys, json, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import agent_cli  # dùng _route + đường dẫn INTAKE
try:
    from post_to_discord import redact as _redact  # ẩn secret/PII TRƯỚC khi đẩy ra Discord (A8)
except Exception:
    def _redact(s): return s or ""

CFG = os.path.join(ROOT, "scripts", "discord_config.json")
STATE = os.path.join(ROOT, "scripts", ".discord_intake_state.json")
DOCS = os.path.join(agent_cli.INTAKE, "docs")
CHANLOG = os.path.join(agent_cli.INTAKE, "channel-log.jsonl")   # TRỌN hội thoại kênh (không sót) → context chung


def _cfg():
    try: return json.load(open(CFG, encoding="utf-8"))
    except Exception: return {}

def _api(path, token):
    req = urllib.request.Request("https://discord.com/api/v10" + path,
                                 headers={"Authorization": f"Bot {token}", "User-Agent": "DiscordBot (local,1.0)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def _ack(text):
    """Báo NGAY ra Discord (webhook) = trạng thái 'loading', để người gửi thấy agent đã nhận."""
    cfg = _cfg(); url = cfg.get("webhook_agents") or cfg.get("webhook_user")
    if not url: return
    try:
        data = json.dumps({"username": "Agent Team", "content": _redact(text)}).encode()
        req = urllib.request.Request(url, data=data,
              headers={"Content-Type": "application/json", "User-Agent": "AgentTeam/1.0 (local)"})
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass

def _download(url, dest):
    try:
        with urllib.request.urlopen(url, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
        return True
    except Exception as e:
        print("  (tải đính kèm lỗi:", e, ")"); return False

def poll_once():
    cfg = _cfg()
    token, chan = cfg.get("bot_token"), cfg.get("intake_channel_id")
    if not token or not chan:
        print("⚠️ Chưa cấu hình. Thêm 'bot_token' + 'intake_channel_id' vào scripts/discord_config.json."
              "\n   (Xem hướng dẫn trong đầu file discord_intake.py.)"); return 0
    os.makedirs(agent_cli.INTAKE, exist_ok=True); os.makedirs(DOCS, exist_ok=True)
    last = json.load(open(STATE)).get("last_id") if os.path.exists(STATE) else None
    q = f"/channels/{chan}/messages?limit=50" + (f"&after={last}" if last else "")
    try:
        msgs = _api(q, token)
    except urllib.error.HTTPError as e:
        print(f"⛔ Discord API lỗi {e.code} (token/quyền/intent?)."); return 0
    except (urllib.error.URLError, OSError) as e:
        print(f"… mạng chập chờn ({e}) — bỏ nhịp này, thử lại nhịp sau."); return 0
    msgs = sorted(msgs, key=lambda m: int(m["id"]))   # cũ → mới
    try: bot_id = _api("/users/@me", token)["id"]
    except Exception: bot_id = None
    n = 0
    for m in msgs:
        if m.get("author", {}).get("bot") or m.get("webhook_id"):   # bỏ tin BOT + tin do WEBHOOK đẩy ra
            continue                                                 # → KHÔNG ăn lại chính output của agent (chống vòng lặp)
        text = (m.get("content") or "").strip()
        atts = m.get("attachments", [])
        if not text and not atts:
            continue
        who = m["author"].get("global_name") or m["author"].get("username", "discord")
        iid = m["id"]
        docs = []
        for att in atts:
            dest = os.path.join(DOCS, f"{iid}_{att['filename']}")
            if _download(att["url"], dest): docs.append(os.path.relpath(dest, ROOT))
        # 1) LUÔN ghi vào context chung (trọn hội thoại — "tránh miss thông tin", CEO/Claude nạp hết để quyết)
        with open(CHANLOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"id": iid, "at": m.get("timestamp"), "who": who,
                                "text": text, "docs": docs}, ensure_ascii=False) + "\n")
        # 2) CHỈ tạo việc (work-item) nếu có hành động rõ (route ra skill / cấm-tự-quyết); còn lại chỉ là trao đổi
        mentioned = bool(bot_id) and any(u.get("id") == bot_id for u in m.get("mentions", []))
        esc, scored = agent_cli._route(text or " ".join(docs))
        if esc or scored:
            routed = "ESCALATE-CEO" if esc else scored[0][2]
            body = (f"---\nid: {iid}\nsource: discord\nrequester: {who}\nstatus: pending\n"
                    f"routed_skill: {routed}\n---\n# Yêu cầu\n{text or '(chỉ đính kèm tài liệu)'}\n")
            if docs: body += "\n## Tài liệu đính kèm\n" + "".join(f"- {d}\n" for d in docs)
            open(os.path.join(agent_cli.INTAKE, f"{iid}.md"), "w", encoding="utf-8").write(body)
            print(f"📥 việc: {who}: {(text or '[tài liệu]')[:45]} → {routed}" + (f" (+{len(docs)} tệp)" if docs else ""))
            _ack(f"⏳ **{who}** — đã nhận, agent đang xử lý… (`{routed}`)")   # LOADING ngay
            n += 1
        else:
            print(f"💬 ghi context (trao đổi): {who}: {text[:50]}")
            if mentioned:   # có gọi @bot nhưng không phải việc → vẫn báo đã nhận
                _ack(f"⏳ **{who}** — đã nhận, agent sẽ phản hồi…")
    if msgs:
        json.dump({"last_id": msgs[-1]["id"]}, open(STATE, "w"))
    print(f"Đã nhận {n} việc mới." if n else "Không có tin mới.")
    return n


def main():
    if "--loop" in sys.argv:
        secs = int(_cfg().get("poll_seconds", 10))   # nhanh hơn (mặc định 10s; chỉnh 'poll_seconds' trong config)
        print(f"▶ intake --loop mỗi {secs}s (Ctrl+C để dừng)")
        while True:
            try:
                poll_once()
            except Exception as e:
                print(f"… lỗi bất ngờ ({e}) — loop vẫn chạy tiếp.")
            time.sleep(secs)
    else:
        poll_once()

if __name__ == "__main__":
    main()
