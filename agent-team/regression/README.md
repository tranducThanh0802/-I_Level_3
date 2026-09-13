# Regression — bộ tình huống hồi quy (§4 đề bài, tầng ngoài)

> "Giữ một bộ hai mươi tình huống lấy từ việc thật để chạy lại mỗi lần cẩm nang hay chuẩn thay đổi,
> thấy tệ đi thì chặn. Thử sửa hỏng một dòng cẩm nang, bộ 20 phải bắt được." (đề bài §4)

## Dùng để làm gì
Đây là **lưới an toàn cho chính agent** (không phải test app). Mỗi lần đổi `memory/playbooks/*`
(cẩm nang) hoặc `memory/core-rules.md`/chuẩn code → **chạy lại bộ này** với agent → nếu tỷ lệ đạt
**tụt so với baseline → CHẶN** thay đổi (không cho merge cẩm nang mới).

## Ba đòi hỏi (đề bài §4, tầng ngoài)
1. Chỉ sửa cẩm nang khi một lỗi **đã lặp ≥3 lần** (xem loop ngoài).
2. **Giữ bộ 20 tình huống** lấy từ việc thật, chạy lại mỗi lần cẩm nang/chuẩn đổi, tệ đi thì chặn.
3. Mọi thay đổi cẩm nang **qua người duyệt**.

## Cấu trúc
- `scenarios.jsonl` — bộ tình huống. Mỗi dòng: `{id, category, input, expected, check}`.
  Hiện có **vài mẫu**; **cần góp đủ 20 từ việc thật** khi hệ chạy.
- `baseline.json` — `{pass_rate, date, approved_by}`: mốc đạt đã được người duyệt.
- `results.jsonl` — kết quả lần chạy gần nhất (mỗi dòng `{id, pass, note}`), sinh khi chạy bộ này
  với agent (runtime). `results.EXAMPLE.jsonl` là mẫu.

## Quy trình (chốt cổng)
```
Đổi cẩm nang/chuẩn
      │
      ▼
Chạy 20 tình huống với agent  → ghi regression/results.jsonl
      │
      ▼
python3 scripts/run_regression.py
      │
      ├─ tỷ lệ ĐẠT ≥ baseline → cho phép (người duyệt) → cập nhật baseline
      └─ tỷ lệ TỤT            → CHẶN, in ra tình huống nào hỏng
```

## Một tình huống tốt gồm
- **input**: tình huống thật (spec thiếu gì, crash gì, task chạm nhóm cấm...).
- **expected**: hành vi/kết quả ĐÚNG mà agent phải cho ra.
- **check**: cách kiểm máy đúng/sai (vd: "spec status KHÔNG được lên approved", "phải dừng hỏi").
