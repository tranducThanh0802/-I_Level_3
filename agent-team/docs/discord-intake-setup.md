# Dựng Discord intake (cổng nhận việc đa người) — 1 trang

> Mục tiêu: cả team gõ yêu cầu + đính kèm tài liệu vào 1 kênh Discord → agent tự nạp (context + việc) →
> làm → đẩy kết quả ra cho cả team theo dõi. Làm 1 lần, ~10 phút. Chỉ CEO/người cấp token (secret).

## 0. Tạo 2 kênh (Discord server của bạn)
- `#agent-requests` — **kênh NHẬN VÀO** (mọi người gõ yêu cầu + kéo thả tài liệu vào đây).
- `#agent-trao-doi` — **kênh ĐẨY RA** (agent báo tiến độ/câu hỏi; đã dùng webhook cũ `post_to_discord`).
- Tách 2 kênh để intake không đọc lại output của agent (dù code đã chặn, tách cho sạch).

## 1. Tạo Bot + lấy TOKEN
1. Vào https://discord.com/developers/applications → **New Application** (đặt tên, vd "Agent Intake").
2. Tab **Bot** → **Reset Token** → **Copy** (đây là token, giữ bí mật, không gửi ai).
3. Vẫn tab **Bot** → kéo xuống **Privileged Gateway Intents** → bật **MESSAGE CONTENT INTENT** → Save.
   (Không bật cái này thì bot đọc được tin nhưng `content` rỗng → không nạp được nội dung.)

## 2. Mời Bot vào server (cấp quyền ĐỌC)
1. Tab **OAuth2** → **URL Generator**.
2. **Scopes**: tick `bot`.
3. **Bot Permissions**: tick `View Channels` + `Read Message History` (chỉ cần đọc; đẩy ra dùng webhook).
4. Copy URL ở dưới → mở trên trình duyệt → chọn server của bạn → **Authorize**.
5. Vào Discord, kéo/đảm bảo bot thấy được kênh `#agent-requests` (quyền kênh).

## 3. Lấy CHANNEL ID của #agent-requests
1. Discord → **User Settings → Advanced → Developer Mode = ON**.
2. Chuột phải kênh `#agent-requests` → **Copy Channel ID**.

## 4. Điền cấu hình
Mở `scripts/discord_config.json`, thêm 2 khoá (giữ nguyên webhook cũ):
```json
{
  "webhook_agents": "…(đã có)…",
  "webhook_user":   "…(đã có)…",
  "bot_token":          "DÁN_TOKEN_Ở_BƯỚC_1",
  "intake_channel_id":  "DÁN_CHANNEL_ID_Ở_BƯỚC_3"
}
```
⚠️ **Token là secret** — file này đã nằm trong `.gitignore` (không commit). Đừng dán token ra chỗ công khai.

## 5. Chạy intake
```bash
python3 scripts/discord_intake.py          # kéo tin mới 1 lần
python3 scripts/discord_intake.py --loop    # lặp mỗi 30s (để chạy nền)
```
Hoặc để Claude chạy định kỳ: `/loop 1m python3 scripts/discord_intake.py` (hoặc cron trên máy host).

## 6. Vòng dùng hằng ngày
- **Team**: gõ vào `#agent-requests`, vd *"làm màn coupon checkout, spec đính kèm"* + kéo file spec.
- **Agent** (trên máy host, qua Claude Code):
  ```bash
  python3 scripts/agent_cli.py context     # đọc TRỌN hội thoại (nắm hết, không sót) trước khi quyết
  python3 scripts/agent_cli.py intake      # xem việc mới + skill đã route
  python3 scripts/agent_cli.py triage      # phân loại → BUG/SPEC/CEO/thảo-luận
  # → tạo bug/spec chuẩn (CEO gắn severity/priority) → python3 scripts/work_queue.py
  # → làm qua skill → gate + reviewer độc lập → CEO merge
  python3 scripts/post_to_discord.py       # đẩy tiến độ/câu hỏi ra #agent-trao-doi
  python3 scripts/agent_cli.py intake done <id>
  ```

## 7. Trục trặc thường gặp
| Hiện tượng | Nguyên nhân |
|---|---|
| `Discord API lỗi 401` | token sai/hết hạn → Reset Token lại |
| `lỗi 403` | bot chưa được mời / không có quyền xem kênh |
| Đọc được tin nhưng text rỗng | chưa bật **Message Content Intent** (bước 1.3) |
| `Không có tin mới` mãi | sai `intake_channel_id`, hoặc chưa có tin người gửi (bot/webhook bị bỏ qua) |

## Giới hạn (thành thật)
- Bot chỉ **đọc + tạo việc**; **thực thi vẫn do 1 agent Claude** chạy trên máy host (không có engine riêng).
- `merge/phát hành/tiền/đăng nhập…` trong tin nhắn → tự động **chặn, leo lên CEO** (không vào backlog agent).
