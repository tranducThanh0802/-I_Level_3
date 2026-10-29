---
name: write-spec
description: Biến ý muốn CEO thành spec máy-làm-được; ĐÁNH DẤU RÕ phần nào AI làm (A1.1).
---

# write-spec

**Phòng:** Sản phẩm  ·  **Checkpoint CEO (A4):** CEO duyệt spec trước khi giao Kỹ thuật.

## Các bước
1. Viết lại QUY TRÌNH làm việc theo bước; mỗi bước đánh dấu [AI] hay [người].
2. Liệt kê TIÊU CHÍ NGHIỆM THU đo được + đủ 4 trạng thái (loading/rỗng/lỗi/mất mạng) nếu là UI.
3. Ghi nguồn chân lý cho mỗi con số/hành vi (không bịa).

## Đầu ra / bằng chứng
- `specs/<feature>.md` có bước [AI]/[người] + tiêu chí nghiệm thu → make-acceptance.
