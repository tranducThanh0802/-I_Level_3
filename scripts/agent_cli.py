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


# Định tuyến ý định → skill (tất-định, minh bạch). Mỗi skill: danh sách từ khoá (vi/en).
# Từ khoá ý định → skill. Nới theo CÁCH NÓI THẬT của CEO (rút từ các phiên Lingora).
INTENT = {
    "fix-bug": ["crash", "bug", "stack trace", "nil", "exception", "văng", "đứng màn", "báo lỗi",
                "thi xong báo lỗi", "không update", "ko update", "không lưu", "ko lưu", "mất thông tin",
                "không hoạt động", "không được", "không đc", "ko đc", "bị lỗi", "lag", "giật",
                "chưa mượt", "không mượt", "ko mượt", "load gì", "sao ko", "sao không", "chậm"],
    "research-idea": ["ý tưởng", "tìm hiểu", "nghiên cứu", "idea", "khám phá", "đề bài thô", "gom yêu cầu"],
    "write-spec": ["viết spec", "yêu cầu", "tính năng mới", "feature mới", "viết quy trình", "đề bài",
                   "thêm chức năng", "làm màn mới", "thiết kế luồng"],
    "review-spec": ["soát spec", "duyệt spec", "review spec", "kiểm spec"],
    "make-acceptance": ["acceptance", "nghiệm thu", "tiêu chí", "checklist", "điều kiện xong"],
    "implement": ["implement", "viết code", "dựng màn", "sửa ui", "sửa lại", "làm lại", "thêm nút",
                  "copy từ android", "copy json", "copy hết", "làm nổi bật", "bị mờ", "màu sắc", "căn lại",
                  "chưa đẹp", "tệ quá", "ui sai", "ui/ux", "thiết kế lại", "đổi màu", "font", "title",
                  "splash", "onboarding", "làm đẹp", "lưu database", "lưu db", "lưu như vậy", "animation"],
    "independent-review": ["check lại", "xem lại", "kiểm lại", "soát lại", "review lại", "review", "phản biện",
                           "độc lập", "đối chiếu", "bác bỏ", "kiểm tra lại", "giống android", "không giống",
                           "ko giống", "chả giống", "khác android", "sai so với", "parity", "re-check",
                           "check toàn bộ", "check hết", "review toàn bộ"],
    "ui-lint": ["icon", "emoji", "asset", "tofu", "biểu tượng", "ảnh icon", "icon bị lỗi"],
    "acceptance-gate": ["xong chưa", "đã xong", "chốt xong", "done", "setup đúng chưa", "đúng chưa",
                        "ổn chưa", "được chưa", "ok chưa"],
    "port-oracle-tests": ["oracle", "port test", "test android", "parity logic", "logic nghiệp vụ",
                          "logic không giống", "logic khác", "số liệu", "giá trị kỳ vọng", "số không khớp",
                          "giá trị nào", "số xp", "điểm số"],
    "regression-gate": ["hồi quy", "regression", "baseline", "tụt baseline"],
    "security-scan": ["secret", "pii", "bảo mật", "khoá bí mật", "token lộ", "rò rỉ"],
    "knowledge-base": ["quy tắc", "luật lõi", "knowledge base", "kb", "version kb", "cẩm nang", "kiến thức"],
    "bug-memory": ["bug cũ", "fingerprint", "đã sửa chưa", "gặp lại", "trùng bug", "sửa rồi"],
    "outer-loop": ["retro", "loop ngoài", "cải thiện quy trình", "lỗi lặp", "sửa cẩm nang"],
    "orchestrate": ["điều phối", "orchestrate", "chạy feature", "trọn quy trình", "từ đầu đến cuối",
                    "làm nốt", "làm hết", "tiếp tục", "các task", "làm tiếp", "task trên", "phải làm hết"],
    "work-queue": ["hàng đợi", "queue", "nhận việc", "danh sách việc"],
    "run-log": ["ghi log", "run log", "nhật ký chạy", "log lại"],
    "automate-repeat": ["tự động hoá", "việc lặp", "auto được", "80%", "lặp lại", "automation"],
    "my-replica": ["thay tôi", "bản sao", "replica", "quyết thay", "trợ lý của tôi"],
}
# Nhóm cấm-tự-quyết → KHÔNG route sang skill, mà LEO LÊN CEO (luật lõi §1/§2). Chỉ bắt ĐỘNG TỪ ĐỔI,
# không bắt câu HỎI/kiểm (vd "domain đã đúng chưa" là verify, không phải đổi).
ESCALATE = ["merge", "phát hành", "release", "đẩy store", "lên store", "tiền", "thanh toán", "in-app",
            "đăng nhập", "xoá dữ liệu", "xóa dữ liệu", "đổi api contract", "sửa api contract",
            "đổi schema", "thêm thư viện", "đổi kiến trúc", "sửa config phát hành"]


