#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cổng hồi quy (§4 đề bài, tầng ngoài): chạy sau khi đổi cẩm nang/chuẩn.
So tỷ lệ ĐẠT của lần chạy gần nhất với baseline. TỤT → CHẶN (exit 1).

Chạy: python3 scripts/run_regression.py [đường-dẫn-results.jsonl]
Mặc định đọc agent-team/regression/results.jsonl (nếu chưa có, dùng results.EXAMPLE.jsonl để minh hoạ).

results.jsonl sinh ra khi chạy bộ tình huống VỚI AGENT (runtime): mỗi dòng {"id","pass":true/false,"note"}.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "agent-team", "regression")


def load_jsonl(p):
    out = []
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def main():
    scen = load_jsonl(os.path.join(REG, "scenarios.jsonl"))
    ids = [s["id"] for s in scen]
    baseline = json.load(open(os.path.join(REG, "baseline.json"), encoding="utf-8"))

    res_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REG, "results.jsonl")
    used_example = False
    if not os.path.exists(res_path):
        ex = os.path.join(REG, "results.EXAMPLE.jsonl")
        if os.path.exists(ex):
            res_path = ex; used_example = True
        else:
            print("Chưa có results.jsonl. Hãy chạy bộ tình huống với agent rồi ghi kết quả vào\n"
                  f"  {os.path.join(REG,'results.jsonl')}  (mỗi dòng {{\"id\",\"pass\":true/false}}).")
            sys.exit(2)

    results = {r["id"]: r for r in load_jsonl(res_path)}
    missing = [i for i in ids if i not in results]
    passed = [i for i in ids if results.get(i, {}).get("pass") is True]
    failed = [i for i in ids if i in results and results[i].get("pass") is not True]

    rate = len(passed) / len(ids) if ids else 0
    base = float(baseline.get("pass_rate", 0))

    print(f"Bộ tình huống: {len(ids)} · ĐẠT: {len(passed)} · HỎNG: {len(failed)} · thiếu kết quả: {len(missing)}")
    print(f"Tỷ lệ đạt: {rate:.0%}  |  Baseline: {base:.0%}  ({baseline.get('date','?')}, duyệt: {baseline.get('approved_by','?')})")
    if used_example:
        print("(Đang dùng results.EXAMPLE.jsonl — minh hoạ. Khi chạy thật, ghi results.jsonl.)")
    if failed:
        print("HỎNG:")
        for i in failed:
            print(f"  - {i}: {results[i].get('note','')}")
    if missing:
        print("THIẾU KẾT QUẢ (coi như chưa đạt):", ", ".join(missing))

    # Cổng chặn: tụt so với baseline → CHẶN
    if rate + 1e-9 < base:
        print(f"\n⛔ CHẶN: tỷ lệ đạt ({rate:.0%}) TỤT dưới baseline ({base:.0%}). "
              f"Không cho áp thay đổi cẩm nang/chuẩn cho tới khi khắc phục.")
        sys.exit(1)
    print(f"\n✅ ĐẠT: không tụt so với baseline. (Người duyệt rồi cập nhật baseline nếu muốn nâng mốc.)")


if __name__ == "__main__":
    main()
