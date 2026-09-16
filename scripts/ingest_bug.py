#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nạp 1 crash/lỗi từ store/CI/tester -> bug (lỗ hổng #7). Tự tính fingerprint + GỘP TRÙNG.
Đây là adapter: Crashlytics/Sentry/CI gọi script này với dữ liệu crash.

Dùng (cờ trực tiếp):
  python3 scripts/ingest_bug.py --exc "NSInvalidArgumentException" \
      --frame "PlayerViewModel.play" --method "PlayerService.load(url:)" \
      --source store --severity crash
Hoặc từ JSON:
  python3 scripts/ingest_bug.py --json crash.json
  (crash.json: {"exc":..,"frame":..,"method":..,"source":..,"severity":..})

Trùng -> count++ (không mở bản ghi mới). Mới -> tạo BUG-<n>.
"""
import os, re, sys, json, glob, hashlib, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(ROOT, "agent-team", "memory", "bugs")


def arg(name, default=""):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def normalize(s):
    s = re.sub(r"\bclosure #\d+\b", "", s or "")
    s = re.sub(r"0x[0-9a-fA-F]+", "", s)
    s = re.sub(r":\d+", "", s)  # bỏ số dòng
    return re.sub(r"\s+", " ", s).strip()


def fingerprint(exc, frame, method):
    raw = f"{normalize(exc)}|{normalize(frame)}|{normalize(method)}"
    return "sha1:" + hashlib.sha1(raw.encode()).hexdigest()[:16]


def fm_block(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], end
    return "", -1


def next_id():
    mx = 0
    for f in glob.glob(os.path.join(BUGS, "*.md")):
        m = re.search(r"^\s*id:\s*BUG-(\d+)", open(f, encoding="utf-8").read(), re.M)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


def main():
    if "--json" in sys.argv:
        d = json.load(open(arg("--json"), encoding="utf-8"))
        exc, frame, method = d.get("exc", ""), d.get("frame", ""), d.get("method", "")
        source, severity = d.get("source", "store"), d.get("severity", "high")
    else:
        exc, frame, method = arg("--exc"), arg("--frame"), arg("--method")
        source, severity = arg("--source", "store"), arg("--severity", "high")
    if not (exc or frame or method):
        print("Thiếu dữ liệu crash. Xem hướng dẫn: head -20 scripts/ingest_bug.py"); sys.exit(1)

    fp = fingerprint(exc, frame, method)
    today = datetime.date.today().isoformat()

    # tìm trùng theo fingerprint
    for f in glob.glob(os.path.join(BUGS, "*.md")):
        if os.path.basename(f).upper() == "README.MD":
            continue
        text = open(f, encoding="utf-8").read()
        if fp in text:
            # count++
            m = re.search(r"^(\s*count:\s*)(\d+)", text, re.M)
            newc = int(m.group(2)) + 1 if m else 2
            text = re.sub(r"^(\s*count:\s*)\d+", rf"\g<1>{newc}", text, count=1, flags=re.M)
            text = re.sub(r"^(\s*last_seen:\s*).*$", rf"\g<1>{today}", text, count=1, flags=re.M)
            open(f, "w", encoding="utf-8").write(text)
            bid = re.search(r"id:\s*(BUG-\d+)", text)
            print(f"🔁 TRÙNG {bid.group(1) if bid else ''} ({os.path.basename(f)}) → count={newc}. Không mở bản ghi mới.")
            return

    # mới -> tạo
    n = next_id()
    key = normalize(method or frame or exc).lower()
    key = re.sub(r"[^a-z0-9]+", "-", key).strip("-")[:40] or "crash"
    path = os.path.join(BUGS, f"bug-{n:03d}-{key}.md")
    open(path, "w", encoding="utf-8").write(f"""---
id: BUG-{n}
key: {key}
fingerprint: "{fp}"
count: 1
severity: {severity}
source: {source}
status: open
assignee:
stuck_reason:
first_seen: {today}
last_seen: {today}
touched_files: []
---

## Dấu hiệu
```
{exc}
frame: {frame}
method: {method}
```

## Bước tái hiện
1. (tự động nạp từ {source} — bổ sung khi triage)

## Nguyên nhân gốc
<chưa xác định>

## Các lần thử
-

## Test chống tái phát
<chưa có>
""")
    print(f"🆕 Tạo BUG-{n}: {os.path.basename(path)} (fingerprint {fp})")


if __name__ == "__main__":
    main()
