# Cẩm nang — Ý tưởng → Spec (PO-agent research & soạn tài liệu)

> Nạp khi PO đưa một **ý tưởng thô** cần biến thành spec. Do người sửa, agent không ghi.
> Mở rộng vai PO-agent (ADR-010/011). Rào: agent ĐỀ XUẤT, người QUYẾT; research có NGUỒN.

## Đầu vào / Đầu ra
- **Vào:** một ý tưởng 1–2 câu (vd: "làm màn thống kê thói quen theo tuần").
- **Ra:** `specs/<feature>.md` (status: **draft**) + câu hỏi mở (nếu có) vào `workspace/` + báo Discord.
  KHÔNG tự đặt `approved` — đó là quyền PO người.

## Các bước

### 1. Làm rõ (trước khi research)
- Nếu ý tưởng mơ hồ ở chỗ **chặn** (đối tượng dùng, mục tiêu, phạm vi) → hỏi 2–3 câu theo **mẫu 30s**
  (chỗ vướng · 2 cách + hệ quả · nghiêng đâu · quá hạn làm gì). Ghi vào `workspace/<feature>.md`.
- Chỗ **đoán được** → ghi **giả định** vào spec, chạy tiếp.
- **Cấm** tự quyết phạm vi sản phẩm (sáng tạo chức năng là của PO người).

### 2. Research (có nguồn)
- Quét: đối thủ/tính năng tương tự · kỳ vọng người dùng · khả thi kỹ thuật iOS · ràng buộc (offline? cần BE?).
- Công cụ: WebSearch / skill `deep-research`. **Mọi khẳng định phải kèm nguồn** (URL). Không bịa số/tính năng.
- Rút ra: nên có gì (must), nên tránh gì, rủi ro, và các **quyết định cần PO** (đưa vào "câu hỏi mở").

### 3. Sinh spec draft → `specs/<feature>.md`
Điền đủ khung của `specs/README.md`, đặc biệt:
- **Tiêu chí nghiệm thu ĐO ĐƯỢC** (không "làm cho đẹp").
- **Đủ 4 trạng thái** loading/rỗng/lỗi/mất mạng.
- **Ngoài phạm vi** (cái gì lần này không làm).
- **API/local** (nếu không BE thì "local-only").
- Thêm mục **## Căn cứ / Research** liệt kê nguồn + tóm tắt phát hiện.
- Mục **## Câu hỏi mở** cho các quyết định cần PO.
- `status: draft`, `version: 1`, `approved_by: null`.

### 4. Bàn giao
- Chuyển **Soát spec** soi độc lập (đối chiếu tiêu chí + 4 trạng thái + docs BE nếu có).
- **PO người** đọc, sửa, chốt → `status: approved`. Chỉ khi đó Dev mới bắt đầu.

## Ví dụ đúng / sai
- ✅ "Đối thủ X, Y có tính năng streak; kỳ vọng chung là nhắc nhở hằng ngày [nguồn]. Đề xuất must: biểu đồ
  tuần + streak. Câu hỏi PO: có làm nhắc nhở push lần này không?" → nêu nguồn + để PO quyết.
- ❌ "Chắc chắn người dùng muốn gamification, làm luôn huy hiệu + bảng xếp hạng" → tự quyết phạm vi, không nguồn.

## Chống lỗi thường gặp
- Không có nguồn cho một claim → đánh dấu "giả định, cần PO xác nhận", không ghi như sự thật.
- Ý tưởng quá mơ hồ → dừng ở bước 1 hỏi, đừng nhảy sang viết spec đầy đủ (spec mơ hồ = càng chạy càng lệch).
