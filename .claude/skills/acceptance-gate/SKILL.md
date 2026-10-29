---
name: acceptance-gate
description: Máy chốt 'XONG': chặn nếu acceptance còn ô trống / ✅ thiếu bằng chứng / reviewer chưa PASS (A4).
---

# acceptance-gate

**Phòng:** Chất lượng  ·  **Checkpoint CEO (A4):** Agent KHÔNG được tự tuyên bố xong; phải reviewer ≠ author PASS + gate xanh.

## Các bước
1. Chạy `python3 scripts/acceptance_gate.py agent-team/acceptance/<feature>.md`.
2. FAIL → bổ sung bằng chứng / out_of_scope / chờ reviewer; chỉ 'xong' khi exit 0.

## Đầu ra / bằng chứng
- Gate xanh = điều kiện cần để CEO duyệt cuối.