def _route(text):
    """Trả (escalate_hits, scored[(count,len,skill,hit)]) — dùng chung cho route + intake."""
    text = text.lower()
    esc = [k for k in ESCALATE if k in text]
    scored = []
    for skill, kws in INTENT.items():
        hit = [k for k in kws if k in text]
        if hit: scored.append((len(hit), sum(len(k) for k in hit), skill, hit))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return esc, scored


def cmd_route(a):
    if not a:
        print('Dùng: agent_cli.py route "<đoạn text mô tả việc>"'); sys.exit(1)
    esc, scored = _route(" ".join(a))
    if esc:
        print(f"⛔ DỪNG — chạm nhóm cấm-tự-quyết ({', '.join(esc)}) → LEO LÊN CEO (luật #1/#2).")
        print("   Agent/replica KHÔNG tự quyết. Đóng gói 2 phương án + hệ quả, hỏi người (core-rules §4).")
        return
    if not scored:
        print("Không khớp từ khoá rõ ràng → bắt đầu `orchestrate`, hoặc `research-idea` nếu mơ hồ."); return
    print(f'Định tuyến cho: "{" ".join(a)[:70]}"')
    for i, (n, _l, skill, hit) in enumerate(scored[:3]):
        print(f"  {'→ DÙNG' if i == 0 else '  (hoặc)'} {skill:<20} (khớp: {', '.join(hit)})")
    print(f"\nGợi ý: chạy `agent_cli.py skill {scored[0][2]}` để xem các bước.")


INTAKE = os.path.join(AGENT, "intake")

def cmd_intake(a):
    """Cổng NHẬN VIỆC đa người (PO/dev/QA nạp yêu cầu + tài liệu) → hàng đợi chung, tự route."""
    import datetime
    os.makedirs(INTAKE, exist_ok=True)
    sub = a[0] if a else "list"
    if sub == "add":
        if len(a) < 3:
            print('Dùng: intake add "<người gửi>" "<yêu cầu>" [đường-dẫn-tài-liệu]'); sys.exit(1)
        requester, rest = a[1], a[2:]
        doc = rest.pop() if rest and os.path.exists(rest[-1]) else None
        text = " ".join(rest)
        iid = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        esc, scored = _route(text)
        routed = "ESCALATE-CEO" if esc else (scored[0][2] if scored else "orchestrate")
        body = (f"---\nid: {iid}\nsource: manual\nrequester: {requester}\nstatus: pending\n"
                f"routed_skill: {routed}\n---\n# Yêu cầu\n{text}\n")
        if doc: body += f"\n## Tài liệu đính kèm\n- {doc}\n"
        open(os.path.join(INTAKE, iid + ".md"), "w", encoding="utf-8").write(body)
        print(f"✅ Nhận việc {iid} từ '{requester}' → route: {routed}" + (f" · đính kèm: {doc}" if doc else ""))
    elif sub == "done" and len(a) > 1:
        p = os.path.join(INTAKE, a[1] + ".md")
        if not os.path.exists(p): print(f"Không có việc {a[1]}"); sys.exit(1)
        t = open(p, encoding="utf-8").read().replace("status: pending", "status: done")
        open(p, "w", encoding="utf-8").write(t); print(f"✅ Đóng việc {a[1]}")
    else:   # list
        pend = [p for p in sorted(glob.glob(os.path.join(INTAKE, "*.md")))
                if "status: pending" in open(p, encoding="utf-8").read()]
        if not pend: print("Hàng đợi intake trống."); return
        print(f"📥 HÀNG ĐỢI INTAKE — {len(pend)} việc chờ (PO/dev/QA nạp vào):")
        for p in pend:
            fm = _frontmatter(p)
            txt = open(p, encoding="utf-8").read().split("# Yêu cầu", 1)[-1].strip().splitlines()
            snippet = (txt[0] if txt else "")[:60]
            flag = "⛔LEO-CEO" if fm.get("routed_skill") == "ESCALATE-CEO" else "→ " + fm.get("routed_skill", "?")
            print(f"  [{fm.get('id')}] {fm.get('requester',''):<12} {flag:<22} {snippet}")
        print("\nAgent: chạy `skill <routed_skill>` cho từng việc; xong → `intake done <id>`; báo lại Discord qua post_to_discord.py.")


