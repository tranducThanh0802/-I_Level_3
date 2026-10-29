#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ui_lint — cổng MÁY cho icon/emoji (A4.2 điểm chặn). Chặn: emoji trong code UI (tofu khi
bọc font app) + ảnh/asset được tham chiếu nhưng không tồn tại.

Ngoại lệ có đánh dấu: dòng chứa `lint:allow-emoji` (vd chuỗi chia sẻ ra app ngoài).
Thư mục UI quét: biến môi trường UI_DIR, hoặc đối số, mặc định "App" (tương đối gốc repo).

Dùng: python3 scripts/ui_lint.py [--quiet] [UI_DIR]
"""
import os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if a != "--quiet"]
UI_DIR = os.path.join(ROOT, args[0] if args else os.environ.get("UI_DIR", "App"))
QUIET = "--quiet" in sys.argv

EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0000FE00-\U0000FE0F\U00002122\U00002139]")
ASSET_REF = re.compile(r'"(ic_ph_[a-z0-9_]+|fl_[a-z0-9_]+|sol_[a-z0-9_]+)"')
IMG_LIT = re.compile(r'(?:BrandIcon|AutoBrandIcon)\(\s*"([A-Za-z0-9_]+)"')
PLAIN_IMG = re.compile(r'(?<![A-Za-z])Image\(\s*"([A-Za-z0-9_ ]+)"\s*\)')


def assets():
    n=set()
    for d in glob.glob(os.path.join(ROOT,"**","*.imageset"),recursive=True): n.add(os.path.basename(d)[:-9])
    for d in glob.glob(os.path.join(ROOT,"**","*.colorset"),recursive=True): n.add(os.path.basename(d)[:-9])
    return n

def strip(l): i=l.find("//"); return l[:i] if i>=0 else l

def main():
    if not os.path.isdir(UI_DIR):
        if not QUIET: print(f"✅ UI lint: bỏ qua (không có thư mục UI '{os.path.relpath(UI_DIR,ROOT)}')."); sys.exit(0)
        sys.exit(0)
    av=assets(); emo=[]; miss=[]
    for p in glob.glob(os.path.join(UI_DIR,"**","*.swift"),recursive=True):
        rel=os.path.relpath(p,ROOT)
        for n,raw in enumerate(open(p,encoding="utf-8"),1):
            code=strip(raw)
            if EMOJI.search(code) and "lint:allow-emoji" not in raw: emo.append((rel,n,raw.strip()[:90]))
            refs=set(ASSET_REF.findall(code))|set(IMG_LIT.findall(code))
            for m in PLAIN_IMG.findall(code):
                if m in av or re.match(r'^(ic_ph_|fl_|sol_)',m): refs.add(m)
            for name in refs:
                if name not in av: miss.append((rel,n,name))
    if emo:
        print(f"⛔ EMOJI trong code UI ({len(emo)}) — tofu trên máy user, đổi BrandIcon/SF:")
        [print(f"   {r}:{n}  {t}") for r,n,t in emo]
    if miss:
        print(f"⛔ ASSET ICON THIẾU ({len(miss)}):")
        [print(f"   {r}:{n}  \"{name}\"") for r,n,name in miss]
    if emo or miss:
        print(f"\nTổng {len(emo)} emoji · {len(miss)} asset thiếu → CHẶN."); sys.exit(1)
    if not QUIET: print(f"✅ UI lint ĐẠT: 0 emoji · 0 asset thiếu (quét {os.path.relpath(UI_DIR,ROOT)})")

if __name__=="__main__": main()
