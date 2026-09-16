#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theo dõi agent chạy TRỰC TIẾP (live) trong terminal — đọc agent-team/live/activity.jsonl.

  python3 scripts/watch_live.py          # theo dõi realtime (Ctrl+C để thoát)
  python3 scripts/watch_live.py --once    # in trạng thái hiện tại rồi thoát
  python3 scripts/watch_live.py --tail 20 # 20 dòng gần nhất rồi theo dõi tiếp
"""
import os, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.path.join(ROOT, "agent-team", "live", "activity.jsonl")
C = {"running": "\033[33m", "done": "\033[32m", "blocked": "\033[35m", "failed": "\033[31m"}
R = "\033[0m"
ICON = {"running": "▶", "done": "✓", "blocked": "⏸", "failed": "✗"}


def show(line):
    try:
        e = json.loads(line)
    except Exception:
        return
    s = e.get("status", "")
    col = C.get(s, "")
    ic = ICON.get(s, "•")
    note = f"  — {e.get('note')}" if e.get("note") else ""
    print(f"{col}{ic} [{e.get('ts','')[-8:]}] {e.get('agent',''):<10} {e.get('task',''):<16} {e.get('step','')}{note}{R}")


def main():
    if not os.path.exists(FEED):
        print("Chưa có hoạt động nào (agent chưa chạy / chưa emit). File:", FEED)
        if "--once" in sys.argv:
            return
    lines = open(FEED, encoding="utf-8").read().splitlines() if os.path.exists(FEED) else []
    if "--once" in sys.argv:
        for l in lines[-50:]:
            show(l)
        return
    tail = int(sys.argv[sys.argv.index("--tail") + 1]) if "--tail" in sys.argv else 10
    for l in lines[-tail:]:
        show(l)
    print("\033[90m… đang theo dõi (Ctrl+C để thoát) …\033[0m")
    pos = os.path.getsize(FEED) if os.path.exists(FEED) else 0
    try:
        while True:
            if os.path.exists(FEED) and os.path.getsize(FEED) > pos:
                with open(FEED, encoding="utf-8") as f:
                    f.seek(pos)
                    for l in f:
                        show(l.rstrip())
                    pos = f.tell()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nĐã dừng theo dõi.")


if __name__ == "__main__":
    main()
