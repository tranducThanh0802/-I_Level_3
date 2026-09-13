---
task: player-nil-url-crash (fingerprint a1b2c3d4)
flow: bugfix
status: machine-decided
rounds: 2
verdict_by: machine
---

## Giả thuyết (con làm)
Crash `NSInvalidArgumentException / AVPlayerItem nil URL` do `PlayerService.load(url:)` force-unwrap
`streamURL` khi mạng mất giữa lúc fetch. Bằng chứng: `blame_frame` = `PlayerViewModel.play`; trace ngược
thấy `streamURL` về nil ở nhánh mất mạng nhưng nút Play vẫn bật. Nguyên nhân gốc, không phải lỗi AVPlayer.

## Phản biện (con phản biện — nhiệm vụ: bác bỏ)
- [x] Chỗ nghi sai 1: "Có chắc chỉ do mất mạng? BE trả 200 với body rỗng thì sao?" → con làm bổ sung:
      đã Grep, cả hai nhánh đều dẫn tới `streamURL == nil`; fix bao cả hai.
- [x] Trường hợp chưa phủ: trạng thái **mất mạng** và **lỗi** — test phải phủ cả hai. → thêm 2 case.
- [x] Rủi ro bán kính ảnh hưởng: `load(url:)` còn gọi từ `DownloadService` → đổi sang non-optional
      buộc sửa 1 call site nữa; đã kiểm, không phá gì.

## Máy kiểm (bên chốt)
| Tín hiệu | Kết quả |
|---|---|
| build | pass |
| test cũ (full suite) | pass |
| test chống tái phát `test_repro_a1b2c3d4` | fail-trước ✓ / pass-sau ✓ |
| lint --strict | pass |
| so ảnh | advisory (chưa gắn cổng cứng) |

## Kết luận
- **verdict: máy chốt — được.** Test tái phát fail trên base, pass sau fix; full suite xanh; lint sạch.
- Không cần leo lên người. Sang bước mở PR (code + video + ảnh trước/sau).
- Ghi vào bug DB: outcome = **được**, cách sửa = chặn Play khi URL nil + hiện trạng thái lỗi/mất mạng +
  đổi `load(url:)` non-optional.
