---
feature: coupon-checkout (IIP-1234)
status: approved
priority: P1
version: 2
approved_by: PO (người)
updated: 2026-09-13
api: "BE: /api/rpc/checkout/apply-coupon (đọc docs BE, không sửa)"
out_of_scope: "Không làm coupon nhiều lớp / gộp nhiều mã trong lần này"
---

## Mục tiêu
Cho người mua nhập mã giảm giá ở màn thanh toán và thấy giá cập nhật ngay.

## Tiêu chí nghiệm thu (máy kiểm được)
- [x] Nhập mã hợp lệ → tổng tiền giảm đúng số BE trả về, hiện dòng "Đã áp mã".
- [x] Nhập mã sai/hết hạn → hiện lỗi "Mã không hợp lệ/đã hết hạn", tổng tiền không đổi.
- [x] Nút "Áp dụng" bị chặn khi ô mã rỗng.

## Bốn trạng thái (bắt buộc đủ)
- [x] Loading: đang gọi BE kiểm mã → spinner trong nút, khoá nhập.
- [x] Rỗng: chưa nhập mã → ô trống + gợi ý placeholder.
- [x] Lỗi: mã sai/hết hạn hoặc BE lỗi → dòng đỏ dưới ô.
- [x] Mất mạng: hiện "Không có kết nối", nút "Thử lại".

## Ngoài phạm vi (lần này không làm)
- Coupon nhiều lớp, gộp mã.
- Lưu lịch sử mã đã dùng.

## Câu hỏi mở
- (đã đóng) Coupon hết hạn hiện gì? → PO chốt: dòng đỏ "Mã đã hết hạn" (xem workspace/TASK-EXAMPLE.md).

## Changelog
- v1 (2026-09-10): spec-drafter soạn nháp.
- v2 (2026-09-13): PO chốt sau khi trả lời câu hỏi coupon hết hạn → approved.
