#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bug board kiểu Jira tối giản → bugboard.html.
Mục tiêu: bug agent KHÔNG fix được hiện rõ ở cột "Cần người" để người nhảy vào làm.
Nguồn: agent-team/memory/bugs/*.md
Chạy: python3 scripts/build_bugboard.py  rồi mở bugboard.html
"""
import os, re, json, glob, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUGS = os.path.join(ROOT, "agent-team", "memory", "bugs")
OUT = os.path.join(ROOT, "bugboard.html")
try:
    PROJECT = json.load(open(os.path.join(ROOT, "project.config.json"), encoding="utf-8")).get("name", "Agent Team")
except Exception:
    PROJECT = "Agent Team"

# status -> cột. Nhóm "cần người" gộp các trạng thái agent bó tay.
COLS = [
    ("open", "🆕 Mới", ["open"]),
    ("doing", "🔧 Đang xử lý", ["in-progress"]),
    ("human", "🙋 Cần người", ["needs-human", "needs-arch", "cant-repro", "be-side"]),
    ("fixed", "✅ Đã sửa", ["fixed"]),
    ("closed", "🗄️ Bỏ qua", ["wontfix"]),
]
STATUS_LABEL = {"needs-human": "cần người", "needs-arch": "đổi kiến trúc", "cant-repro": "không tái hiện được (3 lần)",
                "be-side": "phía BE", "open": "mới", "in-progress": "đang xử lý", "fixed": "đã sửa", "wontfix": "bỏ qua"}
SEV = {"crash": "#b00020", "high": "#e05353", "medium": "#d69200", "low": "#7a8794"}


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


bugs = []
for f in glob.glob(os.path.join(BUGS, "*.md")):
    if os.path.basename(f).upper() == "README.MD":
        continue
    fm = fm_of(open(f, encoding="utf-8").read())
    fm["_file"] = os.path.basename(f)
    bugs.append(fm)


def card(b):
    c = SEV.get((b.get("severity", "")).lower(), "#7a8794")
    st = b.get("status", "")
    stuck = b.get("stuck_reason", "")
    assignee = b.get("assignee", "") or "chưa ai nhận"
    stuck_html = f'<div class="stuck">⚠️ {html.escape(stuck)}</div>' if stuck else ""
    bid = b.get("id", "")
    id_html = f'<span class="bugid">{html.escape(bid)}</span>' if bid else ""
    return f"""<div class="card" style="border-left:4px solid {c}">
      <div class="ck">{id_html}<span class="sev" style="background:{c}">{html.escape(b.get('severity','?'))}</span>
        <b>{html.escape(b.get('key', b['_file']))}</b></div>
      <div class="meta">lặp {html.escape(str(b.get('count','?')))} · nguồn {html.escape(b.get('source','?'))}</div>
      <div class="meta">👤 {html.escape(assignee)}</div>
      {stuck_html}
      <div class="fn">{html.escape(b['_file'])}</div></div>"""


colcount = {}
cols_html = ""
for cid, name, statuses in COLS:
    cards = [card(b) for b in bugs if b.get("status") in statuses]
    colcount[cid] = len(cards)
    hi = ' col-hi' if cid == "human" and cards else ''
    cols_html += f'<div class="col{hi}"><div class="colh">{name} <span class="cnt">{len(cards)}</span></div>{"".join(cards) or "<div class=empty>—</div>"}</div>'

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
need = colcount.get("human", 0)
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(PROJECT)} — Bug board</title>
<style>
 :root{{--bg:#f4f6f9;--card:#fff;--ink:#1a1d21;--muted:#606a76;--line:#e6e9ee;--blue:#2f6feb;--soft:#eef2f7;--red:#e05353}}
 @media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a20;--ink:#eceef1;--muted:#9aa3af;--line:#262a31;--blue:#6ea1ff;--soft:#20252d;--red:#ff6b6b}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
 .wrap{{max-width:1200px;margin:0 auto;padding:22px 16px 60px}} a{{color:var(--blue)}} .back{{font-size:14px}}
 h1{{font-size:22px;margin:6px 0 2px}} .top{{color:var(--muted);font-size:13px;margin:0 0 14px}}
 .callout{{background:#e0535315;border:1px solid var(--red);border-radius:12px;padding:12px 16px;margin-bottom:16px;font-size:14px}}
 .callout b{{color:var(--red)}}
 .board{{display:flex;gap:12px;overflow-x:auto;padding-bottom:8px;align-items:flex-start}}
 .col{{flex:1;min-width:210px;background:var(--soft);border-radius:12px;padding:10px}}
 .col-hi{{box-shadow:0 0 0 2px var(--red)}}
 .colh{{font-size:13px;font-weight:700;padding:2px 4px 10px;display:flex;justify-content:space-between}}
 .cnt{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:0 8px;font-size:12px;color:var(--muted)}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;margin-bottom:9px}}
 .ck{{display:flex;align-items:center;gap:6px;flex-wrap:wrap}} .ck b{{font-size:13px}}
 .bugid{{font-size:11px;font-weight:700;color:var(--blue);background:var(--soft);border:1px solid var(--line);padding:1px 7px;border-radius:6px}}
 .sev{{font-size:10px;font-weight:700;color:#fff;padding:2px 7px;border-radius:5px;text-transform:uppercase}}
 .meta{{font-size:12px;color:var(--muted);margin-top:5px}}
 .stuck{{font-size:12px;color:var(--red);margin-top:6px;background:#e0535315;padding:5px 7px;border-radius:6px}}
 .fn{{font-size:11px;color:var(--muted);margin-top:6px}} .empty{{color:var(--muted);padding:6px;font-size:13px}}
</style></head><body><div class="wrap">
 <a class="back" href="dashboard.html">← Bảng điều khiển</a> · <a class="back" href="board.html">📊 Board</a>
 <h1>🐞 {html.escape(PROJECT)} — Bug board</h1>
 <p class="top">Jira tối giản · {len(bugs)} bug · {now}. Làm mới: <code>python3 scripts/build_bugboard.py</code></p>
 <div class="callout">🙋 <b>{need} bug đang cần người</b> — agent bó tay (đổi kiến trúc / phía BE / không tái hiện được 3 lần).
   <br>Để <b>nhận một bug</b>: mở file <code>agent-team/memory/bugs/&lt;file&gt;.md</code>, đổi <code>assignee:</code> thành tên bạn và <code>status: in-progress</code>.</div>
 <div class="board">{cols_html}</div>
</div></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print(f"Đã tạo: {OUT} · cần người: {need}")
