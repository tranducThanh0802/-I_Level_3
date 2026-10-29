---
name: orchestrate
description: WORKFLOW CHÍNH (A1): nhận 1 đầu việc → route qua Sản phẩm→Kỹ thuật→QA→CEO duyệt theo đúng thứ tự.
---

# orchestrate

**Phòng:** Vận hành  ·  **Checkpoint CEO (A4):** Dừng ở mỗi checkpoint [CEO duyệt]; không chạy thẳng qua điểm người phải quyết.

## Các bước
1. Lấy việc từ work-queue.
2. Chạy chuỗi: research-idea→write-spec→review-spec→[CEO]→make-acceptance→implement→gate→independent-review→[CEO]→run-log→outer-loop.
3. Mỗi bước ghi trạng thái; gặp lỗi → báo NGAY + nêu hành động.

## Đầu ra / bằng chứng
- Đầu việc đi trọn luồng, có điểm dừng thật, log đầy đủ.
