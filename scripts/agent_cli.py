#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent — CLI điều phối "công ty agent" (hình hài A8.2: đóng gói, người khác dựng lại được).

Mọi năng lực là SKILL rời (.claude/skills/<tên>/SKILL.md), CEO (người) duyệt ở checkpoint.
CLI này là CỬA VÀO chung: xem tổ chức, liệt kê skill, chạy các GATE máy (A4 điểm chặn), soi rubric.

Dùng:
  python3 scripts/agent_cli.py org            # sơ đồ tổ chức
  python3 scripts/agent_cli.py skills         # liệt kê mọi skill + mô tả (phòng ban)
  python3 scripts/agent_cli.py skill <tên>    # xem 1 skill
  python3 scripts/agent_cli.py workflow       # luồng chuẩn 1 feature (A1)
  python3 scripts/agent_cli.py rubric         # bản đồ tiêu chí ↔ skill ↔ bằng chứng
  python3 scripts/agent_cli.py gate [accept.md]  # chạy ui_lint + acceptance_gate (A4)
"""
import os, re, sys, subprocess, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")
AGENT = os.path.join(ROOT, "agent-team")
SCRIPTS = os.path.join(ROOT, "scripts")

DEPT = {  # tên phòng cho nhóm skill (prefix)
    "research-idea": "Sản phẩm", "write-spec": "Sản phẩm", "review-spec": "Sản phẩm",
    "make-acceptance": "Kỹ thuật", "implement": "Kỹ thuật", "fix-bug": "Kỹ thuật",
    "independent-review": "Chất lượng", "ui-lint": "Chất lượng", "acceptance-gate": "Chất lượng",
    "port-oracle-tests": "Chất lượng", "regression-gate": "Chất lượng", "security-scan": "Chất lượng",
    "knowledge-base": "Tri thức", "bug-memory": "Tri thức", "outer-loop": "Tri thức",
    "orchestrate": "Vận hành", "work-queue": "Vận hành", "run-log": "Vận hành", "automate-repeat": "Vận hành",
    "my-replica": "A7 (điểm cộng)",
}


def _frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); fm[k.strip()] = v.strip()
    return fm


def _all_skills():
    out = []
    for p in sorted(glob.glob(os.path.join(SKILLS, "*", "SKILL.md"))):
        fm = _frontmatter(p)
        name = fm.get("name", os.path.basename(os.path.dirname(p)))
        out.append((name, fm.get("description", ""), p))
    return out


def cmd_skills():
    skills = _all_skills()
    if not skills:
        print("Chưa có skill nào trong .claude/skills/"); return
    by_dept = {}
    for name, desc, _ in skills:
        by_dept.setdefault(DEPT.get(name, "Khác"), []).append((name, desc))
    print(f"CÔNG TY AGENT — {len(skills)} skill (CEO = người, duyệt checkpoint):\n")
    for dept in ["Sản phẩm", "Kỹ thuật", "Chất lượng", "Tri thức", "Vận hành", "A7 (điểm cộng)", "Khác"]:
        if dept in by_dept:
            print(f"▸ {dept}")
            for name, desc in by_dept[dept]:
                print(f"    {name:<20} {desc}")
            print()


def cmd_skill(name):
    p = os.path.join(SKILLS, name, "SKILL.md")
    if not os.path.exists(p):
        print(f"Không có skill '{name}'. Xem: agent_cli.py skills"); sys.exit(1)
    print(open(p, encoding="utf-8").read())


def _show(f):
    p = os.path.join(AGENT, f)
    print(open(p, encoding="utf-8").read() if os.path.exists(p) else f"(chưa có {f})")


def cmd_gate(args):
    """A4 điểm chặn: chạy gate máy. exit != 0 nếu bất kỳ gate chặn."""
    rc = 0
    uil = os.path.join(SCRIPTS, "ui_lint.py")
    if os.path.exists(uil):
        print("== ui_lint =="); rc |= subprocess.call([sys.executable, uil, "--quiet"])
    acc = os.path.join(SCRIPTS, "acceptance_gate.py")
    if os.path.exists(acc):
        print("== acceptance_gate =="); rc |= subprocess.call([sys.executable, acc] + (args or ["--all"]))
    if not os.path.exists(uil) and not os.path.exists(acc):
        print("(Chưa seed ui_lint.py / acceptance_gate.py vào scripts/ — xem skill ui-lint / acceptance-gate)")
    sys.exit(1 if rc else 0)


def cmd_check():
    """Chạy trọn bộ việc lặp đã tự động: health-check + gate QA. 1 lệnh trước khi giao."""
    rc = 0
    hc = os.path.join(SCRIPTS, "health_check.py")
    if os.path.exists(hc):
        print("== health-check =="); rc |= subprocess.call([sys.executable, hc])
    print("\n== gate QA ==");
    try: cmd_gate([])
    except SystemExit as e: rc |= (e.code or 0)
    sys.exit(1 if rc else 0)


def cmd_new_skill(a):
    """Tự động hoá việc lặp 'thêm skill mới': scaffold SKILL.md."""
    if len(a) < 3:
        print('Dùng: agent_cli.py new-skill <tên> <phòng> "<mô tả>"'); sys.exit(1)
    name, dept, desc = a[0], a[1], " ".join(a[2:])
    d = os.path.join(SKILLS, name); os.makedirs(d, exist_ok=True)
    body = (f"---\nname: {name}\ndescription: {desc}\n---\n\n# {name}\n\n"
            f"**Phòng:** {dept}  ·  **Checkpoint CEO (A4):** <điền>\n\n## Các bước\n1. <điền>\n\n"
            f"## Đầu ra / bằng chứng\n- <điền>\n")
    open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
    print(f"Đã tạo skill '{name}' ({dept}). Nhớ thêm vào DEPT trong agent_cli.py nếu muốn nhóm đúng phòng.")


def cmd_log(a):
    """Tự động hoá việc lặp 'ghi run-log': append 1 dòng runs.jsonl."""
    import json, datetime
    if len(a) < 2:
        print('Dùng: agent_cli.py log "<task>" "<result>" [repeat_task]'); sys.exit(1)
    now = datetime.datetime.now().astimezone()
    run = {"run_id": now.strftime("%Y-%m-%dT%H-%M-%S") + "_" + re.sub(r"\W+", "-", a[0])[:24],
           "agent": "ops", "flow": "ops", "task": a[0],
           "repeat_task": a[2] if len(a) > 2 else None,
           "started_at": now.isoformat(), "ended_at": now.isoformat(),
           "size": "S", "baseline_source": "agent-estimated", "human_minutes": None,
           "steps": [{"step": "run", "check": "-", "result": a[1]}],
           "failed_at": None, "manual_fixes": [], "outcome": "used", "automated": True, "demo": False}
    p = os.path.join(AGENT, "logs", "runs.jsonl")
    with open(p, "a", encoding="utf-8") as f: f.write(json.dumps(run, ensure_ascii=False) + "\n")
    print(f"Logged: {run['run_id']} (baseline_source=agent-estimated → chưa tính §6; CEO đặt baseline để hợp lệ)")


def main():
    a = sys.argv[1:]
    cmd = a[0] if a else "help"
    if cmd == "skills": cmd_skills()
    elif cmd == "check": cmd_check()
    elif cmd == "new-skill": cmd_new_skill(a[1:])
    elif cmd == "log": cmd_log(a[1:])
    elif cmd == "skill" and len(a) > 1: cmd_skill(a[1])
    elif cmd == "org": _show("ORG.md")
    elif cmd == "rubric": _show("RUBRIC-MAP.md")
    elif cmd == "kb": _show(os.path.join("memory", "KB-CHANGELOG.md"))
    elif cmd == "repeat": _show("repeat-tasks.md")
    elif cmd == "replica": _show("ceo-profile.md")   # A7: hồ sơ để my-replica đứng thay CEO (quyết qua skill)
    elif cmd == "workflow":
        print("Luồng chuẩn 1 feature (ghép skill — A1):\n"
              "  CEO ra đề → research-idea → write-spec → review-spec →[CEO duyệt]→ make-acceptance\n"
              "   → implement → gate(ui-lint+acceptance) → independent-review(≠author)\n"
              "   →[CEO duyệt]→ run-log → outer-loop → CEO merge/phát hành")
    elif cmd == "gate": cmd_gate(a[1:])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
