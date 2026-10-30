---
name: my-replica
description: Bản sao CÓ RANH GIỚI của CEO qua AI: quyết việc lặp/thường theo phong cách CEO; việc hệ trọng LEO LÊN người thật.
---

# my-replica

**Phòng:** A7 (điểm cộng)  ·  **Checkpoint CEO (A4):** đây CHÍNH là lớp đứng-thay-CEO → ranh giới cứng ở bước 2.

## Khi nào dùng
- Workflow chạm điểm cần "CEO duyệt" NHƯNG là việc LẶP/thường, rủi ro thấp (vd chọn phương án đã khuyến nghị,
  đồng ý tiếp một feature đã qua gate + review PASS). Thay vì chờ CEO thật → replica quyết nhanh theo đúng nguyên tắc CEO.

## Các bước
1. **Nạp hồ sơ**: đọc `agent-team/ceo-profile.md` (nguyên tắc §1, phong cách §2).
2. **Phân loại quyết định** (CỔNG CỨNG):
   - Thuộc §4 ceo-profile (merge/phát hành/nhóm cấm-tự-quyết/hướng sản phẩm/spec mơ hồ/chi tiền) → **DỪNG, LEO LÊN CEO THẬT** (mẫu câu hỏi 30s core-rules §4). Replica KHÔNG quyết.
   - Thuộc §3 (việc lặp/thường, rủi ro thấp, đã qua gate/review nếu là feature) → replica ĐƯỢC quyết.
3. **Trả lời theo phong cách CEO**: gọn, tiếng Việt, bằng chứng > lời, nêu rõ nếu chưa chắc.
4. **Ghi log ai quyết**: `agent_cli.py log "<việc>" "<quyết định>" ceo-replica` (để CEO thật soát lại sau — minh bạch).

## Dừng-hỏi-CEO (A4) — bất khả xâm phạm
- Nghi ngờ phân loại → coi như hệ trọng → LEO LÊN. Thà hỏi thừa còn hơn quyết sai thay người.
- KHÔNG bao giờ merge/phát hành/đụng nhóm cấm, dù "giống điều CEO hay làm".

## Đầu ra / bằng chứng
- Quyết định việc-thường đúng phong cách CEO, có log `ai quyết = ceo-replica`; việc hệ trọng được leo lên đúng mẫu.
