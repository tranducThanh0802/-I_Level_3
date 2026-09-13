#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo một bug mới với ID tự đánh số (BUG-1, BUG-2, ...) — tránh trùng, dễ phân biệt.
Quét các bug hiện có, lấy số lớn nhất + 1.

Dùng:
  python3 scripts/new_bug.py "<key-slug>" [severity] [source]
Ví dụ:
  python3 scripts/new_bug.py "login-timeout" high store
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(ROOT, "agent-team", "memory", "bugs")


def next_id():
    mx = 0
    for f in glob.glob(os.path.join(BUGS, "*.md")):
        m = re.search(r"^\s*id:\s*BUG-(\d+)", open(f, encoding="utf-8").read(), re.M)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


def main():
    if len(sys.argv) < 2:
        print('Dùng: python3 scripts/new_bug.py "<key-slug>" [severity] [source]'); sys.exit(1)
    key = re.sub(r"[^a-z0-9\-]", "-", sys.argv[1].lower()).strip("-")
    severity = sys.argv[2] if len(sys.argv) > 2 else "medium"
    source = sys.argv[3] if len(sys.argv) > 3 else "tester"
    n = next_id()
    bid = f"BUG-{n}"
    path = os.path.join(BUGS, f"bug-{n:03d}-{key}.md")
    if os.path.exists(path):
        print("Đã tồn tại:", path); sys.exit(1)
    tpl = f"""---
id: {bid}
key: {key}
fingerprint: ""
count: 1
severity: {severity}
source: {source}
status: open
assignee:
stuck_reason:
first_seen: ""
last_seen: ""
touched_files: []
---

## Dấu hiệu
<log / stack trace rút gọn>

## Bước tái hiện
1. ...

## Nguyên nhân gốc
<không phải triệu chứng>

## Các lần thử
- [DATE] cách: <...> → outcome: **được** / **không được**

## Test chống tái phát
<tên test + chặn điều gì>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(tpl)
    print(f"✅ Tạo {bid}: {path}")
    print("Chạy lại: python3 scripts/build_bugboard.py để thấy trên board.")


if __name__ == "__main__":
    main()
