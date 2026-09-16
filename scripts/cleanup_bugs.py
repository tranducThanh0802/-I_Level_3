#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dọn sổ bug định kỳ (lỗ hổng #8, đề bài §3 "dọn định kỳ").
- Chuyển bug status fixed/wontfix + last_seen quá N ngày -> agent-team/memory/bugs/archive/
- Cảnh báo bug có touched_files không còn tồn tại (nếu chạy trong repo iOS thật).

Dùng:
  python3 scripts/cleanup_bugs.py            # xem trước (dry-run)
  python3 scripts/cleanup_bugs.py --apply    # thực sự chuyển vào archive/
  python3 scripts/cleanup_bugs.py --days 60  # đổi ngưỡng (mặc định 90)
"""
import os, re, sys, glob, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(ROOT, "agent-team", "memory", "bugs")
ARCH = os.path.join(BUGS, "archive")
DAYS = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 90
APPLY = "--apply" in sys.argv


def fm_of(text):
    fm, tf = {}, []
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            for line in block.splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            tf = re.findall(r"^\s*-\s*(.+)$", block, re.M)
    return fm, tf


def main():
    today = datetime.date.today()
    to_archive, stale_files = [], []
    for f in glob.glob(os.path.join(BUGS, "*.md")):
        base = os.path.basename(f)
        if base.upper() == "README.MD":
            continue
        fm, tf = fm_of(open(f, encoding="utf-8").read())
        st = fm.get("status", "")
        ls = fm.get("last_seen", "")
        if st in ("fixed", "wontfix") and re.match(r"\d{4}-\d\d-\d\d", ls or ""):
            age = (today - datetime.date.fromisoformat(ls[:10])).days
            if age >= DAYS:
                to_archive.append((base, st, age))
        for p in tf:
            p = p.strip()
            if p and p not in ("[]",) and not os.path.exists(os.path.join(ROOT, p)) and not os.path.exists(p):
                stale_files.append((base, p))

    print(f"Ngưỡng: {DAYS} ngày · chế độ: {'ÁP DỤNG' if APPLY else 'xem trước'}")
    print(f"\nBug đóng quá hạn → archive ({len(to_archive)}):")
    for b, st, age in to_archive:
        print(f"  - {b} ({st}, {age} ngày)")
    if stale_files:
        print(f"\n⚠️ Bug gắn file KHÔNG còn tồn tại ({len(stale_files)}) — xem lại (có thể code đã xoá):")
        for b, p in stale_files[:20]:
            print(f"  - {b} → {p}")

    if APPLY and to_archive:
        os.makedirs(ARCH, exist_ok=True)
        for b, _, _ in to_archive:
            shutil.move(os.path.join(BUGS, b), os.path.join(ARCH, b))
        print(f"\n✅ Đã chuyển {len(to_archive)} bug vào {ARCH}")
    elif to_archive:
        print("\n(Chạy lại với --apply để thực sự chuyển vào archive/)")
    else:
        print("\n✅ Không có gì cần dọn.")


if __name__ == "__main__":
    main()
