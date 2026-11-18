# Phân quyền & kiểm soát dữ liệu — runbook (A8)

> Mục tiêu: trả lời được 3 câu rubric A8 đòi — **(1) khóa để đâu, (2) ai đọc được gì + lọc/ẩn danh
> trước khi dữ liệu rời hệ thống, (3) thu hồi quyền khi người nghỉ/đổi vị trí.**
> File này là người sửa. Agent đọc, không sửa.

## 1. Khóa & bí mật để ở đâu (A8 mức 3)
| Bí mật | Nằm ở | Bảo vệ |
|---|---|---|
| Discord `bot_token`, 2 webhook | `scripts/discord_config.json` | **gitignore** (không commit) + không in ra log. |
| State intake/post | `scripts/.discord_*state*.json` | gitignore. |
| — | KHÔNG để trong code/prompt/CHANGELOG | `scan_secrets.py` chặn pre-commit. |

Không có khóa nào nằm thẳng trong mã nguồn hay tài liệu. Kiểm bất kỳ lúc nào: `python3 scripts/scan_secrets.py --all`.

## 2. Phân loại dữ liệu (ai đọc được gì) (A8 mức 4)
| Loại dữ liệu | Nằm ở | Ai đọc | Rời hệ thống? |
|---|---|---|---|
| **Bí mật** (token/webhook) | `discord_config.json` | chỉ CEO/người cấp | **KHÔNG BAO GIỜ**. |
| **Nội bộ – trọn hội thoại** | `agent-team/intake/channel-log.jsonl` | CEO + agent (ra quyết định) | Local-only, gitignore. KHÔNG đẩy ra. |
| **Nội bộ – việc/tài liệu** | `intake/*.md`, `intake/docs/` | CEO + agent | Local-only, gitignore. |
| **Đẩy ra Discord** (tiến độ, câu hỏi, verdict) | webhook → kênh | cả team trong server | **CÓ** → bắt buộc qua `redact()`. |

**Lọc/ẩn danh trước khi rời hệ thống:** MỌI đường đẩy ra Discord đều chạy `redact()`
(`post_to_discord.py` + `_ack()` của `discord_intake.py`): tự thay webhook/AWS/Google key/JWT bằng `[ẨN-SECRET]`
và che đầu email (`a***@domain`). → Dữ liệu nhạy cảm không lọt ra kênh dù agent lỡ chèn vào nội dung.

**Quyền kênh Discord (người cấu hình trong Server Settings → Roles/Channels):**
- `#agent-requests` (NHẬN): ai trong cty gõ được; bot chỉ cần `View Channels` + `Read Message History`.
- `#agent-trao-doi` (ĐẨY RA): cả team xem; chỉ webhook ghi.
- Người ngoài cty: không mời vào server → không đọc được. (Nội bộ, không đăng nhập — theo yêu cầu CEO.)

## 3. Thu hồi quyền khi người nghỉ/đổi vị trí (A8 mức 5)
Chạy checklist này khi 1 thành viên offboard **hoặc** khi nghi lộ khóa:
1. **Discord:** Server Settings → Members → gỡ role/kick người đó khỏi server (mất quyền đọc mọi kênh ngay).
2. **Xoay bot token** (nếu người đó từng cầm): Developer Portal → Bot → **Reset Token** → cập nhật `discord_config.json`.
3. **Xoay webhook** (nếu URL từng chia sẻ): Channel → Integrations → Webhooks → **Delete** cái cũ, tạo mới → cập nhật config.
4. **Ghi lại**: thêm 1 dòng vào `CHANGELOG.md` (ngày + lý do thu hồi) để có vết.
5. **Kiểm**: `python3 scripts/scan_secrets.py --all` + gửi `post_to_discord.py --test` xác nhận khóa mới chạy.

> Nguyên tắc: **siết được quyền sau khi phát hiện rủi ro, chỉ trong 1 lần theo checklist này** — đúng mức 5 rubric.
> Quyền chỉ cấp tối thiểu (bot chỉ đọc; đẩy ra qua webhook) → bề mặt rủi ro nhỏ.
