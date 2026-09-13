# Reviews — nơi phản biện có cấu trúc (blackboard)

> Mỗi task một file `review-<task>.md`. Người + agent cùng đọc/ghi. Đây là "nơi chung" để các con
> trao đổi & phản biện — nhưng theo cấu trúc, KHÔNG phải chat cãi tự do. Xem ADR-009.
>
> Đây là working-state → **agent ĐƯỢC ghi** vào đây (cùng với bug DB).

## Luật của cuộc phản biện

1. **Con làm** nêu giả thuyết + bằng chứng (không nêu bằng chứng thì không tính).
2. **Con phản biện** (context mới, nhiệm vụ = **bác bỏ**) chỉ ra chỗ sai / rủi ro / trường hợp chưa phủ.
3. **Máy kiểm chốt.** Kết luận đúng/sai luôn do build/test/lint/so ảnh quyết — KHÔNG phải hai con đồng ý.
   Đồng thuận ≠ đúng.
4. **Máy không kiểm được** (nguyên nhân gốc hợp lý không, UI/animation/cảm giác) → đóng gói **2 phương án
   + hệ quả**, gửi **người** quyết (mẫu câu hỏi 30 giây — đề bài §5).
5. **Chốt chặn:** tối đa 2–3 vòng. Hết thì dừng, leo lên người. Không cãi vô hạn.

## Schema mỗi file review

```markdown
---
task: <mô tả ngắn / fingerprint bug / mã task>
flow: bugfix | feature
status: debating | machine-decided | escalated-to-human | resolved
rounds: <số vòng đã cãi>
verdict_by: machine | human | null
---

## Giả thuyết (con làm)
<khẳng định + bằng chứng: log, trace, call site, diff>

## Phản biện (con phản biện — nhiệm vụ: bác bỏ)
- [ ] Chỗ nghi sai 1: <...>
- [ ] Trường hợp chưa phủ: <...> (nhớ 4 trạng thái: loading/rỗng/lỗi/mất mạng)
- [ ] Rủi ro bán kính ảnh hưởng: <call site khác?>

## Máy kiểm (bên chốt)
| Tín hiệu | Kết quả |
|---|---|
| build | pass/fail |
| test cũ (full suite) | pass/fail |
| test chống tái phát | fail-trước / pass-sau |
| lint --strict | pass/fail |
| so ảnh (nếu có) | pass/fail/advisory |

## Kết luận
- verdict: <máy chốt / leo lên người>
- Nếu leo người: 2 phương án + hệ quả + nghiêng về đâu + nếu quá hạn sẽ làm gì.
```

Xem `review-EXAMPLE.md`.
