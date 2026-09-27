# Cẩm nang — Độ phủ test theo tiêu chí nghiệm thu

> Sinh ra từ **loop ngoài** (ADR-035): lỗi loại "thiếu test" lặp 3 lần (forecast → hourly → multi-city),
> lần nào reviewer độc lập cũng bắt "test xanh nhưng lọt tiêu chí spec / bug logic". Đây là luật chặn.
> Do người sửa; mọi thay đổi qua bộ 20 tình huống hồi quy.

## Luật (áp cho con Dev + con Test, TRƯỚC khi đưa reviewer)

1. **Mỗi tiêu chí nghiệm thu trong spec phải có ≥1 test map tới.** Không có test = chưa đạt, dù build xanh.
2. **Ghi bảng "tiêu chí ↔ test"** trong PR/review: liệt kê từng tiêu chí spec và tên test tương ứng.
   Tiêu chí nào chưa có test → đánh dấu THIẾU, không đưa reviewer.
3. **Mỗi trạng thái bắt buộc (loading/rỗng/lỗi/mất mạng) phải có test riêng** ở tầng logic (không gộp).
4. **Bug đã biết → có test tái hiện** (fail-trước/pass-sau) trước khi coi là sửa xong.
5. **Reviewer độc lập KIỂM bảng map này** — không chỉ chạy `swift test` thấy xanh là thôi. "Test xanh"
   KHÔNG chứng minh "đủ tiêu chí" (đã 3 lần test xanh mà lọt bug/tiêu chí).

## Vì sao (bằng chứng thật)
- forecast: reviewer bắt thiếu test cho "rỗng / mảng lệch / mất mạng không cache".
- hourly: reviewer bắt 3 tiêu chí spec thiếu test.
- multi-city: test xanh nhưng che BUG-4 (thêm sai thành phố) vì mock chỉ trả 1 kết quả.

## Anti-pattern (đừng)
- Viết test đi qua happy-path rồi tuyên bố "đủ" — reviewer sẽ bắt.
- Mock quá hiền (chỉ 1 kết quả, không edge) khiến test không chạm nhánh lỗi.
- Tin "build/test xanh = xong". Xanh là điều kiện CẦN, không ĐỦ.
