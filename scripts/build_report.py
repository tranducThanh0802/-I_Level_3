#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Báo cáo đánh giá (§6 đề bài) — tính SỐ từ agent-team/logs/runs.jsonl + bugs/ + workspace/.
Quy tắc §6: dùng MEDIAN (không mean); thời gian chờ ngoài để RIÊNG; tỷ lệ 100% = đang giấu việc bỏ.
Chạy: python3 scripts/build_report.py  rồi mở report.html
"""
import os, re, json, glob, html, statistics, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "agent-team")
OUT = os.path.join(ROOT, "report.html")
try:
    PROJECT = json.load(open(os.path.join(ROOT, "project.config.json"), encoding="utf-8")).get("name", "Agent Team")
except Exception:
    PROJECT = "Agent Team"


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 1) if xs else None


def dur_min(r):
    try:
        s = datetime.datetime.fromisoformat(r["started_at"])
        e = datetime.datetime.fromisoformat(r["ended_at"])
        m = (e - s).total_seconds() / 60 - r.get("wait_external_ms", 0) / 60000
        return max(m, 0)
    except Exception:
        return None


def wait_min(r):
    return r.get("wait_external_ms", 0) / 60000


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


# --- load runs ---
runs = []
rp = os.path.join(AT, "logs", "runs.jsonl")
if os.path.exists(rp):
    for line in open(rp, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                runs.append(json.loads(line))
            except Exception:
                pass

total = len(runs)
used = sum(1 for r in runs if r.get("outcome") == "used")
dropped = sum(1 for r in runs if r.get("outcome") == "discarded")
use_rate = round(used / total * 100) if total else 0
drop_rate = round(dropped / total * 100) if total else 0

# thời gian theo loại việc (flow) — median, tách chờ ngoài
by_flow = {}
for r in runs:
    by_flow.setdefault(r.get("flow", "?"), []).append(r)
flow_rows = ""
for flow, rs in sorted(by_flow.items()):
    d = med([dur_min(r) for r in rs])
    w = med([wait_min(r) for r in rs])
    n = len(rs)
    warn = "" if n >= 5 else f' <span class="warn">(chỉ {n} mẫu — §6 cần ≥5 để so sánh)</span>'
    flow_rows += f"<tr><td>{html.escape(flow)}</td><td>{d if d is not None else '—'} phút</td><td class='muted'>{w if w is not None else '—'} phút</td><td>{n}{warn}</td></tr>"

# sửa tay: tổng + top 3 loại
fix_types = []
for r in runs:
    for mf in r.get("manual_fixes", []):
        fix_types.append(mf.get("type", "?"))
from collections import Counter
fc = Counter(fix_types)
top3 = fc.most_common(3)
top3_html = "".join(f"<li>{html.escape(t)} — {c} lần</li>" for t, c in top3) or "<li class='muted'>chưa có</li>"

# test pass/fail
test_runs = [r for r in runs if r.get("agent") == "test"]
tgreen = sum(1 for r in test_runs if any(s.get("result") == "green" for s in r.get("steps", [])))
tred = len(test_runs) - tgreen

# bugs: dedup + quay lại
bugs = [fm_of(open(f, encoding="utf-8").read()) for f in glob.glob(os.path.join(AT, "memory", "bugs", "*.md"))
        if os.path.basename(f).upper() != "README.MD"]
dedup_saved = 0
for b in bugs:
    try:
        dedup_saved += max(int(b.get("count", 1)) - 1, 0)
    except Exception:
        pass
# bug quay lại (proxy): file bug có attempt "được" nhưng status lại open/in-progress
recurring = 0
for f in glob.glob(os.path.join(AT, "memory", "bugs", "*.md")):
    if os.path.basename(f).upper() == "README.MD":
        continue
    t = open(f, encoding="utf-8").read()
    fm = fm_of(t)
    if fm.get("status") in ("open", "in-progress") and re.search(r"outcome:\s*\*\*được\*\*", t, re.I):
        recurring += 1
bug_recur_rate = round(recurring / len(bugs) * 100) if bugs else 0

# câu hỏi (workspace) — đếm mở/đã đóng (per-week cần mốc thời gian → ghi chú)
q_open = q_done = 0
for f in glob.glob(os.path.join(AT, "workspace", "*.md")):
    if os.path.basename(f).upper() == "README.MD":
        continue
    t = open(f, encoding="utf-8").read()
    grab = False
    for ln in t.splitlines():
        if ln.startswith("## "):
            grab = "câu hỏi" in ln.lower(); continue
        if ln.startswith("#"):
            grab = False; continue
        if grab:
            if re.match(r"^\s*-\s*\[ \]", ln):
                q_open += 1
            elif re.match(r"^\s*-\s*\[[xX]\]", ln):
                q_done += 1

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
# cảnh báo §6
flags = []
if total and drop_rate == 0:
    flags.append("Tỷ lệ bỏ dở = 0% — §6: có thể đang GIẤU việc bỏ dở. Kiểm lại đã log đủ chưa.")
if total < 5:
    flags.append(f"Chỉ {total} lần chạy — chưa đủ mẫu để kết luận (§6 cần ≥5/loại). Số dưới đây là minh hoạ.")
flags_html = "".join(f'<div class="flag">⚠️ {html.escape(x)}</div>' for x in flags)

page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(PROJECT)} — Báo cáo đánh giá</title>
<style>
 :root{{--bg:#f4f6f9;--card:#fff;--ink:#1a1d21;--muted:#606a76;--line:#e6e9ee;--blue:#2f6feb;--soft:#eef2f7;--green:#17a05a;--red:#e05353;--amber:#d69200}}
 @media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a20;--ink:#eceef1;--muted:#9aa3af;--line:#262a31;--blue:#6ea1ff;--soft:#20252d;--green:#3bd07f;--red:#ff6b6b;--amber:#f0b52a}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
 .wrap{{max-width:860px;margin:0 auto;padding:24px 16px 70px}} a{{color:var(--blue)}} .back{{font-size:14px}}
 h1{{font-size:22px;margin:6px 0 2px}} .top{{color:var(--muted);font-size:13px;margin:0 0 16px}}
 h2{{font-size:16px;margin:24px 0 10px}}
 .kpis{{display:flex;gap:10px;flex-wrap:wrap}} .kpi{{flex:1;min-width:130px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
 .kpi .n{{font-size:24px;font-weight:700}} .kpi .l{{font-size:12px;color:var(--muted)}}
 table{{width:100%;border-collapse:collapse;font-size:14px;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
 th,td{{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line)}} th{{color:var(--muted);font-weight:600;background:var(--soft)}}
 .muted{{color:var(--muted)}} .warn{{color:var(--amber);font-size:12px}}
 .flag{{background:#e0535322;border:1px solid var(--red);color:var(--red);border-radius:10px;padding:8px 12px;margin:6px 0;font-size:13.5px}}
 ul{{margin:6px 0;padding-left:20px}} .note{{color:var(--muted);font-size:12.5px;margin-top:6px}}
</style></head><body><div class="wrap">
 <a class="back" href="dashboard.html">← Bảng điều khiển</a> · <a class="back" href="board.html">📊 Board</a>
 <h1>📈 {html.escape(PROJECT)} — Báo cáo đánh giá</h1>
 <p class="top">Theo §6 đề bài · median (không mean) · chờ ngoài để riêng · {now}. Làm mới: <code>python3 scripts/build_report.py</code></p>
 {flags_html}

 <div class="kpis">
   <div class="kpi"><div class="n">{total}</div><div class="l">Lần chạy (có log)</div></div>
   <div class="kpi"><div class="n" style="color:var(--green)">{use_rate}%</div><div class="l">Dùng ngay (không sửa)</div></div>
   <div class="kpi"><div class="n" style="color:var(--red)">{drop_rate}%</div><div class="l">Bỏ giữa chừng</div></div>
   <div class="kpi"><div class="n" style="color:var(--red)">{bug_recur_rate}%</div><div class="l">Bug quay lại</div></div>
 </div>

 <h2>⏱️ Thời gian theo loại việc (median)</h2>
 <table><tr><th>Luồng</th><th>Thời gian làm</th><th>Chờ ngoài (riêng)</th><th>Số mẫu</th></tr>{flow_rows or '<tr><td colspan=4 class=muted>chưa có dữ liệu</td></tr>'}</table>
 <p class="note">Chờ ngoài (chờ PO/BE) để RIÊNG — agent không cắt được phần này (§6).</p>

 <h2>✋ Sửa tay (đầu vào loop ngoài)</h2>
 <p>Tổng lần sửa tay: <b>{len(fix_types)}</b>. Ba loại hay gặp nhất:</p>
 <ul>{top3_html}</ul>

 <h2>🧪 Test &amp; 🐛 Bug</h2>
 <table>
  <tr><th>Chỉ số</th><th>Giá trị</th></tr>
  <tr><td>Test XANH / ĐỎ</td><td>{tgreen} / {tred}</td></tr>
  <tr><td>Bug gộp trùng (đỡ mở bản ghi mới)</td><td>{dedup_saved}</td></tr>
  <tr><td>Bug quay lại sau khi sửa</td><td>{recurring} ({bug_recur_rate}%) — cao là đang chữa triệu chứng</td></tr>
  <tr><td>Câu hỏi: đang mở / đã trả lời</td><td>{q_open} / {q_done}</td></tr>
 </table>
 <p class="note">"Câu hỏi/tuần" cần mốc thời gian để chia tuần — sẽ tính khi có nhiều dữ liệu thật.</p>

 <h2>Nhắc quy tắc §6</h2>
 <ul>
  <li>So sánh: cùng loại việc, độ khó tương đương, <b>≥5 mẫu mỗi bên</b>, dùng <b>median</b>.</li>
  <li>Không tính: việc không log · tỷ lệ thành công tròn 100% (giấu việc bỏ) · "thấy nhanh hơn" không kèm số.</li>
  <li>Đạt: bậc ≥2 · giảm ≥40% thời gian việc lặp · bỏ dở &lt;20% · bug quay lại &lt;10%.</li>
 </ul>
</div></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print(f"Đã tạo: {OUT}")
