#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Báo cáo DÙNG THẬT và TỰ ĐỘNG HOÁ — chứng minh bằng log, không bằng lời (rubric A3, A6).

  python3 scripts/usage_report.py [--root <thư-mục-project>] [--bot-runs <agent-runs.jsonl>]

Đọc (tương đối theo --root, mặc định thư mục chứa scripts/):
  agent-team/logs/runs.jsonl            log mỗi lần chạy (schema: agent-team/logs/run-log.schema.md)
  agent-team/docs/task-catalog.json     danh mục việc lặp, đánh dấu cái nào do AI làm + tên bước tương ứng trong log
  agent-team/docs/usage-targets.json    chỉ tiêu tần suất do NGƯỜI đặt
Nguyên tắc trung thực:
  - Chỉ tiêu chưa có `confirmed_by` của người = CHƯA tính là đạt (không tự đặt chỉ tiêu rồi tự chấm đạt).
  - run có baseline_source != "human" bị loại khỏi mọi phép tính tiết kiệm thời gian.
  - "Có bằng chứng log" = có ít nhất một run với bước tương ứng kết quả không phải miss/fail.
"""
import os, sys, json, datetime, collections


def load_jsonl(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    for l in open(path, encoding="utf-8"):
        l = l.strip()
        if l:
            try:
                out.append(json.loads(l))
            except Exception:
                pass
    return out


def load_json(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default


def week(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main():
    a = sys.argv[1:]
    def opt(f, d=None):
        return a[a.index(f) + 1] if f in a and a.index(f) + 1 < len(a) else d
    root = os.path.abspath(opt("--root", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    runs = load_jsonl(os.path.join(root, "agent-team", "logs", "runs.jsonl"))
    bot = load_jsonl(opt("--bot-runs", os.path.expanduser("~/.claude/skills/project-triage/state/agent-runs.jsonl")))
    catalog = load_json(os.path.join(root, "agent-team", "docs", "task-catalog.json"), {})
    targets = load_json(os.path.join(root, "agent-team", "docs", "usage-targets.json"), {})
    print(f"Báo cáo dùng thật — {os.path.basename(root)}  ({datetime.date.today()})\n")

    # ---------- A3: tần suất ----------
    print("== A3. Tần suất dùng (từ runs.jsonl)")
    days = sorted({r["started_at"][:10] for r in runs if r.get("started_at")})
    by_week = collections.Counter()
    for r in runs:
        try:
            by_week[week(datetime.date.fromisoformat(r["started_at"][:10]))] += 1
        except Exception:
            pass
    print(f"  {len(runs)} run, {len(days)} ngày có chạy ({days[0] if days else '-'} → {days[-1] if days else '-'})")
    for w, n in sorted(by_week.items()):
        print(f"    {w}: {n} run")
    print(f"  Bot Discord `!làm`: {len(bot)} lần ghi nhận (ok: {sum(1 for b in bot if b.get('ok'))})")
    t = targets.get("min_runs_per_week")
    if t is None:
        print("  Chỉ tiêu: CHƯA CÓ → chưa chấm A3 được. Điền agent-team/docs/usage-targets.json.")
    elif not targets.get("confirmed_by"):
        print(f"  Chỉ tiêu đề xuất {t} run/tuần nhưng CHƯA có `confirmed_by` của người → chưa tính là đạt/trượt.")
        for w, n in sorted(by_week.items()):
            print(f"    (tham khảo) {w}: {n} so với {t}")
    else:
        for w, n in sorted(by_week.items()):
            print(f"    {w}: {n}/{t}  {'ĐẠT' if n >= t else 'CHƯA ĐẠT'}")
        print(f"  Chỉ tiêu do {targets['confirmed_by']} đặt ngày {targets.get('confirmed_at', '?')}")

    # ---------- A6: tự động hoá ----------
    print("\n== A6. Tự động hoá việc lặp (danh mục + bằng chứng log)")
    items = catalog.get("items", [])
    if not items:
        print("  Chưa có agent-team/docs/task-catalog.json → chưa khai danh mục (A6 mức 1).")
    else:
        evid = {}
        for it in items:
            names = set(it.get("log_steps", []))
            hits = [r for r in runs for s in r.get("steps", [])
                    if s.get("step") in names and not str(s.get("result", "")).startswith(("miss", "fail", "khong-tai-hien"))]
            evid[it["id"]] = sorted({r["run_id"] for r in hits})
        auto = [it for it in items if it["automated"]]
        proven = [it for it in auto if evid[it["id"]]]
        print(f"  Danh mục: {len(items)} việc, AI làm {len(auto)} ({round(100 * len(auto) / len(items))}%), người giữ {len(items) - len(auto)} (checkpoint)")
        print(f"  Có bằng chứng log: {len(proven)}/{len(auto)} việc AI làm = {round(100 * len(proven) / max(len(auto), 1))}%  ← con số dùng cho A6")
        for it in items:
            tag = "AI " if it["automated"] else "NGƯỜI"
            n = len(evid[it["id"]])
            note = f"{n} run" if it["automated"] else "checkpoint người, không tính"
            print(f"    {it['id']:>2} [{tag}] {it['name'][:52]:52} {note if n or not it['automated'] else 'KHÔNG CÓ BẰNG CHỨNG'}")
        known = {s for it in items for s in it.get("log_steps", [])}
        unk = collections.Counter(s["step"] for r in runs for s in r.get("steps", []) if s.get("step") not in known)
        if unk:
            print(f"  Tên bước trong log chưa gắn vào danh mục (hãy gắn hoặc chuẩn hoá tên): {dict(unk.most_common(8))}")
    done = [r for r in runs if not r.get("failed_at")]
    clean = [r for r in done if not r.get("manual_fixes")]
    print(f"\n  Run xong không hỏng: {len(done)}/{len(runs)}; không cần người sửa tay: {len(clean)}/{len(runs)} = {round(100 * len(clean) / max(len(runs), 1))}%")
    mf = collections.Counter(m.get("type", "?") for r in runs for m in (r.get("manual_fixes") or []))
    if mf:
        print(f"  Người sửa tay theo loại: {dict(mf)}")

    # ---------- thời gian (chỉ baseline do người) ----------
    human = [r for r in runs if r.get("baseline_source") == "human" and r.get("human_baseline_min") and r.get("human_minutes") is not None]
    skipped = len(runs) - len(human)
    print("\n== Thời gian người tiết kiệm")
    if not human:
        print(f"  KHÔNG TÍNH ĐƯỢC: {skipped}/{len(runs)} run có baseline do agent tự ước (baseline_source != human).")
        print("  Cách làm đúng: trước khi giao việc, người ghi `human_baseline_min` và `baseline_source: human` vào run.")
    else:
        b = sum(r["human_baseline_min"] for r in human); h = sum(r["human_minutes"] for r in human)
        print(f"  {len(human)} run có baseline người: tiết kiệm {round(100 * (b - h) / b)}% ({b} → {h} phút); loại {skipped} run baseline agent-estimated")


if __name__ == "__main__":
    main()
