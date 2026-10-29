---
name: ui-lint
description: Máy chặn icon lỗi: emoji-tofu trong UI + BrandIcon/asset không tồn tại.
---

# ui-lint

**Phòng:** Chất lượng  ·  **Checkpoint CEO (A4):** Là GATE: exit 1 → chặn commit (A4.2 điểm chặn). Ngoại lệ phải đánh dấu `// lint:allow-emoji`.

## Các bước
1. Chạy `python3 scripts/ui_lint.py` (quét thư mục UI).
2. FAIL → sửa hết rồi mới commit (pre-commit hook tự chạy).

## Đầu ra / bằng chứng
- 0 vi phạm → qua. Seed script + hook qua `scripts/install_hooks.sh`.
