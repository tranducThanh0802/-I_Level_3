---
name: port-oracle-tests
description: Tạo bằng chứng cho tiêu chí số/logic bằng cách PORT test từ nguồn chân lý (vd Android) — không tự viết kỳ vọng.
---

# port-oracle-tests

**Phòng:** Chất lượng  ·  **Checkpoint CEO (A4):** Giá trị kỳ vọng COPY từ nguồn chân lý, agent không tự quyết con số.

## Các bước
1. Tìm test nguồn (vd *Test.kt) phủ logic cần.
2. Port sang test đích, copy nguyên input + giá trị kỳ vọng.
3. Chạy; nếu đỏ → logic port sai → sửa code (không sửa kỳ vọng).

## Đầu ra / bằng chứng
- Bộ test oracle xanh = bằng chứng parity logic.
