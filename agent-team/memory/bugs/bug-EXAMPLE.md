---
id: BUG-1
key: player-nil-url-crash
fingerprint: "crash:NSInvalidArgumentException:AVPlayerItem.init:PlayerViewModel.play"
count: 3
severity: crash
source: store
status: fixed
first_seen: 2026-08-20
last_seen: 2026-09-10
touched_files:
  - Sources/Player/PlayerViewModel.swift
  - Sources/Player/PlayerService.swift
---

## Dấu hiệu
```
*** Terminating app due to uncaught exception 'NSInvalidArgumentException',
reason: '*** -[AVPlayerItem initWithURL:] nil URL'
PlayerViewModel.play() -> PlayerService.load(url:)
```

## Bước tái hiện
1. Mở màn Player khi mạng vừa mất giữa lúc fetch stream URL.
2. `streamURL` về nil nhưng UI vẫn cho bấm Play.
3. Bấm Play → crash.

## Nguyên nhân gốc
`PlayerService.load(url:)` nhận `URL?` và force-unwrap. URL nil xảy ra ở trạng thái
"mất mạng" — một trong bốn trạng thái spec bắt buộc phủ nhưng luồng cũ bỏ sót.
KHÔNG phải lỗi AVPlayer; đó chỉ là triệu chứng.

## Các lần thử
- 2026-08-21 cách: thêm `guard url != nil` ngay tại AVPlayer init, nuốt lỗi im lặng → outcome: **không được** — hết crash nhưng nút Play vẫn bật, user tưởng hỏng app. Chữa triệu chứng.
- 2026-08-28 cách: chặn nút Play khi `streamURL == nil` + hiện trạng thái lỗi/mất mạng, `load(url:)` đổi sang nhận `URL` non-optional → outcome: **được**.

## Test chống tái phát
`PlayerViewModelTests.test_play_disabled_when_streamURL_nil` — bảo đảm không gọi được
`play()` khi URL nil, và state chuyển sang `.error(.noConnection)`.
