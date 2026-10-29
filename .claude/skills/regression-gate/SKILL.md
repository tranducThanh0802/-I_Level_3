---
name: regression-gate
description: Không cho tụt baseline sau khi đổi luật/chuẩn.
---

# regression-gate

**Phòng:** Chất lượng  ·  **Checkpoint CEO (A4):** Tụt dưới baseline → CHẶN áp thay đổi.

## Các bước
1. Chạy `python3 scripts/run_regression.py`.
2. Tụt → dừng, khắc phục; người duyệt mới nâng baseline.

## Đầu ra / bằng chứng
- Tỷ lệ đạt ≥ baseline.
