---
name: security-scan
description: Quét secret/PII TRƯỚC khi lộ ra ngoài (commit/chia sẻ/publish).
---

# security-scan

**Phòng:** Chất lượng  ·  **Checkpoint CEO (A4):** Dừng nếu phát hiện khoá/secret/PII — hỏi CEO.

## Các bước
1. Chạy `python3 scripts/scan_secrets.py`.
2. Có phát hiện → gỡ/че trước khi tiếp.

## Đầu ra / bằng chứng
- 0 rò rỉ.
