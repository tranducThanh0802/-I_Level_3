#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh DATA DEMO cho báo cáo (chỉ để xem báo cáo trông thế nào + test pipeline).
KHÔNG phải số thật — mỗi dòng có "demo": true. Xoá demo: python3 scripts/seed_demo_data.py --clear

Chạy: python3 scripts/seed_demo_data.py   rồi python3 scripts/build_report.py
"""
import os, sys, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "agent-team", "logs", "runs.jsonl")
BASE = datetime.datetime.fromisoformat("2026-09-08T09:00:00+07:00")

# (flow, agent, task, phút_làm, phút_chờ_ngoài, outcome, [loại_sửa_tay], test_result, handoff_đủ)
DATA = [
    ("bugfix", "fixbug", "BUG-11 crash-settings-nil", 22, 0, "used", [], "green", True),
    ("bugfix", "fixbug", "BUG-12 list-index-oob", 35, 0, "used", ["sai chuẩn"], "green", True),
    ("bugfix", "fixbug", "BUG-13 login-token-expire", 18, 15, "used", [], "green", True),
    ("bugfix", "fixbug", "BUG-14 image-cache-leak", 90, 0, "used", ["sai logic"], "green", True),
    ("bugfix", "fixbug", "BUG-15 deeplink-parse", 26, 0, "used", ["sai chuẩn"], "green", True),
    ("bugfix", "fixbug", "BUG-16 race-feed", 45, 30, "discarded", [], "red", False),   # cant-repro/đổi kiến trúc -> bỏ
    ("bugfix", "fixbug", "BUG-17 date-format", 30, 0, "used", [], "green", True),
    ("feature", "test", "F-coupon-checkout", 55, 60, "used", ["sai chuẩn"], "green", True),
    ("feature", "dev", "F-profile-edit", 120, 240, "used", ["hiểu sai yêu cầu"], "green", True),
    ("feature", "test", "F-dark-mode", 40, 0, "used", [], "green", True),
    ("feature", "dev", "F-search-filter", 75, 120, "used", ["hiểu sai yêu cầu", "thiếu thông tin đầu vào"], "green", True),
    ("feature", "dev", "F-onboarding", 60, 30, "discarded", ["hiểu sai yêu cầu"], "red", False),  # spec mơ hồ -> bỏ giữa chừng
    ("feature", "test", "F-notification-optin", 48, 0, "used", ["thiếu thông tin đầu vào"], "green", True),
    ("feature", "dev", "F-share-sheet", 95, 45, "used", ["sai chuẩn"], "green", True),
]


def build():
    lines, t = [], BASE
    for i, (flow, agent, task, dur, wait, outcome, fixes, test_res, ho) in enumerate(DATA):
        start = t + datetime.timedelta(hours=i * 5)
        end = start + datetime.timedelta(minutes=dur + wait)
        steps = [{"step": "làm", "check": "-", "result": "ok"},
                 {"step": "chạy test", "check": "xcodebuild test", "result": test_res}]
        size = "S" if dur < 30 else ("M" if dur <= 75 else "L")
        baseline = round(dur * (2.6 if flow == "bugfix" else 2.1))  # demo: nếu làm tay ~2-2.6x
        lines.append(json.dumps({
            "run_id": f"DEMO-{i+1:02d}-{task}",
            "agent": agent, "flow": flow, "task": task,
            "started_at": start.isoformat(), "ended_at": end.isoformat(),
            "wait_external_ms": wait * 60000,
            "size": size, "human_baseline_min": baseline,
            "steps": steps,
            "failed_at": None if outcome == "used" else "chạy test",
            "manual_fixes": [{"type": ty, "detail": "demo"} for ty in fixes],
            "outcome": outcome, "pr": None,
            "handoff": {"code": ho, "video": ho, "before_after": ho},
            "demo": True,
        }, ensure_ascii=False))
    return lines


def main():
    # giữ lại các dòng THẬT (không có demo:true), thêm/bớt phần demo
    keep = []
    if os.path.exists(RUNS):
        for ln in open(RUNS, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                if json.loads(ln).get("demo") is True:
                    continue  # bỏ demo cũ
            except Exception:
                continue
            keep.append(ln)

    if "--clear" in sys.argv:
        with open(RUNS, "w", encoding="utf-8") as f:
            f.write("\n".join(keep) + ("\n" if keep else ""))
        print(f"Đã xoá data demo. Còn {len(keep)} dòng thật.")
        return

    out = keep + build()
    with open(RUNS, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Đã ghi {len(build())} dòng DEMO (+{len(keep)} dòng thật giữ lại) vào {RUNS}")
    print("Xem: python3 scripts/build_report.py && open report.html")
    print("Xoá demo khi có số thật: python3 scripts/seed_demo_data.py --clear")


if __name__ == "__main__":
    main()
