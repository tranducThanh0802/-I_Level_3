# Bắt đầu một project mới (mỗi project 1 web quản lý riêng)

> Repo này là **bộ khung mẫu (template)**. Mỗi project thật = một bản sao riêng: dữ liệu riêng
> (specs/workspace/reviews/bugs/logs), web riêng (dashboard/board/exchanges), webhook Discord riêng.
> Dữ liệu KHÔNG lẫn giữa các project.

## Tạo bằng một lệnh

```bash
python3 scripts/init_project.py <thư-mục-project-đích> "Tên project"
# ví dụ:
python3 scripts/init_project.py ~/Project/MyApp "MyApp iOS"
```

Nó copy vào thư mục đích: `agent-team/` (khung + template + ví dụ), `scripts/*.py`, `dashboard.html`,
`CLAUDE.md`, và tạo `project.config.json` (tên project) + `scripts/discord_config.json` rỗng + `.gitignore`.
**Không copy bí mật** (webhook, state) và log để mỗi project sạch dữ liệu.

## Sau khi tạo, trong thư mục project

1. **Điền 2 webhook Discord** riêng của project vào `scripts/discord_config.json`.
2. Sinh web:
   ```bash
   python3 scripts/build_board.py
   python3 scripts/build_exchanges.py
   ```
3. Mở `dashboard.html` (sửa nội dung cho đúng project — file này là mẫu, không tự sinh).
4. **Điền `agent-team/memory/project-knowledge.md`**: lệnh build/test, nguồn crash, BE cùng/khác team.
   Đây là việc chặn để robot chạy được.

## Ba trang web mỗi project có

| Trang | Xem gì | Sinh bằng |
|---|---|---|
| `dashboard.html` | Tổng quan, làm gì tiếp | sửa tay (mẫu) |
| `board.html` | Trạng thái & tiến độ (quy trình, Tester, bug) | `build_board.py` |
| `exchanges.html` | Hội thoại giữa các robot | `build_exchanges.py` |

+ **Discord** real-time (2 phòng) qua `post_to_discord.py`.

## Cái gì dùng chung vs riêng từng project

- **Dùng chung (copy sang, tinh chỉnh nếu cần):** `memory/core-rules.md` (luật lõi), `memory/playbooks/`
  (cẩm nang, rubric UI/UX), cấu trúc thư mục, scripts, các doc hướng dẫn.
- **Riêng từng project:** `project.config.json`, `specs/`, `workspace/`, `reviews/`, `bugs/`, `logs/`,
  `memory/project-knowledge.md`, `discord_config.json` (webhook riêng).

## Nâng cấp bộ khung
Khi cải tiến template ở repo gốc (sửa script, rubric, core-rules), copy lại các file dùng chung sang
từng project — hoặc chạy lại `init_project.py ... --force` (cẩn thận: ghi đè config).
```
