# Cẩm nang — Vòng phản hồi review PR (người ↔ agent)

> Nạp khi agent đã mở PR nháp và chờ người duyệt. Do người sửa, agent không ghi (trừ mục "đã sửa").
> Lấp lỗ hổng: trước đây agent mở PR rồi DỪNG; đây là vòng người-chê → agent-sửa → duyệt/merge.

## Trạng thái PR (ghi ở `workspace/<task>.md` frontmatter: `pr_status`)
```
draft ──► changes-requested ──► approved ──► merged
 (agent mở)   (người chê)        (người OK)   (NGƯỜI merge — agent KHÔNG merge)
```

## Vòng lặp
```
1. Agent mở PR nháp (code + video + ảnh trước/sau) → pr_status: draft → báo Discord phòng hỏi-người.
2. NGƯỜI review → ghi feedback dạng checklist vào mục "## Phản hồi review PR" (workspace).
   - Không có gì sửa → pr_status: approved → NGƯỜI merge → pr_status: merged.
   - Có sửa → pr_status: changes-requested (mỗi ý là 1 dòng - [ ]).
3. Agent đọc từng ý → sửa code → chạy lại MÁY KIỂM (build/test/lint) → đánh dấu - [x] + ghi 1 dòng "đã sửa: ...".
   Ý nào KHÔNG đồng ý/cần làm rõ → hỏi lại theo mẫu 30s, KHÔNG tự bỏ qua.
4. Quay lại bước 2 (người review lại).
```

## Chốt chặn (chống lặp vô hạn — như mọi loop)
- **Tối đa 3 vòng** review. Quá 3 vòng vẫn chưa xong → DỪNG, leo lên người: "cần pair/người tiếp quản".
- 2 vòng liền feedback y hệt → dừng (đang xoay tại chỗ).

## Mẫu mục trong `workspace/<task>.md`
```markdown
## Phản hồi review PR  (vòng <n>)
- [ ] <người: chỗ cần sửa 1>
- [x] <người: chỗ cần sửa 2>   → đã sửa: <agent: sửa gì, máy kiểm xanh chưa>
```

## Rào
- **Agent KHÔNG merge, KHÔNG đẩy store** — chỉ người (đề bài §5, ADR-004). Kể cả khi approved.
- Mỗi lần agent "đã sửa" phải kèm **máy kiểm xanh**, không chỉ nói suông (đề bài §4).
- Feedback chủ quan ("nhìn chưa đẹp") → người quyết; đo được (test đỏ, lint) → máy chốt.

## Discord
- pr_status = draft / approved-cần-merge → báo **phòng hỏi-người** (cần bạn hành động).
- pr_status = changes-requested → báo **phòng agent** (agent cần sửa).
