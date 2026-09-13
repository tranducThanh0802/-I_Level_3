# Cẩm nang — Rubric đánh giá UI/UX (con Senior UI/UX)

> Nạp theo loại việc: khi review một UI vừa sinh. Do **người** sửa, agent không ghi.
> Nguyên tắc: cái đo được → máy chốt; "đẹp" tổng thể → agent gợi ý, **người duyệt cuối** (ADR-009, ADR-013).
> Output ghi vào `agent-team/reviews/review-<task>.md`, kèm điểm từng phần + vi phạm có bằng chứng + ảnh so sánh.

## A. ĐẸP (thẩm mỹ) — phần lớn đo được; tổng thể do NGƯỜI chốt

**Đo được (agent chấm PASS/FAIL, có bằng chứng):**
- [ ] Tương phản chữ/nền đạt **WCAG AA** (thường 4.5:1; chữ lớn 3:1).
- [ ] Bám **thang spacing** (bội số 4/8pt) — không có padding lẻ tuỳ tiện.
- [ ] **Touch target ≥ 44×44pt** (Apple HIG) cho nút/vùng bấm.
- [ ] **Hệ typography giới hạn** — không quá ~4–5 cỡ chữ; đúng scale team.
- [ ] Canh lề nhất quán (các phần tử thẳng theo grid/lề chung).
- [ ] Bo góc / độ đậm / bóng đổ đồng nhất, không mỗi chỗ một kiểu.

**Chủ quan (agent NÊU nhận xét cụ thể, KHÔNG tự chốt — người quyết):**
- Hierarchy thị giác rõ chưa (mắt biết nhìn đâu trước)?
- Có quá tải / rối / thừa không?
- Cảm giác tinh tế, cân đối, hợp tông thương hiệu?

→ Agent cấm nói chung chung "đẹp/ổn". Phải chỉ **cụ thể**: "khoảng cách tiêu đề–subtitle 6pt phá thang 8pt";
"nút phụ và nút chính cùng độ đậm nên mất phân cấp".

## B. HỢP SPEC — checklist, MÁY chốt

- [ ] Đủ **4 trạng thái**: loading · rỗng · lỗi · mất mạng.
- [ ] Đủ **thành phần** spec yêu cầu (không thiếu, không tự thêm ngoài spec).
- [ ] Đúng **luồng / hành vi** mô tả trong tiêu chí nghiệm thu.
- [ ] Đúng **nội dung/label** (đúng chữ, đúng ngôn ngữ, không placeholder sót).
- [ ] Không đụng nhóm cấm-tự-quyết (đăng nhập, tiền, dữ liệu user... → dừng hỏi).

**FAIL bất kỳ mục nào → trả lại, không qua.**

## C. HỢP UI ĐANG LÀM (nhất quán design system) — MÁY (lint) chốt

- [ ] Dùng **component có sẵn của team**, không dựng lại từ stack thô (VStack/HStack rời).
- [ ] Màu lấy từ **tokens**, không `Color(hex:)` / RGB hardcode.
- [ ] Chữ lấy từ **text style tokens**, không `.font(.system(size:))` số lẻ.
- [ ] Spacing lấy từ **hằng số spacing** của team, không số tuỳ tiện.
- [ ] Icon từ **bộ icon chung** (SF Symbols / asset team), không icon lạ.
- [ ] **So snapshot** với màn cùng loại đang có — phong cách khớp, không lệch tông.

**FAIL → trả lại, không qua.**

## Cách chấm & kết luận

1. Chạy máy kiểm cho B + C và các mục đo-được của A → PASS/FAIL kèm bằng chứng.
2. Nêu nhận xét chủ quan phần A (có dẫn chứng cụ thể).
3. **Verdict:**
   - B hoặc C có FAIL → **trả lại** (máy chốt), liệt kê vi phạm.
   - B + C PASS, A đo-được PASS → **chuyển người duyệt "đẹp"** kèm điểm + nhận xét + ảnh so sánh.
4. Không bao giờ tự đóng dấu "đẹp, xong" — quyền đó của người.

## Chống dấu cao su (như mọi con phản biện)
- Mỗi PASS/FAIL phải kèm bằng chứng (trích rule / dòng spec / tên token vi phạm / ảnh).
- Ghi toàn bộ vào `reviews/`, tra lại được.
