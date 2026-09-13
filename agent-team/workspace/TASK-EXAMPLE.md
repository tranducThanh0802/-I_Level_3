---
task: feature-coupon-checkout (IIP-1234)
flow: feature
owner_now: dev
status: waiting-human
updated: 2026-09-13 15:20
links:
  review: reviews/review-feature-coupon-checkout.md
  bug: null
---

## Kế hoạch (thứ tự task, cái nào chờ cái nào)
1. [x] spec-drafter soạn nháp spec màn "Áp mã giảm giá"
2. [x] PO(người) sửa & chốt spec
3. [x] soat-spec soi + đối chiếu docs BE
4. [ ] dev code màn + đủ 4 trạng thái (đang làm)
5. [ ] senior-uiux chấm giao diện (chờ #4)
6. [ ] test viết kịch bản + chạy + quay video (chờ #4)

## Bước hiện tại
dev đang code trạng thái "lỗi" và "mất mạng" của màn áp coupon.

## Bàn giao (log giao việc giữa các con)
- 2026-09-13 10:05 spec-drafter → PO(người): nháp spec xong, nhờ chốt
- 2026-09-13 11:30 PO(người) → soat-spec: spec đã chốt, nhờ soi
- 2026-09-13 13:10 soat-spec → dev: spec đạt; 1 câu hỏi chặn về mã hết hạn (xem dưới)
- 2026-09-13 15:20 dev → PO(người): câu hỏi chặn về hành vi khi coupon hết hạn

## Câu hỏi lên người (mẫu 30 giây)
- [ ] [CHẶN] Coupon hết hạn thì hiện gì?
  · Cách A: ẩn ô nhập → hệ quả: user không hiểu vì sao
  · Cách B: hiện lỗi "Mã đã hết hạn" đỏ dưới ô → hệ quả: rõ ràng, thêm 1 chuỗi dịch
  · Nghiêng: B, vì hợp trạng thái "lỗi" bắt buộc
  · Quá hạn không trả lời: làm theo B, ghi giả định vào PR
- [x] [ĐOÁN ĐƯỢC] Độ dài tối đa mã coupon: giả định 20 ký tự (đã chạy tiếp, chờ xác nhận trong PR)

## Đang chờ
Chờ PO trả lời câu hỏi coupon hết hạn. Trong lúc chờ, dev vẫn code trạng thái loading & rỗng (không liên quan).
