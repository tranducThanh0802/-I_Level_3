#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo bộ quản lý agent-team cho MỘT project mới (mỗi project 1 web quản lý riêng).
Copy bộ khung (agent-team/ + scripts + dashboard) vào thư mục project đích, KHÔNG copy bí mật.

Dùng:
  python3 scripts/init_project.py <thư-mục-project-đích> "Tên project"
Ví dụ:
  python3 scripts/init_project.py ~/Project/MyApp "MyApp iOS"

Sau đó trong thư mục đích:
  1) tạo scripts/discord_config.json (2 webhook riêng của project)
  2) python3 scripts/build_board.py && python3 scripts/build_exchanges.py
  3) mở dashboard.html
"""
import os, sys, json, shutil

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def die(msg):
    print("Lỗi:", msg); sys.exit(1)


def main():
    if len(sys.argv) < 3:
        die('cần: python3 scripts/init_project.py <thư-mục-đích> "Tên project"')
    dst = os.path.abspath(os.path.expanduser(sys.argv[1]))
    name = sys.argv[2]
    force = "--force" in sys.argv

    os.makedirs(dst, exist_ok=True)
    cfg_path = os.path.join(dst, "project.config.json")
    if os.path.exists(cfg_path) and not force:
        die(f"{cfg_path} đã tồn tại. Thêm --force nếu muốn ghi đè.")

    # 1) agent-team/ (khung + template + ví dụ). Giữ example làm mẫu.
    shutil.copytree(os.path.join(SRC, "agent-team"), os.path.join(dst, "agent-team"),
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("runs.jsonl"))  # log là của từng project

    # 2) scripts/*.py (KHÔNG copy bí mật / state)
    os.makedirs(os.path.join(dst, "scripts"), exist_ok=True)
    for fn in os.listdir(os.path.join(SRC, "scripts")):
        if fn.endswith(".py"):
            shutil.copy2(os.path.join(SRC, "scripts", fn), os.path.join(dst, "scripts", fn))

    # 3) dashboard mẫu + CLAUDE.md (luật vận hành)
    for fn in ("dashboard.html", "CLAUDE.md"):
        src_f = os.path.join(SRC, fn)
        if os.path.exists(src_f):
            shutil.copy2(src_f, os.path.join(dst, fn))

    # 4) config riêng của project
    code = "".join(c for c in name.upper() if c.isalnum())[:12] or "PROJECT"
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump({"name": name, "code": code}, f, ensure_ascii=False, indent=2)

    # 5) template discord_config (rỗng) + .gitignore
    dc = os.path.join(dst, "scripts", "discord_config.json")
    if not os.path.exists(dc) or force:
        with open(dc, "w", encoding="utf-8") as f:
            json.dump({"webhook_agents": "", "webhook_user": ""}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(dst, ".gitignore"), "w", encoding="utf-8") as f:
        f.write("scripts/discord_config.json\nscripts/.discord_state.json\n")

    # 6) log rỗng cho project mới
    open(os.path.join(dst, "agent-team", "logs", "runs.jsonl"), "a", encoding="utf-8").close()

    # 7) STATE.md sạch (không kế thừa trạng thái project cũ)
    state_fresh = (
        "# STATE — đang ở đâu (đọc ĐẦU TIÊN mỗi khi mở context mới)\n\n"
        f"> Project: {name}. Đọc file này trước để tiếp tục, không làm lại việc đã xong.\n\n"
        "**Cập nhật lần cuối:** (chưa có) — project mới tạo\n\n"
        "## Đang làm (task còn dở)\n_(chưa có)_\n\n"
        "## Đang chờ (bị chặn)\n_(chưa có)_\n\n"
        "## Đã xong gần đây (để không làm lại)\n_(chưa có)_\n\n"
        "## Việc kế tiếp (theo thứ tự)\n"
        "1. Điền `agent-team/memory/project-knowledge.md` (lệnh build/test, nguồn crash, BE)\n\n"
        "## Ghi chú bàn giao cho phiên sau\n_(chưa có)_\n"
    )
    with open(os.path.join(dst, "agent-team", "STATE.md"), "w", encoding="utf-8") as f:
        f.write(state_fresh)

    print(f"✅ Đã tạo bộ quản lý cho '{name}' tại: {dst}")
    print("Tiếp theo:")
    print(f"  1) Điền 2 webhook vào {dc}")
    print(f"  2) cd '{dst}' && python3 scripts/build_board.py && python3 scripts/build_exchanges.py")
    print("  3) Mở dashboard.html")
    print("  4) Điền agent-team/memory/project-knowledge.md (lệnh build/test, nguồn crash, BE)")


if __name__ == "__main__":
    main()
