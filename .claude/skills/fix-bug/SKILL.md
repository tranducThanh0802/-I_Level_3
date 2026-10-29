---
name: fix-bug
description: Sửa bug: tra bug-memory trước (có thể đã sửa), fingerprint, thêm test hồi quy.
---

# fix-bug

**Phòng:** Kỹ thuật  ·  **Checkpoint CEO (A4):** Bug do nguồn chân lý/BE → đóng gói gửi lên, KHÔNG tự sửa contract.

## Các bước
1. Tra `memory/bugs/` theo fingerprint; nếu trùng → áp cách cũ, đừng sửa lại.
2. Tái hiện → sửa → thêm TEST bắt đúng bug (chống tái phát).
3. Ghi bug mới vào bug-memory.

## Đầu ra / bằng chứng
- Fix + test hồi quy + mục bug-memory.
