# Workspace — nơi các agent trao đổi & bàn giao (tầng "việc đang làm")

> Mỗi task một file `<task>.md`. Đây là chỗ chung để các con **giao việc cho nhau**, ghi **đang ở bước
> nào**, và **định tuyến câu hỏi** lên người. Là tầng "việc đang làm" của đề bài §3 → **agent ĐƯỢC ghi**.
>
> Tắt giữa chừng mở lại phải tiếp được từ đây (trạng thái nằm ngoài context — đề bài §4).

## Bản đồ "nơi trao đổi" (đừng lẫn vai)

| Chỗ | Dùng để | Ai ghi |
|---|---|---|
| **workspace/** (file này) | Việc đang làm, **bàn giao giữa các con**, **câu hỏi lên người** | agent |
| **reviews/** | **Phản biện** một sản phẩm + verdict (máy/người chốt) | agent |
| **bugs/** | Tri thức bug chung (fingerprint, cách sửa, được/không) | agent |
| **logs/runs.jsonl** | Nhật ký mọi lần chạy (đo đạc) | agent |
| **memory/core-rules, project-knowledge, playbooks** | Luật & cẩm nang | **người** |

Nguyên tắc: một task chạy → có 1 file workspace (việc đang làm) + có thể sinh nhiều file review (mỗi lần
phản biện). Workspace trỏ tới review & bug liên quan.

## Schema mỗi file workspace

```markdown
---
task: <mã / mô tả ngắn>
flow: feature | bugfix
owner_now: <con đang cầm việc: spec-drafter | soat-spec | dev | test | fixbug | ui-ux | senior-uiux | reviewer>
status: planning | in-progress | waiting-human | waiting-be | blocked | done
pr_status: none | draft | changes-requested | approved | merged   # vòng review PR (playbook pr-review-loop)
review_round: 0                                                    # số vòng review đã qua (chốt chặn: ≤3)
updated: <YYYY-MM-DD HH:mm>
links:
  review: reviews/review-<task>.md
  bug: bugs/bug-<key>.md
---

## Kế hoạch (thứ tự task, cái nào chờ cái nào)
1. [x] ...
2. [ ] ... (chờ #1)

## Bước hiện tại
<đang làm gì, con nào>

## Bàn giao (log giao việc giữa các con)
- [DATE] spec-drafter → soat-spec: nháp spec xong, nhờ soi + đối chiếu BE
- [DATE] soat-spec → PO(người): 2 câu hỏi chặn (xem mục Câu hỏi)
- [DATE] dev → test: tính năng X xong, nhờ viết kịch bản đủ 4 trạng thái
- [DATE] dev → senior-uiux: màn Y xong, nhờ chấm giao diện

## Câu hỏi lên người (mẫu 30 giây — đề bài §5)
- [ ] [CHẶN] <chỗ vướng> · Cách A → hệ quả · Cách B → hệ quả · nghiêng: A vì... · quá hạn sẽ: ...
- [x] [ĐOÁN ĐƯỢC] <ghi giả định, đã chạy tiếp, chờ người xác nhận trong PR>

## Đang chờ (nếu status = waiting-*)
<chờ ai / cái gì; trong lúc chờ đang chạy tiếp phần nào không liên quan>

## Phản hồi review PR (vòng <n>)   # playbook pr-review-loop; agent chỉ ghi dòng "đã sửa"
- [ ] <người: chỗ cần sửa> 
- [x] <người: chỗ cần sửa>  → đã sửa: <agent: sửa gì, máy kiểm xanh chưa>
```

Xem `TASK-EXAMPLE.md`.

## Luật ghi
- Cập nhật `owner_now` + `status` + `updated` mỗi khi đổi tay hoặc đổi bước.
- Câu hỏi lên người phải đủ mẫu 30 giây; kiểu "em không rõ, anh xem giúp" **không nhận**.
- Câu hỏi loại **chặn** → dừng đúng phần đó; loại **đoán được** → ghi giả định, chạy tiếp.
- Con nào giao việc thì ghi một dòng vào "Bàn giao" — để tra được đường đi của task.
