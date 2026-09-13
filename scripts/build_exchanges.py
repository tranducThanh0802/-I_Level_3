#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gom các cuộc trao đổi của agent (workspace/ + reviews/) thành 1 trang exchanges.html dễ đọc.
Chạy:  python3 scripts/build_exchanges.py    rồi mở exchanges.html
"""
import os, re, html, glob, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    with open(os.path.join(ROOT, "project.config.json"), encoding="utf-8") as _f:
        PROJECT = json.load(_f).get("name", "Agent Team")
except Exception:
    PROJECT = "Agent Team"
SOURCES = [
    ("💬 Việc đang làm & bàn giao (workspace)", os.path.join(ROOT, "agent-team", "workspace")),
    ("🔎 Phản biện & kết luận (reviews)", os.path.join(ROOT, "agent-team", "reviews")),
]
OUT = os.path.join(ROOT, "exchanges.html")


def parse_frontmatter(text):
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip("\n")
            body = text[end + 4:]
            for line in block.splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
    return fm, body


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def md_to_html(body):
    out, lst, tbl = [], False, []

    def close_list():
        nonlocal lst
        if lst:
            out.append("</ul>"); lst = False

    def flush_table():
        nonlocal tbl
        if not tbl:
            return
        rows = [r for r in tbl if not re.match(r"^\|[\s|:-]+\|?$", r)]
        out.append('<table>')
        for i, r in enumerate(rows):
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            tag = "th" if i == 0 else "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table>")
        tbl = []

    for raw in body.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("|"):
            close_list(); tbl.append(line); continue
        else:
            flush_table()
        if not line.strip():
            close_list(); continue
        if line.startswith("### "):
            close_list(); out.append(f"<h4>{inline(line[4:])}</h4>"); continue
        if line.startswith("## "):
            close_list()
            txt = line[3:]
            cls = ' class="q"' if ("Câu hỏi" in txt or "câu hỏi" in txt) else ""
            out.append(f"<h3{cls}>{inline(txt)}</h3>"); continue
        if line.startswith("# "):
            close_list(); out.append(f"<h2>{inline(line[2:])}</h2>"); continue
        if line.strip() == "---":
            close_list(); out.append("<hr>"); continue
        m = re.match(r"^\s*[-*]\s+\[( |x|X)\]\s+(.*)$", line)
        if m:
            if not lst: out.append("<ul class='chk'>"); lst = True
            done = m.group(1).lower() == "x"
            box = "☑" if done else "☐"
            cl = " done" if done else ""
            out.append(f"<li class='c{cl}'><span class='bx'>{box}</span> {inline(m.group(2))}</li>")
            continue
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if not lst: out.append("<ul>"); lst = True
            out.append(f"<li>{inline(m.group(1))}</li>"); continue
        close_list(); out.append(f"<p>{inline(line)}</p>")
    close_list(); flush_table()
    return "\n".join(out)


def status_color(s):
    return {
        "done": "#17a05a", "in-progress": "#d69200", "planning": "#8a5cf6",
        "waiting-human": "#e05353", "waiting-be": "#e05353", "blocked": "#e05353",
        "machine-decided": "#17a05a", "escalated-to-human": "#e05353",
        "resolved": "#17a05a", "debating": "#d69200",
    }.get((s or "").strip(), "#7a8794")


cards = []
total = 0
for section_title, folder in SOURCES:
    files = sorted(glob.glob(os.path.join(folder, "*.md")))
    files = [f for f in files if os.path.basename(f).upper() != "README.MD"]
    inner = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        fm, body = parse_frontmatter(text)
        total += 1
        name = os.path.basename(f)
        is_ex = "EXAMPLE" in name.upper()
        title = fm.get("task", name)
        chips = []
        for k in ("flow", "owner_now", "status", "verdict_by", "updated"):
            if fm.get(k):
                c = status_color(fm[k]) if k in ("status", "verdict_by") else "#7a8794"
                chips.append(f'<span class="chip" style="background:{c}22;color:{c}">{html.escape(fm[k])}</span>')
        ex = '<span class="ex">VÍ DỤ MẪU</span>' if is_ex else ""
        inner.append(f"""
        <details class="card" {'open' if not is_ex else ''}>
          <summary><b>{html.escape(title)}</b> {ex}<div class="chips">{''.join(chips)}</div>
            <span class="fn">{html.escape(name)}</span></summary>
          <div class="body">{md_to_html(body)}</div>
        </details>""")
    if not inner:
        inner.append('<p class="empty">Chưa có file nào.</p>')
    cards.append(f'<section><h2 class="sec">{html.escape(section_title)}</h2>{"".join(inner)}</section>')

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(PROJECT)} — Trao đổi</title>
<style>
 :root{{--bg:#f4f6f9;--card:#fff;--ink:#1a1d21;--muted:#606a76;--line:#e6e9ee;--blue:#2f6feb;--soft:#eef2f7}}
 @media(prefers-color-scheme:dark){{:root{{--bg:#0f1115;--card:#171a20;--ink:#eceef1;--muted:#9aa3af;--line:#262a31;--blue:#6ea1ff;--soft:#20252d}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);
   font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
 .wrap{{max-width:900px;margin:0 auto;padding:26px 18px 70px}}
 h1{{font-size:23px;margin:0 0 2px}} .top{{color:var(--muted);margin:0 0 20px;font-size:14px}}
 .sec{{font-size:16px;margin:26px 0 12px}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:12px;padding:4px 16px}}
 summary{{cursor:pointer;padding:12px 0;list-style:none}}
 summary::-webkit-details-marker{{display:none}}
 summary b{{font-size:15px}}
 .chips{{display:inline-flex;gap:6px;flex-wrap:wrap;margin:6px 0 0}}
 .chip{{font-size:12px;padding:2px 9px;border-radius:999px;font-weight:600}}
 .fn{{display:block;font-size:12px;color:var(--muted);margin-top:4px}}
 .ex{{font-size:11px;font-weight:700;color:#d69200;background:#d6920022;padding:2px 7px;border-radius:6px;margin-left:6px}}
 .body{{border-top:1px solid var(--line);padding:12px 0 8px}}
 .body h2{{font-size:16px;margin:14px 0 6px}} .body h3{{font-size:14px;margin:14px 0 6px}}
 .body h3.q{{color:#e05353}} .body h4{{font-size:13px;margin:10px 0 4px;color:var(--muted)}}
 .body p{{margin:6px 0}} .body ul{{margin:6px 0;padding-left:22px}}
 .body ul.chk{{list-style:none;padding-left:2px}} .body li.c{{margin:4px 0}}
 .body li.c .bx{{color:var(--blue)}} .body li.c.done{{color:var(--muted);text-decoration:line-through}}
 .body code{{background:var(--soft);padding:1px 6px;border-radius:6px;font-size:13px}}
 .body table{{border-collapse:collapse;margin:8px 0;font-size:13.5px;display:block;overflow-x:auto}}
 .body th,.body td{{border:1px solid var(--line);padding:5px 9px;text-align:left}}
 .body th{{background:var(--soft)}} .body hr{{border:0;border-top:1px solid var(--line);margin:10px 0}}
 .empty{{color:var(--muted)}} a{{color:var(--blue)}}
 .back{{display:inline-block;margin-bottom:14px;font-size:14px}}
</style></head><body><div class="wrap">
 <a class="back" href="dashboard.html">← Bảng điều khiển</a>
 <h1>💬 {html.escape(PROJECT)} — Trao đổi giữa các agent</h1>
 <p class="top">{total} cuộc · cập nhật {now}. Bấm vào từng thẻ để mở/đóng. Chạy lại
   <code>python3 scripts/build_exchanges.py</code> để làm mới.</p>
 {''.join(cards)}
</div></body></html>"""

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(page)
print(f"Đã tạo: {OUT}  ({total} cuộc trao đổi)")
