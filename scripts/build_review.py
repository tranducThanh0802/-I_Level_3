#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trang DUYỆT (review.html) — gom mọi thứ cần để PO người duyệt một feature trong 1 cái nhìn:
spec + tiêu chí nghiệm thu + 4 trạng thái + máy kiểm (từ runs.jsonl) + verdict review + ẢNH + VIDEO.
Mục tiêu: "duyệt dễ hơn + nhìn tổng quát" — không phải mở 5 file.

Chạy: python3 scripts/build_review.py  rồi mở review.html
"""
import os, re, json, glob, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "agent-team")
SAMPLES = os.path.join(AT, "design-samples")
OUT = os.path.join(ROOT, "review.html")
try:
    PROJECT = json.load(open(os.path.join(ROOT, "project.config.json"), encoding="utf-8")).get("name", "Agent Team")
except Exception:
    PROJECT = "Agent Team"


def fm_and_body(text):
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            body = text[end + 4:]
    return fm, body


def section(body, title):
    out, grab = [], False
    for ln in body.splitlines():
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
    items = []
    for l in lines:
        m = re.match(r"^\s*-\s*\[([ xX])\]\s*(.*)$", l)
        if m:
            items.append((m.group(1).lower() == "x", m.group(2)))
    return done, total, items


# runs theo task
runs = []
rp = os.path.join(AT, "logs", "runs.jsonl")
if os.path.exists(rp):
    for l in open(rp, encoding="utf-8"):
        l = l.strip()
        if l:
            try:
                runs.append(json.loads(l))
            except Exception:
                pass


def latest_run(task_token):
    matches = [r for r in runs if r.get("task", "").startswith(task_token)]
    return matches[-1] if matches else None


# gallery: ảnh + video mới nhất
imgs = sorted(glob.glob(os.path.join(SAMPLES, "*.png")), key=os.path.getmtime, reverse=True)
vids = sorted(glob.glob(os.path.join(SAMPLES, "*.mov")), key=os.path.getmtime, reverse=True)


def rel(p):
    return os.path.relpath(p, ROOT)


def spec_card(f):
    fm, body = fm_and_body(open(f, encoding="utf-8").read())
    feature = fm.get("feature", os.path.basename(f))
    token = feature.split(" ")[0].split("(")[0]
    status = fm.get("status", "")
    ad, at, aitems = checks(section(body, "Tiêu chí nghiệm thu"))
    sd, st, sitems = checks(section(body, "Bốn trạng thái"))
    run = latest_run(token)
    # máy kiểm badges
    sigs = ""
    if run:
        for s in run.get("steps", []):
            res = s.get("result", "")
            color = "#17a05a" if res in ("green", "ok", "pass") else ("#e05353" if res in ("red", "fail") else "#7a8794")
            sigs += f'<span class="sig" style="background:{color}22;color:{color}">{html.escape(s.get("step",""))}: {html.escape(res)}</span>'
        ho = run.get("handoff", {})
        hoparts = [("code", ho.get("code")), ("video", ho.get("video")), ("ảnh", ho.get("before_after"))]
        hostr = " · ".join(f"{'✓' if v else '✗'} {k}" for k, v in hoparts)
    else:
        sigs = '<span class="muted">chưa có run</span>'
        hostr = "—"

    def itemlist(items):
        return "".join(f'<li class="{ "ok" if ok else "no" }">{"☑" if ok else "☐"} {html.escape(t)}</li>' for ok, t in items) or "<li class='muted'>—</li>"

    return f"""
    <div class="card">
      <div class="chead">
        <b>{html.escape(feature)}</b>
        <span class="chip">{html.escape(status)}</span>
        <span class="chip">{html.escape(fm.get('priority',''))}</span>
      </div>
      <div class="grid2">
        <div>
          <div class="lbl">Tiêu chí nghiệm thu ({ad}/{at})</div>
          <ul class="chk">{itemlist(aitems)}</ul>
          <div class="lbl">Bốn trạng thái ({sd}/{st})</div>
          <ul class="chk">{itemlist(sitems)}</ul>
        </div>
        <div>
          <div class="lbl">Máy kiểm (run gần nhất)</div>
          <div class="sigs">{sigs}</div>
          <div class="lbl" style="margin-top:10px">Bàn giao</div>
          <div>{hostr}</div>
        </div>
      </div>
      <div class="approve">Để duyệt: nhắn <code>duyệt {html.escape(token)}</code> · Cần sửa: <code>cần sửa: &lt;mô tả&gt;</code></div>
    </div>"""


specs = [f for f in glob.glob(os.path.join(AT, "specs", "*.md"))
         if os.path.basename(f).upper() != "README.MD" and "EXAMPLE" not in os.path.basename(f).upper()]
pending = [f for f in specs if fm_and_body(open(f, encoding="utf-8").read())[0].get("status") in ("draft", "reviewing")]
done_specs = [f for f in specs if fm_and_body(open(f, encoding="utf-8").read())[0].get("status") == "done"]

pending_html = "".join(spec_card(f) for f in pending) or '<p class="muted">Không có feature nào chờ duyệt.</p>'
done_html = "".join(f'<li>✅ {html.escape(fm_and_body(open(f,encoding="utf-8").read())[0].get("feature",os.path.basename(f)))}</li>' for f in done_specs) or "<li class='muted'>chưa có</li>"

gallery = ""
for v in vids:
    gallery += f'<div class="media"><video controls src="{html.escape(rel(v))}"></video><div class="fn">🎬 {html.escape(os.path.basename(v))}</div></div>'
for im in imgs:
    gallery += f'<div class="media"><img loading="lazy" src="{html.escape(rel(im))}"><div class="fn">{html.escape(os.path.basename(im))}</div></div>'

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(PROJECT)} — Duyệt</title>
<style>
 :root{{--bg:#f4f6f9;--card:#fff;--ink:#1a1d21;--muted:#606a76;--line:#e6e9ee;--blue:#2f6feb;--soft:#eef2f7;--green:#17a05a;--red:#e05353}}
 @media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a20;--ink:#eceef1;--muted:#9aa3af;--line:#262a31;--blue:#6ea1ff;--soft:#20252d;--green:#3bd07f;--red:#ff6b6b}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
 .wrap{{max-width:1040px;margin:0 auto;padding:24px 16px 70px}} a{{color:var(--blue)}} .back{{font-size:14px}}
 h1{{font-size:22px;margin:6px 0 2px}} .top{{color:var(--muted);font-size:13px;margin:0 0 16px}}
 .callout{{background:#2f6feb14;border:1px solid var(--blue);border-radius:12px;padding:12px 16px;margin-bottom:18px}}
 h2{{font-size:16px;margin:24px 0 10px}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:14px}}
 .chead{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px}} .chead b{{font-size:15px}}
 .chip{{font-size:12px;padding:2px 9px;border-radius:999px;background:var(--soft);color:var(--muted);font-weight:600}}
 .grid2{{display:grid;grid-template-columns:1fr;gap:14px}} @media(min-width:720px){{.grid2{{grid-template-columns:1fr 1fr}}}}
 .lbl{{font-size:12px;color:var(--muted);font-weight:600;margin-bottom:4px}}
 ul.chk{{list-style:none;padding:0;margin:0 0 8px}} ul.chk li{{font-size:13.5px;margin:2px 0}}
 ul.chk li.ok{{color:var(--ink)}} ul.chk li.no{{color:var(--muted)}}
 .sig{{display:inline-block;font-size:11.5px;padding:2px 8px;border-radius:6px;margin:2px 4px 2px 0}}
 .approve{{margin-top:12px;padding-top:10px;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted)}}
 code{{background:var(--soft);padding:1px 6px;border-radius:6px}}
 .gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
 .media{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:6px;overflow:hidden}}
 .media img,.media video{{width:100%;border-radius:6px;display:block}}
 .fn{{font-size:11px;color:var(--muted);margin-top:4px;word-break:break-all}}
 .muted{{color:var(--muted)}} ul.done{{padding-left:18px}} ul.done li{{margin:3px 0}}
</style></head><body><div class="wrap">
 <a class="back" href="dashboard.html">← Bảng điều khiển</a> · <a class="back" href="board.html">📊 Board</a>
 <h1>🔍 {html.escape(PROJECT)} — Cần bạn duyệt</h1>
 <p class="top">Gom spec + máy kiểm + ảnh + video vào 1 chỗ · {now}. Làm mới: <code>python3 scripts/build_review.py</code></p>
 <div class="callout"><b>{len(pending)} feature chờ duyệt.</b> Xem tiêu chí + máy kiểm + ảnh/video bên dưới, rồi
   nhắn <code>duyệt &lt;tên&gt;</code> hoặc <code>cần sửa: …</code>. Agent KHÔNG tự chốt (ADR-033).</div>

 <h2>⏳ Chờ duyệt</h2>
 {pending_html}

 <h2>🎬 Ảnh &amp; video mới nhất</h2>
 <div class="gallery">{gallery or '<p class=muted>chưa có</p>'}</div>

 <h2>✅ Đã duyệt (done)</h2>
 <ul class="done">{done_html}</ul>
</div></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print(f"Đã tạo: {OUT} · {len(pending)} chờ duyệt · {len(imgs)} ảnh · {len(vids)} video")
