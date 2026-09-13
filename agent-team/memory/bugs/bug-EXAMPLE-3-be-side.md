---
id: BUG-3
key: profile-avatar-404
fingerprint: "error:ImageLoad:404:ProfileHeader.avatar"
count: 2
severity: medium
source: tester
status: be-side
assignee:
stuck_reason: "Ảnh đại diện trả 404 từ BE với một số user cũ. Client xử lý đúng (hiện ảnh mặc định); lỗi nằm ở dữ liệu BE → đóng gói bằng chứng gửi BE, agent không tự sửa."
first_seen: 2026-09-11
last_seen: 2026-09-13
touched_files: []
---

## Dấu hiệu
```
GET /avatar/{id} -> 404 với user tạo trước 2024. Ảnh không hiện (đã fallback ảnh mặc định).
```

## Bước tái hiện
1. Đăng nhập user cũ (tạo trước 2024).
2. Vào Profile → ảnh đại diện không tải được (client hiện ảnh mặc định — đúng).

## Nguyên nhân gốc
Dữ liệu avatar phía BE thiếu với nhóm user cũ → 404. Không phải lỗi client.

## Vì sao cần người / phía BE
Client đã xử lý đúng trạng thái lỗi. Cần BE bổ sung/di trú dữ liệu avatar → đã gói bằng chứng gửi BE.
