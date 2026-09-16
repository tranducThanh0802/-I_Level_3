#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent gọi script này để phát 1 sự kiện tiến trình LIVE (theo dõi lúc đang chạy).
Ghi vào agent-team/live/activity.jsonl (+ tùy chọn đẩy Discord realtime).

Agent dùng mỗi khi qua một bước:
  python3 scripts/emit_activity.py --agent fixbug --task BUG-5 --step "tìm nguyên nhân gốc" --status running
  python3 scripts/emit_activity.py --agent fixbug --task BUG-5 --step "chạy test" --status done
  python3 scripts/emit_activity.py --agent dev --task F-x --step "chờ người duyệt PR" --status blocked --discord

status: running | done | blocked | failed
"""
import os, re, sys, json, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "agent-team", "live")
FEED = os.path.join(LIVE, "activity.jsonl")


def arg(name, default=""):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else default


def redact(s):
    s = re.sub(r"https://\S*discord\S*/api/webhooks/\S+", "[ẨN]", s or "")
    return re.sub(r"\b([A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]*@([A-Za-z0-9.\-]+)", r"\1***@\2", s)


def main():
    os.makedirs(LIVE, exist_ok=True)
    ev = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "agent": arg("--agent", "?"), "task": arg("--task", "?"),
        "step": arg("--step", ""), "status": arg("--status", "running"),
        "note": arg("--note", ""),
    }
    with open(FEED, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print(f"[{ev['ts']}] {ev['agent']} · {ev['task']} · {ev['step']} · {ev['status']}")

    if "--discord" in sys.argv:
        try:
            cfg = json.load(open(os.path.join(ROOT, "scripts", "discord_config.json"), encoding="utf-8"))
            url = cfg.get("webhook_agents")
            if url:
                icon = {"running": "▶️", "done": "✅", "blocked": "⏸️", "failed": "❌"}.get(ev["status"], "•")
                body = redact(f"{icon} **{ev['agent']}** · `{ev['task']}` — {ev['step']} ({ev['status']})")
                data = json.dumps({"username": "📡 Live", "content": body}).encode()
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json",
                                                                      "User-Agent": "AgentTeam/1.0"})
                urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print("(Discord bỏ qua:", e, ")")


if __name__ == "__main__":
    main()
