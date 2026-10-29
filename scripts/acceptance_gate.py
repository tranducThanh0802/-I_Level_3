#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acceptance_gate — cổng MÁY chốt "XONG" (A4 điểm chặn): agent KHÔNG tự ký.

CHẶN (exit 1) nếu acceptance/<feature>.md: còn tiêu chí ⛔/ô trống/placeholder `<...>`;
dòng ✅ thiếu bằng chứng; dòng 📋 mà "Out of scope" rỗng; (màn UI) thiếu 4 trạng thái;
reviewer độc lập trống / TRÙNG author / chưa tick / Verdict != PASS.

Dùng: python3 scripts/acceptance_gate.py agent-team/acceptance/<feature>.md
      python3 scripts/acceptance_gate.py --all
"""
import os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACC = os.path.join(ROOT, "agent-team", "acceptance")
PH = re.compile(r"<[^>\n]+>"); DONE="✅"; DEBT="📋"


def fm(t):
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S); d={}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l: k,v=l.split(":",1); d[k.strip()]=v.strip()
    return d

def sect(t, title):
    m=re.search(r"^##\s+"+re.escape(title), t, re.M)
    if not m: return ""
    s=m.end(); nx=re.search(r"^##\s+", t[s:], re.M)
    return t[s:s+nx.start()] if nx else t[s:]

def rows(b):
    out=[]
    for l in b.splitlines():
        l=l.strip()
        if not l.startswith("|"): continue
        c=[x.strip() for x in l.strip("|").split("|")]
        if not c or set("".join(c))<=set("-: "): continue
        out.append(c)
    return out

def empty(s): return (not s) or PH.search(s) is not None

def check(path):
    t=open(path, encoding="utf-8").read(); f=fm(t); author=f.get("author",""); errs=[]
    oos=[l for l in sect(t,"Out of scope").splitlines() if l.strip().startswith("-") and "(chưa" not in l and not empty(l.strip("- ").strip())]
    crit=[r for r in rows(sect(t,"Tiêu chí nghiệm thu")) if r and r[0].isdigit()]
    if not crit: errs.append("Chưa có tiêu chí nào.")
    for r in crit:
        if len(r)<5: errs.append(f"Dòng #{r[0]} thiếu cột."); continue
        num,desc,evid,tt=r[0],r[1],r[3],r[4]
        if empty(desc): errs.append(f"#{num}: mô tả trống/placeholder.")
        if DONE in tt:
            if empty(evid): errs.append(f"#{num}: ✅ nhưng KHÔNG bằng chứng.")
        elif DEBT in tt:
            if not oos: errs.append(f"#{num}: 📋 nhưng Out of scope rỗng.")
        else: errs.append(f"#{num}: chưa xong (TT='{tt or '∅'}').")
    four=sect(t,"Bốn trạng thái")
    if four.strip():
        seen={r[0].lower():r[1] for r in rows(four) if r and r[0].lower() in {"loading","rỗng","lỗi","mất mạng"} and len(r)>=2}
        for st in {"loading","rỗng","lỗi","mất mạng"}:
            tt=seen.get(st,"")
            if not (DONE in tt or DEBT in tt or "n/a" in tt.lower()): errs.append(f"Trạng thái '{st}' chưa khai.")
    rv=sect(t,"Phản biện độc lập"); reviewer=""; checked=False; verdict=""
    for l in rv.splitlines():
        lo=l.lower()
        if "reviewer:" in lo: reviewer=l.split(":",1)[1].strip()
        if "đối chiếu" in lo and "[x]" in lo: checked=True
        if "verdict:" in lo: verdict=l.split(":",1)[1].strip().upper()
    if empty(reviewer): errs.append("Reviewer trống/placeholder.")
    elif author and reviewer.strip()==author.strip(): errs.append(f"Reviewer TRÙNG author ('{author}').")
    if not checked: errs.append("Reviewer chưa tick '[x]' đối chiếu.")
    if "PASS" not in verdict: errs.append(f"Verdict != PASS ('{verdict or '∅'}').")
    return os.path.relpath(path,ROOT), errs

def main():
    args=[a for a in sys.argv[1:] if a!="--all"]
    files = args if args and "--all" not in sys.argv else [f for f in glob.glob(os.path.join(ACC,"*.md")) if os.path.basename(f)!="_TEMPLATE.md"]
    if not files: print("Chưa có file acceptance nào."); sys.exit(1)
    total=0
    for p in files:
        rel,errs=check(p)
        if errs:
            total+=len(errs); print(f"⛔ {rel} — {len(errs)} vấn đề:"); [print(f"   - {e}") for e in errs]
        else: print(f"✅ {rel} — mọi tiêu chí có bằng chứng, reviewer độc lập PASS.")
    if total: print(f"\nTổng {total} vấn đề → CHẶN. Chưa được tuyên bố 'xong'."); sys.exit(1)
    print("\n✅ Acceptance gate ĐẠT.")

if __name__=="__main__": main()
