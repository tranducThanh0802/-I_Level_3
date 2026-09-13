# Log mỗi lần chạy

> Đầu vào của mục 6 (đánh giá) và loop ngoài. Không có file này thì không đo được gì.
> Mọi lần chạy đều phải tra lại được tới từng việc.

## Định dạng

Mỗi lần chạy = một dòng JSON append vào `runs.jsonl` (một dòng một run, dễ query & grep).

```json
{
  "run_id": "2026-09-13T10-42-05_fixbug_player-nil-url",
  "agent": "fixbug | dev | test | spec-review",
  "flow": "bugfix | feature",
  "task": "mô tả ngắn việc gì",
  "started_at": "2026-09-13T10:42:05+07:00",
  "ended_at":   "2026-09-13T11:07:31+07:00",
  "wait_external_ms": 0,           // thời gian CHỜ người/PO/BE — đo nhưng để RIÊNG
  "steps": [                       // qua bước nào
    {"step": "tra-bug-cu", "check": "-", "result": "hit:player-nil-url-crash"},
    {"step": "tim-nguyen-nhan", "check": "-", "result": "ok"},
    {"step": "sua+test", "check": "build+test", "result": "green"}
  ],
  "failed_at": null,               // hỏng ở đâu (step name) hoặc null
  "manual_fixes": [                // người sửa tay bao nhiêu + loại (đầu vào loop ngoài)
    {"type": "sai chuẩn | thiếu thông tin đầu vào | hiểu sai yêu cầu | sai logic",
     "detail": "một câu"}
  ],
  "outcome": "used | discarded",   // cuối cùng dùng được hay bỏ
  "pr": "<link PR hoặc null>",
  "handoff": {"code": true, "video": true, "before_after": true}
}
```

## Quy tắc đo (mục 6)

- **Không có log thì không được tính vào phần "đã cắt".**
- `wait_external_ms` **để riêng**, không gộp vào thời gian làm.
- So sánh: cùng loại việc, độ khó tương đương, ≥5 mẫu mỗi bên.
- Dùng **trung vị (median)**, không dùng trung bình — một việc dài bất thường kéo lệch cả bảng.
- Tỷ lệ thành công tròn 100% = đang giấu việc bỏ dở. Việc bỏ giữa chừng phải có (`outcome: discarded`).

## Phép thử (mục 5)

Bốc ngẫu nhiên một việc tuần trước → phải mở `runs.jsonl` xem lại được toàn bộ hành trình.
