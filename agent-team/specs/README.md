# Specs — nơi kiểm soát spec từng feature

> Mỗi feature một file `<feature>.md`. Đây là spec mà **PO người chốt** để Dev làm.
> KHÁC với `docs/original-spec.md` (= "đề bài", yêu cầu cho cả agent team, bất biến).
>
> Ai ghi: spec-drafter soạn nháp; Soát spec soi; **chỉ PO người đổi được `status: approved`**.

## Luật gating (kiểm soát)

Trạng thái đi một chiều, và **Dev CHỈ được bắt đầu khi `status: approved`**:

```
draft ──► reviewing ──► approved ──► building ──► done
 (spec-drafter) (Soát spec)  (PO người)   (Dev)     (đã merge)
```

- Thiếu tiêu chí nghiệm thu, hoặc thiếu ≥3 trong 4 trạng thái → Soát spec **trả lại** (không lên `approved`).
- Spec đổi sau khi `approved` → **tăng `version`** và ghi vào changelog; nếu đổi lớn, quay lại `reviewing`.
- Dev thấy `status != approved` → dừng, không tự đoán (đề bài §1).

## Schema mỗi spec

```markdown
---
feature: <mã / tên feature>
status: draft | reviewing | approved | building | done
version: 1
approved_by: <tên PO người, hoặc null nếu chưa duyệt>
updated: <YYYY-MM-DD>
api: <endpoint/contract dùng; "BE: <link docs>">
out_of_scope: <cái gì lần này KHÔNG làm>
---

## Mục tiêu
<một câu: feature này cho ai, giải quyết gì>

## Tiêu chí nghiệm thu (máy kiểm được — KHÔNG "làm cho đẹp")
- [ ] <điều kiện đo được 1>
- [ ] <điều kiện đo được 2>

## Bốn trạng thái (BẮT BUỘC đủ)
- [ ] Loading: ...
- [ ] Rỗng (empty): ...
- [ ] Lỗi (error): ...
- [ ] Mất mạng (no connection): ...

## Ngoài phạm vi (lần này không làm)
- ...

## Câu hỏi mở (nếu có) → chuyển workspace/ + Discord
- ...

## Changelog
- v1 (DATE): tạo
```

Xem `EXAMPLE.md`.

## Liên kết
- Nháp/soi/hỏi diễn ra ở `workspace/<task>.md` (bàn giao + câu hỏi lên người).
- Khi `approved`, Dev mở task và trỏ ngược về file spec này.