def cmd_context(a):
    """In TRỌN hội thoại kênh chung (channel-log) để agent/CEO 'nắm hết thông tin' trước khi quyết."""
    import json as _j
    log = os.path.join(INTAKE, "channel-log.jsonl")
    if not os.path.exists(log):
        print("Chưa có context (chưa nối Discord intake hoặc chưa có tin). Xem discord_intake.py."); return
    rows = [l for l in open(log, encoding="utf-8") if l.strip()]
    n = int(a[0]) if a and a[0].isdigit() else 30
    print(f"🧠 CONTEXT KÊNH CHUNG — {len(rows)} tin (hiện {min(n,len(rows))} gần nhất). Agent/CEO đọc trước khi quyết:")
    for l in rows[-n:]:
        m = _j.loads(l)
        doc = f"  [+{len(m['docs'])} tệp]" if m.get("docs") else ""
        print(f"  · {m.get('who','?'):<12} {(m.get('text') or '[tài liệu]')}{doc}")


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
    elif cmd == "boot":   # SessionStart hook in cái này → mỗi phiên BẬT agent-mode (không phải Claude thuần)
        nsk = len(_all_skills())
        print("🏢 CÔNG TY AGENT ĐANG BẬT — bạn KHÔNG phải Claude thuần, đang vận hành theo agent-team.\n"
              f"- {nsk} skill (`agent_cli.py skills`) · Luồng (`workflow`) · Rubric (`rubric`) · Tổ chức (`org`).\n"
              "- Phân loại việc → skill: `agent_cli.py route \"<đoạn text>\"` (chặn nhóm cấm-tự-quyết → leo lên CEO).\n"
              "- LUẬT CỨNG: 'Xong' = acceptance_gate.py XANH + reviewer ĐỘC LẬP ≠ author PASS; agent tự khen không tính.\n"
              "- Agent KHÔNG merge/phát hành (luật #2) — việc đó của CEO (người).\n"
              "- Pre-commit cưỡng chế: scan_secrets + ui_lint. Cổng 'xong': `agent_cli.py gate`.\n"
              "- LÀM TRƯỚC: đọc `agent-team/STATE.md`. Gate đang chạy = bằng chứng agent thật (không phải lời).")
    elif cmd == "status":   # statusLine: 1 dòng ngắn cho thấy agent-mode bật
        hook = "pre-commit✓" if os.path.exists(os.path.join(ROOT, ".git", "hooks", "pre-commit")) else "pre-commit✗"
        print(f"🏢 agent-company · {len(_all_skills())} skills · gate:{hook}")
    elif cmd == "route": cmd_route(a[1:])
    elif cmd == "intake": cmd_intake(a[1:])
    elif cmd == "context": cmd_context(a[1:])
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
