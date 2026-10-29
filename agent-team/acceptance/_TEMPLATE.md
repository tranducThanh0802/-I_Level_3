---
feature: <tên feature / task>
spec: <đường dẫn spec — vd specs/<feature>.md>
source_of_truth: <nguồn chân lý gốc — vd file/app/đặc tả để đối chiếu 1:1>
author: <agent/lượt VIẾT — KHÔNG được tự làm reviewer bên dưới>
status: draft
---

# Acceptance — <tên feature>

> Dẫn TỪ spec/nguồn chân lý **TRƯỚC khi code**. Mỗi tiêu chí = 1 dòng, enumerate ĐỦ, không sót.
> "Xong" = MỌI dòng `✅` (có bằng chứng) hoặc `📋` (khai Out of scope) + reviewer độc lập PASS + `acceptance_gate.py` xanh.

## Tiêu chí nghiệm thu  (enumerate ĐỦ — đối chiếu lại spec để không sót)

| # | Tiêu chí (ref spec/nguồn) | Cách kiểm | Bằng chứng | TT |
|---|----------------------------|-----------|------------|----|
| 1 | <vd: XP mỗi câu = 20 (spec §2)> | test | <tên test / lint / ảnh / commit> | ⛔ |

> TT: `✅` đạt + bằng chứng · `📋` khai nợ (bắt buộc có dòng ở Out of scope) · `⛔` chưa.

## Out of scope (khai nợ — mỗi `📋` ở trên phải có 1 dòng lý do ở đây)
- (chưa có)

## Bốn trạng thái (chỉ nếu là màn UI — nếu không, xoá mục này)

| Trạng thái | TT | Bằng chứng |
|---|---|---|
| loading | ⛔ |  |
| rỗng | ⛔ |  |
| lỗi | ⛔ |  |
| mất mạng | ⛔ |  |

## Phản biện độc lập  (BẮT BUỘC — KHÁC author; context mới)
- Reviewer: <ai — phải khác `author`>
- Đã mở spec + nguồn chân lý đối chiếu TỪNG dòng: [ ]
- Ô trống / thiếu bằng chứng / lệch nguồn: <liệt kê, hoặc "không">
- Verdict: FAIL
