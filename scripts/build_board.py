#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh board.html — bảng theo dõi trạng thái & tiến độ:
- Quy trình công việc (pipeline spec: draft→reviewing→approved→building→done)
- Con Tester: lần chạy test (xanh/đỏ), phủ 4 trạng thái, bug tìm được
- Task đang làm (owner, tiến độ, câu hỏi mở) + bảng bug
Nguồn: agent-team/specs, workspace, memory/bugs, logs/runs.jsonl
Chạy: python3 scripts/build_board.py  rồi mở board.html
"""
import os, re, json, glob, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "agent-team")
OUT = os.path.join(ROOT, "board.html")


def project_name():
    try:
        with open(os.path.join(ROOT, "project.config.json"), encoding="utf-8") as f:
            return json.load(f).get("name", "Agent Team")
    except Exception:
        return "Agent Team"


PROJECT = project_name()


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


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


def section(text, title):
    out, grab = [], False
    for ln in text.splitlines():
        if ln.startswith("## "):
            grab = title.lower() in ln.lower(); continue
        if ln.startswith("#"):
            grab = False; continue
        if grab and ln.strip():
            out.append(ln)
    return out


def checks(lines):
    done = sum(1 for l in lines if re.match(r"^\s*-\s*\[[xX]\]", l))
    total = sum(1 for l in lines if re.match(r"^\s*-\s*\[[ xX]\]", l))
    return done, total


def files(sub):
    fs = sorted(glob.glob(os.path.join(AT, sub, "*.md")))
    return [f for f in fs if os.path.basename(f).upper() != "README.MD"]


def bar(done, total):
    pct = int(done / total * 100) if total else 0
    return f'<div class="bar"><div class="fill" style="width:{pct}%"></div></div><span class="pct">{done}/{total}</span>'


# ---- specs (pipeline) ----
STAGES = [("draft", "Nháp"), ("reviewing", "Đang soi"), ("approved", "Đã duyệt"),
          ("building", "Đang code"), ("done", "Xong")]
specs = []
for f in files("specs"):
    t = read(f); fm = fm_of(t)
    sd, stt = checks(section(t, "Bốn trạng thái"))
    ad, att = checks(section(t, "Tiêu chí nghiệm thu"))
    specs.append({"feature": fm.get("feature", os.path.basename(f)), "status": fm.get("status", "draft"),
                  "ver": fm.get("version", "?"), "states": (sd, stt), "acc": (ad, att),
                  "ex": "EXAMPLE" in os.path.basename(f).upper()})

# ---- workspace (tasks) ----
tasks = []
for f in files("workspace"):
    t = read(f); fm = fm_of(t)
    pd, pt = checks(section(t, "Kế hoạch"))
    q = [l for l in section(t, "Câu hỏi") if re.match(r"^\s*-\s*\[ \]", l)]
    tasks.append({"task": fm.get("task", os.path.basename(f)), "status": fm.get("status", ""),
                  "owner": fm.get("owner_now", ""), "plan": (pd, pt), "q": len(q),
                  "ex": "EXAMPLE" in os.path.basename(f).upper()})

# ---- bugs ----
bugs = []
for f in files("memory/bugs"):
    fm = fm_of(read(f))
    bugs.append({"id": fm.get("id", ""), "key": fm.get("key", os.path.basename(f)), "sev": fm.get("severity", ""),
                 "status": fm.get("status", ""), "count": fm.get("count", "?")})

# ---- runs.jsonl (tester) ----
runs = []
rp = os.path.join(AT, "logs", "runs.jsonl")
if os.path.exists(rp):
    for line in read(rp).splitlines():
        line = line.strip()
        if line:
            try:
                runs.append(json.loads(line))
            except Exception:
                pass
test_runs = [r for r in runs if r.get("agent") == "test"]
green = sum(1 for r in test_runs if any(s.get("result") == "green" for s in r.get("steps", [])))
red = len(test_runs) - green
bugs_open = sum(1 for b in bugs if b["status"] in ("open", "in-progress"))

SEVC = {"crash": "#b00020", "high": "#e05353", "medium": "#d69200", "low": "#7a8794"}
STC = {"draft": "#7a8794", "reviewing": "#d69200", "approved": "#17a05a", "building": "#2f6feb",
       "done": "#6366f1", "waiting-human": "#e05353", "in-progress": "#d69200", "done ": "#17a05a"}


def chip(txt, color="#7a8794"):
    return f'<span class="chip" style="background:{color}22;color:{color}">{html.escape(txt)}</span>'


# ---- render pipeline columns ----
cols = ""
for skey, sname in STAGES:
    cards = ""
    for s in specs:
        if s["status"] == skey:
            ex = '<span class="ex">mẫu</span>' if s["ex"] else ""
            cards += f"""<div class="kcard"><b>{html.escape(s['feature'])}</b>{ex}
              <div class="mini">4 trạng thái {bar(*s['states'])}</div>
              <div class="mini">nghiệm thu {bar(*s['acc'])}</div>
              <div class="mini muted">v{html.escape(str(s['ver']))}</div></div>"""
    if not cards:
        cards = '<div class="empty">—</div>'
    cols += f'<div class="col"><div class="colh" style="border-color:{STC.get(skey,"#888")}">{sname}</div>{cards}</div>'

# ---- render tester runs ----
trows = ""
for r in test_runs:
    ok = any(s.get("result") == "green" for s in r.get("steps", []))
    badge = '<span class="ok">XANH</span>' if ok else '<span class="fail">ĐỎ</span>'
    note = ""
    for s in r.get("steps", []):
        if s.get("result") not in ("green", "ok"):
            note = s.get("result", "")
    trows += f"""<tr><td>{badge}</td><td>{html.escape(r.get('task',''))}</td>
      <td>{html.escape(r.get('outcome',''))}</td><td class="muted">{html.escape(note)}</td></tr>"""
if not trows:
    trows = '<tr><td colspan="4" class="muted">Chưa có lần chạy test nào.</td></tr>'

# ---- render tasks ----
tcards = ""
for t in tasks:
    ex = '<span class="ex">mẫu</span>' if t["ex"] else ""
    qtag = f'<span class="qflag">❓ {t["q"]} câu hỏi mở</span>' if t["q"] else ""
    tcards += f"""<div class="tcard"><b>{html.escape(t['task'])}</b>{ex} {chip(t['status'], STC.get(t['status'],'#7a8794'))}
      <div class="mini">đang: {chip(t['owner'])}</div>
      <div class="mini">tiến độ {bar(*t['plan'])}</div>{qtag}</div>"""
if not tcards:
    tcards = '<div class="empty">Chưa có task nào.</div>'

# ---- render bugs ----
brows = ""
for b in bugs:
    c = SEVC.get(b["sev"].lower(), "#7a8794")
    idp = f"<b>{html.escape(b['id'])}</b> · " if b.get("id") else ""
    brows += f"""<tr><td>{chip(b['sev'] or '?', c)}</td><td>{idp}{html.escape(b['key'])}</td>
      <td>{html.escape(b['status'])}</td><td>lặp {html.escape(str(b['count']))}</td></tr>"""
if not brows:
    brows = '<tr><td colspan="4" class="muted">Chưa có bug.</td></tr>'

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(PROJECT)} — Board</title>
<style>
 :root{{--bg:#f4f6f9;--card:#fff;--ink:#1a1d21;--muted:#606a76;--line:#e6e9ee;--blue:#2f6feb;--soft:#eef2f7;--green:#17a05a;--red:#e05353}}
 @media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a20;--ink:#eceef1;--muted:#9aa3af;--line:#262a31;--blue:#6ea1ff;--soft:#20252d;--green:#3bd07f;--red:#ff6b6b}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
 .wrap{{max-width:1080px;margin:0 auto;padding:24px 16px 70px}}
 a{{color:var(--blue)}} .back{{font-size:14px}}
 h1{{font-size:22px;margin:6px 0 2px}} .top{{color:var(--muted);font-size:13px;margin:0 0 18px}}
 .kpis{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:22px}}
 .kpi{{flex:1;min-width:130px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
 .kpi .n{{font-size:24px;font-weight:700}} .kpi .l{{font-size:12px;color:var(--muted)}}
 h2{{font-size:16px;margin:26px 0 12px}}
 .board{{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}}
 .col{{flex:1;min-width:170px;background:var(--soft);border-radius:12px;padding:8px}}
 .colh{{font-size:13px;font-weight:700;padding:4px 6px 8px;border-bottom:2px solid;margin-bottom:8px}}
 .kcard,.tcard{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;margin-bottom:8px}}
 .kcard b,.tcard b{{font-size:13.5px}}
 .mini{{font-size:12px;color:var(--ink);margin-top:6px;display:flex;align-items:center;gap:6px}}
 .mini.muted,.muted{{color:var(--muted)}}
 .bar{{flex:1;height:8px;background:var(--soft);border:1px solid var(--line);border-radius:5px;overflow:hidden;min-width:60px}}
 .fill{{height:100%;background:var(--green)}} .pct{{font-size:11px;color:var(--muted)}}
 .chip{{font-size:11px;padding:2px 8px;border-radius:999px;font-weight:600}}
 .ex{{font-size:10px;color:#d69200;background:#d6920022;padding:1px 6px;border-radius:5px;margin-left:5px}}
 .grid2{{display:grid;grid-template-columns:1fr;gap:16px}} @media(min-width:760px){{.grid2{{grid-template-columns:1fr 1fr}}}}
 .panel{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
 table{{width:100%;border-collapse:collapse;font-size:13.5px}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}}
 th{{color:var(--muted);font-weight:600}}
 .ok{{background:var(--green);color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:6px}}
 .fail{{background:var(--red);color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:6px}}
 .qflag{{display:inline-block;margin-top:8px;font-size:12px;color:var(--red);font-weight:600}}
 .empty{{color:var(--muted);font-size:13px;padding:6px}}
 .tcard{{margin-bottom:10px}}
</style></head><body><div class="wrap">
 <a class="back" href="dashboard.html">← Bảng điều khiển</a> · <a class="back" href="exchanges.html">💬 Trao đổi</a>
 <h1>📊 {html.escape(PROJECT)} — Board</h1>
 <p class="top">Trạng thái &amp; tiến độ · sinh từ dữ liệu repo · {now}. Chạy lại <code>python3 scripts/build_board.py</code> để làm mới. (Dữ liệu đang là ví dụ mẫu cho tới khi robot chạy thật.)</p>

 <div class="kpis">
   <div class="kpi"><div class="n">{len(specs)}</div><div class="l">Feature trong quy trình</div></div>
   <div class="kpi"><div class="n" style="color:var(--green)">{green}</div><div class="l">Test XANH</div></div>
   <div class="kpi"><div class="n" style="color:var(--red)">{red}</div><div class="l">Test ĐỎ</div></div>
   <div class="kpi"><div class="n" style="color:var(--red)">{bugs_open}</div><div class="l">Bug đang mở</div></div>
   <div class="kpi"><div class="n">{sum(t['q'] for t in tasks)}</div><div class="l">Câu hỏi chờ bạn</div></div>
 </div>

 <h2>🔄 Quy trình công việc (theo spec)</h2>
 <div class="board">{cols}</div>

 <div class="grid2" style="margin-top:22px">
   <div class="panel">
     <h2 style="margin-top:0">🧪 Con Tester — tiến độ</h2>
     <table><tr><th>Kết quả</th><th>Task</th><th>Dùng?</th><th>Ghi chú</th></tr>{trows}</table>
   </div>
   <div class="panel">
     <h2 style="margin-top:0">🐛 Bug — kiểm soát</h2>
     <table><tr><th>Mức</th><th>Bug</th><th>Trạng thái</th><th>Lặp</th></tr>{brows}</table>
   </div>
 </div>

 <h2>📋 Task đang làm</h2>
 {tcards}
</div></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print(f"Đã tạo: {OUT}")
