# Cẩm nang — Retro cuối mỗi feature (theo dõi quá trình để cải thiện agent)

> BẮT BUỘC chạy sau khi làm xong MỖI chức năng (feature/bugfix), trước khi coi là hết việc.
> Mỗi feature là một lần kiểm-thử CHÍNH QUY TRÌNH, không chỉ kiểm-thử code. Do người + agent cùng soát.
> Lý do có luật này: 2 lần retro đầu (ADR-033, ADR-034) lần nào cũng lòi lỗi quy trình nghiêm trọng mà
> lúc làm không thấy — "máy kiểm xanh" che mất lỗi quy trình.

## Checklist retro (5 phút, mỗi feature)

### 1. Đối chiếu quá trình THẬT với đề bài
- Quá trình vừa chạy khác đề bài chỗ nào? Mỗi khác biệt: tốt / xấu / trung tính? (ghi ADR nếu đáng)
- Có bỏ qua bước nào của playbook liên quan không?

### 2. Bốn điểm hay sai (kiểm từng cái)
- [ ] **Phản biện độc lập TRƯỚC khi người duyệt?** (agent context mới/người khác, không phải người viết tự chấm)
- [ ] **Đo `human_minutes`** (thời gian người thật), KHÔNG phải agent wall-clock?
- [ ] **Số liệu gắn nhãn nguồn?** (`baseline_source`, `cost_source` — không bịa, không để 0 giả)
- [ ] **Hạ tầng/playbook liên quan có THỰC SỰ dùng không?** (scan_secrets, work_queue, emit_activity xuyên
      suốt, review.html, bug-memory... — hay lại "có mà không xài")

### 3. Nhóm cấm-tự-quyết có bị chạm không?
- Feature có đụng: quyền, tiền, đăng nhập, dữ liệu user, đổi schema local, thêm thư viện, đổi kiến trúc,
  đổi API contract, sửa config/khoá? → đã DỪNG HỎI người chưa? (đề bài §1)

### 4. Ghi nhận & cải thiện
- Ghi retro vào `DECISIONS.md` (ADR) + cập nhật `STATE.md`.
- Log run với đủ trường: size, human_baseline_min, baseline_source, human_minutes, manual_fixes.
- Lỗi nào LẶP ≥3 lần → đưa vào loop ngoài (`outer_loop.py`) → sửa cẩm nang → chạy bộ 20 hồi quy.
- Lỗi ở KHUÔN MẪU (không phải lần dùng) → sửa ở repo template để project sau không dính lại.

## Thứ tự đúng của một feature (gộp các bài học)
```
xin baseline người → PO-agent research→spec (draft) → Soát spec → Dev + Test (máy kiểm)
  → REVIEWER ĐỘC LẬP (context mới) tìm lỗi → sửa → PO người duyệt → done
  → RETRO (checklist này) → log human_minutes → cải thiện template
```

## Dấu hiệu retro đang bị làm cho-có (đừng)
- "Mọi thứ ổn, không có gì để cải thiện" sau một feature phức tạp → gần như chắc chắn bỏ sót (2/2 lần
  trước đều tưởng ổn rồi lòi lỗi). Retro phải tìm ra ÍT NHẤT một điểm cụ thể để chỉnh hoặc xác nhận-đã-kiểm.
