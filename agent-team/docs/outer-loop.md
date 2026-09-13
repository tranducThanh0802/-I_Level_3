# Loop ngoài (tầng 3) — thứ khiến tháng sau khác tháng này

> §4 đề bài: "Hai tầng đầu chỉ giúp làm xong việc. Tầng ngoài mới là thứ khiến tháng sau khác tháng này...
> đa số người dừng ở hai tầng đầu rồi thắc mắc sao mấy tháng vẫn phải sửa tay đúng mấy lỗi cũ."

## Một vòng loop ngoài

```
(1) Gom lần sửa tay từ logs         →  scripts/outer_loop.py
        │   (đọc manual_fixes trong logs/runs.jsonl)
        ▼
(2) Lỗi nào lặp ≥3 lần?             →  ngưỡng THRESHOLD=3
        │   (1–2 lần = ngoại lệ, KHÔNG nhét vào cẩm nang → tránh phình & mâu thuẫn)
        ▼
(3) Đề xuất sửa cẩm nang            →  agent-team/outer-loop-proposals.md (CHỈ đề xuất)
        │
        ▼
(4) NGƯỜI duyệt + sửa cẩm nang      →  memory/playbooks/* hoặc project-knowledge.md (agent KHÔNG tự sửa)
        │
        ▼
(5) Chạy bộ hồi quy                 →  scripts/run_regression.py
        │
        ├─ TỤT baseline → CHẶN (giữ cẩm nang cũ, sửa lại)
        └─ không tụt   → áp thay đổi → cập nhật baseline (người duyệt)
```

Không có điểm thoát — chạy định kỳ (đề bài: "chạy định kỳ, không có điểm thoát").

## Ba đòi hỏi riêng của tầng ngoài (đề bài §4)
1. **Chỉ sửa cẩm nang khi một lỗi đã lặp ≥3 lần.** (outer_loop.py, THRESHOLD=3)
2. **Giữ bộ tình huống hồi quy**, chạy lại mỗi lần cẩm nang/chuẩn đổi, tệ đi thì chặn. (regression/ + run_regression.py)
3. **Mọi thay đổi cẩm nang qua người duyệt.** (agent chỉ ghi được workspace + bugs; cẩm nang do người sửa — ADR-002)

## Công cụ
| Bước | Lệnh |
|---|---|
| Gom sửa tay → đề xuất | `python3 scripts/outer_loop.py` |
| Cổng hồi quy (sau khi sửa cẩm nang) | `python3 scripts/run_regression.py` |
| Xem số tổng thể | `python3 scripts/build_report.py` → report.html |

## Nhịp chạy gợi ý
- Hằng tuần: `build_report.py` (xem số) + `outer_loop.py` (có lỗi nào chạm ngưỡng chưa).
- Khi có đề xuất chạm ngưỡng: người duyệt → sửa cẩm nang → `run_regression.py` → cập nhật baseline.

## Vì sao quan trọng
Đây là vòng biến "sửa tay lặp lại" thành "cẩm nang tốt hơn" — nếu bỏ, vài tháng sau vẫn sửa tay đúng
mấy lỗi cũ. Nhưng nó cũng nguy hiểm nhất (dễ làm cẩm nang phình/mâu thuẫn), nên có đủ 3 rào ở trên.
