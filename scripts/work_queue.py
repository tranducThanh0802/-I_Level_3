#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hàng đợi ưu tiên (lỗ hổng #5): agent nên làm việc gì tiếp theo.
Xếp hạng bug + spec theo luật rõ ràng. Ghi agent-team/work-queue.md + in ra.

Luật xếp hạng:
- Bug (open/in-progress): điểm = mức_nặng*10 + số_lần_lặp. crash>high>medium>low. Bug 'cần người' TÁCH riêng.
- Spec: theo priority P0>P1>P2>P3; approved -> sẵn cho Dev, reviewing -> sẵn cho Soát spec.

Chạy: python3 scripts/work_queue.py
"""
import os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "agent-team")
OUT = os.path.join(AT, "work-queue.md")
SEVW = {"crash": 4, "high": 3, "medium": 2, "low": 1}
HUMAN = ("needs-human", "needs-arch", "be-side", "cant-repro")


def fm_of(text):
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
    return fm


def files(sub):
    return [f for f in glob.glob(os.path.join(AT, sub, "*.md")) if os.path.basename(f).upper() != "README.MD"
            and "EXAMPLE" not in os.path.basename(f).upper()]


bugs_agent, bugs_human, specs_dev, specs_review = [], [], [], []
# gộp cả file EXAMPLE để demo có nội dung
allbugs = [f for f in glob.glob(os.path.join(AT, "memory", "bugs", "*.md")) if os.path.basename(f).upper() != "README.MD"]
for f in allbugs:
    fm = fm_of(open(f, encoding="utf-8").read())
    st = fm.get("status", "")
    try:
        cnt = int(fm.get("count", 1))
    except Exception:
        cnt = 1
    item = {"id": fm.get("id", ""), "key": fm.get("key", os.path.basename(f)),
            "sev": fm.get("severity", ""), "count": cnt, "status": st,
            "score": SEVW.get(fm.get("severity", "").lower(), 1) * 10 + cnt}
    if st in HUMAN:
        bugs_human.append(item)
    elif st in ("open", "in-progress"):
        bugs_agent.append(item)
bugs_agent.sort(key=lambda x: -x["score"])
bugs_human.sort(key=lambda x: -x["score"])

allspecs = [f for f in glob.glob(os.path.join(AT, "specs", "*.md")) if os.path.basename(f).upper() != "README.MD"]
for f in allspecs:
    fm = fm_of(open(f, encoding="utf-8").read())
    it = {"feature": fm.get("feature", os.path.basename(f)), "prio": fm.get("priority", "P2"),
          "status": fm.get("status", "")}
    if fm.get("status") == "approved":
        specs_dev.append(it)
    elif fm.get("status") == "reviewing":
        specs_review.append(it)
pk = lambda x: x["prio"]
specs_dev.sort(key=pk); specs_review.sort(key=pk)

L = ["# Hàng đợi ưu tiên (tự sinh)\n",
     f"> Cập nhật: {datetime.date.today().isoformat()} · Luật: bug điểm = mức*10 + lặp; spec theo priority.\n",
     "## 🤖 Bug — agent làm tiếp (ưu tiên cao xuống thấp)"]
if bugs_agent:
    for b in bugs_agent:
        L.append(f"1. **{b['id']} {b['key']}** — {b['sev']} · lặp {b['count']} · điểm {b['score']}")
else:
    L.append("- (trống — không có bug open cho agent)")

L.append("\n## 🙋 Bug — CẦN NGƯỜI (tách riêng, không đưa vào hàng đợi agent)")
if bugs_human:
    for b in bugs_human:
        L.append(f"- {b['id']} {b['key']} — {b['status']} ({b['sev']})")
else:
    L.append("- (trống)")

L.append("\n## 📋 Spec sẵn sàng cho Dev (approved, theo priority)")
L += [f"1. **{s['feature']}** — {s['prio']}" for s in specs_dev] or ["- (trống)"]
L.append("\n## 🔍 Spec chờ Soát spec (reviewing)")
L += [f"- {s['feature']} — {s['prio']}" for s in specs_review] or ["- (trống)"]

L.append("\n## Việc tiếp theo NÊN làm")
nxt = []
if bugs_agent:
    nxt.append(f"Fix bug: {bugs_agent[0]['id']} {bugs_agent[0]['key']} (điểm cao nhất)")
if specs_dev:
    nxt.append(f"Dev: {specs_dev[0]['feature']} ({specs_dev[0]['prio']})")
L += [f"→ {x}" for x in nxt] or ["→ (hàng đợi trống)"]

text = "\n".join(L) + "\n"
open(OUT, "w", encoding="utf-8").write(text)
print(text)
print(f"(Đã ghi {OUT})")
