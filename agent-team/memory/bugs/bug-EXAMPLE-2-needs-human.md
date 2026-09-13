---
id: BUG-2
key: feed-scroll-race
fingerprint: "crash:EXC_BAD_ACCESS:FeedViewModel.appendPage:concurrent"
count: 4
severity: high
source: store
status: needs-arch
assignee:
stuck_reason: "Race condition khi cuộn nhanh: 2 lần appendPage chạy song song. Sửa tại chỗ không hết; cần đổi sang actor/serial queue cho FeedViewModel — đụng kiến trúc, agent DỪNG hỏi."
first_seen: 2026-09-05
last_seen: 2026-09-12
touched_files:
  - Sources/Feed/FeedViewModel.swift
---

## Dấu hiệu
```
EXC_BAD_ACCESS (SIGSEGV) — FeedViewModel.appendPage(_:)
Xảy ra khi cuộn nhanh liên tục lúc trang mới đang tải.
```

## Bước tái hiện
1. Mở Feed, cuộn thật nhanh xuống đáy nhiều lần liên tiếp.
2. Thỉnh thoảng crash (khó tái hiện đều — ~1/10 lần).

## Nguyên nhân gốc (giả thuyết)
Hai tác vụ `appendPage` chạy song song ghi cùng mảng `items` → hỏng bộ nhớ. Cần tuần tự hoá truy cập
(actor hoặc serial queue). Đây là đổi kiến trúc → ngoài quyền tự quyết của agent.

## Các lần thử
- 2026-09-08 cách: thêm `guard !isLoading` → outcome: **không được** (vẫn crash, chỉ giảm tần suất — chữa triệu chứng).

## Vì sao cần người
Đổi FeedViewModel sang actor/serial queue là quyết định kiến trúc, ảnh hưởng nhiều nơi → **người quyết**.
