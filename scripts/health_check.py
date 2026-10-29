#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
health_check — tự động hoá ĐẦU VIỆC LẶP "soát sức khoẻ công ty agent" (A6).

Chạy trước khi giao / sau khi thêm skill. Kiểm (máy, không bằng lời):
  1. Mỗi .claude/skills/<x>/SKILL.md có frontmatter đủ: name + description.
  2. Các script xương sống tồn tại: agent_cli, ui_lint, acceptance_gate, run_regression (nếu khai).
  3. Tài liệu tổ chức tồn tại: ORG.md, RUBRIC-MAP.md, acceptance/_TEMPLATE.md.
  4. CLI liệt kê được skill (số > 0).

exit 0 = khoẻ · exit 1 = có lỗi (liệt kê cụ thể). Có nhánh ngoại lệ: thiếu file → báo rõ, không crash.
"""
import os, re, sys, glob, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")

def frontmatter(p):
    m = re.match(r"^---\n(.*?)\n---", open(p, encoding="utf-8").read(), re.S)
    d = {}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l: k, v = l.split(":", 1); d[k.strip()] = v.strip()
    return d

def main():
    errs, oks = [], []

    # 1. skills
    skill_files = sorted(glob.glob(os.path.join(SKILLS, "*", "SKILL.md")))
    if not skill_files: errs.append("Không có skill nào trong .claude/skills/")
    for p in skill_files:
        name = os.path.basename(os.path.dirname(p))
        fm = frontmatter(p)
        if not fm.get("name"): errs.append(f"skill '{name}': thiếu frontmatter `name`")
        if not fm.get("description"): errs.append(f"skill '{name}': thiếu `description`")
    oks.append(f"{len(skill_files)} skill có SKILL.md")

    # 2. scripts xương sống
    for s in ["agent_cli.py", "ui_lint.py", "acceptance_gate.py"]:
        if os.path.exists(os.path.join(ROOT, "scripts", s)): oks.append(f"script {s} ✓")
        else: errs.append(f"thiếu scripts/{s}")

    # 3. tài liệu tổ chức
    for f in ["agent-team/ORG.md", "agent-team/RUBRIC-MAP.md", "agent-team/acceptance/_TEMPLATE.md"]:
        if os.path.exists(os.path.join(ROOT, f)): oks.append(f"{f} ✓")
        else: errs.append(f"thiếu {f}")

    # 4. CLI liệt kê skill
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "agent_cli.py"), "skills"],
                             capture_output=True, text=True, timeout=30).stdout
        n = len(re.findall(r"^    \S", out, re.M))
        if n > 0: oks.append(f"CLI liệt kê {n} skill")
        else: errs.append("CLI không liệt kê được skill")
    except Exception as e:
        errs.append(f"CLI lỗi: {e}")

    print(f"HEALTH-CHECK công ty agent — {len(oks)} OK · {len(errs)} lỗi")
    for o in oks: print(f"  ✓ {o}")
    for e in errs: print(f"  ⛔ {e}")
    if errs: print("\n⛔ CHƯA khoẻ — sửa rồi chạy lại."); sys.exit(1)
    print("\n✅ Công ty agent KHOẺ."); sys.exit(0)

if __name__ == "__main__": main()
